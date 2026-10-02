from collections.abc import Mapping
from typing import Any, TypeVar

from attrs import define as _attrs_define
from attrs import field as _attrs_field

T = TypeVar("T", bound="OfferingSoftwareCatalogRequestEnabledCpuMicroarchitectures")


@_attrs_define
class OfferingSoftwareCatalogRequestEnabledCpuMicroarchitectures:
    """List of enabled CPU microarchitectures: ['generic', 'zen3']"""

    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        offering_software_catalog_request_enabled_cpu_microarchitectures = cls()

        offering_software_catalog_request_enabled_cpu_microarchitectures.additional_properties = d
        return offering_software_catalog_request_enabled_cpu_microarchitectures

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
