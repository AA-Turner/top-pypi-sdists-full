from enum import Enum

from connector.generated import EntitlementType, ResourceType


class {pascal}ResourceTypes(str, Enum):
    # The global resource is implicit
    pass


class {pascal}EntitlementTypes(str, Enum):
    ROLE = "ROLE"


resource_types: list[ResourceType] = []

entitlement_types: list[EntitlementType] = [
    EntitlementType(
        type_id={pascal}EntitlementTypes.ROLE,
        type_label="Role",
        resource_type_id="",  # means that this entitlement is associated with the global resource
        min=0,
        # You can also set a max, if users can't have infinite of these entitlements
        # max=1,
    )
]
