"""Diagnostic reports to the Probe team: what broke on this machine, sent once. ONE implementation for every sender (plan B1, B4, B9). Details: DESIGN.md."""

from __future__ import annotations

import contextlib
import os
import re
import time
from collections.abc import Mapping
from dataclasses import dataclass
from pathlib import Path

from probe.foundation.compat.compat import StrEnum

ROUTE = "/v1/diagnostics/reports"

#: `family` and `reason`: the server's slug rule (no enum on its side).
SLUG = re.compile(r"^[a-z0-9_:.-]{1,64}$")


class Scope(StrEnum):
    #: The small allowlisted report the service and `probe doctor --send` send.
    STAFF = "staff"
    #: The full debug log (`probe doctor --bundle`): whole files, more sources.
    LOCAL = "local"


class Kind(StrEnum):
    AUTO = "auto"
    MANUAL = "manual"


class Failure(StrEnum):
    """Why a send did not land: the contract's error kinds (and the `report`
    read's `skipped` words)."""

    OFFLINE = "offline"
    RATE_LIMITED = "rate_limited"
    TOO_LARGE = "too_large"
    SERVER = "server"
    UNAUTHORIZED = "unauthorized"


#: `skipped` when a report of this family was already sent in this window.
DEDUPED = "deduped"
#: `skipped` prefix when the gate stops an automatic report.
DISABLED = "disabled:"
#: A manual report's family and reason (`probe doctor --send`).
MANUAL_FAMILY = "manual"
MANUAL_REASON = "doctor_send"


@dataclass(frozen=True)
class Answer:
    """The `report` read's one answer object (the contract's shape, exactly)."""

    sent: bool
    id: str | None = None
    skipped: str | None = None
    path: str | None = None

    def as_json(self) -> dict:
        return {"sent": self.sent, "id": self.id, "skipped": self.skipped, "path": self.path}


#: A send that failed on one of these gives its window back (`release`): a
#: later try can land (the network is back, the server too, the rate limit
#: lifted). A report too large, or refused for its credentials, keeps it: the
#: same report would fail the same way.
RELEASED_ON = frozenset({Failure.OFFLINE, Failure.SERVER, Failure.RATE_LIMITED})


# ---------------------------------------------------------------------------
# One report, end to end
# ---------------------------------------------------------------------------


def send(*, auto: bool, family: str, reason: str, sid: str | None = None, env: Mapping[str, str] | None = None,
         facts: dict | None = None, now: float | None = None) -> Answer:
    """Gate (automatic only), dedupe (automatic only), collect, keep the local
    copy, upload. Never raises on the network's account."""
    kind = Kind.AUTO if auto else Kind.MANUAL
    at = time.time() if now is None else now
    if auto:
        try:
            why = disabled(dict(env or {}))
        except Exception:  # noqa: BLE001 -- consent that cannot be read is no consent
            why = "unreadable"
        if why:
            return Answer(sent=False, skipped=f"{DISABLED}{why}")
        try:
            claimed = claim(family, sid or "machine", now=at)
        except OSError:
            # No stamp, no dedupe: an automatic report is not sent without one.
            return Answer(sent=False, skipped=Failure.SERVER.value)
        if not claimed:
            return Answer(sent=False, skipped=DEDUPED)
    try:
        staff = collect(Scope.STAFF, family=family, reason=reason, sid=sid, facts=facts, kind=kind)
        body = wire_body(staff, kind=kind, family=family, reason=reason)
    except Exception:  # noqa: BLE001 -- a bug here still answers; nothing unscrubbed is sent
        if auto:
            release(family, sid or "machine", now=at)
        return Answer(sent=False, skipped=Failure.SERVER.value)
    path: Path | None
    try:
        path = keep_copy(body, {"sent": False, "id": None, "skipped": "sending"})
    except OSError:
        path = None  # the report is still sent; only the local copy is lost
    reply = api_call(lambda transport: transport.request("POST", ROUTE, json_body=body, idempotent=False))
    report_id = reply.body.get("id") if reply.ok and isinstance(reply.body, dict) else None
    shown = str(path) if path is not None else None
    if reply.ok and isinstance(report_id, str) and report_id:
        answer = Answer(sent=True, id=report_id, path=shown)
    else:
        failure = reply.failure or Failure.SERVER
        answer = Answer(sent=False, skipped=failure.value, path=shown)
        if auto and failure in RELEASED_ON:
            release(family, sid or "machine", now=at)
        if auto and failure is Failure.UNAUTHORIZED and reply.status in (401, 403):
            # A key was tried and refused (a signed-out machine holds none: no alert).
            undeliverable(family, reason, now=at)
    if path is not None:
        with contextlib.suppress(OSError):
            keep_copy(body, {**answer.as_json(), "status": reply.status}, path)
    return answer


def undeliverable(family: str, reason: str, *, now: float | None = None) -> None:
    """Every credential here was refused, so the report cannot reach us: say
    so the one way left, a telemetry event a PostHog destination posts to
    #eng-alerts (`service.report_undeliverable`). Once per family per machine
    per dedupe window (its own claim: the report's is per session, and one
    outage fails every session's). Never raises."""
    try:
        if not claim(f"{family}.undeliverable", "machine", now=now):
            return
        from probe import analytics as telemetry

        telemetry.emit_report_undeliverable(family=family, reason=reason, base_url=base_url())
    except Exception:  # noqa: BLE001 -- telemetry never costs the report anything
        pass


def run(request) -> Answer:
    """The `report` read (`probe.core.requests.ReportRequest`)."""
    return send(auto=request.auto, family=request.family, reason=request.reason, sid=request.sid,
                env=request.env or {}, facts=request.facts)


def doctor_row() -> str:
    """`probe doctor`'s row: on (and the last one sent), or off and why."""
    from probe.analytics import report_policy

    why = report_policy.staff_reports_disabled(os.environ, base_url())
    if why:
        label = {
            "telemetry_off": "PROBE_TELEMETRY is off",
            "diagnostics_off": "PROBE_DIAGNOSTICS is off",
            "not_hosted": "this server is not Probe's hosted service",
        }.get(why, why)
        return f"off ({label})"
    last = last_sent()
    if last is None:
        return "on · none sent yet"
    when = time.strftime("%Y-%m-%d %H:%M UTC", time.gmtime(last[0]))
    return f"on · last sent {when} ({last[1]})"
from probe.shared.reports.api import api_call, wire_body  # noqa: E402 -- pieces need each other; the front door loads this one first
from probe.shared.reports.ledger import claim, disabled, keep_copy, last_sent, release  # noqa: E402 -- pieces need each other; the front door loads this one first
from probe.shared.reports.sessions import base_url  # noqa: E402 -- pieces need each other; the front door loads this one first
from probe.shared.reports.staff_report import collect  # noqa: E402 -- pieces need each other; the front door loads this one first
