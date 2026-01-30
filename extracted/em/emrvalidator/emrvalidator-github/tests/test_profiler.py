"""
Tests for DataProfiler class
"""

import pytest
import pandas as pd
import numpy as np
from emrvalidator import DataProfiler


@pytest.fixture
def sample_data():
    """Create sample dataset for profiling"""
    np.random.seed(42)
    n = 100
    
    data = {
        'patient_id': range(1, n + 1),
        'age': np.random.randint(18, 90, n),
        'gender': np.random.choice(['M', 'F'], n),
        'charge': np.random.uniform(1000, 50000, n),
        'date': pd.date_range('2023-01-01', periods=n),
    }
    
    df = pd.DataFrame(data)
    # Add some nulls
    df.loc[0:4, 'age'] = np.nan
    
    return df


class TestDataProfiler:
    """Test DataProfiler functionality"""
    
    def test_initialization(self, sample_data):
        """Test profiler initialization"""
        profiler = DataProfiler(sample_data, "Test Profile")
        assert profiler.name == "Test Profile"
        assert profiler.data is not None
        assert len(profiler.profile) == 0
    
    def test_generate_profile(self, sample_data):
        """Test profile generation"""
        profiler = DataProfiler(sample_data, "Test")
        profile = profiler.generate_profile()
        
        assert 'metadata' in profile
        assert 'overview' in profile
        assert 'columns' in profile
        assert 'quality_summary' in profile
        assert 'recommendations' in profile
    
    def test_metadata(self, sample_data):
        """Test metadata generation"""
        profiler = DataProfiler(sample_data, "Test")
        profile = profiler.generate_profile()
        
        metadata = profile['metadata']
        assert metadata['rows'] == 100
        assert metadata['columns'] == 5
        assert 'memory_usage_mb' in metadata
    
    def test_overview(self, sample_data):
        """Test overview statistics"""
        profiler = DataProfiler(sample_data, "Test")
        profile = profiler.generate_profile()
        
        overview = profile['overview']
        assert 'total_cells' in overview
        assert 'total_missing' in overview
        assert 'missing_percentage' in overview
        assert overview['total_cells'] == 500  # 100 rows * 5 columns
    
    def test_column_profiling(self, sample_data):
        """Test column-level profiling"""
        profiler = DataProfiler(sample_data, "Test")
        profile = profiler.generate_profile()
        
        columns = profile['columns']
        assert len(columns) == 5
        
        # Check numeric column
        age_profile = columns['age']
        assert 'mean' in age_profile
        assert 'std' in age_profile
        assert 'min' in age_profile
        assert 'max' in age_profile
        assert age_profile['missing'] == 5
        
        # Check categorical column
        gender_profile = columns['gender']
        assert 'top_values' in gender_profile
        assert 'most_common' in gender_profile
    
    def test_quality_score(self, sample_data):
        """Test quality score calculation"""
        profiler = DataProfiler(sample_data, "Test")
        profile = profiler.generate_profile()
        
        quality_score = profile['quality_summary']['quality_score']
        assert 0 <= quality_score <= 100
        assert isinstance(quality_score, (int, float))
    
    def test_recommendations(self, sample_data):
        """Test recommendations generation"""
        profiler = DataProfiler(sample_data, "Test")
        profile = profiler.generate_profile()
        
        recommendations = profile['recommendations']
        assert isinstance(recommendations, list)
    
    def test_to_dataframe(self, sample_data):
        """Test converting profile to DataFrame"""
        profiler = DataProfiler(sample_data, "Test")
        profiler.generate_profile()
        
        df = profiler.to_dataframe()
        assert isinstance(df, pd.DataFrame)
        assert len(df) == 5  # 5 columns
    
    def test_empty_dataframe(self):
        """Test profiling empty DataFrame"""
        empty_df = pd.DataFrame()
        profiler = DataProfiler(empty_df, "Empty")
        profile = profiler.generate_profile()
        
        assert profile['metadata']['rows'] == 0
        assert profile['metadata']['columns'] == 0


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
