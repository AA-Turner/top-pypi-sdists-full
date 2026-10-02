from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar, BinaryIO, TextIO, TYPE_CHECKING, Generator

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

from ..types import UNSET, Unset
from typing import cast
from uuid import UUID

if TYPE_CHECKING:
  from ..models.bulk_create_problem_runs_request_dto_grading import BulkCreateProblemRunsRequestDtoGrading





T = TypeVar("T", bound="BulkCreateProblemRunsRequestDto")



@_attrs_define
class BulkCreateProblemRunsRequestDto:
    """ Bulk-create `problem_runs` shells and spawn a v2 `problem_run_batch` root job that drives them.

        Example:
            {'environmentId': 'c2a8a3a4-5e5e-4cf8-b3a1-0d6b9a5e2f10', 'name': 'Baseline sweep', 'problemVersionIds':
                ['0c3ac467-57e1-4074-b57d-b6a7be392f71', '4f1e9b22-2a72-4cb1-9d63-1f8a3b9c0d2e'], 'nAttemptsPerProblem': 3,
                'runConfigVersionId': '39088cb6-ca62-4544-a074-fc66e10807ad'}

        Attributes:
            environment_id (UUID): Stable environment identifier (UUID).
            problem_version_ids (list[UUID]): Problem versions to run. Each must be locked and within the caller scope.
                Duplicates are rejected — use nAttemptsPerProblem to request multiple runs of one version. Capped at 1000 to
                match Send-to-Taiga.
            name (str | Unset): Display name for the batch, shown in the jobs-v2 list and detail views. Defaults to a
                generated label when omitted.
            n_attempts_per_problem (int | Unset): Number of solver attempts to spawn per problem version. One problem-run
                shell is inserted per (problem version, attempt) pair. Defaults to 1. Default: 1.
            run_config_version_id (UUID | Unset): Stable run-config-version identifier (UUID). Points at one specific
                version of a run config.
            run_config_version_ids (list[UUID] | Unset): Solver run-config versions to fan out over — one solver branch per
                entry. Mutually exclusive with runConfigVersionId. Omit all solver inputs to resolve via the environment default
                binding chain.
            grading (BulkCreateProblemRunsRequestDtoGrading | Unset): Per-request grader override for a bulk problem-run
                submission. The grading config itself is read from the locked problem version server-side.
            grader_run_config_version_id (UUID | Unset): Optional locked grader run-config version for rubric/agentic
                grading. When omitted, the problem-version/environment/scope-default grader binding chain is resolved and
                validated before dispatch. Labeler-supplied explicit picks must also be on the environment grader menu. Model-
                less programmatic grader pins are allowed when grading is programmatic-only.
     """

    environment_id: UUID
    problem_version_ids: list[UUID]
    name: str | Unset = UNSET
    n_attempts_per_problem: int | Unset = 1
    run_config_version_id: UUID | Unset = UNSET
    run_config_version_ids: list[UUID] | Unset = UNSET
    grading: BulkCreateProblemRunsRequestDtoGrading | Unset = UNSET
    grader_run_config_version_id: UUID | Unset = UNSET





    def to_dict(self) -> dict[str, Any]:
        from ..models.bulk_create_problem_runs_request_dto_grading import BulkCreateProblemRunsRequestDtoGrading # noqa: PLC0415
        environment_id = str(self.environment_id)

        problem_version_ids = []
        for problem_version_ids_item_data in self.problem_version_ids:
            problem_version_ids_item = str(problem_version_ids_item_data)
            problem_version_ids.append(problem_version_ids_item)



        name = self.name

        n_attempts_per_problem = self.n_attempts_per_problem

        run_config_version_id: str | Unset = UNSET
        if not isinstance(self.run_config_version_id, Unset):
            run_config_version_id = str(self.run_config_version_id)

        run_config_version_ids: list[str] | Unset = UNSET
        if not isinstance(self.run_config_version_ids, Unset):
            run_config_version_ids = []
            for run_config_version_ids_item_data in self.run_config_version_ids:
                run_config_version_ids_item = str(run_config_version_ids_item_data)
                run_config_version_ids.append(run_config_version_ids_item)



        grading: dict[str, Any] | Unset = UNSET
        if not isinstance(self.grading, Unset):
            grading = self.grading.to_dict()

        grader_run_config_version_id: str | Unset = UNSET
        if not isinstance(self.grader_run_config_version_id, Unset):
            grader_run_config_version_id = str(self.grader_run_config_version_id)


        field_dict: dict[str, Any] = {}

        field_dict.update({
            "environmentId": environment_id,
            "problemVersionIds": problem_version_ids,
        })
        if name is not UNSET:
            field_dict["name"] = name
        if n_attempts_per_problem is not UNSET:
            field_dict["nAttemptsPerProblem"] = n_attempts_per_problem
        if run_config_version_id is not UNSET:
            field_dict["runConfigVersionId"] = run_config_version_id
        if run_config_version_ids is not UNSET:
            field_dict["runConfigVersionIds"] = run_config_version_ids
        if grading is not UNSET:
            field_dict["grading"] = grading
        if grader_run_config_version_id is not UNSET:
            field_dict["graderRunConfigVersionId"] = grader_run_config_version_id

        return field_dict



    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.bulk_create_problem_runs_request_dto_grading import BulkCreateProblemRunsRequestDtoGrading # noqa: PLC0415
        d = dict(src_dict)
        environment_id = UUID(d.pop("environmentId"))




        problem_version_ids = []
        _problem_version_ids = d.pop("problemVersionIds")
        for problem_version_ids_item_data in (_problem_version_ids):
            problem_version_ids_item = UUID(problem_version_ids_item_data)



            problem_version_ids.append(problem_version_ids_item)


        name = d.pop("name", UNSET)

        n_attempts_per_problem = d.pop("nAttemptsPerProblem", UNSET)

        _run_config_version_id = d.pop("runConfigVersionId", UNSET)
        run_config_version_id: UUID | Unset
        if isinstance(_run_config_version_id,  Unset):
            run_config_version_id = UNSET
        else:
            run_config_version_id = UUID(_run_config_version_id)




        _run_config_version_ids = d.pop("runConfigVersionIds", UNSET)
        run_config_version_ids: list[UUID] | Unset = UNSET
        if _run_config_version_ids is not UNSET:
            run_config_version_ids = []
            for run_config_version_ids_item_data in _run_config_version_ids:
                run_config_version_ids_item = UUID(run_config_version_ids_item_data)



                run_config_version_ids.append(run_config_version_ids_item)


        _grading = d.pop("grading", UNSET)
        grading: BulkCreateProblemRunsRequestDtoGrading | Unset
        if isinstance(_grading,  Unset):
            grading = UNSET
        else:
            grading = BulkCreateProblemRunsRequestDtoGrading.from_dict(_grading)




        _grader_run_config_version_id = d.pop("graderRunConfigVersionId", UNSET)
        grader_run_config_version_id: UUID | Unset
        if isinstance(_grader_run_config_version_id,  Unset):
            grader_run_config_version_id = UNSET
        else:
            grader_run_config_version_id = UUID(_grader_run_config_version_id)




        bulk_create_problem_runs_request_dto = cls(
            environment_id=environment_id,
            problem_version_ids=problem_version_ids,
            name=name,
            n_attempts_per_problem=n_attempts_per_problem,
            run_config_version_id=run_config_version_id,
            run_config_version_ids=run_config_version_ids,
            grading=grading,
            grader_run_config_version_id=grader_run_config_version_id,
        )

        return bulk_create_problem_runs_request_dto

