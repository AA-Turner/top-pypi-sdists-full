from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar, BinaryIO, TextIO, TYPE_CHECKING, Generator

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

from ..models.managed_agents_hmac_custom_event_source_request_type import ManagedAgentsHmacCustomEventSourceRequestType
from typing import cast

if TYPE_CHECKING:
  from ..models.managed_agents_hmac_webhook_delivery_request import ManagedAgentsHmacWebhookDeliveryRequest





T = TypeVar("T", bound="ManagedAgentsHmacCustomEventSourceRequest")



@_attrs_define
class ManagedAgentsHmacCustomEventSourceRequest:
    """ Closed custom-webhook configuration that verifies HMAC-SHA256 signatures.

        Example:
            {'delivery': {'kind': 'webhook', 'verification': {'signatureHeader': 'example', 'signaturePrefix': 'example',
                'signedParts': [{'kind': 'body'}], 'type': 'hmac_sha256', 'verificationCredential': {'credentialId':
                '9f8b1c2d-3e4f-5a6b-7c8d-9e0f1a2b3c4d', 'vaultId': '9f8b1c2d-3e4f-5a6b-7c8d-9e0f1a2b3c4d'}}}, 'displayName':
                'example', 'type': 'custom_webhook'}

        Attributes:
            delivery (ManagedAgentsHmacWebhookDeliveryRequest): Custom webhook delivery authenticated by HMAC-SHA256.
                Example: {'kind': 'webhook', 'verification': {'signatureHeader': 'example', 'signaturePrefix': 'example',
                'signedParts': [{'kind': 'body'}], 'type': 'hmac_sha256', 'verificationCredential': {'credentialId':
                '9f8b1c2d-3e4f-5a6b-7c8d-9e0f1a2b3c4d', 'vaultId': '9f8b1c2d-3e4f-5a6b-7c8d-9e0f1a2b3c4d'}}}.
            display_name (str): Human-readable source name shown in the automation catalog.
            type_ (ManagedAgentsHmacCustomEventSourceRequestType): Custom webhook protocol.
     """

    delivery: ManagedAgentsHmacWebhookDeliveryRequest
    display_name: str
    type_: ManagedAgentsHmacCustomEventSourceRequestType





    def to_dict(self) -> dict[str, Any]:
        from ..models.managed_agents_hmac_webhook_delivery_request import ManagedAgentsHmacWebhookDeliveryRequest # noqa: PLC0415
        delivery = self.delivery.to_dict()

        display_name = self.display_name

        type_ = self.type_.value


        field_dict: dict[str, Any] = {}

        field_dict.update({
            "delivery": delivery,
            "displayName": display_name,
            "type": type_,
        })

        return field_dict



    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.managed_agents_hmac_webhook_delivery_request import ManagedAgentsHmacWebhookDeliveryRequest # noqa: PLC0415
        d = dict(src_dict)
        delivery = ManagedAgentsHmacWebhookDeliveryRequest.from_dict(d.pop("delivery"))




        display_name = d.pop("displayName")

        type_ = ManagedAgentsHmacCustomEventSourceRequestType(d.pop("type"))




        managed_agents_hmac_custom_event_source_request = cls(
            delivery=delivery,
            display_name=display_name,
            type_=type_,
        )

        return managed_agents_hmac_custom_event_source_request

