from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar, BinaryIO, TextIO, TYPE_CHECKING, Generator

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

from ..models.managed_agents_automation_schedule_config_overlap_policy import ManagedAgentsAutomationScheduleConfigOverlapPolicy
from ..types import UNSET, Unset
from typing import cast
import datetime






T = TypeVar("T", bound="ManagedAgentsAutomationScheduleConfig")



@_attrs_define
class ManagedAgentsAutomationScheduleConfig:
    """ Complete canonical schedule configuration.

        Example:
            {'catchupWindowSeconds': 10, 'cron': 'example', 'endAt': '2026-02-18T09:30:00Z', 'jitterSeconds': 1,
                'overlapPolicy': 'skip', 'startAt': '2026-02-18T09:30:00Z', 'timezone': 'example'}

        Attributes:
            cron (str): Five-field POSIX cron expression.
            timezone (str): IANA timezone used to interpret the cron expression.
            catchup_window_seconds (int | None | Unset): Maximum age of a missed occurrence eligible for catch-up. Defaults
                to 900. Default: 900.
            end_at (datetime.datetime | None | Unset): Optional inclusive schedule end.
            jitter_seconds (int | None | Unset): Maximum deterministic occurrence jitter in seconds. Defaults to 10; zero
                disables jitter. Default: 10.
            overlap_policy (ManagedAgentsAutomationScheduleConfigOverlapPolicy | Unset): Behavior when an earlier occurrence
                is still running. Defaults to skip. Default: ManagedAgentsAutomationScheduleConfigOverlapPolicy.SKIP.
            start_at (datetime.datetime | None | Unset): Optional inclusive schedule start.
     """

    cron: str
    timezone: str
    catchup_window_seconds: int | None | Unset = 900
    end_at: datetime.datetime | None | Unset = UNSET
    jitter_seconds: int | None | Unset = 10
    overlap_policy: ManagedAgentsAutomationScheduleConfigOverlapPolicy | Unset = ManagedAgentsAutomationScheduleConfigOverlapPolicy.SKIP
    start_at: datetime.datetime | None | Unset = UNSET





    def to_dict(self) -> dict[str, Any]:
        cron = self.cron

        timezone = self.timezone

        catchup_window_seconds: int | None | Unset
        if isinstance(self.catchup_window_seconds, Unset):
            catchup_window_seconds = UNSET
        else:
            catchup_window_seconds = self.catchup_window_seconds

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

        overlap_policy: str | Unset = UNSET
        if not isinstance(self.overlap_policy, Unset):
            overlap_policy = self.overlap_policy.value


        start_at: None | str | Unset
        if isinstance(self.start_at, Unset):
            start_at = UNSET
        elif isinstance(self.start_at, datetime.datetime):
            start_at = self.start_at.isoformat()
        else:
            start_at = self.start_at


        field_dict: dict[str, Any] = {}

        field_dict.update({
            "cron": cron,
            "timezone": timezone,
        })
        if catchup_window_seconds is not UNSET:
            field_dict["catchupWindowSeconds"] = catchup_window_seconds
        if end_at is not UNSET:
            field_dict["endAt"] = end_at
        if jitter_seconds is not UNSET:
            field_dict["jitterSeconds"] = jitter_seconds
        if overlap_policy is not UNSET:
            field_dict["overlapPolicy"] = overlap_policy
        if start_at is not UNSET:
            field_dict["startAt"] = start_at

        return field_dict



    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        cron = d.pop("cron")

        timezone = d.pop("timezone")

        def _parse_catchup_window_seconds(data: object) -> int | None | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(int | None | Unset, data)

        catchup_window_seconds = _parse_catchup_window_seconds(d.pop("catchupWindowSeconds", UNSET))


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

        end_at = _parse_end_at(d.pop("endAt", UNSET))


        def _parse_jitter_seconds(data: object) -> int | None | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(int | None | Unset, data)

        jitter_seconds = _parse_jitter_seconds(d.pop("jitterSeconds", UNSET))


        _overlap_policy = d.pop("overlapPolicy", UNSET)
        overlap_policy: ManagedAgentsAutomationScheduleConfigOverlapPolicy | Unset
        if isinstance(_overlap_policy,  Unset):
            overlap_policy = UNSET
        else:
            overlap_policy = ManagedAgentsAutomationScheduleConfigOverlapPolicy(_overlap_policy)




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

        start_at = _parse_start_at(d.pop("startAt", UNSET))


        managed_agents_automation_schedule_config = cls(
            cron=cron,
            timezone=timezone,
            catchup_window_seconds=catchup_window_seconds,
            end_at=end_at,
            jitter_seconds=jitter_seconds,
            overlap_policy=overlap_policy,
            start_at=start_at,
        )

        return managed_agents_automation_schedule_config

