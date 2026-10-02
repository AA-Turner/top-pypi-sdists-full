from collections.abc import Mapping
from typing import Any, TypeVar, Union

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

T = TypeVar("T", bound="ProjectMetadataAnswer")


@_attrs_define
class ProjectMetadataAnswer:
    """
    Attributes:
        question_uuid (Union[Unset, str]):
        question (Union[Unset, str]): Question description.
        question_type (Union[Unset, str]):
        answer (Union[Unset, Any]): Human-readable answer value; select-type option UUIDs are resolved to their labels.
    """

    question_uuid: Union[Unset, str] = UNSET
    question: Union[Unset, str] = UNSET
    question_type: Union[Unset, str] = UNSET
    answer: Union[Unset, Any] = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        question_uuid = self.question_uuid

        question = self.question

        question_type = self.question_type

        answer = self.answer

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if question_uuid is not UNSET:
            field_dict["question_uuid"] = question_uuid
        if question is not UNSET:
            field_dict["question"] = question
        if question_type is not UNSET:
            field_dict["question_type"] = question_type
        if answer is not UNSET:
            field_dict["answer"] = answer

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        question_uuid = d.pop("question_uuid", UNSET)

        question = d.pop("question", UNSET)

        question_type = d.pop("question_type", UNSET)

        answer = d.pop("answer", UNSET)

        project_metadata_answer = cls(
            question_uuid=question_uuid,
            question=question,
            question_type=question_type,
            answer=answer,
        )

        project_metadata_answer.additional_properties = d
        return project_metadata_answer

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
