from collections.abc import Mapping
from typing import Any, TypeVar

from attrs import define as _attrs_define
from attrs import field as _attrs_field

T = TypeVar("T", bound="SoftwareCatalogCpuTarget")


@_attrs_define
class SoftwareCatalogCpuTarget:
    """
    Attributes:
        cpu_family (str):
        cpu_microarchitecture (str):
        full_arch (str):
    """

    cpu_family: str
    cpu_microarchitecture: str
    full_arch: str
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        cpu_family = self.cpu_family

        cpu_microarchitecture = self.cpu_microarchitecture

        full_arch = self.full_arch

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "cpu_family": cpu_family,
                "cpu_microarchitecture": cpu_microarchitecture,
                "full_arch": full_arch,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        cpu_family = d.pop("cpu_family")

        cpu_microarchitecture = d.pop("cpu_microarchitecture")

        full_arch = d.pop("full_arch")

        software_catalog_cpu_target = cls(
            cpu_family=cpu_family,
            cpu_microarchitecture=cpu_microarchitecture,
            full_arch=full_arch,
        )

        software_catalog_cpu_target.additional_properties = d
        return software_catalog_cpu_target

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
