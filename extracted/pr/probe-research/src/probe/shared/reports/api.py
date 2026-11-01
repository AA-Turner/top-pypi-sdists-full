"""POST a report to /v1/diagnostics/reports with the CLI token, then the daemon key."""

from __future__ import annotations
from collections.abc import Callable
from dataclasses import dataclass
SCHEMA = 1
UPLOAD_TIMEOUT_S = 10.0
VERSION_MAX_CHARS = 32


@dataclass(frozen=True)
class Reply:
    """One API call's outcome: its JSON on success, else why not."""

    status: int | None
    body: dict | None = None
    failure: Failure | None = None
    retry_after: float | None = None
    token: str | None = None

    @property
    def ok(self) -> bool:
        return self.failure is None


# ---------------------------------------------------------------------------
# The wire
# ---------------------------------------------------------------------------


def credentials() -> list[str]:
    """The CLI's token, then the daemon key (the same config context)."""
    tokens: list[str] = []
    try:
        from probe.sdk.settings.settings import resolve

        token = resolve().token
        if token:
            tokens.append(token)
    except Exception:  # noqa: BLE001
        pass
    key = daemon_key()
    if key and key not in tokens:
        tokens.append(key)
    return tokens


def failure_for(status: int | None) -> Failure:
    """The contract's error kind for an HTTP status (None: no answer at all)."""
    if status is None:
        return Failure.OFFLINE
    if status in (401, 403):
        return Failure.UNAUTHORIZED
    if status == 413:
        return Failure.TOO_LARGE
    if status == 429:
        return Failure.RATE_LIMITED
    return Failure.SERVER


def api_call(call: Callable, *, timeout: float = UPLOAD_TIMEOUT_S, tokens: list[str] | None = None) -> Reply:
    """One call to the API through the SDK transport (`X-Probe-Device` and the
    CLI's version headers ride along), with each credential in turn: a 401 or
    403 tries the next one. Never retried otherwise, never raises.

    `call(transport)` makes the request with a literal method and path
    (`transport.request("POST", ROUTE, ...)`), so the client/server parity
    check (`tests/test_parity.py`) sees every route this module reaches."""
    from probe.foundation.request_identity.request_identity import client_version_headers
    from probe.sdk import errors
    from probe.sdk.settings.settings import Settings, resolve
    from probe.foundation.request_identity.surface import Surface
    from probe.sdk.delivery.transport.transport import Transport

    try:
        url = resolve().base_url
    except Exception:  # noqa: BLE001
        return Reply(status=None, failure=Failure.UNAUTHORIZED)
    tokens = credentials() if tokens is None else tokens
    if not tokens:
        return Reply(status=None, failure=Failure.UNAUTHORIZED)
    last = Reply(status=None, failure=Failure.UNAUTHORIZED)
    for token in tokens:
        try:
            with Transport(
                Settings(base_url=url, token=token),
                timeout=timeout,
                max_retries=0,
                surface=Surface.CLI.value,
                client_headers=client_version_headers(Surface.CLI.value, _cli_version()),
            ) as transport:
                response = call(transport)
            try:
                parsed = response.json()
            except ValueError:
                parsed = None
            return Reply(status=response.status_code, body=parsed if isinstance(parsed, dict) else {}, token=token)
        except errors.RosError as exc:
            status = exc.status if isinstance(exc.status, int) else None
            retry = getattr(exc, "retry_after", None)
            last = Reply(status=status, failure=failure_for(status),
                         retry_after=float(retry) if isinstance(retry, (int, float)) else None)
            if status in (401, 403):
                continue
            return last
        except Exception:  # noqa: BLE001 -- anything else never reached an answer
            return Reply(status=None, failure=Failure.OFFLINE)
    return last


def wire_body(staff: StaffReport, *, kind: Kind, family: str, reason: str) -> dict:
    """The `POST /v1/diagnostics/reports` body (contract, exactly)."""
    try:
        from probe.shared.updates import updates as versions

        local = versions.local_versions()
    except Exception:  # noqa: BLE001
        local = {"cli": _cli_version()}
    body = {
        "schema": SCHEMA,
        "kind": kind.value,
        "family": family,
        "reason": reason,
        "cli_version": str(local.get("cli") or _cli_version())[:VERSION_MAX_CHARS],
        "os": os_label(),
        "harnesses": staff.harnesses,
        "session_ids": staff.session_ids,
        "report": staff.report,
    }
    for name, wire in (("plugin", "plugin_version"), ("tap", "tap_version")):
        if isinstance(local.get(name), str) and local[name]:
            body[wire] = local[name][:VERSION_MAX_CHARS]
    return body
from probe.shared.reports.facts import _cli_version, os_label  # noqa: E402 -- pieces need each other; the front door loads this one first
from probe.shared.reports.reports import Failure, Kind  # noqa: E402 -- pieces need each other; the front door loads this one first
from probe.shared.reports.sessions import daemon_key  # noqa: E402 -- pieces need each other; the front door loads this one first
from probe.shared.reports.staff_report import StaffReport  # noqa: E402 -- pieces need each other; the front door loads this one first
