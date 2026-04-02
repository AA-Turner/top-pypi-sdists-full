from collections.abc import Mapping
from typing import Any, TypeVar

from attrs import define as _attrs_define
from attrs import field as _attrs_field

T = TypeVar("T", bound="SlurmAllocationSetLimits")


@_attrs_define
class SlurmAllocationSetLimits:
    """
    Attributes:
        cpu_limit (int):
        gpu_limit (int):
        ram_limit (int):
    """

    cpu_limit: int
    gpu_limit: int
    ram_limit: int
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        cpu_limit = self.cpu_limit

        gpu_limit = self.gpu_limit

        ram_limit = self.ram_limit

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "cpu_limit": cpu_limit,
                "gpu_limit": gpu_limit,
                "ram_limit": ram_limit,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        cpu_limit = d.pop("cpu_limit")

        gpu_limit = d.pop("gpu_limit")

        ram_limit = d.pop("ram_limit")

        slurm_allocation_set_limits = cls(
            cpu_limit=cpu_limit,
            gpu_limit=gpu_limit,
            ram_limit=ram_limit,
        )

        slurm_allocation_set_limits.additional_properties = d
        return slurm_allocation_set_limits

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
