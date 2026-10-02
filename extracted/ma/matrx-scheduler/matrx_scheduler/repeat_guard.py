"""THE SCHEDULER REPEAT GUARD — a schedule that can never succeed must not stay silent.

**The failure this exists to kill.** A `sch_task` fires on its trigger forever.
When the task can never succeed, every fire writes one more `failed` `sch_run`
and nothing else happens: the ledger grows, the alarm is per-failure (so it is
indistinguishable from noise), and nobody is told. Measured 2026-08-14 on the
live scheduler: "Human Baseline Schedule" 103 failures, "Daily Standup Summary"
102, "SEO backlink enrichment dispatcher" 83, "SEO Analytics (GA4) sync
dispatcher" 4 of 4 — accumulated across FIVE DAYS and TWO separate repair
attempts without one escalation reaching a human.

**The rule — TWO ceilings, because there are two ways to never work.**

1. **Stuck one way** — the last ``MAX_CONSECUTIVE_FAILURES`` runs all failed with
   the *same* signature and no success between them. The classic broken schedule.
2. **Has never worked, ever** — the task has no successful run anywhere in its
   history and has now failed ``MAX_CONSECUTIVE_FAILURES`` times, *however* it
   failed.
3. **Stopped working** — ``MAX_CONSECUTIVE_ANY_CAUSE`` consecutive failures with
   no success between them, for a task that HAS succeeded before. A higher bar,
   because a task with a working history and a mixed bag of errors is weaker
   evidence per run than one that has never produced a result.

Ceilings 2 and 3 exist because ceiling 1 alone would have stayed silent on the
real case that prompted this. The GA4 dispatcher failed 4 of 4 runs and has
never once succeeded — but its error changed three times as partial repairs
landed ("3 site syncs failed" → a binding error → a Google API that is switched
off), so same-signature counting never reached three. "Never succeeded once" is
the strongest signal a schedule can send, and it is exactly the one that was
being thrown away: a task that fails a DIFFERENT way every single time is not
healthier than one stuck on a single cause; it is a task nobody has seen work.
It also matters that the ceiling is reached in RUNS, not days — GA4 fires daily,
so a count-only ceiling of eight would have meant eight more days of silence.

**Why "the same way" still matters for the tight ceiling.** A dispatcher that
processes many items fails intermittently on individual items and still does
real work — the SEO backlink dispatcher completes 20 enrichments per run and
fails on the two URLs a scraper cannot reach. That is a healthy task with
per-item noise, not a broken schedule, and escalating it at three would train
everyone to ignore the chip. Any success at all resets both counters to zero.

**No new table.** The attempt ledger already exists — ``scheduler.sch_run``
carries a terminal ``status`` and the failure's ``error_message``. The budget is
a read over rows the scheduler already writes, so there is nothing to keep in
sync and a restart forgets nothing.

**Package is capable, implementation chooses.** This module DETECTS and SCREAMS
using only the scheduler's own table — it works in a standalone matrx-scheduler
deployment with nothing else installed. Handing the give-up to a person on a
specific product surface (a ``platform.assists`` chip, an operator page, a page)
is the host's decision, registered as the optional ``escalation_sink`` ext.
Without a sink the guard still screams; it never goes quiet.

**It DOES stop the schedule — and says so.** Once a ceiling is reached the
guard disables the task and every enabled trigger (``_auto_suspend``), records
why on both rows under ``metadata.auto_suspended``, and hands the streak to the
host's ``escalation_sink``. Re-enabling is a deliberate human act after repair.
(An earlier version of this docstring claimed the guard never disabled anything
while the code below did exactly that; a doc that lies about a guard is worse
than no doc.)

**Work done is evidence, status is not.** A run row whose
``result_metadata.units_done`` is above zero COMMITTED work — a bounded
multi-pass job that classified 839 keywords and then hit a transient provider
blip on pass six is such a row, and on 2026-08-26 it was stamped ``failed``.
Counting that as "never succeeded once" and disabling an approved schedule on
it was this guard's own worst failure. A productive row now ends a streak
exactly as a success does, whatever its status says.

**An approval is overridden out loud, never silently.** A task whose metadata
carries a human approval (``approval`` / ``approved_by``) may still be
suspended — a broken schedule is broken — but the suspension record says, in
those words, that it is OVERRIDING that approval, preserves every approval
field untouched, and the streak handed to the sink carries the approval so the
human-facing chip can say it too. Re-enabling such a task RESTORES an existing
approval; it is not a new schedule and needs no new approval
(``common-docs/policies/no-unapproved-schedules.md``).
"""

from __future__ import annotations

import hashlib
import logging
import re
from dataclasses import dataclass, replace
from datetime import UTC, datetime

from ._ext import get_optional_ext, get_db_model

log = logging.getLogger("matrx_scheduler.repeat_guard")

# CAPS constants — a code push to change, never env vars.
#
# How many consecutive same-signature failures prove the schedule cannot work.
# Three is deliberate: one failure is noise, two can be a deploy, three is a
# pattern and every further fire is pure waste.
MAX_CONSECUTIVE_FAILURES = 3
# How many consecutive failures, regardless of cause, prove that a task which
# USED to work has stopped. Higher than the same-signature ceiling because a
# mixed bag of errors is weaker evidence per run.
MAX_CONSECUTIVE_ANY_CAUSE = 8
# The dedupe signature used when a cause-agnostic ceiling fires. Fixed on
# purpose: a task failing a NEW way every run must produce ONE chip, not one
# per run — which is the whole failure mode being escalated.
ANY_CAUSE_SIGNATURE = "never-succeeds"
# Rows inspected per check — newest first, so this only ever reaches back far
# enough to find the last success. Bounded so a task with thousands of failed
# runs (exactly the case this guard exists for) never scans them all.
LEDGER_SCAN_LIMIT = 25
# The escalation source key; one grep finds every alarm this guard raised.
REPEAT_ESCALATION_SOURCE_KEY = "scheduler_repeat_guard"

_TERMINAL_FAILED = frozenset({"failed", "cancelled", "abandoned", "expired"})
_TERMINAL_OK = frozenset({"success", "succeeded", "completed", "complete"})
# Terminal, but neither: the run's PROCESS went away and a continuation carries
# the fire (``continuation.py``). Skipped entirely, like an in-flight row.
_TERMINAL_RESUMABLE = frozenset({"interrupted"})
# The reserved result_metadata key the runner stamps from AgentRunResult.units_done.
# Imported by name rather than from .models so this module keeps its one
# dependency (the ledger rows) and stays runnable against a bare table.
_UNITS_DONE_KEY = "units_done"
# The sch_task.metadata keys that mean "a human approved this schedule".
_APPROVAL_KEYS = ("approval", "approved_by")


def units_done(row: dict) -> int:
    """Units of work a run row says it COMMITTED, or 0 when unmeasured.

    Reads the runner's reserved ``result_metadata.units_done``; anything else
    (missing key, non-dict metadata, garbage) is 0 — "unmeasured" must never
    read as "productive".
    """
    meta = row.get("result_metadata")
    if not isinstance(meta, dict):
        return 0
    try:
        return max(0, int(meta.get(_UNITS_DONE_KEY) or 0))
    except (TypeError, ValueError):
        return 0


def human_approval(task_metadata: dict | None) -> str | None:
    """The human approval a task carries, as one sentence, or None.

    A task with ``approval`` and/or ``approved_by`` in its metadata was
    approved by a person; suspending it is overriding that person.
    """
    if not isinstance(task_metadata, dict):
        return None
    parts = []
    text = task_metadata.get("approval")
    if text:
        parts.append(str(text))
    by = task_metadata.get("approved_by")
    at = task_metadata.get("approved_at")
    if by:
        parts.append(f"approved by {by}" + (f" on {at}" if at else ""))
    return "; ".join(parts) or None


# Volatile fragments that differ every run but do not change what BROKE. Two
# runs failing on different rows for the same reason share a signature.
_UUID_RE = re.compile(r"[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}", re.I)
_URL_RE = re.compile(r"https?://\S+")
_TS_RE = re.compile(r"\d{4}-\d{2}-\d{2}[ T]\d{2}:\d{2}:\d{2}(?:\.\d+)?(?:[+-]\d{2}:?\d{2}|Z)?")
_NUM_RE = re.compile(r"\b\d+\b")
_ANSI_RE = re.compile(r"\x1b\[[0-9;]*m")


def failure_signature(error_message: str | None) -> str:
    """A stable fingerprint of WHAT broke, ignoring which row it broke on.

    Two failures share a signature when they differ only in ids, URLs,
    timestamps, and counts — the things that change every run without changing
    the diagnosis. An empty/absent message still gets a signature so a task
    failing silently over and over is caught too.
    """
    text = _ANSI_RE.sub("", (error_message or "<no error message>"))
    text = _UUID_RE.sub("<id>", text)
    text = _URL_RE.sub("<url>", text)
    text = _TS_RE.sub("<ts>", text)
    text = _NUM_RE.sub("<n>", text)
    # Long batch messages repeat one class per item; the leading window is the
    # class, and hashing it keeps the key bounded regardless of batch size.
    normalized = " ".join(text.split())[:600]
    return hashlib.sha256(normalized.encode("utf-8")).hexdigest()[:16]


async def _has_ever_succeeded(task_id: str) -> bool:
    """Has this task produced a single successful run in its whole history?

    Fails SAFE (returns True, i.e. "assume it has worked") on a read error, so a
    broken lookup can never manufacture a "this has never worked" escalation.
    """
    SchRunModel = get_db_model("SchRun")
    try:
        rows = await (
            SchRunModel.filter(task_id=task_id, status__in=sorted(_TERMINAL_OK))
            .limit(1)
            .values("id")
        )
        return bool(rows)
    except Exception:  # noqa: BLE001 — never invent an escalation from a failed read
        log.exception(
            "[scheduler-repeat-guard] could not check whether sch_task %s has ever "
            "succeeded — assuming it has, so no never-worked alarm is raised.",
            task_id,
        )
        return True


async def _thresholds() -> tuple[int, int]:
    resolver = get_optional_ext("repeat_guard_thresholds")
    if resolver is None:
        return MAX_CONSECUTIVE_FAILURES, MAX_CONSECUTIVE_ANY_CAUSE
    same_way, any_cause = await resolver()
    same_way = int(same_way)
    any_cause = int(any_cause)
    if same_way < 1 or any_cause < same_way:
        raise ValueError("invalid scheduler repeat-guard thresholds")
    return same_way, any_cause


@dataclass(frozen=True)
class FailureStreak:
    """How many times in a row this task failed the same way."""

    task_id: str
    consecutive_failures: int
    signature: str
    sample_error: str
    escalate: bool
    reason: str | None = None
    #: The human approval the task carries, when it carries one. Set by
    #: ``note_failed_run`` before the streak reaches the sink, so the chip can
    #: say "this overrides an approval" in those words.
    approval: str | None = None
    #: Whether THIS call disabled the task. False when it was already disabled
    #: (a previous fire, or a human) — the sink still fires either way.
    suspended: bool = False


async def check_task_failure_streak(
    task_id: str, *, one_shot: bool = False
) -> FailureStreak | None:
    """Count consecutive same-signature failures back to the last success.

    ``one_shot`` — the failed run was a one-shot trigger's fire. A one-shot has
    exactly ONE attempt, so its first failure has exhausted every run it will
    ever make: the ceiling is 1. Without this the guard's ceilings (reached in
    RUNS) can never trip for a schedule that only ever gets one, and a failed
    one-time job is silent forever (live: "learn", 2026-09-16).

    Never raises: a ledger read that fails must not break the run that just
    finished, so an unreadable ledger is logged loudly and returns None. The
    guard exists to surface waste, not to become a new way for work to die.
    """
    SchRunModel = get_db_model("SchRun")
    try:
        rows = await (
            SchRunModel.filter(task_id=task_id)
            .order_by("-created_at")
            .limit(LEDGER_SCAN_LIMIT)
            .values("status", "error_message", "result_metadata")
        )
    except Exception:  # noqa: BLE001 — fail OPEN, loudly
        log.exception(
            "[scheduler-repeat-guard] could not read the run ledger for sch_task %s — "
            "the guard is blind for this task until this is fixed.",
            task_id,
        )
        return None

    same_way = 0  # consecutive failures sharing ONE signature
    any_cause = 0  # consecutive failures, however they failed
    signature: str | None = None
    sample_error = ""
    counting_same_way = True
    for row in rows:  # newest first — stop at the most recent success
        status = str(row.get("status") or "").lower()
        if status in _TERMINAL_RESUMABLE:
            # INTERRUPTED: the run's process went away and a continuation carries
            # the fire. A deploy is not evidence the schedule is broken, and not
            # evidence that it works — the continuation's own verdict decides.
            continue
        if status in _TERMINAL_OK:
            break
        if units_done(row) > 0:
            # WORK LANDED. Whatever the status column says, this run committed
            # real units — the schedule demonstrably works. It ends the streak
            # exactly as a success would; a guard that ignores it is the guard
            # that disabled an approved backfill after it classified 839
            # keywords (2026-08-26).
            break
        if status not in _TERMINAL_FAILED:
            continue  # claimed / running — not yet a verdict, skip it
        any_cause += 1
        sig = failure_signature(row.get("error_message"))
        if signature is None:
            signature = sig
            sample_error = str(row.get("error_message") or "")
        elif sig != signature:
            # The way it fails changed. That ends the same-signature streak, but
            # NOT the any-cause one — a schedule that fails differently every run
            # is still a schedule that has never worked.
            counting_same_way = False
        if counting_same_way:
            same_way += 1

    if signature is None:
        return None

    # "Has it EVER worked?" is the strongest signal available, and the scan
    # window alone cannot answer it — 25 failures in a row look identical
    # whether the last success was yesterday or never happened. One bounded
    # indexed read settles it, and only on a failure.
    saw_success_in_window = any(
        str(r.get("status") or "").lower() in _TERMINAL_OK or units_done(r) > 0 for r in rows
    )
    never_succeeded = False
    if not saw_success_in_window:
        never_succeeded = not await _has_ever_succeeded(task_id)

    if one_shot:
        reason = (
            "This is a one-time schedule and its only run failed, so it will not run "
            "again on its own. Fix the cause, then re-enable it to retry once. "
            f"Last error: {sample_error[:500]}"
        )
        return FailureStreak(
            task_id=task_id,
            consecutive_failures=any_cause,
            signature=signature,
            sample_error=sample_error,
            escalate=True,
            reason=reason,
        )

    same_way_limit, any_cause_limit = await _thresholds()
    stuck_one_way = same_way >= same_way_limit
    never_worked = never_succeeded and any_cause >= same_way_limit
    stopped_working = any_cause >= any_cause_limit
    if not stuck_one_way and not never_worked and not stopped_working:
        return FailureStreak(
            task_id=task_id,
            consecutive_failures=same_way,
            signature=signature,
            sample_error=sample_error,
            escalate=False,
        )

    if stuck_one_way:
        # The sentence lives ON the task row it describes (metadata.auto_suspended)
        # and is read beside the task's own title; naming the id here only put a
        # raw uuid in front of a person (Arman, 2026-09-14: "our platform rule is
        # that you're not allowed to display a UUID").
        reason = (
            f"This schedule has failed {same_way} times in a row the same way, with "
            f"no successful run in between. It is not going to fix itself — a human "
            f"has to decide why. Last error: {sample_error[:500]}"
        )
        return FailureStreak(
            task_id=task_id,
            consecutive_failures=same_way,
            signature=signature,
            sample_error=sample_error,
            escalate=True,
            reason=reason,
        )

    if never_worked:
        reason = (
            f"This schedule has failed {any_cause} times and has NEVER succeeded "
            f"once — the cause keeps changing, which is not progress. Nobody has "
            f"seen this schedule work. Last error: {sample_error[:500]}"
        )
    else:
        reason = (
            f"This schedule used to work and has now failed {any_cause} times in a "
            f"row with no success, failing a different way each time. "
            f"Last error: {sample_error[:500]}"
        )
    return FailureStreak(
        task_id=task_id,
        consecutive_failures=any_cause,
        signature=ANY_CAUSE_SIGNATURE,
        sample_error=sample_error,
        escalate=True,
        reason=reason,
    )


async def note_failed_run(run_id: str, task_id: str | None = None) -> None:
    """Called once per FAILED terminal write. Never raises, never blocks.

    This is the whole public surface: the scheduler finalizes a failed run and
    tells the guard. Everything else — reading the streak, screaming, handing
    it to a person — happens here.
    """
    try:
        if task_id is None:
            SchRunModel = get_db_model("SchRun")
            rows = await SchRunModel.filter(id=run_id).limit(1).values("task_id")
            if not rows:
                return
            task_id = str(rows[0].get("task_id") or "")
            if not task_id:
                return

        streak = await check_task_failure_streak(
            task_id, one_shot=await _fired_by_one_shot(run_id)
        )
        if streak is None or not streak.escalate:
            return
        await escalate_streak(streak, run_id)
    except Exception:  # noqa: BLE001 — the alarm is never allowed to break the run
        log.exception(
            "[scheduler-repeat-guard] failed while checking sch_task %s (run %s). "
            "The run itself is unaffected; the guard is blind for this failure.",
            task_id,
            run_id,
        )


async def _fired_by_one_shot(run_id: str) -> bool:
    """Was this run a one-shot trigger's fire? A manual "Run now" (no trigger)
    is not. Fails to False on a read error: the ordinary ceilings still apply."""
    try:
        SchRunModel = get_db_model("SchRun")
        rows = await SchRunModel.filter(id=run_id).limit(1).values("trigger_id")
        trigger_id = str((rows[0].get("trigger_id") if rows else None) or "")
        if not trigger_id:
            return False
        SchTriggerModel = get_db_model("SchTrigger")
        trows = await SchTriggerModel.filter(id=trigger_id).limit(1).values("type")
        return bool(trows) and trows[0].get("type") == "one-shot"
    except Exception:  # noqa: BLE001
        log.exception(
            "[scheduler-repeat-guard] could not read the trigger of run %s; judging it "
            "as a recurring schedule.",
            run_id,
        )
        return False


async def suspend_schedule_now(
    task_id: str, run_id: str, *, error_message: str, reason: str
) -> None:
    """Pause a schedule the SCHEDULER has decided cannot run, out loud.

    For causes that need no streak to prove — an agent schedule with no agent
    or Mandate can never succeed, so the runner pauses it on its first fire.
    Until 2026-09-28 that pause was a bare ``enabled=false``: no
    ``metadata.auto_suspended`` (so the attention dock's ``suspended`` alarm
    never listed it) and no escalation sink (so the owner was never told).
    This is the same suspension + escalation the ceilings use. The signature is
    the error's, so the one-shot ceiling that sees the same failed run a moment
    later dedupes onto the same owner chip.

    Raises if the suspension write fails — the pause itself must not be lost;
    the escalation half never raises.
    """
    streak = FailureStreak(
        task_id=task_id,
        consecutive_failures=1,
        signature=failure_signature(error_message),
        sample_error=error_message,
        escalate=True,
        reason=reason,
    )
    await escalate_streak(streak, run_id, suspension_must_land=True)


async def escalate_streak(
    streak: FailureStreak, run_id: str, *, suspension_must_land: bool = False
) -> None:
    """Suspend the task (recorded) and hand the streak to the host sink."""
    task_id = streak.task_id
    try:
        # SCREAMING is the point. A guard that fires silently is the bug it replaced.
        log.error("[scheduler-repeat-guard] %s", streak.reason)

        try:
            suspended, approval = await _auto_suspend(streak, run_id)
        except Exception:
            if suspension_must_land:
                raise
            log.exception(
                "[scheduler-repeat-guard] could not suspend sch_task %s; escalating anyway.",
                task_id,
            )
            suspended, approval = False, None
        if approval:
            log.error(
                "[scheduler-repeat-guard] sch_task %s carries a HUMAN APPROVAL (%s) and "
                "the guard is OVERRIDING it by suspending the schedule. Re-enabling "
                "after repair restores that approval; it is not a new schedule.",
                task_id,
                approval,
            )
        streak = replace(streak, approval=approval, suspended=suspended)

        # The sink fires whether or not THIS call won the disable race. Gating
        # it on the suspension meant a task that was already disabled — by an
        # earlier fire, or by a person — could never raise its chip, and a
        # refused or lost suspension went silent. The host sink dedupes.
        sink = get_optional_ext("escalation_sink")
        if sink is None:
            log.error(
                "[scheduler-repeat-guard] no escalation_sink is registered, so NOBODY "
                "has been told about sch_task %s beyond this log line. Register one "
                "with matrx_scheduler.configure(escalation_sink=...).",
                task_id,
            )
            return
        try:
            await sink(streak)
        except Exception:  # noqa: BLE001 — the sink is a notification, never the work
            log.exception(
                "[scheduler-repeat-guard] the escalation sink failed for sch_task %s "
                "(run %s). It is suspended and recorded; its owner may not have been told.",
                task_id,
                run_id,
            )
    except Exception:  # noqa: BLE001 — the alarm is never allowed to break the run
        if suspension_must_land:
            raise
        log.exception(
            "[scheduler-repeat-guard] failed while escalating sch_task %s (run %s). "
            "The run itself is unaffected; nobody may have been told.",
            task_id,
            run_id,
        )


async def _auto_suspend(streak: FailureStreak, run_id: str) -> tuple[bool, str | None]:
    """Disable a repeatedly failing task once, then disable all its triggers.

    Returns ``(suspended_by_this_call, human_approval_or_None)``.

    The conditional task update is the race-safe winner election. The task is
    the firing gate, so even if trigger cleanup has to be retried, no new run
    can be claimed. Metadata preserves the reversible reason and evidence —
    and, when the task carries a human approval, says IN THOSE WORDS that the
    guard is overriding it, leaving every approval field exactly as it was. A
    previous ``auto_suspended`` block is moved to ``auto_suspended_history``,
    never overwritten: a second suspension of the same task is itself evidence.
    """
    SchTaskModel = get_db_model("SchTask")
    SchTriggerModel = get_db_model("SchTrigger")
    task_rows = await SchTaskModel.filter(id=streak.task_id).limit(1).values("enabled", "metadata")
    if not task_rows:
        return False, None
    task = task_rows[0]
    task_metadata = dict(task.get("metadata") or {})
    approval = human_approval(task_metadata)
    now = datetime.now(UTC).isoformat()
    reason = {
        "source": REPEAT_ESCALATION_SOURCE_KEY,
        "at": now,
        "run_id": run_id,
        "failure_signature": streak.signature,
        "consecutive_failures": streak.consecutive_failures,
        "reason": (streak.reason or "")[:2000],
    }
    if approval:
        reason["overriding_approval"] = approval
        reason["override_notice"] = (
            "This schedule carries a HUMAN APPROVAL and the repeat guard is OVERRIDING "
            "it. The approval fields on this row are untouched. Fix the cause, then "
            "re-enable: that RESTORES the existing approval and is not a new schedule."
        )
    if not task.get("enabled"):
        # Already off (an earlier fire, or a person). Nothing to disable; the
        # caller still escalates so a suspension is never silent twice.
        return False, approval

    previous = task_metadata.get("auto_suspended")
    if isinstance(previous, dict):
        history = list(task_metadata.get("auto_suspended_history") or [])
        history.append(previous)
        task_metadata["auto_suspended_history"] = history
    task_metadata["auto_suspended"] = reason
    winner = await SchTaskModel.update_where(
        {"id": streak.task_id, "enabled": True},
        enabled=False,
        metadata=task_metadata,
    )

    triggers = await SchTriggerModel.filter(task_id=streak.task_id, enabled=True).values(
        "id", "metadata"
    )
    for trigger in triggers:
        trigger_metadata = dict(trigger.get("metadata") or {})
        previous_t = trigger_metadata.get("auto_suspended")
        if isinstance(previous_t, dict):
            history_t = list(trigger_metadata.get("auto_suspended_history") or [])
            history_t.append(previous_t)
            trigger_metadata["auto_suspended_history"] = history_t
        trigger_metadata["auto_suspended"] = reason
        await SchTriggerModel.update_where(
            {"id": trigger["id"], "enabled": True},
            enabled=False,
            metadata=trigger_metadata,
        )
    return bool(winner.updated_rows), approval
