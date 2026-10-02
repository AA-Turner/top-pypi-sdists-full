from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar, BinaryIO, TextIO, TYPE_CHECKING, Generator

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

from ..models.finalize_environment_file_uploads_request_dto_type import FinalizeEnvironmentFileUploadsRequestDtoType
from typing import cast

if TYPE_CHECKING:
  from ..models.finalize_environment_file_uploads_request_dto_files_item import FinalizeEnvironmentFileUploadsRequestDtoFilesItem





T = TypeVar("T", bound="FinalizeEnvironmentFileUploadsRequestDto")



@_attrs_define
class FinalizeEnvironmentFileUploadsRequestDto:
    """ Request body for finalizing uploads after the client has PUT the bytes.

        Example:
            {'type': 'instructions', 'files': [{'objectPath':
                'environments/784e2386-e297-4f9d-a886-838422383b65/instructions/labeling-instructions.md', 'fileName':
                'labeling-instructions.md', 'displayName': 'Labeling instructions'}, {'objectPath':
                'environments/784e2386-e297-4f9d-a886-838422383b65/instructions/rubric-examples.pdf', 'fileName': 'rubric-
                examples.pdf', 'displayName': 'Rubric examples'}]}

        Attributes:
            type_ (FinalizeEnvironmentFileUploadsRequestDtoType): Category the finalized files will be classified under.
            files (list[FinalizeEnvironmentFileUploadsRequestDtoFilesItem]): Files to finalize after a successful upload (at
                least one).
     """

    type_: FinalizeEnvironmentFileUploadsRequestDtoType
    files: list[FinalizeEnvironmentFileUploadsRequestDtoFilesItem]
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)





    def to_dict(self) -> dict[str, Any]:
        from ..models.finalize_environment_file_uploads_request_dto_files_item import FinalizeEnvironmentFileUploadsRequestDtoFilesItem # noqa: PLC0415
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
        from ..models.finalize_environment_file_uploads_request_dto_files_item import FinalizeEnvironmentFileUploadsRequestDtoFilesItem # noqa: PLC0415
        d = dict(src_dict)
        type_ = FinalizeEnvironmentFileUploadsRequestDtoType(d.pop("type"))




        files = []
        _files = d.pop("files")
        for files_item_data in (_files):
            files_item = FinalizeEnvironmentFileUploadsRequestDtoFilesItem.from_dict(files_item_data)



            files.append(files_item)


        finalize_environment_file_uploads_request_dto = cls(
            type_=type_,
            files=files,
        )


        finalize_environment_file_uploads_request_dto.additional_properties = d
        return finalize_environment_file_uploads_request_dto

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
