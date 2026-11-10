from collections.abc import Mapping
from typing import TYPE_CHECKING, Any, TypeVar

from attrs import define as _attrs_define
from attrs import field as _attrs_field

if TYPE_CHECKING:
    from ..models.feedback_question_summary import FeedbackQuestionSummary


T = TypeVar("T", bound="FeedbackSurveySummary")


@_attrs_define
class FeedbackSurveySummary:
    """
    Attributes:
        prompted (int):
        answered (int):
        dismissed (int):
        pending (int):
        expired (int):
        questions (list['FeedbackQuestionSummary']):
    """

    prompted: int
    answered: int
    dismissed: int
    pending: int
    expired: int
    questions: list["FeedbackQuestionSummary"]
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        prompted = self.prompted

        answered = self.answered

        dismissed = self.dismissed

        pending = self.pending

        expired = self.expired

        questions = []
        for questions_item_data in self.questions:
            questions_item = questions_item_data.to_dict()
            questions.append(questions_item)

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "prompted": prompted,
                "answered": answered,
                "dismissed": dismissed,
                "pending": pending,
                "expired": expired,
                "questions": questions,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.feedback_question_summary import FeedbackQuestionSummary

        d = dict(src_dict)
        prompted = d.pop("prompted")

        answered = d.pop("answered")

        dismissed = d.pop("dismissed")

        pending = d.pop("pending")

        expired = d.pop("expired")

        questions = []
        _questions = d.pop("questions")
        for questions_item_data in _questions:
            questions_item = FeedbackQuestionSummary.from_dict(questions_item_data)

            questions.append(questions_item)

        feedback_survey_summary = cls(
            prompted=prompted,
            answered=answered,
            dismissed=dismissed,
            pending=pending,
            expired=expired,
            questions=questions,
        )

        feedback_survey_summary.additional_properties = d
        return feedback_survey_summary

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
