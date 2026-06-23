from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar, TYPE_CHECKING

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset


if TYPE_CHECKING:
    from ..models.forwarder_delivery import ForwarderDelivery


T = TypeVar("T", bound="ForwarderDeliveryResource")


@_attrs_define
class ForwarderDeliveryResource:
    """JSON:API resource envelope for a forwarder delivery log entry.

    Example:
        {'attributes': {'attempt_number': 1, 'created_at': '2026-05-07T12:00:01.234Z', 'environment': 'production',
            'event': '33333333-4444-5555-6666-777777777777', 'forwarder': '11111111-2222-3333-4444-555555555555',
            'latency_ms': 187, 'request': {'body': '{"event_type":"user.created","resource_id":"u-1"}', 'headers': {'DD-API-
            KEY': '<redacted>'}, 'method': 'POST', 'url': 'https://http-intake.logs.datadoghq.com/api/v2/logs'},
            'response_body': '', 'response_status': 202, 'status': 'SUCCEEDED'}, 'id':
            '22222222-3333-4444-5555-666666666666', 'type': 'forwarder_delivery'}

    Attributes:
        id (str):
        attributes (ForwarderDelivery): A log entry for one attempt to deliver an event to a forwarder.
        type_ (str | Unset):  Default: 'forwarder_delivery'.
    """

    id: str
    attributes: ForwarderDelivery
    type_: str | Unset = "forwarder_delivery"
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        id = self.id

        attributes = self.attributes.to_dict()

        type_ = self.type_

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "id": id,
                "attributes": attributes,
            }
        )
        if type_ is not UNSET:
            field_dict["type"] = type_

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.forwarder_delivery import ForwarderDelivery

        d = dict(src_dict)
        id = d.pop("id")

        attributes = ForwarderDelivery.from_dict(d.pop("attributes"))

        type_ = d.pop("type", UNSET)

        forwarder_delivery_resource = cls(
            id=id,
            attributes=attributes,
            type_=type_,
        )

        forwarder_delivery_resource.additional_properties = d
        return forwarder_delivery_resource

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
