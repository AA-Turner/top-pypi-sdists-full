from collections.abc import Mapping
from typing import Any, TypeVar

from attrs import define as _attrs_define
from attrs import field as _attrs_field

T = TypeVar("T", bound="SubNetMappingRequest")


@_attrs_define
class SubNetMappingRequest:
    """
    Attributes:
        src_cidr (str):
        dst_cidr (str):
    """

    src_cidr: str
    dst_cidr: str
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        src_cidr = self.src_cidr

        dst_cidr = self.dst_cidr

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "src_cidr": src_cidr,
                "dst_cidr": dst_cidr,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        src_cidr = d.pop("src_cidr")

        dst_cidr = d.pop("dst_cidr")

        sub_net_mapping_request = cls(
            src_cidr=src_cidr,
            dst_cidr=dst_cidr,
        )

        sub_net_mapping_request.additional_properties = d
        return sub_net_mapping_request

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
