from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar, BinaryIO, TextIO, TYPE_CHECKING, Generator

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

from typing import cast
from uuid import UUID

if TYPE_CHECKING:
  from ..models.upsert_form_answer_body_dto_answers import UpsertFormAnswerBodyDtoAnswers





T = TypeVar("T", bound="UpsertFormAnswerBodyDto")



@_attrs_define
class UpsertFormAnswerBodyDto:
    """ Request body for creating or updating a form answer on a problem version.

        Example:
            {'formVersionId': '77e4ffc9-3d40-472c-b160-f163e02df324', 'answers': {'severity': 'major', 'notes': 'Visible
                scratch along the top-left bezel.'}}

        Attributes:
            form_version_id (UUID): Form version that the supplied answers validate against.
            answers (UpsertFormAnswerBodyDtoAnswers): Answer payload keyed by form field name.
     """

    form_version_id: UUID
    answers: UpsertFormAnswerBodyDtoAnswers
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)





    def to_dict(self) -> dict[str, Any]:
        from ..models.upsert_form_answer_body_dto_answers import UpsertFormAnswerBodyDtoAnswers # noqa: PLC0415
        form_version_id = str(self.form_version_id)

        answers = self.answers.to_dict()


        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({
            "formVersionId": form_version_id,
            "answers": answers,
        })

        return field_dict



    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.upsert_form_answer_body_dto_answers import UpsertFormAnswerBodyDtoAnswers # noqa: PLC0415
        d = dict(src_dict)
        form_version_id = UUID(d.pop("formVersionId"))




        answers = UpsertFormAnswerBodyDtoAnswers.from_dict(d.pop("answers"))




        upsert_form_answer_body_dto = cls(
            form_version_id=form_version_id,
            answers=answers,
        )


        upsert_form_answer_body_dto.additional_properties = d
        return upsert_form_answer_body_dto

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
