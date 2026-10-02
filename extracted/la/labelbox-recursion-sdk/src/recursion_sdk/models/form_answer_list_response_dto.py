from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar, BinaryIO, TextIO, TYPE_CHECKING, Generator

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

from typing import cast

if TYPE_CHECKING:
  from ..models.form_answer_list_response_dto_answers_item import FormAnswerListResponseDtoAnswersItem





T = TypeVar("T", bound="FormAnswerListResponseDto")



@_attrs_define
class FormAnswerListResponseDto:
    """ Response listing form answers submitted against a form version.

        Example:
            {'answers': [{'id': 'aec7f936-b556-4011-84ff-558cc238b5b2', 'formVersionId':
                '77e4ffc9-3d40-472c-b160-f163e02df324', 'createdByUserId': '49dea803-7390-49c4-abb1-5629718fc9cd',
                'problemVersionId': '0c3ac467-57e1-4074-b57d-b6a7be392f71', 'answers': {'severity': 'major', 'notes': 'Visible
                scratch along the top-left bezel.'}, 'createdAt': '2026-01-16T15:05:00.000Z', 'updatedAt':
                '2026-01-16T15:05:00.000Z'}]}

        Attributes:
            answers (list[FormAnswerListResponseDtoAnswersItem]): Form answers submitted against the requested scope.
     """

    answers: list[FormAnswerListResponseDtoAnswersItem]





    def to_dict(self) -> dict[str, Any]:
        from ..models.form_answer_list_response_dto_answers_item import FormAnswerListResponseDtoAnswersItem # noqa: PLC0415
        answers = []
        for answers_item_data in self.answers:
            answers_item = answers_item_data.to_dict()
            answers.append(answers_item)




        field_dict: dict[str, Any] = {}

        field_dict.update({
            "answers": answers,
        })

        return field_dict



    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.form_answer_list_response_dto_answers_item import FormAnswerListResponseDtoAnswersItem # noqa: PLC0415
        d = dict(src_dict)
        answers = []
        _answers = d.pop("answers")
        for answers_item_data in (_answers):
            answers_item = FormAnswerListResponseDtoAnswersItem.from_dict(answers_item_data)



            answers.append(answers_item)


        form_answer_list_response_dto = cls(
            answers=answers,
        )

        return form_answer_list_response_dto

