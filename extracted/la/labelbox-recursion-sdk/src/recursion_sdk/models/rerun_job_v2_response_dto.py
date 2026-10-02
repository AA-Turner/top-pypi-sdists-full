from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar, BinaryIO, TextIO, TYPE_CHECKING, Generator

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

from uuid import UUID






T = TypeVar("T", bound="RerunJobV2ResponseDto")



@_attrs_define
class RerunJobV2ResponseDto:
    """ Response from re-executing a terminal jobs_v2 row as a fresh run.

        Example:
            {'jobV2Id': '22222222-2222-4222-8222-222222222222'}

        Attributes:
            job_v2_id (UUID): Id of the new root job created by the rerun.
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




        rerun_job_v2_response_dto = cls(
            job_v2_id=job_v2_id,
        )

        return rerun_job_v2_response_dto

