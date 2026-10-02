from collections.abc import Mapping
from typing import Any, TypeVar, cast

from attrs import define as _attrs_define
from attrs import field as _attrs_field

T = TypeVar("T", bound="DuplicateOfferingMergePlan")


@_attrs_define
class DuplicateOfferingMergePlan:
    """
    Attributes:
        duplicate_id (int):
        duplicate_name (str):
        keeper_id (int):
        keeper_name (str):
        action (str): delete (nothing attached), merge, or skip.
        is_empty (bool):
        resource_count (int):
        order_count (int):
        plan_period_count (int):
        component_usage_count (int):
        component_quota_count (int):
        blockers (list[str]):
    """

    duplicate_id: int
    duplicate_name: str
    keeper_id: int
    keeper_name: str
    action: str
    is_empty: bool
    resource_count: int
    order_count: int
    plan_period_count: int
    component_usage_count: int
    component_quota_count: int
    blockers: list[str]
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        duplicate_id = self.duplicate_id

        duplicate_name = self.duplicate_name

        keeper_id = self.keeper_id

        keeper_name = self.keeper_name

        action = self.action

        is_empty = self.is_empty

        resource_count = self.resource_count

        order_count = self.order_count

        plan_period_count = self.plan_period_count

        component_usage_count = self.component_usage_count

        component_quota_count = self.component_quota_count

        blockers = self.blockers

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "duplicate_id": duplicate_id,
                "duplicate_name": duplicate_name,
                "keeper_id": keeper_id,
                "keeper_name": keeper_name,
                "action": action,
                "is_empty": is_empty,
                "resource_count": resource_count,
                "order_count": order_count,
                "plan_period_count": plan_period_count,
                "component_usage_count": component_usage_count,
                "component_quota_count": component_quota_count,
                "blockers": blockers,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        duplicate_id = d.pop("duplicate_id")

        duplicate_name = d.pop("duplicate_name")

        keeper_id = d.pop("keeper_id")

        keeper_name = d.pop("keeper_name")

        action = d.pop("action")

        is_empty = d.pop("is_empty")

        resource_count = d.pop("resource_count")

        order_count = d.pop("order_count")

        plan_period_count = d.pop("plan_period_count")

        component_usage_count = d.pop("component_usage_count")

        component_quota_count = d.pop("component_quota_count")

        blockers = cast(list[str], d.pop("blockers"))

        duplicate_offering_merge_plan = cls(
            duplicate_id=duplicate_id,
            duplicate_name=duplicate_name,
            keeper_id=keeper_id,
            keeper_name=keeper_name,
            action=action,
            is_empty=is_empty,
            resource_count=resource_count,
            order_count=order_count,
            plan_period_count=plan_period_count,
            component_usage_count=component_usage_count,
            component_quota_count=component_quota_count,
            blockers=blockers,
        )

        duplicate_offering_merge_plan.additional_properties = d
        return duplicate_offering_merge_plan

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
