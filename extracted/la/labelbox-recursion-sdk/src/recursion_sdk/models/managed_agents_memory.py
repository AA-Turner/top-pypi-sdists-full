from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar, BinaryIO, TextIO, TYPE_CHECKING, Generator

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

from ..models.managed_agents_memory_status import ManagedAgentsMemoryStatus
from ..types import UNSET, Unset
from typing import cast
import datetime






T = TypeVar("T", bound="ManagedAgentsMemory")



@_attrs_define
class ManagedAgentsMemory:
    """ One path-addressed document in a memory store. The path hierarchy is the routing structure an agent browses, so it
    carries the meaning a per-memory prompt description otherwise would.

        Example:
            {'byte_size': 1, 'content': 'example', 'content_sha256': 'example', 'created_at': '2026-02-18T09:30:00Z',
                'deleted_at': '2026-02-18T09:30:00Z', 'head_version_id': '9f8b1c2d-3e4f-5a6b-7c8d-9e0f1a2b3c4d', 'memory_id':
                '9f8b1c2d-3e4f-5a6b-7c8d-9e0f1a2b3c4d', 'memory_store_id': '9f8b1c2d-3e4f-5a6b-7c8d-9e0f1a2b3c4d',
                'organization_id': '9f8b1c2d-3e4f-5a6b-7c8d-9e0f1a2b3c4d', 'path': 'example', 'reflection_id':
                '9f8b1c2d-3e4f-5a6b-7c8d-9e0f1a2b3c4d', 'status': 'active', 'summary': 'example', 'superseded_by_memory_id':
                '9f8b1c2d-3e4f-5a6b-7c8d-9e0f1a2b3c4d', 'updated_at': '2026-02-18T09:30:00Z'}

        Attributes:
            byte_size (int): Size of the content in bytes.
            created_at (datetime.datetime): Server-assigned RFC 3339 timestamp of when the memory was created.
            memory_id (str): Server-assigned id of the memory.
            memory_store_id (str): Store this memory belongs to.
            organization_id (str): Organization that owns this record. Resolved from the API key; never accepted from the
                caller.
            path (str): Address of the memory within its store, e.g. /conventions/testing.md. The path hierarchy is the
                routing structure an agent browses, so it carries the meaning a per-memory prompt description otherwise would.
            status (ManagedAgentsMemoryStatus): active is disclosed to sessions; retired and superseded are kept so evidence
                stays resolvable and the next consolidation can see what was already tried.
            updated_at (datetime.datetime): Server-assigned RFC 3339 timestamp of the most recent change.
            content (str | Unset): Full text of the memory. Returned when reading one memory, omitted from listings.
            content_sha256 (str | Unset): SHA-256 of the content. Pass it back as an update precondition to avoid clobbering
                a concurrent write.
            deleted_at (datetime.datetime | Unset): Set when the memory was deleted. A deleted path may be recreated.
            head_version_id (str | Unset): Version id of the current content.
            reflection_id (str | Unset): Reflection run that wrote this memory. Empty for a memory a human seeded.
            summary (str | Unset): One-line description, shown in search results and the console. Not disclosed in the
                system prompt.
            superseded_by_memory_id (str | Unset): Memory that replaced this one, when a consolidation superseded it.
     """

    byte_size: int
    created_at: datetime.datetime
    memory_id: str
    memory_store_id: str
    organization_id: str
    path: str
    status: ManagedAgentsMemoryStatus
    updated_at: datetime.datetime
    content: str | Unset = UNSET
    content_sha256: str | Unset = UNSET
    deleted_at: datetime.datetime | Unset = UNSET
    head_version_id: str | Unset = UNSET
    reflection_id: str | Unset = UNSET
    summary: str | Unset = UNSET
    superseded_by_memory_id: str | Unset = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)





    def to_dict(self) -> dict[str, Any]:
        byte_size = self.byte_size

        created_at = self.created_at.isoformat()

        memory_id = self.memory_id

        memory_store_id = self.memory_store_id

        organization_id = self.organization_id

        path = self.path

        status = self.status.value

        updated_at = self.updated_at.isoformat()

        content = self.content

        content_sha256 = self.content_sha256

        deleted_at: str | Unset = UNSET
        if not isinstance(self.deleted_at, Unset):
            deleted_at = self.deleted_at.isoformat()

        head_version_id = self.head_version_id

        reflection_id = self.reflection_id

        summary = self.summary

        superseded_by_memory_id = self.superseded_by_memory_id


        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({
            "byte_size": byte_size,
            "created_at": created_at,
            "memory_id": memory_id,
            "memory_store_id": memory_store_id,
            "organization_id": organization_id,
            "path": path,
            "status": status,
            "updated_at": updated_at,
        })
        if content is not UNSET:
            field_dict["content"] = content
        if content_sha256 is not UNSET:
            field_dict["content_sha256"] = content_sha256
        if deleted_at is not UNSET:
            field_dict["deleted_at"] = deleted_at
        if head_version_id is not UNSET:
            field_dict["head_version_id"] = head_version_id
        if reflection_id is not UNSET:
            field_dict["reflection_id"] = reflection_id
        if summary is not UNSET:
            field_dict["summary"] = summary
        if superseded_by_memory_id is not UNSET:
            field_dict["superseded_by_memory_id"] = superseded_by_memory_id

        return field_dict



    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        byte_size = d.pop("byte_size")

        created_at = datetime.datetime.fromisoformat(d.pop("created_at"))




        memory_id = d.pop("memory_id")

        memory_store_id = d.pop("memory_store_id")

        organization_id = d.pop("organization_id")

        path = d.pop("path")

        status = ManagedAgentsMemoryStatus(d.pop("status"))




        updated_at = datetime.datetime.fromisoformat(d.pop("updated_at"))




        content = d.pop("content", UNSET)

        content_sha256 = d.pop("content_sha256", UNSET)

        _deleted_at = d.pop("deleted_at", UNSET)
        deleted_at: datetime.datetime | Unset
        if isinstance(_deleted_at,  Unset):
            deleted_at = UNSET
        else:
            deleted_at = datetime.datetime.fromisoformat(_deleted_at)




        head_version_id = d.pop("head_version_id", UNSET)

        reflection_id = d.pop("reflection_id", UNSET)

        summary = d.pop("summary", UNSET)

        superseded_by_memory_id = d.pop("superseded_by_memory_id", UNSET)

        managed_agents_memory = cls(
            byte_size=byte_size,
            created_at=created_at,
            memory_id=memory_id,
            memory_store_id=memory_store_id,
            organization_id=organization_id,
            path=path,
            status=status,
            updated_at=updated_at,
            content=content,
            content_sha256=content_sha256,
            deleted_at=deleted_at,
            head_version_id=head_version_id,
            reflection_id=reflection_id,
            summary=summary,
            superseded_by_memory_id=superseded_by_memory_id,
        )


        managed_agents_memory.additional_properties = d
        return managed_agents_memory

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
