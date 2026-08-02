"""
Core DataValidator class for EMR data validation
"""

import pandas as pd
import numpy as np
from typing import Dict, List, Optional, Union, Callable, Any
from datetime import datetime
import json
from pathlib import Path


class DataValidator:
    """
    Main validation engine for healthcare data.
    
    Simplified API compared to Great Expectations with better performance
    and healthcare-specific features.
    """
    
    def __init__(self, name: str = "EMR Validation"):
        """
        Initialize validator
        
        Args:
            name: Name for this validation context
        """
        self.name = name
        self.data = None
        self.validation_results = []
        self.metadata = {
            "created_at": datetime.now().isoformat(),
            "name": name,
            "total_validations": 0,
            "passed": 0,
            "failed": 0,
            "warnings": 0
        }
        
    def load_data(self, data: Union[pd.DataFrame, str, Path]) -> 'DataValidator':
        """
        Load data for validation
        
        Args:
            data: DataFrame or path to CSV/Excel file
            
        Returns:
            Self for method chaining
        """
        if isinstance(data, pd.DataFrame):
            self.data = data.copy()
        elif isinstance(data, (str, Path)):
            file_path = Path(data)
            if file_path.suffix == '.csv':
                self.data = pd.read_csv(file_path)
            elif file_path.suffix in ['.xlsx', '.xls']:
                self.data = pd.read_excel(file_path)
            else:
                raise ValueError(f"Unsupported file format: {file_path.suffix}")
        else:
            raise TypeError("Data must be DataFrame or file path")
            
        self.metadata["total_rows"] = len(self.data)
        self.metadata["total_columns"] = len(self.data.columns)
        return self
    # code optimized methods below

    def expect_column_exists(self, column: str, critical: bool = True) -> 'DataValidator':
        """Check if column exists in dataset"""
        result = {
            "rule": "column_exists",
            "column": column,
            "critical": critical,
            "passed": column in self.data.columns,
            "message": f"Column '{column}' exists" if column in self.data.columns else f"Column '{column}' missing"
        }
        self._record_result(result)
        return self

    def expect_column_not_null(self, column: str, threshold: float = 1.0, critical: bool = True) -> 'DataValidator':
        """
        Check for null values in column using vectorized pandas ops
        
        Args:
            column: Column name
            threshold: Minimum non-null percentage (0.0 to 1.0)
            critical: Whether this is a critical validation
        """
        if column not in self.data.columns:
            result = {
                "rule": "column_not_null",
                "column": column,
                "critical": critical,
                "passed": False,
                "message": f"Column '{column}' does not exist"
            }
            self._record_result(result)
            return self

        series = self.data[column]
        non_null_frac = float(series.notna().mean())
        passed = non_null_frac >= float(threshold)
        pct = round(non_null_frac * 100, 2)

        result = {
            "rule": "column_not_null",
            "column": column,
            "critical": critical,
            "passed": bool(passed),
            "non_null_percentage": pct,
            "threshold": threshold * 100,
            "null_count": int(series.isna().sum()),
            "message": f"Non-null percentage for '{column}': {pct}% (threshold {threshold*100}%)"
        }
        self._record_result(result)
        return self

    def expect_column_values_in_set(self, column: str, value_set: set, 
                                   threshold: float = 1.0, critical: bool = True) -> 'DataValidator':
        """
        Check if column values are in allowed set using vectorized membership checks
        
        Args:
            column: Column name
            value_set: Set of allowed values
            threshold: Minimum percentage of rows that must match (0.0 to 1.0)
            critical: Whether this is a critical validation
        """
        if column not in self.data.columns:
            result = {
                "rule": "values_in_set",
                "column": column,
                "critical": critical,
                "passed": False,
                "message": f"Column '{column}' does not exist"
            }
            self._record_result(result)
            return self

        series = self.data[column]
        mask = series.isin(value_set)
        valid_frac = float(mask.mean())
        passed = valid_frac >= float(threshold)
        pct = round(valid_frac * 100, 2)

        # Collect invalid example values (dropna to avoid listing NaN)
        invalid_values = series.loc[~mask].dropna().unique()

        result = {
            "rule": "values_in_set",
            "column": column,
            "critical": critical,
            "passed": bool(passed),
            "valid_percentage": pct,
            "threshold": threshold * 100,
            "invalid_count": int((~mask).sum()),
            "invalid_values": list(invalid_values[:10]),
            "message": f"Values in set for '{column}': {pct}% (threshold {threshold*100}%)"
        }
        self._record_result(result)
        return self

    def expect_column_values_unique(self, column: str, threshold: float = 1.0, 
                                   critical: bool = True) -> 'DataValidator':
        """Check for duplicate values in column"""
        if column not in self.data.columns:
            result = {
                "rule": "values_unique",
                "column": column,
                "critical": critical,
                "passed": False,
                "message": f"Column '{column}' does not exist"
            }
            self._record_result(result)
            return self
            
        unique_pct = self.data[column].nunique() / len(self.data)
        passed = unique_pct >= threshold
        duplicate_count = len(self.data) - self.data[column].nunique()
        
        result = {
            "rule": "values_unique",
            "column": column,
            "critical": critical,
            "passed": passed,
            "unique_percentage": round(unique_pct * 100, 2),
            "threshold": threshold * 100,
            "duplicate_count": int(duplicate_count),
            "message": f"Unique: {unique_pct*100:.2f}% (threshold: {threshold*100}%)"
        }
        self._record_result(result)
        return self

    def expect_column_values_between(self, column: str, min_value: float, max_value: float,
                                    threshold: float = 1.0, critical: bool = True) -> 'DataValidator':
        """Check if numeric values are within range"""
        if column not in self.data.columns:
            result = {
                "rule": "values_between",
                "column": column,
                "critical": critical,
                "passed": False,
                "message": f"Column '{column}' does not exist"
            }
            self._record_result(result)
            return self
            
        valid_mask = (self.data[column] >= min_value) & (self.data[column] <= max_value)
        valid_pct = valid_mask.sum() / len(self.data)
        passed = valid_pct >= threshold
        
        result = {
            "rule": "values_between",
            "column": column,
            "critical": critical,
            "passed": passed,
            "valid_percentage": round(valid_pct * 100, 2),
            "threshold": threshold * 100,
            "min_value": min_value,
            "max_value": max_value,
            "out_of_range_count": int((~valid_mask).sum()),
            "message": f"In range [{min_value}, {max_value}]: {valid_pct*100:.2f}%"
        }
        self._record_result(result)
        return self

    def expect_column_date_format(self, column: str, date_format: str = "%Y-%m-%d",
                                 threshold: float = 1.0, critical: bool = True) -> 'DataValidator':
        """Check if dates match expected format"""
        if column not in self.data.columns:
            result = {
                "rule": "date_format",
                "column": column,
                "critical": critical,
                "passed": False,
                "message": f"Column '{column}' does not exist"
            }
            self._record_result(result)
            return self
            
        def is_valid_date(val):
            if pd.isna(val):
                return False
            try:
                datetime.strptime(str(val), date_format)
                return True
            except:
                return False
        
        valid_mask = self.data[column].apply(is_valid_date)
        valid_pct = valid_mask.sum() / len(self.data)
        passed = valid_pct >= threshold
        
        result = {
            "rule": "date_format",
            "column": column,
            "critical": critical,
            "passed": passed,
            "valid_percentage": round(valid_pct * 100, 2),
            "threshold": threshold * 100,
            "date_format": date_format,
            "invalid_count": int((~valid_mask).sum()),
            "message": f"Valid format: {valid_pct*100:.2f}% (expected: {date_format})"
        }
        self._record_result(result)
        return self

    def expect_mrn_format(self, column: str, pattern: Optional[str] = None,
                         threshold: float = 1.0, critical: bool = True) -> 'DataValidator':
        """
        Healthcare-specific: Validate Medical Record Numbers
        """
        if column not in self.data.columns:
            result = {
                "rule": "mrn_format",
                "column": column,
                "critical": critical,
                "passed": False,
                "message": f"Column '{column}' does not exist"
            }
            self._record_result(result)
            return self
            
        if pattern:
            valid_mask = self.data[column].astype(str).str.match(pattern)
        else:
            valid_mask = (
                self.data[column].notna() & 
                (self.data[column].astype(str).str.len() >= 5) &
                (self.data[column].astype(str).str.len() <= 20)
            )
        
        valid_pct = valid_mask.sum() / len(self.data)
        passed = valid_pct >= threshold
        
        result = {
            "rule": "mrn_format",
            "column": column,
            "critical": critical,
            "passed": passed,
            "valid_percentage": round(valid_pct * 100, 2),
            "threshold": threshold * 100,
            "invalid_count": int((~valid_mask).sum()),
            "message": f"Valid MRNs: {valid_pct*100:.2f}%"
        }
        self._record_result(result)
        return self

    def expect_icd_format(self, column: str, version: int = 10, 
                         threshold: float = 1.0, critical: bool = True) -> 'DataValidator':
        """
        Healthcare-specific: Validate ICD codes (vectorized implementation using Series.str.fullmatch)
        """
        if column not in self.data.columns:
            result = {
                "rule": "icd_format",
                "column": column,
                "critical": critical,
                "passed": False,
                "message": f"Column '{column}' does not exist"
            }
            self._record_result(result)
            return self

        series = self.data[column].dropna().astype(str)
        if series.empty:
            result = {
                "rule": "icd_format",
                "column": column,
                "critical": critical,
                "passed": False,
                "message": f"No non-null values in column '{column}' to validate"
            }
            self._record_result(result)
            return self

        if version == 10:
            # ICD-10: Letter + 2 digits + optional decimal + 1-2 more digits
            # pattern anchored, allow lowercase by uppercasing input
            pattern = r'^[A-Z]\d{2}\.?(?:\d{1,2})?$'
            # ensure uppercase for letter comparison
            series = series.str.upper()
        else:
            # ICD-9 (simple heuristic) - allow 3-5 digits, optional decimal + digits
            pattern = r'^\d{3,5}(?:\.\d+)?$'

        matched = series.str.fullmatch(pattern)
        valid_frac = float(matched.sum()) / len(series)
        passed = valid_frac >= float(threshold)
        pct = round(valid_frac * 100, 2)

        result = {
            "rule": "icd_format",
            "column": column,
            "critical": critical,
            "passed": bool(passed),
            "valid_percentage": pct,
            "threshold": threshold * 100,
            "icd_version": version,
            "invalid_count": int((~matched.fillna(False)).sum()),
            "message": f"ICD{version} valid percentage for '{column}': {pct}% (threshold {threshold*100}%)"
        }
        self._record_result(result)
        return self

    def expect_custom(self, rule_name: str, validation_func: Callable, 
                     column: Optional[str] = None, critical: bool = True,
                     **kwargs) -> 'DataValidator':
        """
        Apply custom validation function
        """
        try:
            passed, message, details = validation_func(self.data, **kwargs)
            result = {
                "rule": rule_name,
                "column": column,
                "critical": critical,
                "passed": passed,
                "message": message,
                **details
            }
        except Exception as e:
            result = {
                "rule": rule_name,
                "column": column,
                "critical": critical,
                "passed": False,
                "message": f"Validation error: {str(e)}"
            }
        
        self._record_result(result)
        return self

    def _record_result(self, result: Dict[str, Any]) -> None:
        """Record validation result and update metadata"""
        self.validation_results.append(result)
        self.metadata["total_validations"] += 1
        
        if result["passed"]:
            self.metadata["passed"] += 1
        elif result.get("critical", True):
            self.metadata["failed"] += 1
        else:
            self.metadata["warnings"] += 1
