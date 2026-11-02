"""assemble the STAFF report object (allowlisted, scrubbed) and fit it under REPORT_MAX_BYTES."""

from __future__ import annotations
import json
import re
import time
from dataclasses import dataclass, field
from probe.shared.reports.reports import Kind, MANUAL_FAMILY, MANUAL_REASON, Scope
#: The report object's own cap (the server takes 640 KiB of body).
REPORT_MAX_BYTES = 512 * 1024
#: The service's facts, as the `report` read's contract caps them.
FACTS_MAX_BYTES = 64 * 1024
#: Each STAFF source's own budget: a hung read costs the report one source.
STAFF_SOURCE_BUDGET_S = 2.0
#: The contract's bounds on the wire fields.
MAX_HARNESSES = 8
MAX_SESSION_IDS = 50
_UUID_EXACT = re.compile(r"^[0-9a-fA-F]{8}-[0-9a-fA-F]{4}-[0-9a-fA-F]{4}-[0-9a-fA-F]{4}-[0-9a-fA-F]{12}$")


# ---------------------------------------------------------------------------
# collect(scope)
# ---------------------------------------------------------------------------


@dataclass
class StaffReport:
    """`collect(Scope.STAFF)`: the report object and what the wire body names."""

    report: dict
    harnesses: list[str] = field(default_factory=list)
    session_ids: list[str] = field(default_factory=list)


def collect(scope: Scope, *, family: str = MANUAL_FAMILY, reason: str = MANUAL_REASON, sid: str | None = None,
            facts: dict | None = None, kind: Kind = Kind.MANUAL, deadline_s: float | None = None):
    """What this machine says about itself, for `scope`.

    STAFF: a `StaffReport` (B1: allowlisted, bound, tail-capped, scrubbed with
    this machine's identity removed). LOCAL: the debug log's files
    (`probe.core.debug_bundle.Collection`, B9: whole files, more sources, home
    paths kept). Same readers, same scrubber."""
    if scope is Scope.LOCAL:
        from probe.core import debug_bundle

        return debug_bundle.collect(deadline_s=deadline_s)
    return _collect_staff(family=family, reason=reason, sid=sid, facts=facts or {}, kind=kind)


def _collect_staff(*, family: str, reason: str, sid: str | None, facts: dict, kind: Kind) -> StaffReport:
    now = time.time()
    skipped: dict[str, str] = {}
    live = run_source("live_sessions", live_sessions, STAFF_SOURCE_BUDGET_S, skipped) or []
    include_session = bool(sid) and bool(run_source("binding", lambda: bound(sid), STAFF_SOURCE_BUDGET_S, skipped))
    if sid:
        allowed = {sid.lower()} if include_session else set()
    else:
        # A machine report: lines naming a live session bound to this account.
        allowed = {
            s["sid"].lower() for s in live
            if run_source(f"binding_{s['sid'][:8]}", lambda s=s: bound(s["sid"]), STAFF_SOURCE_BUDGET_S, skipped)
        }
    report: dict = {
        "scope": Scope.STAFF.value,
        "kind": kind.value,
        "family": family,
        "reason": reason,
        "created_at": int(now),
        "install": run_source("install", install_facts, STAFF_SOURCE_BUDGET_S, skipped),
        "service": run_source("service", lambda: service_facts(Scope.STAFF), STAFF_SOURCE_BUDGET_S, skipped),
        "session": (run_source("session", lambda: session_facts(sid, Scope.STAFF), STAFF_SOURCE_BUDGET_S, skipped)
                    if sid else None),
        "facts": _scrubbed_facts(facts),
        "live_sessions": len(live),
    }
    if kind is Kind.MANUAL:
        report["service_view"] = run_source("service_view", _service_view, STAFF_SOURCE_BUDGET_S, skipped)
        report["codex_hooks"] = run_source("codex_hooks", lambda: _codex_hooks(allowed), STAFF_SOURCE_BUDGET_S * 2,
                                           skipped)
    logs = run_source("logs", lambda: staff_logs(sid, allowed, include_session, now, skipped),
                      STAFF_SOURCE_BUDGET_S * 2, skipped) or {}
    report["logs"] = logs
    if sid and not include_session:
        report["withheld"] = ("this session's logs: its daemon trace folder is not recorded under this "
                              "server and daemon key")
    report["skipped"] = skipped
    _fit(report, REPORT_MAX_BYTES)

    harnesses: list[str] = []
    session_ids: list[str] = []
    if sid:
        session_ids.append(sid)
        harnesses.extend(s.get("harness") for s in registry_sessions() if s.get("sid") == sid)
    elif kind is Kind.MANUAL:
        from probe.sdk import agent_session

        own = agent_session.session_id_from_env()
        if own:
            session_ids.append(own)
        harnesses.extend(s.get("harness") for s in live)
    else:
        session_ids.extend(s["sid"] for s in live)
        harnesses.extend(s.get("harness") for s in live)
    return StaffReport(
        report=report,
        harnesses=list(dict.fromkeys(h for h in map(_harness_slug, harnesses) if h))[:MAX_HARNESSES],
        session_ids=list(dict.fromkeys(s.lower() for s in session_ids if _UUID_EXACT.match(s)))[:MAX_SESSION_IDS],
    )


def _scrubbed_facts(facts: dict) -> dict:
    if not facts:
        return {}
    try:
        return redact_tree(facts, Scope.STAFF)
    except Exception:  # noqa: BLE001 -- withheld, never sent raw
        return {"dropped": "the service's facts could not be scrubbed"}


def _service_view() -> dict:
    """The service's own allowlisted summary (`probe doctor`'s, `service_calls.view`)."""
    from probe.cli.lifecycle import service_calls

    return redact_tree(service_calls.view(timeout=STAFF_SOURCE_BUDGET_S), Scope.STAFF)


def _codex_hooks(allowed: set[str]) -> dict:
    """Which of Probe's hooks Codex runs, as `probe status` reads it (`codex_hooks`):
    a session unknown to the service may be one whose hooks Codex skips. The
    session that never heard them is named only when it is in `allowed`."""
    from probe.shared.harness.harnesses.codex import hooks as codex_hooks

    snapshot = codex_hooks.status_snapshot()
    unheard = snapshot.get("unheard_session")
    if unheard and unheard.lower() not in allowed:
        snapshot["unheard_session"] = "withheld"
    return redact_tree(snapshot, Scope.STAFF)


def _size(value: object) -> int:
    """Bytes as the SDK transport sends them (`json.dumps` with its default
    ASCII escapes): non-ASCII text takes 6 bytes a character there."""
    return len(json.dumps(value).encode("utf-8"))


def _fit(report: dict, cap: int) -> None:
    """Past `cap`, the largest log tail loses its oldest lines first, then the
    facts are cut."""
    logs = report.get("logs") or {}
    while _size(report) > cap and logs:
        name = max(logs, key=lambda key: len(logs[key]))
        lines = logs[name].splitlines(keepends=True)
        if len(lines) <= 1:
            del logs[name]
            continue
        logs[name] = "".join(lines[max(1, len(lines) // 10):])
        report["trimmed"] = True
    if _size(report) > cap:
        report["facts"] = {"dropped": "the report was over its size cap"}
        report["trimmed"] = True
from probe.shared.reports.facts import _harness_slug, install_facts, run_source, service_facts, session_facts  # noqa: E402 -- pieces need each other; the front door loads this one first
from probe.shared.reports.logs import staff_logs  # noqa: E402 -- pieces need each other; the front door loads this one first
from probe.shared.reports.scrub import redact_tree  # noqa: E402 -- pieces need each other; the front door loads this one first
from probe.shared.reports.sessions import bound, live_sessions, registry_sessions  # noqa: E402 -- pieces need each other; the front door loads this one first
