from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar, BinaryIO, TextIO, TYPE_CHECKING, Generator

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

from ..models.evaluation_grade_only_results_response_dto_cells_item_grade_type_0_status import EvaluationGradeOnlyResultsResponseDtoCellsItemGradeType0Status
from typing import cast
from uuid import UUID
import datetime






T = TypeVar("T", bound="EvaluationGradeOnlyResultsResponseDtoCellsItemGradeType0")



@_attrs_define
class EvaluationGradeOnlyResultsResponseDtoCellsItemGradeType0:
    """ One grader config’s independent verdict on one existing trajectory.

        Attributes:
            id (UUID): Stable problem-run-grade identifier (UUID). One independent grader verdict on one trajectory
                (`problem_run_grades` row).
            grader_run_config_version_id (UUID): Locked run-config version (kind "grader") that produced this grade.
            status (EvaluationGradeOnlyResultsResponseDtoCellsItemGradeType0Status): Lifecycle status of this grade, from
                queueing through grading to a terminal state. Shares the same status enum as the underlying problem run.
            final_score (float | None): Final score this grader awarded the trajectory. Null until grading completes.
                Example: 0.83.
            justification (None | str): This grader's justification for the score. Null until grading completes.
            cost_usd (float | None): USD cost of running this grader against the trajectory. Null/absent while in-flight or
                when no cost was recorded. Excludes the source solver run cost, which is shown separately as reference to avoid
                double-counting.
            graded_at (datetime.datetime | None): Timestamp when this grade finished grading (ISO-8601, UTC). Null until
                complete.
            error_message (None | str): Error detail if this grade failed. Null on success or while still running.
     """

    id: UUID
    grader_run_config_version_id: UUID
    status: EvaluationGradeOnlyResultsResponseDtoCellsItemGradeType0Status
    final_score: float | None
    justification: None | str
    cost_usd: float | None
    graded_at: datetime.datetime | None
    error_message: None | str





    def to_dict(self) -> dict[str, Any]:
        id = str(self.id)

        grader_run_config_version_id = str(self.grader_run_config_version_id)

        status = self.status.value

        final_score: float | None
        final_score = self.final_score

        justification: None | str
        justification = self.justification

        cost_usd: float | None
        cost_usd = self.cost_usd

        graded_at: None | str
        if isinstance(self.graded_at, datetime.datetime):
            graded_at = self.graded_at.isoformat()
        else:
            graded_at = self.graded_at

        error_message: None | str
        error_message = self.error_message


        field_dict: dict[str, Any] = {}

        field_dict.update({
            "id": id,
            "graderRunConfigVersionId": grader_run_config_version_id,
            "status": status,
            "finalScore": final_score,
            "justification": justification,
            "costUsd": cost_usd,
            "gradedAt": graded_at,
            "errorMessage": error_message,
        })

        return field_dict



    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        id = UUID(d.pop("id"))




        grader_run_config_version_id = UUID(d.pop("graderRunConfigVersionId"))




        status = EvaluationGradeOnlyResultsResponseDtoCellsItemGradeType0Status(d.pop("status"))




        def _parse_final_score(data: object) -> float | None:
            if data is None:
                return data
            return cast(float | None, data)

        final_score = _parse_final_score(d.pop("finalScore"))


        def _parse_justification(data: object) -> None | str:
            if data is None:
                return data
            return cast(None | str, data)

        justification = _parse_justification(d.pop("justification"))


        def _parse_cost_usd(data: object) -> float | None:
            if data is None:
                return data
            return cast(float | None, data)

        cost_usd = _parse_cost_usd(d.pop("costUsd"))


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


        def _parse_error_message(data: object) -> None | str:
            if data is None:
                return data
            return cast(None | str, data)

        error_message = _parse_error_message(d.pop("errorMessage"))


        evaluation_grade_only_results_response_dto_cells_item_grade_type_0 = cls(
            id=id,
            grader_run_config_version_id=grader_run_config_version_id,
            status=status,
            final_score=final_score,
            justification=justification,
            cost_usd=cost_usd,
            graded_at=graded_at,
            error_message=error_message,
        )

        return evaluation_grade_only_results_response_dto_cells_item_grade_type_0

