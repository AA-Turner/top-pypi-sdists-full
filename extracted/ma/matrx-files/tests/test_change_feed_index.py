from pathlib import Path
from importlib.resources import files



PACKAGE_ROOT = Path(__file__).resolve().parents[1]


def test_package_change_feed_index_matches_owner_order_contract() -> None:
    sql = files("matrx_files").joinpath(
        "cloud_sync", "sql", "022_owner_change_feed_index.sql"
    ).read_text()

    assert "ON cld_files (owner_id, updated_at, id)" in sql
    assert "WHERE deleted_at IS NULL" in sql
