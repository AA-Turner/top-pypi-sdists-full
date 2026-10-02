from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar, BinaryIO, TextIO, TYPE_CHECKING, Generator

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

from ..models.managed_agents_event_source_status_response_health import ManagedAgentsEventSourceStatusResponseHealth
from typing import cast
from uuid import UUID

if TYPE_CHECKING:
  from ..models.managed_agents_event_source_last_delivery_response_type_0 import ManagedAgentsEventSourceLastDeliveryResponseType0





T = TypeVar("T", bound="ManagedAgentsEventSourceStatusResponse")



@_attrs_define
class ManagedAgentsEventSourceStatusResponse:
    """ Operational status for one event source without secret material.

        Example:
            {'eventSourceId': '9f8b1c2d-3e4f-5a6b-7c8d-9e0f1a2b3c4d', 'health': 'never_received', 'lastDelivery':
                {'disposition': 'admitted', 'receivedAt': '2026-02-18T09:30:00Z'}, 'triggerCount': 1}

        Attributes:
            event_source_id (UUID): Stable identifier for the event source.
            health (ManagedAgentsEventSourceStatusResponseHealth): Current source availability and receipt history.
                setup_required means the connected installation lacks event permissions; approve the App permission update and
                probe the connection. healthy means a receipt exists, not proof of current provider reachability.
            last_delivery (ManagedAgentsEventSourceLastDeliveryResponseType0 | None): Most recent verified delivery observed
                for the source. Example: {'disposition': 'admitted', 'receivedAt': '2026-02-18T09:30:00Z'}.
            trigger_count (int): Automations currently bound to this event source.
     """

    event_source_id: UUID
    health: ManagedAgentsEventSourceStatusResponseHealth
    last_delivery: ManagedAgentsEventSourceLastDeliveryResponseType0 | None
    trigger_count: int





    def to_dict(self) -> dict[str, Any]:
        from ..models.managed_agents_event_source_last_delivery_response_type_0 import ManagedAgentsEventSourceLastDeliveryResponseType0 # noqa: PLC0415
        event_source_id = str(self.event_source_id)

        health = self.health.value

        last_delivery: dict[str, Any] | None
        if isinstance(self.last_delivery, ManagedAgentsEventSourceLastDeliveryResponseType0):
            last_delivery = self.last_delivery.to_dict()
        else:
            last_delivery = self.last_delivery

        trigger_count = self.trigger_count


        field_dict: dict[str, Any] = {}

        field_dict.update({
            "eventSourceId": event_source_id,
            "health": health,
            "lastDelivery": last_delivery,
            "triggerCount": trigger_count,
        })

        return field_dict



    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.managed_agents_event_source_last_delivery_response_type_0 import ManagedAgentsEventSourceLastDeliveryResponseType0 # noqa: PLC0415
        d = dict(src_dict)
        event_source_id = UUID(d.pop("eventSourceId"))




        health = ManagedAgentsEventSourceStatusResponseHealth(d.pop("health"))




        def _parse_last_delivery(data: object) -> ManagedAgentsEventSourceLastDeliveryResponseType0 | None:
            if data is None:
                return data
            try:
                if not isinstance(data, dict):
                    raise TypeError()
                componentsschemas_managed_agents_event_source_last_delivery_response_type_0 = ManagedAgentsEventSourceLastDeliveryResponseType0.from_dict(data)



                return componentsschemas_managed_agents_event_source_last_delivery_response_type_0
            except (TypeError, ValueError, AttributeError, KeyError):
                pass
            return cast(ManagedAgentsEventSourceLastDeliveryResponseType0 | None, data)

        last_delivery = _parse_last_delivery(d.pop("lastDelivery"))


        trigger_count = d.pop("triggerCount")

        managed_agents_event_source_status_response = cls(
            event_source_id=event_source_id,
            health=health,
            last_delivery=last_delivery,
            trigger_count=trigger_count,
        )

        return managed_agents_event_source_status_response

