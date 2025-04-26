import pytest

from tests.integ.role.utils import assert_basic_grant
from tests.utils import random_string

from snowflake.core.role import ContainingScope, Securable
from snowflake.core.table import Table, TableColumn


pytestmark = pytest.mark.min_sf_ver("8.39.0")


@pytest.mark.use_accountadmin
def test_iter_grant_to(
    roles,
    test_role_name,
    test_role_name_2,
    test_database_role_name,
    test_database_for_grant_name,
    test_schema_for_grant_name,
    test_table_for_grant_name,
    tables_in_test_database,
):
    # test grant role
    roles[test_role_name].grant_role(role_type="ROLE", role=Securable(name=test_role_name_2))
    grants_list = list(roles[test_role_name].iter_grants_to())
    assert len(grants_list) == 1
    grant = grants_list[0]
    assert_basic_grant(grant)
    assert not grant.grant_option
    assert grant.securable.name == test_role_name_2.upper()
    assert grant.securable_type == "ROLE"

    roles[test_role_name].revoke_role(role_type="ROLE", role=Securable(name=test_role_name_2))

    # test grant database role becasue in this we will get the securable database name
    roles[test_role_name].grant_role(
        role_type="DATABASE ROLE",
        role=Securable(name=test_database_role_name, database=test_database_for_grant_name),
    )
    grants_list = list(roles[test_role_name].iter_grants_to())
    assert len(grants_list) == 1
    grant = grants_list[0]
    assert_basic_grant(grant)
    assert not grant.grant_option
    assert grant.securable.name == test_database_role_name.upper()
    assert grant.securable.database == test_database_for_grant_name.upper()
    assert grant.securable_type == "DATABASE ROLE"

    roles[test_role_name].revoke_role(
        role_type="DATABASE ROLE", role=Securable(name=test_database_role_name, database=test_database_for_grant_name)
    )

    # without securable name (to this account)
    roles[test_role_name].grant_privileges(privileges=["CREATE DATABASE"], securable_type="ACCOUNT")
    grants_list = list(roles[test_role_name].iter_grants_to())
    assert len(grants_list) == 1
    grant = grants_list[0]
    assert_basic_grant(grant)
    assert grant.securable.name is not None
    assert grant.securable_type == "ACCOUNT"
    assert grant.securable.database is None
    assert grant.securable.var_schema is None

    roles[test_role_name].revoke_privileges(privileges=["CREATE DATABASE"], securable_type="ACCOUNT")

    # grant on a schema here we will get the securable name as well as schema name
    roles[test_role_name].grant_privileges(
        privileges=["CREATE TASK"],
        securable_type="SCHEMA",
        securable=Securable(database=test_database_for_grant_name, name=test_schema_for_grant_name),
    )
    grants_list = list(roles[test_role_name].iter_grants_to())
    assert len(grants_list) == 1
    grant = grants_list[0]
    assert_basic_grant(grant)
    assert grant.securable.name == test_schema_for_grant_name.upper()
    assert grant.securable_type == "SCHEMA"
    assert grant.securable.database == test_database_for_grant_name

    roles[test_role_name].revoke_privileges(
        privileges=["CREATE TASK"],
        securable_type="SCHEMA",
        securable=Securable(database=test_database_for_grant_name, name=test_schema_for_grant_name),
    )

    # grant on a table
    roles[test_role_name].grant_privileges(
        privileges=["SELECT"],
        securable_type="TABLE",
        securable=Securable(
            database=test_database_for_grant_name, schema=test_schema_for_grant_name, name=test_table_for_grant_name
        ),
    )
    grants_list = list(roles[test_role_name].iter_grants_to())
    assert len(grants_list) == 1
    grant = grants_list[0]
    assert_basic_grant(grant)
    assert grant.securable.name == test_table_for_grant_name.upper()
    assert grant.securable_type == "TABLE"
    assert grant.securable.database == test_database_for_grant_name.upper()
    assert grant.securable.var_schema == test_schema_for_grant_name.upper()

    roles[test_role_name].revoke_privileges(
        privileges=["SELECT"],
        securable_type="TABLE",
        securable=Securable(
            database=test_database_for_grant_name, schema=test_schema_for_grant_name, name=test_table_for_grant_name
        ),
    )

    # all future tables in a schema
    roles[test_role_name].grant_future_privileges(
        privileges=["INSERT"],
        securable_type="TABLE",
        containing_scope=ContainingScope(database=test_database_for_grant_name, schema=test_schema_for_grant_name),
    )

    grants_list = list(roles[test_role_name].iter_grants_to())
    assert len(grants_list) == 0

    try:
        table_name = random_string(5, "test_grant_future_privileges_table_")
        columns = [TableColumn(name="col1", datatype="int"), TableColumn(name="col2", datatype="string")]
        test_table = Table(name=table_name, columns=columns)
        tables_in_test_database.create(test_table)

        grants_list = list(roles[test_role_name].iter_grants_to())
        assert len(grants_list) == 1
        grant = grants_list[0]
        assert_basic_grant(grant)
        assert grant.securable.name == table_name.upper()
        assert grant.securable_type == "TABLE"
        assert grant.securable.database == test_database_for_grant_name.upper()
        assert grant.securable.var_schema == test_schema_for_grant_name.upper()
    finally:
        tables_in_test_database[table_name].drop()


@pytest.mark.use_accountadmin
def test_iter_grant_on(roles, test_role_name):
    # because the role was created by accountadmin, accountadmin alreay have ownership privilages on the role
    grants_list = list(roles[test_role_name].iter_grants_on())
    assert len(grants_list) == 1
    grant = grants_list[0]
    assert grant.created_on is not None
    assert grant.privilege is not None
    assert grant.granted_on == "ROLE"
    assert grant.name == test_role_name.upper()
    assert grant.granted_to == "ROLE"
    assert grant.granted_by == "ACCOUNTADMIN"
    assert grant.granted_by_role_type == "ROLE"
    assert grant.grantee_name == "ACCOUNTADMIN"
    assert grant.grant_option


@pytest.mark.use_accountadmin
def test_iter_grant_of(roles, test_role_name, test_role_name_2):
    grants_list = list(roles[test_role_name].iter_grants_of())
    assert len(grants_list) == 0
    # test grant role
    roles[test_role_name_2].grant_role(role_type="ROLE", role=Securable(name=test_role_name))
    grants_list = list(roles[test_role_name].iter_grants_of())
    assert len(grants_list) == 1
    grant = grants_list[0]
    assert grant.created_on is not None
    assert grant.granted_by == "ACCOUNTADMIN"
    assert grant.grantee_name == test_role_name_2.upper()
    assert grant.granted_to == "ROLE"
    assert grant.role == test_role_name.upper()


@pytest.mark.use_accountadmin
def test_iter_future_grant_to(roles, test_role_name, test_database_for_grant_name, test_schema_for_grant_name):
    assert len(list(roles[test_role_name].iter_future_grants_to())) == 0
    # all future tables in a schema
    roles[test_role_name].grant_future_privileges(
        privileges=["INSERT"],
        securable_type="TABLE",
        containing_scope=ContainingScope(database=test_database_for_grant_name, schema=test_schema_for_grant_name),
    )

    grants_list = list(roles[test_role_name].iter_future_grants_to())
    assert len(grants_list) == 1
    grant = grants_list[0]
    assert_basic_grant(grant, False)  # future grants do not have granted_by
    assert grant.securable.name == '"<TABLE>"'
    assert grant.securable_type == "TABLE"
    assert grant.securable.database == test_database_for_grant_name.upper()
    assert grant.securable.var_schema == test_schema_for_grant_name.upper()
