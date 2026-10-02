from __future__ import annotations

import re
from pathlib import Path

from matrx_seo.orm_repository import _OBSERVATION_MODELS


def test_every_receipt_count_table_has_a_run_id_index_migration() -> None:
    migrations = Path(__file__).parents[1] / "matrx_seo" / "migrations"
    migration_sql = "\n".join(
        path.read_text(encoding="utf-8") for path in sorted(migrations.glob("*.sql"))
    )

    missing = [
        model._table_name
        for model in _OBSERVATION_MODELS
        if re.search(
            rf"create\s+(?:unique\s+)?index\b.*?\bon\s+seo\.{re.escape(model._table_name)}\s*\(\s*run_id\b",
            migration_sql,
            flags=re.IGNORECASE | re.DOTALL,
        )
        is None
    ]

    assert missing == [], (
        "receipt_for_run counts by run_id; add a run_id-leading index migration "
        f"for: {', '.join(missing)}"
    )
