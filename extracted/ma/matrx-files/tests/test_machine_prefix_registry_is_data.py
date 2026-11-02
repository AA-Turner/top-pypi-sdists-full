"""The machine-written prefix registry is DATA, never a filter (SPEC-SERVER §1.5).

It exists for exactly one consumer: the first-run top-level folder selection, which
pre-deselects machine-written trees so a new user is not asked about
``coding-sessions/``. The instant it becomes a query filter it starts HIDING files --
a second visibility rule beside ``files.is_user_visible_path``, which is precisely the
disagreement between disk and browser that D16 forbids. A file under a registered
prefix that the user selects anyway syncs normally.
"""

from __future__ import annotations

import os
from pathlib import Path

import pytest
import matrx_files

SOURCE_ROOT = Path(matrx_files.__file__).resolve().parent
PACKAGE_ROOT = SOURCE_ROOT.parent

_TABLE = "machine_written_prefixes"
_REQUIRED_ENV = ("SUPABASE_MATRIX_HOST", "SUPABASE_MATRIX_PASSWORD")

# The seven seeds, each with a writer named in code (S4). 'Product Captures' and
# 'Inbox' look user-named and are deliberately absent.
EXPECTED_PREFIXES = {
    "coding-sessions",
    "tool-images",
    "pdf-extractions",
    "FastFire",
    "Commerce Intake",
    "Transcripts/Recordings",
    "pc-share",
}


def test_no_package_code_queries_the_registry() -> None:
    """Red the moment somebody joins or filters files.files against this table.

    ``matrx_files/db/`` is excluded: those files are GENERATED from the live
    schema, so the model and its manager exist for every table whether anything
    calls them or not. What this guard is for is hand-written code -- the feed,
    the tree, a service, an RLS helper -- reaching for the registry as a filter.
    """
    offenders: list[str] = []
    for path in SOURCE_ROOT.rglob("*.py"):
        relative = path.relative_to(PACKAGE_ROOT)
        if relative.parts[1:2] == ("db",):
            continue  # generated model/manager surface, not a call site
        text = path.read_text(encoding="utf-8", errors="replace")
        if _TABLE in text or "MachineWrittenPrefixes" in text:
            offenders.append(str(relative))
    assert not offenders, (
        f"{_TABLE} is referenced from hand-written package code ({offenders}). It is "
        "a first-run selection catalog, not a filter: querying it against "
        "files.files creates a second visibility rule the sync feed does not "
        "share, which is exactly the browser/disk disagreement D16 forbids."
    )


def test_the_migration_says_so_in_its_own_header() -> None:
    sql = (SOURCE_ROOT / "cloud_sync" / "sql" / "027_machine_written_prefixes.sql").read_text()
    assert "DATA, NEVER A FILTER" in sql
    assert "p_data_class => 'organization'" in sql


@pytest.mark.integration
@pytest.mark.asyncio
async def test_the_seven_seeds_exist_and_pc_share_is_inactive() -> None:
    if [n for n in _REQUIRED_ENV if not os.environ.get(n)]:
        pytest.skip("live platform database unavailable")
    from matrx_orm import acquire_connection

    from matrx_files.db import bootstrap_db

    async with acquire_connection(bootstrap_db()) as conn:
        rows = [
            dict(r)
            for r in await conn.fetch(
                "SELECT prefix, writer, is_active, deselect_by_default, organization_id "
                "FROM files.machine_written_prefixes WHERE deleted_at IS NULL"
            )
        ]
    by_prefix = {r["prefix"]: r for r in rows}
    assert set(by_prefix) == EXPECTED_PREFIXES
    assert by_prefix["pc-share"]["is_active"] is False, (
        "pc-share has no writer found in six repos; it stays inactive until one is "
        "identified, so it neither deselects nor hides anything."
    )
    for prefix, row in by_prefix.items():
        assert row["organization_id"] is not None, (
            f"{prefix} has no organization_id: every org-scoped write carries one "
            "explicitly (no-db-assigned-org)."
        )
        if prefix != "pc-share":
            assert row["writer"] != "UNKNOWN", f"{prefix} is seeded without a named writer"
