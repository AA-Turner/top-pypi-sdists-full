from collections.abc import Mapping
from typing import TYPE_CHECKING, Any, TypeVar

from attrs import define as _attrs_define
from attrs import field as _attrs_field

if TYPE_CHECKING:
    from ..models.checklist_completion_reviewer import ChecklistCompletionReviewer
    from ..models.checklist_reviewer_response_checklist import ChecklistReviewerResponseChecklist
    from ..models.question_with_answer_reviewer import QuestionWithAnswerReviewer


T = TypeVar("T", bound="ChecklistReviewerResponse")


@_attrs_define
class ChecklistReviewerResponse:
    """
    Attributes:
        checklist (ChecklistReviewerResponseChecklist):
        completion (ChecklistCompletionReviewer):
        questions (list['QuestionWithAnswerReviewer']):
    """

    checklist: "ChecklistReviewerResponseChecklist"
    completion: "ChecklistCompletionReviewer"
    questions: list["QuestionWithAnswerReviewer"]
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        checklist = self.checklist.to_dict()

        completion = self.completion.to_dict()

        questions = []
        for questions_item_data in self.questions:
            questions_item = questions_item_data.to_dict()
            questions.append(questions_item)

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "checklist": checklist,
                "completion": completion,
                "questions": questions,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.checklist_completion_reviewer import ChecklistCompletionReviewer
        from ..models.checklist_reviewer_response_checklist import ChecklistReviewerResponseChecklist
        from ..models.question_with_answer_reviewer import QuestionWithAnswerReviewer

        d = dict(src_dict)
        checklist = ChecklistReviewerResponseChecklist.from_dict(d.pop("checklist"))

        completion = ChecklistCompletionReviewer.from_dict(d.pop("completion"))

        questions = []
        _questions = d.pop("questions")
        for questions_item_data in _questions:
            questions_item = QuestionWithAnswerReviewer.from_dict(questions_item_data)

            questions.append(questions_item)

        checklist_reviewer_response = cls(
            checklist=checklist,
            completion=completion,
            questions=questions,
        )

        checklist_reviewer_response.additional_properties = d
        return checklist_reviewer_response

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
