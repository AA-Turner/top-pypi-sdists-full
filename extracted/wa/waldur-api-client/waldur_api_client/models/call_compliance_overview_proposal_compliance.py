import datetime
from collections.abc import Mapping
from typing import TYPE_CHECKING, Any, TypeVar, Union, cast

from attrs import define as _attrs_define
from attrs import field as _attrs_field
from dateutil.parser import isoparse

if TYPE_CHECKING:
    from ..models.call_compliance_overview_proposal_review_trigger import CallComplianceOverviewProposalReviewTrigger


T = TypeVar("T", bound="CallComplianceOverviewProposalCompliance")


@_attrs_define
class CallComplianceOverviewProposalCompliance:
    """
    Attributes:
        is_completed (bool):
        requires_review (bool):
        completion_percentage (int):
        reviewed_by (Union[None, str]):
        reviewed_at (Union[None, datetime.datetime]):
        review_triggers (list['CallComplianceOverviewProposalReviewTrigger']):
        unanswered_required_count (int):
    """

    is_completed: bool
    requires_review: bool
    completion_percentage: int
    reviewed_by: Union[None, str]
    reviewed_at: Union[None, datetime.datetime]
    review_triggers: list["CallComplianceOverviewProposalReviewTrigger"]
    unanswered_required_count: int
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        is_completed = self.is_completed

        requires_review = self.requires_review

        completion_percentage = self.completion_percentage

        reviewed_by: Union[None, str]
        reviewed_by = self.reviewed_by

        reviewed_at: Union[None, str]
        if isinstance(self.reviewed_at, datetime.datetime):
            reviewed_at = self.reviewed_at.isoformat()
        else:
            reviewed_at = self.reviewed_at

        review_triggers = []
        for review_triggers_item_data in self.review_triggers:
            review_triggers_item = review_triggers_item_data.to_dict()
            review_triggers.append(review_triggers_item)

        unanswered_required_count = self.unanswered_required_count

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "is_completed": is_completed,
                "requires_review": requires_review,
                "completion_percentage": completion_percentage,
                "reviewed_by": reviewed_by,
                "reviewed_at": reviewed_at,
                "review_triggers": review_triggers,
                "unanswered_required_count": unanswered_required_count,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.call_compliance_overview_proposal_review_trigger import (
            CallComplianceOverviewProposalReviewTrigger,
        )

        d = dict(src_dict)
        is_completed = d.pop("is_completed")

        requires_review = d.pop("requires_review")

        completion_percentage = d.pop("completion_percentage")

        def _parse_reviewed_by(data: object) -> Union[None, str]:
            if data is None:
                return data
            return cast(Union[None, str], data)

        reviewed_by = _parse_reviewed_by(d.pop("reviewed_by"))

        def _parse_reviewed_at(data: object) -> Union[None, datetime.datetime]:
            if data is None:
                return data
            try:
                if not isinstance(data, str):
                    raise TypeError()
                reviewed_at_type_0 = isoparse(data)

                return reviewed_at_type_0
            except:  # noqa: E722
                pass
            return cast(Union[None, datetime.datetime], data)

        reviewed_at = _parse_reviewed_at(d.pop("reviewed_at"))

        review_triggers = []
        _review_triggers = d.pop("review_triggers")
        for review_triggers_item_data in _review_triggers:
            review_triggers_item = CallComplianceOverviewProposalReviewTrigger.from_dict(review_triggers_item_data)

            review_triggers.append(review_triggers_item)

        unanswered_required_count = d.pop("unanswered_required_count")

        call_compliance_overview_proposal_compliance = cls(
            is_completed=is_completed,
            requires_review=requires_review,
            completion_percentage=completion_percentage,
            reviewed_by=reviewed_by,
            reviewed_at=reviewed_at,
            review_triggers=review_triggers,
            unanswered_required_count=unanswered_required_count,
        )

        call_compliance_overview_proposal_compliance.additional_properties = d
        return call_compliance_overview_proposal_compliance

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
