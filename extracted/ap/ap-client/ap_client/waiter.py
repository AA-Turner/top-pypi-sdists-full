"""Polling helpers for waiting on jobs/groups."""

from __future__ import annotations

import time
from datetime import datetime
from typing import Callable

from .api import APIClient, APIError

_TRANSIENT_STATUS_CODES = {408, 429, 500, 502, 503, 504}
TERMINAL_JOB_STATUSES = frozenset({"Succeeded", "Failed", "Cancelled", "Unknown"})


class WaitTimeoutError(TimeoutError):
    """Raised when waiting for a job or group exceeds the configured timeout."""

    def __init__(self, resource_type: str, resource_id: str, timeout: float):
        self.resource_type = resource_type
        self.resource_id = resource_id
        self.timeout = timeout
        super().__init__(
            f"timed out waiting for {resource_type} {resource_id} after {_format_seconds(timeout)}"
        )


def wait_for_job(
    client: APIClient,
    job_id: str,
    interval: float = 5.0,
    timeout: float | None = None,
    printer: Callable[[str], None] = print,
) -> dict:
    """Poll until a job reaches a terminal status."""
    deadline = _deadline(timeout)
    first_poll = True
    while True:
        _raise_if_timed_out(deadline, first_poll, "job", job_id, timeout)
        first_poll = False
        try:
            job = client.get_job(
                job_id,
                timeout=_request_timeout(deadline, "job", job_id, timeout),
            )
        except APIError as exc:
            if _is_transient_api_error(exc):
                _print_transient_error("job", job_id, exc, printer)
                _sleep_until_next_poll(interval, deadline, "job", job_id, timeout)
                continue
            raise
        _print_job_status(job, printer)
        if job.get("status") in TERMINAL_JOB_STATUSES and not job.get("retry_pending", False):
            return job
        _sleep_until_next_poll(interval, deadline, "job", job_id, timeout)


def wait_for_group(
    client: APIClient,
    group_id: str,
    interval: float = 5.0,
    timeout: float | None = None,
    printer: Callable[[str], None] = print,
) -> dict:
    """Poll until all jobs in a group are finished."""
    deadline = _deadline(timeout)
    first_poll = True
    while True:
        _raise_if_timed_out(deadline, first_poll, "group", group_id, timeout)
        first_poll = False
        try:
            group = client.get_group_stats(
                group_id,
                timeout=_request_timeout(deadline, "group", group_id, timeout),
            )
        except APIError as exc:
            if _is_transient_api_error(exc):
                _print_transient_error("group", group_id, exc, printer)
                _sleep_until_next_poll(interval, deadline, "group", group_id, timeout)
                continue
            raise
        _print_group_status(group, printer)
        stats = group.get("stats") or {}
        total = int(stats.get("total", 0) or 0)
        finished = int(stats.get("finished", 0) or 0)
        if total == 0 or finished >= total:
            return group
        _sleep_until_next_poll(interval, deadline, "group", group_id, timeout)


def wait_for_group_post_process(
    client: APIClient,
    group_id: str,
    interval: float = 5.0,
    timeout: float | None = None,
    printer: Callable[[str], None] = print,
) -> dict:
    """Poll until regular group jobs finish, then wait for its PostProcess job."""
    deadline = _deadline(timeout)
    group = wait_for_group(
        client,
        group_id,
        interval=interval,
        timeout=timeout,
        printer=printer,
    )

    group = client.get_group(
        group_id,
        timeout=_request_timeout(deadline, "group post-process", group_id, timeout),
    )
    if group.get("group_post_process") is None:
        printer(f"[{_now_str()}] group={group_id} post_process=not_configured")
        return {"group": group, "post_process_job": None}

    first_poll = True
    while True:
        _raise_if_timed_out(deadline, first_poll, "group post-process", group_id, timeout)
        first_poll = False
        job_id = group.get("group_post_process_job_id")
        printer(f"[{_now_str()}] group={group_id} post_process_job_id={job_id or '<pending>'}")
        if job_id:
            post_process_job = wait_for_job(
                client,
                job_id,
                interval=interval,
                timeout=_remaining_timeout(deadline, "job", job_id, timeout),
                printer=printer,
            )
            return {"group": group, "post_process_job": post_process_job}
        _sleep_until_next_poll(interval, deadline, "group post-process", group_id, timeout)
        group = client.get_group(
            group_id,
            timeout=_request_timeout(deadline, "group post-process", group_id, timeout),
        )


def _deadline(timeout: float | None) -> float | None:
    if timeout is None:
        return None
    return time.monotonic() + timeout


def _raise_if_timed_out(
    deadline: float | None,
    first_poll: bool,
    resource_type: str,
    resource_id: str,
    timeout: float | None,
) -> None:
    if deadline is None or first_poll:
        return
    if time.monotonic() >= deadline:
        raise WaitTimeoutError(resource_type, resource_id, timeout or 0.0)


def _request_timeout(
    deadline: float | None,
    resource_type: str,
    resource_id: str,
    timeout: float | None,
) -> float | None:
    if deadline is None:
        return None
    remaining = deadline - time.monotonic()
    if remaining <= 0:
        raise WaitTimeoutError(resource_type, resource_id, timeout or 0.0)
    return remaining


def _remaining_timeout(
    deadline: float | None,
    resource_type: str,
    resource_id: str,
    timeout: float | None,
) -> float | None:
    if deadline is None:
        return None
    return _request_timeout(deadline, resource_type, resource_id, timeout)


def _sleep_until_next_poll(
    interval: float,
    deadline: float | None,
    resource_type: str,
    resource_id: str,
    timeout: float | None,
) -> None:
    if deadline is None:
        time.sleep(interval)
        return
    remaining = deadline - time.monotonic()
    if remaining <= 0:
        raise WaitTimeoutError(resource_type, resource_id, timeout or 0.0)
    time.sleep(min(interval, remaining))


def _is_transient_api_error(exc: APIError) -> bool:
    return exc.status_code is None or exc.status_code in _TRANSIENT_STATUS_CODES


def _print_transient_error(
    resource_type: str,
    resource_id: str,
    exc: APIError,
    printer: Callable[[str], None],
) -> None:
    refreshed_at = _now_str()
    printer(f"[{refreshed_at}] {resource_type}={resource_id} transient_error={exc}")


def _print_job_status(job: dict, printer: Callable[[str], None]) -> None:
    refreshed_at = _now_str()
    status = job.get("status", "Unknown")
    failed_reason = job.get("failed_reason") or ""
    extra = f" failed_reason={failed_reason}" if failed_reason else ""
    printer(f"[{refreshed_at}] job={job.get('job_id')} status={status}{extra}")


def _print_group_status(group: dict, printer: Callable[[str], None]) -> None:
    refreshed_at = _now_str()
    stats = group.get("stats") or {}
    printer(
        f"[{refreshed_at}] group={group.get('group_id')} "
        f"total={stats.get('total', 0)} queued={stats.get('queued', 0)} "
        f"pending={stats.get('pending', 0)} running={stats.get('running', 0)} "
        f"finished={stats.get('finished', 0)} succeeded={stats.get('succeeded', 0)} "
        f"failed={stats.get('failed', 0)} cancelled={stats.get('cancelled', 0)} "
        f"unknown={stats.get('unknown', 0)}"
    )


def _now_str() -> str:
    return datetime.now().astimezone().strftime("%Y-%m-%d %H:%M:%S")


def _format_seconds(value: float) -> str:
    if value == int(value):
        return f"{int(value)}s"
    return f"{value:g}s"
