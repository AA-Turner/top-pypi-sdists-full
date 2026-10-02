from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar, BinaryIO, TextIO, TYPE_CHECKING, Generator

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

from ..models.synthesizer_run_dto_diff_payload_item_type_0_kind import SynthesizerRunDtoDiffPayloadItemType0Kind
from ..models.synthesizer_run_dto_diff_payload_item_type_0_target import SynthesizerRunDtoDiffPayloadItemType0Target
from uuid import UUID






T = TypeVar("T", bound="SynthesizerRunDtoDiffPayloadItemType0")



@_attrs_define
class SynthesizerRunDtoDiffPayloadItemType0:
    """ Row-diff entry for the form-answers target; carries the snapshotted form version so apply can detect schema drift.

        Attributes:
            target (SynthesizerRunDtoDiffPayloadItemType0Target): Diff-entry target marker for the form-answers row.
            kind (SynthesizerRunDtoDiffPayloadItemType0Kind): Diff-entry kind marker for row-shaped (non-file) diffs.
            current (Any): Current form-answers value on the problem version.
            proposed (Any): Proposed form-answers value produced by the synthesizer.
            can_write (bool): Whether the caller is permitted to apply this diff entry against the active form version.
            form_version_id (UUID): Stable form-version identifier (UUID).
     """

    target: SynthesizerRunDtoDiffPayloadItemType0Target
    kind: SynthesizerRunDtoDiffPayloadItemType0Kind
    current: Any
    proposed: Any
    can_write: bool
    form_version_id: UUID





    def to_dict(self) -> dict[str, Any]:
        target = self.target.value

        kind = self.kind.value

        current = self.current

        proposed = self.proposed

        can_write = self.can_write

        form_version_id = str(self.form_version_id)


        field_dict: dict[str, Any] = {}

        field_dict.update({
            "target": target,
            "kind": kind,
            "current": current,
            "proposed": proposed,
            "canWrite": can_write,
            "formVersionId": form_version_id,
        })

        return field_dict



    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        target = SynthesizerRunDtoDiffPayloadItemType0Target(d.pop("target"))




        kind = SynthesizerRunDtoDiffPayloadItemType0Kind(d.pop("kind"))




        current = d.pop("current")

        proposed = d.pop("proposed")

        can_write = d.pop("canWrite")

        form_version_id = UUID(d.pop("formVersionId"))




        synthesizer_run_dto_diff_payload_item_type_0 = cls(
            target=target,
            kind=kind,
            current=current,
            proposed=proposed,
            can_write=can_write,
            form_version_id=form_version_id,
        )

        return synthesizer_run_dto_diff_payload_item_type_0

