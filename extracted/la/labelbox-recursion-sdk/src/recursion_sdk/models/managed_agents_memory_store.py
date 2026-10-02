from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar, BinaryIO, TextIO, TYPE_CHECKING, Generator

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

from ..models.managed_agents_memory_store_origin import ManagedAgentsMemoryStoreOrigin
from ..models.managed_agents_memory_store_status import ManagedAgentsMemoryStoreStatus
from ..types import UNSET, Unset
from typing import cast
import datetime






T = TypeVar("T", bound="ManagedAgentsMemoryStore")



@_attrs_define
class ManagedAgentsMemoryStore:
    """ A collection of path-addressed documents an agent reads across sessions. Attaching a store adds one note to the
    system prompt naming what it contains; the agent browses, searches, and reads its contents on demand, so store size
    does not enter the prompt.

        Example:
            {'agent_id': '9f8b1c2d-3e4f-5a6b-7c8d-9e0f1a2b3c4d', 'archived_at': '2026-02-18T09:30:00Z', 'created_at':
                '2026-02-18T09:30:00Z', 'created_by': 'example', 'description': 'example', 'memory_count': 1, 'memory_store_id':
                '9f8b1c2d-3e4f-5a6b-7c8d-9e0f1a2b3c4d', 'name': 'example-name', 'organization_id':
                '9f8b1c2d-3e4f-5a6b-7c8d-9e0f1a2b3c4d', 'origin': 'curated', 'revision': 1, 'slug': 'example', 'status':
                'active', 'total_bytes': 1, 'updated_at': '2026-02-18T09:30:00Z'}

        Attributes:
            created_at (datetime.datetime): Server-assigned RFC 3339 timestamp of when the store was created.
            memory_count (int): Number of live memories in the store.
            memory_store_id (str): Server-assigned id of the store, used when attaching it to a session and in the memory
                routes.
            name (str): Human-readable name. Shown to the agent as part of the store's note.
            organization_id (str): Organization that owns the store. Server-assigned from the caller's credentials; a value
                sent in a request body is ignored.
            origin (ManagedAgentsMemoryStoreOrigin): Who wrote this store: curated for material a human seeded, reflection
                for a consolidation's output. A reflection store is not hand-editable.
            revision (int): Monotonic revision of the collection, advanced atomically when a learning run changes memories.
            slug (str): Filesystem-safe form of the name, stable across renames.
            status (ManagedAgentsMemoryStoreStatus): Active collections are available to sessions; archived curated stores
                cannot be attached.
            total_bytes (int): Total bytes of live memory content in the store.
            updated_at (datetime.datetime): Server-assigned RFC 3339 timestamp of the most recent change to the store or its
                memories.
            agent_id (str | Unset): Agent this store belongs to. Empty for a workspace store any session may attach.
            archived_at (datetime.datetime | Unset): Set when a curated reference store was archived.
            created_by (str | Unset): Identifier of the caller or reflection that created the store.
            description (str | Unset): What this store contains. Disclosed to the agent in every session the store is
                attached to, so it is the routing signal: write it as what the agent would be looking for.
     """

    created_at: datetime.datetime
    memory_count: int
    memory_store_id: str
    name: str
    organization_id: str
    origin: ManagedAgentsMemoryStoreOrigin
    revision: int
    slug: str
    status: ManagedAgentsMemoryStoreStatus
    total_bytes: int
    updated_at: datetime.datetime
    agent_id: str | Unset = UNSET
    archived_at: datetime.datetime | Unset = UNSET
    created_by: str | Unset = UNSET
    description: str | Unset = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)





    def to_dict(self) -> dict[str, Any]:
        created_at = self.created_at.isoformat()

        memory_count = self.memory_count

        memory_store_id = self.memory_store_id

        name = self.name

        organization_id = self.organization_id

        origin = self.origin.value

        revision = self.revision

        slug = self.slug

        status = self.status.value

        total_bytes = self.total_bytes

        updated_at = self.updated_at.isoformat()

        agent_id = self.agent_id

        archived_at: str | Unset = UNSET
        if not isinstance(self.archived_at, Unset):
            archived_at = self.archived_at.isoformat()

        created_by = self.created_by

        description = self.description


        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({
            "created_at": created_at,
            "memory_count": memory_count,
            "memory_store_id": memory_store_id,
            "name": name,
            "organization_id": organization_id,
            "origin": origin,
            "revision": revision,
            "slug": slug,
            "status": status,
            "total_bytes": total_bytes,
            "updated_at": updated_at,
        })
        if agent_id is not UNSET:
            field_dict["agent_id"] = agent_id
        if archived_at is not UNSET:
            field_dict["archived_at"] = archived_at
        if created_by is not UNSET:
            field_dict["created_by"] = created_by
        if description is not UNSET:
            field_dict["description"] = description

        return field_dict



    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        created_at = datetime.datetime.fromisoformat(d.pop("created_at"))




        memory_count = d.pop("memory_count")

        memory_store_id = d.pop("memory_store_id")

        name = d.pop("name")

        organization_id = d.pop("organization_id")

        origin = ManagedAgentsMemoryStoreOrigin(d.pop("origin"))




        revision = d.pop("revision")

        slug = d.pop("slug")

        status = ManagedAgentsMemoryStoreStatus(d.pop("status"))




        total_bytes = d.pop("total_bytes")

        updated_at = datetime.datetime.fromisoformat(d.pop("updated_at"))




        agent_id = d.pop("agent_id", UNSET)

        _archived_at = d.pop("archived_at", UNSET)
        archived_at: datetime.datetime | Unset
        if isinstance(_archived_at,  Unset):
            archived_at = UNSET
        else:
            archived_at = datetime.datetime.fromisoformat(_archived_at)




        created_by = d.pop("created_by", UNSET)

        description = d.pop("description", UNSET)

        managed_agents_memory_store = cls(
            created_at=created_at,
            memory_count=memory_count,
            memory_store_id=memory_store_id,
            name=name,
            organization_id=organization_id,
            origin=origin,
            revision=revision,
            slug=slug,
            status=status,
            total_bytes=total_bytes,
            updated_at=updated_at,
            agent_id=agent_id,
            archived_at=archived_at,
            created_by=created_by,
            description=description,
        )


        managed_agents_memory_store.additional_properties = d
        return managed_agents_memory_store

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
