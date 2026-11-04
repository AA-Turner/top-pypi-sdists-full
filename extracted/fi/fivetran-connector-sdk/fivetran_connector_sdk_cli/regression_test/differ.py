"""
Compares the warehouse.db of a recording (record_end/) with the one a replay produced, table by table and row for row.

- Rows are keyed by the table's declared primary key, or by _fivetran_id when no primary key is declared.
- _fivetran_synced and _fivetran_index are never compared (non-deterministic or structural). _fivetran_id is skipped
  only when it is the row identity; otherwise it is compared like any other value column.
- Any schema difference (missing or extra table or column, column type, primary key) is reported.

Both files are attached read-only to one in-memory DuckDB, so the row comparison runs inside DuckDB instead of
pulling whole tables into Python. An SQL error on one table is reported as a finding for that table and the remaining
tables are still compared.
"""

from dataclasses import dataclass
from pathlib import Path
from typing import Any, Callable, List, Union

import duckdb

RECORD_DB_ALIAS = "record_db"
REPLAY_DB_ALIAS = "replay_db"

# Findings beyond this are counted but not kept, so a broad regression on a large table cannot exhaust memory.
MAX_REPORTED = 100

ONLY_IN_RECORD = "present in recorded data but missing during replay"
ONLY_IN_REPLAY = "present in replayed data but missing in recorded data"

_IGNORED_SCHEMAS = ("information_schema", "pg_catalog")
_EXCLUDED_VALUE_COLUMNS = ("_fivetran_synced", "_fivetran_index")
_FIVETRAN_ID = "_fivetran_id"

# Constant TRUE columns added to each side. A row unmatched on one side has NULL for all of that side's columns, so
# these tell which side a row came from even when its key is NULL.
_PRESENT_IN_RECORD = "__present_in_record"
_PRESENT_IN_REPLAY = "__present_in_replay"
_RECORD_ROW = "record_row"
_REPLAY_ROW = "replay_row"


class DiffError(Exception):
    """The two warehouse.db files could not be opened for comparison."""


@dataclass(frozen=True, order=True)
class WarehouseTable:
    schema: str
    table: str

    def quoted_name(self) -> str:
        return f"{_quote(self.schema)}.{_quote(self.table)}"

    def __str__(self) -> str:
        return f"{self.schema}.{self.table}"


@dataclass(frozen=True)
class Mismatch:
    table: WarehouseTable
    is_sql_error: bool
    detail: str

    def describe(self) -> str:
        return f"table '{self.table}': {self.detail}"


class DiffReport:
    """Counts every finding but keeps only the first MAX_REPORTED for printing."""

    def __init__(self):
        self._mismatches: List[Mismatch] = []
        self._total = 0
        self._has_sql_error = False

    def add(self, table: WarehouseTable, detail: Union[str, Callable[[], str]]) -> None:
        """Records a finding. A callable detail is only evaluated when the finding is kept."""
        self._total += 1
        if len(self._mismatches) < MAX_REPORTED:
            self._mismatches.append(Mismatch(table, False, detail() if callable(detail) else detail))

    def add_sql_error(self, table: WarehouseTable, detail: str) -> None:
        """Records a finding caused by an internal DuckDB error, not a real data difference."""
        self._total += 1
        self._has_sql_error = True
        if len(self._mismatches) < MAX_REPORTED:
            self._mismatches.append(Mismatch(table, True, detail))

    @property
    def is_empty(self) -> bool:
        return self._total == 0

    @property
    def has_sql_error(self) -> bool:
        return self._has_sql_error

    @property
    def total(self) -> int:
        """Total findings, including those not kept for printing."""
        return self._total

    @property
    def mismatches(self) -> List[Mismatch]:
        return list(self._mismatches)

    def messages(self) -> List[str]:
        """The findings as printable lines, with a trailing count when any were found."""
        if self.is_empty:
            return []
        lines = [m.describe() for m in self._mismatches]
        suffix = f" (showing first {MAX_REPORTED})" if self._total > MAX_REPORTED else ""
        lines.append(f"{self._total} mismatch(es) reported{suffix}")
        return lines


def diff_warehouses(record_db_path: Union[str, Path], replay_db_path: Union[str, Path]) -> DiffReport:
    """
    Compare two warehouse.db files.

    Raises:
        DiffError: If either file does not exist or cannot be opened.
    """
    report = DiffReport()
    with duckdb.connect(":memory:") as conn:
        try:
            _attach_read_only(conn, record_db_path, RECORD_DB_ALIAS)
            _attach_read_only(conn, replay_db_path, REPLAY_DB_ALIAS)
        except duckdb.Error as e:
            raise DiffError(f"failed to open warehouse.db files for diff: {e}") from e
        _compare_all(conn, report)
    return report


def _attach_read_only(conn, path: Union[str, Path], alias: str) -> None:
    if not Path(path).is_file():
        raise DiffError(f"warehouse.db file does not exist: {path}")
    # ATTACH has no bind parameter for the path, so escape embedded single quotes.
    escaped = str(path).replace("'", "''")
    conn.execute(f"ATTACH '{escaped}' AS {alias} (READ_ONLY)")


def _quote(identifier: str) -> str:
    return '"' + identifier.replace('"', '""') + '"'


def _list_tables(conn, alias: str) -> List[WarehouseTable]:
    # information_schema is shared by all attached databases, so filter by table_catalog.
    rows = conn.execute(
        "SELECT table_schema, table_name FROM information_schema.tables "
        "WHERE table_catalog = ? AND table_type = 'BASE TABLE'", [alias]).fetchall()
    return sorted(WarehouseTable(s, t) for s, t in rows if s not in _IGNORED_SCHEMAS)


def _column_types(conn, alias: str, table: WarehouseTable) -> dict:
    """Column name to declared SQL type, in column order."""
    rows = conn.execute(
        "SELECT column_name, data_type FROM information_schema.columns "
        "WHERE table_catalog = ? AND table_schema = ? AND table_name = ? ORDER BY ordinal_position",
        [alias, table.schema, table.table]).fetchall()
    return dict(rows)


def _primary_key(conn, alias: str, table: WarehouseTable) -> List[str]:
    """Declared primary-key columns in key order; empty if the table has no primary key."""
    row = conn.execute(
        "SELECT constraint_column_names FROM duckdb_constraints() "
        "WHERE database_name = ? AND schema_name = ? AND table_name = ? AND constraint_type = 'PRIMARY KEY'",
        [alias, table.schema, table.table]).fetchone()
    return [str(c) for c in row[0]] if row and row[0] else []


def _row_count(conn, alias: str, table: WarehouseTable) -> int:
    return conn.execute(f"SELECT COUNT(*) FROM {alias}.{table.quoted_name()}").fetchone()[0]


def _difference(items, others) -> list:
    """Items of `items` that are not in `others`, in iteration order."""
    others = set(others)
    return [i for i in items if i not in others]


def _compare_all(conn, report: DiffReport) -> None:
    record_tables = _list_tables(conn, RECORD_DB_ALIAS)
    replay_tables = _list_tables(conn, REPLAY_DB_ALIAS)

    for table in _difference(record_tables, replay_tables):
        report.add(table, ONLY_IN_RECORD)
    for table in _difference(replay_tables, record_tables):
        report.add(table, ONLY_IN_REPLAY)

    # An SQL error on one table is a finding for it rather than an abort, so mismatches already found in other
    # tables are kept.
    for table in sorted(set(record_tables) & set(replay_tables)):
        try:
            _compare_table(conn, table, report)
        except duckdb.Error as e:
            report.add_sql_error(table, f"comparison failed: {e}")


def _compare_table(conn, table: WarehouseTable, report: DiffReport) -> None:
    record_types = _column_types(conn, RECORD_DB_ALIAS, table)
    replay_types = _column_types(conn, REPLAY_DB_ALIAS, table)
    _compare_columns(table, record_types, replay_types, report)

    record_key = _primary_key(conn, RECORD_DB_ALIAS, table)
    replay_key = _primary_key(conn, REPLAY_DB_ALIAS, table)
    if record_key != replay_key:
        # A different key means rows can't be meaningfully diffed.
        report.add(table, f"primary key mismatch — record_end={record_key} replay={replay_key}")
        return

    _compare_rows(conn, table, record_types, replay_types, record_key, report)


def _compare_columns(table: WarehouseTable, record_types: dict, replay_types: dict, report: DiffReport) -> None:
    for column in _difference(record_types, replay_types):
        report.add(table, f"column '{column}' {ONLY_IN_RECORD}")
    for column in _difference(replay_types, record_types):
        report.add(table, f"column '{column}' {ONLY_IN_REPLAY}")
    for column, record_type in record_types.items():
        replay_type = replay_types.get(column)
        if replay_type is not None and record_type.lower() != replay_type.lower():
            report.add(table, f"column '{column}' type mismatch — record_end={record_type} replay={replay_type}")


def _same_type(record_types: dict, replay_types: dict, column: str) -> bool:
    return record_types[column].lower() == replay_types[column].lower()


def _compare_rows(conn, table: WarehouseTable, record_types: dict, replay_types: dict, primary_key: List[str],
                  report: DiffReport) -> None:
    # A table empty on both sides has nothing to compare. If only one side is empty, the row counts alone are the
    # mismatch.
    record_rows = _row_count(conn, RECORD_DB_ALIAS, table)
    replay_rows = _row_count(conn, REPLAY_DB_ALIAS, table)
    if record_rows == 0 and replay_rows == 0:
        return
    if record_rows == 0 or replay_rows == 0:
        report.add(table, f"row count mismatch — record_end={record_rows} replay={replay_rows}")
        return

    if primary_key:
        key_columns = primary_key
    elif _FIVETRAN_ID in record_types and _FIVETRAN_ID in replay_types:
        key_columns = [_FIVETRAN_ID]
    else:
        report.add(table, "no primary key declared and no _fivetran_id column — cannot diff rows")
        return

    # A key column whose type changed already got a type-mismatch finding, and joining on it forces an implicit cast
    # that can throw, so skip the row pass.
    if not all(_same_type(record_types, replay_types, k) for k in key_columns):
        return

    # Columns whose type mismatched are reported once above and are not comparable by value.
    value_columns = [
        c for c in record_types
        if c in replay_types and c not in _EXCLUDED_VALUE_COLUMNS and c not in key_columns
        and _same_type(record_types, replay_types, c)
    ]
    # A declared primary key is unique, but the _fivetran_id fallback may repeat; joining on a repeated key would pair
    # every copy with every other and flag identical data, so such tables are compared as multisets of whole rows.
    if not primary_key and not _keys_unique(conn, table, key_columns):
        _report_multiset_mismatches(conn, table, key_columns + value_columns, report)
        return
    _report_row_mismatches(conn, table, key_columns, value_columns, report)


def _keys_unique(conn, table: WarehouseTable, key_columns: List[str]) -> bool:
    keys = ", ".join(_quote(k) for k in key_columns)
    for alias in (RECORD_DB_ALIAS, REPLAY_DB_ALIAS):
        repeated = conn.execute(
            f"SELECT 1 FROM {alias}.{table.quoted_name()} GROUP BY {keys} HAVING COUNT(*) > 1 LIMIT 1").fetchone()
        if repeated:
            return False
    return True


def _report_multiset_mismatches(conn, table: WarehouseTable, columns: List[str], report: DiffReport) -> None:
    select = ", ".join(_quote(c) for c in columns)
    record = f"SELECT {select} FROM {RECORD_DB_ALIAS}.{table.quoted_name()}"
    replay = f"SELECT {select} FROM {REPLAY_DB_ALIAS}.{table.quoted_name()}"
    for left, right, detail in ((record, replay, ONLY_IN_RECORD), (replay, record, ONLY_IN_REPLAY)):
        cursor = conn.execute(f"{left} EXCEPT ALL {right}")
        while True:
            batch = cursor.fetchmany(1000)
            if not batch:
                break
            for row in batch:
                values = {c: _format_value(v) for c, v in zip(columns, row)}
                report.add(table, lambda v=values: f"row {v} {detail}")


def _unused_name(base: str, columns: List[str]) -> str:
    """`base`, prefixed with underscores until no column of the table has that name. DuckDB matches names case-insensitively."""
    used_columns = {c.lower() for c in columns}
    while base.lower() in used_columns:
        base = "_" + base
    return base


def _col(row_alias: str, column: str) -> str:
    return f"{row_alias}.{_quote(column)}"


def _row_comparison_sql(table: WarehouseTable, key_columns: List[str], value_columns: List[str]) -> str:
    """One FULL OUTER JOIN of both copies on the key, filtered to unmatched rows or rows whose values differ.

    Comparisons are NULL-safe, so a NULL key (possible when _fivetran_id is the fallback key) matches the same NULL
    key on the other side. Selected columns are positional: the two presence probes, one COALESCEd value per key,
    then a record/replay/verdict triple per value column.
    """
    def differs(column):
        return f"{_col(_RECORD_ROW, column)} IS DISTINCT FROM {_col(_REPLAY_ROW, column)}"

    # A warehouse column may be called like a marker, and then a reference to the marker could pick that column instead.
    used_columns = key_columns + value_columns
    present_in_record = _unused_name(_PRESENT_IN_RECORD, used_columns)
    present_in_replay = _unused_name(_PRESENT_IN_REPLAY, used_columns)

    select = [_col(_RECORD_ROW, present_in_record), _col(_REPLAY_ROW, present_in_replay)]
    select += [f"COALESCE({_col(_RECORD_ROW, k)}, {_col(_REPLAY_ROW, k)})" for k in key_columns]
    for column in value_columns:
        select += [_col(_RECORD_ROW, column), _col(_REPLAY_ROW, column), differs(column)]

    join = " AND ".join(f"{_col(_RECORD_ROW, k)} IS NOT DISTINCT FROM {_col(_REPLAY_ROW, k)}" for k in key_columns)
    where = f"{_col(_RECORD_ROW, present_in_record)} IS NULL OR {_col(_REPLAY_ROW, present_in_replay)} IS NULL"
    if value_columns:
        where += " OR (" + " OR ".join(differs(c) for c in value_columns) + ")"

    columns = ", ".join(_quote(c) for c in used_columns)

    def side(alias, marker, row_alias):
        return f"(SELECT {columns}, TRUE AS {_quote(marker)} FROM {alias}.{table.quoted_name()}) {row_alias}"

    return (f"SELECT {', '.join(select)} FROM {side(RECORD_DB_ALIAS, present_in_record, _RECORD_ROW)} "
            f"FULL OUTER JOIN {side(REPLAY_DB_ALIAS, present_in_replay, _REPLAY_ROW)} ON {join} WHERE {where}")


def _report_row_mismatches(conn, table: WarehouseTable, key_columns: List[str], value_columns: List[str],
                           report: DiffReport) -> None:
    cursor = conn.execute(_row_comparison_sql(table, key_columns, value_columns))
    # Stream the result so only the findings that are kept are ever held in memory.
    while True:
        batch = cursor.fetchmany(1000)
        if not batch:
            return
        for row in batch:
            _collect_mismatch(row, table, key_columns, value_columns, report)


def _collect_mismatch(row: tuple, table: WarehouseTable, key_columns: List[str], value_columns: List[str],
                      report: DiffReport) -> None:
    present_in_record, present_in_replay = row[0], row[1]
    key = dict(zip(key_columns, row[2:2 + len(key_columns)]))
    if present_in_replay is None:
        report.add(table, lambda: f"row {key} {ONLY_IN_RECORD}")
        return
    if present_in_record is None:
        report.add(table, lambda: f"row {key} {ONLY_IN_REPLAY}")
        return
    offset = 2 + len(key_columns)
    for i, column in enumerate(value_columns):
        recorded, replayed, differs = row[offset + 3 * i: offset + 3 * i + 3]
        if differs:
            report.add(table, lambda c=column, r=recorded, p=replayed:
                       f"row {key} column '{c}': record_end={_format_value(r)} replay={_format_value(p)}")


def _format_value(value: Any) -> str:
    if value is None:
        return "NULL"
    if isinstance(value, str):
        return f"'{value}'"
    if isinstance(value, (bytes, bytearray)):
        return f"bytes[{len(value)}]"
    return str(value)
