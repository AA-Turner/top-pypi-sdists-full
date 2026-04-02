import datetime
from collections.abc import Mapping
from typing import Any, TypeVar, Union, cast
from uuid import UUID

from attrs import define as _attrs_define
from attrs import field as _attrs_field
from dateutil.parser import isoparse

T = TypeVar("T", bound="ReviewerStats")


@_attrs_define
class ReviewerStats:
    """
    Attributes:
        uuid (UUID):
        total_reviews_completed (int):
        total_reviews_declined (int):
        total_reviews_timeout (int):
        average_review_time_days (Union[None, float]):
        average_score_given (Union[None, float]):
        last_review_date (Union[None, datetime.date]):
        quality_rating (Union[None, float]):
        quality_rating_count (int):
    """

    uuid: UUID
    total_reviews_completed: int
    total_reviews_declined: int
    total_reviews_timeout: int
    average_review_time_days: Union[None, float]
    average_score_given: Union[None, float]
    last_review_date: Union[None, datetime.date]
    quality_rating: Union[None, float]
    quality_rating_count: int
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        uuid = str(self.uuid)

        total_reviews_completed = self.total_reviews_completed

        total_reviews_declined = self.total_reviews_declined

        total_reviews_timeout = self.total_reviews_timeout

        average_review_time_days: Union[None, float]
        average_review_time_days = self.average_review_time_days

        average_score_given: Union[None, float]
        average_score_given = self.average_score_given

        last_review_date: Union[None, str]
        if isinstance(self.last_review_date, datetime.date):
            last_review_date = self.last_review_date.isoformat()
        else:
            last_review_date = self.last_review_date

        quality_rating: Union[None, float]
        quality_rating = self.quality_rating

        quality_rating_count = self.quality_rating_count

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "uuid": uuid,
                "total_reviews_completed": total_reviews_completed,
                "total_reviews_declined": total_reviews_declined,
                "total_reviews_timeout": total_reviews_timeout,
                "average_review_time_days": average_review_time_days,
                "average_score_given": average_score_given,
                "last_review_date": last_review_date,
                "quality_rating": quality_rating,
                "quality_rating_count": quality_rating_count,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        uuid = UUID(d.pop("uuid"))

        total_reviews_completed = d.pop("total_reviews_completed")

        total_reviews_declined = d.pop("total_reviews_declined")

        total_reviews_timeout = d.pop("total_reviews_timeout")

        def _parse_average_review_time_days(data: object) -> Union[None, float]:
            if data is None:
                return data
            return cast(Union[None, float], data)

        average_review_time_days = _parse_average_review_time_days(d.pop("average_review_time_days"))

        def _parse_average_score_given(data: object) -> Union[None, float]:
            if data is None:
                return data
            return cast(Union[None, float], data)

        average_score_given = _parse_average_score_given(d.pop("average_score_given"))

        def _parse_last_review_date(data: object) -> Union[None, datetime.date]:
            if data is None:
                return data
            try:
                if not isinstance(data, str):
                    raise TypeError()
                last_review_date_type_0 = isoparse(data).date()

                return last_review_date_type_0
            except:  # noqa: E722
                pass
            return cast(Union[None, datetime.date], data)

        last_review_date = _parse_last_review_date(d.pop("last_review_date"))

        def _parse_quality_rating(data: object) -> Union[None, float]:
            if data is None:
                return data
            return cast(Union[None, float], data)

        quality_rating = _parse_quality_rating(d.pop("quality_rating"))

        quality_rating_count = d.pop("quality_rating_count")

        reviewer_stats = cls(
            uuid=uuid,
            total_reviews_completed=total_reviews_completed,
            total_reviews_declined=total_reviews_declined,
            total_reviews_timeout=total_reviews_timeout,
            average_review_time_days=average_review_time_days,
            average_score_given=average_score_given,
            last_review_date=last_review_date,
            quality_rating=quality_rating,
            quality_rating_count=quality_rating_count,
        )

        reviewer_stats.additional_properties = d
        return reviewer_stats

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
