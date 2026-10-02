from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar, BinaryIO, TextIO, TYPE_CHECKING, Generator

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

from ..models.evaluation_results_response_dto_cells_item_attempts_item_status import EvaluationResultsResponseDtoCellsItemAttemptsItemStatus
from ..types import UNSET, Unset
from typing import cast
from uuid import UUID
import datetime






T = TypeVar("T", bound="EvaluationResultsResponseDtoCellsItemAttemptsItem")



@_attrs_define
class EvaluationResultsResponseDtoCellsItemAttemptsItem:
    """ Result of a single solver attempt at one problem within an evaluation.

        Attributes:
            problem_run_id (UUID): Identifier of the underlying problem run that produced this attempt.
            attempt_number (int): One-based index of the attempt within a solver/problem pairing. Example: 1.
            score (float | None): Final score awarded for the attempt. Null when the attempt did not produce a score
                (incomplete or errored).
            status (EvaluationResultsResponseDtoCellsItemAttemptsItemStatus): Lifecycle status of the underlying problem run
                for this attempt; may be in-progress (pending/running/grading) as well as terminal.
            cost_usd (float | None): Total USD cost recorded for this attempt, summed across its cost rows (agent, compute,
                grading). Null/absent when no cost data is available.
            execution_time_ms (int | None): Wall-clock execution time for this attempt in milliseconds. Null/absent until
                the attempt completes.
            started_at (datetime.datetime | None): Timestamp when this attempt started (ISO-8601, UTC). Null/absent until
                the attempt starts.
            completed_at (datetime.datetime | None): Timestamp when this attempt reached a terminal status (ISO-8601, UTC).
                Null/absent while in-flight.
            error_message (None | str): Error detail recorded for this attempt. Null/absent on success or while still
                running.
            infra_retry_count (int): Number of times this attempt was automatically resubmitted after an infra-classified
                failure (container eviction, image pull error, orphaned queue entry). Zero when the attempt never hit a
                retryable failure.
            input_tokens (int | None): Input tokens consumed by this attempt, summed across its cost rows. Null/absent when
                no token data is available.
            output_tokens (int | None): Output tokens produced by this attempt, summed across its cost rows. Null/absent
                when no token data is available.
            cache_read_input_tokens (int | None): Cache-read input tokens for this attempt, summed across its cost rows.
                Null/absent when no token data is available.
            cache_creation_input_tokens (int | None): Cache-creation input tokens for this attempt, summed across its cost
                rows. Null/absent when no token data is available.
            job_v2_id (None | Unset | UUID): jobs_v2 id of the leaf job that produced this attempt, used to key the rerun
                action. Null/absent for attempts with no linked v2 job (legacy pre-v2 data).
     """

    problem_run_id: UUID
    attempt_number: int
    score: float | None
    status: EvaluationResultsResponseDtoCellsItemAttemptsItemStatus
    cost_usd: float | None
    execution_time_ms: int | None
    started_at: datetime.datetime | None
    completed_at: datetime.datetime | None
    error_message: None | str
    infra_retry_count: int
    input_tokens: int | None
    output_tokens: int | None
    cache_read_input_tokens: int | None
    cache_creation_input_tokens: int | None
    job_v2_id: None | Unset | UUID = UNSET





    def to_dict(self) -> dict[str, Any]:
        problem_run_id = str(self.problem_run_id)

        attempt_number = self.attempt_number

        score: float | None
        score = self.score

        status = self.status.value

        cost_usd: float | None
        cost_usd = self.cost_usd

        execution_time_ms: int | None
        execution_time_ms = self.execution_time_ms

        started_at: None | str
        if isinstance(self.started_at, datetime.datetime):
            started_at = self.started_at.isoformat()
        else:
            started_at = self.started_at

        completed_at: None | str
        if isinstance(self.completed_at, datetime.datetime):
            completed_at = self.completed_at.isoformat()
        else:
            completed_at = self.completed_at

        error_message: None | str
        error_message = self.error_message

        infra_retry_count = self.infra_retry_count

        input_tokens: int | None
        input_tokens = self.input_tokens

        output_tokens: int | None
        output_tokens = self.output_tokens

        cache_read_input_tokens: int | None
        cache_read_input_tokens = self.cache_read_input_tokens

        cache_creation_input_tokens: int | None
        cache_creation_input_tokens = self.cache_creation_input_tokens

        job_v2_id: None | str | Unset
        if isinstance(self.job_v2_id, Unset):
            job_v2_id = UNSET
        elif isinstance(self.job_v2_id, UUID):
            job_v2_id = str(self.job_v2_id)
        else:
            job_v2_id = self.job_v2_id


        field_dict: dict[str, Any] = {}

        field_dict.update({
            "problemRunId": problem_run_id,
            "attemptNumber": attempt_number,
            "score": score,
            "status": status,
            "costUsd": cost_usd,
            "executionTimeMs": execution_time_ms,
            "startedAt": started_at,
            "completedAt": completed_at,
            "errorMessage": error_message,
            "infraRetryCount": infra_retry_count,
            "inputTokens": input_tokens,
            "outputTokens": output_tokens,
            "cacheReadInputTokens": cache_read_input_tokens,
            "cacheCreationInputTokens": cache_creation_input_tokens,
        })
        if job_v2_id is not UNSET:
            field_dict["jobV2Id"] = job_v2_id

        return field_dict



    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        problem_run_id = UUID(d.pop("problemRunId"))




        attempt_number = d.pop("attemptNumber")

        def _parse_score(data: object) -> float | None:
            if data is None:
                return data
            return cast(float | None, data)

        score = _parse_score(d.pop("score"))


        status = EvaluationResultsResponseDtoCellsItemAttemptsItemStatus(d.pop("status"))




        def _parse_cost_usd(data: object) -> float | None:
            if data is None:
                return data
            return cast(float | None, data)

        cost_usd = _parse_cost_usd(d.pop("costUsd"))


        def _parse_execution_time_ms(data: object) -> int | None:
            if data is None:
                return data
            return cast(int | None, data)

        execution_time_ms = _parse_execution_time_ms(d.pop("executionTimeMs"))


        def _parse_started_at(data: object) -> datetime.datetime | None:
            if data is None:
                return data
            try:
                if not isinstance(data, str):
                    raise TypeError()
                started_at_type_0 = datetime.datetime.fromisoformat(data)



                return started_at_type_0
            except (TypeError, ValueError, AttributeError, KeyError):
                pass
            return cast(datetime.datetime | None, data)

        started_at = _parse_started_at(d.pop("startedAt"))


        def _parse_completed_at(data: object) -> datetime.datetime | None:
            if data is None:
                return data
            try:
                if not isinstance(data, str):
                    raise TypeError()
                completed_at_type_0 = datetime.datetime.fromisoformat(data)



                return completed_at_type_0
            except (TypeError, ValueError, AttributeError, KeyError):
                pass
            return cast(datetime.datetime | None, data)

        completed_at = _parse_completed_at(d.pop("completedAt"))


        def _parse_error_message(data: object) -> None | str:
            if data is None:
                return data
            return cast(None | str, data)

        error_message = _parse_error_message(d.pop("errorMessage"))


        infra_retry_count = d.pop("infraRetryCount")

        def _parse_input_tokens(data: object) -> int | None:
            if data is None:
                return data
            return cast(int | None, data)

        input_tokens = _parse_input_tokens(d.pop("inputTokens"))


        def _parse_output_tokens(data: object) -> int | None:
            if data is None:
                return data
            return cast(int | None, data)

        output_tokens = _parse_output_tokens(d.pop("outputTokens"))


        def _parse_cache_read_input_tokens(data: object) -> int | None:
            if data is None:
                return data
            return cast(int | None, data)

        cache_read_input_tokens = _parse_cache_read_input_tokens(d.pop("cacheReadInputTokens"))


        def _parse_cache_creation_input_tokens(data: object) -> int | None:
            if data is None:
                return data
            return cast(int | None, data)

        cache_creation_input_tokens = _parse_cache_creation_input_tokens(d.pop("cacheCreationInputTokens"))


        def _parse_job_v2_id(data: object) -> None | Unset | UUID:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            try:
                if not isinstance(data, str):
                    raise TypeError()
                job_v2_id_type_0 = UUID(data)



                return job_v2_id_type_0
            except (TypeError, ValueError, AttributeError, KeyError):
                pass
            return cast(None | Unset | UUID, data)

        job_v2_id = _parse_job_v2_id(d.pop("jobV2Id", UNSET))


        evaluation_results_response_dto_cells_item_attempts_item = cls(
            problem_run_id=problem_run_id,
            attempt_number=attempt_number,
            score=score,
            status=status,
            cost_usd=cost_usd,
            execution_time_ms=execution_time_ms,
            started_at=started_at,
            completed_at=completed_at,
            error_message=error_message,
            infra_retry_count=infra_retry_count,
            input_tokens=input_tokens,
            output_tokens=output_tokens,
            cache_read_input_tokens=cache_read_input_tokens,
            cache_creation_input_tokens=cache_creation_input_tokens,
            job_v2_id=job_v2_id,
        )

        return evaluation_results_response_dto_cells_item_attempts_item

