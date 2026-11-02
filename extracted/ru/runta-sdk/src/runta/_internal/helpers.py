"""Shared SDK helpers used by the sync and async public modules."""

from __future__ import annotations

import shlex
from collections.abc import Sequence
from urllib.parse import urlparse

import runta as _public


def command_parts(
    command: str | Sequence[str], *, cwd: str | None
) -> tuple[str, list[str]]:
    if isinstance(command, str):
        body = command if cwd is None else f"cd {shlex.quote(cwd)} && {command}"
        return "sh", ["-lc", body]
    parts = [str(item) for item in command]
    if not parts:
        raise ValueError("command must not be empty")
    if cwd is None:
        return parts[0], parts[1:]
    quoted = " ".join(shlex.quote(item) for item in parts)
    return "sh", ["-lc", f"cd {shlex.quote(cwd)} && exec {quoted}"]


def status_query(status: str | Sequence[str] | None) -> str | None:
    if status is None:
        return None
    if isinstance(status, str):
        return _canonical_status(status)
    return ",".join(_canonical_status(item) for item in status)


def status_filter(
    status: str | Sequence[str] | None,
) -> set[_public.RuntimeStatus] | None:
    query = status_query(status)
    if query is None:
        return None
    return {_public.RuntimeStatus.from_user(item) for item in query.split(",")}


def host_from_url(value: str) -> str:
    parsed = urlparse(value if "://" in value else f"https://{value}")
    host = parsed.hostname or value
    return host.strip().rstrip(".").lower()


def ingress_json(item):
    if isinstance(item, _public.IngressSpec):
        return item.to_json()
    return dict(item)


def is_transient_exec_route_miss(exc: _public.ApiError, runtime_id: str) -> bool:
    if exc.status_code != 404:
        return False
    code = (exc.code or "").lower()
    if code and code not in {"not_found", "notfound"}:
        return False
    message = str(exc)
    return (
        f"runtime '{runtime_id}' not found" in message
        or f"runtime {runtime_id} not found" in message
    )


def _canonical_status(status: str) -> str:
    return _public.RuntimeStatus.from_user(status).value


# Internal aliases for existing focused helper tests.
_command_parts = command_parts
_host_from_url = host_from_url
_ingress_json = ingress_json
_is_transient_exec_route_miss = is_transient_exec_route_miss
_status_filter = status_filter
_status_query = status_query


__all__ = [
    "command_parts",
    "host_from_url",
    "ingress_json",
    "is_transient_exec_route_miss",
    "status_filter",
    "status_query",
]
