"""post a hint to the session's mailbox, take hints back, and judge from the files whether hints reach the agent."""

from __future__ import annotations
import json
import os
import time
from pathlib import Path
from probe.service.hints.request import TIMEOUT_S
LEDGER_TAIL_BYTES = 256 * 1024
CLAIM_LOG_TAIL_BYTES = 256 * 1024


class DeliveryState:
    """Whether the hints posted to a session reach its agent (`delivery_receipt`)."""

    OK = "ok"  # a deliverer is there (its heartbeat), or a hint was shown lately
    UNPROVEN = "unproven"  # neither yet: the session's reader keeps its prompt turns and check-ins
    UNDELIVERABLE = "undeliverable"  # hints posted here keep missing chances to be shown


class Deliverer:
    """Who handed a session its messages (`delivery_receipt`'s `deliverer`)."""

    HOOK = "hook"  # Claude Code's / Codex's reads hook
    PI = "pi"  # harness-literal-ok: pi's extension, as a receipt names its deliverer
    ASK = "ask"  # a `probe ask --wait`
    OTHER = "other"


#: A deliverer's own name for itself (`mailbox.touch_alive`, the claim log's `by`) -> who.
_DELIVERER_OF = {"UserPromptSubmit": Deliverer.HOOK, "PostToolUse": Deliverer.HOOK, "Stop": Deliverer.HOOK,
                 "pi poller": Deliverer.PI, "before_agent_start": Deliverer.PI,
                 "probe ask --wait": Deliverer.ASK}
#: How long a deliverer's heartbeat proves it is there: pi's poller touches it
#: every ALIVE_EVERY_S while it runs; a hook only when it runs Python (at a
#: prompt of a session the reader serves, or when a message waits), so its
#: heartbeat says "a current hook serves this session", and a hook that stops
#: delivering shows as missed hints instead (`MISSED_UNDELIVERABLE`).
DELIVERER_FRESH_S = {Deliverer.PI: 600.0}
DELIVERER_FRESH_DEFAULT_S = 12 * 3600.0
#: A hint shown (or, from a deliverer that writes no `shown`, claimed) this
#: recently proves delivery too.
DELIVERED_RECENTLY_S = 1800.0
#: A waiting hint MISSED its chance when at least this many agent tool calls, in
#: turns whose one hint slot was still free, came MISSED_AFTER_S or more after
#: it was posted and while it still waited: a hook delivers after the next tool
#: call, pi's poller within 2 s while the agent runs.
MISSED_TOOL_CALLS = 2
MISSED_AFTER_S = 3.0
#: Hints missed since the last one shown that make a session UNDELIVERABLE.
MISSED_UNDELIVERABLE = 2


# -- delivery ---------------------------------------------------------------------


def post_message(sid: str, state: str, message: dict) -> bool:
    """The hint in the session's mailbox: `mailbox.post`'s own step
    (`MailHost.post`: `mailbox.publish_here` under the session's state folder),
    in this process."""
    from ..mail.mail import MailHost

    answer = MailHost.post({"sid": sid, "state": state, "deadline_mono": time.monotonic() + TIMEOUT_S,
                            "message": message, "question": None})
    return bool(answer.get("posted"))


def withdraw_hints(sid: str, state: str) -> list[str]:
    """Every hint still waiting in the session's mailbox, taken out: the ids.
    Only hints: the mailbox's own `withdraw_unasked` is the reader's, and never
    takes one."""
    from probe.shared import mailbox

    gone: list[str] = []
    with mailbox.rooted(state):
        for path, msg in mailbox.waiting(sid):
            if msg.origin == mailbox.ORIGIN_HINT and msg.kind == mailbox.Kind.MESSAGE:
                try:
                    path.unlink()
                except FileNotFoundError:
                    continue  # a hook delivered it first
                gone.append(msg.id)
    return gone


def waiting_hints(sid: str, state: str) -> set[str]:
    """The ids of the hints waiting in the session's mailbox now (unexpired)."""
    from probe.shared import mailbox

    with mailbox.rooted(state):
        return {msg.id for _path, msg in mailbox.waiting(sid)
                if msg.origin == mailbox.ORIGIN_HINT and msg.kind == mailbox.Kind.MESSAGE}


#: A ledger line for a hint the lane took back before it was shown (`_take_back`).
LEDGER_WITHDRAWN = "withdrawn"
#: A hint claimed this long ago with no `shown` line, from a deliverer that
#: writes them, never reached the agent (its handoff failed after the claim).
SHOWN_AFTER_CLAIM_S = 60.0


def _jsonl(path: Path, tail_bytes: int) -> list[dict]:
    """The object lines of a JSONL file's last `tail_bytes`; [] when unreadable."""
    try:
        with path.open("rb") as handle:
            size = os.fstat(handle.fileno()).st_size
            handle.seek(max(0, size - tail_bytes))
            text = handle.read().decode("utf-8", "replace")
    except OSError:
        return []
    out = []
    for line in text.splitlines():
        try:
            entry = json.loads(line)
        except ValueError:
            continue
        if isinstance(entry, dict):
            out.append(entry)
    return out


def _stamped(entries: list[dict]) -> dict[str, tuple[float, str, bool]]:
    """id -> (the first `at`, its `by`, whether its claimer writes `shown`
    lines: `shows`) of claim-log / shown-log lines."""
    out: dict[str, tuple[float, str, bool]] = {}
    for entry in entries:
        mid, at = entry.get("id"), entry.get("at")
        if isinstance(mid, str) and isinstance(at, (int, float)) and mid not in out:
            out[mid] = (float(at), str(entry.get("by") or ""), entry.get("shows") == 1)
    return out


def delivery_facts(sid: str, state: str, ledger: Path) -> dict:
    """What the files say about the hints the lane posted to `sid` (its ledger
    and the mailbox): `posted` and `withdrawn` (id -> when), the deliverers'
    `claims` and `shown` lines (id -> (when, by)), the hints still `waiting`,
    and the deliverer heartbeat `alive` (or None)."""
    from probe.shared import mailbox

    posted: dict[str, float] = {}
    withdrawn: dict[str, float] = {}
    for entry in _jsonl(ledger, LEDGER_TAIL_BYTES):
        mid, at = entry.get("id"), entry.get("at")
        if not isinstance(mid, str) or not isinstance(at, (int, float)):
            continue
        if entry.get("event") == LEDGER_WITHDRAWN:
            withdrawn.setdefault(mid, float(at))
        elif isinstance(entry.get("keys"), list):
            posted.setdefault(mid, float(at))
    with mailbox.rooted(state):
        claims_path, shown_path = mailbox.claim_log_path(sid), mailbox.shown_log_path(sid)
        alive = mailbox.read_alive(sid)
        waiting = {msg.id for _path, msg in mailbox.waiting(sid)
                   if msg.origin == mailbox.ORIGIN_HINT and msg.kind == mailbox.Kind.MESSAGE}
    claims = {mid: hit for mid, hit in _stamped(_jsonl(claims_path, LEDGER_TAIL_BYTES)).items() if mid in posted}
    shown = {mid: hit for mid, hit in _stamped(_jsonl(shown_path, LEDGER_TAIL_BYTES)).items() if mid in posted}
    return {"posted": posted, "withdrawn": withdrawn, "claims": claims, "shown": shown, "waiting": waiting,
            "alive": alive}


def delivery_receipt(facts: dict, *, tool_calls, prompts, mid_turn: bool, now: float) -> dict:
    """Whether the hints posted to a session reach its agent, from
    `delivery_facts` and the session's tool-call and prompt stamps (epoch
    seconds, the transcript's own; `prompts` only those that started a turn).
    A hint REACHED the agent when a deliverer wrote its `shown` line, or when
    a deliverer that writes none claimed it (its claim line has no `shows`: one
    from before them, so an upgrade or a rollback judges every claim by the
    deliverer that made it). A hint not reached MISSED its chance when, while
    it waited, the agent made MISSED_TOOL_CALLS tool calls in turns whose one
    hint slot was still free (only on a harness that shows a hint mid-turn), or
    when a deliverer that writes `shown` lines claimed it SHOWN_AFTER_CLAIM_S
    ago and wrote none. MISSED_UNDELIVERABLE
    misses since the last hint that reached it make the session UNDELIVERABLE;
    else a fresh deliverer heartbeat, or a hint reached within
    DELIVERED_RECENTLY_S, makes it OK; else UNPROVEN. Counts are over the
    ledger's week; the `delivery` field of a `/v1/hints` request."""
    import bisect

    posted = sorted(facts["posted"].items(), key=lambda item: item[1])
    claims, shown, withdrawn = facts["claims"], facts["shown"], facts["withdrawn"]
    waiting, alive = facts["waiting"], facts["alive"]

    def reached_at(mid: str) -> float | None:
        if mid in shown:
            return shown[mid][0]
        claim = claims.get(mid)
        return claim[0] if claim is not None and not claim[2] else None

    reached = sorted(t for mid, _at in posted if (t := reached_at(mid)) is not None)
    turns = sorted(prompts)
    calls = sorted(tool_calls)

    def slot_free(t: float) -> bool:
        i = bisect.bisect_right(turns, t)
        start = turns[i - 1] if i else float("-inf")
        j = bisect.bisect_left(reached, start)
        return not (j < len(reached) and reached[j] < t)

    missed: set[str] = set()
    for index, (mid, at) in enumerate(posted):
        if reached_at(mid) is not None:
            continue
        claim = claims.get(mid)
        if claim is not None:  # by a deliverer that writes `shown` lines (`reached_at`)
            if now - claim[0] >= SHOWN_AFTER_CLAIM_S:
                missed.add(mid)  # taken, never handed over
            continue
        if not mid_turn:
            continue
        ends = [now]
        if mid in withdrawn:
            ends.append(withdrawn[mid])
        if mid not in waiting and mid not in withdrawn:
            ends.append(at + mailbox_ttl())  # expired, or replaced by the next one
            if index + 1 < len(posted):
                ends.append(posted[index + 1][1])
        end = min(ends)
        lo = bisect.bisect_left(calls, at + MISSED_AFTER_S)
        hi = bisect.bisect_left(calls, end)
        if sum(1 for t in calls[lo:hi] if slot_free(t)) >= MISSED_TOOL_CALLS:
            missed.add(mid)
    last = reached[-1] if reached else None
    since = [mid for mid, at in posted if last is None or at > last]
    by = (alive or {}).get("by") if alive else None
    if by is None and (shown or claims):
        by = max(list(shown.values()) + list(claims.values()))[1]  # the latest line's
    deliverer = _DELIVERER_OF.get(by, Deliverer.OTHER) if by else None
    alive_age = now - float(alive["at"]) if alive else None
    fresh = alive_age is not None and alive_age <= DELIVERER_FRESH_S.get(deliverer, DELIVERER_FRESH_DEFAULT_S)
    if sum(1 for mid in since if mid in missed) >= MISSED_UNDELIVERABLE:
        state = DeliveryState.UNDELIVERABLE
    elif fresh or (last is not None and now - last <= DELIVERED_RECENTLY_S):
        state = DeliveryState.OK
    else:
        state = DeliveryState.UNPROVEN
    return {
        "state": state,
        "deliverer": deliverer,
        "posted": len(posted),
        "claimed": sum(1 for mid, _at in posted if mid in claims),
        "shown": sum(1 for mid, _at in posted if mid in shown),
        "missed": len(missed),
        "withdrawn": sum(1 for mid, _at in posted if mid in withdrawn and mid not in missed
                         and reached_at(mid) is None),
        "unshown_since_shown": sum(1 for mid in since if reached_at(mid) is None),
        "last_shown_age_s": None if last is None else round(max(0.0, now - last), 1),
        "heartbeat_age_s": None if alive_age is None else round(max(0.0, alive_age), 1),
    }


def mailbox_ttl() -> float:
    """How long a hint may wait in a mailbox (`mailbox.UNASKED_TTL_S`)."""
    from probe.shared import mailbox

    return float(mailbox.UNASKED_TTL_S)


def delivered_ids(sid: str, state: str) -> set[str]:
    """The message ids delivered to the session: its claim log's (the tail) and
    the files in its `claimed/` folder (a claim whose log line was lost)."""
    from probe.shared import mailbox

    ids: set[str] = set()
    with mailbox.rooted(state):
        path = mailbox.claim_log_path(sid)
        ids |= mailbox.claimed_ids(sid)
    try:
        with path.open("rb") as handle:
            size = os.fstat(handle.fileno()).st_size
            handle.seek(max(0, size - CLAIM_LOG_TAIL_BYTES))
            tail = handle.read().decode("utf-8", "replace")
    except OSError:
        return ids
    for line in tail.splitlines():
        try:
            entry = json.loads(line)
        except ValueError:
            continue
        if isinstance(entry, dict) and isinstance(entry.get("id"), str):
            ids.add(entry["id"])
    return ids


def record_keys(records: object) -> frozenset[str]:
    """Each shown record as `<doc id> <date>`: the same record changed is new."""
    keys = set()
    for record in records if isinstance(records, list) else []:
        if isinstance(record, dict) and isinstance(record.get("doc_id"), str) and record["doc_id"]:
            keys.add(f"{record['doc_id']} {record.get('date') or ''}")
    return frozenset(keys)
