from collections.abc import Mapping
from typing import Any, TypeVar

from attrs import define as _attrs_define
from attrs import field as _attrs_field

T = TypeVar("T", bound="DashboardCallManagerStats")


@_attrs_define
class DashboardCallManagerStats:
    """
    Attributes:
        pending_assessments (int):
        active_calls (int):
        reviews_due_soon (int):
        reviews_due_within_days (int):
    """

    pending_assessments: int
    active_calls: int
    reviews_due_soon: int
    reviews_due_within_days: int
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        pending_assessments = self.pending_assessments

        active_calls = self.active_calls

        reviews_due_soon = self.reviews_due_soon

        reviews_due_within_days = self.reviews_due_within_days

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "pending_assessments": pending_assessments,
                "active_calls": active_calls,
                "reviews_due_soon": reviews_due_soon,
                "reviews_due_within_days": reviews_due_within_days,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        pending_assessments = d.pop("pending_assessments")

        active_calls = d.pop("active_calls")

        reviews_due_soon = d.pop("reviews_due_soon")

        reviews_due_within_days = d.pop("reviews_due_within_days")

        dashboard_call_manager_stats = cls(
            pending_assessments=pending_assessments,
            active_calls=active_calls,
            reviews_due_soon=reviews_due_soon,
            reviews_due_within_days=reviews_due_within_days,
        )

        dashboard_call_manager_stats.additional_properties = d
        return dashboard_call_manager_stats

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
