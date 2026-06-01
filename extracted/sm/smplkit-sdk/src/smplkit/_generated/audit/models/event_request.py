from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar, TYPE_CHECKING

from attrs import define as _attrs_define
from attrs import field as _attrs_field


if TYPE_CHECKING:
    from ..models.event_resource import EventResource


T = TypeVar("T", bound="EventRequest")


@_attrs_define
class EventRequest:
    """JSON:API request envelope for recording an audit event.

    Attributes:
        data (EventResource): JSON:API resource envelope for an audit event.

            `id` must not be specified for create requests (the server assigns it). Example: {'attributes': {'actor_id':
            'aaaaaaaa-bbbb-cccc-dddd-eeeeeeeeeeee', 'actor_label': 'alice@example.com', 'actor_type': 'USER', 'category':
            'auth', 'created_at': '2026-05-06T20:00:00.123Z', 'data': {'request_id': 'req-abc', 'snapshot': {'email':
            'alice@example.com'}}, 'description': 'Alice signed up via the marketing site.', 'do_not_forward': False,
            'event_type': 'user.created', 'idempotency_key': 'auto-1234abcd', 'occurred_at': '2026-05-06T20:00:00Z',
            'resource_id': 'u-1', 'resource_type': 'user', 'severity': 'INFO'}, 'id':
            '11111111-2222-3333-4444-555555555555', 'type': 'event'}.
    """

    data: EventResource
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        data = self.data.to_dict()

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "data": data,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.event_resource import EventResource

        d = dict(src_dict)
        data = EventResource.from_dict(d.pop("data"))

        event_request = cls(
            data=data,
        )

        event_request.additional_properties = d
        return event_request

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
