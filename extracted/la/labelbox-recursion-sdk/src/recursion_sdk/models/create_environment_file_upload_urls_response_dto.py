from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar, BinaryIO, TextIO, TYPE_CHECKING, Generator

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

from typing import cast

if TYPE_CHECKING:
  from ..models.create_environment_file_upload_urls_response_dto_files_item import CreateEnvironmentFileUploadUrlsResponseDtoFilesItem





T = TypeVar("T", bound="CreateEnvironmentFileUploadUrlsResponseDto")



@_attrs_define
class CreateEnvironmentFileUploadUrlsResponseDto:
    """ Response containing signed upload URLs minted for environment files.

        Example:
            {'files': [{'uploadUrl': 'https://storage.googleapis.com/recursion-example-environment-
                files/environments/784e2386-e297-4f9d-a886-838422383b65/instructions/labeling-instructions.md?X-Goog-
                Algorithm=GOOG4-RSA-SHA256&X-Goog-Expires=900&X-Goog-Signature=1b7e0a92f3c4&X-Goog-SignedHeaders=host',
                'objectPath': 'environments/784e2386-e297-4f9d-a886-838422383b65/instructions/labeling-instructions.md',
                'fileName': 'labeling-instructions.md'}, {'uploadUrl': 'https://storage.googleapis.com/recursion-example-
                environment-files/environments/784e2386-e297-4f9d-a886-838422383b65/instructions/rubric-examples.pdf?X-Goog-
                Algorithm=GOOG4-RSA-SHA256&X-Goog-Expires=900&X-Goog-Signature=8d2c5f0a91be&X-Goog-SignedHeaders=host',
                'objectPath': 'environments/784e2386-e297-4f9d-a886-838422383b65/instructions/rubric-examples.pdf', 'fileName':
                'rubric-examples.pdf'}]}

        Attributes:
            files (list[CreateEnvironmentFileUploadUrlsResponseDtoFilesItem]): Per-file signed upload URLs in the same order
                as the request.
     """

    files: list[CreateEnvironmentFileUploadUrlsResponseDtoFilesItem]





    def to_dict(self) -> dict[str, Any]:
        from ..models.create_environment_file_upload_urls_response_dto_files_item import CreateEnvironmentFileUploadUrlsResponseDtoFilesItem # noqa: PLC0415
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
        from ..models.create_environment_file_upload_urls_response_dto_files_item import CreateEnvironmentFileUploadUrlsResponseDtoFilesItem # noqa: PLC0415
        d = dict(src_dict)
        files = []
        _files = d.pop("files")
        for files_item_data in (_files):
            files_item = CreateEnvironmentFileUploadUrlsResponseDtoFilesItem.from_dict(files_item_data)



            files.append(files_item)


        create_environment_file_upload_urls_response_dto = cls(
            files=files,
        )

        return create_environment_file_upload_urls_response_dto

