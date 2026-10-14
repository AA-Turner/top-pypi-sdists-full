from collections.abc import Mapping
from typing import Any, TypeVar, Union, cast

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..models.missing_usage_policy_enum import MissingUsagePolicyEnum
from ..types import UNSET, Unset

T = TypeVar("T", bound="ComponentUsageItemRequest")


@_attrs_define
class ComponentUsageItemRequest:
    """
    Attributes:
        type_ (str): Type of the component
        amount (str): Usage amount
        description (Union[Unset, str]): Optional description of usage
        missing_usage_policy (Union[Unset, MissingUsagePolicyEnum]):
        recurring (Union[None, Unset, bool]): Deprecated, use missing_usage_policy instead. True is equivalent to
            missing_usage_policy='reuse'.
    """

    type_: str
    amount: str
    description: Union[Unset, str] = UNSET
    missing_usage_policy: Union[Unset, MissingUsagePolicyEnum] = UNSET
    recurring: Union[None, Unset, bool] = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        type_ = self.type_

        amount = self.amount

        description = self.description

        missing_usage_policy: Union[Unset, str] = UNSET
        if not isinstance(self.missing_usage_policy, Unset):
            missing_usage_policy = self.missing_usage_policy.value

        recurring: Union[None, Unset, bool]
        if isinstance(self.recurring, Unset):
            recurring = UNSET
        else:
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
        if missing_usage_policy is not UNSET:
            field_dict["missing_usage_policy"] = missing_usage_policy
        if recurring is not UNSET:
            field_dict["recurring"] = recurring

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        type_ = d.pop("type")

        amount = d.pop("amount")

        description = d.pop("description", UNSET)

        _missing_usage_policy = d.pop("missing_usage_policy", UNSET)
        missing_usage_policy: Union[Unset, MissingUsagePolicyEnum]
        if isinstance(_missing_usage_policy, Unset):
            missing_usage_policy = UNSET
        else:
            missing_usage_policy = MissingUsagePolicyEnum(_missing_usage_policy)

        def _parse_recurring(data: object) -> Union[None, Unset, bool]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(Union[None, Unset, bool], data)

        recurring = _parse_recurring(d.pop("recurring", UNSET))

        component_usage_item_request = cls(
            type_=type_,
            amount=amount,
            description=description,
            missing_usage_policy=missing_usage_policy,
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
