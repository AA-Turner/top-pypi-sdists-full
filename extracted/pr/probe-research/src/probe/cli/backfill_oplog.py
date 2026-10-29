"""The record pass's op log: what one record session asked Probe to write, in order.

An import's record session (`backfill_record`) types the `probe` commands the
researcher's skills name. Commands that only change a local file run at once;
commands that would write to Probe are STAGED here and applied after the
session by code, in order:

    run_set         a run's name and/or description           (`probe run set`)
    experiment_set  an experiment's name, question, conclusion (`probe experiment set`)
    project_metric  the project's headline metric and its goal (`probe project set --metric`)
    note            an entity's whole note, as pushed           (`probe notes push|edit|append`)
    page            a project's or experiment's page, as pushed (`probe summary push`)

ONE JSON OBJECT PER LINE, API-shaped and free of client objects, so another
process can apply the same log (the T5 repair applies it in the maintenance pod
through the in-process API):

    {"schema": "probe.backfill.oplog/1", "id": "<32 hex>", "seq": 3,
     "kind": "run_set",
     "target": {"kind": "run", "id": "<uuid or null>", "folder": "a/b",
                "slug": null, "under": null},
     "fields": {"name": "...", "description": "..."},
     "base_version": null, "session": "<session id>", "at": "<iso>"}

`target` always carries a key that is not an id, so a process that never saw
the ids can resolve them: a run by `folder` (its relative path, the same one in
`metadata.backfill.relative_path` and `external_id`), an experiment by `slug`
and `under` (its folder), a project by `slug`. `id` is there when known.

`base_version` is the version a note or page was checked out at (CAS); null for
the set kinds. `id` is derived from the session and the sequence, so a replay
of the same session's log names the same ops: an applier records what it has
applied by id (an `.applied.jsonl` beside the work dir, never inside the agent's work
dir: `applied_path`) and resumes after a crash without doubling a note.

The log sits in the agent's work dir, so it is EVIDENCE, never authority: every
applier checks each op against what the import made before acting on it.

STDLIB ONLY: the record tool loads this on every `probe` call the agent makes.
"""

from __future__ import annotations

import hashlib
import json
import os
from datetime import datetime, timezone
from enum import Enum
from pathlib import Path

SCHEMA = "probe.backfill.oplog/1"
#: The applied-ops record beside a log (`applied_path`).
APPLIED_SUFFIX = ".applied.jsonl"


class Kind(str, Enum):
    RUN_SET = "run_set"
    EXPERIMENT_SET = "experiment_set"
    PROJECT_METRIC = "project_metric"
    NOTE = "note"
    PAGE = "page"


class TargetKind(str, Enum):
    PROJECT = "project"
    EXPERIMENT = "experiment"
    RUN = "run"


#: The fields each kind may carry, and nothing else.
FIELDS: dict[Kind, tuple[str, ...]] = {
    Kind.RUN_SET: ("name", "description"),
    Kind.EXPERIMENT_SET: ("name", "question", "conclusion"),
    Kind.PROJECT_METRIC: ("key", "goal", "reduce"),
    Kind.NOTE: ("text",),
    Kind.PAGE: ("html",),
}

#: What each kind may be written to.
TARGETS: dict[Kind, frozenset[TargetKind]] = {
    Kind.RUN_SET: frozenset({TargetKind.RUN}),
    Kind.EXPERIMENT_SET: frozenset({TargetKind.EXPERIMENT}),
    Kind.PROJECT_METRIC: frozenset({TargetKind.PROJECT}),
    Kind.NOTE: frozenset({TargetKind.PROJECT, TargetKind.EXPERIMENT, TargetKind.RUN}),
    Kind.PAGE: frozenset({TargetKind.PROJECT, TargetKind.EXPERIMENT}),
}

#: Kinds whose ops each carry a WHOLE document: only the last one per target
#: is the document; the earlier ones are what it replaced.
DOCUMENTS = frozenset({Kind.NOTE, Kind.PAGE})


class Outcome(str, Enum):
    """What applying one op came to (`applied.jsonl`)."""

    APPLIED = "applied"
    #: Nothing to send: the document or field already says it.
    UNCHANGED = "unchanged"
    #: A later op replaces this document whole.
    SUPERSEDED = "superseded"
    #: Probe or the applier's own checks refused it for good; not retried.
    REFUSED = "refused"


def target(kind: TargetKind | str, *, id: str | None = None, slug: str | None = None,
           folder: str | None = None, under: str | None = None) -> dict:
    """An op's target: its kind, its id when known, and the keys that are not ids."""
    return {"kind": TargetKind(kind).value, "id": id, "slug": slug, "folder": folder,
            "under": under}


def target_key(value: dict) -> tuple:
    """One target whatever spelling the op used: by its non-id key."""
    kind = value.get("kind")
    if kind == TargetKind.RUN.value:
        return (kind, value.get("folder"))
    if kind == TargetKind.EXPERIMENT.value:
        return (kind, value.get("under"), value.get("slug"))
    return (kind, value.get("slug"))


def op_id(session: str, seq: int) -> str:
    return hashlib.sha256(f"{session}\0{seq}".encode()).hexdigest()[:32]


def make(kind: Kind | str, target_: dict, fields: dict, *, session: str, seq: int,
         base_version: int | None = None) -> dict:
    """One op line. Raises ValueError for a field its kind does not carry."""
    kind = Kind(kind)
    extra = set(fields) - set(FIELDS[kind])
    if extra:
        raise ValueError(f"{kind.value} carries no {', '.join(sorted(extra))}")
    return {
        "schema": SCHEMA,
        "id": op_id(session, seq),
        "seq": seq,
        "kind": kind.value,
        "target": target_,
        "fields": {key: value for key, value in fields.items() if value is not None},
        "base_version": base_version,
        "session": session,
        "at": datetime.now(timezone.utc).isoformat(),
    }


def problem(op) -> str | None:
    """Why `op` is not a well-formed op line, or None. Its target's existence is
    the applier's to check."""
    if not isinstance(op, dict) or op.get("schema") != SCHEMA:
        return "not an op line"
    try:
        kind = Kind(op.get("kind"))
    except ValueError:
        return f"unknown kind {op.get('kind')!r}"
    where = op.get("target")
    if not isinstance(where, dict):
        return "no target"
    try:
        target_kind = TargetKind(where.get("kind"))
    except ValueError:
        return f"unknown target kind {where.get('kind')!r}"
    if target_kind not in TARGETS[kind]:
        return f"{kind.value} cannot be written to a {target_kind.value}"
    if any(where.get(name) is not None and not isinstance(where.get(name), str)
           for name in ("id", "slug", "folder", "under")):
        return "a target key is not text"
    key = where.get("folder") if target_kind is TargetKind.RUN else where.get("slug")
    if not isinstance(key, str) or (target_kind is not TargetKind.RUN and not key):
        return "the target has no key"
    base = op.get("base_version")
    if base is not None and (not isinstance(base, int) or isinstance(base, bool) or base < 0):
        return "the base version is not a version"
    fields = op.get("fields")
    if not isinstance(fields, dict) or not fields:
        return "no fields"
    if set(fields) - set(FIELDS[kind]):
        return f"{kind.value} carries only {', '.join(FIELDS[kind])}"
    if any(not isinstance(value, str) for value in fields.values()):
        return "a field is not text"
    if kind is Kind.PROJECT_METRIC and (not fields.get("key") or fields.get("goal") not in ("max", "min")
                                        or fields.get("reduce") not in (None, "final", "best")):
        return "a metric needs a key, a goal of max or min, and a reduce of final or best"
    if not isinstance(op.get("id"), str) or not isinstance(op.get("seq"), int):
        return "no id or sequence"
    return None


def append(path: Path, op: dict) -> None:
    """Add one op to the log, durably (one line, flushed and synced)."""
    path.parent.mkdir(parents=True, exist_ok=True)
    line = json.dumps(op, ensure_ascii=False, sort_keys=True) + "\n"
    with open(path, "a", encoding="utf-8") as handle:
        handle.write(line)
        handle.flush()
        os.fsync(handle.fileno())


def read(path: Path) -> tuple[list[dict], int]:
    """`(well-formed ops in sequence order, lines dropped)`. A line the agent
    hand-wrote is read like any other and checked like any other."""
    ops: list[dict] = []
    dropped = 0
    try:
        lines = Path(path).read_text(encoding="utf-8").splitlines()
    except FileNotFoundError:
        return [], 0
    seen: set[str] = set()
    for line in lines:
        if not line.strip():
            continue
        try:
            op = json.loads(line)
        except ValueError:
            dropped += 1
            continue
        if problem(op) is not None or op["id"] in seen:
            dropped += 1
            continue
        seen.add(op["id"])
        ops.append(op)
    ops.sort(key=lambda op: op["seq"])
    return ops, dropped


def next_seq(path: Path) -> int:
    ops, _ = read(path)
    return (ops[-1]["seq"] + 1) if ops else 1


def superseded(ops: list[dict]) -> set[str]:
    """The ids of document ops a later op on the same target replaces whole."""
    last: dict[tuple, str] = {}
    for op in ops:
        if op["kind"] in {kind.value for kind in DOCUMENTS}:
            last[(op["kind"], target_key(op["target"]))] = op["id"]
    keep = set(last.values())
    return {op["id"] for op in ops
            if op["kind"] in {kind.value for kind in DOCUMENTS} and op["id"] not in keep}


def applied_path(log: Path) -> Path:
    """The applied-ops record of `log`: beside the session's work dir, never in
    it, so the agent that wrote the log cannot mark its own ops as done."""
    log = Path(log)
    return log.parent.parent / f"{log.parent.name}.{log.name}{APPLIED_SUFFIX}"


def record_applied(path: Path, op: dict, outcome: Outcome, detail: str = "") -> None:
    append(path, {"id": op["id"], "seq": op["seq"], "outcome": Outcome(outcome).value,
                  "detail": detail[:300], "at": datetime.now(timezone.utc).isoformat()})


def applied(path: Path) -> dict[str, dict]:
    """op id -> its outcome line, for every op a run of the applier settled."""
    out: dict[str, dict] = {}
    try:
        lines = Path(path).read_text(encoding="utf-8").splitlines()
    except FileNotFoundError:
        return out
    for line in lines:
        try:
            row = json.loads(line)
        except ValueError:
            continue
        if isinstance(row, dict) and isinstance(row.get("id"), str):
            out[row["id"]] = row
    return out
