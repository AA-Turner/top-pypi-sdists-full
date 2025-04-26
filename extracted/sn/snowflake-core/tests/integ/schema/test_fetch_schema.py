import pytest


pytestmark = pytest.mark.usefixtures("backup_database_schema")


@pytest.mark.min_sf_ver("9.8.0")
def test_fetch(temp_schema, temp_schema_case_sensitive):
    schema = temp_schema.fetch()
    assert schema.name.upper() == temp_schema.name.upper()

    schema = temp_schema_case_sensitive.fetch()
    assert f'"{schema.name}"' == temp_schema_case_sensitive.name
    assert schema.comment == "created by temp_schema_case_sensitive"
    assert schema.serverless_task_min_statement_size == "XSMALL"
    assert schema.serverless_task_max_statement_size == "X2LARGE"
    assert schema.user_task_managed_initial_warehouse_size == "MEDIUM"
    assert schema.suspend_task_after_num_failures == 10
    assert schema.user_task_timeout_ms == 3600000
