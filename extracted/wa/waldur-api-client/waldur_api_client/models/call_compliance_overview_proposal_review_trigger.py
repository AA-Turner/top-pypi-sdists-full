from collections.abc import Mapping
from typing import TYPE_CHECKING, Any, TypeVar

from attrs import define as _attrs_define
from attrs import field as _attrs_field

if TYPE_CHECKING:
    from ..models.call_compliance_overview_proposal_review_trigger_answer import (
        CallComplianceOverviewProposalReviewTriggerAnswer,
    )
    from ..models.call_compliance_overview_proposal_review_trigger_trigger_value import (
        CallComplianceOverviewProposalReviewTriggerTriggerValue,
    )


T = TypeVar("T", bound="CallComplianceOverviewProposalReviewTrigger")


@_attrs_define
class CallComplianceOverviewProposalReviewTrigger:
    """
    Attributes:
        question (str):
        answer (CallComplianceOverviewProposalReviewTriggerAnswer):
        trigger_value (CallComplianceOverviewProposalReviewTriggerTriggerValue):
        operator (str):
    """

    question: str
    answer: "CallComplianceOverviewProposalReviewTriggerAnswer"
    trigger_value: "CallComplianceOverviewProposalReviewTriggerTriggerValue"
    operator: str
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        question = self.question

        answer = self.answer.to_dict()

        trigger_value = self.trigger_value.to_dict()

        operator = self.operator

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "question": question,
                "answer": answer,
                "trigger_value": trigger_value,
                "operator": operator,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.call_compliance_overview_proposal_review_trigger_answer import (
            CallComplianceOverviewProposalReviewTriggerAnswer,
        )
        from ..models.call_compliance_overview_proposal_review_trigger_trigger_value import (
            CallComplianceOverviewProposalReviewTriggerTriggerValue,
        )

        d = dict(src_dict)
        question = d.pop("question")

        answer = CallComplianceOverviewProposalReviewTriggerAnswer.from_dict(d.pop("answer"))

        trigger_value = CallComplianceOverviewProposalReviewTriggerTriggerValue.from_dict(d.pop("trigger_value"))

        operator = d.pop("operator")

        call_compliance_overview_proposal_review_trigger = cls(
            question=question,
            answer=answer,
            trigger_value=trigger_value,
            operator=operator,
        )

        call_compliance_overview_proposal_review_trigger.additional_properties = d
        return call_compliance_overview_proposal_review_trigger

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
