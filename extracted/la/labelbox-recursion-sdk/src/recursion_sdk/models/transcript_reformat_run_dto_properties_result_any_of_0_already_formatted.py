from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar, BinaryIO, TextIO, TYPE_CHECKING, Generator

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

from ..models.transcript_reformat_run_dto_properties_result_any_of_0_already_formatted_status import TranscriptReformatRunDtoPropertiesResultAnyOf0AlreadyFormattedStatus






T = TypeVar("T", bound="TranscriptReformatRunDtoPropertiesResultAnyOf0AlreadyFormatted")



@_attrs_define
class TranscriptReformatRunDtoPropertiesResultAnyOf0AlreadyFormatted:
    """ The transcript was already well formatted; no re-segmentation was produced.

        Attributes:
            status (TranscriptReformatRunDtoPropertiesResultAnyOf0AlreadyFormattedStatus): Discriminant marking that the
                transcript needed no re-segmentation.
            message (str): Human-readable explanation that the transcript is already well formatted.
            truncated (bool): True when the source transcript was too long to send in full, so the already-formatted verdict
                is based only on its start and end rather than the whole transcript. Set server-side, not by the model. Defaults
                to false so a rolling rollback to a backend revision predating this field never fails validation for the common
                already-formatted case. Default: False.
     """

    status: TranscriptReformatRunDtoPropertiesResultAnyOf0AlreadyFormattedStatus
    message: str
    truncated: bool = False





    def to_dict(self) -> dict[str, Any]:
        status = self.status.value

        message = self.message

        truncated = self.truncated


        field_dict: dict[str, Any] = {}

        field_dict.update({
            "status": status,
            "message": message,
            "truncated": truncated,
        })

        return field_dict



    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        status = TranscriptReformatRunDtoPropertiesResultAnyOf0AlreadyFormattedStatus(d.pop("status"))




        message = d.pop("message")

        truncated = d.pop("truncated")

        transcript_reformat_run_dto_properties_result_any_of_0_already_formatted = cls(
            status=status,
            message=message,
            truncated=truncated,
        )

        return transcript_reformat_run_dto_properties_result_any_of_0_already_formatted

