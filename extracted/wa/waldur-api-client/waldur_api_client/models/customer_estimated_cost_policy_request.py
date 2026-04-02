from collections.abc import Mapping
from typing import Any, TypeVar, Union

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..models.policy_period_enum import PolicyPeriodEnum
from ..types import UNSET, Unset

T = TypeVar("T", bound="CustomerEstimatedCostPolicyRequest")


@_attrs_define
class CustomerEstimatedCostPolicyRequest:
    """
    Attributes:
        scope (str):
        actions (str):
        limit_cost (int):
        options (Union[Unset, Any]): Fields for saving actions extra data. Keys are name of actions.
        period (Union[Unset, PolicyPeriodEnum]):
    """

    scope: str
    actions: str
    limit_cost: int
    options: Union[Unset, Any] = UNSET
    period: Union[Unset, PolicyPeriodEnum] = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        scope = self.scope

        actions = self.actions

        limit_cost = self.limit_cost

        options = self.options

        period: Union[Unset, int] = UNSET
        if not isinstance(self.period, Unset):
            period = self.period.value

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "scope": scope,
                "actions": actions,
                "limit_cost": limit_cost,
            }
        )
        if options is not UNSET:
            field_dict["options"] = options
        if period is not UNSET:
            field_dict["period"] = period

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        scope = d.pop("scope")

        actions = d.pop("actions")

        limit_cost = d.pop("limit_cost")

        options = d.pop("options", UNSET)

        _period = d.pop("period", UNSET)
        period: Union[Unset, PolicyPeriodEnum]
        if isinstance(_period, Unset):
            period = UNSET
        else:
            period = PolicyPeriodEnum(_period)

        customer_estimated_cost_policy_request = cls(
            scope=scope,
            actions=actions,
            limit_cost=limit_cost,
            options=options,
            period=period,
        )

        customer_estimated_cost_policy_request.additional_properties = d
        return customer_estimated_cost_policy_request

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
