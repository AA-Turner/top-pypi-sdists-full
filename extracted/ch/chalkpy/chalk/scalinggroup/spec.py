from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime, timezone
from typing import Any, Optional, Sequence


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


@dataclass(frozen=True)
class CronScalingWindow:
    """A recurring window during which a scaling group keeps a minimum replica count.

    Parameters
    ----------
    start
        Cron expression for when the window opens (e.g. "0 8 * * 1-5").
    end
        Cron expression for when the window closes (e.g. "0 18 * * 1-5").
    desired_replicas
        Replica floor while the window is open. Must not exceed ``max_replicas``;
        0 allows scale-to-zero.
    """

    start: str
    end: str
    desired_replicas: int


@dataclass(frozen=True)
class CronScalingSchedule:
    """Time-of-day replica floors for a scaling group.

    Parameters
    ----------
    timezone
        IANA timezone the cron expressions are evaluated in (e.g. "America/New_York").
    windows
        The windows; outside every window the usual autoscaling applies.
    """

    timezone: str
    windows: Sequence[CronScalingWindow] = ()


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
    queue_depth_target
        Scale on queued ``.defer()`` calls, targeting this many pending calls per
        replica. The server fills in which queue to watch.
    gpu_utilization_target
        Scale to hold this average GPU utilization percentage (1-100) per replica.
        Requires ``min_replicas >= 1``.
    cron
        Time-of-day replica floors.
    shutdown_delay_seconds
        Graceful termination period for a replica (server default: 30).
    window_seconds
        Time window over which scaling triggers are evaluated (server default: 60).
    """

    min_replicas: int = 1
    max_replicas: int = 1
    target_cpu_utilization_percentage: Optional[int] = None
    queue_depth_target: Optional[int] = None
    gpu_utilization_target: Optional[int] = None
    cron: Optional[CronScalingSchedule] = None
    shutdown_delay_seconds: Optional[int] = None
    window_seconds: Optional[int] = None


@dataclass
class GrpcReadinessProbe:
    """gRPC readiness probe configuration for a scaling group container.

    Model deployments only support gRPC readiness checks.

    Parameters
    ----------
    service
        gRPC health-check service name to probe. Leave unset (or empty) to
        check overall server health.
    period_seconds
        How often, in seconds, to perform the probe.
    timeout_seconds
        Number of seconds after which the probe times out.
    failure_threshold
        Number of consecutive failures required to mark the container as not
        ready.
    """

    service: Optional[str] = None
    period_seconds: Optional[int] = None
    timeout_seconds: Optional[int] = None
    failure_threshold: Optional[int] = None


@dataclass
class GrpcStartupProbe:
    """gRPC startup probe configuration for a scaling group container.

    Model deployments only support gRPC startup checks.

    Parameters
    ----------
    method
        Fully qualified gRPC method to call (e.g. "/grpc.health.v1.Health/Check").
        If omitted, defaults to the standard gRPC health check method.
    """

    method: Optional[str] = None


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


def auto_scaling_spec_to_proto(spec: AutoScalingSpec) -> Any:
    """Convert to a ``ScalingSpec`` proto. Unset options are omitted, so the server applies its defaults."""
    from chalk._gen.chalk.scalinggroup.v1 import service_pb2 as sg_pb

    pb = sg_pb.ScalingSpec(
        min_replicas=spec.min_replicas,
        max_replicas=spec.max_replicas,
        target_cpu_utilization_percentage=spec.target_cpu_utilization_percentage,
        shutdown_delay_seconds=spec.shutdown_delay_seconds,
        window_seconds=spec.window_seconds,
    )
    if spec.queue_depth_target is not None:
        pb.function_queue_depth_trigger.target_queue_depth = spec.queue_depth_target
    if spec.gpu_utilization_target is not None:
        pb.gpu_utilization_trigger.target_utilization_percentage = spec.gpu_utilization_target
    if spec.cron is not None:
        pb.cron_scaling_trigger.CopyFrom(
            sg_pb.CronScalingTrigger(
                timezone=spec.cron.timezone,
                windows=[
                    sg_pb.CronScalingWindow(start=w.start, end=w.end, desired_replicas=w.desired_replicas)
                    for w in spec.cron.windows
                ],
            )
        )
    return pb


def auto_scaling_spec_from_proto(pb: Any) -> AutoScalingSpec:
    """Convert a ``ScalingSpec`` proto."""

    def optional(name: str) -> Optional[int]:
        return getattr(pb, name) if pb.HasField(name) else None

    cron = None
    if pb.HasField("cron_scaling_trigger"):
        cron = CronScalingSchedule(
            timezone=pb.cron_scaling_trigger.timezone,
            windows=tuple(
                CronScalingWindow(start=w.start, end=w.end, desired_replicas=w.desired_replicas)
                for w in pb.cron_scaling_trigger.windows
            ),
        )
    return AutoScalingSpec(
        min_replicas=pb.min_replicas,
        max_replicas=pb.max_replicas,
        target_cpu_utilization_percentage=optional("target_cpu_utilization_percentage"),
        queue_depth_target=(
            pb.function_queue_depth_trigger.target_queue_depth if pb.HasField("function_queue_depth_trigger") else None
        ),
        gpu_utilization_target=(
            pb.gpu_utilization_trigger.target_utilization_percentage if pb.HasField("gpu_utilization_trigger") else None
        ),
        cron=cron,
        shutdown_delay_seconds=optional("shutdown_delay_seconds"),
        window_seconds=optional("window_seconds"),
    )


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
