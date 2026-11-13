"""Track coarse startup phases so incomplete startups are diagnosable on shutdown.

``/ok`` only becomes available after lifespan startup finishes (including graph
import). When that hangs and the process is stopped, recording phase history
lets shutdown logs show where time went — not just whatever was running last.

State is process-wide on purpose: phase is set deep in graph load and read from
the SIGTERM / shutdown path, which does not share a call stack or request
context. One ``StartupSnapshot`` per process is enough.
"""

from __future__ import annotations

import time
from dataclasses import asdict, dataclass, field, replace
from typing import Any

from langgraph_api.timing.timer import get_startup_elapsed

# Customer graph / JS import work (import-time cost, FF_PROFILE_IMPORTS).
_GRAPH_IMPORT_PHASES = frozenset(
    {
        "loading_graph",
        "waiting_for_js_graphs",
        "registering_js_graph",
    }
)
_CUSTOM_APP_LIFESPAN_PHASE = "entering_custom_app_lifespan"

# Broader set of phases dominated by customer code (graphs or custom app).
_USER_CODE_PHASES = _GRAPH_IMPORT_PHASES | {_CUSTOM_APP_LIFESPAN_PHASE}

_GRAPH_IMPORT_GUIDANCE = (
    " The slowest phase runs your graph code and the delay is likely"
    " associated with that code. To resolve, move expensive setup out"
    " of module import, and set FF_PROFILE_IMPORTS=true to profile"
    " imports."
)
_CUSTOM_APP_LIFESPAN_GUIDANCE = (
    " The slowest phase is your custom app lifespan (the app configured"
    " under http.app in langgraph.json). Graph imports have already"
    " finished by this point — check startup hooks that lifespan awaits"
    " (DB connects, cache warm-up, network calls) rather than graph"
    " import-time work."
)


@dataclass(frozen=True, slots=True)
class PhaseRecord:
    phase: str
    elapsed_seconds: float
    graph_id: str | None = None
    in_progress: bool = False


@dataclass
class StartupSnapshot:
    phase: str = "starting"
    graph_id: str | None = None
    phase_started_at: float = field(default_factory=time.monotonic)
    startup_complete: bool = False
    phases: list[PhaseRecord] = field(default_factory=list)


# One startup per process; shutdown handlers read the same instance.
_STATUS = StartupSnapshot()


def reset_for_tests() -> None:
    """Reset process startup state between unit tests."""
    global _STATUS
    _STATUS = StartupSnapshot()


def _close_current_phase() -> None:
    elapsed = round(time.monotonic() - _STATUS.phase_started_at, 1)
    _STATUS.phases.append(
        PhaseRecord(
            phase=_STATUS.phase,
            elapsed_seconds=elapsed,
            graph_id=_STATUS.graph_id,
        )
    )


def set_phase(phase: str, *, graph_id: str | None = None) -> None:
    """Record the coarse startup phase currently in progress."""
    if _STATUS.startup_complete:
        return
    _close_current_phase()
    _STATUS.phase = phase
    _STATUS.graph_id = graph_id
    _STATUS.phase_started_at = time.monotonic()


def mark_ready() -> None:
    """Mark startup complete so shutdown context reflects readiness."""
    if not _STATUS.startup_complete:
        _close_current_phase()
    _STATUS.startup_complete = True
    _STATUS.phase = "ready"
    _STATUS.graph_id = None
    _STATUS.phase_started_at = time.monotonic()


def snapshot() -> StartupSnapshot:
    """Return a copy of current startup progress."""
    return replace(_STATUS, phases=list(_STATUS.phases))


def is_user_code_phase(phase: str) -> bool:
    """Return True when ``phase`` is dominated by customer graph/JS/app code."""
    return phase in _USER_CODE_PHASES


def guidance_for_phase(phase: str) -> str | None:
    """Return phase-specific remediation text for the slowest startup phase."""
    if phase in _GRAPH_IMPORT_PHASES:
        return _GRAPH_IMPORT_GUIDANCE
    if phase == _CUSTOM_APP_LIFESPAN_PHASE:
        return _CUSTOM_APP_LIFESPAN_GUIDANCE
    return None


def phases_by_duration(snap: StartupSnapshot) -> list[PhaseRecord]:
    """Completed phases plus the current one, slowest first."""
    current = PhaseRecord(
        phase=snap.phase,
        elapsed_seconds=round(time.monotonic() - snap.phase_started_at, 1),
        graph_id=snap.graph_id,
        in_progress=True,
    )
    records = [*snap.phases, current]
    return sorted(records, key=lambda r: r.elapsed_seconds, reverse=True)


def _format_phase_record(record: PhaseRecord) -> str:
    parts = [record.phase]
    if record.graph_id is not None:
        parts.append(f"graph_id={record.graph_id}")
    parts.append(f"{record.elapsed_seconds}s")
    if record.in_progress:
        parts.append("(in progress)")
    return " ".join(parts)


def incomplete_startup_detail(snap: StartupSnapshot) -> str:
    """Human-readable summary of where startup time went."""
    ranked = phases_by_duration(snap)
    total = round(get_startup_elapsed(), 1)
    ranked_text = ", ".join(_format_phase_record(r) for r in ranked)
    detail = (
        f"Startup did not complete ({total}s elapsed). "
        f"Phases by duration (slowest first): {ranked_text}."
    )
    if ranked:
        guidance = guidance_for_phase(ranked[0].phase)
        if guidance is not None:
            detail += guidance
    return detail


def shutdown_log_fields() -> dict[str, Any]:
    """Structured fields to attach to shutdown / SIGTERM logs.

    Phase timing is only included when startup did not complete — after a
    healthy start, process uptime is not a useful "startup elapsed" signal.
    """
    snap = snapshot()
    fields: dict[str, Any] = {
        "startup_complete": snap.startup_complete,
    }
    if not snap.startup_complete:
        fields["phase"] = snap.phase
        fields["phase_elapsed_seconds"] = round(
            time.monotonic() - snap.phase_started_at, 1
        )
        fields["total_startup_elapsed_seconds"] = round(get_startup_elapsed(), 1)
        if snap.graph_id is not None:
            fields["graph_id"] = snap.graph_id
        ranked = phases_by_duration(snap)
        fields["phases"] = [asdict(r) for r in ranked]
        fields["detail"] = incomplete_startup_detail(snap)
    return fields
