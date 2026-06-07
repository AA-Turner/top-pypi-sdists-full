from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar, TYPE_CHECKING

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

from typing import cast
from typing import Literal

if TYPE_CHECKING:
    from ..models.forwarder import Forwarder


T = TypeVar("T", bound="ForwarderCreateResource")


@_attrs_define
class ForwarderCreateResource:
    r"""JSON:API resource envelope for creating a forwarder (id required).

    Example:
        {'attributes': {'configuration': {'headers': [{'name': 'Content-Type', 'value': 'application/json'}, {'name':
            'DD-API-KEY', 'value': 'dd-api-key-plaintext'}], 'method': 'POST', 'success_status': '2xx', 'url':
            'https://http-intake.logs.datadoghq.com/api/v2/logs'}, 'description': 'Forwards user.* events to the prod
            Datadog tenant.', 'environments': {'production': {'enabled': True}}, 'filter': {'==': [{'var': 'event_type'},
            'user.created']}, 'forwarder_type': 'datadog', 'name': 'Datadog production', 'transform': '{ "message":
            event_type & \' on \' & resource_type }', 'transform_type': 'JSONATA'}, 'id': 'datadog-prod', 'type':
            'forwarder'}

    Attributes:
        id (str): Client-supplied resource id.
        attributes (Forwarder): A destination that receives audit events recorded for the account.

            Each event recorded for the account is evaluated against every enabled
            forwarder. If the filter expression evaluates truthy — or is absent —
            the event is shaped by the configured transform and delivered to the
            destination defined by ``configuration``.
        type_ (Literal['forwarder'] | Unset):  Default: 'forwarder'.
    """

    id: str
    attributes: Forwarder
    type_: Literal["forwarder"] | Unset = "forwarder"
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
        from ..models.forwarder import Forwarder

        d = dict(src_dict)
        id = d.pop("id")

        attributes = Forwarder.from_dict(d.pop("attributes"))

        type_ = cast(Literal["forwarder"] | Unset, d.pop("type", UNSET))
        if type_ != "forwarder" and not isinstance(type_, Unset):
            raise ValueError(f"type must match const 'forwarder', got '{type_}'")

        forwarder_create_resource = cls(
            id=id,
            attributes=attributes,
            type_=type_,
        )

        forwarder_create_resource.additional_properties = d
        return forwarder_create_resource

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
