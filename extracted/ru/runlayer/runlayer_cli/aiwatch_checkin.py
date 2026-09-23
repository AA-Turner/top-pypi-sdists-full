"""Best-effort AI Watch check-ins for the aiwatch bundle."""

from __future__ import annotations

import sys
import time
from collections.abc import Callable, Mapping
from typing import Any, Protocol

import httpx
import structlog

from runlayer_cli import __version__
from runlayer_cli.api import RunlayerClient
from runlayer_cli.hook import host_override
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

# Single-form payload keys that describe the device rather than one feature.
# The batch body carries them once at the top level; everything else in a
# single-form payload is that feature's entry. Mirrored by the backend's
# ``AIWatchCheckInDeviceFields`` (contract test on the backend side).
BATCH_CHECKIN_DEVICE_KEYS: frozenset[str] = frozenset(
    {
        "device_id",
        "hostname",
        "os",
        "os_version",
        "username",
        "org_device_id",
        "serial_number",
        "windows_user_sid",
        "tools",
    }
)

# Failure log event per scan-tick feature. The builders and the batch
# fallback replay both read from here, so the replay cannot log a different
# event than the direct single-form path would have.
_SCAN_LOG_EVENTS: dict[str, str] = {
    "protect": "aiwatch_protect_checkin_failed",
    "enforce": "aiwatch_enforce_checkin_failed",
    "sessions": "aiwatch_sessions_checkin_failed",
    "daemon": "aiwatch_daemon_checkin_failed",
    "detect": "aiwatch_detect_checkin_failed",
}


class CheckInSubmitter(Protocol):
    """The slice of ``RunlayerClient`` the check-in builders depend on."""

    @property
    def base_url(self) -> str: ...

    def submit_aiwatch_checkin(self, payload: dict[str, Any]) -> dict[str, Any]: ...


class _CheckInCollector:
    """Stand-in submitter that captures single-form payloads instead of sending.

    Lets the scan path reuse every existing check-in builder unchanged and ship
    the captured payloads in one batch request afterwards.
    """

    def __init__(self, client: RunlayerClient) -> None:
        self._client = client
        self.payloads: list[dict[str, object]] = []

    @property
    def base_url(self) -> str:
        return self._client.base_url

    def submit_aiwatch_checkin(self, payload: dict[str, Any]) -> dict[str, Any]:
        self.payloads.append(payload)
        return {}


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


def _make_device_context(
    *,
    username: str | None = None,
    windows_user_sid: str | None = None,
) -> DeviceContext:
    """Build a device context from local machine metadata.

    For call paths without a scan result (e.g. enroll) so every check-in caller
    supplies a concrete ``DeviceContext``.
    """
    metadata = get_device_metadata()
    context = DeviceContext(
        device_id=get_or_create_device_id(),
        hostname=metadata.get("hostname"),
        os=metadata.get("os"),
        os_version=metadata.get("os_version"),
        username=(
            username if username is not None else _resolve_checkin_username(metadata)
        ),
        org_device_id=None,
        serial_number=metadata.get("serial_number"),
    )
    if windows_user_sid is not None:
        context["windows_user_sid"] = windows_user_sid
    return context


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


def _submit_payload_for_response(
    client: CheckInSubmitter,
    payload: dict[str, object],
    *,
    log_event: str,
) -> dict[str, object] | None:
    """Like ``_submit_payload`` but returns the response body (None on failure)."""
    for attempt in range(len(_CHECKIN_RETRY_DELAYS_SECONDS) + 1):
        try:
            return client.submit_aiwatch_checkin(payload)
        except ValueError as exc:
            logger.warning(log_event, error=str(exc))
            return None
        except httpx.HTTPStatusError as exc:
            logger.warning(
                "aiwatch_checkin_rejected",
                status_code=exc.response.status_code,
                feature=payload.get("feature"),
                response_body=exc.response.text[
                    :_CHECKIN_REJECTED_RESPONSE_BODY_MAX_LEN
                ],
            )
            return None
        except (httpx.TransportError, OSError) as exc:
            if attempt == len(_CHECKIN_RETRY_DELAYS_SECONDS):
                logger.warning(log_event, error=str(exc))
                return None
            time.sleep(_CHECKIN_RETRY_DELAYS_SECONDS[attempt])
        except httpx.HTTPError as exc:
            logger.warning(log_event, error=str(exc))
            return None
    return None


def _submit_payload(
    client: CheckInSubmitter,
    payload: dict[str, object],
    *,
    log_event: str,
) -> None:
    """Submit a check-in best-effort, retrying bounded transport failures."""
    _submit_payload_for_response(client, payload, log_event=log_event)


def submit_llm_routing_checkin(
    client: RunlayerClient,
    *,
    ctx: DeviceContext,
    tools: list[InstalledTool],
    status: str,
    device_key_hash: str | None,
    rotate: bool = False,
    error_message: str | None = None,
) -> dict[str, object] | None:
    """Report LLM routing state and return the backend's key decision.

    Unlike the other check-ins the caller needs the body (``device_key`` /
    ``device_key_status``). Returns None on any transport/HTTP failure or when
    the backend predates the endpoint (``{"unsupported": True}``).
    ``rotate`` asks the backend to supersede the active key and mint a new one
    when the credential on disk is gone.
    """
    payload = _base_payload(
        ctx,
        feature="llm_routing",
        status=status,
        tools=tools,
        agent_version=__version__,
        error_message=error_message,
    )
    payload["device_key_hash"] = device_key_hash
    if rotate:
        payload["rotate"] = True
    response = _submit_payload_for_response(
        client,
        payload,
        log_event="aiwatch_llm_routing_checkin_failed",
    )
    if response is None or response.get("unsupported"):
        return None
    return response


def _submit_simple_checkin(
    client: CheckInSubmitter,
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


def submit_detect_checkin(client: CheckInSubmitter, result: ScanResult) -> None:
    """Record that a scan ran, even when no findings were submitted."""
    payload = _base_payload(
        device_context_dict(result),
        feature="detect",
        status="ok",
        tools=result.tools,
        agent_version=result.collector_version,
    )
    payload["container_detail"] = {
        "enabled": result.container_scan_requested,
        "host_containers_scanned": result.containers_scanned,
        "failure_reason": (
            result.container_scan_failure_reason()
            if result.container_scan_requested and not result.containers_scanned
            else None
        ),
    }
    # Detect fires every scan on every platform, so it is the carrier for the
    # full-CLI hook host deviation: ``None`` (no fresh marker) clears the
    # tenant-side record, so a fixed ``default_host`` self-heals within a scan.
    payload["hook_host_detail"] = _hook_host_detail(client)
    _submit_payload(client, payload, log_event=_SCAN_LOG_EVENTS["detect"])


def _hook_host_detail(client: CheckInSubmitter) -> host_override.HostOverride | None:
    """Fresh ``hook_host_override`` marker for the user this scan reports on.

    Hooks write it under the user's ``~/.runlayer/state``, and every scan path
    already runs with that user's home: the macOS scan is a per-user
    LaunchAgent, the Windows ``--all-users`` fan-out drops to the logged-on
    user's token or points ``USERPROFILE`` at the logged-off profile, and
    Linux uses ``runuser``. No console-user fallback: on Windows it would pin
    the console user's marker onto another user's check-in.

    Only the managed tenant gets the marker. ``runlayer scan`` follows the
    MDM host by default, but an explicit ``--host`` / ``RUNLAYER_HOST`` can
    still point this check-in elsewhere; the marker describes hooks bound
    for ``managed_host``, so any other destination must not receive it.
    """
    marker = host_override.read_marker()
    if marker is None:
        return None
    if client.base_url.rstrip("/") != marker["managed_host"].rstrip("/"):
        return None
    return marker


def _submit_hook_validation_checkin(
    client: CheckInSubmitter,
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
    payload = _base_payload(
        ctx,
        feature="detect",
        status="error",
        tools=tools or [],
        agent_version=__version__,
        error_message=error_message,
    )
    # The hook host marker is independent of scan outcome; every Detect
    # check-in rewrites the tenant-side record, so omitting it here would
    # clear the badge on any scan failure.
    payload["hook_host_detail"] = _hook_host_detail(client)
    _submit_payload(client, payload, log_event="aiwatch_detect_error_checkin_failed")


def submit_enforce_validation_checkin(
    client: CheckInSubmitter,
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
                log_event=_SCAN_LOG_EVENTS[feature],
            )
        return

    feature = "enforce"
    if mode is AIWatchMode.PROTECT:
        # Clear any formerly-active Enforce state before reporting Protect.
        _submit_simple_checkin(
            client,
            feature="enforce",
            status="disabled",
            ctx=ctx,
            tools=tools,
            log_event=_SCAN_LOG_EVENTS["enforce"],
        )
        feature = "protect"
    else:
        # Enforce and Protect are mutually exclusive endpoint modes. Clear a
        # formerly-active Protect row before reporting current Enforce health.
        _submit_simple_checkin(
            client,
            feature="protect",
            status="disabled",
            ctx=ctx,
            tools=tools,
            log_event=_SCAN_LOG_EVENTS["protect"],
        )

    _submit_hook_validation_checkin(
        client,
        feature=feature,
        include_pipeline=resolve_include_pipeline(False, managed),
        ctx=ctx,
        tools=tools,
        log_event=_SCAN_LOG_EVENTS[feature],
    )


def submit_sessions_validation_checkin(
    client: CheckInSubmitter,
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
            log_event=_SCAN_LOG_EVENTS["sessions"],
        )
        return
    _submit_hook_validation_checkin(
        client,
        feature="sessions",
        include_pipeline=True,
        ctx=ctx,
        tools=tools,
        log_event=_SCAN_LOG_EVENTS["sessions"],
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
    client: CheckInSubmitter,
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
    _submit_payload(client, payload, log_event=_SCAN_LOG_EVENTS["daemon"])


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
    client: CheckInSubmitter,
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


def build_batch_checkin_payload(
    ctx: DeviceContext,
    tools: list[InstalledTool],
    payloads: list[dict[str, object]],
) -> dict[str, object]:
    """Fold single-form payloads into one batch body.

    Every captured payload was built from the same ``ctx`` + ``tools``, so the
    device half goes out once and each entry keeps only its feature half.
    """
    return {
        **ctx,
        "tools": tools,
        "features": [
            {
                key: value
                for key, value in payload.items()
                if key not in BATCH_CHECKIN_DEVICE_KEYS
            }
            for payload in payloads
        ],
    }


def _submit_batch(client: RunlayerClient, payload: dict[str, object]) -> bool:
    """Send one batch; True when the single-form path should run instead.

    Falling back covers a backend without the batch route (the client maps
    that 404 to ``{"unsupported": True}``) and a rejected body (422): one
    refused feature must not cost the others their liveness, which the
    sequential path guarantees by construction. Any other failure is final for
    this tick — replaying five requests against a struggling backend would
    defeat the batching.
    """
    for attempt in range(len(_CHECKIN_RETRY_DELAYS_SECONDS) + 1):
        try:
            response = client.submit_aiwatch_checkin_batch(payload)
        except httpx.HTTPStatusError as exc:
            status_code = exc.response.status_code
            logger.warning(
                "aiwatch_checkin_batch_rejected",
                status_code=status_code,
                response_body=exc.response.text[
                    :_CHECKIN_REJECTED_RESPONSE_BODY_MAX_LEN
                ],
            )
            return status_code == 422
        except (httpx.TransportError, OSError) as exc:
            if attempt == len(_CHECKIN_RETRY_DELAYS_SECONDS):
                logger.warning("aiwatch_checkin_batch_failed", error=str(exc))
                return False
            time.sleep(_CHECKIN_RETRY_DELAYS_SECONDS[attempt])
        except (httpx.HTTPError, ValueError) as exc:
            logger.warning("aiwatch_checkin_batch_failed", error=str(exc))
            return False
        else:
            if response.get("unsupported"):
                logger.debug("aiwatch_checkin_batch_unsupported")
                return True
            return False
    return False


def _flush_scan_checkins(
    client: RunlayerClient,
    *,
    ctx: DeviceContext,
    tools: list[InstalledTool],
    payloads: list[dict[str, object]],
) -> None:
    if not payloads:
        return
    should_fall_back = _submit_batch(
        client, build_batch_checkin_payload(ctx, tools, payloads)
    )
    if not should_fall_back:
        return
    for payload in payloads:
        _submit_payload(
            client,
            payload,
            log_event=_SCAN_LOG_EVENTS.get(
                str(payload.get("feature")), "aiwatch_checkin_failed"
            ),
        )


def submit_all_scan_checkins(client: RunlayerClient, result: ScanResult) -> None:
    """Submit every best-effort AI Watch check-in for a completed scan.

    Owns all scan check-in policy: the enforce + sessions hook-validation
    check-ins, the daemon fleet-health check-in, plus the final detect check-in.
    Detect runs last so its current container health wins over MCP ingestion,
    including when the scan found servers. Each is independently guarded so a
    transient failure — corrupt MDM config, a network blip — never interrupts
    the scan. The builders write into a collector and the captured payloads go
    out as one batch request (one request per feature on backends without the
    batch route), so the per-feature ordering above is preserved either way.
    Callers just hand over the client + scan result.
    """
    ctx = device_context_dict(result)
    collector = _CheckInCollector(client)
    submit_validation_checkins(collector, ctx=ctx, tools=result.tools)
    _run_isolated(
        "daemon",
        lambda: submit_daemon_checkin(collector, ctx=ctx, tools=result.tools),
    )
    _run_isolated("detect", lambda: submit_detect_checkin(collector, result))
    _flush_scan_checkins(
        client, ctx=ctx, tools=result.tools, payloads=collector.payloads
    )
