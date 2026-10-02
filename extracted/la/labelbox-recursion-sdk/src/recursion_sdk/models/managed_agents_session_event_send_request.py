from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar, BinaryIO, TextIO, TYPE_CHECKING, Generator

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

from ..types import UNSET, Unset
from typing import cast

if TYPE_CHECKING:
  from ..models.managed_agents_managed_event_send_params import ManagedAgentsManagedEventSendParams





T = TypeVar("T", bound="ManagedAgentsSessionEventSendRequest")



@_attrs_define
class ManagedAgentsSessionEventSendRequest:
    """ Request body of POST /v1/sessions/{session_id}/events. It has two mutually exclusive forms and events wins: send
    message for the common case of one plain-text user turn, or send events as ordered typed turns with provider-shaped
    content. An empty events array always yields exactly one user turn built from message, even when message is empty.
    The handoff_resolved control form rejects all message and referenced-session fields. The response acknowledges
    durable acceptance of the turn, not the agent's reply.

        Example:
            {'actor': 'human:api', 'events': [{'actor': 'human:api', 'content': [{'byte_size': 1, 'content': [], 'context':
                'example', 'data': 'example', 'encrypted_content': 'example', 'height': 1, 'id':
                '9f8b1c2d-3e4f-5a6b-7c8d-9e0f1a2b3c4d', 'input': {'key': 'example'}, 'is_error': True, 'media_type': 'example',
                'name': 'example-name', 'omitted_bytes': 1, 'payload': 'example', 'provider': 'example', 'provider_payload':
                'example', 'redacted': True, 'semantic_hint': 'example', 'sha256': 'example', 'signature': 'example', 'source':
                {'file_id': '9f8b1c2d-3e4f-5a6b-7c8d-9e0f1a2b3c4d', 'type': 'file'}, 'summary': [], 'text': 'example', 'title':
                'example', 'tool_use_id': '9f8b1c2d-3e4f-5a6b-7c8d-9e0f1a2b3c4d', 'type': 'example', 'uri': 'example', 'url':
                'https://example.com', 'url_expires_at': '2026-02-18T09:30:00Z', 'width': 1}], 'handoff_id':
                '9f8b1c2d-3e4f-5a6b-7c8d-9e0f1a2b3c4d', 'note': 'example', 'text': 'example', 'type': 'user.message'}],
                'message': 'example', 'referenced_session_ids': ['example']}

        Attributes:
            actor (str | Unset): Who the turn is attributed to. Defaults to human:api when omitted.
            events (list[ManagedAgentsManagedEventSendParams] | None | Unset): Typed events to append instead of message.
                When present, message and the top-level actor are ignored.
            message (str | Unset): Plain-text message to append as a single user turn. Used only when events is empty.
            referenced_session_ids (list[str] | Unset): Prior sessions this session may read from this turn on, by session
                id, added to any it already has. Each id is authorized under your own scope and grants read access to the whole
                tree containing it; one you cannot read refuses the whole request with 404 and delivers no message. The grant is
                recorded before the message, so the turn it starts is the first one that can use it.
     """

    actor: str | Unset = UNSET
    events: list[ManagedAgentsManagedEventSendParams] | None | Unset = UNSET
    message: str | Unset = UNSET
    referenced_session_ids: list[str] | Unset = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)





    def to_dict(self) -> dict[str, Any]:
        from ..models.managed_agents_managed_event_send_params import ManagedAgentsManagedEventSendParams # noqa: PLC0415
        actor = self.actor

        events: list[dict[str, Any]] | None | Unset
        if isinstance(self.events, Unset):
            events = UNSET
        elif isinstance(self.events, list):
            events = []
            for events_type_0_item_data in self.events:
                events_type_0_item = events_type_0_item_data.to_dict()
                events.append(events_type_0_item)


        else:
            events = self.events

        message = self.message

        referenced_session_ids: list[str] | Unset = UNSET
        if not isinstance(self.referenced_session_ids, Unset):
            referenced_session_ids = self.referenced_session_ids




        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({
        })
        if actor is not UNSET:
            field_dict["actor"] = actor
        if events is not UNSET:
            field_dict["events"] = events
        if message is not UNSET:
            field_dict["message"] = message
        if referenced_session_ids is not UNSET:
            field_dict["referenced_session_ids"] = referenced_session_ids

        return field_dict



    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.managed_agents_managed_event_send_params import ManagedAgentsManagedEventSendParams # noqa: PLC0415
        d = dict(src_dict)
        actor = d.pop("actor", UNSET)

        def _parse_events(data: object) -> list[ManagedAgentsManagedEventSendParams] | None | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            try:
                if not isinstance(data, list):
                    raise TypeError()
                events_type_0 = []
                _events_type_0 = data
                for events_type_0_item_data in (_events_type_0):
                    events_type_0_item = ManagedAgentsManagedEventSendParams.from_dict(events_type_0_item_data)



                    events_type_0.append(events_type_0_item)

                return events_type_0
            except (TypeError, ValueError, AttributeError, KeyError):
                pass
            return cast(list[ManagedAgentsManagedEventSendParams] | None | Unset, data)

        events = _parse_events(d.pop("events", UNSET))


        message = d.pop("message", UNSET)

        referenced_session_ids = cast(list[str], d.pop("referenced_session_ids", UNSET))


        managed_agents_session_event_send_request = cls(
            actor=actor,
            events=events,
            message=message,
            referenced_session_ids=referenced_session_ids,
        )


        managed_agents_session_event_send_request.additional_properties = d
        return managed_agents_session_event_send_request

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
