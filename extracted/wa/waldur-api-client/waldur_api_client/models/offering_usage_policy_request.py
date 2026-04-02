from collections.abc import Mapping
from typing import TYPE_CHECKING, Any, TypeVar, Union, cast

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..models.policy_period_enum import PolicyPeriodEnum
from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.nested_offering_component_limit_request import NestedOfferingComponentLimitRequest


T = TypeVar("T", bound="OfferingUsagePolicyRequest")


@_attrs_define
class OfferingUsagePolicyRequest:
    """
    Attributes:
        scope (str):
        actions (str):
        component_limits_set (list['NestedOfferingComponentLimitRequest']):
        options (Union[Unset, Any]): Fields for saving actions extra data. Keys are name of actions.
        organization_groups (Union[Unset, list[str]]):
        apply_to_all (Union[Unset, bool]): If True, policy applies to all customers. Mutually exclusive with
            organization_groups.
        period (Union[Unset, PolicyPeriodEnum]):
    """

    scope: str
    actions: str
    component_limits_set: list["NestedOfferingComponentLimitRequest"]
    options: Union[Unset, Any] = UNSET
    organization_groups: Union[Unset, list[str]] = UNSET
    apply_to_all: Union[Unset, bool] = UNSET
    period: Union[Unset, PolicyPeriodEnum] = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        scope = self.scope

        actions = self.actions

        component_limits_set = []
        for component_limits_set_item_data in self.component_limits_set:
            component_limits_set_item = component_limits_set_item_data.to_dict()
            component_limits_set.append(component_limits_set_item)

        options = self.options

        organization_groups: Union[Unset, list[str]] = UNSET
        if not isinstance(self.organization_groups, Unset):
            organization_groups = self.organization_groups

        apply_to_all = self.apply_to_all

        period: Union[Unset, int] = UNSET
        if not isinstance(self.period, Unset):
            period = self.period.value

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "scope": scope,
                "actions": actions,
                "component_limits_set": component_limits_set,
            }
        )
        if options is not UNSET:
            field_dict["options"] = options
        if organization_groups is not UNSET:
            field_dict["organization_groups"] = organization_groups
        if apply_to_all is not UNSET:
            field_dict["apply_to_all"] = apply_to_all
        if period is not UNSET:
            field_dict["period"] = period

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.nested_offering_component_limit_request import NestedOfferingComponentLimitRequest

        d = dict(src_dict)
        scope = d.pop("scope")

        actions = d.pop("actions")

        component_limits_set = []
        _component_limits_set = d.pop("component_limits_set")
        for component_limits_set_item_data in _component_limits_set:
            component_limits_set_item = NestedOfferingComponentLimitRequest.from_dict(component_limits_set_item_data)

            component_limits_set.append(component_limits_set_item)

        options = d.pop("options", UNSET)

        organization_groups = cast(list[str], d.pop("organization_groups", UNSET))

        apply_to_all = d.pop("apply_to_all", UNSET)

        _period = d.pop("period", UNSET)
        period: Union[Unset, PolicyPeriodEnum]
        if isinstance(_period, Unset):
            period = UNSET
        else:
            period = PolicyPeriodEnum(_period)

        offering_usage_policy_request = cls(
            scope=scope,
            actions=actions,
            component_limits_set=component_limits_set,
            options=options,
            organization_groups=organization_groups,
            apply_to_all=apply_to_all,
            period=period,
        )

        offering_usage_policy_request.additional_properties = d
        return offering_usage_policy_request

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
