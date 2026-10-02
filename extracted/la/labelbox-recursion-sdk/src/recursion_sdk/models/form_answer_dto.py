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
  from ..models.form_answer_dto_answers import FormAnswerDtoAnswers





T = TypeVar("T", bound="FormAnswerDto")



@_attrs_define
class FormAnswerDto:
    """ One submitted answer payload for a form version, attached to a specific problem version.

        Example:
            {'id': 'aec7f936-b556-4011-84ff-558cc238b5b2', 'formVersionId': '77e4ffc9-3d40-472c-b160-f163e02df324',
                'createdByUserId': '49dea803-7390-49c4-abb1-5629718fc9cd', 'problemVersionId':
                '0c3ac467-57e1-4074-b57d-b6a7be392f71', 'answers': {'severity': 'major', 'notes': 'Visible scratch along the
                top-left bezel.'}, 'createdAt': '2026-01-16T15:05:00.000Z', 'updatedAt': '2026-01-16T15:05:00.000Z'}

        Attributes:
            id (UUID): Stable form-answer identifier (UUID). One submitted answer payload.
            form_version_id (UUID): Form version this answer payload validates against.
            created_by_user_id (UUID): User who submitted this answer payload.
            problem_version_id (UUID): Problem version this answer is attached to.
            answers (FormAnswerDtoAnswers): Submitted answer payload, keyed by form field name.
            created_at (datetime.datetime): Timestamp when the answer was created (ISO-8601, UTC).
            updated_at (datetime.datetime): Timestamp when the answer was last updated (ISO-8601, UTC).
     """

    id: UUID
    form_version_id: UUID
    created_by_user_id: UUID
    problem_version_id: UUID
    answers: FormAnswerDtoAnswers
    created_at: datetime.datetime
    updated_at: datetime.datetime





    def to_dict(self) -> dict[str, Any]:
        from ..models.form_answer_dto_answers import FormAnswerDtoAnswers # noqa: PLC0415
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
        from ..models.form_answer_dto_answers import FormAnswerDtoAnswers # noqa: PLC0415
        d = dict(src_dict)
        id = UUID(d.pop("id"))




        form_version_id = UUID(d.pop("formVersionId"))




        created_by_user_id = UUID(d.pop("createdByUserId"))




        problem_version_id = UUID(d.pop("problemVersionId"))




        answers = FormAnswerDtoAnswers.from_dict(d.pop("answers"))




        created_at = datetime.datetime.fromisoformat(d.pop("createdAt"))




        updated_at = datetime.datetime.fromisoformat(d.pop("updatedAt"))




        form_answer_dto = cls(
            id=id,
            form_version_id=form_version_id,
            created_by_user_id=created_by_user_id,
            problem_version_id=problem_version_id,
            answers=answers,
            created_at=created_at,
            updated_at=updated_at,
        )

        return form_answer_dto

