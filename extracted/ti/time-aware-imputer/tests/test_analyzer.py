"""Tests for GapAnalyzer."""

import numpy as np
import pandas as pd
import pytest
from matplotlib.figure import Figure

from time_aware_imputer.analyzer import GapAnalyzer


class TestGapAnalyzer:
    """Test suite for GapAnalyzer."""

    @pytest.fixture
    def sample_data_with_gaps(self) -> pd.DataFrame:
        """Create sample data with known gaps."""
        timestamps = pd.date_range("2024-01-01", periods=20, freq="h")
        values = np.ones(20)
        # Create gaps
        values[5:8] = np.nan  # 3-hour gap
        values[15:17] = np.nan  # 2-hour gap
        return pd.DataFrame({"timestamp": timestamps, "value": values})

    @pytest.fixture
    def sample_data_no_gaps(self) -> pd.DataFrame:
        """Create sample data without gaps."""
        return pd.DataFrame(
            {
                "timestamp": pd.date_range("2024-01-01", periods=10, freq="h"),
                "value": np.ones(10),
            }
        )

    @pytest.fixture
    def sample_data_multivariate(self) -> pd.DataFrame:
        """Create multivariate data with gaps."""
        timestamps = pd.date_range("2024-01-01", periods=20, freq="h")
        value1 = np.ones(20)
        value2 = np.ones(20) * 2

        value1[5:8] = np.nan
        value2[10:12] = np.nan

        return pd.DataFrame(
            {"timestamp": timestamps, "value1": value1, "value2": value2}
        )

    def test_init_default(self) -> None:
        """Test default initialization."""
        analyzer = GapAnalyzer()
        assert analyzer.time_column == "timestamp"
        assert analyzer.value_columns is None

    def test_init_custom(self) -> None:
        """Test custom initialization."""
        analyzer = GapAnalyzer(time_column="time", value_columns=["col1"])
        assert analyzer.time_column == "time"
        assert analyzer.value_columns == ["col1"]

    def test_analyze_single_column(self, sample_data_with_gaps: pd.DataFrame) -> None:
        """Test gap analysis on single column."""
        analyzer = GapAnalyzer()
        stats = analyzer.analyze(sample_data_with_gaps)

        assert "value" in stats
        assert stats["value"]["n_gaps"] == 2
        assert stats["value"]["total_missing"] == 5
        assert stats["value"]["missing_percentage"] == 25.0

    def test_analyze_no_gaps(self, sample_data_no_gaps: pd.DataFrame) -> None:
        """Test analysis on data with no gaps."""
        analyzer = GapAnalyzer()
        stats = analyzer.analyze(sample_data_no_gaps)

        assert stats["value"]["n_gaps"] == 0
        assert stats["value"]["total_missing"] == 0
        assert stats["value"]["missing_percentage"] == 0.0
        assert stats["value"]["gap_durations"] == []

    def test_analyze_multivariate(self, sample_data_multivariate: pd.DataFrame) -> None:
        """Test analysis on multiple columns."""
        analyzer = GapAnalyzer()
        stats = analyzer.analyze(sample_data_multivariate)

        assert "value1" in stats
        assert "value2" in stats

        assert stats["value1"]["n_gaps"] == 1
        assert stats["value1"]["total_missing"] == 3

        assert stats["value2"]["n_gaps"] == 1
        assert stats["value2"]["total_missing"] == 2

    def test_analyze_specific_columns(
        self, sample_data_multivariate: pd.DataFrame
    ) -> None:
        """Test analysis on specified columns only."""
        analyzer = GapAnalyzer(value_columns=["value1"])
        stats = analyzer.analyze(sample_data_multivariate)

        assert "value1" in stats
        assert "value2" not in stats

    def test_gap_durations(self, sample_data_with_gaps: pd.DataFrame) -> None:
        """Test gap duration calculation."""
        analyzer = GapAnalyzer()
        stats = analyzer.analyze(sample_data_with_gaps)

        durations = stats["value"]["gap_durations"]
        # First gap: 3 hours = 10800 seconds
        # Second gap: 2 hours = 7200 seconds
        assert len(durations) == 2
        assert durations[0] == pytest.approx(7200.0)  # 2 hours in seconds
        assert durations[1] == pytest.approx(3600.0)  # 1 hour in seconds

    def test_mean_gap_duration(self, sample_data_with_gaps: pd.DataFrame) -> None:
        """Test mean gap duration calculation."""
        analyzer = GapAnalyzer()
        stats = analyzer.analyze(sample_data_with_gaps)

        mean_duration = stats["value"]["mean_gap_duration"]
        assert mean_duration is not None
        # Mean of 7200 and 3600 is 5400
        assert mean_duration == pytest.approx(5400.0)

    def test_max_min_gap_duration(self, sample_data_with_gaps: pd.DataFrame) -> None:
        """Test max and min gap duration."""
        analyzer = GapAnalyzer()
        stats = analyzer.analyze(sample_data_with_gaps)

        assert stats["value"]["max_gap_duration"] == pytest.approx(7200.0)
        assert stats["value"]["min_gap_duration"] == pytest.approx(3600.0)

    def test_get_summary(self, sample_data_with_gaps: pd.DataFrame) -> None:
        """Test summary table generation."""
        analyzer = GapAnalyzer()
        analyzer.analyze(sample_data_with_gaps)

        summary = analyzer.get_summary()

        assert isinstance(summary, pd.DataFrame)
        assert "column" in summary.columns
        assert "n_gaps" in summary.columns
        assert "total_missing" in summary.columns
        assert "missing_percentage" in summary.columns
        assert len(summary) == 1

    def test_get_summary_before_analyze(self) -> None:
        """Test that get_summary raises error before analyze."""
        analyzer = GapAnalyzer()
        with pytest.raises(ValueError, match="Must call analyze"):
            analyzer.get_summary()

    def test_plot_gaps(self, sample_data_with_gaps: pd.DataFrame) -> None:
        """Test gap visualization."""
        analyzer = GapAnalyzer()
        analyzer.analyze(sample_data_with_gaps)

        fig = analyzer.plot_gaps(sample_data_with_gaps)

        assert fig is not None
        assert len(fig.axes) == 2  # Should have 2 subplots

    def test_plot_gaps_specific_column(
        self, sample_data_multivariate: pd.DataFrame
    ) -> None:
        """Test gap visualization for specific column."""
        analyzer = GapAnalyzer()
        analyzer.analyze(sample_data_multivariate)

        fig = analyzer.plot_gaps(sample_data_multivariate, column="value1")

        assert fig is not None

    def test_plot_missing_heatmap(self, sample_data_multivariate: pd.DataFrame) -> None:
        """Test missing data heatmap."""
        analyzer = GapAnalyzer()
        analyzer.analyze(sample_data_multivariate)

        fig = analyzer.plot_missing_heatmap(sample_data_multivariate)
        assert isinstance(fig, Figure)
        assert len(fig.axes) == 2  # Main plot + colorbar

    def test_validate_input_not_dataframe(self) -> None:
        """Test validation rejects non-DataFrame."""
        analyzer = GapAnalyzer()
        with pytest.raises(ValueError, match="must be a pandas DataFrame"):
            analyzer._validate_input([1, 2, 3])  # type: ignore

    def test_validate_input_missing_time_column(
        self, sample_data_with_gaps: pd.DataFrame
    ) -> None:
        """Test validation fails for missing time column."""
        analyzer = GapAnalyzer(time_column="missing")
        with pytest.raises(ValueError, match="not found"):
            analyzer._validate_input(sample_data_with_gaps)

    def test_validate_input_non_datetime_time_column(self) -> None:
        """Test validation fails for non-datetime time column."""
        data = pd.DataFrame({"timestamp": [1, 2, 3], "value": [1.0, 2.0, 3.0]})

        analyzer = GapAnalyzer()
        with pytest.raises(ValueError, match="must be datetime type"):
            analyzer._validate_input(data)

    def test_find_gaps_single_gap(self) -> None:
        """Test finding a single gap."""
        timestamps = pd.date_range("2024-01-01", periods=5, freq="h")
        missing_mask = pd.Series([False, False, True, False, False])

        analyzer = GapAnalyzer()
        gaps = analyzer._find_gaps(timestamps, missing_mask)

        assert len(gaps) == 1
        start_time, end_time, length = gaps[0]
        assert start_time == timestamps[2]
        assert end_time == timestamps[2]
        assert length == 1

    def test_find_gaps_multiple_gaps(self) -> None:
        """Test finding multiple gaps."""
        timestamps = pd.date_range("2024-01-01", periods=10, freq="h")
        missing_mask = pd.Series(
            [False, True, True, False, False, True, False, False, True, True]
        )

        analyzer = GapAnalyzer()
        gaps = analyzer._find_gaps(timestamps, missing_mask)

        assert len(gaps) == 3

    def test_find_gaps_at_start(self) -> None:
        """Test finding gap at start of data."""
        timestamps = pd.date_range("2024-01-01", periods=5, freq="h")
        missing_mask = pd.Series([True, True, False, False, False])

        analyzer = GapAnalyzer()
        gaps = analyzer._find_gaps(timestamps, missing_mask)

        assert len(gaps) == 1
        assert gaps[0][2] == 2  # length

    def test_find_gaps_at_end(self) -> None:
        """Test finding gap at end of data."""
        timestamps = pd.date_range("2024-01-01", periods=5, freq="h")
        missing_mask = pd.Series([False, False, False, True, True])

        analyzer = GapAnalyzer()
        gaps = analyzer._find_gaps(timestamps, missing_mask)

        assert len(gaps) == 1
        assert gaps[0][2] == 2  # length

    def test_find_gaps_no_gaps(self) -> None:
        """Test finding gaps when there are none."""
        timestamps = pd.date_range("2024-01-01", periods=5, freq="h")
        missing_mask = pd.Series([False, False, False, False, False])

        analyzer = GapAnalyzer()
        gaps = analyzer._find_gaps(timestamps, missing_mask)

        assert len(gaps) == 0

    def test_find_gaps_all_missing(self) -> None:
        """Test finding gaps when all data is missing."""
        timestamps = pd.date_range("2024-01-01", periods=5, freq="h")
        missing_mask = pd.Series([True, True, True, True, True])

        analyzer = GapAnalyzer()
        gaps = analyzer._find_gaps(timestamps, missing_mask)

        assert len(gaps) == 1
        assert gaps[0][2] == 5  # All 5 points are missing
