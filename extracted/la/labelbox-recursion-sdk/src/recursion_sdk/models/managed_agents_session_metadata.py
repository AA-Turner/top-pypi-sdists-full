from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar, BinaryIO, TextIO, TYPE_CHECKING, Generator

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset







T = TypeVar("T", bound="ManagedAgentsSessionMetadata")



@_attrs_define
class ManagedAgentsSessionMetadata:
    """ Caller-defined string key/value pairs supplied when the session was started, e.g. ids from your own system.
    Immutable, present on root sessions only, and filterable with metadata=key:value or metadata_key=key on GET
    /v1/sessions. At most 32 entries; keys use letters, digits, '_', '.', and '-' up to 64 characters; values are 1-512
    characters.

     """

    additional_properties: dict[str, str] = _attrs_field(init=False, factory=dict)





    def to_dict(self) -> dict[str, Any]:
        
        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)

        return field_dict



    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        managed_agents_session_metadata = cls(
        )


        managed_agents_session_metadata.additional_properties = d
        return managed_agents_session_metadata

    @property
    def additional_keys(self) -> list[str]:
        return list(self.additional_properties.keys())

    def __getitem__(self, key: str) -> str:
        return self.additional_properties[key]

    def __setitem__(self, key: str, value: str) -> None:
        self.additional_properties[key] = value

    def __delitem__(self, key: str) -> None:
        del self.additional_properties[key]

    def __contains__(self, key: str) -> bool:
        return key in self.additional_properties
