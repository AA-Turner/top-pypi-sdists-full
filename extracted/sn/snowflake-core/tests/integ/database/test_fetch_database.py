#
# Copyright (c) 2012-2023 Snowflake Computing Inc. All rights reserved.
#


import pytest


pytestmark = pytest.mark.usefixtures("backup_database_schema")


@pytest.mark.min_sf_ver("9.8.0")
def test_fetch(databases, temp_db):
    database = databases[temp_db.name].fetch()
    assert database.name.upper() == temp_db.name.upper()
    assert database.comment == "created by temp_db"
    assert database.serverless_task_min_statement_size == "XSMALL"
    assert database.serverless_task_max_statement_size == "X2LARGE"
    assert database.user_task_managed_initial_warehouse_size == "MEDIUM"
    assert database.suspend_task_after_num_failures == 10
    assert database.user_task_timeout_ms == 3600000
