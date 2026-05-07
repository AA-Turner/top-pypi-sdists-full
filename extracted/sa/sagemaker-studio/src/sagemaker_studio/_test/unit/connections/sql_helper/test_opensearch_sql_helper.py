"""
Unit tests for OpenSearch SQL helper.
"""

from dataclasses import make_dataclass

from sagemaker_studio.connections.sql_helper.opensearch_sql_helper import OpenSearchSQLHelper

opensearch_connection = make_dataclass("Connection", ["secret", "connection_creds", "data"])(
    {"USERNAME": "admin", "PASSWORD": "opensearch_secret"},
    make_dataclass("ConnectionCredentials", [])(),
    make_dataclass("ConnectionData", ["physical_endpoints"])(
        [
            make_dataclass("PhysicalEndpoint", ["awsLocation", "glueConnection"])(
                awsLocation={"awsRegion": "us-west-2"},
                glueConnection=make_dataclass("GlueConnection", ["connectionProperties"])(
                    connectionProperties={
                        "DOMAIN_ENDPOINT": "https://search-my-domain.us-west-2.es.amazonaws.com",
                    },
                ),
            )
        ]
    ),
)


def test_to_opensearch_helper_sql_config_returns_expected():
    result = OpenSearchSQLHelper.to_sql_config(opensearch_connection)
    assert result == {
        "domain_endpoint": "https://search-my-domain.us-west-2.es.amazonaws.com",
        "user": "admin",
        "password": "opensearch_secret",
    }


def test_to_opensearch_helper_sql_config_missing_secret_fields():
    """Test that missing secret fields return None values."""
    conn = make_dataclass("Connection", ["secret", "connection_creds", "data"])(
        {},
        make_dataclass("ConnectionCredentials", [])(),
        make_dataclass("ConnectionData", ["physical_endpoints"])(
            [
                make_dataclass("PhysicalEndpoint", ["awsLocation", "glueConnection"])(
                    awsLocation={"awsRegion": "us-east-1"},
                    glueConnection=make_dataclass("GlueConnection", ["connectionProperties"])(
                        connectionProperties={
                            "DOMAIN_ENDPOINT": "https://search-domain.us-east-1.es.amazonaws.com",
                        },
                    ),
                )
            ]
        ),
    )
    result = OpenSearchSQLHelper.to_sql_config(conn)
    assert result["domain_endpoint"] == "https://search-domain.us-east-1.es.amazonaws.com"
    assert result["user"] is None
    assert result["password"] is None


def test_to_opensearch_helper_sql_config_missing_domain_endpoint():
    """Test that missing DOMAIN_ENDPOINT returns None."""
    conn = make_dataclass("Connection", ["secret", "connection_creds", "data"])(
        {"USERNAME": "admin", "PASSWORD": "secret"},
        make_dataclass("ConnectionCredentials", [])(),
        make_dataclass("ConnectionData", ["physical_endpoints"])(
            [
                make_dataclass("PhysicalEndpoint", ["awsLocation", "glueConnection"])(
                    awsLocation={"awsRegion": "us-east-1"},
                    glueConnection=make_dataclass("GlueConnection", ["connectionProperties"])(
                        connectionProperties={},
                    ),
                )
            ]
        ),
    )
    result = OpenSearchSQLHelper.to_sql_config(conn)
    assert result["domain_endpoint"] is None
    assert result["user"] == "admin"
    assert result["password"] == "secret"


def test_to_opensearch_helper_sql_config_secret_key_case_insensitive_preserves_values():
    """Test that secret key lookup is case-insensitive but credential values are not modified."""

    def _make_connection(secret):
        return make_dataclass("Connection", ["secret", "connection_creds", "data"])(
            secret,
            make_dataclass("ConnectionCredentials", [])(),
            make_dataclass("ConnectionData", ["physical_endpoints"])(
                [
                    make_dataclass("PhysicalEndpoint", ["awsLocation", "glueConnection"])(
                        awsLocation={"awsRegion": "us-west-2"},
                        glueConnection=make_dataclass("GlueConnection", ["connectionProperties"])(
                            connectionProperties={
                                "DOMAIN_ENDPOINT": "https://search-my-domain.us-west-2.es.amazonaws.com",
                            },
                        ),
                    )
                ]
            ),
        )

    mixed_case_value_user = "AdMiN_UsEr"
    mixed_case_value_password = "S3cReT!PaSsWoRd"

    # Uppercase keys
    result = OpenSearchSQLHelper.to_sql_config(
        _make_connection({"USERNAME": mixed_case_value_user, "PASSWORD": mixed_case_value_password})
    )
    assert result["user"] == mixed_case_value_user
    assert result["password"] == mixed_case_value_password

    # Lowercase keys
    result = OpenSearchSQLHelper.to_sql_config(
        _make_connection({"username": mixed_case_value_user, "password": mixed_case_value_password})
    )
    assert result["user"] == mixed_case_value_user
    assert result["password"] == mixed_case_value_password

    # Mixed-case keys
    result = OpenSearchSQLHelper.to_sql_config(
        _make_connection({"UserName": mixed_case_value_user, "PassWord": mixed_case_value_password})
    )
    assert result["user"] == mixed_case_value_user
    assert result["password"] == mixed_case_value_password
