from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar, BinaryIO, TextIO, TYPE_CHECKING, Generator

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

from typing import cast

if TYPE_CHECKING:
  from ..models.transcript_reformat_run_dto_properties_result_any_of_0_reformatted_turns_item_blocks_item import TranscriptReformatRunDtoPropertiesResultAnyOf0ReformattedTurnsItemBlocksItem





T = TypeVar("T", bound="TranscriptReformatRunDtoPropertiesResultAnyOf0ReformattedTurnsItem")



@_attrs_define
class TranscriptReformatRunDtoPropertiesResultAnyOf0ReformattedTurnsItem:
    """ One reformatted turn: a labeled group of thinking / assistant blocks.

        Attributes:
            heading (None | str): Short label summarizing this turn, or null when no concise label fits.
            blocks (list[TranscriptReformatRunDtoPropertiesResultAnyOf0ReformattedTurnsItemBlocksItem]): Ordered thinking /
                assistant blocks that make up this turn.
     """

    heading: None | str
    blocks: list[TranscriptReformatRunDtoPropertiesResultAnyOf0ReformattedTurnsItemBlocksItem]





    def to_dict(self) -> dict[str, Any]:
        from ..models.transcript_reformat_run_dto_properties_result_any_of_0_reformatted_turns_item_blocks_item import TranscriptReformatRunDtoPropertiesResultAnyOf0ReformattedTurnsItemBlocksItem # noqa: PLC0415
        heading: None | str
        heading = self.heading

        blocks = []
        for blocks_item_data in self.blocks:
            blocks_item = blocks_item_data.to_dict()
            blocks.append(blocks_item)




        field_dict: dict[str, Any] = {}

        field_dict.update({
            "heading": heading,
            "blocks": blocks,
        })

        return field_dict



    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.transcript_reformat_run_dto_properties_result_any_of_0_reformatted_turns_item_blocks_item import TranscriptReformatRunDtoPropertiesResultAnyOf0ReformattedTurnsItemBlocksItem # noqa: PLC0415
        d = dict(src_dict)
        def _parse_heading(data: object) -> None | str:
            if data is None:
                return data
            return cast(None | str, data)

        heading = _parse_heading(d.pop("heading"))


        blocks = []
        _blocks = d.pop("blocks")
        for blocks_item_data in (_blocks):
            blocks_item = TranscriptReformatRunDtoPropertiesResultAnyOf0ReformattedTurnsItemBlocksItem.from_dict(blocks_item_data)



            blocks.append(blocks_item)


        transcript_reformat_run_dto_properties_result_any_of_0_reformatted_turns_item = cls(
            heading=heading,
            blocks=blocks,
        )

        return transcript_reformat_run_dto_properties_result_any_of_0_reformatted_turns_item

