import os
import pandas as pd
import pytest
from pathlib import Path
import tempfile

from dotenv import load_dotenv

from canonmap import MySQLConnectorConfig, MySQLConnectionMethod, MySQLConnector
from canonmap.connectors.mysql_connector.managers.table_manager.validators.requests import CreateTableRequest, Database, IfExists
from canonmap.connectors.mysql_connector.managers.table_manager.utils.create_table_from_data import _convert_boolean_values, _identify_boolean_columns

load_dotenv(override=True)

# Test credentials
MYSQL_USER = os.getenv("DB_USER", "root")
MYSQL_PASSWORD = os.getenv("DB_PASSWORD", "")
MYSQL_HOST = os.getenv("DB_HOST", "127.0.0.1")
MYSQL_PORT = int(os.getenv("DB_PORT", "3306"))

@pytest.fixture
def mysql_config():
    return MySQLConnectorConfig(
        user=MYSQL_USER,
        password=MYSQL_PASSWORD,
        host=MYSQL_HOST,
        port=MYSQL_PORT,
        connection_method=MySQLConnectionMethod.TCP,
        autocommit=True,
    )

@pytest.fixture
def connector(mysql_config):
    connector = MySQLConnector(mysql_config)
    connector.connect()
    yield connector
    connector.close()

class TestBooleanConversion:
    """Test the boolean conversion functionality for Yes/No fields."""
    
    def test_convert_boolean_values(self):
        """Test the _convert_boolean_values function."""
        # Test true values
        assert _convert_boolean_values("Yes") == 1
        assert _convert_boolean_values("yes") == 1
        assert _convert_boolean_values("Y") == 1
        assert _convert_boolean_values("y") == 1
        assert _convert_boolean_values("True") == 1
        assert _convert_boolean_values("true") == 1
        assert _convert_boolean_values("T") == 1
        assert _convert_boolean_values("t") == 1
        assert _convert_boolean_values("1") == 1
        assert _convert_boolean_values(1) == 1
        
        # Test false values
        assert _convert_boolean_values("No") == 0
        assert _convert_boolean_values("no") == 0
        assert _convert_boolean_values("N") == 0
        assert _convert_boolean_values("n") == 0
        assert _convert_boolean_values("False") == 0
        assert _convert_boolean_values("false") == 0
        assert _convert_boolean_values("F") == 0
        assert _convert_boolean_values("f") == 0
        assert _convert_boolean_values("0") == 0
        assert _convert_boolean_values(0) == 0
        
        # Test non-boolean values (should return as-is)
        assert _convert_boolean_values("Hello") == "Hello"
        assert _convert_boolean_values("123") == "123"
        assert _convert_boolean_values(42) == 42
        assert _convert_boolean_values("") == ""
        
        # Test None and NaN values
        assert _convert_boolean_values(None) is None
        assert _convert_boolean_values(pd.NA) is None
    
    def test_identify_boolean_columns(self):
        """Test the _identify_boolean_columns function."""
        # Test with DataFrame containing boolean columns
        df = pd.DataFrame({
            'name': ['John', 'Jane', 'Bob'],
            'is_active': ['Yes', 'No', 'Yes'],
            'has_permission': ['True', 'False', 'True'],
            'export_warning_needed': ['No', 'Yes', 'No'],
            'age': [25, 30, 35],
            'status': ['Active', 'Inactive', 'Active']
        })
        
        boolean_columns = _identify_boolean_columns(df)
        expected_columns = {'is_active', 'has_permission', 'export_warning_needed'}
        assert boolean_columns == expected_columns
        
        # Test with list of dicts
        data_list = [
            {'name': 'John', 'is_active': 'Yes', 'age': 25},
            {'name': 'Jane', 'is_active': 'No', 'age': 30}
        ]
        
        boolean_columns = _identify_boolean_columns(data_list)
        expected_columns = {'is_active'}
        assert boolean_columns == expected_columns
        
        # Test with CSV file
        with tempfile.NamedTemporaryFile(mode='w', suffix='.csv', delete=False) as f:
            f.write("name,is_active,age\n")
            f.write("John,Yes,25\n")
            f.write("Jane,No,30\n")
            csv_path = f.name
        
        try:
            boolean_columns = _identify_boolean_columns(csv_path)
            expected_columns = {'is_active'}
            assert boolean_columns == expected_columns
        finally:
            os.unlink(csv_path)
    
    def test_create_table_with_boolean_data(self, connector):
        """Test creating a table with Yes/No data that should be converted to TINYINT(1)."""
        # Create test data with Yes/No fields
        test_data = [
            {'name': 'John', 'is_active': 'Yes', 'export_warning_needed': 'No', 'age': 25},
            {'name': 'Jane', 'is_active': 'No', 'export_warning_needed': 'Yes', 'age': 30},
            {'name': 'Bob', 'is_active': 'Yes', 'export_warning_needed': 'No', 'age': 35}
        ]
        
        # Create a test database
        test_db_name = "test_boolean_db"
        connector.run_query(f"CREATE DATABASE IF NOT EXISTS `{test_db_name}`")
        
        try:
            # Create table request
            request = CreateTableRequest(
                name="test_boolean_table",
                database=Database(name=test_db_name),
                if_exists=IfExists.REPLACE,
                autoconnect=True,
                data=test_data
            )
            
            # Import and use TableManager
            from canonmap.connectors.mysql_connector.managers.table_manager.table_manager import TableManager
            table_manager = TableManager(connector)
            
            # Create table from data
            result = table_manager.create_table(request)
            
            # Verify the table was created successfully
            assert result["action"] == "created"
            assert result["rows_inserted"] == 3
            
            # Query the table to verify the data was inserted correctly
            rows = connector.run_query(f"SELECT * FROM `{test_db_name}`.`test_boolean_table` ORDER BY name")
            
            # Check that boolean fields were converted to 1/0
            assert len(rows) == 3
            
            # Check John's data
            john_row = next(row for row in rows if row['name'] == 'John')
            assert john_row['is_active'] == 1  # 'Yes' should be converted to 1
            assert john_row['export_warning_needed'] == 0  # 'No' should be converted to 0
            assert john_row['age'] == 25
            
            # Check Jane's data
            jane_row = next(row for row in rows if row['name'] == 'Jane')
            assert jane_row['is_active'] == 0  # 'No' should be converted to 0
            assert jane_row['export_warning_needed'] == 1  # 'Yes' should be converted to 1
            assert jane_row['age'] == 30
            
            # Check Bob's data
            bob_row = next(row for row in rows if row['name'] == 'Bob')
            assert bob_row['is_active'] == 1  # 'Yes' should be converted to 1
            assert bob_row['export_warning_needed'] == 0  # 'No' should be converted to 0
            assert bob_row['age'] == 35
            
        finally:
            # Clean up
            connector.run_query(f"DROP DATABASE IF EXISTS `{test_db_name}`") 