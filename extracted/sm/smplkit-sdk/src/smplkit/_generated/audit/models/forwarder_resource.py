from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar, TYPE_CHECKING

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

from typing import cast

if TYPE_CHECKING:
    from ..models.forwarder import Forwarder


T = TypeVar("T", bound="ForwarderResource")


@_attrs_define
class ForwarderResource:
    r"""JSON:API resource envelope for a forwarder.

    The caller supplies `id` (the forwarder's key) on create.

        Example:
            {'attributes': {'configuration': {'headers': [{'name': 'Content-Type', 'value': 'application/json'}, {'name':
                'DD-API-KEY', 'value': 'dd-api-key-plaintext'}], 'method': 'POST', 'success_status': '2xx', 'url':
                'https://http-intake.logs.datadoghq.com/api/v2/logs'}, 'created_at': '2026-05-07T12:00:00Z', 'description':
                'Forwards user.* events to the prod Datadog tenant.', 'enabled': False, 'environments': {'production':
                {'enabled': True}}, 'filter': {'==': [{'var': 'event_type'}, 'user.created']}, 'forwarder_type': 'datadog',
                'name': 'Datadog production', 'transform': '{ "message": event_type & \' on \' & resource_type }',
                'transform_type': 'JSONATA', 'updated_at': '2026-05-07T12:00:00Z', 'version': 1}, 'id': 'datadog-prod', 'type':
                'forwarder'}

        Attributes:
            attributes (Forwarder): A destination that receives audit events recorded for the account.

                Each event recorded for the account is evaluated against every enabled
                forwarder. If the filter expression evaluates truthy — or is absent —
                the event is shaped by the configured transform and delivered to the
                destination defined by ``configuration``.
            id (None | str | Unset):
            type_ (str | Unset):  Default: 'forwarder'.
    """

    attributes: Forwarder
    id: None | str | Unset = UNSET
    type_: str | Unset = "forwarder"
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
        from ..models.forwarder import Forwarder

        d = dict(src_dict)
        attributes = Forwarder.from_dict(d.pop("attributes"))

        def _parse_id(data: object) -> None | str | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(None | str | Unset, data)

        id = _parse_id(d.pop("id", UNSET))

        type_ = d.pop("type", UNSET)

        forwarder_resource = cls(
            attributes=attributes,
            id=id,
            type_=type_,
        )

        forwarder_resource.additional_properties = d
        return forwarder_resource

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
