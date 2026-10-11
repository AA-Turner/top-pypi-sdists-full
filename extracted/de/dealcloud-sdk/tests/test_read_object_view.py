"""Unit tests for read_object / read_view (batched read, error handling, output formats)."""

from unittest.mock import MagicMock, patch

import pandas as pd
import pytest

from dealcloud_sdk.data import read as read_mod
from dealcloud_sdk.data.models import BatchResult, ReferenceCache, ReferenceFormat
from dealcloud_sdk.models.schema import Field
from intapp_rest_client.models import ErrorHandling


def _dc_mock():
    dc = MagicMock()
    dc.page_size = 500
    dc.read_concurrency = 2
    dc._logger = MagicMock()
    return dc


class TestReadObject:
    @patch.object(read_mod, "read_data_streaming")
    def test_progress_callback_exception_is_logged(self, mock_stream):
        mock_stream.return_value = iter([[{"EntryId": 1, "Name": "a"}]])
        dc = _dc_mock()

        def bad_cb(cur, total):
            raise RuntimeError("no progress")

        read_mod.read_object(
            dc,
            "Company",
            output="list",
            progress_callback=bad_cb,
        )
        dc._logger.warning.assert_called()
        assert "Progress callback failed" in dc._logger.warning.call_args[0][0]

    @patch.object(read_mod, "read_data_streaming")
    def test_fail_fast_on_stream_error(self, mock_stream):
        mock_stream.side_effect = RuntimeError("network")
        dc = _dc_mock()
        with pytest.raises(RuntimeError, match="network"):
            read_mod.read_object(dc, "Company", output="list")

    @patch.object(read_mod, "read_data_streaming")
    def test_collect_mode_captures_stream_error(self, mock_stream):
        mock_stream.side_effect = ValueError("partial fail")
        dc = _dc_mock()
        out = read_mod.read_object(
            dc,
            "Company",
            output="list",
            error_handling=ErrorHandling.COLLECT,
        )
        assert isinstance(out, BatchResult)
        assert out.errors
        assert "partial fail" in out.errors[0]["error"]

    @patch.object(read_mod, "read_data_streaming")
    def test_log_only_on_stream_error(self, mock_stream):
        mock_stream.side_effect = OSError("boom")
        dc = _dc_mock()
        read_mod.read_object(
            dc,
            "Company",
            output="list",
            error_handling=ErrorHandling.LOG_ONLY,
        )
        dc._logger.error.assert_called()

    @patch.object(read_mod, "read_data_streaming")
    def test_empty_collect_returns_batch_result(self, mock_stream):
        mock_stream.return_value = iter([])
        dc = _dc_mock()
        out = read_mod.read_object(
            dc,
            "Company",
            output="list",
            error_handling=ErrorHandling.COLLECT,
        )
        assert isinstance(out, BatchResult)
        assert out.results == []

    @patch("dealcloud_sdk.data.references.apply_reference_format")
    @patch.object(read_mod, "read_data_streaming")
    def test_reference_format_name_creates_cache_when_missing(
        self, mock_stream, mock_apply
    ):
        mock_stream.return_value = iter([[{"EntryId": 1, "Ref": {"id": 9}}]])
        mock_apply.return_value = [{"EntryId": 1, "Ref": "resolved"}]
        dc = _dc_mock()
        out = read_mod.read_object(
            dc,
            "Contact",
            output="list",
            reference_format=ReferenceFormat.NAME,
            reference_cache=None,
        )
        assert out == [{"EntryId": 1, "Ref": "resolved"}]
        mock_apply.assert_called_once()
        args = mock_apply.call_args[0]
        assert args[3] == ReferenceFormat.NAME
        assert args[4] is not None

    @patch.object(read_mod, "convert_to_polars")
    @patch.object(read_mod, "read_data_streaming")
    def test_polars_output_delegates_to_convert_to_polars(
        self, mock_stream, mock_conv
    ):
        mock_stream.return_value = iter([[{"EntryId": 1}]])
        mock_conv.return_value = "POLARS_DF"
        dc = _dc_mock()
        assert read_mod.read_object(dc, "Company", output="polars") == "POLARS_DF"
        mock_conv.assert_called_once()

    @patch.object(read_mod, "convert_to_polars")
    @patch.object(read_mod, "read_data_streaming")
    def test_polars_collect_returns_batch_result(self, mock_stream, mock_conv):
        mock_stream.return_value = iter([[{"EntryId": 1}]])
        mock_conv.return_value = "LAZY"
        dc = _dc_mock()
        out = read_mod.read_object(
            dc,
            "Company",
            output="polars_lazy",
            error_handling=ErrorHandling.COLLECT,
        )
        assert isinstance(out, BatchResult)
        assert out.results == "LAZY"

    @patch.object(read_mod, "resolve_object", side_effect=lambda v, r: f"id:{v}")
    @patch.object(read_mod, "get_choice_reference_fields")
    @patch.object(read_mod, "read_data_streaming")
    def test_pandas_resolve_mutates_choice_like_columns(
        self, mock_stream, mock_fields, mock_resolve
    ):
        mock_stream.return_value = iter(
            [[{"EntryId": 10, "Status": [1, 2], "Name": "x"}]]
        )
        mock_fields.return_value = [
            Field(apiName="Status", fieldType=2, id=1, entryListId=1),
        ]
        dc = _dc_mock()
        df = read_mod.read_object(
            dc, "Company", output="pandas", resolve="id"
        )
        assert isinstance(df, pd.DataFrame)
        assert "Status" in df.columns
        row = df.iloc[0]
        assert "id:1" in str(row["Status"]) and "id:2" in str(row["Status"])

    @patch("dealcloud_sdk.data.references.apply_reference_format")
    @patch.object(read_mod, "read_data_streaming")
    def test_reference_format_name_uses_provided_cache(
        self, mock_stream, mock_apply
    ):
        """NAME + existing cache: do not allocate a default ReferenceCache."""
        mock_stream.return_value = iter([[{"EntryId": 1, "Ref": {"id": 9}}]])
        mock_apply.return_value = [{"EntryId": 1, "Ref": "x"}]
        cache = ReferenceCache(max_entries=100)
        dc = _dc_mock()
        read_mod.read_object(
            dc,
            "Contact",
            output="list",
            reference_format=ReferenceFormat.NAME,
            reference_cache=cache,
        )
        assert mock_apply.call_args[0][4] is cache

    @patch("dealcloud_sdk.data.references.apply_reference_format")
    @patch.object(read_mod, "read_data_streaming")
    def test_collect_and_reference_format_updates_batch_result(
        self, mock_stream, mock_apply
    ):
        """COLLECT + reference_format assigns transformed rows into BatchResult."""
        mock_stream.return_value = iter([[{"EntryId": 1, "R": 1}]])
        mock_apply.return_value = [{"EntryId": 1, "R": "named"}]
        dc = _dc_mock()
        out = read_mod.read_object(
            dc,
            "Company",
            output="list",
            reference_format=ReferenceFormat.ID,
            error_handling=ErrorHandling.COLLECT,
        )
        assert isinstance(out, BatchResult)
        assert out.results == [{"EntryId": 1, "R": "named"}]

    @patch.object(read_mod, "resolve_object", side_effect=lambda v, r: v)
    @patch.object(read_mod, "get_choice_reference_fields")
    @patch.object(read_mod, "read_data_streaming")
    def test_pandas_resolve_leaves_non_list_cells_unchanged(
        self, mock_stream, mock_fields, mock_resolve
    ):
        mock_stream.return_value = iter(
            [[{"EntryId": 10, "Status": "plain", "Name": "x"}]]
        )
        mock_fields.return_value = [
            Field(apiName="Status", fieldType=2, id=1, entryListId=1),
        ]
        dc = _dc_mock()
        df = read_mod.read_object(
            dc, "Company", output="pandas", resolve="id"
        )
        assert df.iloc[0]["Status"] == "plain"

    @patch.object(read_mod, "read_data_streaming")
    def test_pandas_without_entry_id_no_index(self, mock_stream):
        mock_stream.return_value = iter([[{"Name": "only"}]])
        dc = _dc_mock()
        df = read_mod.read_object(dc, "Company", output="pandas")
        assert "EntryId" not in df.columns
        assert df.index.name != "EntryId"

    @patch.object(read_mod, "read_data_streaming")
    def test_pandas_collect_returns_dataframe_in_batch_result(self, mock_stream):
        mock_stream.return_value = iter([[{"EntryId": 1, "x": "y"}]])
        dc = _dc_mock()
        out = read_mod.read_object(
            dc,
            "Company",
            output="pandas",
            error_handling=ErrorHandling.COLLECT,
        )
        assert isinstance(out, BatchResult)
        assert isinstance(out.results, pd.DataFrame)
        assert out.results.index.name == "EntryId"


class TestReadView:
    @patch.object(read_mod, "read_view_streaming")
    @patch.object(read_mod, "_validate_and_resolve_view_id", return_value=(99, False))
    def test_read_view_list_and_progress_logging(self, mock_validate, mock_vstream):
        mock_vstream.return_value = iter([[{"EntryId": 1}]])
        dc = _dc_mock()

        def bad_cb(a, b):
            raise RuntimeError("x")

        out = read_mod.read_view(
            dc,
            view_id="My View",
            output="list",
            progress_callback=bad_cb,
        )
        assert out == [{"EntryId": 1}]
        dc._logger.warning.assert_called()

    @patch.object(read_mod, "convert_to_polars")
    @patch.object(read_mod, "read_view_streaming")
    @patch.object(read_mod, "_validate_and_resolve_view_id", return_value=(5, False))
    def test_read_view_polars_collect(self, mock_validate, mock_vstream, mock_conv):
        mock_vstream.return_value = iter([[{"EntryId": 2}]])
        mock_conv.return_value = "VDF"
        dc = _dc_mock()
        out = read_mod.read_view(
            dc,
            view_id=5,
            output="polars",
            error_handling=ErrorHandling.COLLECT,
        )
        assert isinstance(out, BatchResult)
        assert out.results == "VDF"

    @patch.object(read_mod, "convert_to_polars")
    @patch.object(read_mod, "read_view_streaming")
    @patch.object(read_mod, "_validate_and_resolve_view_id", return_value=(5, False))
    def test_read_view_polars_fail_fast_returns_dataframe(
        self, mock_validate, mock_vstream, mock_conv
    ):
        mock_vstream.return_value = iter([[{"EntryId": 2}]])
        mock_conv.return_value = "POLARS_DF"
        dc = _dc_mock()
        assert read_mod.read_view(dc, view_id=5, output="polars") == "POLARS_DF"
        mock_conv.assert_called_once()

    @patch.object(read_mod, "read_view_streaming")
    @patch.object(read_mod, "_validate_and_resolve_view_id", return_value=(1, False))
    def test_read_view_fail_fast(self, mock_validate, mock_vstream):
        mock_vstream.side_effect = ConnectionError("down")
        dc = _dc_mock()
        with pytest.raises(ConnectionError):
            read_mod.read_view(dc, view_id=1, output="list")

    @patch.object(read_mod, "read_view_streaming")
    @patch.object(read_mod, "_validate_and_resolve_view_id", return_value=(1, False))
    def test_read_view_empty_pandas(self, mock_validate, mock_vstream):
        mock_vstream.return_value = iter([])
        dc = _dc_mock()
        df = read_mod.read_view(dc, view_id=1, output="pandas")
        assert isinstance(df, pd.DataFrame)
        assert len(df) == 0

    @patch.object(read_mod, "read_view_streaming")
    @patch.object(read_mod, "_validate_and_resolve_view_id", return_value=(1, False))
    def test_read_view_empty_collect_returns_batch_result(
        self, mock_validate, mock_vstream
    ):
        mock_vstream.return_value = iter([])
        dc = _dc_mock()
        out = read_mod.read_view(
            dc,
            view_id=1,
            output="list",
            error_handling=ErrorHandling.COLLECT,
        )
        assert isinstance(out, BatchResult)
        assert out.results == []

    @patch.object(read_mod, "read_view_streaming")
    @patch.object(read_mod, "_validate_and_resolve_view_id", return_value=(1, False))
    def test_read_view_collect_logs_only_on_stream_error(
        self, mock_validate, mock_vstream
    ):
        mock_vstream.side_effect = RuntimeError("stream err")
        dc = _dc_mock()
        read_mod.read_view(
            dc,
            view_id=1,
            output="list",
            error_handling=ErrorHandling.LOG_ONLY,
        )
        dc._logger.error.assert_called()

    @patch.object(read_mod, "read_view_streaming")
    @patch.object(read_mod, "_validate_and_resolve_view_id", return_value=(1, False))
    def test_read_view_collect_captures_stream_error(self, mock_validate, mock_vstream):
        mock_vstream.side_effect = ValueError("view stream")
        dc = _dc_mock()
        out = read_mod.read_view(
            dc,
            view_id=1,
            output="list",
            error_handling=ErrorHandling.COLLECT,
        )
        assert isinstance(out, BatchResult)
        assert "view stream" in out.errors[0]["error"]

    @patch.object(read_mod, "read_view_streaming")
    @patch.object(read_mod, "_validate_and_resolve_view_id", return_value=(1, False))
    def test_read_view_list_collect_with_rows(self, mock_validate, mock_vstream):
        mock_vstream.return_value = iter([[{"a": 1}, {"a": 2}]])
        dc = _dc_mock()
        out = read_mod.read_view(
            dc,
            view_id=1,
            output="list",
            error_handling=ErrorHandling.COLLECT,
        )
        assert isinstance(out, BatchResult)
        assert out.results == [{"a": 1}, {"a": 2}]

    @patch.object(read_mod, "read_view_streaming")
    @patch.object(read_mod, "_validate_and_resolve_view_id", return_value=(1, False))
    def test_read_view_pandas_without_entry_id(self, mock_validate, mock_vstream):
        mock_vstream.return_value = iter([[{"Col": "v"}]])
        dc = _dc_mock()
        df = read_mod.read_view(dc, view_id=1, output="pandas")
        assert "EntryId" not in df.columns

    @patch.object(read_mod, "read_view_streaming")
    @patch.object(read_mod, "_validate_and_resolve_view_id", return_value=(1, False))
    def test_read_view_pandas_collect_with_entry_id(self, mock_validate, mock_vstream):
        mock_vstream.return_value = iter([[{"EntryId": 99, "z": 1}]])
        dc = _dc_mock()
        out = read_mod.read_view(
            dc,
            view_id=1,
            output="pandas",
            error_handling=ErrorHandling.COLLECT,
        )
        assert isinstance(out, BatchResult)
        assert isinstance(out.results, pd.DataFrame)
        assert out.results.index.name == "EntryId"
