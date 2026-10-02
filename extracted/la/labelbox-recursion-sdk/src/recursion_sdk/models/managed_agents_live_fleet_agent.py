from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar, BinaryIO, TextIO, TYPE_CHECKING, Generator

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

from uuid import UUID






T = TypeVar("T", bound="ManagedAgentsLiveFleetAgent")



@_attrs_define
class ManagedAgentsLiveFleetAgent:
    """ One agent's live root sessions: running, waiting for a concurrency slot, and stopped for a person, counted at the
    same instant as the fleet's totals.

        Example:
            {'agent_id': '9f8b1c2d-3e4f-5a6b-7c8d-9e0f1a2b3c4d', 'awaiting_human': 1, 'name': 'example-name', 'running': 1,
                'waiting': 1}

        Attributes:
            agent_id (UUID): Agent identifier.
            awaiting_human (int): Root sessions stopped for a person.
            name (str): Operator-facing agent name.
            running (int): Root sessions running now: they hold one of the agent's concurrency slots, or the agent has no
                cap.
            waiting (int): Root sessions accepted and waiting for a concurrency slot the agent's cap holds back.
     """

    agent_id: UUID
    awaiting_human: int
    name: str
    running: int
    waiting: int
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)





    def to_dict(self) -> dict[str, Any]:
        agent_id = str(self.agent_id)

        awaiting_human = self.awaiting_human

        name = self.name

        running = self.running

        waiting = self.waiting


        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({
            "agent_id": agent_id,
            "awaiting_human": awaiting_human,
            "name": name,
            "running": running,
            "waiting": waiting,
        })

        return field_dict



    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        agent_id = UUID(d.pop("agent_id"))




        awaiting_human = d.pop("awaiting_human")

        name = d.pop("name")

        running = d.pop("running")

        waiting = d.pop("waiting")

        managed_agents_live_fleet_agent = cls(
            agent_id=agent_id,
            awaiting_human=awaiting_human,
            name=name,
            running=running,
            waiting=waiting,
        )


        managed_agents_live_fleet_agent.additional_properties = d
        return managed_agents_live_fleet_agent

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
