from __future__ import annotations

from collections.abc import Mapping
from typing import TYPE_CHECKING, Any, TypeVar

from attrs import define as _attrs_define

if TYPE_CHECKING:
    from ..models.cloud_agent_event import CloudAgentEvent


T = TypeVar("T", bound="CloudAgentSessionEvents")


@_attrs_define
class CloudAgentSessionEvents:
    """
    Attributes:
        agent_id (str):
        session_id (str):
        events (list[CloudAgentEvent]):
    """

    agent_id: str
    session_id: str
    events: list[CloudAgentEvent]

    def to_dict(self) -> dict[str, Any]:
        agent_id = self.agent_id

        session_id = self.session_id

        events = []
        for events_item_data in self.events:
            events_item = events_item_data.to_dict()
            events.append(events_item)

        field_dict: dict[str, Any] = {}

        field_dict.update(
            {
                "agent_id": agent_id,
                "session_id": session_id,
                "events": events,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.cloud_agent_event import CloudAgentEvent

        d = dict(src_dict)
        agent_id = d.pop("agent_id")

        session_id = d.pop("session_id")

        events = []
        _events = d.pop("events")
        for events_item_data in _events:
            events_item = CloudAgentEvent.from_dict(events_item_data)

            events.append(events_item)

        cloud_agent_session_events = cls(
            agent_id=agent_id,
            session_id=session_id,
            events=events,
        )

        return cloud_agent_session_events
