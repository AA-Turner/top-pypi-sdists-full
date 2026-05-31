"""Schema migration runner for the web-editor PostgreSQL backend.

Run once per pod at boot (editor entrypoint and worker entrypoint) — NEVER from
the repository factory, because the factory also runs in each executor warmup and
migrating there would take the advisory lock on every warmup (decision D11).

The DDL is embedded as a Python string rather than shipped as a ``.sql`` data
file: ``setup.py`` ``package_data`` only includes ``templates/*``, so ``.sql``
files would not land in the wheel (decision D2). Embedding also frees the runner
from depending on ``__file__``.

Concurrency: editor + N workers may boot in any order. A session-level advisory
lock serializes them; the first to acquire applies the pending delta, the rest
find nothing to do. ``CREATE TABLE _migrations`` runs *inside* the lock to avoid
the ``tuple concurrently updated`` race that concurrent ``CREATE TABLE IF NOT
EXISTS`` on the same relation can otherwise raise.
"""

from typing import TYPE_CHECKING, List, Tuple, cast

if TYPE_CHECKING:
    from typing_extensions import LiteralString

# Arbitrary fixed 64-bit key, "ABSTRALB" in ASCII hex. Fits a signed bigint.
# Shared by every pod so they serialize on the same lock.
_ADVISORY_LOCK_KEY = 0x4142535452414C42

# Ordered (version, SQL) migrations. Append new tuples with strictly increasing
# versions; never edit an already-released migration.
MIGRATIONS: List[Tuple[int, str]] = [
    (
        1,
        """
CREATE TABLE executions (
  id              text         PRIMARY KEY,
  stage_id        text         NOT NULL,
  status          text         NOT NULL CHECK (status IN ('running','failed','finished','abandoned')),
  pid             integer      NOT NULL,                  -- Execution.create always sets pid (os.getpid())
  worker_id       text         NOT NULL,                  -- Execution.create always sets worker_id
  context         jsonb        NOT NULL,
  created_at      timestamptz  NOT NULL,
  updated_at      timestamptz,                            -- Execution.updated_at is Optional (None until first status change)
  db_inserted_at  timestamptz  NOT NULL DEFAULT now(),
  db_updated_at   timestamptz  NOT NULL DEFAULT now()
);
CREATE INDEX idx_executions_db_updated   ON executions (db_updated_at);
CREATE INDEX idx_executions_created      ON executions (created_at DESC);
CREATE INDEX idx_executions_stage_status ON executions (stage_id, status);

CREATE TABLE tasks (
  id                      text         PRIMARY KEY,
  type                    text         NOT NULL,
  status                  text         NOT NULL CHECK (status IN ('pending','locked','completed')),
  target_stage_id         text         NOT NULL,
  payload                 jsonb        NOT NULL,
  created_at              timestamptz  NOT NULL,
  created_by_execution    text,
  created_by_stage        text,
  locked_at               timestamptz,
  locked_by_execution     text,
  locked_by_stage         text,
  completed_at            timestamptz,
  completed_by_execution  text,
  completed_by_stage      text,
  db_inserted_at          timestamptz  NOT NULL DEFAULT now(),
  db_updated_at           timestamptz  NOT NULL DEFAULT now()
);
CREATE INDEX idx_tasks_target_status_created ON tasks (target_stage_id, status, created_at DESC);
CREATE INDEX idx_tasks_created_by_stage      ON tasks (created_by_stage);
CREATE INDEX idx_tasks_created_by_execution  ON tasks (created_by_execution);
CREATE INDEX idx_tasks_locked_by_execution   ON tasks (locked_by_execution);
CREATE INDEX idx_tasks_db_updated            ON tasks (db_updated_at);

CREATE TABLE execution_logs (
  id              bigserial    PRIMARY KEY,
  execution_id    text         NOT NULL,
  stage_id        text         NOT NULL,
  event           text         NOT NULL CHECK (event IN ('stdout','stderr')),
  text            text         NOT NULL,
  sequence        integer      NOT NULL,
  created_at      timestamptz  NOT NULL,
  db_inserted_at  timestamptz  NOT NULL DEFAULT now()
);
CREATE INDEX idx_logs_execution    ON execution_logs (execution_id, id);
CREATE INDEX idx_logs_db_inserted  ON execution_logs (db_inserted_at);
""",
    ),
]


def apply_migrations() -> None:
    """Create/upgrade the schema. Idempotent and safe under concurrent boots.

    Uses a standalone one-off connection (NOT the shared pool) on purpose: the
    worker runs this at boot, BEFORE it forks the executor forkserver. If we
    created the process-wide pool here, the forkserver (and every executor forked
    from it) would inherit a pool whose background worker threads do not survive
    fork — so every connection checkout in an executor would hang until
    PoolTimeout. Keeping the pool uncreated until after the fork lets each
    executor build its own working pool."""
    from .connection import new_connection

    # Fail fast on a mis-authored migration list (duplicate / non-increasing
    # versions would otherwise be silently skipped by the `version <= current`
    # guard below).
    versions = [v for v, _ in MIGRATIONS]
    assert versions == sorted(set(versions)), (
        "MIGRATIONS versions must be unique and strictly increasing"
    )

    with new_connection() as conn:
        # Bound the advisory-lock wait: statement_timeout interrupts a waiting
        # pg_advisory_lock (lock_timeout does NOT apply to advisory-lock
        # functions), so a wedged holder fails this boot loudly instead of
        # hanging every booting pod indefinitely. Cleared before the DDL runs.
        conn.execute("SET statement_timeout = '30000'")
        conn.execute("SELECT pg_advisory_lock(%s)", (_ADVISORY_LOCK_KEY,))
        conn.execute("SET statement_timeout = '0'")
        try:
            conn.execute(
                "CREATE TABLE IF NOT EXISTS _migrations ("
                "  version integer PRIMARY KEY,"
                "  applied_at timestamptz NOT NULL DEFAULT now()"
                ")"
            )
            row = conn.execute(
                "SELECT COALESCE(MAX(version), 0) FROM _migrations"
            ).fetchone()
            current = row[0] if row else 0

            for version, sql in MIGRATIONS:
                if version <= current:
                    continue
                with conn.transaction():
                    # sql comes only from the in-repo MIGRATIONS literals (never
                    # user input); cast satisfies psycopg's LiteralString typing.
                    conn.execute(cast("LiteralString", sql))
                    conn.execute(
                        "INSERT INTO _migrations (version) VALUES (%s)", (version,)
                    )
        finally:
            conn.execute("SELECT pg_advisory_unlock(%s)", (_ADVISORY_LOCK_KEY,))
