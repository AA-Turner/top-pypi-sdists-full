from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar, BinaryIO, TextIO, TYPE_CHECKING, Generator

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

from ..types import File, FileTypes
from ..types import UNSET, Unset
from io import BytesIO






T = TypeVar("T", bound="ManagedAgentsFormDataFileUploadRequest")



@_attrs_define
class ManagedAgentsFormDataFileUploadRequest:
    """ Multipart body for uploading a file. Send the bytes as the file part; the part's filename and Content-Type become
    the file's name and media type.

        Example:
            {'expires_in_seconds': 1, 'file': 'example', 'metadata': 'example'}

        Attributes:
            expires_in_seconds (int | Unset): How long the file stays attachable and its content served, from 3600 (an hour)
                to 7776000 (ninety days); its metadata stays readable, with expires_at in the past, for a grace after that. Omit
                for a file that does not expire. Set once: a file's expiry cannot be changed.
            file (File | Unset): The file's bytes. Its part filename is the name the file is stored and mounted under; its
                part Content-Type is recorded as the media type. Up to 64 MiB.
            metadata (str | Unset): Caller-owned key/value data as a JSON object, since a form part cannot carry structure.
                Rejected rather than dropped when it does not parse.
     """

    expires_in_seconds: int | Unset = UNSET
    file: File | Unset = UNSET
    metadata: str | Unset = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)





    def to_dict(self) -> dict[str, Any]:
        expires_in_seconds = self.expires_in_seconds

        file: FileTypes | Unset = UNSET
        if not isinstance(self.file, Unset):
            file = self.file.to_tuple()


        metadata = self.metadata


        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({
        })
        if expires_in_seconds is not UNSET:
            field_dict["expires_in_seconds"] = expires_in_seconds
        if file is not UNSET:
            field_dict["file"] = file
        if metadata is not UNSET:
            field_dict["metadata"] = metadata

        return field_dict



    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        expires_in_seconds = d.pop("expires_in_seconds", UNSET)

        _file = d.pop("file", UNSET)
        file: File | Unset
        if isinstance(_file,  Unset):
            file = UNSET
        else:
            file = File(
             payload = BytesIO(_file)
        )




        metadata = d.pop("metadata", UNSET)

        managed_agents_form_data_file_upload_request = cls(
            expires_in_seconds=expires_in_seconds,
            file=file,
            metadata=metadata,
        )


        managed_agents_form_data_file_upload_request.additional_properties = d
        return managed_agents_form_data_file_upload_request

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
