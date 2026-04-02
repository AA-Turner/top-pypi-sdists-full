from typing import Any


def filter_columns(
    data: list[dict[str, Any]], columns: list[str]
) -> list[dict[str, Any]]:
    return [{k: row[k] for k in columns if k in row} for row in data]
