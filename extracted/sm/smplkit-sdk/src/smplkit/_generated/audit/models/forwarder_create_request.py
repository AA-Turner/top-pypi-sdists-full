from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar, TYPE_CHECKING

from attrs import define as _attrs_define
from attrs import field as _attrs_field


if TYPE_CHECKING:
    from ..models.forwarder_create_resource import ForwarderCreateResource


T = TypeVar("T", bound="ForwarderCreateRequest")


@_attrs_define
class ForwarderCreateRequest:
    r"""JSON:API request envelope for creating a forwarder.

    Distinct from :class:`ForwarderRequest` because create requires
    caller-supplied ``data.id`` while update does not.

        Attributes:
            data (ForwarderCreateResource): JSON:API resource envelope for creating a forwarder (id required). Example:
                {'attributes': {'configuration': {'headers': {'Content-Type': 'application/json', 'DD-API-KEY': 'dd-api-key-
                plaintext'}, 'method': 'POST', 'success_status': '2xx', 'url': 'https://http-
                intake.logs.datadoghq.com/api/v2/logs'}, 'description': 'Forwards user.* events to the prod Datadog tenant.',
                'environments': {'production': {'enabled': True, 'headers.DD-API-KEY': 'dd-prod-api-key-plaintext'}}, 'filter':
                {'==': [{'var': 'event_type'}, 'user.created']}, 'forward_smplkit_events': False, 'forwarder_type': 'datadog',
                'name': 'Datadog production', 'transform': '{ "message": event_type & \' on \' & resource_type }',
                'transform_type': 'JSONATA'}, 'id': 'datadog-prod', 'type': 'forwarder'}.
    """

    data: ForwarderCreateResource
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
        from ..models.forwarder_create_resource import ForwarderCreateResource

        d = dict(src_dict)
        data = ForwarderCreateResource.from_dict(d.pop("data"))

        forwarder_create_request = cls(
            data=data,
        )

        forwarder_create_request.additional_properties = d
        return forwarder_create_request

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
