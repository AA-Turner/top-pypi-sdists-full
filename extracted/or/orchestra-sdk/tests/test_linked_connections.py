import pytest

from orchestra_sdk.errors import LinkedConnectionNotFoundError
from orchestra_sdk.linked_connections import (
    LinkedConnection,
    get_linked_connection,
    list_linked_connections,
)

LINKED_ENV = {
    "SNOWFLAKE__PROD_12345__SNOWFLAKE_USER": "analyst",
    "SNOWFLAKE__PROD_12345__SNOWFLAKE_PASSWORD": "hunter22",
    "SNOWFLAKE__DEV_67890__SNOWFLAKE_USER": "dev",
    "BIGQUERY__BQ_1__SERVICE_ACCOUNT_INFO": '{"type":"service_account","project_id":"p"}',
    "BIGQUERY__BQ_1__SCOPES": '["a","b"]',
    "BIGQUERY__BQ_1__DATASET": "[not json",
    "ORCHESTRA_TASK_RUN_ID": "abc",
    "SOME__OTHER__VAR__NAME": "four parts",
    "lower__case__var": "not ours",
    "A____B": "empty part",
}


@pytest.fixture(autouse=True)
def linked_env(mocker):
    mocker.patch.dict("os.environ", LINKED_ENV, clear=True)


def test_list_linked_connections_groups_fields_and_ignores_other_variables():
    assert list_linked_connections() == [
        LinkedConnection(
            integration="BIGQUERY",
            connection_id="BQ_1",
            fields={
                "SERVICE_ACCOUNT_INFO": {"type": "service_account", "project_id": "p"},
                "SCOPES": ["a", "b"],
                "DATASET": "[not json",
            },
        ),
        LinkedConnection(
            integration="SNOWFLAKE",
            connection_id="DEV_67890",
            fields={"SNOWFLAKE_USER": "dev"},
        ),
        LinkedConnection(
            integration="SNOWFLAKE",
            connection_id="PROD_12345",
            fields={"SNOWFLAKE_USER": "analyst", "SNOWFLAKE_PASSWORD": "hunter22"},
        ),
    ]


def test_get_linked_connection_by_id_normalises_names():
    connection = get_linked_connection("snowflake", "prod-12345")

    assert connection.connection_id == "PROD_12345"
    assert connection["snowflake_password"] == "hunter22"
    assert connection.get("missing") is None
    assert "hunter22" not in repr(connection)


def test_get_linked_connection_without_id_when_only_one_is_linked():
    assert get_linked_connection("bigquery").connection_id == "BQ_1"


@pytest.mark.parametrize(
    "integration, connection_id, message",
    [
        (
            "snowflake",
            None,
            r"Several SNOWFLAKE connections .* \(DEV_67890, PROD_12345\)",
        ),
        ("snowflake", "missing", "SNOWFLAKE connection 'missing' is not linked"),
        ("postgres", None, "No POSTGRES connection is linked"),
    ],
)
def test_get_linked_connection_raises_a_clear_error(integration, connection_id, message):
    with pytest.raises(LinkedConnectionNotFoundError, match=message):
        get_linked_connection(integration, connection_id)
