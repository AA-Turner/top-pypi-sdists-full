from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar, BinaryIO, TextIO, TYPE_CHECKING, Generator

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

from ..types import UNSET, Unset
from typing import cast

if TYPE_CHECKING:
  from ..models.managed_agents_webhook_acknowledgement_request import ManagedAgentsWebhookAcknowledgementRequest
  from ..models.managed_agents_webhook_delivery_key_request import ManagedAgentsWebhookDeliveryKeyRequest
  from ..models.managed_agents_webhook_verification_request import ManagedAgentsWebhookVerificationRequest





T = TypeVar("T", bound="ManagedAgentsWebhookEndpointRequest")



@_attrs_define
class ManagedAgentsWebhookEndpointRequest:
    """ Provider-neutral configuration for creating or replacing a webhook endpoint.

        Example:
            {'acknowledgement': {'body': {'key': 'example'}, 'challenge_response_field': 'example', 'challenge_selector':
                {'body_pointer': 'example', 'header': 'example', 'source': 'body'}, 'status_code': 1}, 'delivery_key':
                {'body_pointer': 'example', 'header': 'example', 'selectors': [{'body_pointer': 'example', 'header': 'example',
                'source': 'body'}], 'source': 'body'}, 'display_name': 'example-name', 'enabled': True, 'verification':
                {'invalid_signature_status': 1, 'maximum_age_seconds': 1, 'secret_credential_id':
                '9f8b1c2d-3e4f-5a6b-7c8d-9e0f1a2b3c4d', 'secret_vault_id': '9f8b1c2d-3e4f-5a6b-7c8d-9e0f1a2b3c4d',
                'signature_header': 'example', 'signature_prefix': 'example', 'signed_parts': [{'kind': 'body', 'value':
                'example'}], 'timestamp_header': 'example', 'type': 'hmac_sha256'}}

        Attributes:
            acknowledgement (ManagedAgentsWebhookAcknowledgementRequest): Configures the immediate HTTP response sent after
                a webhook delivery is verified and accepted. Example: {'body': {'key': 'example'}, 'challenge_response_field':
                'example', 'challenge_selector': {'body_pointer': 'example', 'header': 'example', 'source': 'body'},
                'status_code': 1}.
            display_name (str): Human-readable endpoint name shown when configuring automations.
            verification (ManagedAgentsWebhookVerificationRequest): Provider-neutral rules for authenticating an inbound
                webhook before its payload can trigger automations. Example: {'invalid_signature_status': 1,
                'maximum_age_seconds': 1, 'secret_credential_id': '9f8b1c2d-3e4f-5a6b-7c8d-9e0f1a2b3c4d', 'secret_vault_id':
                '9f8b1c2d-3e4f-5a6b-7c8d-9e0f1a2b3c4d', 'signature_header': 'example', 'signature_prefix': 'example',
                'signed_parts': [{'kind': 'body', 'value': 'example'}], 'timestamp_header': 'example', 'type': 'hmac_sha256'}.
            delivery_key (ManagedAgentsWebhookDeliveryKeyRequest | Unset): Selects a stable provider delivery identity,
                optionally composed from multiple verified values. Example: {'body_pointer': 'example', 'header': 'example',
                'selectors': [{'body_pointer': 'example', 'header': 'example', 'source': 'body'}], 'source': 'body'}.
            enabled (bool | Unset): Whether the endpoint accepts inbound webhook deliveries.
     """

    acknowledgement: ManagedAgentsWebhookAcknowledgementRequest
    display_name: str
    verification: ManagedAgentsWebhookVerificationRequest
    delivery_key: ManagedAgentsWebhookDeliveryKeyRequest | Unset = UNSET
    enabled: bool | Unset = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)





    def to_dict(self) -> dict[str, Any]:
        from ..models.managed_agents_webhook_acknowledgement_request import ManagedAgentsWebhookAcknowledgementRequest # noqa: PLC0415
        from ..models.managed_agents_webhook_delivery_key_request import ManagedAgentsWebhookDeliveryKeyRequest # noqa: PLC0415
        from ..models.managed_agents_webhook_verification_request import ManagedAgentsWebhookVerificationRequest # noqa: PLC0415
        acknowledgement = self.acknowledgement.to_dict()

        display_name = self.display_name

        verification = self.verification.to_dict()

        delivery_key: dict[str, Any] | Unset = UNSET
        if not isinstance(self.delivery_key, Unset):
            delivery_key = self.delivery_key.to_dict()

        enabled = self.enabled


        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({
            "acknowledgement": acknowledgement,
            "display_name": display_name,
            "verification": verification,
        })
        if delivery_key is not UNSET:
            field_dict["delivery_key"] = delivery_key
        if enabled is not UNSET:
            field_dict["enabled"] = enabled

        return field_dict



    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.managed_agents_webhook_acknowledgement_request import ManagedAgentsWebhookAcknowledgementRequest # noqa: PLC0415
        from ..models.managed_agents_webhook_delivery_key_request import ManagedAgentsWebhookDeliveryKeyRequest # noqa: PLC0415
        from ..models.managed_agents_webhook_verification_request import ManagedAgentsWebhookVerificationRequest # noqa: PLC0415
        d = dict(src_dict)
        acknowledgement = ManagedAgentsWebhookAcknowledgementRequest.from_dict(d.pop("acknowledgement"))




        display_name = d.pop("display_name")

        verification = ManagedAgentsWebhookVerificationRequest.from_dict(d.pop("verification"))




        _delivery_key = d.pop("delivery_key", UNSET)
        delivery_key: ManagedAgentsWebhookDeliveryKeyRequest | Unset
        if isinstance(_delivery_key,  Unset):
            delivery_key = UNSET
        else:
            delivery_key = ManagedAgentsWebhookDeliveryKeyRequest.from_dict(_delivery_key)




        enabled = d.pop("enabled", UNSET)

        managed_agents_webhook_endpoint_request = cls(
            acknowledgement=acknowledgement,
            display_name=display_name,
            verification=verification,
            delivery_key=delivery_key,
            enabled=enabled,
        )


        managed_agents_webhook_endpoint_request.additional_properties = d
        return managed_agents_webhook_endpoint_request

    @property
    def additional_keys(self) -> list[str]:
        return list(self.additional_properties.keys())

    def __getitem__(self, key: str) -> Any:
        return self.additional_properties[key]

    def __setitem__(self, key: str, value: Any) -> None:
        self.additional_properties[key] = value

    def __delitem__(self, key: str) -> None:
        del self.additional_properties[key]

    def __contains__(self, key: str) -> bool:
        return key in self.additional_properties
