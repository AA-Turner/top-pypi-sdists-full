from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar, BinaryIO, TextIO, TYPE_CHECKING, Generator

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

from ..types import UNSET, Unset
from typing import cast

if TYPE_CHECKING:
  from ..models.managed_agents_memory import ManagedAgentsMemory





T = TypeVar("T", bound="ManagedAgentsAgentMemoriesPage")



@_attrs_define
class ManagedAgentsAgentMemoriesPage:
    """ A searchable page of an agent's current memories.

        Example:
            {'memories': [{'byte_size': 1, 'content': 'example', 'content_sha256': 'example', 'created_at':
                '2026-02-18T09:30:00Z', 'deleted_at': '2026-02-18T09:30:00Z', 'head_version_id':
                '9f8b1c2d-3e4f-5a6b-7c8d-9e0f1a2b3c4d', 'memory_id': '9f8b1c2d-3e4f-5a6b-7c8d-9e0f1a2b3c4d', 'memory_store_id':
                '9f8b1c2d-3e4f-5a6b-7c8d-9e0f1a2b3c4d', 'organization_id': '9f8b1c2d-3e4f-5a6b-7c8d-9e0f1a2b3c4d', 'path':
                'example', 'reflection_id': '9f8b1c2d-3e4f-5a6b-7c8d-9e0f1a2b3c4d', 'status': 'active', 'summary': 'example',
                'superseded_by_memory_id': '9f8b1c2d-3e4f-5a6b-7c8d-9e0f1a2b3c4d', 'updated_at': '2026-02-18T09:30:00Z'}],
                'next_cursor': 'example', 'topics': ['example']}

        Attributes:
            memories (list[ManagedAgentsMemory]): Current memories matching the query, without full content.
            topics (list[str]): Topics from the entire current collection, independent of search and pagination.
            next_cursor (str | Unset): Opaque cursor for the next page; absent on the final page.
     """

    memories: list[ManagedAgentsMemory]
    topics: list[str]
    next_cursor: str | Unset = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)





    def to_dict(self) -> dict[str, Any]:
        from ..models.managed_agents_memory import ManagedAgentsMemory # noqa: PLC0415
        memories = []
        for memories_item_data in self.memories:
            memories_item = memories_item_data.to_dict()
            memories.append(memories_item)



        topics = self.topics



        next_cursor = self.next_cursor


        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({
            "memories": memories,
            "topics": topics,
        })
        if next_cursor is not UNSET:
            field_dict["next_cursor"] = next_cursor

        return field_dict



    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.managed_agents_memory import ManagedAgentsMemory # noqa: PLC0415
        d = dict(src_dict)
        memories = []
        _memories = d.pop("memories")
        for memories_item_data in (_memories):
            memories_item = ManagedAgentsMemory.from_dict(memories_item_data)



            memories.append(memories_item)


        topics = cast(list[str], d.pop("topics"))


        next_cursor = d.pop("next_cursor", UNSET)

        managed_agents_agent_memories_page = cls(
            memories=memories,
            topics=topics,
            next_cursor=next_cursor,
        )


        managed_agents_agent_memories_page.additional_properties = d
        return managed_agents_agent_memories_page

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
