from dataclasses import make_dataclass

from sagemaker_studio.connections.sql_helper.workday_data_connect_sql_helper import (
    WorkdayDataConnectSqlHelper,
)

workday_connection = make_dataclass("Connection", ["secret", "physical_endpoints"])(
    secret={
        "wd.authn.clientId": "client_123",
        "wd.authn.isu": "isu_value",
        "wd.authn.accessTokenEndpoint": "https://auth.example.com/token",
        "wd.authn.privateKey": "-----BEGIN PRIVATE KEY-----\nfakekey\n-----END PRIVATE KEY-----",
    },
    physical_endpoints=[
        make_dataclass("PhysicalEndpoint", ["glue_connection"])(
            glue_connection=make_dataclass("GlueConnection", ["connection_properties"])(
                connection_properties={
                    "HOST": "workday.example.com",
                    "PORT": "443",
                }
            )
        )
    ],
)


def test_to_sql_config_returns_expected_keys():
    result = WorkdayDataConnectSqlHelper.to_sql_config(workday_connection)
    assert result["client_id"] == "client_123"
    assert result["isu"] == "isu_value"
    assert result["access_token_endpoint"] == "https://auth.example.com/token"
    assert (
        result["private_key_file"]
        == "-----BEGIN PRIVATE KEY-----\nfakekey\n-----END PRIVATE KEY-----"
    )
    assert result["host"] == "workday.example.com"
    assert result["port"] == "443"


def test_to_sql_config_missing_port_returns_none():
    conn = make_dataclass("Connection", ["secret", "physical_endpoints"])(
        secret={
            "wd.authn.clientId": "c",
            "wd.authn.isu": "i",
            "wd.authn.accessTokenEndpoint": "https://x.com",
            "wd.authn.privateKey": "key",
        },
        physical_endpoints=[
            make_dataclass("PhysicalEndpoint", ["glue_connection"])(
                glue_connection=make_dataclass("GlueConnection", ["connection_properties"])(
                    connection_properties={"HOST": "h"}
                )
            )
        ],
    )
    result = WorkdayDataConnectSqlHelper.to_sql_config(conn)
    assert result["host"] == "h"
    assert result["port"] is None
