from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar, BinaryIO, TextIO, TYPE_CHECKING, Generator

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

from ..types import UNSET, Unset
from typing import cast






T = TypeVar("T", bound="FinalizeEnvironmentFileUploadsRequestDtoFilesItem")



@_attrs_define
class FinalizeEnvironmentFileUploadsRequestDtoFilesItem:
    """ Finalize metadata for one previously-signed upload.

        Attributes:
            object_path (str): Server-issued object path returned by the upload-URL step.
            file_name (str): Original file name to record alongside the upload.
            display_name (None | str | Unset): Optional user-facing display name; null clears any prior value.
     """

    object_path: str
    file_name: str
    display_name: None | str | Unset = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)





    def to_dict(self) -> dict[str, Any]:
        object_path = self.object_path

        file_name = self.file_name

        display_name: None | str | Unset
        if isinstance(self.display_name, Unset):
            display_name = UNSET
        else:
            display_name = self.display_name


        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({
            "objectPath": object_path,
            "fileName": file_name,
        })
        if display_name is not UNSET:
            field_dict["displayName"] = display_name

        return field_dict



    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        object_path = d.pop("objectPath")

        file_name = d.pop("fileName")

        def _parse_display_name(data: object) -> None | str | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(None | str | Unset, data)

        display_name = _parse_display_name(d.pop("displayName", UNSET))


        finalize_environment_file_uploads_request_dto_files_item = cls(
            object_path=object_path,
            file_name=file_name,
            display_name=display_name,
        )


        finalize_environment_file_uploads_request_dto_files_item.additional_properties = d
        return finalize_environment_file_uploads_request_dto_files_item

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
