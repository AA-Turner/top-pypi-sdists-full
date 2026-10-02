from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar, BinaryIO, TextIO, TYPE_CHECKING, Generator

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

from ..models.managed_agents_automation_trigger_request_type import ManagedAgentsAutomationTriggerRequestType
from ..types import UNSET, Unset
from typing import cast

if TYPE_CHECKING:
  from ..models.managed_agents_automation_schedule_trigger_request import ManagedAgentsAutomationScheduleTriggerRequest
  from ..models.managed_agents_automation_webhook_trigger_request import ManagedAgentsAutomationWebhookTriggerRequest





T = TypeVar("T", bound="ManagedAgentsAutomationTriggerRequest")



@_attrs_define
class ManagedAgentsAutomationTriggerRequest:
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
            display_name (str | Unset): Human-readable name shown beside the trigger in the console.
            enabled (bool | None | Unset): Whether this trigger may start work. Independent of the automation's own status,
                which suspends every trigger at once. Omit to leave it as it is, which for a new trigger means enabled.
            schedule (ManagedAgentsAutomationScheduleTriggerRequest | Unset): Fires an automation using a Temporal Schedule.
                Example: {'catchup_window_seconds': 1, 'cron': 'example', 'end_at': '2026-02-18T09:30:00Z', 'jitter_seconds': 1,
                'last_run_at': '2026-02-18T09:30:00Z', 'missed_catchup_window': 1, 'next_run_at': '2026-02-18T09:30:00Z',
                'overlap_policy': 'skip', 'skipped_overlap': 1, 'start_at': '2026-02-18T09:30:00Z', 'synchronization': {'error':
                'example', 'status': 'pending'}, 'timezone': 'example', 'upcoming_runs_at': ['2026-02-18T09:30:00Z']}.
            trigger_id (str | Unset): Server-assigned trigger identifier, stable across configuration updates. Omit when
                creating.
            type_ (ManagedAgentsAutomationTriggerRequestType | Unset): Which mechanism fires this trigger. Exactly one
                matching payload field must be present, and no other.
            webhook (ManagedAgentsAutomationWebhookTriggerRequest | Unset): Fires an automation on a verified webhook
                delivery matching its filters. Example: {'continue_filter': {'all': [{'operator': 'equals', 'selector':
                {'body_pointer': 'example', 'header': 'example', 'source': 'body'}, 'value': 'example', 'values':
                ['example']}]}, 'conversation_key': [{'selectors': [{'body_pointer': 'example', 'header': 'example', 'source':
                'body'}]}], 'start_filter': {'all': [{'operator': 'equals', 'selector': {'body_pointer': 'example', 'header':
                'example', 'source': 'body'}, 'value': 'example', 'values': ['example']}]}, 'webhook_endpoint_id':
                '9f8b1c2d-3e4f-5a6b-7c8d-9e0f1a2b3c4d'}.
     """

    display_name: str | Unset = UNSET
    enabled: bool | None | Unset = UNSET
    schedule: ManagedAgentsAutomationScheduleTriggerRequest | Unset = UNSET
    trigger_id: str | Unset = UNSET
    type_: ManagedAgentsAutomationTriggerRequestType | Unset = UNSET
    webhook: ManagedAgentsAutomationWebhookTriggerRequest | Unset = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)





    def to_dict(self) -> dict[str, Any]:
        from ..models.managed_agents_automation_schedule_trigger_request import ManagedAgentsAutomationScheduleTriggerRequest # noqa: PLC0415
        from ..models.managed_agents_automation_webhook_trigger_request import ManagedAgentsAutomationWebhookTriggerRequest # noqa: PLC0415
        display_name = self.display_name

        enabled: bool | None | Unset
        if isinstance(self.enabled, Unset):
            enabled = UNSET
        else:
            enabled = self.enabled

        schedule: dict[str, Any] | Unset = UNSET
        if not isinstance(self.schedule, Unset):
            schedule = self.schedule.to_dict()

        trigger_id = self.trigger_id

        type_: str | Unset = UNSET
        if not isinstance(self.type_, Unset):
            type_ = self.type_.value


        webhook: dict[str, Any] | Unset = UNSET
        if not isinstance(self.webhook, Unset):
            webhook = self.webhook.to_dict()


        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({
        })
        if display_name is not UNSET:
            field_dict["display_name"] = display_name
        if enabled is not UNSET:
            field_dict["enabled"] = enabled
        if schedule is not UNSET:
            field_dict["schedule"] = schedule
        if trigger_id is not UNSET:
            field_dict["trigger_id"] = trigger_id
        if type_ is not UNSET:
            field_dict["type"] = type_
        if webhook is not UNSET:
            field_dict["webhook"] = webhook

        return field_dict



    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.managed_agents_automation_schedule_trigger_request import ManagedAgentsAutomationScheduleTriggerRequest # noqa: PLC0415
        from ..models.managed_agents_automation_webhook_trigger_request import ManagedAgentsAutomationWebhookTriggerRequest # noqa: PLC0415
        d = dict(src_dict)
        display_name = d.pop("display_name", UNSET)

        def _parse_enabled(data: object) -> bool | None | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(bool | None | Unset, data)

        enabled = _parse_enabled(d.pop("enabled", UNSET))


        _schedule = d.pop("schedule", UNSET)
        schedule: ManagedAgentsAutomationScheduleTriggerRequest | Unset
        if isinstance(_schedule,  Unset):
            schedule = UNSET
        else:
            schedule = ManagedAgentsAutomationScheduleTriggerRequest.from_dict(_schedule)




        trigger_id = d.pop("trigger_id", UNSET)

        _type_ = d.pop("type", UNSET)
        type_: ManagedAgentsAutomationTriggerRequestType | Unset
        if isinstance(_type_,  Unset):
            type_ = UNSET
        else:
            type_ = ManagedAgentsAutomationTriggerRequestType(_type_)




        _webhook = d.pop("webhook", UNSET)
        webhook: ManagedAgentsAutomationWebhookTriggerRequest | Unset
        if isinstance(_webhook,  Unset):
            webhook = UNSET
        else:
            webhook = ManagedAgentsAutomationWebhookTriggerRequest.from_dict(_webhook)




        managed_agents_automation_trigger_request = cls(
            display_name=display_name,
            enabled=enabled,
            schedule=schedule,
            trigger_id=trigger_id,
            type_=type_,
            webhook=webhook,
        )


        managed_agents_automation_trigger_request.additional_properties = d
        return managed_agents_automation_trigger_request

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
