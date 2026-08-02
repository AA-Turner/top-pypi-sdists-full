"""
Tests for DataValidator class
"""

import pytest
import pandas as pd
import numpy as np
from emrvalidator import DataValidator


@pytest.fixture
def sample_data():
    """Create sample healthcare dataset for testing"""
    np.random.seed(42)
    n = 100
    
    data = {
        'mrn': [f"MRN{str(i).zfill(8)}" for i in range(n)],
        'patient_id': range(1, n + 1),
        'age': np.random.randint(18, 90, n),
        'gender': np.random.choice(['M', 'F', 'Other'], n),
        'icd10_code': np.random.choice(['I10', 'E11.9', 'J44.0'], n),
        'charge_amount': np.random.uniform(1000, 50000, n),
    }
    
    df = pd.DataFrame(data)
    # Add some nulls
    df.loc[0:4, 'age'] = np.nan
    
    return df


class TestDataValidator:
    """Test DataValidator functionality"""
    
    def test_initialization(self):
        """Test validator initialization"""
        validator = DataValidator("Test")
        assert validator.name == "Test"
        assert validator.data is None
        assert len(validator.validation_results) == 0
    
    def test_load_data(self, sample_data):
        """Test data loading"""
        validator = DataValidator("Test")
        validator.load_data(sample_data)
        
        assert validator.data is not None
        assert len(validator.data) == 100
        assert validator.metadata['total_rows'] == 100
        assert validator.metadata['total_columns'] == 6
    
    def test_expect_column_exists(self, sample_data):
        """Test column existence check"""
        validator = DataValidator("Test")
        validator.load_data(sample_data)
        
        # Test existing column
        validator.expect_column_exists('mrn')
        results = validator.get_results()
        assert results['summary']['passed'] == 1
        assert results['summary']['failed'] == 0
        
        # Test non-existing column
        validator.expect_column_exists('nonexistent')
        results = validator.get_results()
        assert results['summary']['failed'] == 1
    
    def test_expect_column_not_null(self, sample_data):
        """Test null value check"""
        validator = DataValidator("Test")
        validator.load_data(sample_data)
        
        # MRN should have no nulls
        validator.expect_column_not_null('mrn', threshold=1.0)
        
        # Age has 5% nulls, should pass with 0.90 threshold
        validator.expect_column_not_null('age', threshold=0.90)
        
        results = validator.get_results()
        assert results['summary']['passed'] == 2
    
    def test_expect_column_values_in_set(self, sample_data):
        """Test value set membership"""
        validator = DataValidator("Test")
        validator.load_data(sample_data)
        
        validator.expect_column_values_in_set('gender', {'M', 'F', 'Other'})
        
        results = validator.get_results()
        assert results['summary']['passed'] == 1
    
    def test_expect_column_values_between(self, sample_data):
        """Test numeric range validation"""
        validator = DataValidator("Test")
        validator.load_data(sample_data)
        
        validator.expect_column_values_between('age', 0, 120, threshold=0.90)
        validator.expect_column_values_between('charge_amount', 0, 100000)
        
        results = validator.get_results()
        assert results['summary']['passed'] == 2
    
    def test_expect_column_values_unique(self, sample_data):
        """Test uniqueness check"""
        validator = DataValidator("Test")
        validator.load_data(sample_data)
        
        # patient_id should be unique
        validator.expect_column_values_unique('patient_id', threshold=1.0)
        
        # gender should not be unique
        validator.expect_column_values_unique('gender', threshold=1.0)
        
        results = validator.get_results()
        assert results['summary']['passed'] == 1
        assert results['summary']['failed'] == 1
    
    def test_expect_mrn_format(self, sample_data):
        """Test MRN format validation"""
        validator = DataValidator("Test")
        validator.load_data(sample_data)
        
        validator.expect_mrn_format('mrn')
        
        results = validator.get_results()
        assert results['summary']['passed'] == 1
    
    def test_expect_icd_format(self, sample_data):
        """Test ICD code format validation"""
        validator = DataValidator("Test")
        validator.load_data(sample_data)
        
        validator.expect_icd_format('icd10_code', version=10)
        
        results = validator.get_results()
        assert results['summary']['passed'] == 1
    
    def test_custom_validation(self, sample_data):
        """Test custom validation function"""
        validator = DataValidator("Test")
        validator.load_data(sample_data)
        
        def custom_check(df, **kwargs):
            passed = len(df) == 100
            return passed, "Row count check", {"count": len(df)}
        
        validator.expect_custom("row_count", custom_check)
        
        results = validator.get_results()
        assert results['summary']['passed'] == 1
    
    def test_method_chaining(self, sample_data):
        """Test method chaining"""
        validator = DataValidator("Test")
        
        result = (validator
            .load_data(sample_data)
            .expect_column_exists('mrn')
            .expect_column_exists('patient_id')
            .expect_column_not_null('mrn')
        )
        
        assert result is validator  # Check chaining returns self
        assert len(validator.validation_results) == 3
    
    def test_is_valid(self, sample_data):
        """Test validation status check"""
        validator = DataValidator("Test")
        validator.load_data(sample_data)
        
        validator.expect_column_exists('mrn')  # Should pass
        assert validator.is_valid() is True
        
        validator.expect_column_exists('nonexistent')  # Should fail
        assert validator.is_valid() is False
    
    def test_get_failed_validations(self, sample_data):
        """Test getting failed validations"""
        validator = DataValidator("Test")
        validator.load_data(sample_data)
        
        validator.expect_column_exists('mrn')  # Pass
        validator.expect_column_exists('nonexistent')  # Fail
        validator.expect_column_not_null('age', threshold=1.0)  # Fail
        
        failed = validator.get_failed_validations()
        assert len(failed) == 2
    
    def test_to_dataframe(self, sample_data):
        """Test converting results to DataFrame"""
        validator = DataValidator("Test")
        validator.load_data(sample_data)
        
        validator.expect_column_exists('mrn')
        validator.expect_column_not_null('age')
        
        results_df = validator.to_dataframe()
        assert isinstance(results_df, pd.DataFrame)
        assert len(results_df) == 2
        assert 'rule' in results_df.columns
        assert 'passed' in results_df.columns


class TestDataValidatorEdgeCases:
    """Test edge cases and error handling"""
    
    def test_validation_before_loading_data(self):
        """Test validation fails gracefully without data"""
        validator = DataValidator("Test")
        
        with pytest.raises(AttributeError):
            validator.expect_column_exists('mrn')
    
    def test_empty_dataframe(self):
        """Test with empty DataFrame"""
        validator = DataValidator("Test")
        empty_df = pd.DataFrame()
        validator.load_data(empty_df)
        
        assert validator.metadata['total_rows'] == 0
        assert validator.metadata['total_columns'] == 0
    
    def test_threshold_values(self, sample_data):
        """Test threshold boundary values"""
        validator = DataValidator("Test")
        validator.load_data(sample_data)
        
        # Test with threshold 0.0
        validator.expect_column_not_null('age', threshold=0.0)
        
        # Test with threshold 1.0
        validator.expect_column_not_null('mrn', threshold=1.0)
        
        results = validator.get_results()
        assert results['summary']['passed'] == 2


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
