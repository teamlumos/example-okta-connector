from enum import Enum

from connector.generated import EntitlementType, ResourceType


class OktaResourceTypes(str, Enum):
    GLOBAL_RESOURCE = "GLOBAL_RESOURCE"

class OktaEntitlementTypes(str, Enum):
    GLOBAL_ROLE = "ROLE"

resource_types: list[ResourceType] = [
    ResourceType(
        type_id=OktaResourceTypes.GLOBAL_RESOURCE,
        type_label="Global Resource",
    )
]

entitlement_types: list[EntitlementType] = [
    EntitlementType(
        type_id=OktaEntitlementTypes.GLOBAL_ROLE,
        type_label="Role",
        resource_type_id="",
        min=0,
        # You can also set a max, if users can't have infinite of these entitlements
        # max=1,
    )
]
class OktaEndpoint(str, Enum):
    # https://developer.okta.com/docs/api/openapi/okta-management/management/tag/User/#tag/User/operation/listUsers
    USERS = "/api/v1/users"
    # https://developer.okta.com/docs/api/openapi/okta-management/management/tag/User/#tag/User/operation/getUser
    USER = "/api/v1/users/{user_id}"
    # https://developer.okta.com/docs/api/openapi/okta-management/management/tag/UserLifecycle/#tag/UserLifecycle/operation/suspendUser
    SUSPEND_USER = "/api/v1/users/{user_id}/lifecycle/suspend"
    # https://developer.okta.com/docs/api/openapi/okta-management/management/tag/UserLifecycle/#tag/UserLifecycle/operation/activateUser
    ACTIVATE_USER = "/api/v1/users/{user_id}/lifecycle/activate"
    # https://developer.okta.com/docs/api/openapi/okta-management/management/tag/UserLifecycle/#tag/UserLifecycle/operation/unsuspendUser
    UNSUSPEND_USER = "/api/v1/users/{user_id}/lifecycle/unsuspend"