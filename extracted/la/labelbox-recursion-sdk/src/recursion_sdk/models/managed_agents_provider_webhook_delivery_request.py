from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar, BinaryIO, TextIO, TYPE_CHECKING, Generator

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

from ..models.managed_agents_provider_webhook_delivery_request_kind import ManagedAgentsProviderWebhookDeliveryRequestKind
from typing import cast

if TYPE_CHECKING:
  from ..models.managed_agents_event_source_credential_ref import ManagedAgentsEventSourceCredentialRef





T = TypeVar("T", bound="ManagedAgentsProviderWebhookDeliveryRequest")



@_attrs_define
class ManagedAgentsProviderWebhookDeliveryRequest:
    """ Verification configuration for a customer-owned Slack or GitHub webhook.

        Example:
            {'kind': 'webhook', 'verificationCredential': {'credentialId': '9f8b1c2d-3e4f-5a6b-7c8d-9e0f1a2b3c4d',
                'vaultId': '9f8b1c2d-3e4f-5a6b-7c8d-9e0f1a2b3c4d'}}

        Attributes:
            kind (ManagedAgentsProviderWebhookDeliveryRequestKind): Customer-configured webhook delivery.
            verification_credential (ManagedAgentsEventSourceCredentialRef): Reference to a managed credential; secret
                material is never returned. Example: {'credentialId': '9f8b1c2d-3e4f-5a6b-7c8d-9e0f1a2b3c4d', 'vaultId':
                '9f8b1c2d-3e4f-5a6b-7c8d-9e0f1a2b3c4d'}.
     """

    kind: ManagedAgentsProviderWebhookDeliveryRequestKind
    verification_credential: ManagedAgentsEventSourceCredentialRef





    def to_dict(self) -> dict[str, Any]:
        from ..models.managed_agents_event_source_credential_ref import ManagedAgentsEventSourceCredentialRef # noqa: PLC0415
        kind = self.kind.value

        verification_credential = self.verification_credential.to_dict()


        field_dict: dict[str, Any] = {}

        field_dict.update({
            "kind": kind,
            "verificationCredential": verification_credential,
        })

        return field_dict



    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.managed_agents_event_source_credential_ref import ManagedAgentsEventSourceCredentialRef # noqa: PLC0415
        d = dict(src_dict)
        kind = ManagedAgentsProviderWebhookDeliveryRequestKind(d.pop("kind"))




        verification_credential = ManagedAgentsEventSourceCredentialRef.from_dict(d.pop("verificationCredential"))




        managed_agents_provider_webhook_delivery_request = cls(
            kind=kind,
            verification_credential=verification_credential,
        )

        return managed_agents_provider_webhook_delivery_request

