from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar, BinaryIO, TextIO, TYPE_CHECKING, Generator

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset







T = TypeVar("T", bound="CreateEnvironmentFileUploadUrlsRequestDtoFilesItem")



@_attrs_define
class CreateEnvironmentFileUploadUrlsRequestDtoFilesItem:
    """ Per-file metadata for which the server should mint a signed upload URL.

        Attributes:
            file_name (str): Original file name the upload URL will be associated with.
            mime_type (str): Client-reported MIME type used only for the pre-upload policy check; re-verified server-side at
                finalize time.
            size_bytes (int): Client-reported byte size used only for the pre-upload policy check; re-verified server-side
                at finalize time. Example: 1048576.
     """

    file_name: str
    mime_type: str
    size_bytes: int
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)





    def to_dict(self) -> dict[str, Any]:
        file_name = self.file_name

        mime_type = self.mime_type

        size_bytes = self.size_bytes


        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({
            "fileName": file_name,
            "mimeType": mime_type,
            "sizeBytes": size_bytes,
        })

        return field_dict



    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        file_name = d.pop("fileName")

        mime_type = d.pop("mimeType")

        size_bytes = d.pop("sizeBytes")

        create_environment_file_upload_urls_request_dto_files_item = cls(
            file_name=file_name,
            mime_type=mime_type,
            size_bytes=size_bytes,
        )


        create_environment_file_upload_urls_request_dto_files_item.additional_properties = d
        return create_environment_file_upload_urls_request_dto_files_item

    @property
    def additional_keys(self) -> list[str]:
        return list(self.additional_properties.keys())

    def __getitem__(self, key: str) -> Any:
        return self.additional_properties[key]

    def __setitem__(self, key: str, value: Any) -> None:
        self.additional_properties[key] = value

    def __delitem__(self, key: str) -> None:
        del self.additional_properties[key]

    def __contains__(self, key: str) -> bool:
        return key in self.additional_properties
