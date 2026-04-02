from connector_sdk_types.generated import AccessGraphResource, ResourceType

ACCESS_GRAPH_GLOBAL_RESOURCE_TYPE = ResourceType(
    type_id="ACCESS_GRAPH_GLOBAL_RESOURCE", type_label="Access Graph Global Resource"
)

ACCESS_GRAPH_GLOBAL_RESOURCE = AccessGraphResource(
    id="",
    label="Access Graph Global Resource",
    description="Access Graph Global Resource representing the integration tenant",
    resource_type=ACCESS_GRAPH_GLOBAL_RESOURCE_TYPE.type_id,
)
