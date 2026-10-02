from collections.abc import Mapping
from typing import Any, TypeVar

from attrs import define as _attrs_define
from attrs import field as _attrs_field

T = TypeVar("T", bound="IPMappingRequest")


@_attrs_define
class IPMappingRequest:
    """
    Attributes:
        floating_ip (str): Floating IP
        external_ip (str): External IP
    """

    floating_ip: str
    external_ip: str
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        floating_ip = self.floating_ip

        external_ip = self.external_ip

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "floating_ip": floating_ip,
                "external_ip": external_ip,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        floating_ip = d.pop("floating_ip")

        external_ip = d.pop("external_ip")

        ip_mapping_request = cls(
            floating_ip=floating_ip,
            external_ip=external_ip,
        )

        ip_mapping_request.additional_properties = d
        return ip_mapping_request

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
