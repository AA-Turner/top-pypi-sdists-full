from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar, TYPE_CHECKING

from attrs import define as _attrs_define
from attrs import field as _attrs_field


if TYPE_CHECKING:
    from ..models.forwarder_resource import ForwarderResource


T = TypeVar("T", bound="ForwarderResponse")


@_attrs_define
class ForwarderResponse:
    r"""JSON:API single-resource response envelope for a forwarder.

    Attributes:
        data (ForwarderResource): JSON:API resource envelope for a forwarder.

            The caller supplies `id` (the forwarder's key) on create. Example: {'attributes': {'configuration': {'headers':
            {'Content-Type': 'application/json', 'DD-API-KEY': 'dd-api-key-plaintext'}, 'method': 'POST', 'success_status':
            '2xx', 'url': 'https://http-intake.logs.datadoghq.com/api/v2/logs'}, 'created_at': '2026-05-07T12:00:00Z',
            'description': 'Forwards user.* events to the prod Datadog tenant.', 'environments': {'production': {'enabled':
            True, 'headers.DD-API-KEY': 'dd-prod-api-key-plaintext'}}, 'filter': {'==': [{'var': 'event_type'},
            'user.created']}, 'forward_smplkit_events': False, 'forwarder_type': 'datadog', 'name': 'Datadog production',
            'transform': '{ "message": event_type & \' on \' & resource_type }', 'transform_type': 'JSONATA', 'updated_at':
            '2026-05-07T12:00:00Z', 'version': 1}, 'id': 'datadog-prod', 'type': 'forwarder'}.
    """

    data: ForwarderResource
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
        from ..models.forwarder_resource import ForwarderResource

        d = dict(src_dict)
        data = ForwarderResource.from_dict(d.pop("data"))

        forwarder_response = cls(
            data=data,
        )

        forwarder_response.additional_properties = d
        return forwarder_response

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
