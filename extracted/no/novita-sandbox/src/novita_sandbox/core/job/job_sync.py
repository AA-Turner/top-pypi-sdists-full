"""Synchronous migration job API (platform contract 0.2.0).

Three endpoints, one job id as the key:

* ``POST /v1/migrations`` — accept a migration. The request carries a
  ``resources`` list (one job may cover N items); the response carries **only
  ``jobId``**. Status is a separate query, not bundled into the accept response.
* ``GET /v1/migrations`` — single lookup by ``job_id``, or a filtered,
  cursor-paginated list. There is no ``/v1/migrations/{id}`` route.
* ``POST /v1/migrations/cancel`` — cancel and roll back: the runner undoes what
  it has already moved instead of only marking items for cancellation, so the
  job sits in ``reverting`` while it does.

The target cluster is never a parameter: it is resolved from the request host,
so the connection config's ``domain`` decides where resources are migrated to.
"""

from __future__ import annotations

import time
import httpx
from typing import Any, Callable, Dict, List, Optional, Sequence, Union

from novita_sandbox.core.api.client_sync import get_api_client
from novita_sandbox.core.compat import raise_if_legacy
from novita_sandbox.core.connection_config import ConnectionConfig
from novita_sandbox.core.exceptions import (
    InvalidArgumentException,
    NotFoundException,
    SandboxException,
    TimeoutException,
)

from .errors import raise_for_job_error, raise_for_terminal_status
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

#: A per-resource ``template_alias``: one fixed alias, or a function of the id.
#: Sandbox migrations also accept None to omit the alias.
AliasArg = Union[str, Callable[[str], str]]


def _connection_config(opts: Dict[str, Any], feature: str) -> ConnectionConfig:
    """Build the connection config from ``**opts`` like every other resource API.

    The migration endpoints only exist on modern domains, so a legacy-domain
    call is rejected before any request, mirroring the JS SDK's
    ``raiseIfLegacy``.
    """
    raise_if_legacy(opts, feature)
    return ConnectionConfig(**opts)


def _require(value: Any, name: str) -> str:
    if not value or not isinstance(value, str):
        raise InvalidArgumentException(f"{name} is required")
    return value


def _normalize_ids(resource_ids: Sequence[str]) -> List[str]:
    """Deduplicate ids, keeping first-occurrence order.

    A job is keyed by resource set rather than by occurrence, and a repeated id
    in one request has no defined meaning in the contract, so repeats collapse.
    """
    if resource_ids is None:
        raise InvalidArgumentException("resource ids are required")
    # A bare string (or any non-sequence) must not be iterated character by
    # character; the JS SDK rejects non-arrays the same way.
    if isinstance(resource_ids, (str, bytes)) or not isinstance(
        resource_ids, (list, tuple)
    ):
        raise InvalidArgumentException(
            "resource ids must be a list or tuple of strings"
        )

    seen = set()
    unique: List[str] = []
    for resource_id in resource_ids:
        if not isinstance(resource_id, str) or not resource_id:
            raise InvalidArgumentException("resource ids must be non-empty strings")
        if resource_id not in seen:
            seen.add(resource_id)
            unique.append(resource_id)
    if not unique:
        # Contract: resources is required with minItems 1. Reject locally so a
        # malformed call costs nothing instead of round-tripping a 400.
        raise InvalidArgumentException("at least one resource id is required")
    return unique


def _resolve_aliases(
    template_alias: Optional[AliasArg], resource_ids: Sequence[str]
) -> List[str]:
    """Resolve the required per-resource ``template_alias`` values.

    Every alias is resolved before any request: a throwing or blank-producing
    callable then aborts the call instead of leaving a half-validated batch on
    the platform. Values are passed through verbatim because the platform does
    not trim either — only whitespace-only strings are rejected, and they are
    rejected locally because the platform would answer them with a 400 anyway.
    """

    def _require_non_blank(value: Any, resource_id: str) -> str:
        if not isinstance(value, str):
            raise InvalidArgumentException(
                "template_alias resolver must return a string"
            )
        if value.strip() == "":
            raise InvalidArgumentException(
                "template_alias is required and must not be blank "
                f"(resource {resource_id!r})"
            )
        return value

    if isinstance(template_alias, str):
        fixed = _require_non_blank(template_alias, resource_ids[0])
        return [fixed] * len(resource_ids)
    if callable(template_alias):
        return [
            _require_non_blank(template_alias(resource_id), resource_id)
            for resource_id in resource_ids
        ]
    raise InvalidArgumentException(
        "template_alias is required: pass a string, or a callable mapping a "
        "resource id to its alias"
    )


def _check_single_string_alias(
    template_alias: Optional[AliasArg], resource_ids: Sequence[str], resource_type: str
) -> None:
    """Reject one fixed alias for several *templates*; allow it for sandboxes.

    N distinct templates claiming the same target alias can only collide, and
    that is knowable locally. N sandboxes sharing one base template is the
    normal case — one fixed alias is then the correct usage — so it is allowed.
    A blank string is skipped here so that the more specific "required and must
    not be blank" error from :func:`_resolve_aliases` is the one the caller sees.
    """
    if (
        resource_type == RESOURCE_TYPE_TEMPLATE
        and isinstance(template_alias, str)
        and template_alias.strip() != ""
        and len(resource_ids) > 1
    ):
        raise InvalidArgumentException(
            f"template_alias as a single string cannot be used for a batch of "
            f"{len(resource_ids)} templates: every one would claim the same "
            "alias on the target cluster. Pass a per-template function instead."
        )


def _build_resources(
    template_alias: Optional[AliasArg], resource_ids: Sequence[str], resource_type: str
) -> List[Dict[str, str]]:
    """Omit unset aliases for sandboxes; validate supplied/distribution aliases."""
    if resource_type == RESOURCE_TYPE_SANDBOX and template_alias is None:
        return [{"id": resource_id} for resource_id in resource_ids]

    _check_single_string_alias(template_alias, resource_ids, resource_type)
    aliases = _resolve_aliases(template_alias, resource_ids)
    return [
        {"id": resource_id, "template_alias": alias}
        for resource_id, alias in zip(resource_ids, aliases)
    ]


class Job:
    """Synchronous cross-cluster migration and template distribution."""

    _base = "/v1/migrations"

    # ------------------------------------------------------------------ #
    # accept
    # ------------------------------------------------------------------ #

    @classmethod
    def migrate_sandbox(
        cls,
        sandbox_id: str,
        *,
        source_region: str,
        template_alias: Optional[str] = None,
        **opts: Any,
    ) -> str:
        """Move a sandbox to the cluster behind the configured domain.

        ``sandbox_id`` may be the short id or the composite
        ``<sandboxId>-<clientId>`` that the rest of the SDK uses; migration-api
        stores the short id.

        The sandbox's base template travels with it. It is reported as an item
        (``resource_type == "base"``) but is not counted in the job's
        ``total``.

        :param template_alias: the target-cluster alias the sandbox's base
            template should land under. Optional: omitted or None leaves the
            field out of the request. Supplied aliases must not be blank and
            are passed through verbatim.
        :returns: the job id. The accept response carries nothing else; call
            :meth:`get` or :meth:`wait` for status.
        """
        return cls._create(
            resource_ids=[_require(sandbox_id, "sandbox_id")],
            resource_type=RESOURCE_TYPE_SANDBOX,
            source_region=source_region,
            template_alias=template_alias,
            opts=opts,
            feature="Job.migrateSandbox",
        )

    @classmethod
    def migrate_sandboxes(
        cls,
        sandbox_ids: Sequence[str],
        *,
        source_region: str,
        template_alias: Optional[AliasArg] = None,
        **opts: Any,
    ) -> str:
        """Move several sandboxes in **one** job (the platform takes N items).

        One accept request, one job id, and one status projection covering all
        items. Per-item outcomes are only visible through the single-job
        ``status.items``; call :meth:`migrate_sandbox` once per sandbox if you
        would rather get one job per sandbox.

        :param template_alias: target alias for the sandboxes' base template,
            optional. Omitted or None leaves the field out of every resource.
            A single string is fine when they share a base template; a callable
            ``sandbox_id -> alias`` distinguishes them. Supplied aliases and
            callable results must not be blank.
        """
        return cls._create(
            resource_ids=_normalize_ids(sandbox_ids),
            resource_type=RESOURCE_TYPE_SANDBOX,
            source_region=source_region,
            template_alias=template_alias,
            opts=opts,
            feature="Job.migrateSandboxes",
        )

    @classmethod
    def distribute_template(
        cls,
        template_id: str,
        *,
        source_region: str,
        template_alias: str,
        **opts: Any,
    ) -> str:
        """Copy a template to the cluster behind the configured domain.

        Distribution is not destructive: the source template stays usable.

        :param template_alias: the target-cluster alias the copy should land
            under. Required — the platform generates no default.
        """
        return cls._create(
            resource_ids=[_require(template_id, "template_id")],
            resource_type=RESOURCE_TYPE_TEMPLATE,
            source_region=source_region,
            template_alias=template_alias,
            opts=opts,
            feature="Job.distributeTemplate",
        )

    @classmethod
    def distribute_templates(
        cls,
        template_ids: Sequence[str],
        *,
        source_region: str,
        template_alias: AliasArg,
        **opts: Any,
    ) -> str:
        """Copy several templates in one job.

        :param template_alias: a per-template function ``template_id -> alias``
            (or one string, which is only meaningful for a single template).
            One fixed string is rejected for several templates: they would all
            claim the same target alias.
        """
        return cls._create(
            resource_ids=_normalize_ids(template_ids),
            resource_type=RESOURCE_TYPE_TEMPLATE,
            source_region=source_region,
            template_alias=template_alias,
            opts=opts,
            feature="Job.distributeTemplates",
        )

    @classmethod
    def _create(
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

        # Request bodies go through protojson, which accepts snake_case here.
        payload: Dict[str, Any] = {
            "resources": resources,
            "resource_type": resource_type,
            "source_region": source_region,
        }

        client = get_api_client(_connection_config(opts, feature))
        res = client.get_httpx_client().post(cls._base, json=payload)
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
    def get(cls, job_id: str, **opts: Any) -> MigrationStatus:
        """Fetch one job's status by id.

        The platform serves single lookups from the list endpoint using the
        ``job_id`` query parameter; there is no ``/v1/migrations/{id}`` route.

        Unlike list responses, a single lookup carries the per-item breakdown in
        :attr:`MigrationStatus.items`.

        A job that does not exist, or that is not visible from this region's
        team, is reported as a 400 with ``reason=RESOURCE_NOT_FOUND`` and
        raised as :class:`NotFoundException`.
        """
        _require(job_id, "job_id")
        return cls._query({"job_id": job_id}, opts, "Job.get").items[0]

    @classmethod
    def list(
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
        """List migration jobs, newest first.

        ``resource_id`` matches jobs *containing* that id as an item; the
        returned counters still cover the job's every item. ``source_region``
        and ``target_region`` keep only jobs moving out of / into that region.

        List responses describe each job by its counters alone, so
        :attr:`MigrationStatus.items` is empty on every page; call :meth:`get`
        for a job's per-item breakdown.

        ``limit`` is validated by the platform: an out-of-range value is a 400
        with ``reason=VALIDATOR_PARAM``, raised as
        :class:`InvalidArgumentException`.
        """
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
        return cls._query(params, opts, "Job.list")

    @classmethod
    def _query(
        cls, params: Dict[str, Any], opts: Dict[str, Any], feature: str
    ) -> JobPage:
        client = get_api_client(_connection_config(opts, feature))

        # GET queries use the form codec, i.e. the pb.go json tags: snake_case.
        res = client.get_httpx_client().get(cls._base, params=params)
        if res.status_code >= 300:
            raise_for_job_error(res)
        page = job_page_from_json(res.json())
        if "job_id" in params and not page.items:
            # Defensive: the contract promises at most one item for a job_id
            # lookup, and an existing visible job always yields one.
            raise NotFoundException(
                f"RESOURCE_NOT_FOUND - no such job {params['job_id']}"
            )
        return page

    # ------------------------------------------------------------------ #
    # cancel
    # ------------------------------------------------------------------ #

    @classmethod
    def cancel(cls, job_id: str, **opts: Any) -> MigrationStatus:
        """Cancel a running job and roll back what it already moved.

        Cancel is idempotent: the runner undoes the already-migrated items
        instead of only marking them for cancellation, so the returned
        ``reverting`` projection means the rollback has been accepted, not that
        it has finished. Poll until ``cancelled`` (or a terminal status) to know
        that the source side is whole again.

        The response carries the same per-item breakdown as :meth:`get`.

        "No such job", "every item already terminal" and "not your job" are
        deliberately indistinguishable on the wire (anti-probing) and all
        surface as :class:`NotFoundException`.

        :raises CancelTooLateError: the job is past the point where a rollback
            is still possible (409 ``MIGRATION_PAST_CANCEL_LINE``); it has to
            run to completion.
        :raises SharedDependencyError: an item cannot be rolled back because
            another resource depends on it (409 ``MIGRATION_SHARED_DEPENDENCY``).
        """
        _require(job_id, "job_id")
        client = get_api_client(_connection_config(opts, "Job.cancel"))
        res = client.get_httpx_client().post(
            f"{cls._base}/cancel", json={"job_id": job_id}
        )
        if res.status_code >= 300:
            raise_for_job_error(res)
        return migration_status_from_json(res.json())

    # ------------------------------------------------------------------ #
    # wait
    # ------------------------------------------------------------------ #

    @classmethod
    def wait(
        cls,
        job_id: str,
        *,
        timeout: float = DEFAULT_WAIT_TIMEOUT_SECONDS,
        poll_interval: float = DEFAULT_WAIT_POLL_INTERVAL_SECONDS,
        on_progress: Optional[Callable[[MigrationStatus], None]] = None,
        **opts: Any,
    ) -> MigrationStatus:
        """Poll until the job reaches a terminal status, and return it.

        ``completed`` is returned, ``failed`` raises
        :class:`JobFailedError` and ``cancelled`` raises
        :class:`JobCancelledError` — both carry the terminal projection on
        ``.status``, including the per-item breakdown. Note a ``completed`` job
        is returned as-is: the contract has no aggregation rule for mixed
        outcomes, so check ``status.failed == 0`` yourself if that matters.

        ``reverting`` is not terminal — a cancel rolls the job back — so it
        keeps polling.

        :param on_progress: called once per poll with the latest projection.
            Every poll goes through the single-job route, so ``items`` is
            populated on each one and can drive per-item progress reporting.
        :raises TimeoutException: when ``timeout`` elapses first; the message
            carries the last-seen status and counters.
        """
        _require(job_id, "job_id")
        if timeout < 0:
            raise InvalidArgumentException("timeout must not be negative")
        if poll_interval <= 0:
            raise InvalidArgumentException("poll_interval must be greater than 0")

        config = _connection_config(opts, "Job.wait")
        deadline = time.monotonic() + timeout
        last: Optional[MigrationStatus] = None

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
            remaining = deadline - time.monotonic()
            if remaining <= 0:
                raise timeout_error()
            request_timeout = (
                min(remaining, config.request_timeout)
                if config.request_timeout is not None
                else remaining
            )
            try:
                last = cls.get(job_id, **{**opts, "request_timeout": request_timeout})
            except httpx.TimeoutException as error:
                if time.monotonic() >= deadline:
                    raise timeout_error() from error
                raise
            if time.monotonic() >= deadline:
                raise timeout_error()
            if on_progress is not None:
                on_progress(last)
            if time.monotonic() >= deadline:
                raise timeout_error()
            if last.status in TERMINAL_JOB_STATUSES:
                return raise_for_terminal_status(last)
            time.sleep(min(poll_interval, max(deadline - time.monotonic(), 0.0)))
