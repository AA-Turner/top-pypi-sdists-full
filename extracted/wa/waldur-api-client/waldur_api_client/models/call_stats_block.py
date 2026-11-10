from collections.abc import Mapping
from typing import TYPE_CHECKING, Any, TypeVar

from attrs import define as _attrs_define
from attrs import field as _attrs_field

if TYPE_CHECKING:
    from ..models.call_stats_block_proposals import CallStatsBlockProposals
    from ..models.call_stats_block_reviews import CallStatsBlockReviews
    from ..models.call_stats_step import CallStatsStep


T = TypeVar("T", bound="CallStatsBlock")


@_attrs_define
class CallStatsBlock:
    """
    Attributes:
        proposals (CallStatsBlockProposals): Proposals by state (accepted = awarded), plus total.
        reviews (CallStatsBlockReviews): Reviews by state, plus total.
        admin_approved (int): Proposals whose administrative check completed as eligible.
        missing_admin_checks (int): Proposals whose administrative check is active or expired.
        missing_reviews (int): Proposals in expert review below the step's minimum reviews.
        overdue_reviews (int): Reviews still in review past their deadline.
        steps (list['CallStatsStep']): Proposals per current workflow step, over the enabled steps.
    """

    proposals: "CallStatsBlockProposals"
    reviews: "CallStatsBlockReviews"
    admin_approved: int
    missing_admin_checks: int
    missing_reviews: int
    overdue_reviews: int
    steps: list["CallStatsStep"]
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
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.call_stats_block_proposals import CallStatsBlockProposals
        from ..models.call_stats_block_reviews import CallStatsBlockReviews
        from ..models.call_stats_step import CallStatsStep

        d = dict(src_dict)
        proposals = CallStatsBlockProposals.from_dict(d.pop("proposals"))

        reviews = CallStatsBlockReviews.from_dict(d.pop("reviews"))

        admin_approved = d.pop("admin_approved")

        missing_admin_checks = d.pop("missing_admin_checks")

        missing_reviews = d.pop("missing_reviews")

        overdue_reviews = d.pop("overdue_reviews")

        steps = []
        _steps = d.pop("steps")
        for steps_item_data in _steps:
            steps_item = CallStatsStep.from_dict(steps_item_data)

            steps.append(steps_item)

        call_stats_block = cls(
            proposals=proposals,
            reviews=reviews,
            admin_approved=admin_approved,
            missing_admin_checks=missing_admin_checks,
            missing_reviews=missing_reviews,
            overdue_reviews=overdue_reviews,
            steps=steps,
        )

        call_stats_block.additional_properties = d
        return call_stats_block

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
