#
# Copyright (c) 2012-2023 Snowflake Computing Inc. All rights reserved.
#

import os
import sys

import pytest

from snowflake.core import CreateMode
from snowflake.core.database import Database, DatabaseCollection
from snowflake.core.exceptions import ConflictError, NotFoundError

from ..utils import random_string


pytestmark = pytest.mark.usefixtures("backup_database_schema")


def test_conflict_error(databases: DatabaseCollection, root):
    root.parameters(refresh=True)
    test_database_name = random_string(3, "test_db_123")
    new_db_def = Database(name=test_database_name)
    database = databases.create(new_db_def)
    try:
        with pytest.raises(ConflictError) as exc_info:
            databases.create(new_db_def, mode=CreateMode.error_if_exists)
        assert f"Error Message: object '{test_database_name}' already exists" in str(exc_info.value)
    finally:
        database.drop()


def test_not_found_error(databases: DatabaseCollection, root):
    test_database_name = random_string(3, "db_doesnt_exist")
    with pytest.raises(NotFoundError) as exc_info:
        databases[test_database_name].fetch()
    assert f"Error Message: database '{test_database_name}' does not exist or not authorized." in str(exc_info.value)
    assert sys.tracebacklimit is None


def test_not_found_error_traceback_disabled(databases: DatabaseCollection, root):
    test_database_name = random_string(3, "db_doesnt_exist")
    os.environ["_SNOWFLAKE_PRINT_VERBOSE_STACK_TRACE"] = "false"
    root.parameters(refresh=True)
    with pytest.raises(NotFoundError) as exc_info:
        databases[test_database_name].fetch()
    assert f"Error Message: database '{test_database_name}' does not exist or not authorized." in str(exc_info.value)
    assert sys.tracebacklimit == 0
    del os.environ["_SNOWFLAKE_PRINT_VERBOSE_STACK_TRACE"]
    root.parameters(refresh=True)
