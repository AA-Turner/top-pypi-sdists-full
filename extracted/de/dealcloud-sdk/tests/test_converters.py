"""Tests for dealcloud_sdk.data.converters (output format conversion)."""

import sys
from types import ModuleType

import pytest
from unittest.mock import patch

try:
    import polars as pl
    HAS_POLARS = True
except ImportError:
    HAS_POLARS = False
    pl = None

from dealcloud_sdk.data.converters import (
    convert_to_output_format,
    convert_to_polars,
)


class TestConvertToOutputFormat:
    """Tests for convert_to_output_format."""

    def test_list_returns_rows_unchanged(self):
        rows = [{"a": 1}, {"a": 2}]
        assert convert_to_output_format(rows, "list") is rows
        assert convert_to_output_format([], "list") == []

    def test_pandas_empty(self):
        import pandas as pd
        result = convert_to_output_format([], "pandas")
        assert isinstance(result, pd.DataFrame)
        assert len(result) == 0

    def test_pandas_with_rows(self):
        import pandas as pd
        rows = [{"x": 1, "y": 2}, {"x": 3, "y": 4}]
        result = convert_to_output_format(rows, "pandas")
        assert isinstance(result, pd.DataFrame)
        assert len(result) == 2
        assert list(result.columns) == ["x", "y"]

    def test_unknown_format_raises(self):
        with pytest.raises(ValueError, match="Unknown output format"):
            convert_to_output_format([], "unknown")

    def test_polars_format_delegates_without_real_polars(self):
        """Cover convert_to_output_format polars branch via patched convert_to_polars."""
        with patch(
            "dealcloud_sdk.data.converters.convert_to_polars", return_value="polars-result"
        ) as mock_cp:
            out = convert_to_output_format([{"a": 1}], "polars")
        assert out == "polars-result"
        mock_cp.assert_called_once_with([{"a": 1}], "polars")

    def test_polars_lazy_format_delegates_without_real_polars(self):
        with patch(
            "dealcloud_sdk.data.converters.convert_to_polars", return_value="lazy-result"
        ) as mock_cp:
            out = convert_to_output_format([], "polars_lazy")
        assert out == "lazy-result"
        mock_cp.assert_called_once_with([], "polars_lazy")

    @pytest.mark.skipif(not HAS_POLARS, reason="Polars not installed")
    def test_polars_via_convert_to_output_format(self):
        rows = [{"a": 1}, {"a": 2}]
        result = convert_to_output_format(rows, "polars")
        assert hasattr(result, "columns")
        assert len(result) == 2

    @pytest.mark.skipif(not HAS_POLARS, reason="Polars not installed")
    def test_polars_lazy_via_convert_to_output_format(self):
        rows = [{"a": 1}]
        result = convert_to_output_format(rows, "polars_lazy")
        assert hasattr(result, "collect")
        assert len(result.collect()) == 1


@pytest.mark.skipif(not HAS_POLARS, reason="Polars not installed")
class TestConvertToPolars:
    """Tests for convert_to_polars."""

    def test_empty_polars_dataframe(self):
        result = convert_to_polars([], "polars")
        assert isinstance(result, pl.DataFrame)
        assert len(result) == 0

    def test_empty_polars_lazyframe(self):
        result = convert_to_polars([], "polars_lazy")
        assert isinstance(result, pl.LazyFrame)
        assert len(result.collect()) == 0

    def test_polars_with_rows(self):
        rows = [{"a": 1, "b": 2}, {"a": 3, "b": 4}]
        result = convert_to_polars(rows, "polars")
        assert isinstance(result, pl.DataFrame)
        assert len(result) == 2
        assert result.columns == ["a", "b"]

    def test_polars_lazy_with_rows(self):
        rows = [{"a": 1}]
        result = convert_to_polars(rows, "polars_lazy")
        assert isinstance(result, pl.LazyFrame)
        assert len(result.collect()) == 1

    def test_convert_to_polars_import_error(self):
        """convert_to_polars raises ImportError when polars is not installed."""
        import builtins
        real_import = builtins.__import__

        def fail_polars(name, *args, **kwargs):
            if name == "polars":
                raise ImportError("No module named 'polars'")
            return real_import(name, *args, **kwargs)

        with patch("builtins.__import__", side_effect=fail_polars):
            with pytest.raises(ImportError, match="Polars is not installed"):
                convert_to_polars([], "polars")


class TestConvertToPolarsFakeModule:
    """Exercise convert_to_polars with a minimal fake polars module (no polars install)."""

    @pytest.fixture
    def fake_polars(self, monkeypatch):
        class FakeLazy:
            pass

        class FakeDataFrame:
            def __init__(self, rows=None):
                self._rows = rows if rows is not None else []

            @property
            def columns(self):
                if not self._rows:
                    return []
                return list(self._rows[0].keys())

            def __len__(self):
                return len(self._rows)

            def lazy(self):
                return FakeLazy()

        fake: ModuleType = ModuleType("polars")
        fake.DataFrame = lambda rows=None: FakeDataFrame(rows)
        fake.LazyFrame = lambda: FakeLazy()
        monkeypatch.setitem(sys.modules, "polars", fake)
        return fake

    def test_empty_dataframe_and_lazyframe_via_fake_module(self, fake_polars):
        df = convert_to_polars([], "polars")
        assert len(df) == 0
        lf = convert_to_polars([], "polars_lazy")
        assert type(lf).__name__ == "FakeLazy"

    def test_non_empty_rows_builds_dataframe_and_lazy(self, fake_polars):
        rows = [{"x": 1, "y": 2}, {"x": 3, "y": 4}]
        df = convert_to_polars(rows, "polars")
        assert len(df) == 2
        assert list(df.columns) == ["x", "y"]
        lazy = convert_to_polars(rows, "polars_lazy")
        assert type(lazy).__name__ == "FakeLazy"
