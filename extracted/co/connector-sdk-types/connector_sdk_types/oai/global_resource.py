from connector_sdk_types.generated import Resource, ResourceType

GLOBAL_RESOURCE_TYPE = ResourceType(type_id="GLOBAL_RESOURCE", type_label="Global Resource")

GLOBAL_RESOURCE = Resource(
    id="",
    label="Global Resource",
    description="Global Resource representing the integration tenant",
    resource_type=GLOBAL_RESOURCE_TYPE.type_id,
)
