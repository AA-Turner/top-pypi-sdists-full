import datetime
from collections.abc import Mapping
from typing import TYPE_CHECKING, Any, TypeVar
from uuid import UUID

from attrs import define as _attrs_define
from attrs import field as _attrs_field
from dateutil.parser import isoparse

if TYPE_CHECKING:
    from ..models.call_stats_round_proposals import CallStatsRoundProposals
    from ..models.call_stats_round_reviews import CallStatsRoundReviews
    from ..models.call_stats_step import CallStatsStep


T = TypeVar("T", bound="CallStatsRound")


@_attrs_define
class CallStatsRound:
    """
    Attributes:
        proposals (CallStatsRoundProposals): Proposals by state (accepted = awarded), plus total.
        reviews (CallStatsRoundReviews): Reviews by state, plus total.
        admin_approved (int): Proposals whose administrative check completed as eligible.
        missing_admin_checks (int): Proposals whose administrative check is active or expired.
        missing_reviews (int): Proposals in expert review below the step's minimum reviews.
        overdue_reviews (int): Reviews still in review past their deadline.
        steps (list['CallStatsStep']): Proposals per current workflow step, over the enabled steps.
        uuid (UUID):
        slug (str):
        start_time (datetime.datetime):
        cutoff_time (datetime.datetime):
    """

    proposals: "CallStatsRoundProposals"
    reviews: "CallStatsRoundReviews"
    admin_approved: int
    missing_admin_checks: int
    missing_reviews: int
    overdue_reviews: int
    steps: list["CallStatsStep"]
    uuid: UUID
    slug: str
    start_time: datetime.datetime
    cutoff_time: datetime.datetime
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        proposals = self.proposals.to_dict()

        reviews = self.reviews.to_dict()

        admin_approved = self.admin_approved

        missing_admin_checks = self.missing_admin_checks

        missing_reviews = self.missing_reviews

        overdue_reviews = self.overdue_reviews

        steps = []
        for steps_item_data in self.steps:
            steps_item = steps_item_data.to_dict()
            steps.append(steps_item)

        uuid = str(self.uuid)

        slug = self.slug

        start_time = self.start_time.isoformat()

        cutoff_time = self.cutoff_time.isoformat()

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "proposals": proposals,
                "reviews": reviews,
                "admin_approved": admin_approved,
                "missing_admin_checks": missing_admin_checks,
                "missing_reviews": missing_reviews,
                "overdue_reviews": overdue_reviews,
                "steps": steps,
                "uuid": uuid,
                "slug": slug,
                "start_time": start_time,
                "cutoff_time": cutoff_time,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.call_stats_round_proposals import CallStatsRoundProposals
        from ..models.call_stats_round_reviews import CallStatsRoundReviews
        from ..models.call_stats_step import CallStatsStep

        d = dict(src_dict)
        proposals = CallStatsRoundProposals.from_dict(d.pop("proposals"))

        reviews = CallStatsRoundReviews.from_dict(d.pop("reviews"))

        admin_approved = d.pop("admin_approved")

        missing_admin_checks = d.pop("missing_admin_checks")

        missing_reviews = d.pop("missing_reviews")

        overdue_reviews = d.pop("overdue_reviews")

        steps = []
        _steps = d.pop("steps")
        for steps_item_data in _steps:
            steps_item = CallStatsStep.from_dict(steps_item_data)

            steps.append(steps_item)

        uuid = UUID(d.pop("uuid"))

        slug = d.pop("slug")

        start_time = isoparse(d.pop("start_time"))

        cutoff_time = isoparse(d.pop("cutoff_time"))

        call_stats_round = cls(
            proposals=proposals,
            reviews=reviews,
            admin_approved=admin_approved,
            missing_admin_checks=missing_admin_checks,
            missing_reviews=missing_reviews,
            overdue_reviews=overdue_reviews,
            steps=steps,
            uuid=uuid,
            slug=slug,
            start_time=start_time,
            cutoff_time=cutoff_time,
        )

        call_stats_round.additional_properties = d
        return call_stats_round

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
