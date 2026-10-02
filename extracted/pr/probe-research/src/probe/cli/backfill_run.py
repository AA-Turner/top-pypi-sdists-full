"""The two-pass import: classify once, then upload in resumable units.

The shape exists to resolve a real conflict in the requirement. Files for one
line of work are scattered across directories, which wants ONE agent with the
whole folder in view. An import that runs for hours will be interrupted, which
wants MANY small agents you can resume. Those pull opposite ways, so the work is
split by what each half is good at:

    PASS A -- classify.  One agent, whole-folder view, uploads nothing. It sees
                         evidence (not a directory listing) and decides which
                         project each FILE belongs to. Completed local turns
                         can be reused when preparation is restarted.

    PASS B -- import.    One agent per unit, each told which project it is
                         filing into. Units are independent, so a crash costs
                         one unit rather than the run.

Between them sits a human, once, looking at the classification with the files
the agent was least sure about pulled to the top.

WHAT EACH HALF IS AUTHORITATIVE FOR, because getting this backwards is how a
backfill lies:

    the walk        how many files exist          (never the model)
    the agent       what they mean                (never the count)
    the ledger      which units are done          (never the agent's word)
    the outbox      what actually reached storage (never "the agent said so")

Agents do not upload. They write a manifest and one process enqueues it: a
process start plus a slug lookup per file is tens of CPU-hours before any bytes
move at the sizes this feature is for.
"""

from __future__ import annotations

import hashlib
import json
import os
import sys
import threading
import time
import uuid
from concurrent.futures import ThreadPoolExecutor, as_completed
from contextlib import contextmanager
from contextvars import ContextVar, copy_context
from dataclasses import dataclass, field
import functools
from pathlib import Path
from typing import TYPE_CHECKING

from . import backfill as bf

if TYPE_CHECKING:
    from .telemetry import TelemetryContext
from . import backfill_evidence as evidence_mod
from . import backfill_index as index_mod
from . import backfill_ledger as ledger_mod
from .backfill_manifest import validate_manifest
from . import backfill_plan as plan_mod
from . import backfill_prompts as prompts

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

#: How many assign slices run at once. Kept lower than the unit count on
#: purpose: a slice holds a 55k-token prompt, and this is the one phase where
#: every worker reads the same evidence set at the same time.
CLASSIFY_CONCURRENCY_DEFAULT = 3


def unit_concurrency() -> int:
    """Read per call, never captured at import.

    A module-level read is set once, at whatever moment this module happens to
    be imported, so an override applied afterwards -- a test monkeypatch, a
    wrapper that configures then imports -- is silently ignored with no error.
    """
    return _env_concurrency("PROBE_UNIT_WORKERS", UNIT_CONCURRENCY_DEFAULT)


def classify_concurrency() -> int:
    return _env_concurrency("PROBE_CLASSIFY_WORKERS", CLASSIFY_CONCURRENCY_DEFAULT)

#: Retained for callers that still name it. New code should call one of the
#: functions above -- they are bounded by different things, which is the whole
#: reason they stopped being one number.
DEFAULT_CONCURRENCY = UNIT_CONCURRENCY_DEFAULT

#: A unit that has not produced an event in this long is wedged. Long, because a
#: classification turn over a large evidence set legitimately thinks for
#: minutes; finite, because `timeout=None` means one stuck unit stalls an
#: overnight import and nobody finds out until morning.
UNIT_TIMEOUT_S = 45 * 60

#: The classify pass gets its own, larger deadline: it reads the whole evidence
#: set in one turn and there is exactly one of it.
CLASSIFY_TIMEOUT_S = 90 * 60


def new_session_id() -> str:
    """A session id Claude Code will accept.

    `str(uuid4())`, NOT `uuid4().hex`. `--session-id` validates the DASHED
    canonical form and rejects the 32-char hex with "Invalid session ID. Must be
    a valid UUID" -- which kills the agent before it reads a single file, so the
    classify pass returns no plan and the import stops having done nothing.

    Caught by the first real end-to-end run and by nothing before it: every test
    fakes `launch_agent`, so the id never reached the binary that validates it.
    """
    return str(uuid.uuid4())


@dataclass
class UnitOutcome:
    unit: ledger_mod.Unit
    ok: bool
    manifest: Path | None = None
    rows: int = 0
    detail: str = ""


@dataclass
class Report:
    """What the caller pages at the end."""

    lines: list[str] = field(default_factory=list)
    projects: list[str] = field(default_factory=list)
    units_done: int = 0
    units_total: int = 0
    enqueued: int = 0

    def add(self, *lines: str) -> None:
        self.lines.extend(lines)


# -- pass A ------------------------------------------------------------------


class _ReadProgress:
    """Measured preparation phases, separate from agent tool-read activity.

    Evidence is already inline in these prompts, so a Read-tool counter cannot
    tell us how many files the model has understood. Only successful slice
    answers advance these bars. A single board owns every concurrent call.
    """

    def __init__(self, folder: Path, files: int, slices: int, stream=None):
        self.out = stream if stream is not None else sys.stdout
        self.phases = ([('survey', 'Read samples', slices),
                        ('name', 'Identify projects', 1),
                        ('assign', 'Prepare file plan', slices)] if slices else
                       [('classify', 'Prepare file plan', 1)])
        self.activity_row = len(self.phases) + 3
        self.guidance_row = self.activity_row + 1
        self.completed: set[tuple[str, str]] = set()
        self.active: dict[tuple[str, str], str] = {}
        self.lock = threading.RLock()
        self.board = None
        self.files = files
        self.folder = folder
        context = _classification_context.get()
        self.background = bool(context and context.background)
        self.auto_approve = bool(context and context.auto_approve)
        self.progress = context.progress if context is not None else None
        self.cancelled = threading.Event()
        self.closed = False

    def __enter__(self):
        from . import tui

        if hasattr(self.out, 'isatty') and self.out.isatty():
            self.board = tui.Board(
                f'Scan and prepare {self.folder.name}', [''] * (self.guidance_row + 2), out=self.out,
            )
            self.board.open()
            self.board.update(0, f'Backfill 1 of 3 · {self.files:,} files found')
            self.board.update(
                self.guidance_row,
                'Automatic import is approved for this folder.' if self.auto_approve else
                'Next: review and approve the plan before anything uploads.',
            )
            self.board.update(
                self.guidance_row + 1,
                'The import starts after preparation finishes.' if self.auto_approve else
                ('After approval, the import runs in the background.' if self.background else
                 'Nothing has been uploaded. You can cancel at the review.'),
            )
            self._paint()
        else:
            self.out.write(
                f'  Scanning {self.files:,} files. '
                + ('Automatic import is approved and starts after preparation.\n'
                   if self.auto_approve else
                   'Review and approve the plan next; the import starts only after approval.\n')
            )
            self.out.flush()
        self.token = _read_progress.set(self)
        return self

    def __exit__(self, *exc):
        _read_progress.reset(self.token)
        with self.lock:
            self.closed = True
            if self.board is not None:
                self.board.close(erase=True)

    def _paint(self):
        from . import tui

        if self.board is None or self.closed:
            return
        for row, (phase, label, total) in enumerate(self.phases, start=2):
            done = sum(key[0] == phase for key in self.completed)
            bar = tui.progress_bar(done / max(1, total), width=12)
            unit = 'slices' if phase in {'survey', 'assign'} else 'step'
            line = f'{label:<20} {bar} {done}/{total} {unit}'
            self.board.update(row, line)
        # The current activity is liveness, never an inferred file percentage.
        activity = next(reversed(self.active.values()), '') if self.active else ''
        self.board.update(self.activity_row, activity)

    def _notify(self, phase: str, *, cached: bool = False):
        """Persist measured phase changes, never spinner ticks or guessed files."""
        if self.progress is None or self.closed:
            return
        stage = next((item for item in self.phases if item[0] == phase), None)
        if stage is None:
            return
        _, label, stage_total = stage
        stage_completed = sum(key[0] == phase for key in self.completed)
        self.progress(
            f"Scanning · {label.lower()} · {stage_completed}/{stage_total}",
            phase="scanning", completed=len(self.completed),
            total=sum(item[2] for item in self.phases),
            stage=phase, stage_completed=stage_completed, stage_total=stage_total,
            cached=cached,
        )

    def begin(self, phase: str, heading: str):
        with self.lock:
            self.active[phase, heading] = heading
            self._paint()
            self._notify(phase)

    def finish(self, phase: str, heading: str, *, success: bool, cached: bool = False):
        with self.lock:
            self.active.pop((phase, heading), None)
            if success:
                self.completed.add((phase, heading))
            self._paint()
            self._notify(phase, cached=cached)
            if self.board is None:
                result = 'reused saved result' if cached else ('complete' if success else 'failed')
                self.out.write(f'  {heading} · {result}\n')
                self.out.flush()

    def activity(self, phase: str, heading: str):
        if self.board is None:
            return None

        def paint(text):
            with self.lock:
                if not self.closed:
                    self.active[phase, heading] = text.strip()
                    self._paint()

        return paint


_read_progress: ContextVar[_ReadProgress | None] = ContextVar(
    'backfill_read_progress', default=None,
)

# Survey calls are independent, but each has a full model context. Two at a
# time reduces waiting without increasing the context floor or request count.
SURVEY_CONCURRENCY = 2


def _classification_results(worker, numbered, *, workers):
    """Run independent slices; Ctrl-C cancels queued work before leaving."""
    pool = ThreadPoolExecutor(max_workers=max(1, min(workers, len(numbered))))
    futures = []
    try:
        # A Context cannot be entered by two threads simultaneously.
        futures = [pool.submit(copy_context().run, worker, pair) for pair in numbered]
        return sorted(future.result() for future in futures)
    except BaseException:
        progress = _read_progress.get()
        if progress is not None:
            progress.cancelled.set()
        for future in futures:
            future.cancel()
        bf.stop_all()
        raise
    finally:
        # Waiting before stopping the children strands Ctrl-C behind a model
        # turn. Successful futures have already returned above.
        pool.shutdown(wait=False, cancel_futures=True)


class _ClassificationProgress:
    """One bounded callback per measured change, shared across worker threads."""

    def __init__(self, callback):
        self.callback = callback
        self.last = None
        self.lock = threading.Lock()

    def __call__(self, message, **fields):
        measured = tuple(fields.get(key) for key in (
            "phase", "completed", "total", "stage", "stage_completed", "stage_total",
        ))
        with self.lock:
            if measured != self.last:
                self.callback(message, **fields)
                self.last = measured


@dataclass(frozen=True)
class _ClassificationContext:
    identity: str
    progress: object = None
    background: bool = False
    auto_approve: bool = False


_classification_context: ContextVar[_ClassificationContext | None] = ContextVar(
    "backfill_classification_context", default=None,
)
_PREP_CACHE_VERSION = 1
_PREP_CACHE_ENTRY_BYTES = 8 * 1024 * 1024
_PREP_CACHE_BYTES = 128 * 1024 * 1024
_PREP_CACHE_ENTRIES = 2048


@contextmanager
def classification_context(
    identity: str, progress=None, *, background: bool = False, auto_approve: bool = False,
):
    """Reuse completed local classification turns within an observed source scope.

    The caller supplies a stable identity covering the destination, source scope
    and FULL observed file hashes, not only the samples in an evidence prompt.
    Revision jobs also include their base plan/correction lineage in that scope.
    Nothing is uploaded or approved here. Without this context, classification
    keeps its ordinary uncached behavior. Each worker attempt must enter it anew.
    `auto_approve` only describes the caller's already authorized mode; it does
    not grant approval or change how the classifier runs.
    """
    token = _classification_context.set(_ClassificationContext(
        identity, _ClassificationProgress(progress) if progress is not None else None,
        background, auto_approve,
    ))
    # The same work directory can be reused after Git/GitHub context changes.
    _git_note.cache_clear()
    try:
        yield
    finally:
        _classification_context.reset(token)


def _classification_progress(heading: str, phase: str, *, cached: bool = False) -> None:
    # A shared scan owner reports aggregate completion for every slice. Per-turn
    # headings must not replace that durable state with a different denominator.
    if _read_progress.get() is not None:
        return
    context = _classification_context.get()
    if context is not None and context.progress is not None:
        message = f"{heading} — reusing saved result" if cached else heading
        done = int(cached)
        context.progress(
            message, phase="scanning", completed=done, total=1,
            stage=phase, stage_completed=done, stage_total=1, cached=cached,
        )


def _classification_cache_path(
    work_dir: Path, *, agent: bf.Agent, prompt: str, phase: str, extra=None,
) -> Path | None:
    context = _classification_context.get()
    if context is None:
        return None
    # Git history is referenced by PATH in the prompt. Hash its bytes too, or a
    # new commit would leave the prompt key unchanged. Reads remain bounded.
    attachments = {}
    for name in ("git-history.md", "github-context.txt"):
        try:
            with (work_dir / name).open("rb") as handle:
                data = handle.read(128 * 1024 + 1)
            if len(data) > 128 * 1024:
                return None
            attachments[name] = hashlib.sha256(data).hexdigest()
        except FileNotFoundError:
            attachments[name] = None
        except OSError:
            return None
    key = json.dumps(
        {"version": _PREP_CACHE_VERSION, "identity": context.identity,
         "agent": agent.value, "prompt": prompt, "phase": phase,
         "attachments": attachments, "extra": extra},
        sort_keys=True, separators=(",", ":"), allow_nan=False,
    )
    return work_dir / "prep-cache" / f"{hashlib.sha256(key.encode()).hexdigest()}.json"


def _read_classification_cache(path: Path | None) -> dict | None:
    if path is None:
        return None
    try:
        with path.open("rb") as handle:
            raw = handle.read(_PREP_CACHE_ENTRY_BYTES + 1)
        if len(raw) > _PREP_CACHE_ENTRY_BYTES:
            return None
        saved = json.loads(raw)
        if (isinstance(saved, dict)
                and saved.get("version") == _PREP_CACHE_VERSION
                and saved.get("key") == path.stem
                and isinstance(saved.get("value"), dict)):
            return saved["value"]
    except (OSError, ValueError, RecursionError):
        pass
    return None


def _write_classification_cache(path: Path | None, value: dict) -> None:
    if path is None:
        return
    from ..sdk.durable import file_lock, write_text_atomic

    try:
        text = json.dumps(
            {"version": _PREP_CACHE_VERSION, "key": path.stem, "value": value},
            sort_keys=True, separators=(",", ":"), allow_nan=False,
        )
        if len(text.encode()) > _PREP_CACHE_ENTRY_BYTES:
            return
        path.parent.mkdir(parents=True, exist_ok=True, mode=0o700)
        os.chmod(path.parent, 0o700)
        # Only local writes/eviction hold the lock, never a paid agent turn.
        with file_lock(path.parent / ".lock"):
            write_text_atomic(path, text, mode=0o600)
            entries = [(p.stat().st_mtime_ns, p.stat().st_size, p)
                       for p in path.parent.glob("*.json")]
            size = sum(item[1] for item in entries)
            count = len(entries)
            for _, amount, old in sorted(entries):
                if count <= _PREP_CACHE_ENTRIES and size <= _PREP_CACHE_BYTES:
                    break
                old.unlink(missing_ok=True)
                size -= amount
                count -= 1
    except (OSError, ValueError, TypeError, RecursionError):
        # A full disk or corrupt cache must not turn a successful read into a
        # failed import. The underlying agent's result remains authoritative.
        pass


def _cached_plan(path: Path | None) -> tuple[plan_mod.Plan, str, str | None] | None:
    saved = _read_classification_cache(path)
    if saved is None or not isinstance(saved.get("tail"), str):
        return None
    session = saved.get("session")
    if session is not None and not isinstance(session, str):
        return None
    try:
        plan = plan_mod.parse(saved["tail"])
    except (ValueError, TypeError, AttributeError, RecursionError):
        return None
    return (plan, saved["tail"], session) if plan is not None else None


def _usable_pass(data: dict, key: str) -> bool:
    rows = data.get(key)
    if not isinstance(rows, list):
        return False
    if key == "projects":
        return any(isinstance(row, dict) and row.get("slug") for row in rows)
    if key == "assignments":
        return any(isinstance(row, dict) and (row.get("path") or row.get("dir"))
                   for row in rows)
    return bool(rows) and all(isinstance(row, dict) for row in rows)


@functools.lru_cache(maxsize=8)
def _git_note(folder: Path, work_dir: Path) -> str:
    """The GIT_HISTORY prompt fragment for this run, or "".

    Cached so the digest is written once per (folder, work_dir) however many
    prompts ask for it; best-effort because an import must never fail over a
    broken .git directory.
    """
    authorized = work_dir / "github-context.txt"
    extra = ""
    try:
        if authorized.is_file() and authorized.stat().st_size <= 128 * 1024:
            extra = "\n\n" + authorized.read_text(encoding="utf-8")
    except OSError:
        pass
    try:
        context = bf.git_context(folder)
        if context is None:
            return extra
        history = bf.write_git_history(context, work_dir)
        if history is None:
            return extra
        return prompts.git_history(
            history_path=str(history), repo=context.repo, branch=context.branch
        ) + extra
    except Exception:
        return extra


def classify(
    folder: Path,
    ev: evidence_mod.Evidence,
    *,
    agent: bf.Agent,
    existing: list[str],
    work_dir: Path,
    stream=None,
) -> tuple[plan_mod.Plan | None, str, str | None]:
    """Run the classification agent. Returns ``(plan, tail, session_id)``.

    The session comes back so the review gate can RESUME it to apply a
    correction. That is the difference between a revision costing one turn and
    costing the whole folder again: the evidence is already in that session's
    context. `None` for Codex, which has no resume here, and the caller falls
    back to a cold re-classify that carries the correction in its prompt.

    Batched by construction rather than by chunking the evidence: the prompt
    carries the whole evidence set and `--autocompact auto` handles the rest.
    The one thing that must not happen quietly is compaction eating the evidence
    mid-decision, so :func:`probe.cli.backfill_prompts.classify` is told when
    the sample budget truncated the input and instructs the agent to mark those
    placements low confidence.
    """
    jsonl = evidence_mod.to_jsonl(ev)
    if evidence_mod.needs_chunking(ev):
        # TOO BIG FOR ONE PROMPT. Not a slow path -- a rejected one: the whole
        # evidence set is a single message, so `--autocompact` cannot help
        # (it compacts across TURNS and there are none yet) and the request
        # fails outright. The chunked route is a genuinely different shape,
        # so it lives in its own function; see `classify_chunked`.
        #
        # Single-shot stays the DEFAULT because it is the better
        # classification when it is possible: every file judged against every
        # other, in one decision, with no summary in between.
        plan, tail = classify_chunked(
            folder, ev, agent=agent, existing=existing,
            work_dir=work_dir, stream=stream,
        )
        # No session to hand back: the chunked route runs many, and resuming
        # "the" one would resume whichever ran last. A correction after this
        # re-classifies cold, which the revise prompt is told about.
        return plan, tail, None

    prompt = prompts.classify(
        root=folder,
        evidence_jsonl=jsonl,
        existing=existing,
        truncated=ev.sample_budget_hit,
        work_dir=str(work_dir),
        mtime_uninformative=ev.mtime_uninformative,
    ) + _git_note(folder, work_dir)
    heading = f"Reading {folder.name} — {ev.total_files:,} files"
    _classification_progress(heading, "classify")
    cache = _classification_cache_path(
        work_dir, agent=agent, prompt=prompt, phase="classify",
    )
    saved = _cached_plan(cache)
    if saved is not None:
        _classification_progress(heading, "classify", cached=True)
        return saved
    session = new_session_id() if agent is bf.Agent.CLAUDE else None
    with _ReadProgress(folder, ev.total_files, 0, stream) as progress:
        progress.begin("classify", heading)
        ok, tail = bf.launch_agent(
            folder,
            prompt,
            agent=agent,
            workdir=work_dir,
            heading=heading,
            total=0,
            timeout=CLASSIFY_TIMEOUT_S,
            stream=stream,
            session_id=session,
            paint_to=progress.activity("classify", heading),
            cancel_event=progress.cancelled,
        )
        plan = plan_mod.parse(tail) if ok else None
        progress.finish("classify", heading, success=plan is not None)
    if not ok:
        return None, tail, session
    if plan is not None:
        _write_classification_cache(cache, {"tail": tail, "session": session})
    return plan, tail, session


#: Tokens the slice summaries may occupy in the naming prompt. Smaller than a
#: chunk budget because this pass is short and its input is prose, and because
#: leaving room matters more here than anywhere else: naming is the ONE step
#: that sees the whole folder, and it only sees it through these.
NAMING_TOKEN_BUDGET = 60_000

#: Attempts per chunked pass. A pass is a whole agent turn over a slice, and
#: the failures that hit it are overwhelmingly transient -- a dropped
#: connection, a turn that ended in prose without its closing JSON. Losing a
#: forty-slice run to one of those, after an hour of successful slices, is the
#: expensive outcome; a second attempt costs one slice.
PASS_ATTEMPTS = 2


def _run_pass(
    folder: Path, prompt: str, *, agent: bf.Agent, heading: str, work_dir: Path,
    total: int, stream=None, key: str, attempts: int = PASS_ATTEMPTS,
) -> tuple[dict | None, str]:
    """One agent turn that answers with JSON. Returns ``(object, detail)``.

    The DETAIL is returned, not swallowed. Discarding it and substituting
    "slice 3 of 9 could not be read" hid every message worth acting on --
    "`claude` is not on PATH", the parenthesis-in-path refusal, "the agent did
    not finish in time" -- behind a sentence naming only where it happened.

    Each chunked pass gets its OWN session. They are deliberately independent --
    that is the whole design -- so sharing one would reintroduce the carry-over
    the chunking exists to avoid, and would put the earlier chunks' evidence
    back in the context that has to hold the later ones. A retry is a fresh
    session for the same reason.
    """
    phase = {"findings": "survey", "projects": "name", "assignments": "assign"}.get(key, key)
    _classification_progress(heading, phase)
    progress = _read_progress.get()
    if progress is not None:
        progress.begin(phase, heading)
    cache = _classification_cache_path(
        work_dir, agent=agent, prompt=prompt, phase=phase, extra={"key": key},
    )
    saved = _read_classification_cache(cache)
    if saved is not None and _usable_pass(saved, key):
        _classification_progress(heading, phase, cached=True)
        if progress is not None:
            progress.finish(phase, heading, success=True, cached=True)
        return saved, ""
    detail = ""
    for attempt in range(max(1, attempts)):
        if progress is not None and progress.cancelled.is_set():
            return None, "scan cancelled"
        ok, tail = bf.launch_agent(
            folder, prompt, agent=agent, workdir=work_dir, heading=heading,
            # The whole evidence sample is already in the prompt. Extra
            # tool reads are activity, not a count of files classified.
            total=0, timeout=CLASSIFY_TIMEOUT_S, stream=stream,
            session_id=new_session_id() if agent is bf.Agent.CLAUDE else None,
            paint_to=progress.activity(phase, heading) if progress is not None else None,
            cancel_event=progress.cancelled if progress is not None else None,
        )
        last = tail.splitlines()[-1] if tail.strip() else "no output"
        if ok:
            # Last wins: an agent that restates its answer means the later one.
            found = None
            for line in tail.splitlines():
                if key not in line:
                    continue
                for data in bf._embedded_summaries(line.strip(), key=key):
                    found = data
            if found is not None:
                usable = _usable_pass(found, key)
                if usable:
                    _write_classification_cache(cache, found)
                if progress is not None:
                    progress.finish(phase, heading, success=usable)
                return found, ""
            detail = f"answered without a usable `{key}` object ({last})"
        else:
            detail = last
        if attempt + 1 < max(1, attempts):
            detail += "  (retried)"
    if progress is not None:
        progress.finish(phase, heading, success=False)
    return None, detail


def _fit_findings(findings: list[dict]) -> tuple[str, int]:
    """Slice summaries as JSON that fits the naming prompt. Returns (json, dropped).

    WHOLE ENTRIES, measured with the same estimator as everything else. The
    first version cut the encoded string at a fixed 200,000 characters, which
    lands mid-object: the naming pass then saw a malformed tail, silently never
    learned what the last slices contained, and named projects those slices'
    files were afterwards forced into. Dropping entries loses the same
    information but says how many, so the caller can report it.
    """
    kept = list(findings)
    while kept:
        text = json.dumps(kept, indent=1)
        if evidence_mod.estimate_tokens(text) <= NAMING_TOKEN_BUDGET:
            return text, len(findings) - len(kept)
        kept.pop()
    return "[]", len(findings)


def classify_chunked(
    folder: Path,
    ev: evidence_mod.Evidence,
    *,
    agent: bf.Agent,
    existing: list[str],
    work_dir: Path,
    stream=None,
    feedback: str = "",
) -> tuple[plan_mod.Plan | None, str]:
    """Classify a folder too big to fit one prompt. Survey -> name -> assign.

    THE SPLIT IS CHOSEN SO NO CHUNK NEEDS ANOTHER CHUNK'S DETAIL. Feeding the
    agent chunks in sequence and letting `--autocompact` absorb the overflow is
    the obvious alternative and it is wrong in a way that does not announce
    itself: compaction is lossy, and what it drops is exactly the evidence the
    classification runs on. Early files would be placed against evidence and
    later ones against a summary of it, with nothing at the review gate able to
    tell the two apart.

    So the one genuinely global decision -- what the projects ARE -- is made
    once, over summaries small enough to fit together. Everything else is
    per-chunk: each slice maps its own rows onto that fixed list, needing
    nothing from its siblings.

    Returns ``(plan, tail)`` like :func:`classify`, so the caller cannot tell
    which route produced the plan. A pass that fails returns no plan rather
    than a partial one: a classification silently missing files is the single
    outcome worth failing the run over.
    """
    jsonl = evidence_mod.to_jsonl(ev)
    chunks = evidence_mod.chunk_lines(jsonl)
    n = len(chunks)

    with _ReadProgress(folder, ev.total_files, n, stream):
        # Independent surveys preserve all evidence and the original slice order.
        # Only the naming step depends on seeing every completed survey.
        def survey_one(pair: tuple[int, list[str]]):
            i, chunk = pair
            return i, _run_pass(
                folder,
                git_note
                + prompts.survey(root=folder, evidence_jsonl="\n".join(chunk),
                                 index=i, total=n, work_dir=str(work_dir),
                                 truncated=ev.sample_budget_hit),
                agent=agent, work_dir=work_dir, stream=stream, total=ev.total_files,
                heading=f"Reading {folder.name} — slice {i} of {n}", key="findings",
            )

        git_note = _git_note(folder, work_dir)
        numbered = list(enumerate(chunks, start=1))
        findings: list[dict] = []
        surveyed = _classification_results(
            survey_one, numbered, workers=SURVEY_CONCURRENCY,
        )
        for i, (got, detail) in surveyed:
            if got is None:
                return None, f"slice {i} of {n} could not be read: {detail}"
            findings.append({"slice": i, **got})

        # -- name: the only step that sees the whole folder at once
        findings_json, dropped = _fit_findings(findings)
        named, detail = _run_pass(
            folder,
            prompts.name_projects(root=folder, findings_json=findings_json,
                                  existing=existing, feedback=feedback),
            agent=agent, work_dir=work_dir, stream=stream, total=ev.total_files,
            heading=f"Naming the projects in {folder.name}", key="projects",
        )
        if named is None or not named.get("projects"):
            return None, f"the projects could not be named: {detail or 'no projects'}"
        specs = [
            plan_mod.ProjectSpec(
                slug=str(p.get("slug") or "").strip(),
                name=str(p.get("name") or p.get("slug") or "").strip(),
                description=str(p.get("description") or "").strip(),
                # Asked for by `name_projects` and parsed by `_plan_from` on the
                # other route. Dropping them here made the two paths produce
                # different Plans from the same agent answer.
                tags=[str(t) for t in (p.get("tags") or []) if t],
            )
            for p in named["projects"]
            if isinstance(p, dict) and p.get("slug")
        ]
        if not specs:
            return None, "the naming pass produced no usable project"
        listing = "\n".join(f"    {s.slug}  —  {s.description or s.name}" for s in specs)
        allowed = {s.slug for s in specs}

        # -- assign: independent per chunk, against the fixed list
        #
        # CONCURRENT, and that is the payoff of the whole design rather than a
        # bolted-on optimisation: a slice needs nothing from its siblings, so
        # nothing is serialised except by the worker bound. Bounded by the
        # context floor each slice pays, which is a different bound from the one
        # on `run_units` -- hence a separate number rather than a shared one.
        # HOISTED. `mtime_uninformative` walks every file in the folder, and this
        # was inside `file_one` -- so a 200,000-file drive rebuilt a 200,000-element
        # list once per slice, across dozens of slices, all holding the GIL.
        mtime_dead = ev.mtime_uninformative

        def file_one(pair: tuple[int, list[str]]):
            i, chunk = pair
            return i, _run_pass(
                folder,
                prompts.assign_chunk(root=folder, evidence_jsonl="\n".join(chunk),
                                     projects=listing, index=i, total=n,
                                     work_dir=str(work_dir),
                                     truncated=ev.sample_budget_hit,
                                     mtime_uninformative=mtime_dead),
                agent=agent, work_dir=work_dir, stream=stream, total=ev.total_files,
                heading=f"Filing slice {i} of {n}", key="assignments",
            )

        filed = _classification_results(
            file_one, numbered, workers=classify_concurrency(),
        )

        assignments: list[plan_mod.Assignment] = []
        unsure: list[str] = []
        for i, (got, detail) in filed:
            if got is None:
                return None, f"slice {i} of {n} could not be filed: {detail}"
            for row in got.get("assignments") or []:
                if not isinstance(row, dict):
                    continue
                # EITHER KEY. A rollup row is addressed by `dir` -- the assign
                # prompt says to use it verbatim -- and the agent echoes whichever
                # key it was shown. `backfill_plan._plan_from` already carries this
                # fix with a comment saying accepting only `path` "dropped every
                # directory assignment silently, so thousands of files fell to
                # inheritance with nothing reported". This path reintroduced it.
                raw = row.get("path") or row.get("dir")
                if not raw:
                    continue
                slug = str(row.get("project") or "")
                # A slug outside the list is the agent inventing a project after
                # being told not to. Dropping the row would lose files silently, so
                # it is parked in the first project and flagged instead -- the
                # reviewer sees it, and `resolve` still accounts for every file.
                confidence = str(row.get("confidence") or "high")
                if slug not in allowed:
                    unsure.append(str(raw))
                    slug = specs[0].slug
                    # LOW, whatever the agent claimed. It was told not to invent a
                    # slug; a row we relocated on its behalf is not a confident
                    # placement, and anything filtering on confidence would read it
                    # as one.
                    confidence = "low"
                assignments.append(plan_mod.Assignment(
                    path=str(raw), project=slug, confidence=confidence,
                    why=str(row.get("why") or ""),
                ))
            unsure += [str(u) for u in (got.get("unsure") or []) if u]

        if not assignments:
            # `_plan_from` ends with the same guard, and without it here an
            # all-empty result is not an error: `resolve` returns an empty map,
            # nothing is `unknown` or `duplicated` so the plan reads as
            # trustworthy, `pack` yields no units, and the run reports
            # "N files found on disk · 0 queued · 0/0 units done" as a success.
            # A green no-op is the worst possible answer here -- it is the one a
            # reader stops investigating.
            return None, "no slice placed a single file"

        plan = plan_mod.Plan(
            projects=specs, assignments=assignments,
            unsure=list(dict.fromkeys(unsure)),
            summary=str(named.get("summary") or ""),
        )
        note = f"; {dropped} slice summary(ies) did not fit the naming step" if dropped else ""
        return plan, f"classified in {n} slices{note}"


def revise(
    folder: Path,
    ev: evidence_mod.Evidence,
    feedback: str,
    *,
    agent: bf.Agent,
    session_id: str | None,
    work_dir: Path,
    stream=None,
) -> tuple[plan_mod.Plan | None, str, str | None]:
    """Re-run the classifier with a correction. Returns ``(plan, tail, session)``.

    Resumes the classify session when there is one, so the agent still has the
    evidence and the correction costs a single turn. Without one it starts cold
    and the prompt says so -- an agent told to "revise your plan" with no plan
    in context will otherwise invent a fresh one that quietly drops everything
    the reviewer did not mention.

    A failed revision returns no plan and the CALLER KEEPS THE OLD ONE. Losing
    a good-enough plan because the correction round-tripped badly would make
    typing anything at the gate a gamble, which is the opposite of the point.

    The session is returned for the SAME reason it is taken: corrections come
    in rounds. A cold rerun mints one of its own and hands it back, so the
    second correction resumes the first one's work instead of starting over
    again -- which is what "revise, look, revise again" costs otherwise.
    """
    prompt = prompts.revise(
        feedback=feedback,
        root=folder,
        work_dir=str(work_dir),
        resumed=session_id is not None,
    )
    heading = f"Revising the plan for {folder.name}"
    _classification_progress(heading, "revise")
    cache = _classification_cache_path(
        work_dir, agent=agent, prompt=prompt, phase="revise",
        extra=({"session": session_id, "evidence": evidence_mod.to_jsonl(ev)}
               if _classification_context.get() is not None else None),
    )
    saved = _cached_plan(cache)
    if saved is not None:
        _classification_progress(heading, "revise", cached=True)
        return saved
    # Mutually exclusive: --resume ADOPTS a session, --session-id MINTS one.
    # Resuming keeps the same id, so `session` is what the next round uses
    # either way.
    fresh = None if session_id else (
        new_session_id() if agent is bf.Agent.CLAUDE else None
    )
    ok, tail = bf.launch_agent(
        folder,
        prompt,
        agent=agent,
        workdir=work_dir,
        heading=heading,
        total=0,
        timeout=CLASSIFY_TIMEOUT_S,
        stream=stream,
        resume=session_id,
        session_id=fresh,
    )
    session = session_id or fresh
    if not ok:
        return None, tail, session
    plan = plan_mod.parse(tail)
    if plan is not None:
        _write_classification_cache(cache, {"tail": tail, "session": session})
    return plan, tail, session


def _destination(path: str, assigned: dict[str, str]) -> str:
    """Where `path` is going, whether it names a FILE or a rollup DIRECTORY.

    `assigned` is keyed by the expanded per-file paths, so a bare lookup misses
    every rollup row and printed `(unplaced)` beside a directory the plan had in
    fact placed -- next to a header saying all 204 files were placed. The label
    was the only thing wrong, which is worse than a real gap: it sends a
    reviewer hunting for a problem that does not exist.
    """
    direct = assigned.get(path)
    if direct:
        return direct
    prefix = path.rstrip("/") + "/"
    under = {project for p, project in assigned.items() if p.startswith(prefix)}
    if len(under) == 1:
        return f"{under.pop()}  (all {sum(1 for p in assigned if p.startswith(prefix)):,} files under it)"
    if under:
        return "split across " + ", ".join(sorted(under))
    return "(unplaced)"


def describe_plan(
    ev: evidence_mod.Evidence,
    plan: plan_mod.Plan,
    assigned: dict[str, str],
    disc: plan_mod.Discrepancy,
    census: bf.Census | None = None,
) -> list[str]:
    """The approval screen's body: what will happen, and what is uncertain.

    Least-certain first. A reviewer reading top-down should meet the decisions
    worth arguing with before the ones that are obviously fine, because the
    whole value of the gate is catching the shared `data/` directory that got
    filed under one researcher.
    """
    per_project: dict[str, int] = {}
    for project in assigned.values():
        per_project[project] = per_project.get(project, 0) + 1

    lines = [f"{len(assigned):,} of {ev.total_files:,} files placed into "
             f"{len(per_project)} project(s):", ""]
    for project in sorted(per_project, key=lambda p: (-per_project[p], p)):
        lines.append(f"  {project:<32} {per_project[project]:>7,} files")

    low = [a for a in plan.assignments if a.confidence != "high"]
    unsure = list(dict.fromkeys(plan.unsure + [a.path for a in low]))
    if unsure:
        lines += ["", "Least certain — check these first:"]
        for path in unsure[:12]:
            lines.append(f"  {path}  ->  {_destination(path, assigned)}")
        if len(unsure) > 12:
            lines.append(f"  ... and {len(unsure) - 12:,} more")

    notes = disc.describe()
    if notes:
        lines += ["", *notes]
    # The linked-directory warning used to be built HERE. It moved to `_index`,
    # which runs straight after the walk: this gate is only reached on the
    # classify path, so resume, already-imported, empty-folder and the stranded
    # recovery all exited without ever mentioning what the walk could not see.
    if plan.summary:
        lines += ["", plan.summary]
    return lines


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

    prompt = prompts.import_unit(
        root=folder,
        project=unit.project,
        paths=list(unit.paths),
        manifest_path=str(manifest),
    ) + _git_note(folder, work_dir)
    def launch():
        return bf.launch_agent(
            folder, prompt, agent=agent, workdir=work_dir,
            heading=f"Importing into {unit.project}", label=unit.project,
            total=unit.files, timeout=UNIT_TIMEOUT_S, stream=stream,
            session_id=session, resume=resume, paint_to=paint_to,
        )

    ok, tail = launch()
    # The ledger start can survive a crash before Claude creates its local
    # session. Retry only its explicit missing-session diagnostic;
    # authentication, permissions, timeouts and arbitrary model errors are not
    # evidence that replaying from scratch is appropriate.
    if (
        not ok and resume and agent is bf.Agent.CLAUDE
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
        ok, tail = launch()
    checked = validate_manifest(manifest, unit.paths, root=folder)
    rows = len(checked.rows)
    problems = [] if ok else [(tail.splitlines()[-1] if tail else "agent failed")[:1000]]
    if not checked.complete:
        ok = False
        problems.append(checked.describe())
    detail = "; ".join(problems)
    ledger.finish_unit(
        unit.unit_id,
        ok=ok,
        enqueued=rows,
        error=None if ok else detail,
    )
    return UnitOutcome(
        unit=unit, ok=ok, manifest=manifest if rows else None, rows=rows,
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
    from probe.cli import tui

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
            sizes=sizes,
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


# -- projects ----------------------------------------------------------------


def ensure_projects(client, plan: plan_mod.Plan, assigned: dict[str, str]) -> tuple[list[str], list[str]]:
    """Create every project the plan needs, BEFORE any unit launches.

    Up front, and not lazily inside the units, because concurrent units filing
    into the same project would otherwise race `probe project create`. Creating
    them here removes the race by construction rather than by locking, and it
    means a killed import still leaves a readable, correctly-named skeleton
    instead of orphaned artifacts.

    Returns ``(slugs, problems)``. A project that cannot be created is a problem
    the caller must surface before uploading anything into a folder whose
    destination does not exist.
    """
    specs = {p.slug: p for p in plan.projects}
    wanted = sorted(set(assigned.values()))
    made: list[str] = []
    problems: list[str] = []
    for slug in wanted:
        spec = specs.get(slug)
        try:
            row = _resolve_or_create(
                client,
                slug,
                name=(spec.name if spec else slug) or slug,
                description=(spec.description if spec else "") or None,
            )
            made.append(row.get("slug") or slug)
        except Exception as exc:  # noqa: BLE001 - surfaced, never swallowed
            problems.append(f"could not create project {slug!r}: {exc}")
    return made, problems


def _resolve_or_create(client, slug: str, *, name: str, description: str | None) -> dict:
    """Use the project called `slug`, creating it if it is not there.

    EXPLICITLY, not through `ensure_project`. That method runs the near-miss
    guard, which refuses a slug resembling one already in the namespace -- and
    the namespace it reads includes the projects this very loop created moments
    earlier. A folder splitting into `odyssey-cluster-deploy`,
    `odyssey-protein-benchmarks` and `odyssey-protein-lm` therefore could not be
    imported at all: the guard read the siblings as typos of each other, refused
    the last, and left the rest behind as orphans.

    The guard is right for what it was built for -- a training loop or a
    detached `probe run start`, where a typo silently opens a second identity
    and nobody is watching. A backfill is the opposite situation, and its slugs
    have already been checked twice by the time they arrive here:

        the classify prompt hands the agent the existing projects and tells it
        to prefer them (REUSE), and a human then reads every project name at
        the review gate with its file count beside it.

    So the guard would be a third opinion holding strictly LESS information
    than the person who just approved the list, and it is the one that cannot
    tell a sibling from a typo. Its own error says the way out is to "create it
    explicitly" -- this is that path, taken deliberately rather than after a
    failure. Duplicates are still impossible: an existing slug resolves and is
    reused, never re-created.
    """
    from probe.sdk import errors

    row = client.resolve_project(slug)
    if row is not None:
        return row
    try:
        # A folder backfill has no intent-holder present: the neutral label.
        return client.create_project(slug, name, kind="general", description=description)
    except errors.ConflictError:
        # Lost a create race with a concurrent process. What we promise is that
        # the project EXISTS afterwards, not that we made it.
        row = client.resolve_project(slug)
        if row is None:
            raise
        return row


def _ingest_summary(stdout: str) -> dict | None:
    """The `{"enqueued": N, ...}` object out of `artifact add`'s output.

    NOT `splitlines()[-1]`. That is what shipped, and the command prints
    PRETTY-PRINTED JSON, so the last line is `}` -- which parses as nothing.
    Every manifest then reported "could not read the ingest summary (['}'])"
    and the run said "0 queued for upload" while all 204 rows sat in the outbox
    delivering perfectly well. A reporting bug that reads exactly like total
    data loss, on the step where bytes finally move.

    Scanning for a balanced brace run instead also survives what else lands on
    stdout: the version-update nudge prints there, and so does anything a
    future release decides to say first.
    """
    best: dict | None = None
    for data in bf._embedded_summaries(stdout, key="failures"):
        best = data
    if best is not None:
        return best
    # `failures` is absent when nothing failed, so fall back to the count --
    # which is the field this is really after.
    depth = 0
    start = -1
    for i, ch in enumerate(stdout):
        if ch == "{":
            if depth == 0:
                start = i
            depth += 1
        elif ch == "}" and depth:
            depth -= 1
            if depth == 0 and start >= 0:
                try:
                    data = json.loads(stdout[start : i + 1])
                except ValueError:
                    continue
                if isinstance(data, dict) and "enqueued" in data:
                    best = data
    return best


def enqueue_manifests(
    folder: Path, outcomes: list[UnitOutcome], *, project_of: dict[str, str],
    ledger: ledger_mod.Ledger | None = None,
) -> tuple[int, list[str]]:
    """Hand every unit's manifest to `artifact add --from-manifest`.

    THE CWD IS LOAD-BEARING. A manifest row's `path` is relative to the imported
    folder and the reader resolves it against the process working directory, so
    this runs with `cwd=folder`. Anywhere else, every row fails "is not a regular
    file" -- or worse, a same-named file under the wrong cwd uploads the wrong
    bytes under the right name.

    THE ANCHOR IS PASSED EXPLICITLY. Rows carry no anchor key, so without
    `--project` every row is rejected for want of one and the command exits 1
    having enqueued nothing -- a zero-import wearing a well-formed error.
    """
    import subprocess
    import sys

    enqueued = 0
    problems: list[str] = []
    for out in outcomes:
        if not out.manifest or not out.rows:
            continue
        checked = validate_manifest(out.manifest, out.unit.paths, root=folder)
        manifest = out.manifest
        if not checked.complete:
            problems.append(f"{manifest.name}: {checked.describe()}")
            if ledger is not None:
                ledger.finish_unit(out.unit.unit_id, ok=False, enqueued=len(checked.rows),
                                   error=checked.describe())
            if not checked.rows:
                continue
            # Retain the original for diagnosis. Only validated, confined rows
            # can cross the upload boundary, even on legacy/recovery paths.
            from ..sdk.durable import write_text_atomic

            manifest = manifest.with_suffix(".validated.jsonl")
            write_text_atomic(manifest, "".join(json.dumps(row) + "\n" for row in checked.rows))
        project = project_of.get(out.unit.unit_id, out.unit.project)
        proc = subprocess.run(  # noqa: S603 - fixed argv, no shell
            [
                sys.executable, "-c",
                "import sys; from probe.cli import main; sys.exit(main(sys.argv[1:]))",
                # NO write-mode flag, and none is needed: `--from-manifest`
                # queues to the outbox and lets the drainer deliver whichever
                # way the flag points -- that is the point of the verb.
                #
                # It was once dropped for a second reason that no longer holds.
                # `--async` used to be ROOT-only, so placing it here produced
                # "Error: No such option: --async" and every manifest silently
                # failed to enqueue while all six units reported success: 204
                # files read, described and manifested, 0 uploaded. The flag is
                # accepted in both positions now (see `write_mode_opt`), so that
                # trap is gone; the first reason is the one that keeps it out.
                "artifact", "add", "--from-manifest", str(manifest),
                "--project", project,
            ],
            cwd=str(folder), capture_output=True, text=True,
        )
        summary = _ingest_summary(proc.stdout)
        if summary is not None:
            landed = int(summary.get("enqueued") or 0)
            enqueued += landed
            # RECORDED SEPARATELY from the unit's DONE. A unit is done when its
            # manifest exists; this is the only record that its rows reached
            # the queue, and the gap between the two is where a dropped
            # connection lands.
            if ledger is not None:
                ledger.record_enqueued(out.unit.unit_id, landed)
            for failure in summary.get("failures") or []:
                problems.append(f"{out.manifest.name} line {failure.get('line')}: "
                                f"{failure.get('error')}")
        else:
            problems.append(
                f"{out.manifest.name}: could not read the ingest summary "
                f"({(proc.stderr or proc.stdout or '').strip().splitlines()[-1:] or ['no output']})"
            )
    return enqueued, problems


#: How often the drain watcher re-counts the outbox. The queue is a directory
#: of files, so this is a cheap listdir -- but not free, and nobody reads a
#: number that changes faster than they can look at it.
WATCH_POLL_S = 1.0


def watch_outbox(total: int, *, stream=None, poll: float = WATCH_POLL_S) -> list[str]:
    """Sit and watch the queue drain. Returns the closing lines.

    OPTIONAL, and it has to be: the outbox is a background drainer precisely so
    an import does not hold anyone's terminal, and on a big folder this runs for
    a long time. Ctrl-C leaves the queue exactly where it was -- nothing here
    touches it, it only counts -- so stopping the watch is not stopping the
    upload, and the closing line says so rather than leaving that to be
    guessed.

    Reuses `bf.Activity` deliberately: this is the same question the import
    screen answers ("how far along, how much longer") and a second progress
    idiom for it would be a second thing to learn.
    """
    import time

    from probe.cli import tui

    from ..sdk.journal import Journal
    from .main import _conn

    journal = Journal(_conn.spool_dir)
    out = stream if stream is not None else sys.stdout
    live = hasattr(out, "isatty") and out.isatty()
    state = bf.Activity(total=max(1, total), doing="draining")
    started = time.monotonic()

    def counts() -> tuple[int, int]:
        # Every queue: a PROBE_TOKEN or in-code credential's uploads queue in
        # their own folder (#2035).
        queues = journal.namespaces()
        return sum(len(q.pending()) for q in queues), sum(len(q.failed()) for q in queues)

    pending, failed = counts()
    board = tui.Board(f"Uploading {total:,} file(s)", [""], out=out) if live else None
    if board is not None:
        board.open()
    try:
        while pending:
            # `done` reads from `seen`, and the outbox counts DOWN -- so the
            # delivered set is synthesised from the difference rather than
            # tracked per item. Nothing else needs the paths.
            delivered = max(0, total - pending)
            state.seen = set(range(delivered))
            state.doing = f"{pending:,} left" + (f" · {failed:,} failed" if failed else "")
            if board is not None:
                state.ticks += 1
                board.update(0, state.line(time.monotonic() - started))
            time.sleep(poll)
            pending, failed = counts()
    except KeyboardInterrupt:
        return [f"Stopped watching. {pending:,} file(s) still queued — the drainer "
                "keeps going in the background.",
                "`probe outbox status` shows where it got to."]
    finally:
        if board is not None:
            board.close(erase=True)

    if failed:
        return [f"{total - failed:,} of {total:,} delivered · {failed:,} failed.",
                "`probe outbox status --verbose` lists them; re-running the "
                "import retries."]
    return [f"All {total:,} file(s) delivered."]


def execute(
    *,
    client_factory,
    folder: Path,
    agent: bf.Agent,
    project: str | None = None,
    interactive: bool = True,
    yes: bool = False,
    concurrency: int | None = None,
    telemetry: TelemetryContext | None = None,
    transcripts: bool = False,
    transcripts_budget: int | None = None,
    source_id: str | None = None,
    import_changed: bool = False,
    import_unverified: bool = False,
    retry_dead: bool = False,
    background: bool = False,
    back_to_selection: bool = False,
    wandb_source: dict | None = None,
    offer_wandb: bool = True,
):
    """The whole import. Returns the lines the caller pages.

    Order is deliberate and each step is cheap-and-certain before the one after:
    census, evidence, classify, REVIEW, create projects, import, enqueue,
    reconcile. Nothing mutates anything server-side until the review has passed.

    LEAVING KILLS EVERY AGENT. `_execute` does the work; this wrapper only
    guarantees the cleanup, on every exit -- Ctrl-C, an exception, or a clean
    return. Belt and braces on purpose: the interrupt paths already call
    `stop_all`, and this is what catches the route nobody thought of. An agent
    that outlives the wizard is invisible, holds the folder, and keeps spending
    tokens with nothing left to report to.

    The OUTBOX is untouched. It is a background drainer with its own
    `probe outbox pause`, and files already queued are already the user's --
    abandoning those on the way out is the one thing leaving must not do.
    """
    from . import telemetry as telemetry_mod, tui

    tel = telemetry_mod.null_context() if telemetry is None else telemetry
    started_at = time.monotonic()
    # Shared with _execute's _summary: a run whose summary already went out
    # must not emit a SECOND one from the interrupt handler — Ctrl-C at the
    # post-success "watch them upload?" prompt is ordinary human use, and a
    # success + aborted pair would corrupt the funnel it reports on.
    summary_state = {"emitted": False}
    # THE CONVERSATIONS RUN HERE, not at the end of `_execute`, and that is not
    # tidiness: `_execute` returns early on nine paths -- an unreadable root, an
    # empty folder, an already-finished import, a refused project, an
    # untrustworthy plan -- and on every one of them a user who passed
    # --transcripts would have been told nothing about the sessions they
    # asked for. The two scopes are independent by design, so the folder half
    # failing must not cancel the machine half.
    lane_state: dict = {}
    try:
        lines = _execute(
            client_factory=client_factory, folder=folder, agent=agent,
            project=project, interactive=interactive, yes=yes,
            concurrency=concurrency, telemetry=tel, started_at=started_at,
            summary_state=summary_state, lane_state=lane_state,
            source_id=source_id, import_changed=import_changed, import_unverified=import_unverified,
            retry_dead=retry_dead,
            background=background,
            back_to_selection=back_to_selection,
            wandb_source=wandb_source, offer_wandb=offer_wandb,
        )
        if lines is tui.BACK or lines is None:
            return lines
        if transcripts:
            # Preserve StartedFolderImport's job metadata while appending the
            # independent session lane's report.
            lines.extend(["", *_run_transcript_lane(
                client_factory=client_factory,
                folder=folder,
                units=lane_state.get("units") or [],
                interactive=interactive,
                yes=yes,
                budget_bytes=transcripts_budget,
            )])
        return lines
    except KeyboardInterrupt:
        bf.stop_all()
        if not summary_state["emitted"]:
            tel.emit(
                telemetry_mod.EVENT_BACKFILL_SUMMARY,
                outcome=telemetry_mod.BackfillOutcome.ABORTED,
                duration_seconds=int(time.monotonic() - started_at),
            )
        if back_to_selection:
            raise
        return ["Stopped. Nothing further was read or uploaded.",
                "Anything already queued keeps uploading — `probe outbox status` "
                "shows it, `probe outbox pause` stops it."]
    except Exception:
        # Observe-and-re-raise, never swallow: a crash without a summary would
        # read as user abandonment in the funnel. No error text on the event —
        # exception strings can embed paths, and the property contract is
        # metadata-only.
        if not summary_state["emitted"]:
            tel.emit(
                telemetry_mod.EVENT_BACKFILL_SUMMARY,
                outcome=telemetry_mod.BackfillOutcome.ERROR,
                duration_seconds=int(time.monotonic() - started_at),
            )
        raise
    finally:
        bf.stop_all()


#: How often the walk repaints its counter. Every file would be a syscall per
#: file on top of the stat; every 2,000 is imperceptible to a reader and free.
PROGRESS_EVERY = 2_000

#: How many linked/unreadable directories the warning names before summarising.
#: A reviewer who cannot reproduce what they were shown cannot act on it, so
#: the list is sorted and the remainder is counted rather than dropped.
WARN_SHOWN = 5


def _index(
    folder: Path, report: "Report"
) -> tuple[bf.Census, list, evidence_mod.WalkWarnings, "index_mod.Index", list]:
    """THE walk. One traversal → census, records, and what it could not see.

    Everything downstream reads these records; nothing walks the folder again.
    Sampling and clustering are NOT done here -- see `evidence.enrich`, which
    the early exits below must be able to skip.

    The counter is painted by THIS loop rather than by a callback handed into
    `walk`, which is what keeps `backfill_evidence` free of any terminal. On a
    research drive this loop runs for minutes; before it existed the screen
    showed the previous menu the whole time and read as a hung program.
    """
    from probe.cli import tui

    warn = evidence_mod.WalkWarnings()
    records: list = []
    count = total = 0

    # THE CALLER GUARDS, not the Board. `Board.open()` writes absolute cursor
    # escapes unconditionally -- piped into a log that is a screenful of
    # garbage. Same shape as the unit board below.
    board = None
    if tui.interactive():
        # EMPTY label, not "counting …". A Board label is a permanent row
        # PREFIX -- `update` renders `f"{label:<width}{text}"` -- so a
        # placeholder-looking label is never replaced, it is glued to every
        # repaint: `counting …12,000 files · 4.2 GB`. In `run_units` the labels
        # are project names, which is what the field is for.
        board = tui.Board(f"Reading {folder}", [""])
        board.open()
    # WRITTEN DOWN ON THE WAY PAST. `Index.write` is a generator that yields
    # what it was given, so this loop is unchanged and the walk is not paid
    # for twice. The previous index is still on disk and still readable at
    # this point -- the diff below reads it BEFORE the new one replaces it.
    index = index_mod.Index.for_folder(folder)
    previous = index.read()
    try:
        for f in index.collect(evidence_mod.walk(folder, warn), root=folder):
            records.append(f)
            count += 1
            total += f.size
            if board is not None and count % PROGRESS_EVERY == 0:
                board.update(0, f"{count:,} files · {bf.human_bytes(total)}")
        if board is not None:
            board.update(0, f"{count:,} files · {bf.human_bytes(total)}")
    finally:
        # In a `finally` so Ctrl-C mid-walk cannot leave the terminal in
        # absolute-cursor mode with no prompt.
        if board is not None:
            board.close()

    census = bf.Census(
        files=count,
        bytes=total,
        linked_dirs=tuple(warn.linked),
        unreadable_dirs=tuple(warn.unreadable),
    )
    report.add(*incomplete_lines(census))
    if count >= index_mod.LARGE_WALK_FILES:
        # NAMED, not refused. The index streams, but `sample`/`cluster_by_mtime`
        # downstream still hold the whole record list, so a tree far past this
        # can be OOM-killed with nothing to show for the walk.
        report.add(
            f"{count:,} files is past what one import holds comfortably in "
            "memory — import subfolders separately if this run is killed."
        )
    return census, records, warn, index, previous


def incomplete_lines(census: bf.Census) -> list[str]:
    """Say what the walk could not see. Rendered in TWO places, on purpose.

    `_index` puts these in the report, which every exit returns -- that is the
    fix for the four paths (resume, already-imported, empty folder, stranded
    recovery) that never reach the review gate and so never said a word about
    a skipped directory.

    The GATE renders them too, ahead of the plan, because that is the moment
    they can still change the answer: after the import, "a directory was
    skipped" is only a regret. The gate splices this list in rather than
    `describe_plan` embedding it, so the copy that lands in the final report
    via `report.add(*body)` is not a second one.
    """
    lines: list[str] = []
    for items, noun, advice in (
        (census.linked_dirs, "linked",
         "Import the directory each one points at separately."),
        (census.unreadable_dirs, "unreadable",
         "Check permissions — anything under them is not counted or imported."),
    ):
        if not items:
            continue
        n = len(items)
        was = "directory was" if n == 1 else "directories were"
        lines += ["", f"{n} {noun} {was} skipped, so anything only reachable "
                      "through them is NOT in this import:"]
        lines += [f"  {i[0] + ' -> ' + i[1] if isinstance(i, tuple) else i}"
                  for i in items[:WARN_SHOWN]]
        if n > WARN_SHOWN:
            lines.append(f"  ... and {n - WARN_SHOWN} more")
        lines.append(f"  {advice}")
    return lines


def _execute(**kwargs) -> list[str]:
    """Run the scoped folder importer; unit execution helpers remain in this module."""
    from .backfill_import import execute as execute_scoped

    return execute_scoped(**kwargs)


def _run_transcript_lane(
    *,
    client_factory,
    folder: Path,
    units: list[plan_mod.Unit],
    interactive: bool,
    yes: bool,
    budget_bytes: int | None,
) -> list[str]:
    """Import standalone sessions; file assignments establish no session link.

    No agent: the local summarizer this lane used to pick went with the
    server-side digest lane. The client STAYS. Uploads go through the capture
    credential's own Wire, but `run_lane` still asks the server about each
    session before importing it and pins the account a background import runs
    under, and both need the wizard's own client.
    """
    from . import backfill_transcripts as transcripts_mod

    try:
        return transcripts_mod.run_lane(
            client=client_factory(),
            interactive=interactive,
            yes=yes,
            budget_bytes=budget_bytes,
        )
    except Exception as exc:  # the files already landed; never lose that report
        return [f"Could not import agent sessions: {exc}"]
