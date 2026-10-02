from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar, BinaryIO, TextIO, TYPE_CHECKING, Generator

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

from ..models.create_environment_file_upload_urls_request_dto_type import CreateEnvironmentFileUploadUrlsRequestDtoType
from typing import cast

if TYPE_CHECKING:
  from ..models.create_environment_file_upload_urls_request_dto_files_item import CreateEnvironmentFileUploadUrlsRequestDtoFilesItem





T = TypeVar("T", bound="CreateEnvironmentFileUploadUrlsRequestDto")



@_attrs_define
class CreateEnvironmentFileUploadUrlsRequestDto:
    """ Request body for minting per-file signed upload URLs for environment files.

        Example:
            {'type': 'instructions', 'files': [{'fileName': 'labeling-instructions.md', 'mimeType': 'text/markdown',
                'sizeBytes': 12840}, {'fileName': 'rubric-examples.pdf', 'mimeType': 'application/pdf', 'sizeBytes': 524288}]}

        Attributes:
            type_ (CreateEnvironmentFileUploadUrlsRequestDtoType): Category the uploaded files will be classified under.
            files (list[CreateEnvironmentFileUploadUrlsRequestDtoFilesItem]): Files for which signed upload URLs should be
                minted (at least one).
     """

    type_: CreateEnvironmentFileUploadUrlsRequestDtoType
    files: list[CreateEnvironmentFileUploadUrlsRequestDtoFilesItem]
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)





    def to_dict(self) -> dict[str, Any]:
        from ..models.create_environment_file_upload_urls_request_dto_files_item import CreateEnvironmentFileUploadUrlsRequestDtoFilesItem # noqa: PLC0415
        type_ = self.type_.value

        files = []
        for files_item_data in self.files:
            files_item = files_item_data.to_dict()
            files.append(files_item)




        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({
            "type": type_,
            "files": files,
        })

        return field_dict



    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.create_environment_file_upload_urls_request_dto_files_item import CreateEnvironmentFileUploadUrlsRequestDtoFilesItem # noqa: PLC0415
        d = dict(src_dict)
        type_ = CreateEnvironmentFileUploadUrlsRequestDtoType(d.pop("type"))




        files = []
        _files = d.pop("files")
        for files_item_data in (_files):
            files_item = CreateEnvironmentFileUploadUrlsRequestDtoFilesItem.from_dict(files_item_data)



            files.append(files_item)


        create_environment_file_upload_urls_request_dto = cls(
            type_=type_,
            files=files,
        )


        create_environment_file_upload_urls_request_dto.additional_properties = d
        return create_environment_file_upload_urls_request_dto

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
