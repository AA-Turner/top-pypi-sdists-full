"""Smpl Jobs surface for the management client (``mgmt.jobs.*``).

Unlike Config/Flags/Logging, Jobs has no live "phone-home" agent — no
environment registration, no WebSocket — so its entire surface lives on the
management client rather than the runtime client. Defining a job, triggering a
run, and reading run history are all plain request/response calls here.

A :class:`Job` is an active record: build it with :meth:`JobsClient.new`, set
fields, and call ``save()`` (create when new, full-replace update when it
already exists) or ``delete()``. Runs are read-only views; run actions live on
``mgmt.jobs.runs``.

Every call delegates HTTP to the auto-generated ``smplkit._generated.jobs``
client; this wrapper only shapes models and raises SDK exceptions.
"""

from __future__ import annotations

import datetime
import json
import re
from typing import Any, Optional
from uuid import UUID

from smplkit._errors import _raise_for_status
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

__all__ = ["HttpConfig", "Job", "AsyncJob", "Run", "Usage", "JobsClient", "AsyncJobsClient"]

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
        """Soft-delete this job."""
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


class _RunsClient:
    """Run history and run actions (``mgmt.jobs.runs``)."""

    def __init__(self, auth: _JobsAuthClient) -> None:
        self._auth = auth

    def list(
        self, *, job: Optional[str] = None, page_size: Optional[int] = None, after: Optional[str] = None
    ) -> list[Run]:
        resp = _gen_list_runs.sync_detailed(client=self._auth, **_run_list_kwargs(job, page_size, after))
        _check(resp)
        return [Run._from_resource(r) for r in _data(resp)]

    def get(self, run_id: str | UUID) -> Run:
        resp = _gen_get_run.sync_detailed(UUID(str(run_id)), client=self._auth)
        _check(resp)
        return Run._from_resource(_data(resp))

    def cancel(self, run_id: str | UUID) -> Run:
        resp = _gen_cancel_run.sync_detailed(UUID(str(run_id)), client=self._auth)
        _check(resp)
        return Run._from_resource(_data(resp))

    def rerun(self, run_id: str | UUID) -> Run:
        resp = _gen_rerun_run.sync_detailed(UUID(str(run_id)), client=self._auth)
        _check(resp)
        return Run._from_resource(_data(resp))


class _AsyncRunsClient:
    def __init__(self, auth: _JobsAuthClient) -> None:
        self._auth = auth

    async def list(
        self, *, job: Optional[str] = None, page_size: Optional[int] = None, after: Optional[str] = None
    ) -> list[Run]:
        resp = await _gen_list_runs.asyncio_detailed(client=self._auth, **_run_list_kwargs(job, page_size, after))
        _check(resp)
        return [Run._from_resource(r) for r in _data(resp)]

    async def get(self, run_id: str | UUID) -> Run:
        resp = await _gen_get_run.asyncio_detailed(UUID(str(run_id)), client=self._auth)
        _check(resp)
        return Run._from_resource(_data(resp))

    async def cancel(self, run_id: str | UUID) -> Run:
        resp = await _gen_cancel_run.asyncio_detailed(UUID(str(run_id)), client=self._auth)
        _check(resp)
        return Run._from_resource(_data(resp))

    async def rerun(self, run_id: str | UUID) -> Run:
        resp = await _gen_rerun_run.asyncio_detailed(UUID(str(run_id)), client=self._auth)
        _check(resp)
        return Run._from_resource(_data(resp))


class JobsClient:
    """Synchronous Smpl Jobs surface (``mgmt.jobs``)."""

    def __init__(self, *, auth_client: _JobsAuthClient) -> None:
        self._auth = auth_client
        self.runs = _RunsClient(auth_client)

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
        resp = _gen_list_jobs.sync_detailed(client=self._auth, **_list_jobs_kwargs(enabled, page_number, page_size))
        _check(resp)
        return [Job._from_resource(r, self) for r in _data(resp)]

    def get(self, id: str) -> Job:
        resp = _gen_get_job.sync_detailed(id, client=self._auth)
        _check(resp)
        return Job._from_resource(_data(resp), self)

    def delete(self, id: str) -> None:
        resp = _gen_delete_job.sync_detailed(id, client=self._auth)
        _check(resp)

    def run(self, id: str) -> Run:
        """Trigger one immediate ``MANUAL`` run of the job."""
        resp = _gen_run_job_now.sync_detailed(id, client=self._auth)
        _check(resp)
        return Run._from_resource(_data(resp))

    def usage(self) -> Usage:
        """Current-period usage counters for the account."""
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


class AsyncJobsClient:
    """Asynchronous Smpl Jobs surface (``mgmt.jobs``)."""

    def __init__(self, *, auth_client: _JobsAuthClient) -> None:
        self._auth = auth_client
        self.runs = _AsyncRunsClient(auth_client)

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
        resp = await _gen_list_jobs.asyncio_detailed(
            client=self._auth, **_list_jobs_kwargs(enabled, page_number, page_size)
        )
        _check(resp)
        return [AsyncJob._from_resource(r, self) for r in _data(resp)]

    async def get(self, id: str) -> AsyncJob:
        resp = await _gen_get_job.asyncio_detailed(id, client=self._auth)
        _check(resp)
        return AsyncJob._from_resource(_data(resp), self)

    async def delete(self, id: str) -> None:
        resp = await _gen_delete_job.asyncio_detailed(id, client=self._auth)
        _check(resp)

    async def run(self, id: str) -> Run:
        resp = await _gen_run_job_now.asyncio_detailed(id, client=self._auth)
        _check(resp)
        return Run._from_resource(_data(resp))

    async def usage(self) -> Usage:
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
