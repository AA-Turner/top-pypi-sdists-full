from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar, BinaryIO, TextIO, TYPE_CHECKING, Generator

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

from ..models.managed_agents_managed_event_send_params_type import ManagedAgentsManagedEventSendParamsType
from ..types import UNSET, Unset
from typing import cast

if TYPE_CHECKING:
  from ..models.managed_agents_content_block_request import ManagedAgentsContentBlockRequest





T = TypeVar("T", bound="ManagedAgentsManagedEventSendParams")



@_attrs_define
class ManagedAgentsManagedEventSendParams:
    """ One typed event in the events array of a POST /v1/sessions/{session_id}/events body. It is lenient for messages: an
    unrecognised type, and a user.message carrying neither content nor text, are dropped silently rather than rejected,
    so compare events_accepted in the response against how many entries were sent. handoff_resolved is a strict control
    event: it must be the only entry and accepts only type, handoff_id, and note. The request fails with 400 only if
    every entry was dropped, leaving nothing to accept.

        Example:
            {'actor': 'human:api', 'content': [{'byte_size': 1, 'content': [], 'context': 'example', 'data': 'example',
                'encrypted_content': 'example', 'height': 1, 'id': '9f8b1c2d-3e4f-5a6b-7c8d-9e0f1a2b3c4d', 'input': {'key':
                'example'}, 'is_error': True, 'media_type': 'example', 'name': 'example-name', 'omitted_bytes': 1, 'payload':
                'example', 'provider': 'example', 'provider_payload': 'example', 'redacted': True, 'semantic_hint': 'example',
                'sha256': 'example', 'signature': 'example', 'source': {'file_id': '9f8b1c2d-3e4f-5a6b-7c8d-9e0f1a2b3c4d',
                'type': 'file'}, 'summary': [], 'text': 'example', 'title': 'example', 'tool_use_id':
                '9f8b1c2d-3e4f-5a6b-7c8d-9e0f1a2b3c4d', 'type': 'example', 'uri': 'example', 'url': 'https://example.com',
                'url_expires_at': '2026-02-18T09:30:00Z', 'width': 1}], 'handoff_id': '9f8b1c2d-3e4f-5a6b-7c8d-9e0f1a2b3c4d',
                'note': 'example', 'text': 'example', 'type': 'user.message'}

        Attributes:
            actor (str | Unset): Who this event is attributed to. Defaults to human:api when omitted.
            content (list[ManagedAgentsContentBlockRequest] | None | Unset): Provider-shaped content blocks, passed through
                verbatim, except that a top-level image or document block may name a file from the organization's catalog with
                source {type: file, file_id} instead of carrying bytes: the file is read when the message is accepted, an image
                is copied into the session and the block keeps the source beside the copy's uri, and a text document is inlined
                as a text block wrapped with its source, name, title, and context. The send route's description carries the
                limits on such blocks and what they may bring in. Takes precedence over text.
            handoff_id (str | Unset): Stable id from session.active_handoff. Required for handoff_resolved and ignored for
                message events.
            note (str | Unset): Optional note telling the agent what the user did before handing the browser back. Used only
                for handoff_resolved.
            text (str | Unset): Convenience shorthand for a single text content block. Ignored when content is set.
            type_ (ManagedAgentsManagedEventSendParamsType | Unset): Event type. Defaults to user.message when omitted.
                handoff_resolved is the dedicated control event for handing the shared browser back; it must be the only event
                in the request. Other unrecognised values are silently ignored. Interrupts use the permission-isolated interrupt
                endpoints.
     """

    actor: str | Unset = UNSET
    content: list[ManagedAgentsContentBlockRequest] | None | Unset = UNSET
    handoff_id: str | Unset = UNSET
    note: str | Unset = UNSET
    text: str | Unset = UNSET
    type_: ManagedAgentsManagedEventSendParamsType | Unset = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)





    def to_dict(self) -> dict[str, Any]:
        from ..models.managed_agents_content_block_request import ManagedAgentsContentBlockRequest # noqa: PLC0415
        actor = self.actor

        content: list[dict[str, Any]] | None | Unset
        if isinstance(self.content, Unset):
            content = UNSET
        elif isinstance(self.content, list):
            content = []
            for content_type_0_item_data in self.content:
                content_type_0_item = content_type_0_item_data.to_dict()
                content.append(content_type_0_item)


        else:
            content = self.content

        handoff_id = self.handoff_id

        note = self.note

        text = self.text

        type_: str | Unset = UNSET
        if not isinstance(self.type_, Unset):
            type_ = self.type_.value



        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({
        })
        if actor is not UNSET:
            field_dict["actor"] = actor
        if content is not UNSET:
            field_dict["content"] = content
        if handoff_id is not UNSET:
            field_dict["handoff_id"] = handoff_id
        if note is not UNSET:
            field_dict["note"] = note
        if text is not UNSET:
            field_dict["text"] = text
        if type_ is not UNSET:
            field_dict["type"] = type_

        return field_dict



    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.managed_agents_content_block_request import ManagedAgentsContentBlockRequest # noqa: PLC0415
        d = dict(src_dict)
        actor = d.pop("actor", UNSET)

        def _parse_content(data: object) -> list[ManagedAgentsContentBlockRequest] | None | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            try:
                if not isinstance(data, list):
                    raise TypeError()
                content_type_0 = []
                _content_type_0 = data
                for content_type_0_item_data in (_content_type_0):
                    content_type_0_item = ManagedAgentsContentBlockRequest.from_dict(content_type_0_item_data)



                    content_type_0.append(content_type_0_item)

                return content_type_0
            except (TypeError, ValueError, AttributeError, KeyError):
                pass
            return cast(list[ManagedAgentsContentBlockRequest] | None | Unset, data)

        content = _parse_content(d.pop("content", UNSET))


        handoff_id = d.pop("handoff_id", UNSET)

        note = d.pop("note", UNSET)

        text = d.pop("text", UNSET)

        _type_ = d.pop("type", UNSET)
        type_: ManagedAgentsManagedEventSendParamsType | Unset
        if isinstance(_type_,  Unset):
            type_ = UNSET
        else:
            type_ = ManagedAgentsManagedEventSendParamsType(_type_)




        managed_agents_managed_event_send_params = cls(
            actor=actor,
            content=content,
            handoff_id=handoff_id,
            note=note,
            text=text,
            type_=type_,
        )


        managed_agents_managed_event_send_params.additional_properties = d
        return managed_agents_managed_event_send_params

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
