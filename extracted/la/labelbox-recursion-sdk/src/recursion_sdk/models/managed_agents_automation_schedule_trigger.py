from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar, BinaryIO, TextIO, TYPE_CHECKING, Generator

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

from ..models.managed_agents_automation_schedule_trigger_overlap_policy import ManagedAgentsAutomationScheduleTriggerOverlapPolicy
from ..types import UNSET, Unset
from typing import cast
import datetime

if TYPE_CHECKING:
  from ..models.managed_agents_schedule_synchronization import ManagedAgentsScheduleSynchronization





T = TypeVar("T", bound="ManagedAgentsAutomationScheduleTrigger")



@_attrs_define
class ManagedAgentsAutomationScheduleTrigger:
    """ Fires an automation using a Temporal Schedule.

        Example:
            {'catchup_window_seconds': 1, 'cron': 'example', 'end_at': '2026-02-18T09:30:00Z', 'jitter_seconds': 1,
                'last_run_at': '2026-02-18T09:30:00Z', 'missed_catchup_window': 1, 'next_run_at': '2026-02-18T09:30:00Z',
                'overlap_policy': 'skip', 'skipped_overlap': 1, 'start_at': '2026-02-18T09:30:00Z', 'synchronization': {'error':
                'example', 'status': 'pending'}, 'timezone': 'example', 'upcoming_runs_at': ['2026-02-18T09:30:00Z']}

        Attributes:
            cron (str): Five-field POSIX cron, at most 256 bytes. Day-of-month and day-of-week use OR when both are
                restricted.
            timezone (str): Required IANA timezone for recurring local time. The console supplies the user's browser
                timezone; API clients supply the intended user's timezone. Nonexistent local times are skipped; repeated local
                times fire twice.
            catchup_window_seconds (int | Unset): Replay missed actions within this many seconds, 10–31622400. Omit for 900.
                Deliberate pauses are not backfilled.
            end_at (datetime.datetime | Unset): Inclusive end of the schedule.
            jitter_seconds (int | Unset): Maximum per-occurrence jitter in seconds, 0–540. Omit for 10; zero disables
                jitter.
            last_run_at (datetime.datetime | Unset): Most recent Temporal action start. Server-assigned.
            missed_catchup_window (int | Unset): Temporal's count of actions outside the catch-up window. Server-assigned.
            next_run_at (datetime.datetime | Unset): Next planned Temporal action time, including jitter. Server-assigned.
            overlap_policy (ManagedAgentsAutomationScheduleTriggerOverlapPolicy | Unset): Temporal overlap policy, covering
                the session's initial execution. Defaults to skip.
            skipped_overlap (int | Unset): Temporal's count of actions skipped for overlap. Server-assigned.
            start_at (datetime.datetime | Unset): Inclusive beginning of the schedule.
            synchronization (ManagedAgentsScheduleSynchronization | Unset): Delivery status of saved schedule configuration,
                independent of run outcomes. Example: {'error': 'example', 'status': 'pending'}.
            upcoming_runs_at (list[datetime.datetime] | Unset): Upcoming planned Temporal action times, including jitter.
                Server-assigned.
     """

    cron: str
    timezone: str
    catchup_window_seconds: int | Unset = UNSET
    end_at: datetime.datetime | Unset = UNSET
    jitter_seconds: int | Unset = UNSET
    last_run_at: datetime.datetime | Unset = UNSET
    missed_catchup_window: int | Unset = UNSET
    next_run_at: datetime.datetime | Unset = UNSET
    overlap_policy: ManagedAgentsAutomationScheduleTriggerOverlapPolicy | Unset = UNSET
    skipped_overlap: int | Unset = UNSET
    start_at: datetime.datetime | Unset = UNSET
    synchronization: ManagedAgentsScheduleSynchronization | Unset = UNSET
    upcoming_runs_at: list[datetime.datetime] | Unset = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)





    def to_dict(self) -> dict[str, Any]:
        from ..models.managed_agents_schedule_synchronization import ManagedAgentsScheduleSynchronization # noqa: PLC0415
        cron = self.cron

        timezone = self.timezone

        catchup_window_seconds = self.catchup_window_seconds

        end_at: str | Unset = UNSET
        if not isinstance(self.end_at, Unset):
            end_at = self.end_at.isoformat()

        jitter_seconds = self.jitter_seconds

        last_run_at: str | Unset = UNSET
        if not isinstance(self.last_run_at, Unset):
            last_run_at = self.last_run_at.isoformat()

        missed_catchup_window = self.missed_catchup_window

        next_run_at: str | Unset = UNSET
        if not isinstance(self.next_run_at, Unset):
            next_run_at = self.next_run_at.isoformat()

        overlap_policy: str | Unset = UNSET
        if not isinstance(self.overlap_policy, Unset):
            overlap_policy = self.overlap_policy.value


        skipped_overlap = self.skipped_overlap

        start_at: str | Unset = UNSET
        if not isinstance(self.start_at, Unset):
            start_at = self.start_at.isoformat()

        synchronization: dict[str, Any] | Unset = UNSET
        if not isinstance(self.synchronization, Unset):
            synchronization = self.synchronization.to_dict()

        upcoming_runs_at: list[str] | Unset = UNSET
        if not isinstance(self.upcoming_runs_at, Unset):
            upcoming_runs_at = []
            for upcoming_runs_at_item_data in self.upcoming_runs_at:
                upcoming_runs_at_item = upcoming_runs_at_item_data.isoformat()
                upcoming_runs_at.append(upcoming_runs_at_item)




        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({
            "cron": cron,
            "timezone": timezone,
        })
        if catchup_window_seconds is not UNSET:
            field_dict["catchup_window_seconds"] = catchup_window_seconds
        if end_at is not UNSET:
            field_dict["end_at"] = end_at
        if jitter_seconds is not UNSET:
            field_dict["jitter_seconds"] = jitter_seconds
        if last_run_at is not UNSET:
            field_dict["last_run_at"] = last_run_at
        if missed_catchup_window is not UNSET:
            field_dict["missed_catchup_window"] = missed_catchup_window
        if next_run_at is not UNSET:
            field_dict["next_run_at"] = next_run_at
        if overlap_policy is not UNSET:
            field_dict["overlap_policy"] = overlap_policy
        if skipped_overlap is not UNSET:
            field_dict["skipped_overlap"] = skipped_overlap
        if start_at is not UNSET:
            field_dict["start_at"] = start_at
        if synchronization is not UNSET:
            field_dict["synchronization"] = synchronization
        if upcoming_runs_at is not UNSET:
            field_dict["upcoming_runs_at"] = upcoming_runs_at

        return field_dict



    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.managed_agents_schedule_synchronization import ManagedAgentsScheduleSynchronization # noqa: PLC0415
        d = dict(src_dict)
        cron = d.pop("cron")

        timezone = d.pop("timezone")

        catchup_window_seconds = d.pop("catchup_window_seconds", UNSET)

        _end_at = d.pop("end_at", UNSET)
        end_at: datetime.datetime | Unset
        if isinstance(_end_at,  Unset):
            end_at = UNSET
        else:
            end_at = datetime.datetime.fromisoformat(_end_at)




        jitter_seconds = d.pop("jitter_seconds", UNSET)

        _last_run_at = d.pop("last_run_at", UNSET)
        last_run_at: datetime.datetime | Unset
        if isinstance(_last_run_at,  Unset):
            last_run_at = UNSET
        else:
            last_run_at = datetime.datetime.fromisoformat(_last_run_at)




        missed_catchup_window = d.pop("missed_catchup_window", UNSET)

        _next_run_at = d.pop("next_run_at", UNSET)
        next_run_at: datetime.datetime | Unset
        if isinstance(_next_run_at,  Unset):
            next_run_at = UNSET
        else:
            next_run_at = datetime.datetime.fromisoformat(_next_run_at)




        _overlap_policy = d.pop("overlap_policy", UNSET)
        overlap_policy: ManagedAgentsAutomationScheduleTriggerOverlapPolicy | Unset
        if isinstance(_overlap_policy,  Unset):
            overlap_policy = UNSET
        else:
            overlap_policy = ManagedAgentsAutomationScheduleTriggerOverlapPolicy(_overlap_policy)




        skipped_overlap = d.pop("skipped_overlap", UNSET)

        _start_at = d.pop("start_at", UNSET)
        start_at: datetime.datetime | Unset
        if isinstance(_start_at,  Unset):
            start_at = UNSET
        else:
            start_at = datetime.datetime.fromisoformat(_start_at)




        _synchronization = d.pop("synchronization", UNSET)
        synchronization: ManagedAgentsScheduleSynchronization | Unset
        if isinstance(_synchronization,  Unset):
            synchronization = UNSET
        else:
            synchronization = ManagedAgentsScheduleSynchronization.from_dict(_synchronization)




        _upcoming_runs_at = d.pop("upcoming_runs_at", UNSET)
        upcoming_runs_at: list[datetime.datetime] | Unset = UNSET
        if _upcoming_runs_at is not UNSET:
            upcoming_runs_at = []
            for upcoming_runs_at_item_data in _upcoming_runs_at:
                upcoming_runs_at_item = datetime.datetime.fromisoformat(upcoming_runs_at_item_data)



                upcoming_runs_at.append(upcoming_runs_at_item)


        managed_agents_automation_schedule_trigger = cls(
            cron=cron,
            timezone=timezone,
            catchup_window_seconds=catchup_window_seconds,
            end_at=end_at,
            jitter_seconds=jitter_seconds,
            last_run_at=last_run_at,
            missed_catchup_window=missed_catchup_window,
            next_run_at=next_run_at,
            overlap_policy=overlap_policy,
            skipped_overlap=skipped_overlap,
            start_at=start_at,
            synchronization=synchronization,
            upcoming_runs_at=upcoming_runs_at,
        )


        managed_agents_automation_schedule_trigger.additional_properties = d
        return managed_agents_automation_schedule_trigger

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
