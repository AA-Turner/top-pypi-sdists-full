from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar, BinaryIO, TextIO, TYPE_CHECKING, Generator

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

from ..models.managed_agents_list_entry_type import ManagedAgentsListEntryType
from ..types import UNSET, Unset






T = TypeVar("T", bound="ManagedAgentsListEntry")



@_attrs_define
class ManagedAgentsListEntry:
    """ One row of a memory browse result: a memory, or a prefix standing for everything beneath it. A prefix carries a
    count so a reader can decide whether to descend without descending.

        Example:
            {'byte_size': 1, 'count': 1, 'path': 'example', 'summary': 'example', 'type': 'memory'}

        Attributes:
            path (str): Path of the memory, or the prefix including its trailing slash.
            type_ (ManagedAgentsListEntryType): memory for a document, memory_prefix for a directory standing for the paths
                beneath it.
            byte_size (int | Unset): Size of the memory in bytes. Absent for a prefix.
            count (int | Unset): Number of memories beneath a prefix. Absent for a memory.
            summary (str | Unset): One-line description. Present for a memory, absent for a prefix.
     """

    path: str
    type_: ManagedAgentsListEntryType
    byte_size: int | Unset = UNSET
    count: int | Unset = UNSET
    summary: str | Unset = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)





    def to_dict(self) -> dict[str, Any]:
        path = self.path

        type_ = self.type_.value

        byte_size = self.byte_size

        count = self.count

        summary = self.summary


        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({
            "path": path,
            "type": type_,
        })
        if byte_size is not UNSET:
            field_dict["byte_size"] = byte_size
        if count is not UNSET:
            field_dict["count"] = count
        if summary is not UNSET:
            field_dict["summary"] = summary

        return field_dict



    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        path = d.pop("path")

        type_ = ManagedAgentsListEntryType(d.pop("type"))




        byte_size = d.pop("byte_size", UNSET)

        count = d.pop("count", UNSET)

        summary = d.pop("summary", UNSET)

        managed_agents_list_entry = cls(
            path=path,
            type_=type_,
            byte_size=byte_size,
            count=count,
            summary=summary,
        )


        managed_agents_list_entry.additional_properties = d
        return managed_agents_list_entry

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
