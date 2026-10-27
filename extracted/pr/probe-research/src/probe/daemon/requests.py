"""The main agent's requests to the daemon's writer, and what the writer sends back.

    probe ask --writer "<request>"   ->  mailbox requests/<sid>/<id>.json
    the worker takes it              ->  write_requests row + a META event on the
                                         `request` stream ("The main agent asks
                                         you: ..."), which starts a run at once
                                         (at most one such run a minute,
                                         `worker.REQUEST_RUN_MIN_GAP_S`)
    the run that saw it finishes     ->  its `final_result` reply, plus the writes
                                         made since the first bite that saw it
                                         (from the logbook, not the model's
                                         account), as ONE answer to each request
                                         that run saw
    it will not run                  ->  failed, with the reason and what was
                                         already written; its event is retired,
                                         and a conversation holding it ends, so
                                         no later run acts on it

A run with structural writes (create, fork, move, set, delete, edge) and no
request in it sends one receipt naming the ones recorded: the main agent learns
what the writer filed on its own, in at most RECEIPT_MAX_CHARS.

A headline metric or a best pick the writer set (track-work: "set it ... and
tell the researcher in one line") is told by a note of its own for the
researcher (`relay`), never by a receipt: the main agent passes it on.

Everything here is plain code over the logbook's rows: the write lists say what
was recorded and what was not (and why, from its status and output), whatever
the reply claims.
"""

from __future__ import annotations

import json
import sqlite3
from dataclasses import dataclass, field

from probe.daemon import mailbox

#: How a request reaches the writer (Richard's approved text, 2026-10-13).
REQUEST_LINE = "The main agent asks you: {text}"
#: A request no run took within this long fails (one 30-minute model call plus margin).
WRITE_REQUEST_TIMEOUT_S = 45 * 60.0
#: A receipt is at most this long; past it, "+N more".
RECEIPT_MAX_CHARS = 600
#: A reply's write lists, the same way.
REPLY_LIST_MAX_CHARS = 4000
#: The writer's own sentence in a reply, at most (the model's text reaches the agent).
REPLY_MAX_CHARS = 4000

#: Why a request will not run (the agent reads it after "did not run your request: ").
REASON_TIMEOUT = f"no run took it within {int(WRITE_REQUEST_TIMEOUT_S // 60)} minutes"
REASON_READ_ONLY = "Probe is read only for this session"
REASON_INLINE = "Probe is inline for this session"
REASON_OFF = "Probe is off for this session"
REASON_SKIPPED = "the run that had it stopped unfinished and was skipped"
REASON_STALLED = (f"the run that had it did not finish within {int(2 * WRITE_REQUEST_TIMEOUT_S // 60)} minutes "
                  "of the request")
REASON_SESSION_END = "the session ended before a run finished it"

#: Writes a reply or a receipt names one by one, as a researcher would say them;
#: any other write is only counted.
STRUCTURAL_HEADS = frozenset({
    "project create", "project delete", "project move", "project set",
    "experiment create", "experiment delete", "experiment fork", "experiment move", "experiment set",
    "group create", "group set",
    "run delete", "run move", "run set",
    "edge add", "edge remove",
})
_PAST = {"create": "created", "delete": "deleted", "fork": "forked", "move": "moved", "set": "changed",
         "add": "added", "remove": "removed"}
#: The parameter (`precheck.parse`) naming what a command of each noun acts on.
_TARGET = {"run": "run", "project": "project_id", "experiment": "experiment_id", "group": "group_id"}
#: Names listed for a group of moves before the rest are counted.
MOVE_NAMES_SHOWN = 6
#: Logbook lines that are not writes: lookups, and a skipped stretch's own line.
_NOT_WRITES = frozenset({"skipped"})

#: What the researcher is told, through the main agent, when the writer sets a
#: project's headline metric or a best pick (`relay`). The main agent sees it
#: as "[Probe] Tell the researcher: ..." (`mailbox.TEXT_WRITER_RELAY`). Richard's
#: approved text (2026-10-26, `~/plans/swarm-visibility-gaps/PROPOSED-track-work.md`).
RELAY_METRIC = mailbox.WRITER_RELAY_PREFIX + "{project}'s headline metric is now {key} ({way} is better{reduce})."
#: ...ranked on each run's best value rather than its final one (`--reduce best`).
RELAY_REDUCE_BEST = ", best value per run"
#: The writer's reason is the model's words: quoted, so the main agent reads it as data.
RELAY_PICK = mailbox.WRITER_RELAY_PREFIX + "{scope}'s best experiment is now {experiment} (\"{reason}\")."
#: ...with no reason (the CLI and Probe refuse an agent's pick without one).
RELAY_PICK_BARE = mailbox.WRITER_RELAY_PREFIX + "{scope}'s best experiment is now {experiment}."
RELAY_WORKSPACE = "workspace {workspace}"
RELAY_WAY = {"max": "higher", "min": "lower"}
#: A pick's reason in a note is one line of at most this many characters.
RELAY_REASON_CHARS = 200
#: The commands whose metric or pick a note tells (`project patch` is `set`'s old, hidden name).
_RELAYED = frozenset({"project set", "project patch", "workspace set"})


@dataclass
class Writes:
    """A run's writes from the logbook: structural ones named, the rest counted."""
    done: list[str] = field(default_factory=list)
    not_done: list[str] = field(default_factory=list)
    others_done: int = 0
    others_not_done: int = 0


def _argv(row: sqlite3.Row) -> list[str]:
    try:
        argv = json.loads(row["argv"])
    except (TypeError, ValueError):
        return []
    return [str(a) for a in argv] if isinstance(argv, list) else []


def _words(argv: list[str]) -> list[str]:
    return argv[1:] if argv[:1] == ["probe"] else argv


def _parsed(argv: list[str]) -> tuple[str, dict] | None:
    """The command's path and parameters by the CLI's own parser; None when it
    is not a `probe` command or does not parse."""
    from probe.daemon import precheck

    if argv[:1] != ["probe"]:
        return None
    try:
        parsed = precheck.parse(argv[1:])
    except Exception:  # noqa: BLE001 - an unparsed write is listed by its words
        return None
    return parsed.path, parsed.params


def _name(head: str, p: dict) -> str:
    noun, verb = head.split(" ", 1)
    if head == "group create":
        return f"created group {p.get('name') or '?'} in {p.get('experiment_id') or '?'}"
    if head == "experiment fork":
        return f"forked experiment {p.get('source') or '?'} as {p.get('slug') or '?'}"
    if head == "edge add":
        return f"linked {p.get('source') or '?'} {p.get('relation') or '?'} {p.get('target') or '?'}"
    if head == "edge remove":
        return f"removed link {p.get('edge_id') or '?'}"
    if verb == "create":
        return f"created {noun} {p.get('slug') or p.get('name') or '?'}"
    target = p.get(_TARGET.get(noun, "")) or "?"
    if verb == "move":
        return f"moved {noun} {target} to {_destination(noun, p)}"
    return f"{_PAST.get(verb, verb)} {noun} {target}"


def _destination(noun: str, p: dict) -> str:
    if noun == "project":
        return p.get("parent") or ("the top level" if p.get("top_level") else p.get("workspace")) or "?"
    return p.get("to") or "?"


def _why_not(row: sqlite3.Row) -> str:
    """Why a write is not recorded, from its status and output (its `reason` is
    the model's own purpose for it, not why it failed)."""
    status = row["status"]
    if status == "queued":
        return "queued: Probe did not answer yet"
    if status == "held":
        return "held for the researcher"
    if status == "cancelled":
        return "cut short while it ran"
    if status == "not_run":
        why = str(row["reason"] or "")
        why = why.split(": ", 1)[1] if why.startswith("block ") and ": " in why else why
        return "not run: " + " ".join(why.split())[:120]
    lines = [line.strip() for line in str(row["output"] or "").splitlines() if line.strip()]
    return f"failed: {lines[-1][:120]}" if lines else "failed"


def describe(rows: list[sqlite3.Row]) -> Writes:
    """The writes in `rows`, in order: structural ones named ("created experiment
    X", "moved 3 runs to X (a, b, c)"), done and not done; any other write
    counted. `--help` and reads are not writes."""
    out = Writes()
    done_slots: list[str | tuple[str, str]] = []  # a move group sits where its first move ran
    moves: dict[tuple[str, str], list[str]] = {}
    for row in rows:
        head = row["head"] or ""
        if row["status"] == "read" or head in _NOT_WRITES:
            continue
        argv = _argv(row)
        if "--help" in argv or "-h" in argv:
            continue
        done = row["status"] == "ran"
        parsed = _parsed(argv)
        if parsed is not None:
            head = parsed[0]  # an approved write is logged as `override` / `approved`
        params = parsed[1] if parsed is not None and head in STRUCTURAL_HEADS else None
        if params is None:
            if head in STRUCTURAL_HEADS:
                text = " ".join(_words(argv))[:160]
                (done_slots.append(text) if done else out.not_done.append(f"{text} ({_why_not(row)})"))
            elif done:
                out.others_done += 1
            else:
                out.others_not_done += 1
            continue
        noun, verb = head.split(" ", 1)
        if verb == "move" and done:
            key = (noun, _destination(noun, params))
            if key not in moves:
                moves[key] = []
                done_slots.append(key)
            moves[key].append(str(params.get(_TARGET.get(noun, "")) or "?"))
            continue
        text = _name(head, params)
        (done_slots.append(text) if done else out.not_done.append(f"{text} ({_why_not(row)})"))
    for slot in done_slots:
        if isinstance(slot, str):
            out.done.append(slot)
            continue
        (noun, dest), names = slot, moves[slot]
        if len(names) == 1:
            out.done.append(f"moved {noun} {names[0]} to {dest}")
        else:
            shown = ", ".join(names[:MOVE_NAMES_SHOWN]) + (", ..." if len(names) > MOVE_NAMES_SHOWN else "")
            out.done.append(f"moved {len(names)} {noun}s to {dest} ({shown})")
    return out


def joined(items: list[str], limit: int) -> str:
    """`items` joined with " · ", cut at `limit` characters with "+N more"."""
    out: list[str] = []
    used = 0
    for i, item in enumerate(items):
        more = len(items) - i - 1
        tail = f" · +{more} more" if more else ""
        piece = (" · " if out else "") + item
        if out and used + len(piece) + len(tail) > limit:
            return " · ".join(out) + f" · +{len(items) - i} more"
        out.append(item)
        used += len(piece)
    text = " · ".join(out)
    return text if len(text) <= limit else text[: limit - 1] + "…"


def _with_others(items: list[str], others: int) -> list[str]:
    return items + ([f"{others} other write{'s' if others != 1 else ''}"] if others else [])


def receipt_text(writes: Writes) -> str:
    """A run with no request: only the structural writes it made (empty: no receipt)."""
    return joined(writes.done, RECEIPT_MAX_CHARS) if writes.done else ""


def reply_text(reply: str, writes: Writes) -> str:
    """The writer's own sentence, then what the run made and did not, in plain code's words."""
    recorded = _with_others(writes.done, writes.others_done)
    missed = _with_others(writes.not_done, writes.others_not_done)
    lines = [(reply or "").strip()[:REPLY_MAX_CHARS]]
    if recorded:
        lines.append(f"Recorded: {joined(recorded, REPLY_LIST_MAX_CHARS)}")
    if missed:
        lines.append(f"Not recorded: {joined(missed, REPLY_LIST_MAX_CHARS)}")
    if not recorded and not missed:
        lines.append("No change recorded.")
    return "\n".join(line for line in lines if line)


def failure_reason(reason: str, writes: Writes | None = None) -> str:
    """A failed request's reason, with what its run already did ("partly done")."""
    done = _with_others(writes.done, writes.others_done) if writes is not None else []
    return f"{reason} (partly done: {joined(done, RECEIPT_MAX_CHARS)})" if done else reason


@dataclass(frozen=True)
class Relay:
    """A note for the researcher: what it is about (`scope`: one project's metric,
    or one project's or workspace's pick), the value it tells (a repeat of it
    tells nothing), its text (None for a clear), and whether the value is a
    person's (`persons`: the write changed nothing)."""
    scope: str
    value: str
    #: None for a clear: it tells nothing, but a later set of the same value does.
    text: str | None
    persons: bool = False


def _printed(output: str | None) -> dict:
    """The record a command printed: its output's first JSON object, else {}."""
    try:
        value, _end = json.JSONDecoder().raw_decode((output or "").lstrip())
    except ValueError:
        return {}
    return value if isinstance(value, dict) else {}


def _field(value: dict, key: str) -> dict:
    found = value.get(key)
    return found if isinstance(found, dict) else {}


def _line(value: object) -> str:
    return " ".join(str(value or "").split())


def _reason(text: object) -> str:
    """A pick's reason as one line of at most RELAY_REASON_CHARS. The note's own
    period follows its closing quote, so a single period ending the reason goes."""
    line = _line(text)
    if len(line) > RELAY_REASON_CHARS:
        line = line[:RELAY_REASON_CHARS - 1].rstrip() + "…"
    elif line.endswith(".") and not line.endswith(".."):
        line = line[:-1].rstrip()
    return line.replace('"', "'")  # it is quoted in the note


def relay(row: sqlite3.Row) -> Relay | None:
    """The note a logbook row owes the researcher: a `probe project set P --metric
    KEY --goal max|min`, `project set P --best EXP --reason "..."` or `workspace set
    W --best EXP --reason "..."` that ran (exit 0, not queued). None for anything
    else: a clear (`--metric ""`, `--best ""`), a failure (an agent's write over a
    person's metric or pick is a 409: exit 1), a help request. Read from the
    command's words (the CLI's own parser) and the record it printed (its
    experiment's slug, whose value it is), never the model's prose."""
    if row["status"] != "ran":
        return None
    from probe.daemon import precheck

    argv = _argv(row)
    if argv[:1] != ["probe"]:
        return None
    try:
        parsed = precheck.parse(argv[1:])
    except Exception:  # noqa: BLE001 - an unparsed write tells nothing
        return None
    # The CLI's own help check (the command's flag or `probe --help`): `--reason
    # --help` is a reason, not a help request.
    if parsed.help or precheck.asks_help(argv[1:]) or parsed.path not in _RELAYED:
        return None
    head, p = parsed.path, parsed.params
    printed = _printed(row["output"])
    project = _line(p.get("project_id")) or "?"
    if p.get("metric") is not None and head != "workspace set":
        metric = _line(p.get("metric"))
        anchor = _field(printed, "anchor").get("id") or project
        if not metric:  # a clear: no note, but the same value set again is told again
            return Relay(scope=f"metric:{anchor}", value="", text=None)
        goal, reduce = _line(p.get("goal")), _line(p.get("reduce")) or "final"
        return Relay(scope=f"metric:{anchor}", value=f"{metric} {goal} {reduce}",
                     text=RELAY_METRIC.format(project=project, key=metric, way=RELAY_WAY.get(goal, goal),
                                              reduce=RELAY_REDUCE_BEST if reduce == "best" else ""),
                     persons=_field(printed, "metric").get("source") == "human")
    if p.get("best") is None:
        return None
    best = _line(p.get("best"))
    pick = _field(printed, "pick")
    experiment = _field(pick, "experiment")
    if head == "workspace set":
        ref = _line(p.get("workspace_id")) or "?"
        where, noun = RELAY_WORKSPACE.format(workspace=ref), "workspace"
    else:
        ref = project
        where, noun = ref, "project"
    scope = f"best:{noun}:{_field(printed, 'scope').get('id') or ref}"
    if not best:  # a clear: no note, but the same pick set again is told again
        return Relay(scope=scope, value="", text=None)
    name = _line(experiment.get("slug")) or best
    reason = _reason(p.get("reason"))
    text = (RELAY_PICK.format(scope=where, experiment=name, reason=reason) if reason
            else RELAY_PICK_BARE.format(scope=where, experiment=name))
    return Relay(scope=scope, value=str(experiment.get("id") or name), text=text,
                 persons=pick.get("source") == "human")


def message(row: sqlite3.Row, session_id: str) -> mailbox.Message:
    """A `writer_messages` row as the mailbox message the agent is handed."""
    return mailbox.Message(id=row["id"], session=session_id, kind=row["kind"], text=row["text"] or "",
                           ask=row["ask"], reason=row["reason"], made_at=float(row["made_at"]),
                           origin=mailbox.ORIGIN_WRITER)
