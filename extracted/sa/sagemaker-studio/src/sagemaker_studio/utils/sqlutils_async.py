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
from dataclasses import dataclass
from typing import Any, Callable, Dict, Iterator, List, Optional

logger = logging.getLogger(__name__)

# Fixed page size. Constant per run; the manifest records it so older/cross-engine
# results stay readable if this ever changes.
ROWS_PER_PAGE = 10_000
MANIFEST_NAME = "_manifest.json"

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

    def to_json(self) -> str:
        return json.dumps(
            {
                "totalfiles": self.totalfiles,
                "rowPerPages": self.rowPerPages,
                "status": self.status,
                "row_count": self.row_count,
            }
        )


class _MaterializationRegistry:
    """Tracks in-flight background materializations, keyed by dataframe name.

    Provides a per-``var_name`` generation token so a stale/superseded thread never
    clobbers the namespace binding of a newer run, and a cooperative cancel flag.
    """

    def __init__(self) -> None:
        self._lock = threading.Lock()
        self._generation: Dict[str, int] = {}
        self._cancel: Dict[str, threading.Event] = {}
        # In-flight runs kept so the atexit hook can finalize them on graceful shutdown.
        self._inflight: "Dict[tuple, _InFlightRun]" = {}

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

    def commit(
        self,
        var_name: str,
        gen: int,
        action: "Callable[[], None]",
        inflight_key: "Optional[tuple]" = None,
    ) -> bool:
        """Atomically run ``action`` (the namespace write) iff ``gen`` is still current
        AND (when ``inflight_key`` is given) this run still owns its ``_inflight`` entry.

        Holding the lock across the generation check + ``action`` closes the TOCTOU
        window where a newer run could supersede between an ``is_current`` check and the
        assignment (clobbering the newer result). The ``inflight_key`` check makes the
        inflight entry the single terminal-ownership token: ``flush_inflight_on_exit``
        removes it under this same lock when it finalizes a run as failed at shutdown, so
        if flush already claimed this run, ``commit`` returns False and the daemon stands
        down (no COMPLETE manifest, no success emit) instead of racing a contradictory
        success against the flush's failed finalization. First to the lock wins; the loser
        emits nothing. Returns True if ``action`` ran (this run still owns the outcome).
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
) -> None:
    """Background body: stream fixed pages to S3, then write the full DataFrame
    into the namespace and emit dataframe_ready. Runs on a daemon thread."""
    from pandas import DataFrame

    manifest = Manifest(rowPerPages=rows_per_page)
    all_rows: List[Any] = []
    settled_df: Any = None  # full DataFrame if this run wins; None if cancelled/superseded/failed
    committed = (
        False  # True once the namespace bind succeeded -> post-commit errors are best-effort
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
                # Superseded mid-stream by a newer run of this var (a same-cell re-run;
                # KernelServer blocks all other cells while the var materializes). Write a
                # terminal manifest for S3 hygiene and stop; no dataframe_ready is emitted --
                # the re-run replaced this run's output, so there is no live card to resolve.
                _write_failed(manifest, prefix, write_manifest_fn)
                registry.clear_inflight(inflight_key)  # terminal: drop before the flush can see it
                return
            write_page_fn(page_key(prefix, page_index), DataFrame(page_rows, columns=columns))
            all_rows.extend(page_rows)
            page_index += 1
            manifest.totalfiles = page_index
            manifest.row_count = len(all_rows)
            write_manifest_fn(manifest_key(prefix), manifest.to_json())

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
    except Exception:
        logger.exception("Async materialization failed for execution %s", execution_id)
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

    def _first_page_parquet_b64(self) -> str:
        import base64

        from pandas import DataFrame

        df = DataFrame(self.first_page_rows, columns=self.columns)
        return base64.b64encode(_df_to_parquet_bytes(df)).decode("utf-8")

    def _repr_mimebundle_(self, include=None, exclude=None):
        return {
            ASYNC_SQL_MIMETYPE: {
                "execution_id": self.execution_id,
                "s3_path": self.s3_path,
                "total_rows": self.total_rows,
                "data": self._first_page_parquet_b64(),
            },
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
    registry: "_MaterializationRegistry" = _registry,
    rows_per_page: int = ROWS_PER_PAGE,
) -> Dict[str, Any]:
    """Display the inline first page and spawn the background materialization.

    Returns the sync-reply payload ``{execution_id, s3_path, total_rows}``. The full
    DataFrame is written to the kernel namespace and ``dataframe_ready`` is emitted
    later, from the background daemon thread.
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
        )
    )

    gen, cancel = registry.start(dataframe_name)

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
        ),
        name=f"async-materialize-{execution_id}",
        daemon=True,
    ).start()

    return {
        "execution_id": execution_id,
        "s3_path": prefix,
        "total_rows": total_rows,
    }


@dataclass
class AsyncResultMarker:
    """Returned by the per-statement async executor for a result-bearing statement.

    Carries only the engine execution_id — the rows are fetched later, by id, via a
    fresh client (so ``execute_statements`` stays the single iteration/error-handling
    path and no rows are fetched inside the statement loop).
    """

    execution_id: Optional[str] = None


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


def spec_from_result(exec_result: Any) -> "StatementSpec":
    """Classify a SqlExecutor ExecutionResult into a StatementSpec.

    A result-bearing statement's executor returns an AsyncResultMarker (carrying the
    execution_id); a DML statement returns an int rowcount.
    """
    payload = exec_result.result
    if isinstance(payload, AsyncResultMarker):
        return StatementSpec(
            index=exec_result.statement_index, kind="result", execution_id=payload.execution_id
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
    results: Dict[int, Any] = {}
    lock = threading.Lock()
    result_specs = [s for s in specs if s.kind == "result"]
    pending = [len(result_specs)]

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
            if ordered is not None:
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
        columns, first_page_rows, remaining_rows, total_rows = reader_factory(spec.execution_id)
        prepared.append((spec, var_name, columns, first_page_rows, remaining_rows, total_rows))

    payloads: List[Dict[str, Any]] = []
    for spec, var_name, columns, first_page_rows, remaining_rows, total_rows in prepared:
        try:
            payloads.append(
                materialize_async(
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
                    registry=registry,
                    rows_per_page=rows_per_page,
                )
            )
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
