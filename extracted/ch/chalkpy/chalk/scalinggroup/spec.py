from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime, timezone
from typing import Any, Optional


@dataclass
class ScalingGroupResourceRequest:
    """Resource requests for a scaling group container.

    Parameters
    ----------
    cpu
        CPU limit (e.g. "2", "500m").
    memory
        Memory limit (e.g. "4Gi", "512Mi").
    gpu
        GPU spec as "type:count" (e.g. "nvidia-tesla-t4:1").
    """

    cpu: Optional[str] = None
    memory: Optional[str] = None
    gpu: Optional[str] = None


@dataclass
class AutoScalingSpec:
    """Autoscaling configuration for a scaling group.

    Parameters
    ----------
    min_replicas
        Minimum number of replicas for autoscaling.
    max_replicas
        Maximum number of replicas for autoscaling.
    target_cpu_utilization_percentage
        Target CPU utilization for autoscaling.
    """

    min_replicas: int = 1
    max_replicas: int = 1
    target_cpu_utilization_percentage: Optional[int] = None


@dataclass
class ResourceLimits:
    """Resource limits for a container.

    Parameters
    ----------
    cpu
        CPU limit (e.g. "2", "500m").
    memory
        Memory limit (e.g. "4Gi", "512Mi").
    gpu
        GPU spec as "type:count" (e.g. "nvidia-tesla-t4:1").
    """

    cpu: Optional[str] = None
    memory: Optional[str] = None
    gpu: Optional[str] = None


@dataclass
class ContainerSpec:
    """Container specification for a scaling group.

    Parameters
    ----------
    name
        Name of the container.
    image
        Container image URL.
    entrypoint
        Container entrypoint command.
    port
        Port number the container listens on.
    resources
        Resource limits for the container.
    envVars
        Environment variables.
    protocol
        Protocol (e.g. "grpc", "http").
    routing
        Routing type (e.g. "private", "public").
    """

    name: Optional[str] = None
    image: Optional[str] = None
    entrypoint: Optional[list[str]] = None
    port: Optional[int] = None
    resources: Optional[ResourceLimits] = None
    envVars: Optional[dict[str, str]] = None
    protocol: Optional[str] = None
    routing: Optional[str] = None


@dataclass
class ScalingSpecResponse:
    """Scaling specification from a scaling group response.

    Parameters
    ----------
    minReplicas
        Minimum number of replicas.
    maxReplicas
        Maximum number of replicas.
    targetCpuUtilizationPercentage
        Target CPU utilization percentage (optional).
    shutdownDelaySeconds
        Shutdown delay in seconds (optional).
    """

    minReplicas: Optional[int] = None
    maxReplicas: Optional[int] = None
    targetCpuUtilizationPercentage: Optional[int] = None
    shutdownDelaySeconds: Optional[int] = None


@dataclass
class ScalingGroupSpec:
    """Specification of a scaling group.

    Parameters
    ----------
    containerSpec
        Container specification.
    scalingSpec
        Scaling specification.
    """

    containerSpec: Optional[ContainerSpec] = None
    scalingSpec: Optional[ScalingSpecResponse] = None


@dataclass
class ScalingGroup:
    """A scaling group response.

    Parameters
    ----------
    id
        Unique identifier of the scaling group.
    name
        Name of the scaling group.
    status
        Current status of the scaling group.
    statusMessage
        Status message if applicable.
    spec
        Specification of the scaling group.
    createdAt
        Timestamp when the scaling group was created.
    deletedAt
        Timestamp when the scaling group was deleted (if applicable).
    webUrl
        Web URL for accessing the scaling group.
    readyReplicas
        Number of ready replicas.
    availableReplicas
        Number of available replicas.
    """

    id: Optional[str] = None
    name: Optional[str] = None
    status: Optional[str] = None
    statusMessage: Optional[str] = None
    spec: Optional[ScalingGroupSpec] = None
    createdAt: Optional[str] = None
    deletedAt: Optional[str] = None
    webUrl: Optional[str] = None
    readyReplicas: Optional[int] = None
    availableReplicas: Optional[int] = None


@dataclass
class ListScalingGroupsResponse:
    """Response containing a list of scaling groups.

    Parameters
    ----------
    scalingGroups
        List of scaling groups.
    """

    scalingGroups: list[ScalingGroup]


@dataclass
class DeleteScalingGroupResponse:
    """Response from deleting a scaling group.

    Parameters
    ----------
    scalingGroup
        The deleted scaling group.
    """

    scalingGroup: Optional[ScalingGroup] = None


def proto_to_scaling_group(pb: Any) -> ScalingGroup:
    """Convert a proto ScalingGroupResponse to a ScalingGroup dataclass.

    Parameters
    ----------
    pb
        Proto ScalingGroupResponse message.

    Returns
    -------
    ScalingGroup
        Converted scaling group dataclass.
    """
    spec = None
    if pb.spec:
        container_spec = None
        if pb.spec.container_spec:
            resources = None
            if pb.spec.container_spec.resources:
                resources = ResourceLimits(
                    cpu=pb.spec.container_spec.resources.cpu,
                    memory=pb.spec.container_spec.resources.memory,
                    gpu=pb.spec.container_spec.resources.gpu,
                )
            container_spec = ContainerSpec(
                name=pb.spec.container_spec.name,
                image=pb.spec.container_spec.image,
                entrypoint=list(pb.spec.container_spec.entrypoint),
                port=pb.spec.container_spec.port,
                resources=resources,
                envVars=dict(pb.spec.container_spec.env_vars),
                protocol=pb.spec.container_spec.protocol,
                routing=pb.spec.container_spec.routing,
            )
        scaling_spec = None
        if pb.spec.scaling_spec:
            scaling_spec = ScalingSpecResponse(
                minReplicas=pb.spec.scaling_spec.min_replicas,
                maxReplicas=pb.spec.scaling_spec.max_replicas,
                targetCpuUtilizationPercentage=pb.spec.scaling_spec.target_cpu_utilization_percentage,
                shutdownDelaySeconds=pb.spec.scaling_spec.shutdown_delay_seconds,
            )
        spec = ScalingGroupSpec(containerSpec=container_spec, scalingSpec=scaling_spec)

    # Convert protobuf Timestamps to ISO format strings
    created_at = None
    if pb.created_at and pb.created_at.seconds:
        created_at = datetime.fromtimestamp(
            pb.created_at.seconds + pb.created_at.nanos / 1e9, tz=timezone.utc
        ).isoformat()

    deleted_at = None
    if pb.deleted_at and pb.deleted_at.seconds:
        deleted_at = datetime.fromtimestamp(
            pb.deleted_at.seconds + pb.deleted_at.nanos / 1e9, tz=timezone.utc
        ).isoformat()

    return ScalingGroup(
        id=pb.id,
        name=pb.name,
        status=pb.status,
        statusMessage=pb.status_message,
        spec=spec,
        createdAt=created_at,
        deletedAt=deleted_at,
        webUrl=pb.web_url,
        readyReplicas=pb.ready_replicas,
        availableReplicas=pb.available_replicas,
    )
