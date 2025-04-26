import pytest

from snowflake.core.exceptions import NotFoundError
from snowflake.core.grant._grant import Grant
from snowflake.core.grant._grantee import Grantees
from snowflake.core.grant._privileges import Privileges
from snowflake.core.grant._securables import Securables
from snowflake.core.role import Role
from tests.utils import random_string


@pytest.mark.use_accountadmin
def test_apply_grant(
    grants, database, schema, test_database_role_name, test_share_name, test_user_name, test_table_name, test_role_name
):
    # grants to current account
    grants.grant(
        Grant(
            grantee=Grantees.role(name=test_role_name),
            securable=Securables.current_account,
            privileges=[
                Privileges.create_database,
                Privileges.create_compute_pool,
                Privileges.create_warehouse,
                Privileges.create_account,
            ],
        )
    )

    # grants to database
    grants.grant(
        Grant(
            grantee=Grantees.role(name=test_role_name),
            securable=Securables.database(database.name),
            privileges=[Privileges.modify, Privileges.monitor],
        )
    )

    # grants to schema
    grants.grant(
        Grant(
            grantee=Grantees.role(name=test_role_name),
            securable=Securables.schema(schema.name),
            privileges=[
                Privileges.create_task,
            ],
        )
    )

    # grants to all schemas in database
    grants.grant(
        Grant(
            grantee=Grantees.role(name=test_role_name),
            securable=Securables.all_schemas(Securables.database(database.name)),
            privileges=[
                Privileges.usage,
            ],
        )
    )

    # grants to future schemas in database
    grants.grant(
        Grant(
            grantee=Grantees.role(name=test_role_name),
            securable=Securables.future_schemas(Securables.database(database.name)),
            privileges=[
                Privileges.create_table,
            ],
        )
    )

    # grants to table
    grants.grant(
        Grant(
            grantee=Grantees.role(name=test_role_name),
            securable=Securables.table(test_table_name),
            privileges=[
                Privileges.select,
                Privileges.insert,
                Privileges.delete,
            ],
        )
    )

    # grants to all tables in schema
    grants.grant(
        Grant(
            grantee=Grantees.role(name=test_role_name),
            securable=Securables.all_tables(Securables.schema(schema.name)),
            privileges=[Privileges.insert],
        )
    )

    # grants to future tables in schema
    grants.grant(
        Grant(
            grantee=Grantees.role(name=test_role_name),
            securable=Securables.future_tables(Securables.schema(schema.name)),
            privileges=[Privileges.delete],
        )
    )

    # grants create schema to database
    grants.grant(
        Grant(
            grantee=Grantees.role(name=test_role_name),
            securable=Securables.database(database.name),
            privileges=[Privileges.create_schema],
        )
    )

    # grants create task to schema
    grants.grant(
        Grant(
            grantee=Grantees.database_role(name=test_database_role_name),
            securable=Securables.schema(schema.name),
            privileges=[Privileges.create_task],
        )
    )

    # grants create task to schema
    grants.grant(
        Grant(
            grantee=Grantees.database_role(name=test_database_role_name),
            securable=Securables.schema(schema.name),
            privileges=[Privileges.create_task],
        )
    )

    grants.grant(
        Grant(
            grantee=Grantees.database_role(name=test_database_role_name),
            securable=Securables.all_schemas(Securables.database(database.name)),
            privileges=[Privileges.usage],
        )
    )

    grants.grant(
        Grant(
            grantee=Grantees.database_role(name=test_database_role_name),
            securable=Securables.future_schemas(Securables.database(database.name)),
            privileges=[Privileges.create_table],
        )
    )

    grants.grant(
        Grant(
            grantee=Grantees.database_role(name=test_database_role_name),
            securable=Securables.table(test_table_name),
            privileges=[Privileges.select],
            grant_option=True,
        )
    )

    grants.grant(
        Grant(
            grantee=Grantees.database_role(name=test_database_role_name),
            securable=Securables.all_tables(Securables.schema(schema.name)),
            privileges=[Privileges.insert],
        )
    )

    grants.grant(
        Grant(
            grantee=Grantees.database_role(name=test_database_role_name),
            securable=Securables.future_tables(Securables.schema(schema.name)),
            privileges=[Privileges.delete],
        )
    )

    grants.grant(
        Grant(
            grantee=Grantees.share(name=test_share_name),
            securable=Securables.database(database.name),
            privileges=[Privileges.usage],
        )
    )

    grants.grant(
        Grant(
            grantee=Grantees.share(name=test_share_name),
            securable=Securables.schema(schema.name),
            privileges=[Privileges.usage],
        )
    )

    grants.grant(
        Grant(
            grantee=Grantees.share(name=test_share_name),
            securable=Securables.table(test_table_name),
            privileges=[Privileges.select],
        )
    )

    grants.grant(
        Grant(
            grantee=Grantees.share(name=test_share_name),
            securable=Securables.all_iceberg_tables(Securables.schema(schema.name)),
            privileges=[Privileges.select],
        )
    )

    grants.grant(
        Grant(
            grantee=Grantees.share(name=test_share_name),
            securable=Securables.database(database.name),
            privileges=[Privileges.reference_usage],
        )
    )

    grants.grant(
        Grant(
            grantee=Grantees.user(name=test_user_name),
            securable=Securables.role(test_role_name),
        )
    )

    grants.grant(
        Grant(
            grantee=Grantees.role(name=test_role_name), securable=Securables.database_role(name=test_database_role_name)
        )
    )


@pytest.mark.use_accountadmin
def test_apply_grant_with_grant_opt(grants, test_role_name):
    grants.grant(
        Grant(
            grantee=Grantees.role(name=test_role_name),
            securable=Securables.current_account,
            privileges=[Privileges.create_database],
            grant_option=False,
        )
    )


@pytest.mark.use_accountadmin
def test_grant_role_to_another_role(roles, grants, session):
    role_one = random_string(4, "test_grant_role_")
    role_two = random_string(4, "test_grant_role_")

    try:
        for role in [role_one, role_two]:
            roles.create(Role(name=role, comment="test_comment"))

        grants.grant(Grant(grantee=Grantees.role(role_one), securable=Securables.role(role_two)))

    finally:
        session.sql(f"DROP ROLE IF EXISTS {role_one}")
        session.sql(f"DROP ROLE IF EXISTS {role_two}")


def test_grants_for_invalid_role_names(grants):
    with pytest.raises(NotFoundError):
        grants.grant(
            Grant(
                grantee=Grantees.role(name='"some-random-role"'),
                securable=Securables.current_account,
                privileges=[Privileges.create_database],
                grant_option=False,
            )
        )


def test_grants_for_invalid_db_securable(grants):
    with pytest.raises(NotFoundError):
        grants.grant(
            Grant(
                grantee=Grantees.role(name="public"),
                securable=Securables.database("invaliddb123"),
                privileges=[Privileges.create_database],
                grant_option=False,
            )
        )
