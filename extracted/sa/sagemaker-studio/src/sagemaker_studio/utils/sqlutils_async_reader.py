"""Read a frozen query result by execution_id, independent of the originating
DB connection.

The background materialization thread uses these readers so it never holds the
SQLAlchemy connection that ran the query. Each result is retrieved with a fresh,
credential-scoped boto3 client (``Connection.create_client(...)``) keyed only by
the engine's execution id:

* Athena   -> ``athena:GetQueryResults(QueryExecutionId=...)`` (paginated)
* Redshift -> ``redshift-data:GetStatementResult(Id=...)`` (paginated)

This makes multi-statement fan-out safe (statements share no cursor/connection)
and is the same capability recovery (v2) needs to rehydrate by execution_id.

Each reader returns ``(columns, chunk_iterator, total_rows)`` where ``chunk_iterator``
yields lists of row-lists (engine-native page sizes); callers re-buffer into fixed
pages via ``sqlutils_async._rebuffer_to_pages``. ``total_rows`` is the upfront row count
when the engine exposes it cheaply (Redshift ``TotalNumRows``); it is ``None`` for
Athena (no cheap upfront count) so the UI paginates from the manifest instead.
"""

import logging
from typing import Any, Iterator, List, Optional, Tuple

logger = logging.getLogger(__name__)

# Engine-native fetch page sizes (independent of the 10k Parquet page size).
_ATHENA_PAGE_SIZE = 1000  # GetQueryResults hard max

# Cross-engine cap on the INLINE first page shown synchronously (Athena AND Redshift use
# it -- see sqlutils._reader_factory), so displaying page 0 costs ONE engine round-trip
# regardless of the larger S3 ROWS_PER_PAGE the background thread re-buffers to. This is a
# threshold for split_first_page, not a fetch size: it stops pulling engine pages once the
# buffer reaches this many rows and preserves any overflow for the remainder, so NO engine
# ever loses or re-fetches rows because of the exact value.
#
# The specific number 999 is the largest value a single Athena GetQueryResults fetch can
# satisfy: that call returns at most _ATHENA_PAGE_SIZE (1000) rows INCLUDING the
# column-label echo read_athena_result strips (rows[1:]), leaving 999 data rows on the
# first fetch. A cap of 1000 would make split_first_page see 999 < 1000 and pull a SECOND
# blocking Athena page -- defeating the single-round-trip goal. 999 is a hard ceiling here
# (Athena's MaxResults maxes at 1000, so 1000 surviving data rows is unreachable).
#
# Redshift's GetStatementResult has no header echo and its own native page size, so the
# 999-vs-1000 distinction is irrelevant to it -- 999 never costs Redshift an extra
# round-trip (the >= threshold can only break the accumulation loop one row sooner) and
# never drops rows (overflow is carried into the remainder). It is intentionally NOT
# derived from _ATHENA_PAGE_SIZE so a future change to Athena's page size cannot silently
# move Redshift's inline cap.
INLINE_FIRST_PAGE_ROWS = 999


def _load_athena_converter():
    """PyAthena's public, connection-free type converter -- the SAME conversion table its
    sync cursor uses (``DefaultTypeConverter`` wraps ``_DEFAULT_CONVERTERS``). Reusing the
    PUBLIC class (not the private dict) keeps async dtypes identical to the sync PyAthena
    path (decimal/date/time/timestamp/timestamp-with-tz incl. named zones/varbinary/json)
    and eliminates per-type parity drift, while staying on a supported API. Returns None if
    PyAthena is somehow unavailable at import; callers then leave values as strings."""
    try:
        from pyathena.converter import DefaultTypeConverter

        return DefaultTypeConverter()
    except Exception:  # pragma: no cover - availability guard
        logger.debug(
            "PyAthena DefaultTypeConverter unavailable; async keeps raw strings", exc_info=True
        )
        return None


_ATHENA_CONVERTER = _load_athena_converter()


def _athena_coerce(value: Optional[str], type_name: str) -> Any:
    """Coerce an Athena ``VarCharValue`` string to the SAME Python type the sync PyAthena
    driver yields, by delegating to PyAthena's public ``DefaultTypeConverter`` (single
    source of truth, so async == sync dtypes). The engine's ColumnInfo ``Type`` may be
    parameterized (``decimal(10,2)``, ``varchar(20)``); the converter keys on the bare
    name, so strip the ``(...)`` suffix. ``convert`` already returns the value unchanged
    (as a string) for unmapped types; any conversion error also degrades to the raw
    string -- matching PyAthena's own default-converter behavior."""
    if value is None:
        return None
    converter = _ATHENA_CONVERTER
    if converter is None:
        return value  # PyAthena converter unavailable -> leave as string
    base = (type_name or "").lower().split("(", 1)[0].strip()
    try:
        return converter.convert(base, value)
    except Exception:
        return value


def read_athena_result(
    client: Any,
    query_execution_id: str,
    page_size: int = _ATHENA_PAGE_SIZE,
    skip_header: bool = True,
) -> "Tuple[List[str], Iterator[List[List[Any]]], Optional[int]]":
    """Stream an Athena result by QueryExecutionId.

    Returns (columns, chunk_iterator, total_rows). total_rows is None -- Athena has no
    cheap upfront row count.

    ``skip_header``: Athena prepends a column-label row on the first page ONLY for
    SELECT/CTAS (DML) results; SHOW/DESCRIBE/EXPLAIN (DDL/UTILITY) return no echo. The
    caller decides this from the STATEMENT TYPE (which it knows) rather than by comparing
    row-0 values to the column names -- value comparison would wrongly drop a legitimate
    first row whose values happen to equal the column labels (e.g. ``SELECT 'id' AS id``).
    The async driver only reads result-bearing SELECT statements, so it passes True.
    """
    first = client.get_query_results(QueryExecutionId=query_execution_id, MaxResults=page_size)
    result_set = first.get("ResultSet", {})
    column_info = result_set.get("ResultSetMetadata", {}).get("ColumnInfo", [])
    columns = [c.get("Name", "") for c in column_info]
    types = [c.get("Type", "varchar") for c in column_info]

    def _rows(result_set_obj: dict, is_first_page: bool) -> List[List[Any]]:
        rows = result_set_obj.get("Rows", [])
        if is_first_page and skip_header and rows:
            rows = rows[1:]  # drop the SELECT/CTAS column-label echo (caller-confirmed type)
        out: List[List[Any]] = []
        for row in rows:
            data = row.get("Data", [])
            out.append(
                [
                    _athena_coerce(
                        cell.get("VarCharValue"), types[i] if i < len(types) else "varchar"
                    )
                    for i, cell in enumerate(data)
                ]
            )
        return out

    def _chunks() -> Iterator[List[List[Any]]]:
        first_rows = _rows(result_set, is_first_page=True)
        if first_rows:
            yield first_rows
        token = first.get("NextToken")
        while token:
            resp = client.get_query_results(
                QueryExecutionId=query_execution_id, MaxResults=page_size, NextToken=token
            )
            page_rows = _rows(resp.get("ResultSet", {}), is_first_page=False)
            if page_rows:
                yield page_rows
            token = resp.get("NextToken")

    return columns, _chunks(), None


def read_redshift_result(
    client: Any,
    statement_id: str,
) -> "Tuple[List[str], Iterator[List[List[Any]]], Optional[int]]":
    """Stream a Redshift Data API result by statement Id.

    Reuses the driver's ResultConverter for column metadata + record conversion.
    ``GetStatementResult`` returns ``TotalNumRows`` on the first page, so the upfront
    total is available for free (``None`` when the API reports it as unavailable).
    """
    from sagemaker_studio.sql_engine._sqlalchemy_redshift_data_api.dbapi.cursor import (
        ResultConverter,
    )

    first = client.get_statement_result(Id=statement_id)
    column_metadata = first.get("ColumnMetadata", [])
    columns = [desc[0] for desc in ResultConverter.convert_column_metadata(column_metadata)]
    total = first.get("TotalNumRows")
    total_rows = total if isinstance(total, int) and total >= 0 else None

    def _chunks() -> Iterator[List[List[Any]]]:
        records = first.get("Records", [])
        if records:
            yield ResultConverter.convert_records(records, column_metadata)
        token = first.get("NextToken")
        while token:
            resp = client.get_statement_result(Id=statement_id, NextToken=token)
            recs = resp.get("Records", [])
            if recs:
                yield ResultConverter.convert_records(recs, column_metadata)
            token = resp.get("NextToken")

    return columns, _chunks(), total_rows


def open_result_reader(
    connection: Any,
    connection_type: str,
    execution_id: str,
    skip_header: bool = True,
) -> "Tuple[List[str], Iterator[List[List[Any]]], Optional[int]]":
    """Build a credentialed client from the connection and stream the frozen
    result by execution_id. Returns (columns, chunk_iterator, total_rows); total_rows is
    None for Athena. Raises ValueError for unsupported engines. ``skip_header`` is the
    caller's statement-type-based decision to drop Athena's SELECT column-label echo
    (ignored for Redshift, which has no such echo)."""
    engine = (connection_type or "").upper()
    if engine == "ATHENA":
        return read_athena_result(
            connection.create_client("athena"), execution_id, skip_header=skip_header
        )
    if engine == "REDSHIFT":
        return read_redshift_result(connection.create_client("redshift-data"), execution_id)
    raise ValueError(f"Async result reader unsupported for connection type: {connection_type}")


def split_first_page(
    chunks: "Iterator[List[List[Any]]]",
    rows_per_page: int,
) -> "Tuple[List[List[Any]], Iterator[List[List[Any]]]]":
    """Pull up to ``rows_per_page`` rows off the front for the inline first page,
    returning (first_page_rows, remaining_chunk_iterator). Any overflow beyond
    rows_per_page from the last consumed chunk is prepended to the remainder.
    """
    buf: List[List[Any]] = []
    for chunk in chunks:
        buf.extend(chunk)
        if len(buf) >= rows_per_page:
            break
    first_page = buf[:rows_per_page]
    overflow = buf[rows_per_page:]

    def _remaining() -> Iterator[List[List[Any]]]:
        if overflow:
            yield overflow
        for c in chunks:
            yield c

    return first_page, _remaining()
