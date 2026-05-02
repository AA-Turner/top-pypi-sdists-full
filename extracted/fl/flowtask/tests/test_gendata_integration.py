"""Integration tests for GenData component.

Tests the full component lifecycle: loading via getComponent(),
start() -> run() pipeline, cross-join behavior, and output compatibility.
"""
import pytest
from datetime import date, timedelta

import pandas as pd

from flowtask.components import getComponent
from flowtask.components.GenData import GenData


class TestComponentLoading:
    """Test that GenData is discoverable via the component registry."""

    def test_component_loadable(self):
        """GenData is discoverable via getComponent."""
        cls = getComponent("GenData")
        assert cls is not None
        assert cls.__name__ == "GenData"

    def test_component_is_gendata_class(self):
        """getComponent returns the GenData class itself."""
        cls = getComponent("GenData")
        assert cls is GenData

    def test_component_cached(self):
        """Repeated getComponent calls return the same class object."""
        cls1 = getComponent("GenData")
        cls2 = getComponent("GenData")
        assert cls1 is cls2


class TestFullLifecycle:
    """Test the complete start() -> run() lifecycle."""

    @staticmethod
    def _make_gendata(rules, variables=None):
        """Helper to create a GenData with minimal init."""
        from unittest.mock import MagicMock
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

    @pytest.mark.asyncio
    async def test_weekly_mondays_full_lifecycle(self):
        """Realistic: every Monday from 2024-01-01 to 2026-03-20."""
        gd = self._make_gendata([
            {
                "type": "date_sequence",
                "column_name": "weekly_date",
                "firstdate": "2024-01-01",
                "lastdate": "2026-03-20",
                "interval": 7,
                "dow": 0,
            }
        ])
        start_ok = await gd.start()
        assert start_ok is True

        run_ok = await gd.run()
        assert run_ok is True

        df = gd._result
        assert isinstance(df, pd.DataFrame)
        assert "weekly_date" in df.columns

        # 2024-01-01 is already a Monday
        assert df["weekly_date"].iloc[0] == date(2024, 1, 1)
        # Last date must be <= 2026-03-20
        assert df["weekly_date"].iloc[-1] <= date(2026, 3, 20)

        # All dates must be Mondays
        for d in df["weekly_date"]:
            assert d.weekday() == 0, f"{d} is not a Monday"

        # Consecutive dates differ by exactly 7 days
        dates = df["weekly_date"].tolist()
        for i in range(1, len(dates)):
            assert dates[i] - dates[i - 1] == timedelta(days=7)

        # Approximately 116-117 weeks in this range
        assert 115 <= len(df) <= 118

    @pytest.mark.asyncio
    async def test_cross_join_two_rules(self):
        """Two rules with 4 and 3 dates produce 12 rows."""
        gd = self._make_gendata([
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

        df = gd._result
        assert len(df) == 12  # 4 * 3
        assert "col_a" in df.columns
        assert "col_b" in df.columns
        # Every col_a value should appear 3 times (for each col_b)
        assert all(df["col_a"].value_counts() == 3)
        # Every col_b value should appear 4 times (for each col_a)
        assert all(df["col_b"].value_counts() == 4)

    @pytest.mark.asyncio
    async def test_date_format_output(self):
        """date_format produces string column in the DataFrame."""
        gd = self._make_gendata([
            {
                "type": "date_sequence",
                "column_name": "formatted",
                "firstdate": "2024-01-01",
                "lastdate": "2024-01-05",
                "interval": 1,
                "date_format": "%Y-%m-%d",
            }
        ])
        await gd.start()
        await gd.run()

        df = gd._result
        assert len(df) == 5
        # All values should be strings
        assert all(isinstance(v, str) for v in df["formatted"])
        assert df["formatted"].iloc[0] == "2024-01-01"
        assert df["formatted"].iloc[-1] == "2024-01-05"

    @pytest.mark.asyncio
    async def test_variable_substitution_lifecycle(self):
        """Pipeline variables resolve through the full lifecycle."""
        gd = self._make_gendata(
            [
                {
                    "type": "date_sequence",
                    "column_name": "dates",
                    "firstdate": "{start}",
                    "lastdate": "{end}",
                    "interval": 7,
                    "dow": 0,
                }
            ],
            variables={"start": "2024-01-01", "end": "2024-02-29"},
        )
        await gd.start()
        await gd.run()

        df = gd._result
        assert len(df) > 0
        # All Mondays
        for d in df["dates"]:
            assert d.weekday() == 0

    @pytest.mark.asyncio
    async def test_same_length_rules_not_cross_joined(self):
        """Two rules producing same row count are concat'd, not cross-joined."""
        gd = self._make_gendata([
            {
                "type": "date_sequence",
                "column_name": "start_dates",
                "firstdate": "2024-01-01",
                "lastdate": "2024-01-03",
                "interval": 1,
            },
            {
                "type": "date_sequence",
                "column_name": "end_dates",
                "firstdate": "2024-12-29",
                "lastdate": "2024-12-31",
                "interval": 1,
            },
        ])
        await gd.start()
        await gd.run()

        df = gd._result
        # Same length (3 each) -> simple concat, not 9-row cross join
        assert len(df) == 3
        assert list(df.columns) == ["start_dates", "end_dates"]

    @pytest.mark.asyncio
    async def test_dow_alignment_with_non_matching_start(self):
        """dow shifts start correctly when firstdate is not the target day."""
        gd = self._make_gendata([
            {
                "type": "date_sequence",
                "column_name": "fridays",
                "firstdate": "2024-01-01",  # Monday
                "lastdate": "2024-03-31",
                "interval": 7,
                "dow": 4,  # Friday
            }
        ])
        await gd.start()
        await gd.run()

        df = gd._result
        # First Friday after 2024-01-01 is 2024-01-05
        assert df["fridays"].iloc[0] == date(2024, 1, 5)
        for d in df["fridays"]:
            assert d.weekday() == 4

    @pytest.mark.asyncio
    async def test_empty_result_for_impossible_range(self):
        """Range too short for dow alignment produces empty DataFrame."""
        gd = self._make_gendata([
            {
                "type": "date_sequence",
                "column_name": "x",
                "firstdate": "2024-01-01",  # Monday
                "lastdate": "2024-01-02",  # Tuesday
                "interval": 7,
                "dow": 5,  # Saturday — first Sat is Jan 6, out of range
            }
        ])
        await gd.start()
        await gd.run()

        df = gd._result
        assert isinstance(df, pd.DataFrame)
        assert len(df) == 0


class TestDataFrameCompatibility:
    """Test that output DataFrames work with standard pandas operations."""

    @staticmethod
    def _make_gendata(rules):
        from unittest.mock import MagicMock
        gd = object.__new__(GenData)
        gd._rules_config = []
        gd._variables = {}
        gd._logger = MagicMock()
        gd._result = None
        gd._stat = MagicMock()
        gd._stat.add_metric = MagicMock()
        gd.rules = rules
        gd.add_metric = MagicMock()
        return gd

    @pytest.mark.asyncio
    async def test_filterable(self):
        """Output DataFrame supports standard pandas filtering."""
        gd = self._make_gendata([
            {
                "type": "date_sequence",
                "column_name": "dates",
                "firstdate": "2024-01-01",
                "lastdate": "2024-12-31",
                "interval": 1,
            }
        ])
        await gd.start()
        await gd.run()

        df = gd._result
        # Filter to just February dates
        feb = df[df["dates"].apply(lambda d: d.month == 2)]
        assert len(feb) == 29  # 2024 is a leap year

    @pytest.mark.asyncio
    async def test_joinable(self):
        """Output DataFrame can be merged with another DataFrame."""
        gd = self._make_gendata([
            {
                "type": "date_sequence",
                "column_name": "report_date",
                "firstdate": "2024-01-01",
                "lastdate": "2024-01-05",
                "interval": 1,
            }
        ])
        await gd.start()
        await gd.run()

        other = pd.DataFrame({
            "report_date": [date(2024, 1, 2), date(2024, 1, 4)],
            "value": [100, 200],
        })

        merged = gd._result.merge(other, on="report_date", how="left")
        assert len(merged) == 5
        assert merged.loc[merged["report_date"] == date(2024, 1, 2), "value"].iloc[0] == 100
        assert pd.isna(merged.loc[merged["report_date"] == date(2024, 1, 1), "value"].iloc[0])
