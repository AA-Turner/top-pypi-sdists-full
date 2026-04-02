from collections.abc import Mapping
from typing import TYPE_CHECKING, Any, TypeVar

from attrs import define as _attrs_define
from attrs import field as _attrs_field

if TYPE_CHECKING:
    from ..models.checklist_template_checklist import ChecklistTemplateChecklist
    from ..models.question import Question


T = TypeVar("T", bound="ChecklistTemplate")


@_attrs_define
class ChecklistTemplate:
    """
    Attributes:
        checklist (ChecklistTemplateChecklist):
        questions (list['Question']):
        initial_visible_questions (list['Question']):
    """

    checklist: "ChecklistTemplateChecklist"
    questions: list["Question"]
    initial_visible_questions: list["Question"]
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        checklist = self.checklist.to_dict()

        questions = []
        for questions_item_data in self.questions:
            questions_item = questions_item_data.to_dict()
            questions.append(questions_item)

        initial_visible_questions = []
        for initial_visible_questions_item_data in self.initial_visible_questions:
            initial_visible_questions_item = initial_visible_questions_item_data.to_dict()
            initial_visible_questions.append(initial_visible_questions_item)

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "checklist": checklist,
                "questions": questions,
                "initial_visible_questions": initial_visible_questions,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.checklist_template_checklist import ChecklistTemplateChecklist
        from ..models.question import Question

        d = dict(src_dict)
        checklist = ChecklistTemplateChecklist.from_dict(d.pop("checklist"))

        questions = []
        _questions = d.pop("questions")
        for questions_item_data in _questions:
            questions_item = Question.from_dict(questions_item_data)

            questions.append(questions_item)

        initial_visible_questions = []
        _initial_visible_questions = d.pop("initial_visible_questions")
        for initial_visible_questions_item_data in _initial_visible_questions:
            initial_visible_questions_item = Question.from_dict(initial_visible_questions_item_data)

            initial_visible_questions.append(initial_visible_questions_item)

        checklist_template = cls(
            checklist=checklist,
            questions=questions,
            initial_visible_questions=initial_visible_questions,
        )

        checklist_template.additional_properties = d
        return checklist_template

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
