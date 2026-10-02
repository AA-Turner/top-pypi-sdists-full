from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar, BinaryIO, TextIO, TYPE_CHECKING, Generator

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset







T = TypeVar("T", bound="SignedUploadUrlRequestDtoFilesItem")



@_attrs_define
class SignedUploadUrlRequestDtoFilesItem:
    """ One file the client wants a signed upload URL for.

        Attributes:
            filename (str): Filename to record on the resulting upload.
            content_type (str): MIME type the client will send with the PUT.
     """

    filename: str
    content_type: str
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)





    def to_dict(self) -> dict[str, Any]:
        filename = self.filename

        content_type = self.content_type


        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({
            "filename": filename,
            "contentType": content_type,
        })

        return field_dict



    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        filename = d.pop("filename")

        content_type = d.pop("contentType")

        signed_upload_url_request_dto_files_item = cls(
            filename=filename,
            content_type=content_type,
        )


        signed_upload_url_request_dto_files_item.additional_properties = d
        return signed_upload_url_request_dto_files_item

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
