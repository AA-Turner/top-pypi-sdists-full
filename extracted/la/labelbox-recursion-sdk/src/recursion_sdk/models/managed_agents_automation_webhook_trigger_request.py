from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar, BinaryIO, TextIO, TYPE_CHECKING, Generator

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

from ..types import UNSET, Unset
from typing import cast

if TYPE_CHECKING:
  from ..models.managed_agents_webhook_conversation_part_request import ManagedAgentsWebhookConversationPartRequest
  from ..models.managed_agents_webhook_filter_request import ManagedAgentsWebhookFilterRequest





T = TypeVar("T", bound="ManagedAgentsAutomationWebhookTriggerRequest")



@_attrs_define
class ManagedAgentsAutomationWebhookTriggerRequest:
    """ Fires an automation on a verified webhook delivery matching its filters.

        Example:
            {'continue_filter': {'all': [{'operator': 'equals', 'selector': {'body_pointer': 'example', 'header': 'example',
                'source': 'body'}, 'value': 'example', 'values': ['example']}]}, 'conversation_key': [{'selectors':
                [{'body_pointer': 'example', 'header': 'example', 'source': 'body'}]}], 'start_filter': {'all': [{'operator':
                'equals', 'selector': {'body_pointer': 'example', 'header': 'example', 'source': 'body'}, 'value': 'example',
                'values': ['example']}]}, 'webhook_endpoint_id': '9f8b1c2d-3e4f-5a6b-7c8d-9e0f1a2b3c4d'}

        Attributes:
            continue_filter (ManagedAgentsWebhookFilterRequest | Unset): A conjunction of conditions that decides whether a
                webhook delivery starts or continues an automation conversation. Example: {'all': [{'operator': 'equals',
                'selector': {'body_pointer': 'example', 'header': 'example', 'source': 'body'}, 'value': 'example', 'values':
                ['example']}]}.
            conversation_key (list[ManagedAgentsWebhookConversationPartRequest] | Unset): Ordered values joined into a
                stable external conversation identity; omit to start an independent session per matching delivery.
            start_filter (ManagedAgentsWebhookFilterRequest | Unset): A conjunction of conditions that decides whether a
                webhook delivery starts or continues an automation conversation. Example: {'all': [{'operator': 'equals',
                'selector': {'body_pointer': 'example', 'header': 'example', 'source': 'body'}, 'value': 'example', 'values':
                ['example']}]}.
            webhook_endpoint_id (str | Unset): Webhook endpoint whose verified deliveries reach this trigger.
     """

    continue_filter: ManagedAgentsWebhookFilterRequest | Unset = UNSET
    conversation_key: list[ManagedAgentsWebhookConversationPartRequest] | Unset = UNSET
    start_filter: ManagedAgentsWebhookFilterRequest | Unset = UNSET
    webhook_endpoint_id: str | Unset = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)





    def to_dict(self) -> dict[str, Any]:
        from ..models.managed_agents_webhook_conversation_part_request import ManagedAgentsWebhookConversationPartRequest # noqa: PLC0415
        from ..models.managed_agents_webhook_filter_request import ManagedAgentsWebhookFilterRequest # noqa: PLC0415
        continue_filter: dict[str, Any] | Unset = UNSET
        if not isinstance(self.continue_filter, Unset):
            continue_filter = self.continue_filter.to_dict()

        conversation_key: list[dict[str, Any]] | Unset = UNSET
        if not isinstance(self.conversation_key, Unset):
            conversation_key = []
            for conversation_key_item_data in self.conversation_key:
                conversation_key_item = conversation_key_item_data.to_dict()
                conversation_key.append(conversation_key_item)



        start_filter: dict[str, Any] | Unset = UNSET
        if not isinstance(self.start_filter, Unset):
            start_filter = self.start_filter.to_dict()

        webhook_endpoint_id = self.webhook_endpoint_id


        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({
        })
        if continue_filter is not UNSET:
            field_dict["continue_filter"] = continue_filter
        if conversation_key is not UNSET:
            field_dict["conversation_key"] = conversation_key
        if start_filter is not UNSET:
            field_dict["start_filter"] = start_filter
        if webhook_endpoint_id is not UNSET:
            field_dict["webhook_endpoint_id"] = webhook_endpoint_id

        return field_dict



    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.managed_agents_webhook_conversation_part_request import ManagedAgentsWebhookConversationPartRequest # noqa: PLC0415
        from ..models.managed_agents_webhook_filter_request import ManagedAgentsWebhookFilterRequest # noqa: PLC0415
        d = dict(src_dict)
        _continue_filter = d.pop("continue_filter", UNSET)
        continue_filter: ManagedAgentsWebhookFilterRequest | Unset
        if isinstance(_continue_filter,  Unset):
            continue_filter = UNSET
        else:
            continue_filter = ManagedAgentsWebhookFilterRequest.from_dict(_continue_filter)




        _conversation_key = d.pop("conversation_key", UNSET)
        conversation_key: list[ManagedAgentsWebhookConversationPartRequest] | Unset = UNSET
        if _conversation_key is not UNSET:
            conversation_key = []
            for conversation_key_item_data in _conversation_key:
                conversation_key_item = ManagedAgentsWebhookConversationPartRequest.from_dict(conversation_key_item_data)



                conversation_key.append(conversation_key_item)


        _start_filter = d.pop("start_filter", UNSET)
        start_filter: ManagedAgentsWebhookFilterRequest | Unset
        if isinstance(_start_filter,  Unset):
            start_filter = UNSET
        else:
            start_filter = ManagedAgentsWebhookFilterRequest.from_dict(_start_filter)




        webhook_endpoint_id = d.pop("webhook_endpoint_id", UNSET)

        managed_agents_automation_webhook_trigger_request = cls(
            continue_filter=continue_filter,
            conversation_key=conversation_key,
            start_filter=start_filter,
            webhook_endpoint_id=webhook_endpoint_id,
        )


        managed_agents_automation_webhook_trigger_request.additional_properties = d
        return managed_agents_automation_webhook_trigger_request

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
