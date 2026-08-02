"""
vitals.py
---------
Module for analyzing patient vital signs.
Provides rolling averages, outlier detection, and trend summaries.
"""

import pandas as pd
import numpy as np


class VitalFrame(pd.DataFrame):
    """Extension of Pandas DataFrame for vital signs analysis."""

    _metadata = ["vital_id"]

    @property
    def _constructor(self):
        return VitalFrame

    def rolling_average(self, column, window=3):
        """Calculates rolling mean for a given vital sign."""
        if column not in self.columns:
            raise ValueError(f"{column} not found in data.")
        self[f"{column}_avg"] = self[column].rolling(window=window).mean()
        print(f"🩺 Calculated {window}-point rolling average for {column}.")
        return self

    def detect_outliers(self, column, z_thresh=3):
        """Flags outliers using Z-score threshold."""
        if column not in self.columns:
            raise ValueError(f"{column} not found in data.")
        z_scores = np.abs((self[column] - self[column].mean()) / self[column].std())
        self["outlier"] = np.where(z_scores > z_thresh, True, False)
        outliers = self["outlier"].sum()
        print(f"⚡ Detected {outliers} outliers in {column}.")
        return self

    def vital_summary(self):
        """Returns basic statistics for all numeric columns."""
        summary = self.describe().T
        print("📊 Vital sign summary statistics generated.")
        return summary
