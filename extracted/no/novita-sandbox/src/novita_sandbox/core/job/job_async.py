"""Asynchronous migration job API (platform contract 0.2.0).

Mirrors :class:`~novita_sandbox.core.job.job_sync.Job`; see that class for the
semantics of each method.
"""

from __future__ import annotations

import asyncio
import httpx
from typing import Any, Callable, Dict, List, Optional, Sequence

from novita_sandbox.core.api.client_async import get_api_client
from novita_sandbox.core.exceptions import (
    InvalidArgumentException,
    NotFoundException,
    SandboxException,
    TimeoutException,
)

from .errors import raise_for_job_error, raise_for_terminal_status
from .job_sync import (
    AliasArg,
    _build_resources,
    _connection_config,
    _normalize_ids,
    _require,
)
from .types import (
    RESOURCE_TYPE_SANDBOX,
    RESOURCE_TYPE_TEMPLATE,
    TERMINAL_JOB_STATUSES,
    JobPage,
    JobStatus,
    JobType,
    MigrationStatus,
    job_page_from_json,
    migration_status_from_json,
    status_wire_value,
)

DEFAULT_WAIT_TIMEOUT_SECONDS = 1800.0
DEFAULT_WAIT_POLL_INTERVAL_SECONDS = 10.0


class AsyncJob:
    """Async cross-cluster migration and template distribution."""

    _base = "/v1/migrations"

    # ------------------------------------------------------------------ #
    # accept
    # ------------------------------------------------------------------ #

    @classmethod
    async def migrate_sandbox(
        cls,
        sandbox_id: str,
        *,
        source_region: str,
        template_alias: Optional[str] = None,
        **opts: Any,
    ) -> str:
        """Move a sandbox to the cluster behind the configured domain.

        See :meth:`Job.migrate_sandbox` for the semantics.
        """
        return await cls._create(
            resource_ids=[_require(sandbox_id, "sandbox_id")],
            resource_type=RESOURCE_TYPE_SANDBOX,
            source_region=source_region,
            template_alias=template_alias,
            opts=opts,
            feature="Job.migrateSandbox",
        )

    @classmethod
    async def migrate_sandboxes(
        cls,
        sandbox_ids: Sequence[str],
        *,
        source_region: str,
        template_alias: Optional[AliasArg] = None,
        **opts: Any,
    ) -> str:
        """Move several sandboxes in one job. See :meth:`Job.migrate_sandboxes`."""
        return await cls._create(
            resource_ids=_normalize_ids(sandbox_ids),
            resource_type=RESOURCE_TYPE_SANDBOX,
            source_region=source_region,
            template_alias=template_alias,
            opts=opts,
            feature="Job.migrateSandboxes",
        )

    @classmethod
    async def distribute_template(
        cls,
        template_id: str,
        *,
        source_region: str,
        template_alias: str,
        **opts: Any,
    ) -> str:
        """Copy a template to the target cluster. See :meth:`Job.distribute_template`."""
        return await cls._create(
            resource_ids=[_require(template_id, "template_id")],
            resource_type=RESOURCE_TYPE_TEMPLATE,
            source_region=source_region,
            template_alias=template_alias,
            opts=opts,
            feature="Job.distributeTemplate",
        )

    @classmethod
    async def distribute_templates(
        cls,
        template_ids: Sequence[str],
        *,
        source_region: str,
        template_alias: AliasArg,
        **opts: Any,
    ) -> str:
        """Copy several templates in one job. See :meth:`Job.distribute_templates`."""
        return await cls._create(
            resource_ids=_normalize_ids(template_ids),
            resource_type=RESOURCE_TYPE_TEMPLATE,
            source_region=source_region,
            template_alias=template_alias,
            opts=opts,
            feature="Job.distributeTemplates",
        )

    @classmethod
    async def _create(
        cls,
        *,
        resource_ids: List[str],
        resource_type: str,
        source_region: str,
        template_alias: Optional[AliasArg],
        opts: Dict[str, Any],
        feature: str,
    ) -> str:
        source_region = _require(source_region, "source_region")
        resources = _build_resources(template_alias, resource_ids, resource_type)

        payload: Dict[str, Any] = {
            "resources": resources,
            "resource_type": resource_type,
            "source_region": source_region,
        }

        client = get_api_client(_connection_config(opts, feature))
        res = await client.get_async_httpx_client().post(cls._base, json=payload)
        if res.status_code >= 300:
            raise_for_job_error(res)
        # Contract 0.2.0: the accept response carries jobId only. A 2xx
        # without a usable id is a platform-side contract violation.
        job_id = res.json().get("jobId")
        if not isinstance(job_id, str) or not job_id:
            raise SandboxException(
                "migration accept response is missing jobId"
            )
        return job_id

    # ------------------------------------------------------------------ #
    # query
    # ------------------------------------------------------------------ #

    @classmethod
    async def get(cls, job_id: str, **opts: Any) -> MigrationStatus:
        """Fetch one job's status by id. See :meth:`Job.get`."""
        _require(job_id, "job_id")
        return (await cls._query({"job_id": job_id}, opts, "Job.get")).items[0]

    @classmethod
    async def list(
        cls,
        *,
        resource_id: Optional[str] = None,
        job_type: Optional[JobType] = None,
        status: Optional[JobStatus] = None,
        source_region: Optional[str] = None,
        target_region: Optional[str] = None,
        limit: Optional[int] = None,
        cursor: Optional[str] = None,
        **opts: Any,
    ) -> JobPage:
        """List migration jobs, newest first. See :meth:`Job.list`."""
        params: Dict[str, Any] = {}
        if resource_id is not None:
            params["resource_id"] = resource_id
        if job_type is not None:
            params["type"] = (
                job_type.value if isinstance(job_type, JobType) else job_type
            )
        if status is not None:
            params["status"] = status.value if isinstance(status, JobStatus) else status
        if source_region is not None:
            params["source_region"] = source_region
        if target_region is not None:
            params["target_region"] = target_region
        if limit is not None:
            params["limit"] = limit
        # An empty cursor means "unset" under the platform's EmitUnpopulated
        # setting (it is how "no next page" is spelled), so it is omitted
        # rather than sent as `cursor=`.
        if cursor:
            params["cursor"] = cursor
        return await cls._query(params, opts, "Job.list")

    @classmethod
    async def _query(
        cls, params: Dict[str, Any], opts: Dict[str, Any], feature: str
    ) -> JobPage:
        client = get_api_client(_connection_config(opts, feature))
        res = await client.get_async_httpx_client().get(cls._base, params=params)
        if res.status_code >= 300:
            raise_for_job_error(res)
        page = job_page_from_json(res.json())
        if "job_id" in params and not page.items:
            raise NotFoundException(
                f"RESOURCE_NOT_FOUND - no such job {params['job_id']}"
            )
        return page

    # ------------------------------------------------------------------ #
    # cancel
    # ------------------------------------------------------------------ #

    @classmethod
    async def cancel(cls, job_id: str, **opts: Any) -> MigrationStatus:
        """Cancel a running job and roll back what it already moved. See
        :meth:`Job.cancel`."""
        _require(job_id, "job_id")
        client = get_api_client(_connection_config(opts, "Job.cancel"))
        res = await client.get_async_httpx_client().post(
            f"{cls._base}/cancel", json={"job_id": job_id}
        )
        if res.status_code >= 300:
            raise_for_job_error(res)
        return migration_status_from_json(res.json())

    # ------------------------------------------------------------------ #
    # wait
    # ------------------------------------------------------------------ #

    @classmethod
    async def wait(
        cls,
        job_id: str,
        *,
        timeout: float = DEFAULT_WAIT_TIMEOUT_SECONDS,
        poll_interval: float = DEFAULT_WAIT_POLL_INTERVAL_SECONDS,
        on_progress: Optional[Callable[[MigrationStatus], None]] = None,
        **opts: Any,
    ) -> MigrationStatus:
        """Poll until terminal. See :meth:`Job.wait`."""
        _require(job_id, "job_id")
        if timeout < 0:
            raise InvalidArgumentException("timeout must not be negative")
        if poll_interval <= 0:
            raise InvalidArgumentException("poll_interval must be greater than 0")

        config = _connection_config(opts, "AsyncJob.wait")
        loop = asyncio.get_running_loop()
        deadline = loop.time() + timeout
        last = None

        def timeout_error():
            message = f"Timed out after {timeout}s waiting for migration job {job_id}"
            if last is not None:
                message += (
                    f"; last status was {status_wire_value(last.status)} "
                    f"(completed={last.completed}, failed={last.failed}, "
                    f"cancelled={last.cancelled}, total={last.total})"
                )
            return TimeoutException(message)

        while True:
            remaining = deadline - loop.time()
            if remaining <= 0:
                raise timeout_error()
            request_timeout = (
                min(remaining, config.request_timeout)
                if config.request_timeout is not None
                else remaining
            )
            try:
                last = await asyncio.wait_for(
                    cls.get(job_id, **{**opts, "request_timeout": request_timeout}),
                    timeout=remaining,
                )
            except (asyncio.TimeoutError, httpx.TimeoutException) as error:
                if isinstance(error, asyncio.TimeoutError) or loop.time() >= deadline:
                    raise timeout_error() from error
                raise
            if loop.time() >= deadline:
                raise timeout_error()
            if on_progress is not None:
                on_progress(last)
            if loop.time() >= deadline:
                raise timeout_error()
            if last.status in TERMINAL_JOB_STATUSES:
                return raise_for_terminal_status(last)
            await asyncio.sleep(min(poll_interval, max(deadline - loop.time(), 0.0)))
