from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar, BinaryIO, TextIO, TYPE_CHECKING, Generator

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

from ..models.transcript_reformat_run_dto_properties_result_any_of_0_reformatted_status import TranscriptReformatRunDtoPropertiesResultAnyOf0ReformattedStatus
from typing import cast

if TYPE_CHECKING:
  from ..models.transcript_reformat_run_dto_properties_result_any_of_0_reformatted_turns_item import TranscriptReformatRunDtoPropertiesResultAnyOf0ReformattedTurnsItem





T = TypeVar("T", bound="TranscriptReformatRunDtoPropertiesResultAnyOf0Reformatted")



@_attrs_define
class TranscriptReformatRunDtoPropertiesResultAnyOf0Reformatted:
    """ The transcript was re-segmented into readable turns.

        Attributes:
            status (TranscriptReformatRunDtoPropertiesResultAnyOf0ReformattedStatus): Discriminant marking that the
                transcript was re-segmented into turns.
            turns (list[TranscriptReformatRunDtoPropertiesResultAnyOf0ReformattedTurnsItem]): Re-segmented turns
                reconstructed from the original transcript.
            truncated (bool): True when the source transcript was too long to send in full, so its middle was dropped before
                re-segmentation — the reformatted turns are therefore incomplete. Set server-side, not by the model.
     """

    status: TranscriptReformatRunDtoPropertiesResultAnyOf0ReformattedStatus
    turns: list[TranscriptReformatRunDtoPropertiesResultAnyOf0ReformattedTurnsItem]
    truncated: bool





    def to_dict(self) -> dict[str, Any]:
        from ..models.transcript_reformat_run_dto_properties_result_any_of_0_reformatted_turns_item import TranscriptReformatRunDtoPropertiesResultAnyOf0ReformattedTurnsItem # noqa: PLC0415
        status = self.status.value

        turns = []
        for turns_item_data in self.turns:
            turns_item = turns_item_data.to_dict()
            turns.append(turns_item)



        truncated = self.truncated


        field_dict: dict[str, Any] = {}

        field_dict.update({
            "status": status,
            "turns": turns,
            "truncated": truncated,
        })

        return field_dict



    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.transcript_reformat_run_dto_properties_result_any_of_0_reformatted_turns_item import TranscriptReformatRunDtoPropertiesResultAnyOf0ReformattedTurnsItem # noqa: PLC0415
        d = dict(src_dict)
        status = TranscriptReformatRunDtoPropertiesResultAnyOf0ReformattedStatus(d.pop("status"))




        turns = []
        _turns = d.pop("turns")
        for turns_item_data in (_turns):
            turns_item = TranscriptReformatRunDtoPropertiesResultAnyOf0ReformattedTurnsItem.from_dict(turns_item_data)



            turns.append(turns_item)


        truncated = d.pop("truncated")

        transcript_reformat_run_dto_properties_result_any_of_0_reformatted = cls(
            status=status,
            turns=turns,
            truncated=truncated,
        )

        return transcript_reformat_run_dto_properties_result_any_of_0_reformatted

