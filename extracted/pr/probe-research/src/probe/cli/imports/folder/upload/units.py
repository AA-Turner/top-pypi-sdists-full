"""run the upload units (one project and its files each), agent-filed or written directly as a tail, and name what never got a manifest."""

from __future__ import annotations
import json
import os
import shutil
import sys
import uuid
from concurrent.futures import ThreadPoolExecutor, as_completed
from dataclasses import dataclass
from pathlib import Path

from ... import folder as bf
from . import ledger as ledger_mod
from .manifest import validate_manifest
from ..classify import plan as plan_mod
from ..classify import plan_tool as tool_mod
from ..agents import prompts as prompts
from ...agent_settings import AgentSettings, Lane, launch_kwargs

def _env_concurrency(name: str, default: int) -> int:
    raw = os.environ.get(name)
    if raw:
        try:
            return max(1, min(int(raw), 32))
        except ValueError:
            pass
    return default


#: How many import units run at once.
#:
#: This used to be 3 with the reason "the drain behind them is a single worker,
#: so more concurrency buys queue depth, not throughput". That reason is gone:
#: delivery now runs per finished unit against a drain that moves several
#: bodies at once. What bounds it now is the machine and the provider -- each
#: unit is a whole agent process paying its own context floor, and a provider
#: rate limit surfaces as unit failures, which the attempt cap turns into a
#: report rather than a loop.
UNIT_CONCURRENCY_DEFAULT = 6


def unit_concurrency() -> int:
    """Read per call, never captured at import.

    A module-level read is set once, at whatever moment this module happens to
    be imported, so an override applied afterwards -- a test monkeypatch, a
    wrapper that configures then imports -- is silently ignored with no error.
    """
    return _env_concurrency("PROBE_UNIT_WORKERS", UNIT_CONCURRENCY_DEFAULT)

#: Retained for callers that still name it. New code should call one of the
#: functions above -- they are bounded by different things, which is the whole
#: reason they stopped being one number.
DEFAULT_CONCURRENCY = UNIT_CONCURRENCY_DEFAULT

#: A unit that has not produced an event in this long is wedged. Long, because a
#: classification turn over a large evidence set legitimately thinks for
#: minutes; finite, because `timeout=None` means one stuck unit stalls an
#: overnight import and nobody finds out until morning.
UNIT_TIMEOUT_S = 45 * 60


@dataclass
class UnitOutcome:
    unit: ledger_mod.Unit
    ok: bool
    manifest: Path | None = None
    rows: int = 0
    detail: str = ""


# -- pass B ------------------------------------------------------------------


def run_unit(
    folder: Path,
    unit: ledger_mod.Unit,
    *,
    agent: bf.Agent,
    ledger: ledger_mod.Ledger,
    work_dir: Path,
    resume: str | None = None,
    stream=None,
    paint_to=None,
    sizes: dict[str, int] | None = None,
    agents: AgentSettings | None = None,
) -> UnitOutcome:
    """One unit: one project, one bounded set of files.

    A TAIL unit is fulfilled here without a model -- see `_fulfil_tail_unit`.

    The ledger is written BEFORE the agent starts and again when it stops. A
    unit recorded as started with no terminal record is the crash signal, and it
    is the only reason a resume knows the difference between "not begun" and
    "died halfway".

    `work_dir` is where the manifest goes, and it is deliberately NOT under the
    folder being imported: the agent may write here and nowhere else, so the
    import cannot leave a trace in the customer's directory.
    """
    manifest = work_dir / f"{unit.unit_id}.jsonl"
    if unit.kind is ledger_mod.UnitKind.TAIL:
        return _fulfil_tail_unit(unit, ledger=ledger, manifest=manifest, sizes=sizes or {})
    session = (resume or new_session_id()) if agent is bf.Agent.CLAUDE else None
    ledger.start_unit(unit.unit_id, session_id=session)

    # THE UPLOAD LIST IS CODE'S. Every file of the unit is on it before the
    # agent starts, so nothing the agent does or fails to do can drop one; the
    # agent only adds notes. Notes an older CLI's agent already wrote into this
    # unit's manifest are kept where they still name one of its files.
    sizes = sizes or {}
    notes_file = manifest.with_name(f"{unit.unit_id}.notes.json")
    notes = _manifest_notes(manifest, unit.paths)
    notes.update(_saved_notes(notes_file, unit.paths))
    ref = tool_mod.Reference(root=str(folder), mode=tool_mod.Mode.NOTE, files=unit.paths)
    state_paths = _plan_state(work_dir, f"notes-{unit.unit_id}-{uuid.uuid4().hex[:8]}")
    ref.write(state_paths.ref_dir)
    state_paths.log.parent.mkdir(parents=True, exist_ok=True)

    prompt = prompts.import_unit(
        root=folder,
        project=unit.project,
        paths=list(unit.paths),
        work_dir=str(work_dir),
    ) + _git_note(folder, work_dir)
    def launch():
        with bf.plan_tool_launcher(state_paths) as bin_dir:
            return bf.launch_agent(
                folder, prompt, agent=agent, workdir=work_dir,
                heading=f"Importing into {unit.project}", label=unit.project,
                total=unit.files, timeout=UNIT_TIMEOUT_S, stream=stream,
                session_id=session, resume=resume, paint_to=paint_to,
                path_prepend=bin_dir,
                # A relaunch's fresh session is not written to the ledger: that
                # would count as another attempt. A later retry resumes the
                # refused session, or restarts when it is missing (below).
                **launch_kwargs(agents, Lane.IMPORT),
            )

    is_ok, tail = launch()
    # The ledger start can survive a crash before Claude creates its local
    # session. Retry only its explicit missing-session diagnostic;
    # authentication, permissions, timeouts and arbitrary model errors are not
    # evidence that replaying from scratch is appropriate.
    if (
        not is_ok and resume and agent is bf.Agent.CLAUDE
        and f"No session found with session ID: {resume}"
        in {line.strip() for line in tail.splitlines()}
    ):
        ledger.finish_unit(unit.unit_id, ok=False, enqueued=0, error=tail.strip()[:1000])
        session, resume = new_session_id(), None
        ledger.start_unit(unit.unit_id, session_id=session)
        print(
            "Saved agent session is unavailable; restarting this batch from its reviewed files.",
            file=stream if stream is not None else sys.stdout, flush=True,
        )
        is_ok, tail = launch()
    written = tool_mod.replay(ref, tool_mod.read_log(state_paths.log))
    shutil.rmtree(state_paths.ref_dir, ignore_errors=True)
    notes.update(written.notes)
    if not is_ok:
        # No manifest for a crashed unit: the recovery paths treat a complete
        # manifest on disk as a finished unit and would upload it without the
        # retry. Its notes wait beside it (not `*.jsonl`, which is read as a
        # manifest) for the retry to start from.
        _save_notes(notes_file, notes)
        return _finish_failed_unit(unit, ledger, tail)
    _write_unit_manifest(folder, unit, manifest, sizes, notes)
    notes_file.unlink(missing_ok=True)
    checked = validate_manifest(manifest, unit.paths, root=folder)
    problems = [] if is_ok else [(tail.splitlines()[-1] if tail else "agent failed")[:1000]]
    if not checked.complete:
        is_ok = False
        problems.append(checked.describe())
    # A unit whose agent finished uploads EVERY file, whatever notes it wrote:
    # the list is code's. One whose agent crashed (above) uploads nothing yet
    # and is retried whole, as it always was: a file sent now would keep none
    # of the notes the retry writes (`Coverage.remember_manifest` settles a row
    # once it is queued).
    rows = len(checked.rows) if is_ok else 0
    detail = "; ".join(problems)
    ledger.finish_unit(
        unit.unit_id,
        ok=is_ok,
        enqueued=rows,
        error=None if is_ok else detail,
    )
    return UnitOutcome(
        unit=unit, ok=is_ok, manifest=manifest if rows else None, rows=rows,
        detail=detail,
    )


def write_unaccounted(index, work_dir: Path, outcomes: list[UnitOutcome]) -> Path | None:
    """Name the files the walk found and the import never manifested.

    Returns the path written, or None when nothing is missing (no file beats
    an empty one that reads as a failed write).

    Deliberately WALKED-vs-MANIFESTED and not walked-vs-landed. What landed is
    the server's answer and paging every artifact of every project back to
    subtract it is a real read path at 200k scale; what was manifested is on
    this disk, and it is the half that actually goes wrong -- a unit that died,
    a manifest a model wrote short, a file no assignment covered.
    """
    # PENDING, not `read()`: the index on disk still holds the previous walk
    # until `commit`, so reading it here would check this run's manifests
    # against the last run's file list.
    walked = {row.path for row in index.pending()} or {row.path for row in index.read()}
    if not walked:
        return None
    # EVERY manifest in the scratch directory, not just this run's outcomes.
    # A resume finishes the units an earlier run did not, so its `outcomes`
    # cover only those -- and diffing the whole walk against them named every
    # file the first run had already imported. The safeguard would have
    # reported thousands of false positives on exactly the runs that needed
    # it. The manifests on disk are the union of every run over this folder.
    manifests = set()
    try:
        manifests.update(work_dir.glob("*.jsonl"))
    except OSError:
        pass
    manifests.update(o.manifest for o in outcomes if o.manifest is not None)
    manifested: set[str] = set()
    for manifest in manifests:
        try:
            with manifest.open(encoding="utf-8") as fh:
                for line in fh:
                    line = line.strip()
                    if not line:
                        continue
                    try:
                        row = json.loads(line)
                    except ValueError:
                        continue
                    path = row.get("path")
                    if isinstance(path, str):
                        manifested.add(path)
        except OSError:
            continue
    missing = sorted(walked - manifested)
    if not missing:
        return None
    out = work_dir / "unaccounted.txt"
    try:
        out.write_text("\n".join(missing) + "\n", encoding="utf-8")
    except OSError:
        return None
    return out


def sizes_for_tails(folder: Path, ev, units: list[ledger_mod.Unit]) -> dict[str, int]:
    """Relative path -> bytes, for the reference/value decision in TAIL rows.

    From the evidence when there is any. On the RESUME path there is none --
    that path deliberately never re-walks -- so the sizes are stat'd back, for
    the TAIL units' paths only. One `stat` per checkpoint is nothing against
    uploading one, and the alternative is worse than slow: an unknown size
    reads as "under the reference threshold", which sends a 10GB checkpoint by
    VALUE. A file that has since vanished is left out and uploads by value,
    which is what a missing file does anyway.
    """
    if ev is not None:
        return plan_mod.sizes_by_path(ev)
    sizes: dict[str, int] = {}
    for unit in units:
        if unit.kind is not ledger_mod.UnitKind.TAIL:
            continue
        for rel in unit.paths:
            try:
                sizes[rel] = (folder / rel).stat().st_size
            except OSError:
                continue
    return sizes


def _manifest_notes(manifest: Path, paths: tuple[str, ...]) -> dict[str, str]:
    """Notes already in this unit's manifest, for its own files only."""
    wanted = set(paths)
    notes: dict[str, str] = {}
    try:
        lines = manifest.read_text(encoding="utf-8", errors="replace").splitlines()
    except OSError:
        return notes
    for line in lines:
        try:
            row = json.loads(line)
        except ValueError:
            continue
        if not isinstance(row, dict):
            continue
        path, text = row.get("path"), row.get("notes")
        if isinstance(path, str) and path in wanted and isinstance(text, str) and text.strip():
            notes[path] = text.strip()[:tool_mod.NOTE_MAX_CHARS]
    return notes


def _saved_notes(path: Path, paths: tuple[str, ...]) -> dict[str, str]:
    try:
        data = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, ValueError):
        return {}
    wanted = set(paths)
    return {p: str(t)[:tool_mod.NOTE_MAX_CHARS] for p, t in (data if isinstance(data, dict) else {}).items()
            if p in wanted and isinstance(t, str) and t.strip()}


def _save_notes(path: Path, notes: dict[str, str]) -> None:
    if not notes:
        return
    try:
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(json.dumps(notes, ensure_ascii=False), encoding="utf-8")
    except OSError:
        pass  # notes are optional; the retry writes them again


def _finish_failed_unit(unit: ledger_mod.Unit, ledger: ledger_mod.Ledger, tail: str) -> UnitOutcome:
    detail = (tail.splitlines()[-1] if tail.strip() else "agent failed")[:1000]
    ledger.finish_unit(unit.unit_id, ok=False, enqueued=0, error=detail)
    return UnitOutcome(unit=unit, ok=False, manifest=None, rows=0, detail=detail)


def _write_unit_manifest(
    folder: Path, unit: ledger_mod.Unit, manifest: Path, sizes: dict[str, int], notes: dict[str, str],
) -> None:
    """Every file of the unit, by code: the same rows a TAIL unit gets, plus notes.

    `reference` comes from size (`REFERENCE_ABOVE_BYTES`), the rule the prompt
    used to ask the model to apply. A size the walk did not record is read from
    disk; a file that is gone keeps its row and fails at enqueue, out loud.
    """
    known = dict(sizes)
    for path in unit.paths:
        if path not in known:
            try:
                known[path] = (folder / path).stat().st_size
            except OSError:
                known[path] = 0
    rows = plan_mod.tail_manifest(unit, known)
    manifest.parent.mkdir(parents=True, exist_ok=True)
    temp = manifest.with_suffix(".tmp")
    with temp.open("w", encoding="utf-8") as fh:
        for row in rows:
            text = notes.get(row["path"])
            if text:
                row = {**row, "notes": text}
            fh.write(json.dumps(row, ensure_ascii=False) + "\n")
    os.replace(temp, manifest)


def _fulfil_tail_unit(
    unit: ledger_mod.Unit,
    *,
    ledger: ledger_mod.Ledger,
    manifest: Path,
    sizes: dict[str, int],
) -> UnitOutcome:
    """Write a TAIL unit's manifest directly. No agent, no turn, no context.

    Ledger-wrapped exactly like an agent unit rather than short-circuited
    around it: the resume path, the delivery tracking and the recovery of a
    lost enqueue all read the ledger, and a unit that never appears there is a
    unit those three cannot see. The only thing that differs is who writes the
    rows.
    """
    ledger.start_unit(unit.unit_id)
    try:
        rows = plan_mod.tail_manifest(unit, sizes)
        with manifest.open("w", encoding="utf-8") as fh:
            for row in rows:
                fh.write(json.dumps(row, ensure_ascii=False) + "\n")
    except OSError as exc:
        ledger.finish_unit(unit.unit_id, ok=False, enqueued=0, error=str(exc))
        return UnitOutcome(unit=unit, ok=False, detail=str(exc))
    ledger.finish_unit(unit.unit_id, ok=True, enqueued=len(rows))
    return UnitOutcome(unit=unit, ok=True, manifest=manifest if rows else None,
                       rows=len(rows))


def _manifest_rows(path: Path) -> int:
    """How many usable rows a manifest carries.

    Counted here rather than trusted from the agent's summary, and tolerant of a
    torn final line for the same reason the ledger is: a killed agent should
    cost the row it was writing, not the manifest.
    """
    if not path.exists():
        return 0
    rows = 0
    try:
        for line in path.read_text(encoding="utf-8", errors="replace").splitlines():
            line = line.strip()
            if not line:
                continue
            try:
                row = json.loads(line)
            except ValueError:
                continue
            if isinstance(row, dict) and row.get("path"):
                rows += 1
    except OSError:
        return 0
    return rows


def run_units(
    folder: Path,
    units: list[ledger_mod.Unit],
    *,
    agent: bf.Agent,
    ledger: ledger_mod.Ledger,
    work_dir: Path,
    concurrency: int = DEFAULT_CONCURRENCY,
    sessions: dict[str, str] | None = None,
    stream=None,
    sizes: dict[str, int] | None = None,
    on_complete=None,
    agents: AgentSettings | None = None,
) -> list[UnitOutcome]:
    """Run units concurrently, bounded.

    `sizes` is relative-path -> bytes, needed only by TAIL units to decide
    which rows upload by reference.

    `on_complete` is called with each outcome AS IT FINISHES, on this thread --
    the caller's thread, never a worker. That is what lets delivery start while
    later units are still being read, and the thread it runs on is not an
    implementation detail: the caller's coverage store is a plain SQLite
    connection, so a worker calling this would raise rather than queue.
    Outcomes are still RETURNED in the order the units were given.

    `sessions` maps a unit id to a session to resume, so a unit interrupted
    mid-turn keeps what it had already read. The ledger decides WHICH units run;
    this only decides whether a rerun starts cold.

    Concurrent units share ONE screen through a `tui.Board` -- a row each,
    addressed absolutely. Left to themselves they all repaint the same line and
    two of the three are invisible.
    """
    if not units:
        return []
    from probe.cli.wizard import terminal as tui

    sessions = sessions or {}
    workers = max(1, min(concurrency, len(units)))

    board = None
    if stream is None and tui.interactive():
        board = tui.Board(
            f"Importing {len(units)} unit(s)",
            [f"{u.project[:24]:<26}" for u in units],
        )
        board.open()
        # EVERY ROW PAINTED UP FRONT. Only `concurrency` units start at once, so
        # a board headed "Importing 6 unit(s)" showed three lines and three
        # blanks -- and a blank row is indistinguishable from a row that is not
        # there, which reads as three units having vanished. Saying "queued" is
        # the difference between a queue and a bug.
        for index, unit in enumerate(units):
            board.update(index, bf.Activity(total=unit.files, queued=True).line(0.0))

    def one(pair: tuple[int, ledger_mod.Unit]) -> UnitOutcome:
        index, unit = pair
        return run_unit(
            folder, unit, agent=agent, ledger=ledger, work_dir=work_dir,
            resume=sessions.get(unit.unit_id), stream=stream,
            paint_to=board.row(index) if board else None,
            sizes=sizes, agents=agents,
        )

    pool = ThreadPoolExecutor(max_workers=workers)
    try:
        futures = [pool.submit(one, pair) for pair in enumerate(units)]
        if on_complete is None:
            return [f.result() for f in futures]
        positions = {future: index for index, future in enumerate(futures)}
        results: list[UnitOutcome | None] = [None] * len(futures)
        for future in as_completed(futures):
            outcome = future.result()
            results[positions[future]] = outcome
            on_complete(outcome)
        return [outcome for outcome in results if outcome is not None]
    except KeyboardInterrupt:
        # LEAVING MEANS LEAVING. `with ThreadPoolExecutor(...)` calls
        # shutdown(wait=True) on the way out, so a Ctrl-C here used to block
        # until every running agent finished on its own -- up to three of them,
        # each with a 45-minute deadline. Killing the agents is what actually
        # ends the wait: their threads then return instead of being waited on.
        bf.stop_all()
        for f in futures:
            f.cancel()
        pool.shutdown(wait=False)
        raise
    finally:
        pool.shutdown(wait=False)
        if board:
            board.close()
from probe.cli.imports.folder.classify.classify import _git_note, new_session_id  # noqa: E402 -- pieces need each other; the front door loads this one first
from probe.cli.imports.folder.classify.passes import _plan_state  # noqa: E402 -- pieces need each other; the front door loads this one first
