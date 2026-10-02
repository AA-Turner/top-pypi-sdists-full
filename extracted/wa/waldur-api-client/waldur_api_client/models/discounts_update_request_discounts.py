from collections.abc import Mapping
from typing import TYPE_CHECKING, Any, TypeVar

from attrs import define as _attrs_define
from attrs import field as _attrs_field

if TYPE_CHECKING:
    from ..models.discount_config_request import DiscountConfigRequest


T = TypeVar("T", bound="DiscountsUpdateRequestDiscounts")


@_attrs_define
class DiscountsUpdateRequestDiscounts:
    """Dictionary mapping component types to their discount configuration."""

    additional_properties: dict[str, "DiscountConfigRequest"] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        field_dict: dict[str, Any] = {}
        for prop_name, prop in self.additional_properties.items():
            field_dict[prop_name] = prop.to_dict()

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.discount_config_request import DiscountConfigRequest

        d = dict(src_dict)
        discounts_update_request_discounts = cls()

        additional_properties = {}
        for prop_name, prop_dict in d.items():
            additional_property = DiscountConfigRequest.from_dict(prop_dict)

            additional_properties[prop_name] = additional_property

        discounts_update_request_discounts.additional_properties = additional_properties
        return discounts_update_request_discounts

    @property
    def additional_keys(self) -> list[str]:
        return list(self.additional_properties.keys())

    def __getitem__(self, key: str) -> "DiscountConfigRequest":
        return self.additional_properties[key]

    def __setitem__(self, key: str, value: "DiscountConfigRequest") -> None:
        self.additional_properties[key] = value

    def __delitem__(self, key: str) -> None:
        del self.additional_properties[key]

    def __contains__(self, key: str) -> bool:
        return key in self.additional_properties
