from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar, BinaryIO, TextIO, TYPE_CHECKING, Generator

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

from ..types import UNSET, Unset
from typing import cast

if TYPE_CHECKING:
  from ..models.managed_agents_webhook_conversation_part import ManagedAgentsWebhookConversationPart
  from ..models.managed_agents_webhook_filter import ManagedAgentsWebhookFilter





T = TypeVar("T", bound="ManagedAgentsAutomationWebhookTrigger")



@_attrs_define
class ManagedAgentsAutomationWebhookTrigger:
    """ Fires an automation on a verified webhook delivery matching its filters.

        Example:
            {'continue_filter': {'all': [{'operator': 'equals', 'selector': {'body_pointer': 'example', 'header': 'example',
                'source': 'body'}, 'value': 'example', 'values': ['example']}]}, 'conversation_key': [{'selectors':
                [{'body_pointer': 'example', 'header': 'example', 'source': 'body'}]}], 'start_filter': {'all': [{'operator':
                'equals', 'selector': {'body_pointer': 'example', 'header': 'example', 'source': 'body'}, 'value': 'example',
                'values': ['example']}]}, 'webhook_endpoint_id': '9f8b1c2d-3e4f-5a6b-7c8d-9e0f1a2b3c4d'}

        Attributes:
            continue_filter (ManagedAgentsWebhookFilter): A conjunction of conditions that decides whether a webhook
                delivery starts or continues an automation conversation. Example: {'all': [{'operator': 'equals', 'selector':
                {'body_pointer': 'example', 'header': 'example', 'source': 'body'}, 'value': 'example', 'values':
                ['example']}]}.
            start_filter (ManagedAgentsWebhookFilter): A conjunction of conditions that decides whether a webhook delivery
                starts or continues an automation conversation. Example: {'all': [{'operator': 'equals', 'selector':
                {'body_pointer': 'example', 'header': 'example', 'source': 'body'}, 'value': 'example', 'values':
                ['example']}]}.
            webhook_endpoint_id (str): Webhook endpoint whose verified deliveries reach this trigger.
            conversation_key (list[ManagedAgentsWebhookConversationPart] | Unset): Ordered values joined into a stable
                external conversation identity; omit to start an independent session per matching delivery.
     """

    continue_filter: ManagedAgentsWebhookFilter
    start_filter: ManagedAgentsWebhookFilter
    webhook_endpoint_id: str
    conversation_key: list[ManagedAgentsWebhookConversationPart] | Unset = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)





    def to_dict(self) -> dict[str, Any]:
        from ..models.managed_agents_webhook_conversation_part import ManagedAgentsWebhookConversationPart # noqa: PLC0415
        from ..models.managed_agents_webhook_filter import ManagedAgentsWebhookFilter # noqa: PLC0415
        continue_filter = self.continue_filter.to_dict()

        start_filter = self.start_filter.to_dict()

        webhook_endpoint_id = self.webhook_endpoint_id

        conversation_key: list[dict[str, Any]] | Unset = UNSET
        if not isinstance(self.conversation_key, Unset):
            conversation_key = []
            for conversation_key_item_data in self.conversation_key:
                conversation_key_item = conversation_key_item_data.to_dict()
                conversation_key.append(conversation_key_item)




        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({
            "continue_filter": continue_filter,
            "start_filter": start_filter,
            "webhook_endpoint_id": webhook_endpoint_id,
        })
        if conversation_key is not UNSET:
            field_dict["conversation_key"] = conversation_key

        return field_dict



    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.managed_agents_webhook_conversation_part import ManagedAgentsWebhookConversationPart # noqa: PLC0415
        from ..models.managed_agents_webhook_filter import ManagedAgentsWebhookFilter # noqa: PLC0415
        d = dict(src_dict)
        continue_filter = ManagedAgentsWebhookFilter.from_dict(d.pop("continue_filter"))




        start_filter = ManagedAgentsWebhookFilter.from_dict(d.pop("start_filter"))




        webhook_endpoint_id = d.pop("webhook_endpoint_id")

        _conversation_key = d.pop("conversation_key", UNSET)
        conversation_key: list[ManagedAgentsWebhookConversationPart] | Unset = UNSET
        if _conversation_key is not UNSET:
            conversation_key = []
            for conversation_key_item_data in _conversation_key:
                conversation_key_item = ManagedAgentsWebhookConversationPart.from_dict(conversation_key_item_data)



                conversation_key.append(conversation_key_item)


        managed_agents_automation_webhook_trigger = cls(
            continue_filter=continue_filter,
            start_filter=start_filter,
            webhook_endpoint_id=webhook_endpoint_id,
            conversation_key=conversation_key,
        )


        managed_agents_automation_webhook_trigger.additional_properties = d
        return managed_agents_automation_webhook_trigger

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
