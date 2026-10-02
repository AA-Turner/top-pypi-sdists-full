from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar, BinaryIO, TextIO, TYPE_CHECKING, Generator

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

from ..models.synthesizer_run_page_dto_items_item_diff_payload_item_type_2_kind import SynthesizerRunPageDtoItemsItemDiffPayloadItemType2Kind
from ..models.synthesizer_run_page_dto_items_item_diff_payload_item_type_2_target import SynthesizerRunPageDtoItemsItemDiffPayloadItemType2Target
from typing import cast

if TYPE_CHECKING:
  from ..models.synthesizer_run_page_dto_items_item_diff_payload_item_type_2_current_item import SynthesizerRunPageDtoItemsItemDiffPayloadItemType2CurrentItem
  from ..models.synthesizer_run_page_dto_items_item_diff_payload_item_type_2_proposed_item import SynthesizerRunPageDtoItemsItemDiffPayloadItemType2ProposedItem





T = TypeVar("T", bound="SynthesizerRunPageDtoItemsItemDiffPayloadItemType2")



@_attrs_define
class SynthesizerRunPageDtoItemsItemDiffPayloadItemType2:
    """ Diff entry for a whole file-bucket target (problem files, supporting files, grader support).

        Attributes:
            target (SynthesizerRunPageDtoItemsItemDiffPayloadItemType2Target): File bucket this diff entry applies to.
            kind (SynthesizerRunPageDtoItemsItemDiffPayloadItemType2Kind): Diff-entry kind marker for file-bucket diffs.
            current (list[SynthesizerRunPageDtoItemsItemDiffPayloadItemType2CurrentItem]): Current file list in this bucket
                on the problem version.
            proposed (list[SynthesizerRunPageDtoItemsItemDiffPayloadItemType2ProposedItem]): Proposed file list in this
                bucket produced by the synthesizer.
            can_write (bool): Whether the caller is permitted to apply this file-bucket diff.
     """

    target: SynthesizerRunPageDtoItemsItemDiffPayloadItemType2Target
    kind: SynthesizerRunPageDtoItemsItemDiffPayloadItemType2Kind
    current: list[SynthesizerRunPageDtoItemsItemDiffPayloadItemType2CurrentItem]
    proposed: list[SynthesizerRunPageDtoItemsItemDiffPayloadItemType2ProposedItem]
    can_write: bool





    def to_dict(self) -> dict[str, Any]:
        from ..models.synthesizer_run_page_dto_items_item_diff_payload_item_type_2_current_item import SynthesizerRunPageDtoItemsItemDiffPayloadItemType2CurrentItem # noqa: PLC0415
        from ..models.synthesizer_run_page_dto_items_item_diff_payload_item_type_2_proposed_item import SynthesizerRunPageDtoItemsItemDiffPayloadItemType2ProposedItem # noqa: PLC0415
        target = self.target.value

        kind = self.kind.value

        current = []
        for current_item_data in self.current:
            current_item = current_item_data.to_dict()
            current.append(current_item)



        proposed = []
        for proposed_item_data in self.proposed:
            proposed_item = proposed_item_data.to_dict()
            proposed.append(proposed_item)



        can_write = self.can_write


        field_dict: dict[str, Any] = {}

        field_dict.update({
            "target": target,
            "kind": kind,
            "current": current,
            "proposed": proposed,
            "canWrite": can_write,
        })

        return field_dict



    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.synthesizer_run_page_dto_items_item_diff_payload_item_type_2_current_item import SynthesizerRunPageDtoItemsItemDiffPayloadItemType2CurrentItem # noqa: PLC0415
        from ..models.synthesizer_run_page_dto_items_item_diff_payload_item_type_2_proposed_item import SynthesizerRunPageDtoItemsItemDiffPayloadItemType2ProposedItem # noqa: PLC0415
        d = dict(src_dict)
        target = SynthesizerRunPageDtoItemsItemDiffPayloadItemType2Target(d.pop("target"))




        kind = SynthesizerRunPageDtoItemsItemDiffPayloadItemType2Kind(d.pop("kind"))




        current = []
        _current = d.pop("current")
        for current_item_data in (_current):
            current_item = SynthesizerRunPageDtoItemsItemDiffPayloadItemType2CurrentItem.from_dict(current_item_data)



            current.append(current_item)


        proposed = []
        _proposed = d.pop("proposed")
        for proposed_item_data in (_proposed):
            proposed_item = SynthesizerRunPageDtoItemsItemDiffPayloadItemType2ProposedItem.from_dict(proposed_item_data)



            proposed.append(proposed_item)


        can_write = d.pop("canWrite")

        synthesizer_run_page_dto_items_item_diff_payload_item_type_2 = cls(
            target=target,
            kind=kind,
            current=current,
            proposed=proposed,
            can_write=can_write,
        )

        return synthesizer_run_page_dto_items_item_diff_payload_item_type_2

