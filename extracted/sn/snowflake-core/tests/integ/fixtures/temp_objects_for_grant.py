from contextlib import suppress

import pytest as pytest

from snowflake.core.database import Database
from snowflake.core.database_role import DatabaseRole
from snowflake.core.exceptions import NotFoundError
from snowflake.core.role import Role
from snowflake.core.schema import Schema
from snowflake.core.table import Table, TableColumn
from snowflake.core.user import User
from tests.integ.utils import random_string


@pytest.fixture
def test_database_role_name(database_roles_in_test_database):
    role_name = random_string(4, "test_database_role_name_")
    test_role = DatabaseRole(name=role_name, comment="test_comment")
    try:
        database_roles_in_test_database.create(test_role)
        yield role_name.upper()
    finally:
        with suppress(NotFoundError):
            database_roles_in_test_database[role_name].drop()


@pytest.fixture
def test_database_role_name_2(database_roles_in_test_database):
    role_name = random_string(4, "test_database_role_name_2_")
    test_role = DatabaseRole(name=role_name, comment="test_comment")
    try:
        database_roles_in_test_database.create(test_role)
        yield role_name.upper()
    finally:
        with suppress(NotFoundError):
            database_roles_in_test_database[role_name].drop()


@pytest.fixture
def test_database_for_grant_name(databases, backup_database_schema):
    del backup_database_schema
    try:
        new_db_def = Database(name=random_string(3, "test_database_for_grant_name_"), kind="TRANSIENT")
        new_db_def.comment = "database first"
        database = databases.create(new_db_def)
        yield database.name.upper()
    finally:
        with suppress(Exception):
            database.drop()


@pytest.fixture
def database_roles_in_test_database(databases, test_database_for_grant_name):
    return databases[test_database_for_grant_name].database_roles


@pytest.fixture
def schemas_in_test_database(databases, test_database_for_grant_name):
    return databases[test_database_for_grant_name].schemas


@pytest.fixture
def tables_in_test_database(schemas_in_test_database, test_schema_for_grant_name):
    return schemas_in_test_database[test_schema_for_grant_name].tables


@pytest.fixture
def test_schema_for_grant_name(schemas_in_test_database):
    schema_name = random_string(5, "test_schema_for_role_grant_name_")
    try:
        new_schema_def = Schema(name=schema_name)
        schema = schemas_in_test_database.create(new_schema_def)
        yield schema_name.upper()
    finally:
        with suppress(NotFoundError):
            schema.drop()


@pytest.fixture
def test_table_for_grant_name(tables_in_test_database):
    table_name = random_string(5, "test_table_for_test_role_")
    columns = [TableColumn(name="col1", datatype="int"), TableColumn(name="col2", datatype="string")]
    test_table = Table(name=table_name, columns=columns)
    try:
        test_table_handle = tables_in_test_database.create(test_table)
        yield table_name.upper()
    finally:
        with suppress(NotFoundError):
            test_table_handle.drop()


@pytest.fixture
def test_role_name(roles):
    role_name = random_string(4, "test_grant_role_")
    test_role = Role(name=role_name, comment="test_comment")
    try:
        roles.create(test_role)
        yield role_name
    finally:
        with suppress(Exception):
            roles[role_name].drop()


@pytest.fixture
def test_role_name_2(roles):
    role_name = random_string(4, "test_grant_role_2_")
    test_role = Role(name=role_name, comment="test_comment")
    try:
        roles.create(test_role)
        yield role_name
    finally:
        with suppress(Exception):
            roles[role_name].drop()


@pytest.fixture
def test_user_name(users):
    user_name = random_string(4, "test_grant_user_")
    test_user = User(
        name=user_name,
        password="test",
        display_name="test_name",
        first_name="firstname",
        last_name="lastname",
        email="test@snowflake.com",
        must_change_password=False,
        disabled=False,
        days_to_expiry=1,
        mins_to_unlock=10,
        mins_to_bypass_mfa=60,
        default_warehouse="test",
        default_namespace="test",
        default_role="public",
        default_secondary_roles="ALL",
        comment="test_comment",
    )
    try:
        users.create(test_user)
        yield user_name
    finally:
        with suppress(Exception):
            users[user_name].drop()
