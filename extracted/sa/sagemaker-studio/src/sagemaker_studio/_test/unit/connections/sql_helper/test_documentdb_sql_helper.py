from dataclasses import make_dataclass

from sagemaker_studio.connections.sql_helper.documentdb_sql_helper import DocumentDBSqlHelper


def _make_connection(auth_type="BASIC", secret=None):
    """Build a minimal Connection-like object for DocumentDB tests."""
    glue_connection = make_dataclass(
        "GlueConnection",
        ["connectionProperties", "authenticationConfiguration"],
    )(
        connectionProperties={
            "HOST": "docdb-cluster.us-west-2.docdb.amazonaws.com",
            "PORT": "27017",
            "DATABASE": "mydb",
        },
        authenticationConfiguration={"authenticationType": auth_type},
    )

    return make_dataclass("Connection", ["secret", "connection_creds", "data"])(
        secret,
        make_dataclass("ConnectionCredentials", [])(),
        make_dataclass("ConnectionData", ["physical_endpoints"])(
            [
                make_dataclass("PhysicalEndpoint", ["awsLocation", "glueConnection"])(
                    awsLocation={"awsRegion": "us-west-2"},
                    glueConnection=glue_connection,
                )
            ]
        ),
    )


class TestDocumentDBSqlHelper:
    """Test suite for DocumentDBSqlHelper."""

    def test_iam_auth_returns_mongodb_aws_mechanism(self):
        connection = _make_connection(auth_type="IAM")
        config = DocumentDBSqlHelper.to_sql_config(connection)

        assert config["auth_mechanism"] == "MONGODB-AWS"
        assert config["user"] is None
        assert config["password"] is None
        assert config["tls"] is True

    def test_iam_auth_extracts_host_port_database(self):
        connection = _make_connection(auth_type="IAM")
        config = DocumentDBSqlHelper.to_sql_config(connection)

        assert config["host"] == "docdb-cluster.us-west-2.docdb.amazonaws.com"
        assert config["port"] == 27017
        assert config["database"] == "mydb"

    def test_basic_auth_extracts_credentials_from_secret(self):
        connection = _make_connection(
            auth_type="BASIC",
            secret={"username": "admin", "password": "secret123"},
        )
        config = DocumentDBSqlHelper.to_sql_config(connection)

        assert config["auth_mechanism"] is None
        assert config["user"] == "admin"
        assert config["password"] == "secret123"
        assert config["tls"] is True

    def test_basic_auth_normalizes_secret_keys_to_lowercase(self):
        connection = _make_connection(
            auth_type="BASIC",
            secret={"Username": "admin", "Password": "secret123"},
        )
        config = DocumentDBSqlHelper.to_sql_config(connection)

        assert config["user"] == "admin"
        assert config["password"] == "secret123"

    def test_defaults_port_to_27017_when_missing(self):
        glue_connection = make_dataclass(
            "GlueConnection",
            ["connectionProperties", "authenticationConfiguration"],
        )(
            connectionProperties={
                "HOST": "docdb-cluster.us-west-2.docdb.amazonaws.com",
                "DATABASE": "mydb",
            },
            authenticationConfiguration={"authenticationType": "IAM"},
        )

        connection = make_dataclass("Connection", ["secret", "connection_creds", "data"])(
            None,
            make_dataclass("ConnectionCredentials", [])(),
            make_dataclass("ConnectionData", ["physical_endpoints"])(
                [
                    make_dataclass("PhysicalEndpoint", ["awsLocation", "glueConnection"])(
                        awsLocation={"awsRegion": "us-west-2"},
                        glueConnection=glue_connection,
                    )
                ]
            ),
        )
        config = DocumentDBSqlHelper.to_sql_config(connection)
        assert config["port"] == 27017

    def test_defaults_database_to_test_when_missing(self):
        glue_connection = make_dataclass(
            "GlueConnection",
            ["connectionProperties", "authenticationConfiguration"],
        )(
            connectionProperties={
                "HOST": "docdb-cluster.us-west-2.docdb.amazonaws.com",
                "PORT": "27017",
            },
            authenticationConfiguration={"authenticationType": "IAM"},
        )

        connection = make_dataclass("Connection", ["secret", "connection_creds", "data"])(
            None,
            make_dataclass("ConnectionCredentials", [])(),
            make_dataclass("ConnectionData", ["physical_endpoints"])(
                [
                    make_dataclass("PhysicalEndpoint", ["awsLocation", "glueConnection"])(
                        awsLocation={"awsRegion": "us-west-2"},
                        glueConnection=glue_connection,
                    )
                ]
            ),
        )
        config = DocumentDBSqlHelper.to_sql_config(connection)
        assert config["database"] == "test"


class TestDocumentDBSqlHelperGetAuthType:
    """Test _get_auth_type edge cases."""

    def test_returns_basic_when_no_physical_endpoints(self):
        connection_data = {"physical_endpoints": None}
        assert DocumentDBSqlHelper._get_auth_type(connection_data) == "BASIC"

    def test_returns_basic_when_empty_list(self):
        connection_data = {"physical_endpoints": []}
        assert DocumentDBSqlHelper._get_auth_type(connection_data) == "BASIC"

    def test_returns_basic_when_no_auth_config(self):
        connection_data = {
            "physical_endpoints": [{"glueConnection": {"authenticationConfiguration": {}}}]
        }
        assert DocumentDBSqlHelper._get_auth_type(connection_data) == "BASIC"

    def test_returns_iam_case_insensitive(self):
        connection_data = {
            "physical_endpoints": [
                {"glueConnection": {"authenticationConfiguration": {"authenticationType": "iam"}}}
            ]
        }
        assert DocumentDBSqlHelper._get_auth_type(connection_data) == "IAM"

    def test_returns_basic_when_endpoint_is_not_dict(self):
        connection_data = {"physical_endpoints": ["not-a-dict"]}
        assert DocumentDBSqlHelper._get_auth_type(connection_data) == "BASIC"

    def test_returns_basic_on_exception(self):
        """Test that exceptions in _get_auth_type are caught and return BASIC."""
        # Pass a non-dict that has no .get() method to trigger AttributeError
        assert DocumentDBSqlHelper._get_auth_type(None) == "BASIC"
