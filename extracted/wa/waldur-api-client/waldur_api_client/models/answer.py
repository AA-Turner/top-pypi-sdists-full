import datetime
from collections.abc import Mapping
from typing import Any, TypeVar, Union
from uuid import UUID

from attrs import define as _attrs_define
from attrs import field as _attrs_field
from dateutil.parser import isoparse

from ..types import UNSET, Unset

T = TypeVar("T", bound="Answer")


@_attrs_define
class Answer:
    """
    Attributes:
        uuid (UUID):
        question_description (str):
        question_type (str):
        question_required (bool):
        requires_review (bool): Internal flag - this answer requires additional review
        user (int):
        user_name (str):
        created (datetime.datetime):
        modified (datetime.datetime):
        answer_data (Union[Unset, Any]): Flexible answer storage for different question types
    """

    uuid: UUID
    question_description: str
    question_type: str
    question_required: bool
    requires_review: bool
    user: int
    user_name: str
    created: datetime.datetime
    modified: datetime.datetime
    answer_data: Union[Unset, Any] = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        uuid = str(self.uuid)

        question_description = self.question_description

        question_type = self.question_type

        question_required = self.question_required

        requires_review = self.requires_review

        user = self.user

        user_name = self.user_name

        created = self.created.isoformat()

        modified = self.modified.isoformat()

        answer_data = self.answer_data

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "uuid": uuid,
                "question_description": question_description,
                "question_type": question_type,
                "question_required": question_required,
                "requires_review": requires_review,
                "user": user,
                "user_name": user_name,
                "created": created,
                "modified": modified,
            }
        )
        if answer_data is not UNSET:
            field_dict["answer_data"] = answer_data

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        uuid = UUID(d.pop("uuid"))

        question_description = d.pop("question_description")

        question_type = d.pop("question_type")

        question_required = d.pop("question_required")

        requires_review = d.pop("requires_review")

        user = d.pop("user")

        user_name = d.pop("user_name")

        created = isoparse(d.pop("created"))

        modified = isoparse(d.pop("modified"))

        answer_data = d.pop("answer_data", UNSET)

        answer = cls(
            uuid=uuid,
            question_description=question_description,
            question_type=question_type,
            question_required=question_required,
            requires_review=requires_review,
            user=user,
            user_name=user_name,
            created=created,
            modified=modified,
            answer_data=answer_data,
        )

        answer.additional_properties = d
        return answer

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
