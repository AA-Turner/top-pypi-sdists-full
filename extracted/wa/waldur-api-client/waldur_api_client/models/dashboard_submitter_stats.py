from collections.abc import Mapping
from typing import Any, TypeVar

from attrs import define as _attrs_define
from attrs import field as _attrs_field

T = TypeVar("T", bound="DashboardSubmitterStats")


@_attrs_define
class DashboardSubmitterStats:
    """
    Attributes:
        total (int):
        draft (int):
        submitted (int):
        in_review (int):
        accepted (int):
        rejected (int):
        canceled (int):
    """

    total: int
    draft: int
    submitted: int
    in_review: int
    accepted: int
    rejected: int
    canceled: int
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        total = self.total

        draft = self.draft

        submitted = self.submitted

        in_review = self.in_review

        accepted = self.accepted

        rejected = self.rejected

        canceled = self.canceled

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "total": total,
                "draft": draft,
                "submitted": submitted,
                "in_review": in_review,
                "accepted": accepted,
                "rejected": rejected,
                "canceled": canceled,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        total = d.pop("total")

        draft = d.pop("draft")

        submitted = d.pop("submitted")

        in_review = d.pop("in_review")

        accepted = d.pop("accepted")

        rejected = d.pop("rejected")

        canceled = d.pop("canceled")

        dashboard_submitter_stats = cls(
            total=total,
            draft=draft,
            submitted=submitted,
            in_review=in_review,
            accepted=accepted,
            rejected=rejected,
            canceled=canceled,
        )

        dashboard_submitter_stats.additional_properties = d
        return dashboard_submitter_stats

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
