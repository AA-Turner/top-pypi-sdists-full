from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar, BinaryIO, TextIO, TYPE_CHECKING, Generator

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

from ..models.managed_agents_automation_definition_schedule_status_synchronization import ManagedAgentsAutomationDefinitionScheduleStatusSynchronization
from typing import cast
from uuid import UUID
import datetime






T = TypeVar("T", bound="ManagedAgentsAutomationDefinitionScheduleStatus")



@_attrs_define
class ManagedAgentsAutomationDefinitionScheduleStatus:
    """ Synchronization, availability, occurrence previews and counters for one schedule trigger.

        Example:
            {'available': True, 'lastRunAt': '2026-02-18T09:30:00Z', 'missedCatchupWindow': 1, 'nextRunAt':
                '2026-02-18T09:30:00Z', 'paused': True, 'skippedOverlap': 1, 'synchronization': 'pending', 'triggerId':
                '9f8b1c2d-3e4f-5a6b-7c8d-9e0f1a2b3c4d', 'upcomingRuns': ['2026-02-18T09:30:00Z']}

        Attributes:
            available (bool): Whether live scheduler state was read successfully.
            last_run_at (datetime.datetime | None): Latest actual scheduler action, or null when unknown.
            missed_catchup_window (int): Occurrences outside the scheduler catch-up window.
            next_run_at (datetime.datetime | None): Next scheduler occurrence, or null when unavailable or paused.
            paused (bool): Whether this schedule is paused by its automation or trigger.
            skipped_overlap (int): Occurrences skipped because an earlier execution was active.
            synchronization (ManagedAgentsAutomationDefinitionScheduleStatusSynchronization): Delivery of saved
                configuration to the scheduler.
            trigger_id (UUID): Schedule trigger identifier.
            upcoming_runs (list[datetime.datetime]): Bounded scheduler preview; empty when unavailable or paused.
     """

    available: bool
    last_run_at: datetime.datetime | None
    missed_catchup_window: int
    next_run_at: datetime.datetime | None
    paused: bool
    skipped_overlap: int
    synchronization: ManagedAgentsAutomationDefinitionScheduleStatusSynchronization
    trigger_id: UUID
    upcoming_runs: list[datetime.datetime]





    def to_dict(self) -> dict[str, Any]:
        available = self.available

        last_run_at: None | str
        if isinstance(self.last_run_at, datetime.datetime):
            last_run_at = self.last_run_at.isoformat()
        else:
            last_run_at = self.last_run_at

        missed_catchup_window = self.missed_catchup_window

        next_run_at: None | str
        if isinstance(self.next_run_at, datetime.datetime):
            next_run_at = self.next_run_at.isoformat()
        else:
            next_run_at = self.next_run_at

        paused = self.paused

        skipped_overlap = self.skipped_overlap

        synchronization = self.synchronization.value

        trigger_id = str(self.trigger_id)

        upcoming_runs = []
        for upcoming_runs_item_data in self.upcoming_runs:
            upcoming_runs_item = upcoming_runs_item_data.isoformat()
            upcoming_runs.append(upcoming_runs_item)




        field_dict: dict[str, Any] = {}

        field_dict.update({
            "available": available,
            "lastRunAt": last_run_at,
            "missedCatchupWindow": missed_catchup_window,
            "nextRunAt": next_run_at,
            "paused": paused,
            "skippedOverlap": skipped_overlap,
            "synchronization": synchronization,
            "triggerId": trigger_id,
            "upcomingRuns": upcoming_runs,
        })

        return field_dict



    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        available = d.pop("available")

        def _parse_last_run_at(data: object) -> datetime.datetime | None:
            if data is None:
                return data
            try:
                if not isinstance(data, str):
                    raise TypeError()
                last_run_at_type_1 = datetime.datetime.fromisoformat(data)



                return last_run_at_type_1
            except (TypeError, ValueError, AttributeError, KeyError):
                pass
            return cast(datetime.datetime | None, data)

        last_run_at = _parse_last_run_at(d.pop("lastRunAt"))


        missed_catchup_window = d.pop("missedCatchupWindow")

        def _parse_next_run_at(data: object) -> datetime.datetime | None:
            if data is None:
                return data
            try:
                if not isinstance(data, str):
                    raise TypeError()
                next_run_at_type_1 = datetime.datetime.fromisoformat(data)



                return next_run_at_type_1
            except (TypeError, ValueError, AttributeError, KeyError):
                pass
            return cast(datetime.datetime | None, data)

        next_run_at = _parse_next_run_at(d.pop("nextRunAt"))


        paused = d.pop("paused")

        skipped_overlap = d.pop("skippedOverlap")

        synchronization = ManagedAgentsAutomationDefinitionScheduleStatusSynchronization(d.pop("synchronization"))




        trigger_id = UUID(d.pop("triggerId"))




        upcoming_runs = []
        _upcoming_runs = d.pop("upcomingRuns")
        for upcoming_runs_item_data in (_upcoming_runs):
            upcoming_runs_item = datetime.datetime.fromisoformat(upcoming_runs_item_data)



            upcoming_runs.append(upcoming_runs_item)


        managed_agents_automation_definition_schedule_status = cls(
            available=available,
            last_run_at=last_run_at,
            missed_catchup_window=missed_catchup_window,
            next_run_at=next_run_at,
            paused=paused,
            skipped_overlap=skipped_overlap,
            synchronization=synchronization,
            trigger_id=trigger_id,
            upcoming_runs=upcoming_runs,
        )

        return managed_agents_automation_definition_schedule_status

