from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar, BinaryIO, TextIO, TYPE_CHECKING, Generator

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

from typing import cast
from uuid import UUID
import datetime






T = TypeVar("T", bound="OrganizationFileMetadataListDtoItem")



@_attrs_define
class OrganizationFileMetadataListDtoItem:
    """ Org-scoped file metadata (name, size, createdAt) without a signed download URL — for list/config UIs that only need
    display fields.

        Attributes:
            id (UUID): Stable file identifier (UUID). Files are problem-scoped uploads.
            filename (str): Original filename of the upload as provided by the user.
            size_bytes (int | None): Size of the file in bytes; null when the size has not yet been recorded. Example:
                1048576.
            created_at (datetime.datetime): Timestamp when the file was uploaded (ISO-8601, UTC).
     """

    id: UUID
    filename: str
    size_bytes: int | None
    created_at: datetime.datetime





    def to_dict(self) -> dict[str, Any]:
        id = str(self.id)

        filename = self.filename

        size_bytes: int | None
        size_bytes = self.size_bytes

        created_at = self.created_at.isoformat()


        field_dict: dict[str, Any] = {}

        field_dict.update({
            "id": id,
            "filename": filename,
            "sizeBytes": size_bytes,
            "createdAt": created_at,
        })

        return field_dict



    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        id = UUID(d.pop("id"))




        filename = d.pop("filename")

        def _parse_size_bytes(data: object) -> int | None:
            if data is None:
                return data
            return cast(int | None, data)

        size_bytes = _parse_size_bytes(d.pop("sizeBytes"))


        created_at = datetime.datetime.fromisoformat(d.pop("createdAt"))




        organization_file_metadata_list_dto_item = cls(
            id=id,
            filename=filename,
            size_bytes=size_bytes,
            created_at=created_at,
        )

        return organization_file_metadata_list_dto_item

