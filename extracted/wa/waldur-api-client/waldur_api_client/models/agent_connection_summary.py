from collections.abc import Mapping
from typing import Any, TypeVar

from attrs import define as _attrs_define
from attrs import field as _attrs_field

T = TypeVar("T", bound="AgentConnectionSummary")


@_attrs_define
class AgentConnectionSummary:
    """
    Attributes:
        total_agents (int): Total number of registered agents
        connected_agents (int): Number of agents with active RMQ connections
        disconnected_agents (int): Number of agents without active connections
        total_queued_messages (int): Total messages across all agent queues
    """

    total_agents: int
    connected_agents: int
    disconnected_agents: int
    total_queued_messages: int
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        total_agents = self.total_agents

        connected_agents = self.connected_agents

        disconnected_agents = self.disconnected_agents

        total_queued_messages = self.total_queued_messages

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "total_agents": total_agents,
                "connected_agents": connected_agents,
                "disconnected_agents": disconnected_agents,
                "total_queued_messages": total_queued_messages,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        total_agents = d.pop("total_agents")

        connected_agents = d.pop("connected_agents")

        disconnected_agents = d.pop("disconnected_agents")

        total_queued_messages = d.pop("total_queued_messages")

        agent_connection_summary = cls(
            total_agents=total_agents,
            connected_agents=connected_agents,
            disconnected_agents=disconnected_agents,
            total_queued_messages=total_queued_messages,
        )

        agent_connection_summary.additional_properties = d
        return agent_connection_summary

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
