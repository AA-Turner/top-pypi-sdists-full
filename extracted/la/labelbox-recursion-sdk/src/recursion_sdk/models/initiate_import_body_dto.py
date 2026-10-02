from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar, BinaryIO, TextIO, TYPE_CHECKING, Generator

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

from ..models.initiate_import_body_dto_format import InitiateImportBodyDtoFormat
from ..types import UNSET, Unset






T = TypeVar("T", bound="InitiateImportBodyDto")



@_attrs_define
class InitiateImportBodyDto:
    """ Request body for initiating an import: declares filename and size and receives a signed upload URL the client uses
    to deliver bytes directly to object storage.

        Example:
            {'filename': 'problems-export.tar.gz', 'fileSizeBytes': 4194304, 'format': 'default'}

        Attributes:
            filename (str): Filename of the archive the caller intends to upload.
            file_size_bytes (int): Total size of the upload in bytes; the per-environment cap is enforced separately at the
                controller level. Example: 1048576.
            format_ (InitiateImportBodyDtoFormat | Unset): User-selected import format; when omitted, the format is detected
                from the file extension.
            assign_external_ids (bool | Unset): When true (also the default when omitted) imported problems keep the
                external IDs from the archive; when false they are imported without external IDs so they can be claimed later.
     """

    filename: str
    file_size_bytes: int
    format_: InitiateImportBodyDtoFormat | Unset = UNSET
    assign_external_ids: bool | Unset = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)





    def to_dict(self) -> dict[str, Any]:
        filename = self.filename

        file_size_bytes = self.file_size_bytes

        format_: str | Unset = UNSET
        if not isinstance(self.format_, Unset):
            format_ = self.format_.value


        assign_external_ids = self.assign_external_ids


        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({
            "filename": filename,
            "fileSizeBytes": file_size_bytes,
        })
        if format_ is not UNSET:
            field_dict["format"] = format_
        if assign_external_ids is not UNSET:
            field_dict["assignExternalIds"] = assign_external_ids

        return field_dict



    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        filename = d.pop("filename")

        file_size_bytes = d.pop("fileSizeBytes")

        _format_ = d.pop("format", UNSET)
        format_: InitiateImportBodyDtoFormat | Unset
        if isinstance(_format_,  Unset):
            format_ = UNSET
        else:
            format_ = InitiateImportBodyDtoFormat(_format_)




        assign_external_ids = d.pop("assignExternalIds", UNSET)

        initiate_import_body_dto = cls(
            filename=filename,
            file_size_bytes=file_size_bytes,
            format_=format_,
            assign_external_ids=assign_external_ids,
        )


        initiate_import_body_dto.additional_properties = d
        return initiate_import_body_dto

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
