from urllib.parse import quote

import pytest

from sagemaker_studio.sql_engine.workday_transformer import WorkdayTransformer

VALID_CONNECTION_DATA = {
    "host": "workday.example.com",
    "port": "443",
    "client_id": "client_123",
    "isu": "isu_value",
    "access_token_endpoint": "https://auth.example.com/token",
    "private_key_file": "-----BEGIN PRIVATE KEY-----\nfakekey\n-----END PRIVATE KEY-----",
}


def test_get_dialect():
    assert WorkdayTransformer.get_dialect() == "trino"


def test_get_required_fields():
    assert WorkdayTransformer.get_required_fields() == [
        "host",
        "port",
        "client_id",
        "isu",
        "access_token_endpoint",
        "private_key_file",
    ]


def test_to_sqlalchemy_config_builds_connection_string():
    result = WorkdayTransformer.to_sqlalchemy_config(VALID_CONNECTION_DATA)

    private_key = "-----BEGIN PRIVATE KEY-----\nfakekey\n-----END PRIVATE KEY-----"
    expected_url = (
        f"workday_data_connect://workday.example.com:443"
        f"?client_id=client_123&isu=isu_value"
        f"&token_endpoint={quote('https://auth.example.com/token', safe='')}"
        f"&private_key={quote(private_key, safe='')}"
    )
    assert result["connection_string"] == expected_url
    assert result["connect_args"] == {}


def test_to_sqlalchemy_config_raises_on_missing_field():
    with pytest.raises(ValueError, match="host is required"):
        WorkdayTransformer.to_sqlalchemy_config({"port": "443"})


def test_get_resources_action_database():
    defn = WorkdayTransformer.get_resources_action(None)
    assert "SHOW CATALOGS" in defn.sql
    assert defn.default_type == "DATABASE"


def test_get_resources_action_schema():
    defn = WorkdayTransformer.get_resources_action("SCHEMA", {"DATABASE": "mydb"})
    assert "mydb.information_schema.schemata" in defn.sql
    assert defn.default_type == "SCHEMA"


def test_get_resources_action_table():
    defn = WorkdayTransformer.get_resources_action("TABLE", {"DATABASE": "mydb", "SCHEMA": "pub"})
    assert "mydb.information_schema.tables" in defn.sql
    assert defn.sql_parameters == {"schema": "pub"}
    assert defn.default_type == "TABLE"


def test_get_resources_action_column():
    defn = WorkdayTransformer.get_resources_action(
        "COLUMN", {"DATABASE": "mydb", "SCHEMA": "pub", "TABLE": "t1"}
    )
    assert "mydb.information_schema.columns" in defn.sql
    assert defn.sql_parameters == {"schema": "pub", "table": "t1"}
    assert defn.default_type == "COLUMN"


def test_get_resources_action_unsupported_type():
    with pytest.raises(ValueError, match="Unsupported resource type"):
        WorkdayTransformer.get_resources_action("INVALID")


def test_get_loggers():
    assert WorkdayTransformer.get_loggers() == ["trino"]
