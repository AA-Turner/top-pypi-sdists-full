from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar, TYPE_CHECKING

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

from dateutil.parser import isoparse
from typing import cast
import datetime

if TYPE_CHECKING:
    from ..models.job_http_configuration import JobHttpConfiguration


T = TypeVar("T", bound="JobEnvironment")


@_attrs_define
class JobEnvironment:
    """Per-environment override for a job's enablement, schedule, and configuration.

    Attributes:
        enabled (bool | Unset): Whether the job schedules runs in this environment. A job runs in an environment only
            via this field; it is disabled in every environment by default. Default: False.
        schedule (None | str | Unset): Per-environment schedule override. Omit to inherit the job's base `schedule`.
            When present, it must be a 5-field cron expression evaluated in **UTC** (e.g. `0 3 * * *`), and is only allowed
            on a recurring (cron) job — it varies the cadence within that environment. It cannot appear on a manual or one-
            off job, and cannot change a job's kind.
        configuration (JobHttpConfiguration | None | Unset): Per-environment HTTP request override. Omit to inherit the
            job's base `configuration`. When present, it fully replaces the base configuration for runs in this environment.
        next_run_at (datetime.datetime | None | Unset): The next scheduled fire time in this environment. `null` when
            the environment is not enabled, or once a one-off run has fired.
    """

    enabled: bool | Unset = False
    schedule: None | str | Unset = UNSET
    configuration: JobHttpConfiguration | None | Unset = UNSET
    next_run_at: datetime.datetime | None | Unset = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        from ..models.job_http_configuration import JobHttpConfiguration

        enabled = self.enabled

        schedule: None | str | Unset
        if isinstance(self.schedule, Unset):
            schedule = UNSET
        else:
            schedule = self.schedule

        configuration: dict[str, Any] | None | Unset
        if isinstance(self.configuration, Unset):
            configuration = UNSET
        elif isinstance(self.configuration, JobHttpConfiguration):
            configuration = self.configuration.to_dict()
        else:
            configuration = self.configuration

        next_run_at: None | str | Unset
        if isinstance(self.next_run_at, Unset):
            next_run_at = UNSET
        elif isinstance(self.next_run_at, datetime.datetime):
            next_run_at = self.next_run_at.isoformat()
        else:
            next_run_at = self.next_run_at

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if enabled is not UNSET:
            field_dict["enabled"] = enabled
        if schedule is not UNSET:
            field_dict["schedule"] = schedule
        if configuration is not UNSET:
            field_dict["configuration"] = configuration
        if next_run_at is not UNSET:
            field_dict["next_run_at"] = next_run_at

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.job_http_configuration import JobHttpConfiguration

        d = dict(src_dict)
        enabled = d.pop("enabled", UNSET)

        def _parse_schedule(data: object) -> None | str | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(None | str | Unset, data)

        schedule = _parse_schedule(d.pop("schedule", UNSET))

        def _parse_configuration(data: object) -> JobHttpConfiguration | None | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            try:
                if not isinstance(data, dict):
                    raise TypeError()
                configuration_type_0 = JobHttpConfiguration.from_dict(data)

                return configuration_type_0
            except (TypeError, ValueError, AttributeError, KeyError):
                pass
            return cast(JobHttpConfiguration | None | Unset, data)

        configuration = _parse_configuration(d.pop("configuration", UNSET))

        def _parse_next_run_at(data: object) -> datetime.datetime | None | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            try:
                if not isinstance(data, str):
                    raise TypeError()
                next_run_at_type_0 = isoparse(data)

                return next_run_at_type_0
            except (TypeError, ValueError, AttributeError, KeyError):
                pass
            return cast(datetime.datetime | None | Unset, data)

        next_run_at = _parse_next_run_at(d.pop("next_run_at", UNSET))

        job_environment = cls(
            enabled=enabled,
            schedule=schedule,
            configuration=configuration,
            next_run_at=next_run_at,
        )

        job_environment.additional_properties = d
        return job_environment

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
