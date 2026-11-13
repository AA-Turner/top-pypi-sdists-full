from unittest.mock import patch

import pytest

from sagemaker_studio.sql_engine.dynamodb_transformer import DynamoDBTransformer


def test_get_required_fields():
    assert DynamoDBTransformer.get_required_fields() == ["region"]


def test_to_sqlalchemy_config_returns_expected_connection_string():
    with patch.object(DynamoDBTransformer, "validate_required_fields") as mocked:
        connection_data = {"region": "us-west-2"}
        result = DynamoDBTransformer.to_sqlalchemy_config(connection_data)
        expected = "dynamodb://@dynamodb.us-west-2.amazonaws.com:443?region_name=us-west-2"
        assert result == {"connection_string": expected}
        mocked.assert_called_once_with(["region"], connection_data)


def test_to_sqlalchemy_config_raises_if_missing_region():
    with patch.object(
        DynamoDBTransformer,
        "validate_required_fields",
        side_effect=ValueError("Missing required fields: region"),
    ):
        with pytest.raises(ValueError):
            DynamoDBTransformer.to_sqlalchemy_config({})


def test_supports_row_limit_is_false():
    assert DynamoDBTransformer.supports_row_limit is False


def test_row_limit_leaves_statement_unchanged():
    statement = "SELECT a FROM t"
    assert DynamoDBTransformer.apply_row_limit(statement, "SELECT", 100) == statement
