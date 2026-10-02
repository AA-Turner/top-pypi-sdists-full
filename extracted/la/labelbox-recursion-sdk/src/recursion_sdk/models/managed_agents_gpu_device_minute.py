from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar, BinaryIO, TextIO, TYPE_CHECKING, Generator

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset







T = TypeVar("T", bound="ManagedAgentsGPUDeviceMinute")



@_attrs_define
class ManagedAgentsGPUDeviceMinute:
    """ One accelerator's summary for a minute bucket: its driver index, average and peak utilization, peak memory used, and
    total memory. The per-sample GPU arrays, and the -1 holes for samples the device did not report, live on the bucket
    itself.

        Example:
            {'index': 1, 'memory_total_bytes': 1, 'memory_used_peak_bytes': 1, 'utilization_avg': 1.5, 'utilization_peak':
                1.5}

        Attributes:
            index (int): Device index as the driver reports it.
            memory_total_bytes (int): Device memory capacity in bytes.
            memory_used_peak_bytes (int): Highest sampled device memory in use during the minute, in bytes.
            utilization_avg (float): Mean utilization percent across the minute's samples.
            utilization_peak (float): Highest sampled utilization percent in the minute.
     """

    index: int
    memory_total_bytes: int
    memory_used_peak_bytes: int
    utilization_avg: float
    utilization_peak: float
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)





    def to_dict(self) -> dict[str, Any]:
        index = self.index

        memory_total_bytes = self.memory_total_bytes

        memory_used_peak_bytes = self.memory_used_peak_bytes

        utilization_avg = self.utilization_avg

        utilization_peak = self.utilization_peak


        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({
            "index": index,
            "memory_total_bytes": memory_total_bytes,
            "memory_used_peak_bytes": memory_used_peak_bytes,
            "utilization_avg": utilization_avg,
            "utilization_peak": utilization_peak,
        })

        return field_dict



    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        index = d.pop("index")

        memory_total_bytes = d.pop("memory_total_bytes")

        memory_used_peak_bytes = d.pop("memory_used_peak_bytes")

        utilization_avg = d.pop("utilization_avg")

        utilization_peak = d.pop("utilization_peak")

        managed_agents_gpu_device_minute = cls(
            index=index,
            memory_total_bytes=memory_total_bytes,
            memory_used_peak_bytes=memory_used_peak_bytes,
            utilization_avg=utilization_avg,
            utilization_peak=utilization_peak,
        )


        managed_agents_gpu_device_minute.additional_properties = d
        return managed_agents_gpu_device_minute

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
