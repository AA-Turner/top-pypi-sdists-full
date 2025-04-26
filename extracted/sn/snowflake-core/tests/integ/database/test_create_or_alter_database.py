#
# Copyright (c) 2012-2023 Snowflake Computing Inc. All rights reserved.
#


import pytest

from snowflake.core.database import Database, DatabaseCollection, DatabaseResource

from ..utils import random_string


pytestmark = pytest.mark.usefixtures("backup_database_schema")


@pytest.mark.min_sf_ver("9.8.0")
def test_create_or_alter_database(databases, temp_db: DatabaseResource):
    db_def = temp_db.fetch()
    db_def.comment = "my new comment"
    db_def.data_retention_time_in_days = 0
    db_def.default_ddl_collation = "en_US-trim"
    db_def.log_level = "INFO"
    db_def.max_data_extension_time_in_days = 7
    db_def.suspend_task_after_num_failures = 1
    db_def.trace_level = "ALWAYS"
    db_def.user_task_managed_initial_warehouse_size = "SMALL"
    db_def.serverless_task_min_statement_size = "SMALL"
    db_def.serverless_task_max_statement_size = "MEDIUM"
    db_def.user_task_timeout_ms = 3600001
    temp_db.create_or_alter(db_def)
    new_db = databases[temp_db.name].fetch()
    assert new_db.name in (temp_db.name, temp_db.name.upper())
    assert new_db.comment == "my new comment"
    assert new_db.data_retention_time_in_days == 0
    assert new_db.default_ddl_collation == "en_US-trim"
    assert new_db.max_data_extension_time_in_days == 7
    assert new_db.suspend_task_after_num_failures == 1
    assert new_db.user_task_managed_initial_warehouse_size == "SMALL"
    assert new_db.serverless_task_min_statement_size == "SMALL"
    assert new_db.serverless_task_max_statement_size == "MEDIUM"
    assert new_db.user_task_timeout_ms == 3600001


def test_resist_multi_statement_sql_injection(databases: DatabaseCollection):
    new_db_name = random_string(3, "test_db_resist_multi_statement_sql_injection_")
    sql_injection_comment = "'comment for disguise'; select '1'"

    new_db = Database(
        name=new_db_name,
        comment=sql_injection_comment,
    )

    db = databases.create(new_db)
    try:
        db.fetch()
    finally:
        db.drop()
