"""Unit tests for tMerge cross_func join type (FEAT-006 / TASK-013)."""
import pytest
import pandas as pd
from unittest.mock import MagicMock

from flowtask.components.tMerge import tMerge
from flowtask.exceptions import ComponentError, ConfigError


class MockComponent:
    """Minimal mock that wraps a DataFrame for tMerge.previous[n].output()."""

    def __init__(self, df: pd.DataFrame):
        self._df = df

    def output(self):
        return self._df


def _make_merge(
    df1: pd.DataFrame,
    df2: pd.DataFrame,
    **kwargs,
) -> tMerge:
    """Create a tMerge instance with cross_func type and inject DataFrames."""
    mock1 = MockComponent(df1)
    mock2 = MockComponent(df2)
    kwargs.setdefault("type", "cross_func")
    merge = tMerge(
        job=[mock1, mock2],
        depends=["left", "right"],
        **kwargs,
    )
    # Inject DataFrames directly (bypasses start() which needs full pipeline)
    merge.df1 = df1
    merge.df2 = df2
    return merge


# ── Fixtures ──────────────────────────────────────────────────────────────


@pytest.fixture
def weekly_dates_df():
    """3 weeks of Mondays."""
    return pd.DataFrame({
        "weekly_date": pd.to_datetime([
            "2025-01-06", "2025-01-13", "2025-01-20",
        ])
    })


@pytest.fixture
def employees_df():
    """Two employees: one active (open range), one terminated mid-range."""
    return pd.DataFrame({
        "employee_id": [1, 2],
        "name": ["Alice", "Bob"],
        "start_date": pd.to_datetime(["2025-01-01", "2025-01-01"]),
        "termination_date": [pd.NaT, pd.Timestamp("2025-01-15")],
    })


# ── Tests ─────────────────────────────────────────────────────────────────


class TestTMergeCrossFunc:

    @pytest.mark.asyncio
    async def test_cross_func_basic(self, weekly_dates_df, employees_df):
        """Cross join + range check produces correct boolean column."""
        merge = _make_merge(
            weekly_dates_df, employees_df,
            eval_column="weekly_date",
            range_start="start_date",
            range_end="termination_date",
        )
        result = await merge.run()

        assert "active" in result.columns
        assert result.shape[0] == 6  # 3 weeks x 2 employees

        # Alice (NaT termination) is always active
        alice = result[result["name"] == "Alice"]
        assert alice["active"].all()

        # Bob terminated 2025-01-15: active on Jan 6 and 13, not on Jan 20
        bob = result[result["name"] == "Bob"].sort_values("weekly_date")
        expected = [True, True, False]
        assert bob["active"].tolist() == expected

    @pytest.mark.asyncio
    async def test_cross_func_open_range(self, weekly_dates_df):
        """NaT in range_end treated as open-ended (always True after start)."""
        employees = pd.DataFrame({
            "employee_id": [1],
            "start_date": pd.to_datetime(["2025-01-01"]),
            "termination_date": [pd.NaT],
        })
        merge = _make_merge(
            weekly_dates_df, employees,
            eval_column="weekly_date",
            range_start="start_date",
            range_end="termination_date",
        )
        result = await merge.run()

        assert result["active"].all()

    @pytest.mark.asyncio
    async def test_cross_func_before_start(self):
        """Date before range_start returns False."""
        dates = pd.DataFrame({
            "weekly_date": pd.to_datetime(["2024-12-30"])
        })
        employees = pd.DataFrame({
            "employee_id": [1],
            "start_date": pd.to_datetime(["2025-01-01"]),
            "termination_date": pd.to_datetime(["2025-12-31"]),
        })
        merge = _make_merge(
            dates, employees,
            eval_column="weekly_date",
            range_start="start_date",
            range_end="termination_date",
        )
        result = await merge.run()

        assert not result["active"].iloc[0]

    @pytest.mark.asyncio
    async def test_cross_func_after_end(self):
        """Date after range_end returns False."""
        dates = pd.DataFrame({
            "weekly_date": pd.to_datetime(["2026-01-05"])
        })
        employees = pd.DataFrame({
            "employee_id": [1],
            "start_date": pd.to_datetime(["2025-01-01"]),
            "termination_date": pd.to_datetime(["2025-12-31"]),
        })
        merge = _make_merge(
            dates, employees,
            eval_column="weekly_date",
            range_start="start_date",
            range_end="termination_date",
        )
        result = await merge.run()

        assert not result["active"].iloc[0]

    @pytest.mark.asyncio
    async def test_cross_func_on_boundary(self):
        """Date exactly on range_start or range_end returns True (inclusive)."""
        dates = pd.DataFrame({
            "weekly_date": pd.to_datetime(["2025-01-01", "2025-12-31"])
        })
        employees = pd.DataFrame({
            "employee_id": [1],
            "start_date": pd.to_datetime(["2025-01-01"]),
            "termination_date": pd.to_datetime(["2025-12-31"]),
        })
        merge = _make_merge(
            dates, employees,
            eval_column="weekly_date",
            range_start="start_date",
            range_end="termination_date",
        )
        result = await merge.run()

        assert result["active"].all()

    @pytest.mark.asyncio
    async def test_cross_func_custom_result_column(
        self, weekly_dates_df, employees_df
    ):
        """Custom result_column name is used instead of default 'active'."""
        merge = _make_merge(
            weekly_dates_df, employees_df,
            eval_column="weekly_date",
            range_start="start_date",
            range_end="termination_date",
            result_column="is_employed",
        )
        result = await merge.run()

        assert "is_employed" in result.columns
        assert "active" not in result.columns

    @pytest.mark.asyncio
    async def test_cross_func_missing_config(self, weekly_dates_df, employees_df):
        """Missing required params raises ConfigError."""
        # Missing eval_column
        merge = _make_merge(
            weekly_dates_df, employees_df,
            eval_column=None,
            range_start="start_date",
            range_end="termination_date",
        )
        with pytest.raises(ConfigError):
            await merge.run()

        # Missing range_start
        merge2 = _make_merge(
            weekly_dates_df, employees_df,
            eval_column="weekly_date",
            range_start=None,
            range_end="termination_date",
        )
        with pytest.raises(ConfigError):
            await merge2.run()

        # Missing range_end
        merge3 = _make_merge(
            weekly_dates_df, employees_df,
            eval_column="weekly_date",
            range_start="start_date",
            range_end=None,
        )
        with pytest.raises(ConfigError):
            await merge3.run()

    @pytest.mark.asyncio
    async def test_cross_func_missing_column(self, weekly_dates_df, employees_df):
        """Column not found in DataFrame raises ComponentError."""
        merge = _make_merge(
            weekly_dates_df, employees_df,
            eval_column="nonexistent_column",
            range_start="start_date",
            range_end="termination_date",
        )
        with pytest.raises(ComponentError, match="nonexistent_column"):
            await merge.run()

    @pytest.mark.asyncio
    async def test_cross_func_string_date_coercion(self):
        """String dates are auto-coerced to datetime by pd.to_datetime."""
        dates = pd.DataFrame({"weekly_date": ["2025-01-06", "2025-01-20"]})
        employees = pd.DataFrame({
            "employee_id": [1],
            "start_date": ["2025-01-01"],
            "termination_date": ["2025-01-15"],
        })
        merge = _make_merge(
            dates, employees,
            eval_column="weekly_date",
            range_start="start_date",
            range_end="termination_date",
        )
        result = await merge.run()

        assert result.shape[0] == 2
        assert result["active"].tolist() == [True, False]
        assert pd.api.types.is_datetime64_any_dtype(result["weekly_date"])

    @pytest.mark.asyncio
    async def test_cross_func_row_count(self, weekly_dates_df, employees_df):
        """Result has len(DF1) * len(DF2) rows."""
        merge = _make_merge(
            weekly_dates_df, employees_df,
            eval_column="weekly_date",
            range_start="start_date",
            range_end="termination_date",
        )
        result = await merge.run()

        expected_rows = len(weekly_dates_df) * len(employees_df)
        assert result.shape[0] == expected_rows

    @pytest.mark.asyncio
    async def test_cross_func_metrics(self, weekly_dates_df, employees_df):
        """ACTIVE_COUNT and INACTIVE_COUNT metrics sum to total rows."""
        stat_mock = MagicMock()
        merge = _make_merge(
            weekly_dates_df, employees_df,
            eval_column="weekly_date",
            range_start="start_date",
            range_end="termination_date",
            stat=stat_mock,
        )
        result = await merge.run()

        # Collect all add_metric calls
        calls = {
            call.args[0]: call.args[1]
            for call in stat_mock.add_metric.call_args_list
        }
        assert calls["NUM_ROWS"] == 6
        assert calls["ACTIVE_COUNT"] + calls["INACTIVE_COUNT"] == 6
        assert calls["ACTIVE_COUNT"] == 5  # Alice 3x + Bob 2x
        assert calls["INACTIVE_COUNT"] == 1  # Bob Jan 20
