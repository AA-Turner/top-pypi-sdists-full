from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar, BinaryIO, TextIO, TYPE_CHECKING, Generator

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

from typing import cast

if TYPE_CHECKING:
  from ..models.finalize_environment_file_uploads_response_dto_files_item import FinalizeEnvironmentFileUploadsResponseDtoFilesItem





T = TypeVar("T", bound="FinalizeEnvironmentFileUploadsResponseDto")



@_attrs_define
class FinalizeEnvironmentFileUploadsResponseDto:
    """ Response containing the persisted environment files after finalize.

        Example:
            {'files': [{'id': 'adcdd7cb-10ed-432f-863e-88a9bacaca60', 'environmentId':
                '784e2386-e297-4f9d-a886-838422383b65', 'type': 'instructions', 'fileName': 'labeling-instructions.md',
                'displayName': 'Labeling instructions', 'mimeType': 'text/markdown', 'sizeBytes': 12840, 'createdById':
                '49dea803-7390-49c4-abb1-5629718fc9cd', 'createdAt': '2026-01-15T09:30:00.000Z', 'downloadUrl':
                'https://storage.googleapis.com/recursion-example-environment-
                files/environments/784e2386-e297-4f9d-a886-838422383b65/instructions/labeling-instructions.md?X-Goog-
                Algorithm=GOOG4-RSA-SHA256&X-Goog-Expires=900&X-Goog-Signature=4a1f9c0b2e7d'}]}

        Attributes:
            files (list[FinalizeEnvironmentFileUploadsResponseDtoFilesItem]): Newly-persisted environment-file rows for the
                finalized uploads.
     """

    files: list[FinalizeEnvironmentFileUploadsResponseDtoFilesItem]





    def to_dict(self) -> dict[str, Any]:
        from ..models.finalize_environment_file_uploads_response_dto_files_item import FinalizeEnvironmentFileUploadsResponseDtoFilesItem # noqa: PLC0415
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
        from ..models.finalize_environment_file_uploads_response_dto_files_item import FinalizeEnvironmentFileUploadsResponseDtoFilesItem # noqa: PLC0415
        d = dict(src_dict)
        files = []
        _files = d.pop("files")
        for files_item_data in (_files):
            files_item = FinalizeEnvironmentFileUploadsResponseDtoFilesItem.from_dict(files_item_data)



            files.append(files_item)


        finalize_environment_file_uploads_response_dto = cls(
            files=files,
        )

        return finalize_environment_file_uploads_response_dto

