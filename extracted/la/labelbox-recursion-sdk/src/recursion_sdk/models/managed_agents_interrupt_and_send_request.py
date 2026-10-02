from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar, BinaryIO, TextIO, TYPE_CHECKING, Generator

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

from ..types import UNSET, Unset
from typing import cast

if TYPE_CHECKING:
  from ..models.managed_agents_content_block_request import ManagedAgentsContentBlockRequest





T = TypeVar("T", bound="ManagedAgentsInterruptAndSendRequest")



@_attrs_define
class ManagedAgentsInterruptAndSendRequest:
    """ Request body for interrupting the active operation and starting a fresh turn with one replacement instruction.

        Example:
            {'content': [{'byte_size': 1, 'content': [], 'context': 'example', 'data': 'example', 'encrypted_content':
                'example', 'height': 1, 'id': '9f8b1c2d-3e4f-5a6b-7c8d-9e0f1a2b3c4d', 'input': {'key': 'example'}, 'is_error':
                True, 'media_type': 'example', 'name': 'example-name', 'omitted_bytes': 1, 'payload': 'example', 'provider':
                'example', 'provider_payload': 'example', 'redacted': True, 'semantic_hint': 'example', 'sha256': 'example',
                'signature': 'example', 'source': {'file_id': '9f8b1c2d-3e4f-5a6b-7c8d-9e0f1a2b3c4d', 'type': 'file'},
                'summary': [], 'text': 'example', 'title': 'example', 'tool_use_id': '9f8b1c2d-3e4f-5a6b-7c8d-9e0f1a2b3c4d',
                'type': 'example', 'uri': 'example', 'url': 'https://example.com', 'url_expires_at': '2026-02-18T09:30:00Z',
                'width': 1}], 'message': 'example', 'referenced_session_ids': ['example']}

        Attributes:
            content (list[ManagedAgentsContentBlockRequest] | None | Unset): Provider-shaped replacement instruction blocks,
                passed through verbatim, except that a top-level image or document block may name a file from the organization's
                catalog with source {type: file, file_id}, resolved exactly as on sendSessionEvents; a refusal names the block
                as content[j]. Takes precedence over message.
            message (str | Unset): Replacement instruction for the fresh turn. Ignored when content is present.
            referenced_session_ids (list[str] | Unset): Prior sessions this session may read from the fresh turn on, by
                session id, added to any it already has. Authorized and recorded before the interrupt is signaled, so
                redirecting the agent at an earlier run is one request rather than two.
     """

    content: list[ManagedAgentsContentBlockRequest] | None | Unset = UNSET
    message: str | Unset = UNSET
    referenced_session_ids: list[str] | Unset = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)





    def to_dict(self) -> dict[str, Any]:
        from ..models.managed_agents_content_block_request import ManagedAgentsContentBlockRequest # noqa: PLC0415
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

        message = self.message

        referenced_session_ids: list[str] | Unset = UNSET
        if not isinstance(self.referenced_session_ids, Unset):
            referenced_session_ids = self.referenced_session_ids




        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({
        })
        if content is not UNSET:
            field_dict["content"] = content
        if message is not UNSET:
            field_dict["message"] = message
        if referenced_session_ids is not UNSET:
            field_dict["referenced_session_ids"] = referenced_session_ids

        return field_dict



    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.managed_agents_content_block_request import ManagedAgentsContentBlockRequest # noqa: PLC0415
        d = dict(src_dict)
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


        message = d.pop("message", UNSET)

        referenced_session_ids = cast(list[str], d.pop("referenced_session_ids", UNSET))


        managed_agents_interrupt_and_send_request = cls(
            content=content,
            message=message,
            referenced_session_ids=referenced_session_ids,
        )


        managed_agents_interrupt_and_send_request.additional_properties = d
        return managed_agents_interrupt_and_send_request

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
