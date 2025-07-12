from typing import Dict
from typing import Optional

from google.protobuf.timestamp_pb2 import Timestamp

from tecton._internals import metadata_service
from tecton_proto.servergroupservice.server_group_service__client_pb2 import AutoscalingConfig
from tecton_proto.servergroupservice.server_group_service__client_pb2 import CreateFeatureServerCacheRequest
from tecton_proto.servergroupservice.server_group_service__client_pb2 import CreateFeatureServerGroupRequest
from tecton_proto.servergroupservice.server_group_service__client_pb2 import CreateIngestServerGroupRequest
from tecton_proto.servergroupservice.server_group_service__client_pb2 import CreateTransformServerGroupRequest
from tecton_proto.servergroupservice.server_group_service__client_pb2 import DeleteFeatureServerCacheRequest
from tecton_proto.servergroupservice.server_group_service__client_pb2 import DeleteFeatureServerGroupRequest
from tecton_proto.servergroupservice.server_group_service__client_pb2 import DeleteIngestServerGroupRequest
from tecton_proto.servergroupservice.server_group_service__client_pb2 import DeleteTransformServerGroupRequest
from tecton_proto.servergroupservice.server_group_service__client_pb2 import FeatureServerCache
from tecton_proto.servergroupservice.server_group_service__client_pb2 import FeatureServerGroup
from tecton_proto.servergroupservice.server_group_service__client_pb2 import GetFeatureServerCacheRequest
from tecton_proto.servergroupservice.server_group_service__client_pb2 import GetFeatureServerGroupRequest
from tecton_proto.servergroupservice.server_group_service__client_pb2 import GetIngestServerGroupRequest
from tecton_proto.servergroupservice.server_group_service__client_pb2 import GetRealtimeLogsRequest
from tecton_proto.servergroupservice.server_group_service__client_pb2 import GetRealtimeLogsResponse
from tecton_proto.servergroupservice.server_group_service__client_pb2 import GetTransformServerGroupRequest
from tecton_proto.servergroupservice.server_group_service__client_pb2 import IngestServerGroup
from tecton_proto.servergroupservice.server_group_service__client_pb2 import ListFeatureServerCachesRequest
from tecton_proto.servergroupservice.server_group_service__client_pb2 import ListFeatureServerCachesResponse
from tecton_proto.servergroupservice.server_group_service__client_pb2 import ListFeatureServerGroupsRequest
from tecton_proto.servergroupservice.server_group_service__client_pb2 import ListFeatureServerGroupsResponse
from tecton_proto.servergroupservice.server_group_service__client_pb2 import ListIngestServerGroupsRequest
from tecton_proto.servergroupservice.server_group_service__client_pb2 import ListIngestServerGroupsResponse
from tecton_proto.servergroupservice.server_group_service__client_pb2 import ListTransformServerGroupsRequest
from tecton_proto.servergroupservice.server_group_service__client_pb2 import ListTransformServerGroupsResponse
from tecton_proto.servergroupservice.server_group_service__client_pb2 import ProvisionedScalingCacheConfig
from tecton_proto.servergroupservice.server_group_service__client_pb2 import ProvisionedScalingConfig
from tecton_proto.servergroupservice.server_group_service__client_pb2 import ResourceMetadata
from tecton_proto.servergroupservice.server_group_service__client_pb2 import TransformServerGroup
from tecton_proto.servergroupservice.server_group_service__client_pb2 import UpdateFeatureServerCacheRequest
from tecton_proto.servergroupservice.server_group_service__client_pb2 import UpdateFeatureServerGroupRequest
from tecton_proto.servergroupservice.server_group_service__client_pb2 import UpdateIngestServerGroupRequest
from tecton_proto.servergroupservice.server_group_service__client_pb2 import UpdateTransformServerGroupRequest


# ============================================================================
# FeatureServerCache Operations
# ============================================================================


def create_feature_server_cache(
    workspace: str,
    name: str,
    num_shards: int,
    num_replicas_per_shard: int,
    preferred_maintenance_window: Optional[str] = None,
    description: Optional[str] = None,
    tags: Optional[Dict[str, str]] = None,
) -> FeatureServerCache:
    """
    Create a new FeatureServerCache in the specified workspace.

    Args:
        workspace: The workspace where the cache will be created
        name: Name of the cache
        num_shards: Number of shards for the cache
        num_replicas_per_shard: Number of replicas per shard
        preferred_maintenance_window: Optional AWS maintenance window (format: "ddd:hh24:mi-ddd:hh24:mi")
        description: Optional description for the cache
        tags: Optional tags to apply to the cache

    Returns:
        The created FeatureServerCache object
    """
    provisioned_scaling = ProvisionedScalingCacheConfig(
        num_shards=num_shards, num_replicas_per_shard=num_replicas_per_shard
    )
    metadata = None
    if description or tags:
        metadata = ResourceMetadata(description=description, tags=tags or {})

    request = CreateFeatureServerCacheRequest(
        workspace=workspace,
        name=name,
        provisioned_config=provisioned_scaling,
        preferred_maintenance_window=preferred_maintenance_window,
        metadata=metadata,
    )

    return metadata_service.instance().CreateFeatureServerCache(request)


def get_feature_server_cache(id: str) -> FeatureServerCache:
    """
    Get a FeatureServerCache by ID.

    Args:
        id: ID of the cache

    Returns:
        The FeatureServerCache object
    """
    request = GetFeatureServerCacheRequest(id=id)
    return metadata_service.instance().GetFeatureServerCache(request)


def update_feature_server_cache(
    id: str,
    num_shards: Optional[int] = None,
    num_replicas_per_shard: Optional[int] = None,
    preferred_maintenance_window: Optional[str] = None,
    description: Optional[str] = None,
    tags: Optional[Dict[str, str]] = None,
) -> FeatureServerCache:
    """
    Update an existing FeatureServerCache.

    Args:
        id: ID of the cache
        num_shards: Updated number of shards
        num_replicas_per_shard: Updated number of replicas per shard
        preferred_maintenance_window: Updated maintenance window
        description: Updated description
        tags: Updated tags

    Returns:
        The updated FeatureServerCache object
    """
    provisioned_scaling = None
    if num_shards is not None or num_replicas_per_shard is not None:
        provisioned_scaling = ProvisionedScalingCacheConfig()
        if num_shards is not None:
            provisioned_scaling.num_shards = num_shards
        if num_replicas_per_shard is not None:
            provisioned_scaling.num_replicas_per_shard = num_replicas_per_shard

    metadata = None
    if description is not None or tags is not None:
        metadata = ResourceMetadata()
        if description is not None:
            metadata.description = description
        if tags is not None:
            metadata.tags.update(tags)

    request = UpdateFeatureServerCacheRequest(
        id=id,
        provisioned_config=provisioned_scaling,
        preferred_maintenance_window=preferred_maintenance_window,
        metadata=metadata,
    )

    return metadata_service.instance().UpdateFeatureServerCache(request)


def delete_feature_server_cache(id: str) -> None:
    """
    Delete a FeatureServerCache.

    Args:
        id: ID of the cache
    """
    request = DeleteFeatureServerCacheRequest(id=id)
    metadata_service.instance().DeleteFeatureServerCache(request)


def list_feature_server_caches(workspace: Optional[str] = None) -> ListFeatureServerCachesResponse:
    """
    List FeatureServerCaches, optionally filtered by workspace.

    Args:
        workspace: Optional workspace to filter caches

    Returns:
        Response containing list of FeatureServerCache objects
    """
    request = ListFeatureServerCachesRequest(workspace=workspace)
    return metadata_service.instance().ListFeatureServerCaches(request)


# ============================================================================
# FeatureServerGroup Operations
# ============================================================================


def create_feature_server_group(
    workspace: str,
    name: str,
    min_nodes: Optional[int] = None,
    max_nodes: Optional[int] = None,
    desired_nodes: Optional[int] = None,
    node_type: Optional[str] = None,
    cache_id: Optional[str] = None,
    description: Optional[str] = None,
    tags: Optional[Dict[str, str]] = None,
) -> FeatureServerGroup:
    """
    Create a new FeatureServerGroup in the specified workspace.

    Args:
        workspace: The workspace where the server group will be created
        name: Name of the server group
        min_nodes: Minimum number of nodes for autoscaling
        max_nodes: Maximum number of nodes for autoscaling
        desired_nodes: Fixed number of nodes for provisioned scaling
        node_type: Optional EC2 instance type
        cache_id: Optional ID of the cache to associate with the server group
        description: Optional description for the server group
        tags: Optional tags to apply to the server group

    Returns:
        The created FeatureServerGroup object
    """
    autoscaling = None
    provisioned_scaling = None

    if min_nodes is not None and max_nodes is not None:
        autoscaling = AutoscalingConfig(min_nodes=min_nodes, max_nodes=max_nodes)
    if desired_nodes is not None:
        provisioned_scaling = ProvisionedScalingConfig(desired_nodes=desired_nodes)

    metadata = None
    if description or tags:
        metadata = ResourceMetadata(description=description, tags=tags or {})

    request = CreateFeatureServerGroupRequest(
        workspace=workspace,
        name=name,
        autoscaling_config=autoscaling,
        provisioned_config=provisioned_scaling,
        node_type=node_type,
        cache_id=cache_id,
        metadata=metadata,
    )

    return metadata_service.instance().CreateFeatureServerGroup(request)


def get_feature_server_group(id: str) -> FeatureServerGroup:
    """
    Get a FeatureServerGroup by ID.

    Args:
        id: ID of the server group

    Returns:
        The FeatureServerGroup object
    """
    request = GetFeatureServerGroupRequest(id=id)
    return metadata_service.instance().GetFeatureServerGroup(request)


def update_feature_server_group(
    id: str,
    min_nodes: Optional[int] = None,
    max_nodes: Optional[int] = None,
    desired_nodes: Optional[int] = None,
    node_type: Optional[str] = None,
    cache_id: Optional[str] = None,
    description: Optional[str] = None,
    tags: Optional[Dict[str, str]] = None,
) -> FeatureServerGroup:
    """
    Update an existing FeatureServerGroup.

    Args:
        id: ID of the server group
        min_nodes: Updated minimum nodes for autoscaling
        max_nodes: Updated maximum nodes for autoscaling
        desired_nodes: Updated desired nodes for provisioned scaling
        node_type: Updated EC2 instance type
        cache_id: Updated cache ID
        description: Updated description
        tags: Updated tags

    Returns:
        The updated FeatureServerGroup object
    """
    autoscaling = None
    provisioned_scaling = None

    if min_nodes is not None and max_nodes is not None:
        autoscaling = AutoscalingConfig(min_nodes=min_nodes, max_nodes=max_nodes)
    elif desired_nodes is not None:
        provisioned_scaling = ProvisionedScalingConfig(desired_nodes=desired_nodes)

    metadata = None
    if description is not None or tags is not None:
        metadata = ResourceMetadata()
        if description is not None:
            metadata.description = description
        if tags is not None:
            metadata.tags.update(tags)

    request = UpdateFeatureServerGroupRequest(
        id=id,
        autoscaling_config=autoscaling,
        provisioned_config=provisioned_scaling,
        node_type=node_type,
        cache_id=cache_id,
        metadata=metadata,
    )

    return metadata_service.instance().UpdateFeatureServerGroup(request)


def delete_feature_server_group(id: str) -> None:
    """
    Delete a FeatureServerGroup.

    Args:
        id: ID of the server group
    """
    request = DeleteFeatureServerGroupRequest(id=id)
    metadata_service.instance().DeleteFeatureServerGroup(request)


def list_feature_server_groups(workspace: Optional[str] = None) -> ListFeatureServerGroupsResponse:
    """
    List FeatureServerGroups, optionally filtered by workspace.

    Args:
        workspace: Optional workspace to filter server groups

    Returns:
        Response containing list of FeatureServerGroup objects
    """
    request = ListFeatureServerGroupsRequest(workspace=workspace)
    return metadata_service.instance().ListFeatureServerGroups(request)


# ============================================================================
# IngestServerGroup Operations
# ============================================================================


def create_ingest_server_group(
    workspace: str,
    name: str,
    min_nodes: Optional[int] = None,
    max_nodes: Optional[int] = None,
    desired_nodes: Optional[int] = None,
    node_type: Optional[str] = None,
    description: Optional[str] = None,
    tags: Optional[Dict[str, str]] = None,
) -> IngestServerGroup:
    """
    Create a new IngestServerGroup in the specified workspace.

    Args:
        workspace: The workspace where the server group will be created
        name: Name of the server group
        min_nodes: Minimum number of nodes for autoscaling
        max_nodes: Maximum number of nodes for autoscaling
        desired_nodes: Fixed number of nodes for provisioned scaling
        node_type: Optional EC2 instance type
        description: Optional description for the server group
        tags: Optional tags to apply to the server group

    Returns:
        The created IngestServerGroup object
    """
    autoscaling = None
    provisioned_scaling = None

    if min_nodes is not None and max_nodes is not None:
        autoscaling = AutoscalingConfig(min_nodes=min_nodes, max_nodes=max_nodes)
    if desired_nodes is not None:
        provisioned_scaling = ProvisionedScalingConfig(desired_nodes=desired_nodes)

    metadata = None
    if description or tags:
        metadata = ResourceMetadata(description=description, tags=tags or {})

    request = CreateIngestServerGroupRequest(
        workspace=workspace,
        name=name,
        autoscaling_config=autoscaling,
        provisioned_config=provisioned_scaling,
        node_type=node_type,
        metadata=metadata,
    )

    return metadata_service.instance().CreateIngestServerGroup(request)


def get_ingest_server_group(id: str) -> IngestServerGroup:
    """
    Get an IngestServerGroup by ID.

    Args:
        id: ID of the server group

    Returns:
        The IngestServerGroup object
    """
    request = GetIngestServerGroupRequest(id=id)
    return metadata_service.instance().GetIngestServerGroup(request)


def update_ingest_server_group(
    id: str,
    min_nodes: Optional[int] = None,
    max_nodes: Optional[int] = None,
    desired_nodes: Optional[int] = None,
    node_type: Optional[str] = None,
    description: Optional[str] = None,
    tags: Optional[Dict[str, str]] = None,
) -> IngestServerGroup:
    """
    Update an existing IngestServerGroup.

    Args:
        id: ID of the server group
        min_nodes: Updated minimum nodes for autoscaling
        max_nodes: Updated maximum nodes for autoscaling
        desired_nodes: Updated desired nodes for provisioned scaling
        node_type: Updated EC2 instance type
        description: Updated description
        tags: Updated tags

    Returns:
        The updated IngestServerGroup object
    """
    autoscaling = None
    provisioned_scaling = None

    if min_nodes is not None and max_nodes is not None:
        autoscaling = AutoscalingConfig(min_nodes=min_nodes, max_nodes=max_nodes)
    elif desired_nodes is not None:
        provisioned_scaling = ProvisionedScalingConfig(desired_nodes=desired_nodes)

    metadata = None
    if description is not None or tags is not None:
        metadata = ResourceMetadata()
        if description is not None:
            metadata.description = description
        if tags is not None:
            metadata.tags.update(tags)

    request = UpdateIngestServerGroupRequest(
        id=id,
        autoscaling_config=autoscaling,
        provisioned_config=provisioned_scaling,
        node_type=node_type,
        metadata=metadata,
    )

    return metadata_service.instance().UpdateIngestServerGroup(request)


def delete_ingest_server_group(id: str) -> None:
    """
    Delete an IngestServerGroup.

    Args:
        id: ID of the server group
    """
    request = DeleteIngestServerGroupRequest(id=id)
    metadata_service.instance().DeleteIngestServerGroup(request)


def list_ingest_server_groups(workspace: Optional[str] = None) -> ListIngestServerGroupsResponse:
    """
    List IngestServerGroups, optionally filtered by workspace.

    Args:
        workspace: Optional workspace to filter server groups

    Returns:
        Response containing list of IngestServerGroup objects
    """
    request = ListIngestServerGroupsRequest(workspace=workspace)
    return metadata_service.instance().ListIngestServerGroups(request)


# ============================================================================
# TransformServerGroup Operations
# ============================================================================


def create_transform_server_group(
    workspace: str,
    name: str,
    environment: str,
    environment_variables: Optional[Dict[str, str]] = None,
    min_nodes: Optional[int] = None,
    max_nodes: Optional[int] = None,
    desired_nodes: Optional[int] = None,
    node_type: Optional[str] = None,
    description: Optional[str] = None,
    tags: Optional[Dict[str, str]] = None,
) -> TransformServerGroup:
    """
    Create a new TransformServerGroup in the specified workspace.

    Args:
        workspace: The workspace where the server group will be created
        name: Name of the server group
        environment: Name of the Python environment to use
        environment_variables: Optional environment variables
        min_nodes: Minimum number of nodes for autoscaling
        max_nodes: Maximum number of nodes for autoscaling
        desired_nodes: Fixed number of nodes for provisioned scaling
        node_type: Optional EC2 instance type
        description: Optional description for the server group
        tags: Optional tags to apply to the server group

    Returns:
        The created TransformServerGroup object
    """
    autoscaling = None
    provisioned_scaling = None

    if min_nodes is not None and max_nodes is not None:
        autoscaling = AutoscalingConfig(min_nodes=min_nodes, max_nodes=max_nodes)
    if desired_nodes is not None:
        provisioned_scaling = ProvisionedScalingConfig(desired_nodes=desired_nodes)

    metadata = None
    if description or tags:
        metadata = ResourceMetadata(description=description, tags=tags or {})

    request = CreateTransformServerGroupRequest(
        workspace=workspace,
        name=name,
        metadata=metadata,
        autoscaling_config=autoscaling,
        provisioned_config=provisioned_scaling,
        node_type=node_type,
        environment=environment,
        environment_variables=environment_variables,
    )
    return metadata_service.instance().CreateTransformServerGroup(request)


def get_transform_server_group(id: str) -> TransformServerGroup:
    """
    Get a TransformServerGroup by ID.

    Args:
        id: ID of the server group

    Returns:
        The TransformServerGroup object
    """
    request = GetTransformServerGroupRequest(id=id)
    return metadata_service.instance().GetTransformServerGroup(request)


def update_transform_server_group(
    id: str,
    environment: Optional[str] = None,
    environment_variables: Optional[Dict[str, str]] = None,
    min_nodes: Optional[int] = None,
    max_nodes: Optional[int] = None,
    desired_nodes: Optional[int] = None,
    node_type: Optional[str] = None,
    description: Optional[str] = None,
    tags: Optional[Dict[str, str]] = None,
) -> TransformServerGroup:
    """
    Update an existing TransformServerGroup.

    Args:
        id: ID of the server group
        environment: Updated Python environment name
        environment_variables: Updated environment variables
        min_nodes: Updated minimum nodes for autoscaling
        max_nodes: Updated maximum nodes for autoscaling
        desired_nodes: Updated desired nodes for provisioned scaling
        node_type: Updated EC2 instance type
        description: Updated description
        tags: Updated tags

    Returns:
        The updated TransformServerGroup object
    """
    autoscaling = None
    provisioned_scaling = None

    if min_nodes is not None and max_nodes is not None:
        autoscaling = AutoscalingConfig(min_nodes=min_nodes, max_nodes=max_nodes)
    elif desired_nodes is not None:
        provisioned_scaling = ProvisionedScalingConfig(desired_nodes=desired_nodes)

    metadata = None
    if description is not None or tags is not None:
        metadata = ResourceMetadata()
        if description is not None:
            metadata.description = description
        if tags is not None:
            metadata.tags.update(tags)

    request = UpdateTransformServerGroupRequest(
        id=id,
        autoscaling_config=autoscaling,
        provisioned_config=provisioned_scaling,
        node_type=node_type,
        environment=environment,
        environment_variables=environment_variables,
        metadata=metadata,
    )
    return metadata_service.instance().UpdateTransformServerGroup(request)


def delete_transform_server_group(id: str) -> None:
    """
    Delete a TransformServerGroup.

    Args:
        id: ID of the server group
    """
    request = DeleteTransformServerGroupRequest(id=id)
    metadata_service.instance().DeleteTransformServerGroup(request)


def list_transform_server_groups(workspace: Optional[str] = None) -> ListTransformServerGroupsResponse:
    """
    List TransformServerGroups, optionally filtered by workspace.

    Args:
        workspace: Optional workspace to filter server groups

    Returns:
        Response containing list of TransformServerGroup objects
    """
    request = ListTransformServerGroupsRequest(workspace=workspace)
    return metadata_service.instance().ListTransformServerGroups(request)


def get_realtime_logs(
    id: str, start: Optional[str] = None, end: Optional[str] = None, tail: Optional[int] = None
) -> GetRealtimeLogsResponse:
    """
    Get realtime logs for a TransformServerGroup.

    Args:
        id: ID of the transform server group
        start: Start timestamp
        end: End timestamp
        tail: Number of logs to return

    Returns:
        The realtime logs
    """
    req = GetRealtimeLogsRequest(transform_server_group_id=id)
    if tail:
        req.tail_log_count = tail
    if start:
        start_timestamp = Timestamp()
        start_timestamp.FromJsonString(start)
        req.start.CopyFrom(start_timestamp)
    if end:
        end_timestamp = Timestamp()
        end_timestamp.FromJsonString(end)
        req.end.CopyFrom(end_timestamp)
    return metadata_service.instance().GetRealtimeLogs(req)
