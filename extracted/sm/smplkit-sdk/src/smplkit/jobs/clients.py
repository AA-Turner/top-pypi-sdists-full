"""Smpl Jobs SDK client (``client.jobs`` on SmplClient, or standalone ``JobsClient``).

Smpl Jobs runs an HTTP call on a schedule and records what happened each
time it fired. A single :class:`JobsClient` (and its async counterpart
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
from typing import Any, Optional
from uuid import UUID

from smplkit._config import _service_url, resolve_client_config
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
    "Job",
    "AsyncJob",
    "Run",
    "Usage",
    "RunsClient",
    "AsyncRunsClient",
    "JobsClient",
    "AsyncJobsClient",
]

HttpHeader = tuple[str, str]


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


class _JobBase:
    """Shared state for ``Job`` / ``AsyncJob``."""

    def __init__(
        self,
        *,
        id: str,
        name: str,
        schedule: str,
        configuration: HttpConfig,
        description: Optional[str] = None,
        enabled: bool = True,
        type: str = "http",
        concurrency_policy: str = "ALLOW",
        next_run_at: Optional[datetime.datetime] = None,
        created_at: Optional[datetime.datetime] = None,
        updated_at: Optional[datetime.datetime] = None,
        deleted_at: Optional[datetime.datetime] = None,
        version: Optional[int] = None,
    ) -> None:
        self.id = id
        self.name = name
        self.description = description
        self.enabled = enabled
        self.type = type
        self.schedule = schedule
        self.configuration = configuration
        self.concurrency_policy = concurrency_policy
        self.next_run_at = next_run_at
        self.created_at = created_at
        self.updated_at = updated_at
        self.deleted_at = deleted_at
        self.version = version

    def _apply(self, other: "_JobBase") -> None:
        self.__dict__.update({k: v for k, v in other.__dict__.items() if not k.startswith("_client")})

    def _attributes(self) -> dict[str, Any]:
        return {
            "name": self.name,
            "description": self.description,
            "enabled": self.enabled,
            "type": self.type,
            "schedule": self.schedule,
            "configuration": self.configuration.to_dict(),
            "concurrency_policy": self.concurrency_policy,
        }

    def __repr__(self) -> str:
        return f"Job(id={self.id!r}, name={self.name!r}, enabled={self.enabled!r})"


def _job_base_from_resource(resource: dict[str, Any]) -> _JobBase:
    a = resource["attributes"]
    return _JobBase(
        id=resource["id"],
        name=a["name"],
        description=a.get("description"),
        enabled=a.get("enabled", True),
        type=a.get("type", "http"),
        schedule=a["schedule"],
        configuration=HttpConfig.from_dict(a["configuration"]),
        concurrency_policy=a.get("concurrency_policy", "ALLOW"),
        next_run_at=_parse_dt(a.get("next_run_at")),
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


class Run:
    """A single execution of a job (read-only)."""

    def __init__(self, attributes: dict[str, Any], id: str) -> None:
        self.id = id
        self.job: str = attributes["job"]
        self.job_version: Optional[int] = attributes.get("job_version")
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

    @classmethod
    def _from_resource(cls, resource: dict[str, Any]) -> "Run":
        return cls(resource["attributes"], id=resource["id"])

    def __repr__(self) -> str:
        return f"Run(id={self.id!r}, job={self.job!r}, status={self.status!r})"


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


def _new_kwargs(id, *, name, schedule, configuration, description, enabled, concurrency_policy):
    return {
        "id": id,
        "name": name,
        "schedule": schedule,
        "configuration": configuration,
        "description": description,
        "enabled": enabled,
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


def _list_jobs_kwargs(enabled, page_number, page_size) -> dict[str, Any]:
    kwargs: dict[str, Any] = {}
    if enabled is not None:
        kwargs["filterenabled"] = enabled
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

    def __init__(self, auth: _JobsAuthClient) -> None:
        self._auth = auth

    def list(
        self, *, job: Optional[str] = None, page_size: Optional[int] = None, after: Optional[str] = None
    ) -> list[Run]:
        """List past runs, most recent first.

        Args:
            job: Return only runs of the job with this id. ``None`` lists runs
                across all jobs in the account.
            page_size: Maximum number of runs to return in this page. ``None``
                uses the server default.
            after: Opaque cursor from a previous page; returns the runs that
                follow it. ``None`` starts from the first page.

        Returns:
            The runs in this page, as a list of :class:`Run`.
        """
        resp = _gen_list_runs.sync_detailed(client=self._auth, **_run_list_kwargs(job, page_size, after))
        _check(resp)
        return [Run._from_resource(r) for r in _data(resp)]

    def get(self, run_id: str | UUID) -> Run:
        """Fetch a single run by its id.

        Args:
            run_id: Identifier of the run to fetch.

        Returns:
            The matching :class:`Run`.
        """
        resp = _gen_get_run.sync_detailed(UUID(str(run_id)), client=self._auth)
        _check(resp)
        return Run._from_resource(_data(resp))

    def cancel(self, run_id: str | UUID) -> Run:
        """Cancel a run that has not finished yet.

        Args:
            run_id: Identifier of the run to cancel.

        Returns:
            The updated :class:`Run` reflecting the cancellation.
        """
        resp = _gen_cancel_run.sync_detailed(UUID(str(run_id)), client=self._auth)
        _check(resp)
        return Run._from_resource(_data(resp))

    def rerun(self, run_id: str | UUID) -> Run:
        """Start a new run that repeats a previous one.

        Args:
            run_id: Identifier of the run to repeat.

        Returns:
            The new :class:`Run`, with ``rerun_of`` set to ``run_id``.
        """
        resp = _gen_rerun_run.sync_detailed(UUID(str(run_id)), client=self._auth)
        _check(resp)
        return Run._from_resource(_data(resp))


class AsyncRunsClient:
    """Read a job's run history and act on individual runs (``jobs.runs``), awaited.

    Reached as ``client.jobs.runs`` on an async client. Use this to list past
    runs, fetch one by id, cancel a run that is still pending, or re-run a
    finished one. To trigger a fresh ad-hoc run of a job, use
    :meth:`AsyncJobsClient.run` instead.
    """

    def __init__(self, auth: _JobsAuthClient) -> None:
        self._auth = auth

    async def list(
        self, *, job: Optional[str] = None, page_size: Optional[int] = None, after: Optional[str] = None
    ) -> list[Run]:
        """List past runs, most recent first.

        Args:
            job: Return only runs of the job with this id. ``None`` lists runs
                across all jobs in the account.
            page_size: Maximum number of runs to return in this page. ``None``
                uses the server default.
            after: Opaque cursor from a previous page; returns the runs that
                follow it. ``None`` starts from the first page.

        Returns:
            The runs in this page, as a list of :class:`Run`.
        """
        resp = await _gen_list_runs.asyncio_detailed(client=self._auth, **_run_list_kwargs(job, page_size, after))
        _check(resp)
        return [Run._from_resource(r) for r in _data(resp)]

    async def get(self, run_id: str | UUID) -> Run:
        """Fetch a single run by its id.

        Args:
            run_id: Identifier of the run to fetch.

        Returns:
            The matching :class:`Run`.
        """
        resp = await _gen_get_run.asyncio_detailed(UUID(str(run_id)), client=self._auth)
        _check(resp)
        return Run._from_resource(_data(resp))

    async def cancel(self, run_id: str | UUID) -> Run:
        """Cancel a run that has not finished yet.

        Args:
            run_id: Identifier of the run to cancel.

        Returns:
            The updated :class:`Run` reflecting the cancellation.
        """
        resp = await _gen_cancel_run.asyncio_detailed(UUID(str(run_id)), client=self._auth)
        _check(resp)
        return Run._from_resource(_data(resp))

    async def rerun(self, run_id: str | UUID) -> Run:
        """Start a new run that repeats a previous one.

        Args:
            run_id: Identifier of the run to repeat.

        Returns:
            The new :class:`Run`, with ``rerun_of`` set to ``run_id``.
        """
        resp = await _gen_rerun_run.asyncio_detailed(UUID(str(run_id)), client=self._auth)
        _check(resp)
        return Run._from_resource(_data(resp))


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
        self.runs = RunsClient(self._auth)

    def new(
        self,
        id: str,
        *,
        name: str,
        schedule: str,
        configuration: HttpConfig,
        description: Optional[str] = None,
        enabled: bool = True,
        concurrency_policy: str = "ALLOW",
    ) -> Job:
        """Return an unsaved :class:`Job`. Call ``.save()`` to create it.

        Args:
            id: Caller-supplied unique identifier for the job. Unique within
                the account and immutable; the service returns 409 if another
                live job already uses this id.
            name: Human-readable name for the job.
            schedule: When the job runs. One of: a 5-field cron expression
                evaluated in UTC (recurring), an ISO-8601 datetime (a one-off
                run at that instant), or the literal ``"now"`` (run once, as
                soon as possible). A datetime or ``"now"`` job disables itself
                after it fires.
            configuration: The HTTP request the job sends each time it fires.
            description: Free-text description for the job. Defaults to none.
            enabled: Whether the job schedules runs. Set to ``False`` to pause
                it without deleting. Defaults to ``True``.
            concurrency_policy: How overlapping runs are handled. ``"ALLOW"``
                (the default and only value today) permits a new run to start
                while a previous one is still in flight.

        Returns:
            An unsaved :class:`Job` bound to this client.
        """
        return Job(
            self,
            **_new_kwargs(
                id,
                name=name,
                schedule=schedule,
                configuration=configuration,
                description=description,
                enabled=enabled,
                concurrency_policy=concurrency_policy,
            ),
        )

    def list(
        self, *, enabled: Optional[bool] = None, page_number: Optional[int] = None, page_size: Optional[int] = None
    ) -> list[Job]:
        """List jobs in the account.

        Args:
            enabled: Return only jobs with this enabled state. ``None`` lists
                both enabled and paused jobs.
            page_number: 1-based page to return. ``None`` returns the first
                page.
            page_size: Maximum number of jobs to return in this page. ``None``
                uses the server default.

        Returns:
            The jobs in this page, as a list of :class:`Job`.
        """
        resp = _gen_list_jobs.sync_detailed(client=self._auth, **_list_jobs_kwargs(enabled, page_number, page_size))
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

    def run(self, id: str) -> Run:
        """Trigger one immediate, manual run of a job, ignoring its schedule.

        This starts an ad-hoc run right now in addition to any scheduled runs;
        it does not alter the job's schedule. To read or act on existing runs,
        use ``jobs.runs``.

        Args:
            id: Identifier of the job to run.

        Returns:
            The :class:`Run` that was started, with ``trigger`` set to
            ``"MANUAL"``.
        """
        resp = _gen_run_job_now.sync_detailed(id, client=self._auth)
        _check(resp)
        return Run._from_resource(_data(resp))

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
        resp = _gen_create_job.sync_detailed(client=self._auth, body=_job_body(job, request_cls=JobCreateRequest))
        _check(resp)
        return Job._from_resource(_data(resp), self)

    def _update(self, job: Job) -> Job:
        resp = _gen_update_job.sync_detailed(job.id, client=self._auth, body=_job_body(job, request_cls=JobRequest))
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
        self.runs = AsyncRunsClient(self._auth)

    def new(
        self,
        id: str,
        *,
        name: str,
        schedule: str,
        configuration: HttpConfig,
        description: Optional[str] = None,
        enabled: bool = True,
        concurrency_policy: str = "ALLOW",
    ) -> AsyncJob:
        """Return an unsaved :class:`AsyncJob`. ``await .save()`` to create it.

        Args:
            id: Caller-supplied unique identifier for the job. Unique within
                the account and immutable; the service returns 409 if another
                live job already uses this id.
            name: Human-readable name for the job.
            schedule: When the job runs. One of: a 5-field cron expression
                evaluated in UTC (recurring), an ISO-8601 datetime (a one-off
                run at that instant), or the literal ``"now"`` (run once, as
                soon as possible). A datetime or ``"now"`` job disables itself
                after it fires.
            configuration: The HTTP request the job sends each time it fires.
            description: Free-text description for the job. Defaults to none.
            enabled: Whether the job schedules runs. Set to ``False`` to pause
                it without deleting. Defaults to ``True``.
            concurrency_policy: How overlapping runs are handled. ``"ALLOW"``
                (the default and only value today) permits a new run to start
                while a previous one is still in flight.

        Returns:
            An unsaved :class:`AsyncJob` bound to this client.
        """
        return AsyncJob(
            self,
            **_new_kwargs(
                id,
                name=name,
                schedule=schedule,
                configuration=configuration,
                description=description,
                enabled=enabled,
                concurrency_policy=concurrency_policy,
            ),
        )

    async def list(
        self, *, enabled: Optional[bool] = None, page_number: Optional[int] = None, page_size: Optional[int] = None
    ) -> list[AsyncJob]:
        """List jobs in the account.

        Args:
            enabled: Return only jobs with this enabled state. ``None`` lists
                both enabled and paused jobs.
            page_number: 1-based page to return. ``None`` returns the first
                page.
            page_size: Maximum number of jobs to return in this page. ``None``
                uses the server default.

        Returns:
            The jobs in this page, as a list of :class:`AsyncJob`.
        """
        resp = await _gen_list_jobs.asyncio_detailed(
            client=self._auth, **_list_jobs_kwargs(enabled, page_number, page_size)
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

    async def run(self, id: str) -> Run:
        """Trigger one immediate, manual run of a job, ignoring its schedule.

        This starts an ad-hoc run right now in addition to any scheduled runs;
        it does not alter the job's schedule. To read or act on existing runs,
        use ``jobs.runs``.

        Args:
            id: Identifier of the job to run.

        Returns:
            The :class:`Run` that was started, with ``trigger`` set to
            ``"MANUAL"``.
        """
        resp = await _gen_run_job_now.asyncio_detailed(id, client=self._auth)
        _check(resp)
        return Run._from_resource(_data(resp))

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
            client=self._auth, body=_job_body(job, request_cls=JobCreateRequest)
        )
        _check(resp)
        return AsyncJob._from_resource(_data(resp), self)

    async def _update(self, job: AsyncJob) -> AsyncJob:
        resp = await _gen_update_job.asyncio_detailed(
            job.id, client=self._auth, body=_job_body(job, request_cls=JobRequest)
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
