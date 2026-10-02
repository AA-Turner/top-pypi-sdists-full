from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar, BinaryIO, TextIO, TYPE_CHECKING, Generator

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset







T = TypeVar("T", bound="ManagedAgentsMemoryCreateRequest")



@_attrs_define
class ManagedAgentsMemoryCreateRequest:
    """ Fields for creating one memory. Path, content and summary are all required; omitting any of them is a 400.

        Example:
            {'content': 'example', 'path': 'example', 'summary': 'example'}

        Attributes:
            content (str): Full text of the memory. Capped at 100 kB; memory works better as many small focused documents.
            path (str): Address within the store, e.g. /conventions/testing.md.
            summary (str): One line describing what this memory says, shown in search results and the console.
     """

    content: str
    path: str
    summary: str
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)





    def to_dict(self) -> dict[str, Any]:
        content = self.content

        path = self.path

        summary = self.summary


        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({
            "content": content,
            "path": path,
            "summary": summary,
        })

        return field_dict



    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        content = d.pop("content")

        path = d.pop("path")

        summary = d.pop("summary")

        managed_agents_memory_create_request = cls(
            content=content,
            path=path,
            summary=summary,
        )


        managed_agents_memory_create_request.additional_properties = d
        return managed_agents_memory_create_request

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
