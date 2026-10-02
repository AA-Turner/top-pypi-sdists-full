from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar, BinaryIO, TextIO, TYPE_CHECKING, Generator

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

from ..models.managed_agents_event_source_response_status import ManagedAgentsEventSourceResponseStatus
from ..models.managed_agents_event_source_response_type import ManagedAgentsEventSourceResponseType
from typing import cast
from uuid import UUID
import datetime

if TYPE_CHECKING:
  from ..models.managed_agents_integration_event_source_delivery import ManagedAgentsIntegrationEventSourceDelivery
  from ..models.managed_agents_webhook_event_source_delivery import ManagedAgentsWebhookEventSourceDelivery





T = TypeVar("T", bound="ManagedAgentsEventSourceResponse")



@_attrs_define
class ManagedAgentsEventSourceResponse:
    """ Configured inbound event source, including its verification policy and lifecycle state.

        Example:
            {'createdAt': '2026-02-18T09:30:00Z', 'delivery': {'kind': 'webhook', 'verification': {'signatureHeader':
                'example', 'signaturePrefix': 'example', 'signedParts': [{'kind': 'body'}], 'type': 'none',
                'verificationCredential': {'credentialId': '9f8b1c2d-3e4f-5a6b-7c8d-9e0f1a2b3c4d', 'vaultId':
                '9f8b1c2d-3e4f-5a6b-7c8d-9e0f1a2b3c4d'}}, 'verificationCredential': {'credentialId':
                '9f8b1c2d-3e4f-5a6b-7c8d-9e0f1a2b3c4d', 'vaultId': '9f8b1c2d-3e4f-5a6b-7c8d-9e0f1a2b3c4d'}, 'webhookUrl':
                'example'}, 'displayName': 'example', 'eventSourceId': '9f8b1c2d-3e4f-5a6b-7c8d-9e0f1a2b3c4d', 'revision': 1,
                'status': 'paused', 'type': 'slack_events_api', 'updatedAt': '2026-02-18T09:30:00Z'}

        Attributes:
            created_at (datetime.datetime): Time the event source was created.
            delivery (ManagedAgentsIntegrationEventSourceDelivery | ManagedAgentsWebhookEventSourceDelivery): Delivery
                identity: a customer webhook or an integration connection. Example: {'kind': 'webhook', 'verification':
                {'signatureHeader': 'example', 'signaturePrefix': 'example', 'signedParts': [{'kind': 'body'}], 'type': 'none',
                'verificationCredential': {'credentialId': '9f8b1c2d-3e4f-5a6b-7c8d-9e0f1a2b3c4d', 'vaultId':
                '9f8b1c2d-3e4f-5a6b-7c8d-9e0f1a2b3c4d'}}, 'verificationCredential': {'credentialId':
                '9f8b1c2d-3e4f-5a6b-7c8d-9e0f1a2b3c4d', 'vaultId': '9f8b1c2d-3e4f-5a6b-7c8d-9e0f1a2b3c4d'}, 'webhookUrl':
                'example'}.
            display_name (str): Human-readable source name shown in the automation catalog.
            event_source_id (UUID): Stable identifier for the event source.
            revision (int): Monotonic revision represented by the response ETag.
            status (ManagedAgentsEventSourceResponseStatus): Lifecycle state. Custom webhook sources start paused;
                connection-managed sources start active.
            type_ (ManagedAgentsEventSourceResponseType): Inbound provider protocol interpreted by this source.
            updated_at (datetime.datetime): Time the event source was last changed.
     """

    created_at: datetime.datetime
    delivery: ManagedAgentsIntegrationEventSourceDelivery | ManagedAgentsWebhookEventSourceDelivery
    display_name: str
    event_source_id: UUID
    revision: int
    status: ManagedAgentsEventSourceResponseStatus
    type_: ManagedAgentsEventSourceResponseType
    updated_at: datetime.datetime





    def to_dict(self) -> dict[str, Any]:
        from ..models.managed_agents_integration_event_source_delivery import ManagedAgentsIntegrationEventSourceDelivery # noqa: PLC0415
        from ..models.managed_agents_webhook_event_source_delivery import ManagedAgentsWebhookEventSourceDelivery # noqa: PLC0415
        created_at = self.created_at.isoformat()

        delivery: dict[str, Any]
        if isinstance(self.delivery, ManagedAgentsWebhookEventSourceDelivery):
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
        from ..models.managed_agents_webhook_event_source_delivery import ManagedAgentsWebhookEventSourceDelivery # noqa: PLC0415
        d = dict(src_dict)
        created_at = datetime.datetime.fromisoformat(d.pop("createdAt"))




        def _parse_delivery(data: object) -> ManagedAgentsIntegrationEventSourceDelivery | ManagedAgentsWebhookEventSourceDelivery:
            try:
                if not isinstance(data, dict):
                    raise TypeError()
                componentsschemas_managed_agents_event_source_delivery_type_0 = ManagedAgentsWebhookEventSourceDelivery.from_dict(data)



                return componentsschemas_managed_agents_event_source_delivery_type_0
            except (TypeError, ValueError, AttributeError, KeyError):
                pass
            if not isinstance(data, dict):
                raise TypeError()
            componentsschemas_managed_agents_event_source_delivery_type_1 = ManagedAgentsIntegrationEventSourceDelivery.from_dict(data)



            return componentsschemas_managed_agents_event_source_delivery_type_1

        delivery = _parse_delivery(d.pop("delivery"))


        display_name = d.pop("displayName")

        event_source_id = UUID(d.pop("eventSourceId"))




        revision = d.pop("revision")

        status = ManagedAgentsEventSourceResponseStatus(d.pop("status"))




        type_ = ManagedAgentsEventSourceResponseType(d.pop("type"))




        updated_at = datetime.datetime.fromisoformat(d.pop("updatedAt"))




        managed_agents_event_source_response = cls(
            created_at=created_at,
            delivery=delivery,
            display_name=display_name,
            event_source_id=event_source_id,
            revision=revision,
            status=status,
            type_=type_,
            updated_at=updated_at,
        )

        return managed_agents_event_source_response

