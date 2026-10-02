from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar, BinaryIO, TextIO, TYPE_CHECKING, Generator

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

from ..types import UNSET, Unset
from typing import cast
import datetime

if TYPE_CHECKING:
  from ..models.managed_agents_webhook_acknowledgement import ManagedAgentsWebhookAcknowledgement
  from ..models.managed_agents_webhook_delivery_key import ManagedAgentsWebhookDeliveryKey
  from ..models.managed_agents_webhook_verification import ManagedAgentsWebhookVerification





T = TypeVar("T", bound="ManagedAgentsWebhookEndpoint")



@_attrs_define
class ManagedAgentsWebhookEndpoint:
    """ An organization-owned, provider-neutral webhook ingress endpoint with configurable verification and acknowledgement.

        Example:
            {'acknowledgement': {'body': {'key': 'example'}, 'challenge_response_field': 'example', 'challenge_selector':
                {'body_pointer': 'example', 'header': 'example', 'source': 'body'}, 'status_code': 1}, 'created_at':
                '2026-02-18T09:30:00Z', 'created_by': 'example', 'delivery_key': {'body_pointer': 'example', 'header':
                'example', 'selectors': [{'body_pointer': 'example', 'header': 'example', 'source': 'body'}], 'source': 'body'},
                'display_name': 'example-name', 'enabled': True, 'endpoint_id': '9f8b1c2d-3e4f-5a6b-7c8d-9e0f1a2b3c4d',
                'organization_id': '9f8b1c2d-3e4f-5a6b-7c8d-9e0f1a2b3c4d', 'updated_at': '2026-02-18T09:30:00Z', 'verification':
                {'invalid_signature_status': 1, 'maximum_age_seconds': 1, 'secret_credential_id':
                '9f8b1c2d-3e4f-5a6b-7c8d-9e0f1a2b3c4d', 'secret_vault_id': '9f8b1c2d-3e4f-5a6b-7c8d-9e0f1a2b3c4d',
                'signature_header': 'example', 'signature_prefix': 'example', 'signed_parts': [{'kind': 'body', 'value':
                'example'}], 'timestamp_header': 'example', 'type': 'hmac_sha256'}}

        Attributes:
            acknowledgement (ManagedAgentsWebhookAcknowledgement): Configures the immediate HTTP response sent after a
                webhook delivery is verified and accepted. Example: {'body': {'key': 'example'}, 'challenge_response_field':
                'example', 'challenge_selector': {'body_pointer': 'example', 'header': 'example', 'source': 'body'},
                'status_code': 1}.
            created_at (datetime.datetime): Server-assigned RFC 3339 creation timestamp.
            display_name (str): Human-readable name shown when configuring automations.
            enabled (bool): Whether the endpoint currently accepts deliveries.
            endpoint_id (str): Server-assigned endpoint identifier used in the public webhook URL.
            organization_id (str): Organization that owns the endpoint, resolved from the authenticated request scope.
            updated_at (datetime.datetime): Server-assigned RFC 3339 timestamp of the most recent configuration change.
            verification (ManagedAgentsWebhookVerification): Provider-neutral rules for authenticating an inbound webhook
                before its payload can trigger automations. Example: {'invalid_signature_status': 1, 'maximum_age_seconds': 1,
                'secret_credential_id': '9f8b1c2d-3e4f-5a6b-7c8d-9e0f1a2b3c4d', 'secret_vault_id':
                '9f8b1c2d-3e4f-5a6b-7c8d-9e0f1a2b3c4d', 'signature_header': 'example', 'signature_prefix': 'example',
                'signed_parts': [{'kind': 'body', 'value': 'example'}], 'timestamp_header': 'example', 'type': 'hmac_sha256'}.
            created_by (str | Unset): Authenticated principal that created the endpoint.
            delivery_key (ManagedAgentsWebhookDeliveryKey | Unset): Selects a stable provider delivery identity, optionally
                composed from multiple verified values. Example: {'body_pointer': 'example', 'header': 'example', 'selectors':
                [{'body_pointer': 'example', 'header': 'example', 'source': 'body'}], 'source': 'body'}.
     """

    acknowledgement: ManagedAgentsWebhookAcknowledgement
    created_at: datetime.datetime
    display_name: str
    enabled: bool
    endpoint_id: str
    organization_id: str
    updated_at: datetime.datetime
    verification: ManagedAgentsWebhookVerification
    created_by: str | Unset = UNSET
    delivery_key: ManagedAgentsWebhookDeliveryKey | Unset = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)





    def to_dict(self) -> dict[str, Any]:
        from ..models.managed_agents_webhook_acknowledgement import ManagedAgentsWebhookAcknowledgement # noqa: PLC0415
        from ..models.managed_agents_webhook_delivery_key import ManagedAgentsWebhookDeliveryKey # noqa: PLC0415
        from ..models.managed_agents_webhook_verification import ManagedAgentsWebhookVerification # noqa: PLC0415
        acknowledgement = self.acknowledgement.to_dict()

        created_at = self.created_at.isoformat()

        display_name = self.display_name

        enabled = self.enabled

        endpoint_id = self.endpoint_id

        organization_id = self.organization_id

        updated_at = self.updated_at.isoformat()

        verification = self.verification.to_dict()

        created_by = self.created_by

        delivery_key: dict[str, Any] | Unset = UNSET
        if not isinstance(self.delivery_key, Unset):
            delivery_key = self.delivery_key.to_dict()


        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({
            "acknowledgement": acknowledgement,
            "created_at": created_at,
            "display_name": display_name,
            "enabled": enabled,
            "endpoint_id": endpoint_id,
            "organization_id": organization_id,
            "updated_at": updated_at,
            "verification": verification,
        })
        if created_by is not UNSET:
            field_dict["created_by"] = created_by
        if delivery_key is not UNSET:
            field_dict["delivery_key"] = delivery_key

        return field_dict



    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.managed_agents_webhook_acknowledgement import ManagedAgentsWebhookAcknowledgement # noqa: PLC0415
        from ..models.managed_agents_webhook_delivery_key import ManagedAgentsWebhookDeliveryKey # noqa: PLC0415
        from ..models.managed_agents_webhook_verification import ManagedAgentsWebhookVerification # noqa: PLC0415
        d = dict(src_dict)
        acknowledgement = ManagedAgentsWebhookAcknowledgement.from_dict(d.pop("acknowledgement"))




        created_at = datetime.datetime.fromisoformat(d.pop("created_at"))




        display_name = d.pop("display_name")

        enabled = d.pop("enabled")

        endpoint_id = d.pop("endpoint_id")

        organization_id = d.pop("organization_id")

        updated_at = datetime.datetime.fromisoformat(d.pop("updated_at"))




        verification = ManagedAgentsWebhookVerification.from_dict(d.pop("verification"))




        created_by = d.pop("created_by", UNSET)

        _delivery_key = d.pop("delivery_key", UNSET)
        delivery_key: ManagedAgentsWebhookDeliveryKey | Unset
        if isinstance(_delivery_key,  Unset):
            delivery_key = UNSET
        else:
            delivery_key = ManagedAgentsWebhookDeliveryKey.from_dict(_delivery_key)




        managed_agents_webhook_endpoint = cls(
            acknowledgement=acknowledgement,
            created_at=created_at,
            display_name=display_name,
            enabled=enabled,
            endpoint_id=endpoint_id,
            organization_id=organization_id,
            updated_at=updated_at,
            verification=verification,
            created_by=created_by,
            delivery_key=delivery_key,
        )


        managed_agents_webhook_endpoint.additional_properties = d
        return managed_agents_webhook_endpoint

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
