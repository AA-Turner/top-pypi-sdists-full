from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar, TYPE_CHECKING

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

from ..models.job_kind_type_0 import check_job_kind_type_0
from ..models.job_kind_type_0 import JobKindType0
from dateutil.parser import isoparse
from typing import cast
from typing import Literal
import datetime

if TYPE_CHECKING:
    from ..models.job_environments import JobEnvironments
    from ..models.job_http_configuration import JobHttpConfiguration


T = TypeVar("T", bound="Job")


@_attrs_define
class Job:
    """A unit of work: an HTTP request, run on a schedule or triggered on demand.

    The job is the definition; each time it fires the service records a run
    capturing the request, response, timing, and outcome. A job runs per
    environment: set `environments[<env>].enabled` to enable it there, and
    optionally give that environment its own `schedule` or `configuration`.

    A job's `kind` follows from its `schedule`: a **recurring** (cron) job may
    be enabled in several environments at once and fires once per enabled
    environment, each on its own next-fire schedule; a **manual** job (no
    schedule) is permanent and never auto-fires — it runs only when triggered;
    a **one-off** (`now` or a future datetime) job runs a single time in the
    environment it was created in and is then spent.

        Attributes:
            name (str): Human-readable name for the job.
            configuration (JobHttpConfiguration): HTTP request a job performs when it fires.

                Extends the shared forwarder configuration with the two fields a scheduled
                job needs beyond a forwarder.
            description (None | str | Unset): Free-text description for the job.
            type_ (Literal['http'] | Unset): Job type. Only `http` is supported today. Default: 'http'.
            schedule (None | str | Unset): The base schedule every environment inherits unless it overrides it, and the
                field that determines the job's `kind`. Omit it (or send `null`) to create a permanent **manual** job that never
                auto-fires and runs only when triggered. Provide a 5-field cron expression evaluated in **UTC** for a
                **recurring** job, an ISO-8601 datetime for a **one-off** run at that instant, or the literal `now` for a one-
                off run as soon as possible. A datetime or `now` job disables itself after it fires.
            environments (JobEnvironments | Unset): Per-environment overrides keyed by environment key (e.g. `production`,
                `staging`). Each entry sets `enabled` (whether the job is enabled — scheduled, for a recurring job, or
                triggerable, for a manual job — in that environment), an optional `schedule` override (a cron expression for
                recurring jobs; omit to inherit the base `schedule`), and an optional `configuration` override (omit to inherit
                the base `configuration`); it also reports the read-only `next_run_at` for that environment. A job with no entry
                for an environment is disabled there. For a recurring or manual job, supply this map to choose where it runs.
                For a one-off job, the environment it is created in is recorded here automatically — name it with the
                `X-Smplkit-Environment` header. Every referenced environment must exist for the account.
            concurrency_policy (Literal['ALLOW'] | Unset): How overlapping runs are handled. `ALLOW` (the only value today)
                permits them. Default: 'ALLOW'.
            kind (JobKindType0 | None | Unset): How the job runs, derived from its base `schedule`: `recurring` for a cron
                schedule (fires on a repeating cadence), `manual` for no schedule (never auto-fires; runs only when triggered),
                or `one_off` for a `now` or datetime schedule (runs a single time, then is spent).
            created_at (datetime.datetime | None | Unset): When the job was created.
            updated_at (datetime.datetime | None | Unset): When the job was last modified.
            deleted_at (datetime.datetime | None | Unset): When the job was deleted. `null` for active jobs.
            version (int | None | Unset): Monotonic counter incremented on every update, starting at 1.
    """

    name: str
    configuration: JobHttpConfiguration
    description: None | str | Unset = UNSET
    type_: Literal["http"] | Unset = "http"
    schedule: None | str | Unset = UNSET
    environments: JobEnvironments | Unset = UNSET
    concurrency_policy: Literal["ALLOW"] | Unset = "ALLOW"
    kind: JobKindType0 | None | Unset = UNSET
    created_at: datetime.datetime | None | Unset = UNSET
    updated_at: datetime.datetime | None | Unset = UNSET
    deleted_at: datetime.datetime | None | Unset = UNSET
    version: int | None | Unset = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        name = self.name

        configuration = self.configuration.to_dict()

        description: None | str | Unset
        if isinstance(self.description, Unset):
            description = UNSET
        else:
            description = self.description

        type_ = self.type_

        schedule: None | str | Unset
        if isinstance(self.schedule, Unset):
            schedule = UNSET
        else:
            schedule = self.schedule

        environments: dict[str, Any] | Unset = UNSET
        if not isinstance(self.environments, Unset):
            environments = self.environments.to_dict()

        concurrency_policy = self.concurrency_policy

        kind: None | str | Unset
        if isinstance(self.kind, Unset):
            kind = UNSET
        elif isinstance(self.kind, str):
            kind = self.kind
        else:
            kind = self.kind

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
                "configuration": configuration,
            }
        )
        if description is not UNSET:
            field_dict["description"] = description
        if type_ is not UNSET:
            field_dict["type"] = type_
        if schedule is not UNSET:
            field_dict["schedule"] = schedule
        if environments is not UNSET:
            field_dict["environments"] = environments
        if concurrency_policy is not UNSET:
            field_dict["concurrency_policy"] = concurrency_policy
        if kind is not UNSET:
            field_dict["kind"] = kind
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
        from ..models.job_environments import JobEnvironments
        from ..models.job_http_configuration import JobHttpConfiguration

        d = dict(src_dict)
        name = d.pop("name")

        configuration = JobHttpConfiguration.from_dict(d.pop("configuration"))

        def _parse_description(data: object) -> None | str | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(None | str | Unset, data)

        description = _parse_description(d.pop("description", UNSET))

        type_ = cast(Literal["http"] | Unset, d.pop("type", UNSET))
        if type_ != "http" and not isinstance(type_, Unset):
            raise ValueError(f"type must match const 'http', got '{type_}'")

        def _parse_schedule(data: object) -> None | str | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(None | str | Unset, data)

        schedule = _parse_schedule(d.pop("schedule", UNSET))

        _environments = d.pop("environments", UNSET)
        environments: JobEnvironments | Unset
        if isinstance(_environments, Unset):
            environments = UNSET
        else:
            environments = JobEnvironments.from_dict(_environments)

        concurrency_policy = cast(Literal["ALLOW"] | Unset, d.pop("concurrency_policy", UNSET))
        if concurrency_policy != "ALLOW" and not isinstance(concurrency_policy, Unset):
            raise ValueError(f"concurrency_policy must match const 'ALLOW', got '{concurrency_policy}'")

        def _parse_kind(data: object) -> JobKindType0 | None | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            try:
                if not isinstance(data, str):
                    raise TypeError()
                kind_type_0 = check_job_kind_type_0(data)

                return kind_type_0
            except (TypeError, ValueError, AttributeError, KeyError):
                pass
            return cast(JobKindType0 | None | Unset, data)

        kind = _parse_kind(d.pop("kind", UNSET))

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
            configuration=configuration,
            description=description,
            type_=type_,
            schedule=schedule,
            environments=environments,
            concurrency_policy=concurrency_policy,
            kind=kind,
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
