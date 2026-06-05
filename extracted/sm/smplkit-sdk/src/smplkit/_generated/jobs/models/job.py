from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar, TYPE_CHECKING

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

from dateutil.parser import isoparse
from typing import cast
from typing import Literal
import datetime

if TYPE_CHECKING:
    from ..models.job_http_configuration import JobHttpConfiguration


T = TypeVar("T", bound="Job")


@_attrs_define
class Job:
    """A scheduled unit of work: an HTTP request run on a schedule.

    The job is the definition; each time it fires the service records a run
    capturing the request, response, timing, and outcome.

        Attributes:
            name (str): Human-readable name for the job.
            schedule (str): When the job runs. One of: an ISO-8601 datetime (a one-off run at that instant), a 5-field cron
                expression evaluated in **UTC** (recurring), or the literal `now` (run once, as soon as possible). A datetime or
                `now` job disables itself after it fires.
            configuration (JobHttpConfiguration): HTTP request a job performs when it fires.

                Extends the shared forwarder configuration with the two fields a scheduled
                job needs beyond a forwarder.
            description (None | str | Unset): Free-text description for the job.
            enabled (bool | Unset): Whether the job is scheduling runs. Set to `false` to pause without deleting. Default:
                True.
            type_ (Literal['http'] | Unset): Job type. Only `http` is supported today. Default: 'http'.
            concurrency_policy (Literal['ALLOW'] | Unset): How overlapping runs are handled. `ALLOW` (the only value today)
                permits them. Default: 'ALLOW'.
            next_run_at (datetime.datetime | None | Unset): The next scheduled fire time. `null` once a one-off job has
                fired.
            created_at (datetime.datetime | None | Unset): When the job was created.
            updated_at (datetime.datetime | None | Unset): When the job was last modified.
            deleted_at (datetime.datetime | None | Unset): When the job was deleted. `null` for active jobs.
            version (int | None | Unset): Monotonic counter incremented on every update, starting at 1.
    """

    name: str
    schedule: str
    configuration: JobHttpConfiguration
    description: None | str | Unset = UNSET
    enabled: bool | Unset = True
    type_: Literal["http"] | Unset = "http"
    concurrency_policy: Literal["ALLOW"] | Unset = "ALLOW"
    next_run_at: datetime.datetime | None | Unset = UNSET
    created_at: datetime.datetime | None | Unset = UNSET
    updated_at: datetime.datetime | None | Unset = UNSET
    deleted_at: datetime.datetime | None | Unset = UNSET
    version: int | None | Unset = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        name = self.name

        schedule = self.schedule

        configuration = self.configuration.to_dict()

        description: None | str | Unset
        if isinstance(self.description, Unset):
            description = UNSET
        else:
            description = self.description

        enabled = self.enabled

        type_ = self.type_

        concurrency_policy = self.concurrency_policy

        next_run_at: None | str | Unset
        if isinstance(self.next_run_at, Unset):
            next_run_at = UNSET
        elif isinstance(self.next_run_at, datetime.datetime):
            next_run_at = self.next_run_at.isoformat()
        else:
            next_run_at = self.next_run_at

        created_at: None | str | Unset
        if isinstance(self.created_at, Unset):
            created_at = UNSET
        elif isinstance(self.created_at, datetime.datetime):
            created_at = self.created_at.isoformat()
        else:
            created_at = self.created_at

        updated_at: None | str | Unset
        if isinstance(self.updated_at, Unset):
            updated_at = UNSET
        elif isinstance(self.updated_at, datetime.datetime):
            updated_at = self.updated_at.isoformat()
        else:
            updated_at = self.updated_at

        deleted_at: None | str | Unset
        if isinstance(self.deleted_at, Unset):
            deleted_at = UNSET
        elif isinstance(self.deleted_at, datetime.datetime):
            deleted_at = self.deleted_at.isoformat()
        else:
            deleted_at = self.deleted_at

        version: int | None | Unset
        if isinstance(self.version, Unset):
            version = UNSET
        else:
            version = self.version

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "name": name,
                "schedule": schedule,
                "configuration": configuration,
            }
        )
        if description is not UNSET:
            field_dict["description"] = description
        if enabled is not UNSET:
            field_dict["enabled"] = enabled
        if type_ is not UNSET:
            field_dict["type"] = type_
        if concurrency_policy is not UNSET:
            field_dict["concurrency_policy"] = concurrency_policy
        if next_run_at is not UNSET:
            field_dict["next_run_at"] = next_run_at
        if created_at is not UNSET:
            field_dict["created_at"] = created_at
        if updated_at is not UNSET:
            field_dict["updated_at"] = updated_at
        if deleted_at is not UNSET:
            field_dict["deleted_at"] = deleted_at
        if version is not UNSET:
            field_dict["version"] = version

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.job_http_configuration import JobHttpConfiguration

        d = dict(src_dict)
        name = d.pop("name")

        schedule = d.pop("schedule")

        configuration = JobHttpConfiguration.from_dict(d.pop("configuration"))

        def _parse_description(data: object) -> None | str | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(None | str | Unset, data)

        description = _parse_description(d.pop("description", UNSET))

        enabled = d.pop("enabled", UNSET)

        type_ = cast(Literal["http"] | Unset, d.pop("type", UNSET))
        if type_ != "http" and not isinstance(type_, Unset):
            raise ValueError(f"type must match const 'http', got '{type_}'")

        concurrency_policy = cast(Literal["ALLOW"] | Unset, d.pop("concurrency_policy", UNSET))
        if concurrency_policy != "ALLOW" and not isinstance(concurrency_policy, Unset):
            raise ValueError(f"concurrency_policy must match const 'ALLOW', got '{concurrency_policy}'")

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

        def _parse_created_at(data: object) -> datetime.datetime | None | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            try:
                if not isinstance(data, str):
                    raise TypeError()
                created_at_type_0 = isoparse(data)

                return created_at_type_0
            except (TypeError, ValueError, AttributeError, KeyError):
                pass
            return cast(datetime.datetime | None | Unset, data)

        created_at = _parse_created_at(d.pop("created_at", UNSET))

        def _parse_updated_at(data: object) -> datetime.datetime | None | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            try:
                if not isinstance(data, str):
                    raise TypeError()
                updated_at_type_0 = isoparse(data)

                return updated_at_type_0
            except (TypeError, ValueError, AttributeError, KeyError):
                pass
            return cast(datetime.datetime | None | Unset, data)

        updated_at = _parse_updated_at(d.pop("updated_at", UNSET))

        def _parse_deleted_at(data: object) -> datetime.datetime | None | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            try:
                if not isinstance(data, str):
                    raise TypeError()
                deleted_at_type_0 = isoparse(data)

                return deleted_at_type_0
            except (TypeError, ValueError, AttributeError, KeyError):
                pass
            return cast(datetime.datetime | None | Unset, data)

        deleted_at = _parse_deleted_at(d.pop("deleted_at", UNSET))

        def _parse_version(data: object) -> int | None | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(int | None | Unset, data)

        version = _parse_version(d.pop("version", UNSET))

        job = cls(
            name=name,
            schedule=schedule,
            configuration=configuration,
            description=description,
            enabled=enabled,
            type_=type_,
            concurrency_policy=concurrency_policy,
            next_run_at=next_run_at,
            created_at=created_at,
            updated_at=updated_at,
            deleted_at=deleted_at,
            version=version,
        )

        job.additional_properties = d
        return job

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
