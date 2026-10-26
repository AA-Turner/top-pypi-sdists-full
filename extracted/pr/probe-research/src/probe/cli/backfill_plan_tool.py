"""`probe-backfill-plan`: how a classifying agent files a folder without copying it.

The classifier used to answer with JSON naming every row of the evidence back,
"verbatim", "exactly once". On 2026-10-25 a 144,178-file folder went through 22
slices that way and the model retyped two of 200 random-hex directory names
wrong in slice 17. The reconcile called them invented paths, refused the whole
plan, and 52 minutes of classification were thrown away over two typos.

A model cannot be trusted to copy data reliably, so it no longer copies any. It
SELECTS: `assign <project> --under <dir>` files every file it owns under a
directory, `--file` one file, `--rest` whatever is still undecided. Each call is
checked against the real file list at the moment it is made, so a name that
matches nothing is refused with the nearest real names while the agent can still
fix it -- the repair happens inside the turn instead of failing the run after it.

THIS FILE IS THE WHOLE CONTRACT, run two ways:

    the agent   `probe-backfill-plan ...` through the launcher the import puts on
                its PATH. It is not a Probe command (no network, no team record;
                see `backfill.plan_tool_launcher`). Every accepted call is appended to a decisions log.
    the import  `replay(reference, log_lines)` -- the SAME `apply` over the same
                lines, against the reference the importing process holds in
                memory. The log is the agent's to write (it sits in the agent's
                own work dir), so it is evidence, never authority: a line the
                agent wrote by hand is checked exactly like one the tool wrote.

Named selectors, not row numbers. A mistyped name matches nothing and is
refused; a mistyped number points at another real row and misfiles it silently.

STDLIB ONLY, and no imports from the package. The launcher loads this file by
path on the agent's fast path: importing `probe.cli` costs ~0.8 s (it pulls in
the SDK client and the whole Typer app), and an agent filing a slice makes
several calls.
"""

from __future__ import annotations

import argparse
import bisect
import difflib
import json
import os
import re
import sys
import time
from dataclasses import dataclass, field
from enum import Enum
from pathlib import Path

#: The directory holding `owned.json`, written by the importer OUTSIDE the
#: agent's work dir. The agent can read it and cannot write it.
REF_ENV = "PROBE_PLAN_REF"
#: The decisions log, inside the agent's work dir (Codex's sandbox confines this
#: tool's writes as well as the agent's, so it cannot live anywhere else).
LOG_ENV = "PROBE_PLAN_LOG"

REF_FILE = "owned.json"
#: Refused calls, one line each. Read only for telemetry: how often a model
#: mistyped and fixed it is the number that says this design is working.
REFUSED_FILE = "refused.jsonl"

#: A note is one line about what a file is. Capped so a note can never push a
#: manifest row or the manifest over `backfill_manifest`'s limits, which would
#: refuse the FILE -- and a note must never cost a file.
NOTE_MAX_CHARS = 2_000
WHY_MAX_CHARS = 300
STATUS_MAX_LINES = 40
SHOW_MAX_LINES = 60
NEAREST = 3

_SLUG = re.compile(r"\A[a-z0-9][a-z0-9-]{0,62}\Z")


class Mode(str, Enum):
    #: One slice of a chunked folder, filed against a project list already named.
    FILE = "file"
    #: A whole folder in one session, which also names its projects.
    CLASSIFY = "classify"
    #: A reviewer's correction over the whole folder, starting from the plan.
    REVISE = "revise"
    #: One upload unit: the files are fixed, only notes are written.
    NOTE = "note"


class Op(str, Enum):
    ASSIGN = "assign"
    LEAVE_OUT = "leave_out"
    PROJECT = "project"
    NOTE = "note"


class Kind(str, Enum):
    ASSIGNED = "assigned"
    LEFT_OUT = "left_out"


#: Which operations each mode accepts. A filing session cannot invent a
#: project; a notes session cannot move a file.
_ALLOWED = {
    Mode.FILE: {Op.ASSIGN, Op.LEAVE_OUT},
    Mode.CLASSIFY: {Op.ASSIGN, Op.LEAVE_OUT, Op.PROJECT},
    Mode.REVISE: {Op.ASSIGN, Op.LEAVE_OUT, Op.PROJECT},
    Mode.NOTE: {Op.NOTE},
}


def norm(path: str) -> str:
    """One spelling for comparison: `/` separators, no `./`, no trailing `/`.

    Only the OS separator is translated, and nothing is stripped from inside a
    name: on POSIX `a\\b.py` and `a/b.py`, or `x.py` and `x.py `, are different
    files, and folding them together selected the wrong one.
    """
    out = path.replace(os.sep, "/") if os.sep != "/" else path
    while out.startswith("./"):
        out = out[2:]
    while "//" in out:
        out = out.replace("//", "/")
    return out.rstrip("/") if out not in ("", "/") else out


@dataclass
class Reference:
    """What one session may decide. The importer's copy is the authority."""

    root: str
    mode: Mode
    #: Root-relative paths of every walked file this session owns.
    files: tuple[str, ...]
    #: Project slugs that exist before the session starts.
    projects: tuple[str, ...] = ()
    #: REVISE only: the plan being corrected, file -> decision dict.
    seed: dict[str, dict] = field(default_factory=dict)

    def __post_init__(self):
        self.mode = Mode(self.mode)
        # The agent reads files by the absolute path the prompt shows, and
        # names them back that way; compare against the same spelling.
        self.root = os.path.abspath(self.root)
        by_norm: dict[str, str] = {}
        for f in self.files:
            by_norm.setdefault(norm(f), f)
        self._by_norm = by_norm
        self._sorted = sorted(by_norm)

    # -- persistence ---------------------------------------------------------

    def to_json(self) -> str:
        return json.dumps({
            "root": self.root, "mode": self.mode.value, "files": list(self.files),
            "projects": list(self.projects), "seed": self.seed,
        }, ensure_ascii=False)

    @classmethod
    def from_json(cls, text: str) -> "Reference":
        data = json.loads(text)
        return cls(
            root=str(data["root"]), mode=Mode(data["mode"]),
            files=tuple(str(f) for f in data.get("files") or ()),
            projects=tuple(str(p) for p in data.get("projects") or ()),
            seed={str(k): dict(v) for k, v in (data.get("seed") or {}).items()},
        )

    def write(self, directory: Path) -> Path:
        directory.mkdir(parents=True, exist_ok=True)
        path = directory / REF_FILE
        tmp = path.with_suffix(".tmp")
        tmp.write_text(self.to_json(), encoding="utf-8")
        os.replace(tmp, path)
        return path

    # -- selection -----------------------------------------------------------

    def relative(self, selector: str) -> str | None:
        """The selector as a folder-relative path, or None if it is outside."""
        raw = selector if norm(selector) in self._by_norm else selector.strip()
        root = norm(self.root)
        candidate = norm(raw)
        if raw.startswith("/") or re.match(r"\A[A-Za-z]:[\\/]", raw):
            if candidate == root:
                return ""
            if not candidate.startswith(root + "/"):
                return None
            candidate = candidate[len(root) + 1:]
        if candidate in (".", "/"):
            return ""
        if ".." in candidate.split("/"):
            return None
        return candidate

    def under(self, directory: str) -> list[str]:
        """Every owned file at or below `directory` (or the file itself)."""
        if directory == "":
            return [self._by_norm[k] for k in self._sorted]
        out = []
        if directory in self._by_norm:
            out.append(self._by_norm[directory])
        prefix = directory + "/"
        i = bisect.bisect_left(self._sorted, prefix)
        while i < len(self._sorted) and self._sorted[i].startswith(prefix):
            out.append(self._by_norm[self._sorted[i]])
            i += 1
        return out

    def exact(self, path: str) -> list[str]:
        return [self._by_norm[path]] if path in self._by_norm else []

    def nearest(self, wanted: str) -> list[str]:
        """Real names closest to a selector that matched nothing.

        Walks up to the deepest directory that DOES exist and compares the next
        component against that directory's children, which is where a typo in a
        long name lives. A difflib pass over every file in a 144k-file folder
        would be slower and worse: the useful candidates are the siblings.
        """
        parts = [p for p in wanted.split("/") if p]
        depth = 0
        for n in range(len(parts) - 1, 0, -1):
            if self.under("/".join(parts[:n])):
                depth = n
                break
        base = "/".join(parts[:depth])
        rest = parts[depth] if depth < len(parts) else ""
        children = self._children(base)
        if not children:
            return []
        picks = difflib.get_close_matches(rest, children, n=NEAREST, cutoff=0.4) or children[:NEAREST]
        return [f"{base}/{c}" if base else c for c in picks]

    def _children(self, base: str, cap: int = 50_000) -> list[str]:
        prefix = base + "/" if base else ""
        i = bisect.bisect_left(self._sorted, prefix)
        seen: dict[str, None] = {}
        scanned = 0
        while i < len(self._sorted) and self._sorted[i].startswith(prefix) and scanned < cap:
            seen.setdefault(self._sorted[i][len(prefix):].split("/", 1)[0], None)
            i += 1
            scanned += 1
        return list(seen)


@dataclass
class Decision:
    kind: Kind
    project: str | None = None
    why: str = ""
    low: bool = False

    def as_dict(self) -> dict:
        out: dict = {"kind": self.kind.value}
        if self.project:
            out["project"] = self.project
        if self.why:
            out["why"] = self.why
        if self.low:
            out["low"] = True
        return out

    @classmethod
    def from_dict(cls, data: dict) -> "Decision":
        return cls(Kind(data["kind"]), data.get("project"), str(data.get("why") or ""),
                   bool(data.get("low")))


@dataclass
class State:
    decided: dict[str, Decision] = field(default_factory=dict)
    #: Projects this session declared: slug -> {name, description, tags}.
    declared: dict[str, dict] = field(default_factory=dict)
    notes: dict[str, str] = field(default_factory=dict)
    #: Low-confidence selectors as the agent wrote them, for the review screen.
    unsure: list[str] = field(default_factory=list)
    #: Lines replay rejected. The tool never writes one, so these were written
    #: by hand or edited: counted, never applied.
    invalid: int = 0
    #: Lines replay accepted beyond the seed.
    accepted: int = 0


def initial_state(ref: Reference) -> State:
    state = State()
    for path, data in ref.seed.items():
        if ref.exact(norm(path)):
            try:
                state.decided[ref.exact(norm(path))[0]] = Decision.from_dict(data)
            except (KeyError, ValueError):
                continue
    return state


class Refused(ValueError):
    """A call that changes nothing, with the message the agent reads."""


def _selection(ref: Reference, state: State, op: dict) -> tuple[list[str], str]:
    given = [k for k in ("under", "file", "rest") if op.get(k) not in (None, False, "")]
    if len(given) != 1:
        raise Refused("give exactly one of --under <dir>, --file <path> or --rest")
    key = given[0]
    if key == "rest":
        return [f for f in ref.files if f not in state.decided], "the rest"
    raw = str(op[key])
    rel = ref.relative(raw)
    if rel is None:
        raise Refused(f"{raw!r} is not inside {ref.root}")
    files = ref.under(rel) if key == "under" else ref.exact(rel)
    if not files:
        if key == "file" and ref.under(rel):
            raise Refused(f"{raw!r} is a directory here; use --under")
        near = ref.nearest(rel)
        hint = ("; nearest: " + ", ".join(near)) if near else ""
        raise Refused(f"nothing in this {_scope(ref)} is at {raw!r}{hint}")
    return files, rel or "."


def _scope(ref: Reference) -> str:
    return "unit" if ref.mode is Mode.NOTE else ("slice" if ref.mode is Mode.FILE else "folder")


def _text(value, limit: int, what: str) -> str:
    text = "" if value is None else str(value).strip()
    if len(text) > limit:
        raise Refused(f"{what} is {len(text):,} characters; keep it under {limit:,}")
    return text


def apply(ref: Reference, state: State, op: dict) -> str:
    """Apply one operation to `state`, or raise `Refused` leaving it untouched.

    The one place the rules live. The CLI calls it before appending a line to
    the log; `replay` calls it on every line the log holds.
    """
    try:
        kind = Op(str(op.get("op")))
    except ValueError:
        raise Refused(f"unknown operation {op.get('op')!r}") from None
    if kind not in _ALLOWED[ref.mode]:
        raise Refused(f"`{kind.value.replace('_', '-')}` is not available in this {_scope(ref)}")

    if kind is Op.PROJECT:
        slug = str(op.get("slug") or "").strip()
        if not _SLUG.match(slug):
            raise Refused(f"{slug!r} is not a usable slug (lowercase letters, digits and hyphens)")
        state.declared[slug] = {
            "slug": slug,
            "name": _text(op.get("name") or slug, 120, "the name"),
            "description": _text(op.get("description"), 1_000, "the description"),
            "tags": [str(t) for t in (op.get("tags") or []) if str(t).strip()][:8],
        }
        return f"project {slug} is available"

    files, label = _selection(ref, state, op)

    if kind is Op.NOTE:
        text = _text(op.get("notes"), NOTE_MAX_CHARS, "the note")
        if not text:
            raise Refused("the note is empty")
        for f in files:
            state.notes[f] = text
        return f"noted {len(files):,} file{'s' if len(files) != 1 else ''}"

    why = _text(op.get("why"), WHY_MAX_CHARS, "--why")
    if kind is Op.LEAVE_OUT:
        if not why:
            raise Refused("say why with --why; a left-out file is not uploaded")
        new = Decision(Kind.LEFT_OUT, None, why)
        target = "left out"
    else:
        project = str(op.get("project") or "").strip()
        allowed = set(ref.projects) | set(state.declared)
        if project not in allowed:
            listed = ", ".join(sorted(allowed)) or "(none yet)"
            extra = " Declare it first with `probe-backfill-plan project`." if Op.PROJECT in _ALLOWED[ref.mode] else ""
            raise Refused(f"{project!r} is not a project here. Projects: {listed}.{extra}")
        new = Decision(Kind.ASSIGNED, project, why, bool(op.get("low")))
        target = project
        if new.low:
            state.unsure.append(label)

    moved: dict[str, int] = {}
    for f in files:
        old = state.decided.get(f)
        if old is not None and (old.kind, old.project) != (new.kind, new.project):
            name = old.project if old.kind is Kind.ASSIGNED else "left out"
            moved[name] = moved.get(name, 0) + 1
        state.decided[f] = new
    msg = f"{target}: {len(files):,} file{'s' if len(files) != 1 else ''} ({label})"
    if moved:
        msg += "; moved " + ", ".join(f"{n:,} from {k}" for k, n in sorted(moved.items()))
    return msg


def replay(ref: Reference, lines) -> State:
    """Rebuild a session's state from its log, validating every line again."""
    state = initial_state(ref)
    for raw in lines:
        raw = raw.strip() if isinstance(raw, str) else raw
        if not raw:
            continue
        try:
            op = json.loads(raw) if isinstance(raw, str) else dict(raw)
            if not isinstance(op, dict):
                raise Refused("not an object")
            apply(ref, state, op)
            state.accepted += 1
        except (Refused, ValueError, TypeError, KeyError):
            state.invalid += 1
    return state


def read_log(path: Path) -> list[str]:
    try:
        return path.read_text(encoding="utf-8", errors="replace").splitlines()
    except FileNotFoundError:
        return []


def refused_count(log: Path) -> int:
    return len(read_log(log.parent / REFUSED_FILE))


# -- what the agent sees -----------------------------------------------------


def status(ref: Reference, state: State) -> str:
    if ref.mode is Mode.NOTE:
        noted = sum(1 for f in ref.files if f in state.notes)
        return f"{noted:,} of {len(ref.files):,} files have a note. Notes are optional; every file uploads."
    counts: dict[str, int] = {}
    for d in state.decided.values():
        name = d.project if d.kind is Kind.ASSIGNED else "left out"
        counts[name] = counts.get(name, 0) + 1
    undecided = [f for f in ref.files if f not in state.decided]
    lines = [f"{len(ref.files) - len(undecided):,} of {len(ref.files):,} files decided"
             + (" (" + ", ".join(f"{k} {v:,}" for k, v in sorted(counts.items())) + ")" if counts else "")
             + "."]
    if not undecided:
        lines.append("0 undecided. This " + _scope(ref) + " is done.")
        return "\n".join(lines)
    lines.append(f"{len(undecided):,} undecided:")
    groups = _groups(undecided)
    for prefix, n in groups[:STATUS_MAX_LINES]:
        lines.append(f"  {prefix or '.'}{'/' if prefix and n > 1 else ''}  ({n:,} file{'s' if n != 1 else ''})")
    if len(groups) > STATUS_MAX_LINES:
        lines.append(f"  ... and {len(groups) - STATUS_MAX_LINES:,} more places")
    lines.append("File them with `assign <project> --under <dir>` (or `--rest`), or `leave-out`.")
    return "\n".join(lines)


def _groups(paths: list[str]) -> list[tuple[str, int]]:
    """Undecided files grouped at the deepest level that still fits the screen."""
    normed = [norm(p) for p in paths]
    best: list[tuple[str, int]] = []
    for depth in range(1, 9):
        counts: dict[str, int] = {}
        for p in normed:
            parts = p.split("/")
            key = "/".join(parts[:depth]) if len(parts) > depth else p
            counts[key] = counts.get(key, 0) + 1
        groups = sorted(counts.items(), key=lambda kv: (-kv[1], kv[0]))
        if len(groups) > STATUS_MAX_LINES and best:
            break
        best = groups
        if len(groups) == len(normed):
            break
    return best


def show(ref: Reference, state: State, directory: str) -> str:
    rel = ref.relative(directory) if directory else ""
    if rel is None:
        raise Refused(f"{directory!r} is not inside {ref.root}")
    files = ref.under(rel)
    if not files:
        near = ref.nearest(rel)
        raise Refused(f"nothing in this {_scope(ref)} is at {directory!r}"
                      + (("; nearest: " + ", ".join(near)) if near else ""))
    prefix = rel + "/" if rel else ""
    rows: dict[str, list[str]] = {}
    for f in files:
        rest = norm(f)[len(prefix):] if norm(f).startswith(prefix) else norm(f)
        head = rest.split("/", 1)[0]
        rows.setdefault(head + ("/" if "/" in rest else ""), []).append(f)
    out = [f"{rel or '.'}: {len(files):,} files"]
    for name, members in sorted(rows.items())[:SHOW_MAX_LINES]:
        where = {_label(state.decided.get(m)) for m in members}
        out.append(f"  {name}  ({len(members):,})  -> {', '.join(sorted(where))}")
    if len(rows) > SHOW_MAX_LINES:
        out.append(f"  ... and {len(rows) - SHOW_MAX_LINES:,} more")
    return "\n".join(out)


def _label(decision: Decision | None) -> str:
    if decision is None:
        return "undecided"
    return decision.project if decision.kind is Kind.ASSIGNED else "left out"


# -- the command ---------------------------------------------------------------


def _parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(prog="probe-backfill-plan", add_help=True)
    sub = parser.add_subparsers(dest="cmd", required=True)

    def selectors(p, *, rest=True):
        group = p.add_mutually_exclusive_group(required=True)
        group.add_argument("--under", metavar="DIR")
        group.add_argument("--file", metavar="PATH")
        if rest:
            group.add_argument("--rest", action="store_true")

    p = sub.add_parser("assign", help="file files into a project")
    p.add_argument("project")
    selectors(p)
    p.add_argument("--low", action="store_true", help="you are unsure; a person checks these first")
    p.add_argument("--why", default="")

    p = sub.add_parser("leave-out", help="mark files as not research (not uploaded)")
    selectors(p)
    p.add_argument("--why", required=True)

    p = sub.add_parser("project", help="declare a new project")
    p.add_argument("slug")
    p.add_argument("--name", default="")
    p.add_argument("--description", default="")
    p.add_argument("--tag", action="append", default=[])

    p = sub.add_parser("note", help="say what files are (optional; never changes what uploads)")
    selectors(p, rest=False)
    p.add_argument("--text", required=True)

    p = sub.add_parser("apply", help="many operations from a JSONL file")
    p.add_argument("--from", dest="source", required=True, metavar="FILE")

    sub.add_parser("status", help="what is decided and what is not")
    p = sub.add_parser("show", help="what is under a directory")
    p.add_argument("directory", nargs="?", default="")
    return parser


def _op_from_args(args) -> dict:
    if args.cmd == "assign":
        return {"op": Op.ASSIGN.value, "project": args.project, "under": args.under,
                "file": args.file, "rest": args.rest, "low": args.low, "why": args.why}
    if args.cmd == "leave-out":
        return {"op": Op.LEAVE_OUT.value, "under": args.under, "file": args.file,
                "rest": args.rest, "why": args.why}
    if args.cmd == "project":
        return {"op": Op.PROJECT.value, "slug": args.slug, "name": args.name,
                "description": args.description, "tags": args.tag}
    return {"op": Op.NOTE.value, "under": args.under, "file": args.file, "notes": args.text}


def _clean(op: dict) -> dict:
    return {k: v for k, v in op.items() if v not in (None, False, "", [])}


class _Locked:
    """Serialise read-validate-append against parallel calls in one session."""

    def __init__(self, log: Path):
        self.path = log.parent / ".lock"
        self.fd = None

    def __enter__(self):
        self.path.parent.mkdir(parents=True, exist_ok=True)
        self.fd = os.open(self.path, os.O_RDWR | os.O_CREAT, 0o600)
        try:
            import fcntl
            fcntl.flock(self.fd, fcntl.LOCK_EX)
        except ImportError:  # pragma: no cover - Windows: one call at a time is the norm
            pass
        return self

    def __exit__(self, *exc):
        os.close(self.fd)


def _append(path: Path, op: dict) -> None:
    line = json.dumps({**_clean(op), "at": round(time.time(), 3)}, ensure_ascii=False) + "\n"
    with open(path, "a", encoding="utf-8") as fh:
        fh.write(line)


def main(argv: list[str] | None = None, *, out=None) -> int:
    out = out or sys.stdout
    ref_dir = os.environ.get(REF_ENV)
    log_env = os.environ.get(LOG_ENV)
    if not ref_dir or not log_env:
        print("probe-backfill-plan only runs inside a folder import's classifier session.", file=out)
        return 2
    try:
        ref = Reference.from_json((Path(ref_dir) / REF_FILE).read_text(encoding="utf-8"))
    except (OSError, ValueError, KeyError) as exc:
        print(f"the import's file list could not be read: {exc}", file=out)
        return 2
    log = Path(log_env)
    try:
        args = _parser().parse_args(argv)
    except SystemExit as exc:
        return int(exc.code or 0)

    with _Locked(log):
        state = replay(ref, read_log(log))
        if args.cmd == "status":
            print(status(ref, state), file=out)
            return 0
        if args.cmd == "show":
            try:
                print(show(ref, state, args.directory), file=out)
                return 0
            except Refused as exc:
                print(f"refused: {exc}", file=out)
                return 1
        ops = []
        if args.cmd == "apply":
            try:
                text = Path(args.source).read_text(encoding="utf-8")
            except OSError as exc:
                print(f"refused: cannot read {args.source}: {exc}", file=out)
                return 1
            for n, raw in enumerate(text.splitlines(), 1):
                if raw.strip():
                    try:
                        ops.append((n, json.loads(raw)))
                    except ValueError as exc:
                        ops.append((n, {"op": None, "_error": f"not JSON: {exc}"}))
        else:
            ops.append((0, _op_from_args(args)))

        refused = 0
        for n, op in ops:
            where = f"line {n}: " if n else ""
            try:
                if not isinstance(op, dict):
                    raise Refused("each line must be a JSON object")
                if op.get("_error"):
                    raise Refused(op["_error"])
                msg = apply(ref, state, op)
                _append(log, op)
                print(f"{where}{msg}", file=out)
            except Refused as exc:
                refused += 1
                _append(log.parent / REFUSED_FILE, {"op": str(op.get("op")) if isinstance(op, dict) else None,
                                                    "reason": str(exc)[:200]})
                print(f"{where}refused: {exc}", file=out)
        if ref.mode is not Mode.NOTE:
            left = sum(1 for f in ref.files if f not in state.decided)
            print(f"{left:,} undecided." if left else "0 undecided.", file=out)
        return 1 if refused else 0


if __name__ == "__main__":  # pragma: no cover - the launcher runs `main` directly
    raise SystemExit(main(sys.argv[1:]))
