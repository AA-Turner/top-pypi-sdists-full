"""
patient.py
-----------
Module for managing and analyzing patient-level healthcare data.
Includes de-identification, cohort analysis, and readmission metrics.
"""

import pandas as pd
import numpy as np
from datetime import timedelta


class PatientFrame(pd.DataFrame):
    """Extension of Pandas DataFrame for patient data."""

    _metadata = ["patient_id"]

    @property
    def _constructor(self):
        return PatientFrame

    def deidentify(self, remove=None):
        """
        Removes personally identifiable information (PII) columns
        for HIPAA-safe data handling.

        Parameters
        ----------
        remove : list, optional
            Columns to remove (default: common identifiers)
        """
        if remove is None:
            remove = ["name", "ssn", "address", "email", "phone"]

        for col in remove:
            if col in self.columns:
                self.drop(columns=[col], inplace=True)

        print("✅ Patient data de-identified successfully.")
        return self

    def readmission_rate(self, days=30):
        """
        Calculates readmission rate within a given time window.

        Parameters
        ----------
        days : int
            Time window in days for readmission count.

        Returns
        -------
        float
            Readmission rate as a percentage.
        """
        if "admit_date" not in self.columns or "discharge_date" not in self.columns:
            raise ValueError("Missing admit_date or discharge_date columns.")

        self = self.sort_values(by=["patient_id", "admit_date"])
        readmissions = 0
        total_patients = self["patient_id"].nunique()

        for pid, group in self.groupby("patient_id"):
            discharge_dates = group["discharge_date"].values
            admit_dates = group["admit_date"].values
            for i in range(1, len(admit_dates)):
                if (admit_dates[i] - discharge_dates[i - 1]) <= np.timedelta64(days, "D"):
                    readmissions += 1
                    break

        rate = (readmissions / total_patients) * 100
        print(f"📊 Readmission rate ({days} days): {rate:.2f}%")
        return rate

    def length_of_stay_mean(self):
        """Returns the average length of stay (LOS) in days."""
        if {"admit_date", "discharge_date"}.issubset(self.columns):
            los = (self["discharge_date"] - self["admit_date"]).dt.days
            return los.mean()
        else:
            raise ValueError("admit_date and discharge_date columns are required.")
