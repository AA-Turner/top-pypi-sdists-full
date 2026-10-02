from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar, BinaryIO, TextIO, TYPE_CHECKING, Generator

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

from ..types import UNSET, Unset
from typing import cast

if TYPE_CHECKING:
  from ..models.managed_agents_webhook_acknowledgement_request_body import ManagedAgentsWebhookAcknowledgementRequestBody
  from ..models.managed_agents_webhook_value_selector_request import ManagedAgentsWebhookValueSelectorRequest





T = TypeVar("T", bound="ManagedAgentsWebhookAcknowledgementRequest")



@_attrs_define
class ManagedAgentsWebhookAcknowledgementRequest:
    """ Configures the immediate HTTP response sent after a webhook delivery is verified and accepted.

        Example:
            {'body': {'key': 'example'}, 'challenge_response_field': 'example', 'challenge_selector': {'body_pointer':
                'example', 'header': 'example', 'source': 'body'}, 'status_code': 1}

        Attributes:
            body (ManagedAgentsWebhookAcknowledgementRequestBody | Unset): Static JSON object returned to the webhook sender
                after acceptance.
            challenge_response_field (str | Unset): Response property populated with the selected challenge value during
                endpoint verification.
            challenge_selector (ManagedAgentsWebhookValueSelectorRequest | Unset): Selects one value from a verified webhook
                delivery body or headers. Example: {'body_pointer': 'example', 'header': 'example', 'source': 'body'}.
            status_code (int | Unset): HTTP status returned after a verified delivery is durably accepted; defaults to 200.
     """

    body: ManagedAgentsWebhookAcknowledgementRequestBody | Unset = UNSET
    challenge_response_field: str | Unset = UNSET
    challenge_selector: ManagedAgentsWebhookValueSelectorRequest | Unset = UNSET
    status_code: int | Unset = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)





    def to_dict(self) -> dict[str, Any]:
        from ..models.managed_agents_webhook_acknowledgement_request_body import ManagedAgentsWebhookAcknowledgementRequestBody # noqa: PLC0415
        from ..models.managed_agents_webhook_value_selector_request import ManagedAgentsWebhookValueSelectorRequest # noqa: PLC0415
        body: dict[str, Any] | Unset = UNSET
        if not isinstance(self.body, Unset):
            body = self.body.to_dict()

        challenge_response_field = self.challenge_response_field

        challenge_selector: dict[str, Any] | Unset = UNSET
        if not isinstance(self.challenge_selector, Unset):
            challenge_selector = self.challenge_selector.to_dict()

        status_code = self.status_code


        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({
        })
        if body is not UNSET:
            field_dict["body"] = body
        if challenge_response_field is not UNSET:
            field_dict["challenge_response_field"] = challenge_response_field
        if challenge_selector is not UNSET:
            field_dict["challenge_selector"] = challenge_selector
        if status_code is not UNSET:
            field_dict["status_code"] = status_code

        return field_dict



    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.managed_agents_webhook_acknowledgement_request_body import ManagedAgentsWebhookAcknowledgementRequestBody # noqa: PLC0415
        from ..models.managed_agents_webhook_value_selector_request import ManagedAgentsWebhookValueSelectorRequest # noqa: PLC0415
        d = dict(src_dict)
        _body = d.pop("body", UNSET)
        body: ManagedAgentsWebhookAcknowledgementRequestBody | Unset
        if isinstance(_body,  Unset):
            body = UNSET
        else:
            body = ManagedAgentsWebhookAcknowledgementRequestBody.from_dict(_body)




        challenge_response_field = d.pop("challenge_response_field", UNSET)

        _challenge_selector = d.pop("challenge_selector", UNSET)
        challenge_selector: ManagedAgentsWebhookValueSelectorRequest | Unset
        if isinstance(_challenge_selector,  Unset):
            challenge_selector = UNSET
        else:
            challenge_selector = ManagedAgentsWebhookValueSelectorRequest.from_dict(_challenge_selector)




        status_code = d.pop("status_code", UNSET)

        managed_agents_webhook_acknowledgement_request = cls(
            body=body,
            challenge_response_field=challenge_response_field,
            challenge_selector=challenge_selector,
            status_code=status_code,
        )


        managed_agents_webhook_acknowledgement_request.additional_properties = d
        return managed_agents_webhook_acknowledgement_request

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
