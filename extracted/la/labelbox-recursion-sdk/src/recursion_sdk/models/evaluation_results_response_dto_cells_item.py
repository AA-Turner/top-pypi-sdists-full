from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar, BinaryIO, TextIO, TYPE_CHECKING, Generator

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

from typing import cast
from uuid import UUID

if TYPE_CHECKING:
  from ..models.evaluation_results_response_dto_cells_item_attempts_item import EvaluationResultsResponseDtoCellsItemAttemptsItem





T = TypeVar("T", bound="EvaluationResultsResponseDtoCellsItem")



@_attrs_define
class EvaluationResultsResponseDtoCellsItem:
    """ Aggregate result for one solver and problem-version pair in an evaluation.

        Attributes:
            solver_id (UUID): Stable evaluation-solver identifier (UUID). Refers to one solver participating in an
                evaluation.
            problem_version_id (UUID): Stable problem-version identifier (UUID). Each problem can have many versions; this
                points at one specific version.
            mean_score (float | None): Mean score across all completed attempts in this cell. Null when no attempt produced
                a score.
            stddev (float | None): Standard deviation of scores across completed attempts. Null when fewer than two scored
                attempts exist.
            min_score (float | None): Minimum score across completed attempts. Null when no attempt produced a score.
            max_score (float | None): Maximum score across completed attempts. Null when no attempt produced a score.
            pass_count (int): Number of attempts in this cell that passed. Example: 2.
            fail_count (int): Number of attempts in this cell that failed. Example: 1.
            total_runs (int): Total number of attempts expected for this cell. Example: 3.
            completed_runs (int): Number of attempts in this cell that have reached a terminal status. Example: 3.
            total_cost_usd (float | None): Total USD cost across completed attempts in this cell. Null when no cost data is
                available.
            mean_execution_time_ms (float | None): Mean wall-clock execution time across completed attempts (milliseconds).
                Null when no timing data is available.
            attempts (list[EvaluationResultsResponseDtoCellsItemAttemptsItem]): Per-attempt results in attempt-number order.
     """

    solver_id: UUID
    problem_version_id: UUID
    mean_score: float | None
    stddev: float | None
    min_score: float | None
    max_score: float | None
    pass_count: int
    fail_count: int
    total_runs: int
    completed_runs: int
    total_cost_usd: float | None
    mean_execution_time_ms: float | None
    attempts: list[EvaluationResultsResponseDtoCellsItemAttemptsItem]





    def to_dict(self) -> dict[str, Any]:
        from ..models.evaluation_results_response_dto_cells_item_attempts_item import EvaluationResultsResponseDtoCellsItemAttemptsItem # noqa: PLC0415
        solver_id = str(self.solver_id)

        problem_version_id = str(self.problem_version_id)

        mean_score: float | None
        mean_score = self.mean_score

        stddev: float | None
        stddev = self.stddev

        min_score: float | None
        min_score = self.min_score

        max_score: float | None
        max_score = self.max_score

        pass_count = self.pass_count

        fail_count = self.fail_count

        total_runs = self.total_runs

        completed_runs = self.completed_runs

        total_cost_usd: float | None
        total_cost_usd = self.total_cost_usd

        mean_execution_time_ms: float | None
        mean_execution_time_ms = self.mean_execution_time_ms

        attempts = []
        for attempts_item_data in self.attempts:
            attempts_item = attempts_item_data.to_dict()
            attempts.append(attempts_item)




        field_dict: dict[str, Any] = {}

        field_dict.update({
            "solverId": solver_id,
            "problemVersionId": problem_version_id,
            "meanScore": mean_score,
            "stddev": stddev,
            "minScore": min_score,
            "maxScore": max_score,
            "passCount": pass_count,
            "failCount": fail_count,
            "totalRuns": total_runs,
            "completedRuns": completed_runs,
            "totalCostUsd": total_cost_usd,
            "meanExecutionTimeMs": mean_execution_time_ms,
            "attempts": attempts,
        })

        return field_dict



    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.evaluation_results_response_dto_cells_item_attempts_item import EvaluationResultsResponseDtoCellsItemAttemptsItem # noqa: PLC0415
        d = dict(src_dict)
        solver_id = UUID(d.pop("solverId"))




        problem_version_id = UUID(d.pop("problemVersionId"))




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


        def _parse_min_score(data: object) -> float | None:
            if data is None:
                return data
            return cast(float | None, data)

        min_score = _parse_min_score(d.pop("minScore"))


        def _parse_max_score(data: object) -> float | None:
            if data is None:
                return data
            return cast(float | None, data)

        max_score = _parse_max_score(d.pop("maxScore"))


        pass_count = d.pop("passCount")

        fail_count = d.pop("failCount")

        total_runs = d.pop("totalRuns")

        completed_runs = d.pop("completedRuns")

        def _parse_total_cost_usd(data: object) -> float | None:
            if data is None:
                return data
            return cast(float | None, data)

        total_cost_usd = _parse_total_cost_usd(d.pop("totalCostUsd"))


        def _parse_mean_execution_time_ms(data: object) -> float | None:
            if data is None:
                return data
            return cast(float | None, data)

        mean_execution_time_ms = _parse_mean_execution_time_ms(d.pop("meanExecutionTimeMs"))


        attempts = []
        _attempts = d.pop("attempts")
        for attempts_item_data in (_attempts):
            attempts_item = EvaluationResultsResponseDtoCellsItemAttemptsItem.from_dict(attempts_item_data)



            attempts.append(attempts_item)


        evaluation_results_response_dto_cells_item = cls(
            solver_id=solver_id,
            problem_version_id=problem_version_id,
            mean_score=mean_score,
            stddev=stddev,
            min_score=min_score,
            max_score=max_score,
            pass_count=pass_count,
            fail_count=fail_count,
            total_runs=total_runs,
            completed_runs=completed_runs,
            total_cost_usd=total_cost_usd,
            mean_execution_time_ms=mean_execution_time_ms,
            attempts=attempts,
        )

        return evaluation_results_response_dto_cells_item

