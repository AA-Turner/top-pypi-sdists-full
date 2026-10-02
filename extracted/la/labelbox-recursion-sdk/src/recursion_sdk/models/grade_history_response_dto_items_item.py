from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar, BinaryIO, TextIO, TYPE_CHECKING, Generator

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

from typing import cast
from uuid import UUID
import datetime






T = TypeVar("T", bound="GradeHistoryResponseDtoItemsItem")



@_attrs_define
class GradeHistoryResponseDtoItemsItem:
    """ A superseded grade in a problem run’s re-grade history.

        Attributes:
            id (UUID): Identifier of the archived grade snapshot.
            final_score (float | None): Aggregated final score of this superseded grade.
            graded_at (datetime.datetime | None): When this grade finished grading (ISO-8601, UTC).
            justification (None | str): Aggregated grader justification of this superseded grade.
            grading_model_name (None | str): Grader model recorded for this superseded grade, or null.
            archived_at (datetime.datetime): When this grade was superseded by a re-grade (ISO-8601, UTC).
     """

    id: UUID
    final_score: float | None
    graded_at: datetime.datetime | None
    justification: None | str
    grading_model_name: None | str
    archived_at: datetime.datetime





    def to_dict(self) -> dict[str, Any]:
        id = str(self.id)

        final_score: float | None
        final_score = self.final_score

        graded_at: None | str
        if isinstance(self.graded_at, datetime.datetime):
            graded_at = self.graded_at.isoformat()
        else:
            graded_at = self.graded_at

        justification: None | str
        justification = self.justification

        grading_model_name: None | str
        grading_model_name = self.grading_model_name

        archived_at = self.archived_at.isoformat()


        field_dict: dict[str, Any] = {}

        field_dict.update({
            "id": id,
            "finalScore": final_score,
            "gradedAt": graded_at,
            "justification": justification,
            "gradingModelName": grading_model_name,
            "archivedAt": archived_at,
        })

        return field_dict



    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        id = UUID(d.pop("id"))




        def _parse_final_score(data: object) -> float | None:
            if data is None:
                return data
            return cast(float | None, data)

        final_score = _parse_final_score(d.pop("finalScore"))


        def _parse_graded_at(data: object) -> datetime.datetime | None:
            if data is None:
                return data
            try:
                if not isinstance(data, str):
                    raise TypeError()
                graded_at_type_0 = datetime.datetime.fromisoformat(data)



                return graded_at_type_0
            except (TypeError, ValueError, AttributeError, KeyError):
                pass
            return cast(datetime.datetime | None, data)

        graded_at = _parse_graded_at(d.pop("gradedAt"))


        def _parse_justification(data: object) -> None | str:
            if data is None:
                return data
            return cast(None | str, data)

        justification = _parse_justification(d.pop("justification"))


        def _parse_grading_model_name(data: object) -> None | str:
            if data is None:
                return data
            return cast(None | str, data)

        grading_model_name = _parse_grading_model_name(d.pop("gradingModelName"))


        archived_at = datetime.datetime.fromisoformat(d.pop("archivedAt"))




        grade_history_response_dto_items_item = cls(
            id=id,
            final_score=final_score,
            graded_at=graded_at,
            justification=justification,
            grading_model_name=grading_model_name,
            archived_at=archived_at,
        )

        return grade_history_response_dto_items_item

