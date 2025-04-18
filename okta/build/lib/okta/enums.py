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
