"""Migration runner for the cloud sync database schema.

Provides utilities to apply the SQL migration scripts that create the
required tables, indexes, triggers, and RLS policies.

Usage::

    from matrx_files.cloud_sync import run_migrations

    # Option 1: Direct Postgres connection (requires psycopg2)
    run_migrations("postgresql://user:pass@host:5432/dbname")

    # Option 2: Print the SQL for manual execution
    sql = get_migration_sql()
    print(sql)  # paste into Supabase SQL Editor, psql, etc.

    # Option 3: Check if the schema is already applied
    if not is_schema_applied("postgresql://..."):
        run_migrations("postgresql://...")
"""

from __future__ import annotations

import logging
from importlib.resources import files as pkg_files
from pathlib import Path

logger = logging.getLogger(__name__)

_SQL_DIR = Path(__file__).parent / "sql"


def get_migration_sql(migration: str = "001_initial_schema.sql") -> str:
    """Return the raw SQL text of a migration file.

    The SQL files are shipped inside the package so they're available
    even when installed via pip.
    """
    sql_path = _SQL_DIR / migration
    if not sql_path.exists():
        raise FileNotFoundError(f"Migration file not found: {sql_path}")
    return sql_path.read_text(encoding="utf-8")


def get_all_migration_files() -> list[str]:
    """Return sorted list of migration file names."""
    if not _SQL_DIR.exists():
        return []
    return sorted(f.name for f in _SQL_DIR.glob("*.sql"))


def run_migrations(
    database_url: str,
    *,
    migrations: list[str] | None = None,
    dry_run: bool = False,
) -> list[str]:
    """Apply SQL migrations to a Postgres database.

    Requires ``psycopg2`` (or ``psycopg2-binary``) to be installed.
    If not available, use ``get_migration_sql()`` to get the raw SQL
    and run it manually.

    Parameters
    ----------
    database_url:
        PostgreSQL connection string.
    migrations:
        List of migration filenames to run.  Defaults to all files
        in the sql/ directory, sorted alphabetically.
    dry_run:
        If True, print the SQL instead of executing it.

    Returns
    -------
    list[str]
        Names of migrations that were applied.
    """
    try:
        import psycopg2  # type: ignore[import-untyped]
    except ImportError:
        raise ImportError(
            "psycopg2 is required to run migrations programmatically. "
            "Install it with: pip install psycopg2-binary\n"
            "Alternatively, use get_migration_sql() to get the raw SQL "
            "and run it in your Supabase SQL Editor or psql."
        )

    if migrations is None:
        migrations = get_all_migration_files()

    applied: list[str] = []

    conn = psycopg2.connect(database_url)
    try:
        conn.autocommit = False
        cur = conn.cursor()

        for migration_name in migrations:
            sql = get_migration_sql(migration_name)

            if dry_run:
                logger.info("DRY RUN — would apply: %s", migration_name)
                print(f"-- Migration: {migration_name}")
                print(sql)
                print()
                applied.append(migration_name)
                continue

            logger.info("Applying migration: %s", migration_name)
            cur.execute(sql)
            applied.append(migration_name)
            logger.info("Applied: %s", migration_name)

        if not dry_run:
            conn.commit()
            logger.info("All migrations committed successfully.")

    except Exception:
        if not dry_run:
            conn.rollback()
            logger.error("Migration failed — rolled back.", exc_info=True)
        raise
    finally:
        conn.close()

    return applied


def is_schema_applied(database_url: str) -> bool:
    """Check if the cloud_sync tables already exist.

    Returns True if the canonical ``files.files`` table is found (the 2026
    DB canonicalization moved the file tables into the ``files`` schema and
    dropped the ``cld_`` prefix). Requires ``psycopg2``.
    """
    try:
        import psycopg2  # type: ignore[import-untyped]
    except ImportError:
        raise ImportError(
            "psycopg2 is required for schema checks. "
            "Install it with: pip install psycopg2-binary"
        )

    conn = psycopg2.connect(database_url)
    try:
        cur = conn.cursor()
        cur.execute("""
            -- pg_catalog, never information_schema: this decides whether the
            -- schema is already installed. information_schema is privilege-
            -- filtered, so read as an unexpected role it reports an existing
            -- files.files as absent and the installer re-runs against a live
            -- schema. (aidream FOUND_DEFECTS: pooler role contamination.)
            SELECT EXISTS (
                SELECT 1 FROM pg_class c
                JOIN pg_namespace n ON n.oid = c.relnamespace
                WHERE n.nspname = 'files' AND c.relname = 'files'
                  AND c.relkind = ANY ('{r,p,v,m,f}')
            )
        """)
        return cur.fetchone()[0]
    finally:
        conn.close()


def print_migration_sql(migration: str = "001_initial_schema.sql") -> None:
    """Print the migration SQL to stdout for manual execution."""
    sql = get_migration_sql(migration)
    print(f"-- Cloud Sync Migration: {migration}")
    print(f"-- Copy and paste this into your Supabase SQL Editor or psql")
    print(f"-- " + "=" * 60)
    print(sql)
