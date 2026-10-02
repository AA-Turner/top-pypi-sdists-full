from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar, BinaryIO, TextIO, TYPE_CHECKING, Generator

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

from typing import cast
from uuid import UUID






T = TypeVar("T", bound="BulkCreateProblemRunsResponseDto")



@_attrs_define
class BulkCreateProblemRunsResponseDto:
    """ Result of a bulk problem-runs submission via the v2 path.

        Example:
            {'jobV2Id': '7f6e5d4c-3b2a-4190-8d6e-9c0b1a2d3e4f', 'problemRunIds': ['f3c1a2b4-5d6e-4f70-8192-a3b4c5d6e7f8',
                '8e6d1c7f-3b4a-4d12-9a5e-2c0b1a3d4e5f', 'a1b2c3d4-e5f6-4a7b-8c9d-0e1f2a3b4c5d',
                'd4e5f6a7-b8c9-4d0e-9f1a-2b3c4d5e6f70', 'b1a2c3d4-5e6f-4a7b-8c9d-0e1f2a3b4c5d',
                'c1d2e3f4-5a6b-4c7d-8e9f-0a1b2c3d4e5f']}

        Attributes:
            job_v2_id (UUID): New jobs-v2 root job id, a problem-run-batch orchestration root. Use the jobs-v2 surface to
                poll status, cancel, or fetch the orchestration tree.
            problem_run_ids (list[UUID]): IDs of the problem-run shells inserted by this request — one per (problem version,
                attempt) pair. Read individual run status via the problem-run detail endpoint.
     """

    job_v2_id: UUID
    problem_run_ids: list[UUID]





    def to_dict(self) -> dict[str, Any]:
        job_v2_id = str(self.job_v2_id)

        problem_run_ids = []
        for problem_run_ids_item_data in self.problem_run_ids:
            problem_run_ids_item = str(problem_run_ids_item_data)
            problem_run_ids.append(problem_run_ids_item)




        field_dict: dict[str, Any] = {}

        field_dict.update({
            "jobV2Id": job_v2_id,
            "problemRunIds": problem_run_ids,
        })

        return field_dict



    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        job_v2_id = UUID(d.pop("jobV2Id"))




        problem_run_ids = []
        _problem_run_ids = d.pop("problemRunIds")
        for problem_run_ids_item_data in (_problem_run_ids):
            problem_run_ids_item = UUID(problem_run_ids_item_data)



            problem_run_ids.append(problem_run_ids_item)


        bulk_create_problem_runs_response_dto = cls(
            job_v2_id=job_v2_id,
            problem_run_ids=problem_run_ids,
        )

        return bulk_create_problem_runs_response_dto

