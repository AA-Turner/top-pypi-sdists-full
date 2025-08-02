#
# Copyright (c) 2012-2023 Snowflake Computing Inc. All rights reserved.
#
import pytest

from pydantic_core._pydantic_core import ValidationError

from tests.utils import unquote


pytestmark = [pytest.mark.usefixtures("backup_database_schema")]


def test_iter(databases, temp_db, temp_db_case_sensitive):
    database_names = [db.name for db in databases.iter()]
    assert temp_db.name.upper() in database_names
    assert unquote(temp_db_case_sensitive.name) in database_names


def test_iter_like(databases, temp_db, temp_db_case_sensitive):
    database_names = [db.name for db in databases.iter(like="test_database%")]
    assert temp_db.name.upper() in database_names
    assert unquote(temp_db_case_sensitive.name) in database_names


def test_iter_starts_with(databases, temp_db, temp_db_case_sensitive):
    database_names = [db.name for db in databases.iter(starts_with="Test_database")]
    assert temp_db.name.upper() not in database_names
    assert unquote(temp_db_case_sensitive.name) not in database_names

    database_names = [db.name for db in databases.iter(starts_with="TEST_DATABASE")]
    assert temp_db.name.upper() in database_names
    assert unquote(temp_db_case_sensitive.name) not in database_names


# The limit keyword is required for the from keyword to function, limit=100 was chosen arbitrarily
# as it does not affect the test
def test_iter_from_name(databases, temp_db, temp_db_case_sensitive):
    database_names = [db.name for db in databases.iter(limit=100, from_name="test_database")]
    assert temp_db.name.upper() not in database_names
    assert unquote(temp_db_case_sensitive.name) in database_names


def test_iter_limit(databases):
    data = list(databases.iter())
    initial_length = min(len(data), 10000)

    data = list(databases.iter(limit=initial_length))
    assert len(data) <= initial_length

    data = list(databases.iter(limit=initial_length - 1))
    assert len(data) <= initial_length - 1

    data = list(databases.iter(limit=10000))
    assert len(data) <= 10000

    with pytest.raises(ValidationError):
        list(databases.iter(limit=10001))
