"""Smpl Jobs SDK client (``client.jobs`` on SmplClient, or standalone ``JobsClient``).

Smpl Jobs runs an HTTP call — on a schedule or on demand — and records what
happened each time it fired. A single :class:`JobsClient` (and its async counterpart
:class:`AsyncJobsClient`) exposes the full surface, reachable two ways:

* ``client.jobs.*`` on :class:`smplkit.SmplClient`
* directly — ``JobsClient(api_key=...)`` — for callers that only need jobs.

A :class:`Job` is an active record: build it with :meth:`JobsClient.new`,
set fields, and call ``save()`` (create when new, full-replace update when it
already exists) or ``delete()``. A :class:`Run` is a read-only record of one
execution; run history and run actions live on ``jobs.runs``.
"""

from __future__ import annotations

import datetime
import json
import re
from dataclasses import dataclass
from enum import Enum
from typing import Any, Optional
from uuid import UUID

from smplkit._config import _service_url, resolve_client_config
from smplkit._generated.jobs.types import UNSET
from smplkit.errors import _raise_for_status
from smplkit._generated.jobs.api.jobs import (
    create_job as _gen_create_job,
    delete_job as _gen_delete_job,
    get_job as _gen_get_job,
    list_jobs as _gen_list_jobs,
    run_job_now as _gen_run_job_now,
    update_job as _gen_update_job,
)
from smplkit._generated.jobs.api.runs import (
    cancel_run as _gen_cancel_run,
    get_run as _gen_get_run,
    list_runs as _gen_list_runs,
    rerun_run as _gen_rerun_run,
)
from smplkit._generated.jobs.api.usage import get_usage as _gen_get_usage
from smplkit._generated.jobs.client import AuthenticatedClient as _JobsAuthClient
from smplkit._generated.jobs.models.job_create_request import JobCreateRequest
from smplkit._generated.jobs.models.job_request import JobRequest

__all__ = [
    "HttpConfig",
    "JobEnvironment",
    "JobKind",
    "RunTrigger",
    "Job",
    "AsyncJob",
    "Run",
    "AsyncRun",
    "Usage",
    "RunsClient",
    "AsyncRunsClient",
    "JobsClient",
    "AsyncJobsClient",
]

HttpHeader = tuple[str, str]


class JobKind(str, Enum):
    """How a job runs, derived from its schedule (read-only).

    Attributes:
        MANUAL: No schedule — never auto-fires; runs only when triggered.
        ONE_OFF: A ``now`` or datetime schedule — runs a single time, then is
            spent.
        RECURRING: A cron schedule — fires on a repeating cadence.
    """

    MANUAL = "manual"
    ONE_OFF = "one_off"
    RECURRING = "recurring"


class RunTrigger(str, Enum):
    """What started a run (read-only).

    Attributes:
        MANUAL: A ``run``/``trigger`` call started it on demand.
        RERUN: It repeats an earlier run.
        SCHEDULE: The job's schedule fired.
    """

    MANUAL = "MANUAL"
    RERUN = "RERUN"
    SCHEDULE = "SCHEDULE"


def _parse_dt(value: Any) -> Optional[datetime.datetime]:
    if not value:
        return None
    if isinstance(value, datetime.datetime):
        return value
    text = value.replace("Z", "+00:00")
    # Python 3.10's ``fromisoformat`` only accepts 3- or 6-digit fractional
    # seconds; normalize any precision (e.g. ".1", ".43") to 6 digits so the
    # parse succeeds uniformly across supported runtimes.
    text = re.sub(r"\.(\d+)", lambda m: "." + (m.group(1) + "000000")[:6], text, count=1)
    return datetime.datetime.fromisoformat(text)


def _check(resp: Any) -> None:
    _raise_for_status(int(resp.status_code), resp.content)


def _data(resp: Any) -> Any:
    return json.loads(resp.content)["data"]


def _jobs_transport(
    *,
    api_key: str | None,
    profile: str | None,
    base_domain: str | None,
    scheme: str | None,
    debug: bool | None,
    extra_headers: dict[str, str] | None,
) -> _JobsAuthClient:
    """Build a standalone Smpl Jobs transport from resolved config.

    Reuses the config resolver (jobs is account-global and never
    environment-scoped) and the shared per-service URL helper, so a
    standalone jobs client resolves credentials/base-domain from
    ``~/.smplkit`` / env vars / constructor args exactly like the top-level
    clients do.
    """
    cfg = resolve_client_config(
        profile=profile,
        api_key=api_key,
        base_domain=base_domain,
        scheme=scheme,
        debug=debug,
    )
    jobs_url = _service_url(cfg.scheme, "jobs", cfg.base_domain)
    headers = {"Accept": "application/vnd.api+json"}
    headers.update(cfg.extra_headers or {})
    headers.update(extra_headers or {})
    return _JobsAuthClient(base_url=jobs_url, token=cfg.api_key, headers=headers)


class HttpConfig:
    """The HTTP request a job performs when it fires (the ``http`` configuration)."""

    def __init__(
        self,
        *,
        url: str,
        method: str = "POST",
        headers: Optional[list[HttpHeader]] = None,
        body: Optional[str] = None,
        success_status: str = "2xx",
        timeout: int = 30,
        tls_verify: bool = True,
        ca_cert: Optional[str] = None,
    ) -> None:
        """Describe the HTTP request a job sends when it fires.

        Args:
            url: Destination URL the job sends its request to.
            method: HTTP verb used for the request. Defaults to ``"POST"``.
            headers: Headers attached to the request, as ``(name, value)``
                tuples. Defaults to no extra headers.
            body: Request body sent with the call, or ``None`` for no body.
            success_status: Status the destination must return for the run to
                count as a success — an exact code (``"200"``) or a class
                (``"2xx"``). Defaults to ``"2xx"``.
            timeout: Seconds to wait for a response before the run is treated
                as failed. Defaults to ``30``.
            tls_verify: Whether the destination's TLS certificate is verified.
                Defaults to ``True``.
            ca_cert: PEM-encoded certificate authority used to verify the
                destination, for self-signed or private CAs. ``None`` uses the
                system trust store.
        """
        self.url = url
        self.method = method
        self.headers: list[HttpHeader] = list(headers or [])
        self.body = body
        self.success_status = success_status
        self.timeout = timeout
        self.tls_verify = tls_verify
        self.ca_cert = ca_cert

    def to_dict(self) -> dict[str, Any]:
        return {
            "method": self.method,
            "url": self.url,
            "headers": [{"name": n, "value": v} for n, v in self.headers],
            "body": self.body,
            "success_status": self.success_status,
            "timeout": self.timeout,
            "tls_verify": self.tls_verify,
            "ca_cert": self.ca_cert,
        }

    @classmethod
    def from_dict(cls, d: dict[str, Any]) -> "HttpConfig":
        """Build an :class:`HttpConfig` from its dictionary representation.

        Args:
            d: HTTP configuration as a mapping, with at least a ``"url"`` key
                and optional ``method``, ``headers``, ``body``,
                ``success_status``, ``timeout``, ``tls_verify``, and
                ``ca_cert`` entries. Omitted keys fall back to their defaults.

        Returns:
            The corresponding :class:`HttpConfig`.
        """
        return cls(
            url=d["url"],
            method=d.get("method", "POST"),
            headers=[(h["name"], h["value"]) for h in (d.get("headers") or [])],
            body=d.get("body"),
            success_status=d.get("success_status", "2xx"),
            timeout=d.get("timeout", 30),
            tls_verify=d.get("tls_verify", True),
            ca_cert=d.get("ca_cert"),
        )

    def __repr__(self) -> str:
        return f"HttpConfig(method={self.method!r}, url={self.url!r})"


@dataclass(slots=True)
class JobEnvironment:
    """Per-environment enablement, schedule, and configuration override for a job.

    A job runs in a given environment only when that environment has an entry in
    :attr:`Job.environments` with ``enabled=True`` (scheduled there for a
    recurring job, triggerable there for a manual one); an environment with no
    entry (or ``enabled=False``) is disabled there.

    Attributes:
        enabled: Whether the job is enabled in this environment. Defaults to
            ``False``.
        schedule: Optional per-environment cron override that varies the cadence
            for this environment. ``None`` (the default) inherits the job's base
            :attr:`Job.schedule`.
        configuration: Optional per-environment request configuration that
            fully replaces the job's base :attr:`Job.configuration` for this
            environment. ``None`` (the default) inherits the base
            configuration.
        next_run_at: Read-only next scheduled fire time in this environment, as
            reported by the server. ``None`` when the environment is not enabled
            or once a one-off run has fired. Never sent on save.
    """

    enabled: bool = False
    schedule: Optional[str] = None
    configuration: Optional[HttpConfig] = None
    next_run_at: Optional[datetime.datetime] = None

    @classmethod
    def _from_dict(cls, raw: dict[str, Any]) -> "JobEnvironment":
        cfg = raw.get("configuration")
        return cls(
            enabled=bool(raw.get("enabled", False)),
            schedule=raw.get("schedule"),
            configuration=HttpConfig.from_dict(cfg) if cfg else None,
            next_run_at=_parse_dt(raw.get("next_run_at")),
        )

    def _to_payload(self) -> dict[str, Any]:
        payload: dict[str, Any] = {"enabled": self.enabled}
        if self.schedule is not None:
            payload["schedule"] = self.schedule
        if self.configuration is not None:
            payload["configuration"] = self.configuration.to_dict()
        return payload


def _normalize_environments(
    environments: Optional[dict[str, "JobEnvironment | dict[str, Any]"]],
) -> dict[str, JobEnvironment]:
    """Coerce a loose ``environments`` mapping into ``{key: JobEnvironment}``."""
    if not environments:
        return {}
    out: dict[str, JobEnvironment] = {}
    for env_key, value in environments.items():
        if isinstance(value, JobEnvironment):
            out[env_key] = value
        else:
            # A dict-form override may carry its configuration as an HttpConfig
            # or a plain dict — coerce a dict so it serializes on save (matches
            # the server-parse path in JobEnvironment._from_dict).
            cfg = value.get("configuration")
            if cfg is not None and not isinstance(cfg, HttpConfig):
                cfg = HttpConfig.from_dict(cfg)
            out[env_key] = JobEnvironment(
                enabled=bool(value.get("enabled", False)),
                schedule=value.get("schedule"),
                configuration=cfg,
            )
    return out


def _env_header(value: Optional[str]) -> "str | Any":
    """An ``X-Smplkit-Environment`` header value, or ``UNSET`` when unset."""
    return value if value is not None else UNSET


def _join_environments(environments: Optional[list[str]]) -> "str | Any":
    if not environments:
        return UNSET
    return ",".join(environments)


def _resolve_environment_filter(environments: Optional[list[str]], default: Optional[str]) -> "str | Any":
    """Resolve ``filter[environment]``: explicit list → client default → unset.

    An explicit ``environments`` list always wins and is comma-joined; otherwise
    the client's configured environment (if any) is used; otherwise the read
    covers every environment the caller can access.
    """
    if environments:
        return _join_environments(environments)
    if default is not None:
        return default
    return UNSET


class _JobBase:
    """Shared state for ``Job`` / ``AsyncJob``."""

    def __init__(
        self,
        *,
        id: str,
        name: str,
        schedule: Optional[str] = None,
        configuration: HttpConfig,
        description: Optional[str] = None,
        environments: Optional[dict[str, JobEnvironment]] = None,
        kind: Optional[JobKind] = None,
        type: str = "http",
        concurrency_policy: str = "ALLOW",
        created_at: Optional[datetime.datetime] = None,
        updated_at: Optional[datetime.datetime] = None,
        deleted_at: Optional[datetime.datetime] = None,
        version: Optional[int] = None,
    ) -> None:
        self.id = id
        self.name = name
        self.description = description
        # Per-environment overrides ``{env_key: JobEnvironment}``. The writable
        # surface for enablement: set an entry's ``enabled`` (and optional
        # schedule / configuration) to make the job fire in that environment.
        # Each entry also reports its read-only ``next_run_at``.
        self.environments: dict[str, JobEnvironment] = environments if environments is not None else {}
        # Read-only server-derived kind (see :class:`JobKind`).
        self.kind = kind
        self.type = type
        self.schedule = schedule
        self.configuration = configuration
        self.concurrency_policy = concurrency_policy
        self.created_at = created_at
        self.updated_at = updated_at
        self.deleted_at = deleted_at
        self.version = version
        # Creation-time only: the environment a one-off job is born in, sent as
        # the X-Smplkit-Environment header by ``_create``. Ignored for recurring
        # and manual jobs (whose environments come from the map).
        self._birth_environment: Optional[str] = None

    @property
    def enabled(self) -> bool:
        """Read-only roll-up: ``True`` when enabled in at least one environment.

        Derived from the :attr:`environments` map — the job has no server-side
        top-level ``enabled`` field. Set enablement per environment via
        :meth:`set_enabled` (or the ``environments`` map).
        """
        return any(env.enabled for env in self.environments.values())

    def is_recurring(self) -> bool:
        """Whether this is a recurring (cron-scheduled) job."""
        return self.kind == JobKind.RECURRING

    def is_manual(self) -> bool:
        """Whether this is a manual job — no schedule; runs only when triggered."""
        return self.kind == JobKind.MANUAL

    def is_one_off(self) -> bool:
        """Whether this is a one-off job — a single ``now`` / datetime run."""
        return self.kind == JobKind.ONE_OFF

    def _apply(self, other: "_JobBase") -> None:
        self.__dict__.update({k: v for k, v in other.__dict__.items() if not k.startswith("_client")})

    def _environment_override(self, environment: str) -> JobEnvironment:
        env = self.environments.get(environment)
        if env is None:
            env = JobEnvironment()
            self.environments[environment] = env
        return env

    def set_enabled(self, enabled: bool, environment: str) -> None:
        """Enable or disable the job in a single environment."""
        self._environment_override(environment).enabled = enabled

    def is_enabled(self, environment: Optional[str] = None) -> bool:
        """Whether the job is enabled.

        With ``environment=None`` (the default), returns the derived roll-up —
        ``True`` when the job is enabled in at least one environment. With an
        ``environment``, returns whether the job is enabled in that specific
        environment.
        """
        if environment is None:
            return self.enabled
        override = self.environments.get(environment)
        return bool(override and override.enabled)

    def set_configuration(self, configuration: HttpConfig, environment: Optional[str] = None) -> None:
        """Set the job's configuration — base (``environment=None``) or per-environment."""
        if environment is None:
            self.configuration = configuration
        else:
            self._environment_override(environment).configuration = configuration

    def get_configuration(self, environment: Optional[str] = None) -> HttpConfig:
        """The job's effective configuration.

        With ``environment=None`` (the default), returns the base
        configuration. With an ``environment``, returns that environment's
        configuration override when it has one, else the base configuration —
        the request the job actually sends when it fires in that environment.
        """
        if environment is not None:
            override = self.environments.get(environment)
            if override is not None and override.configuration is not None:
                return override.configuration
        return self.configuration

    def set_schedule(self, schedule: str, environment: Optional[str] = None) -> None:
        """Set the job's schedule — base (``environment=None``) or per-environment.

        With ``environment=None`` (the default) this sets the job's base
        :attr:`schedule`, the cadence every environment inherits unless it
        overrides it. With an ``environment``, this sets a per-environment cron
        override that varies the cadence for just that environment (recurring
        jobs only); pass the environment's base cadence back, or clear the
        override, to fall back to the base schedule.
        """
        if environment is None:
            self.schedule = schedule
        else:
            self._environment_override(environment).schedule = schedule

    def _attributes(self) -> dict[str, Any]:
        attrs: dict[str, Any] = {
            "name": self.name,
            "description": self.description,
            "type": self.type,
            "schedule": self.schedule,
            "configuration": self.configuration.to_dict(),
            "concurrency_policy": self.concurrency_policy,
        }
        if self.environments:
            attrs["environments"] = {env_key: env._to_payload() for env_key, env in self.environments.items()}
        return attrs

    def __repr__(self) -> str:
        enabled_in = sorted(k for k, v in self.environments.items() if v.enabled)
        return f"Job(id={self.id!r}, name={self.name!r}, enabled_in={enabled_in!r})"


def _job_base_from_resource(resource: dict[str, Any]) -> _JobBase:
    a = resource["attributes"]
    environments = {
        env_key: JobEnvironment._from_dict(env_raw or {}) for env_key, env_raw in (a.get("environments") or {}).items()
    }
    raw_kind = a.get("kind")
    return _JobBase(
        id=resource["id"],
        name=a["name"],
        description=a.get("description"),
        environments=environments,
        kind=JobKind(raw_kind) if raw_kind else None,
        type=a.get("type", "http"),
        schedule=a.get("schedule"),
        configuration=HttpConfig.from_dict(a["configuration"]),
        concurrency_policy=a.get("concurrency_policy", "ALLOW"),
        created_at=_parse_dt(a.get("created_at")),
        updated_at=_parse_dt(a.get("updated_at")),
        deleted_at=_parse_dt(a.get("deleted_at")),
        version=a.get("version"),
    )


class Job(_JobBase):
    """A job definition (sync). Mutate fields, then call :meth:`save`."""

    def __init__(self, client: "Optional[JobsClient]" = None, **kwargs: Any) -> None:
        super().__init__(**kwargs)
        self._client = client

    @classmethod
    def _from_resource(cls, resource: dict[str, Any], client: "JobsClient") -> "Job":
        base = _job_base_from_resource(resource)
        job = cls(client, id=base.id, name=base.name, schedule=base.schedule, configuration=base.configuration)
        job._apply(base)
        return job

    def save(self) -> None:
        """Create this job, or full-replace it if it already exists."""
        if self._client is None:
            raise RuntimeError("Job was constructed without a client; cannot save")
        other = self._client._create(self) if self.created_at is None else self._client._update(self)
        self._apply(other)

    def delete(self) -> None:
        """Delete this job."""
        if self._client is None:
            raise RuntimeError("Job was constructed without a client; cannot delete")
        self._client.delete(self.id)

    def trigger(self, *, environment: Optional[str] = None) -> "Run":
        """Trigger one immediate, manual run of this job (a ``MANUAL`` run).

        Args:
            environment: Environment the run executes in. Defaults to the
                client's configured environment; when the job is enabled in
                exactly one environment that environment is used.

        Returns:
            The :class:`Run` that was started.
        """
        if self._client is None:
            raise RuntimeError("Job was constructed without a client; cannot trigger a run")
        return self._client.run(self.id, environment=environment)

    def list_runs(
        self,
        *,
        environment: Optional[str] = None,
        page_size: Optional[int] = None,
        after: Optional[str] = None,
    ) -> "list[Run]":
        """List this job's run history, most recent first.

        Args:
            environment: Restrict to runs stamped with this environment. ``None``
                covers every environment you can access.
            page_size: Maximum number of runs to return in this page.
            after: Opaque cursor from a previous page.

        Returns:
            The runs in this page, as a list of :class:`Run`.
        """
        if self._client is None:
            raise RuntimeError("Job was constructed without a client; cannot list runs")
        return self._client.runs.list(
            job=self.id,
            environments=[environment] if environment is not None else None,
            page_size=page_size,
            after=after,
        )


class AsyncJob(_JobBase):
    """A job definition (async). Mutate fields, then ``await save()``."""

    def __init__(self, client: "Optional[AsyncJobsClient]" = None, **kwargs: Any) -> None:
        super().__init__(**kwargs)
        self._client = client

    @classmethod
    def _from_resource(cls, resource: dict[str, Any], client: "AsyncJobsClient") -> "AsyncJob":
        base = _job_base_from_resource(resource)
        job = cls(client, id=base.id, name=base.name, schedule=base.schedule, configuration=base.configuration)
        job._apply(base)
        return job

    async def save(self) -> None:
        if self._client is None:
            raise RuntimeError("AsyncJob was constructed without a client; cannot save")
        other = await self._client._create(self) if self.created_at is None else await self._client._update(self)
        self._apply(other)

    async def delete(self) -> None:
        if self._client is None:
            raise RuntimeError("AsyncJob was constructed without a client; cannot delete")
        await self._client.delete(self.id)

    async def trigger(self, *, environment: Optional[str] = None) -> "AsyncRun":
        """Trigger one immediate, manual run of this job (a ``MANUAL`` run).

        Args:
            environment: Environment the run executes in. Defaults to the
                client's configured environment; when the job is enabled in
                exactly one environment that environment is used.

        Returns:
            The :class:`AsyncRun` that was started.
        """
        if self._client is None:
            raise RuntimeError("AsyncJob was constructed without a client; cannot trigger a run")
        return await self._client.run(self.id, environment=environment)

    async def list_runs(
        self,
        *,
        environment: Optional[str] = None,
        page_size: Optional[int] = None,
        after: Optional[str] = None,
    ) -> "list[AsyncRun]":
        """List this job's run history, most recent first.

        Args:
            environment: Restrict to runs stamped with this environment. ``None``
                covers every environment you can access.
            page_size: Maximum number of runs to return in this page.
            after: Opaque cursor from a previous page.

        Returns:
            The runs in this page, as a list of :class:`Run`.
        """
        if self._client is None:
            raise RuntimeError("AsyncJob was constructed without a client; cannot list runs")
        return await self._client.runs.list(
            job=self.id,
            environments=[environment] if environment is not None else None,
            page_size=page_size,
            after=after,
        )


class _RunBase:
    """Shared read-only state for ``Run`` / ``AsyncRun``."""

    def __init__(self, attributes: dict[str, Any], id: str) -> None:
        self.id = id
        self.job: str = attributes["job"]
        self.job_version: Optional[int] = attributes.get("job_version")
        self.environment: str = attributes["environment"]
        # Raw trigger string; compare against the :class:`RunTrigger` constants.
        self.trigger: str = attributes["trigger"]
        self.rerun_of: Optional[str] = attributes.get("rerun_of")
        self.scheduled_for = _parse_dt(attributes.get("scheduled_for"))
        self.status: str = attributes["status"]
        self.started_at = _parse_dt(attributes.get("started_at"))
        self.finished_at = _parse_dt(attributes.get("finished_at"))
        self.pending_duration_ms: Optional[int] = attributes.get("pending_duration_ms")
        self.run_duration_ms: Optional[int] = attributes.get("run_duration_ms")
        self.total_duration_ms: Optional[int] = attributes.get("total_duration_ms")
        self.failure_reason: Optional[str] = attributes.get("failure_reason")
        self.error: Optional[str] = attributes.get("error")
        self.request: Optional[dict[str, Any]] = attributes.get("request")
        self.result: Optional[dict[str, Any]] = attributes.get("result")
        self.created_at = _parse_dt(attributes.get("created_at"))

    def __repr__(self) -> str:
        return f"Run(id={self.id!r}, job={self.job!r}, status={self.status!r})"


class Run(_RunBase):
    """A single execution of a job (read-only) with ``rerun`` / ``cancel`` (sync)."""

    def __init__(self, attributes: dict[str, Any], id: str, runs: "Optional[RunsClient]" = None) -> None:
        super().__init__(attributes, id)
        self._runs = runs

    @classmethod
    def _from_resource(cls, resource: dict[str, Any], runs: "Optional[RunsClient]" = None) -> "Run":
        return cls(resource["attributes"], id=resource["id"], runs=runs)

    def rerun(self) -> "Run":
        """Start a new run that repeats this one (a ``RERUN``), in the same environment."""
        if self._runs is None:
            raise RuntimeError("Run was constructed without a client; cannot rerun")
        return self._runs.rerun(self.id)

    def cancel(self) -> "Run":
        """Cancel this run if it has not finished yet."""
        if self._runs is None:
            raise RuntimeError("Run was constructed without a client; cannot cancel")
        return self._runs.cancel(self.id)


class AsyncRun(_RunBase):
    """A single execution of a job (read-only) with ``rerun`` / ``cancel`` (async)."""

    def __init__(self, attributes: dict[str, Any], id: str, runs: "Optional[AsyncRunsClient]" = None) -> None:
        super().__init__(attributes, id)
        self._runs = runs

    @classmethod
    def _from_resource(cls, resource: dict[str, Any], runs: "Optional[AsyncRunsClient]" = None) -> "AsyncRun":
        return cls(resource["attributes"], id=resource["id"], runs=runs)

    async def rerun(self) -> "AsyncRun":
        """Start a new run that repeats this one (a ``RERUN``), in the same environment."""
        if self._runs is None:
            raise RuntimeError("AsyncRun was constructed without a client; cannot rerun")
        return await self._runs.rerun(self.id)

    async def cancel(self) -> "AsyncRun":
        """Cancel this run if it has not finished yet."""
        if self._runs is None:
            raise RuntimeError("AsyncRun was constructed without a client; cannot cancel")
        return await self._runs.cancel(self.id)


class Usage:
    """Current-period usage against the account's plan allotments (read-only)."""

    def __init__(self, attributes: dict[str, Any]) -> None:
        self.period: str = attributes["period"]
        self.runs_used: int = attributes["runs_used"]
        self.runs_included: int = attributes["runs_included"]
        self.active_jobs: int = attributes["active_jobs"]
        self.active_jobs_limit: int = attributes["active_jobs_limit"]

    @classmethod
    def _from_resource(cls, resource: dict[str, Any]) -> "Usage":
        return cls(resource["attributes"])

    def __repr__(self) -> str:
        return f"Usage(period={self.period!r}, runs_used={self.runs_used!r}/{self.runs_included!r})"


def _job_body(job: _JobBase, *, request_cls: Any) -> Any:
    return request_cls.from_dict({"data": {"id": job.id, "type": "job", "attributes": job._attributes()}})


def _new_kwargs(id, *, name, schedule, configuration, description, environments, concurrency_policy):
    return {
        "id": id,
        "name": name,
        "schedule": schedule,
        "configuration": configuration,
        "description": description,
        "environments": environments,
        "concurrency_policy": concurrency_policy,
    }


def _run_list_kwargs(job: Optional[str], page_size: Optional[int], after: Optional[str]) -> dict[str, Any]:
    kwargs: dict[str, Any] = {}
    if job is not None:
        kwargs["filterjob"] = job
    if page_size is not None:
        kwargs["pagesize"] = page_size
    if after is not None:
        kwargs["pageafter"] = after
    return kwargs


def _list_jobs_kwargs(kind, scheduled, name, page_number, page_size) -> dict[str, Any]:
    kwargs: dict[str, Any] = {}
    if kind is not None:
        kwargs["filterkind"] = kind.value
    if scheduled is not None:
        kwargs["filterscheduled"] = scheduled
    if name is not None:
        kwargs["filtername"] = name
    if page_number is not None:
        kwargs["pagenumber"] = page_number
    if page_size is not None:
        kwargs["pagesize"] = page_size
    return kwargs


class RunsClient:
    """Read a job's run history and act on individual runs (``jobs.runs``).

    Reached as ``client.jobs.runs``. Use this to list past runs, fetch one by
    id, cancel a run that is still pending, or re-run a finished one. To
    trigger a fresh ad-hoc run of a job, use :meth:`JobsClient.run` instead.
    """

    def __init__(self, auth: _JobsAuthClient, *, environment: Optional[str] = None) -> None:
        self._auth = auth
        self._environment = environment

    def list(
        self,
        *,
        job: Optional[str] = None,
        environments: Optional[list[str]] = None,
        page_size: Optional[int] = None,
        after: Optional[str] = None,
    ) -> list[Run]:
        """List past runs, most recent first.

        Args:
            job: Return only runs of the job with this id. ``None`` lists runs
                across all jobs in the account.
            environments: Restrict to runs stamped with any of these environment
                keys. ``None`` falls back to the client's configured environment
                (if any), otherwise covers every environment you can access.
            page_size: Maximum number of runs to return in this page. ``None``
                uses the server default.
            after: Opaque cursor from a previous page; returns the runs that
                follow it. ``None`` starts from the first page.

        Returns:
            The runs in this page, as a list of :class:`Run`.
        """
        resp = _gen_list_runs.sync_detailed(
            client=self._auth,
            filterenvironment=_resolve_environment_filter(environments, self._environment),
            **_run_list_kwargs(job, page_size, after),
        )
        _check(resp)
        return [Run._from_resource(r, self) for r in _data(resp)]

    def get(self, run_id: str | UUID) -> Run:
        """Fetch a single run by its id.

        Args:
            run_id: Identifier of the run to fetch.

        Returns:
            The matching :class:`Run`.
        """
        resp = _gen_get_run.sync_detailed(UUID(str(run_id)), client=self._auth)
        _check(resp)
        return Run._from_resource(_data(resp), self)

    def cancel(self, run_id: str | UUID) -> Run:
        """Cancel a run that has not finished yet.

        Args:
            run_id: Identifier of the run to cancel.

        Returns:
            The updated :class:`Run` reflecting the cancellation.
        """
        resp = _gen_cancel_run.sync_detailed(UUID(str(run_id)), client=self._auth)
        _check(resp)
        return Run._from_resource(_data(resp), self)

    def rerun(self, run_id: str | UUID) -> Run:
        """Start a new run that repeats a previous one.

        Args:
            run_id: Identifier of the run to repeat.

        Returns:
            The new :class:`Run`, with ``rerun_of`` set to ``run_id``.
        """
        resp = _gen_rerun_run.sync_detailed(UUID(str(run_id)), client=self._auth)
        _check(resp)
        return Run._from_resource(_data(resp), self)


class AsyncRunsClient:
    """Read a job's run history and act on individual runs (``jobs.runs``), awaited.

    Reached as ``client.jobs.runs`` on an async client. Use this to list past
    runs, fetch one by id, cancel a run that is still pending, or re-run a
    finished one. To trigger a fresh ad-hoc run of a job, use
    :meth:`AsyncJobsClient.run` instead.
    """

    def __init__(self, auth: _JobsAuthClient, *, environment: Optional[str] = None) -> None:
        self._auth = auth
        self._environment = environment

    async def list(
        self,
        *,
        job: Optional[str] = None,
        environments: Optional[list[str]] = None,
        page_size: Optional[int] = None,
        after: Optional[str] = None,
    ) -> list[AsyncRun]:
        """List past runs, most recent first.

        Args:
            job: Return only runs of the job with this id. ``None`` lists runs
                across all jobs in the account.
            environments: Restrict to runs stamped with any of these environment
                keys. ``None`` falls back to the client's configured environment
                (if any), otherwise covers every environment you can access.
            page_size: Maximum number of runs to return in this page. ``None``
                uses the server default.
            after: Opaque cursor from a previous page; returns the runs that
                follow it. ``None`` starts from the first page.

        Returns:
            The runs in this page, as a list of :class:`AsyncRun`.
        """
        resp = await _gen_list_runs.asyncio_detailed(
            client=self._auth,
            filterenvironment=_resolve_environment_filter(environments, self._environment),
            **_run_list_kwargs(job, page_size, after),
        )
        _check(resp)
        return [AsyncRun._from_resource(r, self) for r in _data(resp)]

    async def get(self, run_id: str | UUID) -> AsyncRun:
        """Fetch a single run by its id.

        Args:
            run_id: Identifier of the run to fetch.

        Returns:
            The matching :class:`AsyncRun`.
        """
        resp = await _gen_get_run.asyncio_detailed(UUID(str(run_id)), client=self._auth)
        _check(resp)
        return AsyncRun._from_resource(_data(resp), self)

    async def cancel(self, run_id: str | UUID) -> AsyncRun:
        """Cancel a run that has not finished yet.

        Args:
            run_id: Identifier of the run to cancel.

        Returns:
            The updated :class:`AsyncRun` reflecting the cancellation.
        """
        resp = await _gen_cancel_run.asyncio_detailed(UUID(str(run_id)), client=self._auth)
        _check(resp)
        return AsyncRun._from_resource(_data(resp), self)

    async def rerun(self, run_id: str | UUID) -> AsyncRun:
        """Start a new run that repeats a previous one.

        Args:
            run_id: Identifier of the run to repeat.

        Returns:
            The new :class:`AsyncRun`, with ``rerun_of`` set to ``run_id``.
        """
        resp = await _gen_rerun_run.asyncio_detailed(UUID(str(run_id)), client=self._auth)
        _check(resp)
        return AsyncRun._from_resource(_data(resp), self)


class JobsClient:
    """Synchronous Smpl Jobs client.

    Reachable as ``client.jobs`` (:class:`smplkit.SmplClient`) or constructed
    directly:

        from smplkit import JobsClient

        with JobsClient() as jobs:
            for job in jobs.list():
                print(job.id)

    Args:
        api_key: API key. When omitted, resolved from ``SMPLKIT_API_KEY`` or
            ``~/.smplkit``.
        profile: Named ``~/.smplkit`` profile section.
        base_domain: Base domain for API requests (default ``"smplkit.com"``).
        scheme: URL scheme (default ``"https"``).
        debug: Enable SDK debug logging.
        extra_headers: Extra headers attached to every request.
        environment: Default environment for environment-scoped operations —
            the environment a one-off job created through this client is born
            in, the default a manual run executes in, and the default scope for
            ``jobs.runs.list()``. ``None`` leaves these unset (the credential's
            permitted environment is implied where unambiguous).
        auth_client: Internal — a pre-built transport supplied by a top-level
            client so the jobs surface shares one connection pool. Not for
            direct use.
    """

    def __init__(
        self,
        api_key: str | None = None,
        *,
        profile: str | None = None,
        base_domain: str | None = None,
        scheme: str | None = None,
        debug: bool | None = None,
        extra_headers: dict[str, str] | None = None,
        environment: str | None = None,
        auth_client: _JobsAuthClient | None = None,
    ) -> None:
        if auth_client is not None:
            self._auth = auth_client
            self._owns_transport = False
        else:
            self._auth = _jobs_transport(
                api_key=api_key,
                profile=profile,
                base_domain=base_domain,
                scheme=scheme,
                debug=debug,
                extra_headers=extra_headers,
            )
            self._owns_transport = True
        self._environment = environment
        self.runs = RunsClient(self._auth, environment=environment)

    def _new_job(
        self,
        id: str,
        *,
        name: str,
        schedule: Optional[str],
        configuration: HttpConfig,
        description: Optional[str],
        environments: Optional[dict[str, "JobEnvironment | dict[str, Any]"]],
        concurrency_policy: str,
        environment: Optional[str],
    ) -> Job:
        job = Job(
            self,
            **_new_kwargs(
                id,
                name=name,
                schedule=schedule,
                configuration=configuration,
                description=description,
                environments=_normalize_environments(environments),
                concurrency_policy=concurrency_policy,
            ),
        )
        job._birth_environment = environment if environment is not None else self._environment
        return job

    def new_recurring_job(
        self,
        id: str,
        *,
        name: str,
        schedule: str,
        configuration: HttpConfig,
        description: Optional[str] = None,
        environments: Optional[dict[str, "JobEnvironment | dict[str, Any]"]] = None,
        concurrency_policy: str = "ALLOW",
    ) -> Job:
        """Return an unsaved recurring :class:`Job`. Call ``.save()`` to create it.

        Args:
            id: Caller-supplied unique identifier for the job. Unique within
                the account and immutable; the service returns 409 if another
                live job already uses this id.
            name: Human-readable name for the job.
            schedule: The base cadence — a 5-field cron expression evaluated in
                UTC (e.g. ``"0 2 * * *"``) — that every environment inherits
                unless it sets its own override.
            configuration: The HTTP request the job sends each time it fires.
            description: Free-text description for the job. Defaults to none.
            environments: Per-environment overrides keyed by environment key —
                each a :class:`JobEnvironment`, or a plain dict
                ``{"enabled": bool}`` optionally with ``"schedule"`` /
                ``"configuration"`` overrides. The job is scheduled only in
                environments enabled here.
            concurrency_policy: How overlapping runs are handled. ``"ALLOW"``
                (the default and only value today) permits a new run to start
                while a previous one is still in flight.

        Returns:
            An unsaved recurring :class:`Job` bound to this client.
        """
        return self._new_job(
            id,
            name=name,
            schedule=schedule,
            configuration=configuration,
            description=description,
            environments=environments,
            concurrency_policy=concurrency_policy,
            environment=None,
        )

    def new_manual_job(
        self,
        id: str,
        *,
        name: str,
        configuration: HttpConfig,
        description: Optional[str] = None,
        environments: Optional[dict[str, "JobEnvironment | dict[str, Any]"]] = None,
        concurrency_policy: str = "ALLOW",
    ) -> Job:
        """Return an unsaved manual :class:`Job`. Call ``.save()`` to create it.

        A manual job has no schedule — it never auto-fires and runs only when
        triggered via :meth:`run` / :meth:`Job.trigger`.

        Args:
            id: Caller-supplied unique identifier for the job. Unique within
                the account and immutable; the service returns 409 if another
                live job already uses this id.
            name: Human-readable name for the job.
            configuration: The HTTP request the job sends each time it runs.
            description: Free-text description for the job. Defaults to none.
            environments: Per-environment overrides keyed by environment key —
                each a :class:`JobEnvironment`, or a plain dict
                ``{"enabled": bool}`` optionally with a ``"configuration"``
                override. The job is triggerable only in environments enabled
                here.
            concurrency_policy: How overlapping runs are handled. ``"ALLOW"``
                (the default and only value today) permits a new run to start
                while a previous one is still in flight.

        Returns:
            An unsaved manual :class:`Job` bound to this client.
        """
        return self._new_job(
            id,
            name=name,
            schedule=None,
            configuration=configuration,
            description=description,
            environments=environments,
            concurrency_policy=concurrency_policy,
            environment=None,
        )

    def schedule(
        self,
        id: str,
        *,
        name: str,
        schedule: datetime.datetime,
        configuration: HttpConfig,
        description: Optional[str] = None,
        concurrency_policy: str = "ALLOW",
        environment: Optional[str] = None,
    ) -> Job:
        """Return an unsaved one-off :class:`Job`. Call ``.save()`` to create it.

        A one-off job runs a single time at ``schedule`` and is then spent.

        Args:
            id: Caller-supplied unique identifier for the job. Unique within
                the account and immutable; the service returns 409 if another
                live job already uses this id.
            name: Human-readable name for the job.
            schedule: The instant the single run fires, as a ``datetime``.
            configuration: The HTTP request the job sends when it runs.
            description: Free-text description for the job. Defaults to none.
            concurrency_policy: How overlapping runs are handled. ``"ALLOW"``
                (the default and only value today) permits a new run to start
                while a previous one is still in flight.
            environment: The environment the job is born in. Defaults to the
                client's configured environment.

        Returns:
            An unsaved one-off :class:`Job` bound to this client.
        """
        return self._new_job(
            id,
            name=name,
            schedule=schedule.isoformat(),
            configuration=configuration,
            description=description,
            environments=None,
            concurrency_policy=concurrency_policy,
            environment=environment,
        )

    def list(
        self,
        *,
        kind: Optional[JobKind] = None,
        scheduled: Optional[bool] = None,
        name: Optional[str] = None,
        page_number: Optional[int] = None,
        page_size: Optional[int] = None,
    ) -> list[Job]:
        """List jobs in the account.

        Args:
            kind: Return only jobs of this :class:`JobKind`. ``None`` lists
                recurring and manual jobs; one-off jobs are omitted unless you
                pass :attr:`JobKind.ONE_OFF`.
            scheduled: Return only jobs that have an upcoming fire in some
                environment (``True``) or none (``False``) — the feed for an
                upcoming-runs view, which includes one-offs. ``None`` does not
                filter on scheduling.
            name: Return only jobs whose name contains this text
                (case-insensitive). ``None`` lists all.
            page_number: 1-based page to return. ``None`` returns the first
                page.
            page_size: Maximum number of jobs to return in this page. ``None``
                uses the server default.

        Returns:
            The jobs in this page, as a list of :class:`Job`.
        """
        resp = _gen_list_jobs.sync_detailed(
            client=self._auth, **_list_jobs_kwargs(kind, scheduled, name, page_number, page_size)
        )
        _check(resp)
        return [Job._from_resource(r, self) for r in _data(resp)]

    def get(self, id: str) -> Job:
        """Fetch a single job by its id.

        Args:
            id: Identifier of the job to fetch.

        Returns:
            The matching :class:`Job`.
        """
        resp = _gen_get_job.sync_detailed(id, client=self._auth)
        _check(resp)
        return Job._from_resource(_data(resp), self)

    def delete(self, id: str) -> None:
        """Delete a job by its id.

        Args:
            id: Identifier of the job to delete.
        """
        resp = _gen_delete_job.sync_detailed(id, client=self._auth)
        _check(resp)

    def run(self, id: str, *, environment: Optional[str] = None) -> Run:
        """Trigger one immediate, manual run of a job, ignoring its schedule.

        This starts an ad-hoc run right now in addition to any scheduled runs;
        it does not alter the job's schedule. To read or act on existing runs,
        use ``jobs.runs``.

        Args:
            id: Identifier of the job to run.
            environment: Environment the manual run executes in. Defaults to the
                client's configured environment; when the job is enabled in
                exactly one environment that environment is used, and a
                single-environment credential implies it. The job must be
                enabled in the chosen environment.

        Returns:
            The :class:`Run` that was started, with ``trigger`` set to
            ``"MANUAL"``.
        """
        resp = _gen_run_job_now.sync_detailed(
            id,
            client=self._auth,
            x_smplkit_environment=_env_header(environment if environment is not None else self._environment),
        )
        _check(resp)
        return Run._from_resource(_data(resp), self.runs)

    def usage(self) -> Usage:
        """Report current-period usage against the account's plan allotments.

        Returns:
            A :class:`Usage` snapshot with runs used/included and active-job
            counts for the current period.
        """
        resp = _gen_get_usage.sync_detailed(client=self._auth)
        _check(resp)
        return Usage._from_resource(_data(resp))

    def _create(self, job: Job) -> Job:
        resp = _gen_create_job.sync_detailed(
            client=self._auth,
            body=_job_body(job, request_cls=JobCreateRequest),
            x_smplkit_environment=_env_header(job._birth_environment),
        )
        _check(resp)
        return Job._from_resource(_data(resp), self)

    def _update(self, job: Job) -> Job:
        resp = _gen_update_job.sync_detailed(
            job.id,
            client=self._auth,
            body=_job_body(job, request_cls=JobRequest),
            x_smplkit_environment=_env_header(self._environment),
        )
        _check(resp)
        return Job._from_resource(_data(resp), self)

    def close(self) -> None:
        """Release HTTP resources — only when this client owns its transport.

        A jobs client wired by a top-level client shares that client's
        transport and must not close it here; the owning client's ``close()``
        handles teardown.
        """
        if self._owns_transport:
            client = self._auth._client
            if client is not None:
                client.close()
                self._auth._client = None

    def __enter__(self) -> "JobsClient":
        return self

    def __exit__(self, *args: object) -> None:
        self.close()


class AsyncJobsClient:
    """Asynchronous Smpl Jobs client (async counterpart of :class:`JobsClient`)."""

    def __init__(
        self,
        api_key: str | None = None,
        *,
        profile: str | None = None,
        base_domain: str | None = None,
        scheme: str | None = None,
        debug: bool | None = None,
        extra_headers: dict[str, str] | None = None,
        environment: str | None = None,
        auth_client: _JobsAuthClient | None = None,
    ) -> None:
        if auth_client is not None:
            self._auth = auth_client
            self._owns_transport = False
        else:
            self._auth = _jobs_transport(
                api_key=api_key,
                profile=profile,
                base_domain=base_domain,
                scheme=scheme,
                debug=debug,
                extra_headers=extra_headers,
            )
            self._owns_transport = True
        self._environment = environment
        self.runs = AsyncRunsClient(self._auth, environment=environment)

    def _new_job(
        self,
        id: str,
        *,
        name: str,
        schedule: Optional[str],
        configuration: HttpConfig,
        description: Optional[str],
        environments: Optional[dict[str, "JobEnvironment | dict[str, Any]"]],
        concurrency_policy: str,
        environment: Optional[str],
    ) -> AsyncJob:
        job = AsyncJob(
            self,
            **_new_kwargs(
                id,
                name=name,
                schedule=schedule,
                configuration=configuration,
                description=description,
                environments=_normalize_environments(environments),
                concurrency_policy=concurrency_policy,
            ),
        )
        job._birth_environment = environment if environment is not None else self._environment
        return job

    def new_recurring_job(
        self,
        id: str,
        *,
        name: str,
        schedule: str,
        configuration: HttpConfig,
        description: Optional[str] = None,
        environments: Optional[dict[str, "JobEnvironment | dict[str, Any]"]] = None,
        concurrency_policy: str = "ALLOW",
    ) -> AsyncJob:
        """Return an unsaved recurring :class:`AsyncJob`. ``await .save()`` to create it.

        Args:
            id: Caller-supplied unique identifier for the job. Unique within
                the account and immutable; the service returns 409 if another
                live job already uses this id.
            name: Human-readable name for the job.
            schedule: The base cadence — a 5-field cron expression evaluated in
                UTC (e.g. ``"0 2 * * *"``) — that every environment inherits
                unless it sets its own override.
            configuration: The HTTP request the job sends each time it fires.
            description: Free-text description for the job. Defaults to none.
            environments: Per-environment overrides keyed by environment key —
                each a :class:`JobEnvironment`, or a plain dict
                ``{"enabled": bool}`` optionally with ``"schedule"`` /
                ``"configuration"`` overrides. The job is scheduled only in
                environments enabled here.
            concurrency_policy: How overlapping runs are handled. ``"ALLOW"``
                (the default and only value today) permits a new run to start
                while a previous one is still in flight.

        Returns:
            An unsaved recurring :class:`AsyncJob` bound to this client.
        """
        return self._new_job(
            id,
            name=name,
            schedule=schedule,
            configuration=configuration,
            description=description,
            environments=environments,
            concurrency_policy=concurrency_policy,
            environment=None,
        )

    def new_manual_job(
        self,
        id: str,
        *,
        name: str,
        configuration: HttpConfig,
        description: Optional[str] = None,
        environments: Optional[dict[str, "JobEnvironment | dict[str, Any]"]] = None,
        concurrency_policy: str = "ALLOW",
    ) -> AsyncJob:
        """Return an unsaved manual :class:`AsyncJob`. ``await .save()`` to create it.

        A manual job has no schedule — it never auto-fires and runs only when
        triggered via :meth:`run` / :meth:`AsyncJob.trigger`.

        Args:
            id: Caller-supplied unique identifier for the job. Unique within
                the account and immutable; the service returns 409 if another
                live job already uses this id.
            name: Human-readable name for the job.
            configuration: The HTTP request the job sends each time it runs.
            description: Free-text description for the job. Defaults to none.
            environments: Per-environment overrides keyed by environment key —
                each a :class:`JobEnvironment`, or a plain dict
                ``{"enabled": bool}`` optionally with a ``"configuration"``
                override. The job is triggerable only in environments enabled
                here.
            concurrency_policy: How overlapping runs are handled. ``"ALLOW"``
                (the default and only value today) permits a new run to start
                while a previous one is still in flight.

        Returns:
            An unsaved manual :class:`AsyncJob` bound to this client.
        """
        return self._new_job(
            id,
            name=name,
            schedule=None,
            configuration=configuration,
            description=description,
            environments=environments,
            concurrency_policy=concurrency_policy,
            environment=None,
        )

    def schedule(
        self,
        id: str,
        *,
        name: str,
        schedule: datetime.datetime,
        configuration: HttpConfig,
        description: Optional[str] = None,
        concurrency_policy: str = "ALLOW",
        environment: Optional[str] = None,
    ) -> AsyncJob:
        """Return an unsaved one-off :class:`AsyncJob`. ``await .save()`` to create it.

        A one-off job runs a single time at ``schedule`` and is then spent.

        Args:
            id: Caller-supplied unique identifier for the job. Unique within
                the account and immutable; the service returns 409 if another
                live job already uses this id.
            name: Human-readable name for the job.
            schedule: The instant the single run fires, as a ``datetime``.
            configuration: The HTTP request the job sends when it runs.
            description: Free-text description for the job. Defaults to none.
            concurrency_policy: How overlapping runs are handled. ``"ALLOW"``
                (the default and only value today) permits a new run to start
                while a previous one is still in flight.
            environment: The environment the job is born in. Defaults to the
                client's configured environment.

        Returns:
            An unsaved one-off :class:`AsyncJob` bound to this client.
        """
        return self._new_job(
            id,
            name=name,
            schedule=schedule.isoformat(),
            configuration=configuration,
            description=description,
            environments=None,
            concurrency_policy=concurrency_policy,
            environment=environment,
        )

    async def list(
        self,
        *,
        kind: Optional[JobKind] = None,
        scheduled: Optional[bool] = None,
        name: Optional[str] = None,
        page_number: Optional[int] = None,
        page_size: Optional[int] = None,
    ) -> list[AsyncJob]:
        """List jobs in the account.

        Args:
            kind: Return only jobs of this :class:`JobKind`. ``None`` lists
                recurring and manual jobs; one-off jobs are omitted unless you
                pass :attr:`JobKind.ONE_OFF`.
            scheduled: Return only jobs that have an upcoming fire in some
                environment (``True``) or none (``False``) — the feed for an
                upcoming-runs view, which includes one-offs. ``None`` does not
                filter on scheduling.
            name: Return only jobs whose name contains this text
                (case-insensitive). ``None`` lists all.
            page_number: 1-based page to return. ``None`` returns the first
                page.
            page_size: Maximum number of jobs to return in this page. ``None``
                uses the server default.

        Returns:
            The jobs in this page, as a list of :class:`AsyncJob`.
        """
        resp = await _gen_list_jobs.asyncio_detailed(
            client=self._auth, **_list_jobs_kwargs(kind, scheduled, name, page_number, page_size)
        )
        _check(resp)
        return [AsyncJob._from_resource(r, self) for r in _data(resp)]

    async def get(self, id: str) -> AsyncJob:
        """Fetch a single job by its id.

        Args:
            id: Identifier of the job to fetch.

        Returns:
            The matching :class:`AsyncJob`.
        """
        resp = await _gen_get_job.asyncio_detailed(id, client=self._auth)
        _check(resp)
        return AsyncJob._from_resource(_data(resp), self)

    async def delete(self, id: str) -> None:
        """Delete a job by its id.

        Args:
            id: Identifier of the job to delete.
        """
        resp = await _gen_delete_job.asyncio_detailed(id, client=self._auth)
        _check(resp)

    async def run(self, id: str, *, environment: Optional[str] = None) -> AsyncRun:
        """Trigger one immediate, manual run of a job, ignoring its schedule.

        This starts an ad-hoc run right now in addition to any scheduled runs;
        it does not alter the job's schedule. To read or act on existing runs,
        use ``jobs.runs``.

        Args:
            id: Identifier of the job to run.
            environment: Environment the manual run executes in. Defaults to the
                client's configured environment; when the job is enabled in
                exactly one environment that environment is used, and a
                single-environment credential implies it. The job must be
                enabled in the chosen environment.

        Returns:
            The :class:`AsyncRun` that was started, with ``trigger`` set to
            ``"MANUAL"``.
        """
        resp = await _gen_run_job_now.asyncio_detailed(
            id,
            client=self._auth,
            x_smplkit_environment=_env_header(environment if environment is not None else self._environment),
        )
        _check(resp)
        return AsyncRun._from_resource(_data(resp), self.runs)

    async def usage(self) -> Usage:
        """Report current-period usage against the account's plan allotments.

        Returns:
            A :class:`Usage` snapshot with runs used/included and active-job
            counts for the current period.
        """
        resp = await _gen_get_usage.asyncio_detailed(client=self._auth)
        _check(resp)
        return Usage._from_resource(_data(resp))

    async def _create(self, job: AsyncJob) -> AsyncJob:
        resp = await _gen_create_job.asyncio_detailed(
            client=self._auth,
            body=_job_body(job, request_cls=JobCreateRequest),
            x_smplkit_environment=_env_header(job._birth_environment),
        )
        _check(resp)
        return AsyncJob._from_resource(_data(resp), self)

    async def _update(self, job: AsyncJob) -> AsyncJob:
        resp = await _gen_update_job.asyncio_detailed(
            job.id,
            client=self._auth,
            body=_job_body(job, request_cls=JobRequest),
            x_smplkit_environment=_env_header(self._environment),
        )
        _check(resp)
        return AsyncJob._from_resource(_data(resp), self)

    async def aclose(self) -> None:
        """Release async HTTP resources — only when this client owns its transport."""
        if self._owns_transport:
            ac = self._auth._async_client
            if ac is not None:
                await ac.aclose()
                self._auth._async_client = None

    async def __aenter__(self) -> "AsyncJobsClient":
        return self

    async def __aexit__(self, *args: object) -> None:
        await self.aclose()
