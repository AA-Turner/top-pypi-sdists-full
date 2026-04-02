from collections.abc import Mapping
from typing import Any, TypeVar, Union

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

T = TypeVar("T", bound="IPMapping")


@_attrs_define
class IPMapping:
    """
    Attributes:
        floating_ip (Union[Unset, str]): Floating IP
        external_ip (Union[Unset, str]): External IP
    """

    floating_ip: Union[Unset, str] = UNSET
    external_ip: Union[Unset, str] = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        floating_ip = self.floating_ip

        external_ip = self.external_ip

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if floating_ip is not UNSET:
            field_dict["floating_ip"] = floating_ip
        if external_ip is not UNSET:
            field_dict["external_ip"] = external_ip

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        floating_ip = d.pop("floating_ip", UNSET)

        external_ip = d.pop("external_ip", UNSET)

        ip_mapping = cls(
            floating_ip=floating_ip,
            external_ip=external_ip,
        )

        ip_mapping.additional_properties = d
        return ip_mapping

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
