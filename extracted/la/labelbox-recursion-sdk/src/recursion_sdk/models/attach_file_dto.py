from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar, BinaryIO, TextIO, TYPE_CHECKING, Generator

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

from ..models.attach_file_dto_type import AttachFileDtoType
from uuid import UUID






T = TypeVar("T", bound="AttachFileDto")



@_attrs_define
class AttachFileDto:
    """ Request body for attaching a single environment file to a problem version with a role.

        Example:
            {'fileId': 'e2a910d9-32c4-4ed6-8071-c7190a8c1951', 'type': 'problem'}

        Attributes:
            file_id (UUID): Environment file to attach to the problem version.
            type_ (AttachFileDtoType): Role of the attached file: solver-visible input, reference material, or grader-only
                assets.
     """

    file_id: UUID
    type_: AttachFileDtoType
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)





    def to_dict(self) -> dict[str, Any]:
        file_id = str(self.file_id)

        type_ = self.type_.value


        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({
            "fileId": file_id,
            "type": type_,
        })

        return field_dict



    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        file_id = UUID(d.pop("fileId"))




        type_ = AttachFileDtoType(d.pop("type"))




        attach_file_dto = cls(
            file_id=file_id,
            type_=type_,
        )


        attach_file_dto.additional_properties = d
        return attach_file_dto

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
