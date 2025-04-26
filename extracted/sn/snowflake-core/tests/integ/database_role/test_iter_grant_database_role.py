import pytest

from snowflake.core.database_role import ContainingScope, Securable
from snowflake.core.table import Table, TableColumn
from tests.integ.database_role.utils import assert_basic_grant, clear_default_grant
from tests.utils import random_string


pytestmark = pytest.mark.min_sf_ver("8.39.0")


@pytest.mark.use_accountadmin
def test_iter_grant_to(
    database_roles_in_test_database,
    test_database_role_name,
    test_database_role_name_2,
    test_database_for_grant_name,
    test_schema_for_grant_name,
    test_table_for_grant_name,
    tables_in_test_database,
):
    # test grant database role becasue in this we will get the securable database name
    database_roles_in_test_database[test_database_role_name].grant_role(
        role_type="DATABASE ROLE",
        role=Securable(name=test_database_role_name_2, database=test_database_for_grant_name),
    )
    grants_list = list(database_roles_in_test_database[test_database_role_name].iter_grants_to())
    assert len(grants_list) == 2
    grants_list = clear_default_grant(grants_list)
    grant = grants_list[0]
    assert_basic_grant(grant)
    assert not grant.grant_option
    assert grant.securable.name == test_database_role_name_2.upper()
    assert grant.securable.database == test_database_for_grant_name.upper()
    assert grant.securable_type == "DATABASE ROLE"

    # testing limit
    grants_list = list(database_roles_in_test_database[test_database_role_name].iter_grants_to(show_limit=1))
    assert len(grants_list) == 1

    database_roles_in_test_database[test_database_role_name].revoke_role(
        role_type="DATABASE ROLE",
        role=Securable(name=test_database_role_name_2, database=test_database_for_grant_name),
    )

    # grant on a schema here we will get the securable name as well as schema name
    database_roles_in_test_database[test_database_role_name].grant_privileges(
        privileges=["CREATE TASK"],
        securable_type="SCHEMA",
        securable=Securable(database=test_database_for_grant_name, name=test_schema_for_grant_name),
    )
    grants_list = list(database_roles_in_test_database[test_database_role_name].iter_grants_to())
    assert len(grants_list) == 2
    grants_list = clear_default_grant(grants_list)
    grant = grants_list[0]
    assert_basic_grant(grant)
    assert grant.securable.name == test_schema_for_grant_name.upper()
    assert grant.securable_type == "SCHEMA"
    assert grant.securable.database == test_database_for_grant_name

    database_roles_in_test_database[test_database_role_name].revoke_privileges(
        privileges=["CREATE TASK"],
        securable_type="SCHEMA",
        securable=Securable(database=test_database_for_grant_name, name=test_schema_for_grant_name),
    )

    # grant on a table
    database_roles_in_test_database[test_database_role_name].grant_privileges(
        privileges=["SELECT"],
        securable_type="TABLE",
        securable=Securable(
            database=test_database_for_grant_name,
            schema=test_schema_for_grant_name,
            name=test_table_for_grant_name,
        ),
    )
    grants_list = list(database_roles_in_test_database[test_database_role_name].iter_grants_to())
    assert len(grants_list) == 2
    grants_list = clear_default_grant(grants_list)
    grant = grants_list[0]
    assert_basic_grant(grant)
    assert grant.securable.name == test_table_for_grant_name.upper()
    assert grant.securable_type == "TABLE"
    assert grant.securable.database == test_database_for_grant_name.upper()
    assert grant.securable.var_schema == test_schema_for_grant_name.upper()

    database_roles_in_test_database[test_database_role_name].revoke_privileges(
        privileges=["SELECT"],
        securable_type="TABLE",
        securable=Securable(
            database=test_database_for_grant_name,
            schema=test_schema_for_grant_name,
            name=test_table_for_grant_name,
        ),
    )

    # all future tables in a schema
    database_roles_in_test_database[test_database_role_name].grant_future_privileges(
        privileges=["INSERT"],
        securable_type="TABLE",
        containing_scope=ContainingScope(database=test_database_for_grant_name, schema=test_schema_for_grant_name),
    )

    grants_list = list(database_roles_in_test_database[test_database_role_name].iter_grants_to())
    assert len(grants_list) == 1

    try:
        table_name = random_string(5, "test_grant_future_privileges_table_")
        columns = [TableColumn(name="col1", datatype="int"), TableColumn(name="col2", datatype="string")]
        test_table = Table(name=table_name, columns=columns)
        tables_in_test_database.create(test_table)

        grants_list = list(database_roles_in_test_database[test_database_role_name].iter_grants_to())
        assert len(grants_list) == 2
        grants_list = clear_default_grant(grants_list)
        grant = grants_list[0]
        assert_basic_grant(grant)
        assert grant.securable.name == table_name.upper()
        assert grant.securable_type == "TABLE"
        assert grant.securable.database == test_database_for_grant_name.upper()
        assert grant.securable.var_schema == test_schema_for_grant_name.upper()
    finally:
        tables_in_test_database[table_name].drop()


@pytest.mark.use_accountadmin
def test_iter_future_grant_to(
    database_roles_in_test_database,
    test_database_role_name,
    test_database_for_grant_name,
    test_schema_for_grant_name,
):
    assert len(list(database_roles_in_test_database[test_database_role_name].iter_future_grants_to())) == 0
    # all future tables in a schema
    database_roles_in_test_database[test_database_role_name].grant_future_privileges(
        privileges=["INSERT"],
        securable_type="TABLE",
        containing_scope=ContainingScope(database=test_database_for_grant_name, schema=test_schema_for_grant_name),
    )

    grants_list = list(database_roles_in_test_database[test_database_role_name].iter_future_grants_to())
    assert len(grants_list) == 1
    grant = grants_list[0]
    assert_basic_grant(grant, False)  # future grants do not have granted_by
    assert grant.securable.name == '"<TABLE>"'
    assert grant.securable_type == "TABLE"
    assert grant.securable.database == test_database_for_grant_name.upper()
    assert grant.securable.var_schema == test_schema_for_grant_name.upper()

    database_roles_in_test_database[test_database_role_name].grant_future_privileges(
        privileges=["UPDATE"],
        securable_type="TABLE",
        containing_scope=ContainingScope(database=test_database_for_grant_name, schema=test_schema_for_grant_name),
    )

    grants_list = list(database_roles_in_test_database[test_database_role_name].iter_future_grants_to())
    assert len(grants_list) == 2

    # testing limit
    grants_list = list(database_roles_in_test_database[test_database_role_name].iter_future_grants_to(show_limit=1))
    assert len(grants_list) == 1
