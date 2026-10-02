from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar, BinaryIO, TextIO, TYPE_CHECKING, Generator

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset







T = TypeVar("T", bound="WorkspaceFileDownloadUrlResponseDto")



@_attrs_define
class WorkspaceFileDownloadUrlResponseDto:
    """ Signed download URL for one file in a run workspace, resolved on demand.

        Example:
            {'downloadUrl': 'https://storage.googleapis.com/agent-service-workspaces/runs/9a2c8b7d/output/reports/defect-
                report.json?X-Goog-Algorithm=GOOG4-RSA-SHA256&X-Goog-Expires=600&X-Goog-Signature=f6e5d4c3b2a1'}

        Attributes:
            download_url (str): Short-lived signed URL for downloading the file contents directly.
     """

    download_url: str





    def to_dict(self) -> dict[str, Any]:
        download_url = self.download_url


        field_dict: dict[str, Any] = {}

        field_dict.update({
            "downloadUrl": download_url,
        })

        return field_dict



    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        download_url = d.pop("downloadUrl")

        workspace_file_download_url_response_dto = cls(
            download_url=download_url,
        )

        return workspace_file_download_url_response_dto

