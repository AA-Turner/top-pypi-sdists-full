"""Unit tests for GenData FlowComponent."""
import pytest
from datetime import date
from unittest.mock import MagicMock

import pandas as pd

from flowtask.components.GenData import GenData
from flowtask.exceptions import ComponentError


def _make_gendata(rules: list[dict], variables: dict | None = None) -> GenData:
    """Create a GenData instance with the given rules config.

    This bypasses the full FlowComponent init chain by creating a minimal
    instance and setting the necessary attributes directly.
    """
    gd = object.__new__(GenData)
    gd._rules_config = []
    gd._variables = variables or {}
    gd._logger = MagicMock()
    gd._result = None
    gd._stat = MagicMock()
    gd._stat.add_metric = MagicMock()
    gd.rules = rules
    gd.add_metric = MagicMock()
    return gd


class TestGenDataStart:
    """Tests for GenData.start() method."""

    @pytest.mark.asyncio
    async def test_valid_rules(self):
        """start() succeeds with valid rules."""
        gd = _make_gendata([
            {
                "type": "date_sequence",
                "column_name": "dates",
                "firstdate": "2024-01-01",
                "lastdate": "2024-01-31",
                "interval": 7,
            }
        ])
        result = await gd.start()
        assert result is True
        assert len(gd._rules_config) == 1

    @pytest.mark.asyncio
    async def test_missing_rules_raises(self):
        """start() raises ComponentError when rules is missing."""
        gd = _make_gendata([])
        gd.rules = []
        with pytest.raises(ComponentError, match="rules"):
            await gd.start()

    @pytest.mark.asyncio
    async def test_no_rules_attr_raises(self):
        """start() raises ComponentError when rules attr doesn't exist."""
        gd = _make_gendata([])
        delattr(gd, "rules")
        with pytest.raises(ComponentError, match="rules"):
            await gd.start()

    @pytest.mark.asyncio
    async def test_unknown_rule_type_raises(self):
        """start() raises ComponentError for unknown rule type."""
        gd = _make_gendata([
            {"type": "nonexistent_type", "column_name": "x"}
        ])
        with pytest.raises(ComponentError, match="unknown rule type"):
            await gd.start()

    @pytest.mark.asyncio
    async def test_missing_type_field_raises(self):
        """start() raises ComponentError when rule has no type."""
        gd = _make_gendata([
            {"column_name": "x", "firstdate": "2024-01-01"}
        ])
        with pytest.raises(ComponentError, match="type"):
            await gd.start()

    @pytest.mark.asyncio
    async def test_variable_substitution(self):
        """Pipeline variables are resolved in rule values."""
        gd = _make_gendata(
            [
                {
                    "type": "date_sequence",
                    "column_name": "dates",
                    "firstdate": "{start_date}",
                    "lastdate": "{end_date}",
                    "interval": 7,
                }
            ],
            variables={
                "start_date": "2024-01-01",
                "end_date": "2024-03-31",
            },
        )
        result = await gd.start()
        assert result is True
        assert gd._rules_config[0]["firstdate"] == "2024-01-01"
        assert gd._rules_config[0]["lastdate"] == "2024-03-31"

    @pytest.mark.asyncio
    async def test_metrics_logged(self):
        """start() logs RULES_COUNT metric."""
        gd = _make_gendata([
            {
                "type": "date_sequence",
                "column_name": "dates",
                "firstdate": "2024-01-01",
                "lastdate": "2024-01-31",
            }
        ])
        await gd.start()
        gd.add_metric.assert_any_call("RULES_COUNT", 1)


class TestGenDataRun:
    """Tests for GenData.run() method."""

    @pytest.mark.asyncio
    async def test_single_rule_produces_dataframe(self):
        """Single rule produces a DataFrame with one column."""
        gd = _make_gendata([
            {
                "type": "date_sequence",
                "column_name": "daily",
                "firstdate": "2024-01-01",
                "lastdate": "2024-01-10",
                "interval": 1,
            }
        ])
        await gd.start()
        result = await gd.run()
        assert result is True
        assert isinstance(gd._result, pd.DataFrame)
        assert "daily" in gd._result.columns
        assert len(gd._result) == 10

    @pytest.mark.asyncio
    async def test_multiple_rules_same_length(self):
        """Two rules with same row count produce a multi-column DataFrame."""
        gd = _make_gendata([
            {
                "type": "date_sequence",
                "column_name": "col_a",
                "firstdate": "2024-01-01",
                "lastdate": "2024-01-05",
                "interval": 1,
            },
            {
                "type": "date_sequence",
                "column_name": "col_b",
                "firstdate": "2024-06-01",
                "lastdate": "2024-06-05",
                "interval": 1,
            },
        ])
        await gd.start()
        await gd.run()
        assert len(gd._result) == 5
        assert list(gd._result.columns) == ["col_a", "col_b"]

    @pytest.mark.asyncio
    async def test_cross_join_different_lengths(self):
        """Two rules with different row counts produce a cross-joined DataFrame."""
        gd = _make_gendata([
            {
                "type": "date_sequence",
                "column_name": "col_a",
                "firstdate": "2024-01-01",
                "lastdate": "2024-01-04",
                "interval": 1,
            },
            {
                "type": "date_sequence",
                "column_name": "col_b",
                "firstdate": "2024-06-01",
                "lastdate": "2024-06-03",
                "interval": 1,
            },
        ])
        await gd.start()
        await gd.run()
        # 4 * 3 = 12 rows
        assert len(gd._result) == 12
        assert "col_a" in gd._result.columns
        assert "col_b" in gd._result.columns

    @pytest.mark.asyncio
    async def test_output_metrics(self):
        """run() logs OUTPUT_ROWS and OUTPUT_COLUMNS metrics."""
        gd = _make_gendata([
            {
                "type": "date_sequence",
                "column_name": "dates",
                "firstdate": "2024-01-01",
                "lastdate": "2024-01-05",
                "interval": 1,
            }
        ])
        await gd.start()
        await gd.run()
        gd.add_metric.assert_any_call("OUTPUT_ROWS", 5)
        gd.add_metric.assert_any_call("OUTPUT_COLUMNS", 1)

    @pytest.mark.asyncio
    async def test_result_stored(self):
        """Result is stored in self._result."""
        gd = _make_gendata([
            {
                "type": "date_sequence",
                "column_name": "dates",
                "firstdate": "2024-01-01",
                "lastdate": "2024-01-03",
                "interval": 1,
            }
        ])
        await gd.start()
        await gd.run()
        assert gd._result is not None
        assert isinstance(gd._result, pd.DataFrame)

    @pytest.mark.asyncio
    async def test_date_format_in_output(self):
        """date_format produces string columns."""
        gd = _make_gendata([
            {
                "type": "date_sequence",
                "column_name": "formatted",
                "firstdate": "2024-01-01",
                "lastdate": "2024-01-03",
                "interval": 1,
                "date_format": "%Y-%m-%d",
            }
        ])
        await gd.start()
        await gd.run()
        assert gd._result["formatted"].iloc[0] == "2024-01-01"

    @pytest.mark.asyncio
    async def test_dow_in_full_pipeline(self):
        """dow alignment works through the full start->run pipeline."""
        gd = _make_gendata([
            {
                "type": "date_sequence",
                "column_name": "mondays",
                "firstdate": "2024-01-03",  # Wednesday
                "lastdate": "2024-03-31",
                "interval": 7,
                "dow": 0,
            }
        ])
        await gd.start()
        await gd.run()
        # First date should be 2024-01-08 (Monday)
        first_date = gd._result["mondays"].iloc[0]
        assert first_date == date(2024, 1, 8)
        # All should be Mondays
        for d in gd._result["mondays"]:
            assert d.weekday() == 0


class TestGenDataVariableResolution:
    """Tests for variable resolution in GenData."""

    def test_resolve_simple_variable(self):
        """Simple {var} substitution works."""
        gd = _make_gendata([], variables={"myvar": "hello"})
        result = gd._resolve_variables_in_value("{myvar}")
        assert result == "hello"

    def test_resolve_no_variable(self):
        """Non-template strings pass through unchanged."""
        gd = _make_gendata([], variables={})
        result = gd._resolve_variables_in_value("plain_text")
        assert result == "plain_text"

    def test_resolve_missing_variable_kept(self):
        """Missing variables are kept as-is (SafeDict behavior)."""
        gd = _make_gendata([], variables={})
        result = gd._resolve_variables_in_value("{missing}")
        assert result == "{missing}"

    def test_resolve_non_string(self):
        """Non-string values pass through unchanged."""
        gd = _make_gendata([], variables={})
        assert gd._resolve_variables_in_value(42) == 42
        assert gd._resolve_variables_in_value(None) is None

    def test_resolve_rules_list(self):
        """_resolve_variables_in_rules processes all rules."""
        gd = _make_gendata(
            [],
            variables={"start": "2024-01-01", "end": "2024-12-31"},
        )
        rules = [
            {"firstdate": "{start}", "lastdate": "{end}", "interval": 7},
            {"firstdate": "{start}", "lastdate": "{end}", "interval": 14},
        ]
        resolved = gd._resolve_variables_in_rules(rules)
        assert resolved[0]["firstdate"] == "2024-01-01"
        assert resolved[1]["lastdate"] == "2024-12-31"
        # Non-string values unchanged
        assert resolved[0]["interval"] == 7


class TestCrossJoin:
    """Tests for the cross-join assembly logic."""

    def test_empty_series_list(self):
        """Empty series list produces empty DataFrame."""
        gd = _make_gendata([])
        result = gd._assemble_dataframe([])
        assert isinstance(result, pd.DataFrame)
        assert len(result) == 0

    def test_single_series(self):
        """Single series produces a single-column DataFrame."""
        gd = _make_gendata([])
        s = pd.Series([1, 2, 3], name="col")
        result = gd._assemble_dataframe([s])
        assert list(result.columns) == ["col"]
        assert len(result) == 3

    def test_same_length_concat(self):
        """Same-length series are concatenated, not cross-joined."""
        gd = _make_gendata([])
        s1 = pd.Series(["a", "b"], name="letters")
        s2 = pd.Series([1, 2], name="numbers")
        result = gd._assemble_dataframe([s1, s2])
        assert len(result) == 2
        assert list(result.columns) == ["letters", "numbers"]

    def test_different_length_cross_join(self):
        """Different-length series are cross-joined."""
        gd = _make_gendata([])
        s1 = pd.Series(["a", "b", "c"], name="letters")
        s2 = pd.Series([1, 2], name="numbers")
        result = gd._assemble_dataframe([s1, s2])
        assert len(result) == 6  # 3 * 2
        assert set(result.columns) == {"letters", "numbers"}

    def test_three_series_cross_join(self):
        """Three series with different lengths cross-join correctly."""
        gd = _make_gendata([])
        s1 = pd.Series(["a", "b"], name="x")
        s2 = pd.Series([1, 2, 3], name="y")
        s3 = pd.Series([True, False], name="z")
        result = gd._assemble_dataframe([s1, s2, s3])
        assert len(result) == 12  # 2 * 3 * 2
