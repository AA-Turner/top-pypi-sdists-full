from collections.abc import Mapping
from typing import Any, TypeVar, Union

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

T = TypeVar("T", bound="ComponentUsageItemRequest")


@_attrs_define
class ComponentUsageItemRequest:
    """
    Attributes:
        type_ (str): Type of the component
        amount (str): Usage amount
        description (Union[Unset, str]): Optional description of usage
        recurring (Union[Unset, bool]): Whether this usage is recurring Default: False.
    """

    type_: str
    amount: str
    description: Union[Unset, str] = UNSET
    recurring: Union[Unset, bool] = False
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        type_ = self.type_

        amount = self.amount

        description = self.description

        recurring = self.recurring

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "type": type_,
                "amount": amount,
            }
        )
        if description is not UNSET:
            field_dict["description"] = description
        if recurring is not UNSET:
            field_dict["recurring"] = recurring

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        type_ = d.pop("type")

        amount = d.pop("amount")

        description = d.pop("description", UNSET)

        recurring = d.pop("recurring", UNSET)

        component_usage_item_request = cls(
            type_=type_,
            amount=amount,
            description=description,
            recurring=recurring,
        )

        component_usage_item_request.additional_properties = d
        return component_usage_item_request

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
