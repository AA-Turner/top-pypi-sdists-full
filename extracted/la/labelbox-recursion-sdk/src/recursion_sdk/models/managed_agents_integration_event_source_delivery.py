from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar, BinaryIO, TextIO, TYPE_CHECKING, Generator

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

from ..models.managed_agents_integration_event_source_delivery_kind import ManagedAgentsIntegrationEventSourceDeliveryKind
from uuid import UUID






T = TypeVar("T", bound="ManagedAgentsIntegrationEventSourceDelivery")



@_attrs_define
class ManagedAgentsIntegrationEventSourceDelivery:
    """ Connection-managed delivery; no customer webhook or verification credential is required.

        Example:
            {'connectionId': '9f8b1c2d-3e4f-5a6b-7c8d-9e0f1a2b3c4d', 'kind': 'integration'}

        Attributes:
            connection_id (UUID): Owning integration connection in the same workspace.
            kind (ManagedAgentsIntegrationEventSourceDeliveryKind): Delivery through the platform integration callback.
     """

    connection_id: UUID
    kind: ManagedAgentsIntegrationEventSourceDeliveryKind





    def to_dict(self) -> dict[str, Any]:
        connection_id = str(self.connection_id)

        kind = self.kind.value


        field_dict: dict[str, Any] = {}

        field_dict.update({
            "connectionId": connection_id,
            "kind": kind,
        })

        return field_dict



    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        connection_id = UUID(d.pop("connectionId"))




        kind = ManagedAgentsIntegrationEventSourceDeliveryKind(d.pop("kind"))




        managed_agents_integration_event_source_delivery = cls(
            connection_id=connection_id,
            kind=kind,
        )

        return managed_agents_integration_event_source_delivery

