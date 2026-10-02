from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar, BinaryIO, TextIO, TYPE_CHECKING, Generator

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

from ..models.managed_agents_github_event_source_request_type import ManagedAgentsGithubEventSourceRequestType
from typing import cast

if TYPE_CHECKING:
  from ..models.managed_agents_provider_webhook_delivery_request import ManagedAgentsProviderWebhookDeliveryRequest





T = TypeVar("T", bound="ManagedAgentsGithubEventSourceRequest")



@_attrs_define
class ManagedAgentsGithubEventSourceRequest:
    """ Closed configuration for a GitHub webhook source.

        Example:
            {'delivery': {'kind': 'webhook', 'verificationCredential': {'credentialId':
                '9f8b1c2d-3e4f-5a6b-7c8d-9e0f1a2b3c4d', 'vaultId': '9f8b1c2d-3e4f-5a6b-7c8d-9e0f1a2b3c4d'}}, 'displayName':
                'example', 'type': 'github_webhook'}

        Attributes:
            delivery (ManagedAgentsProviderWebhookDeliveryRequest): Verification configuration for a customer-owned Slack or
                GitHub webhook. Example: {'kind': 'webhook', 'verificationCredential': {'credentialId':
                '9f8b1c2d-3e4f-5a6b-7c8d-9e0f1a2b3c4d', 'vaultId': '9f8b1c2d-3e4f-5a6b-7c8d-9e0f1a2b3c4d'}}.
            display_name (str): Human-readable source name shown in the automation catalog.
            type_ (ManagedAgentsGithubEventSourceRequestType): GitHub webhook protocol with service-owned verification
                semantics.
     """

    delivery: ManagedAgentsProviderWebhookDeliveryRequest
    display_name: str
    type_: ManagedAgentsGithubEventSourceRequestType





    def to_dict(self) -> dict[str, Any]:
        from ..models.managed_agents_provider_webhook_delivery_request import ManagedAgentsProviderWebhookDeliveryRequest # noqa: PLC0415
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
        from ..models.managed_agents_provider_webhook_delivery_request import ManagedAgentsProviderWebhookDeliveryRequest # noqa: PLC0415
        d = dict(src_dict)
        delivery = ManagedAgentsProviderWebhookDeliveryRequest.from_dict(d.pop("delivery"))




        display_name = d.pop("displayName")

        type_ = ManagedAgentsGithubEventSourceRequestType(d.pop("type"))




        managed_agents_github_event_source_request = cls(
            delivery=delivery,
            display_name=display_name,
            type_=type_,
        )

        return managed_agents_github_event_source_request

