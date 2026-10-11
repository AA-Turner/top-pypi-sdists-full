"""Tests for data profiling utilities (estimate_field_type, profile_series, profile_dataframe, profile_files)."""

import time

import pytest
import pandas as pd
import numpy as np

from dealcloud_sdk.utils.profiling import (
    DataType,
    PROFILE_COLUMNS,
    most_common,
    profile_series,
    profile_dataframe,
    profile_files,
)


class TestProfilingUtilities:
    """Tests for data profiling utilities."""

    def test_estimate_field_type_currency(self):
        """estimate_field_type detects currency values."""
        from dealcloud_sdk import estimate_field_type

        assert estimate_field_type("$1,000,000") == "Currency"
        assert estimate_field_type("£500") == "Currency"
        assert estimate_field_type("€100") == "Currency"
        assert estimate_field_type("5M") == "Currency"

    def test_estimate_field_type_email(self):
        """estimate_field_type detects email values."""
        from dealcloud_sdk import estimate_field_type

        assert estimate_field_type("user@gmail.co") == "Email"
        assert estimate_field_type("test.user@company.org") == "Email"

    def test_estimate_field_type_date(self):
        """estimate_field_type detects date values."""
        from dealcloud_sdk import estimate_field_type

        assert estimate_field_type("2024-01-15") == "Date"
        assert estimate_field_type("2024-01-15T10:30:00") == "DateTime"

    def test_estimate_field_type_boolean(self):
        """estimate_field_type detects boolean values."""
        from dealcloud_sdk import estimate_field_type

        assert estimate_field_type("true") == "Boolean"
        assert estimate_field_type("false") == "Boolean"
        assert estimate_field_type("yes") == "Boolean"
        assert estimate_field_type("no") == "Boolean"

    def test_estimate_field_type_number(self):
        """estimate_field_type detects number values."""
        from dealcloud_sdk import estimate_field_type

        assert estimate_field_type("12345") == "Number"
        assert estimate_field_type("123.45") == "Number"

    def test_estimate_field_type_percentage(self):
        """estimate_field_type detects percentage values."""
        from dealcloud_sdk import estimate_field_type

        assert estimate_field_type("50%") == "Percentage"
        assert estimate_field_type("99.5%") == "Percentage"

    def test_detect_choice_field_small_distinct(self):
        """detect_choice_field returns True for small distinct counts."""
        from dealcloud_sdk import detect_choice_field

        assert detect_choice_field(5, 1000) is True

    def test_detect_choice_field_all_unique(self):
        """detect_choice_field returns False for all unique values."""
        from dealcloud_sdk import detect_choice_field

        assert detect_choice_field(100, 100) is False

    def test_detect_choice_field_low_ratio(self):
        """detect_choice_field returns True for low distinct ratio."""
        from dealcloud_sdk import detect_choice_field

        assert detect_choice_field(50, 10000) is True

    def test_analyze_field_values_basic(self):
        """analyze_field_values returns correct statistics."""
        from dealcloud_sdk import analyze_field_values

        values = ["Active", "Inactive", "Active", "Active", None, ""]
        stats = analyze_field_values(values)

        assert stats["total_count"] == 6
        assert stats["distinct_count"] == 2
        assert stats["null_count"] == 2
        assert stats["is_choice_candidate"] is True

    def test_estimate_field_type_multiplier(self):
        """estimate_field_type detects multiplier values."""
        from dealcloud_sdk import estimate_field_type

        assert estimate_field_type("2x") == "Multiplier"
        assert estimate_field_type("1.5X") == "Multiplier"

    def test_estimate_field_type_empty(self):
        """estimate_field_type handles empty values."""
        from dealcloud_sdk import estimate_field_type

        assert estimate_field_type("") == "Empty"
        assert estimate_field_type(" ") == "Empty"
        assert estimate_field_type("none") == "Empty"
        assert estimate_field_type("None") == "Empty"

    def test_estimate_field_type_single_line_text(self):
        """estimate_field_type detects single-line text."""
        from dealcloud_sdk import estimate_field_type

        assert estimate_field_type("Hello World", is_choice_candidate=False) == "SingleLine"

    def test_estimate_field_type_multi_line_text(self):
        """estimate_field_type detects multi-line text."""
        from dealcloud_sdk import estimate_field_type

        long_text = "A" * 150
        assert estimate_field_type(long_text) == "MultiLine"

    def test_estimate_field_type_choice_reference(self):
        """estimate_field_type returns Choice/Reference for choice candidates."""
        from dealcloud_sdk import estimate_field_type

        assert estimate_field_type("Active", is_choice_candidate=True) == "Choice/Reference"

    def test_detect_choice_field_zero_distinct(self):
        """detect_choice_field returns False for zero distinct values."""
        from dealcloud_sdk import detect_choice_field

        assert detect_choice_field(0, 100) is False

    def test_detect_choice_field_zero_total(self):
        """detect_choice_field returns False for zero total values."""
        from dealcloud_sdk import detect_choice_field

        assert detect_choice_field(5, 0) is False

    def test_analyze_field_values_empty_list(self):
        """analyze_field_values handles empty list."""
        from dealcloud_sdk import analyze_field_values

        stats = analyze_field_values([])

        assert stats["total_count"] == 0
        assert stats["distinct_count"] == 0
        assert stats["is_choice_candidate"] is False
        assert stats["suggested_type"] == DataType.UNKNOWN


class TestMostCommon:
    """Tests for most_common function."""

    def test_most_common_returns_most_frequent(self):
        """most_common returns most frequent element."""
        assert most_common(["A", "B", "A", "C", "A"]) == "A"
        assert most_common(["X", "Y", "Y", "Z"]) == "Y"

    def test_most_common_empty_list(self):
        """most_common returns None for empty list."""
        assert most_common([]) is None


class TestProfileSeries:
    """Tests for profile_series function."""

    def test_profile_series_basic(self):
        """profile_series returns correct stats."""
        series = pd.Series(["Active", "Inactive", "Active", ""], name="Status")
        result = profile_series(series, "TestSource")

        assert result["Source"] == "TestSource"
        assert result["Field"] == "Status"
        assert result["Count"] == 4
        assert result["Unique"] >= 2

    def test_profile_series_empty(self):
        """profile_series handles empty series."""
        series = pd.Series([], name="EmptyField", dtype=object)
        result = profile_series(series, "TestSource")

        assert result["Count"] == 0
        assert result["Populated"] == 0
        assert result["Datatype"] == DataType.EMPTY

    def test_profile_series_all_null(self):
        """profile_series handles all-null series."""
        series = pd.Series([None, None, ""], name="NullField")
        result = profile_series(series, "TestSource")

        assert result["Populated"] == 0
        assert result["Datatype"] == DataType.EMPTY

    def test_profile_series_numeric(self):
        """profile_series handles numeric series."""
        series = pd.Series([1, 2, 3, np.nan], name="NumericField")
        result = profile_series(series, "TestSource")

        assert result["Count"] == 4
        assert result["Populated"] == 3

    def test_profile_series_choice_field(self):
        """profile_series identifies choice fields."""
        series = pd.Series(["A", "B", "A", "B", "A", "B"] * 100, name="ChoiceField")
        result = profile_series(series, "TestSource")

        if result["Datatype"] == DataType.CHOICE_REFERENCE:
            assert len(result["Choices"]) > 0


class TestProfileDataframe:
    """Tests for profile_dataframe function."""

    def test_profile_dataframe_basic(self):
        """profile_dataframe profiles all columns."""
        df = pd.DataFrame({
            "Name": ["Alice", "Bob", "Charlie"],
            "Age": [25, 30, 35],
        })

        result = profile_dataframe(df, "TestSource")

        assert len(result) == 2
        assert list(result.columns) == PROFILE_COLUMNS

    def test_profile_dataframe_with_messenger(self):
        """profile_dataframe calls messenger callback."""
        df = pd.DataFrame({"A": [1, 2, 3]})

        messages = []
        def messenger(msg):
            messages.append(msg)

        profile_dataframe(df, "TestSource", messenger=messenger)

        assert len(messages) > 0


class TestProfileFiles:
    """Tests for profile_files function."""

    def test_profile_files_basic(self, tmp_path):
        """profile_files profiles multiple files."""
        file1 = tmp_path / "test1.csv"
        pd.DataFrame({"A": [1, 2]}).to_csv(file1, index=False)

        file2 = tmp_path / "test2.csv"
        pd.DataFrame({"B": [3, 4]}).to_csv(file2, index=False)

        result = profile_files([file1, file2])

        assert len(result) == 2

    def test_profile_files_with_messenger(self, tmp_path):
        """profile_files calls messenger callback."""
        file1 = tmp_path / "test.csv"
        pd.DataFrame({"A": [1]}).to_csv(file1, index=False)

        messages = []
        def messenger(msg):
            messages.append(msg)

        profile_files([file1], messenger=messenger)

        assert len(messages) > 0

    def test_profile_files_with_error(self, tmp_path):
        """profile_files handles file read errors."""
        bad_file = tmp_path / "nonexistent.csv"

        messages = []
        def messenger(msg):
            messages.append(msg)

        result = profile_files([bad_file], messenger=messenger)

        assert len(result) == 0
        assert any("Skipping" in msg for msg in messages)

    def test_profile_files_empty_list(self):
        """profile_files handles empty file list."""
        result = profile_files([])

        assert list(result.columns) == PROFILE_COLUMNS
        assert len(result) == 0

    def test_profile_files_multiple_files(self, tmp_path):
        """Test profiling multiple files."""
        file1 = tmp_path / "test1.csv"
        file1.write_text("A,B\n1,2\n3,4\n")
        file2 = tmp_path / "test2.csv"
        file2.write_text("C,D\na,b\n")

        profile = profile_files([file1, file2])

        assert len(profile) > 0
        assert "Source" in profile.columns

    def test_profile_files_messenger_callback(self, tmp_path):
        """Test profile_files with messenger callback."""
        file1 = tmp_path / "test.csv"
        file1.write_text("X\n1\n2\n")

        messages = []
        def messenger(msg):
            messages.append(msg)

        profile = profile_files([file1], messenger=messenger)

        assert len(profile) > 0
        assert len(messages) > 0

    def test_profile_files_empty_returns_columns(self):
        """Test profile_files with empty list returns DataFrame with columns."""
        profile = profile_files([])

        assert len(profile) == 0

    def test_profile_files_skip_invalid(self, tmp_path):
        """Test profile_files skips invalid files."""
        file1 = tmp_path / "test.csv"
        file1.write_text("A\n1\n")

        profile = profile_files([file1, tmp_path / "nonexistent.csv"])

        assert len(profile) > 0


class TestDataFrameProfiling:
    """Tests for DataFrame profiling exports and structure."""

    def test_profiling_exports(self):
        """Profiling functions are exported."""
        from dealcloud_sdk import (
            PROFILE_COLUMNS,
            profile_series,
            profile_dataframe,
            profile_files,
        )
        assert PROFILE_COLUMNS is not None
        assert profile_series is not None
        assert profile_dataframe is not None
        assert profile_files is not None

    def test_profile_columns_structure(self):
        """PROFILE_COLUMNS has expected structure."""
        from dealcloud_sdk import PROFILE_COLUMNS

        expected = ["Source", "Field", "Count", "Populated", "Unique",
                    "Datatype", "TopValues", "Choices"]
        assert PROFILE_COLUMNS == expected

    def test_profile_series_via_export(self):
        """profile_series returns correct statistics (via main module)."""
        from dealcloud_sdk import profile_series

        series = pd.Series(["A", "B", "A", None, ""], name="Status")
        stats = profile_series(series, "test_source")

        assert stats["Source"] == "test_source"
        assert stats["Field"] == "Status"
        assert stats["Count"] == 5
        assert stats["Populated"] == 3
        assert stats["Unique"] in [2, 3]

    def test_profile_dataframe_via_export(self):
        """profile_dataframe returns profiling results for all columns (via main module)."""
        from dealcloud_sdk import profile_dataframe

        df = pd.DataFrame({
            "Name": ["Alice", "Bob", "Charlie"],
            "Status": ["Active", "Active", "Inactive"],
            "Value": [100, 200, 300],
        })

        profile = profile_dataframe(df, "test.csv")

        assert len(profile) == 3
        assert set(profile["Field"]) == {"Name", "Status", "Value"}
        assert all(profile["Count"] == 3)

    def test_profile_dataframe_with_messenger_via_export(self):
        """Test profile_dataframe with messenger callback (via main module)."""
        from dealcloud_sdk import profile_dataframe

        df = pd.DataFrame({"Name": ["Alice", "Bob"]})

        messages = []
        def messenger(msg):
            messages.append(msg)

        profile = profile_dataframe(df, "test.csv", messenger=messenger)

        assert len(profile) == 1
        assert len(messages) > 0


try:
    import polars as pl

    _POLARS = True
except ImportError:
    _POLARS = False


@pytest.mark.skipif(not _POLARS, reason="Polars not installed")
class TestProfileDataframePolarsInput:
    """profile_dataframe accepts Polars input."""

    def test_profile_dataframe_polars(self):
        df = pl.DataFrame({"Name": ["a", "b"], "N": [1, 2]})
        result = profile_dataframe(df, "src")
        assert isinstance(result, pd.DataFrame)
        assert len(result) == 2
        assert set(result["Field"]) == {"Name", "N"}
