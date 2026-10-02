from collections.abc import Mapping
from typing import Any, TypeVar

from attrs import define as _attrs_define
from attrs import field as _attrs_field

T = TypeVar("T", bound="HypervisorSummary")


@_attrs_define
class HypervisorSummary:
    """
    Attributes:
        total_vcpus (int):
        used_vcpus (int):
        total_memory_mb (int):
        used_memory_mb (int):
        total_local_gb (int):
        used_local_gb (int):
        total_running_vms (int):
    """

    total_vcpus: int
    used_vcpus: int
    total_memory_mb: int
    used_memory_mb: int
    total_local_gb: int
    used_local_gb: int
    total_running_vms: int
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        total_vcpus = self.total_vcpus

        used_vcpus = self.used_vcpus

        total_memory_mb = self.total_memory_mb

        used_memory_mb = self.used_memory_mb

        total_local_gb = self.total_local_gb

        used_local_gb = self.used_local_gb

        total_running_vms = self.total_running_vms

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "total_vcpus": total_vcpus,
                "used_vcpus": used_vcpus,
                "total_memory_mb": total_memory_mb,
                "used_memory_mb": used_memory_mb,
                "total_local_gb": total_local_gb,
                "used_local_gb": used_local_gb,
                "total_running_vms": total_running_vms,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        total_vcpus = d.pop("total_vcpus")

        used_vcpus = d.pop("used_vcpus")

        total_memory_mb = d.pop("total_memory_mb")

        used_memory_mb = d.pop("used_memory_mb")

        total_local_gb = d.pop("total_local_gb")

        used_local_gb = d.pop("used_local_gb")

        total_running_vms = d.pop("total_running_vms")

        hypervisor_summary = cls(
            total_vcpus=total_vcpus,
            used_vcpus=used_vcpus,
            total_memory_mb=total_memory_mb,
            used_memory_mb=used_memory_mb,
            total_local_gb=total_local_gb,
            used_local_gb=used_local_gb,
            total_running_vms=total_running_vms,
        )

        hypervisor_summary.additional_properties = d
        return hypervisor_summary

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
