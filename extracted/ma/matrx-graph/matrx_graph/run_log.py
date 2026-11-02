"""THE ONE ``workflow.run_log`` writer — every warning and diagnostic a run records.

Two callers, one writer (design DESIGN.md §7.1, owner ruling 2026-10-07):

* the authorable ``log.record`` node ("Record a Problem"), and
* ``NodeExecutionContext.warn`` — the engine's warnings channel, which any node
  (``ai.conversation.revise`` first) uses to say "this step worked, but it missed".

The row is the user's own diagnostic record (org-scoped, owner-readable), never
the platform's ``system_error`` queue. **Writing never fails a run**: a write
that cannot land returns ``recorded=False`` with the reason, loudly logged.

**The per-run cap is counted from durable rows**, never process memory: a
module-level counter restarts with the worker and differs between workers, so
"at most 200 entries per run" was really "per run per process". The cap reads
``workflow.run_log`` itself.

REVIEW FLAGS (0117, 2026-10-17): a row written with ``needs_review=True`` is a review
flag — "the run succeeded, but this should never have happened". The database groups it
into ONE ``workflow.review_issue`` per (workflow, step, connection, label), reopens an
issue marked fixed, and counts it on the run; the receipt's ``issue_event`` says whether
this occurrence was the issue's first (``new``), a return after a fix (``reopened``) or a
``repeat``. On ``new``/``reopened`` the host's review notifier (``configure_review_notifier``)
is told — the engine never imports a notification system.

Revision budgets read the same table: :func:`run_revision_turns` sums the
``revision_turns`` every ``response_check.*`` warning of a run recorded.
"""

from __future__ import annotations

import asyncio
import json
import logging
from collections.abc import Awaitable, Callable
from typing import Any

from pydantic import BaseModel, ConfigDict, Field, JsonValue

log = logging.getLogger(__name__)

#: Mirrors the ``run_log_severity_check`` CHECK constraint. Closed vocabulary.
SEVERITIES: tuple[str, ...] = ("debug", "info", "warning", "error", "critical")

#: One record is a diagnostic; ten thousand is an outage in the logger. A run
#: that reaches this is looping, and the cap makes that visible.
MAX_ENTRIES_PER_RUN = 200

#: Payloads are evidence, not archives — truncated with a marker past this.
MAX_PAYLOAD_CHARS = 100_000

#: Mirrors ``run_log_category_check`` — WHY a review flag was raised. Closed vocabulary.
CATEGORIES: tuple[str, ...] = (
    "recovered_error", "retry", "rework", "fallback", "validation_failed",
    "unexpected_path", "extra_cost", "degraded_output", "skipped_item",
    "human_handoff", "stall_recovery", "other",
)

#: Mirrors ``run_log_source_check`` — WHO raised it.
SOURCES: tuple[str, ...] = ("flagged_step", "flagged_path", "engine", "record_step", "step_code")

#: Labels that carry a ``revision_turns`` count in their payload (closed vocabulary).
REVISION_LABELS: tuple[str, ...] = (
    "response_check.revised",
    "response_check.off_target",
    "response_check.failed",
)


class RunLogEntry(BaseModel):
    """The receipt. Mirrored by the registered ``run_log_entry`` kind."""

    model_config = ConfigDict(extra="forbid")

    recorded: bool = Field(
        description=(
            "True when the record landed in the database. FALSE means the "
            "problem happened AND we failed to write it down — branch on this."
        )
    )
    entry_id: str | None = Field(default=None, description="The workflow.run_log row id.")
    label: str = ""
    severity: str = "warning"
    message: str = ""
    occurred_at: str | None = None
    #: Populated only when `recorded` is false — why the write did not land.
    not_recorded_reason: str | None = None
    needs_review: bool = Field(
        default=False, description="True when this record is a review flag on the workflow."
    )
    issue_id: str | None = Field(
        default=None, description="The workflow.review_issue this flag was grouped into."
    )
    issue_event: str | None = Field(
        default=None,
        description="new = first time this issue happened; reopened = it came back after "
        "being marked fixed; repeat = it happens again.",
    )


ReviewNotifier = Callable[["ReviewFlagNotice"], Awaitable[None]]


class ReviewFlagNotice(BaseModel):
    """What the host's notifier is told when an issue is new or came back."""

    model_config = ConfigDict(extra="forbid")

    run_id: str
    definition_id: str | None
    organization_id: str
    user_id: str | None
    issue_id: str
    issue_event: str
    node_id: str | None
    edge_id: str | None
    label: str
    message: str
    category: str
    severity: str


_review_notifier: ReviewNotifier | None = None


async def _notify_once(notice: ReviewFlagNotice) -> None:
    if _review_notifier is not None:
        await _review_notifier(notice)

#: A replacement for :func:`write_run_log`'s database path, called with the same keyword
#: arguments. The ONE test seam (an in-memory recorder) — a host never sets it.
RunLogWriter = Callable[..., Awaitable[RunLogEntry]]
_writer_override: RunLogWriter | None = None


def configure_run_log_writer(writer: RunLogWriter | None) -> None:
    """Swap the database path of :func:`write_run_log` (tests). ``None`` restores it."""
    global _writer_override
    _writer_override = writer


def configure_review_notifier(notifier: ReviewNotifier | None) -> None:
    """Host wiring: called once per new or reopened review issue. Never fails a write."""
    global _review_notifier
    _review_notifier = notifier


def _truncate(value: JsonValue) -> tuple[JsonValue, bool]:
    try:
        rendered = json.dumps(value, default=str)
    except Exception:  # noqa: BLE001 — evidence is never worth an exception
        return {"unserializable": repr(value)[:2000]}, True
    if len(rendered) <= MAX_PAYLOAD_CHARS:
        return value, False
    return {
        "truncated": True,
        "original_chars": len(rendered),
        "preview": rendered[:MAX_PAYLOAD_CHARS],
    }, True


async def run_log_count(run_id: str, *, needs_review: bool | None = None) -> int:
    """Durable count of this run's entries (optionally only flags / only non-flags).
    Raises on a read failure."""
    from matrx_graph.db._registry import get_model

    query = get_model("WfRunLog").filter(run_id=run_id)
    if needs_review is not None:
        query = query.filter(needs_review=needs_review)
    return int(await query.count())


async def run_revision_turns(run_id: str) -> int:
    """Revision turns this run has already paid for, summed from durable rows."""
    from matrx_graph.db._registry import get_model

    rows = await get_model("WfRunLog").filter(
        run_id=run_id, label__in=list(REVISION_LABELS)
    ).values("payload")
    total = 0
    for row in rows or []:
        payload = row.get("payload") or {}
        try:
            total += int(payload.get("revision_turns") or 0)
        except (TypeError, ValueError, AttributeError):
            continue
    return total


async def write_run_log(
    *,
    run_id: str,
    node_id: str,
    step: int,
    attempt: int,
    label: str,
    message: str = "",
    severity: str = "warning",
    payload: JsonValue = None,
    payload_kind: str | None = None,
    organization_id: str | None = None,
    user_id: str | None = None,
    needs_review: bool = False,
    category: str | None = None,
    source: str | None = None,
    edge_id: str | None = None,
    occurrence_key: str | None = None,
) -> RunLogEntry:
    """Write one row. Never raises; ``recorded`` says whether it landed.

    ``needs_review=True`` makes the row a review flag (see the module docstring);
    ``category``/``source`` are the closed vocabularies above (an unknown value
    becomes ``other`` / ``engine`` rather than failing the write).

    ``occurrence_key`` makes the write IDEMPOTENT across a crash/resume replay: it is
    stored in the payload, and a row of this run with the same node, label, step,
    attempt and key already present is returned instead of writing a second one.
    """
    if _writer_override is not None:
        try:
            return await _writer_override(
                run_id=run_id, node_id=node_id, step=step, attempt=attempt, label=label,
                message=message, severity=severity, payload=payload, payload_kind=payload_kind,
                organization_id=organization_id, user_id=user_id, needs_review=needs_review,
                category=category, source=source, edge_id=edge_id, occurrence_key=occurrence_key,
            )
        except Exception as exc:  # noqa: BLE001 — the recorder never fails the run
            return RunLogEntry(recorded=False, label=label or "", not_recorded_reason=str(exc)[:500])
    label = (label or "").strip() or "unlabelled_issue"
    severity = severity if severity in SEVERITIES else "warning"
    message = (message or "").strip() or label
    if needs_review:
        category = category if category in CATEGORIES else "other"
        source = source if source in SOURCES else "engine"
    else:
        category = category if category in CATEGORIES else None
        source = source if source in SOURCES else None

    def refused(reason: str) -> RunLogEntry:
        return RunLogEntry(
            recorded=False, label=label, severity=severity, message=message,
            not_recorded_reason=reason, needs_review=needs_review,
        )

    # Review flags and diagnostics keep SEPARATE budgets, so a chatty Record a Problem loop
    # can never silence the run's review flags (and vice versa). The flag budget is a knob.
    from matrx_graph.knobs import review_flag_policy

    policy = await review_flag_policy()
    cap = policy.max_flags_per_run if needs_review else MAX_ENTRIES_PER_RUN
    try:
        seen = await run_log_count(run_id, needs_review=needs_review)
    except Exception as exc:  # noqa: BLE001 — the recorder never fails the run
        log.exception("[wf:%s node=%s] run_log cap read failed for '%s'", run_id[:8], node_id, label)
        return refused(f"could not read this run's entry count: {type(exc).__name__}: {exc}"[:500])
    if seen >= cap:
        kind = "review flags" if needs_review else "entries"
        log.error(
            "[wf:%s] run_log holds %d %s — capping. The run is looping on '%s'.",
            run_id[:8], seen, kind, label,
        )
        return refused(f"this run already recorded {cap} {kind}")

    if occurrence_key:
        try:
            from matrx_graph.db._registry import get_model

            prior = await get_model("WfRunLog").filter(
                run_id=run_id, node_id=node_id, label=label, step=step, attempt=attempt
            ).values("id", "payload", "issue_id", "needs_review")
            for row in prior or []:
                if (row.get("payload") or {}).get("occurrence_key") == occurrence_key:
                    log.info(
                        "[wf:%s node=%s] run_log '%s' already recorded for this occurrence "
                        "(replay) — not writing it twice", run_id[:8], node_id, label,
                    )
                    return RunLogEntry(
                        recorded=True, entry_id=str(row.get("id") or "") or None, label=label,
                        severity=severity, message=message,
                        needs_review=bool(row.get("needs_review")),
                        issue_id=str(row.get("issue_id") or "") or None,
                    )
        except Exception:  # noqa: BLE001 — a failed dedupe read writes rather than loses
            log.warning("[wf:%s] run_log replay check failed for '%s'", run_id[:8], label, exc_info=True)
        if isinstance(payload, dict):
            payload = {**payload, "occurrence_key": occurrence_key}
        elif payload is None:
            payload = {"occurrence_key": occurrence_key}
        else:
            payload = {"value": payload, "occurrence_key": occurrence_key}

    stored, truncated = _truncate(payload)
    if truncated:
        message = f"{message} (evidence truncated)"

    try:
        from datetime import UTC, datetime

        from matrx_graph.db._registry import get_model

        # THE ORG IS THE RUN'S — the run row is the durable authority every
        # lane resolves against (queued workers never pass through a request).
        definition_id: str | None = None
        org: str | None = None
        run_rows = await get_model("WfRun").filter(id=run_id).values("definition_id", "organization_id")
        if run_rows:
            raw_def = run_rows[0].get("definition_id")
            definition_id = str(raw_def) if raw_def else None
            raw_org = run_rows[0].get("organization_id")
            org = str(raw_org) if raw_org else None
        org = org or organization_id
        if not org:
            log.error(
                "[wf:%s node=%s] PLATFORM DEFECT — run has NO organization, so '%s' "
                "cannot be recorded. Every workflow run belongs to an organization.",
                run_id[:8], node_id, label,
            )
            return refused(
                "PLATFORM DEFECT: this run carries no organization. Every workflow "
                "run belongs to one — refusing to let the database guess."
            )

        now = datetime.now(UTC)
        row: Any = await get_model("WfRunLog").create_item(
            run_id=run_id,
            definition_id=definition_id,
            node_id=node_id or None,  # a run-level record (stall recovery) names no step
            step=step,
            attempt=attempt,
            severity=severity,
            label=label,
            message=message,
            payload={"value": stored} if not isinstance(stored, dict) else stored,
            payload_kind=(payload_kind or "").strip() or None,
            occurred_at=now,
            organization_id=str(org),
            created_by=str(user_id) if user_id else None,
            needs_review=needs_review,
            category=category,
            source=source,
            edge_id=(edge_id or None),
        )
        entry_id = str(getattr(row, "id", "") or "") or None
        issue_id = str(getattr(row, "issue_id", "") or "") or None
        issue_event = (getattr(row, "metadata", None) or {}).get("issue_event") if needs_review else None
        log.warning(
            "[wf:%s node=%s] RUN LOG %s%s — %s: %s (entry %s%s)",
            run_id[:8], node_id, severity.upper(), " REVIEW FLAG" if needs_review else "",
            label, message[:300], entry_id, f", issue {issue_event}" if issue_event else "",
        )
        entry = RunLogEntry(
            recorded=True, entry_id=entry_id, label=label, severity=severity,
            message=message, occurred_at=now.isoformat(), needs_review=needs_review,
            issue_id=issue_id, issue_event=issue_event,
        )
        if needs_review and issue_id and issue_event in ("new", "reopened") and _review_notifier:
            try:
                # Bounded by a knob: the notice rides the step that raised the flag (only on a
                # new or returning issue), so a slow notification system delays it at most this.
                await asyncio.wait_for(_notify_once(
                    ReviewFlagNotice(
                        run_id=run_id, definition_id=definition_id, organization_id=str(org),
                        user_id=str(user_id) if user_id else None, issue_id=issue_id,
                        issue_event=issue_event, node_id=node_id or None, edge_id=edge_id or None,
                        label=label, message=message, category=category or "other",
                        severity=severity,
                    )
                ), timeout=policy.notify_timeout_ms / 1000.0)
            except Exception:  # noqa: BLE001 — telling someone never un-records the flag
                log.exception(
                    "[wf:%s] review notifier FAILED or timed out for issue %s (%s) — the flag is "
                    "recorded, the owner was NOT told", run_id[:8], issue_id, issue_event,
                )
        return entry
    except Exception as exc:  # noqa: BLE001 — the recorder never fails the run
        log.exception("[wf:%s node=%s] run_log could NOT write '%s'", run_id[:8], node_id, label)
        # Never fail the run, but never lose it quietly either: a flag that did not land is a
        # captured error (live 2026-10-28: a review issue owned by another organization refused
        # every later flag on a shared workflow, and only a log line said so).
        await _capture_not_recorded(exc, run_id=run_id, node_id=node_id, label=label,
                                    needs_review=needs_review, organization_id=organization_id)
        return refused(f"{type(exc).__name__}: {exc}"[:500])


NOT_RECORDED_ERROR_KIND = "workflow_run_log_not_recorded"


async def _capture_not_recorded(
    exc: BaseException, *, run_id: str, node_id: str, label: str, needs_review: bool, organization_id: str | None
) -> None:
    try:
        from matrx_utils import capture_error

        await capture_error(
            exc,
            kind=NOT_RECORDED_ERROR_KIND,
            error_type=NOT_RECORDED_ERROR_KIND,
            error_text=f"{'Review flag' if needs_review else 'Run log entry'} '{label}' was NOT recorded: "
                       f"{type(exc).__name__}: {exc}"[:2000],
            organization_id=organization_id,
            context={"run_id": run_id, "node_id": node_id, "label": label, "needs_review": needs_review},
        )
    except Exception:  # noqa: BLE001 — capture is best effort; the log line above already screamed
        log.exception("[wf:%s] could not capture the lost run_log write '%s'", run_id[:8], label)


__all__ = [
    "CATEGORIES",
    "MAX_ENTRIES_PER_RUN",
    "MAX_PAYLOAD_CHARS",
    "REVISION_LABELS",
    "SEVERITIES",
    "SOURCES",
    "ReviewFlagNotice",
    "ReviewNotifier",
    "RunLogEntry",
    "RunLogWriter",
    "configure_review_notifier",
    "configure_run_log_writer",
    "run_log_count",
    "run_revision_turns",
    "write_run_log",
]
