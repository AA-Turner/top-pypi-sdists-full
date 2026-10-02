from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar, BinaryIO, TextIO, TYPE_CHECKING, Generator

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

from typing import cast
from uuid import UUID

if TYPE_CHECKING:
  from ..models.managed_agents_automation_definition_schedule_status import ManagedAgentsAutomationDefinitionScheduleStatus





T = TypeVar("T", bound="ManagedAgentsAutomationDefinitionRuntimeStatus")



@_attrs_define
class ManagedAgentsAutomationDefinitionRuntimeStatus:
    """ Read-only scheduler state for a canonical automation, independent of its writable definition.

        Example:
            {'automationId': '9f8b1c2d-3e4f-5a6b-7c8d-9e0f1a2b3c4d', 'triggers': [{'available': True, 'lastRunAt':
                '2026-02-18T09:30:00Z', 'missedCatchupWindow': 1, 'nextRunAt': '2026-02-18T09:30:00Z', 'paused': True,
                'skippedOverlap': 1, 'synchronization': 'pending', 'triggerId': '9f8b1c2d-3e4f-5a6b-7c8d-9e0f1a2b3c4d',
                'upcomingRuns': ['2026-02-18T09:30:00Z']}]}

        Attributes:
            automation_id (UUID): Automation whose scheduler state was read.
            triggers (list[ManagedAgentsAutomationDefinitionScheduleStatus]): Runtime status of each configured schedule
                trigger.
     """

    automation_id: UUID
    triggers: list[ManagedAgentsAutomationDefinitionScheduleStatus]





    def to_dict(self) -> dict[str, Any]:
        from ..models.managed_agents_automation_definition_schedule_status import ManagedAgentsAutomationDefinitionScheduleStatus # noqa: PLC0415
        automation_id = str(self.automation_id)

        triggers = []
        for triggers_item_data in self.triggers:
            triggers_item = triggers_item_data.to_dict()
            triggers.append(triggers_item)




        field_dict: dict[str, Any] = {}

        field_dict.update({
            "automationId": automation_id,
            "triggers": triggers,
        })

        return field_dict



    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.managed_agents_automation_definition_schedule_status import ManagedAgentsAutomationDefinitionScheduleStatus # noqa: PLC0415
        d = dict(src_dict)
        automation_id = UUID(d.pop("automationId"))




        triggers = []
        _triggers = d.pop("triggers")
        for triggers_item_data in (_triggers):
            triggers_item = ManagedAgentsAutomationDefinitionScheduleStatus.from_dict(triggers_item_data)



            triggers.append(triggers_item)


        managed_agents_automation_definition_runtime_status = cls(
            automation_id=automation_id,
            triggers=triggers,
        )

        return managed_agents_automation_definition_runtime_status

