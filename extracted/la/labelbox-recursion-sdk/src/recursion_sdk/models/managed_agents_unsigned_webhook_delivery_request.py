from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar, BinaryIO, TextIO, TYPE_CHECKING, Generator

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

from ..models.managed_agents_unsigned_webhook_delivery_request_kind import ManagedAgentsUnsignedWebhookDeliveryRequestKind
from typing import cast

if TYPE_CHECKING:
  from ..models.managed_agents_unsigned_custom_event_source_verification import ManagedAgentsUnsignedCustomEventSourceVerification





T = TypeVar("T", bound="ManagedAgentsUnsignedWebhookDeliveryRequest")



@_attrs_define
class ManagedAgentsUnsignedWebhookDeliveryRequest:
    """ Custom webhook delivery without cryptographic verification.

        Example:
            {'kind': 'webhook', 'verification': {'type': 'none'}}

        Attributes:
            kind (ManagedAgentsUnsignedWebhookDeliveryRequestKind): Customer-configured webhook delivery.
            verification (ManagedAgentsUnsignedCustomEventSourceVerification): Explicit unsigned-delivery policy for a
                custom webhook. Example: {'type': 'none'}.
     """

    kind: ManagedAgentsUnsignedWebhookDeliveryRequestKind
    verification: ManagedAgentsUnsignedCustomEventSourceVerification





    def to_dict(self) -> dict[str, Any]:
        from ..models.managed_agents_unsigned_custom_event_source_verification import ManagedAgentsUnsignedCustomEventSourceVerification # noqa: PLC0415
        kind = self.kind.value

        verification = self.verification.to_dict()


        field_dict: dict[str, Any] = {}

        field_dict.update({
            "kind": kind,
            "verification": verification,
        })

        return field_dict



    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.managed_agents_unsigned_custom_event_source_verification import ManagedAgentsUnsignedCustomEventSourceVerification # noqa: PLC0415
        d = dict(src_dict)
        kind = ManagedAgentsUnsignedWebhookDeliveryRequestKind(d.pop("kind"))




        verification = ManagedAgentsUnsignedCustomEventSourceVerification.from_dict(d.pop("verification"))




        managed_agents_unsigned_webhook_delivery_request = cls(
            kind=kind,
            verification=verification,
        )

        return managed_agents_unsigned_webhook_delivery_request

