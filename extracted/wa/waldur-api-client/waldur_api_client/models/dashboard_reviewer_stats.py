from collections.abc import Mapping
from typing import TYPE_CHECKING, Any, TypeVar

from attrs import define as _attrs_define
from attrs import field as _attrs_field

if TYPE_CHECKING:
    from ..models.dashboard_review_deadline import DashboardReviewDeadline


T = TypeVar("T", bound="DashboardReviewerStats")


@_attrs_define
class DashboardReviewerStats:
    """
    Attributes:
        assigned (int):
        pending (int):
        completed (int):
        deadlines (list['DashboardReviewDeadline']):
        deadlines_total (int):
    """

    assigned: int
    pending: int
    completed: int
    deadlines: list["DashboardReviewDeadline"]
    deadlines_total: int
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        assigned = self.assigned

        pending = self.pending

        completed = self.completed

        deadlines = []
        for deadlines_item_data in self.deadlines:
            deadlines_item = deadlines_item_data.to_dict()
            deadlines.append(deadlines_item)

        deadlines_total = self.deadlines_total

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "assigned": assigned,
                "pending": pending,
                "completed": completed,
                "deadlines": deadlines,
                "deadlines_total": deadlines_total,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.dashboard_review_deadline import DashboardReviewDeadline

        d = dict(src_dict)
        assigned = d.pop("assigned")

        pending = d.pop("pending")

        completed = d.pop("completed")

        deadlines = []
        _deadlines = d.pop("deadlines")
        for deadlines_item_data in _deadlines:
            deadlines_item = DashboardReviewDeadline.from_dict(deadlines_item_data)

            deadlines.append(deadlines_item)

        deadlines_total = d.pop("deadlines_total")

        dashboard_reviewer_stats = cls(
            assigned=assigned,
            pending=pending,
            completed=completed,
            deadlines=deadlines,
            deadlines_total=deadlines_total,
        )

        dashboard_reviewer_stats.additional_properties = d
        return dashboard_reviewer_stats

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
