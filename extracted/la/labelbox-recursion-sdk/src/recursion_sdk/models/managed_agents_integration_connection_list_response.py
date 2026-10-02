from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar, BinaryIO, TextIO, TYPE_CHECKING, Generator

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

from typing import cast

if TYPE_CHECKING:
  from ..models.managed_agents_integration_connection import ManagedAgentsIntegrationConnection





T = TypeVar("T", bound="ManagedAgentsIntegrationConnectionListResponse")



@_attrs_define
class ManagedAgentsIntegrationConnectionListResponse:
    """ The integration connections belonging to the calling organization, as resolved from the API key. Returned when
    listing connections.

        Example:
            {'connections': [{'account_login': 'example', 'account_type': 'example', 'connected_by': 'example',
                'connection_id': '9f8b1c2d-3e4f-5a6b-7c8d-9e0f1a2b3c4d', 'created_at': '2026-02-18T09:30:00Z', 'external_id':
                '9f8b1c2d-3e4f-5a6b-7c8d-9e0f1a2b3c4d', 'organization_id': '9f8b1c2d-3e4f-5a6b-7c8d-9e0f1a2b3c4d',
                'permissions': {'key': 'example'}, 'provider': 'example', 'resource_selection': 'example', 'state': 'example',
                'updated_at': '2026-02-18T09:30:00Z', 'usage': {'agents': 1, 'automations': 1}}]}

        Attributes:
            connections (list[ManagedAgentsIntegrationConnection] | None): The organization's integration connections,
                including pending (registered, trust not yet proved), suspended, and revoked ones. Disconnected connections are
                omitted.
     """

    connections: list[ManagedAgentsIntegrationConnection] | None
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)





    def to_dict(self) -> dict[str, Any]:
        from ..models.managed_agents_integration_connection import ManagedAgentsIntegrationConnection # noqa: PLC0415
        connections: list[dict[str, Any]] | None
        if isinstance(self.connections, list):
            connections = []
            for connections_type_0_item_data in self.connections:
                connections_type_0_item = connections_type_0_item_data.to_dict()
                connections.append(connections_type_0_item)


        else:
            connections = self.connections


        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({
            "connections": connections,
        })

        return field_dict



    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.managed_agents_integration_connection import ManagedAgentsIntegrationConnection # noqa: PLC0415
        d = dict(src_dict)
        def _parse_connections(data: object) -> list[ManagedAgentsIntegrationConnection] | None:
            if data is None:
                return data
            try:
                if not isinstance(data, list):
                    raise TypeError()
                connections_type_0 = []
                _connections_type_0 = data
                for connections_type_0_item_data in (_connections_type_0):
                    connections_type_0_item = ManagedAgentsIntegrationConnection.from_dict(connections_type_0_item_data)



                    connections_type_0.append(connections_type_0_item)

                return connections_type_0
            except (TypeError, ValueError, AttributeError, KeyError):
                pass
            return cast(list[ManagedAgentsIntegrationConnection] | None, data)

        connections = _parse_connections(d.pop("connections"))


        managed_agents_integration_connection_list_response = cls(
            connections=connections,
        )


        managed_agents_integration_connection_list_response.additional_properties = d
        return managed_agents_integration_connection_list_response

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
