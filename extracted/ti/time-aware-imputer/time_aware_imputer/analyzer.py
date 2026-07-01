"""Gap analysis tools for time series data."""

from typing import Any, Dict, Optional, Tuple, Union

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from matplotlib.figure import Figure


class GapAnalyzer:
    """Analyze missing data patterns in time series.

    This class provides tools to understand the structure and characteristics
    of missing data gaps in time series, including duration analysis,
    frequency, and visualizations.

    Parameters
    ----------
    time_column : str, optional (default='timestamp')
        Name of the column containing timestamps.
    value_columns : list of str, optional (default=None)
        List of column names to analyze. If None, analyzes all numeric columns.

    Attributes
    ----------
    gap_stats_ : dict
        Dictionary containing gap statistics for each column.
    time_column_ : str
        Name of the time column.
    value_columns_ : list of str
        List of value columns analyzed.

    Examples
    --------
    >>> import pandas as pd
    >>> import numpy as np
    >>> from time_aware_imputer import GapAnalyzer
    >>> df = pd.DataFrame({
    ...     'timestamp': pd.date_range('2024-01-01', periods=100, freq='h'),
    ...     'value': np.random.randn(100)
    ... })
    >>> df.loc[10:15, 'value'] = np.nan
    >>> df.loc[30:32, 'value'] = np.nan
    >>> analyzer = GapAnalyzer()
    >>> stats = analyzer.analyze(df)
    >>> print(stats['value']['n_gaps'])
    2
    """

    def __init__(
        self,
        time_column: str = "timestamp",
        value_columns: Optional[list[str]] = None,
    ) -> None:
        """Initialize GapAnalyzer."""
        self.time_column = time_column
        self.value_columns = value_columns

    def analyze(self, data: pd.DataFrame) -> Dict[str, Dict[str, Any]]:
        """Analyze gaps in the time series data.

        Parameters
        ----------
        data : pd.DataFrame
            Time series data with timestamp and value columns.

        Returns
        -------
        stats : dict
            Dictionary mapping column names to their gap statistics.
            Each value is a dict containing:
            - 'n_gaps': Number of gaps
            - 'total_missing': Total number of missing values
            - 'missing_percentage': Percentage of missing values
            - 'gap_durations': List of gap durations in time units
            - 'mean_gap_duration': Mean gap duration
            - 'max_gap_duration': Maximum gap duration
            - 'min_gap_duration': Minimum gap duration
        """
        self._validate_input(data)

        # Determine value columns
        if self.value_columns is None:
            self.value_columns_ = [
                col
                for col in data.columns
                if col != self.time_column and pd.api.types.is_numeric_dtype(data[col])
            ]
        else:
            self.value_columns_ = self.value_columns

        self.gap_stats_ = {}

        for col in self.value_columns_:
            self.gap_stats_[col] = self._analyze_column(data, col)

        return self.gap_stats_

    def _analyze_column(self, data: pd.DataFrame, column: str) -> Dict[str, Any]:
        """Analyze gaps in a single column.

        Parameters
        ----------
        data : pd.DataFrame
            Time series data.
        column : str
            Column name to analyze.

        Returns
        -------
        stats : dict
            Gap statistics for the column.
        """
        missing_mask = data[column].isna()
        n_total = len(data)
        n_missing = missing_mask.sum()

        if n_missing == 0:
            return {
                "n_gaps": 0,
                "total_missing": 0,
                "missing_percentage": 0.0,
                "gap_durations": [],
                "mean_gap_duration": None,
                "max_gap_duration": None,
                "min_gap_duration": None,
            }

        # Find gap segments
        timestamps_col: pd.Series = data[self.time_column]  # type: ignore[assignment]
        if isinstance(timestamps_col, pd.DatetimeIndex):
            timestamps_col = pd.Series(
                timestamps_col.values, index=range(len(timestamps_col))
            )
        missing_mask_series: pd.Series = missing_mask  # type: ignore[assignment]
        gaps = self._find_gaps(timestamps_col, missing_mask_series)

        # Calculate gap durations
        gap_durations = [
            (end_time - start_time).total_seconds()  # type: ignore[operator]
            for start_time, end_time, _ in gaps
        ]

        return {
            "n_gaps": len(gaps),
            "total_missing": int(n_missing),  # type: ignore[arg-type]
            "missing_percentage": float(n_missing / n_total * 100),
            "gap_durations": gap_durations,
            "mean_gap_duration": (
                float(np.mean(gap_durations)) if gap_durations else None
            ),
            "max_gap_duration": float(np.max(gap_durations)) if gap_durations else None,
            "min_gap_duration": float(np.min(gap_durations)) if gap_durations else None,
            "gap_details": gaps,
        }

    def _find_gaps(
        self, timestamps: Union[pd.Series, pd.DatetimeIndex], missing_mask: pd.Series
    ) -> list[Tuple[pd.Timestamp, pd.Timestamp, int]]:
        """Find contiguous gaps in the data.

        Parameters
        ----------
        timestamps : pd.Series or pd.DatetimeIndex
            Series or Index of timestamps.
        missing_mask : pd.Series
            Boolean mask where True indicates missing value.

        Returns
        -------
        gaps : list of tuple
            List of tuples (start_time, end_time, length) for each gap.
        """
        # Convert to Series if DatetimeIndex
        if isinstance(timestamps, pd.DatetimeIndex):
            timestamps = pd.Series(timestamps.values, index=range(len(timestamps)))

        gaps: list[Tuple[pd.Timestamp, pd.Timestamp, int]] = []
        in_gap = False
        gap_start: Optional[pd.Timestamp] = None
        gap_start_idx: Optional[int] = None

        for idx, (timestamp, is_missing) in enumerate(zip(timestamps, missing_mask)):
            if is_missing and not in_gap:
                # Start of new gap
                in_gap = True
                gap_start = timestamp
                gap_start_idx = idx
            elif not is_missing and in_gap:
                # End of gap
                gap_end = timestamps.iloc[idx - 1]
                if gap_start_idx is not None and gap_start is not None:
                    gap_length = idx - gap_start_idx
                    gaps.append((gap_start, gap_end, gap_length))
                in_gap = False
                gap_start = None
                gap_start_idx = None

        # Handle case where data ends with a gap
        if in_gap and gap_start is not None and gap_start_idx is not None:
            gap_end = timestamps.iloc[-1]
            gap_length = len(timestamps) - gap_start_idx
            gaps.append((gap_start, gap_end, gap_length))

        return gaps

    def plot_gaps(
        self,
        data: pd.DataFrame,
        column: Optional[str] = None,
        figsize: Tuple[int, int] = (12, 6),
    ) -> Figure:
        """Visualize gaps in the time series data.

        Parameters
        ----------
        data : pd.DataFrame
            Time series data.
        column : str, optional (default=None)
            Column to visualize. If None, plots the first value column.
        figsize : tuple of int, optional (default=(12, 6))
            Figure size (width, height) in inches.

        Returns
        -------
        fig : matplotlib.figure.Figure
            The created figure.
        """
        if not hasattr(self, "gap_stats_"):
            self.analyze(data)

        if column is None:
            column = self.value_columns_[0]

        fig, (ax1, ax2) = plt.subplots(2, 1, figsize=figsize)

        # Plot 1: Time series with gaps highlighted
        timestamps = data[self.time_column]
        values = data[column]

        # Plot non-missing values
        mask_present = ~values.isna()
        ax1.plot(
            timestamps[mask_present],
            values[mask_present],
            "o-",
            label="Present",
            markersize=3,
        )

        # Highlight gaps
        gaps = self.gap_stats_[column]["gap_details"]
        for start_time, end_time, _ in gaps:
            ax1.axvspan(start_time, end_time, alpha=0.3, color="red")

        ax1.set_xlabel("Time")
        ax1.set_ylabel(column)
        ax1.set_title(f"Time Series with Gaps Highlighted: {column}")
        ax1.legend()
        ax1.grid(True, alpha=0.3)

        # Plot 2: Gap duration histogram
        gap_durations = self.gap_stats_[column]["gap_durations"]
        if gap_durations:
            # Convert to hours for better readability
            gap_durations_hours = [d / 3600 for d in gap_durations]
            ax2.hist(gap_durations_hours, bins=20, edgecolor="black", alpha=0.7)
            ax2.set_xlabel("Gap Duration (hours)")
            ax2.set_ylabel("Frequency")
            ax2.set_title(f"Distribution of Gap Durations: {column}")
            ax2.grid(True, alpha=0.3)
        else:
            ax2.text(
                0.5,
                0.5,
                "No gaps found",
                ha="center",
                va="center",
                transform=ax2.transAxes,
            )

        plt.tight_layout()
        return fig

    def plot_missing_heatmap(
        self, data: pd.DataFrame, figsize: Tuple[int, int] = (12, 8)
    ) -> Figure:
        """Create a heatmap showing missing data patterns.

        Parameters
        ----------
        data : pd.DataFrame
            Time series data.
        figsize : tuple of int, optional (default=(12, 8))
            Figure size (width, height) in inches.

        Returns
        -------
        fig : matplotlib.figure.Figure
            The created figure.
        """
        if not hasattr(self, "gap_stats_"):
            self.analyze(data)

        fig, ax = plt.subplots(figsize=figsize)

        # Create binary matrix (1 = missing, 0 = present)
        missing_matrix = data[self.value_columns_].isna().astype(int)

        # Plot heatmap
        im = ax.imshow(
            missing_matrix.T, aspect="auto", cmap="RdYlGn_r", interpolation="nearest"
        )

        # Set ticks
        ax.set_yticks(range(len(self.value_columns_)))
        ax.set_yticklabels(self.value_columns_)
        ax.set_xlabel("Time Index")
        ax.set_ylabel("Variables")
        ax.set_title("Missing Data Heatmap (Red = Missing, Green = Present)")

        # Add colorbar
        cbar = plt.colorbar(im, ax=ax)
        cbar.set_label("Missing")

        plt.tight_layout()
        return fig

    def get_summary(self) -> pd.DataFrame:
        """Get a summary table of gap statistics.

        Returns
        -------
        summary : pd.DataFrame
            Summary table with gap statistics for each column.

        Raises
        ------
        ValueError
            If analyze() has not been called yet.
        """
        if not hasattr(self, "gap_stats_"):
            raise ValueError("Must call analyze() before get_summary()")

        summary_data = []
        for col, stats in self.gap_stats_.items():
            summary_data.append(
                {
                    "column": col,
                    "n_gaps": stats["n_gaps"],
                    "total_missing": stats["total_missing"],
                    "missing_percentage": stats["missing_percentage"],
                    "mean_gap_duration_seconds": stats["mean_gap_duration"],
                    "max_gap_duration_seconds": stats["max_gap_duration"],
                }
            )

        return pd.DataFrame(summary_data)

    def _validate_input(self, data: pd.DataFrame) -> None:
        """Validate input data.

        Parameters
        ----------
        data : pd.DataFrame
            Input data to validate.

        Raises
        ------
        ValueError
            If input validation fails.
        """
        if not isinstance(data, pd.DataFrame):
            raise ValueError("Input must be a pandas DataFrame")

        if self.time_column not in data.columns:
            raise ValueError(f"Time column '{self.time_column}' not found in data")

        # Convert time column to datetime if needed
        if not pd.api.types.is_datetime64_any_dtype(data[self.time_column]):
            raise ValueError(f"Time column '{self.time_column}' must be datetime type")
