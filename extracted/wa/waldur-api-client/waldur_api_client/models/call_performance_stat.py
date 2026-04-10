import datetime
from collections.abc import Mapping
from typing import Any, TypeVar, Union, cast
from uuid import UUID

from attrs import define as _attrs_define
from attrs import field as _attrs_field
from dateutil.parser import isoparse

T = TypeVar("T", bound="CallPerformanceStat")


@_attrs_define
class CallPerformanceStat:
    """
    Attributes:
        call_uuid (UUID):
        call_name (str):
        managing_organization_name (str):
        state (str):
        total_proposals (int):
        proposals_draft (int):
        proposals_submitted (int):
        proposals_in_review (int):
        proposals_accepted (int):
        proposals_rejected (int):
        proposals_canceled (int):
        acceptance_rate (float):
        total_reviews (int):
        reviews_completed (int):
        average_score (Union[None, float]):
        active_rounds (int):
        last_submission_date (Union[None, datetime.date]):
    """

    call_uuid: UUID
    call_name: str
    managing_organization_name: str
    state: str
    total_proposals: int
    proposals_draft: int
    proposals_submitted: int
    proposals_in_review: int
    proposals_accepted: int
    proposals_rejected: int
    proposals_canceled: int
    acceptance_rate: float
    total_reviews: int
    reviews_completed: int
    average_score: Union[None, float]
    active_rounds: int
    last_submission_date: Union[None, datetime.date]
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        call_uuid = str(self.call_uuid)

        call_name = self.call_name

        managing_organization_name = self.managing_organization_name

        state = self.state

        total_proposals = self.total_proposals

        proposals_draft = self.proposals_draft

        proposals_submitted = self.proposals_submitted

        proposals_in_review = self.proposals_in_review

        proposals_accepted = self.proposals_accepted

        proposals_rejected = self.proposals_rejected

        proposals_canceled = self.proposals_canceled

        acceptance_rate = self.acceptance_rate

        total_reviews = self.total_reviews

        reviews_completed = self.reviews_completed

        average_score: Union[None, float]
        average_score = self.average_score

        active_rounds = self.active_rounds

        last_submission_date: Union[None, str]
        if isinstance(self.last_submission_date, datetime.date):
            last_submission_date = self.last_submission_date.isoformat()
        else:
            last_submission_date = self.last_submission_date

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "call_uuid": call_uuid,
                "call_name": call_name,
                "managing_organization_name": managing_organization_name,
                "state": state,
                "total_proposals": total_proposals,
                "proposals_draft": proposals_draft,
                "proposals_submitted": proposals_submitted,
                "proposals_in_review": proposals_in_review,
                "proposals_accepted": proposals_accepted,
                "proposals_rejected": proposals_rejected,
                "proposals_canceled": proposals_canceled,
                "acceptance_rate": acceptance_rate,
                "total_reviews": total_reviews,
                "reviews_completed": reviews_completed,
                "average_score": average_score,
                "active_rounds": active_rounds,
                "last_submission_date": last_submission_date,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        call_uuid = UUID(d.pop("call_uuid"))

        call_name = d.pop("call_name")

        managing_organization_name = d.pop("managing_organization_name")

        state = d.pop("state")

        total_proposals = d.pop("total_proposals")

        proposals_draft = d.pop("proposals_draft")

        proposals_submitted = d.pop("proposals_submitted")

        proposals_in_review = d.pop("proposals_in_review")

        proposals_accepted = d.pop("proposals_accepted")

        proposals_rejected = d.pop("proposals_rejected")

        proposals_canceled = d.pop("proposals_canceled")

        acceptance_rate = d.pop("acceptance_rate")

        total_reviews = d.pop("total_reviews")

        reviews_completed = d.pop("reviews_completed")

        def _parse_average_score(data: object) -> Union[None, float]:
            if data is None:
                return data
            return cast(Union[None, float], data)

        average_score = _parse_average_score(d.pop("average_score"))

        active_rounds = d.pop("active_rounds")

        def _parse_last_submission_date(data: object) -> Union[None, datetime.date]:
            if data is None:
                return data
            try:
                if not isinstance(data, str):
                    raise TypeError()
                last_submission_date_type_0 = isoparse(data).date()

                return last_submission_date_type_0
            except:  # noqa: E722
                pass
            return cast(Union[None, datetime.date], data)

        last_submission_date = _parse_last_submission_date(d.pop("last_submission_date"))

        call_performance_stat = cls(
            call_uuid=call_uuid,
            call_name=call_name,
            managing_organization_name=managing_organization_name,
            state=state,
            total_proposals=total_proposals,
            proposals_draft=proposals_draft,
            proposals_submitted=proposals_submitted,
            proposals_in_review=proposals_in_review,
            proposals_accepted=proposals_accepted,
            proposals_rejected=proposals_rejected,
            proposals_canceled=proposals_canceled,
            acceptance_rate=acceptance_rate,
            total_reviews=total_reviews,
            reviews_completed=reviews_completed,
            average_score=average_score,
            active_rounds=active_rounds,
            last_submission_date=last_submission_date,
        )

        call_performance_stat.additional_properties = d
        return call_performance_stat

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
