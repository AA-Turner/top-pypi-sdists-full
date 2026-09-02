"""Database module for InnoDay."""

from contextlib import contextmanager

from .factory import (
    DatabaseFactory,
    close_database,
    get_database_backend,
    get_db_backend,
    get_db_session,
    initialize_database,
    set_database_backend,
)


def create_db_and_tables_sync():
    """Create database tables (synchronous, backward compatible)"""
    # Import here to avoid circular imports
    import os

    from sqlmodel import SQLModel, create_engine

    # Import models to ensure they're registered
    from ..domain import (
        BoardMetadata,
        BoardRegistration,
        BoardSyncHistory,
        ContainerExecution,
        LicenseAuditLog,
        LicenseTier,
        Organization,
        OrganizationLicense,
        OrganizationMembership,
        Repository,
        Ticket,
        TicketComment,
        UsageTracking,
        User,
    )

    DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///./innoday.db")
    engine = create_engine(
        DATABASE_URL, echo=os.getenv("DATABASE_ECHO", "false").lower() == "true"
    )
    SQLModel.metadata.create_all(engine)


import os

# Create a global engine for backward compatibility
from sqlmodel import create_engine

DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///./innoday.db")


def connect_args_for(url: str) -> dict:
    """Driver-specific connect kwargs -- today, a bound on how long a connect
    may take.

    psycopg2 inherits libpq's `connect_timeout`, which defaults to
    **unlimited**: a database that completes the TCP handshake and then never
    answers -- a black-holed route, a saturated pooler -- blocks the caller
    forever rather than failing. Unbounded was survivable while nothing touched
    the database at boot (`_assert_schema_at_head` is opt-in and off, and
    `create_db_and_tables_sync` is no longer called), but `_reap_orphaned_syncs`
    (#613) now runs before `lifespan` yields, so an unresponsive database would
    hang the deploy indefinitely instead of failing it -- turning a fix for a
    deploy-time bug into a new deploy-time hazard.

    Applied by driver because the key is not portable: SQLite's `connect()`
    raises `TypeError` on an unrecognised kwarg, so the test suite's SQLite URL
    must get an empty dict, not this. `INNODAY_DB_CONNECT_TIMEOUT` overrides the
    default; libpq's own minimum is 2 seconds.

    This is a *connect* bound only. It does not bound a query that has connected
    and hangs -- that needs `statement_timeout`, which is a separate decision
    about live request traffic and is deliberately not made here.
    """
    if url.startswith("postgres"):
        return {"connect_timeout": int(os.getenv("INNODAY_DB_CONNECT_TIMEOUT", "10"))}
    return {}


engine = create_engine(
    DATABASE_URL,
    echo=os.getenv("DATABASE_ECHO", "false").lower() == "true",
    connect_args=connect_args_for(DATABASE_URL),
)


def get_session():
    """FastAPI dependency. **Do not call this directly.**

    It is a generator so that `Depends(get_session)` can close the session when
    the request ends. Calling it by hand -- `next(get_session())` -- advances it
    to the `yield` and then discards the generator, so the `with` block below
    never exits deterministically and the connection is only returned when the
    garbage collector eventually finalises it. Behind Supabase's pooler that
    shows up as a session stuck `idle in transaction`, holding locks that make
    later `ALTER`/`DROP` statements hang (#482).

    Outside a request, use `session_scope()`.
    """
    from sqlmodel import Session

    with Session(engine) as session:
        yield session


@contextmanager
def session_scope():
    """A session for code that is not a FastAPI request.

    The counterpart to `get_session`, and the reason it exists: the generator
    form only cleans up when *something* closes it, and a plain call does not.
    This does, on every path including exceptions.
    """
    from sqlmodel import Session

    with Session(engine) as session:
        yield session


__all__ = [
    "DatabaseFactory",
    "get_database_backend",
    "set_database_backend",
    "initialize_database",
    "close_database",
    "get_db_session",
    "get_db_backend",
    "create_db_and_tables_sync",
    "connect_args_for",
    "get_session",
    "session_scope",
    "engine",
]
