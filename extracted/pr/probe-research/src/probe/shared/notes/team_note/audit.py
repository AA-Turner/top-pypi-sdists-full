"""the note's audit: health measured at render, when it is due (size or age), the advisory line, and the one-session dispatch lease."""

from __future__ import annotations

import hashlib
import datetime as _dt
import json
import math
import os
import re
import time
from dataclasses import dataclass
from pathlib import Path
from probe.foundation.durable.durable import SYNC_NONE, file_lock, write_text_atomic
from probe.shared.updates.version_policy import state_dir


#: Where the last render's size health waits for the session-start audit
#: trigger. The pointer-vs-full decision is made HERE, against the real
#: instruction budget — a hook cannot know that constant without growing a
#: drifting mirror of it, so the render writes what it measured and the hook
#: only reads. Advisory: a missing or stale file just means the size half of
#: the trigger stays quiet.
HEALTH_FILE = "health.json"


def note_health_path() -> Path:
    return state_dir() / "team-note" / HEALTH_FILE


#: The audit stamp, in the ONE shape the skill documents and the trigger hook
#: parses. Three surfaces carry this literal and
#: `tests/test_notes_audit_trigger.py` pins them together — reword one without
#: the others and the churn guard silently stops recognising an audit.
AUDIT_STAMP_RE = re.compile(r"<!--\s*audited\s+(\d{4}-\d{2}-\d{2})\s*-->", re.IGNORECASE)


def _audit_baseline(document: str, previous: dict[str, object] | None) -> dict[str, object]:
    """The post-audit fingerprint the trigger compares against.

    WHY THE STAMP GATES THE HASH. The question the churn guard answers is "has
    anyone written since the last AUDIT", and this runs at every render — so a
    hash refreshed on every render would answer "since the last render" instead,
    which is nearly always "no" and would suppress tightening forever. The hash
    therefore moves only when the STAMP moves: a new stamp means an audit just
    finished, so the document as it stands now IS that audit's result. Every
    later render leaves it alone, and an append between audits shows up as a
    mismatch, which is exactly the signal.

    THE FIRST SIGHTING RECORDS NO HASH, and that is the whole safety of this.
    On the first render after this ships every machine has no `audit` key, and
    hashing the document THEN would file weeks of un-audited appends under the
    old stamp as "what the last audit produced" -- so the very next audit would
    be told to skip its tightening. A hash is only ever written when a stamp
    CHANGE is observed, because that is the only evidence available here that an
    audit actually ran.

    A note with no stamp records none: there is no audit to be unchanged since.

    HASHED OVER THE STRIPPED DOCUMENT, matching `render_blocks`, which strips
    before it renders. The hook must strip too or the two hash different bytes
    and the guard never fires -- and it would never fire LOUDLY, it would just
    silently tighten every cycle forever.
    """
    match = AUDIT_STAMP_RE.search(document)
    if match is None:
        return {}
    stamp = match.group(1)
    if not previous or not previous.get("stamp"):
        return {"stamp": stamp}
    if previous.get("stamp") == stamp:
        return dict(previous)
    digest = hashlib.sha256(document.strip().encode("utf-8")).hexdigest()
    return {"stamp": stamp, "content_sha256": digest}


#: The deletion kill switch, read here rather than in a hook: this module already
#: owns the stamp, the health file and the budget, so the knob lives beside the
#: numbers it acts on instead of in a second process that has to mirror it.
#:
#: DAYS-SHAPED BUT READ AS A SWITCH: anything above zero means the auditor may
#: delete. It is NOT the cadence -- that is `AUDIT_INTERVAL_DAYS` below, and the
#: two sevens beside each other mean different things.
AUDIT_HORIZON_DAYS = 7

#: Fires the size half when the LAST render measured the block at or above this
#: fraction of the room its instruction file had.
AUDIT_SIZE_PCT = 0.8

#: Fires the TRUTH half when nobody has audited the note in this many days,
#: whatever its size. 0 disables the calendar.
#:
#: A calendar is still the wrong shape for TIGHTENING and is not used for it: a
#: date says nothing about whether a document is too long, and compacting a note
#: nobody is struggling to read spends a background agent for nothing. What it
#: buys is the half the on-read prong was never closing -- "has anyone checked
#: this is still TRUE?" -- because a reader only corrects a claim they happen to
#: hold the evidence against, and the quiet claims are the ones nobody tests.
AUDIT_INTERVAL_DAYS = 7

#: What Claude Code reports when a person is at the keyboard. Everything else it
#: reports -- `sdk-cli` for `claude -p`, the language SDKs, `mcp` -- is a program
#: driving the session.
INTERACTIVE_ENTRYPOINTS = frozenset(
    {"cli", "vscode", "vscode-insiders", "cursor", "windsurf"}
)


def session_is_automated(env: "dict | None" = None) -> bool:
    """Is this session being driven by a program rather than a person?

    A DENY-LIST, deliberately. The hook that asks this only fires when a prompt
    is submitted, so presence is already most of the way proven; this filters the
    two known automated submitters and lets an unrecognised harness through. An
    allow-list would silently disable the audit on every harness we have not met
    yet, and silence is the failure mode nobody notices.

    Measured on this box: `codex exec` sets `CODEX_CI=1`, `claude -p` reports
    `CLAUDE_CODE_ENTRYPOINT=sdk-cli`, an interactive Claude Code session reports
    `cli`.
    """
    env = os.environ if env is None else env
    if str(env.get("CODEX_CI", "")).strip().lower() not in ("", "0", "false"):
        return True
    entrypoint = str(env.get("CLAUDE_CODE_ENTRYPOINT", "")).strip().lower()
    if entrypoint:
        return entrypoint not in INTERACTIVE_ENTRYPOINTS
    return False


def _audit_env(name: str, default: int, floor: int) -> int:
    raw = os.environ.get(name, "")
    try:
        value = int(raw)
    except ValueError:
        return default
    return value if value >= floor else default


def _stamp_age_days(document: str, today) -> "int | None":
    """Days since the audit stamp, or None when there is no usable stamp.

    None means "never audited" and is DUE: absent, malformed and future-dated
    stamps all land here, so a corrupted stamp buys an audit (which rewrites it)
    rather than suppressing audits until someone notices.
    """
    match = AUDIT_STAMP_RE.search(document)
    if match is None:
        return None
    try:
        stamped = _dt.date.fromisoformat(match.group(1))
    except ValueError:
        return None
    age = (today - stamped).days
    return age if age >= 0 else None


def _untouched_since_audit(document: str, baseline: "dict | None") -> bool:
    """Has NOBODY written since the audit that produced this text?

    Gates TIGHTENING only, never the truth pass: a document nobody has edited
    can still have gone stale, because the world moves underneath it. Any
    missing or unparseable half answers False -- the guard may only ever
    suppress work it is CERTAIN is redundant.
    """
    if not isinstance(baseline, dict):
        return False
    recorded, stamp = baseline.get("content_sha256"), baseline.get("stamp")
    if not isinstance(recorded, str) or not isinstance(stamp, str):
        return False
    match = AUDIT_STAMP_RE.search(document)
    if match is None or match.group(1) != stamp:
        return False
    return hashlib.sha256(document.strip().encode("utf-8")).hexdigest() == recorded


@dataclass(frozen=True)
class AuditDue:
    """Why the note is due its audit, in the words both dispatches use: the
    prompt hook's line (`audit_advisory`, for an agent that starts the audit
    itself) and the daemon's (`AuditDue.brief`, daemon-team-note-audit)."""

    headline: str
    reasons: str
    removal: str
    job: str

    def brief(self) -> str:
        return f"> **{self.headline}** ({self.reasons}). {self.removal} {self.job}"


def audit_due(document: str, *, pct: "float | None", baseline: "dict | None", today=None) -> "AuditDue | None":
    """Is the note due its audit, and which half? None when it is not."""
    today = today or _dt.date.today()
    horizon = _audit_env("PROBE_NOTES_AUDIT_HORIZON_DAYS", AUDIT_HORIZON_DAYS, 0)
    age = _stamp_age_days(document, today)
    interval = _audit_env("PROBE_NOTES_AUDIT_INTERVAL_DAYS", AUDIT_INTERVAL_DAYS, 0)
    # TWO TRIGGERS, AND THE SENTENCE SAYS WHICH ONE. Size fires the TIGHTENING
    # half: the block is about to stop arriving at all, and only cutting bytes
    # fixes that. The interval fires the TRUTH half: a small note is otherwise
    # re-checked by nothing, because the on-read prong corrects only the claims
    # a reader happens to hold evidence against. They are not interchangeable --
    # tightening a note that is inside its budget is busywork, so the overdue
    # dispatch says not to. No SECTION NUMBERS in either sentence: the skills
    # renumber, and a stale pointer sends the auditor to the wrong rules.
    oversized = pct is not None and pct >= AUDIT_SIZE_PCT
    overdue = interval > 0 and (age is None or age >= interval)
    if not oversized and not overdue:
        return None
    # A 24-hour floor: a note stamped TODAY is not asked again, however large.
    # It caps the rate at one audit per day rather than one per session.
    if age is not None and age < 1:
        return None
    # An unchanged document cannot have GROWN since the last pass, so a second
    # tightening has nothing to find. It gates SIZE only: the world moves under
    # a document nobody has touched, which is the whole point of the interval.
    if oversized and not overdue and _untouched_since_audit(document, baseline):
        return None
    removal = (
        "Delete what the evidence disproves."
        if horizon > 0
        else "Deletion is DISABLED: correct claims in place, delete nothing."
    )
    if oversized:
        return AuditDue("This note has outgrown its budget", f"at {round(pct * 100)}% of its render budget",
                        removal, "Tighten what stays.")
    return AuditDue(
        "This note is due its periodic re-check",
        "never audited" if age is None else f"{age} days since the last audit",
        removal,
        "Do NOT tighten it -- it is inside its budget, and this pass is about what is still TRUE.",
    )


def audit_advisory(
    document: str, *, source: str, pct: "float | None", baseline: "dict | None", today=None
) -> str:
    """The line the block carries when the team note is due for its audit.

    THIS REPLACED A SESSIONSTART HOOK, and the move is the point. A hook was the
    only way a TIMER could reach the model, because the render runs detached
    with its output discarded -- but a timer on the context channel is the wrong
    shape: it spends the session's context to say something about a document
    that is already in that context. Written into the block instead, the
    reminder rides the note it is about, and the per-source loop gives each
    harness its own correct dispatch with no environment sniffing.

    The SIZE half reads the LAST render's measurement, not this one's: this
    string is about to change the length it would be measuring.
    """
    due = audit_due(document, pct=pct, baseline=baseline, today=today)
    if due is None:
        return ""
    from probe.shared.harness.harness import get_integration

    integration = get_integration(source)
    dispatch = (
        "Run the `audit-team-note` skill (`notes-audit` on plugins before 0.90.0) YOURSELF now, before taking up the user's work "
        "-- this sandbox reaps detached processes, and it is one small file."
        if integration is not None and integration.should_audit_inline
        else "Run the `audit-team-note` skill (`notes-audit` on plugins before 0.90.0) in a BACKGROUND subagent and carry on with "
        "the user's work -- never inline."
    )
    return (
        f"> **{due.headline}** ({due.reasons}). "
        f"{dispatch} {due.removal} {due.job} "
        "If research tracking is off for this session, skip it."
    )


def _local_note_state(source: str, *, settings) -> "tuple[str, float | None, dict | None] | None":
    """This machine's note, and the last render's size and audit baseline for
    `source`, off disk. None when the note is unreadable or empty, or hidden by
    this computer's workspace limit (no audit of a note the machine does not show)."""
    if hidden_by_limit(settings):
        return None
    try:
        document = paths_for(settings).document.read_text(encoding="utf-8").strip()
    except OSError:
        return None
    if not document:
        return None
    try:
        health = json.loads(note_health_path().read_text(encoding="utf-8"))
    except (OSError, ValueError):
        health = {}
    sources = health.get("sources") if isinstance(health, dict) else None
    entry = sources.get(source) if isinstance(sources, dict) else None
    pct = entry.get("pct") if isinstance(entry, dict) else None
    baseline = health.get("audit") if isinstance(health, dict) else None
    return (document, pct if isinstance(pct, (int, float)) else None,
            baseline if isinstance(baseline, dict) else None)


def advisory_for_source(source: str, *, settings, today=None) -> str:
    """The audit line for THIS machine's note, from local state only.

    NO NETWORK AND NO RENDER. The caller is a prompt-submit hook with a few
    seconds of budget, so this reads the document and the last render's
    measurements off disk and asks the same `audit_advisory` the render used to
    ask. Anything unreadable answers "" -- a missing health file means no
    measurement, which is not an audit trigger.
    """
    state = _local_note_state(source, settings=settings)
    if state is None:
        return ""
    document, pct, baseline = state
    return audit_advisory(document, source=source, pct=pct, baseline=baseline, today=today)


def audit_due_for_source(source: str, *, settings, today=None) -> "AuditDue | None":
    """`audit_due` for THIS machine's note, from local state only (the daemon's
    audit pulls the team's copy first, then asks this)."""
    state = _local_note_state(source, settings=settings)
    if state is None:
        return None
    document, pct, baseline = state
    return audit_due(document, pct=pct, baseline=baseline, today=today)


#: How long one session's dispatch holds this machine's audit. The advisory is
#: per SESSION and the stamp that silences it is written by the auditor, so every
#: session that submitted a prompt between the dispatch and that write was told
#: to spawn its own auditor: N sessions on one box, N subagents rewriting one
#: file. The lease closes that window. It only has to outlive "subagent starts,
#: stamps the note", which the skill does first; after that the stamp's same-day
#: floor keeps everyone quiet. Its expiry is the recovery path for a claim nobody
#: acted on (session closed, line ignored, subagent died): each such claim holds
#: the audit for this long, and the next prompt after it takes over.
AUDIT_LEASE_SECONDS = 2 * 60 * 60

#: The session the prompt hook is asking for. Set by `note_audit.py` in the
#: environment rather than as a flag, so a new hook calling an older CLI is not
#: refused an option it has never heard of.
AUDIT_SESSION_ENV = "PROBE_NOTE_AUDIT_SESSION"


def audit_lease_path() -> Path:
    return state_dir() / "team-note" / "audit-lease.json"


#: A real lease is under 100 bytes. Anything longer is corrupt, and reading it
#: whole could hand the JSON decoder a nesting deep enough to raise
#: RecursionError on every prompt -- a lease no expiry ever clears.
_LEASE_MAX_BYTES = 4096


def _read_lease(lease: Path) -> dict:
    """The lease as a dict, or {} for anything that is not a small JSON object.

    Not a regular file (a FIFO would block every prompt's hook until its
    timeout), too long, or undecodable: all corrupt, all free.
    """
    try:
        if not lease.is_file():
            return {}
        with lease.open("rb") as handle:
            raw = handle.read(_LEASE_MAX_BYTES + 1)
        if len(raw) > _LEASE_MAX_BYTES:
            return {}
        held = json.loads(raw)
    except (OSError, ValueError, RecursionError):
        return {}
    return held if isinstance(held, dict) else {}


def _lease_time(raw: object) -> "float | None":
    """A lease's `claimed_at` as a finite number, or None. A 400-digit integer
    overflows the float arithmetic below and NaN compares false both ways;
    either would otherwise pin the lease or crash the hook's CLI call."""
    if isinstance(raw, bool):
        return None
    try:
        value = float(raw)
    except (TypeError, ValueError, OverflowError):
        return None
    return value if math.isfinite(value) else None


def claim_audit_dispatch(*, holder: "str | None" = None, now: "float | None" = None) -> bool:
    """Take this machine's audit, or learn another session already has it.

    Under a lock: two sessions whose prompts land together both read "free" and
    both claim otherwise.

    THE HOLDER MAY ASK AGAIN. The lease is written before the line reaches the
    model, so a hook killed by its timeout, or output the harness dropped, would
    otherwise leave the claiming session as silent as everyone else for the
    whole lease. Its hook did not mark it as told, so it asks on its next prompt
    and gets the line back -- and the lease RENEWS, because that telling is the
    one its auditor starts from; a re-telling a second before expiry must not
    let another session dispatch a second later. A claim with no holder (an
    older hook, a person at a terminal) cannot be re-asked; it just expires.

    A lease timestamped up to one lease-length AHEAD still counts: on one
    machine that is a clock stepped backwards, and reading it as free let a
    second session dispatch. Further ahead than that, or unreadable, it is
    corrupt and free. A lease that cannot be recorded answers True -- a
    duplicate audit costs tokens, a silenced one lets the note rot unnoticed.
    """
    now = time.time() if now is None else now
    lease = audit_lease_path()
    try:
        with file_lock(lease.parent / "locks" / "audit-lease.lock"):
            held = _read_lease(lease)
            claimed_at = _lease_time(held.get("claimed_at"))
            live = claimed_at is not None and abs(now - claimed_at) < AUDIT_LEASE_SECONDS
            if live and not (holder and held.get("holder") == holder):
                return False
            # NO FSYNC. The rename alone keeps readers off a torn file, a lease
            # lost to a crash only costs a duplicate audit, and every fsync here
            # is spent holding a lock the other sessions' prompts are queued on.
            write_text_atomic(
                lease, json.dumps({"claimed_at": now, "holder": holder}) + "\n", sync=SYNC_NONE
            )
    except OSError:
        return True
    return True


def _record_health(entries: dict[str, dict[str, object]], document: str = "") -> None:
    """Persist what the render measured, for the audit trigger to read."""
    if not entries:
        return
    path = note_health_path()
    try:
        previous = json.loads(path.read_text(encoding="utf-8")).get("audit")
    except (OSError, ValueError, AttributeError):
        previous = None
    payload: dict[str, object] = {"sources": entries}
    baseline = _audit_baseline(document, previous if isinstance(previous, dict) else None)
    if baseline:
        payload["audit"] = baseline
    try:
        path.parent.mkdir(parents=True, exist_ok=True)
        write_text_atomic(path, json.dumps(payload, indent=2) + "\n")
    except OSError:
        # Health is advisory; failing to record it must not fail the render.
        pass
from probe.shared.notes.team_note.render import hidden_by_limit  # noqa: E402 -- pieces need each other; the front door loads this one first
from probe.shared.notes.team_note.team_note import paths_for  # noqa: E402 -- pieces need each other; the front door loads this one first
