from __future__ import annotations

from typing import Any

from matrx_ai._ext import get_ext

def _df(name: str) -> Any:
    """Resolve one of the host's dataset fetchers LAZILY, at first use.

    Binding these at import time made ``import matrx_ai.db.content_types.datasets``
    raise ``ExtNotConfiguredError`` on a standalone install — an un-importable
    module, not a degraded capability. The package must import cleanly with no
    host configured; only actually *calling* a dataset fetcher requires one.
    """
    return get_ext("dataset_reference_fetch")[name]


def fetch_full_table(*args: Any, **kwargs: Any) -> Any:
    return _df("fetch_full_table")(*args, **kwargs)


def fetch_table_cell(*args: Any, **kwargs: Any) -> Any:
    return _df("fetch_table_cell")(*args, **kwargs)


def fetch_table_column(*args: Any, **kwargs: Any) -> Any:
    return _df("fetch_table_column")(*args, **kwargs)


def fetch_table_row(*args: Any, **kwargs: Any) -> Any:
    return _df("fetch_table_row")(*args, **kwargs)


# ---------------------------------------------------------------------------
# Manager — backed by the udt_datasets / udt_dataset_fields / udt_dataset_rows
# tables (see aidream db migration 0011). Bookmark wire types are kept under
# their original names ("full_table", "table_row", "table_cell", "table_column")
# because frontends already serialize cookies that way.
# ---------------------------------------------------------------------------

class DatasetsManager:
    _instance: DatasetsManager | None = None

    def __new__(cls) -> DatasetsManager:
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance

    # ------------------------------------------------------------------
    # Raw fetch — returns plain Python data, no XML
    # ------------------------------------------------------------------

    def get_full_table(
        self,
        table_id: str,
        *,
        limit: int = 100,
        offset: int = 0,
        sort_field: str | None = None,
        sort_direction: str = "asc",
    ) -> dict[str, Any]:
        try:
            rows = fetch_full_table(
                table_id,
                limit=limit,
                offset=offset,
                sort_field=sort_field,
                sort_direction=sort_direction,
            )
            return {"success": True, "table_id": table_id, "rows": rows, "row_count": len(rows)}
        except Exception as e:
            return {"success": False, "operation": "get_full_table", "table_id": table_id, "error": str(e)}

    def get_table_column(
        self,
        table_id: str,
        column_name: str,
        *,
        limit: int = 100,
        offset: int = 0,
    ) -> dict[str, Any]:
        try:
            rows = fetch_table_column(table_id, column_name, limit=limit, offset=offset)
            return {"success": True, "table_id": table_id, "column_name": column_name, "rows": rows}
        except Exception as e:
            return {"success": False, "operation": "get_table_column", "table_id": table_id, "error": str(e)}

    def get_table_row(self, table_id: str, row_id: str) -> dict[str, Any]:
        try:
            row = fetch_table_row(table_id, row_id)
            return {"success": True, "table_id": table_id, "row_id": row_id, "row": row}
        except Exception as e:
            return {"success": False, "operation": "get_table_row", "table_id": table_id, "error": str(e)}

    def get_table_cell(self, table_id: str, row_id: str, column_name: str) -> dict[str, Any]:
        try:
            value = fetch_table_cell(table_id, row_id, column_name)
            return {"success": True, "table_id": table_id, "row_id": row_id, "column_name": column_name, "value": value}
        except Exception as e:
            return {"success": False, "operation": "get_table_cell", "table_id": table_id, "error": str(e)}


datasets_manager_instance = DatasetsManager()
