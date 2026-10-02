from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar, BinaryIO, TextIO, TYPE_CHECKING, Generator

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

from ..types import UNSET, Unset
from typing import cast






T = TypeVar("T", bound="SynthesizerRunPageDtoItemsItemDiffPayloadItemType2CurrentItem")



@_attrs_define
class SynthesizerRunPageDtoItemsItemDiffPayloadItemType2CurrentItem:
    """ Single file entry inside a synthesizer diff payload, used for file-target buckets like problem files or grader
    support.

        Attributes:
            filename (str): Relative filename of the synthesized file.
            contents (None | str): File contents — UTF-8 text for non-binary entries, base64-encoded bytes for binary
                entries. Null only on legacy rows that predate binary-apply support.
            is_binary (bool): True when the file bytes are not safely UTF-8 decodable.
            mount_path (None | str | Unset): Mount path inside the grader container; only set for grader-support files.
     """

    filename: str
    contents: None | str
    is_binary: bool
    mount_path: None | str | Unset = UNSET





    def to_dict(self) -> dict[str, Any]:
        filename = self.filename

        contents: None | str
        contents = self.contents

        is_binary = self.is_binary

        mount_path: None | str | Unset
        if isinstance(self.mount_path, Unset):
            mount_path = UNSET
        else:
            mount_path = self.mount_path


        field_dict: dict[str, Any] = {}

        field_dict.update({
            "filename": filename,
            "contents": contents,
            "isBinary": is_binary,
        })
        if mount_path is not UNSET:
            field_dict["mountPath"] = mount_path

        return field_dict



    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        filename = d.pop("filename")

        def _parse_contents(data: object) -> None | str:
            if data is None:
                return data
            return cast(None | str, data)

        contents = _parse_contents(d.pop("contents"))


        is_binary = d.pop("isBinary")

        def _parse_mount_path(data: object) -> None | str | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(None | str | Unset, data)

        mount_path = _parse_mount_path(d.pop("mountPath", UNSET))


        synthesizer_run_page_dto_items_item_diff_payload_item_type_2_current_item = cls(
            filename=filename,
            contents=contents,
            is_binary=is_binary,
            mount_path=mount_path,
        )

        return synthesizer_run_page_dto_items_item_diff_payload_item_type_2_current_item

