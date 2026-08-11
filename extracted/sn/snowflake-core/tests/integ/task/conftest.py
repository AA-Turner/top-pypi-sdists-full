# Copyright (c) 2012-2023 Snowflake Computing Inc. All rights reserved.


import pytest

from snowflake.connector.cursor import SnowflakeCursor
from snowflake.core.database import DatabaseCollection  # noqa: F401
from snowflake.core.task import TaskCollection
from tests.integ.fixtures.temp_objects_for_grant import test_user_name  # noqa: F401 # pylint: disable=unused-import

from ..fixtures.pre_checks import my_integration_exists  # noqa: F401 # pylint: disable=unused-import


@pytest.fixture(scope="module")
def tasks(schema) -> TaskCollection:
    return schema.tasks


@pytest.fixture
def grant_test_user_impersonation(cursor: SnowflakeCursor, request: pytest.FixtureRequest):
    """Grant IMPERSONATE and the current role to ``test_user_name`` for execute_as_user tests."""
    user_name: str = request.getfixturevalue("test_user_name")
    current_role = cursor.connection.role
    cursor.execute(f"GRANT IMPERSONATE ON USER {user_name} TO ROLE {current_role}")
    cursor.execute(f"GRANT ROLE {current_role} TO USER {user_name}")
    try:
        yield
    finally:
        cursor.execute(f"REVOKE ROLE {current_role} FROM USER {user_name}")
        cursor.execute(f"REVOKE IMPERSONATE ON USER {user_name} FROM ROLE {current_role}")
