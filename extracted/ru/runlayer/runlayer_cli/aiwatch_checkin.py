"""Best-effort AI Watch check-ins for the aiwatch bundle."""

from __future__ import annotations

import sys
import time
from collections.abc import Callable, Mapping

import httpx
import structlog

from runlayer_cli import __version__
from runlayer_cli.api import RunlayerClient
from runlayer_cli.hook_install import ClientStatus, InstallScope, check_all
from runlayer_cli.mdm_config import (
    AIWatchMode,
    daemon_gate_open,
    read_managed_config,
    resolve_include_pipeline,
    resolve_mode,
)
from runlayer_cli.scan.device import (
    DeviceContext,
    InstalledTool,
    get_device_metadata,
    get_or_create_device_id,
)
from runlayer_cli.scan.service import ScanResult, device_context_dict
from runlayer_cli.scan.windows_users import is_running_as_system
from runlayer_cli.skills.device_sync import SyncReport

logger = structlog.get_logger(__name__)

# Per-item / per-list caps for the skill-sync detail payload so a pathological
# manifest (many skills, long skip reasons) can't bloat the check-in body.
_SYNC_DETAIL_MAX_ITEMS = 50
_SYNC_DETAIL_MAX_ITEM_LEN = 200
_CHECKIN_RETRY_DELAYS_SECONDS = (0.1, 0.2)
_CHECKIN_REJECTED_RESPONSE_BODY_MAX_LEN = 500

_PRIVILEGED_USERNAMES = frozenset(
    {
        "system",
        "local service",
        "network service",
        "root",
        "_mbsetupuser",
        "loginwindow",
    }
)


def _resolve_checkin_username(metadata: Mapping[str, object]) -> str | None:
    """Resolve a real console user for privileged desktop check-ins."""
    username = metadata.get("username")
    normalized_username = username.casefold() if isinstance(username, str) else None
    desktop_os = metadata.get("os") in {"windows", "darwin"}
    if not desktop_os or (
        normalized_username is not None
        and normalized_username not in _PRIVILEGED_USERNAMES
    ):
        return username if isinstance(username, str) else None

    try:
        from runlayer_cli.hook_install.console_user import (  # noqa: PLC0415
            find_console_user_home,
        )

        console_home = find_console_user_home()
    except Exception:
        console_home = None
    return console_home.name if console_home is not None else None


def _make_device_context() -> DeviceContext:
    """Build a device context from local machine metadata.

    For call paths without a scan result (e.g. enroll) so every check-in caller
    supplies a concrete ``DeviceContext``.
    """
    metadata = get_device_metadata()
    return {
        "device_id": get_or_create_device_id(),
        "hostname": metadata.get("hostname"),
        "os": metadata.get("os"),
        "os_version": metadata.get("os_version"),
        "username": _resolve_checkin_username(metadata),
        "org_device_id": None,
        "serial_number": metadata.get("serial_number"),
    }


def _base_payload(
    ctx: DeviceContext,
    *,
    feature: str,
    status: str,
    tools: list[InstalledTool],
    agent_version: str | None = None,
    error_message: str | None = None,
) -> dict[str, object]:
    payload: dict[str, object] = {
        **ctx,
        "feature": feature,
        "status": status,
        "tools": tools,
    }
    if agent_version:
        payload["agent_version"] = agent_version
    if error_message:
        payload["error_message"] = error_message[:500]
    return payload


def _submit_payload(
    client: RunlayerClient,
    payload: dict[str, object],
    *,
    log_event: str,
) -> None:
    """Submit a check-in best-effort, retrying bounded transport failures."""
    for attempt in range(len(_CHECKIN_RETRY_DELAYS_SECONDS) + 1):
        try:
            client.submit_aiwatch_checkin(payload)
            return
        except ValueError as exc:
            logger.warning(log_event, error=str(exc))
            return
        except httpx.HTTPStatusError as exc:
            logger.warning(
                "aiwatch_checkin_rejected",
                status_code=exc.response.status_code,
                feature=payload.get("feature"),
                response_body=exc.response.text[
                    :_CHECKIN_REJECTED_RESPONSE_BODY_MAX_LEN
                ],
            )
            return
        except (httpx.TransportError, OSError) as exc:
            if attempt == len(_CHECKIN_RETRY_DELAYS_SECONDS):
                logger.warning(log_event, error=str(exc))
                return
            time.sleep(_CHECKIN_RETRY_DELAYS_SECONDS[attempt])
        except httpx.HTTPError as exc:
            logger.warning(log_event, error=str(exc))
            return


def _submit_simple_checkin(
    client: RunlayerClient,
    *,
    feature: str,
    status: str,
    ctx: DeviceContext,
    tools: list[InstalledTool],
    log_event: str,
    error_message: str | None = None,
) -> None:
    """Submit one feature check-in with an explicit ``status`` (no hook validation).

    Shared submit for the statuses the client asserts directly — ``disabled``
    (feature gated off by MDM config) and ``error`` (e.g. a detect scan
    failure) — plus the computed hook-validation result. Swallows expected
    network errors like the other check-ins.
    """
    payload = _base_payload(
        ctx,
        feature=feature,
        status=status,
        tools=tools,
        agent_version=__version__,
        error_message=error_message,
    )
    _submit_payload(client, payload, log_event=log_event)


def submit_detect_checkin(client: RunlayerClient, result: ScanResult) -> None:
    """Record that a scan ran, even when no findings were submitted."""
    payload = _base_payload(
        device_context_dict(result),
        feature="detect",
        status="ok",
        tools=result.tools,
        agent_version=result.collector_version,
    )
    _submit_payload(client, payload, log_event="aiwatch_detect_checkin_failed")


def _submit_hook_validation_checkin(
    client: RunlayerClient,
    *,
    feature: str,
    include_pipeline: bool,
    ctx: DeviceContext,
    tools: list[InstalledTool],
    log_event: str,
) -> None:
    """Run hook-config validation and report feature health for the device."""
    results = check_all(
        scope=InstallScope.MDM,
        include_pipeline=include_pipeline,
    )
    problems = [
        result
        for result in results
        if result.status not in {ClientStatus.OK, ClientStatus.CLIENT_NOT_INSTALLED}
    ]
    # Every remaining problem means the installed hook configuration is absent
    # or no longer matches the desired state, so report drift.
    status = "drifted" if problems else "ok"
    error_message = "; ".join(
        f"{problem.client.value}: {problem.status.value}"
        + (f" ({problem.detail})" if problem.detail else "")
        for problem in problems
    )

    _submit_simple_checkin(
        client,
        feature=feature,
        status=status,
        ctx=ctx,
        tools=tools,
        log_event=log_event,
        error_message=error_message or None,
    )


def submit_detect_error_checkin(
    client: RunlayerClient,
    *,
    ctx: DeviceContext,
    error_message: str,
    tools: list[InstalledTool] | None = None,
) -> None:
    """Report a Detect scan failure so the device shows a Detect error, not silence.

    Detect otherwise only reports on success (``submit_detect_checkin``); this
    is the failure counterpart, fired best-effort from the scan-failure path.
    """
    _submit_simple_checkin(
        client,
        feature="detect",
        status="error",
        ctx=ctx,
        tools=tools or [],
        log_event="aiwatch_detect_error_checkin_failed",
        error_message=error_message,
    )


def submit_enforce_validation_checkin(
    client: RunlayerClient,
    *,
    ctx: DeviceContext,
    tools: list[InstalledTool],
) -> None:
    """Report the effective decision-capable hook mode without conflating it.

    Protect has its own liveness feature so the device table never claims full
    Enforce governance is active when only scanner Block/Mask is applied.
    """
    managed = read_managed_config()
    mode = resolve_mode(managed)
    if mode is AIWatchMode.MONITOR:
        # Clear both decision-capable feature rows. Without the Protect update,
        # a device moved Protect -> Monitor remains falsely active forever.
        for feature in ("protect", "enforce"):
            _submit_simple_checkin(
                client,
                feature=feature,
                status="disabled",
                ctx=ctx,
                tools=tools,
                log_event=f"aiwatch_{feature}_checkin_failed",
            )
        return

    feature = "enforce"
    log_event = "aiwatch_enforce_checkin_failed"
    if mode is AIWatchMode.PROTECT:
        # Clear any formerly-active Enforce state before reporting Protect.
        _submit_simple_checkin(
            client,
            feature="enforce",
            status="disabled",
            ctx=ctx,
            tools=tools,
            log_event="aiwatch_enforce_checkin_failed",
        )
        feature = "protect"
        log_event = "aiwatch_protect_checkin_failed"
    else:
        # Enforce and Protect are mutually exclusive endpoint modes. Clear a
        # formerly-active Protect row before reporting current Enforce health.
        _submit_simple_checkin(
            client,
            feature="protect",
            status="disabled",
            ctx=ctx,
            tools=tools,
            log_event="aiwatch_protect_checkin_failed",
        )

    _submit_hook_validation_checkin(
        client,
        feature=feature,
        include_pipeline=resolve_include_pipeline(False, managed),
        ctx=ctx,
        tools=tools,
        log_event=log_event,
    )


def submit_sessions_validation_checkin(
    client: RunlayerClient,
    *,
    ctx: DeviceContext,
    tools: list[InstalledTool],
) -> None:
    """Validate the session/transcript event-pipeline hooks and report Sessions health."""
    managed = read_managed_config()
    if not resolve_include_pipeline(False, managed):
        # Gated off by MDM config: report disabled (not silence) so the backend
        # can distinguish "intentionally off" from "never ran".
        _submit_simple_checkin(
            client,
            feature="sessions",
            status="disabled",
            ctx=ctx,
            tools=tools,
            log_event="aiwatch_sessions_checkin_failed",
        )
        return
    _submit_hook_validation_checkin(
        client,
        feature="sessions",
        include_pipeline=True,
        ctx=ctx,
        tools=tools,
        log_event="aiwatch_sessions_checkin_failed",
    )


def _cap_sync_items(items: list[str]) -> list[str]:
    return [item[:_SYNC_DETAIL_MAX_ITEM_LEN] for item in items[:_SYNC_DETAIL_MAX_ITEMS]]


def submit_skill_sync_checkin(
    client: RunlayerClient,
    *,
    ctx: DeviceContext,
    tools: list[InstalledTool],
    report: SyncReport,
) -> None:
    """Report the outcome of one skill-sync reconcile as a feature check-in.

    Status mapping: any reconcile error → ``error``; else any skipped item
    (user-owned dir squatting a managed name, name collision, …) → ``drifted``
    — the device diverges from the assigned manifest without it being a
    failure; else ``ok``.
    """
    if report.errors:
        status = "error"
        error_message = "; ".join(report.errors)
    elif report.skipped:
        status = "drifted"
        error_message = "; ".join(report.skipped)
    else:
        status = "ok"
        error_message = None

    payload = _base_payload(
        ctx,
        feature="skill_sync",
        status=status,
        tools=tools,
        agent_version=__version__,
        error_message=error_message,
    )
    payload["sync_detail"] = {
        "installed": _cap_sync_items(report.installed),
        "updated": _cap_sync_items(report.updated),
        "removed": _cap_sync_items(report.removed),
        # Local edits to managed skills re-fetched back to the published
        # content — normal enforcement, so it never affects the status.
        "restored": _cap_sync_items(report.restored),
        "skipped": _cap_sync_items(report.skipped),
        "errors": _cap_sync_items(report.errors),
        "up_to_date_count": len(report.up_to_date),
    }
    _submit_payload(client, payload, log_event="aiwatch_skill_sync_checkin_failed")


def submit_skill_sync_disabled_checkin(
    client: RunlayerClient,
    *,
    ctx: DeviceContext,
    tools: list[InstalledTool],
) -> None:
    """Report skill sync gated off by MDM config (``disabled``, not silence).

    Mirrors the sessions/enforce disabled reporting so the backend can tell
    "intentionally off" from "never ran".
    """
    _submit_simple_checkin(
        client,
        feature="skill_sync",
        status="disabled",
        ctx=ctx,
        tools=tools,
        log_event="aiwatch_skill_sync_checkin_failed",
    )


def _daemon_health_snapshot() -> dict[str, object]:
    """Collect desired vs observed hook-daemon state for the fleet check-in.

    Reuses the existing local signals (gate predicate, supervisor query, IPC
    health probe) rather than inventing a parallel status path. The derived
    ``state`` mirrors ``daemon_lifecycle.DaemonState`` plus the fleet-level
    ``gate_off`` / ``degraded`` distinctions:

    - ``gate_off``  — rollout gate closed (desired state: no daemon)
    - ``healthy``   — gate open, supervisor up, probe ok, version match
    - ``draining``  — daemon answering ``restarting`` (version-skew drain)
    - ``degraded``  — gate open but probe unavailable, supervisor down, or
      version skew: hooks are paying the fallback path
    """
    # Lazy imports: the daemon modules are macOS/Windows-shaped and only
    # needed on the scan tick for this one snapshot.
    from runlayer_cli.daemon.status import supervisor_is_running  # noqa: PLC0415
    from runlayer_cli.hook.daemon_client import probe_daemon  # noqa: PLC0415
    from runlayer_cli.hook.daemon_protocol import protocol_version  # noqa: PLC0415

    gate_open = daemon_gate_open(read_managed_config())
    response = probe_daemon()
    if response is None:
        probe = "unavailable"
        probe_version: str | None = None
    else:
        probe = dict(response).get("status", "unavailable")
        probe_version = dict(response).get("version")
    try:
        supervisor_running = supervisor_is_running()
    except OSError:
        supervisor_running = False

    version_match = probe == "ok" and probe_version == protocol_version()
    if not gate_open:
        state = "gate_off"
    elif probe == "restarting":
        state = "draining"
    elif version_match and supervisor_running:
        state = "healthy"
    else:
        state = "degraded"
    return {
        "state": state,
        "gate_open": gate_open,
        "supervisor_running": supervisor_running,
        "probe": probe,
        "probe_version": probe_version,
    }


def _daemon_degraded_message(detail: Mapping[str, object]) -> str:
    parts: list[str] = []
    probe = detail.get("probe")
    probe_version = detail.get("probe_version")
    if probe == "unavailable":
        parts.append("daemon unavailable")
    elif probe == "ok" and probe_version != __version__:
        parts.append(
            f"daemon version skew (running {probe_version}, expected {__version__})"
        )
    if not detail.get("supervisor_running"):
        parts.append("supervisor not running")
    return "; ".join(parts) or "daemon degraded"


def submit_daemon_checkin(
    client: RunlayerClient,
    *,
    ctx: DeviceContext,
    tools: list[InstalledTool],
) -> None:
    """Report hook-daemon fleet health, piggybacked on the scan tick.

    Status mapping keeps the coarse wire vocabulary (``disabled`` = gate off,
    ``ok`` = healthy or draining, ``error`` = degraded) while the full
    granularity rides in ``daemon_detail`` for fleet dashboards. No per-hook
    network request is ever added — this only fires with the ~15m scan.
    """
    if sys.platform not in {"darwin", "win32"}:
        # Linux is a Detect-only distribution with no daemon: stay silent so
        # those devices never show up in daemon fleet-state counts.
        return
    if sys.platform == "win32" and is_running_as_system():
        # Logged-off profile scans run as SYSTEM and cannot probe a user-owned
        # daemon pipe. Stay silent instead of reporting false degradation.
        return
    detail = _daemon_health_snapshot()
    state = detail["state"]
    if state == "gate_off":
        status = "disabled"
        error_message = None
    elif state == "degraded":
        status = "error"
        error_message = _daemon_degraded_message(detail)
    else:
        status = "ok"
        error_message = None

    payload = _base_payload(
        ctx,
        feature="daemon",
        status=status,
        tools=tools,
        agent_version=__version__,
        error_message=error_message,
    )
    payload["daemon_detail"] = detail
    _submit_payload(client, payload, log_event="aiwatch_daemon_checkin_failed")


def _run_isolated(feature: str, run: Callable[[], None]) -> None:
    """Run one best-effort check-in, logging (never raising) on failure.

    The check-ins already swallow *expected* network errors internally; this
    guards against *unexpected* ones (e.g. a corrupt MDM plist) so one check-in
    can't block the others or the caller.
    """
    try:
        run()
    except Exception as exc:
        logger.warning(
            "aiwatch_checkin_failed",
            feature=feature,
            error=str(exc),
            error_type=type(exc).__name__,
            exc_info=True,
        )


def submit_validation_checkins(
    client: RunlayerClient,
    *,
    ctx: DeviceContext,
    tools: list[InstalledTool],
) -> None:
    """Run the Enforce + Sessions hook-validation check-ins, each isolated.

    Shared by the scan path (``submit_all_scan_checkins``) and the enroll path,
    so both report feature health identically. Each check-in self-gates on
    managed config; failures are logged, never raised.
    """
    _run_isolated(
        "enforce",
        lambda: submit_enforce_validation_checkin(client, ctx=ctx, tools=tools),
    )
    _run_isolated(
        "sessions",
        lambda: submit_sessions_validation_checkin(client, ctx=ctx, tools=tools),
    )


def submit_all_scan_checkins(client: RunlayerClient, result: ScanResult) -> None:
    """Submit every best-effort AI Watch check-in for a completed scan.

    Owns all scan check-in policy: the enforce + sessions hook-validation
    check-ins, the daemon fleet-health check-in, plus a detect check-in when the
    scan found no MCP servers (so the
    device still records liveness). Each is independently guarded so a transient
    failure — corrupt MDM config, a network blip — never interrupts the scan.
    Callers just hand over the client + scan result.
    """
    ctx = device_context_dict(result)
    submit_validation_checkins(client, ctx=ctx, tools=result.tools)
    _run_isolated(
        "daemon",
        lambda: submit_daemon_checkin(client, ctx=ctx, tools=result.tools),
    )
    if result.total_servers == 0:
        _run_isolated("detect", lambda: submit_detect_checkin(client, result))
