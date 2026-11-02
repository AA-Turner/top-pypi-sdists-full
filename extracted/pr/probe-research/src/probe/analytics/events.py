"""Every product event name (`Event`, generated from the contracts catalog; values are wire names
and never change), its EVENT_* string aliases and the emit_* wrappers that shape each one's props."""

from __future__ import annotations

from probe.analytics.generated import Event
from probe.analytics.context import detached_context, outbox_context
from probe.analytics.outcomes import InvokedBy, Via
from probe.analytics import sender  # call through the module: one binding for tests to patch
from probe.analytics.throttle import _age_hours, _error_kind, stuck_report_due, stuck_status

#: The EVENT_* names, kept as plain strings: each is its member's wire name (docs: the generated
#: `Event`, from the contracts catalog). New code sends `track(Event.X, ...)`.
EVENT_WIZARD_INVOKED = Event.WIZARD_INVOKED.value
EVENT_WIZARD_STARTED = Event.WIZARD_STARTED.value
EVENT_WIZARD_ACTION_CHOSEN = Event.WIZARD_ACTION_CHOSEN.value
EVENT_WIZARD_CONFIGURE_STARTED = Event.WIZARD_CONFIGURE_STARTED.value
EVENT_WIZARD_SIGNED_IN = Event.WIZARD_SIGNED_IN.value
EVENT_WIZARD_CONFIGURE_COMPLETED = Event.WIZARD_CONFIGURE_COMPLETED.value
EVENT_INTEGRATION_REINSTALL_STARTED = Event.INTEGRATION_REINSTALL_STARTED.value
EVENT_INTEGRATION_REINSTALL_COMPLETED = Event.INTEGRATION_REINSTALL_COMPLETED.value
EVENT_BACKFILL_INVOKED = Event.BACKFILL_INVOKED.value
EVENT_BACKFILL_STARTED = Event.BACKFILL_STARTED.value
EVENT_BACKFILL_SCANNED = Event.BACKFILL_SCANNED.value
EVENT_BACKFILL_PLAN_READY = Event.BACKFILL_PLAN_READY.value
EVENT_BACKFILL_APPROVED = Event.BACKFILL_APPROVED.value
EVENT_BACKFILL_SUMMARY = Event.BACKFILL_SUMMARY.value
EVENT_WIZARD_INSTALL_SETTLED = Event.WIZARD_INSTALL_SETTLED.value
EVENT_WIZARD_IMPORTS_CHOSEN = Event.WIZARD_IMPORTS_CHOSEN.value
EVENT_WIZARD_ONBOARDING_COMPLETED = Event.WIZARD_ONBOARDING_COMPLETED.value
EVENT_WIZARD_UNINSTALL_STARTED = Event.WIZARD_UNINSTALL_STARTED.value
EVENT_WIZARD_UNINSTALL_COMPLETED = Event.WIZARD_UNINSTALL_COMPLETED.value
EVENT_WIZARD_SIGNED_OUT = Event.WIZARD_SIGNED_OUT.value
EVENT_WIZARD_RECORDER_CHANGED = Event.WIZARD_RECORDER_CHANGED.value
EVENT_TRANSCRIPTS_SUMMARY = Event.TRANSCRIPTS_SUMMARY.value
EVENT_IMPORT_JOB_ENQUEUED = Event.IMPORT_JOB_ENQUEUED.value
EVENT_IMPORT_JOB_STALLED = Event.IMPORT_JOB_STALLED.value
EVENT_IMPORT_JOB_FINISHED = Event.IMPORT_JOB_FINISHED.value
EVENT_IMPORT_JOB_CLEARED = Event.IMPORT_JOB_CLEARED.value
EVENT_OUTBOX_DRAINED = Event.OUTBOX_DRAINED.value
EVENT_OUTBOX_STUCK = Event.OUTBOX_STUCK.value
EVENT_OUTBOX_RESCUED = Event.OUTBOX_RESCUED.value
EVENT_OUTBOX_DISCARDED = Event.OUTBOX_DISCARDED.value
EVENT_OUTBOX_RESTORED = Event.OUTBOX_RESTORED.value
EVENT_OUTBOX_PAUSE_LIFTED = Event.OUTBOX_PAUSE_LIFTED.value
EVENT_CAPTURE_REPAIR_APPLIED = Event.CAPTURE_REPAIR_APPLIED.value
EVENT_SETTINGS_REMOTE_APPLIED = Event.SETTINGS_REMOTE_APPLIED.value
EVENT_DELIVERY_SUMMARY = Event.DELIVERY_SUMMARY.value
EVENT_REPORT_UNDELIVERABLE = Event.REPORT_UNDELIVERABLE.value
EVENT_DAEMON_ERROR = Event.DAEMON_ERROR.value
EVENT_SERVICE_STARTED = Event.SERVICE_STARTED.value
EVENT_SERVICE_STATE = Event.SERVICE_STATE.value
EVENT_SERVICE_STOPPED = Event.SERVICE_STOPPED.value
EVENT_LIFEBOAT_ACTED = Event.LIFEBOAT_ACTED.value
EVENT_MCP_TOOL_SERVED = Event.MCP_TOOL_SERVED.value
EVENT_EXCEPTION = Event.EXCEPTION.value
#: The only events `emit_service_event` sends.
SERVICE_EVENTS = frozenset({EVENT_SERVICE_STARTED, EVENT_SERVICE_STATE, EVENT_SERVICE_STOPPED, EVENT_LIFEBOAT_ACTED})


def emit_report_undeliverable(*, family: str, reason: str, base_url: str | None) -> bool:
    """`service.report_undeliverable`: the report (`family`, `reason`, both
    slugs) could not go because the API refused every credential here, or none
    is held. Gated like every client event (opt-out, hosted backend only). True
    when it was handed to the sender. Never raises."""
    try:
        context = detached_context(base_url, via=Via.SERVICE)
        if not context.enabled:
            return False
        context.emit(EVENT_REPORT_UNDELIVERABLE, family=str(family)[:64], reason=str(reason)[:64])
        return True
    except Exception:
        return False  # observability must never become observable


def emit_service_event(event: str, props: dict, *, base_url: str | None) -> bool:
    """One of the Probe service's own events (`probe.service.watch.statepost`:
    `service.started`, `service.state`, `service.stopped`), with the
    properties `statepost.snapshot` built: its allow-list is the contract, and
    nothing is added here but the envelope. Gated like every client event: the
    opt-out, and ``base_url`` a hosted backend; the caller has asked the
    machine's consent. True when it was handed to the sender. Never raises."""
    try:
        if event not in SERVICE_EVENTS:
            return False
        context = detached_context(base_url, via=Via.SERVICE)
        if not context.enabled:
            return False
        context.emit(event, **props)
        return True
    except Exception:
        return False  # observability must never become observable


def emit_outbox_drained(
    *,
    base_url: str | None,
    outcome: str,  # an OutboxOutcome; defined at the producer, sdk.outbox_worker
    delivered: int,
    dead_lettered: int,
    remaining: int,
    passes: int,
    duration_s: float,
    dead_lettered_by_status: dict[str, int] | None = None,
    dead_lettered_no_such_run: int = 0,
) -> None:
    """Report one finished drain episode. Never raises: the worker owns data.
    ``dead_lettered_by_status``: the server's answer per dead letter, keyed like
    `sdk.delivery.summary`'s (``"404"``; ``"none"`` with no HTTP answer).
    ``dead_lettered_no_such_run``: how many of them were the run resolver's own
    "run not found" (`errors.names_no_such_run`), so the loss alert can tell a
    write naming no run from a 404 that lost it for reasons of ours."""
    try:
        outbox_context(base_url).emit(
            EVENT_OUTBOX_DRAINED,
            outcome=str(outcome),
            delivered=delivered,
            dead_lettered=dead_lettered,
            dead_lettered_by_status=dict(dead_lettered_by_status or {}) or None,
            dead_lettered_no_such_run=int(dead_lettered_no_such_run) or None,
            remaining=remaining,
            passes=passes,
            duration_s=round(duration_s, 2),
        )
    except Exception:
        pass  # observability must never become observable


def emit_outbox_rescued(
    *,
    base_url: str | None,
    credentials: int,
    writes: int,
    delivered: int,
    dead_lettered: int,
    remaining: int,
) -> None:
    """Report one automatic rescue: how many credentials were adopted, how
    many of their writes, and what its pass did with them; counts only.
    Never raises."""
    try:
        outbox_context(base_url).emit(
            EVENT_OUTBOX_RESCUED,
            credentials=credentials,
            writes=writes,
            delivered=delivered,
            dead_lettered=dead_lettered,
            remaining=remaining,
        )
    except Exception:
        pass  # observability must never become observable


def emit_outbox_discarded(counts, *, reason: str, interactive: bool = False) -> bool:
    """Report writes set aside (`DiscardReason`), from a `journal.DiscardCounts`:
    counts and enqueue dates only, never a fingerprint, key, body, name or path.
    Gated on the server the writes were pinned to (one, hosted), like every
    outbox event; ``interactive``: a person at a terminal ran it. The coding
    agent that ran it, if any, rides the envelope (`agent`). At most
    ``counts.reported_days`` enqueue days ride it (the journal's DISCARD_DAYS). True
    when it was handed to the sender. Never raises."""
    try:
        if not counts.writes:
            return False
        context = detached_context(counts.base_url, via=Via.OUTBOX)
        if not context.enabled:
            return False
        if interactive:
            context.invoked_by = InvokedBy.HUMAN
        days = sorted(counts.by_enqueue_day.items(), reverse=True)
        context.emit(
            EVENT_OUTBOX_DISCARDED,
            reason=str(reason),
            writes=int(counts.writes),
            uploads=int(counts.uploads),
            bytes=int(counts.bytes),
            run_closes=int(counts.run_closes),
            credentials=len(counts.credentials),
            by_enqueue_day=dict(days[: counts.reported_days]) or None,
            oldest_enqueue_day=days[-1][0] if days else None,
        )
        return True
    except Exception:
        return False  # observability must never become observable


def emit_outbox_restored(counts) -> bool:
    """Report the one-time restore of set-aside writes, from a `journal.RestoreCounts`: how many
    went back in the queue (and uploads), the enqueue days, what stayed aside by reason
    (`KeptAside`; ``bytes_gone`` on its own too), how many the login check set aside again and
    why (`NotAdoptable`), how many still wait and how many could not be moved. Counts only, never a fingerprint, key, body,
    name or path. Gated like every outbox event on the one server the writes were pinned to
    (hosted) and the person's switches. True when it was handed to the sender. Never raises."""
    try:
        context = detached_context(counts.base_url, via=Via.OUTBOX)
        if not context.enabled:
            return False
        days = sorted(counts.by_enqueue_day.items(), reverse=True)
        context.emit(
            EVENT_OUTBOX_RESTORED,
            writes=int(counts.writes),
            uploads=int(counts.uploads),
            bytes_gone=int(counts.bytes_gone),
            by_enqueue_day=dict(days[: counts.reported_days]) or None,
            kept={str(k): int(v) for k, v in counts.kept.items()} or None,
            refused=int(counts.refused),
            refused_reason=str(counts.refused_reason) if counts.refused_reason else None,
            deferred=int(counts.deferred),
            unmoved=int(counts.unmoved),
        )
        return True
    except Exception:
        return False  # observability must never become observable


#: What `emit_delivery_summary` may carry. Anything else is dropped at the door:
#: the event is counts only (plan 1.12).
DELIVERY_SUMMARY_FIELDS = frozenset(
    {
        "attempted",
        "dropped",
        "direct_sends",
        "dead_lettered",
        "dead_lettered_by_status",
        "discarded",
        "pending",
        "oldest_pending_s",
        "auth_blocked_s",
        "final",
        "interval_s",
    }
)


def emit_delivery_summary(*, base_url: str | None, flush: bool = False, **counts) -> None:
    """Report one training process's delivery counts. Never raises; gated on
    the telemetry opt-out and the caller's backend like every outbox event.
    ``flush``: send now (the caller is exiting and the sender's own exit flush
    may already have run); waits at most the sender's flush bound."""
    try:
        props = {key: value for key, value in counts.items() if key in DELIVERY_SUMMARY_FIELDS}
        context = detached_context(base_url, via=Via.OUTBOX)
        context.emit(EVENT_DELIVERY_SUMMARY, **props)
        if flush and context.enabled:
            sender._flush_at_exit()
    except Exception:
        pass  # observability must never become observable


def emit_outbox_stuck(
    status: dict, *, auth_blocked_since: str | None, spool_dir: str | None, base_url: str | None
) -> bool:
    """Report a stuck queue, at most once per :data:`STUCK_REPORT_INTERVAL_S`.

    Takes the banner's status dict (the every-command path allows one stat, no second
    read). ``auth_blocked_since``: the caller's `journal.auth_blocked_since(status)`;
    ``spool_dir``: its resolved queue dir. ORDER MATTERS: gates before the stamp, or
    `PROBE_TELEMETRY=off` burns the 6 h window; True only when sent. DESIGN.md (emit_outbox_stuck).
    """
    try:
        if not stuck_status(status, auth_blocked_since=auth_blocked_since):
            return False
        context = outbox_context(base_url)
        if not context.enabled:  # killswitch or self-host: report nothing, stamp nothing
            return False
        if not stuck_report_due(spool_dir):
            return False
        blocked_since = auth_blocked_since
        context.emit(
            EVENT_OUTBOX_STUCK,
            pending=status.get("pending") or 0,
            dead_lettered=status.get("failed") or 0,
            paused=bool(status.get("paused")),
            auth_blocked=bool(blocked_since),
            auth_blocked_age_hours=_age_hours(blocked_since),
            oldest_pending_age_hours=_age_hours(status.get("oldest_pending")),
            last_error_kind=_error_kind(status.get("last_error")),
            held=int(status.get("held") or 0),
            refused_credentials=len(status.get("refused_fingerprints") or {}),
        )
        return True
    except Exception:
        return False  # observability must never become observable


def emit_outbox_pause_lifted(status: dict, *, base_url: str | None) -> bool:
    """Report a pause that no longer held being lifted (its end passed, or an
    older CLI's endless one), with the writes it held (the outbox status read
    before the lift). Sent beside the command's own context, never as it
    (`detached_context`). Never raises; True when it was handed to the sender."""
    try:
        context = detached_context(base_url, via=Via.OUTBOX)
        if not context.enabled:
            return False
        context.emit(
            EVENT_OUTBOX_PAUSE_LIFTED,
            pending=status.get("pending") or 0,
            oldest_pending_age_hours=_age_hours(status.get("oldest_pending")),
        )
        return True
    except Exception:
        return False  # observability must never become observable


def emit_capture_repair_applied(
    *,
    sources: list[str],
    outcome: str,
    locks_lifted: int,
    base_url: str | None,
    kept_off: list[str] | None = None,
    confirmed: bool | None = None,
    unsupported: list[str] | None = None,
) -> bool:
    """Report a staff capture repair this machine applied (`EVENT_CAPTURE_REPAIR_APPLIED`):
    the agents written, those kept off by a turn-off made after staff asked, and
    whether the server took the confirmation. Slugs and counts only. Sent beside
    the command's own context, never as it (`detached_context`). Never raises;
    True when it was handed to the sender."""
    try:
        context = detached_context(base_url, via=Via.COMMAND)
        if not context.enabled:
            return False
        context.emit(
            EVENT_CAPTURE_REPAIR_APPLIED,
            sources=sorted(sources),
            outcome=outcome,
            locks_lifted=locks_lifted,
            kept_off=sorted(kept_off or []),
            unsupported=sorted(unsupported or []),
            confirmed=confirmed,
        )
        return True
    except Exception:
        return False  # observability must never become observable


def emit_settings_remote_applied(
    *,
    setting: str,
    value: str,
    default_changed: bool,
    sessions_moved: int,
    env_shadowed: bool,
    unsupported: bool,
    reported: bool,
    base_url: str | None,
) -> bool:
    """Report a staff settings change this machine applied (`EVENT_SETTINGS_REMOTE_APPLIED`).
    Sent beside the command's own context, never as it (`detached_context`). Never
    raises; True when it was handed to the sender."""
    try:
        context = detached_context(base_url, via=Via.COMMAND)
        if not context.enabled:
            return False
        context.emit(
            EVENT_SETTINGS_REMOTE_APPLIED,
            setting=setting,
            value=value,
            default_changed=default_changed,
            sessions_moved=sessions_moved,
            env_shadowed=env_shadowed,
            unsupported=unsupported,
            reported=reported,
        )
        return True
    except Exception:
        return False  # observability must never become observable
