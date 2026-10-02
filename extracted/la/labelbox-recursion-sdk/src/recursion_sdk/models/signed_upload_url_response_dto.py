from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar, BinaryIO, TextIO, TYPE_CHECKING, Generator

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

from typing import cast

if TYPE_CHECKING:
  from ..models.signed_upload_url_response_dto_files_item import SignedUploadUrlResponseDtoFilesItem





T = TypeVar("T", bound="SignedUploadUrlResponseDto")



@_attrs_define
class SignedUploadUrlResponseDto:
    """ Response carrying signed upload URLs and target object paths for a batch upload request.

        Example:
            {'files': [{'uploadUrl': 'https://storage.googleapis.com/recursion-example-uploads/environments/784e2386-e297-
                4f9d-a886-838422383b65/uploads/e2a910d9-32c4-4ed6-8071-c7190a8c1951/dataset.jsonl?X-Goog-Algorithm=GOOG4-RSA-
                SHA256&X-Goog-Expires=900&X-Goog-Signature=4a1f9c2e7b5d3a8f0e6c1b9d2a4f7e3c8b5a0d6f1e9c2b4a7d3f8e5c0b6a1d9f',
                'objectPath':
                'environments/784e2386-e297-4f9d-a886-838422383b65/uploads/e2a910d9-32c4-4ed6-8071-c7190a8c1951/dataset.jsonl',
                'filename': 'dataset.jsonl'}]}

        Attributes:
            files (list[SignedUploadUrlResponseDtoFilesItem]): Signed upload slots, in the same order as the requested
                files.
     """

    files: list[SignedUploadUrlResponseDtoFilesItem]





    def to_dict(self) -> dict[str, Any]:
        from ..models.signed_upload_url_response_dto_files_item import SignedUploadUrlResponseDtoFilesItem # noqa: PLC0415
        files = []
        for files_item_data in self.files:
            files_item = files_item_data.to_dict()
            files.append(files_item)




        field_dict: dict[str, Any] = {}

        field_dict.update({
            "files": files,
        })

        return field_dict



    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.signed_upload_url_response_dto_files_item import SignedUploadUrlResponseDtoFilesItem # noqa: PLC0415
        d = dict(src_dict)
        files = []
        _files = d.pop("files")
        for files_item_data in (_files):
            files_item = SignedUploadUrlResponseDtoFilesItem.from_dict(files_item_data)



            files.append(files_item)


        signed_upload_url_response_dto = cls(
            files=files,
        )

        return signed_upload_url_response_dto

