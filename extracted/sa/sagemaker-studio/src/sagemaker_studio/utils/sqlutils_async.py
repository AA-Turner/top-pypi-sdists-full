"""Async SQL result materialization.

Parallel to the synchronous path in ``sqlutils.sql_stream_with_display``. When the
UI opts in via ``materialize="async"`` the kernel returns the first page inline and
a background daemon thread streams the full result to S3 as fixed-size Parquet
pages, writes the full DataFrame into the kernel namespace, and emits a
``dataframe_ready`` IOPub event. Scope: Athena + Redshift single-statement SELECTs.

IO seams (S3 writes, kernel event emission) are injected so the core is unit
testable without a live kernel or S3.
"""

import atexit
import json
import logging
import threading
import time
from dataclasses import dataclass
from typing import Any, Callable, Dict, Iterator, List, Optional

logger = logging.getLogger(__name__)

# Fixed page size. Constant per run; the manifest records it so older/cross-engine
# results stay readable if this ever changes.
ROWS_PER_PAGE = 10_000
MANIFEST_NAME = "_manifest.json"

# Upper bound on GetQueryRuntimeStatistics poll attempts for the exact Athena total
# (#6): the poll rides the per-page write loop, so this caps control-plane calls on a
# query whose OutputRows never populates (DDL / non-Presto / a role without
# athena:GetQueryRuntimeStatistics). Generous -- the happy path stops at the first
# non-None hit long before this; when the cap is reached the UI falls back to the exact
# counted row_count, so correctness is preserved.
_STATS_MAX_ATTEMPTS = 15

# Manifest status values.
STATUS_IN_PROGRESS = "in_progress"
STATUS_COMPLETE = "complete"
STATUS_FAILED = "failed"

# dataframe_ready status values.
READY_SUCCESS = "success"
READY_FAILED = "failed"

# Mimetype for the async first-page card, in the existing datanotebooks Parquet family
# (see the UI's kernel.types.ts). Payload carries the sync-reply fields + inline first page.
ASYNC_SQL_MIMETYPE = "application/vnd.datanotebooks+async-sql+json"


def extract_execution_id(execution_metadata: Optional[Dict[str, Any]]) -> Optional[str]:
    """Return the engine execution id used as the S3 partition + correlation key.

    Athena exposes ``query_execution_id``; Redshift Data API exposes ``statement_id``.
    Returns None when neither is present (engine unsupported / metadata missing).
    """
    if not execution_metadata:
        return None
    return execution_metadata.get("query_execution_id") or execution_metadata.get("statement_id")


def extract_redshift_query_id(execution_metadata: Optional[Dict[str, Any]]) -> Optional[int]:
    """Redshift's own query id (RedshiftQueryId) from the statement's execution metadata.

    None for other engines and when Redshift assigned no id (the Data API reports -1 for
    leader-node-only statements, which the cursor already drops).
    """
    if not execution_metadata:
        return None
    query_id = execution_metadata.get("redshift_query_id")
    return query_id if isinstance(query_id, int) and query_id > 0 else None


def build_result_prefix(project_s3_root: str, execution_id: str) -> str:
    """Deterministic result prefix rooted under the project S3 root.

    The project root is the isolation boundary (per-project bucket, IAM scoped);
    execution_id is only the uniqueness key.
    """
    if not project_s3_root:
        raise ValueError("project_s3_root is required to build the async result prefix")
    if not execution_id:
        raise ValueError("execution_id is required to build the async result prefix")
    return f"{project_s3_root.rstrip('/')}/results/{execution_id}/"


def page_key(prefix: str, page_index: int) -> str:
    """S3 key for a zero-indexed page (page_000.parquet, page_001.parquet, ...)."""
    return f"{prefix}page_{page_index:03d}.parquet"


def manifest_key(prefix: str) -> str:
    return f"{prefix}{MANIFEST_NAME}"


@dataclass
class Manifest:
    """`_manifest.json` contents. Rewritten as each page lands."""

    totalfiles: int = 0
    rowPerPages: int = ROWS_PER_PAGE
    status: str = STATUS_IN_PROGRESS
    row_count: int = 0
    # Exact upfront total when the engine exposes it: Redshift ``TotalNumRows`` at first
    # paint (stamped by the caller), or Athena ``OutputRows`` fetched off the page loop
    # (see the gated GetQueryRuntimeStatistics call in ``_background_materialize``). None
    # until known; the UI shows this when present, else falls back to ``row_count`` (which
    # equals the exact total once ``status=='complete'``). Never a lag-induced 0.
    total_rows: Optional[int] = None

    def to_json(self) -> str:
        return json.dumps(
            {
                "totalfiles": self.totalfiles,
                "rowPerPages": self.rowPerPages,
                "status": self.status,
                "row_count": self.row_count,
                "total_rows": self.total_rows,
            }
        )


class _AsyncMaterializationError(Exception):
    """Base for terminal non-success outcomes of a background materialization, raised to a
    ``PendingDataFrame`` waiter when it resolves a run that did not succeed."""


class _AsyncMaterializationFailed(_AsyncMaterializationError):
    """The background materialization of ``var_name`` failed (an exception was raised while
    streaming/building the result)."""

    def __init__(self, var_name: str) -> None:
        super().__init__(
            f"Async materialization of DataFrame '{var_name}' failed; the upstream query "
            f"did not complete successfully."
        )
        self.var_name = var_name


class _AsyncMaterializationSuperseded(_AsyncMaterializationError):
    """The run a waiter was bound to was superseded by a newer run of the same variable
    (a same-cell re-run) or was cancelled before it completed."""

    def __init__(self, var_name: str) -> None:
        super().__init__(
            f"Async materialization of DataFrame '{var_name}' was superseded or cancelled "
            f"by a newer run before it completed."
        )
        self.var_name = var_name


class _MaterializationRegistry:
    """Tracks in-flight background materializations, keyed by dataframe name.

    Provides a per-``var_name`` generation token so a stale/superseded thread never
    clobbers the namespace binding of a newer run, and a cooperative cancel flag.

    It also exposes a per-``(var_name, generation)`` completion signal (a
    ``threading.Event`` plus a result/error slot) that a ``PendingDataFrame`` proxy waits
    on: the background materialize thread settles the signal exactly once on every
    terminal outcome (success / failure / supersession / cancel), and a waiter blocks on
    it via ``wait_until_ready`` then reads the outcome via ``get_result``. This is a
    handoff flag between two threads that already exist (the daemon materialize thread and
    the cell's own execution thread), not a new thread.
    """

    def __init__(self) -> None:
        # RLock (reentrant): commit() runs the namespace write (action) while holding the
        # lock, and that write can drop the last reference to a PendingDataFrame proxy,
        # whose weakref.finalize fires synchronously ON THIS SAME THREAD and calls
        # release_consumer -- which re-acquires this lock. A plain Lock would self-deadlock
        # there; RLock lets the same thread re-enter, so the atomic commit (generation
        # check + write under one lock) is preserved without the deadlock.
        self._lock = threading.RLock()
        self._generation: Dict[str, int] = {}
        self._cancel: Dict[str, threading.Event] = {}
        # In-flight runs kept so the atexit hook can finalize them on graceful shutdown.
        self._inflight: "Dict[tuple, _InFlightRun]" = {}
        # Per-(var_name, generation) completion signal for PendingDataFrame waiters.
        # _done[key] is set() exactly once on a run's terminal outcome; _result[key] holds
        # the materialized DataFrame on success, and _error[key] holds the Exception (or a
        # sentinel) on failure/supersession. Keyed by (var_name, gen) so a superseded run's
        # stale signal can never satisfy a waiter bound to a newer generation.
        self._done: "Dict[tuple, threading.Event]" = {}
        self._result: "Dict[tuple, Any]" = {}
        self._error: "Dict[tuple, BaseException]" = {}
        # Live proxy count per (var_name, gen). A result slot is released once the last
        # proxy bound to it has resolved (cached the frame in its own _real), so the
        # materialized frame is not retained by the module-level registry for the life of
        # the kernel. See retain/release_consumer/reap.
        self._consumers: "Dict[tuple, int]" = {}
        # Per-(var_name, gen) materialization progress: [page_counter, last_change_monotonic].
        # The background thread bumps it via note_progress on every page write; the proxy's
        # wait uses it to distinguish a HEALTHY-but-slow run (still advancing -> keep waiting)
        # from a genuinely STALLED one (no advance for the stall window -> time out). This is
        # what makes the wait bound a hang, not a large result. See wait_until_ready.
        self._progress: "Dict[tuple, list]" = {}

    def start(self, var_name: str) -> "tuple[int, threading.Event]":
        """Register a new run for ``var_name``, cancelling any prior in-flight run.

        Returns (generation_token, cancel_event) for the new run.
        """
        with self._lock:
            prior = self._cancel.get(var_name)
            if prior is not None:
                prior.set()  # signal the superseded run to stop
            gen = self._generation.get(var_name, 0) + 1
            self._generation[var_name] = gen
            event = threading.Event()
            self._cancel[var_name] = event
            # Arm this run's completion signal. A fresh Event per (var_name, gen); any
            # prior generation's Event/result/error stays under its own key untouched, so
            # a waiter already blocked on an older generation is unaffected. The prior
            # generation's retained frame is reclaimed by its own run's reap() (consumer
            # count 0) or by the last bound proxy's release_consumer -- not here, so we
            # never yank a completion Event out from under a still-blocked waiter.
            self._done[(var_name, gen)] = threading.Event()
            self._result.pop((var_name, gen), None)
            self._error.pop((var_name, gen), None)
            # Arm progress at "just started" so the stall clock runs from now; the first
            # page write (or settle) advances it.
            self._progress[(var_name, gen)] = [0, time.monotonic()]
            return gen, event

    def is_current(self, var_name: str, gen: int) -> bool:
        """True if ``gen`` is still the newest run for ``var_name``."""
        with self._lock:
            return self._generation.get(var_name) == gen

    def finish(self, var_name: str, gen: int) -> None:
        """Clear registry state for a run if it is still the current one."""
        with self._lock:
            if self._generation.get(var_name) == gen:
                self._cancel.pop(var_name, None)

    # --- Completion signal (consumed by PendingDataFrame waiters) ---

    def settle(
        self,
        var_name: str,
        gen: int,
        result: "Optional[Any]" = None,
        error: "Optional[BaseException]" = None,
    ) -> None:
        """Settle the ``(var_name, gen)`` completion signal exactly once.

        Called by the background thread on every terminal outcome. On success pass the
        materialized ``result`` DataFrame; on failure/supersession/cancel pass an
        ``error`` (a waiter then raises it). Idempotent: if the Event is already set (a
        second terminal path), the later call is ignored so the first outcome wins. Safe
        to call for a generation whose Event was never armed (defensive no-op).
        """
        key = (var_name, gen)
        with self._lock:
            event = self._done.get(key)
            if event is None or event.is_set():
                return
            if error is not None:
                self._error[key] = error
            else:
                self._result[key] = result
            event.set()

    def note_progress(self, var_name: str, gen: int) -> None:
        """Record that materialization advanced (one page written) for ``(var_name, gen)``.

        Bumps the page counter and stamps the change time, so a waiter blocked in
        ``wait_until_ready`` treats the run as healthy-and-advancing rather than stalled.
        Called from the background page-write loop. No-op if the run was already reaped."""
        with self._lock:
            p = self._progress.get((var_name, gen))
            if p is not None:
                p[0] += 1
                p[1] = time.monotonic()

    def wait_until_ready(self, var_name: str, gen: int, timeout: "Optional[float]" = None) -> bool:
        """Block until ``(var_name, gen)`` settles, or materialization STALLS.

        ``timeout`` here is a STALL window, not a total-duration cap: the wait only gives up
        if materialization makes no progress (no new page via ``note_progress``) for
        ``timeout`` seconds. A healthy-but-large result that keeps writing pages is waited on
        indefinitely; only a genuinely hung run (query/network wedged, thread dead) times
        out. This bounds a HANG without false-failing a slow-but-progressing materialization
        -- the reason a fixed total cap was wrong (it bounds query execution, but this wait
        covers rebuffering every row + one S3 PUT per page, which legitimately exceeds any
        fixed cap for a big result). ``timeout=None`` waits with no stall bound.

        Returns True if the run settled, False on stall-timeout. If the generation was never
        armed (or already reaped), returns True immediately.
        """
        with self._lock:
            event = self._done.get((var_name, gen))
        if event is None:
            return True
        if timeout is None:
            event.wait()
            return True
        # Poll in slices; reset patience whenever progress advanced since the last slice.
        # ``deadline`` is an absolute backstop: it starts as (now + timeout) and is pushed
        # forward on every observed progress. If the progress record is missing (e.g. the
        # run was reaped mid-wait), we do NOT push the deadline, so the backstop still fires
        # -- a missing record can never turn this into an unbounded wait.
        slice_seconds = min(timeout, 5.0)
        deadline = time.monotonic() + timeout
        while True:
            if event.wait(slice_seconds):
                return True
            with self._lock:
                p = self._progress.get((var_name, gen))
                last_change = p[1] if p is not None else None
            if last_change is not None:
                # Progressing: extend the backstop to (last page time + stall window).
                deadline = last_change + timeout
            if time.monotonic() >= deadline:
                # Either no page for the full stall window, or the progress record is gone
                # and the absolute backstop elapsed -> treat as hung.
                return event.wait(0)  # final non-blocking check in case it settled just now

    def get_result(self, var_name: str, gen: int) -> "Any":
        """Return the materialized DataFrame for a settled run, or raise its error.

        Must be called only after ``wait_until_ready`` returns True. Raises ``KeyError``
        if the run never settled a result AND recorded no error (defensive -- should not
        happen once settle() runs on every terminal path). Raises the recorded error for a
        failed/superseded run.
        """
        key = (var_name, gen)
        with self._lock:
            if key in self._error:
                raise self._error[key]
            if key in self._result:
                return self._result[key]
        raise KeyError(f"No settled result for {var_name!r} generation {gen}")

    def consume_result(self, var_name: str, gen: int) -> Any:
        """Atomically read this run's result AND release this consumer, under ONE lock.

        Folds ``get_result`` + ``release_consumer`` into a single critical section so two
        threads resolving the same proxy concurrently cannot race: without this, thread A's
        release could drop ``_result`` between thread B's read and B's release, so B's
        separate ``get_result`` would raise ``KeyError``. Here the frame is read and the
        consumer decremented together, and the read value is returned even when this call is
        the last consumer and drops the slot. Raises the recorded terminal error for a
        failed/superseded run (before touching the consumer count, matching get_result).
        Must be called only after ``wait_until_ready`` returns True."""
        key = (var_name, gen)
        with self._lock:
            if key in self._error:
                # Failed/superseded: raise as get_result would. Still release the consumer
                # so a failed run does not leak its _error/_consumers entries (the error
                # object is small but the count is unbounded across runs).
                err = self._error[key]
                remaining = self._consumers.get(key, 0) - 1
                if remaining > 0:
                    self._consumers[key] = remaining
                else:
                    self._consumers.pop(key, None)
                    self._result.pop(key, None)
                    self._error.pop(key, None)
                raise err
            if key not in self._result:
                raise KeyError(f"No settled result for {var_name!r} generation {gen}")
            result = self._result[key]
            remaining = self._consumers.get(key, 0) - 1
            if remaining > 0:
                self._consumers[key] = remaining
            else:
                # Last (or only) consumer: drop the registry's copy. The frame survives in
                # the caller's returned reference (and, after commit, the namespace).
                self._consumers.pop(key, None)
                self._result.pop(key, None)
                self._error.pop(key, None)
            return result

    def retain(self, var_name: str, gen: int) -> None:
        """Register one live proxy bound to ``(var_name, gen)``. Called from
        ``PendingDataFrame.__init__``. Paired with ``release_consumer`` on resolve, so the
        registry knows when the last consumer has cached the frame and the retained
        result slot can be dropped."""
        with self._lock:
            key = (var_name, gen)
            self._consumers[key] = self._consumers.get(key, 0) + 1

    def release_consumer(self, var_name: str, gen: int) -> None:
        """Mark one proxy for ``(var_name, gen)`` as resolved (it has cached the frame in
        its own ``_real``). When the last consumer releases, drop the retained
        ``_result``/``_error`` so the frame is no longer held by the module-level registry
        -- it then lives only in the resolved proxy and (after commit) the namespace. Safe
        if called for an already-reaped run (no-op)."""
        with self._lock:
            key = (var_name, gen)
            remaining = self._consumers.get(key, 0) - 1
            if remaining > 0:
                self._consumers[key] = remaining
                return
            self._consumers.pop(key, None)
            # Last (or only) consumer resolved: the frame is cached in the proxy's _real,
            # so the registry's copy is now dead weight. Drop it. Keep _done as-is; reap
            # (or a future start) handles the signal's lifecycle.
            self._result.pop(key, None)
            self._error.pop(key, None)

    def reap(self, var_name: str, gen: int) -> None:
        """Drop the completion signal for a fully-consumed run, and the result/error slot
        UNLESS a proxy is still bound (consumer count > 0). Called from the background
        thread's ``finally`` after settle(). If a proxy is still waiting, its
        ``release_consumer`` (on resolve) drops the frame instead -- so a large result is
        never retained for the life of the kernel, whether it was consumed before or after
        reap. A late waiter that finds no Event falls through ``wait_until_ready``->True;
        if reap already dropped its slot (no consumer was registered) ``get_result`` raises
        KeyError, which only happens when no proxy is bound to read it anyway."""
        key = (var_name, gen)
        with self._lock:
            self._done.pop(key, None)
            self._progress.pop(key, None)
            # Only reclaim the frame here if no live proxy is waiting to read it. If a
            # proxy IS bound (count > 0), leave _result/_error for it and let its
            # release_consumer drop the slot once it has resolved.
            if self._consumers.get(key, 0) <= 0:
                self._consumers.pop(key, None)
                self._result.pop(key, None)
                self._error.pop(key, None)

    def commit(
        self,
        var_name: str,
        gen: int,
        action: "Callable[[], None]",
        inflight_key: "Optional[tuple]" = None,
    ) -> bool:
        """Atomically run ``action`` (the namespace write) iff ``gen`` is still current
        AND (when ``inflight_key`` is given) this run still owns its ``_inflight`` entry.

        Holding the lock across the generation check + ``action`` closes the TOCTOU window
        where a newer run could supersede between the check and the write (clobbering the
        newer result). The ``inflight_key`` check makes the inflight entry the single
        terminal-ownership token: ``flush_inflight_on_exit`` removes it under this same lock
        when it finalizes a run as failed at shutdown, so if flush already claimed this run,
        ``commit`` returns False and the daemon stands down (no COMPLETE manifest, no success
        emit) instead of racing a contradictory success against the flush's failed
        finalization. First to the lock wins; the loser emits nothing.

        Running ``action`` under the lock is safe because ``self._lock`` is an RLock: the
        namespace write can drop the last reference to the name's ``PendingDataFrame`` proxy,
        whose ``weakref.finalize`` fires synchronously on THIS SAME THREAD and re-acquires
        the lock via ``release_consumer``. A plain Lock would self-deadlock there; the RLock
        lets the same thread re-enter. Returns True if ``action`` ran (this run owns the
        outcome).
        """
        with self._lock:
            if self._generation.get(var_name) != gen:
                return False
            if inflight_key is not None and inflight_key not in self._inflight:
                # Flush (or another terminal path) already claimed this run's finalization.
                return False
            action()
            if inflight_key is not None:
                self._inflight.pop(inflight_key, None)
            return True

    def mark_inflight(self, key: "tuple", run: "_InFlightRun") -> None:
        """Track a run so ``flush_inflight_on_exit`` can finalize it if the process
        shuts down before the run's own ``finally`` clears it."""
        with self._lock:
            self._inflight[key] = run

    def clear_inflight(self, key: "tuple") -> None:
        with self._lock:
            self._inflight.pop(key, None)

    def claim_terminal(self, key: "Optional[tuple]") -> bool:
        """Atomically claim the right to finalize a run: pop its ``_inflight`` entry and
        return True only if THIS caller removed it. Makes failure finalization single-owner
        (like the success path's ``commit``) -- if ``flush_inflight_on_exit`` already claimed
        and emitted ``dataframe_ready(failed)`` at shutdown, the daemon's own except branch
        sees the entry gone and does NOT emit a duplicate. ``key=None`` (no inflight tracked)
        counts as a claim so single-statement/non-tracked runs still emit once."""
        if key is None:
            return True
        with self._lock:
            return self._inflight.pop(key, None) is not None

    def flush_inflight_on_exit(self) -> None:
        """atexit hook: on graceful interpreter shutdown (kernel stop_session / restart),
        finalize any run whose background thread never reached its ``finally`` -- write a
        terminal ``failed`` manifest and emit ``dataframe_ready(failed)`` so a killed run
        does not leave an ``in_progress`` manifest / a UI card / the KernelServer gate
        waiting forever. Best-effort; does NOT cover SIGKILL/OOM (atexit does not run)."""
        with self._lock:
            # Snapshot AND transition under the lock: for each still-in-progress run, flip
            # its manifest to FAILED here so the decision + write is atomic w.r.t. any other
            # lock holder. A run that already reached a terminal status (complete / failed)
            # at one of its own terminal points is skipped -- never re-finalized as failed
            # (which would overwrite COMPLETE or emit a duplicate). (A daemon thread still
            # mutates its manifest without the lock; taking the lock here is the tightest
            # we can be without routing the thread's terminal writes through it too.)
            to_finalize = []
            for run in self._inflight.values():
                if run.manifest.status == STATUS_IN_PROGRESS:
                    run.manifest.status = STATUS_FAILED
                    to_finalize.append(run)
            self._inflight.clear()
        for run in to_finalize:
            try:
                run.write_manifest_fn(manifest_key(run.prefix), run.manifest.to_json())
            except Exception:
                logger.debug("atexit: failed to write terminal manifest", exc_info=True)
            try:
                run.emit_ready_fn(run.execution_id, READY_FAILED)
            except Exception:
                logger.debug("atexit: failed to emit dataframe_ready(failed)", exc_info=True)


@dataclass
class _InFlightRun:
    """State an in-flight materialization needs so ``flush_inflight_on_exit`` can write
    its terminal manifest and emit failure at shutdown."""

    execution_id: str
    prefix: str
    manifest: "Manifest"
    write_manifest_fn: "Callable[[str, str], None]"
    emit_ready_fn: "Callable[[str, str], None]"


# Module-level singleton (persists for the kernel process lifetime).
_registry = _MaterializationRegistry()

# Finalize any in-flight runs on graceful shutdown so they never leak (see flush docs).
atexit.register(_registry.flush_inflight_on_exit)


def _rebuffer_to_pages(
    first_page: List[Any],
    remaining: Iterator[List[Any]],
    rows_per_page: int,
    cancel: threading.Event,
) -> Iterator[List[Any]]:
    """Re-buffer variable-size engine chunks into fixed ``rows_per_page`` pages.

    ``first_page`` is the already-fetched inline page (reused verbatim so the S3
    page_000 matches the inline first page from the same frozen execution_id).
    Yields lists of rows of length ``rows_per_page`` (last page may be shorter).
    Stops early if ``cancel`` is set.
    """
    buffer: List[Any] = list(first_page)
    while len(buffer) >= rows_per_page:
        yield buffer[:rows_per_page]
        buffer = buffer[rows_per_page:]

    for chunk in remaining:
        if cancel.is_set():
            return
        buffer.extend(chunk)
        while len(buffer) >= rows_per_page:
            yield buffer[:rows_per_page]
            buffer = buffer[rows_per_page:]

    if buffer:
        yield buffer


# Connection types eligible for the async path. Everything else falls back to sync.
ASYNC_SUPPORTED_CONNECTION_TYPES = {"ATHENA", "REDSHIFT"}


def _write_failed(
    manifest: Manifest, prefix: str, write_manifest_fn: "Callable[[str, str], None]"
) -> None:
    manifest.status = STATUS_FAILED
    try:
        write_manifest_fn(manifest_key(prefix), manifest.to_json())
    except Exception:
        logger.debug("Failed to write failed-status manifest", exc_info=True)


def extract_output_rows(stats: "Optional[Dict[str, Any]]") -> Optional[int]:
    """Pull ``QueryRuntimeStatistics.Rows.OutputRows`` from a GetQueryRuntimeStatistics
    response, or return None when it is not present.

    CRITICAL: distinguishes "not populated yet" (Athena stats lag -> the field is
    absent -> None) from a genuine empty result (``OutputRows == 0`` -> 0). The caller
    only stamps a returned value that is ``>= manifest.row_count`` (the rows already
    counted): a genuine empty result stamps as ``0 >= 0`` while a lag-induced 0 (which is
    ``< row_count`` once any page is written) is rejected and polling continues -- never
    surfacing a bogus 0 the way the old Query Editor's retry-then-default-to-0 mitigation
    could. A None return (absent/unexpected shape) keeps polling / falls back to the
    counted row_count, never a spurious number.
    """
    if not stats:
        return None
    rows = (stats.get("QueryRuntimeStatistics") or {}).get("Rows") or {}
    value = rows.get("OutputRows")
    return value if isinstance(value, int) else None


def _background_materialize(
    *,
    dataframe_name: str,
    columns: List[str],
    first_page_rows: List[Any],
    remaining_rows: "Iterator[List[Any]]",
    prefix: str,
    execution_id: str,
    gen: int,
    cancel: "threading.Event",
    registry: "_MaterializationRegistry",
    rows_per_page: int,
    assign_namespace_fn: "Callable[[str, Any], None]",
    write_page_fn: "Callable[[str, Any], None]",
    write_manifest_fn: "Callable[[str, str], None]",
    emit_ready_fn: "Callable[[str, str], None]",
    on_settle: "Optional[Callable[[Any], None]]" = None,
    total_rows: Optional[int] = None,
    stats_fn: "Optional[Callable[[], Optional[int]]]" = None,
) -> None:
    """Background body: stream fixed pages to S3, then write the full DataFrame
    into the namespace and emit dataframe_ready. Runs on a daemon thread.

    ``total_rows``: an exact upfront total the engine gave cheaply (Redshift
    ``TotalNumRows``); stamped into the manifest immediately so the UI shows it from the
    first page write. ``stats_fn``: an optional best-effort callable (Athena only) that
    returns ``OutputRows`` or None; called after each page write until it yields a non-None
    value, then the exact total is stamped and the calls stop. When neither yields a total,
    the manifest's ``total_rows`` stays None and the UI falls back to the counted
    ``row_count`` (exact once ``status=='complete'``) -- never a lag-induced 0."""
    from pandas import DataFrame

    manifest = Manifest(rowPerPages=rows_per_page, total_rows=total_rows)
    all_rows: List[Any] = []
    # Bound the per-page GetQueryRuntimeStatistics polling (#6): stop permanently after a
    # non-transient error (AccessDenied / DDL / non-Presto has no OutputRows) or after
    # _STATS_MAX_ATTEMPTS misses, so a never-populating query does not fire one control-plane
    # call per page for ~100 pages. Generous cap: on the happy path we stop at the first hit,
    # and the exact-count fallback preserves correctness when the cap is reached.
    stats_attempts = 0
    stats_stopped = False
    settled_df: Any = None  # full DataFrame if this run wins; None if cancelled/superseded/failed
    committed = (
        False  # True once the namespace bind succeeded -> post-commit errors are best-effort
    )
    terminal_error: "Optional[BaseException]" = (
        None  # non-success reason, raised to PendingDataFrame waiters
    )
    inflight_key = (dataframe_name, gen)
    registry.mark_inflight(
        inflight_key,
        _InFlightRun(
            execution_id=execution_id,
            prefix=prefix,
            manifest=manifest,
            write_manifest_fn=write_manifest_fn,
            emit_ready_fn=emit_ready_fn,
        ),
    )
    try:
        page_index = 0
        for page_rows in _rebuffer_to_pages(first_page_rows, remaining_rows, rows_per_page, cancel):
            if cancel.is_set():
                # Superseded mid-stream by a newer run of this var (a same-cell re-run).
                # Write a terminal manifest for S3 hygiene and stop; no dataframe_ready is
                # emitted -- the re-run replaced this run's output, so there is no live card
                # to resolve.
                _write_failed(manifest, prefix, write_manifest_fn)
                registry.clear_inflight(inflight_key)  # terminal: drop before the flush can see it
                terminal_error = _AsyncMaterializationSuperseded(dataframe_name)
                return
            write_page_fn(page_key(prefix, page_index), DataFrame(page_rows, columns=columns))
            all_rows.extend(page_rows)
            page_index += 1
            manifest.totalfiles = page_index
            manifest.row_count = len(all_rows)
            # Progress heartbeat for the stall-based resolve wait: a waiter treats this run
            # as advancing (not hung) as long as pages keep landing.
            registry.note_progress(dataframe_name, gen)
            # Best-effort exact total off the page loop (Athena: GetQueryRuntimeStatistics
            # OutputRows; stats_fn is None for Redshift, which already stamped total_rows
            # upfront). Retry once per page until it yields a non-None value, then stop --
            # so a freshly-fetched total lands in THIS manifest write, no extra write. Gate
            # on ``is not None`` so a genuine empty result (0) is stamped while a lagging
            # absent value keeps polling; swallow+log any error (never fail the run for a
            # metadata read). Adds no foreground latency -- runs on this daemon thread only.
            if manifest.total_rows is None and stats_fn is not None and not stats_stopped:
                stats_attempts += 1
                try:
                    fetched = stats_fn()
                except Exception:
                    # Swallow and retry on the next page: the error may be transient (a
                    # throttle, a not-yet-ready stats endpoint). It still counts toward
                    # _STATS_MAX_ATTEMPTS below, so a persistently-failing call (AccessDenied
                    # for a role without athena:GetQueryRuntimeStatistics, or DDL that never
                    # has stats) stops after the cap instead of firing once per page for the
                    # whole result.
                    logger.debug(
                        "GetQueryRuntimeStatistics failed; will retry until cap", exc_info=True
                    )
                    fetched = None
                # #5 lag-0 gate: only stamp a fetched total that is at least the rows we have
                # ALREADY counted. A real result's OutputRows is >= what we've paged; a
                # lag-induced 0 (stats not settled) is < row_count once any page is written,
                # so it is rejected and polling continues. A genuine empty result has
                # row_count == 0, so fetched == 0 >= 0 stamps correctly. Never writes a
                # lag-induced 0 as the exact total.
                if fetched is not None and fetched >= manifest.row_count:
                    manifest.total_rows = fetched
                elif stats_attempts >= _STATS_MAX_ATTEMPTS:
                    # Cap reached without a usable total (persistent error, or OutputRows
                    # that never populates / never catches up to row_count): stop polling.
                    # The UI falls back to the exact counted row_count at status=='complete'.
                    stats_stopped = True
            write_manifest_fn(manifest_key(prefix), manifest.to_json())

        # Heartbeat once more before the (potentially large) frame build + commit: for a
        # result big enough that DataFrame(all_rows) alone exceeds the stall window, a waiter
        # would otherwise false-time-out on a healthy run between the last page write and the
        # namespace bind. This stamps progress so the stall clock is reset going into finalize.
        registry.note_progress(dataframe_name, gen)

        # Build the full DataFrame, then commit the namespace write ATOMICALLY: commit()
        # re-checks the generation under the registry lock, closing the window where a run
        # superseded during the (possibly slow) DataFrame build could clobber a newer
        # result. Only the current run writes the namespace / signals success.
        full_df = DataFrame(all_rows, columns=columns)

        def _commit() -> None:
            nonlocal settled_df
            assign_namespace_fn(dataframe_name, full_df)
            settled_df = full_df

        if registry.commit(dataframe_name, gen, _commit, inflight_key=inflight_key):
            # Past the point of no return: df is bound in the namespace and the run is a
            # success. The COMPLETE manifest write + success emit below are best-effort
            # finalization -- if one raises (e.g. a transient S3 put error) the except must
            # NOT re-finalize this run as failed (df is already good), so mark committed.
            committed = True
            manifest.status = STATUS_COMPLETE
            write_manifest_fn(manifest_key(prefix), manifest.to_json())
            emit_ready_fn(execution_id, READY_SUCCESS)
        else:
            # Either superseded by a newer run, OR the atexit flush already claimed this
            # run's finalization at shutdown (removed the inflight entry under the lock).
            # In both cases do NOT bind the namespace or emit dataframe_ready -- the flush
            # already emitted failed (or a newer run owns the card). Write a terminal
            # manifest for S3 hygiene; this is idempotent with the flush's own FAILED write.
            logger.info(
                "Async materialization for '%s' was superseded or flush-claimed; "
                "skipping namespace write and success emit",
                dataframe_name,
            )
            _write_failed(manifest, prefix, write_manifest_fn)
            terminal_error = _AsyncMaterializationSuperseded(dataframe_name)
    except Exception as exc:
        logger.exception("Async materialization failed for execution %s", execution_id)
        terminal_error = exc
        if committed:
            # A post-commit finalization step (COMPLETE manifest write / success emit)
            # raised. df is already bound and correct -- do NOT mark the run failed or emit
            # dataframe_ready(failed). The error is logged; the card resolves via the
            # success emit (or the UI's manifest-stall timeout if that emit was the failure).
            pass
        else:
            _write_failed(manifest, prefix, write_manifest_fn)
            # Single-owner finalization (symmetric with the success path's commit): only
            # emit failed if we still own the inflight entry. If flush already claimed and
            # emitted failed for this run at shutdown, claim_terminal returns False -> no
            # duplicate dataframe_ready(failed) for the same execution_id.
            if registry.claim_terminal(inflight_key):
                emit_ready_fn(execution_id, READY_FAILED)
    finally:
        registry.clear_inflight(inflight_key)
        registry.finish(dataframe_name, gen)
        # Settle the PendingDataFrame completion signal exactly once, on EVERY terminal
        # path (success / failure / supersession / cancel), so a proxy waiter never hangs.
        # On success (settled_df bound, or committed with a best-effort post-commit error)
        # hand over the real df; otherwise hand over the terminal error for the waiter to
        # raise. committed implies the df was bound even if a later finalization step threw.
        if settled_df is not None or committed:
            registry.settle(dataframe_name, gen, result=settled_df)
        else:
            registry.settle(
                dataframe_name,
                gen,
                error=terminal_error or _AsyncMaterializationFailed(dataframe_name),
            )
        registry.reap(dataframe_name, gen)
        # Always settle the completion barrier exactly once -- even on cancel /
        # supersession / failure -- so a multi-statement consolidated df never hangs.
        if on_settle is not None:
            try:
                on_settle(settled_df)
            except Exception:
                logger.debug("Async materialization barrier settle failed", exc_info=True)


def _flatten_nested_columns(dataframe: Any) -> Any:
    """Convert columns whose values are dicts/lists to JSON strings so pyarrow does not
    build nested (struct/list) Parquet schemas the UI grid can't render. Matches the
    kernel formatter: a column is flattened if its first non-null value is a dict/list;
    other scalars in that column are stringified; nulls stay None. Returns the original
    frame unchanged when nothing needs flattening (no copy)."""
    import json

    from pandas import isna

    cols_to_flatten = []
    for col in dataframe.columns:
        non_null = dataframe[col].dropna()
        if len(non_null) and isinstance(non_null.iloc[0], (dict, list)):
            cols_to_flatten.append(col)
    if not cols_to_flatten:
        return dataframe
    df = dataframe.copy()
    for col in cols_to_flatten:
        df[col] = df[col].apply(
            lambda x: (
                json.dumps(x, default=str)
                if isinstance(x, (dict, list))
                else (None if isna(x) else str(x))
            )
        )
    return df


def _escape_dotted_columns(dataframe: Any) -> "tuple[Any, Dict[str, str]]":
    """Escape dotted column names (``a.b`` -> ``a__DOT__b``) and return the escaped frame
    plus a ``{escaped: original}`` mapping the UI un-escapes from. Matches the kernel
    formatter. Returns the frame unchanged (empty mapping) when no name has a dot."""
    mapping: Dict[str, str] = {}
    escaped = []
    for col in dataframe.columns.tolist():
        if "." in str(col):
            e = str(col).replace(".", "__DOT__")
            mapping[e] = col
            escaped.append(e)
        else:
            escaped.append(col)
    if mapping:
        df = dataframe.copy()
        df.columns = escaped
        return df, mapping
    return dataframe, {}


def _df_to_parquet_bytes(dataframe: Any) -> bytes:
    """Serialize a DataFrame to snappy-Parquet bytes with the SAME transforms the kernel
    formatter applies, so async pages/first-page decode identically in the UI: nested
    columns JSON-stringified + dotted names escaped with a ``column_name_mapping`` in the
    Parquet key-value metadata. Single source of truth for both the inline first page and
    the S3 page writes (the kernel formatter should import this to drop its duplicate)."""
    import io
    import json

    import pyarrow as pa
    import pyarrow.parquet as pq

    df, column_mapping = _escape_dotted_columns(dataframe)
    df = _flatten_nested_columns(df)
    table = pa.Table.from_pandas(df, preserve_index=False)
    if column_mapping:
        meta = dict(table.schema.metadata or {})
        meta[b"column_name_mapping"] = json.dumps(column_mapping).encode("utf-8")
        table = table.replace_schema_metadata(meta)
    buffer = io.BytesIO()
    pq.write_table(table, buffer, compression="snappy")
    return buffer.getvalue()


@dataclass
class AsyncSqlResult:
    """Display object for the async first page.

    Its ``_repr_mimebundle_`` emits ``ASYNC_SQL_MIMETYPE`` carrying the sync-reply payload
    (execution_id + s3 prefix + total_rows) plus the inline first page as base64 snappy
    parquet, so the UI renders page 0 instantly and paginates the rest from S3 via the
    manifest. Displaying this object (not a bare DataFrame) also bypasses the kernel's
    ``_LargeDataframeFormatter`` (which is DataFrame-typed).
    """

    execution_id: str
    s3_path: str
    columns: List[str]
    first_page_rows: List[Any]
    total_rows: Optional[int] = None
    redshift_query_id: Optional[int] = None

    def _first_page_parquet_b64(self) -> str:
        import base64

        from pandas import DataFrame

        df = DataFrame(self.first_page_rows, columns=self.columns)
        return base64.b64encode(_df_to_parquet_bytes(df)).decode("utf-8")

    def _repr_mimebundle_(self, include=None, exclude=None):
        payload: Dict[str, Any] = {
            "execution_id": self.execution_id,
            "s3_path": self.s3_path,
            "total_rows": self.total_rows,
            "data": self._first_page_parquet_b64(),
        }
        if self.redshift_query_id is not None:
            payload["redshift_query_id"] = self.redshift_query_id
        return {
            ASYNC_SQL_MIMETYPE: payload,
            "text/plain": (
                f"[async SQL result] {len(self.first_page_rows)} rows shown -- "
                f"full result materializing to {self.s3_path}"
            ),
        }


def materialize_async(
    *,
    dataframe_name: str,
    columns: List[str],
    first_page_rows: List[Any],
    remaining_rows: "Iterator[List[Any]]",
    execution_id: str,
    project_s3_root: str,
    # Upfront row count when the engine provides it cheaply (Redshift TotalNumRows);
    # None for Athena (no cheap upfront count) -> the UI paginates from the manifest.
    total_rows: Optional[int] = None,
    display_fn: "Callable[[Any], None]",
    assign_namespace_fn: "Callable[[str, Any], None]",
    write_page_fn: "Callable[[str, Any], None]",
    write_manifest_fn: "Callable[[str, str], None]",
    emit_ready_fn: "Callable[[str, str], None]",
    on_settle: "Optional[Callable[[Any], None]]" = None,
    bind_pending_fn: "Optional[Callable[[str, int, _MaterializationRegistry], None]]" = None,
    stats_fn: "Optional[Callable[[], Optional[int]]]" = None,
    extra_retain: bool = False,
    registry: "_MaterializationRegistry" = _registry,
    rows_per_page: int = ROWS_PER_PAGE,
    redshift_query_id: Optional[int] = None,
) -> Dict[str, Any]:
    """Display the inline first page and spawn the background materialization.

    Returns the sync-reply payload ``{execution_id, s3_path, total_rows, dataframe_name,
    gen}`` -- ``dataframe_name``/``gen`` are exposed so ``materialize_async_multi`` can build
    the consolidated ``df`` list from the same per-index proxies. The full
    DataFrame is written to the kernel namespace and ``dataframe_ready`` is emitted
    later, from the background daemon thread.

    ``stats_fn``: optional best-effort exact-total fetcher (Athena
    GetQueryRuntimeStatistics OutputRows), called off the background page loop until it
    yields a value. None for Redshift, which passes the exact ``total_rows`` upfront.
    """
    prefix = build_result_prefix(project_s3_root, execution_id)

    # Inline first page as a display object carrying the sync-reply payload (execution_id
    # + s3 prefix + total_rows) so the UI renders page 0 instantly and paginates the rest
    # from S3. Displaying this wrapper (not a bare DataFrame) also bypasses the kernel's
    # _LargeDataframeFormatter.
    display_fn(
        AsyncSqlResult(
            execution_id=execution_id,
            s3_path=prefix,
            columns=columns,
            first_page_rows=first_page_rows,
            total_rows=total_rows,
            redshift_query_id=redshift_query_id,
        )
    )

    gen, cancel = registry.start(dataframe_name)

    # extra_retain (multi only): bump the consumer count for this (name, gen) BEFORE the
    # daemon is spawned, so the daemon's reap can never drop _result before the caller
    # (materialize_async_multi) builds the consolidated-list proxy that will read it. The
    # consolidated proxy is created on the main thread only AFTER this returns, by which
    # point a tiny result's daemon may already have committed + reaped; retaining pre-spawn
    # is the only point guaranteed to be before reap. The caller releases this placeholder
    # once the consolidated proxy (which retains on its own) exists, leaving a net count of
    # one live consumer. Best-effort: a registry without retain is tolerated.
    if extra_retain:
        _pre_retain = getattr(registry, "retain", None)
        if _pre_retain is not None:
            _pre_retain(dataframe_name, gen)

    # Bind the name to a PendingDataFrame proxy IMMEDIATELY (before the background thread
    # finishes), so during the pending window `dataframe_name` is a real, waitable object
    # rather than unbound (NameError) or None (AttributeError). A downstream cell that
    # touches it blocks-then-resolves instead of erroring; DuckDB's pre-resolve pass can
    # also find it by isinstance. On completion the background thread rebinds the name to
    # the real DataFrame (swap, don't spoof).
    #
    # #2: everything between registry.start() and a SUCCESSFUL thread .start() must settle
    # the generation on failure. Otherwise the completion Event is armed but never set, and
    # a waiter (the bound proxy, or a downstream cell) blocks for the full resolve timeout
    # before raising. On any failure here we settle an error so the waiter fails fast.
    try:
        if bind_pending_fn is not None:
            bind_pending_fn(dataframe_name, gen, registry)

        threading.Thread(
            target=_background_materialize,
            kwargs=dict(
                dataframe_name=dataframe_name,
                columns=columns,
                first_page_rows=first_page_rows,
                remaining_rows=remaining_rows,
                prefix=prefix,
                execution_id=execution_id,
                gen=gen,
                cancel=cancel,
                registry=registry,
                rows_per_page=rows_per_page,
                assign_namespace_fn=assign_namespace_fn,
                write_page_fn=write_page_fn,
                write_manifest_fn=write_manifest_fn,
                emit_ready_fn=emit_ready_fn,
                on_settle=on_settle,
                total_rows=total_rows,
                stats_fn=stats_fn,
            ),
            name=f"async-materialize-{execution_id}",
            daemon=True,
        ).start()
    except Exception:
        # The background thread never started (or bind raised): settle an error so any
        # waiter raises immediately instead of hanging until the resolve timeout, then
        # re-raise so the caller's own failure handling (e.g. materialize_async_multi's
        # spawn-failure branch) runs as before.
        logger.exception("Async materialization failed to start for %s", dataframe_name)
        # Release the pre-spawn placeholder retain (extra_retain) before settling: the
        # caller never reaches its post-proxy release on this failure path, so drop it here
        # so a failed spawn does not leak a consumer that would pin _error.
        if extra_retain:
            _rel = getattr(registry, "release_consumer", None)
            if _rel is not None:
                _rel(dataframe_name, gen)
        registry.settle(dataframe_name, gen, error=_AsyncMaterializationFailed(dataframe_name))
        registry.clear_inflight((dataframe_name, gen))
        # reap drops the _done Event entry (which settle armed) so a failed spawn does not
        # retain it. reap keeps _error while a proxy is still bound (consumers > 0) -- the
        # bind_pending_fn proxy above -- so that proxy still fails fast with the settled
        # error; its release_consumer/finalize then drops _error, leaking nothing.
        registry.reap(dataframe_name, gen)
        raise

    return {
        "execution_id": execution_id,
        "s3_path": prefix,
        "total_rows": total_rows,
        # Exposed so materialize_async_multi can bind the CONSOLIDATED df to a real list
        # of these same per-index PendingDataFrame proxies during the pending window,
        # keeping df[i] block-then-resolvable and df itself a genuine list.
        "dataframe_name": dataframe_name,
        "gen": gen,
    }


@dataclass
class AsyncResultMarker:
    """Returned by the per-statement async executor for a result-bearing statement.

    Carries only the engine execution_id — the rows are fetched later, by id, via a
    fresh client (so ``execute_statements`` stays the single iteration/error-handling
    path and no rows are fetched inside the statement loop).
    """

    execution_id: Optional[str] = None
    redshift_query_id: Optional[int] = None


@dataclass
class StatementSpec:
    """One statement in a (possibly multi-statement) cell.

    kind='result' -> async-materialized; rows are fetched lazily by execution_id via the
    ``reader_factory`` passed to ``materialize_async_multi``. kind='dml' -> no result set;
    rowcount is assigned synchronously to preserve today's ``df_i = rowcount`` behavior.
    """

    index: int
    kind: str  # "result" | "dml"
    execution_id: Optional[str] = None
    rowcount: Optional[int] = None
    redshift_query_id: Optional[int] = None


def spec_from_result(exec_result: Any) -> "StatementSpec":
    """Classify a SqlExecutor ExecutionResult into a StatementSpec.

    A result-bearing statement's executor returns an AsyncResultMarker (carrying the
    execution_id); a DML statement returns an int rowcount.
    """
    payload = exec_result.result
    if isinstance(payload, AsyncResultMarker):
        return StatementSpec(
            index=exec_result.statement_index,
            kind="result",
            execution_id=payload.execution_id,
            redshift_query_id=payload.redshift_query_id,
        )
    return StatementSpec(index=exec_result.statement_index, kind="dml", rowcount=payload)


def materialize_async_multi(
    *,
    base_name: str,
    specs: List[StatementSpec],
    project_s3_root: str,
    reader_factory: "Callable[[str], Any]",
    display_fn: "Callable[[Any], None]",
    assign_namespace_fn: "Callable[[str, Any], None]",
    write_page_fn: "Callable[[str, Any], None]",
    write_manifest_fn: "Callable[[str, str], None]",
    emit_ready_fn: "Callable[[str, str], None]",
    bind_pending_fn: "Optional[Callable[[str, int, _MaterializationRegistry], None]]" = None,
    make_pending_fn: "Optional[Callable[[str, int, _MaterializationRegistry], Any]]" = None,
    registry: "_MaterializationRegistry" = _registry,
    rows_per_page: int = ROWS_PER_PAGE,
) -> List[Dict[str, Any]]:
    """Materialize every result-bearing statement in a cell, preserving today's
    namespace semantics.

    Single successful statement -> the result is bound to ``base_name`` (``df``).
    Multiple -> each statement binds ``base_name_{index}`` (``df_0``, ``df_1`` …) and the
    consolidated ``df`` list ``[result_0, …]`` is assigned once ALL result-bearing
    statements settle (completion barrier). DML rowcounts are recorded immediately.

    DML-only cells (no result-bearing statement) are handled in-place here (display +
    namespace bind) rather than deferred, so the caller never has to re-run the query.
    The barrier settles on every terminal outcome (success / cancel / supersession /
    failure), so it can never hang; the consolidated ``df`` is assembled from whatever
    settled successfully, in statement order.
    """
    multi = len(specs) > 1
    if make_pending_fn is None:
        make_pending_fn = _default_make_pending
    results: Dict[int, Any] = {}
    lock = threading.Lock()
    result_specs = [s for s in specs if s.kind == "result"]
    pending = [len(result_specs)]
    # barrier_done flips True (under `lock`) the moment the barrier binds the real
    # consolidated frames, so the early consolidated-list bind below -- which runs on the
    # main thread AFTER the spawn loop and races the barrier for tiny/empty results that
    # settle in microseconds -- becomes a no-op instead of overwriting real frames with
    # proxies (last-writer-wins). Whichever of the two runs second, under the shared lock,
    # loses.
    barrier_done = [False]

    # DML results are available synchronously (display + record + per-index bind).
    for spec in specs:
        if spec.kind == "dml":
            display_fn(spec.rowcount)
            with lock:
                results[spec.index] = spec.rowcount
            if multi:
                assign_namespace_fn(f"{base_name}_{spec.index}", spec.rowcount)

    # No result-bearing statements (DML-only cell): nothing to stream. Bind the
    # consolidated variable now -- mirroring the sync namespace semantics -- and return.
    if not result_specs:
        if specs:
            ordered = [results[i] for i in sorted(results)]
            assign_namespace_fn(base_name, ordered if multi else ordered[0])
        return []

    def _make_on_settle(index: int) -> "Callable[[Any], None]":
        def _on_settle(df: Any) -> None:
            # Runs once per result statement on ANY terminal outcome (success / cancel /
            # supersession / failure) so the multi-statement barrier never hangs.
            ordered = None
            with lock:
                if df is not None:  # None => this run was cancelled/superseded/failed
                    results[index] = df
                pending[0] -= 1
                if pending[0] == 0 and multi:
                    # Span the full statement index range, inserting None for any result
                    # statement that failed/was superseded, so df[i] stays aligned with
                    # statement i and with the df_i bindings (a gap must not left-shift).
                    ordered = [results.get(i) for i in range(len(specs))]
                    # Claim the consolidated bind under the lock and assign it here (still
                    # holding the lock) so the early consolidated-list bind, which checks
                    # barrier_done under the same lock, cannot overwrite these real frames
                    # afterwards. Assigning under the lock is cheap (a namespace dict set).
                    barrier_done[0] = True
                    assign_namespace_fn(base_name, ordered)

        return _on_settle

    # Open every reader FIRST (each fetches its statement's first page). If any reader
    # open raises (e.g. a GetQueryResults/GetStatementResult error), no background thread
    # has been spawned yet -> the barrier is never left half-armed and nothing is
    # partially materialized; the error propagates cleanly.
    prepared = []
    for spec in result_specs:
        # Validate before arming the barrier: an empty execution_id would make
        # materialize_async -> build_result_prefix raise, and if that happened mid
        # spawn-loop (after earlier threads spawned) the barrier would never reach 0.
        if not spec.execution_id:
            raise RuntimeError(
                "Async materialization: missing execution_id for a result-bearing statement"
            )
        var_name = f"{base_name}_{spec.index}" if multi else base_name
        # reader_factory returns (columns, first_page, remaining, total_rows) and may
        # additionally return a 5th element: a best-effort stats_fn (Athena exact-total
        # fetcher). Accept both shapes so callers/tests that return the 4-tuple keep working.
        _reader_out = reader_factory(spec.execution_id)
        stats_fn = None
        if len(_reader_out) == 5:
            columns, first_page_rows, remaining_rows, total_rows, stats_fn = _reader_out
        else:
            columns, first_page_rows, remaining_rows, total_rows = _reader_out
        prepared.append(
            (spec, var_name, columns, first_page_rows, remaining_rows, total_rows, stats_fn)
        )

    payloads: List[Dict[str, Any]] = []
    proxy_by_index: Dict[int, Any] = {}
    for spec, var_name, columns, first_page_rows, remaining_rows, total_rows, stats_fn in prepared:
        try:
            payload = materialize_async(
                dataframe_name=var_name,
                columns=columns,
                first_page_rows=first_page_rows,
                remaining_rows=remaining_rows,
                execution_id=spec.execution_id or "",
                project_s3_root=project_s3_root,
                total_rows=total_rows,
                display_fn=display_fn,
                assign_namespace_fn=assign_namespace_fn,
                write_page_fn=write_page_fn,
                write_manifest_fn=write_manifest_fn,
                emit_ready_fn=emit_ready_fn,
                on_settle=_make_on_settle(spec.index),
                # Bind a PendingDataFrame proxy for EVERY per-statement name -- df_0,
                # df_1, ... for multi, or df for single. var_name is already the
                # per-index name for multi, so a downstream cell referencing df_0 while
                # it materializes blocks-then-resolves via the proxy (same as single).
                # A failure to spawn settles this generation's error (materialize_async's
                # #2 guard), so the per-index proxy fails fast instead of hanging.
                bind_pending_fn=bind_pending_fn,
                stats_fn=stats_fn,
                # Pre-spawn placeholder retain so a tiny result's daemon cannot reap
                # _result before the consolidated proxy below is built (multi only).
                extra_retain=(multi and bind_pending_fn is not None),
                registry=registry,
                rows_per_page=rows_per_page,
                redshift_query_id=getattr(spec, "redshift_query_id", None),
            )
            payloads.append(payload)
            # Collect the per-index proxy for the consolidated bind below, keyed by
            # the statement's own spec.index (no string-parsing of the name). Only when multi
            # and proxy-binding is active; the proxy shares this payload's (name, gen), i.e.
            # the SAME (var_name, gen) bind_pending_fn just bound to df_i.
            if multi and bind_pending_fn is not None:
                name, run_gen = payload["dataframe_name"], payload["gen"]
                # materialize_async took a pre-spawn placeholder retain (extra_retain=True),
                # so _result is guaranteed still present here even if the daemon already
                # committed+reaped. Build the consolidated proxy (which retains on its own),
                # then release the placeholder -- net one live consumer, held by the proxy.
                proxy_by_index[spec.index] = make_pending_fn(name, run_gen, registry)
                release = getattr(registry, "release_consumer", None)
                if release is not None:
                    release(name, run_gen)
        except Exception:
            # A spawn failed AFTER earlier specs armed the barrier. The first-page card was
            # already displayed (display_fn runs before the thread spawns), so emit a failed
            # dataframe_ready to resolve that orphaned card (consistent with the background
            # thread's own failure path), THEN settle this spec's barrier slot so the
            # consolidated df can still bind rather than hanging forever.
            logger.exception("Async materialization failed to start for statement %s", spec.index)
            if spec.execution_id:
                emit_ready_fn(spec.execution_id, READY_FAILED)
            _make_on_settle(spec.index)(None)
            if not multi:
                # Single-result cell: the success bind of ``base_name`` (``df``) happens
                # inside the (never-spawned) background thread, and the single-statement
                # on_settle above does NOT bind ``base_name`` (it only assigns the
                # consolidated list when ``multi``). Returning here would leave ``df``
                # silently unbound/stale with no error -- diverging from the sync path,
                # which raises on failure. Re-raise so the caller surfaces the failure.
                raise

    # Bind the CONSOLIDATED ``base_name`` (``df``) to a REAL list during the pending
    # window, so an early reference to the whole list is a live list-of-proxies instead of
    # NameError. Only when multi AND proxy-binding is active (bind_pending_fn).
    # The list is barrier-aligned: it spans the full statement index range with the
    # per-index PendingDataFrame proxy at each successfully spawned RESULT index, and
    # results.get(i) elsewhere -- the DML rowcount at a DML index, or None where a result
    # spec failed to spawn. This matches the shape the barrier (_on_settle) writes on
    # completion, so df[i] stays aligned with statement i whether read early (proxy) or
    # after settle (real frame). Each proxy shares the (name, gen) already bound to df_i,
    # so df[i] block-then-resolves; df itself is a genuine list (len/isinstance/iter work).
    #
    # RACE: for tiny/empty results the daemon threads can settle and fire the barrier BEFORE
    # this line runs. The barrier sets barrier_done and binds the real frames under `lock`;
    # we check barrier_done under the SAME lock and skip if it already ran, so we never
    # overwrite real frames with proxies (which would strand df as proxies forever and pin
    # the registry frames). If we win the race instead, the barrier's later under-lock
    # assign overwrites our proxy list with the real frames, as intended.
    if multi and bind_pending_fn is not None:
        with lock:
            if not barrier_done[0]:
                early_consolidated = [
                    proxy_by_index.get(i, results.get(i)) for i in range(len(specs))
                ]
                assign_namespace_fn(base_name, early_consolidated)

    return payloads


# --- Default IO seams (touch S3 / IPython / kernel; injected so the core is testable) ---


def _parse_s3_uri(uri: str) -> "tuple[str, str]":
    """Split an s3://bucket/key URI into (bucket, key)."""
    if not uri.startswith("s3://"):
        raise ValueError(f"Not an s3:// URI: {uri}")
    without_scheme = uri[len("s3://") :]
    bucket, _, key = without_scheme.partition("/")
    return bucket, key


def _default_write_page(s3_uri: str, df: Any) -> None:
    """Write one Parquet page to S3 (bytes via boto3), applying the same nested/dotted
    column handling as the inline first page + the kernel formatter for UI-decode parity."""
    bucket, key = _parse_s3_uri(s3_uri)
    _get_s3_client().put_object(Bucket=bucket, Key=key, Body=_df_to_parquet_bytes(df))


# Cached S3 client for manifest writes. The manifest is rewritten once per page, so a
# large result would otherwise construct a boto3 client (loading service models +
# resolving credentials) hundreds of times. boto3 clients are safe to reuse across
# threads; guard construction with a lock since writes run on background daemon threads.
_s3_client = None
_s3_client_lock = threading.Lock()


def _get_s3_client():
    global _s3_client
    if _s3_client is None:
        with _s3_client_lock:
            if _s3_client is None:
                import boto3

                _s3_client = boto3.client("s3")
    return _s3_client


def _default_write_manifest(s3_uri: str, body: str) -> None:
    """Overwrite the manifest object in S3 with the given JSON body."""
    bucket, key = _parse_s3_uri(s3_uri)
    _get_s3_client().put_object(Bucket=bucket, Key=key, Body=body.encode("utf-8"))


def _default_assign_namespace(name: str, df: Any) -> None:
    """Atomic single dict setitem into the IPython user namespace."""
    from IPython import get_ipython

    ip = get_ipython()
    if ip is not None:
        ip.user_ns[name] = df


def _default_bind_pending(name: str, gen: int, registry: "_MaterializationRegistry") -> None:
    """Bind a ``PendingDataFrame`` proxy into the IPython user namespace for the pending
    window. On completion the background thread's ``assign_namespace_fn`` rebinds the same
    name to the real DataFrame (swap, don't spoof)."""
    from IPython import get_ipython

    from sagemaker_studio.utils.pending_dataframe import PendingDataFrame

    ip = get_ipython()
    if ip is not None:
        ip.user_ns[name] = PendingDataFrame(name, gen, registry)


def _default_make_pending(name: str, gen: int, registry: "_MaterializationRegistry") -> Any:
    """Construct a ``PendingDataFrame`` proxy WITHOUT binding it into the namespace.

    Used by ``materialize_async_multi`` to build the consolidated ``df`` list out of the
    same (name, gen) proxies already bound to the per-index ``df_i`` names, so the whole
    list is a live list-of-proxies during the pending window."""
    from sagemaker_studio.utils.pending_dataframe import PendingDataFrame

    return PendingDataFrame(name, gen, registry)


def _default_display(df: Any) -> None:
    from IPython.display import display

    display(df)


def _default_emit_dataframe_ready(execution_id: str, status: str) -> None:
    """Emit the custom ``dataframe_ready`` IOPub message from the running kernel.

    Best-effort: the kernel server relays unknown IOPub msg_types transparently.
    """
    try:
        from IPython import get_ipython

        ip = get_ipython()
        kernel = getattr(ip, "kernel", None)
        if kernel is None:
            logger.debug("No kernel available to emit dataframe_ready")
            return
        kernel.session.send(
            kernel.iopub_socket,
            "dataframe_ready",
            content={"execution_id": execution_id, "status": status},
            parent=getattr(kernel, "_parent_header", None),
        )
    except Exception:
        logger.debug("Failed to emit dataframe_ready", exc_info=True)
