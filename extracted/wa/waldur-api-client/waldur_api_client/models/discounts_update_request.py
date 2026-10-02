from collections.abc import Mapping
from typing import TYPE_CHECKING, Any, TypeVar

from attrs import define as _attrs_define
from attrs import field as _attrs_field

if TYPE_CHECKING:
    from ..models.discounts_update_request_discounts import DiscountsUpdateRequestDiscounts


T = TypeVar("T", bound="DiscountsUpdateRequest")


@_attrs_define
class DiscountsUpdateRequest:
    """
    Attributes:
        discounts (DiscountsUpdateRequestDiscounts): Dictionary mapping component types to their discount configuration.
    """

    discounts: "DiscountsUpdateRequestDiscounts"
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        discounts = self.discounts.to_dict()

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "discounts": discounts,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.discounts_update_request_discounts import DiscountsUpdateRequestDiscounts

        d = dict(src_dict)
        discounts = DiscountsUpdateRequestDiscounts.from_dict(d.pop("discounts"))

        discounts_update_request = cls(
            discounts=discounts,
        )

        discounts_update_request.additional_properties = d
        return discounts_update_request

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
