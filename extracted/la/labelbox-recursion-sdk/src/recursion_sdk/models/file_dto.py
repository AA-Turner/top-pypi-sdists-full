from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar, BinaryIO, TextIO, TYPE_CHECKING, Generator

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

from typing import cast
from uuid import UUID
import datetime






T = TypeVar("T", bound="FileDto")



@_attrs_define
class FileDto:
    """ An environment-scoped file upload that can be attached to problem versions or skill bundles.

        Example:
            {'id': 'e2a910d9-32c4-4ed6-8071-c7190a8c1951', 'url': 'https://storage.googleapis.com/recursion-example-uploads/
                environments/784e2386-e297-4f9d-a886-838422383b65/uploads/e2a910d9-32c4-4ed6-8071-c7190a8c1951/dataset.jsonl?X-
                Goog-Algorithm=GOOG4-RSA-SHA256&X-Goog-Expires=900&X-Goog-
                Signature=4a1f9c2e7b5d3a8f0e6c1b9d2a4f7e3c8b5a0d6f1e9c2b4a7d3f8e5c0b6a1d9f', 'filename': 'dataset.jsonl',
                'sizeBytes': 1048576, 'createdAt': '2026-01-15T09:30:00.000Z', 'createdById':
                '49dea803-7390-49c4-abb1-5629718fc9cd'}

        Attributes:
            id (UUID): Stable file identifier (UUID). Files are problem-scoped uploads.
            url (str): Signed download URL for the file contents.
            filename (str): Original filename of the upload as provided by the user.
            size_bytes (int | None): Size of the file in bytes; null when the size has not yet been recorded. Example:
                1048576.
            created_at (datetime.datetime): Timestamp when the file was uploaded (ISO-8601, UTC).
            created_by_id (None | UUID): User who uploaded the file; null for system-uploaded or pre-attribution files.
     """

    id: UUID
    url: str
    filename: str
    size_bytes: int | None
    created_at: datetime.datetime
    created_by_id: None | UUID





    def to_dict(self) -> dict[str, Any]:
        id = str(self.id)

        url = self.url

        filename = self.filename

        size_bytes: int | None
        size_bytes = self.size_bytes

        created_at = self.created_at.isoformat()

        created_by_id: None | str
        if isinstance(self.created_by_id, UUID):
            created_by_id = str(self.created_by_id)
        else:
            created_by_id = self.created_by_id


        field_dict: dict[str, Any] = {}

        field_dict.update({
            "id": id,
            "url": url,
            "filename": filename,
            "sizeBytes": size_bytes,
            "createdAt": created_at,
            "createdById": created_by_id,
        })

        return field_dict



    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        id = UUID(d.pop("id"))




        url = d.pop("url")

        filename = d.pop("filename")

        def _parse_size_bytes(data: object) -> int | None:
            if data is None:
                return data
            return cast(int | None, data)

        size_bytes = _parse_size_bytes(d.pop("sizeBytes"))


        created_at = datetime.datetime.fromisoformat(d.pop("createdAt"))




        def _parse_created_by_id(data: object) -> None | UUID:
            if data is None:
                return data
            try:
                if not isinstance(data, str):
                    raise TypeError()
                created_by_id_type_0 = UUID(data)



                return created_by_id_type_0
            except (TypeError, ValueError, AttributeError, KeyError):
                pass
            return cast(None | UUID, data)

        created_by_id = _parse_created_by_id(d.pop("createdById"))


        file_dto = cls(
            id=id,
            url=url,
            filename=filename,
            size_bytes=size_bytes,
            created_at=created_at,
            created_by_id=created_by_id,
        )

        return file_dto

