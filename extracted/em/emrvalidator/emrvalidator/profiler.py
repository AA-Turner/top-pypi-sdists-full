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
        
        return {
            "total_cells": len(self.data) * len(self.data.columns),
            "total_missing": int(self.data.isna().sum().sum()),
            "missing_percentage": round(self.data.isna().sum().sum() / (len(self.data) * len(self.data.columns)) * 100, 2),
            "duplicate_rows": int(duplicate_rows),
            "duplicate_percentage": round(duplicate_rows / len(self.data) * 100, 2),
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
        
        profile = {
            "dtype": str(col_data.dtype),
            "count": int(col_data.count()),
            "missing": int(col_data.isna().sum()),
            "missing_percentage": round(col_data.isna().sum() / len(col_data) * 100, 2),
            "unique_values": int(col_data.nunique()),
            "unique_percentage": round(col_data.nunique() / len(col_data) * 100, 2)
        }
        
        # Numeric columns
        if pd.api.types.is_numeric_dtype(col_data):
            profile.update({
                "mean": round(float(col_data.mean()), 2) if not col_data.isna().all() else None,
                "std": round(float(col_data.std()), 2) if not col_data.isna().all() else None,
                "min": round(float(col_data.min()), 2) if not col_data.isna().all() else None,
                "max": round(float(col_data.max()), 2) if not col_data.isna().all() else None,
                "median": round(float(col_data.median()), 2) if not col_data.isna().all() else None,
                "q25": round(float(col_data.quantile(0.25)), 2) if not col_data.isna().all() else None,
                "q75": round(float(col_data.quantile(0.75)), 2) if not col_data.isna().all() else None,
                "zeros": int((col_data == 0).sum()),
                "negative": int((col_data < 0).sum()),
                "outliers": self._detect_outliers(col_data)
            })
        
        # Categorical/Object columns
        elif pd.api.types.is_object_dtype(col_data) or pd.api.types.is_categorical_dtype(col_data):
            value_counts = col_data.value_counts()
            profile.update({
                "top_values": value_counts.head(sample_values).to_dict(),
                "most_common": str(value_counts.index[0]) if len(value_counts) > 0 else None,
                "most_common_count": int(value_counts.iloc[0]) if len(value_counts) > 0 else 0,
                "min_length": int(col_data.astype(str).str.len().min()) if not col_data.isna().all() else None,
                "max_length": int(col_data.astype(str).str.len().max()) if not col_data.isna().all() else None,
                "avg_length": round(float(col_data.astype(str).str.len().mean()), 2) if not col_data.isna().all() else None
            })
        
        # DateTime columns
        elif pd.api.types.is_datetime64_any_dtype(col_data):
            profile.update({
                "min_date": str(col_data.min()) if not col_data.isna().all() else None,
                "max_date": str(col_data.max()) if not col_data.isna().all() else None,
                "date_range_days": (col_data.max() - col_data.min()).days if not col_data.isna().all() else None
            })
        
        # Sample values (non-null)
        sample = col_data.dropna().head(sample_values).tolist()
        profile["sample_values"] = [str(v) for v in sample]
        
        return profile
    
    def _detect_outliers(self, series: pd.Series) -> Dict[str, Any]:
        """Detect outliers using IQR method"""
        q1 = series.quantile(0.25)
        q3 = series.quantile(0.75)
        iqr = q3 - q1
        
        lower_bound = q1 - 1.5 * iqr
        upper_bound = q3 + 1.5 * iqr
        
        outliers = ((series < lower_bound) | (series > upper_bound)).sum()
        
        return {
            "count": int(outliers),
            "percentage": round(outliers / len(series) * 100, 2),
            "lower_bound": round(float(lower_bound), 2),
            "upper_bound": round(float(upper_bound), 2)
        }
    
    def _quality_summary(self) -> Dict[str, Any]:
        """Overall quality assessment"""
        issues = []
        
        # Check for high missing data
        for col in self.data.columns:
            missing_pct = self.data[col].isna().sum() / len(self.data) * 100
            if missing_pct > 50:
                issues.append(f"High missing data in '{col}': {missing_pct:.1f}%")
            elif missing_pct > 20:
                issues.append(f"Moderate missing data in '{col}': {missing_pct:.1f}%")
        
        # Check for low cardinality in object columns
        for col in self.data.select_dtypes(include=['object']).columns:
            if self.data[col].nunique() == 1:
                issues.append(f"Column '{col}' has only one unique value")
        
        # Check for high cardinality
        for col in self.data.columns:
            if self.data[col].nunique() == len(self.data):
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
        """Generate actionable recommendations"""
        recommendations = []
        
        # Missing data recommendations
        for col in self.data.columns:
            missing_pct = self.data[col].isna().sum() / len(self.data) * 100
            if missing_pct > 50:
                recommendations.append(f"Consider dropping column '{col}' due to {missing_pct:.1f}% missing data")
            elif missing_pct > 20:
                recommendations.append(f"Investigate missing data in '{col}' ({missing_pct:.1f}%)")
        
        # Duplicate recommendations
        dup_count = self.data.duplicated().sum()
        if dup_count > 0:
            recommendations.append(f"Remove {dup_count} duplicate rows")
        
        # Data type recommendations
        for col in self.data.select_dtypes(include=['object']).columns:
            if self.data[col].nunique() / len(self.data) > 0.95:
                recommendations.append(f"Column '{col}' appears to be an ID - consider using as index")
        
        # Healthcare-specific recommendations
        for col in self.data.columns:
            col_lower = col.lower()
            if 'date' in col_lower and self.data[col].dtype == 'object':
                recommendations.append(f"Convert '{col}' to datetime format")
            elif 'mrn' in col_lower or 'patient_id' in col_lower:
                recommendations.append(f"Validate medical record numbers in '{col}'")
            elif 'icd' in col_lower or 'diagnosis' in col_lower:
                recommendations.append(f"Validate ICD codes in '{col}'")
        
        return recommendations[:15]  # Top 15 recommendations
    
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
