from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar, BinaryIO, TextIO, TYPE_CHECKING, Generator

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

from typing import cast

if TYPE_CHECKING:
  from ..models.managed_agents_webhook_endpoint import ManagedAgentsWebhookEndpoint





T = TypeVar("T", bound="ManagedAgentsWebhookEndpointListResponse")



@_attrs_define
class ManagedAgentsWebhookEndpointListResponse:
    """ Webhook endpoints available to automations in the calling organization.

        Example:
            {'webhook_endpoints': [{'acknowledgement': {'body': {'key': 'example'}, 'challenge_response_field': 'example',
                'challenge_selector': {'body_pointer': 'example', 'header': 'example', 'source': 'body'}, 'status_code': 1},
                'created_at': '2026-02-18T09:30:00Z', 'created_by': 'example', 'delivery_key': {'body_pointer': 'example',
                'header': 'example', 'selectors': [{'body_pointer': 'example', 'header': 'example', 'source': 'body'}],
                'source': 'body'}, 'display_name': 'example-name', 'enabled': True, 'endpoint_id':
                '9f8b1c2d-3e4f-5a6b-7c8d-9e0f1a2b3c4d', 'organization_id': '9f8b1c2d-3e4f-5a6b-7c8d-9e0f1a2b3c4d', 'updated_at':
                '2026-02-18T09:30:00Z', 'verification': {'invalid_signature_status': 1, 'maximum_age_seconds': 1,
                'secret_credential_id': '9f8b1c2d-3e4f-5a6b-7c8d-9e0f1a2b3c4d', 'secret_vault_id':
                '9f8b1c2d-3e4f-5a6b-7c8d-9e0f1a2b3c4d', 'signature_header': 'example', 'signature_prefix': 'example',
                'signed_parts': [{'kind': 'body', 'value': 'example'}], 'timestamp_header': 'example', 'type': 'hmac_sha256'}}]}

        Attributes:
            webhook_endpoints (list[ManagedAgentsWebhookEndpoint] | None): Webhook endpoints owned by the calling
                organization.
     """

    webhook_endpoints: list[ManagedAgentsWebhookEndpoint] | None
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)





    def to_dict(self) -> dict[str, Any]:
        from ..models.managed_agents_webhook_endpoint import ManagedAgentsWebhookEndpoint # noqa: PLC0415
        webhook_endpoints: list[dict[str, Any]] | None
        if isinstance(self.webhook_endpoints, list):
            webhook_endpoints = []
            for webhook_endpoints_type_0_item_data in self.webhook_endpoints:
                webhook_endpoints_type_0_item = webhook_endpoints_type_0_item_data.to_dict()
                webhook_endpoints.append(webhook_endpoints_type_0_item)


        else:
            webhook_endpoints = self.webhook_endpoints


        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({
            "webhook_endpoints": webhook_endpoints,
        })

        return field_dict



    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.managed_agents_webhook_endpoint import ManagedAgentsWebhookEndpoint # noqa: PLC0415
        d = dict(src_dict)
        def _parse_webhook_endpoints(data: object) -> list[ManagedAgentsWebhookEndpoint] | None:
            if data is None:
                return data
            try:
                if not isinstance(data, list):
                    raise TypeError()
                webhook_endpoints_type_0 = []
                _webhook_endpoints_type_0 = data
                for webhook_endpoints_type_0_item_data in (_webhook_endpoints_type_0):
                    webhook_endpoints_type_0_item = ManagedAgentsWebhookEndpoint.from_dict(webhook_endpoints_type_0_item_data)



                    webhook_endpoints_type_0.append(webhook_endpoints_type_0_item)

                return webhook_endpoints_type_0
            except (TypeError, ValueError, AttributeError, KeyError):
                pass
            return cast(list[ManagedAgentsWebhookEndpoint] | None, data)

        webhook_endpoints = _parse_webhook_endpoints(d.pop("webhook_endpoints"))


        managed_agents_webhook_endpoint_list_response = cls(
            webhook_endpoints=webhook_endpoints,
        )


        managed_agents_webhook_endpoint_list_response.additional_properties = d
        return managed_agents_webhook_endpoint_list_response

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
