from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar, BinaryIO, TextIO, TYPE_CHECKING, Generator

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

from ..models.transcript_reformat_run_ref_dto_status import TranscriptReformatRunRefDtoStatus
from uuid import UUID






T = TypeVar("T", bound="TranscriptReformatRunRefDto")



@_attrs_define
class TranscriptReformatRunRefDto:
    """ Handle to an enqueued transcript-reformat run, returned by the async enqueue endpoint.

        Attributes:
            reformat_run_id (UUID): Identifier of the enqueued (or already in-flight) reformat run to poll.
            status (TranscriptReformatRunRefDtoStatus): Status of the reformat run at enqueue time.
     """

    reformat_run_id: UUID
    status: TranscriptReformatRunRefDtoStatus





    def to_dict(self) -> dict[str, Any]:
        reformat_run_id = str(self.reformat_run_id)

        status = self.status.value


        field_dict: dict[str, Any] = {}

        field_dict.update({
            "reformatRunId": reformat_run_id,
            "status": status,
        })

        return field_dict



    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        reformat_run_id = UUID(d.pop("reformatRunId"))




        status = TranscriptReformatRunRefDtoStatus(d.pop("status"))




        transcript_reformat_run_ref_dto = cls(
            reformat_run_id=reformat_run_id,
            status=status,
        )

        return transcript_reformat_run_ref_dto

