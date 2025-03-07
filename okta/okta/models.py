from enum import Enum
from pydantic import BaseModel
from okta.enums import OktaEntitlementTypes
from connector.generated import FoundAccountData, AccountStatus, AccountType, FoundEntitlementAssociation, FoundEntitlementData


class PaginatedOktaResponse(BaseModel):
    # must be derived from the links headers in the response
    after: str | None = None

class UserStatus(Enum):
    STAGED = "STAGED"
    PROVISIONED = "PROVISIONED"
    ACTIVE = "ACTIVE"
    DEPROVISIONED = "DEPROVISIONED"
    RECOVERY = "RECOVERY"
    SUSPENDED = "SUSPENDED"
    LOCKED_OUT= "LOCKED_OUT"
    PASSWORD_EXPIRED = "PASSWORD_EXPIRED"
    
class Profile(BaseModel):
    firstName: str
    lastName: str
    email: str
    login: str
    mobilePhone: str | None

class User(BaseModel):
    id: str
    status: str
    created: str
    activated: str | None
    statusChanged: str | None
    lastLogin: str | None
    lastUpdated: str
    passwordChanged: str | None
    profile: Profile

    def to_account_data(self) -> FoundAccountData:
        if self.status in [UserStatus.STAGED, UserStatus.PROVISIONED]:
            user_status = AccountStatus.PENDING
        elif self.status in [UserStatus.DEPROVISIONED]:
            user_status = AccountStatus.DEPROVISIONED
        elif self.status in [UserStatus.RECOVERY, UserStatus.PASSWORD_EXPIRED]:
            user_status = AccountStatus.PENDING
        elif self.status in [UserStatus.SUSPENDED, UserStatus.LOCKED_OUT]:
            user_status = AccountStatus.SUSPENDED
        else:
            user_status = AccountStatus.ACTIVE

        return FoundAccountData(
            account_type=AccountType.USER,
            email=self.profile.email,
            integration_specific_id=self.id,
            given_name=self.profile.firstName,
            family_name=self.profile.lastName,
            user_status=user_status,
            username=self.profile.login,
        )

class UsersResponse(PaginatedOktaResponse):
    root: list[User]

    def to_accounts(self) -> list[FoundAccountData]:
        return [user.to_account_data() for user in self.root]
    

class UserRole(BaseModel):
    id: str
    label: str
    type: str
    status: str
    created: str
    lastUpdated: str
    assignmentType: str

class UserRolesResponse(BaseModel):
    root: list[UserRole]

    def to_found_entitlement_associations(self, user_id: str) -> list[FoundEntitlementAssociation]:
        return [FoundEntitlementAssociation(
            account_id=user_id,
            integration_specific_entitlement_id=role.id,
            integration_specific_resource_id="",
        ) for role in self.root]
    
    def to_found_entitlement_data(self) -> list[FoundEntitlementData]:
        return [FoundEntitlementData(
            entitlement_type=OktaEntitlementTypes.GLOBAL_ROLE,
            integration_specific_id=role.id,
            integration_specific_resource_id="",
            label=role.label,
        ) for role in self.root]
    