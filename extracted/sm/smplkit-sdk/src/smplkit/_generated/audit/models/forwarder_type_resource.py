from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar, TYPE_CHECKING

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset


if TYPE_CHECKING:
    from ..models.forwarder_type_attributes import ForwarderTypeAttributes


T = TypeVar("T", bound="ForwarderTypeResource")


@_attrs_define
class ForwarderTypeResource:
    """JSON:API resource envelope for a forwarder type.

    Example:
        {'attributes': {'base_type': 'HTTP', 'configuration': {'headers': [{'name': 'Content-Type', 'value':
            'application/json'}, {'name': 'DD-API-KEY', 'value': '{api_key}'}], 'method': 'POST', 'success_status': '2xx',
            'url': 'https://http-intake.logs.datadoghq.com/api/v2/logs'}, 'docs_url':
            'https://docs.datadoghq.com/api/latest/logs/', 'icon':
            'https://audit.smplkit.com/api/v1/forwarder_types/datadog.svg', 'is_custom': False, 'name': 'Datadog Logs',
            'placeholders': {'api_key': {'label': 'Datadog API key', 'secret': True}}, 'transform': {'default': '{
            "ddsource": "smplkit", "message": event_type }', 'type': 'JSONATA'}}, 'id': 'datadog', 'type': 'forwarder_type'}

    Attributes:
        id (str): Lowercase forwarder type id — matches `forwarder.forwarder_type` values and is the filename stem of
            `forwarder_types/<id>.yaml`.
        attributes (ForwarderTypeAttributes): The catalog entry's attributes — one branded forwarder type or the
            synthetic Custom HTTP entry.
        type_ (str | Unset):  Default: 'forwarder_type'.
    """

    id: str
    attributes: ForwarderTypeAttributes
    type_: str | Unset = "forwarder_type"
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
        from ..models.forwarder_type_attributes import ForwarderTypeAttributes

        d = dict(src_dict)
        id = d.pop("id")

        attributes = ForwarderTypeAttributes.from_dict(d.pop("attributes"))

        type_ = d.pop("type", UNSET)

        forwarder_type_resource = cls(
            id=id,
            attributes=attributes,
            type_=type_,
        )

        forwarder_type_resource.additional_properties = d
        return forwarder_type_resource

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
