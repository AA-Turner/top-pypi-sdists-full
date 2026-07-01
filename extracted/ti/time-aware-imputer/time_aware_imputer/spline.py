"""Spline-based time-aware imputation."""

from typing import Any, Literal, Optional, Union

import numpy as np
import pandas as pd
from scipy import interpolate

from time_aware_imputer.base import TimeAwareImputer


class SplineImputer(TimeAwareImputer):
    """Time-aware imputation using spline interpolation.

    This imputer uses various spline interpolation methods to fill missing
    values in time series data. It respects the temporal structure of the
    data by using actual timestamps rather than sequential indices.

    Parameters
    ----------
    method : {'linear', 'cubic', 'quadratic', 'slinear', 'pchip', 'akima'}, \
            optional (default='cubic')
        Interpolation method to use:
        - 'linear': Linear interpolation
        - 'cubic': Cubic spline interpolation
        - 'quadratic': Quadratic interpolation
        - 'slinear': First-order spline (same as linear)
        - 'pchip': Piecewise Cubic Hermite Interpolating Polynomial
        - 'akima': Akima spline interpolation
    fill_value : {'extrapolate', float}, optional (default='extrapolate')
        How to handle values outside the interpolation range.
        If 'extrapolate', extrapolate using the interpolation method.
        If a float, use that value for out-of-bounds points.
    bounds_error : bool, optional (default=False)
        If True, raise an error when interpolating outside the data range.
    time_column : str, optional (default='timestamp')
        Name of the column containing timestamps.
    value_columns : list of str, optional (default=None)
        List of column names to impute. If None, imputes all numeric columns.
    validate_timestamps : bool, optional (default=True)
        Whether to validate that timestamps are sorted and unique.
    copy : bool, optional (default=True)
        If True, create a copy of the input data.

    Attributes
    ----------
    is_fitted_ : bool
        Whether the imputer has been fitted.
    interpolators_ : dict
        Dictionary mapping column names to fitted interpolator objects.

    Examples
    --------
    >>> import pandas as pd
    >>> import numpy as np
    >>> from time_aware_imputer import SplineImputer
    >>> df = pd.DataFrame({
    ...     'timestamp': pd.date_range('2024-01-01', periods=10, freq='h'),
    ...     'value': [1, 2, np.nan, 4, 5, np.nan, 7, 8, 9, 10]
    ... })
    >>> imputer = SplineImputer(method='cubic')
    >>> df_imputed = imputer.fit_transform(df)
    """

    def __init__(
        self,
        method: Literal[
            "linear", "cubic", "quadratic", "slinear", "pchip", "akima"
        ] = "cubic",
        fill_value: Union[Literal["extrapolate"], float] = "extrapolate",
        bounds_error: bool = False,
        time_column: str = "timestamp",
        value_columns: Optional[list[str]] = None,
        validate_timestamps: bool = True,
        copy: bool = True,
    ) -> None:
        """Initialize SplineImputer."""
        super().__init__(
            time_column=time_column,
            value_columns=value_columns,
            validate_timestamps=validate_timestamps,
            copy=copy,
        )
        self.method = method
        self.fill_value = fill_value
        self.bounds_error = bounds_error

    def fit(self, X: pd.DataFrame, y: Optional[pd.Series] = None) -> "SplineImputer":
        """Fit the imputer on the training data.

        Parameters
        ----------
        X : pd.DataFrame
            Training data with timestamp column and value columns.
        y : pd.Series, optional (default=None)
            Ignored. Present for sklearn compatibility.

        Returns
        -------
        self : SplineImputer
            Fitted imputer.
        """
        super().fit(X, y)
        self.interpolators_: dict[str, object] = {}
        return self

    def _impute(self, X: pd.DataFrame) -> pd.DataFrame:
        """Impute missing values using spline interpolation.

        Parameters
        ----------
        X : pd.DataFrame
            Data with missing values.

        Returns
        -------
        X_imputed : pd.DataFrame
            Data with imputed values.
        """
        X_imputed = X.copy()

        # Convert timestamps to numeric (seconds since first timestamp)
        timestamps_col = X[self.time_column]
        time_numeric = self._timestamps_to_numeric(timestamps_col)

        for col in self.value_columns_:
            # Get non-missing values
            mask = ~X[col].isna()

            if mask.sum() < 2:
                # Need at least 2 points to interpolate
                continue

            x_known = np.asarray(time_numeric[mask])
            y_known = np.asarray(X.loc[mask, col])

            # Create interpolator based on method
            interpolator = self._create_interpolator(x_known, y_known)

            # Interpolate missing values
            x_missing = np.asarray(time_numeric[~mask])
            if len(x_missing) > 0:
                try:
                    y_imputed = interpolator(x_missing)
                    X_imputed.loc[~mask, col] = y_imputed
                except ValueError as e:
                    # If extrapolation fails, skip this column
                    import warnings

                    warnings.warn(f"Could not impute column '{col}': {e}", UserWarning)
                    continue

        return X_imputed

    def _create_interpolator(self, x: np.ndarray, y: np.ndarray) -> Any:
        """Create an interpolator object.

        Parameters
        ----------
        x : np.ndarray
            Known x values (time).
        y : np.ndarray
            Known y values (measurements).

        Returns
        -------
        interpolator : callable
            Interpolation function.
        """
        if self.method == "pchip":
            return interpolate.PchipInterpolator(
                x, y, extrapolate=self.fill_value == "extrapolate"
            )
        elif self.method == "akima":
            return interpolate.Akima1DInterpolator(x, y)
        else:
            # Use scipy's interp1d for other methods
            # Handle fill_value type conversion for interp1d
            fill_val: Union[str, float, tuple[float, float]]
            if isinstance(self.fill_value, str):
                fill_val = self.fill_value
            else:
                fill_val = self.fill_value
            return interpolate.interp1d(  # type: ignore[arg-type]
                x,
                y,
                kind=self.method,
                bounds_error=self.bounds_error,
                fill_value=fill_val,  # type: ignore[arg-type]
            )

    def _timestamps_to_numeric(self, timestamps: Union[pd.Series, Any]) -> pd.Series:
        """Convert timestamps to numeric values (seconds since first timestamp).

        Parameters
        ----------
        timestamps : pd.Series
            Timestamp series.

        Returns
        -------
        numeric : pd.Series
            Numeric representation of timestamps.
        """
        first_timestamp = timestamps.iloc[0]
        return (timestamps - first_timestamp).dt.total_seconds()
