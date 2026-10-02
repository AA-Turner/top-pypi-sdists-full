from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar, BinaryIO, TextIO, TYPE_CHECKING, Generator

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

from ..models.list_environment_files_response_dto_files_item_type import ListEnvironmentFilesResponseDtoFilesItemType
from typing import cast
from uuid import UUID
import datetime






T = TypeVar("T", bound="ListEnvironmentFilesResponseDtoFilesItem")



@_attrs_define
class ListEnvironmentFilesResponseDtoFilesItem:
    """ A file uploaded into an environment, typically labeler-facing instructions.

        Attributes:
            id (UUID): Stable environment-file identifier (UUID). Files scoped to an environment (templates, shared assets).
            environment_id (UUID): Stable environment identifier (UUID).
            type_ (ListEnvironmentFilesResponseDtoFilesItemType): Category of this environment-scoped file.
            file_name (str): Original file name as uploaded by the client.
            display_name (None | str): Optional user-facing display name. Null falls back to the original file name.
            mime_type (str): MIME type detected server-side from the uploaded bytes.
            size_bytes (int): Size of the uploaded object in bytes. Example: 524288.
            created_by_id (None | UUID): User who uploaded the file. Null for system-uploaded files.
            created_at (datetime.datetime): Timestamp when the file was uploaded (ISO-8601, UTC).
            download_url (str): Short-lived signed URL for download or preview.
     """

    id: UUID
    environment_id: UUID
    type_: ListEnvironmentFilesResponseDtoFilesItemType
    file_name: str
    display_name: None | str
    mime_type: str
    size_bytes: int
    created_by_id: None | UUID
    created_at: datetime.datetime
    download_url: str





    def to_dict(self) -> dict[str, Any]:
        id = str(self.id)

        environment_id = str(self.environment_id)

        type_ = self.type_.value

        file_name = self.file_name

        display_name: None | str
        display_name = self.display_name

        mime_type = self.mime_type

        size_bytes = self.size_bytes

        created_by_id: None | str
        if isinstance(self.created_by_id, UUID):
            created_by_id = str(self.created_by_id)
        else:
            created_by_id = self.created_by_id

        created_at = self.created_at.isoformat()

        download_url = self.download_url


        field_dict: dict[str, Any] = {}

        field_dict.update({
            "id": id,
            "environmentId": environment_id,
            "type": type_,
            "fileName": file_name,
            "displayName": display_name,
            "mimeType": mime_type,
            "sizeBytes": size_bytes,
            "createdById": created_by_id,
            "createdAt": created_at,
            "downloadUrl": download_url,
        })

        return field_dict



    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        id = UUID(d.pop("id"))




        environment_id = UUID(d.pop("environmentId"))




        type_ = ListEnvironmentFilesResponseDtoFilesItemType(d.pop("type"))




        file_name = d.pop("fileName")

        def _parse_display_name(data: object) -> None | str:
            if data is None:
                return data
            return cast(None | str, data)

        display_name = _parse_display_name(d.pop("displayName"))


        mime_type = d.pop("mimeType")

        size_bytes = d.pop("sizeBytes")

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


        created_at = datetime.datetime.fromisoformat(d.pop("createdAt"))




        download_url = d.pop("downloadUrl")

        list_environment_files_response_dto_files_item = cls(
            id=id,
            environment_id=environment_id,
            type_=type_,
            file_name=file_name,
            display_name=display_name,
            mime_type=mime_type,
            size_bytes=size_bytes,
            created_by_id=created_by_id,
            created_at=created_at,
            download_url=download_url,
        )

        return list_environment_files_response_dto_files_item

