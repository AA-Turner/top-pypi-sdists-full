"""Load paginated Agent Tasks inventory from the GitHub REST API."""

from __future__ import annotations

import json
import logging
import subprocess
from dataclasses import dataclass
from enum import StrEnum
from urllib.parse import quote

from agentic_devtools.ai_providers.agent_tasks_payload import (
    AGENT_TASKS_API_VERSION,
    AGENT_TASKS_ENDPOINT_TEMPLATE,
)
from agentic_devtools.cli.shared.retry import (
    ProviderRateLimitError,
    RetryableError,
    _provider_rate_limit_error_from_retryable,
)
from agentic_devtools.cli.subprocess_utils import run_safe

logger = logging.getLogger(__name__)

_AGENT_TASK_TIMEOUT_SECONDS = 10
_AGENT_TASK_PAGE_SIZE = 100
_AGENT_TASK_MAX_PAGES = 10
_KNOWN_TASK_STATES = frozenset(
    {
        "idle",
        "in_progress",
        "queued",
        "requested",
        "running",
        "waiting",
        "waiting_for_user",
        "canceled",
        "cancelled",
        "completed",
        "failed",
        "stopped",
        "timed_out",
    }
)


class AgentTaskInventoryAvailability(StrEnum):
    """Whether a bounded task inventory can establish absence."""

    COMPLETE = "complete"
    PARTIAL = "partial"
    UNAVAILABLE = "unavailable"


class AgentTaskInventoryFailureCategory(StrEnum):
    """Observed inventory failure facts, not endpoint capability judgments."""

    HTTP_NOT_FOUND = "http_not_found"
    AUTHENTICATION = "authentication"
    PERMISSION = "permission"
    MALFORMED_RESPONSE = "malformed_response"
    UNKNOWN_TASK_STATE = "unknown_task_state"
    RETRIEVAL_EXHAUSTED = "retrieval_exhausted"
    PROVIDER_UNAVAILABLE = "provider_unavailable"


FailureCategory = AgentTaskInventoryFailureCategory


def _normalize_inventory_availability(value: object, *, has_tasks: bool) -> AgentTaskInventoryAvailability | None:
    """Canonicalize availability while downgrading invalid explicit evidence."""
    if value is None:
        return None
    if isinstance(value, str):
        try:
            return AgentTaskInventoryAvailability(value)
        except ValueError:
            pass
    return AgentTaskInventoryAvailability.PARTIAL if has_tasks else AgentTaskInventoryAvailability.UNAVAILABLE


@dataclass(frozen=True)
class AgentTaskInventoryLoadResult[TaskT = object]:
    """Bounded raw retrieval evidence; lifecycle inventories specialize task typing.

    After normalization, ``complete`` is true iff ``availability`` is ``COMPLETE``.
    """

    tasks: tuple[TaskT, ...]
    complete: bool = True
    incomplete_reasons: tuple[str, ...] = ()
    availability: AgentTaskInventoryAvailability | None = None
    failure_category: FailureCategory | None = None
    http_status: int | None = None

    def __post_init__(self) -> None:
        """Normalize legacy completeness without promoting contradictory evidence."""
        availability = _normalize_inventory_availability(self.availability, has_tasks=bool(self.tasks))
        has_failure = bool(self.incomplete_reasons or self.failure_category)
        has_http_failure = self.http_status is not None and self.http_status >= 400
        can_be_complete = self.complete and not has_failure and not has_http_failure
        if availability is None or availability == AgentTaskInventoryAvailability.COMPLETE:
            availability = (
                AgentTaskInventoryAvailability.COMPLETE
                if can_be_complete
                else AgentTaskInventoryAvailability.PARTIAL
                if self.tasks
                else AgentTaskInventoryAvailability.UNAVAILABLE
            )
        elif availability == AgentTaskInventoryAvailability.PARTIAL and not self.tasks:
            availability = AgentTaskInventoryAvailability.UNAVAILABLE
        object.__setattr__(self, "availability", availability)
        object.__setattr__(self, "complete", availability == AgentTaskInventoryAvailability.COMPLETE)


def _classify_agent_task_page_response(
    response: subprocess.CompletedProcess[str],
    *,
    pr_number: int,
) -> list[object] | None:
    """Return task rows for a successful page response, or ``None`` if malformed."""
    if response.returncode != 0:
        logger.warning("PR #%d: Agent Tasks REST inventory exited with code %d", pr_number, response.returncode)
        return None

    payload = json.loads(response.stdout)
    absent = object()
    candidates = [getattr(response, name, absent) for name in ("http_status", "status_code", "status")]
    nested = getattr(response, "response", absent)
    if nested is not absent and nested is not None:
        candidates.append(getattr(nested, "status_code", absent))
    if isinstance(payload, dict) and "status" in payload:
        candidates.append(payload["status"])
    statuses = [
        int(value) if isinstance(value, str) and value.isascii() and value.isdigit() else value
        for value in candidates
        if value is not absent
    ]
    if any(not isinstance(value, int) or isinstance(value, bool) or not 200 <= value < 300 for value in statuses):
        logger.warning("PR #%d: Agent Tasks REST inventory returned an invalid status", pr_number)
        return None
    if isinstance(payload, dict) and any(key in payload for key in ("error", "errors", "message")):
        logger.warning("PR #%d: Agent Tasks REST inventory returned an error envelope", pr_number)
        return None
    page_tasks = payload if isinstance(payload, list) else payload.get("tasks") if isinstance(payload, dict) else None
    if not isinstance(page_tasks, list):
        logger.warning("PR #%d: Agent Tasks REST inventory returned malformed data", pr_number)
        return None
    return page_tasks


def _agent_task_http_status(response: object) -> int | None:
    """Read an explicit HTTP status from structured attributes or JSON only."""
    absent = object()
    candidates = [getattr(response, name, absent) for name in ("http_status", "status_code", "status")]
    nested = getattr(response, "response", absent)
    if nested is not absent and nested is not None:
        candidates.append(getattr(nested, "status_code", absent))
    try:
        payload = json.loads(getattr(response, "stdout", ""))
    except ValueError, TypeError:
        payload = None
    if isinstance(payload, dict) and "status" in payload:
        candidates.append(payload["status"])
    statuses = [
        int(value) if isinstance(value, str) and value.isascii() and value.isdigit() else value
        for value in candidates
        if value is not absent
    ]
    numeric = [
        value for value in statuses if isinstance(value, int) and not isinstance(value, bool) and 100 <= value <= 599
    ]
    failure = next((value for value in numeric if not 200 <= value < 300), None)
    return failure if failure is not None else numeric[0] if numeric else None


def _agent_task_failure_category(status: int | None) -> FailureCategory:
    """Classify an observed HTTP failure without inferring endpoint support."""
    return {
        404: FailureCategory.HTTP_NOT_FOUND,
        401: FailureCategory.AUTHENTICATION,
        403: FailureCategory.PERMISSION,
    }.get(status or 0, FailureCategory.PROVIDER_UNAVAILABLE)


def _agent_task_row_failure(row: object) -> FailureCategory | None:
    """Identify unusable rows while leaving supported raw task shapes untouched."""
    if not isinstance(row, dict):
        return FailureCategory.MALFORMED_RESPONSE
    state = row.get("state") or row.get("status")
    if isinstance(state, dict):
        state = state.get("state") or state.get("status")
    if not isinstance(state, str) or state.strip().casefold() not in _KNOWN_TASK_STATES:
        return FailureCategory.UNKNOWN_TASK_STATE
    return None


def _filter_agent_task_rows(rows: list[object]) -> AgentTaskInventoryLoadResult:
    """Preserve usable rows and record each rejected row's failure category."""
    tasks = []
    reasons = []
    failure_category = None
    for index, row in enumerate(rows):
        category = _agent_task_row_failure(row)
        if category is None:
            tasks.append(row)
        else:
            failure_category = failure_category or category
            reasons.append(f"row {index}: {category.value}")
    return AgentTaskInventoryLoadResult(tuple(tasks), not reasons, tuple(reasons), failure_category=failure_category)


def _failed_agent_task_page(
    category: FailureCategory, *, http_status: int | None = None
) -> AgentTaskInventoryLoadResult:
    """Build a failed-page result from observed failure facts."""
    return AgentTaskInventoryLoadResult(
        (), False, (category.value,), failure_category=category, http_status=http_status
    )


def normalize_agent_task_inventory(value: object) -> AgentTaskInventoryLoadResult:
    """Normalize typed results and legacy raw lists without treating failure as absence."""
    if isinstance(value, AgentTaskInventoryLoadResult):
        return value
    if isinstance(value, list):
        return _filter_agent_task_rows(value)
    category = FailureCategory.PROVIDER_UNAVAILABLE if value is None else FailureCategory.MALFORMED_RESPONSE
    return _failed_agent_task_page(category)


def extract_agent_task_inventory(payload: object) -> list[object] | AgentTaskInventoryLoadResult:
    """Keep HTTP failures typed and malformed envelopes explicit before returning legacy rows."""
    response = subprocess.CompletedProcess([], 0, stdout=json.dumps(payload))
    status = _agent_task_http_status(response)
    if status is not None and not 200 <= status < 300:
        return _failed_agent_task_page(_agent_task_failure_category(status), http_status=status)
    tasks = _classify_agent_task_page_response(response, pr_number=0)
    if tasks is None:
        if isinstance(payload, dict) and (
            any(key in payload for key in ("error", "errors", "message")) or "status" in payload
        ):
            error = ValueError("Agent Tasks API returned an invalid page envelope")
            if status is not None:
                setattr(error, "status_code", status)
            raise error
        raise ValueError("Agent Tasks API returned no task list")
    return tasks


def extract_paginated_agent_task_inventory(raw: str) -> list[object] | AgentTaskInventoryLoadResult:
    """Validate each task envelope before combining concatenated API documents."""
    decoder = json.JSONDecoder()
    remaining = raw.strip()
    tasks: list[object] = []
    reasons: list[str] = []
    category = None
    status = None
    page = 0
    while remaining:
        page += 1
        try:
            payload, end = decoder.raw_decode(remaining)
            if not isinstance(payload, dict):
                raise ValueError("Agent Tasks API returned an invalid page envelope")
            result = extract_agent_task_inventory(payload)
        except ValueError as exc:
            result = inventory_failure_result(exc)
            # A decoding error has no reliable boundary for the next document.
            if isinstance(exc, json.JSONDecodeError):
                remaining = ""
                end = 0
        if isinstance(result, AgentTaskInventoryLoadResult):
            tasks.extend(result.tasks)
            reasons.extend(f"page {page}: {reason}" for reason in result.incomplete_reasons)
            category = result.failure_category or category
            status = result.http_status or status
        else:
            tasks.extend(result)
        remaining = remaining[end:].lstrip()
    if not page:
        return _failed_agent_task_page(FailureCategory.MALFORMED_RESPONSE)
    if reasons:
        return AgentTaskInventoryLoadResult(
            tuple(tasks), False, tuple(reasons), failure_category=category, http_status=status
        )
    return tasks


def inventory_failure_result(exc: Exception) -> AgentTaskInventoryLoadResult:
    """Classify inventory exceptions from explicit HTTP facts and exception types only."""
    if isinstance(exc, ProviderRateLimitError) and exc.is_rate_limit:
        raise exc.with_traceback(exc.__traceback__)
    if isinstance(exc, RetryableError) and exc.is_rate_limit:
        raise _provider_rate_limit_error_from_retryable(exc) from exc
    status = _agent_task_http_status(exc)
    if status is not None and not 200 <= status < 300:
        category = _agent_task_failure_category(status)
    elif isinstance(exc, subprocess.TimeoutExpired):
        category = FailureCategory.RETRIEVAL_EXHAUSTED
    elif isinstance(exc, (ValueError, TypeError)):
        category = FailureCategory.MALFORMED_RESPONSE
    else:
        category = FailureCategory.PROVIDER_UNAVAILABLE
    return _failed_agent_task_page(category, http_status=status)


def _load_agent_task_page(
    endpoint: str, *, page: int, pr_number: int
) -> tuple[AgentTaskInventoryLoadResult, int | None]:
    """Read one page without retrying, preserving provider rate-limit exceptions."""
    from agentic_devtools.cli.ci.github_provider import _run_readonly_gh_command

    status = None
    try:
        response = _run_readonly_gh_command(
            [
                "api",
                f"{endpoint}?per_page={_AGENT_TASK_PAGE_SIZE}&page={page}",
                "--header",
                "Accept: application/vnd.github+json",
                "--header",
                f"X-GitHub-Api-Version: {AGENT_TASKS_API_VERSION}",
            ],
            timeout_seconds=_AGENT_TASK_TIMEOUT_SECONDS,
            runner=run_safe,
        )
        status = _agent_task_http_status(response)
        if response.returncode != 0 or (status is not None and not 200 <= status < 300):
            return _failed_agent_task_page(_agent_task_failure_category(status), http_status=status), None
        rows = _classify_agent_task_page_response(response, pr_number=pr_number)
        if rows is None:
            return _failed_agent_task_page(FailureCategory.MALFORMED_RESPONSE, http_status=status), None
        return _filter_agent_task_rows(rows), len(rows)
    except ProviderRateLimitError as exc:
        if exc.is_rate_limit:
            raise
        return inventory_failure_result(exc), None
    except (subprocess.TimeoutExpired, OSError, ValueError, TypeError, RuntimeError, RetryableError) as exc:
        return inventory_failure_result(exc), None


def load_agent_task_inventory(repo: str, *, pr_number: int) -> AgentTaskInventoryLoadResult:
    """Load bounded Agent Tasks pages, retaining usable rows and failure evidence."""
    owner, repository = repo.split("/", 1)
    endpoint = AGENT_TASKS_ENDPOINT_TEMPLATE.format(
        owner=quote(owner, safe=""),
        repo=quote(repository, safe=""),
    ).lstrip("/")

    inventory: list[object] = []
    reasons: list[str] = []
    category = None
    status = None
    for page in range(1, _AGENT_TASK_MAX_PAGES + 1):
        result, row_count = _load_agent_task_page(endpoint, page=page, pr_number=pr_number)
        inventory.extend(result.tasks)
        reasons.extend(f"page {page}: {reason}" for reason in result.incomplete_reasons)
        category = result.failure_category or category
        status = result.http_status or status
        if row_count is None or row_count < _AGENT_TASK_PAGE_SIZE:
            break
    else:
        category = FailureCategory.RETRIEVAL_EXHAUSTED
        reasons.append("page limit reached")
        logger.warning("PR #%d: Agent Tasks REST inventory reached the page limit", pr_number)
    return AgentTaskInventoryLoadResult(
        tuple(inventory), not reasons, tuple(reasons), failure_category=category, http_status=status
    )
