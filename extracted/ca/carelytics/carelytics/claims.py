"""
claims.py
----------
Functions for analyzing healthcare claims and revenue cycle data.
Includes denial rate, reimbursement efficiency, and claim volume tracking.
"""

import pandas as pd
import numpy as np


class ClaimFrame(pd.DataFrame):
    """Extension of Pandas DataFrame for claims data analysis."""

    _metadata = ["claim_id"]

    @property
    def _constructor(self):
        return ClaimFrame

    def clean_codes(self, icd_version="10"):
        """
        Cleans ICD or CPT codes by stripping spaces and converting to uppercase.
        """
        if "icd_code" in self.columns:
            self["icd_code"] = self["icd_code"].astype(str).str.strip().str.upper()
            print(f"🩻 ICD-{icd_version} codes standardized.")
        return self

    def denial_rate(self):
        """
        Calculates the percentage of denied claims.
        """
        if "status" not in self.columns:
            raise ValueError("Claims data must include 'status' column.")

        total = len(self)
        denied = len(self[self["status"].str.lower() == "denied"])
        rate = (denied / total) * 100
        print(f"🚫 Denial rate: {rate:.2f}%")
        return rate

    def revenue_efficiency(self):
        """
        Computes efficiency as approved claim amount / total claim amount.
        """
        if not {"status", "amount"}.issubset(self.columns):
            raise ValueError("Claims data must include 'status' and 'amount' columns.")

        approved = self[self["status"].str.lower() == "approved"]["amount"].sum()
        total = self["amount"].sum()
        efficiency = approved / total if total else 0
        print(f"💵 Revenue cycle efficiency: {efficiency:.2%}")
        return efficiency

    def average_payment_delay(self):
        """
        Calculates the average payment delay in days between claim date and payment date.
        """
        if {"claim_date", "payment_date"}.issubset(self.columns):
            delay = (self["payment_date"] - self["claim_date"]).dt.days
            avg_delay = delay.mean()
            print(f"⏱️ Average payment delay: {avg_delay:.1f} days")
            return avg_delay
        else:
            raise ValueError("Columns 'claim_date' and 'payment_date' required.")
