"""Smoke test for the Postgres test infrastructure (S0).

Confirms the ephemeral container fixture yields a usable, isolated database.
"""

import psycopg


def test_pg_uri_connects_and_selects_one(pg_uri):
    with psycopg.connect(pg_uri, autocommit=True) as conn:
        row = conn.execute("SELECT 1").fetchone()
        assert row is not None and row[0] == 1


def test_pg_uri_is_isolated_fresh_database(pg_uri):
    # A brand-new database has no user tables.
    with psycopg.connect(pg_uri, autocommit=True) as conn:
        row = conn.execute(
            "SELECT count(*) FROM information_schema.tables "
            "WHERE table_schema = 'public'"
        ).fetchone()
        assert row is not None and row[0] == 0
