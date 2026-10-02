from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar, BinaryIO, TextIO, TYPE_CHECKING, Generator

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

from typing import cast
from uuid import UUID






T = TypeVar("T", bound="EvaluationGradeOnlyResultsResponseDtoTrajectoriesItem")



@_attrs_define
class EvaluationGradeOnlyResultsResponseDtoTrajectoriesItem:
    """ Per-trajectory grader-agreement summary across all grader columns.

        Attributes:
            source_problem_run_id (UUID): The trajectory this agreement summarizes.
            mean_score (float | None): Mean score across the graders that produced a score for this trajectory. Null when no
                grader scored it.
            stddev (float | None): Standard deviation of grader scores for this trajectory — the grader-agreement metric
                (lower = more agreement). Null when fewer than two graders scored it.
            graded_count (int): Number of graders that produced a score for this trajectory. Example: 3.
            grader_count (int): Total number of graders in the evaluation (the expected scores per trajectory). Example: 3.
     """

    source_problem_run_id: UUID
    mean_score: float | None
    stddev: float | None
    graded_count: int
    grader_count: int





    def to_dict(self) -> dict[str, Any]:
        source_problem_run_id = str(self.source_problem_run_id)

        mean_score: float | None
        mean_score = self.mean_score

        stddev: float | None
        stddev = self.stddev

        graded_count = self.graded_count

        grader_count = self.grader_count


        field_dict: dict[str, Any] = {}

        field_dict.update({
            "sourceProblemRunId": source_problem_run_id,
            "meanScore": mean_score,
            "stddev": stddev,
            "gradedCount": graded_count,
            "graderCount": grader_count,
        })

        return field_dict



    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        source_problem_run_id = UUID(d.pop("sourceProblemRunId"))




        def _parse_mean_score(data: object) -> float | None:
            if data is None:
                return data
            return cast(float | None, data)

        mean_score = _parse_mean_score(d.pop("meanScore"))


        def _parse_stddev(data: object) -> float | None:
            if data is None:
                return data
            return cast(float | None, data)

        stddev = _parse_stddev(d.pop("stddev"))


        graded_count = d.pop("gradedCount")

        grader_count = d.pop("graderCount")

        evaluation_grade_only_results_response_dto_trajectories_item = cls(
            source_problem_run_id=source_problem_run_id,
            mean_score=mean_score,
            stddev=stddev,
            graded_count=graded_count,
            grader_count=grader_count,
        )

        return evaluation_grade_only_results_response_dto_trajectories_item

