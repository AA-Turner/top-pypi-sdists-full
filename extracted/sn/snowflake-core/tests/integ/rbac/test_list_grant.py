import pytest

from snowflake.core.grant._grant import Grant
from snowflake.core.grant._grantee import Grantees
from snowflake.core.grant._privileges import Privileges
from snowflake.core.grant._securables import Securables


@pytest.mark.use_accountadmin
@pytest.mark.usefixtures("backup_warehouse_fixture")
def test_list_grant(
    test_role_name,
    test_function_name,
    test_warehouse_name,
    grants,
    session,
    schema,
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

    # check roles have been granted
    grants_to_role = session.sql(f"SHOW GRANTS TO ROLE {test_role_name}").collect()
    grants_list = [grant for grant in grants_to_role]
    assert len(grants_list) > 0
    grants_to_role_list_with_api = [grants for grants in grants.to(Grantees.role(test_role_name))]
    assert len(grants_to_role_list_with_api) == len(grants_list)
