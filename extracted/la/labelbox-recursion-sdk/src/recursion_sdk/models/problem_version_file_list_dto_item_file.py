from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar, BinaryIO, TextIO, TYPE_CHECKING, Generator

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

from typing import cast
from uuid import UUID
import datetime






T = TypeVar("T", bound="ProblemVersionFileListDtoItemFile")



@_attrs_define
class ProblemVersionFileListDtoItemFile:
    """ Materialized file record, included so consumers do not need a second fetch.

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


        problem_version_file_list_dto_item_file = cls(
            id=id,
            url=url,
            filename=filename,
            size_bytes=size_bytes,
            created_at=created_at,
            created_by_id=created_by_id,
        )

        return problem_version_file_list_dto_item_file

