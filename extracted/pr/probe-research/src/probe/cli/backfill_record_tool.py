"""`probe` inside an import's record session: the commands the skills name, checked.

The record session (`backfill_record`) is the researcher's own agent reading
their skills verbatim (`track-work`, `write-summary`, `edit-notes`) over a
folder that was ALREADY imported. Those skills write with `probe` commands, so
the session gets a `probe` -- this one, first on its PATH -- that understands
the same commands, parsed by the CLI's own parser (`daemon.precheck.parse`,
the tree in `daemon/cli_spec.json`), and does with each one of three things:

    local     runs at once on a file in the agent's work dir: `notes checkout`,
              `summary checkout`, `draft edit`, `notes edit|append`,
              `summary edit`, and the reads (`run get|list`, `experiment
              get|list`, `project get`, `notes show`, `session status`),
              answered from the listing code wrote before the session.
    staged    a write to Probe: `run set`, `experiment set`, `project set
              --metric`, `notes push`, `summary push` (and the note an edit or
              append leaves). Checked
              now -- the entity must be one this import made, the field one a
              person has not written -- and appended to the op log
              (`backfill_oplog`); code applies the log after the session.
    refused   everything else, with the reason. Imports make no links
              (Richard 2026-10-27): `edge`, `experiment fork`, `--parent`,
              `checkpoint use`, `dataset use`, paper links. Nor do they upload,
              create, move or delete: code made the folder's projects,
              experiments, runs and files already.

No network, so it works in Codex's sandbox: the listing is a file code wrote
OUTSIDE the work dir (the agent can read it, not rewrite it); the documents and
the op log sit INSIDE it, because the sandbox confines this tool's writes too.

`probe batch --from FILE` runs many of these at once, one command's words per
line as a JSON array (`["run", "set", "a/b", "--name", "..."]`): a folder of a
thousand runs is named in a few calls, each line checked like a typed command.
"""

from __future__ import annotations

import difflib
import hashlib
import json
import os
import shlex
import sys
from pathlib import Path

from probe.cli import backfill_oplog as oplog

#: The listing (`listing.json`), written by the import outside the work dir.
LISTING_ENV = "PROBE_RECORD_LISTING"
#: The work dir: the op log and the checked-out documents live here.
WORK_ENV = "PROBE_RECORD_WORK"

LISTING_FILE = "listing.json"
LOG_FILE = "ops.jsonl"
DOCS_DIR = "probe"
REFUSED_FILE = "refused.jsonl"
LOCK_FILE = "ops.lock"
NEAREST = 3

NO_LINKS = ("imports make no links: an import has no record of what came from what, "
            "and a link is never guessed")
NOT_HERE = ("not part of recording an import: the import already made this folder's projects, "
            "experiments, runs and files. Here you write names, descriptions, notes, "
            "conclusions and pages")
LINK_COMMANDS = frozenset({"edge add", "edge remove", "experiment fork", "run fork", "run child", "checkpoint use",
                           "dataset use", "run link", "paper add", "paper update"})
LINK_OPTIONS = ("parent", "relation", "relates_to", "via", "relates_reason", "via_reason")
READS = frozenset({"run get", "run list", "experiment get", "experiment list", "project get",
                   "notes show", "session status"})


class Refused(Exception):
    pass


# -- the listing ---------------------------------------------------------------


class Listing:
    """What the import made, as code read it before the session."""

    def __init__(self, data: dict, work: Path):
        self.data = data
        self.work = work
        self.session = str(data.get("session") or "record")
        self.project = data.get("project") or {}
        self.experiments = list(data.get("experiments") or [])
        self.runs = list(data.get("runs") or [])
        writes = data.get("writes") or {}
        self.writes = {key: bool(writes.get(key, True)) for key in ("project", "experiments", "runs")}

    @classmethod
    def load(cls) -> Listing:
        listing = os.environ.get(LISTING_ENV)
        work = os.environ.get(WORK_ENV)
        if not listing or not work:
            raise Refused("this `probe` runs only inside an import's record session")
        return cls(json.loads(Path(listing).read_text(encoding="utf-8")), Path(work))

    # entities by any name the agent may type
    def run(self, ref: str | None) -> dict:
        ref = _strip(ref)
        for row in self.runs:
            if ref in (row.get("folder"), row.get("slug"), row.get("id")):
                return row
        raise Refused(_missing("run", ref, [r.get("folder") or "" for r in self.runs]
                               + [r.get("slug") or "" for r in self.runs]))

    def experiment(self, ref: str | None) -> dict:
        ref = _strip(ref)
        for row in self.experiments:
            if ref in (row.get("slug"), row.get("id"), row.get("under")):
                return row
        raise Refused(_missing("experiment", ref, [e.get("slug") or "" for e in self.experiments]))

    def project_row(self, ref: str | None) -> dict:
        ref = _strip(ref)
        if ref in (self.project.get("slug"), self.project.get("id")):
            return self.project
        raise Refused(_missing("project", ref, [self.project.get("slug") or ""]))

    def entity(self, params: dict) -> tuple[str, dict]:
        """`--project|--experiment|--run` -> (kind, row). Exactly one."""
        given = [(kind, params.get(kind)) for kind in ("project", "experiment", "run")
                 if params.get(kind)]
        if len(given) != 1:
            raise Refused("name exactly one of --project, --experiment or --run")
        kind, ref = given[0]
        if kind == "run":
            return kind, self.run(ref)
        if kind == "experiment":
            return kind, self.experiment(ref)
        return kind, self.project_row(ref)

    def writable(self, kind: str) -> None:
        group = {"project": "project", "experiment": "experiments", "run": "runs"}[kind]
        if not self.writes[group]:
            raise Refused(f"this session records {', '.join(k for k, v in self.writes.items() if v)} "
                          f"only; another session of this import writes {group}")

    # documents in the work dir
    def doc_path(self, kind: str, row: dict, ext: str) -> Path:
        """The entity's document in the work dir: a readable handle, then a hash of
        the entity itself, so two slugs that read alike never share a file."""
        identity = str(row.get("id") or row.get("folder") or row.get("slug"))
        digest = hashlib.sha256(f"{kind}\0{identity}".encode()).hexdigest()[:10]
        handle = row.get("slug") or row.get("folder") or "root"
        name = "".join(c if c.isalnum() or c in "-_" else "-" for c in str(handle))[:60]
        return self.work / DOCS_DIR / f"{kind}-{name}-{digest}{ext}"

    def docs(self) -> Path:
        """The documents folder, refused when it is not a plain folder in the work
        dir: a symlinked one would carry reads and writes outside it."""
        docs = self.work / DOCS_DIR
        if docs.is_symlink() or (docs.exists() and not docs.is_dir()):
            raise Refused(f"{docs} is not a plain folder; documents live only in the work dir")
        return docs

    def target(self, kind: str, row: dict) -> dict:
        if kind == "run":
            return oplog.target(kind, id=row.get("id"), folder=row.get("folder"),
                                slug=row.get("slug"))
        if kind == "experiment":
            return oplog.target(kind, id=row.get("id"), slug=row.get("slug"),
                                under=row.get("under"))
        return oplog.target(kind, id=row.get("id"), slug=row.get("slug"))

    def stage(self, kind: oplog.Kind, target_kind: str, row: dict, fields: dict,
              base_version: int | None = None) -> dict:
        """Append one op. Under a lock: the agent may run `probe` calls in
        parallel, and two that read the same next sequence would make one id,
        which the reader drops as a duplicate."""
        from probe.sdk.durable import file_lock

        log = self.work / LOG_FILE
        with file_lock(self.work / LOCK_FILE):
            op = oplog.make(kind, self.target(target_kind, row), fields, session=self.session,
                            seq=oplog.next_seq(log), base_version=base_version)
            oplog.append(log, op)
        return op


def _strip(ref: str | None) -> str:
    """The ref as the listing spells it. `.` is the folder's root (a run or an
    experiment whose folder is the whole import); nothing at all is refused."""
    ref = (ref or "").strip()
    if not ref:
        raise Refused("name the run by its folder, the experiment or project by its slug")
    if ref in (".", "./"):
        return ""
    return ref[3:] if ref.startswith("id:") else ref


def _missing(kind: str, ref: str, names: list[str]) -> str:
    near = difflib.get_close_matches(ref, [n for n in names if n], n=NEAREST, cutoff=0.4)
    tail = f"; nearest: {', '.join(near)}" if near else ""
    return f"no {kind} {ref!r} in this import{tail} (the listing names them all)"


# -- the documents -------------------------------------------------------------


def _plain(listing: Listing, path: Path) -> Path:
    """`path` as a document: a plain file (or none yet) in the documents folder.
    A symlink there would let a read or a push carry another file's text."""
    listing.docs()
    if path.is_symlink() or (path.exists() and not path.is_file()):
        raise Refused(f"{path} is not a plain file; documents are the files checkout printed")
    return path


def _note_doc(listing: Listing, kind: str, row: dict) -> Path:
    path = _plain(listing, listing.doc_path(kind, row, ".note.md"))
    if not path.exists():
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(row.get("notes") or "", encoding="utf-8")
    return path


def _page_doc(listing: Listing, kind: str, row: dict) -> Path:
    page = row.get("page")
    if not isinstance(page, dict):
        raise Refused(f"this {kind} has no page to write")
    path = _plain(listing, listing.doc_path(kind, row, ".page.html"))
    if not path.exists():
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(page.get("draft") or "", encoding="utf-8")
    return path


def _replace_once(path: Path, old: str, new: str) -> str:
    from probe import drafts

    try:
        return drafts.replace_once(path, old, new, str(path))
    except drafts.Refused as refused:
        if refused.kind is drafts.Refusal.MANY:
            raise Refused(f"the old text appears {refused.count} times; add text around it "
                          "so it matches once") from None
        if refused.kind is drafts.Refusal.EMPTY_OLD:
            raise Refused("the old text is empty") from None
        raise Refused(f"the old text is not in {path}; copy it exactly") from None


# -- the commands --------------------------------------------------------------


def _set_only(params: dict, allowed: tuple[str, ...], what: str) -> dict:
    """The fields a set command carries; refused for any other option given."""
    fields = {}
    for key, value in params.items():
        if value in (None, False, (), []):
            continue
        if key in allowed:
            fields[key] = str(value)
        elif key in LINK_OPTIONS:
            raise Refused(NO_LINKS)
        elif key == "authored_by":
            if value != "agent":
                raise Refused("an import's agent writes as `agent`, never for a person")
        elif key not in ("run", "experiment_id"):
            raise Refused(f"`{what}` here sets only {', '.join('--' + a for a in allowed)}; "
                          f"--{key.replace('_', '-')} is {NOT_HERE.split(':')[0]}")
    if not fields:
        raise Refused(f"give at least one of {', '.join('--' + a for a in allowed)}")
    return fields


def _unlocked(row: dict, fields: dict, kind: str) -> None:
    locked = set(row.get("locked") or ()) & set(fields)
    if locked:
        raise Refused(f"a person wrote this {kind}'s {', '.join(sorted(locked))}; leave it as it is")


def _run_set(listing: Listing, params: dict) -> dict:
    listing.writable("run")
    row = listing.run(params.get("run"))
    fields = _set_only(params, ("name", "description"), "probe run set")
    _unlocked(row, fields, "run")
    op = listing.stage(oplog.Kind.RUN_SET, "run", row, fields)
    row.update(fields)
    return {"staged": op["id"], "run": row.get("folder"), "fields": sorted(fields)}


def _experiment_set(listing: Listing, params: dict) -> dict:
    listing.writable("experiment")
    row = listing.experiment(params.get("experiment_id"))
    fields = _set_only(params, ("name", "question", "conclusion"), "probe experiment set")
    _unlocked(row, fields, "experiment")
    op = listing.stage(oplog.Kind.EXPERIMENT_SET, "experiment", row, fields)
    row.update(fields)
    return {"staged": op["id"], "experiment": row.get("slug"), "fields": sorted(fields)}


#: What a project's metric may be reduced by (`Client.set_project_metric`).
GOALS = ("max", "min")
REDUCES = ("final", "best")


def _project_set(listing: Listing, params: dict) -> dict:
    """`probe project set P --metric KEY --goal max|min [--reduce final|best]`:
    the headline metric track-work asks for, named from what the runs logged.
    Nothing else a project set carries is an import's: its description comes
    from its page, and picking the best experiment is the researcher's."""
    listing.writable("project")
    row = listing.project_row(params.get("project_id"))
    others = [key for key, value in params.items()
              if value not in (None, False, (), []) and key not in ("project_id", "metric", "goal",
                                                                     "reduce", "authored_by")]
    if others or not params.get("metric"):
        raise Refused("`probe project set` here sets only the headline metric: "
                      "--metric KEY --goal max|min [--reduce final|best]")
    if params.get("authored_by") not in (None, "agent"):
        raise Refused("an import's agent writes as `agent`, never for a person")
    key, goal, reduce = str(params["metric"]), params.get("goal"), params.get("reduce")
    if goal not in GOALS:
        raise Refused("--goal is max or min: say which way is better, it is never guessed")
    if reduce not in (None, *REDUCES):
        raise Refused("--reduce is final or best")
    logged = sorted({k for run in listing.runs for k in (run.get("metrics") or {})})
    if key not in logged:
        raise Refused(_missing("metric", key, logged).replace("in this import",
                                                              "logged by this import's runs"))
    op = listing.stage(oplog.Kind.PROJECT_METRIC, "project", row,
                       {"key": key, "goal": goal, "reduce": reduce})
    return {"staged": op["id"], "project": row.get("slug"), "metric": key, "goal": goal}


def _no_sub_note(params: dict) -> None:
    if params.get("note") or params.get("team"):
        raise Refused("an import writes each entity's main note only (no sub-notes, no team note)")


def _stage_note(listing: Listing, kind: str, row: dict, path: Path) -> dict | None:
    text = path.read_text(encoding="utf-8")
    if text == (row.get("notes") or "") and not row.get("_staged_note"):
        return None
    op = listing.stage(oplog.Kind.NOTE, kind, row, {"text": text},
                       base_version=int(row.get("notes_version") or 0))
    row["_staged_note"] = op["id"]
    return op


def _notes(listing: Listing, verb: str, params: dict, out: dict) -> dict:
    _no_sub_note(params)
    kind, row = listing.entity(params)
    label = row.get("slug") or row.get("folder")
    if verb == "show":
        path = _plain(listing, listing.doc_path(kind, row, ".note.md"))
        return {"target": kind, "label": label,
                "notes": path.read_text(encoding="utf-8") if path.exists() else row.get("notes") or ""}
    listing.writable(kind)
    path = _note_doc(listing, kind, row)
    if verb == "checkout":
        out["stderr"] = f"checked out {kind} note ({label})\n{path}"
        return {"target": kind, "label": label, "path": str(path),
                "version": int(row.get("notes_version") or 0)}
    if verb == "edit":
        if not params.get("old"):
            raise Refused("--old is empty")
        _replace_once(path, params["old"], params.get("new") or "")
    elif verb == "append":
        from probe.sdk.notes import append_to_document

        text = params.get("text") or ""
        if not text.strip():
            raise Refused("--text is empty")
        path.write_text(append_to_document(path.read_text(encoding="utf-8"), text), encoding="utf-8")
    op = _stage_note(listing, kind, row, path)
    return {"target": kind, "label": label, "pushed": False, "staged": op["id"] if op else None,
            "detail": "staged; applied after this session" if op else "no local edits"}


def _page_entity(listing: Listing, params: dict) -> tuple[str, dict]:
    if params.get("experiment"):
        return "experiment", listing.experiment(params["experiment"])
    if params.get("project"):
        return "project", listing.project_row(params["project"])
    raise Refused("pass --project P or --experiment E")


def _summary(listing: Listing, verb: str, params: dict, out: dict) -> dict:
    kind, row = _page_entity(listing, params)
    listing.writable(kind)
    path = _page_doc(listing, kind, row)
    page = row["page"]
    label = row.get("slug")
    if verb == "checkout":
        out["stderr"] = f"checked out {kind} summary ({label}) v{int(page.get('version') or 0)}"
        return {"target": kind, "label": label, "path": str(path), "version": int(page.get("version") or 0),
                "format": "html", "html": path.read_text(encoding="utf-8")}
    if verb == "edit":
        if not params.get("old"):
            raise Refused("--old is empty")
        _replace_once(path, params["old"], params.get("new") or "")
    elif verb == "append":
        raise Refused("edit the checked-out draft instead: `probe draft edit <path>`")
    text = path.read_text(encoding="utf-8")
    if text == (page.get("draft") or "") and not page.get("_staged"):
        return {"target": kind, "label": label, "pushed": False, "detail": "no local edits"}
    op = listing.stage(oplog.Kind.PAGE, kind, row, {"html": text},
                       base_version=int(page.get("version") or 0))
    page["_staged"] = op["id"]
    return {"target": kind, "label": label, "pushed": False, "staged": op["id"],
            "detail": "staged; applied after this session"}


def _draft_edit(listing: Listing, params: dict, stdin: str) -> str:
    from probe import drafts

    raw = str(params.get("path") or "")
    full = Path(os.path.expanduser(raw))
    full = full if full.is_absolute() else Path.cwd() / full
    real = Path(os.path.realpath(full))
    docs = Path(os.path.realpath(listing.docs()))
    if (not drafts.within(real, docs) or not real.is_file() or full.is_symlink()
            or not drafts.within(docs, Path(os.path.realpath(listing.work)))):
        raise Refused(f"`probe draft edit` changes only a draft `probe summary checkout` or "
                      f"`probe notes checkout` printed (under {docs})")
    try:
        old, new = drafts.parse_change(stdin)
    except drafts.Refused as refused:
        raise Refused(f"the change goes on stdin, as\n{drafts.EDIT_FORMAT}\n({refused.detail})") from None
    return _replace_once(real, old, new)


def _reads(listing: Listing, path: str, params: dict) -> dict | list:
    if path == "session status":
        return {"state": "on", "tracking": True, "writes_allowed": True,
                "detail": "recording a folder import: the listing says what it holds"}
    if path == "run get":
        return {k: v for k, v in listing.run(params.get("run")).items() if not k.startswith("_")}
    if path == "run list":
        rows = listing.runs
        if params.get("experiment"):
            slug = listing.experiment(params["experiment"]).get("slug")
            rows = [r for r in rows if r.get("experiment") == slug]
        return [{k: r.get(k) for k in ("folder", "slug", "experiment", "name", "status")} for r in rows]
    if path == "experiment get":
        return {k: v for k, v in listing.experiment(params.get("experiment_id")).items()
                if not k.startswith("_") and k != "page"}
    if path == "experiment list":
        return [{k: e.get(k) for k in ("slug", "name", "question", "under")} for e in listing.experiments]
    if path == "project get":
        return {k: v for k, v in listing.project_row(params.get("project_id")).items()
                if not k.startswith("_") and k != "page"}
    raise Refused(NOT_HERE)


def run_command(listing: Listing, argv: list[str], stdin: str = "") -> tuple[int, str, str]:
    """One `probe <argv>`: (exit code, stdout, stderr). Never raises for a refusal."""
    from probe.daemon import precheck

    out: dict = {}
    try:
        if argv[:1] == ["batch"]:
            return _batch(listing, argv[1:])
        if argv[:1] == ["mcp"]:
            raise Refused("Probe's MCP reads are not available here; the listing at "
                          f"{os.environ.get(LISTING_ENV)} holds this import, and `probe run get` "
                          "reads one run from it")
        try:
            parsed = precheck.parse(argv)
        except precheck.ParseError as exc:
            raise Refused(str(exc)) from None
        if parsed.help:
            return 0, "", "help is not available inside an import's record session"
        path, params = parsed.path, parsed.params
        if path in LINK_COMMANDS or any(params.get(key) for key in LINK_OPTIONS):
            raise Refused(NO_LINKS)
        if path in READS:
            result = _reads(listing, path, params) if path != "notes show" else _notes(
                listing, "show", params, out)
        elif path == "run set":
            result = _run_set(listing, params)
        elif path == "experiment set":
            result = _experiment_set(listing, params)
        elif path == "project set":
            result = _project_set(listing, params)
        elif path in ("notes checkout", "notes push", "notes edit", "notes append"):
            result = _notes(listing, path.split()[1], params, out)
        elif path in ("summary checkout", "summary push", "summary edit", "summary append"):
            result = _summary(listing, path.split()[1], params, out)
        elif path == "draft edit":
            return 0, _draft_edit(listing, params, stdin) + "\n", ""
        else:
            raise Refused(NOT_HERE)
    except Refused as refused:
        _note_refusal(listing, argv, str(refused))
        return 1, "", f"refused: {refused}\n"
    return 0, json.dumps(result, ensure_ascii=False, indent=2) + "\n", out.get("stderr", "")


def _batch(listing: Listing, argv: list[str]) -> tuple[int, str, str]:
    if len(argv) != 2 or argv[0] != "--from":
        raise Refused("usage: probe batch --from FILE (one command's words a line, as a JSON array)")
    lines = Path(argv[1]).read_text(encoding="utf-8").splitlines()
    done = refused = 0
    errors: list[str] = []
    for number, line in enumerate(lines, 1):
        if not line.strip():
            continue
        try:
            words = json.loads(line)
            if not (isinstance(words, list) and words and all(isinstance(w, str) for w in words)):
                raise ValueError
        except ValueError:
            refused += 1
            errors.append(f"line {number}: not a JSON array of words")
            continue
        if words[0] == "probe":
            words = words[1:]
        if words[:1] in (["batch"], ["draft"]):
            refused += 1
            errors.append(f"line {number}: `probe {words[0]}` cannot run inside a batch")
            continue
        code, _, err = run_command(listing, words)
        if code:
            refused += 1
            errors.append(f"line {number}: {err.strip()}")
        else:
            done += 1
    shown = "\n".join(errors[:20]) + (f"\n... and {len(errors) - 20} more" if len(errors) > 20 else "")
    summary = json.dumps({"ran": done, "refused": refused}) + "\n"
    return (1 if refused else 0), summary, (shown + "\n" if shown else "")


def _note_refusal(listing: Listing, argv: list[str], why: str) -> None:
    try:
        with open(listing.work / REFUSED_FILE, "a", encoding="utf-8") as handle:
            handle.write(json.dumps({"argv": argv[:3], "why": why[:200]}) + "\n")
    except OSError:
        pass


def finish(listing: Listing) -> int:
    """Stage every checked-out document that differs from what was staged last:
    the edits of an agent that forgot to push are not lost. Returns how many.
    Only plain files in a plain documents folder: never a symlink's target."""
    try:
        listing.docs()
    except Refused:
        return 0
    ops, _ = oplog.read(listing.work / LOG_FILE)
    last: dict[tuple, str] = {}
    for op in ops:
        if op["kind"] in (oplog.Kind.NOTE.value, oplog.Kind.PAGE.value):
            field = "text" if op["kind"] == oplog.Kind.NOTE.value else "html"
            last[(op["kind"], oplog.target_key(op["target"]))] = op["fields"].get(field)
    staged = 0
    groups = {"project": "project", "experiment": "experiments", "run": "runs"}
    for kind, rows in (("project", [listing.project]), ("experiment", listing.experiments),
                       ("run", listing.runs)):
        if not listing.writes[groups[kind]]:
            continue
        for row in rows:
            if not row:
                continue
            key = oplog.target_key(listing.target(kind, row))
            note = listing.doc_path(kind, row, ".note.md")
            if note.is_file() and not note.is_symlink():
                text = note.read_text(encoding="utf-8")
                if text != last.get((oplog.Kind.NOTE.value, key), row.get("notes") or ""):
                    listing.stage(oplog.Kind.NOTE, kind, row, {"text": text},
                                  base_version=int(row.get("notes_version") or 0))
                    staged += 1
            page_row = row.get("page")
            page = listing.doc_path(kind, row, ".page.html")
            if isinstance(page_row, dict) and page.is_file() and not page.is_symlink():
                text = page.read_text(encoding="utf-8")
                if text != last.get((oplog.Kind.PAGE.value, key), page_row.get("draft") or ""):
                    listing.stage(oplog.Kind.PAGE, kind, row, {"html": text},
                                  base_version=int(page_row.get("version") or 0))
                    staged += 1
    return staged


def _rehydrate(listing: Listing) -> None:
    """A later call sees what earlier calls staged (each call is a new process)."""
    ops, _ = oplog.read(listing.work / LOG_FILE)
    for op in ops:
        where = op["target"]
        try:
            if where["kind"] == "run":
                row = listing.run(where.get("folder"))
            elif where["kind"] == "experiment":
                row = listing.experiment(where.get("slug"))
            else:
                row = listing.project
        except Refused:
            continue
        if op["kind"] in (oplog.Kind.RUN_SET.value, oplog.Kind.EXPERIMENT_SET.value):
            row.update(op["fields"])
        elif op["kind"] == oplog.Kind.NOTE.value:
            row["_staged_note"] = op["id"]
        elif op["kind"] == oplog.Kind.PAGE.value and isinstance(row.get("page"), dict):
            row["page"]["_staged"] = op["id"]


def main(argv: list[str] | None = None, *, stdin=None, out=None, err=None) -> int:
    argv = list(sys.argv[1:] if argv is None else argv)
    out = out or sys.stdout
    err = err or sys.stderr
    try:
        listing = Listing.load()
    except Refused as refused:
        err.write(f"refused: {refused}\n")
        return 1
    _rehydrate(listing)
    text = ""
    if argv[:2] == ["draft", "edit"]:
        source = stdin if stdin is not None else sys.stdin
        text = "" if source is None or (hasattr(source, "isatty") and source.isatty()) else source.read()
    code, stdout, stderr = run_command(listing, argv, text)
    out.write(stdout)
    if stderr:
        err.write(stderr if stderr.endswith("\n") else stderr + "\n")
    return code


def launcher_script(listing: Path, work: Path) -> str:
    """The `probe` the record session runs. `-c` puts the work dir on sys.path,
    where the agent can write: that entry is dropped before anything imports."""
    src = str(Path(__file__).resolve().parents[2])
    boot = (
        "import sys; "
        "sys.path[:] = [p for p in sys.path if p not in ('', '.')]; "
        f"sys.path.insert(0, {src!r}); "
        "from probe.cli.backfill_record_tool import main; raise SystemExit(main())"
    )
    return (
        "#!/bin/sh\n"
        f"{LISTING_ENV}={shlex.quote(str(listing))}; export {LISTING_ENV}\n"
        f"{WORK_ENV}={shlex.quote(str(work))}; export {WORK_ENV}\n"
        "exec " + shlex.quote(sys.executable) + " -c " + shlex.quote(boot) + ' "$@"\n'
    )


if __name__ == "__main__":  # pragma: no cover
    raise SystemExit(main())
