from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar, BinaryIO, TextIO, TYPE_CHECKING, Generator

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

from ..models.managed_agents_hmac_webhook_delivery_request_kind import ManagedAgentsHmacWebhookDeliveryRequestKind
from typing import cast

if TYPE_CHECKING:
  from ..models.managed_agents_hmac_custom_event_source_verification import ManagedAgentsHmacCustomEventSourceVerification





T = TypeVar("T", bound="ManagedAgentsHmacWebhookDeliveryRequest")



@_attrs_define
class ManagedAgentsHmacWebhookDeliveryRequest:
    """ Custom webhook delivery authenticated by HMAC-SHA256.

        Example:
            {'kind': 'webhook', 'verification': {'signatureHeader': 'example', 'signaturePrefix': 'example', 'signedParts':
                [{'kind': 'body'}], 'type': 'hmac_sha256', 'verificationCredential': {'credentialId':
                '9f8b1c2d-3e4f-5a6b-7c8d-9e0f1a2b3c4d', 'vaultId': '9f8b1c2d-3e4f-5a6b-7c8d-9e0f1a2b3c4d'}}}

        Attributes:
            kind (ManagedAgentsHmacWebhookDeliveryRequestKind): Customer-configured webhook delivery.
            verification (ManagedAgentsHmacCustomEventSourceVerification): HMAC-SHA256 verification policy for a custom
                webhook. Example: {'signatureHeader': 'example', 'signaturePrefix': 'example', 'signedParts': [{'kind':
                'body'}], 'type': 'hmac_sha256', 'verificationCredential': {'credentialId':
                '9f8b1c2d-3e4f-5a6b-7c8d-9e0f1a2b3c4d', 'vaultId': '9f8b1c2d-3e4f-5a6b-7c8d-9e0f1a2b3c4d'}}.
     """

    kind: ManagedAgentsHmacWebhookDeliveryRequestKind
    verification: ManagedAgentsHmacCustomEventSourceVerification





    def to_dict(self) -> dict[str, Any]:
        from ..models.managed_agents_hmac_custom_event_source_verification import ManagedAgentsHmacCustomEventSourceVerification # noqa: PLC0415
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
        from ..models.managed_agents_hmac_custom_event_source_verification import ManagedAgentsHmacCustomEventSourceVerification # noqa: PLC0415
        d = dict(src_dict)
        kind = ManagedAgentsHmacWebhookDeliveryRequestKind(d.pop("kind"))




        verification = ManagedAgentsHmacCustomEventSourceVerification.from_dict(d.pop("verification"))




        managed_agents_hmac_webhook_delivery_request = cls(
            kind=kind,
            verification=verification,
        )

        return managed_agents_hmac_webhook_delivery_request

