from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar, BinaryIO, TextIO, TYPE_CHECKING, Generator

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

from ..models.managed_agents_webhook_event_source_delivery_kind import ManagedAgentsWebhookEventSourceDeliveryKind
from ..types import UNSET, Unset
from typing import cast

if TYPE_CHECKING:
  from ..models.managed_agents_event_source_credential_ref import ManagedAgentsEventSourceCredentialRef
  from ..models.managed_agents_event_source_verification_response import ManagedAgentsEventSourceVerificationResponse





T = TypeVar("T", bound="ManagedAgentsWebhookEventSourceDelivery")



@_attrs_define
class ManagedAgentsWebhookEventSourceDelivery:
    """ Customer-owned webhook endpoint and its non-secret verification configuration.

        Example:
            {'kind': 'webhook', 'verification': {'signatureHeader': 'example', 'signaturePrefix': 'example', 'signedParts':
                [{'kind': 'body'}], 'type': 'none', 'verificationCredential': {'credentialId':
                '9f8b1c2d-3e4f-5a6b-7c8d-9e0f1a2b3c4d', 'vaultId': '9f8b1c2d-3e4f-5a6b-7c8d-9e0f1a2b3c4d'}},
                'verificationCredential': {'credentialId': '9f8b1c2d-3e4f-5a6b-7c8d-9e0f1a2b3c4d', 'vaultId':
                '9f8b1c2d-3e4f-5a6b-7c8d-9e0f1a2b3c4d'}, 'webhookUrl': 'example'}

        Attributes:
            kind (ManagedAgentsWebhookEventSourceDeliveryKind): Customer-configured webhook delivery.
            webhook_url (str): Relative public endpoint to configure at the event provider.
            verification (ManagedAgentsEventSourceVerificationResponse | Unset): Verification policy for a custom webhook
                event source. Example: {'signatureHeader': 'example', 'signaturePrefix': 'example', 'signedParts': [{'kind':
                'body'}], 'type': 'none', 'verificationCredential': {'credentialId': '9f8b1c2d-3e4f-5a6b-7c8d-9e0f1a2b3c4d',
                'vaultId': '9f8b1c2d-3e4f-5a6b-7c8d-9e0f1a2b3c4d'}}.
            verification_credential (ManagedAgentsEventSourceCredentialRef | Unset): Reference to a managed credential;
                secret material is never returned. Example: {'credentialId': '9f8b1c2d-3e4f-5a6b-7c8d-9e0f1a2b3c4d', 'vaultId':
                '9f8b1c2d-3e4f-5a6b-7c8d-9e0f1a2b3c4d'}.
     """

    kind: ManagedAgentsWebhookEventSourceDeliveryKind
    webhook_url: str
    verification: ManagedAgentsEventSourceVerificationResponse | Unset = UNSET
    verification_credential: ManagedAgentsEventSourceCredentialRef | Unset = UNSET





    def to_dict(self) -> dict[str, Any]:
        from ..models.managed_agents_event_source_credential_ref import ManagedAgentsEventSourceCredentialRef # noqa: PLC0415
        from ..models.managed_agents_event_source_verification_response import ManagedAgentsEventSourceVerificationResponse # noqa: PLC0415
        kind = self.kind.value

        webhook_url = self.webhook_url

        verification: dict[str, Any] | Unset = UNSET
        if not isinstance(self.verification, Unset):
            verification = self.verification.to_dict()

        verification_credential: dict[str, Any] | Unset = UNSET
        if not isinstance(self.verification_credential, Unset):
            verification_credential = self.verification_credential.to_dict()


        field_dict: dict[str, Any] = {}

        field_dict.update({
            "kind": kind,
            "webhookUrl": webhook_url,
        })
        if verification is not UNSET:
            field_dict["verification"] = verification
        if verification_credential is not UNSET:
            field_dict["verificationCredential"] = verification_credential

        return field_dict



    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.managed_agents_event_source_credential_ref import ManagedAgentsEventSourceCredentialRef # noqa: PLC0415
        from ..models.managed_agents_event_source_verification_response import ManagedAgentsEventSourceVerificationResponse # noqa: PLC0415
        d = dict(src_dict)
        kind = ManagedAgentsWebhookEventSourceDeliveryKind(d.pop("kind"))




        webhook_url = d.pop("webhookUrl")

        _verification = d.pop("verification", UNSET)
        verification: ManagedAgentsEventSourceVerificationResponse | Unset
        if isinstance(_verification,  Unset):
            verification = UNSET
        else:
            verification = ManagedAgentsEventSourceVerificationResponse.from_dict(_verification)




        _verification_credential = d.pop("verificationCredential", UNSET)
        verification_credential: ManagedAgentsEventSourceCredentialRef | Unset
        if isinstance(_verification_credential,  Unset):
            verification_credential = UNSET
        else:
            verification_credential = ManagedAgentsEventSourceCredentialRef.from_dict(_verification_credential)




        managed_agents_webhook_event_source_delivery = cls(
            kind=kind,
            webhook_url=webhook_url,
            verification=verification,
            verification_credential=verification_credential,
        )

        return managed_agents_webhook_event_source_delivery

