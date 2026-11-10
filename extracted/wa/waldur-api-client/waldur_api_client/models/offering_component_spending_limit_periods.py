from collections.abc import Mapping
from typing import TYPE_CHECKING, Any, TypeVar

from attrs import define as _attrs_define
from attrs import field as _attrs_field

if TYPE_CHECKING:
    from ..models.spending_limit_bounds import SpendingLimitBounds


T = TypeVar("T", bound="OfferingComponentSpendingLimitPeriods")


@_attrs_define
class OfferingComponentSpendingLimitPeriods:
    """Periods (day, week, month, quarter, year, total) for which customers can set a spending limit on this usage-based
    component; total counts all the usage since the resource started and never resets. Day and week need the integration
    to report usage per day. Empty when customers cannot set spending limits.

    """

    additional_properties: dict[str, "SpendingLimitBounds"] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        field_dict: dict[str, Any] = {}
        for prop_name, prop in self.additional_properties.items():
            field_dict[prop_name] = prop.to_dict()

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.spending_limit_bounds import SpendingLimitBounds

        d = dict(src_dict)
        offering_component_spending_limit_periods = cls()

        additional_properties = {}
        for prop_name, prop_dict in d.items():
            additional_property = SpendingLimitBounds.from_dict(prop_dict)

            additional_properties[prop_name] = additional_property

        offering_component_spending_limit_periods.additional_properties = additional_properties
        return offering_component_spending_limit_periods

    @property
    def additional_keys(self) -> list[str]:
        return list(self.additional_properties.keys())

    def __getitem__(self, key: str) -> "SpendingLimitBounds":
        return self.additional_properties[key]

    def __setitem__(self, key: str, value: "SpendingLimitBounds") -> None:
        self.additional_properties[key] = value

    def __delitem__(self, key: str) -> None:
        del self.additional_properties[key]

    def __contains__(self, key: str) -> bool:
        return key in self.additional_properties
