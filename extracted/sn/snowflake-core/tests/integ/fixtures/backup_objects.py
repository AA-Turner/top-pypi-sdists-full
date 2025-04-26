from contextlib import suppress

import pytest

from tests.integ.utils import backup_database_and_schema as _backup_database_and_schema
from tests.integ.utils import backup_warehouse


@pytest.fixture
def backup_database_schema(connection):
    """Reset the current database and schema after a test is complete.

    These 2 resources go hand-in-hand, so they should be backed up together.
    This fixture should be used when a database, or schema is created,
    or used in a test.
    """
    with connection.cursor() as cursor, _backup_database_and_schema(cursor):
        with suppress(Exception):
            yield


@pytest.fixture
def backup_warehouse_fixture(connection):
    """Reset the current warehouse after a test is complete.

    This fixture should be used when a warehouse is created, or used in a test.
    """
    with connection.cursor() as cursor, backup_warehouse(cursor) as current_warehouse:
        with suppress(Exception):
            yield current_warehouse
