"""
Unit tests for OpenSearchTransformer.
"""

from unittest.mock import patch

import pytest

from sagemaker_studio.sql_engine.opensearch_transformer import OpenSearchTransformer
from sagemaker_studio.sql_engine.resource_fetching_definition import (
    FetchMode,
    SQLAlchemyMetadataAction,
)

# ---------------------------------------------------------------------------
# get_required_fields
# ---------------------------------------------------------------------------


def test_get_required_fields():
    assert OpenSearchTransformer.get_required_fields() == [
        "domain_endpoint",
        "user",
        "password",
    ]


# ---------------------------------------------------------------------------
# to_sqlalchemy_config
# ---------------------------------------------------------------------------


def test_to_sqlalchemy_config_basic():
    with patch.object(OpenSearchTransformer, "validate_required_fields") as mocked:
        connection_data = {
            "domain_endpoint": "search-my-domain.us-east-1.es.amazonaws.com",
            "user": "admin",
            "password": "Secret123",
        }
        result = OpenSearchTransformer.to_sqlalchemy_config(connection_data)

        expected = "opensearch://search-my-domain.us-east-1.es.amazonaws.com/_all"
        assert result["connection_string"] == expected
        assert result["connect_args"] == {"username": "admin", "password": "Secret123"}
        mocked.assert_called_once_with(["domain_endpoint", "user", "password"], connection_data)


def test_to_sqlalchemy_config_strips_https_prefix():
    with patch.object(OpenSearchTransformer, "validate_required_fields"):
        connection_data = {
            "domain_endpoint": "https://search-my-domain.us-east-1.es.amazonaws.com",
            "user": "admin",
            "password": "Secret123",
        }
        result = OpenSearchTransformer.to_sqlalchemy_config(connection_data)
        assert "https://" not in result["connection_string"]
        assert "search-my-domain.us-east-1.es.amazonaws.com/_all" in result["connection_string"]
        assert "admin" not in result["connection_string"]
        assert result["connect_args"]["username"] == "admin"


def test_to_sqlalchemy_config_strips_http_prefix():
    with patch.object(OpenSearchTransformer, "validate_required_fields"):
        connection_data = {
            "domain_endpoint": "http://localhost:9200",
            "user": "admin",
            "password": "admin",
        }
        result = OpenSearchTransformer.to_sqlalchemy_config(connection_data)
        assert "http://" not in result["connection_string"]
        assert result["connection_string"] == "opensearch://localhost:9200/_all"
        assert result["connect_args"] == {"username": "admin", "password": "admin"}


def test_to_sqlalchemy_config_raises_if_required_fields_missing():
    with patch.object(
        OpenSearchTransformer,
        "validate_required_fields",
        side_effect=ValueError("domain_endpoint is required for connection"),
    ):
        with pytest.raises(ValueError, match="domain_endpoint is required"):
            OpenSearchTransformer.to_sqlalchemy_config({"user": "admin", "password": "pass"})


# ---------------------------------------------------------------------------
# get_resources_action
# ---------------------------------------------------------------------------


def test_get_resources_action_database():
    plan = OpenSearchTransformer.get_resources_action("DATABASE")
    assert plan.mode is FetchMode.SQLALCHEMY_METADATA
    assert plan.sqlalchemy_action is SQLAlchemyMetadataAction.GET_SCHEMA_NAMES
    assert plan.default_type == "DATABASE"
    assert plan.children == ("TABLE",)


def test_get_resources_action_none_defaults_to_database():
    plan = OpenSearchTransformer.get_resources_action(None)
    assert plan.mode is FetchMode.SQLALCHEMY_METADATA
    assert plan.sqlalchemy_action is SQLAlchemyMetadataAction.GET_SCHEMA_NAMES
    assert plan.default_type == "DATABASE"
    assert plan.children == ("TABLE",)


def test_get_resources_action_table():
    plan = OpenSearchTransformer.get_resources_action("TABLE")
    assert plan.mode is FetchMode.SQLALCHEMY_METADATA
    assert plan.sqlalchemy_action is SQLAlchemyMetadataAction.GET_TABLE_NAMES
    assert plan.default_type == "TABLE"
    assert plan.children == ("COLUMN",)


def test_get_resources_action_column():
    plan = OpenSearchTransformer.get_resources_action("COLUMN")
    assert plan.mode is FetchMode.SQLALCHEMY_METADATA
    assert plan.sqlalchemy_action is SQLAlchemyMetadataAction.GET_COLUMN_NAMES
    assert plan.default_type == "COLUMN"
    assert plan.children == ()


def test_get_resources_action_unsupported_raises():
    with pytest.raises(ValueError, match="Unsupported resource type"):
        OpenSearchTransformer.get_resources_action("VIEW")


# ---------------------------------------------------------------------------
# get_loggers
# ---------------------------------------------------------------------------


def test_get_loggers_returns_expected_list():
    loggers = OpenSearchTransformer.get_loggers()
    assert isinstance(loggers, list)
    assert len(loggers) > 0
    assert "opensearch" in loggers
    assert "opensearchpy" in loggers
    assert "sagemaker_studio.sql_engine._sqlalchemy_opensearch" in loggers
