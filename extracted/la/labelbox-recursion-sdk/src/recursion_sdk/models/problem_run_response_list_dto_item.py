from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar, BinaryIO, TextIO, TYPE_CHECKING, Generator

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

from ..models.problem_run_response_list_dto_item_provenance_type_0 import ProblemRunResponseListDtoItemProvenanceType0
from ..models.problem_run_response_list_dto_item_source_type_0 import ProblemRunResponseListDtoItemSourceType0
from ..models.problem_run_response_list_dto_item_status import ProblemRunResponseListDtoItemStatus
from ..types import UNSET, Unset
from typing import cast
from uuid import UUID
import datetime

if TYPE_CHECKING:
  from ..models.grading_config_agentic import GradingConfigAgentic
  from ..models.grading_config_compute_exec import GradingConfigComputeExec
  from ..models.grading_config_max import GradingConfigMax
  from ..models.grading_config_mcp_tool_call import GradingConfigMcpToolCall
  from ..models.grading_config_none import GradingConfigNone
  from ..models.grading_config_programmatic import GradingConfigProgrammatic
  from ..models.grading_config_rubric import GradingConfigRubric
  from ..models.grading_config_weighted_sum import GradingConfigWeightedSum





T = TypeVar("T", bound="ProblemRunResponseListDtoItem")



@_attrs_define
class ProblemRunResponseListDtoItem:
    """ A single solver attempt against one problem version, with its grading outcome.

        Attributes:
            id (UUID): Stable problem-run identifier (UUID). One solver attempt at one problem version.
            job_id (None | UUID): Legacy job that launched this run. Null for jobs-v2, interactive, and evaluation runs.
            run_name (None | str): User-supplied display name for the run. Null for unnamed runs such as Taiga imports,
                interactive single runs, and evaluation-spawned runs.
            batch_id (None | UUID): Identifier shared by every run submitted in the same batch. Null for standalone runs
                such as interactive single runs, single-attempt reruns, and Taiga imports.
            job_v2_id (None | UUID): jobs_v2 id of the leaf job that produced this run, used to key the cancel action. Null
                when no v2 job is linked.
            top_job_id (None | UUID): jobs_v2 id of the top job of the tree that produced this run. Null when the run has no
                linked job or its tree predates the pointer.
            top_job_type (None | str): Job type of the top job of this run's tree, which decides whether the tree is this
                submission alone or a larger piece of work. Null whenever the top job is unknown. Example: problem_run_batch.
            top_job_environment_id (None | UUID): One environment the top job is linked to, used to build an environment-
                scoped link to it. Null when the top job is unknown or has no environment link.
            problem_id (UUID): Stable problem identifier (UUID).
            problem_version_id (None | UUID): Specific problem version exercised by the run. Null for legacy runs that
                predate versioning.
            status (ProblemRunResponseListDtoItemStatus): Current lifecycle status of the run.
            attempt_number (int): One-based attempt number within the parent job for this problem. Example: 1.
            queue_position (int | None): Position in the pending queue when applicable. Null once the run has started.
                Example: 5.
            prompt (None | str): Final prompt handed to the solver. Null for runs that omit a prompt.
            execution_time_ms (int | None): Wall-clock duration of the solver execution in milliseconds. Null until the run
                completes. Example: 42000.
            final_score (float | None): Aggregated final score after grading. Null until grading completes. Example: 0.83.
            error_message (None | str): Error detail if the run failed. Null on success or while still running.
            api_model_name (None | str): Solver model used for this run. Null when no model was bound.
            grading_model_name (None | str): Grader model explicitly pinned for this run, or null when the model comes from
                the resolved grader run config or grading uses no model.
            turns_count (int | None): Number of solver turns observed during the run. Null until the run completes. Example:
                12.
            created_at (datetime.datetime): Timestamp when the run row was created (ISO-8601, UTC).
            started_at (datetime.datetime | None): Timestamp when solver execution began (ISO-8601, UTC). Null until the run
                starts.
            completed_at (datetime.datetime | None): Timestamp when the run reached a terminal status (ISO-8601, UTC). Null
                while in-flight.
            transcript (None | str): Inlined solver transcript when small enough to embed. Null when stored separately.
            source (None | ProblemRunResponseListDtoItemSourceType0): Origin of the run: a queued batch job (job), an
                evaluation comparison run (evaluation), or a legacy interactive origin (interactive, interactive_local_docker)
                retained for historical rows. Null for rows that predate source tracking or were imported from Taiga.
            provenance (None | ProblemRunResponseListDtoItemProvenanceType0): Orchestration source that created the run:
                'taiga' for a Taiga import, 'v2' for jobs-v2, or null for native legacy-jobs runs.
            graded_at (datetime.datetime | None): Timestamp when grading finished (ISO-8601, UTC). Null until grading
                completes.
            grading_error (None | str): Error detail from grading if it failed. Null on success or while still running.
            grading_justification (None | str): Aggregated grader justification text. Null until grading completes.
            grading_config (GradingConfigAgentic | GradingConfigComputeExec | GradingConfigMax | GradingConfigMcpToolCall |
                GradingConfigNone | GradingConfigProgrammatic | GradingConfigRubric | GradingConfigWeightedSum | None): Grading
                configuration used for this run. Null for runs that ran without a grading config.
            solver_run_config_version_id (None | UUID): Run-config-version that drove the solver, captured at INSERT time.
                Null for legacy runs or runs without a binding.
            solver_run_config_name (None | str): Display name of the run-config that drove the solver. Non-null whenever a
                solver run-config version was captured.
            solver_run_config_version_number (int | None): Version number (1-based) of the solver run-config-version. Non-
                null whenever a solver run-config version was captured. Example: 2.
            grader_run_config_version_id (None | UUID): Representative grader run-config-version captured from grading sub-
                runs. Null when no qualifying grader audit exists.
            grader_run_config_name (None | str): Display name of the representative grader run-config. Non-null whenever a
                representative grader run-config version was captured.
            grader_run_config_version_number (int | None): Version number (1-based) of the representative grader run-config-
                version. Non-null whenever a representative grader run-config version was captured. Example: 2.
            output_files_truncated (bool): True when output-file ingestion hit a cap (file count, root file count, per-file
                bytes, total bytes, depth, or directory count) or lost files to a partial-listing/signing failure, and stored
                only a subset of the files the run produced.
            output_files_listed_count (int | None): Number of output files observed before ingestion stopped — a lower bound
                when truncated. Null for runs recorded before this was tracked. Example: 1200.
            has_retained_solver_run (bool | Unset): Whether this run retains an agent-service solver workspace that can be
                reused for re-grading. Absent responses are treated as unavailable.
            regrade_count (int | Unset): Number of re-grades represented by the run’s live grade-history snapshots. Absent
                responses are treated as zero. Example: 0.
     """

    id: UUID
    job_id: None | UUID
    run_name: None | str
    batch_id: None | UUID
    job_v2_id: None | UUID
    top_job_id: None | UUID
    top_job_type: None | str
    top_job_environment_id: None | UUID
    problem_id: UUID
    problem_version_id: None | UUID
    status: ProblemRunResponseListDtoItemStatus
    attempt_number: int
    queue_position: int | None
    prompt: None | str
    execution_time_ms: int | None
    final_score: float | None
    error_message: None | str
    api_model_name: None | str
    grading_model_name: None | str
    turns_count: int | None
    created_at: datetime.datetime
    started_at: datetime.datetime | None
    completed_at: datetime.datetime | None
    transcript: None | str
    source: None | ProblemRunResponseListDtoItemSourceType0
    provenance: None | ProblemRunResponseListDtoItemProvenanceType0
    graded_at: datetime.datetime | None
    grading_error: None | str
    grading_justification: None | str
    grading_config: GradingConfigAgentic | GradingConfigComputeExec | GradingConfigMax | GradingConfigMcpToolCall | GradingConfigNone | GradingConfigProgrammatic | GradingConfigRubric | GradingConfigWeightedSum | None
    solver_run_config_version_id: None | UUID
    solver_run_config_name: None | str
    solver_run_config_version_number: int | None
    grader_run_config_version_id: None | UUID
    grader_run_config_name: None | str
    grader_run_config_version_number: int | None
    output_files_truncated: bool
    output_files_listed_count: int | None
    has_retained_solver_run: bool | Unset = UNSET
    regrade_count: int | Unset = UNSET





    def to_dict(self) -> dict[str, Any]:
        from ..models.grading_config_agentic import GradingConfigAgentic # noqa: PLC0415
        from ..models.grading_config_compute_exec import GradingConfigComputeExec # noqa: PLC0415
        from ..models.grading_config_max import GradingConfigMax # noqa: PLC0415
        from ..models.grading_config_mcp_tool_call import GradingConfigMcpToolCall # noqa: PLC0415
        from ..models.grading_config_none import GradingConfigNone # noqa: PLC0415
        from ..models.grading_config_programmatic import GradingConfigProgrammatic # noqa: PLC0415
        from ..models.grading_config_rubric import GradingConfigRubric # noqa: PLC0415
        from ..models.grading_config_weighted_sum import GradingConfigWeightedSum # noqa: PLC0415
        id = str(self.id)

        job_id: None | str
        if isinstance(self.job_id, UUID):
            job_id = str(self.job_id)
        else:
            job_id = self.job_id

        run_name: None | str
        run_name = self.run_name

        batch_id: None | str
        if isinstance(self.batch_id, UUID):
            batch_id = str(self.batch_id)
        else:
            batch_id = self.batch_id

        job_v2_id: None | str
        if isinstance(self.job_v2_id, UUID):
            job_v2_id = str(self.job_v2_id)
        else:
            job_v2_id = self.job_v2_id

        top_job_id: None | str
        if isinstance(self.top_job_id, UUID):
            top_job_id = str(self.top_job_id)
        else:
            top_job_id = self.top_job_id

        top_job_type: None | str
        top_job_type = self.top_job_type

        top_job_environment_id: None | str
        if isinstance(self.top_job_environment_id, UUID):
            top_job_environment_id = str(self.top_job_environment_id)
        else:
            top_job_environment_id = self.top_job_environment_id

        problem_id = str(self.problem_id)

        problem_version_id: None | str
        if isinstance(self.problem_version_id, UUID):
            problem_version_id = str(self.problem_version_id)
        else:
            problem_version_id = self.problem_version_id

        status = self.status.value

        attempt_number = self.attempt_number

        queue_position: int | None
        queue_position = self.queue_position

        prompt: None | str
        prompt = self.prompt

        execution_time_ms: int | None
        execution_time_ms = self.execution_time_ms

        final_score: float | None
        final_score = self.final_score

        error_message: None | str
        error_message = self.error_message

        api_model_name: None | str
        api_model_name = self.api_model_name

        grading_model_name: None | str
        grading_model_name = self.grading_model_name

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

        transcript: None | str
        transcript = self.transcript

        source: None | str
        if isinstance(self.source, ProblemRunResponseListDtoItemSourceType0):
            source = self.source.value
        else:
            source = self.source

        provenance: None | str
        if isinstance(self.provenance, ProblemRunResponseListDtoItemProvenanceType0):
            provenance = self.provenance.value
        else:
            provenance = self.provenance

        graded_at: None | str
        if isinstance(self.graded_at, datetime.datetime):
            graded_at = self.graded_at.isoformat()
        else:
            graded_at = self.graded_at

        grading_error: None | str
        grading_error = self.grading_error

        grading_justification: None | str
        grading_justification = self.grading_justification

        grading_config: dict[str, Any] | None
        if isinstance(self.grading_config, GradingConfigNone):
            grading_config = self.grading_config.to_dict()
        elif isinstance(self.grading_config, GradingConfigRubric):
            grading_config = self.grading_config.to_dict()
        elif isinstance(self.grading_config, GradingConfigAgentic):
            grading_config = self.grading_config.to_dict()
        elif isinstance(self.grading_config, GradingConfigProgrammatic):
            grading_config = self.grading_config.to_dict()
        elif isinstance(self.grading_config, GradingConfigMcpToolCall):
            grading_config = self.grading_config.to_dict()
        elif isinstance(self.grading_config, GradingConfigComputeExec):
            grading_config = self.grading_config.to_dict()
        elif isinstance(self.grading_config, GradingConfigWeightedSum):
            grading_config = self.grading_config.to_dict()
        elif isinstance(self.grading_config, GradingConfigMax):
            grading_config = self.grading_config.to_dict()
        else:
            grading_config = self.grading_config

        solver_run_config_version_id: None | str
        if isinstance(self.solver_run_config_version_id, UUID):
            solver_run_config_version_id = str(self.solver_run_config_version_id)
        else:
            solver_run_config_version_id = self.solver_run_config_version_id

        solver_run_config_name: None | str
        solver_run_config_name = self.solver_run_config_name

        solver_run_config_version_number: int | None
        solver_run_config_version_number = self.solver_run_config_version_number

        grader_run_config_version_id: None | str
        if isinstance(self.grader_run_config_version_id, UUID):
            grader_run_config_version_id = str(self.grader_run_config_version_id)
        else:
            grader_run_config_version_id = self.grader_run_config_version_id

        grader_run_config_name: None | str
        grader_run_config_name = self.grader_run_config_name

        grader_run_config_version_number: int | None
        grader_run_config_version_number = self.grader_run_config_version_number

        output_files_truncated = self.output_files_truncated

        output_files_listed_count: int | None
        output_files_listed_count = self.output_files_listed_count

        has_retained_solver_run = self.has_retained_solver_run

        regrade_count = self.regrade_count


        field_dict: dict[str, Any] = {}

        field_dict.update({
            "id": id,
            "jobId": job_id,
            "runName": run_name,
            "batchId": batch_id,
            "jobV2Id": job_v2_id,
            "topJobId": top_job_id,
            "topJobType": top_job_type,
            "topJobEnvironmentId": top_job_environment_id,
            "problemId": problem_id,
            "problemVersionId": problem_version_id,
            "status": status,
            "attemptNumber": attempt_number,
            "queuePosition": queue_position,
            "prompt": prompt,
            "executionTimeMs": execution_time_ms,
            "finalScore": final_score,
            "errorMessage": error_message,
            "apiModelName": api_model_name,
            "gradingModelName": grading_model_name,
            "turnsCount": turns_count,
            "createdAt": created_at,
            "startedAt": started_at,
            "completedAt": completed_at,
            "transcript": transcript,
            "source": source,
            "provenance": provenance,
            "gradedAt": graded_at,
            "gradingError": grading_error,
            "gradingJustification": grading_justification,
            "gradingConfig": grading_config,
            "solverRunConfigVersionId": solver_run_config_version_id,
            "solverRunConfigName": solver_run_config_name,
            "solverRunConfigVersionNumber": solver_run_config_version_number,
            "graderRunConfigVersionId": grader_run_config_version_id,
            "graderRunConfigName": grader_run_config_name,
            "graderRunConfigVersionNumber": grader_run_config_version_number,
            "outputFilesTruncated": output_files_truncated,
            "outputFilesListedCount": output_files_listed_count,
        })
        if has_retained_solver_run is not UNSET:
            field_dict["hasRetainedSolverRun"] = has_retained_solver_run
        if regrade_count is not UNSET:
            field_dict["regradeCount"] = regrade_count

        return field_dict



    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.grading_config_agentic import GradingConfigAgentic # noqa: PLC0415
        from ..models.grading_config_compute_exec import GradingConfigComputeExec # noqa: PLC0415
        from ..models.grading_config_max import GradingConfigMax # noqa: PLC0415
        from ..models.grading_config_mcp_tool_call import GradingConfigMcpToolCall # noqa: PLC0415
        from ..models.grading_config_none import GradingConfigNone # noqa: PLC0415
        from ..models.grading_config_programmatic import GradingConfigProgrammatic # noqa: PLC0415
        from ..models.grading_config_rubric import GradingConfigRubric # noqa: PLC0415
        from ..models.grading_config_weighted_sum import GradingConfigWeightedSum # noqa: PLC0415
        d = dict(src_dict)
        id = UUID(d.pop("id"))




        def _parse_job_id(data: object) -> None | UUID:
            if data is None:
                return data
            try:
                if not isinstance(data, str):
                    raise TypeError()
                job_id_type_0 = UUID(data)



                return job_id_type_0
            except (TypeError, ValueError, AttributeError, KeyError):
                pass
            return cast(None | UUID, data)

        job_id = _parse_job_id(d.pop("jobId"))


        def _parse_run_name(data: object) -> None | str:
            if data is None:
                return data
            return cast(None | str, data)

        run_name = _parse_run_name(d.pop("runName"))


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


        def _parse_job_v2_id(data: object) -> None | UUID:
            if data is None:
                return data
            try:
                if not isinstance(data, str):
                    raise TypeError()
                job_v2_id_type_0 = UUID(data)



                return job_v2_id_type_0
            except (TypeError, ValueError, AttributeError, KeyError):
                pass
            return cast(None | UUID, data)

        job_v2_id = _parse_job_v2_id(d.pop("jobV2Id"))


        def _parse_top_job_id(data: object) -> None | UUID:
            if data is None:
                return data
            try:
                if not isinstance(data, str):
                    raise TypeError()
                top_job_id_type_0 = UUID(data)



                return top_job_id_type_0
            except (TypeError, ValueError, AttributeError, KeyError):
                pass
            return cast(None | UUID, data)

        top_job_id = _parse_top_job_id(d.pop("topJobId"))


        def _parse_top_job_type(data: object) -> None | str:
            if data is None:
                return data
            return cast(None | str, data)

        top_job_type = _parse_top_job_type(d.pop("topJobType"))


        def _parse_top_job_environment_id(data: object) -> None | UUID:
            if data is None:
                return data
            try:
                if not isinstance(data, str):
                    raise TypeError()
                top_job_environment_id_type_0 = UUID(data)



                return top_job_environment_id_type_0
            except (TypeError, ValueError, AttributeError, KeyError):
                pass
            return cast(None | UUID, data)

        top_job_environment_id = _parse_top_job_environment_id(d.pop("topJobEnvironmentId"))


        problem_id = UUID(d.pop("problemId"))




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


        status = ProblemRunResponseListDtoItemStatus(d.pop("status"))




        attempt_number = d.pop("attemptNumber")

        def _parse_queue_position(data: object) -> int | None:
            if data is None:
                return data
            return cast(int | None, data)

        queue_position = _parse_queue_position(d.pop("queuePosition"))


        def _parse_prompt(data: object) -> None | str:
            if data is None:
                return data
            return cast(None | str, data)

        prompt = _parse_prompt(d.pop("prompt"))


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


        def _parse_error_message(data: object) -> None | str:
            if data is None:
                return data
            return cast(None | str, data)

        error_message = _parse_error_message(d.pop("errorMessage"))


        def _parse_api_model_name(data: object) -> None | str:
            if data is None:
                return data
            return cast(None | str, data)

        api_model_name = _parse_api_model_name(d.pop("apiModelName"))


        def _parse_grading_model_name(data: object) -> None | str:
            if data is None:
                return data
            return cast(None | str, data)

        grading_model_name = _parse_grading_model_name(d.pop("gradingModelName"))


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


        def _parse_transcript(data: object) -> None | str:
            if data is None:
                return data
            return cast(None | str, data)

        transcript = _parse_transcript(d.pop("transcript"))


        def _parse_source(data: object) -> None | ProblemRunResponseListDtoItemSourceType0:
            if data is None:
                return data
            try:
                if not isinstance(data, str):
                    raise TypeError()
                source_type_0 = ProblemRunResponseListDtoItemSourceType0(data)



                return source_type_0
            except (TypeError, ValueError, AttributeError, KeyError):
                pass
            return cast(None | ProblemRunResponseListDtoItemSourceType0, data)

        source = _parse_source(d.pop("source"))


        def _parse_provenance(data: object) -> None | ProblemRunResponseListDtoItemProvenanceType0:
            if data is None:
                return data
            try:
                if not isinstance(data, str):
                    raise TypeError()
                provenance_type_0 = ProblemRunResponseListDtoItemProvenanceType0(data)



                return provenance_type_0
            except (TypeError, ValueError, AttributeError, KeyError):
                pass
            return cast(None | ProblemRunResponseListDtoItemProvenanceType0, data)

        provenance = _parse_provenance(d.pop("provenance"))


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


        def _parse_grading_error(data: object) -> None | str:
            if data is None:
                return data
            return cast(None | str, data)

        grading_error = _parse_grading_error(d.pop("gradingError"))


        def _parse_grading_justification(data: object) -> None | str:
            if data is None:
                return data
            return cast(None | str, data)

        grading_justification = _parse_grading_justification(d.pop("gradingJustification"))


        def _parse_grading_config(data: object) -> GradingConfigAgentic | GradingConfigComputeExec | GradingConfigMax | GradingConfigMcpToolCall | GradingConfigNone | GradingConfigProgrammatic | GradingConfigRubric | GradingConfigWeightedSum | None:
            if data is None:
                return data
            try:
                if not isinstance(data, dict):
                    raise TypeError()
                componentsschemas_grading_config_type_0 = GradingConfigNone.from_dict(data)



                return componentsschemas_grading_config_type_0
            except (TypeError, ValueError, AttributeError, KeyError):
                pass
            try:
                if not isinstance(data, dict):
                    raise TypeError()
                componentsschemas_grading_config_type_1 = GradingConfigRubric.from_dict(data)



                return componentsschemas_grading_config_type_1
            except (TypeError, ValueError, AttributeError, KeyError):
                pass
            try:
                if not isinstance(data, dict):
                    raise TypeError()
                componentsschemas_grading_config_type_2 = GradingConfigAgentic.from_dict(data)



                return componentsschemas_grading_config_type_2
            except (TypeError, ValueError, AttributeError, KeyError):
                pass
            try:
                if not isinstance(data, dict):
                    raise TypeError()
                componentsschemas_grading_config_type_3 = GradingConfigProgrammatic.from_dict(data)



                return componentsschemas_grading_config_type_3
            except (TypeError, ValueError, AttributeError, KeyError):
                pass
            try:
                if not isinstance(data, dict):
                    raise TypeError()
                componentsschemas_grading_config_type_4 = GradingConfigMcpToolCall.from_dict(data)



                return componentsschemas_grading_config_type_4
            except (TypeError, ValueError, AttributeError, KeyError):
                pass
            try:
                if not isinstance(data, dict):
                    raise TypeError()
                componentsschemas_grading_config_type_5 = GradingConfigComputeExec.from_dict(data)



                return componentsschemas_grading_config_type_5
            except (TypeError, ValueError, AttributeError, KeyError):
                pass
            try:
                if not isinstance(data, dict):
                    raise TypeError()
                componentsschemas_grading_config_type_6 = GradingConfigWeightedSum.from_dict(data)



                return componentsschemas_grading_config_type_6
            except (TypeError, ValueError, AttributeError, KeyError):
                pass
            try:
                if not isinstance(data, dict):
                    raise TypeError()
                componentsschemas_grading_config_type_7 = GradingConfigMax.from_dict(data)



                return componentsschemas_grading_config_type_7
            except (TypeError, ValueError, AttributeError, KeyError):
                pass
            return cast(GradingConfigAgentic | GradingConfigComputeExec | GradingConfigMax | GradingConfigMcpToolCall | GradingConfigNone | GradingConfigProgrammatic | GradingConfigRubric | GradingConfigWeightedSum | None, data)

        grading_config = _parse_grading_config(d.pop("gradingConfig"))


        def _parse_solver_run_config_version_id(data: object) -> None | UUID:
            if data is None:
                return data
            try:
                if not isinstance(data, str):
                    raise TypeError()
                solver_run_config_version_id_type_0 = UUID(data)



                return solver_run_config_version_id_type_0
            except (TypeError, ValueError, AttributeError, KeyError):
                pass
            return cast(None | UUID, data)

        solver_run_config_version_id = _parse_solver_run_config_version_id(d.pop("solverRunConfigVersionId"))


        def _parse_solver_run_config_name(data: object) -> None | str:
            if data is None:
                return data
            return cast(None | str, data)

        solver_run_config_name = _parse_solver_run_config_name(d.pop("solverRunConfigName"))


        def _parse_solver_run_config_version_number(data: object) -> int | None:
            if data is None:
                return data
            return cast(int | None, data)

        solver_run_config_version_number = _parse_solver_run_config_version_number(d.pop("solverRunConfigVersionNumber"))


        def _parse_grader_run_config_version_id(data: object) -> None | UUID:
            if data is None:
                return data
            try:
                if not isinstance(data, str):
                    raise TypeError()
                grader_run_config_version_id_type_0 = UUID(data)



                return grader_run_config_version_id_type_0
            except (TypeError, ValueError, AttributeError, KeyError):
                pass
            return cast(None | UUID, data)

        grader_run_config_version_id = _parse_grader_run_config_version_id(d.pop("graderRunConfigVersionId"))


        def _parse_grader_run_config_name(data: object) -> None | str:
            if data is None:
                return data
            return cast(None | str, data)

        grader_run_config_name = _parse_grader_run_config_name(d.pop("graderRunConfigName"))


        def _parse_grader_run_config_version_number(data: object) -> int | None:
            if data is None:
                return data
            return cast(int | None, data)

        grader_run_config_version_number = _parse_grader_run_config_version_number(d.pop("graderRunConfigVersionNumber"))


        output_files_truncated = d.pop("outputFilesTruncated")

        def _parse_output_files_listed_count(data: object) -> int | None:
            if data is None:
                return data
            return cast(int | None, data)

        output_files_listed_count = _parse_output_files_listed_count(d.pop("outputFilesListedCount"))


        has_retained_solver_run = d.pop("hasRetainedSolverRun", UNSET)

        regrade_count = d.pop("regradeCount", UNSET)

        problem_run_response_list_dto_item = cls(
            id=id,
            job_id=job_id,
            run_name=run_name,
            batch_id=batch_id,
            job_v2_id=job_v2_id,
            top_job_id=top_job_id,
            top_job_type=top_job_type,
            top_job_environment_id=top_job_environment_id,
            problem_id=problem_id,
            problem_version_id=problem_version_id,
            status=status,
            attempt_number=attempt_number,
            queue_position=queue_position,
            prompt=prompt,
            execution_time_ms=execution_time_ms,
            final_score=final_score,
            error_message=error_message,
            api_model_name=api_model_name,
            grading_model_name=grading_model_name,
            turns_count=turns_count,
            created_at=created_at,
            started_at=started_at,
            completed_at=completed_at,
            transcript=transcript,
            source=source,
            provenance=provenance,
            graded_at=graded_at,
            grading_error=grading_error,
            grading_justification=grading_justification,
            grading_config=grading_config,
            solver_run_config_version_id=solver_run_config_version_id,
            solver_run_config_name=solver_run_config_name,
            solver_run_config_version_number=solver_run_config_version_number,
            grader_run_config_version_id=grader_run_config_version_id,
            grader_run_config_name=grader_run_config_name,
            grader_run_config_version_number=grader_run_config_version_number,
            output_files_truncated=output_files_truncated,
            output_files_listed_count=output_files_listed_count,
            has_retained_solver_run=has_retained_solver_run,
            regrade_count=regrade_count,
        )

        return problem_run_response_list_dto_item

