from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar, TYPE_CHECKING

from attrs import define as _attrs_define
from attrs import field as _attrs_field


if TYPE_CHECKING:
    from ..models.forwarder_type_resource import ForwarderTypeResource


T = TypeVar("T", bound="ForwarderTypeResponse")


@_attrs_define
class ForwarderTypeResponse:
    """JSON:API single-resource response for a forwarder type.

    Attributes:
        data (ForwarderTypeResource): JSON:API resource envelope for a forwarder type. Example: {'attributes':
            {'base_type': 'HTTP', 'configuration': {'headers': [{'name': 'Content-Type', 'value': 'application/json'},
            {'name': 'DD-API-KEY', 'value': '{api_key}'}], 'method': 'POST', 'success_status': '2xx', 'url': 'https://http-
            intake.logs.datadoghq.com/api/v2/logs'}, 'docs_url': 'https://docs.datadoghq.com/api/latest/logs/', 'icon':
            'https://audit.smplkit.com/api/v1/forwarder_types/datadog.svg', 'is_custom': False, 'name': 'Datadog Logs',
            'placeholders': {'api_key': {'label': 'Datadog API key', 'secret': True}}, 'transform': {'default': '{
            "ddsource": "smplkit", "message": event_type }', 'type': 'JSONATA'}}, 'id': 'datadog', 'type':
            'forwarder_type'}.
    """

    data: ForwarderTypeResource
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
        from ..models.forwarder_type_resource import ForwarderTypeResource

        d = dict(src_dict)
        data = ForwarderTypeResource.from_dict(d.pop("data"))

        forwarder_type_response = cls(
            data=data,
        )

        forwarder_type_response.additional_properties = d
        return forwarder_type_response

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
