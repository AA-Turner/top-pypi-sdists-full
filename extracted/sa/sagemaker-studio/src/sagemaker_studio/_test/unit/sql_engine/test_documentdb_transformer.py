from unittest.mock import patch

import pytest

from sagemaker_studio.sql_engine.documentdb_transformer import DocumentDBTransformer


class TestDocumentDBTransformer:
    """Test suite for DocumentDBTransformer."""

    def test_get_dialect_returns_none(self):
        assert DocumentDBTransformer.get_dialect() is None

    def test_get_required_fields(self):
        assert DocumentDBTransformer.get_required_fields() == ["host", "port", "database"]

    def test_get_loggers(self):
        assert DocumentDBTransformer.get_loggers() == ["pymongo", "pymongosql"]

    def test_iam_auth_connection_string(self):
        connection_data = {
            "host": "docdb-cluster.us-west-2.docdb.amazonaws.com",
            "port": 27017,
            "database": "mydb",
            "auth_mechanism": "MONGODB-AWS",
            "tls": True,
        }
        result = DocumentDBTransformer.to_sqlalchemy_config(connection_data)
        conn_str = result["connection_string"]

        assert conn_str.startswith(
            "mongodb://docdb-cluster.us-west-2.docdb.amazonaws.com:27017/mydb?"
        )
        assert "authMechanism=MONGODB-AWS" in conn_str
        assert "authSource=%24external" in conn_str
        assert "retryWrites=false" in conn_str
        assert "replicaSet=rs0" in conn_str
        assert "readPreference=secondaryPreferred" in conn_str
        assert "tls=true" in conn_str

    def test_basic_auth_connection_string(self):
        connection_data = {
            "host": "docdb-cluster.us-west-2.docdb.amazonaws.com",
            "port": 27017,
            "database": "mydb",
            "auth_mechanism": None,
            "user": "admin",
            "password": "secret123",
            "tls": True,
        }
        result = DocumentDBTransformer.to_sqlalchemy_config(connection_data)
        conn_str = result["connection_string"]

        assert conn_str.startswith(
            "mongodb://admin:secret123@docdb-cluster.us-west-2.docdb.amazonaws.com:27017/mydb?"
        )
        assert "retryWrites=false" in conn_str
        assert "replicaSet=rs0" in conn_str
        assert "readPreference=secondaryPreferred" in conn_str
        assert "tls=true" in conn_str
        assert "authMechanism" not in conn_str

    def test_basic_auth_url_encodes_special_characters(self):
        connection_data = {
            "host": "docdb-cluster.us-west-2.docdb.amazonaws.com",
            "port": 27017,
            "database": "mydb",
            "auth_mechanism": None,
            "user": "user@domain",
            "password": "p@ss:word/123",
            "tls": True,
        }
        result = DocumentDBTransformer.to_sqlalchemy_config(connection_data)
        conn_str = result["connection_string"]

        # Special characters should be URL-encoded
        assert "user%40domain" in conn_str
        assert "p%40ss%3Aword%2F123" in conn_str

    def test_tls_disabled(self):
        connection_data = {
            "host": "docdb-cluster.local",
            "port": 27017,
            "database": "mydb",
            "auth_mechanism": None,
            "user": "admin",
            "password": "pass",
            "tls": False,
        }
        result = DocumentDBTransformer.to_sqlalchemy_config(connection_data)
        conn_str = result["connection_string"]

        assert "tls=true" not in conn_str

    def test_raises_if_missing_required_fields(self):
        with patch.object(
            DocumentDBTransformer,
            "validate_required_fields",
            side_effect=ValueError("Missing required fields: host"),
        ):
            with pytest.raises(ValueError):
                DocumentDBTransformer.to_sqlalchemy_config({})
