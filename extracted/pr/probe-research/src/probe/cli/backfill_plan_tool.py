"""`probe-backfill-plan`: how a classifying agent files a folder without copying it.

The classifier used to answer with JSON naming every row of the evidence back,
"verbatim", "exactly once". On 2026-10-25 a 144,178-file folder went through 22
slices that way and the model retyped two of 200 random-hex directory names
wrong in slice 17. The reconcile called them invented paths, refused the whole
plan, and 52 minutes of classification were thrown away over two typos.

A model cannot be trusted to copy data reliably, so it no longer copies any. It
SELECTS: `assign <project> --under <dir>` files every file it owns under a
directory, `--file` one file, `--rest` whatever is still undecided;
`experiment --under <dir>` and `run --under <dir>` / `run --each-under <dir>`
name the folders that hold an experiment or runs, and code builds them from the
files (a run's numbers, config and times are read by code, never typed). Each call is
checked against the real file list at the moment it is made, so a name that
matches nothing is refused with the nearest real names while the agent can still
fix it -- the repair happens inside the turn instead of failing the run after it.

Projects follow the same rule. `project <slug>` declares a NEW one and refuses a
slug an existing project holds; `project --reuse <slug>` selects an EXISTING one,
checked against the workspace's real projects, nearest names on a miss. An
existing project is never a destination just by being named in `assign`: until
2026-10-26 it was, and two throwaway folders were filed into unrelated projects.

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
    #: A directory's files go into a new experiment of their project.
    EXPERIMENT = "experiment"
    #: A folder (or each folder under a directory) is one run.
    RUN = "run"


class Kind(str, Enum):
    ASSIGNED = "assigned"
    LEFT_OUT = "left_out"


#: Which operations each mode accepts. A filing session cannot invent a
#: project; a notes session cannot move a file.
_ALLOWED = {
    Mode.FILE: {Op.ASSIGN, Op.LEAVE_OUT, Op.EXPERIMENT, Op.RUN},
    Mode.CLASSIFY: {Op.ASSIGN, Op.LEAVE_OUT, Op.PROJECT, Op.EXPERIMENT, Op.RUN},
    Mode.REVISE: {Op.ASSIGN, Op.LEAVE_OUT, Op.PROJECT, Op.EXPERIMENT, Op.RUN},
    Mode.NOTE: {Op.NOTE},
}

_UUID = re.compile(r"\A[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}\Z")


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
    #: Project slugs files may be assigned to without declaring one: this
    #: folder's own projects (imported into before, its repository's code
    #: source, already-imported files' homes) and, past naming, the plan's.
    projects: tuple[str, ...] = ()
    #: Every project slug that already exists in the workspace. Never
    #: assignable as such: `project --reuse <slug>` selects one (a person
    #: confirms it), and `project <slug>` cannot declare one as new.
    existing: tuple[str, ...] = ()
    #: REVISE only: the plan being corrected, file -> decision dict.
    seed: dict[str, dict] = field(default_factory=dict)
    #: Files already imported into a project (their `seed` names it). They keep
    #: that project: an assignment or leave-out passes over them, and only
    #: `experiment`/`run` reach them, so a re-import never re-uploads a file to
    #: move it.
    fixed: tuple[str, ...] = ()
    #: Experiments and runs already planned (REVISE, or a re-import):
    #: `{"experiments": {slug: {...}}, "runs": {dir: {...}}}`.
    structure: dict = field(default_factory=dict)

    def __post_init__(self):
        self.mode = Mode(self.mode)
        self._fixed = frozenset(self.fixed)
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
            "projects": list(self.projects), "existing": list(self.existing), "seed": self.seed,
            "fixed": list(self.fixed), "structure": self.structure,
        }, ensure_ascii=False)

    @classmethod
    def from_json(cls, text: str) -> "Reference":
        data = json.loads(text)
        return cls(
            root=str(data["root"]), mode=Mode(data["mode"]),
            files=tuple(str(f) for f in data.get("files") or ()),
            projects=tuple(str(p) for p in data.get("projects") or ()),
            existing=tuple(str(p) for p in data.get("existing") or ()),
            seed={str(k): dict(v) for k, v in (data.get("seed") or {}).items()},
            fixed=tuple(str(f) for f in data.get("fixed") or ()),
            structure=dict(data.get("structure") or {}),
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

    def is_fixed(self, path: str) -> bool:
        return path in self._fixed

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
    #: Projects this session declared: slug -> {name, description, tags}. An
    #: existing project selected with `project --reuse` is `{slug, reuse: True}`:
    #: its name and description are the project's own, read by code.
    declared: dict[str, dict] = field(default_factory=dict)
    notes: dict[str, str] = field(default_factory=dict)
    #: Low-confidence selectors as the agent wrote them, for the review screen.
    unsure: list[str] = field(default_factory=list)
    #: Lines replay rejected. The tool never writes one, so these were written
    #: by hand or edited: counted, never applied.
    invalid: int = 0
    #: Lines replay accepted beyond the seed.
    accepted: int = 0
    #: Experiments this session named: slug -> {slug, project, name, question, under}.
    experiments: dict[str, dict] = field(default_factory=dict)
    #: Runs: folder -> {under, experiment, project}. One folder is one run.
    runs: dict[str, dict] = field(default_factory=dict)


def initial_state(ref: Reference) -> State:
    state = State()
    for path, data in ref.seed.items():
        if ref.exact(norm(path)):
            try:
                state.decided[ref.exact(norm(path))[0]] = Decision.from_dict(data)
            except (KeyError, ValueError):
                continue
    structure = ref.structure or {}
    for slug, spec in (structure.get("experiments") or {}).items():
        if isinstance(spec, dict):
            state.experiments[str(slug)] = dict(spec)
    for under, spec in (structure.get("runs") or {}).items():
        if isinstance(spec, dict):
            state.runs[str(under)] = dict(spec)
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


def _check_project(ref: Reference, state: State, project: str) -> None:
    """Refuse a destination this session may not file into (yet)."""
    allowed = set(ref.projects) | set(state.declared)
    if project in allowed:
        return
    can_declare = Op.PROJECT in _ALLOWED[ref.mode]
    if can_declare and project in ref.existing:
        # An existing project is never a destination by being named: the
        # classifier was told to "prefer" existing projects and filed two
        # throwaway folders into unrelated ones (2026-10-26).
        raise Refused(
            f"{project!r} is an existing project that holds other work. Select it with "
            f"`probe-backfill-plan project --reuse {project}` only if these files continue "
            "its work (a person confirms it); otherwise declare a new project.")
    listed = ", ".join(sorted(allowed)) or "(none yet)"
    extra = " Declare it first with `probe-backfill-plan project`." if can_declare else ""
    raise Refused(f"{project!r} is not a project here. Projects: {listed}.{extra}")


def _project(ref: Reference, state: State, op: dict) -> str:
    """Declare a new project, or select an existing one with `reuse`.

    Reuse is a SELECTION, checked against the workspace's real projects when
    it is made; a slug that matches none is refused with the nearest real ones.
    The model never types an existing slug into an answer nobody checks.
    """
    slug = str(op.get("slug") or "").strip()
    existing = set(ref.existing)
    if op.get("reuse"):
        if slug in ref.projects and slug in existing:
            return f"project {slug} already holds this folder's work; assign files to it"
        if slug in ref.projects or (slug in state.declared and not state.declared[slug].get("reuse")):
            raise Refused(f"{slug!r} is a new project in this plan, not an existing one; "
                          "assign files to it")
        if slug not in existing:
            near = difflib.get_close_matches(slug, sorted(existing), n=NEAREST, cutoff=0.5)
            hint = ("; nearest: " + ", ".join(near)) if near else (
                "" if existing else "; this workspace has no other projects")
            raise Refused(f"no existing project is called {slug!r}{hint}")
        state.declared[slug] = {"slug": slug, "reuse": True}
        return (f"existing project {slug} is available. A person confirms it on review; "
                "an import nobody reviews gives these files a new project instead")
    if not _SLUG.match(slug) or _UUID.match(slug):
        raise Refused(f"{slug!r} is not a usable slug (lowercase letters, digits and hyphens)")
    if slug in existing:
        if slug in ref.projects:
            raise Refused(f"{slug!r} already holds this folder's work; assign files to it")
        raise Refused(f"{slug!r} is an existing project's slug. Give the new project a slug of "
                      "its own; if these files continue that project's work, select it with "
                      f"`probe-backfill-plan project --reuse {slug}`")
    state.declared[slug] = {
        "slug": slug,
        "name": _text(op.get("name") or slug, 120, "the name"),
        "description": _text(op.get("description"), 1_000, "the description"),
        "tags": [str(t) for t in (op.get("tags") or []) if str(t).strip()][:8],
    }
    return f"project {slug} is available"


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
        return _project(ref, state, op)

    if kind is Op.EXPERIMENT:
        return _experiment(ref, state, op)
    if kind is Op.RUN:
        return _run(ref, state, op)

    files, label = _selection(ref, state, op)

    if kind is Op.NOTE:
        text = _text(op.get("notes"), NOTE_MAX_CHARS, "the note")
        if not text:
            raise Refused("the note is empty")
        for f in files:
            state.notes[f] = text
        return f"noted {len(files):,} file{'s' if len(files) != 1 else ''}"

    why = _text(op.get("why"), WHY_MAX_CHARS, "--why")
    kept = [f for f in files if ref.is_fixed(f)]
    if kept:
        files = [f for f in files if not ref.is_fixed(f)]
        if not files:
            return (f"{len(kept):,} file{'s' if len(kept) != 1 else ''} at {label} "
                    "already imported; they stay in their project")
    if kind is Op.LEAVE_OUT:
        if not why:
            raise Refused("say why with --why; a left-out file is not uploaded")
        new = Decision(Kind.LEFT_OUT, None, why)
        target = "left out"
    else:
        project = str(op.get("project") or "").strip()
        _check_project(ref, state, project)
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
    if kept:
        msg += f"; {len(kept):,} already imported stay in their project"
    return msg


# -- experiments and runs ------------------------------------------------------
#
# The model names WHICH folders; code reads everything else. An experiment or a
# run holds the files of ONE project, so every file under the folder must be
# decided first: assigned to that project, or left out.


def _folder(ref: Reference, raw) -> tuple[str, list[str]]:
    """A selected directory as (relative path, its files), or a refusal."""
    raw = str(raw or "").strip()
    if not raw:
        raise Refused("give the directory with --under")
    rel = ref.relative(raw)
    if rel is None:
        raise Refused(f"{raw!r} is not inside {ref.root}")
    files = ref.under(rel)
    if not files:
        near = ref.nearest(rel)
        raise Refused(f"nothing in this {_scope(ref)} is at {raw!r}"
                      + (("; nearest: " + ", ".join(near)) if near else ""))
    if files == ref.exact(rel):
        raise Refused(f"{raw!r} is a file; name the folder that holds it")
    return rel, files


def _one_project(state: State, files: list[str]) -> tuple[set[str], int]:
    """The projects these files are assigned to, and how many are undecided."""
    undecided = 0
    projects: set[str] = set()
    for f in files:
        decision = state.decided.get(f)
        if decision is None:
            undecided += 1
        elif decision.kind is Kind.ASSIGNED and decision.project:
            projects.add(decision.project)
    return projects, undecided


def _inside(child: str, parent: str) -> bool:
    return parent == "" or child == parent or child.startswith(parent + "/")


def _experiment(ref: Reference, state: State, op: dict) -> str:
    slug = str(op.get("slug") or "").strip()
    known = ", ".join(sorted(state.experiments)) or "(none yet)"
    if op.get("drop"):
        if slug not in state.experiments:
            raise Refused(f"{slug!r} is not an experiment here. Experiments: {known}.")
        del state.experiments[slug]
        for run in state.runs.values():
            if run.get("experiment") == slug:
                run["experiment"] = None
        return f"experiment {slug} dropped; its runs stay, in no experiment"
    if not _SLUG.match(slug) or _UUID.match(slug):
        raise Refused(f"{slug!r} is not a usable slug (lowercase letters, digits and hyphens)")
    project = str(op.get("project") or "").strip()
    _check_project(ref, state, project)
    allowed = set(ref.projects) | set(state.declared)
    if slug in allowed:
        raise Refused(f"{slug!r} is a project; give the experiment a slug of its own")
    question = _text(op.get("question"), 1_000, "--question")
    if not question:
        raise Refused("say what the experiment asks with --question")
    name = _text(op.get("name") or slug, 120, "the name")
    rel, files = _folder(ref, op.get("under"))
    projects, undecided = _one_project(state, files)
    if undecided:
        raise Refused(f"{undecided:,} files under {rel or '.'} are undecided; assign them first")
    if not projects:
        raise Refused(f"every file under {rel or '.'} is left out; an experiment needs files")
    if projects != {project}:
        raise Refused(f"files under {rel or '.'} are in {', '.join(sorted(projects))}; an "
                      f"experiment holds files of {project} only. Assign them, or pick a "
                      "narrower directory.")
    other = next((s for s, e in state.experiments.items() if e.get("under") == rel and s != slug), None)
    if other:
        raise Refused(f"{rel or '.'} is already experiment {other}; drop it first "
                      f"(`experiment --slug {other} --drop`)")
    state.experiments[slug] = {"slug": slug, "project": project, "name": name,
                               "question": question, "under": rel}
    return f"experiment {slug} in {project}: {len(files):,} files ({rel or '.'})"


def _run(ref: Reference, state: State, op: dict) -> str:
    given = [k for k in ("under", "each_under") if op.get(k) not in (None, False, "")]
    if len(given) != 1:
        raise Refused("give exactly one of --under <dir> or --each-under <dir>")
    rel, files = _folder(ref, op[given[0]])
    if op.get("drop"):
        gone = [d for d in state.runs if _inside(d, rel)]
        if not gone:
            raise Refused(f"no run is at or under {rel or '.'}")
        for d in gone:
            del state.runs[d]
        return f"dropped {len(gone):,} run{'s' if len(gone) != 1 else ''} ({rel or '.'})"
    experiment = str(op.get("experiment") or "").strip() or None
    if experiment is not None and experiment not in state.experiments:
        known = ", ".join(sorted(state.experiments)) or "(none yet)"
        raise Refused(f"{experiment!r} is not an experiment here. Experiments: {known}. "
                      "Declare it first with `probe-backfill-plan experiment`.")
    if given[0] == "under":
        folders = [rel]
    else:
        prefix = rel + "/" if rel else ""
        folders = sorted({prefix + norm(f)[len(prefix):].split("/", 1)[0]
                          for f in files if "/" in norm(f)[len(prefix):]})
        if not folders:
            raise Refused(f"{rel or '.'} has no folders inside; use --under for one run")
    accepted: list[tuple[str, str]] = []
    problems: list[str] = []
    empty = 0
    for folder in folders:
        projects, undecided = _one_project(state, ref.under(folder))
        if undecided:
            problems.append(f"{folder} ({undecided:,} undecided)")
            continue
        if not projects:
            empty += 1
            continue
        if len(projects) > 1:
            problems.append(f"{folder} (files in {', '.join(sorted(projects))})")
            continue
        project = projects.pop()
        if experiment is not None and state.experiments[experiment]["project"] != project:
            problems.append(f"{folder} (in {project}; experiment {experiment} is in "
                            f"{state.experiments[experiment]['project']})")
            continue
        overlap = next((d for d in state.runs if d not in folders and d != folder
                        and (_inside(d, folder) or _inside(folder, d))), None)
        if overlap is not None:
            problems.append(f"{folder} (overlaps run {overlap}; runs do not nest)")
            continue
        accepted.append((folder, project))
    if problems:
        more = f" and {len(problems) - 5:,} more" if len(problems) > 5 else ""
        raise Refused(f"{len(problems):,} of {len(folders):,} folders cannot be runs yet: "
                      + ", ".join(problems[:5]) + more
                      + ". A run holds the files of one project: assign them first, "
                      "or name other folders.")
    if not accepted:
        raise Refused(f"every file under {rel or '.'} is left out; nothing to make a run of")
    for folder, project in accepted:
        state.runs[folder] = {"under": folder, "experiment": experiment, "project": project}
    msg = (f"{len(accepted):,} run{'s' if len(accepted) != 1 else ''}"
           + (f" in experiment {experiment}" if experiment else "") + f" ({rel or '.'})")
    if empty:
        msg += f"; {empty:,} folder{'s' if empty != 1 else ''} with every file left out are not runs"
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
    if state.experiments or state.runs:
        lines.append(f"{len(state.experiments):,} experiment{'s' if len(state.experiments) != 1 else ''}"
                     + (" (" + ", ".join(sorted(state.experiments)) + ")" if state.experiments else "")
                     + f", {len(state.runs):,} run{'s' if len(state.runs) != 1 else ''}.")
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
    out = [f"{rel or '.'}: {len(files):,} files" + _marks(state, rel)]
    for name, members in sorted(rows.items())[:SHOW_MAX_LINES]:
        where = {_label(state.decided.get(m)) for m in members}
        out.append(f"  {name}  ({len(members):,})  -> {', '.join(sorted(where))}"
                   + _marks(state, prefix + name.rstrip("/")))
    if len(rows) > SHOW_MAX_LINES:
        out.append(f"  ... and {len(rows) - SHOW_MAX_LINES:,} more")
    return "\n".join(out)


def _marks(state: State, folder: str) -> str:
    """` [run]` / ` [experiment X]` beside a folder that is one."""
    marks = [f"experiment {slug}" for slug, e in sorted(state.experiments.items())
             if e.get("under") == folder]
    if folder in state.runs:
        run = state.runs[folder]
        marks.append("run" + (f" in {run['experiment']}" if run.get("experiment") else ""))
    return f"  [{'; '.join(marks)}]" if marks else ""


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

    p = sub.add_parser("project", help="declare a new project, or --reuse an existing one")
    p.add_argument("slug")
    p.add_argument("--reuse", action="store_true",
                   help="select the existing project <slug> (a person confirms it on review)")
    p.add_argument("--name", default="")
    p.add_argument("--description", default="")
    p.add_argument("--tag", action="append", default=[])

    p = sub.add_parser("experiment", help="file a directory's files into a new experiment")
    p.add_argument("--slug", required=True)
    p.add_argument("--project", default="")
    p.add_argument("--name", default="")
    p.add_argument("--question", default="")
    p.add_argument("--under", metavar="DIR", default="")
    p.add_argument("--drop", action="store_true", help="remove this experiment from the plan")

    p = sub.add_parser("run", help="make a folder one run, or each folder under a directory one run each")
    group = p.add_mutually_exclusive_group(required=True)
    group.add_argument("--under", metavar="DIR")
    group.add_argument("--each-under", metavar="DIR", dest="each_under")
    p.add_argument("--experiment", default="")
    p.add_argument("--drop", action="store_true", help="remove the runs at or under the directory")

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
        return {"op": Op.PROJECT.value, "slug": args.slug, "reuse": args.reuse, "name": args.name,
                "description": args.description, "tags": args.tag}
    if args.cmd == "experiment":
        return {"op": Op.EXPERIMENT.value, "slug": args.slug, "project": args.project,
                "name": args.name, "question": args.question, "under": args.under,
                "drop": args.drop}
    if args.cmd == "run":
        return {"op": Op.RUN.value, "under": args.under, "each_under": args.each_under,
                "experiment": args.experiment, "drop": args.drop}
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
