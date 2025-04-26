import pytest

from snowflake.core import CreateMode
from snowflake.core.database import Database
from snowflake.core.database_role import DatabaseRole
from snowflake.core.exceptions import ConflictError
from tests.integ.utils import backup_database_and_schema
from tests.utils import random_string


pytestmark = pytest.mark.min_sf_ver("8.39.0")


def test_create(databases, cursor):
    try:
        with backup_database_and_schema(cursor):
            new_db_def = Database(name=random_string(3, "test_database_$12create_"), kind="TRANSIENT")
            new_db_def.comment = "database first"
            database_handle = databases.create(new_db_def)
            cursor.execute(f"USE DATABASE {new_db_def.name}")

            database_role_name = random_string(10, "test_database_role")
            database_role = DatabaseRole(name=database_role_name, comment="test_comment")

            database_role_handles = []

            database_roles = databases[new_db_def.name].database_roles

            try:
                # check there are no database roles yet
                assert len(list(database_roles.iter(limit=1, from_name=database_role_name.upper()[:-1]))) == 0

                # happy path
                database_role_handles += [database_roles.create(database_role)]
                database_roles_list = list(database_roles.iter(limit=1, from_name=database_role_name.upper()[:-1]))
                assert len(database_roles_list) == 1
                assert database_roles_list[0].name == database_role_name.upper()
                assert database_roles_list[0].comment == "test_comment"

                # create role with already existing name with mode or_replace change comment
                database_role.comment = "test_comment_2"
                database_roles.create(database_role, mode=CreateMode.or_replace)
                database_roles_list = list(database_roles.iter(limit=1, from_name=database_role_name.upper()[:-1]))
                assert len(database_roles_list) == 1
                assert database_roles_list[0].name == database_role_name.upper()
                assert database_roles_list[0].comment == "test_comment_2"

                # create role with already existing name with mode if_not_exists
                database_role.comment = "test_comment_3"
                database_roles.create(database_role, mode=CreateMode.if_not_exists)
                database_roles_list = list(database_roles.iter(limit=1, from_name=database_role_name.upper()[:-1]))
                assert len(database_roles_list) == 1
                assert database_roles_list[0].name == database_role_name.upper()
                assert database_roles_list[0].comment == "test_comment_2"

                # create role with already existing name with mode error_if_exists
                database_role.comment = "test_comment_4"
                with pytest.raises(ConflictError):
                    database_roles.create(database_role, mode=CreateMode.error_if_exists)

            finally:
                for database_role_handle in database_role_handles:
                    database_role_handle.drop()
    finally:
        database_handle.drop()
