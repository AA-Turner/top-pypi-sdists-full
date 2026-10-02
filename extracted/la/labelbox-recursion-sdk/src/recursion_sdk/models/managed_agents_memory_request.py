from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar, BinaryIO, TextIO, TYPE_CHECKING, Generator

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

from ..types import UNSET, Unset






T = TypeVar("T", bound="ManagedAgentsMemoryRequest")



@_attrs_define
class ManagedAgentsMemoryRequest:
    """ Fields for updating one memory. Every field is optional and an omitted one is left unchanged. Supply content_sha256
    to apply the write only if the stored content still matches what you read.

        Example:
            {'content': 'example', 'content_sha256': 'example', 'path': 'example', 'summary': 'example'}

        Attributes:
            content (str | Unset): Full text of the memory. Capped at 100 kB; memory works better as many small focused
                documents.
            content_sha256 (str | Unset): Apply only if the stored content hash still matches this value. On mismatch the
                request is a 409 and the caller should re-read and retry.
            path (str | Unset): Address within the store, e.g. /conventions/testing.md. On update, supplying a different
                path renames the memory.
            summary (str | Unset): One line describing what this memory says, shown in search results and the console.
     """

    content: str | Unset = UNSET
    content_sha256: str | Unset = UNSET
    path: str | Unset = UNSET
    summary: str | Unset = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)





    def to_dict(self) -> dict[str, Any]:
        content = self.content

        content_sha256 = self.content_sha256

        path = self.path

        summary = self.summary


        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({
        })
        if content is not UNSET:
            field_dict["content"] = content
        if content_sha256 is not UNSET:
            field_dict["content_sha256"] = content_sha256
        if path is not UNSET:
            field_dict["path"] = path
        if summary is not UNSET:
            field_dict["summary"] = summary

        return field_dict



    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        content = d.pop("content", UNSET)

        content_sha256 = d.pop("content_sha256", UNSET)

        path = d.pop("path", UNSET)

        summary = d.pop("summary", UNSET)

        managed_agents_memory_request = cls(
            content=content,
            content_sha256=content_sha256,
            path=path,
            summary=summary,
        )


        managed_agents_memory_request.additional_properties = d
        return managed_agents_memory_request

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
