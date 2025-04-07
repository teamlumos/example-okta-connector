from enum import Enum

from connector.generated import EntitlementType, FoundEntitlementData, ResourceType


class SharepointResourceTypes(str, Enum):
    SITE = "SITE"
    GROUP = "GROUP"


class SharepointGroupRole(str, Enum):
    OWNER = "owner"
    MEMBER = "member"


class SharepointEntitlementTypes(str, Enum):
    USER_PERMISSION = "USER_PERMISSION"
    GROUP_MEMBERSHIP = "GROUP_MEMBERSHIP"


class SharepointEndpoint(str, Enum):
    TENANT = "/tenantRelationships/findTenantInformationByTenantId(tenantId='{tenant_id}')"
    USERS = "/users"
    USER = "/users/{user_id}"
    USER_INVITE = "/invitations"
    GROUPS = "/groups"
    GROUP_OWNERS = "/groups/{group_id}/owners"
    GROUP_MEMBERS = "/groups/{group_id}/members"
    SITES = "/sites"
    SITE_PERMISSIONS = "/sites/{site_id}/permissions"
    SITE_PERMISSION = "/sites/{site_id}/permissions/{permission_id}"
    PERMANENT_DELETE = "/directory/deletedItems/{id}"


class SharepointSitePersmissions(str, Enum):
    READ = "read"
    WRITE = "write"
    OWNER = "owner"

    @classmethod
    def to_entitlements(cls) -> list[FoundEntitlementData]:
        return [
            FoundEntitlementData(
                entitlement_type=SharepointEntitlementTypes.USER_PERMISSION,
                integration_specific_id=permission,
                integration_specific_resource_id="",
                label=permission.title(),
                is_assignable=True,
            )
            for permission in list(cls)
        ]


resource_types: list[ResourceType] = [
    ResourceType(
        type_id=SharepointResourceTypes.SITE,
        type_label="Site",
    ),
    ResourceType(
        type_id=SharepointResourceTypes.GROUP,
        type_label="Group",
    ),
]

entitlement_types: list[EntitlementType] = [
    EntitlementType(
        type_id=SharepointEntitlementTypes.USER_PERMISSION,
        type_label="User Permission",
        resource_type_id=SharepointResourceTypes.SITE,
        min=0,
    ),
    EntitlementType(
        type_id=SharepointEntitlementTypes.GROUP_MEMBERSHIP,
        type_label="Group Membership",
        resource_type_id=SharepointResourceTypes.GROUP,
        min=0,
        max=2,
    ),
]
