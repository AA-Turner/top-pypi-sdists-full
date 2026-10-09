"""Unit tests for sagemaker_studio.utils.sqlutils_async_reader."""

import unittest
from unittest import mock

from sagemaker_studio.utils import sqlutils_async_reader as reader_mod
from sagemaker_studio.utils.sqlutils_async_reader import (
    _athena_coerce,
    open_result_reader,
    read_athena_result,
    read_redshift_result,
    split_first_page,
)


class InlineFirstPageSizeTest(unittest.TestCase):
    """The inline first page is capped at ONE engine fetch so displaying page 0
    is a single round-trip. Athena returns <=1000 rows INCLUDING the header echo that
    read_athena_result strips, leaving 999 data rows -- so the cap is page_size - 1."""

    def test_inline_cap_is_one_athena_fetch_minus_header(self):
        # The value must be 999: the largest a single Athena GetQueryResults (<=1000 rows
        # incl. header echo) yields as DATA rows. Asserted as a literal because the constant
        # is intentionally decoupled from _ATHENA_PAGE_SIZE (so a future Athena page-size
        # change cannot silently move the shared/Redshift inline cap) -- while still
        # confirming the number equals one Athena fetch minus the stripped header row.
        self.assertEqual(reader_mod.INLINE_FIRST_PAGE_ROWS, 999)
        self.assertEqual(reader_mod.INLINE_FIRST_PAGE_ROWS, reader_mod._ATHENA_PAGE_SIZE - 1)

    def test_one_athena_fetch_fills_inline_page_with_header_echo(self):
        # Realistic end-to-end: page 0 = 1 header echo + 999 data rows (a full 1000-row
        # GetQueryResults). split_first_page(chunks, INLINE_FIRST_PAGE_ROWS) must fill the
        # inline page from this SINGLE fetch and NOT trigger a second GetQueryResults.
        n_data = reader_mod._ATHENA_PAGE_SIZE - 1  # 999 data rows after header strip
        calls = [0]

        class _Client:
            def get_query_results(self, **kwargs):
                calls[0] += 1
                if kwargs.get("NextToken") is None:
                    # page 0: header echo row + 999 data rows == 1000-row GetQueryResults max
                    rows = [_athena_row("n")] + [_athena_row(str(i)) for i in range(n_data)]
                    return {
                        "ResultSet": {**_athena_meta(("n", "integer")), "Rows": rows},
                        "NextToken": "1",
                    }  # a second page exists but must NOT be fetched
                return {
                    "ResultSet": {**_athena_meta(("n", "integer")), "Rows": [_athena_row("9999")]}
                }

        _cols, chunks, _total = read_athena_result(_Client(), "q-inline")
        first, _remaining = split_first_page(chunks, reader_mod.INLINE_FIRST_PAGE_ROWS)
        self.assertEqual(len(first), n_data)  # inline page filled by page 0 alone (999 rows)
        self.assertEqual(calls[0], 1)  # exactly ONE GetQueryResults round-trip

    def test_split_first_page_stops_at_one_engine_page(self):
        # split_first_page consumes only the FIRST chunk when it already meets the cap; the
        # rest stays lazily in the remainder for the background thread.
        calls = [0]

        def chunks():
            for _ in range(3):
                calls[0] += 1
                yield [[i] for i in range(reader_mod.INLINE_FIRST_PAGE_ROWS)]

        first, remaining = split_first_page(chunks(), reader_mod.INLINE_FIRST_PAGE_ROWS)
        self.assertEqual(len(first), reader_mod.INLINE_FIRST_PAGE_ROWS)
        self.assertEqual(calls[0], 1)  # only ONE chunk pulled for the inline first page
        rest = [r for c in remaining for r in c]
        self.assertEqual(len(rest), 2 * reader_mod.INLINE_FIRST_PAGE_ROWS)


def _athena_row(*vals):
    return {"Data": [({"VarCharValue": v} if v is not None else {}) for v in vals]}


def _athena_meta(*cols):
    return {"ResultSetMetadata": {"ColumnInfo": [{"Name": n, "Type": t} for n, t in cols]}}


class _FakeAthenaClient:
    def __init__(self, pages):
        self.pages = pages

    def get_query_results(self, **kwargs):
        token = kwargs.get("NextToken")
        return self.pages[0 if token is None else int(token)]


class AthenaReaderTest(unittest.TestCase):
    def test_header_skip_types_and_pagination(self):
        meta = _athena_meta(("id", "integer"), ("name", "varchar"), ("ok", "boolean"))
        pages = [
            {
                "ResultSet": {
                    **meta,
                    # first data row echoes column names (skipped on page 0 only)
                    "Rows": [_athena_row("id", "name", "ok"), _athena_row("1", "alice", "true")],
                },
                "NextToken": "1",
            },
            {"ResultSet": {**meta, "Rows": [_athena_row("2", None, "false")]}},
        ]
        columns, chunks, total = read_athena_result(_FakeAthenaClient(pages), "q-1")
        self.assertEqual(columns, ["id", "name", "ok"])
        self.assertIsNone(total)  # Athena has no cheap upfront row count
        rows = [r for chunk in chunks for r in chunk]
        self.assertEqual(rows, [[1, "alice", True], [2, None, False]])

    def test_multi_page_next_token_loop_follows_all_pages(self):
        # Exercises the NextToken while-loop across THREE pages (page 0 + two follow-ups),
        # including a middle page that yields no rows (skipped) but still advances the token.
        meta = _athena_meta(("n", "integer"))
        pages = [
            {"ResultSet": {**meta, "Rows": [_athena_row("n"), _athena_row("1")]}, "NextToken": "1"},
            {"ResultSet": {**meta, "Rows": []}, "NextToken": "2"},  # empty follow-up page
            {
                "ResultSet": {**meta, "Rows": [_athena_row("2"), _athena_row("3")]}
            },  # last page, no token
        ]
        _cols, chunks, _total = read_athena_result(_FakeAthenaClient(pages), "q-2")
        rows = [r for chunk in chunks for r in chunk]
        self.assertEqual(rows, [[1], [2], [3]])  # header dropped only on page 0

    def test_converter_unavailable_keeps_raw_string(self):
        # When PyAthena's DefaultTypeConverter could not be imported, _athena_coerce
        # returns the raw string instead of coercing (graceful degradation branch).
        with mock.patch.object(reader_mod, "_ATHENA_CONVERTER", None):
            self.assertEqual(_athena_coerce("42", "bigint"), "42")
            self.assertIsNone(_athena_coerce(None, "bigint"))

    def test_empty_first_page_skips_yield(self):
        # `if first_rows:` FALSE edge: a SELECT whose only first-page row is the header
        # echo leaves zero data rows, so the first chunk must NOT be yielded; a follow-up
        # page then supplies the data.
        meta = _athena_meta(("n", "integer"))
        pages = [
            {
                "ResultSet": {**meta, "Rows": [_athena_row("n")]},
                "NextToken": "1",
            },  # header only -> empty
            {"ResultSet": {**meta, "Rows": [_athena_row("1"), _athena_row("2")]}},
        ]
        _cols, chunks, _total = read_athena_result(_FakeAthenaClient(pages), "q-3")
        rows = [r for chunk in chunks for r in chunk]
        self.assertEqual(rows, [[1], [2]])


class RedshiftReaderTest(unittest.TestCase):
    def _cols(self):
        return [{"name": "id", "typeName": "int4"}, {"name": "name", "typeName": "varchar"}]

    class _FakeRedshiftClient:
        def __init__(self, pages):
            self.pages = pages

        def get_statement_result(self, **kwargs):
            token = kwargs.get("NextToken")
            return self.pages[0 if token is None else int(token)]

    def test_column_metadata_records_and_pagination(self):
        cols = self._cols()
        pages = [
            {
                "ColumnMetadata": cols,
                "TotalNumRows": 3,
                "Records": [
                    [{"longValue": 1}, {"stringValue": "a"}],
                    [{"longValue": 2}, {"stringValue": "b"}],
                ],
                "NextToken": "1",
            },
            {"ColumnMetadata": cols, "Records": [[{"longValue": 3}, {"stringValue": "c"}]]},
        ]
        columns, chunks, total = read_redshift_result(self._FakeRedshiftClient(pages), "stmt-1")
        self.assertEqual(columns, ["id", "name"])
        self.assertEqual(total, 3)  # from GetStatementResult TotalNumRows
        rows = [r for chunk in chunks for r in chunk]
        self.assertEqual(rows, [[1, "a"], [2, "b"], [3, "c"]])

    def test_pagination_empty_middle_page_is_skipped(self):
        # Covers the `if recs:` FALSE edge: a follow-up page with no Records must be
        # skipped (yield nothing) yet still advance NextToken to the final page.
        cols = self._cols()
        pages = [
            {
                "ColumnMetadata": cols,
                "TotalNumRows": 2,
                "Records": [[{"longValue": 1}, {"stringValue": "a"}]],
                "NextToken": "1",
            },
            {
                "ColumnMetadata": cols,
                "Records": [],
                "NextToken": "2",
            },  # empty follow-up (if recs: False)
            {
                "ColumnMetadata": cols,
                "Records": [[{"longValue": 2}, {"stringValue": "b"}]],
            },  # last page
        ]
        _columns, chunks, _total = read_redshift_result(self._FakeRedshiftClient(pages), "stmt-2")
        rows = [r for chunk in chunks for r in chunk]
        self.assertEqual(rows, [[1, "a"], [2, "b"]])  # empty page contributed nothing

    def test_empty_first_page_skips_yield(self):
        # `if records:` FALSE edge on the FIRST page: an empty first page must not yield,
        # yet a follow-up page still supplies the data.
        cols = self._cols()
        pages = [
            {
                "ColumnMetadata": cols,
                "TotalNumRows": 1,
                "Records": [],
                "NextToken": "1",
            },  # empty first page
            {"ColumnMetadata": cols, "Records": [[{"longValue": 9}, {"stringValue": "z"}]]},
        ]
        _columns, chunks, _total = read_redshift_result(self._FakeRedshiftClient(pages), "stmt-3")
        rows = [r for chunk in chunks for r in chunk]
        self.assertEqual(rows, [[9, "z"]])

    def test_shared_inline_cap_no_extra_roundtrip_or_row_loss(self):
        # Redshift uses the SAME INLINE_FIRST_PAGE_ROWS (999) as Athena via
        # sqlutils._reader_factory. Redshift has no header echo, so a native first page of
        # 1000 records satisfies the 999 cap in ONE get_statement_result call, and the 1
        # overflow row + the second page must all survive in the remainder (no row loss).
        cols = self._cols()
        first_page_recs = [[{"longValue": i}, {"stringValue": f"n{i}"}] for i in range(1000)]
        second_page_recs = [[{"longValue": 1000}, {"stringValue": "n1000"}]]
        pages = [
            {
                "ColumnMetadata": cols,
                "TotalNumRows": 1001,
                "Records": first_page_recs,
                "NextToken": "1",
            },
            {"ColumnMetadata": cols, "Records": second_page_recs},
        ]

        calls = [0]

        class _CountingClient(self._FakeRedshiftClient):
            def get_statement_result(self, **kwargs):
                calls[0] += 1
                return super().get_statement_result(**kwargs)

        _columns, chunks, total = read_redshift_result(_CountingClient(pages), "stmt-rs")
        first, remaining = split_first_page(chunks, reader_mod.INLINE_FIRST_PAGE_ROWS)

        self.assertEqual(total, 1001)
        self.assertEqual(len(first), 999)  # inline page capped at 999
        self.assertEqual(calls[0], 1)  # ONE round-trip: 1000 native rows >= 999
        rest = [r for c in remaining for r in c]
        self.assertEqual(len(rest), 2)  # 1 overflow row + 1 second-page row
        self.assertEqual(calls[0], 2)  # second page fetched only when remainder drained
        # No row lost or duplicated across the split boundary.
        all_ids = [r[0] for r in first] + [r[0] for r in rest]
        self.assertEqual(all_ids, list(range(1001)))

    def test_first_page_convert_rows_slices_a_large_first_page(self):
        # first_page_convert_rows=N converts the first native page in N-sized slices, so the
        # FOREGROUND converts only the inline slice; split_first_page breaks after it, and
        # the rest of the page converts lazily as the remainder is drained. No row loss.
        cols = self._cols()
        first_page_recs = [[{"longValue": i}, {"stringValue": f"n{i}"}] for i in range(2500)]
        pages = [{"ColumnMetadata": cols, "TotalNumRows": 2500, "Records": first_page_recs}]
        _columns, chunks, total = read_redshift_result(
            self._FakeRedshiftClient(pages), "stmt-slice", first_page_convert_rows=1000
        )
        chunk_list = list(chunks)
        self.assertEqual(total, 2500)
        # 2500 rows in 1000-sized slices -> 3 chunks (1000, 1000, 500), not one 2500 chunk.
        self.assertEqual([len(c) for c in chunk_list], [1000, 1000, 500])
        rows = [r for c in chunk_list for r in c]
        self.assertEqual(len(rows), 2500)
        self.assertEqual([r[0] for r in rows], list(range(2500)))  # order + no loss

    def test_first_page_convert_rows_none_keeps_whole_page_conversion(self):
        # Default (None): the first page is converted in ONE chunk (original behavior).
        cols = self._cols()
        recs = [[{"longValue": i}, {"stringValue": f"n{i}"}] for i in range(1500)]
        pages = [{"ColumnMetadata": cols, "TotalNumRows": 1500, "Records": recs}]
        _columns, chunks, _total = read_redshift_result(
            self._FakeRedshiftClient(pages), "stmt-whole"
        )
        chunk_list = list(chunks)
        self.assertEqual([len(c) for c in chunk_list], [1500])  # single chunk, not sliced

    def test_first_page_convert_rows_larger_than_page_is_single_chunk(self):
        # When the slice size exceeds the page size, no slicing happens (one chunk).
        cols = self._cols()
        recs = [[{"longValue": i}, {"stringValue": f"n{i}"}] for i in range(200)]
        pages = [{"ColumnMetadata": cols, "TotalNumRows": 200, "Records": recs}]
        _columns, chunks, _total = read_redshift_result(
            self._FakeRedshiftClient(pages), "stmt-small", first_page_convert_rows=999
        )
        self.assertEqual([len(c) for c in chunks], [200])


class SplitFirstPageTest(unittest.TestCase):
    def test_first_page_and_overflow(self):
        def chunks():
            yield [[1], [2], [3]]
            yield [[4], [5]]

        first, remaining = split_first_page(chunks(), 2)
        self.assertEqual(first, [[1], [2]])
        self.assertEqual([r for c in remaining for r in c], [[3], [4], [5]])

    def test_small_result_fits_in_first_page(self):
        first, remaining = split_first_page(iter([[[1]]]), 10)
        self.assertEqual(first, [[1]])
        self.assertEqual(list(remaining), [])


class OpenResultReaderTest(unittest.TestCase):
    def test_unsupported_engine_raises(self):
        with self.assertRaises(ValueError):
            open_result_reader(object(), "SPARK", "id-1")

    def test_athena_builds_client_when_none_passed(self):
        # Default (athena_client=None): the reader builds its own client via the connection.
        conn = mock.Mock()
        with mock.patch.object(reader_mod, "read_athena_result") as read:
            read.return_value = (["a"], iter([]), None)
            open_result_reader(conn, "ATHENA", "q-1")
        conn.create_client.assert_called_once_with("athena")
        # The built client is the one handed to read_athena_result.
        self.assertIs(read.call_args.args[0], conn.create_client.return_value)

    def test_athena_reuses_passed_client_without_creating(self):
        # Option B: when a pre-built client is passed, the reader reuses it and does NOT
        # call connection.create_client -- so the caller can share ONE client between the
        # reader and its stats fetcher (no second Session.client() build on the daemon).
        conn = mock.Mock()
        shared = mock.Mock(name="shared-athena-client")
        with mock.patch.object(reader_mod, "read_athena_result") as read:
            read.return_value = (["a"], iter([]), None)
            open_result_reader(conn, "ATHENA", "q-1", athena_client=shared)
        conn.create_client.assert_not_called()
        self.assertIs(read.call_args.args[0], shared)

    def test_redshift_receives_first_page_convert_rows(self):
        # open_result_reader threads first_page_convert_rows to the Redshift reader.
        conn = mock.Mock()
        with mock.patch.object(reader_mod, "read_redshift_result") as read:
            read.return_value = (["a"], iter([]), None)
            open_result_reader(conn, "REDSHIFT", "sid-1", first_page_convert_rows=999)
        self.assertEqual(read.call_args.kwargs.get("first_page_convert_rows"), 999)

    def test_athena_ignores_first_page_convert_rows(self):
        # Athena's native page is already capped at 1000, so the hint is not forwarded to
        # the Athena reader (its signature does not take it).
        conn = mock.Mock()
        with mock.patch.object(reader_mod, "read_athena_result") as read:
            read.return_value = (["a"], iter([]), None)
            open_result_reader(conn, "ATHENA", "q-1", first_page_convert_rows=999)
        self.assertNotIn("first_page_convert_rows", read.call_args.kwargs)


class ReadAthenaOutputRowsTest(unittest.TestCase):
    """The Athena exact-total fetch off the background page loop."""

    def test_populated_output_rows(self):
        client = mock.Mock()
        client.get_query_runtime_statistics.return_value = {
            "QueryRuntimeStatistics": {"Rows": {"OutputRows": 1_000_000}}
        }
        self.assertEqual(reader_mod.read_athena_output_rows(client, "q-1"), 1_000_000)
        client.get_query_runtime_statistics.assert_called_once_with(QueryExecutionId="q-1")

    def test_lagging_output_rows_returns_none(self):
        client = mock.Mock()
        client.get_query_runtime_statistics.return_value = {"QueryRuntimeStatistics": {"Rows": {}}}
        self.assertIsNone(reader_mod.read_athena_output_rows(client, "q-1"))

    def test_genuine_zero_returned(self):
        client = mock.Mock()
        client.get_query_runtime_statistics.return_value = {
            "QueryRuntimeStatistics": {"Rows": {"OutputRows": 0}}
        }
        self.assertEqual(reader_mod.read_athena_output_rows(client, "q-1"), 0)

    def test_api_error_swallowed_returns_none(self):
        client = mock.Mock()
        client.get_query_runtime_statistics.side_effect = RuntimeError("throttled")
        self.assertIsNone(reader_mod.read_athena_output_rows(client, "q-1"))


if __name__ == "__main__":
    unittest.main()
