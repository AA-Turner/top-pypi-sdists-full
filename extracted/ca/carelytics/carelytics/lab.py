"""
lab.py
------
Module for handling and analyzing laboratory test data.
Includes trend detection, abnormal flagging, and summary statistics.
"""

import pandas as pd
import numpy as np


class LabFrame(pd.DataFrame):
    """Extension of Pandas DataFrame for lab result analysis."""

    _metadata = ["lab_id"]

    @property
    def _constructor(self):
        return LabFrame

    def flag_abnormal(self):
        """
        Flags abnormal lab results based on normal range columns.
        Expects 'value', 'normal_low', and 'normal_high' columns.
        """
        if not {"value", "normal_low", "normal_high"}.issubset(self.columns):
            raise ValueError("Columns 'value', 'normal_low', and 'normal_high' are required.")

        self["flag"] = np.where(
            (self["value"] < self["normal_low"]) | (self["value"] > self["normal_high"]),
            "Abnormal",
            "Normal",
        )
        print(f"🧫 Flagged abnormal values in {self['flag'].value_counts().to_dict()}")
        return self

    def abnormal_rate(self):
        """Calculates percentage of abnormal lab results."""
        if "flag" not in self.columns:
            raise ValueError("Run flag_abnormal() first.")
        abnormal = (self["flag"] == "Abnormal").mean() * 100
        print(f"⚠️ Abnormal lab rate: {abnormal:.2f}%")
        return abnormal

    def lab_trends(self, lab_name):
        """
        Returns trend of lab values over time for a given lab test.
        """
        subset = self[self["lab_name"].str.lower() == lab_name.lower()]
        trend = subset.groupby("date")["value"].mean().reset_index()
        print(f"📈 Trend for {lab_name}: {len(trend)} time points.")
        return trend
