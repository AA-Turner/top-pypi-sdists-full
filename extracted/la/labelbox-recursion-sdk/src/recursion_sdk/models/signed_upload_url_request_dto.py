from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar, BinaryIO, TextIO, TYPE_CHECKING, Generator

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

from typing import cast

if TYPE_CHECKING:
  from ..models.signed_upload_url_request_dto_files_item import SignedUploadUrlRequestDtoFilesItem





T = TypeVar("T", bound="SignedUploadUrlRequestDto")



@_attrs_define
class SignedUploadUrlRequestDto:
    """ Request body for minting one or more signed upload URLs that target object storage directly, bypassing the API
    server.

        Example:
            {'files': [{'filename': 'dataset.jsonl', 'contentType': 'application/jsonl'}]}

        Attributes:
            files (list[SignedUploadUrlRequestDtoFilesItem]): Files the client intends to upload in this batch.
     """

    files: list[SignedUploadUrlRequestDtoFilesItem]
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)





    def to_dict(self) -> dict[str, Any]:
        from ..models.signed_upload_url_request_dto_files_item import SignedUploadUrlRequestDtoFilesItem # noqa: PLC0415
        files = []
        for files_item_data in self.files:
            files_item = files_item_data.to_dict()
            files.append(files_item)




        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({
            "files": files,
        })

        return field_dict



    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.signed_upload_url_request_dto_files_item import SignedUploadUrlRequestDtoFilesItem # noqa: PLC0415
        d = dict(src_dict)
        files = []
        _files = d.pop("files")
        for files_item_data in (_files):
            files_item = SignedUploadUrlRequestDtoFilesItem.from_dict(files_item_data)



            files.append(files_item)


        signed_upload_url_request_dto = cls(
            files=files,
        )


        signed_upload_url_request_dto.additional_properties = d
        return signed_upload_url_request_dto

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
