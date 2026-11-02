"""The canonical tool-call event — single source of truth for both sinks.

One wide, denormalized record per tool call. `build_event` assembles it from the
request identity, the tool name/args, and the outcome. It reads `request.state`
defensively (via getattr) so tests can pass a lightweight stand-in.
"""

from __future__ import annotations

import json
import uuid
from dataclasses import asdict, dataclass, field
from datetime import datetime, timezone
from typing import Any

from cube_cloud.config import settings
from cube_cloud.telemetry import classify, redaction

try:  # package version, best-effort
    from importlib.metadata import version as _pkg_version

    _CLOUD_VERSION = _pkg_version("cube-cloud")
except Exception:  # pragma: no cover - metadata missing in some envs
    _CLOUD_VERSION = "unknown"

# tool name -> coarse domain bucket for rollups. Names not listed fall back to
# "other"; keep in sync with the dispatch domains in main.py.
_TOOL_DOMAINS: dict[str, str] = {
    # environment / entity
    "list_environments": "environment",
    "install_entity": "entity",
    "uninstall_entity": "entity",
    "update_entity_config": "entity",
    "enforce_entity_config": "entity",
    "entity_health": "entity",
    "plan_details": "entity",
    "cancel_active_plan": "entity",
    # module
    "list_modules": "module",
    "install_module": "module",
    "uninstall_module": "module",
    "update_module_variables": "module",
    # secret
    "create_secret": "secret",
    "update_secret": "secret",
    # product / release
    "list_products": "product",
    "compare_product_versions": "product",
    "get_product_releases": "product",
    "list_release_channels": "product",
    # acr / publish
    "acr_get_token": "acr",
    "apollo_publish_manifest": "acr",
    # remote image builds (kaniko)
    "build_image_prepare": "build",
    "build_image_start": "build",
    "build_image_status": "build",
    # teleport
    "expose": "teleport",
    "unexpose": "teleport",
    "list_exposed": "teleport",
    "list_services": "teleport",
    "cube_status": "teleport",
    "cube_list": "teleport",
    "kubectl_exec": "teleport",
    "app_list": "teleport",
    # groundcover
    "groundcover_list_clusters": "groundcover",
    "groundcover_list_workloads": "groundcover",
    "groundcover_query_metrics": "groundcover",
    "groundcover_list_metrics": "groundcover",
    "groundcover_search_logs": "groundcover",
    "groundcover_search_traces": "groundcover",
    "groundcover_k8s_events": "groundcover",
    # feedback
    "send_feedback": "feedback",
    # Kept alongside it: `submit_feedback` was renamed to `send_feedback` when the
    # tool gained the Freshservice route, and the archive holds rows under the old
    # name. Dropping the mapping would reclassify that history as "other" the moment
    # anything reprocessed it.
    "submit_feedback": "feedback",
}

# arg keys that name the cube/environment, checked in order of preference.
_CUBE_ARG_KEYS = ("cube", "environment", "cluster")

# `source` distinguishes the surface that produced the row. The MCP tool wrapper
# emits `cloud`; the console seam (console_events.py) emits `console`. Reusing
# this column rather than adding one means a console row needs no change to the
# dataclass, the compaction Lambda, the Glue table, or the dashboard's export —
# `local` stays reserved for the uninstrumented local-agent tools (spec follow-up 4).
SOURCE_CLOUD = "cloud"
SOURCE_CONSOLE = "console"
# Every console event shares one domain bucket, matching how the dashboard rolls
# tool_domain up; the per-route detail is in `tool` (`console.view_cube`, ...).
CONSOLE_DOMAIN = "console"


def _tool_domain(name: str) -> str:
    return _TOOL_DOMAINS.get(name, "other")


def _response_dropped_tools() -> set[str]:
    """Tools whose response body is withheld (args are still captured)."""
    return {t.strip() for t in (settings.telemetry_drop_response_tools or "").split(",") if t.strip()}


def _extract_cube(args: dict[str, Any]) -> str | None:
    if not isinstance(args, dict):
        return None
    for key in _CUBE_ARG_KEYS:
        value = args.get(key)
        if isinstance(value, str) and value:
            return value
    return None


@dataclass
class ToolCallEvent:
    """One tool call. Field names are the analytics schema (Parquet columns /
    span attributes)."""

    call_id: str
    ts: str  # ISO-8601 UTC
    ts_epoch_ms: int
    dt: str  # YYYY-MM-DD partition
    env: str
    source: str
    cloud_version: str

    tool: str
    tool_domain: str
    profile: str | None
    key_id: str | None
    user_domain: str | None  # email domain of the key's owner, when known
    user_email_hash: str | None  # SHA-256 of the owner's email, when known
    caller_ip: str | None
    cube: str | None

    status: str
    error_class: str | None
    latency_ms: float

    args: dict[str, Any]  # redacted, full
    response: str  # redacted; the archive layer may clip the stored copy
    error_message: str | None  # redacted
    response_size_bytes: int  # true full size in bytes, regardless of clipping
    response_truncated: bool = False  # whether the stored `response` was clipped
    response_dropped: bool = False  # response body withheld (args still kept)

    actor_type: str | None = None  # 'user' (a person), 'bot' (service/agent key) or 'test' (plus-addressed home-domain login; not a person)
    bot_name: str | None = None  # service label for bot keys; None for users and test accounts

    trace_id: str | None = None  # populated once OTLP span export lands

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)

    def to_json(self) -> str:
        return json.dumps(self.to_dict(), default=str, separators=(",", ":"))


def build_event(
    req: Any,
    name: str,
    arguments: dict[str, Any],
    result: str,
    latency_ms: float,
    exception: BaseException | None = None,
) -> ToolCallEvent:
    """Assemble a `ToolCallEvent` from the request + outcome. Pure and defensive
    — never raises on missing state; unknown fields default to None/empty."""
    now = datetime.now(timezone.utc)
    args = arguments if isinstance(arguments, dict) else {}

    status, error_class = classify.classify(result, exception)
    cube = _extract_cube(args)

    full_response = result or ""
    # True size is always recorded, even when the stored body is dropped.
    response_size_bytes = len(full_response.encode("utf-8"))

    # Args are always captured (secret-bearing arg *keys* are still masked by
    # redact_args). For response-dropped tools we withhold only the response
    # body + error text, which can carry data our key-based redaction can't see
    # (kubectl_exec output such as env dumps; acr_get_token's response is itself
    # a credential). The command/args ARE kept for those tools — useful for
    # spotting which raw calls to promote into first-class tools.
    secret_values = redaction.collect_secret_values(args)
    redacted_args = redaction.redact_args(args)

    response_dropped = name in _response_dropped_tools()
    if response_dropped:
        response_text = ""
        error_message: str | None = None
    else:
        response_text = redaction.scrub_secrets(full_response, secret_values) or ""
        if exception is not None:
            error_message = f"{type(exception).__name__}: {exception}"
        elif status == classify.STATUS_ERROR:
            error_message = result
        else:
            error_message = None
        error_message = redaction.scrub_secrets(error_message, secret_values)

    state = getattr(req, "state", None)

    return ToolCallEvent(
        call_id=str(uuid.uuid4()),
        ts=now.isoformat(),
        ts_epoch_ms=int(now.timestamp() * 1000),
        dt=now.strftime("%Y-%m-%d"),
        env=settings.env_name,
        source=SOURCE_CLOUD,
        cloud_version=_CLOUD_VERSION,
        tool=name,
        tool_domain=_tool_domain(name),
        profile=getattr(state, "profile", None),
        key_id=getattr(state, "key_id", None),
        user_domain=getattr(state, "user_domain", None),
        user_email_hash=getattr(state, "user_email_hash", None),
        caller_ip=_caller_ip(req),
        cube=cube,
        status=status,
        error_class=error_class,
        latency_ms=round(float(latency_ms), 3),
        args=redacted_args,
        response=response_text,
        error_message=error_message,
        response_size_bytes=response_size_bytes,
        response_dropped=response_dropped,
        actor_type=getattr(state, "actor_type", None),
        bot_name=getattr(state, "bot_name", None),
    )


def build_console_event(
    req: Any,
    event_name: str,
    args: dict[str, Any],
    cube: str | None,
    status: str,
    error_class: str | None,
    latency_ms: float,
    response_size_bytes: int = 0,
) -> ToolCallEvent:
    """Assemble a `ToolCallEvent` for one console request.

    Same record, same identity fields, same redaction as `build_event` — the row
    differs only in `source`/`tool`/`tool_domain` and in never carrying a body.
    A console read's response is the caller's own view of the fleet (a cube list
    is every cube they may see); it has no analytics value and the archive is
    long-lived, so `response` is always empty and `response_dropped` is always
    True. Only the size is kept. Status is decided by the caller from the HTTP
    outcome rather than by `classify`, which reads tool result *strings*.
    """
    now = datetime.now(timezone.utc)
    safe_args = args if isinstance(args, dict) else {}
    state = getattr(req, "state", None)

    return ToolCallEvent(
        call_id=str(uuid.uuid4()),
        ts=now.isoformat(),
        ts_epoch_ms=int(now.timestamp() * 1000),
        dt=now.strftime("%Y-%m-%d"),
        env=settings.env_name,
        source=SOURCE_CONSOLE,
        cloud_version=_CLOUD_VERSION,
        tool=event_name,
        tool_domain=CONSOLE_DOMAIN,
        profile=getattr(state, "profile", None),
        key_id=getattr(state, "key_id", None),
        user_domain=getattr(state, "user_domain", None),
        user_email_hash=getattr(state, "user_email_hash", None),
        caller_ip=_caller_ip(req),
        cube=cube or None,
        status=status,
        error_class=error_class,
        latency_ms=round(float(latency_ms), 3),
        args=redaction.redact_args(safe_args),
        response="",
        error_message=None,
        response_size_bytes=int(response_size_bytes or 0),
        response_dropped=True,
        actor_type=getattr(state, "actor_type", None),
        bot_name=getattr(state, "bot_name", None),
    )


def _caller_ip(req: Any) -> str | None:
    # Prefer X-Forwarded-For (behind the ALB); fall back to the socket peer.
    try:
        headers = getattr(req, "headers", {}) or {}
        xff = headers.get("x-forwarded-for") if hasattr(headers, "get") else None
        if xff:
            return xff.split(",")[0].strip()
        client = getattr(req, "client", None)
        if client is not None:
            return getattr(client, "host", None)
    except Exception:
        return None
    return None
