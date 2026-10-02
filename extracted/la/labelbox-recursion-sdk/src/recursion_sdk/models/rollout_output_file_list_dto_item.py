from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar, BinaryIO, TextIO, TYPE_CHECKING, Generator

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset







T = TypeVar("T", bound="RolloutOutputFileListDtoItem")



@_attrs_define
class RolloutOutputFileListDtoItem:
    """ One output file produced by a rollout's agent-service run, with a ready-to-use signed download URL. Signed URLs are
    short-lived and expire after a brief window.

        Example:
            {'path': 'output/trace.json', 'download_url': 'https://storage.googleapis.com/recursion-example-
                outputs/runs/abc123/output/trace.json?X-Goog-Algorithm=GOOG4-RSA-SHA256&X-Goog-Expires=3600&X-Goog-
                Signature=a1b2c3'}

        Attributes:
            path (str): Workspace-relative path of the output file (e.g. "output/trace.json").
            download_url (str): Signed download URL for the output file contents.
     """

    path: str
    download_url: str





    def to_dict(self) -> dict[str, Any]:
        path = self.path

        download_url = self.download_url


        field_dict: dict[str, Any] = {}

        field_dict.update({
            "path": path,
            "download_url": download_url,
        })

        return field_dict



    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        path = d.pop("path")

        download_url = d.pop("download_url")

        rollout_output_file_list_dto_item = cls(
            path=path,
            download_url=download_url,
        )

        return rollout_output_file_list_dto_item

