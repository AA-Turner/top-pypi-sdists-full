from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar, BinaryIO, TextIO, TYPE_CHECKING, Generator

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

from ..types import File, FileTypes
from ..types import UNSET, Unset
from io import BytesIO






T = TypeVar("T", bound="ManagedAgentsFormDataSessionFileUploadRequest")



@_attrs_define
class ManagedAgentsFormDataSessionFileUploadRequest:
    """ Multipart body carrying one image in the file part.

        Example:
            {'file': 'example'}

        Attributes:
            file (File | Unset): The image bytes. PNG, JPEG and WebP are accepted; the media type is sniffed from the bytes.
     """

    file: File | Unset = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)





    def to_dict(self) -> dict[str, Any]:
        file: FileTypes | Unset = UNSET
        if not isinstance(self.file, Unset):
            file = self.file.to_tuple()



        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({
        })
        if file is not UNSET:
            field_dict["file"] = file

        return field_dict



    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        _file = d.pop("file", UNSET)
        file: File | Unset
        if isinstance(_file,  Unset):
            file = UNSET
        else:
            file = File(
             payload = BytesIO(_file)
        )




        managed_agents_form_data_session_file_upload_request = cls(
            file=file,
        )


        managed_agents_form_data_session_file_upload_request.additional_properties = d
        return managed_agents_form_data_session_file_upload_request

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
