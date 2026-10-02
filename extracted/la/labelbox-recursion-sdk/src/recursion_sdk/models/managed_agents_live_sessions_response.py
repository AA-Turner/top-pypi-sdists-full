from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar, BinaryIO, TextIO, TYPE_CHECKING, Generator

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

from ..types import UNSET, Unset
from typing import cast
import datetime

if TYPE_CHECKING:
  from ..models.managed_agents_live_fleet_agent import ManagedAgentsLiveFleetAgent





T = TypeVar("T", bound="ManagedAgentsLiveSessionsResponse")



@_attrs_define
class ManagedAgentsLiveSessionsResponse:
    """ Response body of GET /v1/sessions/live: what an organization's agents are running at one instant, whenever those
    sessions were created.

        Example:
            {'agents': [{'agent_id': '9f8b1c2d-3e4f-5a6b-7c8d-9e0f1a2b3c4d', 'awaiting_human': 1, 'name': 'example-name',
                'running': 1, 'waiting': 1}], 'as_of': '2026-02-18T09:30:00Z', 'awaiting_human': 1, 'running': 1, 'truncated':
                True, 'waiting': 1}

        Attributes:
            agents (list[ManagedAgentsLiveFleetAgent]): Every agent with at least one live root session, busiest first.
                Always an array.
            as_of (datetime.datetime): RFC 3339 timestamp the counts were read at.
            awaiting_human (int): Root sessions stopped for a person across the agents counted.
            running (int): Running root sessions across the agents counted.
            waiting (int): Waiting root sessions across the agents counted.
            truncated (bool | Unset): True when the organization has more agents than one read counts, so the totals are of
                the agents counted rather than of the fleet.
     """

    agents: list[ManagedAgentsLiveFleetAgent]
    as_of: datetime.datetime
    awaiting_human: int
    running: int
    waiting: int
    truncated: bool | Unset = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)





    def to_dict(self) -> dict[str, Any]:
        from ..models.managed_agents_live_fleet_agent import ManagedAgentsLiveFleetAgent # noqa: PLC0415
        agents = []
        for agents_item_data in self.agents:
            agents_item = agents_item_data.to_dict()
            agents.append(agents_item)



        as_of = self.as_of.isoformat()

        awaiting_human = self.awaiting_human

        running = self.running

        waiting = self.waiting

        truncated = self.truncated


        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({
            "agents": agents,
            "as_of": as_of,
            "awaiting_human": awaiting_human,
            "running": running,
            "waiting": waiting,
        })
        if truncated is not UNSET:
            field_dict["truncated"] = truncated

        return field_dict



    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.managed_agents_live_fleet_agent import ManagedAgentsLiveFleetAgent # noqa: PLC0415
        d = dict(src_dict)
        agents = []
        _agents = d.pop("agents")
        for agents_item_data in (_agents):
            agents_item = ManagedAgentsLiveFleetAgent.from_dict(agents_item_data)



            agents.append(agents_item)


        as_of = datetime.datetime.fromisoformat(d.pop("as_of"))




        awaiting_human = d.pop("awaiting_human")

        running = d.pop("running")

        waiting = d.pop("waiting")

        truncated = d.pop("truncated", UNSET)

        managed_agents_live_sessions_response = cls(
            agents=agents,
            as_of=as_of,
            awaiting_human=awaiting_human,
            running=running,
            waiting=waiting,
            truncated=truncated,
        )


        managed_agents_live_sessions_response.additional_properties = d
        return managed_agents_live_sessions_response

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
