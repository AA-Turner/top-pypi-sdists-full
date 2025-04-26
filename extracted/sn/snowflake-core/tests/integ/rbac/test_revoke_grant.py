import pytest

from snowflake.core._common import DeleteMode
from snowflake.core.grant._grant import Grant
from snowflake.core.grant._grantee import Grantees
from snowflake.core.grant._privileges import Privileges
from snowflake.core.grant._securables import Securables


@pytest.mark.use_accountadmin
@pytest.mark.usefixtures("backup_warehouse_fixture")
def test_revoke_grant(
    grants,
    session,
    schema,
    test_role_name,
    test_database_role_name,
    test_warehouse_name,
    test_function_name,
):
    # grant roles

    grants.grant(
        Grant(
            grantee=Grantees.role(test_role_name),
            securable=Securables.warehouse(test_warehouse_name),
            privileges=[Privileges.operate],
        )
    )

    grants.grant(
        Grant(
            grantee=Grantees.role(test_role_name),
            securable=Securables.warehouse(test_warehouse_name),
            privileges=[Privileges.operate],
        )
    )

    grants.grant(
        Grant(
            grantee=Grantees.role(test_role_name),
            securable=Securables.all_tables(Securables.schema(schema.name)),
            privileges=[Privileges.select],
        )
    )

    grants.grant(
        Grant(
            grantee=Grantees.role(test_role_name),
            securable=Securables.function(f"{test_function_name}(number, number)"),
            privileges=[Privileges.all_privileges],
        )
    )

    grants.grant(
        Grant(
            grantee=Grantees.role(test_role_name),
            securable=Securables.future_tables(Securables.schema(schema.name)),
            privileges=[Privileges.select, Privileges.insert],
        )
    )

    grants.grant(
        Grant(
            grantee=Grantees.database_role(test_database_role_name),
            securable=Securables.all_tables(Securables.schema(schema.name)),
            privileges=[Privileges.select],
        )
    )

    # check roles have been granted
    grants_to_role = session.sql(f"SHOW GRANTS TO ROLE {test_role_name}").collect()
    grants_list = [grant for grant in grants_to_role]
    assert len(grants_list) > 0
    grants_to_database_role = session.sql(f"SHOW GRANTS TO DATABASE ROLE {test_database_role_name}").collect()
    grants_list = [grant for grant in grants_to_database_role]
    assert len(grants_list) > 0

    # revoke roles
    grants.revoke(
        Grant(
            grantee=Grantees.role(test_role_name),
            securable=Securables.warehouse(test_warehouse_name),
            privileges=[Privileges.operate],
        ),
        mode=DeleteMode.cascade,
    )

    grants.revoke(
        Grant(
            grantee=Grantees.role(test_role_name),
            securable=Securables.warehouse(test_warehouse_name),
            privileges=[Privileges.operate],
        )
    )

    grants.revoke(
        Grant(
            grantee=Grantees.role(test_role_name),
            securable=Securables.all_tables(Securables.schema(schema.name)),
            privileges=[Privileges.select],
        )
    )

    grants.revoke(
        Grant(
            grantee=Grantees.role(test_role_name),
            securable=Securables.function(f"{test_function_name}(number, number)"),
            privileges=[Privileges.all_privileges],
        )
    )

    grants.revoke(
        Grant(
            grantee=Grantees.role(test_role_name),
            securable=Securables.future_tables(Securables.schema(schema.name)),
            privileges=[Privileges.select, Privileges.insert],
        )
    )

    grants.revoke(
        Grant(
            grantee=Grantees.database_role(test_database_role_name),
            securable=Securables.all_tables(Securables.schema(schema.name)),
            privileges=[Privileges.select],
        )
    )

    # check revoked roles have been removed
    grants_to_role = session.sql(f"SHOW GRANTS TO ROLE {test_role_name}").collect()
    grants_list = [grant for grant in grants_to_role]
    assert len(grants_list) == 0
    grants_to_database_role = session.sql(f"SHOW GRANTS TO DATABASE ROLE {test_database_role_name}").collect()
    grants_list = [grant for grant in grants_to_database_role]
    assert len(grants_list) == 1  # USAGE ROLE WOULD ALWAYS BE THERE


@pytest.mark.use_accountadmin
@pytest.mark.usefixtures("backup_warehouse_fixture")
def test_revoke_grant_with_grant_option(
    grants,
    session,
    schema,
    test_role_name,
    test_database_role_name,
    test_warehouse_name,
    test_function_name,
):
    # grant roles

    grants.grant(
        Grant(
            grantee=Grantees.role(test_role_name),
            securable=Securables.warehouse(test_warehouse_name),
            privileges=[Privileges.operate],
            grant_option=True,
        )
    )

    grants.grant(
        Grant(
            grantee=Grantees.role(test_role_name),
            securable=Securables.warehouse(test_warehouse_name),
            privileges=[Privileges.operate],
            grant_option=True,
        )
    )

    grants.grant(
        Grant(
            grantee=Grantees.role(test_role_name),
            securable=Securables.all_tables(Securables.schema(schema.name)),
            privileges=[Privileges.select],
            grant_option=True,
        )
    )

    grants.grant(
        Grant(
            grantee=Grantees.role(test_role_name),
            securable=Securables.function(f"{test_function_name}(number, number)"),
            privileges=[Privileges.all_privileges],
            grant_option=True,
        )
    )

    grants.grant(
        Grant(
            grantee=Grantees.role(test_role_name),
            securable=Securables.future_tables(Securables.schema(schema.name)),
            privileges=[Privileges.select, Privileges.insert],
            grant_option=True,
        )
    )

    grants.grant(
        Grant(
            grantee=Grantees.database_role(test_database_role_name),
            securable=Securables.all_tables(Securables.schema(schema.name)),
            privileges=[Privileges.select],
            grant_option=True,
        )
    )

    # check roles have been granted
    grants_to_role = session.sql(f"SHOW GRANTS TO ROLE {test_role_name}").collect()
    grants_list = [grant for grant in grants_to_role]
    assert len(grants_list) > 0
    grants_to_database_role = session.sql(f"SHOW GRANTS TO DATABASE ROLE {test_database_role_name}").collect()
    grants_list = [grant for grant in grants_to_database_role]
    assert len(grants_list) > 0

    # revoke roles
    grants.revoke_grant_option(
        Grant(
            grantee=Grantees.role(test_role_name),
            securable=Securables.warehouse(test_warehouse_name),
            privileges=[Privileges.operate],
        ),
        mode=DeleteMode.cascade,
    )

    grants.revoke_grant_option(
        Grant(
            grantee=Grantees.role(test_role_name),
            securable=Securables.warehouse(test_warehouse_name),
            privileges=[Privileges.operate],
        )
    )

    grants.revoke_grant_option(
        Grant(
            grantee=Grantees.role(test_role_name),
            securable=Securables.all_tables(Securables.schema(schema.name)),
            privileges=[Privileges.select],
        )
    )

    grants.revoke_grant_option(
        Grant(
            grantee=Grantees.role(test_role_name),
            securable=Securables.function(f"{test_function_name}(number, number)"),
            privileges=[Privileges.all_privileges],
        )
    )

    grants.revoke_grant_option(
        Grant(
            grantee=Grantees.role(test_role_name),
            securable=Securables.future_tables(Securables.schema(schema.name)),
            privileges=[Privileges.select, Privileges.insert],
        )
    )

    grants.revoke_grant_option(
        Grant(
            grantee=Grantees.database_role(test_database_role_name),
            securable=Securables.all_tables(Securables.schema(schema.name)),
            privileges=[Privileges.select],
        )
    )

    # grant option removal does not remove already existing privileges
    grants_to_role = session.sql(f"SHOW GRANTS TO ROLE {test_role_name}").collect()
    grants_list = [grant for grant in grants_to_role]
    assert len(grants_list) > 0
    grants_to_database_role = session.sql(f"SHOW GRANTS TO DATABASE ROLE {test_database_role_name}").collect()
    grants_list = [grant for grant in grants_to_database_role]
    assert len(grants_list) > 0  # USAGE ROLE WOULD ALWAYS BE THERE
