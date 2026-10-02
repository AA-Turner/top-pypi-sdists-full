from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar, BinaryIO, TextIO, TYPE_CHECKING, Generator

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

from ..models.public_problem_detail_dto_runs_items_item_status import PublicProblemDetailDtoRunsItemsItemStatus
from typing import cast
from uuid import UUID
import datetime






T = TypeVar("T", bound="PublicProblemDetailDtoRunsItemsItem")



@_attrs_define
class PublicProblemDetailDtoRunsItemsItem:
    """ Public execution summary for one run of a locked problem version, excluding private run artifacts and grading
    internals.

        Attributes:
            id (UUID): Identifier of this public run summary.
            run_name (None | str): User-supplied run name. Null when the run was not named.
            problem_version_id (UUID): Locked problem version exercised by this public run.
            status (PublicProblemDetailDtoRunsItemsItemStatus): Current lifecycle status of the run.
            attempt_number (int): Attempt number recorded for the run. Historical imports preserve their source value.
                Example: 1.
            execution_time_ms (int | None): Recorded solver execution time in milliseconds. Null when unavailable;
                historical imports preserve their source value. Example: 42000.
            final_score (float | None): Aggregated grader score. Null until grading completes; some grading schemes may
                produce negative values. Example: 0.83.
            api_model_name (None | str): Solver model used for this run. Null when no model was recorded.
            turns_count (int | None): Recorded solver turn count. Null when unavailable; historical imports preserve their
                source value. Example: 12.
            created_at (datetime.datetime): Timestamp when the run was created (ISO-8601, UTC).
            started_at (datetime.datetime | None): Timestamp when solver execution began (ISO-8601, UTC). Null until
                started.
            completed_at (datetime.datetime | None): Timestamp when the run completed (ISO-8601, UTC). Null while in flight.
     """

    id: UUID
    run_name: None | str
    problem_version_id: UUID
    status: PublicProblemDetailDtoRunsItemsItemStatus
    attempt_number: int
    execution_time_ms: int | None
    final_score: float | None
    api_model_name: None | str
    turns_count: int | None
    created_at: datetime.datetime
    started_at: datetime.datetime | None
    completed_at: datetime.datetime | None





    def to_dict(self) -> dict[str, Any]:
        id = str(self.id)

        run_name: None | str
        run_name = self.run_name

        problem_version_id = str(self.problem_version_id)

        status = self.status.value

        attempt_number = self.attempt_number

        execution_time_ms: int | None
        execution_time_ms = self.execution_time_ms

        final_score: float | None
        final_score = self.final_score

        api_model_name: None | str
        api_model_name = self.api_model_name

        turns_count: int | None
        turns_count = self.turns_count

        created_at = self.created_at.isoformat()

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


        field_dict: dict[str, Any] = {}

        field_dict.update({
            "id": id,
            "runName": run_name,
            "problemVersionId": problem_version_id,
            "status": status,
            "attemptNumber": attempt_number,
            "executionTimeMs": execution_time_ms,
            "finalScore": final_score,
            "apiModelName": api_model_name,
            "turnsCount": turns_count,
            "createdAt": created_at,
            "startedAt": started_at,
            "completedAt": completed_at,
        })

        return field_dict



    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        id = UUID(d.pop("id"))




        def _parse_run_name(data: object) -> None | str:
            if data is None:
                return data
            return cast(None | str, data)

        run_name = _parse_run_name(d.pop("runName"))


        problem_version_id = UUID(d.pop("problemVersionId"))




        status = PublicProblemDetailDtoRunsItemsItemStatus(d.pop("status"))




        attempt_number = d.pop("attemptNumber")

        def _parse_execution_time_ms(data: object) -> int | None:
            if data is None:
                return data
            return cast(int | None, data)

        execution_time_ms = _parse_execution_time_ms(d.pop("executionTimeMs"))


        def _parse_final_score(data: object) -> float | None:
            if data is None:
                return data
            return cast(float | None, data)

        final_score = _parse_final_score(d.pop("finalScore"))


        def _parse_api_model_name(data: object) -> None | str:
            if data is None:
                return data
            return cast(None | str, data)

        api_model_name = _parse_api_model_name(d.pop("apiModelName"))


        def _parse_turns_count(data: object) -> int | None:
            if data is None:
                return data
            return cast(int | None, data)

        turns_count = _parse_turns_count(d.pop("turnsCount"))


        created_at = datetime.datetime.fromisoformat(d.pop("createdAt"))




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


        public_problem_detail_dto_runs_items_item = cls(
            id=id,
            run_name=run_name,
            problem_version_id=problem_version_id,
            status=status,
            attempt_number=attempt_number,
            execution_time_ms=execution_time_ms,
            final_score=final_score,
            api_model_name=api_model_name,
            turns_count=turns_count,
            created_at=created_at,
            started_at=started_at,
            completed_at=completed_at,
        )

        return public_problem_detail_dto_runs_items_item

