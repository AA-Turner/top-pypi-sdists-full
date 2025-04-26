import pytest

from snowflake.core import CreateMode
from snowflake.core.database import Database
from snowflake.core.database_role import DatabaseRole
from snowflake.core.exceptions import ConflictError, UnauthorizedError
from tests.integ.utils import backup_database_and_schema
from tests.utils import random_string


pytestmark = pytest.mark.min_sf_ver("8.39.0")


def test_clone(databases, cursor):
    try:
        with backup_database_and_schema(cursor):
            new_db_def = Database(name=random_string(3, "test_database_$12create_"), kind="TRANSIENT")
            new_db_def.comment = "database first"
            database_handle_first = databases.create(new_db_def)
            cursor.execute(f"USE DATABASE {new_db_def.name}")

            database_role_name = random_string(10, "test_database_role")
            database_role = DatabaseRole(name=database_role_name, comment="test_comment")

            database_role_handles = []
            database_handle = None

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

                # clone from existing role in the same database throws error
                target_database_role_name = random_string(10, "test_database_role")
                with pytest.raises(UnauthorizedError):
                    database_roles[database_role_name].clone(target_database_role_name)

                with backup_database_and_schema(cursor):
                    new_db_def = Database(name=random_string(3, "test_database_$12create_"), kind="TRANSIENT")
                    new_db_def.comment = "database first"
                    database_handle = databases.create(new_db_def)
                    cursor.execute(f"USE DATABASE {new_db_def.name}")

                    # clone when specifying the target database
                    database_roles[database_role_name].clone(target_database_role_name, target_database=new_db_def.name)
                    database_roles_list = list(
                        databases[new_db_def.name].database_roles.iter(
                            limit=1, from_name=target_database_role_name.upper()[:-1]
                        )
                    )
                    assert len(database_roles_list) == 1

                    # clone from existing role or_replace
                    database_roles[database_role_name].clone(
                        target_database_role_name, target_database=new_db_def.name, mode=CreateMode.or_replace
                    )
                    database_roles_list = list(
                        databases[new_db_def.name].database_roles.iter(
                            limit=1, from_name=target_database_role_name.upper()[:-1]
                        )
                    )
                    assert len(database_roles_list) == 1

                    # clone from existing role if_not_exists
                    # TODO(SNOW-1707547): Uncomment this when the bug is fixed
                    # database_roles[database_role_name].clone(
                    #     target_database_role_name, target_database=new_db_def.name, mode="if_not_exists"
                    # )
                    # database_roles_list = list(
                    #     databases[new_db_def.name].database_roles.iter(
                    #         limit=1, from_name=target_database_role_name.upper()[:-1]
                    #     )
                    # )
                    # assert len(database_roles_list) == 1

                    # clone from existing role error_if_exists
                    with pytest.raises(ConflictError):
                        database_roles[database_role_name].clone(
                            target_database_role_name, target_database=new_db_def.name, mode=CreateMode.error_if_exists
                        )

                # clone when specifying the target database which is different from the current database
                database_roles[database_role_name].clone(
                    target_database_role_name, target_database=new_db_def.name, mode=CreateMode.or_replace
                )
                database_roles_list = list(
                    databases[new_db_def.name].database_roles.iter(
                        limit=1, from_name=target_database_role_name.upper()[:-1]
                    )
                )
                assert len(database_roles_list) == 1

            finally:
                database_handle.drop()
                for database_role_handle in database_role_handles:
                    database_role_handle.drop()
    finally:
        database_handle_first.drop()
