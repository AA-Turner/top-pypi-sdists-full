from collections.abc import Mapping
from typing import Any, TypeVar, Union
from uuid import UUID

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..models.policy_period_enum import PolicyPeriodEnum
from ..types import UNSET, Unset

T = TypeVar("T", bound="NestedCustomerUsagePolicyComponent")


@_attrs_define
class NestedCustomerUsagePolicyComponent:
    """
    Attributes:
        type_ (str):
        limit (int):
        period_name (str):
        component (UUID):
        period (Union[Unset, PolicyPeriodEnum]):
    """

    type_: str
    limit: int
    period_name: str
    component: UUID
    period: Union[Unset, PolicyPeriodEnum] = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        type_ = self.type_

        limit = self.limit

        period_name = self.period_name

        component = str(self.component)

        period: Union[Unset, int] = UNSET
        if not isinstance(self.period, Unset):
            period = self.period.value

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "type": type_,
                "limit": limit,
                "period_name": period_name,
                "component": component,
            }
        )
        if period is not UNSET:
            field_dict["period"] = period

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        type_ = d.pop("type")

        limit = d.pop("limit")

        period_name = d.pop("period_name")

        component = UUID(d.pop("component"))

        _period = d.pop("period", UNSET)
        period: Union[Unset, PolicyPeriodEnum]
        if isinstance(_period, Unset):
            period = UNSET
        else:
            period = PolicyPeriodEnum(_period)

        nested_customer_usage_policy_component = cls(
            type_=type_,
            limit=limit,
            period_name=period_name,
            component=component,
            period=period,
        )

        nested_customer_usage_policy_component.additional_properties = d
        return nested_customer_usage_policy_component

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
