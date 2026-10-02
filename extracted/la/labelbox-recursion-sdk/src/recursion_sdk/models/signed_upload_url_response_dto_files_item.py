from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar, BinaryIO, TextIO, TYPE_CHECKING, Generator

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset







T = TypeVar("T", bound="SignedUploadUrlResponseDtoFilesItem")



@_attrs_define
class SignedUploadUrlResponseDtoFilesItem:
    """ One signed upload slot for a single file.

        Attributes:
            upload_url (str): Signed PUT URL the client should upload bytes to.
            object_path (str): Object-storage path that the upload writes to; pass back to finalize.
            filename (str): Filename echoed back so clients can correlate slots.
     """

    upload_url: str
    object_path: str
    filename: str





    def to_dict(self) -> dict[str, Any]:
        upload_url = self.upload_url

        object_path = self.object_path

        filename = self.filename


        field_dict: dict[str, Any] = {}

        field_dict.update({
            "uploadUrl": upload_url,
            "objectPath": object_path,
            "filename": filename,
        })

        return field_dict



    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        upload_url = d.pop("uploadUrl")

        object_path = d.pop("objectPath")

        filename = d.pop("filename")

        signed_upload_url_response_dto_files_item = cls(
            upload_url=upload_url,
            object_path=object_path,
            filename=filename,
        )

        return signed_upload_url_response_dto_files_item

