from collections.abc import Mapping
from typing import Any, TypeVar, Union, cast
from uuid import UUID

from attrs import define as _attrs_define
from attrs import field as _attrs_field

T = TypeVar("T", bound="ReviewProgressStat")


@_attrs_define
class ReviewProgressStat:
    """
    Attributes:
        reviewer_uuid (UUID):
        reviewer_name (str):
        reviewer_email (str):
        total_assigned (int):
        pending (int):
        in_progress (int):
        completed (int):
        declined (int):
        average_score (Union[None, float]):
        average_review_time_days (Union[None, float]):
        completion_rate (float):
    """

    reviewer_uuid: UUID
    reviewer_name: str
    reviewer_email: str
    total_assigned: int
    pending: int
    in_progress: int
    completed: int
    declined: int
    average_score: Union[None, float]
    average_review_time_days: Union[None, float]
    completion_rate: float
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        reviewer_uuid = str(self.reviewer_uuid)

        reviewer_name = self.reviewer_name

        reviewer_email = self.reviewer_email

        total_assigned = self.total_assigned

        pending = self.pending

        in_progress = self.in_progress

        completed = self.completed

        declined = self.declined

        average_score: Union[None, float]
        average_score = self.average_score

        average_review_time_days: Union[None, float]
        average_review_time_days = self.average_review_time_days

        completion_rate = self.completion_rate

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "reviewer_uuid": reviewer_uuid,
                "reviewer_name": reviewer_name,
                "reviewer_email": reviewer_email,
                "total_assigned": total_assigned,
                "pending": pending,
                "in_progress": in_progress,
                "completed": completed,
                "declined": declined,
                "average_score": average_score,
                "average_review_time_days": average_review_time_days,
                "completion_rate": completion_rate,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        reviewer_uuid = UUID(d.pop("reviewer_uuid"))

        reviewer_name = d.pop("reviewer_name")

        reviewer_email = d.pop("reviewer_email")

        total_assigned = d.pop("total_assigned")

        pending = d.pop("pending")

        in_progress = d.pop("in_progress")

        completed = d.pop("completed")

        declined = d.pop("declined")

        def _parse_average_score(data: object) -> Union[None, float]:
            if data is None:
                return data
            return cast(Union[None, float], data)

        average_score = _parse_average_score(d.pop("average_score"))

        def _parse_average_review_time_days(data: object) -> Union[None, float]:
            if data is None:
                return data
            return cast(Union[None, float], data)

        average_review_time_days = _parse_average_review_time_days(d.pop("average_review_time_days"))

        completion_rate = d.pop("completion_rate")

        review_progress_stat = cls(
            reviewer_uuid=reviewer_uuid,
            reviewer_name=reviewer_name,
            reviewer_email=reviewer_email,
            total_assigned=total_assigned,
            pending=pending,
            in_progress=in_progress,
            completed=completed,
            declined=declined,
            average_score=average_score,
            average_review_time_days=average_review_time_days,
            completion_rate=completion_rate,
        )

        review_progress_stat.additional_properties = d
        return review_progress_stat

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
