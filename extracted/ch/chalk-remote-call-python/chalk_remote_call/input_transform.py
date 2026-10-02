from __future__ import annotations

import os
from collections.abc import Sequence

import pyarrow as pa

# Columns the caller attaches as framework side channels rather than handler arguments.
# They are identified by name and are optional per request, so they must be held out of the
# positional CHALK_INPUT_ARGS mapping, which describes only the handler's declared arguments.
RESERVED_COLUMNS = frozenset({"__chalk_row_metadata__"})


def resolve_column_names(field_names: Sequence[str], arg_names: Sequence[str]) -> list[str]:
    """Map `arg_names` positionally onto the non-reserved columns of `field_names`.

    Reserved columns keep their own name and consume no entry from `arg_names`, so a request
    that carries one maps its arguments exactly as a request without one does.
    """
    positional = [name for name in field_names if name not in RESERVED_COLUMNS]
    if len(arg_names) != len(positional):
        raise ValueError(
            f"CHALK_INPUT_ARGS specifies {len(arg_names)} names but RecordBatch has {len(positional)} columns"
        )
    remaining = iter(arg_names)
    return [name if name in RESERVED_COLUMNS else next(remaining) for name in field_names]


def parse_input_args() -> list[str] | None:
    """Parse CHALK_INPUT_ARGS env var into a list of column names.

    Returns None if the env var is unset or empty.
    """
    raw = os.environ.get("CHALK_INPUT_ARGS", "").strip()
    if not raw:
        return None
    return [name.strip() for name in raw.split(",") if name.strip()]


def transform(batch: pa.RecordBatch, arg_names: list[str] | None) -> dict[str, pa.Array]:
    """Transform a RecordBatch into a dict of named arrays.

    If arg_names is provided, columns are renamed by index to the given names
    (ignoring the original column names), except for reserved columns, which keep
    their own name. If arg_names is None, the original column names are used.
    """
    if arg_names is not None:
        names = resolve_column_names(batch.schema.names, arg_names)
        return {name: batch.column(i) for i, name in enumerate(names)}
    return {batch.schema.field(i).name: batch.column(i) for i in range(batch.num_columns)}
