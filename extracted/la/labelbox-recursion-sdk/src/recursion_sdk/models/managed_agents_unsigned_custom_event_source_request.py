from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar, BinaryIO, TextIO, TYPE_CHECKING, Generator

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

from ..models.managed_agents_unsigned_custom_event_source_request_type import ManagedAgentsUnsignedCustomEventSourceRequestType
from typing import cast

if TYPE_CHECKING:
  from ..models.managed_agents_unsigned_webhook_delivery_request import ManagedAgentsUnsignedWebhookDeliveryRequest





T = TypeVar("T", bound="ManagedAgentsUnsignedCustomEventSourceRequest")



@_attrs_define
class ManagedAgentsUnsignedCustomEventSourceRequest:
    """ Closed custom-webhook configuration that explicitly accepts unsigned deliveries.

        Example:
            {'delivery': {'kind': 'webhook', 'verification': {'type': 'none'}}, 'displayName': 'example', 'type':
                'custom_webhook'}

        Attributes:
            delivery (ManagedAgentsUnsignedWebhookDeliveryRequest): Custom webhook delivery without cryptographic
                verification. Example: {'kind': 'webhook', 'verification': {'type': 'none'}}.
            display_name (str): Human-readable source name shown in the automation catalog.
            type_ (ManagedAgentsUnsignedCustomEventSourceRequestType): Custom webhook protocol.
     """

    delivery: ManagedAgentsUnsignedWebhookDeliveryRequest
    display_name: str
    type_: ManagedAgentsUnsignedCustomEventSourceRequestType





    def to_dict(self) -> dict[str, Any]:
        from ..models.managed_agents_unsigned_webhook_delivery_request import ManagedAgentsUnsignedWebhookDeliveryRequest # noqa: PLC0415
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
        from ..models.managed_agents_unsigned_webhook_delivery_request import ManagedAgentsUnsignedWebhookDeliveryRequest # noqa: PLC0415
        d = dict(src_dict)
        delivery = ManagedAgentsUnsignedWebhookDeliveryRequest.from_dict(d.pop("delivery"))




        display_name = d.pop("displayName")

        type_ = ManagedAgentsUnsignedCustomEventSourceRequestType(d.pop("type"))




        managed_agents_unsigned_custom_event_source_request = cls(
            delivery=delivery,
            display_name=display_name,
            type_=type_,
        )

        return managed_agents_unsigned_custom_event_source_request

