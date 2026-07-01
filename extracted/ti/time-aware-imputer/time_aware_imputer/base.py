"""Base class for time-aware imputation."""

import warnings
from typing import Any, Dict, Optional, Union

import numpy as np
import pandas as pd
from sklearn.base import BaseEstimator, TransformerMixin
from sklearn.utils.validation import check_is_fitted


class TimeAwareImputer(BaseEstimator, TransformerMixin):
    """Base class for time-aware missing data imputation.

    This class provides the foundation for all time-aware imputation strategies.
    It handles timestamp parsing, validation, and provides a scikit-learn
    compatible interface.

    Parameters
    ----------
    time_column : str, optional (default='timestamp')
        Name of the column containing timestamps.
    value_columns : list of str, optional (default=None)
        List of column names to impute. If None, imputes all numeric columns
        except the time column.
    validate_timestamps : bool, optional (default=True)
        Whether to validate that timestamps are sorted and unique.
    copy : bool, optional (default=True)
        If True, create a copy of the input data. If False, impute in place.

    Attributes
    ----------
    is_fitted_ : bool
        Whether the imputer has been fitted.
    feature_names_in_ : list of str
        Names of features seen during fit.
    n_features_in_ : int
        Number of features seen during fit.
    imputed_mask_ : pd.DataFrame
        Boolean mask indicating which values were imputed.
    """

    def __init__(
        self,
        time_column: str = "timestamp",
        value_columns: Optional[list[str]] = None,
        validate_timestamps: bool = True,
        copy: bool = True,
    ) -> None:
        """Initialize TimeAwareImputer."""
        self.time_column = time_column
        self.value_columns = value_columns
        self.validate_timestamps = validate_timestamps
        self.copy = copy

    def fit(self, X: pd.DataFrame, y: Optional[pd.Series] = None) -> "TimeAwareImputer":
        """Fit the imputer on the training data.

        Parameters
        ----------
        X : pd.DataFrame
            Training data with timestamp column and value columns.
        y : pd.Series, optional (default=None)
            Ignored. Present for sklearn compatibility.

        Returns
        -------
        self : TimeAwareImputer
            Fitted imputer.
        """
        X = self._validate_input(X)

        # Store feature names
        self.feature_names_in_ = list(X.columns)
        self.n_features_in_ = len(self.feature_names_in_)

        # Determine value columns if not specified
        if self.value_columns is None:
            self.value_columns_ = [col for col in X.columns if col != self.time_column]
        else:
            self.value_columns_ = self.value_columns

        # Validate value columns exist
        missing_cols = set(self.value_columns_) - set(X.columns)
        if missing_cols:
            raise ValueError(f"Value columns not found in data: {missing_cols}")

        self.is_fitted_ = True
        return self

    def transform(self, X: pd.DataFrame) -> pd.DataFrame:
        """Transform data by imputing missing values.

        Parameters
        ----------
        X : pd.DataFrame
            Data to transform with timestamp column and value columns.

        Returns
        -------
        X_imputed : pd.DataFrame
            Transformed data with imputed values.
        """
        check_is_fitted(self, "is_fitted_")
        X = self._validate_input(X)

        if self.copy:
            X = X.copy()

        # Create mask for imputed values
        self.imputed_mask_ = X[self.value_columns_].isna()

        # Subclasses should override this method to implement imputation
        X_imputed: pd.DataFrame = self._impute(X)

        return X_imputed

    def fit_transform(
        self, X: pd.DataFrame, y: Optional[pd.Series] = None
    ) -> pd.DataFrame:
        """Fit and transform in one step.

        Parameters
        ----------
        X : pd.DataFrame
            Data to fit and transform.
        y : pd.Series, optional (default=None)
            Ignored. Present for sklearn compatibility.

        Returns
        -------
        X_imputed : pd.DataFrame
            Transformed data with imputed values.
        """
        return self.fit(X, y).transform(X)

    def _validate_input(self, X: pd.DataFrame) -> pd.DataFrame:
        """Validate input data.

        Parameters
        ----------
        X : pd.DataFrame
            Input data to validate.

        Returns
        -------
        X : pd.DataFrame
            Validated input data.

        Raises
        ------
        ValueError
            If input validation fails.
        """
        if not isinstance(X, pd.DataFrame):
            raise ValueError("Input must be a pandas DataFrame")

        if self.time_column not in X.columns:
            raise ValueError(f"Time column '{self.time_column}' not found in data")

        # Convert time column to datetime if not already
        if not pd.api.types.is_datetime64_any_dtype(X[self.time_column]):
            try:
                X = X.copy()
                X[self.time_column] = pd.to_datetime(X[self.time_column])
            except Exception as e:
                raise ValueError(
                    f"Could not convert time column to datetime: {e}"
                ) from e

        if self.validate_timestamps:
            # Check if timestamps are sorted
            if not X[self.time_column].is_monotonic_increasing:
                warnings.warn(
                    "Timestamps are not sorted. Sorting automatically.",
                    UserWarning,
                )
                X = X.sort_values(self.time_column).reset_index(drop=True)

            # Check for duplicate timestamps
            if X[self.time_column].duplicated().any():
                warnings.warn(
                    "Duplicate timestamps found. Keeping first occurrence.",
                    UserWarning,
                )
                X = X.drop_duplicates(subset=[self.time_column], keep="first")

        return X

    def _impute(self, X: pd.DataFrame) -> pd.DataFrame:
        """Impute missing values.

        This method should be overridden by subclasses to implement
        specific imputation strategies.

        Parameters
        ----------
        X : pd.DataFrame
            Data with missing values.

        Returns
        -------
        X_imputed : pd.DataFrame
            Data with imputed values.
        """
        raise NotImplementedError("Subclasses must implement the _impute method")

    def get_imputed_mask(self) -> pd.DataFrame:
        """Get boolean mask of imputed values.

        Returns
        -------
        mask : pd.DataFrame
            Boolean mask where True indicates an imputed value.

        Raises
        ------
        NotFittedError
            If the imputer has not been fitted yet.
        """
        check_is_fitted(self, "imputed_mask_")
        return self.imputed_mask_  # type: ignore[return-value]

    def get_feature_names_out(
        self, input_features: Optional[list[str]] = None
    ) -> list[str]:
        """Get output feature names.

        Parameters
        ----------
        input_features : list of str, optional (default=None)
            Not used. Present for sklearn compatibility.

        Returns
        -------
        feature_names : list of str
            Output feature names.
        """
        check_is_fitted(self, "feature_names_in_")
        return self.feature_names_in_
