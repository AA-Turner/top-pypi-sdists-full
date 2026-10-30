"""Unit-level tests for the cancelled-query connection reset.

These cover the parts of the fix that the mechanism file
(``test_cancelled_query_connection_rollback.py``) and the regression file
(``..._preservation.py``) structurally cannot reach:

* the reset ladder's escalation steps -- a healthy connection never makes ``rollback()`` raise,
  so ``invalidate()`` and the both-fail ``False`` return need stubbed failures;
* ``connection_needs_reset`` over the full transaction-state cross product, including the
  boundary case (ACTIVE transaction on a VALID connection) that must stay ``False``;
* Layer 2 (``ConnectionCache.get``) in isolation, with the bug state CONSTRUCTED directly
  rather than produced by a cancellation, so the healing is tested independently of Layer 1;
* every interrupt position in a multi-statement cell recovering end to end.

The end-to-end guarantee -- a cancellation propagates unchanged AND the next statement succeeds
-- is asserted in ``test_cancelled_query_connection_rollback.py`` and is not duplicated here.
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
from sagemaker_studio.sql_engine.sql_executor import ExecutionStatus, SqlExecutor
from sagemaker_studio.utils import sqlutils
from sagemaker_studio.utils import sqlutils_async as _async_mod
from sagemaker_studio.utils._sql_cache import (
    ConnectionCache,
    ManagedConnection,
    connection_needs_reset,
    reset_connection_state,
)

_HARNESS_MODULE = "test_cancelled_query_connection_rollback"
_CACHE_LOGGER = "sagemaker_studio.utils._sql_cache"


def _load_harness():
    """Import ``test_cancelled_query_connection_rollback`` as a library, however this file was
    invoked.

    Same shim the preservation file uses: under pytest's prepend import mode the sibling module
    is importable by name, under plain ``unittest`` discovery it is not. Either way the
    Engine/DBAPI-proxy harness stays defined exactly once, in that module.
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
interrupt_through_executor = _harness.interrupt_through_executor
PENDING_ROLLBACK_MESSAGE = _harness.PENDING_ROLLBACK_MESSAGE


class FakeTransaction:
    """Stands in for a ``RootTransaction`` so a test can set ``is_active`` directly."""

    def __init__(self, is_active: bool = True):
        self.is_active = is_active


class StubConnection:
    """Connection stand-in with directly settable transaction/validity state.

    Lets a test construct the measured bug state (invalidated + attached active transaction)
    without needing a cancellation, and make either ladder step fail on demand.
    """

    def __init__(
        self,
        *,
        closed: bool = False,
        invalidated: bool = False,
        transaction: Optional[FakeTransaction] = None,
        rollback_error: Optional[BaseException] = None,
        invalidate_error: Optional[BaseException] = None,
        closed_error: Optional[BaseException] = None,
        get_transaction_error: Optional[BaseException] = None,
        invalidated_error: Optional[BaseException] = None,
    ):
        self._closed = closed
        self._invalidated = invalidated
        self._transaction = transaction
        self._rollback_error = rollback_error
        self._invalidate_error = invalidate_error
        self._closed_error = closed_error
        self._get_transaction_error = get_transaction_error
        self._invalidated_error = invalidated_error
        self.calls: List[str] = []

    @property
    def closed(self):
        if self._closed_error is not None:
            raise self._closed_error
        return self._closed

    @property
    def invalidated(self):
        if self._invalidated_error is not None:
            raise self._invalidated_error
        return self._invalidated

    def get_transaction(self):
        if self._get_transaction_error is not None:
            raise self._get_transaction_error
        return self._transaction

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
        self._transaction = None

    def close(self):
        self.calls.append("close")
        self._closed = True

    def execute(self, statement, parameters=None):
        raise AssertionError("StubConnection.execute should not be reached")


class StubEngine:
    """Engine stand-in recording ``dispose()``, for the eviction-teardown assertions."""

    def __init__(self):
        self.calls: List[str] = []

    def dispose(self):
        self.calls.append("dispose")


def bug_state_connection(**kwargs) -> StubConnection:
    """The measured cancellation state: invalidated, with an attached ACTIVE transaction."""
    return StubConnection(invalidated=True, transaction=FakeTransaction(is_active=True), **kwargs)


class ConnectionNeedsResetTest(unittest.TestCase):
    """``connection_needs_reset`` over the full transaction-state cross product."""

    def test_none_connection_needs_no_reset(self):
        self.assertFalse(connection_needs_reset(None))

    def test_closed_connection_is_left_to_the_eviction_path(self):
        connection = StubConnection(closed=True, transaction=FakeTransaction(is_active=False))
        self.assertFalse(connection_needs_reset(connection))
        self.assertEqual([], connection.calls)

    def test_no_transaction_needs_no_reset_valid_or_invalidated(self):
        """The non-transactional baseline (Athena, Redshift Data API): nothing attached."""
        for invalidated in (False, True):
            with self.subTest(invalidated=invalidated):
                self.assertFalse(
                    connection_needs_reset(
                        StubConnection(invalidated=invalidated, transaction=None)
                    )
                )

    def test_active_transaction_on_a_valid_connection_needs_no_reset(self):
        """The boundary case: identical to the bug state except ``invalidated`` is False."""
        connection = StubConnection(invalidated=False, transaction=FakeTransaction(is_active=True))
        self.assertFalse(connection_needs_reset(connection))
        self.assertEqual([], connection.calls)

    def test_active_transaction_on_an_invalidated_connection_needs_reset(self):
        """PRIMARY trigger -- the measured cancellation state. ``invalidated`` is checked
        BEFORE ``is_active``, which is what makes the predicate fire at all here."""
        self.assertTrue(connection_needs_reset(bug_state_connection()))

    def test_deactivated_transaction_needs_reset_valid_or_invalidated(self):
        """SECONDARY trigger -- un-executable, though not what a cancellation produces."""
        for invalidated in (False, True):
            with self.subTest(invalidated=invalidated):
                self.assertTrue(
                    connection_needs_reset(
                        StubConnection(
                            invalidated=invalidated, transaction=FakeTransaction(is_active=False)
                        )
                    )
                )

    def test_a_raising_accessor_is_logged_and_treated_as_no_reset_needed(self):
        """A driver surprise must never break a healthy hand-out.

        All three accessors the predicate touches are covered: ``closed``, ``get_transaction()``
        and ``invalidated``. The ``invalidated`` case only reaches the raise once a transaction
        is attached, which is why it is the only one given one.
        """
        for label, connection in (
            ("closed", StubConnection(closed_error=RuntimeError("driver says no"))),
            ("get_transaction", StubConnection(get_transaction_error=RuntimeError("driver"))),
            (
                "invalidated",
                StubConnection(
                    transaction=FakeTransaction(is_active=True),
                    invalidated_error=RuntimeError("driver says no"),
                ),
            ),
        ):
            with self.subTest(raising=label):
                with self.assertLogs(_CACHE_LOGGER, level="WARNING") as logs:
                    self.assertFalse(connection_needs_reset(connection))
                self.assertTrue(any("assuming no reset" in line for line in logs.output))

    def test_predicate_sees_the_real_bug_state_on_a_real_connection(self):
        """The same predicate against a genuinely cancelled SQLAlchemy connection."""
        engine, injector = build_interruptible_engine()
        self.addCleanup(engine.dispose)
        connection = engine.connect()
        self.addCleanup(connection.close)
        connection.execute(text("SELECT 1"))
        self.assertFalse(connection_needs_reset(connection))

        injector.arm(KeyboardInterrupt("simulated UI cancel"), match="SELECT 2")
        with self.assertRaises(KeyboardInterrupt):
            connection.execute(text("SELECT 2"))

        observed = transaction_state(connection)
        self.assertTrue(connection_needs_reset(connection), f"observed: {observed}")


class ResetConnectionStateLadderTest(unittest.TestCase):
    """The escalation ladder, including the steps a healthy connection cannot reach."""

    def test_none_connection_is_a_no_op(self):
        self.assertTrue(reset_connection_state(None))

    def test_rollback_succeeds_and_invalidate_is_never_reached(self):
        connection = bug_state_connection()

        self.assertTrue(reset_connection_state(connection))

        self.assertEqual(["rollback"], connection.calls)
        self.assertIsNone(connection.get_transaction())

    def test_rollback_failure_escalates_to_invalidate_and_is_logged(self):
        """Step 2: ``rollback()`` raises (broken socket), ``invalidate()`` succeeds."""
        connection = bug_state_connection(rollback_error=RuntimeError("socket is gone"))

        with self.assertLogs(_CACHE_LOGGER, level="WARNING") as logs:
            self.assertTrue(reset_connection_state(connection))

        self.assertEqual(["rollback", "invalidate"], connection.calls)
        self.assertTrue(any("escalating to invalidate" in line for line in logs.output))
        self.assertTrue(any("socket is gone" in line for line in logs.output))

    def test_both_steps_failing_returns_false_and_is_logged(self):
        """Step 3: nothing worked, so the caller is told to evict and rebuild."""
        connection = bug_state_connection(
            rollback_error=RuntimeError("socket is gone"),
            invalidate_error=RuntimeError("invalidate exploded"),
        )

        with self.assertLogs(_CACHE_LOGGER, level="WARNING") as logs:
            self.assertFalse(reset_connection_state(connection))

        self.assertEqual(["rollback", "invalidate"], connection.calls)
        self.assertTrue(any("connection is unusable" in line for line in logs.output))
        self.assertTrue(any("invalidate exploded" in line for line in logs.output))

    def test_the_ladder_never_raises_and_never_closes(self):
        """``close()`` would destroy a persisted session for a merely dirty connection."""
        for label, errors in (
            ("rollback raises", {"rollback_error": RuntimeError("x")}),
            (
                "both raise",
                {
                    "rollback_error": RuntimeError("x"),
                    "invalidate_error": RuntimeError("y"),
                },
            ),
        ):
            with self.subTest(case=label):
                connection = bug_state_connection(**errors)
                with self.assertLogs(_CACHE_LOGGER, level="WARNING"):
                    reset_connection_state(connection)  # must not raise
                self.assertNotIn("close", connection.calls)

    def test_a_connection_without_the_ladder_methods_is_tolerated(self):
        """A non-SQLAlchemy connection stand-in (no ``rollback``/``invalidate`` at all) must
        still not propagate anything -- the helper only ever reports usability."""

        class BareConnection:
            closed = False
            invalidated = False

            def get_transaction(self):
                return None

        with self.assertLogs(_CACHE_LOGGER, level="WARNING"):
            self.assertFalse(reset_connection_state(BareConnection()))


class ConnectionCacheHealOnAcquireTest(unittest.TestCase):
    """Layer 2 in isolation -- the bug state is CONSTRUCTED, not produced by a cancellation."""

    def _cache_with(self, connection):
        cache = ConnectionCache()
        engine = StubEngine()
        managed = ManagedConnection(
            engine=engine, connection=connection, id=str(uuid4()), cache_key="k"
        )
        cache.put("k", managed)
        return cache, managed, engine

    def test_primary_bug_state_is_reset_in_place_keeping_the_same_entry(self):
        """Session continuity: the entry is healed, not replaced, so ``id`` is unchanged."""
        connection = bug_state_connection()
        cache, managed, engine = self._cache_with(connection)

        with self.assertLogs(_CACHE_LOGGER, level="WARNING") as logs:
            handed_out = cache.get("k")

        self.assertIs(handed_out, managed)
        self.assertEqual(managed.id, handed_out.id)
        self.assertEqual(["rollback"], connection.calls)
        self.assertEqual([], engine.calls, "a recoverable connection must not be torn down")
        self.assertIn("k", cache)
        self.assertTrue(any("invalid transaction" in line for line in logs.output))
        self.assertTrue(any("k" in line for line in logs.output))

        # The check is lazy, not one-shot: the healed connection hands out clean next time.
        self.assertIs(cache.get("k"), managed)
        self.assertEqual(["rollback"], connection.calls)

    def test_secondary_deactivated_transaction_state_is_healed_too(self):
        connection = StubConnection(invalidated=False, transaction=FakeTransaction(is_active=False))
        cache, managed, engine = self._cache_with(connection)

        with self.assertLogs(_CACHE_LOGGER, level="WARNING"):
            handed_out = cache.get("k")

        self.assertIs(handed_out, managed)
        self.assertEqual(["rollback"], connection.calls)
        self.assertEqual([], engine.calls)

    def test_unrecoverable_connection_is_evicted_and_the_entry_removed(self):
        """Reset fails -> ``get()`` returns ``None`` so the caller builds a replacement."""
        connection = bug_state_connection(
            rollback_error=RuntimeError("socket is gone"),
            invalidate_error=RuntimeError("invalidate exploded"),
        )
        cache, _, engine = self._cache_with(connection)

        with self.assertLogs(_CACHE_LOGGER, level="WARNING") as logs:
            self.assertIsNone(cache.get("k"))

        self.assertNotIn("k", cache)
        self.assertEqual(0, len(cache))
        self.assertEqual(["rollback", "invalidate", "close"], connection.calls)
        self.assertEqual(["dispose"], engine.calls)
        self.assertTrue(any("Failed to reset cached connection k" in line for line in logs.output))

    def test_a_concurrent_put_during_the_reset_wins_the_compare_and_swap(self):
        """If ``put(key, fresh)`` lands while the reset runs outside the lock, this stale read
        must return ``None`` rather than hand back the entry it was holding."""
        cache = ConnectionCache()
        fresh = ManagedConnection(
            engine=StubEngine(),
            connection=StubConnection(transaction=None),
            id=str(uuid4()),
            cache_key="k",
        )

        class ReplacingConnection(StubConnection):
            def rollback(self):
                super().rollback()
                cache.put("k", fresh)  # simulates another thread racing us

        connection = ReplacingConnection(
            invalidated=True, transaction=FakeTransaction(is_active=True)
        )
        stale = ManagedConnection(
            engine=StubEngine(), connection=connection, id=str(uuid4()), cache_key="k"
        )
        cache.put("k", stale)

        with self.assertLogs(_CACHE_LOGGER, level="WARNING"):
            self.assertIsNone(cache.get("k"))

        self.assertIs(cache.get("k"), fresh, "the fresh entry must be left intact")

    def test_a_real_cancelled_connection_is_healed_on_acquire(self):
        """The same path against a real SQLAlchemy connection, Layer 1 bypassed by poisoning
        the connection directly rather than through ``SqlExecutor.execute``."""
        engine, injector = build_interruptible_engine()
        self.addCleanup(engine.dispose)
        connection = engine.connect()
        self.addCleanup(connection.close)
        connection.execute(text("SELECT 1"))
        injector.arm(KeyboardInterrupt("simulated UI cancel"), match="SELECT 2")
        with self.assertRaises(KeyboardInterrupt):
            connection.execute(text("SELECT 2"))

        cache = ConnectionCache()
        managed = ManagedConnection(
            engine=engine, connection=connection, id=str(uuid4()), cache_key="k"
        )
        cache.put("k", managed)

        with self.assertLogs(_CACHE_LOGGER, level="WARNING"):
            handed_out = cache.get("k")

        self.assertIsNotNone(handed_out)
        self.assertEqual(managed.id, handed_out.id)
        self.assertIsNone(handed_out.connection.get_transaction())
        self.assertEqual([(3,)], handed_out.connection.execute(text("SELECT 3")).fetchall())


class SqlExecutorBaseExceptionGuardTest(unittest.TestCase):
    """The Layer 1 guard itself, at the exception kinds it must tell apart.

    ``KeyboardInterrupt`` through the caller-managed branch -- the cancellation propagating
    unchanged and the next statement succeeding -- is asserted in
    ``test_cancelled_query_connection_rollback.py``; what is covered here is the rest of the
    guard's contract, which no other test reaches:

    * ``GeneratorExit`` -- also a ``BaseException``, so it lands in the same handler, but it
      arrives from ordinary early-stream teardown (``_result_stream.close()``) on a HEALTHY
      connection. The guard must propagate it and must NOT reset, which is exactly why the reset
      is gated on ``connection_needs_reset`` instead of being unconditional. It must still reset
      when the connection it closes over genuinely is poisoned.
    * the ``connection is None`` branch -- deliberately unguarded, so a cancellation there must
      make no reset call at all and leave the ``with engine.connect()`` teardown to do the work.
    """

    def setUp(self):
        self.executor = SqlExecutor()

    def _suspended_stream(self, engine, connection):
        """Drive the caller-managed branch to a yield, so the guard's frame is live."""
        stream = self.executor.execute(engine, "SELECT 1; SELECT 2", connection=connection)
        first = next(stream)
        self.assertEqual(ExecutionStatus.SUCCESS.value, first.status)
        return stream

    def test_generator_exit_on_a_healthy_connection_propagates_without_resetting(self):
        """The measured constraint on the fix: early-stream teardown must not roll back.

        ``_result_stream.close()`` throws ``GeneratorExit`` into this generator as part of
        ordinary teardown, on a connection that is open, valid and carrying an active
        transaction. An unconditional reset here would silently discard the persisted session's
        open transaction, which the pre-fix code does not do.
        """
        engine, _ = build_interruptible_engine()
        self.addCleanup(engine.dispose)
        connection = engine.connect()
        self.addCleanup(connection.close)

        stream = self._suspended_stream(engine, connection)
        transaction_before = connection.get_transaction()
        self.assertIsNotNone(transaction_before)
        self.assertFalse(connection_needs_reset(connection))

        with self.assertRaises(GeneratorExit):
            stream.throw(GeneratorExit("stream closed"))

        # Untouched: same transaction object, still active, still usable.
        observed = transaction_state(connection)
        self.assertIs(connection.get_transaction(), transaction_before, f"observed: {observed}")
        self.assertTrue(connection.get_transaction().is_active, f"observed: {observed}")
        self.assertFalse(connection.invalidated, f"observed: {observed}")
        self.assertEqual([(3,)], connection.execute(text("SELECT 3")).fetchall())

    def test_generator_exit_on_a_poisoned_connection_resets_and_propagates(self):
        """The other half: when the connection IS poisoned, the same handler must heal it.

        The poisoning happens outside the executor (directly on the connection, while the
        stream is suspended) so that what is under test is the handler's behaviour for
        ``GeneratorExit`` specifically, not the cancellation path.
        """
        engine, injector = build_interruptible_engine()
        self.addCleanup(engine.dispose)
        connection = engine.connect()
        self.addCleanup(connection.close)

        stream = self._suspended_stream(engine, connection)

        injector.arm(KeyboardInterrupt("simulated UI cancel"), match="SELECT 99")
        with self.assertRaises(KeyboardInterrupt):
            connection.execute(text("SELECT 99"))
        self.assertTrue(connection_needs_reset(connection))

        with self.assertRaises(GeneratorExit) as ctx:
            stream.throw(GeneratorExit("stream closed"))
        self.assertEqual("stream closed", str(ctx.exception))

        observed = transaction_state(connection)
        self.assertIsNone(connection.get_transaction(), f"observed: {observed}")
        self.assertEqual([(3,)], connection.execute(text("SELECT 3")).fetchall())

    def test_generator_close_is_a_clean_teardown_not_a_runtime_error(self):
        """The handler must only reset and re-raise -- never yield.

        A ``GeneratorExit`` handler that yielded would make ``close()`` raise
        ``RuntimeError: generator ignored GeneratorExit``, so this pins the finalisation rule
        on the path that actually runs it, with the reset firing.
        """
        engine, injector = build_interruptible_engine()
        self.addCleanup(engine.dispose)
        connection = engine.connect()
        self.addCleanup(connection.close)

        stream = self._suspended_stream(engine, connection)
        injector.arm(KeyboardInterrupt("simulated UI cancel"), match="SELECT 99")
        with self.assertRaises(KeyboardInterrupt):
            connection.execute(text("SELECT 99"))

        stream.close()  # must not raise

        self.assertIsNone(connection.get_transaction())

    def test_cancellation_on_the_auto_managed_branch_is_left_unguarded(self):
        """``connection is None``: the guard is not applied, and the ``with`` block closes it.

        The guard is deliberately scoped to the caller-managed branch. Here the connection the
        executor opened is torn down by ``with engine.connect()``, and the pool's
        reset-on-return clears the transaction, so adding a reset would be a behaviour change on
        the ``persist_session=False`` path.

        Asserted by patching the two helpers as ``sql_executor`` imports them, rather than by
        spying on the connection: SQLAlchemy calls ``Connection.invalidate()`` ITSELF when it
        classifies the escaping ``BaseException`` as a disconnect, on both branches and on
        pre-fix code too, so a call log on the connection cannot tell that apart from a reset
        the guard performed.
        """
        engine, injector = build_interruptible_engine()
        self.addCleanup(engine.dispose)

        opened = []
        real_connect = engine.connect

        def _connect(*args, **kwargs):
            connection = real_connect(*args, **kwargs)
            opened.append(connection)
            return connection

        engine.connect = _connect
        self.addCleanup(setattr, engine, "connect", real_connect)

        needs_reset = mock.Mock(return_value=True)
        reset = mock.Mock(return_value=True)
        injector.arm(KeyboardInterrupt("simulated UI cancel"), match="SELECT 1")
        with mock.patch.object(
            _executor_mod, "connection_needs_reset", needs_reset
        ), mock.patch.object(_executor_mod, "reset_connection_state", reset):
            with self.assertRaises(KeyboardInterrupt) as ctx:
                list(self.executor.execute(engine, "SELECT 1"))

        self.assertEqual("simulated UI cancel", str(ctx.exception))
        needs_reset.assert_not_called()
        reset.assert_not_called()
        self.assertEqual(1, len(opened))
        self.assertTrue(opened[0].closed, "the `with` block must close its own connection")

    def test_the_caller_managed_branch_does_apply_the_guard(self):
        """The contrast that makes the previous test meaningful: same patches, other branch."""
        engine, injector = build_interruptible_engine()
        self.addCleanup(engine.dispose)
        connection = engine.connect()
        self.addCleanup(connection.close)

        needs_reset = mock.Mock(return_value=True)
        reset = mock.Mock(return_value=True)
        injector.arm(KeyboardInterrupt("simulated UI cancel"), match="SELECT 1")
        with mock.patch.object(
            _executor_mod, "connection_needs_reset", needs_reset
        ), mock.patch.object(_executor_mod, "reset_connection_state", reset):
            with self.assertRaises(KeyboardInterrupt):
                list(self.executor.execute(engine, "SELECT 1", connection=connection))

        needs_reset.assert_called_once_with(connection)
        reset.assert_called_once_with(connection)

    def test_an_ordinary_statement_error_never_reaches_the_guard(self):
        """``execute_statements`` keeps its ``except Exception``, so an ordinary SQL error
        becomes an ERROR result and the ``BaseException`` handler is never entered."""
        engine, injector = build_interruptible_engine()
        self.addCleanup(engine.dispose)
        connection = engine.connect()
        self.addCleanup(connection.close)

        needs_reset = mock.Mock(return_value=True)
        reset = mock.Mock(return_value=True)
        injector.arm(sqlite3.OperationalError("boom"), match="SELECT 1")
        with mock.patch.object(
            _executor_mod, "connection_needs_reset", needs_reset
        ), mock.patch.object(_executor_mod, "reset_connection_state", reset):
            yielded = list(self.executor.execute(engine, "SELECT 1", connection=connection))

        self.assertEqual([ExecutionStatus.ERROR.value], [r.status for r in yielded])
        needs_reset.assert_not_called()
        reset.assert_not_called()


class AsyncMaterializationResetDelegationTest(unittest.TestCase):
    """``sqlutils._stream_with_async_materialization`` delegates to the shared reset helper.

    The preservation file pins this branch's observable call sequence (``["rollback"]``, or
    ``["rollback", "invalidate"]`` when the rollback raises) and that the original statement
    error is never masked. What that cannot see is WHICH code produced the sequence, which is
    the whole point of the refactor, so the delegation is asserted directly here.
    """

    def _drive(self, reset):
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

        connection = StubConnection(transaction=FakeTransaction(is_active=True))
        cached = SimpleNamespace(
            engine=SimpleNamespace(get_execution_options=lambda: {"connection_type": "ATHENA"}),
            connection=connection,
        )
        dz_connection = mock.Mock()
        dz_connection.type = "ATHENA"
        patches = dict(
            _is_spark_connection=mock.Mock(return_value=False),
            _resolve_connection=mock.Mock(return_value=dz_connection),
            _apply_athena_context=mock.Mock(),
            _get_or_create_connection=mock.Mock(return_value=cached),
            _ensure_sql_executor=mock.Mock(return_value=executor),
            _bind_succeeded_partials=mock.Mock(),
            _stream_and_capture_metadata=lambda stream, **kwargs: stream,
            reset_connection_state=reset,
        )
        with contextlib.ExitStack() as stack:
            for name, patched in patches.items():
                stack.enter_context(mock.patch.object(sqlutils, name, patched))
            with self.assertRaises(Exception) as ctx:
                sqlutils._stream_with_async_materialization("SELECT 1; SELECT 2", "df")
        return ctx.exception, connection

    def test_the_error_branch_calls_reset_connection_state_with_the_cached_connection(self):
        reset = mock.Mock(return_value=True)

        raised, connection = self._drive(reset)

        reset.assert_called_once_with(connection)
        self.assertEqual("statement blew up", str(raised))
        # Delegated, so the branch itself makes no ladder call of its own.
        self.assertEqual([], connection.calls)

    def test_a_failing_reset_still_does_not_mask_the_statement_error(self):
        """The helper reports failure by returning ``False`` rather than raising, and the
        branch must not react to it by replacing the error it is about to raise."""
        reset = mock.Mock(return_value=False)

        raised, _ = self._drive(reset)

        reset.assert_called_once()
        self.assertEqual("statement blew up", str(raised))


class InterruptPositionRecoveryTest(unittest.TestCase):
    """Every interrupt position in a 3-statement cell must recover.

    This class also carries the parameterization of the now-obsolete
    ``test_interrupt_position_within_a_multi_statement_cell`` characterization test -- same three
    positions, same partial-results assertion -- which is why that test was removed rather than
    kept alongside this one. What it measured on pre-fix code is recorded in the
    ``test_cancelled_query_connection_rollback`` module docstring.
    """

    def test_every_interrupt_position_propagates_and_leaves_the_connection_usable(self):
        """Position 0 included: autobegin attaches the root transaction before the DBAPI call,
        so interrupting the first statement poisons the connection just the same."""
        executor = SqlExecutor()
        query = "SELECT 1; SELECT 2; SELECT 3"
        for position, match in enumerate(["SELECT 1", "SELECT 2", "SELECT 3"]):
            with self.subTest(interrupt_at_statement=position):
                engine, injector = build_interruptible_engine()
                self.addCleanup(engine.dispose)
                connection = engine.connect()
                self.addCleanup(connection.close)

                raised, yielded = interrupt_through_executor(
                    executor, engine, connection, query, injector, match
                )

                # The cancellation still reaches the user, unchanged.
                self.assertIsInstance(raised, KeyboardInterrupt)
                self.assertEqual("simulated UI cancel", str(raised))
                # The statements that already ran keep their results.
                self.assertEqual(position, len(yielded))
                for result in yielded:
                    self.assertEqual(ExecutionStatus.SUCCESS.value, result.status)

                # The transaction state is clean ...
                observed = transaction_state(connection)
                self.assertIsNone(connection.get_transaction(), f"observed: {observed}")
                self.assertFalse(connection.closed, f"observed: {observed}")

                # ... and the next statement runs normally on the same connection.
                followup = list(executor.execute(engine, "SELECT 4", connection=connection))
                self.assertEqual(1, len(followup))
                self.assertEqual(
                    ExecutionStatus.SUCCESS.value,
                    followup[0].status,
                    f"next statement failed with: {followup[0].error}",
                )
                self.assertNotIn(PENDING_ROLLBACK_MESSAGE, str(followup[0].error))

    def test_the_original_cancellation_survives_a_failing_reset(self):
        """When both ladder steps fail, the caller must still see the ``KeyboardInterrupt`` --
        never the reset error."""

        class CancellingConnection(StubConnection):
            def execute(self, statement, parameters=None):
                raise KeyboardInterrupt("simulated UI cancel")

        connection = CancellingConnection(
            invalidated=True,
            transaction=FakeTransaction(is_active=True),
            rollback_error=RuntimeError("rollback failed"),
            invalidate_error=RuntimeError("invalidate failed"),
        )
        engine, _ = build_interruptible_engine()
        self.addCleanup(engine.dispose)

        with self.assertLogs(_CACHE_LOGGER, level="WARNING"):
            with self.assertRaises(KeyboardInterrupt) as ctx:
                list(SqlExecutor().execute(engine, "SELECT 1", connection=connection))

        self.assertEqual("simulated UI cancel", str(ctx.exception))
        self.assertEqual(["rollback", "invalidate"], connection.calls)


if __name__ == "__main__":
    unittest.main()
