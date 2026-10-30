"""Cancellation mechanism and end-to-end behaviour of the cancelled-query connection reset.

``CancellationMechanismCharacterizationTest`` records what SQLAlchemy actually does to a
connection when a statement is cancelled mid-execution -- it measures below both layers of the
fix, so the fix does not move it. ``CancelledQueryExpectedBehaviorTest`` and
``CancelledQueryExpectedBehaviorEndToEndTest`` assert the behaviour the fix guarantees: the
cancellation reaches the caller unchanged, the connection's transaction state is clean
afterwards, and the next statement runs normally on the same connection.

No real database is used. A real SQLAlchemy ``Engine`` runs over in-memory SQLite, and the
cancellation is injected at the DBAPI layer: ``cursor.execute`` raises ``KeyboardInterrupt`` on
demand, so the exception escapes from inside ``Connection.execute`` with the same stack shape a
SIGINT-driven cancel produces in the kernel.

OBSERVED TRANSACTION STATE (SQLAlchemy 2.0.41, recorded verbatim)
----------------------------------------------------------------
After a ``KeyboardInterrupt`` escapes ``cursor.execute`` on a connection that already had an
autobegun root transaction::

    get_transaction()  = <sqlalchemy.engine.base.RootTransaction object at 0x10991ddb0>
                         (the SAME object as before the interrupt -- not None, not replaced)
    is_active          = True
    closed             = False
    invalidated        = True
    in_transaction()   = True
    next execute()     -> PendingRollbackError:
                          "Can't reconnect until invalid transaction is rolled back.
                           Please rollback() fully before proceeding"  (code 8s2b)

The transaction is NOT deactivated: it is still **active**, and the *connection* is what got
invalidated. ``Connection._handle_dbapi_exception`` classifies any non-``Exception`` escape as an
exit exception, sets ``_is_disconnect``, and calls ``Connection.invalidate()``, which drops
``_dbapi_connection`` while leaving the active ``RootTransaction`` attached. The next execute hits
``_revalidate_connection()``, which refuses to reconnect while ``_transaction is not None`` ->
``PendingRollbackError``. ``closed`` stays ``False`` (it is ``_dbapi_connection is None and not
_can_reconnect``), which is why the cache's ``closed``-only health check hands the poisoned
connection straight back out.

CONSEQUENCE FOR THE DETECTION PREDICATE: a predicate of the form "a root transaction exists AND is
not active" returns ``False`` for the state above, so it would never fire on a cancellation.
``connection_needs_reset`` must key off ``Connection.invalidated`` together with an attached
transaction (``get_transaction() is not None``), and keep the deactivated-transaction case only as
an additional, not the primary, trigger. That ordering is the load-bearing consequence of the
measurement above, so the measurement is kept in this module even where the tests that produced it
have been retargeted or removed (see below).

OBSOLETE CHARACTERIZATION TESTS AND WHERE THEIR FACTS LIVE NOW
--------------------------------------------------------------
Three of the eight original characterization tests pinned the pre-fix SYMPTOM at a layer the fix
deliberately changes, which makes them obsolete as written: they would now have to assert both
that the connection is poisoned and that it is not. Their measurements are recorded here so
nothing observed on pre-fix code is lost, and each one's facts are accounted for:

1. ``test_interrupt_through_sql_executor_escapes_and_poisons_the_connection`` -- **removed as a
   duplicate.** Measured on pre-fix code: driving ``SqlExecutor.execute``'s caller-managed branch
   with an armed DBAPI interrupt let the ``KeyboardInterrupt`` escape unchanged, yielded ZERO
   ``ExecutionResult``s (``execute_statements`` only catches ``Exception``, so the interrupt was
   never converted into an ERROR result), and left ``invalidated True`` / ``closed False`` with an
   attached transaction, so the next statement raised ``PendingRollbackError``. Every fact in it
   except the final poisoning is now asserted post-fix by
   ``CancelledQueryExpectedBehaviorTest.test_cancellation_leaves_the_connection_reusable`` (same
   drive, same escape-unchanged assertion, then a clean transaction and a working next statement),
   and the "no ERROR result is yielded" fact by
   ``InterruptPositionRecoveryTest.test_every_interrupt_position_propagates_and_leaves_the_connection_usable``
   in ``..._fix.py``, whose position-0 case asserts an empty yield list.

2. ``test_interrupt_position_within_a_multi_statement_cell`` -- **removed as a duplicate.**
   Measured on pre-fix code: interrupting position 0, 1 or 2 of a 3-statement cell poisoned the
   connection identically (position 0 included, because autobegin attaches the root transaction
   before the DBAPI call is issued), while the statements before the interrupt kept their SUCCESS
   results. ``InterruptPositionRecoveryTest.test_every_interrupt_position_propagates_and_leaves_the_connection_usable``
   in ``..._fix.py`` is the same parameterization over the same three positions, keeps the
   partial-results assertion verbatim, and asserts the post-fix outcome. The autobegin fact that
   made position 0 a real bug case is recorded in that test's docstring.

3. ``test_sql_stream_second_call_fails_after_the_first_is_cancelled`` -- **retargeted, not
   removed** (see ``CancelledQueryEndToEndCharacterizationTest`` below). It carries one fact no
   other test does: end to end through ``sqlutils.sql_stream``, the cancelled connection is still
   the SAME cached ``Connection`` object afterwards. Pre-fix that was the bug's propagation
   mechanism; post-fix it is what keeps the persisted session continuous (the connection is
   healed in place, never evicted), so the assertion is still true, still valuable, and now
   carries the opposite verdict.

The raw-mechanism test (``test_mechanism_...``) is untouched and still passes: it measures
SQLAlchemy at the ``connection.execute()`` level, below both layers of the fix, so the fix does
not change it. It remains the executable record of the state table above.
"""

import gc
import sqlite3
import unittest
from types import SimpleNamespace
from unittest.mock import patch
from uuid import uuid4

from sqlalchemy import create_engine, text
from sqlalchemy.engine import Engine
from sqlalchemy.exc import PendingRollbackError
from sqlalchemy.pool import StaticPool

from sagemaker_studio.sql_engine.sql_executor import ExecutionStatus, SqlExecutor
from sagemaker_studio.utils import sqlutils
from sagemaker_studio.utils._sql_cache import ConnectionCache, ManagedConnection

# Substring of the SQLAlchemy 2.0 PendingRollbackError message (see sqlalche.me/e/20/8s2b).
PENDING_ROLLBACK_MESSAGE = "Can't reconnect until invalid transaction is rolled back"

# SQLite stands in for a transactional engine (Redshift/PostgreSQL). The executor resolves a
# transformer from the engine's connection_type execution option, so the SQLite engine is tagged
# as POSTGRESQL: that only selects statement splitting + metadata extraction, both of which are
# dialect-neutral for the statements used here.
TRANSACTIONAL_CONNECTION_TYPE = "POSTGRESQL"


class InterruptInjector:
    """Arms a one-shot exception to be raised from ``cursor.execute`` at the DBAPI layer."""

    def __init__(self):
        self.pending = None
        self.match = None
        self.executed = []
        self.injected = []

    def arm(self, exception=None, match=None):
        """Raise ``exception`` from the next ``cursor.execute`` whose SQL contains ``match``."""
        self.pending = exception if exception is not None else KeyboardInterrupt("simulated cancel")
        self.match = match

    def check(self, operation):
        if self.pending is not None and (self.match is None or self.match in operation):
            exception = self.pending
            self.pending = None
            self.injected.append(operation)
            raise exception
        self.executed.append(operation)


class _DbapiProxy:
    """Attribute-forwarding proxy over a DBAPI object.

    ``__setattr__`` forwards too, so dialect-driven writes (e.g. ``isolation_level``) land on the
    real sqlite3 object instead of being shadowed on the proxy.
    """

    __slots__ = ("_wrapped", "_control")

    def __init__(self, wrapped, control):
        object.__setattr__(self, "_wrapped", wrapped)
        object.__setattr__(self, "_control", control)

    def __getattr__(self, name):
        return getattr(object.__getattribute__(self, "_wrapped"), name)

    def __setattr__(self, name, value):
        setattr(object.__getattribute__(self, "_wrapped"), name, value)


class _InterruptingCursor(_DbapiProxy):
    __slots__ = ()

    def execute(self, operation, *args, **kwargs):
        self._control.check(operation)
        return self._wrapped.execute(operation, *args, **kwargs)

    def executemany(self, operation, *args, **kwargs):
        self._control.check(operation)
        return self._wrapped.executemany(operation, *args, **kwargs)


class _InterruptingDbapiConnection(_DbapiProxy):
    __slots__ = ()

    def cursor(self, *args, **kwargs):
        return _InterruptingCursor(self._wrapped.cursor(*args, **kwargs), self._control)


def build_interruptible_engine(connection_type=TRANSACTIONAL_CONNECTION_TYPE):
    """Return ``(engine, injector)``: a real Engine over in-memory SQLite, interruptible at DBAPI.

    ``StaticPool`` keeps one DBAPI connection so the in-memory database is stable across
    checkouts, matching a persisted kernel session.
    """
    injector = InterruptInjector()

    def _creator():
        return _InterruptingDbapiConnection(sqlite3.connect(":memory:"), injector)

    engine = create_engine("sqlite://", creator=_creator, poolclass=StaticPool)
    return engine.execution_options(connection_type=connection_type), injector


def transaction_state(connection):
    """Snapshot of the public transaction/liveness state, for assertions and failure messages."""
    try:
        transaction = connection.get_transaction()
    except BaseException as exc:  # pragma: no cover - defensive, drivers may surprise us
        return {"get_transaction_raised": f"{type(exc).__name__}: {exc}"}
    return {
        "get_transaction()": repr(transaction),
        "transaction_is_none": transaction is None,
        "is_active": getattr(transaction, "is_active", "<no transaction>"),
        "closed": connection.closed,
        "invalidated": connection.invalidated,
        "in_transaction()": connection.in_transaction(),
    }


class _NonTransactionalResult:
    """Minimal DBAPI-ish result for the non-transactional control engine."""

    returns_rows = False
    rowcount = 0
    cursor = None


class NonTransactionalConnection:
    """Stands in for Athena / the Redshift Data API: no transaction is ever held.

    ``get_transaction()`` returns ``None`` and an interrupt leaves nothing to roll back, so a
    later statement must keep working. This is the baseline the fix must not move.
    """

    def __init__(self, engine: Engine):
        self.engine = engine
        self.closed = False
        self.executed = []
        self._pending_interrupt = None

    def arm(self, exception=None):
        self._pending_interrupt = (
            exception if exception is not None else KeyboardInterrupt("simulated cancel")
        )

    def get_transaction(self):
        return None

    def in_transaction(self):
        return False

    def execute(self, statement, parameters=None):
        if self._pending_interrupt is not None:
            exception = self._pending_interrupt
            self._pending_interrupt = None
            raise exception
        self.executed.append(str(statement))
        return _NonTransactionalResult()


def interrupt_through_executor(executor, engine, connection, query, injector, match):
    """Run ``query`` through ``SqlExecutor.execute`` with an armed DBAPI interrupt.

    Returns ``(raised, yielded)``: the exception that escaped (or ``None``) and the results the
    generator yielded before it did.
    """
    injector.arm(KeyboardInterrupt("simulated UI cancel"), match=match)
    yielded = []
    raised = None
    try:
        for result in executor.execute(engine, query, connection=connection):
            yielded.append(result)
    except BaseException as exc:  # noqa: BLE001 - the point is to catch the BaseException
        raised = exc
    return raised, yielded


class CancellationMechanismCharacterizationTest(unittest.TestCase):
    """What state a cancellation actually leaves behind, measured below both layers of the fix."""

    def setUp(self):
        self.engine, self.injector = build_interruptible_engine()
        self.executor = SqlExecutor()
        self.addCleanup(self.engine.dispose)

    def _warm_connection(self):
        """Open a connection and run one statement so a root transaction is autobegun."""
        connection = self.engine.connect()
        self.addCleanup(connection.close)
        connection.execute(text("SELECT 1"))
        self.assertIsNotNone(
            connection.get_transaction(),
            "precondition: a root transaction should be autobegun by the first execute",
        )
        return connection

    def test_mechanism_interrupt_leaves_invalidated_connection_with_active_transaction(self):
        """Mechanism characterization. Observed state, recorded verbatim:

            get_transaction()  = <sqlalchemy.engine.base.RootTransaction object at 0x10991ddb0>
                                 (identical object to the pre-interrupt transaction)
            is_active          = True
            closed             = False
            invalidated        = True
            in_transaction()   = True
            next execute()     -> PendingRollbackError
                                  "Can't reconnect until invalid transaction is rolled back.
                                   Please rollback() fully before proceeding"

        The transaction is not deactivated (``is_active`` stays ``True``): it is still active
        and the *connection* is what got invalidated.
        """
        connection = self._warm_connection()
        transaction_before = connection.get_transaction()

        self.injector.arm(KeyboardInterrupt("simulated UI cancel"), match="SELECT 2")
        with self.assertRaises(KeyboardInterrupt):
            connection.execute(text("SELECT 2"))

        observed = transaction_state(connection)
        transaction_after = connection.get_transaction()

        # The root transaction is still attached, and it is the SAME object.
        self.assertIsNotNone(transaction_after, f"observed state: {observed}")
        self.assertIs(transaction_after, transaction_before, f"observed state: {observed}")
        # ... and it is still ACTIVE, which is why `is_active` alone cannot detect this state.
        self.assertTrue(
            transaction_after.is_active,
            f"the root transaction is still active after the interrupt; observed: {observed}",
        )
        # The connection, not the transaction, is what carries the damage.
        self.assertTrue(connection.invalidated, f"observed state: {observed}")
        self.assertFalse(connection.closed, f"observed state: {observed}")
        self.assertTrue(connection.in_transaction(), f"observed state: {observed}")

        # Symptom from the ticket: the next statement cannot run.
        with self.assertRaises(PendingRollbackError) as ctx:
            connection.execute(text("SELECT 3"))
        self.assertIn(PENDING_ROLLBACK_MESSAGE, str(ctx.exception))

    def test_mechanism_ordinary_sql_exception_does_not_poison_the_connection(self):
        """Contrast case: an ordinary ``Exception`` from the DBAPI does NOT invalidate.

        Observed: ``invalidated = False``, the transaction stays active, and the next statement
        succeeds. Only a ``BaseException`` escape (the cancellation) is treated as a disconnect,
        which is exactly why ``Exception``-scoped handling never had to deal with this state.
        """
        connection = self._warm_connection()

        self.injector.arm(sqlite3.OperationalError("boom"), match="SELECT 2")
        with self.assertRaises(Exception) as ctx:
            connection.execute(text("SELECT 2"))
        self.assertNotIsInstance(ctx.exception, PendingRollbackError)

        observed = transaction_state(connection)
        self.assertFalse(connection.invalidated, f"observed state: {observed}")
        self.assertEqual([(3,)], connection.execute(text("SELECT 3")).fetchall())

    # NOTE: `test_interrupt_through_sql_executor_escapes_and_poisons_the_connection` and
    # `test_interrupt_position_within_a_multi_statement_cell` lived here. Both pinned the pre-fix
    # symptom at the `SqlExecutor.execute` layer -- exactly what the Layer 1 guard changes -- and
    # both are fully subsumed by the expected-behaviour tests below and in `..._fix.py`. They were
    # removed rather than weakened; see "OBSOLETE CHARACTERIZATION TESTS AND WHERE THEIR FACTS
    # LIVE NOW" in the module docstring for what each measured and which test now owns it.

    def test_poisoned_connection_survives_the_connection_cache(self):
        """``closed`` cannot distinguish a poisoned connection, so eviction never fires on it.

        Observed on pre-fix code: ``ConnectionCache.get`` returned the very same
        ``ManagedConnection`` with ``connection.closed is False`` -- the connection is
        invalidated, not closed, so the ``closed``-only health check passed and the broken
        connection was handed straight to the next query. That is how the poison propagated.

        These assertions hold unchanged after the fix, with the opposite reading: the entry is
        still the same object and still not closed, because Layer 2 resets a recoverable
        connection IN PLACE rather than evicting it, which is what keeps the persisted session
        continuous. ``invalidated`` also stays ``True`` here, because ``rollback()`` clears the
        transaction without reconnecting; the connection revalidates on its next ``execute()``.
        That the reset actually happened, and that the connection is usable afterwards, is
        asserted by the Layer 2 tests in ``..._fix.py`` -- this test only pins that the
        ``closed``-based eviction path is not what reacts to this state.
        """
        connection = self._warm_connection()
        raised, _ = interrupt_through_executor(
            self.executor, self.engine, connection, "SELECT 2", self.injector, "SELECT 2"
        )
        self.assertIsInstance(raised, KeyboardInterrupt)

        cache = ConnectionCache()
        key = "conn-1"
        managed = ManagedConnection(
            engine=self.engine, connection=connection, id=str(uuid4()), cache_key=key
        )
        cache.put(key, managed)

        handed_out = cache.get(key)

        observed = transaction_state(connection)
        self.assertIs(handed_out, managed, f"observed state: {observed}")
        self.assertFalse(connection.closed, f"observed state: {observed}")
        self.assertTrue(connection.invalidated, f"observed state: {observed}")

    def test_interrupt_while_executor_generator_is_suspended_window_b(self):
        """Window B (exploratory): interrupt delivered between ``next()`` calls.

        Statement 1 yields successfully, then the consumer (standing in for ``display()``) is
        interrupted while the executor generator is suspended. Observed, recorded verbatim:

            while suspended:   txn=<RootTransaction ...> is_active=True
                               invalidated=False closed=False
            after gc.collect() (generator finalized, GeneratorExit thrown in):
                               txn=<RootTransaction ...> is_active=True
                               invalidated=False closed=False
            next statement:    SUCCESS -- no PendingRollbackError

        So Window B does NOT poison the connection: the interrupt never reaches the DBAPI call,
        nothing is invalidated, and the connection stays usable. It leaves an open, uncommitted
        transaction, nothing more. So this window does not on its own justify Layer 2 (the cache
        hand-out check): there is nothing here to heal.
        """
        connection = self._warm_connection()
        generator = self.executor.execute(self.engine, "SELECT 1; SELECT 2", connection=connection)

        first = next(generator)
        self.assertEqual(ExecutionStatus.SUCCESS.value, first.status)

        # The interrupt lands in the consumer's frame, not the generator's.
        with self.assertRaises(KeyboardInterrupt):
            raise KeyboardInterrupt("cancel during display()")

        while_suspended = transaction_state(connection)
        self.assertFalse(connection.invalidated, f"observed state: {while_suspended}")

        del generator
        gc.collect()

        after_finalize = transaction_state(connection)
        self.assertFalse(connection.invalidated, f"observed state: {after_finalize}")
        self.assertFalse(connection.closed, f"observed state: {after_finalize}")
        self.assertIsNotNone(connection.get_transaction(), f"observed state: {after_finalize}")
        self.assertTrue(connection.get_transaction().is_active, f"observed state: {after_finalize}")
        self.assertEqual(
            [(3,)],
            connection.execute(text("SELECT 3")).fetchall(),
            f"Window B left the connection usable; observed: {after_finalize}",
        )

    def test_non_transactional_engine_is_unaffected_by_the_interrupt(self):
        """Control: the Athena / Redshift Data API baseline, which the fix must not move.

        ``get_transaction()`` returns ``None``, so an interrupt leaves no transaction to abort and
        the next statement runs normally -- before and after the fix alike.
        """
        connection = NonTransactionalConnection(self.engine)
        connection.arm(KeyboardInterrupt("simulated UI cancel"))

        raised, yielded = None, []
        try:
            for result in self.executor.execute(self.engine, "SELECT 1", connection=connection):
                yielded.append(result)
        except BaseException as exc:  # noqa: BLE001
            raised = exc

        self.assertIsInstance(raised, KeyboardInterrupt)
        self.assertEqual([], yielded)
        self.assertIsNone(connection.get_transaction())
        self.assertFalse(connection.closed)

        followup = list(self.executor.execute(self.engine, "SELECT 2", connection=connection))
        self.assertEqual(1, len(followup))
        self.assertEqual(ExecutionStatus.SUCCESS.value, followup[0].status)
        self.assertNotIn(PENDING_ROLLBACK_MESSAGE, str(followup[0].error))


class CancelledQueryEndToEndCharacterizationTest(unittest.TestCase):
    """End-to-end through ``sqlutils.sql_stream`` with ``persist_session=True``.

    The single test here originally asserted the pre-fix symptom (call 3 fails after call 2 is
    cancelled); it now asserts the fixed behaviour on the one fact that is still true and still
    load-bearing -- the cancelled connection stays the SAME cached object. See the test docstring
    for the pre-fix measurement.
    """

    def setUp(self):
        self.engine, self.injector = build_interruptible_engine()
        self.addCleanup(self.engine.dispose)

        self._previous_executor = sqlutils._sql_executor
        sqlutils._sql_executor = SqlExecutor()
        sqlutils._connection_cache.clear()
        self.addCleanup(sqlutils._connection_cache.clear)
        self.addCleanup(setattr, sqlutils, "_sql_executor", self._previous_executor)

        patches = [
            patch.object(
                sqlutils,
                "_resolve_connection",
                return_value=SimpleNamespace(type=TRANSACTIONAL_CONNECTION_TYPE),
            ),
            patch.object(sqlutils, "_get_engine_from_connection", return_value=self.engine),
            # Athena-only context sniffing; irrelevant here and it would hit sql_handler.
            patch.object(sqlutils, "_apply_athena_context", return_value=None),
        ]
        for p in patches:
            p.start()
            self.addCleanup(p.stop)

    def _cached_connection(self):
        managed = sqlutils._connection_cache.get("conn-1")
        self.assertIsNotNone(managed, "persist_session=True should have cached the connection")
        return managed.connection

    def test_cancelled_connection_is_healed_in_place_and_stays_the_cached_one(self):
        """The cancelled connection is repaired in place, not replaced, and keeps working.

        MEASURED ON PRE-FIX CODE (this test's original form, kept as the record of what the bug
        did end to end). Cancelling call 2 left the poisoned ``Connection`` as the cached one and
        every later query on it failed::

            call 1 "SELECT 1"  -> [success]; cache key conn-1 now holds a live Connection
            call 2 "SELECT 2"  -> KeyboardInterrupt raised out of sql_stream
            cached connection  -> the SAME object, invalidated, closed False
            call 3 "SELECT 3"  -> [error], error text contains
                                  "Can't reconnect until invalid transaction is rolled back"
            connection.execute(text("SELECT 4")) -> PendingRollbackError

        Call 3 did not *raise* out of ``sql_stream``: ``PendingRollbackError`` is an
        ``Exception``, so ``execute_statements`` converted it into an ERROR ``ExecutionResult``
        (``_materialise_stream`` is what turns that into a raised error in the real cell). The
        underlying ``Connection`` did raise it, which is why the original asserted on both.

        AFTER THE FIX the connection-identity assertion is unchanged and is the point of the
        test: the cancellation is healed in place by Layer 1, so the cache entry is neither
        evicted nor rebuilt and the persisted session stays continuous. Only the verdict on the
        following statement flips, from ``PendingRollbackError`` to success.
        """
        # Call 1: warm the cache and the root transaction.
        warmup = list(sqlutils.sql_stream("SELECT 1", connection_id="conn-1"))
        self.assertEqual([ExecutionStatus.SUCCESS.value], [r.status for r in warmup])
        connection = self._cached_connection()

        # Call 2: cancelled mid-statement. The cancellation still reaches the caller.
        self.injector.arm(KeyboardInterrupt("simulated UI cancel"), match="SELECT 2")
        with self.assertRaises(KeyboardInterrupt) as ctx:
            list(sqlutils.sql_stream("SELECT 2", connection_id="conn-1"))
        self.assertEqual("simulated UI cancel", str(ctx.exception))

        # Repaired in place: the same Connection object is still the cached one, and the cache
        # still holds exactly one entry for the key (nothing was evicted and rebuilt).
        self.assertIs(connection, self._cached_connection())
        self.assertFalse(connection.closed)
        self.assertEqual(1, len(sqlutils._connection_cache))

        # Call 3: every later query on that connection now works.
        results = list(sqlutils.sql_stream("SELECT 3", connection_id="conn-1"))
        self.assertEqual(1, len(results))
        self.assertEqual(
            ExecutionStatus.SUCCESS.value,
            results[0].status,
            f"query after cancellation failed with: {results[0].error}",
        )
        self.assertNotIn(PENDING_ROLLBACK_MESSAGE, str(results[0].error))

        # ... including directly on the Connection, which is where the symptom used to surface.
        self.assertEqual([(4,)], connection.execute(text("SELECT 4")).fetchall())


class CancelledQueryExpectedBehaviorTest(unittest.TestCase):
    """The behaviour the fix guarantees for a cancelled statement.

    For any statement cancelled mid-execution on a cached, caller-managed connection to a
    transactional engine, the cancellation must propagate unchanged, the connection's transaction
    state must be clean afterwards, and the next statement must run normally -- with no
    ``PendingRollbackError`` and no kernel restart or manual ``close_connection()``.
    """

    def setUp(self):
        self.engine, self.injector = build_interruptible_engine()
        self.executor = SqlExecutor()
        self.addCleanup(self.engine.dispose)

    def test_cancellation_leaves_the_connection_reusable(self):
        """Layer 1: interrupt through the caller-managed branch, then reuse the connection."""
        connection = self.engine.connect()
        self.addCleanup(connection.close)
        connection.execute(text("SELECT 1"))

        raised, _ = interrupt_through_executor(
            self.executor, self.engine, connection, "SELECT 2", self.injector, "SELECT 2"
        )

        # The cancellation still reaches the user, unchanged.
        self.assertIsInstance(raised, KeyboardInterrupt)
        self.assertEqual("simulated UI cancel", str(raised))

        # The transaction state is clean ...
        observed = transaction_state(connection)
        self.assertIsNone(
            connection.get_transaction(),
            f"cancellation should have reset the transaction; observed: {observed}",
        )
        # ... and the next statement runs normally.
        followup = list(self.executor.execute(self.engine, "SELECT 3", connection=connection))
        self.assertEqual(1, len(followup))
        self.assertEqual(
            ExecutionStatus.SUCCESS.value,
            followup[0].status,
            f"next statement failed with: {followup[0].error}",
        )

    def test_connection_cache_does_not_hand_out_a_poisoned_connection(self):
        """Layer 2: a connection poisoned outside the executor must be healed on acquire."""
        connection = self.engine.connect()
        self.addCleanup(connection.close)
        connection.execute(text("SELECT 1"))
        self.injector.arm(KeyboardInterrupt("simulated UI cancel"), match="SELECT 2")
        with self.assertRaises(KeyboardInterrupt):
            connection.execute(text("SELECT 2"))

        cache = ConnectionCache()
        key = "conn-1"
        managed = ManagedConnection(
            engine=self.engine, connection=connection, id=str(uuid4()), cache_key=key
        )
        cache.put(key, managed)

        handed_out = cache.get(key)

        self.assertIsNotNone(handed_out, "get() should reset and return, or evict and replace")
        self.assertEqual(
            managed.id,
            handed_out.id,
            "a recoverable connection should be reset in place, keeping session continuity",
        )
        self.assertEqual([(3,)], handed_out.connection.execute(text("SELECT 3")).fetchall())


class CancelledQueryExpectedBehaviorEndToEndTest(unittest.TestCase):
    """The same guarantee end to end through ``sqlutils.sql_stream``."""

    def setUp(self):
        self.engine, self.injector = build_interruptible_engine()
        self.addCleanup(self.engine.dispose)

        self._previous_executor = sqlutils._sql_executor
        sqlutils._sql_executor = SqlExecutor()
        sqlutils._connection_cache.clear()
        self.addCleanup(sqlutils._connection_cache.clear)
        self.addCleanup(setattr, sqlutils, "_sql_executor", self._previous_executor)

        patches = [
            patch.object(
                sqlutils,
                "_resolve_connection",
                return_value=SimpleNamespace(type=TRANSACTIONAL_CONNECTION_TYPE),
            ),
            patch.object(sqlutils, "_get_engine_from_connection", return_value=self.engine),
            patch.object(sqlutils, "_apply_athena_context", return_value=None),
        ]
        for p in patches:
            p.start()
            self.addCleanup(p.stop)

    def test_next_query_succeeds_without_closing_the_connection(self):
        """No kernel restart and no manual ``close_connection()`` should be needed."""
        list(sqlutils.sql_stream("SELECT 1", connection_id="conn-1"))

        self.injector.arm(KeyboardInterrupt("simulated UI cancel"), match="SELECT 2")
        with self.assertRaises(KeyboardInterrupt):
            list(sqlutils.sql_stream("SELECT 2", connection_id="conn-1"))

        results = list(sqlutils.sql_stream("SELECT 3", connection_id="conn-1"))
        self.assertEqual(1, len(results))
        self.assertEqual(
            ExecutionStatus.SUCCESS.value,
            results[0].status,
            f"query after cancellation failed with: {results[0].error}",
        )


if __name__ == "__main__":
    unittest.main()
