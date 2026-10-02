from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar, BinaryIO, TextIO, TYPE_CHECKING, Generator

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

from ..models.synthesizer_run_dto_diff_payload_item_type_2_kind import SynthesizerRunDtoDiffPayloadItemType2Kind
from ..models.synthesizer_run_dto_diff_payload_item_type_2_target import SynthesizerRunDtoDiffPayloadItemType2Target
from typing import cast

if TYPE_CHECKING:
  from ..models.synthesizer_run_dto_diff_payload_item_type_2_current_item import SynthesizerRunDtoDiffPayloadItemType2CurrentItem
  from ..models.synthesizer_run_dto_diff_payload_item_type_2_proposed_item import SynthesizerRunDtoDiffPayloadItemType2ProposedItem





T = TypeVar("T", bound="SynthesizerRunDtoDiffPayloadItemType2")



@_attrs_define
class SynthesizerRunDtoDiffPayloadItemType2:
    """ Diff entry for a whole file-bucket target (problem files, supporting files, grader support).

        Attributes:
            target (SynthesizerRunDtoDiffPayloadItemType2Target): File bucket this diff entry applies to.
            kind (SynthesizerRunDtoDiffPayloadItemType2Kind): Diff-entry kind marker for file-bucket diffs.
            current (list[SynthesizerRunDtoDiffPayloadItemType2CurrentItem]): Current file list in this bucket on the
                problem version.
            proposed (list[SynthesizerRunDtoDiffPayloadItemType2ProposedItem]): Proposed file list in this bucket produced
                by the synthesizer.
            can_write (bool): Whether the caller is permitted to apply this file-bucket diff.
     """

    target: SynthesizerRunDtoDiffPayloadItemType2Target
    kind: SynthesizerRunDtoDiffPayloadItemType2Kind
    current: list[SynthesizerRunDtoDiffPayloadItemType2CurrentItem]
    proposed: list[SynthesizerRunDtoDiffPayloadItemType2ProposedItem]
    can_write: bool





    def to_dict(self) -> dict[str, Any]:
        from ..models.synthesizer_run_dto_diff_payload_item_type_2_current_item import SynthesizerRunDtoDiffPayloadItemType2CurrentItem # noqa: PLC0415
        from ..models.synthesizer_run_dto_diff_payload_item_type_2_proposed_item import SynthesizerRunDtoDiffPayloadItemType2ProposedItem # noqa: PLC0415
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
        from ..models.synthesizer_run_dto_diff_payload_item_type_2_current_item import SynthesizerRunDtoDiffPayloadItemType2CurrentItem # noqa: PLC0415
        from ..models.synthesizer_run_dto_diff_payload_item_type_2_proposed_item import SynthesizerRunDtoDiffPayloadItemType2ProposedItem # noqa: PLC0415
        d = dict(src_dict)
        target = SynthesizerRunDtoDiffPayloadItemType2Target(d.pop("target"))




        kind = SynthesizerRunDtoDiffPayloadItemType2Kind(d.pop("kind"))




        current = []
        _current = d.pop("current")
        for current_item_data in (_current):
            current_item = SynthesizerRunDtoDiffPayloadItemType2CurrentItem.from_dict(current_item_data)



            current.append(current_item)


        proposed = []
        _proposed = d.pop("proposed")
        for proposed_item_data in (_proposed):
            proposed_item = SynthesizerRunDtoDiffPayloadItemType2ProposedItem.from_dict(proposed_item_data)



            proposed.append(proposed_item)


        can_write = d.pop("canWrite")

        synthesizer_run_dto_diff_payload_item_type_2 = cls(
            target=target,
            kind=kind,
            current=current,
            proposed=proposed,
            can_write=can_write,
        )

        return synthesizer_run_dto_diff_payload_item_type_2

