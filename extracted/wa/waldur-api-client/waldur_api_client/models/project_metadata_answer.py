import datetime
from collections.abc import Mapping
from typing import Any, TypeVar, Union, cast

from attrs import define as _attrs_define
from attrs import field as _attrs_field
from dateutil.parser import isoparse

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
        min_value (Union[None, Unset, str]):
        max_value (Union[None, Unset, str]):
        likert_scale_length (Union[None, Unset, int]):
        likert_low_label (Union[Unset, str]):
        likert_high_label (Union[Unset, str]):
        modified (Union[Unset, datetime.datetime]): When this answer was last saved.
    """

    question_uuid: Union[Unset, str] = UNSET
    question: Union[Unset, str] = UNSET
    question_type: Union[Unset, str] = UNSET
    answer: Union[Unset, Any] = UNSET
    min_value: Union[None, Unset, str] = UNSET
    max_value: Union[None, Unset, str] = UNSET
    likert_scale_length: Union[None, Unset, int] = UNSET
    likert_low_label: Union[Unset, str] = UNSET
    likert_high_label: Union[Unset, str] = UNSET
    modified: Union[Unset, datetime.datetime] = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        question_uuid = self.question_uuid

        question = self.question

        question_type = self.question_type

        answer = self.answer

        min_value: Union[None, Unset, str]
        if isinstance(self.min_value, Unset):
            min_value = UNSET
        else:
            min_value = self.min_value

        max_value: Union[None, Unset, str]
        if isinstance(self.max_value, Unset):
            max_value = UNSET
        else:
            max_value = self.max_value

        likert_scale_length: Union[None, Unset, int]
        if isinstance(self.likert_scale_length, Unset):
            likert_scale_length = UNSET
        else:
            likert_scale_length = self.likert_scale_length

        likert_low_label = self.likert_low_label

        likert_high_label = self.likert_high_label

        modified: Union[Unset, str] = UNSET
        if not isinstance(self.modified, Unset):
            modified = self.modified.isoformat()

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
        if min_value is not UNSET:
            field_dict["min_value"] = min_value
        if max_value is not UNSET:
            field_dict["max_value"] = max_value
        if likert_scale_length is not UNSET:
            field_dict["likert_scale_length"] = likert_scale_length
        if likert_low_label is not UNSET:
            field_dict["likert_low_label"] = likert_low_label
        if likert_high_label is not UNSET:
            field_dict["likert_high_label"] = likert_high_label
        if modified is not UNSET:
            field_dict["modified"] = modified

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        question_uuid = d.pop("question_uuid", UNSET)

        question = d.pop("question", UNSET)

        question_type = d.pop("question_type", UNSET)

        answer = d.pop("answer", UNSET)

        def _parse_min_value(data: object) -> Union[None, Unset, str]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(Union[None, Unset, str], data)

        min_value = _parse_min_value(d.pop("min_value", UNSET))

        def _parse_max_value(data: object) -> Union[None, Unset, str]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(Union[None, Unset, str], data)

        max_value = _parse_max_value(d.pop("max_value", UNSET))

        def _parse_likert_scale_length(data: object) -> Union[None, Unset, int]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(Union[None, Unset, int], data)

        likert_scale_length = _parse_likert_scale_length(d.pop("likert_scale_length", UNSET))

        likert_low_label = d.pop("likert_low_label", UNSET)

        likert_high_label = d.pop("likert_high_label", UNSET)

        _modified = d.pop("modified", UNSET)
        modified: Union[Unset, datetime.datetime]
        if isinstance(_modified, Unset):
            modified = UNSET
        else:
            modified = isoparse(_modified)

        project_metadata_answer = cls(
            question_uuid=question_uuid,
            question=question,
            question_type=question_type,
            answer=answer,
            min_value=min_value,
            max_value=max_value,
            likert_scale_length=likert_scale_length,
            likert_low_label=likert_low_label,
            likert_high_label=likert_high_label,
            modified=modified,
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
