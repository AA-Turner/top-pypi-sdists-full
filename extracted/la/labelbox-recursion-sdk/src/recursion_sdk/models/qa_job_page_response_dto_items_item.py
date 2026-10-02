from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar, BinaryIO, TextIO, TYPE_CHECKING, Generator

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

from ..models.qa_job_page_response_dto_items_item_kind import QaJobPageResponseDtoItemsItemKind
from ..models.qa_job_page_response_dto_items_item_status import QaJobPageResponseDtoItemsItemStatus
from ..types import UNSET, Unset
from typing import cast
from uuid import UUID

if TYPE_CHECKING:
  from ..models.qa_job_page_response_dto_items_item_child_runs_item import QaJobPageResponseDtoItemsItemChildRunsItem
  from ..models.qa_job_page_response_dto_items_item_result_type_0 import QaJobPageResponseDtoItemsItemResultType0





T = TypeVar("T", bound="QaJobPageResponseDtoItemsItem")



@_attrs_define
class QaJobPageResponseDtoItemsItem:
    """ QA job row exposed by the platform API, with denormalized result summary and run-config metadata.

        Attributes:
            id (UUID): Stable QA-job identifier (UUID).
            qa_config_id (None | UUID): QA configuration executed by this job; null when the job was created without a
                persisted QA config.
            qa_config_name (None | str): Display name of the QA config bound to this job, denormalized via JOIN; null when
                no config is bound.
            batch_id (None | UUID): QA batch that scheduled this job; null when the job was triggered individually.
            environment_id (UUID): Stable environment identifier (UUID).
            problem_id (None | UUID): Problem evaluated by this job; null for aggregate jobs that span multiple problems.
            problem_version_id (None | UUID): Specific problem version evaluated by this job; null when the job is not
                version-scoped.
            kind (QaJobPageResponseDtoItemsItemKind): Kind of QA job: a single-problem evaluation, or an aggregate
                evaluation across a set of problems.
            status (QaJobPageResponseDtoItemsItemStatus): Lifecycle status of a QA job from queueing through dispatch and
                execution to a terminal state.
            container_image (None | str): Container image actually executed for this QA job.
            external_run_id (None | str): Launcher-assigned external run identifier, or null before submission.
            error_message (None | str): Error message captured when the QA job failed; null otherwise.
            execution_time_ms (float | None): Wall-clock execution time of the QA job in milliseconds; null if not yet
                recorded. Example: 12500.
            total_cost_usd (None | str): Total cost of the QA job in USD as a decimal string; null when cost is unknown.
                Example: 0.12.
            attempt_count (float): Number of attempts executed so far for this QA job.
            max_retries (float): Maximum number of automatic retries allowed for this QA job. Applies to single-container QA
                kinds (standard, grading-oracle, metrics-validator), where a failed or unusable attempt is re-dispatched until
                the budget is spent. Ignored by the composite kinds (gtGradingOracle, standard-composite), which always run a
                single attempt.
            started_at (None | str): Timestamp when the QA job started running (ISO-8601, UTC); null before start.
            completed_at (None | str): Timestamp when the QA job reached a terminal status (ISO-8601, UTC); null while in-
                flight.
            created_at (str): Timestamp when the QA job was created (ISO-8601, UTC).
            updated_at (str): Timestamp when the QA job was last updated (ISO-8601, UTC).
            score (float | None): Summary score from the QA result; populated in both list and detail responses.
            grade (None | str): Summary grade label from the QA result; populated in both list and detail responses.
            problem_title (None | str): Problem title denormalized for convenience; populated in both list and detail
                responses.
            result (None | QaJobPageResponseDtoItemsItemResultType0): Detailed QA result payload; only populated on the
                single-job detail endpoint and null in list responses.
            qa_run_config_version_id (None | UUID): Run-config-version that drove the QA pipeline for this job, captured at
                job-insert time for audit fidelity.
            qa_run_config_name (None | str): Display name of the QA run-config bound to this job, denormalized via JOIN.
            qa_run_config_version_number (int | None): Version number of the QA run-config-version, denormalized via JOIN.
            child_runs (list[QaJobPageResponseDtoItemsItemChildRunsItem] | Unset): Per-leaf child runs of a composite QA
                job; populated on the detail endpoint for composite jobs only.
     """

    id: UUID
    qa_config_id: None | UUID
    qa_config_name: None | str
    batch_id: None | UUID
    environment_id: UUID
    problem_id: None | UUID
    problem_version_id: None | UUID
    kind: QaJobPageResponseDtoItemsItemKind
    status: QaJobPageResponseDtoItemsItemStatus
    container_image: None | str
    external_run_id: None | str
    error_message: None | str
    execution_time_ms: float | None
    total_cost_usd: None | str
    attempt_count: float
    max_retries: float
    started_at: None | str
    completed_at: None | str
    created_at: str
    updated_at: str
    score: float | None
    grade: None | str
    problem_title: None | str
    result: None | QaJobPageResponseDtoItemsItemResultType0
    qa_run_config_version_id: None | UUID
    qa_run_config_name: None | str
    qa_run_config_version_number: int | None
    child_runs: list[QaJobPageResponseDtoItemsItemChildRunsItem] | Unset = UNSET





    def to_dict(self) -> dict[str, Any]:
        from ..models.qa_job_page_response_dto_items_item_child_runs_item import QaJobPageResponseDtoItemsItemChildRunsItem # noqa: PLC0415
        from ..models.qa_job_page_response_dto_items_item_result_type_0 import QaJobPageResponseDtoItemsItemResultType0 # noqa: PLC0415
        id = str(self.id)

        qa_config_id: None | str
        if isinstance(self.qa_config_id, UUID):
            qa_config_id = str(self.qa_config_id)
        else:
            qa_config_id = self.qa_config_id

        qa_config_name: None | str
        qa_config_name = self.qa_config_name

        batch_id: None | str
        if isinstance(self.batch_id, UUID):
            batch_id = str(self.batch_id)
        else:
            batch_id = self.batch_id

        environment_id = str(self.environment_id)

        problem_id: None | str
        if isinstance(self.problem_id, UUID):
            problem_id = str(self.problem_id)
        else:
            problem_id = self.problem_id

        problem_version_id: None | str
        if isinstance(self.problem_version_id, UUID):
            problem_version_id = str(self.problem_version_id)
        else:
            problem_version_id = self.problem_version_id

        kind = self.kind.value

        status = self.status.value

        container_image: None | str
        container_image = self.container_image

        external_run_id: None | str
        external_run_id = self.external_run_id

        error_message: None | str
        error_message = self.error_message

        execution_time_ms: float | None
        execution_time_ms = self.execution_time_ms

        total_cost_usd: None | str
        total_cost_usd = self.total_cost_usd

        attempt_count = self.attempt_count

        max_retries = self.max_retries

        started_at: None | str
        started_at = self.started_at

        completed_at: None | str
        completed_at = self.completed_at

        created_at = self.created_at

        updated_at = self.updated_at

        score: float | None
        score = self.score

        grade: None | str
        grade = self.grade

        problem_title: None | str
        problem_title = self.problem_title

        result: dict[str, Any] | None
        if isinstance(self.result, QaJobPageResponseDtoItemsItemResultType0):
            result = self.result.to_dict()
        else:
            result = self.result

        qa_run_config_version_id: None | str
        if isinstance(self.qa_run_config_version_id, UUID):
            qa_run_config_version_id = str(self.qa_run_config_version_id)
        else:
            qa_run_config_version_id = self.qa_run_config_version_id

        qa_run_config_name: None | str
        qa_run_config_name = self.qa_run_config_name

        qa_run_config_version_number: int | None
        qa_run_config_version_number = self.qa_run_config_version_number

        child_runs: list[dict[str, Any]] | Unset = UNSET
        if not isinstance(self.child_runs, Unset):
            child_runs = []
            for child_runs_item_data in self.child_runs:
                child_runs_item = child_runs_item_data.to_dict()
                child_runs.append(child_runs_item)




        field_dict: dict[str, Any] = {}

        field_dict.update({
            "id": id,
            "qaConfigId": qa_config_id,
            "qaConfigName": qa_config_name,
            "batchId": batch_id,
            "environmentId": environment_id,
            "problemId": problem_id,
            "problemVersionId": problem_version_id,
            "kind": kind,
            "status": status,
            "containerImage": container_image,
            "externalRunId": external_run_id,
            "errorMessage": error_message,
            "executionTimeMs": execution_time_ms,
            "totalCostUsd": total_cost_usd,
            "attemptCount": attempt_count,
            "maxRetries": max_retries,
            "startedAt": started_at,
            "completedAt": completed_at,
            "createdAt": created_at,
            "updatedAt": updated_at,
            "score": score,
            "grade": grade,
            "problemTitle": problem_title,
            "result": result,
            "qaRunConfigVersionId": qa_run_config_version_id,
            "qaRunConfigName": qa_run_config_name,
            "qaRunConfigVersionNumber": qa_run_config_version_number,
        })
        if child_runs is not UNSET:
            field_dict["childRuns"] = child_runs

        return field_dict



    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.qa_job_page_response_dto_items_item_child_runs_item import QaJobPageResponseDtoItemsItemChildRunsItem # noqa: PLC0415
        from ..models.qa_job_page_response_dto_items_item_result_type_0 import QaJobPageResponseDtoItemsItemResultType0 # noqa: PLC0415
        d = dict(src_dict)
        id = UUID(d.pop("id"))




        def _parse_qa_config_id(data: object) -> None | UUID:
            if data is None:
                return data
            try:
                if not isinstance(data, str):
                    raise TypeError()
                qa_config_id_type_0 = UUID(data)



                return qa_config_id_type_0
            except (TypeError, ValueError, AttributeError, KeyError):
                pass
            return cast(None | UUID, data)

        qa_config_id = _parse_qa_config_id(d.pop("qaConfigId"))


        def _parse_qa_config_name(data: object) -> None | str:
            if data is None:
                return data
            return cast(None | str, data)

        qa_config_name = _parse_qa_config_name(d.pop("qaConfigName"))


        def _parse_batch_id(data: object) -> None | UUID:
            if data is None:
                return data
            try:
                if not isinstance(data, str):
                    raise TypeError()
                batch_id_type_0 = UUID(data)



                return batch_id_type_0
            except (TypeError, ValueError, AttributeError, KeyError):
                pass
            return cast(None | UUID, data)

        batch_id = _parse_batch_id(d.pop("batchId"))


        environment_id = UUID(d.pop("environmentId"))




        def _parse_problem_id(data: object) -> None | UUID:
            if data is None:
                return data
            try:
                if not isinstance(data, str):
                    raise TypeError()
                problem_id_type_0 = UUID(data)



                return problem_id_type_0
            except (TypeError, ValueError, AttributeError, KeyError):
                pass
            return cast(None | UUID, data)

        problem_id = _parse_problem_id(d.pop("problemId"))


        def _parse_problem_version_id(data: object) -> None | UUID:
            if data is None:
                return data
            try:
                if not isinstance(data, str):
                    raise TypeError()
                problem_version_id_type_0 = UUID(data)



                return problem_version_id_type_0
            except (TypeError, ValueError, AttributeError, KeyError):
                pass
            return cast(None | UUID, data)

        problem_version_id = _parse_problem_version_id(d.pop("problemVersionId"))


        kind = QaJobPageResponseDtoItemsItemKind(d.pop("kind"))




        status = QaJobPageResponseDtoItemsItemStatus(d.pop("status"))




        def _parse_container_image(data: object) -> None | str:
            if data is None:
                return data
            return cast(None | str, data)

        container_image = _parse_container_image(d.pop("containerImage"))


        def _parse_external_run_id(data: object) -> None | str:
            if data is None:
                return data
            return cast(None | str, data)

        external_run_id = _parse_external_run_id(d.pop("externalRunId"))


        def _parse_error_message(data: object) -> None | str:
            if data is None:
                return data
            return cast(None | str, data)

        error_message = _parse_error_message(d.pop("errorMessage"))


        def _parse_execution_time_ms(data: object) -> float | None:
            if data is None:
                return data
            return cast(float | None, data)

        execution_time_ms = _parse_execution_time_ms(d.pop("executionTimeMs"))


        def _parse_total_cost_usd(data: object) -> None | str:
            if data is None:
                return data
            return cast(None | str, data)

        total_cost_usd = _parse_total_cost_usd(d.pop("totalCostUsd"))


        attempt_count = d.pop("attemptCount")

        max_retries = d.pop("maxRetries")

        def _parse_started_at(data: object) -> None | str:
            if data is None:
                return data
            return cast(None | str, data)

        started_at = _parse_started_at(d.pop("startedAt"))


        def _parse_completed_at(data: object) -> None | str:
            if data is None:
                return data
            return cast(None | str, data)

        completed_at = _parse_completed_at(d.pop("completedAt"))


        created_at = d.pop("createdAt")

        updated_at = d.pop("updatedAt")

        def _parse_score(data: object) -> float | None:
            if data is None:
                return data
            return cast(float | None, data)

        score = _parse_score(d.pop("score"))


        def _parse_grade(data: object) -> None | str:
            if data is None:
                return data
            return cast(None | str, data)

        grade = _parse_grade(d.pop("grade"))


        def _parse_problem_title(data: object) -> None | str:
            if data is None:
                return data
            return cast(None | str, data)

        problem_title = _parse_problem_title(d.pop("problemTitle"))


        def _parse_result(data: object) -> None | QaJobPageResponseDtoItemsItemResultType0:
            if data is None:
                return data
            try:
                if not isinstance(data, dict):
                    raise TypeError()
                result_type_0 = QaJobPageResponseDtoItemsItemResultType0.from_dict(data)



                return result_type_0
            except (TypeError, ValueError, AttributeError, KeyError):
                pass
            return cast(None | QaJobPageResponseDtoItemsItemResultType0, data)

        result = _parse_result(d.pop("result"))


        def _parse_qa_run_config_version_id(data: object) -> None | UUID:
            if data is None:
                return data
            try:
                if not isinstance(data, str):
                    raise TypeError()
                qa_run_config_version_id_type_0 = UUID(data)



                return qa_run_config_version_id_type_0
            except (TypeError, ValueError, AttributeError, KeyError):
                pass
            return cast(None | UUID, data)

        qa_run_config_version_id = _parse_qa_run_config_version_id(d.pop("qaRunConfigVersionId"))


        def _parse_qa_run_config_name(data: object) -> None | str:
            if data is None:
                return data
            return cast(None | str, data)

        qa_run_config_name = _parse_qa_run_config_name(d.pop("qaRunConfigName"))


        def _parse_qa_run_config_version_number(data: object) -> int | None:
            if data is None:
                return data
            return cast(int | None, data)

        qa_run_config_version_number = _parse_qa_run_config_version_number(d.pop("qaRunConfigVersionNumber"))


        _child_runs = d.pop("childRuns", UNSET)
        child_runs: list[QaJobPageResponseDtoItemsItemChildRunsItem] | Unset = UNSET
        if _child_runs is not UNSET:
            child_runs = []
            for child_runs_item_data in _child_runs:
                child_runs_item = QaJobPageResponseDtoItemsItemChildRunsItem.from_dict(child_runs_item_data)



                child_runs.append(child_runs_item)


        qa_job_page_response_dto_items_item = cls(
            id=id,
            qa_config_id=qa_config_id,
            qa_config_name=qa_config_name,
            batch_id=batch_id,
            environment_id=environment_id,
            problem_id=problem_id,
            problem_version_id=problem_version_id,
            kind=kind,
            status=status,
            container_image=container_image,
            external_run_id=external_run_id,
            error_message=error_message,
            execution_time_ms=execution_time_ms,
            total_cost_usd=total_cost_usd,
            attempt_count=attempt_count,
            max_retries=max_retries,
            started_at=started_at,
            completed_at=completed_at,
            created_at=created_at,
            updated_at=updated_at,
            score=score,
            grade=grade,
            problem_title=problem_title,
            result=result,
            qa_run_config_version_id=qa_run_config_version_id,
            qa_run_config_name=qa_run_config_name,
            qa_run_config_version_number=qa_run_config_version_number,
            child_runs=child_runs,
        )

        return qa_job_page_response_dto_items_item

