"""Tests for TimeAwareImputer base class."""

import numpy as np
import pandas as pd
import pytest

from time_aware_imputer.base import TimeAwareImputer


class TestTimeAwareImputer:
    """Test suite for TimeAwareImputer."""

    @pytest.fixture
    def sample_data(self) -> pd.DataFrame:
        """Create sample time series data."""
        return pd.DataFrame(
            {
                "timestamp": pd.date_range("2024-01-01", periods=10, freq="h"),
                "value1": [1.0, 2.0, np.nan, 4.0, 5.0, np.nan, 7.0, 8.0, 9.0, 10.0],
                "value2": [10.0, 9.0, 8.0, np.nan, 6.0, 5.0, np.nan, 3.0, 2.0, 1.0],
            }
        )

    def test_init(self) -> None:
        """Test initialization."""
        imputer = TimeAwareImputer()
        assert imputer.time_column == "timestamp"
        assert imputer.value_columns is None
        assert imputer.validate_timestamps is True
        assert imputer.copy is True

    def test_init_custom_params(self) -> None:
        """Test initialization with custom parameters."""
        imputer = TimeAwareImputer(
            time_column="time",
            value_columns=["col1", "col2"],
            validate_timestamps=False,
            copy=False,
        )
        assert imputer.time_column == "time"
        assert imputer.value_columns == ["col1", "col2"]
        assert imputer.validate_timestamps is False
        assert imputer.copy is False

    def test_validate_input_dataframe(self, sample_data: pd.DataFrame) -> None:
        """Test input validation accepts DataFrame."""
        imputer = TimeAwareImputer()
        validated = imputer._validate_input(sample_data)
        assert isinstance(validated, pd.DataFrame)

    def test_validate_input_not_dataframe(self) -> None:
        """Test input validation rejects non-DataFrame."""
        imputer = TimeAwareImputer()
        with pytest.raises(ValueError, match="Input must be a pandas DataFrame"):
            imputer._validate_input([1, 2, 3])  # type: ignore

    def test_validate_input_missing_time_column(
        self, sample_data: pd.DataFrame
    ) -> None:
        """Test validation fails when time column is missing."""
        imputer = TimeAwareImputer(time_column="missing_col")
        with pytest.raises(ValueError, match="Time column .* not found"):
            imputer._validate_input(sample_data)

    def test_validate_input_converts_datetime(self) -> None:
        """Test that string timestamps are converted to datetime."""
        data = pd.DataFrame(
            {
                "timestamp": ["2024-01-01 00:00:00", "2024-01-01 01:00:00"],
                "value": [1.0, 2.0],
            }
        )
        imputer = TimeAwareImputer()
        validated = imputer._validate_input(data)
        assert pd.api.types.is_datetime64_any_dtype(validated["timestamp"])

    def test_validate_input_sorts_timestamps(self) -> None:
        """Test that unsorted timestamps are sorted."""
        data = pd.DataFrame(
            {
                "timestamp": pd.to_datetime(
                    ["2024-01-01 02:00:00", "2024-01-01 00:00:00"]
                ),
                "value": [3.0, 1.0],
            }
        )
        imputer = TimeAwareImputer()
        with pytest.warns(UserWarning, match="not sorted"):
            validated = imputer._validate_input(data)
        assert validated["timestamp"].is_monotonic_increasing

    def test_validate_input_removes_duplicates(self) -> None:
        """Test that duplicate timestamps are removed."""
        data = pd.DataFrame(
            {
                "timestamp": pd.to_datetime(
                    [
                        "2024-01-01 00:00:00",
                        "2024-01-01 00:00:00",
                        "2024-01-01 01:00:00",
                    ]
                ),
                "value": [1.0, 2.0, 3.0],
            }
        )
        imputer = TimeAwareImputer()
        with pytest.warns(UserWarning, match="Duplicate timestamps"):
            validated = imputer._validate_input(data)
        assert len(validated) == 2

    def test_fit(self, sample_data: pd.DataFrame) -> None:
        """Test fitting the imputer."""
        imputer = TimeAwareImputer()
        result = imputer.fit(sample_data)

        assert result is imputer
        assert hasattr(imputer, "is_fitted_")
        assert imputer.is_fitted_ is True
        assert hasattr(imputer, "feature_names_in_")
        assert hasattr(imputer, "n_features_in_")
        assert imputer.n_features_in_ == 3

    def test_fit_determines_value_columns(self, sample_data: pd.DataFrame) -> None:
        """Test that fit determines value columns when not specified."""
        imputer = TimeAwareImputer()
        imputer.fit(sample_data)
        assert "value1" in imputer.value_columns_
        assert "value2" in imputer.value_columns_
        assert "timestamp" not in imputer.value_columns_

    def test_fit_uses_specified_value_columns(self, sample_data: pd.DataFrame) -> None:
        """Test that fit uses specified value columns."""
        imputer = TimeAwareImputer(value_columns=["value1"])
        imputer.fit(sample_data)
        assert imputer.value_columns_ == ["value1"]

    def test_fit_raises_for_missing_value_columns(
        self, sample_data: pd.DataFrame
    ) -> None:
        """Test that fit raises error for non-existent value columns."""
        imputer = TimeAwareImputer(value_columns=["missing_col"])
        with pytest.raises(ValueError, match="Value columns not found"):
            imputer.fit(sample_data)

    def test_transform_not_fitted(self, sample_data: pd.DataFrame) -> None:
        """Test that transform raises error when not fitted."""
        imputer = TimeAwareImputer()
        with pytest.raises(Exception):  # sklearn raises NotFittedError
            imputer.transform(sample_data)

    def test_get_feature_names_out(self, sample_data: pd.DataFrame) -> None:
        """Test getting output feature names."""
        imputer = TimeAwareImputer()
        imputer.fit(sample_data)
        names = imputer.get_feature_names_out()
        assert names == list(sample_data.columns)

    def test_get_feature_names_out_not_fitted(self) -> None:
        """Test that get_feature_names_out raises when not fitted."""
        imputer = TimeAwareImputer()
        with pytest.raises(Exception):  # sklearn raises NotFittedError
            imputer.get_feature_names_out()
