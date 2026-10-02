from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar, BinaryIO, TextIO, TYPE_CHECKING, Generator

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

from ..models.evaluation_detail_response_dto_kind import EvaluationDetailResponseDtoKind
from ..models.evaluation_detail_response_dto_status import EvaluationDetailResponseDtoStatus
from typing import cast
from uuid import UUID
import datetime

if TYPE_CHECKING:
  from ..models.evaluation_detail_response_dto_metadata import EvaluationDetailResponseDtoMetadata
  from ..models.evaluation_detail_response_dto_problems_item import EvaluationDetailResponseDtoProblemsItem
  from ..models.evaluation_detail_response_dto_solvers_item import EvaluationDetailResponseDtoSolversItem





T = TypeVar("T", bound="EvaluationDetailResponseDto")



@_attrs_define
class EvaluationDetailResponseDto:
    """ Detail view of an evaluation, including the solver and problem rosters.

        Example:
            {'id': '40811982-da7a-42bb-9963-5ca612372c63', 'kind': 'solve_and_grade', 'name': 'claude-sonnet-baseline',
                'description': 'Baseline run of Claude Sonnet against the surface-defect detection problem.', 'status':
                'completed', 'nAttemptsPerProblem': 3, 'tags': [], 'graderRunConfigVersionId': None, 'totalSolvers': 1,
                'totalProblems': 1, 'createdAt': '2026-01-15T09:30:00.000Z', 'updatedAt': '2026-01-15T10:05:00.000Z',
                'startedAt': '2026-01-15T09:30:12.000Z', 'completedAt': '2026-01-15T10:05:00.000Z', 'metadata':
                {'schemaVersion': 1, 'attemptsPerProblem': 3}, 'solvers': [{'id': 'b5d0f1c2-3e4a-4b6c-8d7e-9f0a1b2c3d4e',
                'evaluationId': '40811982-da7a-42bb-9963-5ca612372c63', 'displayName': 'claude-sonnet-baseline',
                'runConfigVersionId': 'e9d0f1c2-3e4a-4b6c-8d7e-9f0a1b2c3d4e', 'solverLabel': 'claude-sonnet-baseline',
                'jobStatus': 'completed', 'sortOrder': 0, 'metadata': {'schemaVersion': 1}}], 'problems': [{'id':
                'c7e1a2b3-4d5e-4f6a-8b7c-9d0e1f2a3b4c', 'evaluationId': '40811982-da7a-42bb-9963-5ca612372c63', 'problemId':
                '2d3fe029-a7d1-4747-9d09-81b976087bbb', 'problemVersionId': '0c3ac467-57e1-4074-b57d-b6a7be392f71',
                'environmentId': '784e2386-e297-4f9d-a886-838422383b65', 'problemTitle': 'Detect surface defects on machined
                parts', 'environmentName': 'vision-agent-eval', 'versionLabel': '1.0.0', 'sortOrder': 0}]}

        Attributes:
            id (UUID): Stable evaluation identifier (UUID). An evaluation is a multi-problem comparison run.
            kind (EvaluationDetailResponseDtoKind): Which evaluation shape this is. Defaults to solve-and-grade for pre-kind
                records. Default: EvaluationDetailResponseDtoKind.SOLVE_AND_GRADE.
            name (str): Human-readable display name of the evaluation.
            description (str): Free-form description of the evaluation. Empty string when not provided.
            status (EvaluationDetailResponseDtoStatus): Lifecycle status of the evaluation.
            n_attempts_per_problem (int): Number of attempts each solver makes against each problem, read from the
                evaluation metadata. Example: 3.
            tags (list[str]): Free-form tags for list filtering. Empty when the evaluation is untagged.
            grader_run_config_version_id (None | UUID): Locked run-config version (kind "grader") pinned as the grader for
                every run in this evaluation. Null when grading falls back to the problem-version / environment grader default.
                One grader per evaluation keeps every solver on the same reward scale.
            total_solvers (int): Number of solvers participating in this evaluation. Example: 2.
            total_problems (int): Number of problems included in this evaluation. Example: 10.
            created_at (datetime.datetime): Timestamp when the evaluation was created (ISO-8601, UTC).
            updated_at (datetime.datetime): Timestamp when the evaluation was last updated (ISO-8601, UTC).
            started_at (datetime.datetime | None): Timestamp when the evaluation began running (ISO-8601, UTC). Null while
                still pending.
            completed_at (datetime.datetime | None): Timestamp when the evaluation reached a terminal status (ISO-8601,
                UTC). Null while still running or pending.
            metadata (EvaluationDetailResponseDtoMetadata): Orchestration metadata persisted on the evaluation (attempts per
                problem, success threshold).
            solvers (list[EvaluationDetailResponseDtoSolversItem]): Solvers participating in this evaluation, in display
                order.
            problems (list[EvaluationDetailResponseDtoProblemsItem]): Problems included in this evaluation, in display
                order.
     """

    id: UUID
    name: str
    description: str
    status: EvaluationDetailResponseDtoStatus
    n_attempts_per_problem: int
    tags: list[str]
    grader_run_config_version_id: None | UUID
    total_solvers: int
    total_problems: int
    created_at: datetime.datetime
    updated_at: datetime.datetime
    started_at: datetime.datetime | None
    completed_at: datetime.datetime | None
    metadata: EvaluationDetailResponseDtoMetadata
    solvers: list[EvaluationDetailResponseDtoSolversItem]
    problems: list[EvaluationDetailResponseDtoProblemsItem]
    kind: EvaluationDetailResponseDtoKind = EvaluationDetailResponseDtoKind.SOLVE_AND_GRADE





    def to_dict(self) -> dict[str, Any]:
        from ..models.evaluation_detail_response_dto_metadata import EvaluationDetailResponseDtoMetadata # noqa: PLC0415
        from ..models.evaluation_detail_response_dto_problems_item import EvaluationDetailResponseDtoProblemsItem # noqa: PLC0415
        from ..models.evaluation_detail_response_dto_solvers_item import EvaluationDetailResponseDtoSolversItem # noqa: PLC0415
        id = str(self.id)

        kind = self.kind.value

        name = self.name

        description = self.description

        status = self.status.value

        n_attempts_per_problem = self.n_attempts_per_problem

        tags = self.tags



        grader_run_config_version_id: None | str
        if isinstance(self.grader_run_config_version_id, UUID):
            grader_run_config_version_id = str(self.grader_run_config_version_id)
        else:
            grader_run_config_version_id = self.grader_run_config_version_id

        total_solvers = self.total_solvers

        total_problems = self.total_problems

        created_at = self.created_at.isoformat()

        updated_at = self.updated_at.isoformat()

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

        metadata = self.metadata.to_dict()

        solvers = []
        for solvers_item_data in self.solvers:
            solvers_item = solvers_item_data.to_dict()
            solvers.append(solvers_item)



        problems = []
        for problems_item_data in self.problems:
            problems_item = problems_item_data.to_dict()
            problems.append(problems_item)




        field_dict: dict[str, Any] = {}

        field_dict.update({
            "id": id,
            "kind": kind,
            "name": name,
            "description": description,
            "status": status,
            "nAttemptsPerProblem": n_attempts_per_problem,
            "tags": tags,
            "graderRunConfigVersionId": grader_run_config_version_id,
            "totalSolvers": total_solvers,
            "totalProblems": total_problems,
            "createdAt": created_at,
            "updatedAt": updated_at,
            "startedAt": started_at,
            "completedAt": completed_at,
            "metadata": metadata,
            "solvers": solvers,
            "problems": problems,
        })

        return field_dict



    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.evaluation_detail_response_dto_metadata import EvaluationDetailResponseDtoMetadata # noqa: PLC0415
        from ..models.evaluation_detail_response_dto_problems_item import EvaluationDetailResponseDtoProblemsItem # noqa: PLC0415
        from ..models.evaluation_detail_response_dto_solvers_item import EvaluationDetailResponseDtoSolversItem # noqa: PLC0415
        d = dict(src_dict)
        id = UUID(d.pop("id"))




        kind = EvaluationDetailResponseDtoKind(d.pop("kind"))




        name = d.pop("name")

        description = d.pop("description")

        status = EvaluationDetailResponseDtoStatus(d.pop("status"))




        n_attempts_per_problem = d.pop("nAttemptsPerProblem")

        tags = cast(list[str], d.pop("tags"))


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


        total_solvers = d.pop("totalSolvers")

        total_problems = d.pop("totalProblems")

        created_at = datetime.datetime.fromisoformat(d.pop("createdAt"))




        updated_at = datetime.datetime.fromisoformat(d.pop("updatedAt"))




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


        metadata = EvaluationDetailResponseDtoMetadata.from_dict(d.pop("metadata"))




        solvers = []
        _solvers = d.pop("solvers")
        for solvers_item_data in (_solvers):
            solvers_item = EvaluationDetailResponseDtoSolversItem.from_dict(solvers_item_data)



            solvers.append(solvers_item)


        problems = []
        _problems = d.pop("problems")
        for problems_item_data in (_problems):
            problems_item = EvaluationDetailResponseDtoProblemsItem.from_dict(problems_item_data)



            problems.append(problems_item)


        evaluation_detail_response_dto = cls(
            id=id,
            kind=kind,
            name=name,
            description=description,
            status=status,
            n_attempts_per_problem=n_attempts_per_problem,
            tags=tags,
            grader_run_config_version_id=grader_run_config_version_id,
            total_solvers=total_solvers,
            total_problems=total_problems,
            created_at=created_at,
            updated_at=updated_at,
            started_at=started_at,
            completed_at=completed_at,
            metadata=metadata,
            solvers=solvers,
            problems=problems,
        )

        return evaluation_detail_response_dto

