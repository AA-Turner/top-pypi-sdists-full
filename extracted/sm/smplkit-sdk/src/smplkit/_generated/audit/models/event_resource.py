from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar, TYPE_CHECKING

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

from typing import cast

if TYPE_CHECKING:
    from ..models.event import Event


T = TypeVar("T", bound="EventResource")


@_attrs_define
class EventResource:
    """JSON:API resource envelope for an audit event.

    `id` must not be specified for create requests (the server assigns it).

        Example:
            {'attributes': {'actor_id': 'aaaaaaaa-bbbb-cccc-dddd-eeeeeeeeeeee', 'actor_label': 'alice@example.com',
                'actor_type': 'USER', 'category': 'auth', 'created_at': '2026-05-06T20:00:00.123Z', 'data': {'request_id': 'req-
                abc', 'snapshot': {'email': 'alice@example.com'}}, 'description': 'Alice signed up via the marketing site.',
                'do_not_forward': False, 'environment': 'production', 'event_type': 'user.created', 'idempotency_key':
                'auto-1234abcd', 'occurred_at': '2026-05-06T20:00:00Z', 'resource_id': 'u-1', 'resource_type': 'user',
                'severity': 'INFO'}, 'id': '11111111-2222-3333-4444-555555555555', 'type': 'event'}

        Attributes:
            attributes (Event): An audit event — a record that something happened, attributed to
                an actor and a resource.

                When recording a snapshot of the resource at the time of the event,
                place it inside `data`. smplkit's own integrations nest it under
                `data.snapshot`, but the slot is yours to use however you like.
            id (None | str | Unset):
            type_ (str | Unset):  Default: 'event'.
    """

    attributes: Event
    id: None | str | Unset = UNSET
    type_: str | Unset = "event"
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        attributes = self.attributes.to_dict()

        id: None | str | Unset
        if isinstance(self.id, Unset):
            id = UNSET
        else:
            id = self.id

        type_ = self.type_

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "attributes": attributes,
            }
        )
        if id is not UNSET:
            field_dict["id"] = id
        if type_ is not UNSET:
            field_dict["type"] = type_

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.event import Event

        d = dict(src_dict)
        attributes = Event.from_dict(d.pop("attributes"))

        def _parse_id(data: object) -> None | str | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(None | str | Unset, data)

        id = _parse_id(d.pop("id", UNSET))

        type_ = d.pop("type", UNSET)

        event_resource = cls(
            attributes=attributes,
            id=id,
            type_=type_,
        )

        event_resource.additional_properties = d
        return event_resource

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
