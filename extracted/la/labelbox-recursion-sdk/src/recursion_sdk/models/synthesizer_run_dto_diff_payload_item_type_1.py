from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar, BinaryIO, TextIO, TYPE_CHECKING, Generator

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

from ..models.synthesizer_run_dto_diff_payload_item_type_1_kind import SynthesizerRunDtoDiffPayloadItemType1Kind
from ..models.synthesizer_run_dto_diff_payload_item_type_1_target import SynthesizerRunDtoDiffPayloadItemType1Target






T = TypeVar("T", bound="SynthesizerRunDtoDiffPayloadItemType1")



@_attrs_define
class SynthesizerRunDtoDiffPayloadItemType1:
    """ Row-diff entry for any non-form-answers row target.

        Attributes:
            target (SynthesizerRunDtoDiffPayloadItemType1Target): Row target this diff entry applies to, excluding form-
                answers.
            kind (SynthesizerRunDtoDiffPayloadItemType1Kind): Diff-entry kind marker for row-shaped (non-file) diffs.
            current (Any): Current field value on the problem version.
            proposed (Any): Proposed field value produced by the synthesizer.
            can_write (bool): Whether the caller is permitted to apply this diff entry given environment permissions.
     """

    target: SynthesizerRunDtoDiffPayloadItemType1Target
    kind: SynthesizerRunDtoDiffPayloadItemType1Kind
    current: Any
    proposed: Any
    can_write: bool





    def to_dict(self) -> dict[str, Any]:
        target = self.target.value

        kind = self.kind.value

        current = self.current

        proposed = self.proposed

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
        d = dict(src_dict)
        target = SynthesizerRunDtoDiffPayloadItemType1Target(d.pop("target"))




        kind = SynthesizerRunDtoDiffPayloadItemType1Kind(d.pop("kind"))




        current = d.pop("current")

        proposed = d.pop("proposed")

        can_write = d.pop("canWrite")

        synthesizer_run_dto_diff_payload_item_type_1 = cls(
            target=target,
            kind=kind,
            current=current,
            proposed=proposed,
            can_write=can_write,
        )

        return synthesizer_run_dto_diff_payload_item_type_1

