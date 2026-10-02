from collections.abc import Mapping
from typing import Any, TypeVar, Union

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

T = TypeVar("T", bound="AllowedAddressPairEntryRequest")


@_attrs_define
class AllowedAddressPairEntryRequest:
    """
    Attributes:
        ip_address (str):
        mac_address (Union[Unset, str]):
    """

    ip_address: str
    mac_address: Union[Unset, str] = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        ip_address = self.ip_address

        mac_address = self.mac_address

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "ip_address": ip_address,
            }
        )
        if mac_address is not UNSET:
            field_dict["mac_address"] = mac_address

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        ip_address = d.pop("ip_address")

        mac_address = d.pop("mac_address", UNSET)

        allowed_address_pair_entry_request = cls(
            ip_address=ip_address,
            mac_address=mac_address,
        )

        allowed_address_pair_entry_request.additional_properties = d
        return allowed_address_pair_entry_request

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
