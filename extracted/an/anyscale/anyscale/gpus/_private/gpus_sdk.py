from datetime import datetime, timezone
from typing import Any, Optional

from anyscale._private.sdk.base_sdk import BaseSDK
from anyscale.client.openapi_client.models import (
    GpuDetail,
    GpuMetadata,
    GpuTelemetry as ApiGpuTelemetry,
    GpuWorkloadRef,
    GpuXid as ApiGpuXid,
    NodeGpusResponse,
)
from anyscale.gpus.models import (
    Gpu,
    GpuPlacement,
    GpuState,
    GpuTelemetry,
    GpuWorkload,
    GpuXid,
    NodeGpus,
)


class PrivateGpusSDK(BaseSDK):
    def node_gpus(
        self,
        cluster_id: str,
        node_id: str,
        *,
        time: Optional[datetime] = None,
    ) -> NodeGpus:
        """Every GPU on `node_id` of `cluster_id` at `time` (now when None)."""
        raw = self.client.get_node_gpus(cluster_id=cluster_id, node_id=node_id, time=_epoch(time))
        return _to_node_gpus(raw)

    def get(self, cluster_id: str, gpu_uuid: str, *, time: Optional[datetime] = None) -> Gpu:
        """One GPU of `cluster_id` by UUID at `time` (now when None)."""
        raw = self.client.get_gpu(cluster_id=cluster_id, gpu_uuid=gpu_uuid, time=_epoch(time))
        return _to_gpu(raw)


def _epoch(value: Optional[datetime]) -> Optional[float]:
    if value is None:
        return None
    # A naive datetime is taken as UTC, matching the CLI's time flags.
    aware = value if value.tzinfo else value.replace(tzinfo=timezone.utc)
    return aware.timestamp()


def _from_epoch(value: Optional[Any]) -> Optional[datetime]:
    return None if value is None else datetime.fromtimestamp(float(value), tz=timezone.utc)


def _to_node_gpus(raw: NodeGpusResponse) -> NodeGpus:
    return NodeGpus(
        cluster_id=raw.cluster_id,
        node_id=raw.node_id,
        gpu_count=raw.gpu_count,
        gpus=[_to_telemetry(gpu) for gpu in raw.gpus or []],
        time=datetime.fromtimestamp(raw.time, tz=timezone.utc),
        instance_id=raw.instance_id,
        instance_type=raw.instance_type,
        hostname=raw.hostname,
        node_ip=raw.node_ip,
    )


def _to_gpu(raw: GpuDetail) -> Gpu:
    return Gpu(
        gpu_uuid=raw.gpu_uuid,
        placement=_to_placement(raw.metadata),
        telemetry=_to_telemetry(raw.telemetry),
        time=datetime.fromtimestamp(raw.time, tz=timezone.utc),
    )


def _to_placement(raw: GpuMetadata) -> GpuPlacement:
    return GpuPlacement(
        gpu_index=raw.gpu_index,
        cloud_id=raw.cloud_id,
        cluster_id=raw.cluster_id,
        gpu_model=raw.gpu_model,
        pci_bus_id=raw.pci_bus_id,
        driver_version=raw.driver_version,
        node_id=raw.node_id,
        instance_id=raw.instance_id,
        instance_type=raw.instance_type,
        hostname=raw.hostname,
        node_ip=raw.node_ip,
        workload=_to_workload(raw.workload),
    )


def _to_telemetry(raw: ApiGpuTelemetry) -> GpuTelemetry:
    return GpuTelemetry(
        gpu_index=raw.gpu_index,
        uuid=raw.uuid,
        # The wire value is lowercase (allocated, ...); the model's enum is uppercase.
        state=GpuState.validate(str(raw.state)),
        gpu_model=raw.gpu_model,
        pci_bus_id=raw.pci_bus_id,
        driver_version=raw.driver_version,
        last_reported_at=_from_epoch(raw.last_reported_at),
        utilization_pct=raw.utilization_pct,
        utilization_source=_enum_value(raw.utilization_source),
        fb_used_mib=raw.fb_used_mib,
        fb_free_mib=raw.fb_free_mib,
        fb_total_mib=raw.fb_total_mib,
        gpu_temp_c=raw.gpu_temp_c,
        memory_temp_c=raw.memory_temp_c,
        power_usage_w=raw.power_usage_w,
        power_source=_enum_value(raw.power_source),
        power_limit_w=raw.power_limit_w,
        sm_clock_mhz=raw.sm_clock_mhz,
        mem_clock_mhz=raw.mem_clock_mhz,
        ecc_sbe_total=raw.ecc_sbe_total,
        ecc_dbe_total=raw.ecc_dbe_total,
        ecc_sbe_aggregate_total=raw.ecc_sbe_aggregate_total,
        ecc_dbe_aggregate_total=raw.ecc_dbe_aggregate_total,
        correctable_remapped_rows=raw.correctable_remapped_rows,
        uncorrectable_remapped_rows=raw.uncorrectable_remapped_rows,
        nvlink_replay_count=raw.nvlink_replay_count,
        xids=[_to_xid(xid) for xid in raw.xids or []],
        workload=_to_workload(raw.workload),
    )


def _to_xid(raw: ApiGpuXid) -> GpuXid:
    return GpuXid(
        code=raw.code,
        message=raw.message,
        critical=bool(raw.critical),
        active=bool(raw.active),
    )


def _to_workload(raw: Optional[GpuWorkloadRef]) -> Optional[GpuWorkload]:
    if raw is None:
        return None
    return GpuWorkload(
        type=raw.type,
        id=raw.id,
        name=raw.name,
        job_attempt_id=raw.job_attempt_id,
    )


def _enum_value(raw: Optional[Any]) -> Optional[str]:
    # The generated client hands enum fields back as plain strings; an Enum, should the
    # generator ever change, carries the same text in `.value`.
    if raw is None:
        return None
    return str(getattr(raw, "value", raw))
