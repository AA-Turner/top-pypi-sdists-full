"""
Validation rules and expectations
"""

from typing import Callable, List, Dict, Any, Optional
import pandas as pd


class ValidationRule:
    """
    A single validation rule that can be reused across datasets
    """
    
    def __init__(self, 
                 name: str,
                 description: str,
                 validation_func: Callable,
                 critical: bool = True,
                 **kwargs):
        """
        Initialize validation rule
        
        Args:
            name: Rule name
            description: Human-readable description
            validation_func: Function that takes data and returns (passed, message, details)
            critical: Whether this is a critical validation
            **kwargs: Additional parameters for validation function
        """
        self.name = name
        self.description = description
        self.validation_func = validation_func
        self.critical = critical
        self.params = kwargs
        
    def execute(self, data: pd.DataFrame) -> Dict[str, Any]:
        """Execute the validation rule"""
        try:
            passed, message, details = self.validation_func(data, **self.params)
            return {
                "rule": self.name,
                "description": self.description,
                "critical": self.critical,
                "passed": passed,
                "message": message,
                **details
            }
        except Exception as e:
            return {
                "rule": self.name,
                "description": self.description,
                "critical": self.critical,
                "passed": False,
                "message": f"Validation error: {str(e)}"
            }


class RuleSet:
    """
    Collection of validation rules that can be applied together
    """
    
    def __init__(self, name: str, description: Optional[str] = None):
        """
        Initialize rule set
        
        Args:
            name: Rule set name
            description: Optional description
        """
        self.name = name
        self.description = description or f"{name} validation rules"
        self.rules: List[ValidationRule] = []
        
    def add_rule(self, rule: ValidationRule) -> 'RuleSet':
        """Add a rule to the set"""
        self.rules.append(rule)
        return self
    
    def create_rule(self,
                   name: str,
                   description: str,
                   validation_func: Callable,
                   critical: bool = True,
                   **kwargs) -> 'RuleSet':
        """Create and add a rule in one step"""
        rule = ValidationRule(name, description, validation_func, critical, **kwargs)
        self.rules.append(rule)
        return self
    
    def execute_all(self, data: pd.DataFrame) -> List[Dict[str, Any]]:
        """Execute all rules in the set"""
        results = []
        for rule in self.rules:
            results.append(rule.execute(data))
        return results
    
    def __len__(self) -> int:
        """Number of rules in set"""
        return len(self.rules)


class Expectation:
    """
    Expectation-based validation (similar to Great Expectations but simpler)
    """
    
    @staticmethod
    def column_to_exist(column: str):
        """Expect column to exist"""
        def validate(df: pd.DataFrame, **kwargs):
            passed = column in df.columns
            message = f"Column '{column}' exists" if passed else f"Column '{column}' not found"
            return passed, message, {"column": column}
        return validate
    
    @staticmethod
    def column_values_to_not_be_null(column: str, mostly: float = 1.0):
        """Expect column values to not be null"""
        def validate(df: pd.DataFrame, **kwargs):
            if column not in df.columns:
                return False, f"Column '{column}' not found", {}
            
            non_null_pct = df[column].notna().sum() / len(df)
            passed = non_null_pct >= mostly
            
            return passed, f"Non-null: {non_null_pct*100:.2f}% (expected: {mostly*100}%)", {
                "column": column,
                "non_null_percentage": round(non_null_pct * 100, 2),
                "null_count": int(df[column].isna().sum())
            }
        return validate
    
    @staticmethod
    def column_values_to_be_in_set(column: str, value_set: set, mostly: float = 1.0):
        """Expect column values to be in set"""
        def validate(df: pd.DataFrame, **kwargs):
            if column not in df.columns:
                return False, f"Column '{column}' not found", {}
            
            valid_pct = df[column].isin(value_set).sum() / len(df)
            passed = valid_pct >= mostly
            
            invalid = df.loc[~df[column].isin(value_set), column].unique()
            
            return passed, f"Valid: {valid_pct*100:.2f}% (expected: {mostly*100}%)", {
                "column": column,
                "valid_percentage": round(valid_pct * 100, 2),
                "invalid_values": list(invalid[:5])
            }
        return validate
    
    @staticmethod
    def column_values_to_be_unique(column: str, mostly: float = 1.0):
        """Expect column values to be unique"""
        def validate(df: pd.DataFrame, **kwargs):
            if column not in df.columns:
                return False, f"Column '{column}' not found", {}
            
            unique_pct = df[column].nunique() / len(df)
            passed = unique_pct >= mostly
            
            return passed, f"Unique: {unique_pct*100:.2f}% (expected: {mostly*100}%)", {
                "column": column,
                "unique_percentage": round(unique_pct * 100, 2),
                "duplicate_count": len(df) - df[column].nunique()
            }
        return validate
    
    @staticmethod
    def column_values_to_be_between(column: str, min_value: float, max_value: float, mostly: float = 1.0):
        """Expect numeric values to be between min and max"""
        def validate(df: pd.DataFrame, **kwargs):
            if column not in df.columns:
                return False, f"Column '{column}' not found", {}
            
            in_range = ((df[column] >= min_value) & (df[column] <= max_value)).sum() / len(df)
            passed = in_range >= mostly
            
            return passed, f"In range [{min_value}, {max_value}]: {in_range*100:.2f}%", {
                "column": column,
                "in_range_percentage": round(in_range * 100, 2),
                "min_value": min_value,
                "max_value": max_value
            }
        return validate
    
    @staticmethod
    def column_mean_to_be_between(column: str, min_value: float, max_value: float):
        """Expect column mean to be in range"""
        def validate(df: pd.DataFrame, **kwargs):
            if column not in df.columns:
                return False, f"Column '{column}' not found", {}
            
            mean_val = df[column].mean()
            passed = min_value <= mean_val <= max_value
            
            return passed, f"Mean: {mean_val:.2f} (expected: [{min_value}, {max_value}])", {
                "column": column,
                "mean": round(float(mean_val), 2),
                "min_expected": min_value,
                "max_expected": max_value
            }
        return validate
    
    @staticmethod
    def table_row_count_to_be_between(min_count: int, max_count: int):
        """Expect row count to be in range"""
        def validate(df: pd.DataFrame, **kwargs):
            row_count = len(df)
            passed = min_count <= row_count <= max_count
            
            return passed, f"Row count: {row_count:,} (expected: [{min_count:,}, {max_count:,}])", {
                "row_count": row_count,
                "min_expected": min_count,
                "max_expected": max_count
            }
        return validate
    
    @staticmethod
    def table_column_count_to_equal(expected_count: int):
        """Expect specific number of columns"""
        def validate(df: pd.DataFrame, **kwargs):
            col_count = len(df.columns)
            passed = col_count == expected_count
            
            return passed, f"Column count: {col_count} (expected: {expected_count})", {
                "column_count": col_count,
                "expected": expected_count
            }
        return validate


class ExpectationSuite:
    """
    Suite of expectations that can be executed together
    """
    
    def __init__(self, suite_name: str):
        """
        Initialize expectation suite
        
        Args:
            suite_name: Name for this suite
        """
        self.suite_name = suite_name
        self.expectations: List[tuple] = []  # (name, validation_func, critical)
        
    def expect(self, 
               expectation_name: str,
               validation_func: Callable,
               critical: bool = True) -> 'ExpectationSuite':
        """
        Add an expectation to the suite
        
        Args:
            expectation_name: Name for this expectation
            validation_func: Validation function from Expectation class
            critical: Whether this is critical
        """
        self.expectations.append((expectation_name, validation_func, critical))
        return self
    
    def validate(self, data: pd.DataFrame) -> List[Dict[str, Any]]:
        """Execute all expectations"""
        results = []
        
        for name, func, critical in self.expectations:
            try:
                passed, message, details = func(data)
                results.append({
                    "expectation": name,
                    "critical": critical,
                    "passed": passed,
                    "message": message,
                    **details
                })
            except Exception as e:
                results.append({
                    "expectation": name,
                    "critical": critical,
                    "passed": False,
                    "message": f"Validation error: {str(e)}"
                })
        
        return results
    
    def __len__(self) -> int:
        """Number of expectations"""
        return len(self.expectations)


# Pre-built rule sets for common healthcare scenarios

class HealthcareRuleSets:
    """Pre-configured rule sets for healthcare data"""
    
    @staticmethod
    def patient_demographics() -> RuleSet:
        """Standard validations for patient demographics"""
        ruleset = RuleSet("Patient Demographics", "Validations for patient demographic data")
        
        # MRN validation
        def validate_mrn(df, column='mrn'):
            if column not in df.columns:
                return False, f"Column '{column}' not found", {}
            valid = df[column].notna() & (df[column].astype(str).str.len() >= 5)
            pct = valid.sum() / len(df) * 100
            return pct > 95, f"Valid MRNs: {pct:.1f}%", {"valid_percentage": round(pct, 2)}
        
        ruleset.create_rule("mrn_format", "MRN format validation", validate_mrn)
        
        # Age validation
        def validate_age(df, column='age'):
            if column not in df.columns:
                return False, f"Column '{column}' not found", {}
            valid = (df[column] >= 0) & (df[column] <= 120)
            pct = valid.sum() / len(df) * 100
            return pct > 99, f"Valid ages: {pct:.1f}%", {"valid_percentage": round(pct, 2)}
        
        ruleset.create_rule("age_range", "Age range validation", validate_age)
        
        return ruleset
    
    @staticmethod
    def financial_data() -> RuleSet:
        """Standard validations for financial/billing data"""
        ruleset = RuleSet("Financial Data", "Validations for financial and billing data")
        
        def validate_charges(df, column='charge_amount'):
            if column not in df.columns:
                return False, f"Column '{column}' not found", {}
            valid = df[column] >= 0
            pct = valid.sum() / len(df) * 100
            return pct > 99, f"Valid charges: {pct:.1f}%", {"valid_percentage": round(pct, 2)}
        
        ruleset.create_rule("positive_charges", "Charges must be non-negative", validate_charges)
        
        return ruleset
