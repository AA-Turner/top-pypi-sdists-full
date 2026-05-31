"""PostgreSQL connection handling for the web-editor DB backend.

Used only on the DB path (``ABSTRA_WEB_EDITOR_DATABASE_URI`` present). Imported
lazily from the repository factory so pods without the env var never import
psycopg.

Connection strategy (decision D11): every long-lived process — the editor pod,
the worker main process, and each (long-lived, pre-warmed) executor subprocess —
uses its own module-level ``ConnectionPool``. The pool gives us, for free:

* thread-safety: the log-flush daemon thread and the synchronous final-flush from
  ``ExecutionController.run()`` each check out a *distinct* connection;
* liveness/reconnect: ``check=ConnectionPool.check_connection`` validates a
  connection at checkout and transparently reopens one the server has dropped;
* clean teardown: ``close_pool()`` closes everything on shutdown.

A single hand-rolled persistent connection (as an earlier design suggested) would
have to reimplement all three and is easy to get wrong, so we do not.

A pool cannot be shared *across* processes (its background worker threads don't
survive ``fork`` — the very bug behind the executor ``PoolTimeout``), so each
process owns one. To keep the per-project connection budget bounded on the shared
tenants cluster, each process sizes its pool to its real concurrency via
``configure_pool(max_size=...)`` at boot: the worker main and each (serial)
executor need only ~2 (the synchronous final-flush + the log-flush daemon), while
the editor runs a threaded Flask server + the poller (~3).

Security: connection errors must never leak the password. Helpers here read the
URI from :mod:`abstra_internals.environment`; exceptions raised on a missing URI
never include its value, and callers that log connection failures must run the
message through :func:`mask_dsn_password`.
"""

import re

from abstra_internals.environment import WEB_EDITOR_DATABASE_URI

# Lazy imports of psycopg live inside the functions (D8): importing this module
# must not require psycopg unless the DB path is actually exercised. In practice
# the factory only imports this module on the DB path, but keeping psycopg out of
# module import scope is a cheap extra guard.

_pool = None  # type: ignore[var-annotated]  # Optional[psycopg_pool.ConnectionPool]

# Per-process pool ceiling. Overridden once at boot by each entrypoint via
# configure_pool(); the conservative default covers any process that forgets to.
_DEFAULT_MAX_SIZE = 4
_max_size = _DEFAULT_MAX_SIZE

_MISSING_URI_MESSAGE = "ABSTRA_WEB_EDITOR_DATABASE_URI not set"

# Matches the password component of a libpq URI/keyword DSN so it can be redacted
# before any error text is logged. Never log a raw DSN.
_PASSWORD_PATTERNS = (
    re.compile(r"(://[^:/?#@]+:)[^@/?#]*(@)"),  # postgresql://user:PASS@host
    re.compile(r"(password=)[^\s]*"),  # keyword/value: password=PASS
)


def mask_dsn_password(text: str) -> str:
    """Redact any password embedded in a DSN/URI within ``text`` for safe logging."""
    masked = _PASSWORD_PATTERNS[0].sub(r"\1***\2", text)
    masked = _PASSWORD_PATTERNS[1].sub(r"\1***", masked)
    return masked


def configure_pool(*, max_size: int) -> None:
    """Set this process's pool ``max_size``. Call once at boot, before the first
    ``get_pool()``.

    Per-process sizing keeps the per-project connection budget bounded on the
    shared tenants cluster (a pool can't be shared across processes — see module
    docstring). Sensible values: executor=2, worker=2, editor=3. Has no effect on
    an already-created pool (sizing is fixed at creation), so it must precede the
    first checkout — which every entrypoint does (it runs before building repos).
    """
    global _max_size
    _max_size = max_size


def get_pool():
    """Return the process-wide connection pool, creating it on first use.

    Raises ``RuntimeError`` (without echoing the URI) if the DB env var is unset.
    """
    global _pool
    if _pool is None:
        if WEB_EDITOR_DATABASE_URI is None:
            raise RuntimeError(_MISSING_URI_MESSAGE)
        from psycopg_pool import ConnectionPool

        _pool = ConnectionPool(
            conninfo=WEB_EDITOR_DATABASE_URI,
            min_size=0,
            max_size=_max_size,
            # Cover typical inter-execution idle gaps so the first log flush of a
            # burst doesn't pay a cold TCP+auth handshake (adds latency to the
            # first live-log line). min_size=0 still releases on true idle.
            max_idle=120,
            timeout=10,
            # autocommit: every statement is its own transaction, so a connection
            # returned to the pool never lingers "idle in transaction" (which would
            # hold row locks and block VACUUM).
            kwargs={"autocommit": True},
            # Validate the connection at checkout; transparently reopen a stale one
            # the server dropped during an idle gap.
            check=ConnectionPool.check_connection,
        )
    return _pool


def new_connection():
    """Open a single standalone autocommit connection.

    Kept for one-off scripts/migrations contexts; the repositories use the pool.
    """
    if WEB_EDITOR_DATABASE_URI is None:
        raise RuntimeError(_MISSING_URI_MESSAGE)
    import psycopg

    return psycopg.connect(WEB_EDITOR_DATABASE_URI, autocommit=True)


def close_pool() -> None:
    """Close the process-wide pool on graceful shutdown."""
    global _pool
    if _pool is not None:
        _pool.close()
        _pool = None


def log_pool_stats() -> None:
    """Best-effort emit of pool statistics for observability (§24.6).

    Emits as structured attrs (not a repr) so ``requests_waiting`` etc. are
    queryable/alertable; warns separately when checkouts are queuing (the
    pool-exhaustion signal §24.6 asks for)."""
    global _pool
    if _pool is None:
        return
    try:
        from abstra_internals.logger import AbstraLogger

        stats = _pool.get_stats()
        AbstraLogger.info("[db.pool] stats", dict(stats))
        if stats.get("requests_waiting"):
            AbstraLogger.warning(
                "[db.pool] checkouts waiting (pool may be exhausted)",
                {"requests_waiting": stats.get("requests_waiting")},
            )
    except Exception:
        pass


def _reset_pool_for_tests() -> None:
    """Test helper: close any live pool before dropping it.

    Closing (rather than just nulling) joins the pool's worker threads on the
    caller's thread, so the orphaned pool is never finalized by the GC on one of
    its own worker threads — which would raise "cannot join current thread"."""
    global _pool, _max_size
    if _pool is not None:
        try:
            _pool.close()
        except Exception:
            pass
        _pool = None
    _max_size = _DEFAULT_MAX_SIZE
