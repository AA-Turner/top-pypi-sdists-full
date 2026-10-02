from collections.abc import Mapping
from typing import Any, TypeVar, Union
from uuid import UUID

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

T = TypeVar("T", bound="QuestionOptionsAdmin")


@_attrs_define
class QuestionOptionsAdmin:
    """
    Attributes:
        uuid (UUID):
        label (str):
        url (str):
        question (str):
        question_uuid (UUID):
        order (Union[Unset, int]):
    """

    uuid: UUID
    label: str
    url: str
    question: str
    question_uuid: UUID
    order: Union[Unset, int] = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        uuid = str(self.uuid)

        label = self.label

        url = self.url

        question = self.question

        question_uuid = str(self.question_uuid)

        order = self.order

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "uuid": uuid,
                "label": label,
                "url": url,
                "question": question,
                "question_uuid": question_uuid,
            }
        )
        if order is not UNSET:
            field_dict["order"] = order

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        uuid = UUID(d.pop("uuid"))

        label = d.pop("label")

        url = d.pop("url")

        question = d.pop("question")

        question_uuid = UUID(d.pop("question_uuid"))

        order = d.pop("order", UNSET)

        question_options_admin = cls(
            uuid=uuid,
            label=label,
            url=url,
            question=question,
            question_uuid=question_uuid,
            order=order,
        )

        question_options_admin.additional_properties = d
        return question_options_admin

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
