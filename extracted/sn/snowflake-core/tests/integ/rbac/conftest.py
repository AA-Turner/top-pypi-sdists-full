import pytest as pytest

from tests.integ.utils import random_string


@pytest.fixture
def test_database_role_name(connection):
    database_role_name = random_string(4, "test_database_grant_role_")
    with connection.cursor() as cursor:
        cursor.execute(f"create database role if not exists {database_role_name}")
        try:
            yield database_role_name
        finally:
            cursor.execute(f"drop database role if exists {database_role_name}")


@pytest.fixture
def test_share_name(connection):
    share_name = random_string(4, "test_share_")
    with connection.cursor() as cursor:
        cursor.execute(f"create share if not exists {share_name}")
        try:
            yield share_name
        finally:
            cursor.execute(f"drop share if exists {share_name}")


@pytest.fixture
def test_role_name(connection):
    role_name = random_string(4, "test_grant_role_")
    with connection.cursor() as cursor:
        cursor.execute(f"create role if not exists {role_name}")
        try:
            yield role_name
        finally:
            cursor.execute(f"drop role if exists {role_name}")


@pytest.fixture
def test_user_name(connection):
    user_name = random_string(10, "test_user_")
    with connection.cursor() as cursor:
        cursor.execute(f"create user if not exists {user_name}")
        try:
            yield user_name
        finally:
            cursor.execute(f"drop user if exists {user_name}")


@pytest.fixture
def test_table_name(connection):
    table_name = random_string(10, "test_table_")
    with connection.cursor() as cursor:
        cursor.execute(f"CREATE TABLE {table_name}(a INT)")
        try:
            yield table_name
        finally:
            cursor.execute(f"drop table if exists {table_name}")


@pytest.fixture
def test_warehouse_name(connection):
    warehouse_name = random_string(10, "test_warehouse_")
    with connection.cursor() as cursor:
        cursor.execute(f"create warehouse {warehouse_name}")
        try:
            yield warehouse_name
        finally:
            cursor.execute(f"drop warehouse if exists {warehouse_name}")


@pytest.fixture
def test_function_name(connection):
    function_name = random_string(10, "test_function_")
    with connection.cursor() as cursor:
        cursor.execute(
            f"CREATE FUNCTION {function_name}(a number, b number) RETURNS number COMMENT='multiply two numbers' AS 'a * b'"  # noqa: E501
        )
        try:
            yield function_name
        finally:
            cursor.execute(f"drop FUNCTION if exists {function_name}(number, number)")
