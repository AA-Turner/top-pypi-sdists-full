from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar, BinaryIO, TextIO, TYPE_CHECKING, Generator

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

from ..models.transcript_reformat_run_dto_properties_result_any_of_0_reformatted_turns_item_blocks_item_type import TranscriptReformatRunDtoPropertiesResultAnyOf0ReformattedTurnsItemBlocksItemType






T = TypeVar("T", bound="TranscriptReformatRunDtoPropertiesResultAnyOf0ReformattedTurnsItemBlocksItem")



@_attrs_define
class TranscriptReformatRunDtoPropertiesResultAnyOf0ReformattedTurnsItemBlocksItem:
    """ One re-segmented block within a reformatted turn.

        Attributes:
            type_ (TranscriptReformatRunDtoPropertiesResultAnyOf0ReformattedTurnsItemBlocksItemType): Kind of re-segmented
                block: internal reasoning (thinking) or the model’s visible response (assistant).
            content (str): Markdown content of this block, extracted from the original transcript.
     """

    type_: TranscriptReformatRunDtoPropertiesResultAnyOf0ReformattedTurnsItemBlocksItemType
    content: str





    def to_dict(self) -> dict[str, Any]:
        type_ = self.type_.value

        content = self.content


        field_dict: dict[str, Any] = {}

        field_dict.update({
            "type": type_,
            "content": content,
        })

        return field_dict



    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        type_ = TranscriptReformatRunDtoPropertiesResultAnyOf0ReformattedTurnsItemBlocksItemType(d.pop("type"))




        content = d.pop("content")

        transcript_reformat_run_dto_properties_result_any_of_0_reformatted_turns_item_blocks_item = cls(
            type_=type_,
            content=content,
        )

        return transcript_reformat_run_dto_properties_result_any_of_0_reformatted_turns_item_blocks_item

