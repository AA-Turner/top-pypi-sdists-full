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
                job needs beyond a forwarder, and represents headers as a name→value object
                so an individual header can be overridden per environment by its name.
            description (None | str | Unset): Free-text description for the job.
            type_ (Literal['http'] | Unset): Job type. Only `http` is supported today. Default: 'http'.
            schedule (None | str | Unset): The base schedule every environment inherits unless it overrides it, and the
                field that determines the job's `kind`. Omit it (or send `null`) to create a permanent **manual** job that never
                auto-fires and runs only when triggered. Provide a 5-field cron expression evaluated in the job's `timezone`
                (UTC by default) for a **recurring** job, an ISO-8601 datetime for a **one-off** run at that instant, or the
                literal `now` for a one-off run as soon as possible. A datetime or `now` job disables itself after it fires.
            timezone (None | str | Unset): IANA timezone the cron `schedule` is evaluated in (e.g. `America/New_York`); null
                or omitted means UTC. The base every environment inherits unless it sets its own `timezone`. The cron fires on
                this zone's wall clock (DST-aware) while `next_run_at` is still reported as a UTC instant. Only valid on a
                recurring (cron) job — it cannot be set on a manual or one-off job.
            environments (JobEnvironments | Unset): Per-environment overrides keyed by environment key (e.g. `production`,
                `staging`). Each entry is a flat, sparse overlay: only the leaves that differ from the base definition are
                present, and everything absent is inherited. Set `enabled` to `true` to run the job in that environment (the
                base is disabled everywhere; an environment with no entry, or an entry without `enabled: true`, does not run).
                Overridable leaves are `url`, `method`, `timeout`, `body`, `success_status`, `tls_verify`, `ca_cert`, `schedule`
                and `timezone` (recurring jobs only), `retry_policy` (the `id` of a retry policy, or `Default`), and an
                individual header as `headers.<name>` (e.g. `headers.Authorization`). On read, each entry also reports the read-
                only `next_run_at` for that environment (the next fire time, or `null`). For a recurring or manual job, supply
                this map to choose where it runs. For a one-off job, the environment it is created in is recorded here
                automatically — name it with the `X-Smplkit-Environment` header. Every referenced environment must exist for the
                account.
            concurrency_policy (Literal['ALLOW'] | Unset): How overlapping runs are handled. `ALLOW` (the only value today)
                permits them. Default: 'ALLOW'.
            retry_policy (None | str | Unset): The base retry policy for failed runs — the `id` of a retry policy (or the
                built-in `Default`), overridable per environment. Omit (or send `null`) to use `Default`, which never retries —
                so a job that sets nothing behaves exactly as before retries existed.
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
    timezone: None | str | Unset = UNSET
    environments: JobEnvironments | Unset = UNSET
    concurrency_policy: Literal["ALLOW"] | Unset = "ALLOW"
    retry_policy: None | str | Unset = UNSET
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

        timezone: None | str | Unset
        if isinstance(self.timezone, Unset):
            timezone = UNSET
        else:
            timezone = self.timezone

        environments: dict[str, Any] | Unset = UNSET
        if not isinstance(self.environments, Unset):
            environments = self.environments.to_dict()

        concurrency_policy = self.concurrency_policy

        retry_policy: None | str | Unset
        if isinstance(self.retry_policy, Unset):
            retry_policy = UNSET
        else:
            retry_policy = self.retry_policy

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
        if timezone is not UNSET:
            field_dict["timezone"] = timezone
        if environments is not UNSET:
            field_dict["environments"] = environments
        if concurrency_policy is not UNSET:
            field_dict["concurrency_policy"] = concurrency_policy
        if retry_policy is not UNSET:
            field_dict["retry_policy"] = retry_policy
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

        def _parse_timezone(data: object) -> None | str | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(None | str | Unset, data)

        timezone = _parse_timezone(d.pop("timezone", UNSET))

        _environments = d.pop("environments", UNSET)
        environments: JobEnvironments | Unset
        if isinstance(_environments, Unset):
            environments = UNSET
        else:
            environments = JobEnvironments.from_dict(_environments)

        concurrency_policy = cast(Literal["ALLOW"] | Unset, d.pop("concurrency_policy", UNSET))
        if concurrency_policy != "ALLOW" and not isinstance(concurrency_policy, Unset):
            raise ValueError(f"concurrency_policy must match const 'ALLOW', got '{concurrency_policy}'")

        def _parse_retry_policy(data: object) -> None | str | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(None | str | Unset, data)

        retry_policy = _parse_retry_policy(d.pop("retry_policy", UNSET))

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
            timezone=timezone,
            environments=environments,
            concurrency_policy=concurrency_policy,
            retry_policy=retry_policy,
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
