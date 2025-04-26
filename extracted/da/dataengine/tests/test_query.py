import os
import pytest
from unittest.mock import patch
from dataengine import query

DIRNAME = os.path.dirname(os.path.realpath(__file__))
TEST_SQL_PATH = os.path.join(DIRNAME, "sql/test_query.sql")

# Mock BaseDataset Inputs
@pytest.fixture
def valid_base_query_data():
    return {
        "asset_name": "TestQuery",
        "description": "This is a test query.",
        "dirname": DIRNAME,
        "sql_info": {"filename": TEST_SQL_PATH},
        "output": "result.csv",
        "file_format": "csv",
        "separator": ",",
        "use_pandas": True,
        "header": True,
        "dependencies": [
            {
                "table_name": "test_table",
                "base_dataset": "test_base_dataset"
            }
        ],
    }

def test_base_query(valid_base_query_data):
    """
    Test the BaseQuery class.
    """
    schema = query.BaseQuerySchema()
    result = schema.load(valid_base_query_data)
    assert isinstance(result, query.BaseQuery)
    assert result.asset_name == "TestQuery"
    assert result.output == "result.csv"
    assert result.description == "This is a test query."

def test_query(valid_base_query_data):
    """
    Test the Query class.
    """
    schema = query.BaseQuerySchema()
    base_query = schema.load(valid_base_query_data)
    query_object = query.Query.from_base_query(base_query)
    assert isinstance(query_object, query.Query)
    assert query_object.sql == open(TEST_SQL_PATH, "r").read()
