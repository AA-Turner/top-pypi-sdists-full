from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar, BinaryIO, TextIO, TYPE_CHECKING, Generator

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

from ..models.evaluation_page_response_dto_items_item_kind import EvaluationPageResponseDtoItemsItemKind
from ..models.evaluation_page_response_dto_items_item_status import EvaluationPageResponseDtoItemsItemStatus
from typing import cast
from uuid import UUID
import datetime






T = TypeVar("T", bound="EvaluationPageResponseDtoItemsItem")



@_attrs_define
class EvaluationPageResponseDtoItemsItem:
    """ Summary view of an evaluation for list endpoints, including the creator name but excluding solver and problem detail
    arrays.

        Attributes:
            id (UUID): Stable evaluation identifier (UUID). An evaluation is a multi-problem comparison run.
            kind (EvaluationPageResponseDtoItemsItemKind): Which evaluation shape this is. Defaults to solve-and-grade for
                pre-kind records. Default: EvaluationPageResponseDtoItemsItemKind.SOLVE_AND_GRADE.
            name (str): Human-readable display name of the evaluation.
            description (str): Free-form description of the evaluation. Empty string when not provided.
            status (EvaluationPageResponseDtoItemsItemStatus): Lifecycle status of the evaluation.
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
            created_by_name (str): Display name of the user who created the evaluation.
     """

    id: UUID
    name: str
    description: str
    status: EvaluationPageResponseDtoItemsItemStatus
    n_attempts_per_problem: int
    tags: list[str]
    grader_run_config_version_id: None | UUID
    total_solvers: int
    total_problems: int
    created_at: datetime.datetime
    updated_at: datetime.datetime
    started_at: datetime.datetime | None
    completed_at: datetime.datetime | None
    created_by_name: str
    kind: EvaluationPageResponseDtoItemsItemKind = EvaluationPageResponseDtoItemsItemKind.SOLVE_AND_GRADE





    def to_dict(self) -> dict[str, Any]:
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

        created_by_name = self.created_by_name


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
            "createdByName": created_by_name,
        })

        return field_dict



    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        id = UUID(d.pop("id"))




        kind = EvaluationPageResponseDtoItemsItemKind(d.pop("kind"))




        name = d.pop("name")

        description = d.pop("description")

        status = EvaluationPageResponseDtoItemsItemStatus(d.pop("status"))




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


        created_by_name = d.pop("createdByName")

        evaluation_page_response_dto_items_item = cls(
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
            created_by_name=created_by_name,
        )

        return evaluation_page_response_dto_items_item

