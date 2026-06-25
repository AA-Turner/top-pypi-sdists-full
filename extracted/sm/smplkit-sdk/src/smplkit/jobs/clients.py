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
from smplkit._generated.jobs.api.retry_policies import (
    create_retry_policy as _gen_create_retry_policy,
    delete_retry_policy as _gen_delete_retry_policy,
    get_retry_policy as _gen_get_retry_policy,
    list_retry_policies as _gen_list_retry_policies,
    update_retry_policy as _gen_update_retry_policy,
)
from smplkit._generated.jobs.api.usage import get_usage as _gen_get_usage
from smplkit._generated.jobs.client import AuthenticatedClient as _JobsAuthClient
from smplkit._generated.jobs.models.job_create_request import JobCreateRequest
from smplkit._generated.jobs.models.job_request import JobRequest
from smplkit._generated.jobs.models.run_now_request import RunNowRequest
from smplkit._generated.jobs.models.retry_policy_create_request import RetryPolicyCreateRequest
from smplkit._generated.jobs.models.retry_policy_request import RetryPolicyRequest

__all__ = [
    "HttpConfig",
    "JobEnvironment",
    "JobKind",
    "RunTrigger",
    "Backoff",
    "RunRetry",
    "Job",
    "AsyncJob",
    "Run",
    "AsyncRun",
    "Usage",
    "RetryPolicy",
    "AsyncRetryPolicy",
    "RunsClient",
    "AsyncRunsClient",
    "RetryPoliciesClient",
    "AsyncRetryPoliciesClient",
    "JobsClient",
    "AsyncJobsClient",
]


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
        RETRY: An automatic retry of a failed run, per the job's retry policy.
        SCHEDULE: The job's schedule fired.
    """

    MANUAL = "MANUAL"
    RERUN = "RERUN"
    RETRY = "RETRY"
    SCHEDULE = "SCHEDULE"


class Backoff(str, Enum):
    """How the wait between retries grows (a retry policy's backoff strategy).

    Attributes:
        EXPONENTIAL: Double the wait each retry — ``delay_seconds``, then ``2×``,
            ``4×``, … — capped at ``max_delay_seconds``.
        FIXED: Wait a constant ``delay_seconds`` before every retry.
    """

    EXPONENTIAL = "exponential"
    FIXED = "fixed"


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


def _coerce_policy_id(value: "RetryPolicy | AsyncRetryPolicy | str | None") -> Optional[str]:
    """Coerce a retry-policy reference to its id.

    Accepts a policy id string, a :class:`RetryPolicy` / :class:`AsyncRetryPolicy`
    instance (its ``id`` is used), or ``None`` (no override / inherit). This is
    the one coercion behind the ``retry_policy`` attribute on both :class:`Job`
    and :class:`JobEnvironment`, so ``x.retry_policy = some_policy`` and
    ``x.retry_policy = "retry-on-5xx"`` both work.
    """
    if value is None:
        return None
    return value.id if isinstance(value, _RetryPolicyBase) else value


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
        headers: Optional[dict[str, str]] = None,
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
            headers: Headers attached to the request, as a name→value object
                (e.g. ``{"Authorization": "Bearer s3cr3t"}``). Defaults to no
                extra headers.
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
        self.headers: dict[str, str] = dict(headers or {})
        self.body = body
        self.success_status = success_status
        self.timeout = timeout
        self.tls_verify = tls_verify
        self.ca_cert = ca_cert

    def set_header(self, name: str, value: str) -> None:
        """Set (or replace) a single request header by name."""
        self.headers[name] = value

    def get_header(self, name: str) -> Optional[str]:
        """The value of header ``name``, or ``None`` if it is not set."""
        return self.headers.get(name)

    def to_dict(self) -> dict[str, Any]:
        return {
            "method": self.method,
            "url": self.url,
            "headers": dict(self.headers),
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
                and optional ``method``, ``headers`` (a name→value object),
                ``body``, ``success_status``, ``timeout``, ``tls_verify``, and
                ``ca_cert`` entries. Omitted keys fall back to their defaults.

        Returns:
            The corresponding :class:`HttpConfig`.
        """
        return cls(
            url=d["url"],
            method=d.get("method", "POST"),
            headers=dict(d.get("headers") or {}),
            body=d.get("body"),
            success_status=d.get("success_status", "2xx"),
            timeout=d.get("timeout", 30),
            tls_verify=d.get("tls_verify", True),
            ca_cert=d.get("ca_cert"),
        )

    def __repr__(self) -> str:
        return f"HttpConfig(method={self.method!r}, url={self.url!r})"


# The request-config leaves an environment may override (everything except
# headers, which are addressed individually as ``headers.<name>``). These map
# 1:1 onto :class:`HttpConfig` fields and onto top-level overlay leaf paths.
_REQUEST_LEAVES = ("url", "method", "timeout", "body", "success_status", "tls_verify", "ca_cert")
# The scalar (non-header) overlay leaves, in payload order.
_SCALAR_LEAVES = ("schedule", "timezone", "retry_policy", *_REQUEST_LEAVES)


class JobEnvironment:
    """One environment's **sparse override** for a job (ADR-056).

    A job's :attr:`Job.environments` map holds one of these per environment. Only
    the leaves you set are sent on save; everything you leave unset is inherited
    from the job's base definition, and the server resolves base ⊕ overrides when
    the job fires. The base definition is disabled everywhere, so a job runs in an
    environment only when that environment's override sets ``enabled=True``.

    Set overrides through :meth:`Job.environment`, e.g.
    ``job.environment("production").url = "https://prod.example.com/warm"``.

    **Reading a leaf returns this environment's override, or ``None`` when it does
    not override that leaf** — the SDK does not merge in the base value (jobs
    resolve server-side). To see a base value, read the job's base definition
    (``job.configuration``, ``job.schedule``, …).

    Attributes:
        enabled: Whether the job runs in this environment. Defaults to ``False``.
        schedule: Per-environment cron override (recurring jobs only). ``None``
            inherits the base :attr:`Job.schedule`.
        timezone: Per-environment IANA timezone override (recurring jobs only).
            ``None`` inherits the base :attr:`Job.timezone`, else UTC.
        retry_policy: Per-environment retry-policy override — a policy id, a
            :class:`RetryPolicy` (coerced to its id), or ``"Default"``. ``None``
            inherits the base :attr:`Job.retry_policy`.
        url, method, timeout, body, success_status, tls_verify, ca_cert:
            Per-environment overrides of the corresponding request field.
            ``None`` inherits the base :attr:`Job.configuration` value.
        headers: Per-environment header overrides, as a name→value object. Each
            entry overrides (or adds) that one header by name on top of the base
            headers, leaving the rest inherited. Use :meth:`set_header` /
            :meth:`get_header`.
        next_run_at: Read-only next scheduled fire time in this environment (UTC),
            or ``None`` when not enabled / once a one-off has fired. Never sent on
            save.
    """

    def __init__(
        self,
        *,
        enabled: bool = False,
        schedule: Optional[str] = None,
        timezone: Optional[str] = None,
        retry_policy: "RetryPolicy | AsyncRetryPolicy | str | None" = None,
        url: Optional[str] = None,
        method: Optional[str] = None,
        timeout: Optional[int] = None,
        body: Optional[str] = None,
        success_status: Optional[str] = None,
        tls_verify: Optional[bool] = None,
        ca_cert: Optional[str] = None,
        headers: Optional[dict[str, str]] = None,
        next_run_at: Optional[datetime.datetime] = None,
    ) -> None:
        self.enabled = enabled
        self.schedule = schedule
        self.timezone = timezone
        self.retry_policy = retry_policy  # coercing property
        self.url = url
        self.method = method
        self.timeout = timeout
        self.body = body
        self.success_status = success_status
        self.tls_verify = tls_verify
        self.ca_cert = ca_cert
        self.headers: dict[str, str] = dict(headers or {})
        self.next_run_at = next_run_at

    @property
    def retry_policy(self) -> Optional[str]:
        return self._retry_policy

    @retry_policy.setter
    def retry_policy(self, value: "RetryPolicy | AsyncRetryPolicy | str | None") -> None:
        self._retry_policy = _coerce_policy_id(value)

    def set_header(self, name: str, value: str) -> None:
        """Override (or add) a single header by name in this environment."""
        self.headers[name] = value

    def get_header(self, name: str) -> Optional[str]:
        """This environment's override for header ``name``, or ``None`` when it
        does not override that header."""
        return self.headers.get(name)

    @classmethod
    def _from_dict(cls, raw: dict[str, Any]) -> "JobEnvironment":
        """Parse the flat leaf-path overlay the server returns (ADR-056).

        Header leaves arrive as ``headers.<name>`` (parsed on the first dot, so a
        dotted header name like ``X-Foo.Bar`` is preserved); every other leaf is
        a single top-level key. Unknown leaves are ignored for forward
        compatibility.
        """
        headers: dict[str, str] = {}
        scalars: dict[str, Any] = {}
        for key, value in (raw or {}).items():
            if key == "next_run_at":
                continue
            group, _, name = key.partition(".")
            if group == "headers" and name:
                headers[name] = value
            elif key in _SCALAR_LEAVES or key == "enabled":
                scalars[key] = value
        return cls(
            enabled=bool(scalars.get("enabled", False)),
            schedule=scalars.get("schedule"),
            timezone=scalars.get("timezone"),
            retry_policy=scalars.get("retry_policy"),
            url=scalars.get("url"),
            method=scalars.get("method"),
            timeout=scalars.get("timeout"),
            body=scalars.get("body"),
            success_status=scalars.get("success_status"),
            tls_verify=scalars.get("tls_verify"),
            ca_cert=scalars.get("ca_cert"),
            headers=headers,
            next_run_at=_parse_dt(raw.get("next_run_at")),
        )

    def _to_payload(self) -> dict[str, Any]:
        """Emit the flat sparse leaf-path overlay (ADR-056) — ``enabled`` plus
        only the leaves this environment overrides, with each header as a
        ``headers.<name>`` leaf."""
        payload: dict[str, Any] = {"enabled": self.enabled}
        for leaf in _SCALAR_LEAVES:
            value = getattr(self, leaf)
            if value is not None:
                payload[leaf] = value
        for name, value in self.headers.items():
            payload[f"headers.{name}"] = value
        return payload

    def __repr__(self) -> str:
        overridden = sorted(
            [leaf for leaf in _SCALAR_LEAVES if getattr(self, leaf) is not None]
            + [f"headers.{n}" for n in self.headers]
        )
        return f"JobEnvironment(enabled={self.enabled!r}, overrides={overridden!r})"


def _normalize_environments(
    environments: Optional[dict[str, "JobEnvironment | dict[str, Any]"]],
) -> dict[str, JobEnvironment]:
    """Coerce a loose ``environments`` mapping into ``{key: JobEnvironment}``.

    A value may be a :class:`JobEnvironment` (used as-is) or a plain dict of
    constructor kwargs (``{"enabled": True, "url": ..., "headers": {...}}``),
    which is splatted into :class:`JobEnvironment`.
    """
    if not environments:
        return {}
    out: dict[str, JobEnvironment] = {}
    for env_key, value in environments.items():
        out[env_key] = value if isinstance(value, JobEnvironment) else JobEnvironment(**value)
    return out


def _run_environment(value: Optional[str]) -> "str | Any":
    """A run-now ``environment`` body value, or ``UNSET`` when unset."""
    return value if value is not None else UNSET


def _birth_env_map(environment: Optional[str]) -> "Optional[dict[str, JobEnvironment]]":
    """A one-off job's birth environment as an enabled ``environments`` entry.

    The target environment of a one-off job is conveyed by the keys of the
    body's ``environments`` map (there is no request header). ``None`` when the
    environment is unknown, leaving the map empty so a single-environment
    credential implies it server-side.
    """
    if not environment:
        return None
    return {environment: JobEnvironment(enabled=True)}


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
        timezone: Optional[str] = None,
        retry_policy: Optional[str] = None,
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
        # Per-environment sparse overrides ``{env_key: JobEnvironment}`` (ADR-056).
        # Reach one via :meth:`environment` and set its ``enabled`` / leaf
        # overrides to make the job run (and vary its request) in that
        # environment. Each entry also reports its read-only ``next_run_at``.
        self.environments: dict[str, JobEnvironment] = environments if environments is not None else {}
        # Read-only server-derived kind (see :class:`JobKind`).
        self.kind = kind
        self.type = type
        self.schedule = schedule
        # Base IANA timezone the cron schedule is evaluated in (e.g.
        # "America/New_York"); ``None`` means UTC. The base every environment
        # inherits unless it sets its own timezone. The cron fires on this
        # zone's wall clock (DST-aware) while next_run_at stays a UTC instant.
        # Only meaningful on a recurring job. Sent on writes only when not None.
        self.timezone = timezone
        # Base retry policy for failed runs — the id of a RetryPolicy (or the
        # built-in "Default", which never retries), overridable per environment.
        # ``None`` (omitted on the wire) means Default. Sent only when not None.
        self.retry_policy = retry_policy
        self.configuration = configuration
        self.concurrency_policy = concurrency_policy
        self.created_at = created_at
        self.updated_at = updated_at
        self.deleted_at = deleted_at
        self.version = version

    @property
    def enabled(self) -> bool:
        """Read-only roll-up: ``True`` when enabled in at least one environment.

        Derived from the :attr:`environments` map — the job has no server-side
        top-level ``enabled`` field. Enable per environment via
        ``job.environment(env).enabled = True``.
        """
        return any(env.enabled for env in self.environments.values())

    @property
    def retry_policy(self) -> Optional[str]:
        """The base retry-policy id, or ``None`` for the built-in ``Default``.

        Assigning accepts a policy id string or a :class:`RetryPolicy` /
        :class:`AsyncRetryPolicy` instance (coerced to its id)."""
        return self._retry_policy

    @retry_policy.setter
    def retry_policy(self, value: "RetryPolicy | AsyncRetryPolicy | str | None") -> None:
        self._retry_policy = _coerce_policy_id(value)

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

    def environment(self, environment: str) -> JobEnvironment:
        """The per-environment override for ``environment`` — the single place to
        read or set what this job overrides there (ADR-056).

        Returns the :class:`JobEnvironment` for ``environment``, creating an empty
        one (and inserting it into :attr:`environments`) on first access, so you
        can set overrides directly::

            job.environment("production").enabled = True
            job.environment("production").url = "https://prod.example.com/warm"
            job.environment("production").set_header("Authorization", "Bearer prod")

        Only the leaves you set are sent on save; everything else inherits the
        base definition (the server resolves base ⊕ overrides when the job fires).
        """
        env = self.environments.get(environment)
        if env is None:
            env = JobEnvironment()
            self.environments[environment] = env
        return env

    def _attributes(self) -> dict[str, Any]:
        attrs: dict[str, Any] = {
            "name": self.name,
            "description": self.description,
            "type": self.type,
            "schedule": self.schedule,
            "configuration": self.configuration.to_dict(),
            "concurrency_policy": self.concurrency_policy,
        }
        # Timezone is the IANA zone the cron is evaluated in (recurring jobs
        # only); ``None`` is omitted, leaving the server default of UTC.
        if self.timezone is not None:
            attrs["timezone"] = self.timezone
        # Retry policy id; ``None`` is omitted, leaving the server default
        # (the built-in ``Default`` policy, which never retries).
        if self.retry_policy is not None:
            attrs["retry_policy"] = self.retry_policy
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
        timezone=a.get("timezone"),
        retry_policy=a.get("retry_policy"),
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
        job = cls(
            client,
            id=base.id,
            name=base.name,
            schedule=base.schedule,
            timezone=base.timezone,
            configuration=base.configuration,
        )
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
        triggers: Optional[list[RunTrigger]] = None,
        last_run_only: bool = False,
        page_size: Optional[int] = None,
        after: Optional[str] = None,
    ) -> "list[Run]":
        """List this job's run history, most recent first.

        Args:
            environment: Restrict to runs stamped with this environment. ``None``
                covers every environment you can access.
            triggers: Restrict to runs started by any of these triggers (see
                :class:`RunTrigger`) — e.g. ``[RunTrigger.RETRY]`` for automatic
                retries. ``None`` covers every trigger.
            last_run_only: When ``True``, return only the last completed run per
                environment (in-flight runs excluded). Defaults to ``False``.
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
            triggers=triggers,
            last_run_only=last_run_only,
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
        job = cls(
            client,
            id=base.id,
            name=base.name,
            schedule=base.schedule,
            timezone=base.timezone,
            configuration=base.configuration,
        )
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
        triggers: Optional[list[RunTrigger]] = None,
        last_run_only: bool = False,
        page_size: Optional[int] = None,
        after: Optional[str] = None,
    ) -> "list[AsyncRun]":
        """List this job's run history, most recent first.

        Args:
            environment: Restrict to runs stamped with this environment. ``None``
                covers every environment you can access.
            triggers: Restrict to runs started by any of these triggers (see
                :class:`RunTrigger`) — e.g. ``[RunTrigger.RETRY]`` for automatic
                retries. ``None`` covers every trigger.
            last_run_only: When ``True``, return only the last completed run per
                environment (in-flight runs excluded). Defaults to ``False``.
            page_size: Maximum number of runs to return in this page.
            after: Opaque cursor from a previous page.

        Returns:
            The runs in this page, as a list of :class:`AsyncRun`.
        """
        if self._client is None:
            raise RuntimeError("AsyncJob was constructed without a client; cannot list runs")
        return await self._client.runs.list(
            job=self.id,
            environments=[environment] if environment is not None else None,
            triggers=triggers,
            last_run_only=last_run_only,
            page_size=page_size,
            after=after,
        )


@dataclass(frozen=True, slots=True)
class RunRetry:
    """Where a ``RETRY`` run sits in its retry chain (read-only).

    Attributes:
        of: Id of the chain's original run — the first attempt that failed and
            started the chain.
        attempt: Which retry this run is — ``1`` for the first retry, ``2`` for
            the second, and so on.
    """

    of: str
    attempt: int


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
        # Retry-chain position, present only when ``trigger`` is ``RETRY``.
        retry = attributes.get("retry")
        self.retry: Optional[RunRetry] = RunRetry(of=str(retry["of"]), attempt=retry["attempt"]) if retry else None
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


class _RetryPolicyBase:
    """Shared state for ``RetryPolicy`` / ``AsyncRetryPolicy``."""

    def __init__(
        self,
        *,
        id: str,
        name: str,
        max_retries: int,
        backoff: Backoff,
        delay_seconds: int,
        max_delay_seconds: Optional[int] = None,
        retry_on_timeout: bool = False,
        retry_on_connection_error: bool = False,
        retry_statuses: Optional[list[str]] = None,
        retry_statuses_except: Optional[list[str]] = None,
        created_at: Optional[datetime.datetime] = None,
        updated_at: Optional[datetime.datetime] = None,
        deleted_at: Optional[datetime.datetime] = None,
        version: Optional[int] = None,
    ) -> None:
        self.id = id
        self.name = name
        self.max_retries = max_retries
        self.backoff = backoff
        self.delay_seconds = delay_seconds
        # Ceiling on the wait between retries, for ``exponential`` backoff only;
        # ``None`` (omitted) leaves it uncapped. Invalid with ``fixed`` backoff.
        self.max_delay_seconds = max_delay_seconds
        # Which failures to retry. Each field is independently neutral, so a
        # policy retries exactly the failures you opt into; all-off retries
        # nothing. ``retry_statuses`` allowlists response statuses (exact codes
        # like ``"429"`` or classes like ``"5xx"``) on a non-success response,
        # and ``retry_statuses_except`` subtracts from it (``except`` wins).
        self.retry_on_timeout = retry_on_timeout
        self.retry_on_connection_error = retry_on_connection_error
        self.retry_statuses = list(retry_statuses) if retry_statuses is not None else []
        self.retry_statuses_except = list(retry_statuses_except) if retry_statuses_except is not None else []
        self.created_at = created_at
        self.updated_at = updated_at
        self.deleted_at = deleted_at
        self.version = version

    def _apply(self, other: "_RetryPolicyBase") -> None:
        self.__dict__.update({k: v for k, v in other.__dict__.items() if not k.startswith("_client")})

    def _attributes(self) -> dict[str, Any]:
        attrs: dict[str, Any] = {
            "name": self.name,
            "max_retries": self.max_retries,
            "backoff": Backoff(self.backoff).value,
            "delay_seconds": self.delay_seconds,
            "retry_on_timeout": self.retry_on_timeout,
            "retry_on_connection_error": self.retry_on_connection_error,
            "retry_statuses": list(self.retry_statuses),
            "retry_statuses_except": list(self.retry_statuses_except),
        }
        # Only valid with exponential backoff; omitted when unset.
        if self.max_delay_seconds is not None:
            attrs["max_delay_seconds"] = self.max_delay_seconds
        return attrs

    def __repr__(self) -> str:
        return f"RetryPolicy(id={self.id!r}, name={self.name!r}, max_retries={self.max_retries!r})"


def _retry_policy_base_from_resource(resource: dict[str, Any]) -> _RetryPolicyBase:
    a = resource["attributes"]
    return _RetryPolicyBase(
        id=resource["id"],
        name=a["name"],
        max_retries=a["max_retries"],
        backoff=Backoff(a["backoff"]),
        delay_seconds=a["delay_seconds"],
        max_delay_seconds=a.get("max_delay_seconds"),
        retry_on_timeout=bool(a.get("retry_on_timeout", False)),
        retry_on_connection_error=bool(a.get("retry_on_connection_error", False)),
        retry_statuses=list(a.get("retry_statuses") or []),
        retry_statuses_except=list(a.get("retry_statuses_except") or []),
        created_at=_parse_dt(a.get("created_at")),
        updated_at=_parse_dt(a.get("updated_at")),
        deleted_at=_parse_dt(a.get("deleted_at")),
        version=a.get("version"),
    )


class RetryPolicy(_RetryPolicyBase):
    """A named, reusable retry policy (sync). Mutate fields, then call :meth:`save`."""

    def __init__(self, client: "Optional[RetryPoliciesClient]" = None, **kwargs: Any) -> None:
        super().__init__(**kwargs)
        self._client = client

    @classmethod
    def _from_resource(cls, resource: dict[str, Any], client: "RetryPoliciesClient") -> "RetryPolicy":
        base = _retry_policy_base_from_resource(resource)
        policy = cls(
            client,
            id=base.id,
            name=base.name,
            max_retries=base.max_retries,
            backoff=base.backoff,
            delay_seconds=base.delay_seconds,
        )
        policy._apply(base)
        return policy

    def save(self) -> None:
        """Create this policy, or full-replace it if it already exists."""
        if self._client is None:
            raise RuntimeError("RetryPolicy was constructed without a client; cannot save")
        other = self._client._create(self) if self.created_at is None else self._client._update(self)
        self._apply(other)

    def delete(self) -> None:
        """Delete this policy."""
        if self._client is None:
            raise RuntimeError("RetryPolicy was constructed without a client; cannot delete")
        self._client.delete(self.id)


class AsyncRetryPolicy(_RetryPolicyBase):
    """A named, reusable retry policy (async). Mutate fields, then ``await save()``."""

    def __init__(self, client: "Optional[AsyncRetryPoliciesClient]" = None, **kwargs: Any) -> None:
        super().__init__(**kwargs)
        self._client = client

    @classmethod
    def _from_resource(cls, resource: dict[str, Any], client: "AsyncRetryPoliciesClient") -> "AsyncRetryPolicy":
        base = _retry_policy_base_from_resource(resource)
        policy = cls(
            client,
            id=base.id,
            name=base.name,
            max_retries=base.max_retries,
            backoff=base.backoff,
            delay_seconds=base.delay_seconds,
        )
        policy._apply(base)
        return policy

    async def save(self) -> None:
        if self._client is None:
            raise RuntimeError("AsyncRetryPolicy was constructed without a client; cannot save")
        other = await self._client._create(self) if self.created_at is None else await self._client._update(self)
        self._apply(other)

    async def delete(self) -> None:
        if self._client is None:
            raise RuntimeError("AsyncRetryPolicy was constructed without a client; cannot delete")
        await self._client.delete(self.id)


def _retry_policy_body(policy: _RetryPolicyBase, *, request_cls: Any) -> Any:
    return request_cls.from_dict(
        {"data": {"id": policy.id, "type": "retry_policy", "attributes": policy._attributes()}}
    )


def _retry_policy_list_kwargs(name, page_number, page_size) -> dict[str, Any]:
    kwargs: dict[str, Any] = {}
    if name is not None:
        kwargs["filtername"] = name
    if page_number is not None:
        kwargs["pagenumber"] = page_number
    if page_size is not None:
        kwargs["pagesize"] = page_size
    return kwargs


def _job_body(job: _JobBase, *, request_cls: Any) -> Any:
    return request_cls.from_dict({"data": {"id": job.id, "type": "job", "attributes": job._attributes()}})


def _new_kwargs(
    id, *, name, schedule, timezone, retry_policy, configuration, description, environments, concurrency_policy
):
    return {
        "id": id,
        "name": name,
        "schedule": schedule,
        "timezone": timezone,
        "retry_policy": retry_policy,
        "configuration": configuration,
        "description": description,
        "environments": environments,
        "concurrency_policy": concurrency_policy,
    }


def _run_list_kwargs(
    job: Optional[str],
    triggers: Optional[list[RunTrigger]],
    last_run_only: bool,
    page_size: Optional[int],
    after: Optional[str],
) -> dict[str, Any]:
    kwargs: dict[str, Any] = {}
    if job is not None:
        kwargs["filterjob"] = job
    if triggers:
        kwargs["filtertrigger"] = ",".join(t.value for t in triggers)
    # The generated default (False) would emit ``last_run_only=false`` on every
    # call; pass UNSET unless explicitly requested so the param stays off the wire.
    kwargs["last_run_only"] = True if last_run_only else UNSET
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
        triggers: Optional[list[RunTrigger]] = None,
        last_run_only: bool = False,
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
            triggers: Restrict to runs started by any of these triggers (see
                :class:`RunTrigger`) — e.g. ``[RunTrigger.RETRY]`` for automatic
                retries. ``None`` covers every trigger.
            last_run_only: When ``True``, collapse the result to the last
                completed (succeeded / failed / canceled) run per
                job-and-environment; in-flight runs are excluded. The other
                filters apply first, then the collapse. Defaults to ``False``.
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
            **_run_list_kwargs(job, triggers, last_run_only, page_size, after),
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
        triggers: Optional[list[RunTrigger]] = None,
        last_run_only: bool = False,
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
            triggers: Restrict to runs started by any of these triggers (see
                :class:`RunTrigger`) — e.g. ``[RunTrigger.RETRY]`` for automatic
                retries. ``None`` covers every trigger.
            last_run_only: When ``True``, collapse the result to the last
                completed (succeeded / failed / canceled) run per
                job-and-environment; in-flight runs are excluded. The other
                filters apply first, then the collapse. Defaults to ``False``.
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
            **_run_list_kwargs(job, triggers, last_run_only, page_size, after),
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


class RetryPoliciesClient:
    """Manage reusable retry policies (``jobs.retry_policies``).

    Reached as ``client.jobs.retry_policies``. A :class:`RetryPolicy` is an
    active record: build one with :meth:`new`, set fields, and call ``save()``;
    then reference it from a job's ``retry_policy`` (base: ``job.retry_policy =
    policy``; per-environment: ``job.environment(env).retry_policy = policy``).
    Retry policies are account-global — never environment-scoped.
    """

    def __init__(self, auth: _JobsAuthClient) -> None:
        self._auth = auth

    def new(
        self,
        id: str,
        *,
        name: str,
        max_retries: int,
        backoff: Backoff,
        delay_seconds: int,
        max_delay_seconds: Optional[int] = None,
        retry_on_timeout: bool = False,
        retry_on_connection_error: bool = False,
        retry_statuses: Optional[list[str]] = None,
        retry_statuses_except: Optional[list[str]] = None,
    ) -> RetryPolicy:
        """Return an unsaved :class:`RetryPolicy`. Call ``.save()`` to create it.

        Args:
            id: Caller-supplied unique identifier for the policy. Unique within
                the account and immutable; the service returns 409 if another
                live policy already uses this id.
            name: Human-readable name for the policy.
            max_retries: How many times a failed run is retried after the
                initial attempt — ``3`` means up to 4 attempts total. ``0``
                disables retries. Maximum 10.
            backoff: How the wait between retries grows (see :class:`Backoff`).
            delay_seconds: The wait before a retry, in seconds — the constant
                wait for ``fixed`` backoff, or the base that doubles each retry
                for ``exponential``.
            max_delay_seconds: Ceiling on the wait between retries, for
                ``exponential`` backoff only. ``None`` (the default) leaves it
                uncapped; omit it for ``fixed`` backoff.
            retry_on_timeout: Retry a run that timed out. Defaults to ``False``.
            retry_on_connection_error: Retry a run whose destination could not
                be reached. Defaults to ``False``.
            retry_statuses: Allowlist of response status patterns to retry on a
                non-success response — each an exact 3-digit code (``"429"``) or
                a class (``"5xx"``). ``None`` (the default) matches nothing.
            retry_statuses_except: Patterns subtracted from ``retry_statuses``
                (``except`` wins on overlap), same syntax. ``None`` (the
                default) subtracts nothing.

        Returns:
            An unsaved :class:`RetryPolicy` bound to this client.
        """
        return RetryPolicy(
            self,
            id=id,
            name=name,
            max_retries=max_retries,
            backoff=backoff,
            delay_seconds=delay_seconds,
            max_delay_seconds=max_delay_seconds,
            retry_on_timeout=retry_on_timeout,
            retry_on_connection_error=retry_on_connection_error,
            retry_statuses=retry_statuses,
            retry_statuses_except=retry_statuses_except,
        )

    def list(
        self,
        *,
        name: Optional[str] = None,
        page_number: Optional[int] = None,
        page_size: Optional[int] = None,
    ) -> list[RetryPolicy]:
        """List retry policies in the account.

        Args:
            name: Return only policies whose name contains this text
                (case-insensitive). ``None`` lists all.
            page_number: 1-based page to return. ``None`` returns the first page.
            page_size: Maximum number of policies to return in this page.
                ``None`` uses the server default.

        Returns:
            The policies in this page, as a list of :class:`RetryPolicy`.
        """
        resp = _gen_list_retry_policies.sync_detailed(
            client=self._auth, **_retry_policy_list_kwargs(name, page_number, page_size)
        )
        _check(resp)
        return [RetryPolicy._from_resource(r, self) for r in _data(resp)]

    def get(self, id: str) -> RetryPolicy:
        """Fetch a single retry policy by its id.

        Args:
            id: Identifier of the policy to fetch.

        Returns:
            The matching :class:`RetryPolicy`.
        """
        resp = _gen_get_retry_policy.sync_detailed(id, client=self._auth)
        _check(resp)
        return RetryPolicy._from_resource(_data(resp), self)

    def delete(self, id: str) -> None:
        """Delete a retry policy by its id.

        Args:
            id: Identifier of the policy to delete.
        """
        resp = _gen_delete_retry_policy.sync_detailed(id, client=self._auth)
        _check(resp)

    def _create(self, policy: RetryPolicy) -> RetryPolicy:
        resp = _gen_create_retry_policy.sync_detailed(
            client=self._auth, body=_retry_policy_body(policy, request_cls=RetryPolicyCreateRequest)
        )
        _check(resp)
        return RetryPolicy._from_resource(_data(resp), self)

    def _update(self, policy: RetryPolicy) -> RetryPolicy:
        resp = _gen_update_retry_policy.sync_detailed(
            policy.id, client=self._auth, body=_retry_policy_body(policy, request_cls=RetryPolicyRequest)
        )
        _check(resp)
        return RetryPolicy._from_resource(_data(resp), self)


class AsyncRetryPoliciesClient:
    """Manage reusable retry policies (``jobs.retry_policies``), awaited.

    Async counterpart of :class:`RetryPoliciesClient`, reached as
    ``client.jobs.retry_policies`` on an async client.
    """

    def __init__(self, auth: _JobsAuthClient) -> None:
        self._auth = auth

    def new(
        self,
        id: str,
        *,
        name: str,
        max_retries: int,
        backoff: Backoff,
        delay_seconds: int,
        max_delay_seconds: Optional[int] = None,
        retry_on_timeout: bool = False,
        retry_on_connection_error: bool = False,
        retry_statuses: Optional[list[str]] = None,
        retry_statuses_except: Optional[list[str]] = None,
    ) -> AsyncRetryPolicy:
        """Return an unsaved :class:`AsyncRetryPolicy`. ``await .save()`` to create it.

        See :meth:`RetryPoliciesClient.new` for the argument semantics.

        Returns:
            An unsaved :class:`AsyncRetryPolicy` bound to this client.
        """
        return AsyncRetryPolicy(
            self,
            id=id,
            name=name,
            max_retries=max_retries,
            backoff=backoff,
            delay_seconds=delay_seconds,
            max_delay_seconds=max_delay_seconds,
            retry_on_timeout=retry_on_timeout,
            retry_on_connection_error=retry_on_connection_error,
            retry_statuses=retry_statuses,
            retry_statuses_except=retry_statuses_except,
        )

    async def list(
        self,
        *,
        name: Optional[str] = None,
        page_number: Optional[int] = None,
        page_size: Optional[int] = None,
    ) -> list[AsyncRetryPolicy]:
        """List retry policies in the account.

        See :meth:`RetryPoliciesClient.list` for the argument semantics.

        Returns:
            The policies in this page, as a list of :class:`AsyncRetryPolicy`.
        """
        resp = await _gen_list_retry_policies.asyncio_detailed(
            client=self._auth, **_retry_policy_list_kwargs(name, page_number, page_size)
        )
        _check(resp)
        return [AsyncRetryPolicy._from_resource(r, self) for r in _data(resp)]

    async def get(self, id: str) -> AsyncRetryPolicy:
        """Fetch a single retry policy by its id.

        Returns:
            The matching :class:`AsyncRetryPolicy`.
        """
        resp = await _gen_get_retry_policy.asyncio_detailed(id, client=self._auth)
        _check(resp)
        return AsyncRetryPolicy._from_resource(_data(resp), self)

    async def delete(self, id: str) -> None:
        """Delete a retry policy by its id."""
        resp = await _gen_delete_retry_policy.asyncio_detailed(id, client=self._auth)
        _check(resp)

    async def _create(self, policy: AsyncRetryPolicy) -> AsyncRetryPolicy:
        resp = await _gen_create_retry_policy.asyncio_detailed(
            client=self._auth, body=_retry_policy_body(policy, request_cls=RetryPolicyCreateRequest)
        )
        _check(resp)
        return AsyncRetryPolicy._from_resource(_data(resp), self)

    async def _update(self, policy: AsyncRetryPolicy) -> AsyncRetryPolicy:
        resp = await _gen_update_retry_policy.asyncio_detailed(
            policy.id, client=self._auth, body=_retry_policy_body(policy, request_cls=RetryPolicyRequest)
        )
        _check(resp)
        return AsyncRetryPolicy._from_resource(_data(resp), self)


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
        self.retry_policies = RetryPoliciesClient(self._auth)

    def _new_job(
        self,
        id: str,
        *,
        name: str,
        schedule: Optional[str],
        timezone: Optional[str],
        retry_policy: Optional[str],
        configuration: HttpConfig,
        description: Optional[str],
        environments: Optional[dict[str, "JobEnvironment | dict[str, Any]"]],
        concurrency_policy: str,
    ) -> Job:
        job = Job(
            self,
            **_new_kwargs(
                id,
                name=name,
                schedule=schedule,
                timezone=timezone,
                retry_policy=retry_policy,
                configuration=configuration,
                description=description,
                environments=_normalize_environments(environments),
                concurrency_policy=concurrency_policy,
            ),
        )
        return job

    def new_recurring_job(
        self,
        id: str,
        *,
        name: str,
        schedule: str,
        timezone: Optional[str] = None,
        retry_policy: Optional[str] = None,
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
                the job's ``timezone`` (UTC by default), e.g. ``"0 2 * * *"`` —
                that every environment inherits unless it sets its own override.
            timezone: Base IANA timezone the cron ``schedule`` is evaluated in
                (e.g. ``"America/New_York"``), DST-aware. ``None`` (the default)
                means UTC. Every environment inherits it unless it overrides it.
            retry_policy: Base retry policy for failed runs — the id of a
                :class:`RetryPolicy`, overridable per environment. ``None`` (the
                default) uses the built-in ``Default`` policy, which never
                retries.
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
            timezone=timezone,
            retry_policy=retry_policy,
            configuration=configuration,
            description=description,
            environments=environments,
            concurrency_policy=concurrency_policy,
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
        retry_policy: Optional[str] = None,
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
            retry_policy: Retry policy for failed runs — the id of a
                :class:`RetryPolicy`, overridable per environment. ``None`` (the
                default) uses the built-in ``Default`` policy, which never
                retries.

        Returns:
            An unsaved manual :class:`Job` bound to this client.
        """
        return self._new_job(
            id,
            name=name,
            schedule=None,
            timezone=None,
            retry_policy=retry_policy,
            configuration=configuration,
            description=description,
            environments=environments,
            concurrency_policy=concurrency_policy,
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
        retry_policy: Optional[str] = None,
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
            retry_policy: Retry policy for failed runs — the id of a
                :class:`RetryPolicy`. ``None`` (the default) uses the built-in
                ``Default`` policy, which never retries.
            environment: The environment the job is born in. Defaults to the
                client's configured environment.

        Returns:
            An unsaved one-off :class:`Job` bound to this client.
        """
        return self._new_job(
            id,
            name=name,
            schedule=schedule.isoformat(),
            timezone=None,
            retry_policy=retry_policy,
            configuration=configuration,
            description=description,
            environments=_birth_env_map(environment if environment is not None else self._environment),
            concurrency_policy=concurrency_policy,
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
            body=RunNowRequest(
                environment=_run_environment(environment if environment is not None else self._environment)
            ),
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
        )
        _check(resp)
        return Job._from_resource(_data(resp), self)

    def _update(self, job: Job) -> Job:
        resp = _gen_update_job.sync_detailed(
            job.id,
            client=self._auth,
            body=_job_body(job, request_cls=JobRequest),
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
        self.retry_policies = AsyncRetryPoliciesClient(self._auth)

    def _new_job(
        self,
        id: str,
        *,
        name: str,
        schedule: Optional[str],
        timezone: Optional[str],
        retry_policy: Optional[str],
        configuration: HttpConfig,
        description: Optional[str],
        environments: Optional[dict[str, "JobEnvironment | dict[str, Any]"]],
        concurrency_policy: str,
    ) -> AsyncJob:
        job = AsyncJob(
            self,
            **_new_kwargs(
                id,
                name=name,
                schedule=schedule,
                timezone=timezone,
                retry_policy=retry_policy,
                configuration=configuration,
                description=description,
                environments=_normalize_environments(environments),
                concurrency_policy=concurrency_policy,
            ),
        )
        return job

    def new_recurring_job(
        self,
        id: str,
        *,
        name: str,
        schedule: str,
        timezone: Optional[str] = None,
        retry_policy: Optional[str] = None,
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
                the job's ``timezone`` (UTC by default), e.g. ``"0 2 * * *"`` —
                that every environment inherits unless it sets its own override.
            timezone: Base IANA timezone the cron ``schedule`` is evaluated in
                (e.g. ``"America/New_York"``), DST-aware. ``None`` (the default)
                means UTC. Every environment inherits it unless it overrides it.
            retry_policy: Base retry policy for failed runs — the id of a
                :class:`RetryPolicy`, overridable per environment. ``None`` (the
                default) uses the built-in ``Default`` policy, which never
                retries.
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
            timezone=timezone,
            retry_policy=retry_policy,
            configuration=configuration,
            description=description,
            environments=environments,
            concurrency_policy=concurrency_policy,
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
        retry_policy: Optional[str] = None,
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
            retry_policy: Retry policy for failed runs — the id of a
                :class:`RetryPolicy`, overridable per environment. ``None`` (the
                default) uses the built-in ``Default`` policy, which never
                retries.

        Returns:
            An unsaved manual :class:`AsyncJob` bound to this client.
        """
        return self._new_job(
            id,
            name=name,
            schedule=None,
            timezone=None,
            retry_policy=retry_policy,
            configuration=configuration,
            description=description,
            environments=environments,
            concurrency_policy=concurrency_policy,
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
        retry_policy: Optional[str] = None,
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
            retry_policy: Retry policy for failed runs — the id of a
                :class:`RetryPolicy`. ``None`` (the default) uses the built-in
                ``Default`` policy, which never retries.
            environment: The environment the job is born in. Defaults to the
                client's configured environment.

        Returns:
            An unsaved one-off :class:`AsyncJob` bound to this client.
        """
        return self._new_job(
            id,
            name=name,
            schedule=schedule.isoformat(),
            timezone=None,
            retry_policy=retry_policy,
            configuration=configuration,
            description=description,
            environments=_birth_env_map(environment if environment is not None else self._environment),
            concurrency_policy=concurrency_policy,
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
            body=RunNowRequest(
                environment=_run_environment(environment if environment is not None else self._environment)
            ),
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
        )
        _check(resp)
        return AsyncJob._from_resource(_data(resp), self)

    async def _update(self, job: AsyncJob) -> AsyncJob:
        resp = await _gen_update_job.asyncio_detailed(
            job.id,
            client=self._auth,
            body=_job_body(job, request_cls=JobRequest),
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
