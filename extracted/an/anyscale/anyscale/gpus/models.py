"""Models for `anyscale node gpus`, `anyscale gpu get` and `anyscale.gpus.*`.

Every value comes from the DCGM exporter on the node, read through the control plane.
A GPU that stopped reporting still appears, as OFFLINE with its last-known telemetry,
for as long as the backend looks back (the cluster's lifetime, capped at seven days).
"""

from dataclasses import dataclass, field
from datetime import datetime
from typing import ClassVar, Dict, List, Optional

from anyscale._private.models import ModelBase, ModelEnum


class GpuState(ModelEnum):
    """What a GPU is doing, derived from its DCGM telemetry."""

    ALLOCATED = "ALLOCATED"
    IDLE = "IDLE"
    UNHEALTHY = "UNHEALTHY"
    OFFLINE = "OFFLINE"

    __docstrings__: ClassVar[Dict[str, str]] = {
        ALLOCATED: "A workload holds the GPU.",
        IDLE: "The GPU reports telemetry and no workload holds it.",
        UNHEALTHY: "The GPU reports an active critical XID error.",
        OFFLINE: "The GPU stopped reporting more than five minutes before the snapshot "
        "time: its node is terminated, dead or not exporting. Telemetry is the last known.",
    }


@dataclass(frozen=True)
class GpuWorkload(ModelBase):
    """The workload that holds a GPU."""

    __doc_py_example__ = """\
import anyscale

node = anyscale.gpus.node_gpus(cluster_id="ses_abc123", node_id="nod_abc123")
for gpu in node.gpus:
    if gpu.workload:
        print(gpu.uuid, gpu.workload.type, gpu.workload.id)
"""

    type: str = field(metadata={"docstring": "The workload type: job, service or workspace."})
    id: Optional[str] = field(default=None, metadata={"docstring": "ID of the workload."})
    name: Optional[str] = field(default=None, metadata={"docstring": "Name of the workload."})
    job_attempt_id: Optional[str] = field(
        default=None, metadata={"docstring": "ID of the job attempt. Only set for jobs."}
    )

    def _validate_type(self, type: str):  # noqa: A002
        if not isinstance(type, str) or not type:
            raise ValueError("type must be a non-empty string.")

    def _validate_id(self, id: Optional[str]):  # noqa: A002
        _optional_str("id", id)

    def _validate_name(self, name: Optional[str]):
        _optional_str("name", name)

    def _validate_job_attempt_id(self, job_attempt_id: Optional[str]):
        _optional_str("job_attempt_id", job_attempt_id)


@dataclass(frozen=True)
class GpuXid(ModelBase):
    """One NVIDIA XID error reported by a GPU."""

    __doc_py_example__ = """\
import anyscale

gpu = anyscale.gpus.get(cluster_id="ses_abc123", gpu_uuid="GPU-8f2e...")
for xid in gpu.telemetry.xids:
    print(xid.code, xid.message, "critical" if xid.critical else "", "active" if xid.active else "")
"""

    code: int = field(metadata={"docstring": "The NVIDIA XID error code."})
    message: Optional[str] = field(
        default=None, metadata={"docstring": "What the code means, as DCGM decodes it."}
    )
    critical: bool = field(
        default=False,
        metadata={"docstring": "Whether the code is one NVIDIA lists as a hardware fault."},
    )
    active: bool = field(
        default=False,
        metadata={
            "docstring": "Whether the error was still reported at the snapshot time, "
            "as opposed to an earlier one in the look-back window."
        },
    )

    def _validate_code(self, code: int):
        if isinstance(code, bool) or not isinstance(code, int):
            raise TypeError("code must be an int.")

    def _validate_message(self, message: Optional[str]):
        _optional_str("message", message)

    def _validate_critical(self, critical: bool):
        if not isinstance(critical, bool):
            raise TypeError("critical must be a bool.")

    def _validate_active(self, active: bool):
        if not isinstance(active, bool):
            raise TypeError("active must be a bool.")


@dataclass(frozen=True)
class GpuTelemetry(ModelBase):
    """DCGM telemetry of one GPU at the snapshot time.

    A field is None when the GPU's exporter does not report it (an older driver, or a
    sensor the model lacks).
    """

    __doc_py_example__ = """\
import anyscale

node = anyscale.gpus.node_gpus(cluster_id="ses_abc123", node_id="nod_abc123")
for gpu in node.gpus:
    print(gpu.gpu_index, gpu.uuid, gpu.state, gpu.utilization_pct, gpu.fb_used_mib)
"""

    gpu_index: int = field(metadata={"docstring": "Index of the GPU on its node, from 0."})
    uuid: str = field(metadata={"docstring": "The GPU UUID, GPU-..., as the driver reports it."})
    state: GpuState = field(metadata={"docstring": "What the GPU is doing; see GpuState."})
    gpu_model: Optional[str] = field(
        default=None, metadata={"docstring": "The GPU model, e.g. NVIDIA L4."}
    )
    pci_bus_id: Optional[str] = field(default=None, metadata={"docstring": "The PCI bus ID."})
    driver_version: Optional[str] = field(
        default=None, metadata={"docstring": "The NVIDIA driver version on the node."}
    )
    last_reported_at: Optional[datetime] = field(
        default=None,
        metadata={
            "docstring": "When the GPU last reported telemetry, as a timezone-aware UTC "
            "datetime. Earlier than the snapshot time for an OFFLINE GPU."
        },
    )
    utilization_pct: Optional[float] = field(
        default=None, metadata={"docstring": "GPU utilization, 0 to 100."}
    )
    utilization_source: Optional[str] = field(
        default=None,
        metadata={"docstring": "Which DCGM field served utilization_pct: sm_active or gpu_util."},
    )
    fb_used_mib: Optional[int] = field(
        default=None, metadata={"docstring": "Frame-buffer memory in use, in MiB."}
    )
    fb_free_mib: Optional[int] = field(
        default=None, metadata={"docstring": "Frame-buffer memory free, in MiB."}
    )
    fb_total_mib: Optional[int] = field(
        default=None, metadata={"docstring": "Frame-buffer memory on the GPU, in MiB."}
    )
    gpu_temp_c: Optional[int] = field(
        default=None, metadata={"docstring": "GPU temperature, in degrees Celsius."}
    )
    memory_temp_c: Optional[int] = field(
        default=None, metadata={"docstring": "Memory temperature, in degrees Celsius."}
    )
    power_usage_w: Optional[float] = field(
        default=None, metadata={"docstring": "Power draw, in watts."}
    )
    power_source: Optional[str] = field(
        default=None,
        metadata={
            "docstring": "Which DCGM field served power_usage_w: energy_counter or power_usage."
        },
    )
    power_limit_w: Optional[float] = field(
        default=None, metadata={"docstring": "Configured power limit, in watts."}
    )
    sm_clock_mhz: Optional[int] = field(default=None, metadata={"docstring": "SM clock, in MHz."})
    mem_clock_mhz: Optional[int] = field(
        default=None, metadata={"docstring": "Memory clock, in MHz."}
    )
    ecc_sbe_total: Optional[int] = field(
        default=None, metadata={"docstring": "Single-bit ECC errors since the driver loaded."}
    )
    ecc_dbe_total: Optional[int] = field(
        default=None, metadata={"docstring": "Double-bit ECC errors since the driver loaded."}
    )
    ecc_sbe_aggregate_total: Optional[int] = field(
        default=None, metadata={"docstring": "Single-bit ECC errors over the GPU's lifetime."}
    )
    ecc_dbe_aggregate_total: Optional[int] = field(
        default=None, metadata={"docstring": "Double-bit ECC errors over the GPU's lifetime."}
    )
    correctable_remapped_rows: Optional[int] = field(
        default=None, metadata={"docstring": "Memory rows remapped after correctable errors."}
    )
    uncorrectable_remapped_rows: Optional[int] = field(
        default=None, metadata={"docstring": "Memory rows remapped after uncorrectable errors."}
    )
    nvlink_replay_count: Optional[int] = field(
        default=None, metadata={"docstring": "NVLink replay errors since the driver loaded."}
    )
    xids: List[GpuXid] = field(
        default_factory=list,
        metadata={"docstring": "XID errors seen in the look-back window; see GpuXid."},
    )
    workload: Optional[GpuWorkload] = field(
        default=None,
        metadata={"docstring": "The workload holding the GPU. None when idle or offline."},
    )

    def _validate_gpu_index(self, gpu_index: int):
        _int("gpu_index", gpu_index)

    def _validate_uuid(self, uuid: str):
        # Empty when the GPU's DCGM series carries no UUID label; the backend still
        # returns the GPU, so one such GPU must not fail the whole node listing.
        if not isinstance(uuid, str):
            raise TypeError("uuid must be a string.")

    def _validate_state(self, state: GpuState) -> GpuState:
        return GpuState.validate(state)

    def _validate_gpu_model(self, gpu_model: Optional[str]):
        _optional_str("gpu_model", gpu_model)

    def _validate_pci_bus_id(self, pci_bus_id: Optional[str]):
        _optional_str("pci_bus_id", pci_bus_id)

    def _validate_driver_version(self, driver_version: Optional[str]):
        _optional_str("driver_version", driver_version)

    def _validate_last_reported_at(self, last_reported_at: Optional[datetime]):
        if last_reported_at is not None and not isinstance(last_reported_at, datetime):
            raise TypeError("last_reported_at must be a datetime or None.")

    def _validate_utilization_pct(self, utilization_pct: Optional[float]):
        _optional_number("utilization_pct", utilization_pct)

    def _validate_utilization_source(self, utilization_source: Optional[str]):
        _optional_str("utilization_source", utilization_source)

    def _validate_fb_used_mib(self, fb_used_mib: Optional[int]):
        _optional_int("fb_used_mib", fb_used_mib)

    def _validate_fb_free_mib(self, fb_free_mib: Optional[int]):
        _optional_int("fb_free_mib", fb_free_mib)

    def _validate_fb_total_mib(self, fb_total_mib: Optional[int]):
        _optional_int("fb_total_mib", fb_total_mib)

    def _validate_gpu_temp_c(self, gpu_temp_c: Optional[int]):
        _optional_int("gpu_temp_c", gpu_temp_c)

    def _validate_memory_temp_c(self, memory_temp_c: Optional[int]):
        _optional_int("memory_temp_c", memory_temp_c)

    def _validate_power_usage_w(self, power_usage_w: Optional[float]):
        _optional_number("power_usage_w", power_usage_w)

    def _validate_power_source(self, power_source: Optional[str]):
        _optional_str("power_source", power_source)

    def _validate_power_limit_w(self, power_limit_w: Optional[float]):
        _optional_number("power_limit_w", power_limit_w)

    def _validate_sm_clock_mhz(self, sm_clock_mhz: Optional[int]):
        _optional_int("sm_clock_mhz", sm_clock_mhz)

    def _validate_mem_clock_mhz(self, mem_clock_mhz: Optional[int]):
        _optional_int("mem_clock_mhz", mem_clock_mhz)

    def _validate_ecc_sbe_total(self, ecc_sbe_total: Optional[int]):
        _optional_int("ecc_sbe_total", ecc_sbe_total)

    def _validate_ecc_dbe_total(self, ecc_dbe_total: Optional[int]):
        _optional_int("ecc_dbe_total", ecc_dbe_total)

    def _validate_ecc_sbe_aggregate_total(self, ecc_sbe_aggregate_total: Optional[int]):
        _optional_int("ecc_sbe_aggregate_total", ecc_sbe_aggregate_total)

    def _validate_ecc_dbe_aggregate_total(self, ecc_dbe_aggregate_total: Optional[int]):
        _optional_int("ecc_dbe_aggregate_total", ecc_dbe_aggregate_total)

    def _validate_correctable_remapped_rows(self, correctable_remapped_rows: Optional[int]):
        _optional_int("correctable_remapped_rows", correctable_remapped_rows)

    def _validate_uncorrectable_remapped_rows(self, uncorrectable_remapped_rows: Optional[int]):
        _optional_int("uncorrectable_remapped_rows", uncorrectable_remapped_rows)

    def _validate_nvlink_replay_count(self, nvlink_replay_count: Optional[int]):
        _optional_int("nvlink_replay_count", nvlink_replay_count)

    def _validate_xids(self, xids: List[GpuXid]):
        if not isinstance(xids, list) or not all(isinstance(xid, GpuXid) for xid in xids):
            raise TypeError("xids must be a list of GpuXid.")

    def _validate_workload(self, workload: Optional[GpuWorkload]):
        if workload is not None and not isinstance(workload, GpuWorkload):
            raise TypeError("workload must be a GpuWorkload or None.")


@dataclass(frozen=True)
class NodeGpus(ModelBase):
    """Every GPU on one node of a cluster, with the node's placement."""

    __doc_py_example__ = """\
import anyscale

node = anyscale.gpus.node_gpus(cluster_id="ses_abc123", node_id="nod_abc123")
print(node.instance_type, node.gpu_count)
for gpu in node.gpus:
    print(gpu.gpu_index, gpu.state, gpu.utilization_pct)
"""

    cluster_id: str = field(metadata={"docstring": "ID of the cluster."})
    node_id: str = field(metadata={"docstring": "ID of the node."})
    gpu_count: int = field(metadata={"docstring": "How many GPUs the node reports."})
    gpus: List[GpuTelemetry] = field(
        metadata={"docstring": "The GPUs, sorted by gpu_index; see GpuTelemetry."}
    )
    time: datetime = field(
        metadata={"docstring": "The snapshot time, as a timezone-aware UTC datetime."}
    )
    instance_id: Optional[str] = field(
        default=None, metadata={"docstring": "Cloud instance ID of the node."}
    )
    instance_type: Optional[str] = field(
        default=None, metadata={"docstring": "Cloud instance type of the node."}
    )
    hostname: Optional[str] = field(default=None, metadata={"docstring": "Hostname of the node."})
    node_ip: Optional[str] = field(default=None, metadata={"docstring": "IP of the node."})

    def _validate_cluster_id(self, cluster_id: str):
        _required_str("cluster_id", cluster_id)

    def _validate_node_id(self, node_id: str):
        _required_str("node_id", node_id)

    def _validate_gpu_count(self, gpu_count: int):
        _int("gpu_count", gpu_count)

    def _validate_gpus(self, gpus: List[GpuTelemetry]):
        if not isinstance(gpus, list) or not all(isinstance(gpu, GpuTelemetry) for gpu in gpus):
            raise TypeError("gpus must be a list of GpuTelemetry.")

    def _validate_time(self, time: datetime):
        if not isinstance(time, datetime):
            raise TypeError("time must be a datetime.")

    def _validate_instance_id(self, instance_id: Optional[str]):
        _optional_str("instance_id", instance_id)

    def _validate_instance_type(self, instance_type: Optional[str]):
        _optional_str("instance_type", instance_type)

    def _validate_hostname(self, hostname: Optional[str]):
        _optional_str("hostname", hostname)

    def _validate_node_ip(self, node_ip: Optional[str]):
        _optional_str("node_ip", node_ip)


@dataclass(frozen=True)
class GpuPlacement(ModelBase):
    """Where one GPU is: its cloud, cluster, node and instance."""

    __doc_py_example__ = """\
import anyscale

gpu = anyscale.gpus.get(cluster_id="ses_abc123", gpu_uuid="GPU-8f2e...")
print(gpu.placement.node_id, gpu.placement.instance_id, gpu.placement.instance_type)
"""

    gpu_index: int = field(metadata={"docstring": "Index of the GPU on its node, from 0."})
    cloud_id: str = field(metadata={"docstring": "ID of the cloud."})
    cluster_id: str = field(metadata={"docstring": "ID of the cluster."})
    gpu_model: Optional[str] = field(
        default=None, metadata={"docstring": "The GPU model, e.g. NVIDIA L4."}
    )
    pci_bus_id: Optional[str] = field(default=None, metadata={"docstring": "The PCI bus ID."})
    driver_version: Optional[str] = field(
        default=None, metadata={"docstring": "The NVIDIA driver version on the node."}
    )
    node_id: Optional[str] = field(default=None, metadata={"docstring": "ID of the node."})
    instance_id: Optional[str] = field(
        default=None, metadata={"docstring": "Cloud instance ID of the node."}
    )
    instance_type: Optional[str] = field(
        default=None, metadata={"docstring": "Cloud instance type of the node."}
    )
    hostname: Optional[str] = field(default=None, metadata={"docstring": "Hostname of the node."})
    node_ip: Optional[str] = field(default=None, metadata={"docstring": "IP of the node."})
    workload: Optional[GpuWorkload] = field(
        default=None,
        metadata={"docstring": "The workload holding the GPU. None when idle or offline."},
    )

    def _validate_gpu_index(self, gpu_index: int):
        _int("gpu_index", gpu_index)

    def _validate_cloud_id(self, cloud_id: str):
        _required_str("cloud_id", cloud_id)

    def _validate_cluster_id(self, cluster_id: str):
        _required_str("cluster_id", cluster_id)

    def _validate_gpu_model(self, gpu_model: Optional[str]):
        _optional_str("gpu_model", gpu_model)

    def _validate_pci_bus_id(self, pci_bus_id: Optional[str]):
        _optional_str("pci_bus_id", pci_bus_id)

    def _validate_driver_version(self, driver_version: Optional[str]):
        _optional_str("driver_version", driver_version)

    def _validate_node_id(self, node_id: Optional[str]):
        _optional_str("node_id", node_id)

    def _validate_instance_id(self, instance_id: Optional[str]):
        _optional_str("instance_id", instance_id)

    def _validate_instance_type(self, instance_type: Optional[str]):
        _optional_str("instance_type", instance_type)

    def _validate_hostname(self, hostname: Optional[str]):
        _optional_str("hostname", hostname)

    def _validate_node_ip(self, node_ip: Optional[str]):
        _optional_str("node_ip", node_ip)

    def _validate_workload(self, workload: Optional[GpuWorkload]):
        if workload is not None and not isinstance(workload, GpuWorkload):
            raise TypeError("workload must be a GpuWorkload or None.")


@dataclass(frozen=True)
class Gpu(ModelBase):
    """One GPU, addressed by UUID: where it is and what it reports."""

    __doc_py_example__ = """\
import anyscale

gpu = anyscale.gpus.get(cluster_id="ses_abc123", gpu_uuid="GPU-8f2e...")
print(gpu.placement.node_id, gpu.telemetry.state, gpu.telemetry.utilization_pct)
"""

    gpu_uuid: str = field(metadata={"docstring": "The GPU UUID, GPU-..."})
    placement: GpuPlacement = field(
        metadata={"docstring": "Cloud, cluster, node and instance; see GpuPlacement."}
    )
    telemetry: GpuTelemetry = field(
        metadata={"docstring": "DCGM telemetry at the snapshot time; see GpuTelemetry."}
    )
    time: datetime = field(
        metadata={"docstring": "The snapshot time, as a timezone-aware UTC datetime."}
    )

    def _validate_gpu_uuid(self, gpu_uuid: str):
        _required_str("gpu_uuid", gpu_uuid)

    def _validate_placement(self, placement: GpuPlacement):
        if not isinstance(placement, GpuPlacement):
            raise TypeError("placement must be a GpuPlacement.")

    def _validate_telemetry(self, telemetry: GpuTelemetry):
        if not isinstance(telemetry, GpuTelemetry):
            raise TypeError("telemetry must be a GpuTelemetry.")

    def _validate_time(self, time: datetime):
        if not isinstance(time, datetime):
            raise TypeError("time must be a datetime.")


# --- field checks shared by the models above -----------------------------------------------


def _required_str(name: str, value: str) -> None:
    if not isinstance(value, str) or not value:
        raise ValueError(f"{name} must be a non-empty string.")


def _optional_str(name: str, value: Optional[str]) -> None:
    if value is not None and not isinstance(value, str):
        raise TypeError(f"{name} must be a string or None.")


def _int(name: str, value: int) -> None:
    if isinstance(value, bool) or not isinstance(value, int):
        raise TypeError(f"{name} must be an int.")


def _optional_int(name: str, value: Optional[int]) -> None:
    if value is not None:
        _int(name, value)


def _optional_number(name: str, value: Optional[float]) -> None:
    if value is not None and (isinstance(value, bool) or not isinstance(value, (int, float))):
        raise TypeError(f"{name} must be a number or None.")
