from collections.abc import Mapping
from typing import TYPE_CHECKING, Any, TypeVar

from attrs import define as _attrs_define
from attrs import field as _attrs_field

if TYPE_CHECKING:
    from ..models.allowed_address_pair_entry_request import AllowedAddressPairEntryRequest


T = TypeVar("T", bound="SetAllowedAddressPairsRequest")


@_attrs_define
class SetAllowedAddressPairsRequest:
    """
    Attributes:
        allowed_address_pairs (list['AllowedAddressPairEntryRequest']):
    """

    allowed_address_pairs: list["AllowedAddressPairEntryRequest"]
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        allowed_address_pairs = []
        for allowed_address_pairs_item_data in self.allowed_address_pairs:
            allowed_address_pairs_item = allowed_address_pairs_item_data.to_dict()
            allowed_address_pairs.append(allowed_address_pairs_item)

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "allowed_address_pairs": allowed_address_pairs,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.allowed_address_pair_entry_request import AllowedAddressPairEntryRequest

        d = dict(src_dict)
        allowed_address_pairs = []
        _allowed_address_pairs = d.pop("allowed_address_pairs")
        for allowed_address_pairs_item_data in _allowed_address_pairs:
            allowed_address_pairs_item = AllowedAddressPairEntryRequest.from_dict(allowed_address_pairs_item_data)

            allowed_address_pairs.append(allowed_address_pairs_item)

        set_allowed_address_pairs_request = cls(
            allowed_address_pairs=allowed_address_pairs,
        )

        set_allowed_address_pairs_request.additional_properties = d
        return set_allowed_address_pairs_request

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
