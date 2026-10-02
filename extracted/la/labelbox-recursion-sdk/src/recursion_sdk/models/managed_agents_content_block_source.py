from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar, BinaryIO, TextIO, TYPE_CHECKING, Generator

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

from ..models.managed_agents_content_block_source_type import ManagedAgentsContentBlockSourceType






T = TypeVar("T", bound="ManagedAgentsContentBlockSource")



@_attrs_define
class ManagedAgentsContentBlockSource:
    """ Where a user-sent image or document block takes its bytes from when the caller names a file instead of carrying
    them: a file from the organization's catalog, read and copied into the session when the message is accepted, so the
    block the transcript keeps names both the source and the copy.

        Example:
            {'file_id': '9f8b1c2d-3e4f-5a6b-7c8d-9e0f1a2b3c4d', 'type': 'file'}

        Attributes:
            file_id (str): The file whose bytes the block carries, from the caller's organization, unexpired.
            type_ (ManagedAgentsContentBlockSourceType): Always file.
     """

    file_id: str
    type_: ManagedAgentsContentBlockSourceType
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)





    def to_dict(self) -> dict[str, Any]:
        file_id = self.file_id

        type_ = self.type_.value


        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({
            "file_id": file_id,
            "type": type_,
        })

        return field_dict



    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        file_id = d.pop("file_id")

        type_ = ManagedAgentsContentBlockSourceType(d.pop("type"))




        managed_agents_content_block_source = cls(
            file_id=file_id,
            type_=type_,
        )


        managed_agents_content_block_source.additional_properties = d
        return managed_agents_content_block_source

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
