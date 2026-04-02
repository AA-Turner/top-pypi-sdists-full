from collections.abc import Mapping
from typing import Any, TypeVar
from uuid import UUID

from attrs import define as _attrs_define
from attrs import field as _attrs_field

T = TypeVar("T", bound="AnswerSubmitRequest")


@_attrs_define
class AnswerSubmitRequest:
    """
    Attributes:
        question_uuid (UUID):
        answer_data (Any):
    """

    question_uuid: UUID
    answer_data: Any
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        question_uuid = str(self.question_uuid)

        answer_data = self.answer_data

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "question_uuid": question_uuid,
                "answer_data": answer_data,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        question_uuid = UUID(d.pop("question_uuid"))

        answer_data = d.pop("answer_data")

        answer_submit_request = cls(
            question_uuid=question_uuid,
            answer_data=answer_data,
        )

        answer_submit_request.additional_properties = d
        return answer_submit_request

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
