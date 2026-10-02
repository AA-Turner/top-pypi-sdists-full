from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar, BinaryIO, TextIO, TYPE_CHECKING, Generator

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

from ..models.managed_agents_event_source_summary_status import ManagedAgentsEventSourceSummaryStatus
from ..models.managed_agents_event_source_summary_type import ManagedAgentsEventSourceSummaryType
from typing import cast
from uuid import UUID
import datetime

if TYPE_CHECKING:
  from ..models.managed_agents_integration_event_source_delivery import ManagedAgentsIntegrationEventSourceDelivery
  from ..models.managed_agents_webhook_event_source_delivery_summary import ManagedAgentsWebhookEventSourceDeliverySummary





T = TypeVar("T", bound="ManagedAgentsEventSourceSummary")



@_attrs_define
class ManagedAgentsEventSourceSummary:
    """ Compact event-source representation returned by the collection endpoint.

        Example:
            {'createdAt': '2026-02-18T09:30:00Z', 'delivery': {'kind': 'webhook', 'webhookUrl': 'example'}, 'displayName':
                'example', 'eventSourceId': '9f8b1c2d-3e4f-5a6b-7c8d-9e0f1a2b3c4d', 'revision': 1, 'status': 'paused', 'type':
                'slack_events_api', 'updatedAt': '2026-02-18T09:30:00Z'}

        Attributes:
            created_at (datetime.datetime): Time the event source was created.
            delivery (ManagedAgentsIntegrationEventSourceDelivery | ManagedAgentsWebhookEventSourceDeliverySummary):
                Delivery identity without member-only verification configuration. Example: {'kind': 'webhook', 'webhookUrl':
                'example'}.
            display_name (str): Human-readable source name.
            event_source_id (UUID): Stable identifier for the event source.
            revision (int): Monotonic revision represented by the member ETag.
            status (ManagedAgentsEventSourceSummaryStatus): Current lifecycle state.
            type_ (ManagedAgentsEventSourceSummaryType): Inbound provider protocol interpreted by this source.
            updated_at (datetime.datetime): Time the event source was last changed.
     """

    created_at: datetime.datetime
    delivery: ManagedAgentsIntegrationEventSourceDelivery | ManagedAgentsWebhookEventSourceDeliverySummary
    display_name: str
    event_source_id: UUID
    revision: int
    status: ManagedAgentsEventSourceSummaryStatus
    type_: ManagedAgentsEventSourceSummaryType
    updated_at: datetime.datetime





    def to_dict(self) -> dict[str, Any]:
        from ..models.managed_agents_integration_event_source_delivery import ManagedAgentsIntegrationEventSourceDelivery # noqa: PLC0415
        from ..models.managed_agents_webhook_event_source_delivery_summary import ManagedAgentsWebhookEventSourceDeliverySummary # noqa: PLC0415
        created_at = self.created_at.isoformat()

        delivery: dict[str, Any]
        if isinstance(self.delivery, ManagedAgentsWebhookEventSourceDeliverySummary):
            delivery = self.delivery.to_dict()
        else:
            delivery = self.delivery.to_dict()


        display_name = self.display_name

        event_source_id = str(self.event_source_id)

        revision = self.revision

        status = self.status.value

        type_ = self.type_.value

        updated_at = self.updated_at.isoformat()


        field_dict: dict[str, Any] = {}

        field_dict.update({
            "createdAt": created_at,
            "delivery": delivery,
            "displayName": display_name,
            "eventSourceId": event_source_id,
            "revision": revision,
            "status": status,
            "type": type_,
            "updatedAt": updated_at,
        })

        return field_dict



    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.managed_agents_integration_event_source_delivery import ManagedAgentsIntegrationEventSourceDelivery # noqa: PLC0415
        from ..models.managed_agents_webhook_event_source_delivery_summary import ManagedAgentsWebhookEventSourceDeliverySummary # noqa: PLC0415
        d = dict(src_dict)
        created_at = datetime.datetime.fromisoformat(d.pop("createdAt"))




        def _parse_delivery(data: object) -> ManagedAgentsIntegrationEventSourceDelivery | ManagedAgentsWebhookEventSourceDeliverySummary:
            try:
                if not isinstance(data, dict):
                    raise TypeError()
                componentsschemas_managed_agents_event_source_delivery_summary_type_0 = ManagedAgentsWebhookEventSourceDeliverySummary.from_dict(data)



                return componentsschemas_managed_agents_event_source_delivery_summary_type_0
            except (TypeError, ValueError, AttributeError, KeyError):
                pass
            if not isinstance(data, dict):
                raise TypeError()
            componentsschemas_managed_agents_event_source_delivery_summary_type_1 = ManagedAgentsIntegrationEventSourceDelivery.from_dict(data)



            return componentsschemas_managed_agents_event_source_delivery_summary_type_1

        delivery = _parse_delivery(d.pop("delivery"))


        display_name = d.pop("displayName")

        event_source_id = UUID(d.pop("eventSourceId"))




        revision = d.pop("revision")

        status = ManagedAgentsEventSourceSummaryStatus(d.pop("status"))




        type_ = ManagedAgentsEventSourceSummaryType(d.pop("type"))




        updated_at = datetime.datetime.fromisoformat(d.pop("updatedAt"))




        managed_agents_event_source_summary = cls(
            created_at=created_at,
            delivery=delivery,
            display_name=display_name,
            event_source_id=event_source_id,
            revision=revision,
            status=status,
            type_=type_,
            updated_at=updated_at,
        )

        return managed_agents_event_source_summary

