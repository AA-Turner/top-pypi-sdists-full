from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar, BinaryIO, TextIO, TYPE_CHECKING, Generator

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

from typing import cast

if TYPE_CHECKING:
  from ..models.managed_agents_agent_memory_summary import ManagedAgentsAgentMemorySummary





T = TypeVar("T", bound="ManagedAgentsAgentMemoryListResponse")



@_attrs_define
class ManagedAgentsAgentMemoryListResponse:
    """ Current memory and learning status across the organization's agents.

        Example:
            {'agents': [{'agent_id': '9f8b1c2d-3e4f-5a6b-7c8d-9e0f1a2b3c4d', 'agent_name': 'example', 'effective_model':
                'example', 'failed_session_count': 1, 'last_checked_at': '2026-02-18T09:30:00Z', 'last_updated_at':
                '2026-02-18T09:30:00Z', 'memory_count': 1, 'memory_model_ref': 'example', 'memory_store_id':
                '9f8b1c2d-3e4f-5a6b-7c8d-9e0f1a2b3c4d', 'next_retry_at': '2026-02-18T09:30:00Z', 'pending_session_count': 1,
                'revision': 1, 'state': 'waiting', 'total_bytes': 1}]}

        Attributes:
            agents (list[ManagedAgentsAgentMemorySummary]): Memory summary for every customer agent in the calling
                organization, including empty collections.
     """

    agents: list[ManagedAgentsAgentMemorySummary]
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)





    def to_dict(self) -> dict[str, Any]:
        from ..models.managed_agents_agent_memory_summary import ManagedAgentsAgentMemorySummary # noqa: PLC0415
        agents = []
        for agents_item_data in self.agents:
            agents_item = agents_item_data.to_dict()
            agents.append(agents_item)




        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({
            "agents": agents,
        })

        return field_dict



    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.managed_agents_agent_memory_summary import ManagedAgentsAgentMemorySummary # noqa: PLC0415
        d = dict(src_dict)
        agents = []
        _agents = d.pop("agents")
        for agents_item_data in (_agents):
            agents_item = ManagedAgentsAgentMemorySummary.from_dict(agents_item_data)



            agents.append(agents_item)


        managed_agents_agent_memory_list_response = cls(
            agents=agents,
        )


        managed_agents_agent_memory_list_response.additional_properties = d
        return managed_agents_agent_memory_list_response

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
