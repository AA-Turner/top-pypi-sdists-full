from pathlib import Path
from importlib.resources import files

import pytest


PACKAGE_ROOT = Path(__file__).resolve().parents[1]
REPO_ROOT = PACKAGE_ROOT.parents[1]


def test_package_change_feed_index_matches_owner_order_contract() -> None:
    sql = files("matrx_files").joinpath(
        "cloud_sync", "sql", "022_owner_change_feed_index.sql"
    ).read_text()

    assert "ON cld_files (owner_id, updated_at, id)" in sql
    assert "WHERE deleted_at IS NULL" in sql


def test_host_change_feed_index_targets_canonical_table() -> None:
    migration = REPO_ROOT / "db" / "migrations" / "0475_files_owner_change_feed_index.sql"
    if not migration.exists():
        pytest.skip("host migration is unavailable in a standalone package install")
    sql = migration.read_text()

    assert "ON files.files (created_by, updated_at, id)" in sql
    assert "WHERE deleted_at IS NULL" in sql
