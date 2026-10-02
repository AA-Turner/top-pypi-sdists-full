from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar, BinaryIO, TextIO, TYPE_CHECKING, Generator

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

from ..models.managed_agents_automation_trigger_type import ManagedAgentsAutomationTriggerType
from ..types import UNSET, Unset
from typing import cast

if TYPE_CHECKING:
  from ..models.managed_agents_automation_schedule_trigger import ManagedAgentsAutomationScheduleTrigger
  from ..models.managed_agents_automation_webhook_trigger import ManagedAgentsAutomationWebhookTrigger





T = TypeVar("T", bound="ManagedAgentsAutomationTrigger")



@_attrs_define
class ManagedAgentsAutomationTrigger:
    """ One reason an automation starts work: a schedule, a verified webhook delivery, or a manual request.

        Example:
            {'display_name': 'example-name', 'enabled': True, 'schedule': {'catchup_window_seconds': 1, 'cron': 'example',
                'end_at': '2026-02-18T09:30:00Z', 'jitter_seconds': 1, 'last_run_at': '2026-02-18T09:30:00Z',
                'missed_catchup_window': 1, 'next_run_at': '2026-02-18T09:30:00Z', 'overlap_policy': 'skip', 'skipped_overlap':
                1, 'start_at': '2026-02-18T09:30:00Z', 'synchronization': {'error': 'example', 'status': 'pending'}, 'timezone':
                'example', 'upcoming_runs_at': ['2026-02-18T09:30:00Z']}, 'trigger_id': '9f8b1c2d-3e4f-5a6b-7c8d-9e0f1a2b3c4d',
                'type': 'schedule', 'webhook': {'continue_filter': {'all': [{'operator': 'equals', 'selector': {'body_pointer':
                'example', 'header': 'example', 'source': 'body'}, 'value': 'example', 'values': ['example']}]},
                'conversation_key': [{'selectors': [{'body_pointer': 'example', 'header': 'example', 'source': 'body'}]}],
                'start_filter': {'all': [{'operator': 'equals', 'selector': {'body_pointer': 'example', 'header': 'example',
                'source': 'body'}, 'value': 'example', 'values': ['example']}]}, 'webhook_endpoint_id':
                '9f8b1c2d-3e4f-5a6b-7c8d-9e0f1a2b3c4d'}}

        Attributes:
            type_ (ManagedAgentsAutomationTriggerType): Which mechanism fires this trigger. Exactly one matching payload
                field must be present, and no other.
            display_name (str | Unset): Human-readable name shown beside the trigger in the console.
            enabled (bool | Unset): Whether this trigger may start work. Independent of the automation's own status, which
                suspends every trigger at once. Omit to leave it as it is, which for a new trigger means enabled.
            schedule (ManagedAgentsAutomationScheduleTrigger | Unset): Fires an automation using a Temporal Schedule.
                Example: {'catchup_window_seconds': 1, 'cron': 'example', 'end_at': '2026-02-18T09:30:00Z', 'jitter_seconds': 1,
                'last_run_at': '2026-02-18T09:30:00Z', 'missed_catchup_window': 1, 'next_run_at': '2026-02-18T09:30:00Z',
                'overlap_policy': 'skip', 'skipped_overlap': 1, 'start_at': '2026-02-18T09:30:00Z', 'synchronization': {'error':
                'example', 'status': 'pending'}, 'timezone': 'example', 'upcoming_runs_at': ['2026-02-18T09:30:00Z']}.
            trigger_id (str | Unset): Server-assigned trigger identifier, stable across configuration updates. Omit when
                creating.
            webhook (ManagedAgentsAutomationWebhookTrigger | Unset): Fires an automation on a verified webhook delivery
                matching its filters. Example: {'continue_filter': {'all': [{'operator': 'equals', 'selector': {'body_pointer':
                'example', 'header': 'example', 'source': 'body'}, 'value': 'example', 'values': ['example']}]},
                'conversation_key': [{'selectors': [{'body_pointer': 'example', 'header': 'example', 'source': 'body'}]}],
                'start_filter': {'all': [{'operator': 'equals', 'selector': {'body_pointer': 'example', 'header': 'example',
                'source': 'body'}, 'value': 'example', 'values': ['example']}]}, 'webhook_endpoint_id':
                '9f8b1c2d-3e4f-5a6b-7c8d-9e0f1a2b3c4d'}.
     """

    type_: ManagedAgentsAutomationTriggerType
    display_name: str | Unset = UNSET
    enabled: bool | Unset = UNSET
    schedule: ManagedAgentsAutomationScheduleTrigger | Unset = UNSET
    trigger_id: str | Unset = UNSET
    webhook: ManagedAgentsAutomationWebhookTrigger | Unset = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)





    def to_dict(self) -> dict[str, Any]:
        from ..models.managed_agents_automation_schedule_trigger import ManagedAgentsAutomationScheduleTrigger # noqa: PLC0415
        from ..models.managed_agents_automation_webhook_trigger import ManagedAgentsAutomationWebhookTrigger # noqa: PLC0415
        type_ = self.type_.value

        display_name = self.display_name

        enabled = self.enabled

        schedule: dict[str, Any] | Unset = UNSET
        if not isinstance(self.schedule, Unset):
            schedule = self.schedule.to_dict()

        trigger_id = self.trigger_id

        webhook: dict[str, Any] | Unset = UNSET
        if not isinstance(self.webhook, Unset):
            webhook = self.webhook.to_dict()


        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({
            "type": type_,
        })
        if display_name is not UNSET:
            field_dict["display_name"] = display_name
        if enabled is not UNSET:
            field_dict["enabled"] = enabled
        if schedule is not UNSET:
            field_dict["schedule"] = schedule
        if trigger_id is not UNSET:
            field_dict["trigger_id"] = trigger_id
        if webhook is not UNSET:
            field_dict["webhook"] = webhook

        return field_dict



    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.managed_agents_automation_schedule_trigger import ManagedAgentsAutomationScheduleTrigger # noqa: PLC0415
        from ..models.managed_agents_automation_webhook_trigger import ManagedAgentsAutomationWebhookTrigger # noqa: PLC0415
        d = dict(src_dict)
        type_ = ManagedAgentsAutomationTriggerType(d.pop("type"))




        display_name = d.pop("display_name", UNSET)

        enabled = d.pop("enabled", UNSET)

        _schedule = d.pop("schedule", UNSET)
        schedule: ManagedAgentsAutomationScheduleTrigger | Unset
        if isinstance(_schedule,  Unset):
            schedule = UNSET
        else:
            schedule = ManagedAgentsAutomationScheduleTrigger.from_dict(_schedule)




        trigger_id = d.pop("trigger_id", UNSET)

        _webhook = d.pop("webhook", UNSET)
        webhook: ManagedAgentsAutomationWebhookTrigger | Unset
        if isinstance(_webhook,  Unset):
            webhook = UNSET
        else:
            webhook = ManagedAgentsAutomationWebhookTrigger.from_dict(_webhook)




        managed_agents_automation_trigger = cls(
            type_=type_,
            display_name=display_name,
            enabled=enabled,
            schedule=schedule,
            trigger_id=trigger_id,
            webhook=webhook,
        )


        managed_agents_automation_trigger.additional_properties = d
        return managed_agents_automation_trigger

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
