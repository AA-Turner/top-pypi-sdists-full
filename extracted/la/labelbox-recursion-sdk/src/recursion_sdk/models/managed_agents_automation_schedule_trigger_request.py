from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar, BinaryIO, TextIO, TYPE_CHECKING, Generator

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

from ..models.managed_agents_automation_schedule_trigger_request_overlap_policy import ManagedAgentsAutomationScheduleTriggerRequestOverlapPolicy
from ..types import UNSET, Unset
from typing import cast
import datetime

if TYPE_CHECKING:
  from ..models.managed_agents_schedule_synchronization_request import ManagedAgentsScheduleSynchronizationRequest





T = TypeVar("T", bound="ManagedAgentsAutomationScheduleTriggerRequest")



@_attrs_define
class ManagedAgentsAutomationScheduleTriggerRequest:
    """ Fires an automation using a Temporal Schedule.

        Example:
            {'catchup_window_seconds': 1, 'cron': 'example', 'end_at': '2026-02-18T09:30:00Z', 'jitter_seconds': 1,
                'last_run_at': '2026-02-18T09:30:00Z', 'missed_catchup_window': 1, 'next_run_at': '2026-02-18T09:30:00Z',
                'overlap_policy': 'skip', 'skipped_overlap': 1, 'start_at': '2026-02-18T09:30:00Z', 'synchronization': {'error':
                'example', 'status': 'pending'}, 'timezone': 'example', 'upcoming_runs_at': ['2026-02-18T09:30:00Z']}

        Attributes:
            catchup_window_seconds (int | None | Unset): Replay missed actions within this many seconds, 10–31622400. Omit
                for 900. Deliberate pauses are not backfilled.
            cron (str | Unset): Five-field POSIX cron, at most 256 bytes. Day-of-month and day-of-week use OR when both are
                restricted.
            end_at (datetime.datetime | None | Unset): Inclusive end of the schedule.
            jitter_seconds (int | None | Unset): Maximum per-occurrence jitter in seconds, 0–540. Omit for 10; zero disables
                jitter.
            last_run_at (datetime.datetime | None | Unset): Most recent Temporal action start. Server-assigned.
            missed_catchup_window (int | Unset): Temporal's count of actions outside the catch-up window. Server-assigned.
            next_run_at (datetime.datetime | None | Unset): Next planned Temporal action time, including jitter. Server-
                assigned.
            overlap_policy (ManagedAgentsAutomationScheduleTriggerRequestOverlapPolicy | Unset): Temporal overlap policy,
                covering the session's initial execution. Defaults to skip.
            skipped_overlap (int | Unset): Temporal's count of actions skipped for overlap. Server-assigned.
            start_at (datetime.datetime | None | Unset): Inclusive beginning of the schedule.
            synchronization (ManagedAgentsScheduleSynchronizationRequest | Unset): Delivery status of saved schedule
                configuration, independent of run outcomes. Example: {'error': 'example', 'status': 'pending'}.
            timezone (str | Unset): Required IANA timezone for recurring local time. The console supplies the user's browser
                timezone; API clients supply the intended user's timezone. Nonexistent local times are skipped; repeated local
                times fire twice.
            upcoming_runs_at (list[datetime.datetime] | Unset): Upcoming planned Temporal action times, including jitter.
                Server-assigned.
     """

    catchup_window_seconds: int | None | Unset = UNSET
    cron: str | Unset = UNSET
    end_at: datetime.datetime | None | Unset = UNSET
    jitter_seconds: int | None | Unset = UNSET
    last_run_at: datetime.datetime | None | Unset = UNSET
    missed_catchup_window: int | Unset = UNSET
    next_run_at: datetime.datetime | None | Unset = UNSET
    overlap_policy: ManagedAgentsAutomationScheduleTriggerRequestOverlapPolicy | Unset = UNSET
    skipped_overlap: int | Unset = UNSET
    start_at: datetime.datetime | None | Unset = UNSET
    synchronization: ManagedAgentsScheduleSynchronizationRequest | Unset = UNSET
    timezone: str | Unset = UNSET
    upcoming_runs_at: list[datetime.datetime] | Unset = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)





    def to_dict(self) -> dict[str, Any]:
        from ..models.managed_agents_schedule_synchronization_request import ManagedAgentsScheduleSynchronizationRequest # noqa: PLC0415
        catchup_window_seconds: int | None | Unset
        if isinstance(self.catchup_window_seconds, Unset):
            catchup_window_seconds = UNSET
        else:
            catchup_window_seconds = self.catchup_window_seconds

        cron = self.cron

        end_at: None | str | Unset
        if isinstance(self.end_at, Unset):
            end_at = UNSET
        elif isinstance(self.end_at, datetime.datetime):
            end_at = self.end_at.isoformat()
        else:
            end_at = self.end_at

        jitter_seconds: int | None | Unset
        if isinstance(self.jitter_seconds, Unset):
            jitter_seconds = UNSET
        else:
            jitter_seconds = self.jitter_seconds

        last_run_at: None | str | Unset
        if isinstance(self.last_run_at, Unset):
            last_run_at = UNSET
        elif isinstance(self.last_run_at, datetime.datetime):
            last_run_at = self.last_run_at.isoformat()
        else:
            last_run_at = self.last_run_at

        missed_catchup_window = self.missed_catchup_window

        next_run_at: None | str | Unset
        if isinstance(self.next_run_at, Unset):
            next_run_at = UNSET
        elif isinstance(self.next_run_at, datetime.datetime):
            next_run_at = self.next_run_at.isoformat()
        else:
            next_run_at = self.next_run_at

        overlap_policy: str | Unset = UNSET
        if not isinstance(self.overlap_policy, Unset):
            overlap_policy = self.overlap_policy.value


        skipped_overlap = self.skipped_overlap

        start_at: None | str | Unset
        if isinstance(self.start_at, Unset):
            start_at = UNSET
        elif isinstance(self.start_at, datetime.datetime):
            start_at = self.start_at.isoformat()
        else:
            start_at = self.start_at

        synchronization: dict[str, Any] | Unset = UNSET
        if not isinstance(self.synchronization, Unset):
            synchronization = self.synchronization.to_dict()

        timezone = self.timezone

        upcoming_runs_at: list[str] | Unset = UNSET
        if not isinstance(self.upcoming_runs_at, Unset):
            upcoming_runs_at = []
            for upcoming_runs_at_item_data in self.upcoming_runs_at:
                upcoming_runs_at_item = upcoming_runs_at_item_data.isoformat()
                upcoming_runs_at.append(upcoming_runs_at_item)




        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({
        })
        if catchup_window_seconds is not UNSET:
            field_dict["catchup_window_seconds"] = catchup_window_seconds
        if cron is not UNSET:
            field_dict["cron"] = cron
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
        if timezone is not UNSET:
            field_dict["timezone"] = timezone
        if upcoming_runs_at is not UNSET:
            field_dict["upcoming_runs_at"] = upcoming_runs_at

        return field_dict



    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.managed_agents_schedule_synchronization_request import ManagedAgentsScheduleSynchronizationRequest # noqa: PLC0415
        d = dict(src_dict)
        def _parse_catchup_window_seconds(data: object) -> int | None | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(int | None | Unset, data)

        catchup_window_seconds = _parse_catchup_window_seconds(d.pop("catchup_window_seconds", UNSET))


        cron = d.pop("cron", UNSET)

        def _parse_end_at(data: object) -> datetime.datetime | None | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            try:
                if not isinstance(data, str):
                    raise TypeError()
                end_at_type_1 = datetime.datetime.fromisoformat(data)



                return end_at_type_1
            except (TypeError, ValueError, AttributeError, KeyError):
                pass
            return cast(datetime.datetime | None | Unset, data)

        end_at = _parse_end_at(d.pop("end_at", UNSET))


        def _parse_jitter_seconds(data: object) -> int | None | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(int | None | Unset, data)

        jitter_seconds = _parse_jitter_seconds(d.pop("jitter_seconds", UNSET))


        def _parse_last_run_at(data: object) -> datetime.datetime | None | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            try:
                if not isinstance(data, str):
                    raise TypeError()
                last_run_at_type_1 = datetime.datetime.fromisoformat(data)



                return last_run_at_type_1
            except (TypeError, ValueError, AttributeError, KeyError):
                pass
            return cast(datetime.datetime | None | Unset, data)

        last_run_at = _parse_last_run_at(d.pop("last_run_at", UNSET))


        missed_catchup_window = d.pop("missed_catchup_window", UNSET)

        def _parse_next_run_at(data: object) -> datetime.datetime | None | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            try:
                if not isinstance(data, str):
                    raise TypeError()
                next_run_at_type_1 = datetime.datetime.fromisoformat(data)



                return next_run_at_type_1
            except (TypeError, ValueError, AttributeError, KeyError):
                pass
            return cast(datetime.datetime | None | Unset, data)

        next_run_at = _parse_next_run_at(d.pop("next_run_at", UNSET))


        _overlap_policy = d.pop("overlap_policy", UNSET)
        overlap_policy: ManagedAgentsAutomationScheduleTriggerRequestOverlapPolicy | Unset
        if isinstance(_overlap_policy,  Unset):
            overlap_policy = UNSET
        else:
            overlap_policy = ManagedAgentsAutomationScheduleTriggerRequestOverlapPolicy(_overlap_policy)




        skipped_overlap = d.pop("skipped_overlap", UNSET)

        def _parse_start_at(data: object) -> datetime.datetime | None | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            try:
                if not isinstance(data, str):
                    raise TypeError()
                start_at_type_1 = datetime.datetime.fromisoformat(data)



                return start_at_type_1
            except (TypeError, ValueError, AttributeError, KeyError):
                pass
            return cast(datetime.datetime | None | Unset, data)

        start_at = _parse_start_at(d.pop("start_at", UNSET))


        _synchronization = d.pop("synchronization", UNSET)
        synchronization: ManagedAgentsScheduleSynchronizationRequest | Unset
        if isinstance(_synchronization,  Unset):
            synchronization = UNSET
        else:
            synchronization = ManagedAgentsScheduleSynchronizationRequest.from_dict(_synchronization)




        timezone = d.pop("timezone", UNSET)

        _upcoming_runs_at = d.pop("upcoming_runs_at", UNSET)
        upcoming_runs_at: list[datetime.datetime] | Unset = UNSET
        if _upcoming_runs_at is not UNSET:
            upcoming_runs_at = []
            for upcoming_runs_at_item_data in _upcoming_runs_at:
                upcoming_runs_at_item = datetime.datetime.fromisoformat(upcoming_runs_at_item_data)



                upcoming_runs_at.append(upcoming_runs_at_item)


        managed_agents_automation_schedule_trigger_request = cls(
            catchup_window_seconds=catchup_window_seconds,
            cron=cron,
            end_at=end_at,
            jitter_seconds=jitter_seconds,
            last_run_at=last_run_at,
            missed_catchup_window=missed_catchup_window,
            next_run_at=next_run_at,
            overlap_policy=overlap_policy,
            skipped_overlap=skipped_overlap,
            start_at=start_at,
            synchronization=synchronization,
            timezone=timezone,
            upcoming_runs_at=upcoming_runs_at,
        )


        managed_agents_automation_schedule_trigger_request.additional_properties = d
        return managed_agents_automation_schedule_trigger_request

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
