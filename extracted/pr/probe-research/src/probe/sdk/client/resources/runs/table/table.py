"""RunTable: every listed run as one table row (`client.runs.table(...)`), W&B's `runs` DataFrame: the run's
identity, its config flattened to `config.<dot.path>` columns and its final metrics as `metric.<key>` columns
(twin: app/runs/listing)."""

from __future__ import annotations

from collections.abc import Iterator, Mapping
from dataclasses import dataclass, field
from enum import Enum
from typing import Any
from uuid import UUID

from pydantic import BaseModel

#: The columns every table starts with, in this order.
RUN_COLUMNS = ("id", "name", "status", "created_at")


@dataclass
class RunTable:
    """Typed run rows (as `client.runs.iter` yields them) and their table view. ``to_pandas()`` needs pandas,
    which probe does not depend on; ``to_records()`` is the same table as plain dicts."""

    rows: list[BaseModel] = field(default_factory=list)

    def __len__(self) -> int:
        return len(self.rows)

    def __iter__(self) -> Iterator[BaseModel]:
        return iter(self.rows)

    @property
    def columns(self) -> list[str]:
        """`id, name, status, created_at`, then every `config.<path>` and `metric.<key>` any row has, sorted."""
        records = self.to_records()
        config = sorted({key for record in records for key in record if key.startswith("config.")})
        metric = sorted({key for record in records for key in record if key.startswith("metric.")})
        return [*RUN_COLUMNS, *config, *metric]

    def to_records(self) -> list[dict[str, Any]]:
        """One flat dict per run: its identity, its config leaves and the last value of each final metric (a run
        without that metric, or a retention-locked one, has none)."""
        return [_to_record(row) for row in self.rows]

    def to_pandas(self):
        """A DataFrame, one row per run, with `columns` (a value a run lacks is NaN/None)."""
        try:
            import pandas
        except ModuleNotFoundError as exc:  # pragma: no cover - depends on the env
            raise ModuleNotFoundError(
                "to_pandas() needs pandas, which probe does not depend on. `pip install pandas`, or use "
                ".to_records() -- the same table as dicts."
            ) from exc
        return pandas.DataFrame(self.to_records(), columns=self.columns)


def _to_record(row: BaseModel) -> dict[str, Any]:
    record: dict[str, Any] = {column: _to_cell(getattr(row, column, None)) for column in RUN_COLUMNS}
    config = getattr(row, "config", None)
    if isinstance(config, Mapping):
        _flatten_config(config, "config", record)
    for key, final in (getattr(row, "latest_metrics", None) or {}).items():
        record[f"metric.{key}"] = getattr(final, "last", None)
    return record


def _flatten_config(value: Mapping[str, Any], prefix: str, into: dict[str, Any]) -> None:
    """Nested dicts become dotted columns (`config.opt.name`); a list stays one cell, as W&B's table keeps it."""
    for key, item in value.items():
        path = f"{prefix}.{key}"
        if isinstance(item, Mapping) and item:
            _flatten_config(item, path, into)
        else:
            into[path] = item


def _to_cell(value: Any) -> Any:
    # A run id and status as plain text, the way a table is filtered and joined; times stay datetimes.
    if isinstance(value, Enum):
        return value.value
    if isinstance(value, UUID):
        return str(value)
    return value
