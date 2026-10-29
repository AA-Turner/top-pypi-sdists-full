"""The record pass: an imported project, recorded by the researcher's own skills.

A folder import used to be a second recorder with rules of its own: runs named
after their folders (1,008 of Tokenless's 1,032 were hex ids), one template
description for 93% of them, no notes, no conclusion on the experiments that
held the runs, and a page draft of cited claims that only an interactive run
ever published (prod, 2026-10-28). Live recording follows the researcher's
skills (`track-work`, `write-summary`, `edit-notes`); the import now does too:

    code builds the skeleton        projects, experiments, runs, files (as before)
    the record pass                 one session of the researcher's own agent per
                                    project, given those skills VERBATIM
                                    (`daemon.bite.skills_text`, main-agent
                                    version) and only mechanics around them
    the session's `probe`           `backfill_record_tool`: the commands the
                                    skills name, checked when typed; local
                                    documents edited at once, writes to Probe
                                    staged in an op log (`backfill_oplog`)
    code applies the log            names, descriptions, notes, conclusions and
                                    pages, CAS on documents, each op once

A project of more than `RUNS_PER_SESSION` runs is recorded by one session per
group of its experiments (they write experiments and runs), then one more for
the project's own page and note.

THREE ENTRY POINTS, so the T5 repair can run the pass where its data is:

    listing_for(client, ...)        what the import made, read from Probe
    run_sessions(listing, ...)      the agent sessions, OFFLINE: a listing in,
                                    op logs out, nothing applied
    apply_log(client, log, ...)     one op log applied through a client

`complete_record` is the import's: all three, per project, at most
`MAX_PROJECTS` per run, rotating. A failed session never fails the import: the
files are delivered, the project says "not recorded yet", the next run retries.
Imports make no links (Richard 2026-10-27): there is no evidence in a folder of
what came from what that the skills accept, and a link is never guessed.
"""

from __future__ import annotations

import hashlib
import json
import os
import re
import shutil
import stat
import tempfile
import uuid
from bisect import bisect_right
from collections import Counter
from datetime import datetime, timezone
from pathlib import Path

from ..sdk.durable import write_text_atomic
from ..sdk.secret_gate import CredentialBlocked, _redact_read
from . import backfill as bf
from . import backfill_oplog as oplog
from . import backfill_prompts as prompts
from . import backfill_record_tool as tool
from . import backfill_structure as structure
from .backfill_coverage import delivers_approved_bytes
from .import_agent_settings import AgentSettings, Lane, launch_kwargs, lane_settings

SCHEMA = "probe.backfill.record/1"
MAX_PROJECTS = 20
#: Runs one session names. Tokenless's largest project held 1,011; listed at
#: ~120 characters a run, 300 fit a session with room for its work.
RUNS_PER_SESSION = 300
#: One record session. A unit's 45 minutes bound an open-ended walk; this one
#: reads a bounded listing and the files it chooses.
RECORD_TIMEOUT_S = 45 * 60
MAX_FILES = 64
MAX_SAMPLE_BYTES = 4096
MAX_HASH_BYTES = 1024 * 1024
MAX_EXCERPT_BYTES = 40_000
#: One import note's share (the unit agents' one line about a file).
MAX_NOTE_CHARS = 240
MAX_RUN_NOTES = 3
#: The listing as the prompt shows it. The JSON beside it holds everything.
MAX_LISTING_CHARS = 120_000
META_PREFIX = "record:"
CURSOR_KEY = "record_cursor"
DONE_FILE = "done.json"

#: The record session's Claude allowlist: its one shell command is `probe`,
#: which resolves to `backfill_record_tool` first on its PATH; files are read
#: anywhere and written only in its work dir (the deny rule over the folder,
#: `backfill.readonly_settings`). Codex has no allowlist flag: its sandbox
#: confines writes to the work dir and has no network, and the tool needs none.
RECORD_TOOLS = "Bash(probe:*),Read,Glob,Grep,Write,Edit"


def _json(value) -> str:
    return json.dumps(value, ensure_ascii=False, sort_keys=True, default=str)


def _hash(value) -> str:
    return hashlib.sha256(_json(value).encode()).hexdigest()


def _now() -> str:
    return datetime.now(timezone.utc).isoformat()


# -- the files' evidence (moved from the retired claims draft) -----------------


def _file_role(relative: str) -> tuple[int, str]:
    """Navigation hints, never evidence that a document is authoritative/current."""
    path = Path(relative)
    name = path.stem.casefold()
    parts = [part.casefold() for part in path.parts]
    metadata = any(
        part.startswith(".") or part in {"vendor", "vendored", "third_party", "node_modules"}
        for part in parts
    )
    metadata |= bool(
        re.search(r"^(changelog|changes|history|license|licence|code.of.conduct|contributing)", name)
    )
    if metadata:
        return 5, "repository_metadata_or_history"
    if name == "readme" and len(parts) == 1:
        return 0, "project_overview"
    narrative = path.suffix.casefold() in {".md", ".markdown", ".rst", ".txt"}
    if narrative and re.search(r"(?:^|[_. -])(status|progress|handoff|as.built|current)(?:$|[_. -])", name):
        return 1, "status_or_handoff"
    if name == "readme":
        return 2, "component_overview"
    return (3, "documentation") if narrative else (4, "implementation_or_data")


def _read_sample(folder: Path, row: dict) -> tuple[str | None, str | None]:
    """A bounded excerpt of one delivered file, masked by the upload gate's own
    check, or `(None, why)`. Only the bytes that were approved and delivered:
    a file changed since is refused, never read."""
    relative = Path(row["path"])
    path = (folder / relative).resolve(strict=True)
    if relative.is_absolute() or not path.is_relative_to(folder.resolve()):
        raise ValueError("source outside approved folder")
    if path.suffix.lower() in {".jsonl", ".ndjson"}:
        return None, "event streams are not excerpted"
    with path.open("rb") as handle:
        info = os.fstat(handle.fileno())
        if not stat.S_ISREG(info.st_mode) or info.st_size > MAX_HASH_BYTES:
            return None, "binary or large file: metadata only"
        data = handle.read(MAX_HASH_BYTES + 1)
    if hashlib.sha256(data).hexdigest() != row["approved_hash"]:
        raise ValueError("source bytes differ from approved receipt")
    if b"\x00" in data:
        return None, "binary file: metadata only"
    try:
        data.decode("utf-8")
    except UnicodeDecodeError:
        return None, "non-UTF-8 file: metadata only"
    # The excerpt goes into a model's input: mask what the upload gate masked
    # (the stored artifact may be exactly that redaction), with the gate's own
    # check. Only text gets here, so no archive is opened.
    try:
        data, _ = _redact_read(data, scan_policy=None, full_scan=False)
    except CredentialBlocked:
        return None, "credential inspection refused: metadata only"
    text = data.decode("utf-8")
    if len(data) <= MAX_SAMPLE_BYTES:
        return text, None
    return data[:MAX_SAMPLE_BYTES].decode("utf-8", errors="ignore"), "excerpt truncated"


def _note(row: dict) -> str | None:
    """The unit agent's line about this file (`probe-backfill-plan note`), or None.

    Written by a model from the file's text, so masked by the same gate as an
    excerpt -- WHOLE, then cut: a cut first can split a token so the gate no
    longer recognises it, and its head reaches the model."""
    raw = row.get("manifest")
    if not raw:
        return None
    try:
        manifest = json.loads(raw)
    except (TypeError, ValueError):
        return None
    text = manifest.get("notes") if isinstance(manifest, dict) else None
    if not isinstance(text, str) or not text.strip():
        return None
    try:
        data, _ = _redact_read(" ".join(text.split()).encode("utf-8"), scan_policy=None, full_scan=False)
    except CredentialBlocked:
        return None
    return data.decode("utf-8", errors="ignore")[:MAX_NOTE_CHARS] or None


def _receipt(coverage, row: dict) -> dict:
    """The delivery receipt that proves `row`'s approved bytes reached Probe."""
    value = coverage.conn.execute(
        "SELECT receipt, intent FROM versions WHERE correlation=?", (row["correlation"],)
    ).fetchone()
    receipt = json.loads(value[0]) if value and value[0] else {}
    intent = json.loads(value[1]) if value and value[1] else {}
    if (
        receipt.get("state") != "delivered"
        or receipt.get("status") != "complete"
        or receipt.get("anchor_id") != row["project_id"]
        or intent.get("content_hash") != row["approved_hash"]
        or not delivers_approved_bytes(intent, receipt)
        or not receipt.get("artifact_id")
    ):
        raise ValueError(f"unverified receipt: {row['path']}")
    return receipt


def _project_rows(coverage, project_id: str) -> list[dict]:
    return [row for row in coverage.rows()
            if row.get("project_id") == project_id and not row.get("exclusion")
            and not (row.get("skipped") and not row.get("present"))]


def excerpts(coverage, folder: Path, project_id: str) -> tuple[list[dict], list[str]]:
    """`(excerpts, gaps)`: bounded, masked excerpts of the project's narrative
    files first (READMEs, status notes, docs), each with the unit agent's note
    when it has one. Only delivered files whose receipt proves their bytes."""
    rows = sorted(_project_rows(coverage, project_id), key=lambda row: row["path"])
    gaps: list[str] = []
    candidates = []
    for row in rows:
        try:
            receipt = _receipt(coverage, row)
        except (ValueError, KeyError):
            continue
        if receipt.get("is_reference"):
            continue
        candidates.append(row)
    candidates.sort(key=lambda row: (_file_role(row["path"])[0], _note(row) is None,
                                     len(Path(row["path"]).parts), row["path"]))
    out: list[dict] = []
    used = 0
    for row in candidates:
        if len(out) >= MAX_FILES:
            gaps.append("file excerpt limit reached")
            break
        try:
            sample, limitation = _read_sample(folder, row)
        except (OSError, ValueError):
            continue
        if limitation:
            gaps.append(f"{row['path']}: {limitation}")
        if not sample:
            continue
        if used + len(sample.encode()) > MAX_EXCERPT_BYTES:
            gaps.append("file excerpt byte limit reached")
            break
        used += len(sample.encode())
        note = _note(row)
        out.append({"path": row["path"], "role": _file_role(row["path"])[1], "text": sample,
                    **({"note": note} if note else {})})
    return out, gaps


def render_excerpts(items: list[dict], gaps: list[str]) -> str:
    if not items:
        return "No file excerpts: read the files you need by path."
    parts = ["FILES TO READ FIRST (bounded excerpts; read any other file by path):"]
    for item in items:
        note = f"  [import note: {item['note']}]" if item.get("note") else ""
        parts.append(f"--- {item['path']} ({item['role']}){note}\n{item['text'].rstrip()}")
    if gaps:
        parts.append("(" + "; ".join(gaps[:8]) + ")")
    return "\n\n".join(parts)


# -- what the import made, read from Probe -------------------------------------


def _locked(current: str | None, *, customized: bool, ours: tuple) -> bool:
    """A field a person wrote: customized, and not a value this import set."""
    return bool(customized and current and current not in {v for v in ours if v})


def _page(client, *, project: str, experiment: str | None = None) -> dict | None:
    """The page as a checked-out HTML draft (`summary_cli.compose_draft`), or
    None from a server without full pages: no page is written then."""
    from .summary_cli import compose_draft

    row = client.get_summary(project=project, experiment=experiment, format="html")
    if row.get("format") != "html" or not isinstance(row.get("html"), str):
        return None
    return {"draft": compose_draft(row["html"], row.get("series")),
            "version": int(row.get("version") or 0)}


def _all_runs(client, project_id: str) -> dict[str, dict]:
    rows: dict[str, dict] = {}
    cursor = None
    while True:
        page = client.list_runs(project_id=project_id, limit=200,
                                **({"cursor": cursor} if cursor else {}))
        for row in page.items:
            rows[str(row.get("id"))] = row
        cursor = page.next_cursor
        if not cursor or not page.items:
            return rows


def _run_notes(coverage, project_id: str, folders: list[str]) -> dict[str, list[str]]:
    """Per run folder, up to `MAX_RUN_NOTES` of the unit agents' file notes."""
    out: dict[str, list[str]] = {}
    ordered = sorted(folders, key=len, reverse=True)
    for row in _project_rows(coverage, project_id):
        note = _note(row)
        if not note:
            continue
        folder = next((f for f in ordered if row["path"] == f or row["path"].startswith(f + "/")), None)
        if folder is not None and len(out.setdefault(folder, [])) < MAX_RUN_NOTES:
            out[folder].append(f"{row['path'][len(folder) + 1:] or row['path']}: {note}")
    return out


def listing_for(client, coverage, project_id: str, *, applied: dict | None = None) -> dict:
    """What this import made in `project_id`, as the record session sees it:
    the project, the experiments and runs it created (`backfill_structure`),
    each with its current words, note and page, and which fields a person
    wrote (`locked`). `applied` is what earlier record passes wrote, field by
    field (`complete_record`): a value this import set is its own to change."""
    applied = applied or {}
    saved = coverage.meta(structure.META_KEY) or {}
    experiments = {under: spec for under, spec in (saved.get("experiments") or {}).items()
                   if spec.get("id") and spec.get("project_id") == project_id}
    runs = {under: spec for under, spec in (saved.get("runs") or {}).items()
            if spec.get("id") and spec.get("project_id") == project_id}
    project = client.get_project(project_id)
    slug_of = {}
    out_experiments = []
    for under, spec in sorted(experiments.items()):
        row = client.get_experiment(spec["id"], project_id=project_id)
        mine = applied.get(f"experiment:{under}") or {}
        slug = row.get("slug") or spec.get("slug")
        slug_of[under] = slug
        out_experiments.append({
            "id": spec["id"], "slug": slug, "under": under,
            "name": row.get("name"), "question": row.get("question"),
            "conclusion": row.get("conclusion"),
            "notes": row.get("notes") or "", "notes_version": int(row.get("notes_version") or 0),
            "locked": [field for field, ours in (("name", (spec.get("name"), spec.get("slug"), mine.get("name"))),
                                                 ("question", (spec.get("question"), mine.get("question"))))
                       if _locked(row.get(field), customized=True, ours=ours)],
            "page": _page(client, project=project_id, experiment=spec["id"]),
        })
    rows = _all_runs(client, project_id) if runs else {}
    notes_of = _run_notes(coverage, project_id, list(runs))
    placed = Counter(row["folder"] for row in coverage.planned_placements()
                     if row.get("level") == structure.Level.RUN.value)
    out_runs = []
    for under, spec in sorted(runs.items()):
        row = rows.get(str(spec["id"]))
        if row is None:
            continue  # trashed or gone since: nothing to record
        mine = applied.get(f"run:{under}") or {}
        basename = under.rsplit("/", 1)[-1] or "run"
        locked = []
        if _locked(row.get("name"), customized=bool(row.get("name_customized")),
                   ours=(basename, mine.get("name"))):
            locked.append("name")
        if _locked(row.get("description"), customized=bool(row.get("description_customized")),
                   ours=(mine.get("description"),)):
            locked.append("description")
        out_runs.append({
            "id": str(spec["id"]), "folder": under, "slug": row.get("slug"),
            "experiment": slug_of.get(spec.get("experiment")) if spec.get("experiment") else None,
            "name": row.get("name"), "description": row.get("description"),
            "notes": row.get("notes") or "", "notes_version": int(row.get("notes_version") or 0),
            "locked": locked, "status": row.get("status"),
            "metrics": row.get("summary_metrics") or {}, "config": row.get("config") or {},
            "started_at": row.get("started_at"), "ended_at": row.get("ended_at"),
            "files": placed.get(under, 0), "import_notes": notes_of.get(under, []),
        })
    return {
        "schema": SCHEMA,
        "folder": None,
        "project": {
            "id": project_id, "slug": project.get("slug"), "name": project.get("name"),
            "description": project.get("description"),
            "notes": project.get("notes") or "", "notes_version": int(project.get("notes_version") or 0),
            "page": _page(client, project=project_id),
        },
        "experiments": out_experiments,
        "runs": out_runs,
    }


# -- the listing as the prompt shows it ----------------------------------------


def _short(value, limit: int = 60) -> str:
    text = value if isinstance(value, str) else json.dumps(value, ensure_ascii=False, default=str)
    text = " ".join(text.split())
    return text if len(text) <= limit else text[: limit - 1] + "…"


def _numbers(metrics: dict, limit: int = 6) -> str:
    items = list(metrics.items())[:limit]
    more = f" +{len(metrics) - limit}" if len(metrics) > limit else ""
    return ", ".join(f"{key}={_short(value, 24)}" for key, value in items) + more


def _run_words(run: dict) -> str:
    """What the run is called now. A server placeholder (the run's own slug, never
    chosen by anyone) reads as having no name, so the session can see it."""
    name = run.get("name")
    named = f"name {_short(name, 80)!r}" if name and name != run.get("slug") else "no name yet"
    description = run.get("description")
    return named + (f", description {_short(description, 160)!r}" if description else ", no description")


def _run_line(run: dict) -> str:
    parts = [run["folder"], _run_words(run), str(run.get("status") or "?")]
    if run.get("metrics"):
        parts.append(_numbers(run["metrics"]))
    if run.get("config"):
        parts.append("config " + _numbers(run["config"], 4))
    parts.append(f"{run.get('files', 0)} files")
    line = "  - " + " · ".join(parts)
    if run.get("locked"):
        line += f" · a person wrote its {', '.join(run['locked'])}"
    for note in run.get("import_notes") or []:
        line += f"\n      note: {_short(note, 200)}"
    return line


def _experiment_summary(runs: list[dict]) -> str:
    status = Counter(str(r.get("status") or "?") for r in runs)
    ranges: dict[str, list[float]] = {}
    for run in runs:
        for key, value in (run.get("metrics") or {}).items():
            if isinstance(value, (int, float)) and not isinstance(value, bool):
                ranges.setdefault(key, []).append(float(value))
    parts = [f"{len(runs)} runs (" + ", ".join(f"{n} {s}" for s, n in status.most_common()) + ")"]
    for key, values in list(ranges.items())[:4]:
        parts.append(f"{key} {min(values):g}..{max(values):g} (mean {sum(values) / len(values):g})")
    return "; ".join(parts)


def render_listing(listing: dict, *, max_chars: int = MAX_LISTING_CHARS) -> str:
    project = listing["project"]
    lines = [f"PROJECT {project.get('slug')}: {project.get('name') or ''}".rstrip(),
             f"  description: {_short(project.get('description') or '(none)', 300)}"]
    runs_by: dict[str | None, list[dict]] = {}
    for run in listing.get("runs") or []:
        runs_by.setdefault(run.get("experiment"), []).append(run)
    summaries = listing.get("summaries") or {}
    for exp in listing.get("experiments") or []:
        lines.append(f"\nEXPERIMENT {exp['slug']} (folder {exp['under'] or '.'})")
        lines.append(f"  name: {_short(exp.get('name') or '', 200)}")
        lines.append(f"  question: {_short(exp.get('question') or '', 300)}")
        if exp.get("conclusion"):
            lines.append(f"  conclusion: {_short(exp['conclusion'], 400)}")
        if exp.get("locked"):
            lines.append(f"  a person wrote its {', '.join(exp['locked'])}")
        if exp["slug"] in summaries:
            lines.append(f"  runs: {summaries[exp['slug']]}")
        lines.extend(_run_line(run) for run in runs_by.get(exp["slug"], []))
    direct = runs_by.get(None) or []
    if direct:
        lines.append("\nRUNS FILED AT THE PROJECT")
        lines.extend(_run_line(run) for run in direct)
    text = "\n".join(lines)
    if len(text) > max_chars:
        text = text[:max_chars] + "\n... (the listing JSON holds the rest)"
    return text


# -- the sessions (offline: a listing in, op logs out) --------------------------


def sessions_for(listing: dict) -> list[dict]:
    """The sessions that record one project: one when it is small enough, else
    one per group of experiments (and of project-direct runs), each writing its
    experiments and runs, then one for the project's own page and note."""
    runs = listing.get("runs") or []
    every = {"project": True, "experiments": True, "runs": True}
    if len(runs) <= RUNS_PER_SESSION:
        return [{**listing, "writes": every}]
    by_exp: dict[str | None, list[dict]] = {}
    for run in runs:
        by_exp.setdefault(run.get("experiment"), []).append(run)
    sessions: list[dict] = []
    group: list[dict] = []
    count = 0

    def close():
        nonlocal group, count
        if group:
            slugs = {e["slug"] for e in group}
            sessions.append({**listing, "experiments": group,
                             "runs": [r for r in runs if r.get("experiment") in slugs],
                             "writes": {"project": False, "experiments": True, "runs": True}})
        group, count = [], 0

    for exp in listing.get("experiments") or []:
        n = len(by_exp.get(exp["slug"], []))
        if group and count + n > RUNS_PER_SESSION:
            close()
        group.append(exp)
        count += n
    close()
    direct = by_exp.get(None) or []
    for start in range(0, len(direct), RUNS_PER_SESSION):
        sessions.append({**listing, "experiments": [], "runs": direct[start:start + RUNS_PER_SESSION],
                         "writes": {"project": False, "experiments": False, "runs": True}})
    sessions.append({**listing, "runs": [],
                     "summaries": {e["slug"]: _experiment_summary(by_exp.get(e["slug"], []))
                                   for e in listing.get("experiments") or []},
                     "writes": {"project": True, "experiments": False, "runs": False}})
    return sessions


def _scope(writes: dict) -> str:
    if all(writes.values()):
        return ""
    if writes == {"project": True, "experiments": False, "runs": False}:
        return ("This session writes the PROJECT's page and note; earlier sessions of this "
                "import recorded its experiments and runs (summarised below).")
    return ("This session records the experiments and runs listed below; another session "
            "of this import writes the project's page and note.")


def _carry(sessions: list[dict], index: int, ops: list[dict]) -> None:
    """Later sessions see the names, questions and conclusions earlier ones staged."""
    for later in sessions[index + 1:]:
        for op in ops:
            if op["kind"] != oplog.Kind.EXPERIMENT_SET.value:
                continue
            for exp in later.get("experiments") or []:
                if exp.get("slug") == op["target"].get("slug"):
                    exp.update(op["fields"])


class SessionResult:
    def __init__(self, log: Path, ok: bool, detail: str = ""):
        self.log, self.ok, self.detail = log, ok, detail


def run_sessions(listing: dict, folder: Path, root: Path, *, agent: bf.Agent,
                 agents: AgentSettings | None = None, excerpts_text: str = "",
                 git_note: str = "", stream=None) -> list[SessionResult]:
    """Record one project's listing with the researcher's agent. OFFLINE: no
    client; the listing carries every current note and page, and the result is
    op logs, never applied. A session already finished in `root` is not run
    again (its log is returned as it stands)."""
    from probe import skill_versions
    from probe.daemon.bite import SHARED_SKILLS, skills_root, skills_text

    skills = skills_text(SHARED_SKILLS, reader=skill_versions.MAIN_AGENT)
    where_skills = str(skills_root() or "<skills folder>")
    folder = Path(folder)
    results: list[SessionResult] = []
    sessions = sessions_for(json.loads(_json(listing)))
    base = listing.get("session") or _hash([listing["project"].get("id"), str(root)])[:16]
    for index, data in enumerate(sessions):
        directory = root / f"s{index + 1}"
        work, ref = directory / "work", directory / "ref"
        log = work / tool.LOG_FILE
        done = directory / DONE_FILE
        if done.exists():
            results.append(SessionResult(log, True))
            ops, _ = oplog.read(log)
            _carry(sessions, index, ops)
            continue
        work.mkdir(parents=True, exist_ok=True, mode=0o700)
        ref.mkdir(parents=True, exist_ok=True, mode=0o700)
        data = {**data, "session": f"{base}-{index + 1}", "folder": str(folder)}
        listing_path = ref / tool.LISTING_FILE
        write_text_atomic(listing_path, _json(data), mode=0o600)
        session_listing = tool.Listing(data, work)
        tool._rehydrate(session_listing)
        pages = []
        for kind, rows in (("project", [data["project"]]), ("experiment", data.get("experiments") or [])):
            group = {"project": "project", "experiment": "experiments"}[kind]
            if not data["writes"][group]:
                continue
            for row in rows:
                if isinstance(row.get("page"), dict):
                    pages.append(f"{kind} {row.get('slug')}: {tool._page_doc(session_listing, kind, row)}")
        prompt = prompts.record(
            root=folder, project=str(data["project"].get("slug")), work_dir=str(work),
            listing_path=str(listing_path), listing=render_listing(data),
            excerpts=excerpts_text, pages=pages, skills_root=where_skills, skills=skills,
            scope=_scope(data["writes"]),
        ) + git_note
        bin_dir = tempfile.mkdtemp(prefix="probe-record-")
        try:
            launcher = Path(bin_dir) / "probe"
            launcher.write_text(tool.launcher_script(listing_path, work), encoding="utf-8")
            launcher.chmod(0o700)
            with open(os.devnull, "w") as discarded:
                ok, tail = bf.launch_agent(
                    folder, prompt, agent=agent, workdir=work,
                    tools=RECORD_TOOLS if agent is bf.Agent.CLAUDE else None,
                    heading=f"Recording {data['project'].get('slug')}",
                    label=str(data["project"].get("slug")), timeout=RECORD_TIMEOUT_S,
                    stream=stream, progress=False, raw_stream=discarded,
                    session_id=str(uuid.uuid4()) if agent is bf.Agent.CLAUDE else None,
                    path_prepend=bin_dir, **launch_kwargs(agents, Lane.RECORD),
                )
        finally:
            shutil.rmtree(bin_dir, ignore_errors=True)
        # Edits the agent made and never pushed are its edits all the same.
        tool.finish(tool.Listing(data, work))
        ops, _ = oplog.read(log)
        _carry(sessions, index, ops)
        if ok:
            write_text_atomic(done, _json({"at": _now(), "ops": len(ops)}), mode=0o600)
            results.append(SessionResult(log, True))
        else:
            last = (tail or "").strip().splitlines()[-1:] or ["the agent did not finish"]
            results.append(SessionResult(log, False, last[0][:300]))
    return results


# -- applying a log through a client -------------------------------------------


class ApplyStopped(Exception):
    """Probe could not be reached: the rest of the log waits for the next run."""


def _mask(text: str) -> str | None:
    """Outgoing text through the upload gate's own credential check."""
    try:
        data, _ = _redact_read(text.encode("utf-8"), scan_policy=None, full_scan=False)
    except CredentialBlocked:
        return None
    return data.decode("utf-8", errors="ignore")


def _find(listing: dict, target: dict) -> tuple[str, dict] | None:
    key = oplog.target_key(target)
    kind = target.get("kind")
    if kind == "project":
        project = listing["project"]
        return (kind, project) if key == oplog.target_key(
            oplog.target(kind, slug=project.get("slug"))) or target.get("id") == project.get("id") else None
    rows = listing.get("experiments" if kind == "experiment" else "runs") or []
    for row in rows:
        mine = (oplog.target(kind, folder=row.get("folder")) if kind == "run"
                else oplog.target(kind, slug=row.get("slug"), under=row.get("under")))
        if oplog.target_key(mine) == key:
            return kind, row
    return None


def _listed_version(row: dict, *, page: bool) -> int:
    """The version the listing saw: the trusted base of a document push."""
    if page:
        return int((row.get("page") or {}).get("version") or 0)
    return int(row.get("notes_version") or 0)


def _claimed_since(current: dict, row: dict, fields: dict) -> list[str]:
    """The fields a person claimed AFTER the listing was read: the run's
    `<field>_customized` is set and the text is no longer what the listing saw.
    A run's PATCH replaces a person's words even from an agent (only the claim
    flag is monotonic, `app/runs/router.py`), so the session's minutes are
    re-checked here, just before the write."""
    return sorted(field for field in fields
                  if current.get(f"{field}_customized") and current.get(field) != row.get(field))


def _transient(exc) -> bool:
    status = getattr(exc, "status", None)
    return status is None or status >= 500 or status == 429


def _push_document(client, listing: dict, kind: str, row: dict, text: str, base_version: int,
                   scratch: Path, *, page: bool) -> tuple[oplog.Outcome, str]:
    """One whole document (a note or a page) sent with its base version; a head
    that moved meanwhile is merged three ways once (`notes_file.push`), then
    sent again. A merge that conflicts is refused, never forced."""
    from probe.sdk import errors

    from . import notes_file
    from .note_sync import Paths, commit
    from .summary_cli import compose_draft

    project_id = listing["project"]["id"]
    entity = row.get("id")
    base_text = (row.get("page") or {}).get("draft", "") if page else (row.get("notes") or "")
    scratch.mkdir(parents=True, exist_ok=True, mode=0o700)
    where = Paths(document=scratch / "document", base=scratch / "base", meta=scratch / "meta.json",
                  lock=scratch / "lock", owner="", stamp=scratch / "owner")
    if not where.base.exists():
        # A fresh push: the listing's text is the base, the op's text the edit.
        # On a resume the scratch holds the last merge (its base the head it
        # merged with): sending the op's text again over that base would undo
        # what the person wrote meanwhile, so the merged draft is kept.
        commit(where, body=base_text, version=base_version, write_document=False)
        write_text_atomic(where.document, text, mode=0o600)
    elif not where.document.exists():
        write_text_atomic(where.document, text, mode=0o600)
    failure: dict = {}
    anchors = ({"project": project_id, "experiment": entity} if kind == "experiment"
               else {"project": project_id})

    def send(body: str, version, op_key):
        try:
            if page:
                answer = client.put_summary(html=body, expected_version=version, **anchors)
                return int(answer.get("version") or 0)
            answer = client._replace_notes(kind, entity, body, base_version=version, op_key=op_key)
            return int((answer or {}).get("notes_version") or 0)
        except errors.ConflictError:
            raise
        except errors.RosError as exc:
            failure["error"] = exc
            raise

    def fetch():
        if page:
            head = client.get_summary(format="html", **anchors)
            return compose_draft(head.get("html") or "", head.get("series")), int(head.get("version") or 0)
        if kind == "project":
            head = client.get_project(entity)
        elif kind == "experiment":
            head = client.get_experiment(entity, project_id=project_id)
        else:
            head = client.get_run(entity)
        return head.get("notes") or "", int(head.get("notes_version") or 0)

    label = f"{kind} {'page' if page else 'note'}"
    report = notes_file.push(where, send=send, fetch=fetch, label=label)
    if report.merged:
        # The head already says what this op says (a lost response replayed):
        # the merge only re-terminated the last line, so nothing is sent.
        merged, head = where.document.read_text(encoding="utf-8"), where.base.read_text(encoding="utf-8")
        if merged.rstrip("\n") == head.rstrip("\n"):
            return oplog.Outcome.UNCHANGED, ""
        report = notes_file.push(where, send=send, fetch=fetch, label=label)
    if "error" in failure and _transient(failure["error"]):
        raise ApplyStopped(type(failure["error"]).__name__)
    if report.pushed:
        return oplog.Outcome.APPLIED, ""
    if report.detail == "no local edits":
        return oplog.Outcome.UNCHANGED, ""
    return oplog.Outcome.REFUSED, str(report.detail or "not sent")[:300]


def apply_log(client, log: Path, listing: dict, *, scratch: Path | None = None) -> dict:
    """Apply one op log through `client`, each op once (`oplog.applied`).

    Every op is checked against `listing` -- an entity this import made, a
    field no person wrote -- before it is sent, and every text through the
    credential mask. Returns counts by outcome and kind, and `values`: what
    landed, field by field, so the next pass knows those words are its own.
    Raises `ApplyStopped` when Probe cannot be reached; what landed is kept."""
    from probe.sdk import agent_session, errors

    log = Path(log)
    ops, dropped = oplog.read(log)
    done_path = oplog.applied_path(log)
    done = oplog.applied(done_path)
    replaced = oplog.superseded(ops)
    counts: Counter = Counter()
    values: dict[str, dict] = {}
    scratch = scratch or log.parent.parent / "apply"
    counts["dropped"] += dropped
    for op in ops:
        if op["id"] in done:
            counts[f"{op['kind']}:{done[op['id']].get('outcome')}"] += 1
            continue
        if op["id"] in replaced:
            oplog.record_applied(done_path, op, oplog.Outcome.SUPERSEDED)
            continue
        found = _find(listing, op["target"])
        if found is None:
            oplog.record_applied(done_path, op, oplog.Outcome.REFUSED, "not an entity this import made")
            counts[f"{op['kind']}:refused"] += 1
            continue
        kind, row = found
        locked = set(row.get("locked") or ()) & set(op["fields"])
        fields = {key: _mask(value) for key, value in op["fields"].items()}
        if locked or any(value is None for value in fields.values()):
            why = (f"a person wrote its {', '.join(sorted(locked))}" if locked
                   else "the text holds a credential")
            oplog.record_applied(done_path, op, oplog.Outcome.REFUSED, why)
            counts[f"{op['kind']}:refused"] += 1
            continue
        try:
            if op["kind"] == oplog.Kind.RUN_SET.value:
                claimed = _claimed_since(client.get_run(row["id"]), row, fields)
                if claimed:
                    outcome, detail = oplog.Outcome.REFUSED, f"a person wrote its {', '.join(claimed)}"
                elif all(row.get(k) == v for k, v in fields.items()):
                    outcome, detail = oplog.Outcome.UNCHANGED, ""
                else:
                    client.update_run(row["id"], authored_by=agent_session.AUTHORSHIP_AGENT, **fields)
                    outcome, detail = oplog.Outcome.APPLIED, ""
            elif op["kind"] == oplog.Kind.PROJECT_METRIC.value:
                client.set_project_metric(row["id"], fields["key"], goal=fields["goal"],
                                          reduce=fields.get("reduce"))
                outcome, detail = oplog.Outcome.APPLIED, ""
            elif op["kind"] == oplog.Kind.EXPERIMENT_SET.value:
                if all(row.get(k) == v for k, v in fields.items()):
                    outcome, detail = oplog.Outcome.UNCHANGED, ""
                else:
                    client.update_experiment(row["id"], project_id=listing["project"]["id"],
                                             authored_by=agent_session.AUTHORSHIP_AGENT, **fields)
                    outcome, detail = oplog.Outcome.APPLIED, ""
            else:
                page = op["kind"] == oplog.Kind.PAGE.value
                text = fields["html" if page else "text"]
                # The version the document was checked out at comes from the
                # listing code read, never from the op: the log is in the agent's
                # work dir, and a forged version would pass a newer head's check.
                outcome, detail = _push_document(
                    client, listing, kind, row, text, _listed_version(row, page=page),
                    # One scratch per OP: a resume of this op finds its own merge,
                    # and another op on the same document starts from the listing.
                    scratch / hashlib.sha256(op["id"].encode()).hexdigest()[:24],
                    page=page)
        except ApplyStopped:
            raise
        except errors.RosError as exc:
            if _transient(exc):
                raise ApplyStopped(type(exc).__name__) from None
            outcome, detail = oplog.Outcome.REFUSED, f"{type(exc).__name__} {getattr(exc, 'status', '')}"
        oplog.record_applied(done_path, op, outcome, detail)
        counts[f"{op['kind']}:{outcome.value}"] += 1
        if outcome in (oplog.Outcome.APPLIED, oplog.Outcome.UNCHANGED) and op["kind"] in (
                oplog.Kind.RUN_SET.value, oplog.Kind.EXPERIMENT_SET.value):
            name = f"{kind}:{row.get('folder') if kind == 'run' else row.get('under')}"
            values.setdefault(name, {}).update(fields)
            row.update(fields)
    return {"counts": dict(counts), "values": values}


# -- the import's step -----------------------------------------------------------


def _line(slug: str, counts: dict, *, runs: int | None = None) -> str:
    def n(prefix: str) -> int:
        return sum(v for k, v in counts.items() if k.startswith(prefix) and k.endswith(":applied"))
    of = f" of {runs:,}" if runs is not None else ""
    parts = [f"{n('run_set'):,}{of} run(s) named or described", f"{n('experiment_set'):,} experiment(s) set",
             f"{n('note'):,} note(s)", f"{n('page'):,} page(s)"]
    if n("project_metric"):
        parts.append("its headline metric set")
    refused = sum(v for k, v in counts.items() if k.endswith(":refused"))
    tail = f"; {refused:,} write(s) refused" if refused else ""
    return f"{slug}: recorded by your skills — " + ", ".join(parts) + tail + "."


def complete_record(client, folder, coverage, git_bundle=None, *, agent: bf.Agent,
                    agents: AgentSettings | None = None, stream=None) -> list[str]:
    """Record every project this import filed files into, at most `MAX_PROJECTS`
    per run (rotating across runs). A project is recorded again only when the
    prompt, the agent's model or what the import made in it changed."""
    from .backfill_run import _git_note

    del git_bundle  # the session reads the git digest itself (`_git_note`)
    folder = Path(folder)
    projects = sorted({row["project_id"] for row in coverage.rows()
                       if row.get("project_id") and not row.get("exclusion")
                       and not (row.get("skipped") and not row.get("present"))})
    saved = coverage.meta(structure.META_KEY) or {}
    cursor = coverage.meta(CURSOR_KEY)
    start = bisect_right(projects, cursor) if isinstance(cursor, str) else 0
    ordered = projects[start:] + projects[:start]
    model = lane_settings(agents, agent, Lane.RECORD).model or "configured_default"
    lines: list[str] = []
    for project_id in ordered[:MAX_PROJECTS]:
        coverage.put_meta(CURSOR_KEY, project_id)
        meta_key = META_PREFIX + project_id
        state = coverage.meta(meta_key, {}) or {}
        made = sorted(
            [f"e:{under}:{spec.get('id')}" for under, spec in (saved.get("experiments") or {}).items()
             if spec.get("project_id") == project_id and spec.get("id")]
            + [f"r:{under}:{spec.get('id')}" for under, spec in (saved.get("runs") or {}).items()
               if spec.get("project_id") == project_id and spec.get("id")])
        key = _hash([prompts.RECORD_PROMPT_VERSION, getattr(agent, "value", str(agent)), model,
                     project_id, made])
        if state.get("key") == key and state.get("state") == "recorded":
            continue
        if state.get("key") != key:
            state = {"key": key, "applied": state.get("applied") or {}, "state": "pending"}
        slug = project_id
        try:
            listing = listing_for(client, coverage, project_id, applied=state.get("applied"))
            slug = listing["project"].get("slug") or project_id
            root = coverage.directory / "record" / project_id / key[:32]
            root.mkdir(parents=True, exist_ok=True, mode=0o700)
            items, gaps = excerpts(coverage, folder, project_id)
            state["state"] = "recording"
            coverage.put_meta(meta_key, state)
            results = run_sessions(listing, folder, root, agent=agent, agents=agents,
                                   excerpts_text=render_excerpts(items, gaps),
                                   git_note=_git_note(folder, root), stream=stream)
            counts: Counter = Counter()
            for result in results:
                applied = apply_log(client, result.log, listing)
                counts.update(applied["counts"])
                for name, fields in applied["values"].items():
                    state["applied"].setdefault(name, {}).update(fields)
            failed = [r for r in results if not r.ok]
            state.update(state="partial" if failed else "recorded", counts=dict(counts), at=_now())
            for field in ("error",):
                state.pop(field, None)
            coverage.put_meta(meta_key, state)
            lines.append(_line(slug, dict(counts), runs=len(listing.get("runs") or [])))
            if failed:
                lines.append(f"{slug}: {len(failed)} record session(s) did not finish "
                             f"({failed[0].detail}); the next import finishes it.")
        except ApplyStopped as stopped:
            state.update(state="partial", error=str(stopped))
            coverage.put_meta(meta_key, state)
            lines.append(f"{slug}: not recorded yet (Probe could not be reached: {stopped}); "
                         "the next import finishes it.")
        except Exception as exc:  # noqa: BLE001 - the files are delivered; recording retries
            state.update(state="failed", error=type(exc).__name__)
            coverage.put_meta(meta_key, state)
            lines.append(f"{slug}: not recorded yet ({type(exc).__name__}); the next import retries.")
    if len(projects) > MAX_PROJECTS:
        lines.append("Record limit reached; rerun to record the next projects.")
    return lines
