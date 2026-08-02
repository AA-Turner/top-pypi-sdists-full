"""
Data Profiler for automated quality assessment
"""

import pandas as pd
import numpy as np
from typing import Dict, List, Any, Optional
from datetime import datetime


class DataProfiler:
    """
    Automated data profiling and quality assessment.
    Simpler and faster than pandas-profiling with healthcare focus.
    """
    
    def __init__(self, data: pd.DataFrame, name: str = "Data Profile"):
        """
        Initialize profiler
        
        Args:
            data: DataFrame to profile
            name: Name for this profile
        """
        self.data = data
        self.name = name
        self.profile = {}
        
    def generate_profile(self, sample_values: int = 5) -> Dict[str, Any]:
        """
        Generate comprehensive data profile
        
        Args:
            sample_values: Number of sample values to include
            
        Returns:
            Dictionary with profile results
        """
        self.profile = {
            "metadata": self._profile_metadata(),
            "overview": self._profile_overview(),
            "columns": self._profile_columns(sample_values),
            "quality_summary": self._quality_summary(),
            "correlations": self._profile_correlations(),
            "recommendations": self._generate_recommendations()
        }
        
        return self.profile
    
    def _profile_metadata(self) -> Dict[str, Any]:
        """Profile metadata"""
        return {
            "name": self.name,
            "generated_at": datetime.now().isoformat(),
            "rows": len(self.data),
            "columns": len(self.data.columns),
            "memory_usage_mb": round(self.data.memory_usage(deep=True).sum() / 1024**2, 2)
        }
    
    def _profile_overview(self) -> Dict[str, Any]:
        """Overall dataset statistics"""
        duplicate_rows = self.data.duplicated().sum()
        
        total_cells = len(self.data) * len(self.data.columns) if len(self.data) and len(self.data.columns) else 0
        total_missing = int(self.data.isna().sum().sum())
        missing_percentage = round(total_missing / total_cells * 100, 2) if total_cells else 0.0
        
        return {
            "total_cells": total_cells,
            "total_missing": total_missing,
            "missing_percentage": missing_percentage,
            "duplicate_rows": int(duplicate_rows),
            "duplicate_percentage": round(duplicate_rows / len(self.data) * 100, 2) if len(self.data) else 0.0,
            "column_types": self.data.dtypes.value_counts().to_dict()
        }
    
    def _profile_columns(self, sample_values: int = 5) -> Dict[str, Dict[str, Any]]:
        """Profile each column"""
        column_profiles = {}
        
        for col in self.data.columns:
            column_profiles[col] = self._profile_single_column(col, sample_values)
        
        return column_profiles
    
    def _profile_single_column(self, column: str, sample_values: int) -> Dict[str, Any]:
        """Profile a single column"""
        col_data = self.data[column]
        
        n = len(col_data)
        count = int(col_data.count())
        missing = int(col_data.isna().sum())
        missing_percentage = round(missing / n * 100, 2) if n else 0.0
        unique_values = int(col_data.nunique(dropna=True))
        unique_percentage = round(unique_values / n * 100, 2) if n else 0.0

        profile = {
            "dtype": str(col_data.dtype),
            "count": count,
            "missing": missing,
            "missing_percentage": missing_percentage,
            "unique_values": unique_values,
            "unique_percentage": unique_percentage
        }
        
        # Numeric columns
        if pd.api.types.is_numeric_dtype(col_data):
            not_all_na = not col_data.isna().all()
            profile.update({
                "mean": round(float(col_data.mean()), 2) if not_all_na else None,
                "std": round(float(col_data.std()), 2) if not_all_na else None,
                "min": round(float(col_data.min()), 2) if not_all_na else None,
                "max": round(float(col_data.max()), 2) if not_all_na else None,
                "median": round(float(col_data.median()), 2) if not_all_na else None,
                "q25": round(float(col_data.quantile(0.25)), 2) if not_all_na else None,
                "q75": round(float(col_data.quantile(0.75)), 2) if not_all_na else None,
                "zeros": int((col_data == 0).sum()),
                "negative": int((col_data < 0).sum()),
                "outliers": self._detect_outliers(col_data)
            })
        
        # Categorical/Object columns
        elif pd.api.types.is_object_dtype(col_data) or pd.api.types.is_categorical_dtype(col_data):
            value_counts = col_data.value_counts(dropna=True)
            not_all_na = not col_data.isna().all()
            str_lens = col_data.dropna().astype(str).str.len() if not_all_na else pd.Series(dtype=int)
            profile.update({
                "top_values": value_counts.head(sample_values).to_dict(),
                "most_common": str(value_counts.index[0]) if len(value_counts) > 0 else None,
                "most_common_count": int(value_counts.iloc[0]) if len(value_counts) > 0 else 0,
                "min_length": int(str_lens.min()) if not str_lens.empty else None,
                "max_length": int(str_lens.max()) if not str_lens.empty else None,
                "avg_length": round(float(str_lens.mean()), 2) if not str_lens.empty else None
            })
        
        # DateTime columns
        elif pd.api.types.is_datetime64_any_dtype(col_data):
            not_all_na = not col_data.isna().all()
            profile.update({
                "min_date": str(col_data.min()) if not_all_na else None,
                "max_date": str(col_data.max()) if not_all_na else None,
                "date_range_days": (col_data.max() - col_data.min()).days if not_all_na else None
            })
        
        # Sample values (non-null)
        sample = col_data.dropna().head(sample_values).tolist()
        profile["sample_values"] = [str(v) for v in sample]
        
        return profile
    
    def _detect_outliers(self, series: pd.Series) -> Dict[str, Any]:
        """Detect outliers using IQR method (vectorized, handles NaNs safely)"""
        if series.dropna().empty:
            return {"count": 0, "percentage": 0.0, "lower_bound": None, "upper_bound": None}

        q1 = series.quantile(0.25)
        q3 = series.quantile(0.75)
        iqr = q3 - q1

        lower_bound = q1 - 1.5 * iqr
        upper_bound = q3 + 1.5 * iqr

        # mask out NaNs before comparison for correct counting
        mask = (series < lower_bound) | (series > upper_bound)
        mask = mask & series.notna()
        outliers = int(mask.sum())

        non_null_count = int(series.count())
        percentage = round(outliers / non_null_count * 100, 2) if non_null_count else 0.0

        return {
            "count": outliers,
            "percentage": percentage,
            "lower_bound": round(float(lower_bound), 2),
            "upper_bound": round(float(upper_bound), 2)
        }
    
    def _quality_summary(self) -> Dict[str, Any]:
        """Overall quality assessment (vectorized computations for speed)"""
        df = self.data
        n = len(df)
        issues: List[str] = []

        if n == 0:
            return {"quality_score": self._calculate_quality_score(), "total_issues": 0, "issues": []}

        # Missing data percentages (vectorized)
        missing_pct = df.isna().mean() * 100  # Series indexed by column

        high_missing = missing_pct[missing_pct > 50]
        moderate_missing = missing_pct[(missing_pct > 20) & (missing_pct <= 50)]

        for col, pct in high_missing.items():
            issues.append(f"High missing data in '{col}': {pct:.1f}%")
        for col, pct in moderate_missing.items():
            issues.append(f"Moderate missing data in '{col}': {pct:.1f}%")

        # Unique counts (vectorized)
        nunique = df.nunique(dropna=True)  # faster than calling per-column
        object_cols = df.select_dtypes(include=['object']).columns

        # Low cardinality (object columns)
        if len(object_cols):
            low_card = nunique.loc[object_cols][nunique.loc[object_cols] == 1]
            for col in low_card.index:
                issues.append(f"Column '{col}' has only one unique value")

        # High cardinality (possible ID columns)
        high_card = nunique[nunique == n]
        for col in high_card.index:
            issues.append(f"Column '{col}' has all unique values (potential ID column)")

        return {
            "quality_score": self._calculate_quality_score(),
            "total_issues": len(issues),
            "issues": issues[:20]  # Top 20 issues
        }
    
    def _calculate_quality_score(self) -> float:
        """Calculate overall quality score (0-100)"""
        scores = []
        
        # Completeness score
        completeness = (1 - self.data.isna().sum().sum() / (len(self.data) * len(self.data.columns))) * 100
        scores.append(completeness)
        
        # Uniqueness score (for potential ID columns)
        unique_scores = []
        for col in self.data.columns:
            if self.data[col].dtype in ['int64', 'object']:
                unique_pct = self.data[col].nunique() / len(self.data)
                if 0.8 < unique_pct < 1.0:  # High but not perfect uniqueness
                    unique_scores.append(100)
        if unique_scores:
            scores.append(np.mean(unique_scores))
        
        # Duplicate score
        dup_score = (1 - self.data.duplicated().sum() / len(self.data)) * 100
        scores.append(dup_score)
        
        return round(np.mean(scores), 2)
    
    def _profile_correlations(self) -> Dict[str, Any]:
        """Calculate correlations for numeric columns"""
        numeric_cols = self.data.select_dtypes(include=[np.number]).columns
        
        if len(numeric_cols) < 2:
            return {"message": "Insufficient numeric columns for correlation analysis"}
        
        corr_matrix = self.data[numeric_cols].corr()
        
        # Find high correlations
        high_corr = []
        for i in range(len(corr_matrix.columns)):
            for j in range(i + 1, len(corr_matrix.columns)):
                corr_val = corr_matrix.iloc[i, j]
                if abs(corr_val) > 0.7:
                    high_corr.append({
                        "column1": corr_matrix.columns[i],
                        "column2": corr_matrix.columns[j],
                        "correlation": round(float(corr_val), 3)
                    })
        
        return {
            "numeric_columns": len(numeric_cols),
            "high_correlations": sorted(high_corr, key=lambda x: abs(x['correlation']), reverse=True)[:10]
        }
    
    def _generate_recommendations(self) -> List[str]:
        """Generate actionable recommendations (single-pass per-column analysis)"""
        df = self.data
        n = len(df)
        if n == 0:
            return []

        recommendations: List[str] = []

        # Precompute useful stats vectorized
        nunique = df.nunique(dropna=True)
        dtypes = df.dtypes.astype(str)

        for col in df.columns:
            col_lower = col.lower()
            col_nunique = int(nunique.get(col, 0))
            col_dtype = dtypes.get(col, "object")

            # ID detection
            if col_nunique == n:
                recommendations.append(f"Column '{col}' appears to be an ID - consider using as index")

            # Healthcare-specific recommendations
            if 'date' in col_lower and col_dtype == 'object':
                recommendations.append(f"Convert '{col}' to datetime format")
            if 'mrn' in col_lower or 'patient_id' in col_lower:
                recommendations.append(f"Validate medical record numbers in '{col}'")
            if 'icd' in col_lower or 'diagnosis' in col_lower:
                recommendations.append(f"Validate ICD codes in '{col}'")

        # Keep top 15 recommendations
        return recommendations[:15]

    def to_dict(self) -> Dict[str, Any]:
        """Get profile as dictionary"""
        if not self.profile:
            self.generate_profile()
        return self.profile
    
    def to_dataframe(self) -> pd.DataFrame:
        """Convert column profiles to DataFrame"""
        if not self.profile:
            self.generate_profile()
        
        return pd.DataFrame(self.profile['columns']).T
    
    def print_summary(self) -> None:
        """Print formatted summary"""
        if not self.profile:
            self.generate_profile()
        
        print(f"\n{'='*60}")
        print(f"DATA PROFILE: {self.profile['metadata']['name']}")
        print(f"{'='*60}\n")
        
        print(f"Dataset Shape: {self.profile['metadata']['rows']:,} rows × {self.profile['metadata']['columns']} columns")
        print(f"Memory Usage: {self.profile['metadata']['memory_usage_mb']} MB")
        print(f"Quality Score: {self.profile['quality_summary']['quality_score']}/100\n")
        
        print(f"Missing Data: {self.profile['overview']['missing_percentage']}%")
        print(f"Duplicate Rows: {self.profile['overview']['duplicate_rows']:,}")
        print(f"\n{'='*60}")
        print("RECOMMENDATIONS")
        print(f"{'='*60}\n")
        
        for i, rec in enumerate(self.profile['recommendations'], 1):
            print(f"{i}. {rec}")
        
        print(f"\n{'='*60}\n")

