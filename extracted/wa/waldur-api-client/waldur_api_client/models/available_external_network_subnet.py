from collections.abc import Mapping
from typing import Any, TypeVar

from attrs import define as _attrs_define
from attrs import field as _attrs_field

T = TypeVar("T", bound="AvailableExternalNetworkSubnet")


@_attrs_define
class AvailableExternalNetworkSubnet:
    """
    Attributes:
        backend_id (str):
        name (str):
        cidr (str):
    """

    backend_id: str
    name: str
    cidr: str
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        backend_id = self.backend_id

        name = self.name

        cidr = self.cidr

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "backend_id": backend_id,
                "name": name,
                "cidr": cidr,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        backend_id = d.pop("backend_id")

        name = d.pop("name")

        cidr = d.pop("cidr")

        available_external_network_subnet = cls(
            backend_id=backend_id,
            name=name,
            cidr=cidr,
        )

        available_external_network_subnet.additional_properties = d
        return available_external_network_subnet

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
