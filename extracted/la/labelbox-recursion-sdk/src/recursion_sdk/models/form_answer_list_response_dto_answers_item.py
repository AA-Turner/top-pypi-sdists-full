from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar, BinaryIO, TextIO, TYPE_CHECKING, Generator

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

from typing import cast
from uuid import UUID
import datetime

if TYPE_CHECKING:
  from ..models.form_answer_list_response_dto_answers_item_answers import FormAnswerListResponseDtoAnswersItemAnswers





T = TypeVar("T", bound="FormAnswerListResponseDtoAnswersItem")



@_attrs_define
class FormAnswerListResponseDtoAnswersItem:
    """ One submitted answer payload for a form version, attached to a specific problem version.

        Attributes:
            id (UUID): Stable form-answer identifier (UUID). One submitted answer payload.
            form_version_id (UUID): Form version this answer payload validates against.
            created_by_user_id (UUID): User who submitted this answer payload.
            problem_version_id (UUID): Problem version this answer is attached to.
            answers (FormAnswerListResponseDtoAnswersItemAnswers): Submitted answer payload, keyed by form field name.
            created_at (datetime.datetime): Timestamp when the answer was created (ISO-8601, UTC).
            updated_at (datetime.datetime): Timestamp when the answer was last updated (ISO-8601, UTC).
     """

    id: UUID
    form_version_id: UUID
    created_by_user_id: UUID
    problem_version_id: UUID
    answers: FormAnswerListResponseDtoAnswersItemAnswers
    created_at: datetime.datetime
    updated_at: datetime.datetime





    def to_dict(self) -> dict[str, Any]:
        from ..models.form_answer_list_response_dto_answers_item_answers import FormAnswerListResponseDtoAnswersItemAnswers # noqa: PLC0415
        id = str(self.id)

        form_version_id = str(self.form_version_id)

        created_by_user_id = str(self.created_by_user_id)

        problem_version_id = str(self.problem_version_id)

        answers = self.answers.to_dict()

        created_at = self.created_at.isoformat()

        updated_at = self.updated_at.isoformat()


        field_dict: dict[str, Any] = {}

        field_dict.update({
            "id": id,
            "formVersionId": form_version_id,
            "createdByUserId": created_by_user_id,
            "problemVersionId": problem_version_id,
            "answers": answers,
            "createdAt": created_at,
            "updatedAt": updated_at,
        })

        return field_dict



    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.form_answer_list_response_dto_answers_item_answers import FormAnswerListResponseDtoAnswersItemAnswers # noqa: PLC0415
        d = dict(src_dict)
        id = UUID(d.pop("id"))




        form_version_id = UUID(d.pop("formVersionId"))




        created_by_user_id = UUID(d.pop("createdByUserId"))




        problem_version_id = UUID(d.pop("problemVersionId"))




        answers = FormAnswerListResponseDtoAnswersItemAnswers.from_dict(d.pop("answers"))




        created_at = datetime.datetime.fromisoformat(d.pop("createdAt"))




        updated_at = datetime.datetime.fromisoformat(d.pop("updatedAt"))




        form_answer_list_response_dto_answers_item = cls(
            id=id,
            form_version_id=form_version_id,
            created_by_user_id=created_by_user_id,
            problem_version_id=problem_version_id,
            answers=answers,
            created_at=created_at,
            updated_at=updated_at,
        )

        return form_answer_list_response_dto_answers_item

