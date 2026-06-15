from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar

from attrs import define as _attrs_define
from attrs import field as _attrs_field


T = TypeVar("T", bound="PlanDefinitionOverageRates")


@_attrs_define
class PlanDefinitionOverageRates:
    """For metered products only: map of metered limit key to the per-unit overage price in micro-USD ($0.000001) charged
    for each unit beyond the plan's included allotment. A rate of `0` means the plan stops at its allotment with no
    overage. Omitted for products that are not metered.

    """

    additional_properties: dict[str, int] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        plan_definition_overage_rates = cls()

        plan_definition_overage_rates.additional_properties = d
        return plan_definition_overage_rates

    @property
    def additional_keys(self) -> list[str]:
        return list(self.additional_properties.keys())

    def __getitem__(self, key: str) -> int:
        return self.additional_properties[key]

    def __setitem__(self, key: str, value: int) -> None:
        self.additional_properties[key] = value

    def __delitem__(self, key: str) -> None:
        del self.additional_properties[key]

    def __contains__(self, key: str) -> bool:
        return key in self.additional_properties
