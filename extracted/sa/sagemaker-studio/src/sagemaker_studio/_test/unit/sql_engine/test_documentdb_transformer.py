from unittest.mock import patch

import pytest
from sqlalchemy import make_url
from sqlalchemy.engine import URL

from sagemaker_studio.sql_engine.documentdb_transformer import DocumentDBTransformer


def _rendered(config):
    """Render the returned connection URL to a full string (password visible)."""
    url = config["connection_string"]
    assert isinstance(url, URL)
    return url.render_as_string(hide_password=False)


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
        url = DocumentDBTransformer.to_sqlalchemy_config(connection_data)["connection_string"]

        assert url.drivername == "mongodb"
        assert url.host == "docdb-cluster.us-west-2.docdb.amazonaws.com"
        assert url.port == 27017
        assert url.database == "mydb"
        assert url.username is None
        assert url.password is None
        # Query options carry the intended values.
        assert url.query["authMechanism"] == "MONGODB-AWS"
        assert url.query["authSource"] == "$external"
        assert url.query["retryWrites"] == "false"
        assert url.query["replicaSet"] == "rs0"
        assert url.query["readPreference"] == "secondaryPreferred"
        assert url.query["tls"] == "true"

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
        url = DocumentDBTransformer.to_sqlalchemy_config(connection_data)["connection_string"]

        assert url.username == "admin"
        assert url.password == "secret123"
        assert url.host == "docdb-cluster.us-west-2.docdb.amazonaws.com"
        assert url.port == 27017
        assert url.database == "mydb"
        assert url.query["retryWrites"] == "false"
        assert url.query["replicaSet"] == "rs0"
        assert url.query["readPreference"] == "secondaryPreferred"
        assert url.query["tls"] == "true"
        assert "authMechanism" not in url.query

    def test_basic_auth_encodes_special_characters(self):
        connection_data = {
            "host": "docdb-cluster.us-west-2.docdb.amazonaws.com",
            "port": 27017,
            "database": "mydb",
            "auth_mechanism": None,
            "user": "user@domain",
            "password": "p@ss:word/123",
            "tls": True,
        }
        config = DocumentDBTransformer.to_sqlalchemy_config(connection_data)
        rendered = _rendered(config)

        # The raw (unencoded) credential separators must not leak into the URI,
        # otherwise they would corrupt parsing.
        assert "user@domain" not in rendered
        assert "p@ss:word/123" not in rendered

        # Re-parsing the rendered URL yields back the exact original credentials.
        parsed = make_url(rendered)
        assert parsed.username == "user@domain"
        assert parsed.password == "p@ss:word/123"

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
        url = DocumentDBTransformer.to_sqlalchemy_config(connection_data)["connection_string"]
        assert "tls" not in url.query

    def test_string_port_is_coerced_to_int(self):
        connection_data = {
            "host": "docdb-cluster.local",
            "port": "27017",
            "database": "mydb",
            "auth_mechanism": "MONGODB-AWS",
            "tls": True,
        }
        url = DocumentDBTransformer.to_sqlalchemy_config(connection_data)["connection_string"]
        assert url.port == 27017

    def test_raises_if_missing_required_fields(self):
        with patch.object(
            DocumentDBTransformer,
            "validate_required_fields",
            side_effect=ValueError("Missing required fields: host"),
        ):
            with pytest.raises(ValueError):
                DocumentDBTransformer.to_sqlalchemy_config({})


class TestDocumentDBTransformerInjection:
    """URL.create() must neutralize connection-string injection via host/database."""

    def test_malicious_host_cannot_override_security_options(self):
        # A crafted HOST that tries to inject tls=false / authMechanism=PLAIN
        # ahead of the hardcoded options must NOT alter the query we control.
        connection_data = {
            "host": "attacker.com/?tls=false&authMechanism=PLAIN&fake=",
            "port": 27017,
            "database": "mydb",
            "auth_mechanism": "MONGODB-AWS",
            "tls": True,
        }
        config = DocumentDBTransformer.to_sqlalchemy_config(connection_data)
        url = config["connection_string"]

        # Our security options are intact and unaffected by the injection.
        assert url.query["tls"] == "true"
        assert url.query["authMechanism"] == "MONGODB-AWS"
        assert url.query["authSource"] == "$external"
        # No injected keys leaked into the query.
        assert "fake" not in url.query
        assert set(url.query.keys()) == {
            "retryWrites",
            "replicaSet",
            "readPreference",
            "tls",
            "authMechanism",
            "authSource",
        }

        # create_engine consumes this URL object directly — it uses the parsed
        # components (host, database, query) and never re-serializes then
        # re-parses a string. So url.query above is authoritative, and the
        # payload stays confined to the opaque host token; it can never become
        # a query option that reaches the driver.
        assert url.host == "attacker.com/?tls=false&authMechanism=PLAIN&fake="

    def test_malicious_database_cannot_inject_options(self):
        connection_data = {
            "host": "docdb-cluster.us-west-2.docdb.amazonaws.com",
            "port": 27017,
            "database": "mydb?tls=false&x=1",
            "auth_mechanism": "MONGODB-AWS",
            "tls": True,
        }
        config = DocumentDBTransformer.to_sqlalchemy_config(connection_data)
        url = config["connection_string"]

        assert url.query["tls"] == "true"
        assert "x" not in url.query
        # The payload stays confined to the database component; it is not parsed
        # as query options. url.query above is authoritative for the URL object
        # that create_engine consumes.
        assert url.database == "mydb?tls=false&x=1"

    def test_basic_auth_password_cannot_inject_options(self):
        # A password containing URI metacharacters must be encoded, not able to
        # break out into the query string.
        connection_data = {
            "host": "docdb-cluster.us-west-2.docdb.amazonaws.com",
            "port": 27017,
            "database": "mydb",
            "auth_mechanism": None,
            "user": "admin",
            "password": "p@ss?tls=false&evil=1",
            "tls": True,
        }
        config = DocumentDBTransformer.to_sqlalchemy_config(connection_data)
        url = config["connection_string"]

        assert url.query["tls"] == "true"
        assert "evil" not in url.query
        rendered = _rendered(config)
        assert "tls=false" not in rendered
        # Round-trip proves the password is preserved exactly.
        assert make_url(rendered).password == "p@ss?tls=false&evil=1"

    def test_legitimate_endpoints_still_work(self):
        for host in [
            "docdb-cluster.us-west-2.docdb.amazonaws.com",
            "docdb-cluster.local",
        ]:
            connection_data = {
                "host": host,
                "port": "27017",
                "database": "my_db",
                "auth_mechanism": "MONGODB-AWS",
                "tls": True,
            }
            url = DocumentDBTransformer.to_sqlalchemy_config(connection_data)["connection_string"]
            assert url.host == host
            assert url.port == 27017
            assert url.database == "my_db"
            assert url.query["tls"] == "true"
