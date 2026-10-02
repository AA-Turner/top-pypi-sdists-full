from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar, BinaryIO, TextIO, TYPE_CHECKING, Generator

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

from ..types import UNSET, Unset
from typing import cast
import datetime

if TYPE_CHECKING:
  from ..models.managed_agents_gpu_device_minute import ManagedAgentsGPUDeviceMinute





T = TypeVar("T", bound="ManagedAgentsResourceSampleBucket")



@_attrs_define
class ManagedAgentsResourceSampleBucket:
    """ One sandbox attachment's resource usage for one minute. Per-sample CPU, memory, and disk readings are parallel
    arrays indexed by offsets_ms; the average and peak columns summarize the minute and are all a summary-resolution
    read returns. Capacities and limits give each series its denominator.

        Example:
            {'bucket_start': '2026-02-18T09:30:00Z', 'complete': True, 'cpu_capacity_millicores': 1, 'cpu_limit_millicores':
                1, 'cpu_millicores': [1], 'cpu_millicores_avg': 1, 'cpu_millicores_peak': 1, 'disk_capacity_bytes': 1,
                'disk_used_avg_bytes': 1, 'disk_used_bytes': [1], 'disk_used_peak_bytes': 1, 'gpu_count': 1, 'gpu_devices':
                [{'index': 1, 'memory_total_bytes': 1, 'memory_used_peak_bytes': 1, 'utilization_avg': 1.5, 'utilization_peak':
                1.5}], 'gpu_memory_total_bytes': 1, 'gpu_memory_used_bytes': [1], 'gpu_memory_used_peak_bytes': 1,
                'gpu_utilization_avg': 1.5, 'gpu_utilization_peak': 1.5, 'gpu_utilization_percent': [1.5], 'interval_ms': 1,
                'memory_capacity_bytes': 1, 'memory_limit_bytes': 1, 'memory_working_set_avg_bytes': 1,
                'memory_working_set_bytes': [1], 'memory_working_set_peak_bytes': 1, 'offsets_ms': [1], 'received_at':
                '2026-02-18T09:30:00Z', 'sample_count': 1, 'sandbox_id': '9f8b1c2d-3e4f-5a6b-7c8d-9e0f1a2b3c4d', 'shared_slots':
                1}

        Attributes:
            bucket_start (datetime.datetime): RFC 3339 timestamp of the minute's start, on the producer's clock.
            complete (bool): True once the producer has moved past this minute. An incomplete bucket is the one being filled
                and is rewritten by the next drain.
            cpu_millicores_avg (int): Mean CPU millicores over the minute.
            cpu_millicores_peak (int): Highest sampled CPU millicores in the minute.
            interval_ms (int): Producer sampling cadence in milliseconds.
            memory_working_set_avg_bytes (int): Mean memory working set over the minute, in bytes.
            memory_working_set_peak_bytes (int): Highest sampled memory working set in the minute, in bytes.
            received_at (datetime.datetime): RFC 3339 commit timestamp of the write that last touched this bucket.
            sample_count (int): Number of samples in the minute; twelve at the default five-second cadence.
            sandbox_id (str): Attachment the bucket belongs to.
            cpu_capacity_millicores (int | Unset): CPU the container could use in millicores: its quota when set, otherwise
                the CPUs its cpuset allows. Divide cpu_millicores by this for utilization percent.
            cpu_limit_millicores (int | Unset): CPU quota of the container in millicores, when one is set.
            cpu_millicores (list[int] | Unset): Per-sample CPU consumption in millicores; 1000 is one core fully busy.
            disk_capacity_bytes (int | Unset): Bytes the workspace volume can hold for an unprivileged writer (size less the
                root reserve). Divide disk_used by this for utilization percent.
            disk_used_avg_bytes (int | Unset): Mean bytes in use on the workspace volume over the minute. Absent without a
                disk reading.
            disk_used_bytes (list[int] | Unset): Per-sample bytes in use on the volume holding the workspace. -1 marks a
                sample without a disk reading. Absent when the producer never saw the volume.
            disk_used_peak_bytes (int | Unset): Highest sampled bytes in use on the workspace volume in the minute. Absent
                without a disk reading.
            gpu_count (int | Unset): Number of accelerators visible to the container. Absent without accelerators.
            gpu_devices (list[ManagedAgentsGPUDeviceMinute] | Unset): Per-device summary for the minute. Absent without
                accelerators.
            gpu_memory_total_bytes (int | Unset): Total accelerator memory in bytes across devices. Absent without
                accelerators.
            gpu_memory_used_bytes (list[int] | Unset): Per-sample GPU memory in use, summed across devices. Absent without
                accelerators.
            gpu_memory_used_peak_bytes (int | Unset): Highest sampled GPU memory in use during the minute, in bytes. Absent
                without accelerators.
            gpu_utilization_avg (float | Unset): Mean GPU utilization percent over the minute. Absent without accelerators.
            gpu_utilization_peak (float | Unset): Highest sampled GPU utilization percent in the minute. Absent without
                accelerators.
            gpu_utilization_percent (list[float] | Unset): Per-sample GPU utilization percent, mean across devices. Absent
                without accelerators.
            memory_capacity_bytes (int | Unset): Memory the container could use in bytes: its limit when set, otherwise the
                machine's total. Divide the working set by this for utilization percent.
            memory_limit_bytes (int | Unset): Memory limit of the container in bytes, when one is set.
            memory_working_set_bytes (list[int] | Unset): Per-sample memory working set in bytes (resident less reclaimable
                file cache).
            offsets_ms (list[int] | Unset): Sample times as milliseconds after bucket_start, ascending. Indexes the other
                per-sample arrays.
            shared_slots (int | Unset): Historical count of sessions that shared the retired environment worker's process
                boundary, including this one. Absent on samples from active providers.
     """

    bucket_start: datetime.datetime
    complete: bool
    cpu_millicores_avg: int
    cpu_millicores_peak: int
    interval_ms: int
    memory_working_set_avg_bytes: int
    memory_working_set_peak_bytes: int
    received_at: datetime.datetime
    sample_count: int
    sandbox_id: str
    cpu_capacity_millicores: int | Unset = UNSET
    cpu_limit_millicores: int | Unset = UNSET
    cpu_millicores: list[int] | Unset = UNSET
    disk_capacity_bytes: int | Unset = UNSET
    disk_used_avg_bytes: int | Unset = UNSET
    disk_used_bytes: list[int] | Unset = UNSET
    disk_used_peak_bytes: int | Unset = UNSET
    gpu_count: int | Unset = UNSET
    gpu_devices: list[ManagedAgentsGPUDeviceMinute] | Unset = UNSET
    gpu_memory_total_bytes: int | Unset = UNSET
    gpu_memory_used_bytes: list[int] | Unset = UNSET
    gpu_memory_used_peak_bytes: int | Unset = UNSET
    gpu_utilization_avg: float | Unset = UNSET
    gpu_utilization_peak: float | Unset = UNSET
    gpu_utilization_percent: list[float] | Unset = UNSET
    memory_capacity_bytes: int | Unset = UNSET
    memory_limit_bytes: int | Unset = UNSET
    memory_working_set_bytes: list[int] | Unset = UNSET
    offsets_ms: list[int] | Unset = UNSET
    shared_slots: int | Unset = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)





    def to_dict(self) -> dict[str, Any]:
        from ..models.managed_agents_gpu_device_minute import ManagedAgentsGPUDeviceMinute # noqa: PLC0415
        bucket_start = self.bucket_start.isoformat()

        complete = self.complete

        cpu_millicores_avg = self.cpu_millicores_avg

        cpu_millicores_peak = self.cpu_millicores_peak

        interval_ms = self.interval_ms

        memory_working_set_avg_bytes = self.memory_working_set_avg_bytes

        memory_working_set_peak_bytes = self.memory_working_set_peak_bytes

        received_at = self.received_at.isoformat()

        sample_count = self.sample_count

        sandbox_id = self.sandbox_id

        cpu_capacity_millicores = self.cpu_capacity_millicores

        cpu_limit_millicores = self.cpu_limit_millicores

        cpu_millicores: list[int] | Unset = UNSET
        if not isinstance(self.cpu_millicores, Unset):
            cpu_millicores = self.cpu_millicores



        disk_capacity_bytes = self.disk_capacity_bytes

        disk_used_avg_bytes = self.disk_used_avg_bytes

        disk_used_bytes: list[int] | Unset = UNSET
        if not isinstance(self.disk_used_bytes, Unset):
            disk_used_bytes = self.disk_used_bytes



        disk_used_peak_bytes = self.disk_used_peak_bytes

        gpu_count = self.gpu_count

        gpu_devices: list[dict[str, Any]] | Unset = UNSET
        if not isinstance(self.gpu_devices, Unset):
            gpu_devices = []
            for gpu_devices_item_data in self.gpu_devices:
                gpu_devices_item = gpu_devices_item_data.to_dict()
                gpu_devices.append(gpu_devices_item)



        gpu_memory_total_bytes = self.gpu_memory_total_bytes

        gpu_memory_used_bytes: list[int] | Unset = UNSET
        if not isinstance(self.gpu_memory_used_bytes, Unset):
            gpu_memory_used_bytes = self.gpu_memory_used_bytes



        gpu_memory_used_peak_bytes = self.gpu_memory_used_peak_bytes

        gpu_utilization_avg = self.gpu_utilization_avg

        gpu_utilization_peak = self.gpu_utilization_peak

        gpu_utilization_percent: list[float] | Unset = UNSET
        if not isinstance(self.gpu_utilization_percent, Unset):
            gpu_utilization_percent = self.gpu_utilization_percent



        memory_capacity_bytes = self.memory_capacity_bytes

        memory_limit_bytes = self.memory_limit_bytes

        memory_working_set_bytes: list[int] | Unset = UNSET
        if not isinstance(self.memory_working_set_bytes, Unset):
            memory_working_set_bytes = self.memory_working_set_bytes



        offsets_ms: list[int] | Unset = UNSET
        if not isinstance(self.offsets_ms, Unset):
            offsets_ms = self.offsets_ms



        shared_slots = self.shared_slots


        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({
            "bucket_start": bucket_start,
            "complete": complete,
            "cpu_millicores_avg": cpu_millicores_avg,
            "cpu_millicores_peak": cpu_millicores_peak,
            "interval_ms": interval_ms,
            "memory_working_set_avg_bytes": memory_working_set_avg_bytes,
            "memory_working_set_peak_bytes": memory_working_set_peak_bytes,
            "received_at": received_at,
            "sample_count": sample_count,
            "sandbox_id": sandbox_id,
        })
        if cpu_capacity_millicores is not UNSET:
            field_dict["cpu_capacity_millicores"] = cpu_capacity_millicores
        if cpu_limit_millicores is not UNSET:
            field_dict["cpu_limit_millicores"] = cpu_limit_millicores
        if cpu_millicores is not UNSET:
            field_dict["cpu_millicores"] = cpu_millicores
        if disk_capacity_bytes is not UNSET:
            field_dict["disk_capacity_bytes"] = disk_capacity_bytes
        if disk_used_avg_bytes is not UNSET:
            field_dict["disk_used_avg_bytes"] = disk_used_avg_bytes
        if disk_used_bytes is not UNSET:
            field_dict["disk_used_bytes"] = disk_used_bytes
        if disk_used_peak_bytes is not UNSET:
            field_dict["disk_used_peak_bytes"] = disk_used_peak_bytes
        if gpu_count is not UNSET:
            field_dict["gpu_count"] = gpu_count
        if gpu_devices is not UNSET:
            field_dict["gpu_devices"] = gpu_devices
        if gpu_memory_total_bytes is not UNSET:
            field_dict["gpu_memory_total_bytes"] = gpu_memory_total_bytes
        if gpu_memory_used_bytes is not UNSET:
            field_dict["gpu_memory_used_bytes"] = gpu_memory_used_bytes
        if gpu_memory_used_peak_bytes is not UNSET:
            field_dict["gpu_memory_used_peak_bytes"] = gpu_memory_used_peak_bytes
        if gpu_utilization_avg is not UNSET:
            field_dict["gpu_utilization_avg"] = gpu_utilization_avg
        if gpu_utilization_peak is not UNSET:
            field_dict["gpu_utilization_peak"] = gpu_utilization_peak
        if gpu_utilization_percent is not UNSET:
            field_dict["gpu_utilization_percent"] = gpu_utilization_percent
        if memory_capacity_bytes is not UNSET:
            field_dict["memory_capacity_bytes"] = memory_capacity_bytes
        if memory_limit_bytes is not UNSET:
            field_dict["memory_limit_bytes"] = memory_limit_bytes
        if memory_working_set_bytes is not UNSET:
            field_dict["memory_working_set_bytes"] = memory_working_set_bytes
        if offsets_ms is not UNSET:
            field_dict["offsets_ms"] = offsets_ms
        if shared_slots is not UNSET:
            field_dict["shared_slots"] = shared_slots

        return field_dict



    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.managed_agents_gpu_device_minute import ManagedAgentsGPUDeviceMinute # noqa: PLC0415
        d = dict(src_dict)
        bucket_start = datetime.datetime.fromisoformat(d.pop("bucket_start"))




        complete = d.pop("complete")

        cpu_millicores_avg = d.pop("cpu_millicores_avg")

        cpu_millicores_peak = d.pop("cpu_millicores_peak")

        interval_ms = d.pop("interval_ms")

        memory_working_set_avg_bytes = d.pop("memory_working_set_avg_bytes")

        memory_working_set_peak_bytes = d.pop("memory_working_set_peak_bytes")

        received_at = datetime.datetime.fromisoformat(d.pop("received_at"))




        sample_count = d.pop("sample_count")

        sandbox_id = d.pop("sandbox_id")

        cpu_capacity_millicores = d.pop("cpu_capacity_millicores", UNSET)

        cpu_limit_millicores = d.pop("cpu_limit_millicores", UNSET)

        cpu_millicores = cast(list[int], d.pop("cpu_millicores", UNSET))


        disk_capacity_bytes = d.pop("disk_capacity_bytes", UNSET)

        disk_used_avg_bytes = d.pop("disk_used_avg_bytes", UNSET)

        disk_used_bytes = cast(list[int], d.pop("disk_used_bytes", UNSET))


        disk_used_peak_bytes = d.pop("disk_used_peak_bytes", UNSET)

        gpu_count = d.pop("gpu_count", UNSET)

        _gpu_devices = d.pop("gpu_devices", UNSET)
        gpu_devices: list[ManagedAgentsGPUDeviceMinute] | Unset = UNSET
        if _gpu_devices is not UNSET:
            gpu_devices = []
            for gpu_devices_item_data in _gpu_devices:
                gpu_devices_item = ManagedAgentsGPUDeviceMinute.from_dict(gpu_devices_item_data)



                gpu_devices.append(gpu_devices_item)


        gpu_memory_total_bytes = d.pop("gpu_memory_total_bytes", UNSET)

        gpu_memory_used_bytes = cast(list[int], d.pop("gpu_memory_used_bytes", UNSET))


        gpu_memory_used_peak_bytes = d.pop("gpu_memory_used_peak_bytes", UNSET)

        gpu_utilization_avg = d.pop("gpu_utilization_avg", UNSET)

        gpu_utilization_peak = d.pop("gpu_utilization_peak", UNSET)

        gpu_utilization_percent = cast(list[float], d.pop("gpu_utilization_percent", UNSET))


        memory_capacity_bytes = d.pop("memory_capacity_bytes", UNSET)

        memory_limit_bytes = d.pop("memory_limit_bytes", UNSET)

        memory_working_set_bytes = cast(list[int], d.pop("memory_working_set_bytes", UNSET))


        offsets_ms = cast(list[int], d.pop("offsets_ms", UNSET))


        shared_slots = d.pop("shared_slots", UNSET)

        managed_agents_resource_sample_bucket = cls(
            bucket_start=bucket_start,
            complete=complete,
            cpu_millicores_avg=cpu_millicores_avg,
            cpu_millicores_peak=cpu_millicores_peak,
            interval_ms=interval_ms,
            memory_working_set_avg_bytes=memory_working_set_avg_bytes,
            memory_working_set_peak_bytes=memory_working_set_peak_bytes,
            received_at=received_at,
            sample_count=sample_count,
            sandbox_id=sandbox_id,
            cpu_capacity_millicores=cpu_capacity_millicores,
            cpu_limit_millicores=cpu_limit_millicores,
            cpu_millicores=cpu_millicores,
            disk_capacity_bytes=disk_capacity_bytes,
            disk_used_avg_bytes=disk_used_avg_bytes,
            disk_used_bytes=disk_used_bytes,
            disk_used_peak_bytes=disk_used_peak_bytes,
            gpu_count=gpu_count,
            gpu_devices=gpu_devices,
            gpu_memory_total_bytes=gpu_memory_total_bytes,
            gpu_memory_used_bytes=gpu_memory_used_bytes,
            gpu_memory_used_peak_bytes=gpu_memory_used_peak_bytes,
            gpu_utilization_avg=gpu_utilization_avg,
            gpu_utilization_peak=gpu_utilization_peak,
            gpu_utilization_percent=gpu_utilization_percent,
            memory_capacity_bytes=memory_capacity_bytes,
            memory_limit_bytes=memory_limit_bytes,
            memory_working_set_bytes=memory_working_set_bytes,
            offsets_ms=offsets_ms,
            shared_slots=shared_slots,
        )


        managed_agents_resource_sample_bucket.additional_properties = d
        return managed_agents_resource_sample_bucket

    @property
    def additional_keys(self) -> list[str]:
        return list(self.additional_properties.keys())

    def __getitem__(self, key: str) -> Any:
        return self.additional_properties[key]

    def __setitem__(self, key: str, value: Any) -> None:
        self.additional_properties[key] = value

    def __delitem__(self, key: str) -> None:
        del self.additional_properties[key]

    def __contains__(self, key: str) -> bool:
        return key in self.additional_properties
