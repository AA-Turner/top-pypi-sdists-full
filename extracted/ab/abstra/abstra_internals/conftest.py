"""Shared pytest fixtures for the PostgreSQL-backed web-editor storage tests.

Provisions an ephemeral PostgreSQL via ``testcontainers`` and hands each test a
freshly-created, empty database for isolation. Lives here (rather than under
``services/db/``) so both the ``services/db`` and ``repositories`` test suites
can request the same fixtures.

Docker is detected **inside** the fixture (runtime ``pytest.skip``), never via a
collection-time ``skipif`` — so on a machine without Docker the DB tests are
*skipped*, not *errored*. These fixtures are lazy: tests that only use mocks
(factory branching, send_stdio gating, final-flush wiring) never request them, so
they do not start Docker.
"""

from typing import TYPE_CHECKING, cast
from uuid import uuid4

import pytest

if TYPE_CHECKING:
    from typing_extensions import LiteralString

# Production runs PostgreSQL 17.10; pin the test image to the same major.
POSTGRES_IMAGE = "postgres:17"


@pytest.fixture(scope="session")
def pg_container():
    """Session-wide ephemeral Postgres container.

    Skips (does not error) when Docker / testcontainers is unavailable.
    """
    pytest.importorskip("testcontainers.postgres")
    from testcontainers.postgres import PostgresContainer

    try:
        # driver=None → plain ``postgresql://`` URL (libpq), which psycopg 3 uses
        # directly. The default ``postgresql+psycopg2`` driver string would not.
        container = PostgresContainer(POSTGRES_IMAGE, driver=None)
        container.start()
    except Exception as exc:  # Docker missing / daemon not running / image pull fails
        pytest.skip(f"Docker unavailable for Postgres testcontainer: {exc}")

    try:
        yield container
    finally:
        container.stop()


@pytest.fixture
def pg_uri(pg_container):
    """A fresh, empty database per test, for isolation.

    Yields a ``postgresql://`` URI pointing at the new database; drops it on
    teardown.
    """
    import psycopg

    admin_uri = pg_container.get_connection_url(driver=None)
    db_name = f"t_{uuid4().hex}"

    with psycopg.connect(admin_uri, autocommit=True) as conn:
        # db_name is a server-generated identifier (uuid hex) — safe to inline;
        # DDL identifiers cannot be parameterized anyway.
        conn.execute(cast("LiteralString", f'CREATE DATABASE "{db_name}"'))

    base = admin_uri.rsplit("/", 1)[0]
    uri = f"{base}/{db_name}"

    try:
        yield uri
    finally:
        with psycopg.connect(admin_uri, autocommit=True) as conn:
            conn.execute(
                cast(
                    "LiteralString", f'DROP DATABASE IF EXISTS "{db_name}" WITH (FORCE)'
                )
            )
