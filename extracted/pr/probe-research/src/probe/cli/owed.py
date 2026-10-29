"""What a session owes (notes parity N3): ONE ledger the daemon's writer and an
inline agent both read, kept by the `probe` CLI itself.

Two kinds of item, each a fact a write left behind, never a judgment of what a
note should say (Richard rejected a general "you wrote no notes" nudge):

  summary  a project or experiment the session created, or an experiment whose
           conclusion it set, until a write of that entity's summary lands
           (`probe summary push`, `edit` or `append`; write-summary)
  note     a run the session tagged `invalid` (`probe run tag RUN invalid`),
           until a note on that run lands (track-work: "plus a note on what to
           believe instead")

Both recorders feed it the same way: the daemon records with the same `probe`
commands, under `PROBE_DAEMON_SESSION` (`summary_cli.session_id`). Each item
says who wrote it (`by`: `daemon` | `agent`) and when (`seq`, the ledger's own
counter), so the daemon's writer reads only what its run owes
(`daemon/tools.py summaries_owed`, `notes_owed`) and sends the run back once each
(`daemon/agent.py`), and an inline agent is sent back at the end of its turn
(`probe session owed --send-back`, run by the plugin's Stop hook and pi's
extension) with the same words, at most `MAX_ASKS` times per item.

    <state>/owed/<session id>.json   {"seq": 3, "items": [...], "asks": {...}}

Bookkeeping, never a failed write: every entry point swallows its own errors.
"""

from __future__ import annotations

import json
import os
from pathlib import Path
from typing import Any

from ..sdk.session_marker import OWED_MAX_ASKS

#: Kinds of item.
SUMMARY = "summary"
NOTE = "note"
#: Who wrote the item.
BY_DAEMON = "daemon"
BY_AGENT = "agent"
#: The tag that makes a run's note owed.
INVALID_TAG = "invalid"
#: How many times an inline agent is sent back for one item, per session (the
#: hooks' cheap check reads the same number: `session_marker.OWED_MAX_ASKS`).
MAX_ASKS = OWED_MAX_ASKS
#: The send-backs, as the daemon's writer has read SUMMARY_OWED since plan 3.5;
#: the daemon ends each with ", then end with final_result." (its output tool),
#: an inline agent's end with ".".
SUMMARY_OWED = ("Not ended: these summaries were not updated in this run: {entities}. Update each "
                "(probe summary checkout, edit the file, probe summary push), or say why not")
NOTE_OWED = ("Not ended: these runs are tagged invalid with no note on what to believe instead: {entities}. "
             "Write one (probe notes append --run RUN --text \"...\"), or say why not")
#: The commands that make a summary owed: the entity is new, or (below) an
#: experiment's question got its answer.
_OWES_SUMMARY = frozenset({"project create", "experiment create"})


def path(sid: str) -> Path:
    from ..sdk import session_marker

    if not session_marker.valid_session_id(sid):
        raise ValueError(f"not a session id: {sid!r}")
    return session_marker.owed_path(sid)


def writer() -> str:
    from .summary_cli import DAEMON_SESSION_ENV

    return BY_DAEMON if os.environ.get(DAEMON_SESSION_ENV) else BY_AGENT


def _session() -> str | None:
    from .summary_cli import RUN_ID_ENV, session_id

    if os.environ.get(RUN_ID_ENV):
        return None  # a run recording its own data (`probe exec`, the SDK)
    return session_id()


def read(sid: str) -> dict[str, Any]:
    """The ledger (`{"seq", "items", "asks"}`); empty when there is none."""
    try:
        data = json.loads(path(sid).read_text(encoding="utf-8"))
    except (OSError, ValueError):
        data = {}
    if not isinstance(data, dict):
        data = {}
    items = [i for i in data.get("items") or [] if isinstance(i, dict)
             and all(isinstance(i.get(k), str) for k in ("why", "kind", "ref")) and isinstance(i.get("seq"), int)]
    asks = data.get("asks") if isinstance(data.get("asks"), dict) else {}
    seq = data.get("seq") if isinstance(data.get("seq"), int) else 0
    return {"seq": seq, "items": items, "asks": {k: v for k, v in asks.items() if isinstance(v, int)}}


def _update(sid: str, change) -> None:
    from ..sdk.durable import file_lock, write_text_atomic

    target = path(sid)
    target.parent.mkdir(parents=True, exist_ok=True)
    with file_lock(target.with_suffix(".lock")):
        data = read(sid)
        change(data)
        write_text_atomic(target, json.dumps(data), mode=0o600)


def _key(item: dict) -> str:
    return f"{item['why']} {item['kind']} {item['ref']}"


def _spellings(item: dict) -> set[str]:
    names = {item["ref"], *(str(i) for i in item.get("ids") or [])}
    names |= {f"id:{i}" for i in item.get("ids") or []}
    return {f"{item['kind']}:{n}" for n in names}


def owe(why: str, kind: str, ref: str, *, ids: tuple[str, ...] = (), sid: str | None = None) -> None:
    """Record that this session owes `why` on `kind` `ref` (as typed). Owed
    again after it was settled: a summary pushed before a conclusion does not
    cover it."""
    sid = sid or _session()
    if not sid or not ref:
        return

    def change(data: dict) -> None:
        data["seq"] += 1
        data["items"] = [i for i in data["items"] if (i.get("why"), i.get("kind"), i.get("ref")) != (why, kind, ref)]
        data["items"].append({"why": why, "kind": kind, "ref": ref, "ids": [i for i in ids if i],
                              "by": writer(), "seq": data["seq"]})

    try:
        _update(sid, change)
    except Exception:  # noqa: BLE001 -- bookkeeping, never a failed write
        pass


def settle(why: str, keys: set[str], *, sid: str | None = None) -> None:
    """A write of `why` landed on the entity `keys` names (`kind:<spelling>`,
    as `summary_cli.Target.keys`): nothing is owed for it any more."""
    sid = sid or _session()
    if not sid or not keys:
        return
    try:
        if not any(i.get("why") == why and _spellings(i) & keys for i in read(sid)["items"]):
            return  # the common case: nothing owed, no write
        _update(sid, lambda data: data.update(
            items=[i for i in data["items"] if not (i.get("why") == why and _spellings(i) & keys)]))
    except Exception:  # noqa: BLE001
        pass


def after_write(args: list[str]) -> None:
    """After a `probe` write exited 0 (`main.main`): a create or a conclusion
    makes that entity's summary owed. A run's `invalid` tag is recorded by
    `run tag` itself, which knows the run's id (`after_tag`)."""
    try:
        from probe.daemon import precheck

        from ..sdk import session_marker
        from . import summary_cli

        if session_marker.classify_probe_args(list(args))[0] != "write" or _session() is None:
            return
        parsed = precheck.parse(list(args))
        concluding = parsed.path == "experiment set" and any(
            c.strip() for c in precheck._strings(parsed.params.get("conclusion")))
        if parsed.path not in _OWES_SUMMARY and not concluding:
            return
        found = summary_cli.landing(list(args))
        if found is not None:
            owe(SUMMARY, found[0], found[1])
    except Exception:  # noqa: BLE001 -- bookkeeping, never a failed write
        pass


def _invalid(tags: list[str] | None) -> bool:
    return any(str(t).strip().lower() == INVALID_TAG for t in tags or [])


def after_tag(label: str, run_id: str, before: list[str] | None, after: list[str] | None) -> None:
    """`probe run tag` landed: adding `invalid` owes a note on the run; taking
    it off settles what was owed (the run is to be believed again)."""
    if _invalid(after) and not _invalid(before):
        owe(NOTE, "run", label, ids=(run_id,))
    elif not _invalid(after):
        settle(NOTE, {f"run:{run_id}"})


def owed(sid: str, *, by: str | None = None, since: int = 0, why: str | None = None) -> list[dict]:
    """The items still owed, oldest first: `by` one writer, `since` after that
    `seq` (a daemon run's start), `why` one kind."""
    return [i for i in read(sid)["items"]
            if (by is None or i.get("by") == by) and (why is None or i.get("why") == why)
            and int(i.get("seq") or 0) > since]


def entities(items: list[dict]) -> str:
    """`experiment wider, project p`: the items as SUMMARY_OWED names them."""
    return ", ".join(f"{i['kind']} {i['ref']}" for i in items)


def send_back(sid: str) -> str | None:
    """What an inline agent is told at the end of its turn, or None: the
    agent's own items, each at most MAX_ASKS times this session (counted here);
    summaries only while this machine last saw the team in recorder mode, as the
    daemon asks only then (a lane team's push is refused)."""
    from . import summary_cli

    asks = read(sid)["asks"]
    items = [i for i in owed(sid, by=BY_AGENT) if asks.get(_key(i), 0) < MAX_ASKS]
    if summary_cli.seen_mode() != summary_cli.MODE_RECORDER:
        items = [i for i in items if i.get("why") != SUMMARY]
    if not items:
        return None
    lines = []
    for why, text in ((SUMMARY, SUMMARY_OWED), (NOTE, NOTE_OWED)):
        due = [i for i in items if i.get("why") == why]
        if due:
            lines.append(text.format(entities=entities(due)) + ".")

    def asked(data: dict) -> None:
        for item in items:
            data["asks"][_key(item)] = data["asks"].get(_key(item), 0) + 1

    _update(sid, asked)
    return "\n".join(lines)
