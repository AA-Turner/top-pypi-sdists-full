from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar, BinaryIO, TextIO, TYPE_CHECKING, Generator

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset







T = TypeVar("T", bound="CreateEnvironmentFileUploadUrlsResponseDtoFilesItem")



@_attrs_define
class CreateEnvironmentFileUploadUrlsResponseDtoFilesItem:
    """ Signed upload coordinates for one file.

        Attributes:
            upload_url (str): Signed URL the client must PUT the file bytes to.
            object_path (str): Server-issued object path identifying the uploaded blob in storage.
            file_name (str): Original file name the URL was minted for.
     """

    upload_url: str
    object_path: str
    file_name: str





    def to_dict(self) -> dict[str, Any]:
        upload_url = self.upload_url

        object_path = self.object_path

        file_name = self.file_name


        field_dict: dict[str, Any] = {}

        field_dict.update({
            "uploadUrl": upload_url,
            "objectPath": object_path,
            "fileName": file_name,
        })

        return field_dict



    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        upload_url = d.pop("uploadUrl")

        object_path = d.pop("objectPath")

        file_name = d.pop("fileName")

        create_environment_file_upload_urls_response_dto_files_item = cls(
            upload_url=upload_url,
            object_path=object_path,
            file_name=file_name,
        )

        return create_environment_file_upload_urls_response_dto_files_item

