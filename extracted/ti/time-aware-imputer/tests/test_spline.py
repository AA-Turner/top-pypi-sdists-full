"""Tests for SplineImputer."""

import numpy as np
import pandas as pd
import pytest

from time_aware_imputer.spline import SplineImputer


class TestSplineImputer:
    """Test suite for SplineImputer."""

    @pytest.fixture
    def sample_data(self) -> pd.DataFrame:
        """Create sample time series data with gaps."""
        timestamps = pd.date_range("2024-01-01", periods=10, freq="h")
        values = np.array([1.0, 2.0, np.nan, 4.0, 5.0, np.nan, 7.0, 8.0, 9.0, 10.0])
        return pd.DataFrame({"timestamp": timestamps, "value": values})

    @pytest.fixture
    def sample_data_multivariate(self) -> pd.DataFrame:
        """Create multivariate time series data with gaps."""
        timestamps = pd.date_range("2024-01-01", periods=10, freq="h")
        return pd.DataFrame(
            {
                "timestamp": timestamps,
                "value1": [1.0, 2.0, np.nan, 4.0, 5.0, np.nan, 7.0, 8.0, 9.0, 10.0],
                "value2": [10.0, 9.0, 8.0, np.nan, 6.0, 5.0, np.nan, 3.0, 2.0, 1.0],
            }
        )

    def test_init_default(self) -> None:
        """Test default initialization."""
        imputer = SplineImputer()
        assert imputer.method == "cubic"
        assert imputer.fill_value == "extrapolate"
        assert imputer.bounds_error is False

    def test_init_custom_method(self) -> None:
        """Test initialization with custom method."""
        imputer = SplineImputer(method="linear")
        assert imputer.method == "linear"

    def test_fit_transform_linear(self, sample_data: pd.DataFrame) -> None:
        """Test linear interpolation."""
        imputer = SplineImputer(method="linear")
        result = imputer.fit_transform(sample_data)

        # Check that missing values are filled
        assert result["value"].isna().any() == False

        # Check that known values are preserved
        known_mask = ~sample_data["value"].isna()
        np.testing.assert_array_almost_equal(
            result.loc[known_mask, "value"].values,
            sample_data.loc[known_mask, "value"].values,
        )

        # Check linear interpolation result at index 2
        # Should be midpoint between 2.0 and 4.0
        assert abs(result.loc[2, "value"] - 3.0) < 0.01

    def test_fit_transform_cubic(self, sample_data: pd.DataFrame) -> None:
        """Test cubic spline interpolation."""
        imputer = SplineImputer(method="cubic")
        result = imputer.fit_transform(sample_data)

        # Check that missing values are filled
        assert result["value"].isna().any() == False

        # Check that known values are preserved
        known_mask = ~sample_data["value"].isna()
        np.testing.assert_array_almost_equal(
            result.loc[known_mask, "value"].values,
            sample_data.loc[known_mask, "value"].values,
        )

    def test_fit_transform_pchip(self, sample_data: pd.DataFrame) -> None:
        """Test PCHIP interpolation."""
        imputer = SplineImputer(method="pchip")
        result = imputer.fit_transform(sample_data)

        # Check that missing values are filled
        assert result["value"].isna().any() == False

        # Check that known values are preserved
        known_mask = ~sample_data["value"].isna()
        np.testing.assert_array_almost_equal(
            result.loc[known_mask, "value"].values,
            sample_data.loc[known_mask, "value"].values,
        )

    def test_fit_transform_akima(self, sample_data: pd.DataFrame) -> None:
        """Test Akima interpolation."""
        imputer = SplineImputer(method="akima")
        result = imputer.fit_transform(sample_data)

        # Check that missing values are filled
        assert result["value"].isna().any() == False

        # Check that known values are preserved
        known_mask = ~sample_data["value"].isna()
        np.testing.assert_array_almost_equal(
            result.loc[known_mask, "value"].values,
            sample_data.loc[known_mask, "value"].values,
        )

    def test_fit_transform_multivariate(
        self, sample_data_multivariate: pd.DataFrame
    ) -> None:
        """Test imputation with multiple value columns."""
        imputer = SplineImputer(method="linear")
        result = imputer.fit_transform(sample_data_multivariate)

        # Check that all missing values are filled
        assert result["value1"].isna().any() == False
        assert result["value2"].isna().any() == False

        # Check that known values are preserved
        for col in ["value1", "value2"]:
            known_mask = ~sample_data_multivariate[col].isna()
            np.testing.assert_array_almost_equal(
                result.loc[known_mask, col].values,
                sample_data_multivariate.loc[known_mask, col].values,
            )

    def test_fit_then_transform(self, sample_data: pd.DataFrame) -> None:
        """Test separate fit and transform."""
        imputer = SplineImputer(method="linear")

        # Fit on data
        imputer.fit(sample_data)
        assert hasattr(imputer, "is_fitted_")
        assert imputer.is_fitted_ is True

        # Transform data
        result = imputer.transform(sample_data)
        assert result["value"].isna().any() == False

    def test_copy_parameter(self, sample_data: pd.DataFrame) -> None:
        """Test that copy parameter works."""
        imputer = SplineImputer(method="linear", copy=False)
        original_id = id(sample_data)

        result = imputer.fit_transform(sample_data)

        # When copy=False, should modify in place
        # (though pandas may still create a copy in some cases)
        assert result["value"].isna().any() == False

    def test_get_imputed_mask(self, sample_data: pd.DataFrame) -> None:
        """Test getting imputed value mask."""
        imputer = SplineImputer(method="linear")
        imputer.fit_transform(sample_data)

        mask = imputer.get_imputed_mask()
        assert isinstance(mask, pd.DataFrame)

        # Check that mask correctly identifies originally missing values
        original_missing = sample_data["value"].isna()
        np.testing.assert_array_equal(mask["value"].values, original_missing.values)

    def test_insufficient_data(self) -> None:
        """Test behavior with insufficient data points."""
        data = pd.DataFrame(
            {
                "timestamp": pd.date_range("2024-01-01", periods=2, freq="h"),
                "value": [np.nan, np.nan],
            }
        )

        imputer = SplineImputer(method="linear")
        result = imputer.fit_transform(data)

        # Should not impute when there are no known values
        assert result["value"].isna().all() == True

    def test_single_known_point(self) -> None:
        """Test behavior with only one known data point."""
        data = pd.DataFrame(
            {
                "timestamp": pd.date_range("2024-01-01", periods=3, freq="h"),
                "value": [np.nan, 5.0, np.nan],
            }
        )

        imputer = SplineImputer(method="linear")
        result = imputer.fit_transform(data)

        # Need at least 2 points to interpolate
        # Missing values should remain NaN
        assert result["value"].isna().sum() == 2
        assert result.loc[1, "value"] == 5.0

    def test_no_missing_values(self) -> None:
        """Test behavior when there are no missing values."""
        data = pd.DataFrame(
            {
                "timestamp": pd.date_range("2024-01-01", periods=5, freq="h"),
                "value": [1.0, 2.0, 3.0, 4.0, 5.0],
            }
        )

        imputer = SplineImputer(method="linear")
        result = imputer.fit_transform(data)

        # Should return data unchanged
        pd.testing.assert_frame_equal(result, data)

    def test_irregular_timestamps(self) -> None:
        """Test with irregular time intervals."""
        data = pd.DataFrame(
            {
                "timestamp": pd.to_datetime(
                    [
                        "2024-01-01 00:00:00",
                        "2024-01-01 01:00:00",
                        "2024-01-01 03:00:00",  # 2-hour gap
                        "2024-01-01 03:30:00",  # 30-min gap
                        "2024-01-01 06:00:00",  # 2.5-hour gap
                    ]
                ),
                "value": [1.0, 2.0, np.nan, 4.0, 5.0],
            }
        )

        imputer = SplineImputer(method="linear")
        result = imputer.fit_transform(data)

        # Should handle irregular intervals
        assert result["value"].isna().any() == False

    def test_timestamps_to_numeric(self, sample_data: pd.DataFrame) -> None:
        """Test timestamp to numeric conversion."""
        imputer = SplineImputer()
        numeric = imputer._timestamps_to_numeric(sample_data["timestamp"])

        # First timestamp should be 0
        assert numeric.iloc[0] == 0

        # Should be monotonically increasing
        assert numeric.is_monotonic_increasing

        # Differences should be 3600 seconds (1 hour)
        diffs = numeric.diff().dropna()
        np.testing.assert_array_almost_equal(np.asarray(diffs), 3600.0)
