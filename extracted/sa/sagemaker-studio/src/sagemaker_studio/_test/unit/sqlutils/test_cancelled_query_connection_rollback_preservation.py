"""Regression tests for the cancelled-query connection reset.

Every execution path that is NOT a cancellation must behave exactly as it did before the
connection-reset fix. The sharp form of that is asserted throughout: ``connection.rollback`` and
``connection.invalidate`` are **never** called, and the yielded ``ExecutionResult``s are identical
to what the pre-fix code yields.

That is checked by **deterministic exhaustive enumeration**, not by random sampling: the
non-cancellation input space is small enough to enumerate completely. :func:`non_buggy_runs`
returns all **80** inputs -- 20 success runs (statement count 1..5 x persistence x error strategy)
plus 60
ordinary-error runs (15 valid ``(statement_count, error_index)`` pairs x persistence x error
strategy) -- and each test loops over the whole list under ``subTest``, so a failure names its own
input and does not mask the remaining inputs. The cache hand-out tests enumerate their state
dicts the same way. :class:`EnumerationShapeTest` pins the 80 and the absence of duplicates so the
cross product cannot silently shrink.

Every assertion here was written **after** observing the behaviour on pre-fix code
(observation-first), and the observed values are recorded in the docstrings below. The file
records the baseline the fix must not disturb, so it passing unchanged after the fix is what
shows there is no regression.

The SQLite/DBAPI-proxy harness is reused from ``test_cancelled_query_connection_rollback`` rather
than rebuilt: a real SQLAlchemy ``Engine`` over in-memory SQLite with ``StaticPool``,
interruptible (and here, error-injectable) at the DBAPI layer.

OBSERVED BASELINE ON PRE-FIX CODE (SQLAlchemy 2.0.41, recorded verbatim)
-----------------------------------------------------------------------
``SqlExecutor.execute`` on a caller-managed (persisted) connection, 3 statements, all succeed::

    yielded            = 3 results, statement_index 0..2, statement "SELECT 1".."SELECT 3",
                         statement_type "SELECT", status "success", error None,
                         result a DataFrame, rows_affected None, execution_metadata None
    connection calls   = []          (no rollback, no invalidate, no close, no commit)
    closed/invalidated = False / False
    transaction        = RootTransaction, is_active True  (autobegun, left open for reuse)

Ordinary ``sqlite3.OperationalError`` raised from statement 1 of 3::

    STOP_ON_ERROR      = [success, error]            (2 results; iteration stops)
    CONTINUE_ON_ERROR  = [success, error, success]   (3 results)
    error text         = "(sqlite3.OperationalError) boom\\n[SQL: SELECT 2]..."
    connection calls   = []
    invalidated        = False   <-- an ordinary Exception is NOT a disconnect, so the
                                     ordinary-error path is structurally outside the bug

Persisted session state, three ``sqlutils.sql_stream`` calls on cache key ``conn-1``::

    CREATE TEMP TABLE tt (id INT) -> INSERT INTO tt VALUES (42) -> SELECT id FROM tt
    third call returns [{'id': 42}]          (temp table survived across calls)
    ManagedConnection.id unchanged across calls; cache length 1; connection calls []

``persist_session=False``::

    engine.connect() called once; that connection is closed after the stream is drained;
    connection calls []; _connection_cache length 0 (no cache entry)

``ConnectionCache.get`` hand-out, by connection state::

    no transaction on a valid connection          -> same entry, same id, no calls
    no transaction on an invalidated connection   -> same entry, same id, no calls
    ACTIVE transaction on a VALID connection      -> same entry, same id, no calls
    genuinely closed connection                   -> returns None, entry removed,
                                                     connection.close() then engine.dispose()

``sqlutils._stream_with_async_materialization`` statement-error branch::

    connection calls = ["rollback"]                      (rollback succeeds)
    rollback raises  -> ["rollback", "invalidate"]
    partials bound before raising; the ORIGINAL statement error propagates unmasked

Spark / IRC-Glue / DuckDB::

    results flow through SqlExecutor.execute_statements directly; SqlExecutor.execute is
    never called, so no SQLAlchemy Connection and no reset is reachable; cache length 0

THE BOUNDARY THAT MATTERS
-------------------------
``ACTIVE transaction on a VALID connection`` is the preservation case to get right: it differs
from the measured bug state (``active transaction on an INVALIDATED connection``) only by
``Connection.invalidated``. ``connection_needs_reset`` must return ``False`` for it, so ``get()``
must still make zero mutating calls on such a connection. That case is generated explicitly below.
"""

import contextlib
import importlib
import importlib.util
import sqlite3
import sys
import unittest
from pathlib import Path
from types import SimpleNamespace
from typing import List, Optional
from unittest import mock
from uuid import uuid4

from sqlalchemy import text

from sagemaker_studio.sql_engine import sql_executor as _executor_mod
from sagemaker_studio.sql_engine.duckdb_engine import engine as duckdb_engine
from sagemaker_studio.sql_engine.sql_executor import (
    ErrorStrategy,
    ExecutionStatus,
    SqlExecutor,
)
from sagemaker_studio.utils import duckdbutils, sqlutils
from sagemaker_studio.utils import sqlutils_async as _async_mod
from sagemaker_studio.utils._sql_cache import ConnectionCache, ManagedConnection

_HARNESS_MODULE = "test_cancelled_query_connection_rollback"


def _load_harness():
    """Import ``test_cancelled_query_connection_rollback`` as a library, however this file was
    invoked.

    Under pytest's default (prepend) import mode the sibling test module is importable by
    name; under plain ``unittest`` discovery it is not, so fall back to loading it by path.
    Either way the engine/DBAPI-proxy harness stays defined exactly once, in that module.
    """
    if _HARNESS_MODULE in sys.modules:
        return sys.modules[_HARNESS_MODULE]
    try:
        return importlib.import_module(_HARNESS_MODULE)
    except ImportError:
        path = Path(__file__).with_name(_HARNESS_MODULE + ".py")
        spec = importlib.util.spec_from_file_location(_HARNESS_MODULE, path)
        module = importlib.util.module_from_spec(spec)
        sys.modules[_HARNESS_MODULE] = module
        spec.loader.exec_module(module)
        return module


_harness = _load_harness()

build_interruptible_engine = _harness.build_interruptible_engine
transaction_state = _harness.transaction_state
NonTransactionalConnection = _harness.NonTransactionalConnection
TRANSACTIONAL_CONNECTION_TYPE = _harness.TRANSACTIONAL_CONNECTION_TYPE

# Mutating lifecycle calls. These are the ones the fix could add and the ones that must stay
# unmade on a non-cancellation input.
MUTATING_CALLS = ("rollback", "invalidate", "close", "commit")


def unpolluted_error_strategy(test_case):
    """Re-point ``sql_executor.ErrorStrategy`` at the class every other module holds.

    Pre-existing suite coupling, not a product issue, but it lands squarely on these tests.
    ``_test/unit/sql_engine/test_sql_executor.py`` calls ``importlib.reload()`` on
    ``sagemaker_studio.sql_engine.sql_executor`` to exercise its module-level teradata-import
    guard. A reload re-executes the module body in place, so ``ErrorStrategy`` is rebound to a
    BRAND NEW ``Enum`` class while every module that did ``from ... import ErrorStrategy`` at
    its own import time -- including ``sqlutils``, whose ``sql_stream`` default argument is
    already bound -- keeps a member of the OLD class. Enum members compare by identity, so
    ``execute_statements``' ``error_strategy == ErrorStrategy.STOP_ON_ERROR`` silently becomes
    ``False`` and STOP_ON_ERROR stops honouring itself. ``ExecutionStatus`` is unaffected
    because it is always compared through ``.value``.

    These tests are the only ones in the suite that drive ``error_strategy`` end to end after
    that reload, so they are the only ones that see it; in isolation they pass. Restoring the
    one reference for the duration of the test keeps the assertions themselves untouched and
    makes the result independent of collection order.
    """
    patcher = mock.patch.object(_executor_mod, "ErrorStrategy", ErrorStrategy)
    patcher.start()
    test_case.addCleanup(patcher.stop)


class ResetSpyConnection:
    """Attribute-forwarding proxy over a real SQLAlchemy ``Connection`` that records the
    mutating lifecycle calls a reset would make.

    Only ``rollback``/``invalidate``/``close``/``commit`` are recorded; plain attribute reads
    (``closed``, ``invalidated``, ``get_transaction``) are forwarded untouched, because the fix
    is expected to *inspect* a connection on hand-out and pinning inspections would pin the
    implementation rather than the behaviour.
    """

    def __init__(self, connection):
        object.__setattr__(self, "_connection", connection)
        object.__setattr__(self, "calls", [])

    def __getattr__(self, name):
        target = getattr(object.__getattribute__(self, "_connection"), name)
        if name not in MUTATING_CALLS:
            return target
        calls = object.__getattribute__(self, "calls")

        def _recording(*args, **kwargs):
            calls.append(name)
            return target(*args, **kwargs)

        return _recording

    def __setattr__(self, name, value):
        setattr(object.__getattribute__(self, "_connection"), name, value)

    # `with engine.connect() as conn:` looks these up on the type, so they cannot be proxied
    # through __getattr__.
    def __enter__(self):
        object.__getattribute__(self, "_connection").__enter__()
        return self

    def __exit__(self, *exc_info):
        return object.__getattribute__(self, "_connection").__exit__(*exc_info)


@contextlib.contextmanager
def spy_connections(engine):
    """Wrap every ``engine.connect()`` result in a :class:`ResetSpyConnection`.

    Yields the list of proxies handed out, so a test can assert on the call log of a connection
    it never sees directly (the auto-managed branch's own connection, or the one the cache
    opens).
    """
    opened: List[ResetSpyConnection] = []
    real_connect = engine.connect

    def _connect(*args, **kwargs):
        proxy = ResetSpyConnection(real_connect(*args, **kwargs))
        opened.append(proxy)
        return proxy

    engine.connect = _connect
    try:
        yield opened
    finally:
        engine.connect = real_connect


class FakeTransaction:
    """Stands in for a ``RootTransaction`` so a test can set ``is_active`` directly."""

    def __init__(self, is_active=True):
        self.is_active = is_active


class RecordingConnection:
    """Connection stand-in for the cache-level properties.

    ``ConnectionCache.get`` only reads ``closed`` today, and the fix adds reads of
    ``get_transaction()``/``invalidated``; this stub lets a test pin the exact state those see
    while recording mutating calls separately from inspections.
    """

    def __init__(
        self,
        *,
        closed: bool = False,
        invalidated: bool = False,
        transaction: Optional[FakeTransaction] = None,
        rollback_error: Optional[BaseException] = None,
        invalidate_error: Optional[BaseException] = None,
    ):
        self._closed = closed
        self._invalidated = invalidated
        self._transaction = transaction
        self._rollback_error = rollback_error
        self._invalidate_error = invalidate_error
        self.calls: List[str] = []
        self.reads: List[str] = []

    @property
    def closed(self):
        self.reads.append("closed")
        return self._closed

    @property
    def invalidated(self):
        self.reads.append("invalidated")
        return self._invalidated

    def get_transaction(self):
        self.reads.append("get_transaction")
        return self._transaction

    def in_transaction(self):
        self.reads.append("in_transaction")
        return self._transaction is not None

    def rollback(self):
        self.calls.append("rollback")
        if self._rollback_error is not None:
            raise self._rollback_error
        self._transaction = None

    def invalidate(self):
        self.calls.append("invalidate")
        if self._invalidate_error is not None:
            raise self._invalidate_error
        self._invalidated = True

    def close(self):
        self.calls.append("close")
        self._closed = True

    def commit(self):
        self.calls.append("commit")


class RecordingEngine:
    """Engine stand-in that records ``dispose()``, for the eviction-teardown baseline."""

    def __init__(self):
        self.calls: List[str] = []

    def dispose(self):
        self.calls.append("dispose")

    def get_execution_options(self):
        return {"connection_type": TRANSACTIONAL_CONNECTION_TYPE}


# ConnectionCache.get hand-out states where the bug condition does NOT hold. These must be
# preserved exactly: no mutating call, same entry handed back.
PRESERVED_CACHE_STATES = {
    "no_transaction_on_valid_connection": lambda: RecordingConnection(
        invalidated=False, transaction=None
    ),
    "no_transaction_on_invalidated_connection": lambda: RecordingConnection(
        invalidated=True, transaction=None
    ),
    # The boundary case: identical to the measured bug state except `invalidated` is False.
    "active_transaction_on_valid_connection": lambda: RecordingConnection(
        invalidated=False, transaction=FakeTransaction(is_active=True)
    ),
}

# States that ARE the reset's remit (the measured bug state and the secondary deactivated state).
# Recorded here for completeness of the cross product, but only invariants that hold both before
# and after the fix are asserted on them; their post-fix hand-out behaviour is asserted in
# `test_cancelled_query_connection_rollback_fix.py`.
FIX_TARGET_CACHE_STATES = {
    "active_transaction_on_invalidated_connection": lambda: RecordingConnection(
        invalidated=True, transaction=FakeTransaction(is_active=True)
    ),
    "deactivated_transaction_on_valid_connection": lambda: RecordingConnection(
        invalidated=False, transaction=FakeTransaction(is_active=False)
    ),
    "deactivated_transaction_on_invalidated_connection": lambda: RecordingConnection(
        invalidated=True, transaction=FakeTransaction(is_active=False)
    ),
}


def multi_statement_query(statement_count: int) -> str:
    """``"SELECT 1; SELECT 2; ..."`` -- each statement's text is its own unique match token."""
    return "; ".join(f"SELECT {i + 1}" for i in range(statement_count))


def expected_statuses(statement_count, error_index, error_strategy):
    """The statuses pre-fix code yields, as observed: STOP_ON_ERROR truncates at the error,
    CONTINUE_ON_ERROR keeps going and marks only the failing statement."""
    success = ExecutionStatus.SUCCESS.value
    error = ExecutionStatus.ERROR.value
    if error_index is None:
        return [success] * statement_count
    if error_strategy == ErrorStrategy.STOP_ON_ERROR:
        return [success] * error_index + [error]
    return [error if i == error_index else success for i in range(statement_count)]


# The enumerated axes of the non-buggy input space.
STATEMENT_COUNTS = (1, 2, 3, 4, 5)
PERSIST_SESSION_CHOICES = (True, False)
ERROR_STRATEGIES = (ErrorStrategy.STOP_ON_ERROR, ErrorStrategy.CONTINUE_ON_ERROR)

# Size of the complete cross product returned by `non_buggy_runs()`, pinned by
# `EnumerationShapeTest` so a later edit cannot shrink the space unnoticed.
#   success        : 5 counts            x 2 persistence x 2 strategies = 20
#   ordinary_error : 15 (count, index)   x 2 persistence x 2 strategies = 60
NON_BUGGY_RUN_COUNT = 80


def non_buggy_runs() -> List[SimpleNamespace]:
    """The COMPLETE non-buggy input cross product: outcome x statement count x error index x
    persistence x error strategy -- enumerated exhaustively, in a fixed order.

    ``cancelled_mid_statement`` never appears -- that is what keeps every enumerated input
    outside the cancellation case. ``error_index`` only ever ranges over the statement range, so
    the injected ordinary error always lands on a real statement; that is what makes the
    ordinary-error half 15 ``(statement_count, error_index)`` pairs rather than 25.

    Returns all :data:`NON_BUGGY_RUN_COUNT` (80) inputs, each a ``SimpleNamespace`` with the
    fields ``statement_count``, ``outcome``, ``error_index``, ``persist_session`` and
    ``error_strategy``.
    """
    runs: List[SimpleNamespace] = []
    for statement_count in STATEMENT_COUNTS:
        # `None` is the success outcome; 0..n-1 are the ordinary-error positions.
        for error_index in (None, *range(statement_count)):
            for persist_session in PERSIST_SESSION_CHOICES:
                for error_strategy in ERROR_STRATEGIES:
                    runs.append(
                        SimpleNamespace(
                            statement_count=statement_count,
                            outcome="success" if error_index is None else "ordinary_error",
                            error_index=error_index,
                            persist_session=persist_session,
                            error_strategy=error_strategy,
                        )
                    )
    return runs


def _run_key(run: SimpleNamespace):
    """Hashable identity of an enumerated input, for the duplicate check."""
    return (
        run.statement_count,
        run.outcome,
        run.error_index,
        run.persist_session,
        run.error_strategy,
    )


class EnumerationShapeTest(unittest.TestCase):
    """Guards the enumeration itself, so the cross product cannot silently shrink.

    With random generation a shrunken space still produced green runs; with a fixed enumeration
    the size IS the coverage, so it is asserted directly.
    """

    def test_enumeration_is_the_complete_cross_product_without_duplicates(self):
        runs = non_buggy_runs()

        self.assertEqual(NON_BUGGY_RUN_COUNT, len(runs))
        keys = [_run_key(run) for run in runs]
        self.assertEqual(len(keys), len(set(keys)), "enumerated inputs must be distinct")

        successes = [run for run in runs if run.error_index is None]
        errors = [run for run in runs if run.error_index is not None]
        self.assertEqual(20, len(successes))
        self.assertEqual(60, len(errors))

        # Every axis value is actually exercised, and every error index is in range.
        self.assertEqual(set(STATEMENT_COUNTS), {run.statement_count for run in runs})
        self.assertEqual(set(PERSIST_SESSION_CHOICES), {run.persist_session for run in runs})
        self.assertEqual(set(ERROR_STRATEGIES), {run.error_strategy for run in runs})
        self.assertEqual({"success", "ordinary_error"}, {run.outcome for run in runs})
        for run in errors:
            self.assertIn(run.error_index, range(run.statement_count), f"input: {run}")


class PreservedExecutorRunTest(unittest.TestCase):
    """Preservation over ``SqlExecutor.execute``: unchanged results, and no reset ever performed.

    Enumerated exhaustively over outcome (success / ordinary error) x error index x persistence
    (caller-managed vs auto-managed connection) x statement count x error strategy -- all 80
    inputs from :func:`non_buggy_runs`. For every one of those inputs the observed baseline is:
    the expected ``ExecutionResult``s, an EMPTY mutating-call log on the connection, and
    ``invalidated is False``.
    """

    def setUp(self):
        unpolluted_error_strategy(self)

    def _assert_results(self, run, yielded):
        statuses = expected_statuses(run.statement_count, run.error_index, run.error_strategy)
        self.assertEqual(statuses, [r.status for r in yielded], f"input: {run}")
        for position, result in enumerate(yielded):
            self.assertEqual(position, result.statement_index)
            self.assertEqual(f"SELECT {position + 1}", result.statement)
            self.assertEqual("SELECT", result.statement_type)
            self.assertIsNone(result.rows_affected)
            if result.status == ExecutionStatus.SUCCESS.value:
                self.assertIsNone(result.error)
                self.assertEqual(position + 1, result.result.iloc[0, 0])
            else:
                self.assertIn("sqlite3.OperationalError", result.error)
                self.assertIsNone(result.result)

    def test_non_buggy_run_yields_recorded_results_and_never_resets(self):
        """Sharp form: identical results, and zero rollback/invalidate calls.

        Driven over every one of the 80 enumerated non-cancellation inputs, each under its own
        ``subTest`` so a failure names its input and the rest still run. A fresh real ``Engine``
        over in-memory SQLite is built inside the loop body rather than in ``setUp`` so each
        input gets its own connection pool and an unarmed error injector.
        """
        for run in non_buggy_runs():
            with self.subTest(run=run):
                engine, injector = build_interruptible_engine()
                try:
                    if run.error_index is not None:
                        injector.arm(
                            sqlite3.OperationalError("boom"),
                            match=f"SELECT {run.error_index + 1}",
                        )
                    query = multi_statement_query(run.statement_count)
                    executor = SqlExecutor()

                    with spy_connections(engine) as opened:
                        if run.persist_session:
                            # Caller-managed branch: the cache owns the connection's lifecycle.
                            connection = engine.connect()
                            yielded = list(
                                executor.execute(
                                    engine,
                                    query,
                                    connection=connection,
                                    error_strategy=run.error_strategy,
                                )
                            )
                        else:
                            # Auto-managed branch: `with engine.connect()` inside the executor.
                            connection = None
                            yielded = list(
                                executor.execute(engine, query, error_strategy=run.error_strategy)
                            )

                        self._assert_results(run, yielded)

                        for proxy in opened:
                            self.assertEqual(
                                [],
                                proxy.calls,
                                f"no reset may happen on a non-buggy input; input: {run}",
                            )

                        if run.persist_session:
                            observed = transaction_state(connection)
                            self.assertFalse(connection.closed, f"observed: {observed}")
                            self.assertFalse(connection.invalidated, f"observed: {observed}")
                            # Still usable for the next cell, with no intervening reset.
                            self.assertEqual(
                                [(9,)], connection.execute(text("SELECT 9")).fetchall()
                            )
                            connection.close()
                        else:
                            self.assertEqual(1, len(opened), f"input: {run}")
                            self.assertTrue(
                                opened[0].closed,
                                "the auto-managed branch must close its own connection",
                            )
                finally:
                    engine.dispose()

    def test_ordinary_error_leaves_the_connection_valid_and_reusable(self):
        """An ordinary statement error must leave the connection valid and reusable.

        Observed: after an ordinary ``Exception`` from a statement, ``invalidated is False`` --
        only a ``BaseException`` escape is classified as a disconnect -- the transaction is
        still attached and active, and the next statement succeeds. This is why the
        ordinary-error path is structurally outside the bug condition.
        """
        engine, injector = build_interruptible_engine()
        self.addCleanup(engine.dispose)
        connection = ResetSpyConnection(engine.connect())
        self.addCleanup(connection.close)
        executor = SqlExecutor()

        injector.arm(sqlite3.OperationalError("boom"), match="SELECT 2")
        yielded = list(
            executor.execute(
                engine,
                "SELECT 1; SELECT 2; SELECT 3",
                connection=connection,
                error_strategy=ErrorStrategy.CONTINUE_ON_ERROR,
            )
        )

        self.assertEqual(
            [
                ExecutionStatus.SUCCESS.value,
                ExecutionStatus.ERROR.value,
                ExecutionStatus.SUCCESS.value,
            ],
            [r.status for r in yielded],
        )
        self.assertIn("(sqlite3.OperationalError) boom", yielded[1].error)

        observed = transaction_state(connection)
        self.assertEqual([], connection.calls, f"observed: {observed}")
        self.assertFalse(connection.invalidated, f"observed: {observed}")
        self.assertFalse(connection.closed, f"observed: {observed}")
        self.assertIsNotNone(connection.get_transaction(), f"observed: {observed}")
        self.assertTrue(connection.get_transaction().is_active, f"observed: {observed}")
        self.assertEqual([(4,)], connection.execute(text("SELECT 4")).fetchall())

    def test_non_transactional_connection_is_never_reset_by_the_executor(self):
        """The Athena / Redshift Data API baseline: a connection that never holds a transaction
        is never reset.

        ``NonTransactionalConnection`` has no ``rollback`` or ``invalidate`` attribute at all,
        so a reset reaching this path would raise ``AttributeError`` rather than quietly pass.
        Observed: the statement succeeds and ``get_transaction()`` stays ``None``.
        """
        engine, _ = build_interruptible_engine()
        self.addCleanup(engine.dispose)
        connection = NonTransactionalConnection(engine)

        yielded = list(SqlExecutor().execute(engine, "SELECT 1", connection=connection))

        self.assertEqual([ExecutionStatus.SUCCESS.value], [r.status for r in yielded])
        self.assertIsNone(connection.get_transaction())
        self.assertFalse(connection.closed)
        self.assertFalse(hasattr(connection, "rollback"))
        self.assertFalse(hasattr(connection, "invalidate"))


class PreservedSessionLifecycleTest(unittest.TestCase):
    """Preservation over ``sqlutils.sql_stream``: session state and connection lifecycle."""

    def setUp(self):
        unpolluted_error_strategy(self)
        self.engine, self.injector = build_interruptible_engine()
        self.addCleanup(self.engine.dispose)

        self._previous_executor = sqlutils._sql_executor
        sqlutils._sql_executor = SqlExecutor()
        sqlutils._connection_cache.clear()
        self.addCleanup(sqlutils._connection_cache.clear)
        self.addCleanup(setattr, sqlutils, "_sql_executor", self._previous_executor)

        patches = [
            mock.patch.object(
                sqlutils,
                "_resolve_connection",
                return_value=SimpleNamespace(type=TRANSACTIONAL_CONNECTION_TYPE),
            ),
            mock.patch.object(sqlutils, "_get_engine_from_connection", return_value=self.engine),
            # Athena-only context sniffing; irrelevant here and it would hit sql_handler.
            mock.patch.object(sqlutils, "_apply_athena_context", return_value=None),
        ]
        for patch in patches:
            patch.start()
            self.addCleanup(patch.stop)

    def test_persisted_session_state_survives_across_calls_with_no_reset(self):
        """Temp tables and other session state must survive across calls on a persisted
        connection.

        Observed: the temp table created by call 1 is visible in call 3 on the same cached
        connection, ``ManagedConnection.id`` is unchanged, the cache holds one entry, and the
        connection's mutating-call log is empty throughout.
        """
        with spy_connections(self.engine) as opened:
            created = list(sqlutils.sql_stream("CREATE TEMP TABLE tt (id INT)", connection_id="c1"))
            first_id = sqlutils._connection_cache.get("c1").id

            inserted = list(sqlutils.sql_stream("INSERT INTO tt VALUES (42)", connection_id="c1"))
            selected = list(sqlutils.sql_stream("SELECT id FROM tt", connection_id="c1"))
            second_id = sqlutils._connection_cache.get("c1").id

        self.assertEqual([ExecutionStatus.SUCCESS.value], [r.status for r in created])
        self.assertEqual([ExecutionStatus.SUCCESS.value], [r.status for r in inserted])
        self.assertEqual([ExecutionStatus.SUCCESS.value], [r.status for r in selected])
        self.assertEqual([{"id": 42}], selected[0].result.to_dict("records"))

        # A healthy get() hands back the same ManagedConnection, so the session is continuous.
        self.assertEqual(first_id, second_id)
        self.assertEqual(1, len(sqlutils._connection_cache))
        self.assertEqual(1, len(opened), "the persisted session must open exactly one connection")
        self.assertEqual([], opened[0].calls)
        self.assertFalse(opened[0].closed)

    def test_persist_session_false_opens_and_closes_its_own_connection(self):
        """``persist_session=False`` must own its connection's whole lifecycle.

        Observed: one ``engine.connect()``, closed when the stream is drained, no mutating
        calls, and no cache entry at all.
        """
        with spy_connections(self.engine) as opened:
            results = list(
                sqlutils.sql_stream("SELECT 1; SELECT 2", connection_id="c1", persist_session=False)
            )

        self.assertEqual(
            [ExecutionStatus.SUCCESS.value, ExecutionStatus.SUCCESS.value],
            [r.status for r in results],
        )
        self.assertEqual(1, len(opened))
        self.assertTrue(opened[0].closed, "the auto-managed connection must be closed on exit")
        self.assertEqual([], opened[0].calls)
        self.assertEqual(0, len(sqlutils._connection_cache))
        self.assertEqual([], sqlutils._connection_cache.list_keys())

    def test_sql_stream_results_and_cache_shape_are_preserved(self):
        """The same complete 80-input cross product driven end-to-end through ``sql_stream``.

        Observed: the yielded statuses match the executor-level baseline exactly, and the cache
        holds one entry for ``persist_session=True`` and none for ``persist_session=False`` --
        with no mutating call on any connection either way.

        The engine here comes from ``setUp`` (one per enumerated run would also re-patch
        ``sqlutils``), so each input clears the cache itself before driving the stream.
        """
        for run in non_buggy_runs():
            with self.subTest(run=run):
                sqlutils._connection_cache.clear()
                if run.error_index is not None:
                    self.injector.arm(
                        sqlite3.OperationalError("boom"), match=f"SELECT {run.error_index + 1}"
                    )

                with spy_connections(self.engine) as opened:
                    results = list(
                        sqlutils.sql_stream(
                            multi_statement_query(run.statement_count),
                            connection_id="c1",
                            error_strategy=run.error_strategy,
                            persist_session=run.persist_session,
                        )
                    )

                self.assertEqual(
                    expected_statuses(run.statement_count, run.error_index, run.error_strategy),
                    [r.status for r in results],
                    f"input: {run}",
                )
                self.assertEqual(1 if run.persist_session else 0, len(sqlutils._connection_cache))
                for proxy in opened:
                    self.assertEqual([], proxy.calls, f"input: {run}")


class PreservedCacheHandOutTest(unittest.TestCase):
    """Preservation over ``ConnectionCache.get``: healthy hand-out, and eviction when closed."""

    def test_healthy_hand_out_makes_no_calls_on_the_connection(self):
        """Observed for every state outside the bug condition -- no transaction (on a valid or
        an invalidated connection) and an ACTIVE transaction on a VALID connection: ``get()``
        returns the same ``ManagedConnection``, keeps the same ``id``, advances ``last_used``,
        and makes ZERO mutating calls on the connection.

        All three preserved states are enumerated, each under its own ``subTest``.

        The active-on-valid case is the boundary: it differs from the measured bug state only
        by ``Connection.invalidated``, so a predicate that crossed it would be caught here.
        """
        for state_name, build_connection in sorted(PRESERVED_CACHE_STATES.items()):
            with self.subTest(state=state_name):
                connection = build_connection()
                engine = RecordingEngine()
                cache = ConnectionCache()
                managed = ManagedConnection(
                    engine=engine, connection=connection, id=str(uuid4()), cache_key="k"
                )
                cache.put("k", managed)
                created_at_handout = managed.last_used

                handed_out = cache.get("k")

                self.assertIs(handed_out, managed, f"state: {state_name}")
                self.assertEqual(managed.id, handed_out.id, f"state: {state_name}")
                self.assertEqual([], connection.calls, f"state: {state_name}")
                self.assertEqual([], engine.calls, f"state: {state_name}")
                self.assertIn("k", cache)
                self.assertEqual(1, len(cache))
                self.assertGreaterEqual(handed_out.last_used, created_at_handout)
                # A second hand-out behaves identically (the check is lazy, not one-shot).
                self.assertIs(cache.get("k"), managed)
                self.assertEqual([], connection.calls, f"state: {state_name}")

    def test_closed_connection_is_evicted_and_torn_down(self):
        """A genuinely closed connection still belongs to the eviction path, not the reset path.

        Observed: ``get()`` returns ``None``, the entry is removed, and teardown runs as
        ``connection.close()`` then ``engine.dispose()``.
        """
        connection = RecordingConnection(closed=True)
        engine = RecordingEngine()
        cache = ConnectionCache()
        managed = ManagedConnection(
            engine=engine, connection=connection, id=str(uuid4()), cache_key="k"
        )
        cache.put("k", managed)

        self.assertIsNone(cache.get("k"))
        self.assertNotIn("k", cache)
        self.assertEqual(0, len(cache))
        self.assertEqual(["close"], connection.calls)
        self.assertEqual(["dispose"], engine.calls)

    def test_closed_real_connection_is_evicted(self):
        """The same eviction baseline against a real SQLAlchemy connection, not a stub."""
        engine, _ = build_interruptible_engine()
        connection = engine.connect()
        connection.close()
        cache = ConnectionCache()
        managed = ManagedConnection(
            engine=engine, connection=connection, id=str(uuid4()), cache_key="k"
        )
        cache.put("k", managed)

        self.assertIsNone(cache.get("k"))
        self.assertNotIn("k", cache)

    def test_healthy_real_connection_hand_out_keeps_the_same_managed_connection(self):
        """Same property against a real connection carrying a real ACTIVE transaction on a
        VALID connection -- the boundary state, built for real rather than stubbed.

        Observed: ``get_transaction()`` is a live ``RootTransaction`` with ``is_active True``,
        ``invalidated`` is ``False``, and ``get()`` hands back the same entry with no calls.
        """
        engine, _ = build_interruptible_engine()
        self.addCleanup(engine.dispose)
        connection = ResetSpyConnection(engine.connect())
        self.addCleanup(connection.close)
        connection.execute(text("SELECT 1"))  # autobegins the root transaction

        cache = ConnectionCache()
        managed = ManagedConnection(
            engine=engine, connection=connection, id=str(uuid4()), cache_key="k"
        )
        cache.put("k", managed)

        handed_out = cache.get("k")

        observed = transaction_state(connection)
        self.assertIsNotNone(connection.get_transaction(), f"observed: {observed}")
        self.assertTrue(connection.get_transaction().is_active, f"observed: {observed}")
        self.assertFalse(connection.invalidated, f"observed: {observed}")
        self.assertIsNotNone(handed_out)
        self.assertEqual(managed.id, handed_out.id)
        self.assertEqual([], connection.calls, f"observed: {observed}")
        self.assertEqual([(2,)], handed_out.connection.execute(text("SELECT 2")).fetchall())

    def test_fix_target_states_are_recorded_not_pinned(self):
        """The other half of the transaction-state cross product, recorded for completeness.

        These three states ARE the reset's remit (``active_transaction_on_invalidated_connection``
        is the measured cancellation state; the deactivated ones are the predicate's secondary
        trigger), so their hand-out behaviour deliberately CHANGES and must not be pinned here:
        ``test_cancelled_query_connection_rollback_fix.py`` asserts the post-fix behaviour.

        All three states are enumerated, each under its own ``subTest``.

        Observed on pre-fix code: ``get()`` returns the very same ``ManagedConnection`` with no
        calls made on it, because the ``closed``-only health check cannot see either state. Only
        the invariants that survive the fix are asserted: ``get()`` does not raise, the
        connection is not closed, and an entry remains reachable under the key.
        """
        for state_name, build_connection in sorted(FIX_TARGET_CACHE_STATES.items()):
            with self.subTest(state=state_name):
                connection = build_connection()
                cache = ConnectionCache()
                managed = ManagedConnection(
                    engine=RecordingEngine(), connection=connection, id=str(uuid4()), cache_key="k"
                )
                cache.put("k", managed)

                handed_out = cache.get("k")

                self.assertIsNotNone(handed_out, f"state: {state_name}")
                self.assertNotIn("close", connection.calls, f"state: {state_name}")
                self.assertFalse(connection._closed, f"state: {state_name}")


class PreservedAsyncOnErrorResetTest(unittest.TestCase):
    """Preservation over ``sqlutils._stream_with_async_materialization``.

    This statement-error branch ran a rollback/invalidate ladder inline before the fix and now
    delegates to ``reset_connection_state``; the observable call sequence and the unmasked
    original error are exactly what must survive that change.
    """

    def _drive(self, connection, rollback_error=None):
        executor = mock.Mock()
        executor._get_transformer.return_value = mock.Mock()
        good = SimpleNamespace(
            status=ExecutionStatus.SUCCESS.value,
            statement_index=0,
            result=_async_mod.AsyncResultMarker(execution_id="e0"),
        )
        bad = SimpleNamespace(
            status=ExecutionStatus.ERROR.value, statement_index=1, error="statement blew up"
        )
        executor.execute.return_value = iter([good, bad])

        dz_connection = mock.Mock()
        dz_connection.type = "ATHENA"
        cached = SimpleNamespace(
            engine=SimpleNamespace(get_execution_options=lambda: {"connection_type": "ATHENA"}),
            connection=connection,
        )
        bind = mock.Mock()
        patches = dict(
            _is_spark_connection=mock.Mock(return_value=False),
            _resolve_connection=mock.Mock(return_value=dz_connection),
            _apply_athena_context=mock.Mock(),
            _get_or_create_connection=mock.Mock(return_value=cached),
            _ensure_sql_executor=mock.Mock(return_value=executor),
            _bind_succeeded_partials=bind,
            _stream_and_capture_metadata=lambda stream, **kwargs: stream,
        )
        with contextlib.ExitStack() as stack:
            for name, patched in patches.items():
                stack.enter_context(mock.patch.object(sqlutils, name, patched))
            with self.assertRaises(Exception) as ctx:
                sqlutils._stream_with_async_materialization("SELECT 1; SELECT 2", "df")
        return ctx.exception, bind

    def test_statement_error_runs_the_rollback_ladder_and_raises_unmasked(self):
        """Observed: call log ``["rollback"]`` (rollback succeeds, so invalidate is never
        reached), the already-succeeded partials are bound before raising, and the ORIGINAL
        statement error propagates.
        """
        connection = RecordingConnection(transaction=FakeTransaction(is_active=True))

        raised, bind = self._drive(connection)

        self.assertEqual("statement blew up", str(raised))
        self.assertEqual(["rollback"], connection.calls)
        bind.assert_called_once()
        self.assertEqual("df", bind.call_args[0][1])
        self.assertEqual([0], [spec.index for spec in bind.call_args[0][0]])

    def test_rollback_failure_escalates_to_invalidate_without_masking_the_error(self):
        """Observed: call log ``["rollback", "invalidate"]`` when rollback raises, and the
        original statement error still propagates -- the reset error never replaces it.
        """
        connection = RecordingConnection(
            transaction=FakeTransaction(is_active=True),
            rollback_error=RuntimeError("rollback failed"),
        )

        raised, bind = self._drive(connection)

        self.assertEqual("statement blew up", str(raised))
        self.assertNotIn("rollback failed", str(raised))
        self.assertEqual(["rollback", "invalidate"], connection.calls)
        bind.assert_called_once()


class PreservedNonSqlAlchemyPathsTest(unittest.TestCase):
    """Preservation over the Spark / IRC-Glue / DuckDB paths.

    These paths call ``SqlExecutor.execute_statements`` directly, with no ``Connection`` in
    play, so neither layer of the fix is reachable from them. The assertion that pins this is
    that ``SqlExecutor.execute`` -- where the ``BaseException`` guard lives -- is never called,
    and that no connection is cached.
    """

    def setUp(self):
        unpolluted_error_strategy(self)
        sqlutils._connection_cache.clear()
        self.addCleanup(sqlutils._connection_cache.clear)
        patcher = mock.patch.object(
            SqlExecutor, "execute", side_effect=AssertionError("SqlExecutor.execute reached")
        )
        self.execute = patcher.start()
        self.addCleanup(patcher.stop)

    def _assert_no_sqlalchemy_connection(self):
        self.execute.assert_not_called()
        self.assertEqual(0, len(sqlutils._connection_cache))

    def test_spark_path_runs_execute_statements_directly(self):
        """Observed: two SUCCESS results carrying the Spark DataFrames, schema forced per
        statement, no cache entry, and ``SqlExecutor.execute`` never called.
        """
        calls = []

        class FakeDataFrame:
            @property
            def schema(self):
                calls.append("schema")
                return "schema"

        class FakeSpark:
            def sql(self, statement):
                calls.append(statement)
                return FakeDataFrame()

        with mock.patch.object(sqlutils, "_ensure_spark", return_value=FakeSpark()):
            results = list(sqlutils.sql_stream("SELECT 1; SELECT 2", connection={"type": "spark"}))

        self.assertEqual(
            [ExecutionStatus.SUCCESS.value, ExecutionStatus.SUCCESS.value],
            [r.status for r in results],
        )
        self.assertEqual(["SELECT 1", "SELECT 2"], [r.statement for r in results])
        self.assertEqual(["SELECT 1", "schema", "SELECT 2", "schema"], calls)
        self._assert_no_sqlalchemy_connection()

    def test_spark_path_error_is_reported_without_any_reset(self):
        """Observed: a failing Spark statement yields an ERROR result and STOP_ON_ERROR
        truncates, exactly as on the SQL path -- still with no Connection in play.
        """

        class FailingSpark:
            def sql(self, statement):
                if "SELECT 2" in statement:
                    raise Exception("TABLE_OR_VIEW_NOT_FOUND")
                return SimpleNamespace(schema="schema")

        with mock.patch.object(sqlutils, "_ensure_spark", return_value=FailingSpark()):
            results = list(
                sqlutils.sql_stream("SELECT 1; SELECT 2; SELECT 3", connection={"type": "spark"})
            )

        self.assertEqual(
            [ExecutionStatus.SUCCESS.value, ExecutionStatus.ERROR.value],
            [r.status for r in results],
        )
        self.assertIn("TABLE_OR_VIEW_NOT_FOUND", results[1].error)
        self._assert_no_sqlalchemy_connection()

    def test_irc_glue_path_runs_execute_statements_directly(self):
        """Observed: each statement is routed through ``_execute_irc_connection_query`` (Glue
        Spark), never through a SQLAlchemy connection, and nothing is cached.
        """
        irc_type = next(iter(sqlutils.SUPPORTED_IRC_GLUE_CONNECTION_TYPES))
        with mock.patch.object(
            sqlutils, "_resolve_connection", return_value=SimpleNamespace(type=irc_type)
        ), mock.patch.object(
            sqlutils,
            "_execute_irc_connection_query",
            side_effect=lambda statement, resolved: f"df({statement})",
        ):
            results = list(sqlutils.sql_stream("SELECT 1; SELECT 2", connection_id="c1"))

        self.assertEqual(
            [ExecutionStatus.SUCCESS.value, ExecutionStatus.SUCCESS.value],
            [r.status for r in results],
        )
        self.assertEqual(["df(SELECT 1)", "df(SELECT 2)"], [r.result for r in results])
        self._assert_no_sqlalchemy_connection()

    def test_duckdb_path_runs_execute_statements_directly(self):
        """Observed: with no resolvable connection the local DuckDB path runs the statements
        and no SQLAlchemy connection is created or cached.
        """
        duck = object()  # the cell's engine, handed to every statement of the stream
        with mock.patch.object(
            sqlutils, "_resolve_connection", return_value=None
        ), mock.patch.object(duckdb_engine, "_ensure_duckdb", return_value=duck), mock.patch.object(
            duckdbutils,
            "_run_duckdb_statement",
            side_effect=lambda duck, statement: f"duckdf({statement})",
        ) as run, mock.patch.object(
            sqlutils, "_get_or_create_connection"
        ) as native:
            results = list(sqlutils.sql_stream("SELECT 1; SELECT 2"))

        self.assertEqual(
            [ExecutionStatus.SUCCESS.value, ExecutionStatus.SUCCESS.value],
            [r.status for r in results],
        )
        self.assertEqual(["duckdf(SELECT 1)", "duckdf(SELECT 2)"], [r.result for r in results])
        self.assertEqual(
            [(duck, "SELECT 1"), (duck, "SELECT 2")],
            [call.args for call in run.call_args_list],
        )
        native.assert_not_called()
        self._assert_no_sqlalchemy_connection()


if __name__ == "__main__":
    unittest.main()
