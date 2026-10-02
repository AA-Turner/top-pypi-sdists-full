from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar, BinaryIO, TextIO, TYPE_CHECKING, Generator

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

from ..models.submit_probe_response_dto_status import SubmitProbeResponseDtoStatus
from typing import cast
from uuid import UUID
import datetime






T = TypeVar("T", bound="SubmitProbeResponseDto")



@_attrs_define
class SubmitProbeResponseDto:
    """ Response body after a new probe-run is submitted.

        Example:
            {'probeRunId': '1be7d569-e271-4926-af2c-569798de74d7', 'status': 'pending', 'submittedAt':
                '2026-01-16T14:05:00.000Z'}

        Attributes:
            probe_run_id (UUID): New probe-run row the client should poll for terminal status.
            status (SubmitProbeResponseDtoStatus): Current status of the newly submitted probe-run — typically pending or
                running.
            submitted_at (datetime.datetime): Timestamp when the probe run was submitted (ISO-8601, UTC).
     """

    probe_run_id: UUID
    status: SubmitProbeResponseDtoStatus
    submitted_at: datetime.datetime





    def to_dict(self) -> dict[str, Any]:
        probe_run_id = str(self.probe_run_id)

        status = self.status.value

        submitted_at = self.submitted_at.isoformat()


        field_dict: dict[str, Any] = {}

        field_dict.update({
            "probeRunId": probe_run_id,
            "status": status,
            "submittedAt": submitted_at,
        })

        return field_dict



    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        probe_run_id = UUID(d.pop("probeRunId"))




        status = SubmitProbeResponseDtoStatus(d.pop("status"))




        submitted_at = datetime.datetime.fromisoformat(d.pop("submittedAt"))




        submit_probe_response_dto = cls(
            probe_run_id=probe_run_id,
            status=status,
            submitted_at=submitted_at,
        )

        return submit_probe_response_dto

