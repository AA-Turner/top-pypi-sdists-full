from collections.abc import Mapping
from typing import Any, TypeVar, Union

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..models.checklist_operators import ChecklistOperators
from ..types import UNSET, Unset

T = TypeVar("T", bound="PatchedQuestionDependencyRequest")


@_attrs_define
class PatchedQuestionDependencyRequest:
    """
    Attributes:
        question (Union[Unset, str]):
        depends_on_question (Union[Unset, str]):
        required_answer_value (Union[Unset, Any]): The answer value(s) that make this question visible
        operator (Union[Unset, ChecklistOperators]):
    """

    question: Union[Unset, str] = UNSET
    depends_on_question: Union[Unset, str] = UNSET
    required_answer_value: Union[Unset, Any] = UNSET
    operator: Union[Unset, ChecklistOperators] = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        question = self.question

        depends_on_question = self.depends_on_question

        required_answer_value = self.required_answer_value

        operator: Union[Unset, str] = UNSET
        if not isinstance(self.operator, Unset):
            operator = self.operator.value

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if question is not UNSET:
            field_dict["question"] = question
        if depends_on_question is not UNSET:
            field_dict["depends_on_question"] = depends_on_question
        if required_answer_value is not UNSET:
            field_dict["required_answer_value"] = required_answer_value
        if operator is not UNSET:
            field_dict["operator"] = operator

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        question = d.pop("question", UNSET)

        depends_on_question = d.pop("depends_on_question", UNSET)

        required_answer_value = d.pop("required_answer_value", UNSET)

        _operator = d.pop("operator", UNSET)
        operator: Union[Unset, ChecklistOperators]
        if isinstance(_operator, Unset):
            operator = UNSET
        else:
            operator = ChecklistOperators(_operator)

        patched_question_dependency_request = cls(
            question=question,
            depends_on_question=depends_on_question,
            required_answer_value=required_answer_value,
            operator=operator,
        )

        patched_question_dependency_request.additional_properties = d
        return patched_question_dependency_request

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
