"""THE SCHEDULER DUPLICATE GUARD — two schedules doing one job must not stay silent.

**The failure this exists to kill.** Measured on the live scheduler 2026-08-14:
"Human Baseline Schedule" existed TWICE in ``scheduler.sch_task`` — rows
``515dcc49-…`` and ``da07e6c6-…``, created 36 seconds apart by the same user,
byte-identical in every field that decides what runs (same Agent or Mandate, same
prompt, same queue, same trigger). Both were enabled. Both fired hourly for FIVE
DAYS. Every fire paid for an agent run whose twin had already produced the same
answer, and nothing anywhere said a word.

Nothing was broken, which is exactly why nobody caught it. Two healthy schedules
running perfectly is indistinguishable — in the ledger, in the logs, in the
run history — from one schedule running perfectly, unless something is
explicitly looking for the pair.

**Root cause.** The CREATE path had no notion of identity. A double-submit — a
UI double-click, or a retried ``create_scheduled_task`` MCP call whose first
attempt actually succeeded — inserted a second complete schedule, and an
always-on trigger turned that one accidental instant into open-ended recurring
cost.

**The rule — ONE identity, computed from what a schedule DOES.**

``task_fingerprint`` deliberately ignores ``title`` and ``description``. Two
schedules named "Morning Brief" and "Daily Summary" that run the SAME agent with
the SAME prompt on the SAME trigger cost exactly as much as two identically-named
ones; a fingerprint over the display name would have called those distinct and
missed the expensive half of the problem. What identifies a schedule is the work
it dispatches and when it dispatches it.

Verified against the whole live table before it shipped: across all 39 rows
(including soft-deleted ones) this fingerprint produced exactly ONE group — the
two rows above — and zero false positives. Notably it does NOT collapse the two
distinct schedules both titled "Weekly Marketing Recap", which a title-based
check would have wrongly flagged.

**Disabled triggers are excluded on purpose.** A schedule with no enabled
trigger cannot fire, so it costs nothing and is not a duplicate of anything.
Pausing one of a pair is therefore a real, immediately-effective resolution.

**No new table and no new column.** The fingerprint is DERIVED, computed on read
from rows the scheduler already writes. A stored fingerprint column would need a
backfill and would have to be kept in sync across three tables on every edit —
two ways to silently drift into a guard that no longer guards. At the observed
scale (32 schedules for the busiest user) computing it costs one bounded read.

**Package is capable, implementation chooses.** This module DETECTS and SCREAMS
using only the scheduler's own tables — it works in a standalone matrx-scheduler
deployment with nothing else installed. Handing the finding to a person on a
specific product surface is the host's decision, registered as the same optional
``escalation_sink`` ext THE SCHEDULER REPEAT GUARD uses; the sink dispatches on
the payload type it receives. There is ONE alarm path out of this package, not
two. Without a sink the guard still screams; it never goes quiet.

**What it refuses to decide.** It never picks a winner and never deletes. On the
create path the host may return the EXISTING schedule instead of inserting a
twin (see ``api.router_scheduler.create_task``) — that is refusing to create a
second thing, not destroying a first. Merging or disabling an existing pair is a
human's call, offered one-click on the surface, never taken by a guard.
"""

from __future__ import annotations

import hashlib
import json
import logging
from collections.abc import Iterable, Mapping, Sequence
from dataclasses import dataclass, field
from typing import Any

from ._ext import get_optional_ext

log = logging.getLogger("matrx_scheduler.duplicate_guard")

# CAPS constants — a code push to change, never env vars.
#
# The escalation source key; one grep finds every alarm this guard raised.
DUPLICATE_ESCALATION_SOURCE_KEY = "scheduler_duplicate_guard"
# Fields that identify a schedule by WHAT IT DOES. Documented as a constant so
# the answer to "does the title count?" lives in one greppable place: it does not.
FINGERPRINT_FIELDS = (
    "kind",
    "queue",
    "agent_id",
    "mandate_key",
    "prompt",
    "variables",
    "triggers",
)
# Length of the hex digest kept. 16 hex chars = 64 bits; at a few dozen
# schedules per user a collision is not a practical concern, and a short key
# stays readable in a log line and an assist dedupe key.
FINGERPRINT_LENGTH = 16


def _normalize(value: Any) -> Any:
    """Collapse the differences that do not change what a schedule does.

    Whitespace and case in a prompt, and key order in a JSON config, are not
    meaningful differences — a double-submit can produce either. Everything
    else is preserved exactly; this normalizes noise, it does not fuzzy-match.
    """
    if isinstance(value, Mapping):
        return {str(k): _normalize(value[k]) for k in sorted(value, key=str)}
    if isinstance(value, (list, tuple)):
        return [_normalize(v) for v in value]
    if isinstance(value, str):
        return " ".join(value.split()).strip().lower()
    return value


def task_fingerprint(
    *,
    kind: str | None,
    queue: str | None,
    agent_id: str | None = None,
    mandate_key: str | None = None,
    prompt: str | None = None,
    variables: Mapping[str, Any] | None = None,
    triggers: Iterable[Mapping[str, Any]] | None = None,
) -> str:
    """A stable fingerprint of WHAT a schedule does and WHEN it fires.

    Pure: no DB, no clock, no host. The same inputs always give the same key, in
    any process, which is what lets the create path, the fleet sweep, and the
    admin surface all agree on what "duplicate" means without sharing state.

    ``triggers`` should already be filtered to the ENABLED ones by the caller
    (see ``fingerprint_from_rows``) — a trigger that cannot fire is not part of
    what the schedule does.
    """
    trigger_keys = sorted(
        json.dumps(
            {"type": t.get("type"), "config": _normalize(t.get("config") or {})},
            sort_keys=True,
            default=str,
        )
        for t in (triggers or [])
    )
    payload = {
        "kind": _normalize(kind),
        "queue": _normalize(queue),
        "agent_id": str(agent_id) if agent_id else None,
        "mandate_key": str(mandate_key) if mandate_key else None,
        "prompt": _normalize(prompt),
        "variables": _normalize(dict(variables or {})),
        "triggers": trigger_keys,
    }
    encoded = json.dumps(payload, sort_keys=True, default=str).encode("utf-8")
    return hashlib.sha256(encoded).hexdigest()[:FINGERPRINT_LENGTH]


def can_fire(
    task: Mapping[str, Any],
    triggers: Sequence[Mapping[str, Any]] | None,
) -> bool:
    """Can this schedule actually run? Only a schedule that fires can duplicate one.

    The entire case against duplicates is cost: two schedules doing one job bill
    twice. A schedule that is paused, or that has no enabled trigger, bills
    nothing and is therefore not a duplicate of anything — flagging it would be
    a false positive, and blocking its creation would be a real bug in exchange
    for an imaginary one.

    This is also what makes the fix offered on the surface honest: pausing one of
    a pair genuinely resolves the duplication, because the paused one stops
    being able to fire.
    """
    if not task.get("enabled", True):
        return False
    return any(t.get("enabled", True) for t in (triggers or []))


def fingerprint_from_rows(
    task: Mapping[str, Any],
    agent_task: Mapping[str, Any] | None,
    triggers: Sequence[Mapping[str, Any]] | None,
) -> str:
    """Fingerprint a schedule that already exists, from its three rows.

    The counterpart of fingerprinting a create request: same key space, so a
    stored schedule and an inbound request are directly comparable.
    """
    return task_fingerprint(
        kind=task.get("kind"),
        queue=task.get("queue"),
        agent_id=(agent_task or {}).get("agent_id"),
        mandate_key=(agent_task or {}).get("mandate_key"),
        prompt=(agent_task or {}).get("prompt"),
        variables=(agent_task or {}).get("variables"),
        # Only triggers that can actually fire. A paused trigger costs nothing.
        triggers=[t for t in (triggers or []) if t.get("enabled", True)],
    )


@dataclass(frozen=True)
class DuplicateFinding:
    """A set of schedules that all do the same work on the same trigger.

    ``task_ids`` is ordered oldest-first, so ``task_ids[0]`` is the original and
    everything after it is redundant. The guard states that ordering as fact; it
    does not act on it.
    """

    fingerprint: str
    user_id: str
    task_ids: tuple[str, ...]
    titles: tuple[str, ...] = ()
    reason: str | None = None
    # Present when the finding came from the create path — the schedule that
    # already existed and that the caller was about to duplicate.
    existing_task_id: str | None = None
    evidence: dict[str, Any] = field(default_factory=dict)

    @property
    def redundant_count(self) -> int:
        """How many of these schedules are paying for work already being done."""
        return max(0, len(self.task_ids) - 1)


def group_duplicates(rows: Iterable[Mapping[str, Any]]) -> list[DuplicateFinding]:
    """Group already-loaded schedules into duplicate sets.

    Each row needs ``id``, ``user_id``, ``fingerprint``, and optionally
    ``title`` / ``created_at`` / ``can_fire``. Pure — the caller decides which
    rows are in scope (one user's, or the whole fleet) and how they were read,
    so the same grouping serves the per-user surface and the fleet sweep alike.

    Rows whose ``can_fire`` is False are skipped entirely (see ``can_fire``):
    a paused or trigger-less schedule costs nothing and duplicates nothing.

    Duplicates are only ever grouped WITHIN one user. Two people independently
    running the same public agent on the same cron is not a duplicate; it is two
    customers, and merging across that line would be a data-leak-shaped bug.
    """
    buckets: dict[tuple[str, str], list[Mapping[str, Any]]] = {}
    for row in rows:
        fp = str(row.get("fingerprint") or "")
        user_id = str(row.get("user_id") or "")
        if not fp or not user_id:
            continue
        if not row.get("can_fire", True):
            continue
        buckets.setdefault((user_id, fp), []).append(row)

    findings: list[DuplicateFinding] = []
    for (user_id, fp), group in buckets.items():
        if len(group) < 2:
            continue
        ordered = sorted(group, key=lambda r: (str(r.get("created_at") or ""), str(r.get("id"))))
        task_ids = tuple(str(r.get("id")) for r in ordered)
        titles = tuple(str(r.get("title") or "Untitled schedule") for r in ordered)
        findings.append(
            DuplicateFinding(
                fingerprint=fp,
                user_id=user_id,
                task_ids=task_ids,
                titles=titles,
                reason=(
                    f"{len(task_ids)} schedules run the same work on the same trigger: "
                    f"{', '.join(repr(t) for t in titles)}. The oldest ({task_ids[0]}) is "
                    f"the original; the other {len(task_ids) - 1} pay for work that is "
                    f"already being done."
                ),
                evidence={
                    "fingerprint": fp,
                    "task_ids": list(task_ids),
                    "titles": list(titles),
                    "redundant_count": len(task_ids) - 1,
                },
            )
        )
    return findings


async def note_duplicate(finding: DuplicateFinding) -> None:
    """Scream, then hand the finding to a person. Never raises, never blocks.

    Called both from the create path (when a twin was refused or forced through)
    and from the fleet sweep. Like THE SCHEDULER REPEAT GUARD, the alarm is
    never allowed to become a new way for work to fail: a sink that throws is
    logged and swallowed, because failing to NOTIFY about a duplicate must not
    also fail the create the user asked for.
    """
    try:
        # SCREAMING is the point. A guard that fires silently is the bug it replaced.
        log.error("[scheduler-duplicate-guard] %s", finding.reason or finding.fingerprint)

        sink = get_optional_ext("escalation_sink")
        if sink is None:
            log.error(
                "[scheduler-duplicate-guard] no escalation_sink is registered, so NOBODY "
                "has been told that schedules %s duplicate each other beyond this log "
                "line. Register one with matrx_scheduler.configure(escalation_sink=...).",
                ", ".join(finding.task_ids),
            )
            return
        await sink(finding)
    except Exception:  # noqa: BLE001 — the alarm is never allowed to break the caller
        log.exception(
            "[scheduler-duplicate-guard] failed while escalating duplicate schedules %s. "
            "The duplicates still exist; nobody has been told.",
            ", ".join(finding.task_ids),
        )
