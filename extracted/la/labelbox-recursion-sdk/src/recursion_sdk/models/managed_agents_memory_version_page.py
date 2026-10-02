from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar, BinaryIO, TextIO, TYPE_CHECKING, Generator

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

from ..types import UNSET, Unset
from typing import cast

if TYPE_CHECKING:
  from ..models.managed_agents_memory_version import ManagedAgentsMemoryVersion





T = TypeVar("T", bound="ManagedAgentsMemoryVersionPage")



@_attrs_define
class ManagedAgentsMemoryVersionPage:
    """ A page of immutable memory history, including the evidence and reason for each change.

        Example:
            {'memory_versions': [{'author_kind': 'session', 'author_principal': 'example', 'author_session_id':
                '9f8b1c2d-3e4f-5a6b-7c8d-9e0f1a2b3c4d', 'byte_size': 1, 'content': 'example', 'content_sha256': 'example',
                'created_at': '2026-02-18T09:30:00Z', 'evidence_session_ids': ['example'], 'memory_id':
                '9f8b1c2d-3e4f-5a6b-7c8d-9e0f1a2b3c4d', 'memory_store_id': '9f8b1c2d-3e4f-5a6b-7c8d-9e0f1a2b3c4d',
                'memory_version_id': '9f8b1c2d-3e4f-5a6b-7c8d-9e0f1a2b3c4d', 'operation': 'create', 'organization_id':
                '9f8b1c2d-3e4f-5a6b-7c8d-9e0f1a2b3c4d', 'path': 'example', 'rationale': 'example', 'redacted_at':
                '2026-02-18T09:30:00Z', 'redacted_by': 'example', 'reflection_id': '9f8b1c2d-3e4f-5a6b-7c8d-9e0f1a2b3c4d',
                'status': 'active', 'summary': 'example', 'superseded_by_memory_id': '9f8b1c2d-3e4f-5a6b-7c8d-9e0f1a2b3c4d'}],
                'next_cursor': 'example'}

        Attributes:
            memory_versions (list[ManagedAgentsMemoryVersion]): Changes to the collection's memories, newest first, without
                full content.
            next_cursor (str | Unset): Opaque cursor for the next page of retained memory history.
     """

    memory_versions: list[ManagedAgentsMemoryVersion]
    next_cursor: str | Unset = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)





    def to_dict(self) -> dict[str, Any]:
        from ..models.managed_agents_memory_version import ManagedAgentsMemoryVersion # noqa: PLC0415
        memory_versions = []
        for memory_versions_item_data in self.memory_versions:
            memory_versions_item = memory_versions_item_data.to_dict()
            memory_versions.append(memory_versions_item)



        next_cursor = self.next_cursor


        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({
            "memory_versions": memory_versions,
        })
        if next_cursor is not UNSET:
            field_dict["next_cursor"] = next_cursor

        return field_dict



    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.managed_agents_memory_version import ManagedAgentsMemoryVersion # noqa: PLC0415
        d = dict(src_dict)
        memory_versions = []
        _memory_versions = d.pop("memory_versions")
        for memory_versions_item_data in (_memory_versions):
            memory_versions_item = ManagedAgentsMemoryVersion.from_dict(memory_versions_item_data)



            memory_versions.append(memory_versions_item)


        next_cursor = d.pop("next_cursor", UNSET)

        managed_agents_memory_version_page = cls(
            memory_versions=memory_versions,
            next_cursor=next_cursor,
        )


        managed_agents_memory_version_page.additional_properties = d
        return managed_agents_memory_version_page

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
