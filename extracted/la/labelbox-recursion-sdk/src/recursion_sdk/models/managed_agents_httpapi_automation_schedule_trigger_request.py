from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar, BinaryIO, TextIO, TYPE_CHECKING, Generator

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

from ..models.managed_agents_httpapi_automation_schedule_trigger_request_type import ManagedAgentsHttpapiAutomationScheduleTriggerRequestType
from typing import cast
from uuid import UUID

if TYPE_CHECKING:
  from ..models.managed_agents_automation_schedule_config_request import ManagedAgentsAutomationScheduleConfigRequest





T = TypeVar("T", bound="ManagedAgentsHttpapiAutomationScheduleTriggerRequest")



@_attrs_define
class ManagedAgentsHttpapiAutomationScheduleTriggerRequest:
    """ Closed schedule-trigger configuration.

        Example:
            {'enabled': True, 'schedule': {'catchupWindowSeconds': 10, 'cron': 'example', 'endAt': '2026-02-18T09:30:00Z',
                'jitterSeconds': 1, 'overlapPolicy': 'skip', 'startAt': '2026-02-18T09:30:00Z', 'timezone': 'example'},
                'triggerId': '9f8b1c2d-3e4f-5a6b-7c8d-9e0f1a2b3c4d', 'type': 'schedule'}

        Attributes:
            enabled (bool): Whether this trigger may admit runs while the automation is active.
            schedule (ManagedAgentsAutomationScheduleConfigRequest): Complete canonical schedule configuration. Example:
                {'catchupWindowSeconds': 10, 'cron': 'example', 'endAt': '2026-02-18T09:30:00Z', 'jitterSeconds': 1,
                'overlapPolicy': 'skip', 'startAt': '2026-02-18T09:30:00Z', 'timezone': 'example'}.
            trigger_id (UUID): Caller-generated stable trigger identifier.
            type_ (ManagedAgentsHttpapiAutomationScheduleTriggerRequestType): Schedule trigger discriminant.
     """

    enabled: bool
    schedule: ManagedAgentsAutomationScheduleConfigRequest
    trigger_id: UUID
    type_: ManagedAgentsHttpapiAutomationScheduleTriggerRequestType





    def to_dict(self) -> dict[str, Any]:
        from ..models.managed_agents_automation_schedule_config_request import ManagedAgentsAutomationScheduleConfigRequest # noqa: PLC0415
        enabled = self.enabled

        schedule = self.schedule.to_dict()

        trigger_id = str(self.trigger_id)

        type_ = self.type_.value


        field_dict: dict[str, Any] = {}

        field_dict.update({
            "enabled": enabled,
            "schedule": schedule,
            "triggerId": trigger_id,
            "type": type_,
        })

        return field_dict



    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.managed_agents_automation_schedule_config_request import ManagedAgentsAutomationScheduleConfigRequest # noqa: PLC0415
        d = dict(src_dict)
        enabled = d.pop("enabled")

        schedule = ManagedAgentsAutomationScheduleConfigRequest.from_dict(d.pop("schedule"))




        trigger_id = UUID(d.pop("triggerId"))




        type_ = ManagedAgentsHttpapiAutomationScheduleTriggerRequestType(d.pop("type"))




        managed_agents_httpapi_automation_schedule_trigger_request = cls(
            enabled=enabled,
            schedule=schedule,
            trigger_id=trigger_id,
            type_=type_,
        )

        return managed_agents_httpapi_automation_schedule_trigger_request

