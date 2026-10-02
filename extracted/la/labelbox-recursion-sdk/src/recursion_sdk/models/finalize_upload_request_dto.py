from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar, BinaryIO, TextIO, TYPE_CHECKING, Generator

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

from typing import cast

if TYPE_CHECKING:
  from ..models.finalize_upload_request_dto_files_item import FinalizeUploadRequestDtoFilesItem





T = TypeVar("T", bound="FinalizeUploadRequestDto")



@_attrs_define
class FinalizeUploadRequestDto:
    """ Request body that finalizes a batch of direct-to-object-storage uploads into file records on the environment.

        Example:
            {'files': [{'objectPath': 'environments/784e2386-e297-4f9d-a886-838422383b65/uploads/e2a910d9-32c4-4ed6-8071-
                c7190a8c1951/dataset.jsonl'}]}

        Attributes:
            files (list[FinalizeUploadRequestDtoFilesItem]): Uploaded objects to finalize; must come from a previously-
                issued signed upload batch.
     """

    files: list[FinalizeUploadRequestDtoFilesItem]
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)





    def to_dict(self) -> dict[str, Any]:
        from ..models.finalize_upload_request_dto_files_item import FinalizeUploadRequestDtoFilesItem # noqa: PLC0415
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
        from ..models.finalize_upload_request_dto_files_item import FinalizeUploadRequestDtoFilesItem # noqa: PLC0415
        d = dict(src_dict)
        files = []
        _files = d.pop("files")
        for files_item_data in (_files):
            files_item = FinalizeUploadRequestDtoFilesItem.from_dict(files_item_data)



            files.append(files_item)


        finalize_upload_request_dto = cls(
            files=files,
        )


        finalize_upload_request_dto.additional_properties = d
        return finalize_upload_request_dto

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
