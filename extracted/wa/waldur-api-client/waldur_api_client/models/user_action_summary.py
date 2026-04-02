from collections.abc import Mapping
from typing import TYPE_CHECKING, Any, TypeVar

from attrs import define as _attrs_define
from attrs import field as _attrs_field

if TYPE_CHECKING:
    from ..models.user_action_summary_by_type import UserActionSummaryByType
    from ..models.user_action_summary_by_urgency import UserActionSummaryByUrgency


T = TypeVar("T", bound="UserActionSummary")


@_attrs_define
class UserActionSummary:
    """
    Attributes:
        total (int):
        by_urgency (UserActionSummaryByUrgency):
        by_type (UserActionSummaryByType):
        overdue (int):
    """

    total: int
    by_urgency: "UserActionSummaryByUrgency"
    by_type: "UserActionSummaryByType"
    overdue: int
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        total = self.total

        by_urgency = self.by_urgency.to_dict()

        by_type = self.by_type.to_dict()

        overdue = self.overdue

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "total": total,
                "by_urgency": by_urgency,
                "by_type": by_type,
                "overdue": overdue,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.user_action_summary_by_type import UserActionSummaryByType
        from ..models.user_action_summary_by_urgency import UserActionSummaryByUrgency

        d = dict(src_dict)
        total = d.pop("total")

        by_urgency = UserActionSummaryByUrgency.from_dict(d.pop("by_urgency"))

        by_type = UserActionSummaryByType.from_dict(d.pop("by_type"))

        overdue = d.pop("overdue")

        user_action_summary = cls(
            total=total,
            by_urgency=by_urgency,
            by_type=by_type,
            overdue=overdue,
        )

        user_action_summary.additional_properties = d
        return user_action_summary

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
