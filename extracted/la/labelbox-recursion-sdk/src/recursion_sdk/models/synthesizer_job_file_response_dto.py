from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar, BinaryIO, TextIO, TYPE_CHECKING, Generator

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

from typing import cast
from uuid import UUID






T = TypeVar("T", bound="SynthesizerJobFileResponseDto")



@_attrs_define
class SynthesizerJobFileResponseDto:
    """ File attached to a user-defined synthesizer job and mounted into the agent container at run time.

        Example:
            {'id': 'a7c9f2e1-4b3d-4a6e-9f1c-2d8e5b7a0c34', 'fileId': 'e2a910d9-32c4-4ed6-8071-c7190a8c1951', 'filename':
                'style-guide.md', 'mountPath': '/workspace/files/style-guide.md', 'sizeBytes': 4096, 'createdAt':
                '2026-01-15T09:35:00.000Z'}

        Attributes:
            id (str): Stable identifier of the synthesizer-job file attachment.
            file_id (UUID): Stable file identifier (UUID). Files are problem-scoped uploads.
            filename (str): Original filename of the attached file.
            mount_path (str): Absolute path inside the synthesizer container where this file is mounted.
            size_bytes (float | None): Size of the file in bytes; null when unknown.
            created_at (str): Timestamp when the file was attached to the synthesizer job (ISO-8601, UTC).
     """

    id: str
    file_id: UUID
    filename: str
    mount_path: str
    size_bytes: float | None
    created_at: str





    def to_dict(self) -> dict[str, Any]:
        id = self.id

        file_id = str(self.file_id)

        filename = self.filename

        mount_path = self.mount_path

        size_bytes: float | None
        size_bytes = self.size_bytes

        created_at = self.created_at


        field_dict: dict[str, Any] = {}

        field_dict.update({
            "id": id,
            "fileId": file_id,
            "filename": filename,
            "mountPath": mount_path,
            "sizeBytes": size_bytes,
            "createdAt": created_at,
        })

        return field_dict



    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        id = d.pop("id")

        file_id = UUID(d.pop("fileId"))




        filename = d.pop("filename")

        mount_path = d.pop("mountPath")

        def _parse_size_bytes(data: object) -> float | None:
            if data is None:
                return data
            return cast(float | None, data)

        size_bytes = _parse_size_bytes(d.pop("sizeBytes"))


        created_at = d.pop("createdAt")

        synthesizer_job_file_response_dto = cls(
            id=id,
            file_id=file_id,
            filename=filename,
            mount_path=mount_path,
            size_bytes=size_bytes,
            created_at=created_at,
        )

        return synthesizer_job_file_response_dto

