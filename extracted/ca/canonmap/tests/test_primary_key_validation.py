import pytest
import pandas as pd
from pathlib import Path
import tempfile
import os

from canonmap.connectors.mysql_connector.managers.table_manager.utils.validate_primary_key import validate_primary_key_field


class TestPrimaryKeyValidation:
    
    def test_validate_primary_key_field_unique_dataframe(self):
        """Test validation with unique values in DataFrame"""
        data = pd.DataFrame({
            'id': [1, 2, 3, 4, 5],
            'name': ['Alice', 'Bob', 'Alice', 'David', 'Eve'],  # Duplicate name
            'email': ['alice@test.com', 'bob@test.com', 'charlie@test.com', 'david@test.com', 'eve@test.com']
        })
        
        # Test with unique field
        assert validate_primary_key_field(data, 'id') == True
        assert validate_primary_key_field(data, 'email') == True
        
        # Test with non-unique field
        assert validate_primary_key_field(data, 'name') == False
    
    def test_validate_primary_key_field_with_duplicates(self):
        """Test validation with duplicate values"""
        data = pd.DataFrame({
            'id': [1, 2, 2, 3, 4],  # Duplicate value
            'name': ['Alice', 'Bob', 'Charlie', 'David', 'Eve'],
            'email': ['alice@test.com', 'bob@test.com', 'bob@test.com', 'david@test.com', 'eve@test.com']  # Duplicate email
        })
        
        # Test with duplicate field
        assert validate_primary_key_field(data, 'id') == False
        assert validate_primary_key_field(data, 'email') == False
        assert validate_primary_key_field(data, 'name') == True
    
    def test_validate_primary_key_field_with_nulls(self):
        """Test validation with null values"""
        data = pd.DataFrame({
            'id': [1, 2, None, 4, 5],  # Null value
            'name': ['Alice', 'Bob', 'Charlie', 'David', 'Eve'],
            'email': ['alice@test.com', 'bob@test.com', '', 'david@test.com', 'eve@test.com']  # Empty string
        })
        
        # Test with null values
        assert validate_primary_key_field(data, 'id') == False
        assert validate_primary_key_field(data, 'email') == False
        assert validate_primary_key_field(data, 'name') == True
    
    def test_validate_primary_key_field_missing_column(self):
        """Test validation with non-existent column"""
        data = pd.DataFrame({
            'id': [1, 2, 3, 4, 5],
            'name': ['Alice', 'Bob', 'Charlie', 'David', 'Eve']
        })
        
        # Test with non-existent column
        assert validate_primary_key_field(data, 'non_existent') == False
    
    def test_validate_primary_key_field_list_data(self):
        """Test validation with list of dictionaries"""
        data = [
            {'id': 1, 'name': 'Alice', 'email': 'alice@test.com'},
            {'id': 2, 'name': 'Bob', 'email': 'bob@test.com'},
            {'id': 3, 'name': 'Alice', 'email': 'charlie@test.com'}  # Duplicate name
        ]
        
        # Test with unique field
        assert validate_primary_key_field(data, 'id') == True
        assert validate_primary_key_field(data, 'email') == True
        
        # Test with non-unique field
        assert validate_primary_key_field(data, 'name') == False
    
    def test_validate_primary_key_field_csv_file(self):
        """Test validation with CSV file"""
        # Create temporary CSV file
        with tempfile.NamedTemporaryFile(mode='w', suffix='.csv', delete=False) as f:
            f.write("id,name,email\n")
            f.write("1,Alice,alice@test.com\n")
            f.write("2,Bob,bob@test.com\n")
            f.write("3,Alice,charlie@test.com\n")  # Duplicate name
            temp_file = f.name
        
        try:
            # Test with unique field
            assert validate_primary_key_field(temp_file, 'id') == True
            assert validate_primary_key_field(temp_file, 'email') == True
            
            # Test with non-unique field
            assert validate_primary_key_field(temp_file, 'name') == False
        finally:
            # Clean up
            os.unlink(temp_file)
    
    def test_validate_primary_key_field_unsupported_data_type(self):
        """Test validation with unsupported data type"""
        # Test with unsupported data type
        assert validate_primary_key_field("not_a_dataframe", 'id') == False 