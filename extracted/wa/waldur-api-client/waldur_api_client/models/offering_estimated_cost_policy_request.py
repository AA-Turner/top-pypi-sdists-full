from collections.abc import Mapping
from typing import Any, TypeVar, Union, cast

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..models.policy_period_enum import PolicyPeriodEnum
from ..types import UNSET, Unset

T = TypeVar("T", bound="OfferingEstimatedCostPolicyRequest")


@_attrs_define
class OfferingEstimatedCostPolicyRequest:
    """
    Attributes:
        scope (str):
        actions (str):
        limit_cost (int):
        options (Union[Unset, Any]): Fields for saving actions extra data. Keys are name of actions.
        period (Union[Unset, PolicyPeriodEnum]):
        organization_groups (Union[Unset, list[str]]):
        apply_to_all (Union[Unset, bool]): If True, policy applies to all customers. Mutually exclusive with
            organization_groups.
    """

    scope: str
    actions: str
    limit_cost: int
    options: Union[Unset, Any] = UNSET
    period: Union[Unset, PolicyPeriodEnum] = UNSET
    organization_groups: Union[Unset, list[str]] = UNSET
    apply_to_all: Union[Unset, bool] = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        scope = self.scope

        actions = self.actions

        limit_cost = self.limit_cost

        options = self.options

        period: Union[Unset, int] = UNSET
        if not isinstance(self.period, Unset):
            period = self.period.value

        organization_groups: Union[Unset, list[str]] = UNSET
        if not isinstance(self.organization_groups, Unset):
            organization_groups = self.organization_groups

        apply_to_all = self.apply_to_all

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
        if organization_groups is not UNSET:
            field_dict["organization_groups"] = organization_groups
        if apply_to_all is not UNSET:
            field_dict["apply_to_all"] = apply_to_all

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

        organization_groups = cast(list[str], d.pop("organization_groups", UNSET))

        apply_to_all = d.pop("apply_to_all", UNSET)

        offering_estimated_cost_policy_request = cls(
            scope=scope,
            actions=actions,
            limit_cost=limit_cost,
            options=options,
            period=period,
            organization_groups=organization_groups,
            apply_to_all=apply_to_all,
        )

        offering_estimated_cost_policy_request.additional_properties = d
        return offering_estimated_cost_policy_request

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
