from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar, BinaryIO, TextIO, TYPE_CHECKING, Generator

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

from uuid import UUID






T = TypeVar("T", bound="RegradeFailedGradersResponseDtoRegradesItem")



@_attrs_define
class RegradeFailedGradersResponseDtoRegradesItem:
    """ A single problem run for which a re-grade was enqueued.

        Attributes:
            problem_run_id (UUID): The problem run whose grader is being re-run.
            regrade_job_v2_id (UUID): The regrade orchestration root minted for this run. Poll it (or the run) for the new
                grade.
     """

    problem_run_id: UUID
    regrade_job_v2_id: UUID





    def to_dict(self) -> dict[str, Any]:
        problem_run_id = str(self.problem_run_id)

        regrade_job_v2_id = str(self.regrade_job_v2_id)


        field_dict: dict[str, Any] = {}

        field_dict.update({
            "problemRunId": problem_run_id,
            "regradeJobV2Id": regrade_job_v2_id,
        })

        return field_dict



    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        problem_run_id = UUID(d.pop("problemRunId"))




        regrade_job_v2_id = UUID(d.pop("regradeJobV2Id"))




        regrade_failed_graders_response_dto_regrades_item = cls(
            problem_run_id=problem_run_id,
            regrade_job_v2_id=regrade_job_v2_id,
        )

        return regrade_failed_graders_response_dto_regrades_item

