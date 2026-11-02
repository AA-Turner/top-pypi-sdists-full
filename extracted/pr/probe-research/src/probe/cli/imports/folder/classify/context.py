"""one source snapshot's classification context: measured read progress and the turn cache that reuses completed turns."""

from __future__ import annotations
import hashlib
import json
import os
import sys
import threading
from contextlib import contextmanager
from contextvars import ContextVar
from dataclasses import dataclass
from pathlib import Path

from ... import folder as bf
from . import plan as plan_mod
from ...agent_settings import cached


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
        from ....wizard import terminal as tui

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
        from ....wizard import terminal as tui

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
_PREP_CACHE_VERSION = 2
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
    from .....foundation.durable.durable import file_lock, write_text_atomic

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
from probe.cli.imports.folder.classify.classify import _git_note  # noqa: E402 -- pieces need each other; the front door loads this one first
