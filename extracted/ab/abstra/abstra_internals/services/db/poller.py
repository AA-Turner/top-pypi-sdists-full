"""Editor-side poller: streams DB changes to the frontend WebSocket.

Replaces the RabbitMQ ``stdio_broadcast`` consumer on the DB path. Runs only in
the editor pod (Knative ``min 0/max 1`` → a single poller, no coordination). The
frontend contract is unchanged: it still receives ``{"type":"stdio",...}``,
``{"type":"task",...}`` and ``{"type":"execution:update",...}`` on the same
``BroadcastController`` channel.

Cursor: the time window is computed from the DATABASE clock (``now()`` in SQL),
never the pod clock, to avoid pod↔server skew. A forward-only floor
(``boot_cursor``, captured on the first successful tick, back-dated by the window
so logs of an already-running execution at boot aren't missed) keeps older
history from being replayed; a ``WINDOW_SECONDS`` overlap behind the advancing
cursor catches commits that landed out of ``bigserial`` order.

The window + per-id dedup REDUCES but does not guarantee exactly-once: a flush
that takes longer than the window between its ``now()`` and commit can be missed.
This is accepted, bounded loss — the instance is disposable and the frontend
re-fetches history via ``GET /logs/<id>`` on reconnect.
"""

import threading
from datetime import timedelta

from abstra_internals.controllers.execution.execution_stdio import BroadcastController
from abstra_internals.logger import AbstraLogger
from abstra_internals.utils import serialize

CADENCE = 0.2
WINDOW_SECONDS = 2
_QUERY_LIMIT = 5000  # defensive per-tick cap, shared by all three scans

# Window floored at the forward-only boot cursor, then a WINDOW_SECONDS overlap
# behind the advancing cursor. Both bounds are DB-clock timestamptz parameters.
# WINDOW_SECONDS is interpolated from the int constant (never user input) so the
# SQL and the Python prune logic can never disagree on the window.
_LOGS_SQL = (
    "SELECT id, execution_id, stage_id, event, text, db_inserted_at "
    "FROM execution_logs "
    "WHERE db_inserted_at >= GREATEST(%s::timestamptz, "
    f"%s::timestamptz - interval '{WINDOW_SECONDS} seconds') "
    "ORDER BY id LIMIT %s"
)

_EXECUTIONS_SQL = (
    "SELECT id FROM executions "
    "WHERE db_updated_at >= GREATEST(%s::timestamptz, "
    f"%s::timestamptz - interval '{WINDOW_SECONDS} seconds') "
    "ORDER BY db_updated_at LIMIT %s"
)

_TASKS_SQL = (
    "SELECT * FROM tasks "
    "WHERE db_updated_at >= GREATEST(%s::timestamptz, "
    f"%s::timestamptz - interval '{WINDOW_SECONDS} seconds') "
    "ORDER BY db_updated_at LIMIT %s"
)


def start_poller() -> "tuple[threading.Event, threading.Thread]":
    """Start the poller daemon thread; return ``(stop_event, thread)`` so the
    shutdown path can stop AND join it before the pool is closed."""
    stop = threading.Event()
    thread = threading.Thread(target=_loop, args=(stop,), daemon=True, name="DbPoller")
    thread.start()
    return stop, thread


def _db_now(conn):
    return conn.execute("SELECT now()").fetchone()[0]


def _broadcast_stdio(row) -> None:
    # Shape required by the frontend WS client (decision D9): snake_case keys,
    # ``log`` (not ``payload.text``), ``type`` carrying the stdout/stderr event.
    payload = {
        "type": row[3],
        "log": row[4],
        "execution_id": row[1],
        "stage_id": row[2],
    }
    BroadcastController.broadcast(msg=serialize({"type": "stdio", "payload": payload}))


def _poll_logs(conn, boot_cursor, last_tick, seen: dict) -> None:
    cur = conn.execute(_LOGS_SQL, (boot_cursor, last_tick, _QUERY_LIMIT))
    for row in cur.fetchall():
        log_id = row[0]
        if log_id in seen:
            continue
        # Record before broadcasting so a tick that fails mid-emit does not
        # re-broadcast already-sent lines on the next tick.
        seen[log_id] = row[5]
        _broadcast_stdio(row)


def _poll_executions(conn, boot_cursor, last_tick) -> None:
    # No dedup: each event carries the full state, so re-emission within the
    # window is harmless. The UI's actual finished/failed transition comes from
    # stdout (D10); this keeps the existing execution:update channel populated.
    cur = conn.execute(_EXECUTIONS_SQL, (boot_cursor, last_tick, _QUERY_LIMIT))
    for (execution_id,) in cur.fetchall():
        BroadcastController.broadcast(
            msg=serialize(
                {"type": "execution:update", "payload": {"execution_id": execution_id}}
            )
        )


def _poll_tasks(conn, boot_cursor, last_tick) -> None:
    from psycopg.rows import dict_row

    from abstra_internals.repositories.tasks import task_row_to_dto

    with conn.cursor(row_factory=dict_row) as cur:
        cur.execute(_TASKS_SQL, (boot_cursor, last_tick, _QUERY_LIMIT))
        for row in cur.fetchall():
            dto = task_row_to_dto(row)
            BroadcastController.broadcast(
                msg=serialize({"type": "task", "payload": dto.dump()})
            )


def _prune_seen(seen: dict, tick_now) -> None:
    # Keep only ids whose db_inserted_at is still within the overlap window; ids
    # older than that can never reappear in a future query, so drop them. Bounds
    # the set to ~WINDOW_SECONDS of logs.
    cutoff = tick_now - timedelta(seconds=WINDOW_SECONDS)
    stale = [log_id for log_id, ts in seen.items() if ts < cutoff]
    for log_id in stale:
        del seen[log_id]


def _loop(stop: threading.Event) -> None:
    from .connection import get_pool, log_pool_stats

    # boot_cursor/last_tick are acquired lazily on the first successful tick, so a
    # transient DB outage at editor cold-start doesn't permanently kill streaming.
    boot_cursor = None
    last_tick = None
    seen: dict = {}
    ticks = 0
    consecutive_failures = 0
    stats_every = max(1, int(30 / CADENCE))

    while not stop.wait(CADENCE):
        tick_now = None
        try:
            with get_pool().connection() as conn:
                tick_now = _db_now(conn)
                if boot_cursor is None:
                    # Forward-only floor, back-dated by the window so logs of an
                    # execution already running at boot are still picked up.
                    boot_cursor = tick_now - timedelta(seconds=WINDOW_SECONDS)
                    last_tick = boot_cursor
                _poll_logs(conn, boot_cursor, last_tick, seen)
                _poll_executions(conn, boot_cursor, last_tick)
                _poll_tasks(conn, boot_cursor, last_tick)
            # Advance only on full success so a failed tick is retried (the
            # window + dedup make the retry idempotent).
            last_tick = tick_now
            consecutive_failures = 0
        except Exception as e:
            consecutive_failures += 1
            # Rate-limit: capture/warn on the first failure and then only every
            # ~10s, so a sustained outage doesn't flood Sentry every 200ms.
            if consecutive_failures == 1 or consecutive_failures % 50 == 0:
                AbstraLogger.warning(
                    "[db.poller] tick failed",
                    {"consecutiveFailures": consecutive_failures},
                )
                AbstraLogger.capture_exception(e)
        finally:
            # Prune even on partial failure (as long as we read the DB clock) so
            # `seen` can't grow unbounded during a stream that fails after logs.
            if tick_now is not None:
                _prune_seen(seen, tick_now)

        ticks += 1
        if ticks % stats_every == 0:
            AbstraLogger.info(
                "[db.poller] stats",
                {
                    "dedupSetSize": len(seen),
                    "consecutiveFailures": consecutive_failures,
                },
            )
            log_pool_stats()
