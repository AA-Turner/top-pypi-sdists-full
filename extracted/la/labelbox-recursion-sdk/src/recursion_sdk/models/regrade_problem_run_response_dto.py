from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar, BinaryIO, TextIO, TYPE_CHECKING, Generator

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

from uuid import UUID






T = TypeVar("T", bound="RegradeProblemRunResponseDto")



@_attrs_define
class RegradeProblemRunResponseDto:
    """ Result of enqueueing a re-grade of an existing problem run.

        Example:
            {'jobV2Id': '7f6e5d4c-3b2a-4190-8d6e-9c0b1a2d3e4f'}

        Attributes:
            job_v2_id (UUID): New jobs-v2 root job id, a regrade orchestration root. Use the jobs-v2 surface to poll status
                or cancel; the problem run is re-graded in place.
     """

    job_v2_id: UUID





    def to_dict(self) -> dict[str, Any]:
        job_v2_id = str(self.job_v2_id)


        field_dict: dict[str, Any] = {}

        field_dict.update({
            "jobV2Id": job_v2_id,
        })

        return field_dict



    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        job_v2_id = UUID(d.pop("jobV2Id"))




        regrade_problem_run_response_dto = cls(
            job_v2_id=job_v2_id,
        )

        return regrade_problem_run_response_dto

