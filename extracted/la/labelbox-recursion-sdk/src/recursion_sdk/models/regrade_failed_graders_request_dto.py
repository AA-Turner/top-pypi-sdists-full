from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar, BinaryIO, TextIO, TYPE_CHECKING, Generator

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

from ..types import UNSET, Unset
from uuid import UUID






T = TypeVar("T", bound="RegradeFailedGradersRequestDto")



@_attrs_define
class RegradeFailedGradersRequestDto:
    """ Re-grade every failed-grader run in a single run (batch). Runs whose solver failed are excluded.

        Example:
            {'jobV2Id': '7f6e5d4c-3b2a-4190-8d6e-9c0b1a2d3e4f', 'graderRunConfigVersionId':
                '39088cb6-ca62-4544-a074-fc66e10807ad'}

        Attributes:
            job_v2_id (UUID | Unset): The run to re-grade, identified by the batch root job id returned by bulk-create. When
                omitted, the caller's most recent problem-run batch in scope is targeted.
            grader_run_config_version_id (UUID | Unset): Optional locked grader run-config version applied to every re-
                graded run in the batch. Must be on the batch environment's grader menu. When omitted, each run's existing
                grader binding is re-resolved live at dispatch.
     """

    job_v2_id: UUID | Unset = UNSET
    grader_run_config_version_id: UUID | Unset = UNSET





    def to_dict(self) -> dict[str, Any]:
        job_v2_id: str | Unset = UNSET
        if not isinstance(self.job_v2_id, Unset):
            job_v2_id = str(self.job_v2_id)

        grader_run_config_version_id: str | Unset = UNSET
        if not isinstance(self.grader_run_config_version_id, Unset):
            grader_run_config_version_id = str(self.grader_run_config_version_id)


        field_dict: dict[str, Any] = {}

        field_dict.update({
        })
        if job_v2_id is not UNSET:
            field_dict["jobV2Id"] = job_v2_id
        if grader_run_config_version_id is not UNSET:
            field_dict["graderRunConfigVersionId"] = grader_run_config_version_id

        return field_dict



    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        _job_v2_id = d.pop("jobV2Id", UNSET)
        job_v2_id: UUID | Unset
        if isinstance(_job_v2_id,  Unset):
            job_v2_id = UNSET
        else:
            job_v2_id = UUID(_job_v2_id)




        _grader_run_config_version_id = d.pop("graderRunConfigVersionId", UNSET)
        grader_run_config_version_id: UUID | Unset
        if isinstance(_grader_run_config_version_id,  Unset):
            grader_run_config_version_id = UNSET
        else:
            grader_run_config_version_id = UUID(_grader_run_config_version_id)




        regrade_failed_graders_request_dto = cls(
            job_v2_id=job_v2_id,
            grader_run_config_version_id=grader_run_config_version_id,
        )

        return regrade_failed_graders_request_dto

