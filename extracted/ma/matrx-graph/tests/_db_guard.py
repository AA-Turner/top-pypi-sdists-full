"""Production-database refusal gate for DB-writing test suites.

WHY THIS EXISTS: the Postgres-backed integration tests (DefinitionStore /
RunStore / PostgresCheckpointer) create and archive real ``workflow.*``
rows. DB targeting is purely ``SUPABASE_MATRIX_*`` env vars — the same
vars that point at PRODUCTION on a developer machine with a normal
``.env``. That is exactly how 46 junk ``e2e-test-*`` / ``transition-test-*``
definitions ended up in the production database (see
``docs/archive/2026/workflow__AUDIT_2026_07_08.md``).

This gate resolves the registered matrx-orm config and HARD-FAILS —
loudly, before any row is written — when its connection fingerprint
(host / user / database name / supabase_url) matches a known production
project ref.

Escape hatch: ``MATRX_ALLOW_PROD_DB_TESTS=1`` (explicit, per-invocation,
never set in CI). If you think you need it, you almost certainly don't.

Usage — call right after ``register_database_from_env(...)`` in any
fixture that bootstraps a real DB connection for tests:

    from tests_db_guard import assert_not_production_db   # or relative import
    assert_not_production_db("supabase_automation_matrix")
"""

from __future__ import annotations

import os

# Supabase project refs that are PRODUCTION. The ref appears in the direct
# host (db.<ref>.supabase.co), the pooler user (postgres.<ref>), and the
# project API URL (https://<ref>.supabase.co) — the fingerprint below
# checks all of them.
PRODUCTION_PROJECT_REFS: tuple[str, ...] = (
    # THE LIVE PLATFORM DATABASE. `db.matrxserver.com` resolves here — verified
    # 2026-08-20 via the gateway's own `sb-project-ref` header. This is the ref
    # that must never be a test target.
    "brsgrqvjdzwihsvnfqkf",
    # The former West project. Named "Matrx Main" in the Supabase dashboard,
    # which is why agents keep reaching for it; it is rollback-only and still
    # ACTIVE_HEALTHY, so it is equally forbidden as a test target.
    "txzxabzwovsujtloxrus",
)

ALLOW_ENV_VAR = "MATRX_ALLOW_PROD_DB_TESTS"

_BANNER = "=" * 78


class ProductionDatabaseRefused(RuntimeError):
    """Raised when a test suite is pointed at a production database."""


def assert_not_production_db(config_name: str) -> None:
    """Hard-fail if the registered matrx-orm config points at production.

    Call this AFTER ``register_database_from_env(...)`` and BEFORE any test
    writes a row. Raises :class:`ProductionDatabaseRefused` unless
    ``MATRX_ALLOW_PROD_DB_TESTS=1`` is explicitly set.
    """
    from matrx_orm import get_database_config

    cfg = get_database_config(config_name)
    fingerprint = " ".join(
        str(cfg.get(key) or "") for key in ("host", "user", "database_name", "supabase_url")
    ).lower()

    hits = [ref for ref in PRODUCTION_PROJECT_REFS if ref in fingerprint]
    if not hits:
        return

    if os.environ.get(ALLOW_ENV_VAR) == "1":
        print(
            f"\n{_BANNER}\n"
            f"⚠️  {ALLOW_ENV_VAR}=1 — tests are RUNNING AGAINST PRODUCTION "
            f"(project ref: {', '.join(hits)}).\n"
            f"Every row these tests create lands in the live database. "
            f"You asked for this explicitly.\n{_BANNER}\n"
        )
        return

    raise ProductionDatabaseRefused(
        f"\n{_BANNER}\n"
        f"🛑 REFUSING TO RUN DB-WRITING TESTS AGAINST PRODUCTION\n"
        f"{_BANNER}\n"
        f"The registered database '{config_name}' resolves to production "
        f"project ref(s): {', '.join(hits)}\n"
        f"  host          = {cfg.get('host')}\n"
        f"  user          = {cfg.get('user')}\n"
        f"  database_name = {cfg.get('database_name')}\n\n"
        f"These tests CREATE AND ARCHIVE real workflow.* rows. Running them "
        f"here is how 46 junk\n"
        f"e2e-test-*/transition-test-* definitions polluted the production DB "
        f"(docs/archive/2026/workflow__AUDIT_2026_07_08.md).\n\n"
        f"Fix: point SUPABASE_MATRIX_* at a scratch/CI Postgres (see "
        f"packages/matrx-graph/tests/ci/), or —\n"
        f"if you REALLY mean production — set {ALLOW_ENV_VAR}=1 explicitly.\n"
        f"{_BANNER}"
    )
