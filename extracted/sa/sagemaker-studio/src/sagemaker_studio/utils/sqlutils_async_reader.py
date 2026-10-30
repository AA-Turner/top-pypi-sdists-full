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

import base64
import json
import logging
from typing import Any, Iterator, List, Optional, Tuple

from sagemaker_studio.utils.athena_type_converter import convert_athena_value

logger = logging.getLogger(__name__)

# Engine-native fetch page sizes (independent of the 10k Parquet page size).
_ATHENA_PAGE_SIZE = 1000  # GetQueryResults hard max

# DEFAULT cap on the INLINE first page shown synchronously (Athena AND Redshift use it --
# see sqlutils._reader_factory), so at the default, displaying page 0 costs ONE engine
# round-trip regardless of the larger S3 ROWS_PER_PAGE the background thread re-buffers to.
# A UI-supplied first_page_rows (up to MAX_INLINE_FIRST_PAGE_ROWS) overrides this per call
# and deliberately trades extra round-trips for more inline rows -- the one-round-trip
# property holds only for this default value. This is a threshold for split_first_page, not
# a fetch size: it stops pulling engine pages once the buffer reaches this many rows and
# preserves any overflow for the remainder, so NO engine ever loses or re-fetches rows
# because of the exact value.
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

# Hard ceiling for a UI-configurable inline first page (see sqlutils._stream_with_async_materialization
# `first_page_rows`). The inline page is delivered in the kernel's SYNCHRONOUS reply and Athena's
# GetQueryResults caps at 1000 rows/call, so N inline rows costs ~N/1000 serial round-trips ON THE
# FOREGROUND before the first paint. This ceiling bounds that worst-case first-view latency (~20
# round-trips); rows beyond it are still available via the background S3 pagination. A requested value
# above this is clamped, not rejected.
MAX_INLINE_FIRST_PAGE_ROWS = 20000


def _athena_coerce(value: Optional[str], type_name: str) -> Any:
    """Convert a Row/Datum string to the Python type used by Athena result DataFrames."""
    return convert_athena_value(value, type_name)


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


def read_athena_output_rows(client: Any, query_execution_id: str) -> Optional[int]:
    """Return Athena's exact ``OutputRows`` for a query via GetQueryRuntimeStatistics,
    or None when it is not yet populated (stats lag) or unavailable.

    A lightweight control-plane metadata read by QueryExecutionId (no data scan,
    ~50-150ms), called off the background materialization page loop -- never on the
    foreground first-page path, so it adds no first-view latency. Returns ``None`` on any
    error or missing field so the caller keeps polling on the next page and ultimately
    falls back to the counted ``row_count``; distinguishing a genuine empty result
    (``OutputRows == 0``) from lag (absent) is done by the caller's ``is not None`` gate
    (see ``sqlutils_async.extract_output_rows``). ``OutputRows`` is populated for the
    Presto/Trino engine (the normal SELECT path); DDL/CTAS leave it absent -> None.
    """
    from sagemaker_studio.utils.sqlutils_async import extract_output_rows

    try:
        stats = client.get_query_runtime_statistics(QueryExecutionId=query_execution_id)
    except Exception:
        logger.debug("GetQueryRuntimeStatistics failed for %s", query_execution_id, exc_info=True)
        return None
    return extract_output_rows(stats)


_RECORDS_PASSTHROUGH_EVENT = "before-parse.redshift-data.GetStatementResult"
_RECORDS_PASSTHROUGH_ID = "sagemaker_studio.sqlutils_async_reader.records_passthrough"


def _records_passthrough(response_dict, customized_response_dict=None, **_kwargs) -> None:
    """Move GetStatementResult ``Records`` from the body to the parsed response as plain JSON."""
    if customized_response_dict is None or response_dict.get("status_code") != 200:
        return
    body = response_dict.get("body")
    if not isinstance(body, (bytes, bytearray)):
        return
    try:
        parsed = json.loads(body)
    except ValueError:
        return
    records = parsed.pop("Records", None) if isinstance(parsed, dict) else None
    if records is None:
        return
    if b'"blobValue"' in body:
        for row in records:
            for field in row:
                if "blobValue" in field:
                    field["blobValue"] = base64.b64decode(field["blobValue"])
    response_dict["body"] = json.dumps(parsed).encode("utf-8")
    customized_response_dict["Records"] = records


def enable_records_passthrough(client: Any) -> bool:
    """Register ``_records_passthrough`` on ``client``; False when the client has no event system."""
    try:
        client.meta.events.register(
            _RECORDS_PASSTHROUGH_EVENT, _records_passthrough, unique_id=_RECORDS_PASSTHROUGH_ID
        )
        return True
    except Exception:
        logger.debug(
            "Records passthrough unavailable; botocore parses GetStatementResult", exc_info=True
        )
        return False


def read_redshift_result(
    client: Any,
    statement_id: str,
    first_page_convert_rows: Optional[int] = None,
) -> "Tuple[List[str], Iterator[List[List[Any]]], Optional[int]]":
    """Stream a Redshift Data API result by statement Id.

    Reuses the driver's ResultConverter for column metadata + record conversion.
    ``GetStatementResult`` returns ``TotalNumRows`` on the first page, so the upfront
    total is available for free (``None`` when the API reports it as unavailable).

    ``first_page_convert_rows``: when set, the first native page's records are converted
    in slices of this size instead of all at once, so the foreground (which only needs the
    inline first page) converts just one slice before ``split_first_page`` breaks; the rest
    converts lazily on the background thread. Redshift's first page can be 100k+ rows, so
    converting it whole on the foreground is the dominant first-paint cost. ``None`` keeps
    the original whole-page conversion.
    """
    from sagemaker_studio.sql_engine._sqlalchemy_redshift_data_api.dbapi.cursor import (
        ResultConverter,
    )

    enable_records_passthrough(client)
    first = client.get_statement_result(Id=statement_id)
    column_metadata = first.get("ColumnMetadata", [])
    columns = [desc[0] for desc in ResultConverter.convert_column_metadata(column_metadata)]
    total = first.get("TotalNumRows")
    total_rows = total if isinstance(total, int) and total >= 0 else None

    # Redshift's first GetStatementResult page can carry a very large native page
    # (100k+ rows for a big result), whereas Athena's is capped at 1000. If we convert
    # the whole first page in one call, ``split_first_page`` receives an already-converted
    # 100k-row chunk and the FOREGROUND pays the full conversion cost before the inline
    # first page can be shown -- even though only ``first_page_convert_rows`` are displayed.
    # So convert the first page in SLICES: ``split_first_page`` breaks after the first
    # slice reaches the inline size, and the remaining raw records of this page (and every
    # later page) are converted lazily on the BACKGROUND thread as it pulls chunks.
    slice_size = (
        first_page_convert_rows if first_page_convert_rows and first_page_convert_rows > 0 else None
    )

    def _chunks() -> Iterator[List[List[Any]]]:
        records = first.get("Records", [])
        if records:
            if slice_size and len(records) > slice_size:
                # Yield the inline-sized slice first (small foreground convert), then the
                # rest of THIS page in slices consumed lazily by the background thread.
                for start in range(0, len(records), slice_size):
                    yield ResultConverter.convert_records(
                        records[start : start + slice_size], column_metadata
                    )
            else:
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
    athena_client: Any = None,
    first_page_convert_rows: Optional[int] = None,
) -> "Tuple[List[str], Iterator[List[List[Any]]], Optional[int]]":
    """Build a credentialed client from the connection and stream the frozen
    result by execution_id. Returns (columns, chunk_iterator, total_rows); total_rows is
    None for Athena. Raises ValueError for unsupported engines. ``skip_header`` is the
    caller's statement-type-based decision to drop Athena's SELECT column-label echo
    (ignored for Redshift, which has no such echo).

    ``athena_client``: an optional pre-built Athena boto3 client. When given (ATHENA only),
    it is reused instead of creating a new one, so the caller can share ONE client between
    this reader and its Athena stats fetcher rather than each calling ``create_client``
    (which is the boto3 ``Session.client()`` step exposed to the ``upload_file`` attribute-
    injection race). Defaults to None -> build internally, so existing callers are unchanged.

    ``first_page_convert_rows``: REDSHIFT-only hint (ignored for Athena, whose native page is
    already capped at 1000). When set, the first native page is converted in slices of this
    size so the foreground converts only the inline first page, not the whole 100k+ page."""
    engine = (connection_type or "").upper()
    if engine == "ATHENA":
        return read_athena_result(
            athena_client if athena_client is not None else connection.create_client("athena"),
            execution_id,
            skip_header=skip_header,
        )
    if engine == "REDSHIFT":
        return read_redshift_result(
            connection.create_client("redshift-data"),
            execution_id,
            first_page_convert_rows=first_page_convert_rows,
        )
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
