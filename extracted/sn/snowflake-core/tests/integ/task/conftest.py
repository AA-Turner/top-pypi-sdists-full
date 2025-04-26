# Copyright (c) 2012-2023 Snowflake Computing Inc. All rights reserved.


import pytest

from snowflake.core.database import DatabaseCollection  # noqa: F401
from snowflake.core.task import TaskCollection

from ..fixtures.pre_checks import my_integration_exists  # noqa: F401 # pylint: disable=unused-import


@pytest.fixture(scope="module")
def tasks(schema) -> TaskCollection:
    return schema.tasks
