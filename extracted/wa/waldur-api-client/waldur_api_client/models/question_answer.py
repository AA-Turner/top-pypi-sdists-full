from collections.abc import Mapping
from typing import TYPE_CHECKING, Any, TypeVar, Union, cast
from uuid import UUID

from attrs import define as _attrs_define
from attrs import field as _attrs_field

if TYPE_CHECKING:
    from ..models.question_answer_project_answers_item import QuestionAnswerProjectAnswersItem
    from ..models.question_answer_question_options_item import QuestionAnswerQuestionOptionsItem


T = TypeVar("T", bound="QuestionAnswer")


@_attrs_define
class QuestionAnswer:
    """
    Attributes:
        question_uuid (UUID):
        question_description (str):
        question_type (str):
        required (bool):
        order (int):
        min_value (Union[None, str]):
        max_value (Union[None, str]):
        total_projects (int): Get total projects count.
        answered_projects_count (int): Get count of projects that answered this question.
        project_answers (list['QuestionAnswerProjectAnswersItem']): Get all project answers for this question.
        question_options (list['QuestionAnswerQuestionOptionsItem']): Get question options for select-type questions.
    """

    question_uuid: UUID
    question_description: str
    question_type: str
    required: bool
    order: int
    min_value: Union[None, str]
    max_value: Union[None, str]
    total_projects: int
    answered_projects_count: int
    project_answers: list["QuestionAnswerProjectAnswersItem"]
    question_options: list["QuestionAnswerQuestionOptionsItem"]
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        question_uuid = str(self.question_uuid)

        question_description = self.question_description

        question_type = self.question_type

        required = self.required

        order = self.order

        min_value: Union[None, str]
        min_value = self.min_value

        max_value: Union[None, str]
        max_value = self.max_value

        total_projects = self.total_projects

        answered_projects_count = self.answered_projects_count

        project_answers = []
        for project_answers_item_data in self.project_answers:
            project_answers_item = project_answers_item_data.to_dict()
            project_answers.append(project_answers_item)

        question_options = []
        for question_options_item_data in self.question_options:
            question_options_item = question_options_item_data.to_dict()
            question_options.append(question_options_item)

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "question_uuid": question_uuid,
                "question_description": question_description,
                "question_type": question_type,
                "required": required,
                "order": order,
                "min_value": min_value,
                "max_value": max_value,
                "total_projects": total_projects,
                "answered_projects_count": answered_projects_count,
                "project_answers": project_answers,
                "question_options": question_options,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.question_answer_project_answers_item import QuestionAnswerProjectAnswersItem
        from ..models.question_answer_question_options_item import QuestionAnswerQuestionOptionsItem

        d = dict(src_dict)
        question_uuid = UUID(d.pop("question_uuid"))

        question_description = d.pop("question_description")

        question_type = d.pop("question_type")

        required = d.pop("required")

        order = d.pop("order")

        def _parse_min_value(data: object) -> Union[None, str]:
            if data is None:
                return data
            return cast(Union[None, str], data)

        min_value = _parse_min_value(d.pop("min_value"))

        def _parse_max_value(data: object) -> Union[None, str]:
            if data is None:
                return data
            return cast(Union[None, str], data)

        max_value = _parse_max_value(d.pop("max_value"))

        total_projects = d.pop("total_projects")

        answered_projects_count = d.pop("answered_projects_count")

        project_answers = []
        _project_answers = d.pop("project_answers")
        for project_answers_item_data in _project_answers:
            project_answers_item = QuestionAnswerProjectAnswersItem.from_dict(project_answers_item_data)

            project_answers.append(project_answers_item)

        question_options = []
        _question_options = d.pop("question_options")
        for question_options_item_data in _question_options:
            question_options_item = QuestionAnswerQuestionOptionsItem.from_dict(question_options_item_data)

            question_options.append(question_options_item)

        question_answer = cls(
            question_uuid=question_uuid,
            question_description=question_description,
            question_type=question_type,
            required=required,
            order=order,
            min_value=min_value,
            max_value=max_value,
            total_projects=total_projects,
            answered_projects_count=answered_projects_count,
            project_answers=project_answers,
            question_options=question_options,
        )

        question_answer.additional_properties = d
        return question_answer

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
