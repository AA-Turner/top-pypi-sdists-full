import pytest

from snowflake.core.database_role import ContainingScope, Securable
from snowflake.core.schema import Schema
from snowflake.core.table import Table, TableColumn
from tests.utils import random_string


pytestmark = pytest.mark.min_sf_ver("8.39.0")


@pytest.mark.use_accountadmin
def test_grant_role(database_roles_in_test_database, test_database_role_name, test_database_role_name_2):
    database_roles_in_test_database[test_database_role_name].grant_role(
        role_type="DATABASE ROLE", role=Securable(name=test_database_role_name_2)
    )

    # running the same grant again should not be an issue
    database_roles_in_test_database[test_database_role_name].grant_role(
        role_type="DATABASE ROLE", role=Securable(name=test_database_role_name_2)
    )

    grants = list(database_roles_in_test_database[test_database_role_name].iter_grants_to())
    assert len(grants) == 2  # a grant of usage on database is by default granted to a database role
    for grant in grants:
        assert grant.securable_type in ["DATABASE", "DATABASE ROLE"]


@pytest.mark.use_accountadmin
def test_grant_privileges(
    database_roles_in_test_database,
    test_database_role_name,
    test_database_for_grant_name,
    test_schema_for_grant_name,
    test_table_for_grant_name,
):
    # grant on a specific database
    database_roles_in_test_database[test_database_role_name].grant_privileges(
        privileges=["MODIFY", "MONITOR"],
        securable_type="DATABASE",
        securable=Securable(name=test_database_for_grant_name),
    )

    # grant on a schema
    database_roles_in_test_database[test_database_role_name].grant_privileges(
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

    assert len(list(database_roles_in_test_database[test_database_role_name].iter_grants_to())) == 5


@pytest.mark.use_accountadmin
def test_grant_privileges_with_grant_option(
    database_roles_in_test_database,
    test_database_role_name,
    test_database_for_grant_name,
    test_schema_for_grant_name,
    test_table_for_grant_name,
):
    # grant on a specific database
    database_roles_in_test_database[test_database_role_name].grant_privileges(
        privileges=["MODIFY", "MONITOR"],
        securable_type="DATABASE",
        securable=Securable(name=test_database_for_grant_name),
        grant_option=True,
    )

    # grant on a schema
    database_roles_in_test_database[test_database_role_name].grant_privileges(
        privileges=["CREATE TASK"],
        securable_type="SCHEMA",
        securable=Securable(database=test_database_for_grant_name, name=test_schema_for_grant_name),
        grant_option=True,
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
        grant_option=True,
    )

    grant_list = list(database_roles_in_test_database[test_database_role_name].iter_grants_to())
    assert len(grant_list) == 5

    for grant in grant_list:
        if not (grant.securable_type == "DATABASE" and grant.privileges == ["USAGE"]):
            assert grant.grant_option


@pytest.mark.use_accountadmin
def test_grant_privileges_on_all(
    test_database_role_name,
    test_database_for_grant_name,
    test_schema_for_grant_name,
    test_table_for_grant_name,
    database_roles_in_test_database,
):
    del test_table_for_grant_name
    # all schemas in a database
    database_roles_in_test_database[test_database_role_name].grant_privileges_on_all(
        privileges=["USAGE"],
        securable_type="SCHEMA",
        containing_scope=ContainingScope(database=test_database_for_grant_name),
    )

    # all tables in a schema
    database_roles_in_test_database[test_database_role_name].grant_privileges_on_all(
        privileges=["SELECT"],
        securable_type="TABLE",
        containing_scope=ContainingScope(database=test_database_for_grant_name, schema=test_schema_for_grant_name),
    )

    grants = list(database_roles_in_test_database[test_database_role_name].iter_grants_to())
    for grant in grants:
        if not (grant.securable_type == "DATABASE" and grant.privileges == ["USAGE"]):
            if grant.securable_type == "SCHEMA":
                assert grant.securable.database == test_database_for_grant_name.upper()
                assert grant.securable.name is not None
            else:
                assert grant.securable_type == "TABLE"
                assert grant.securable.database == test_database_for_grant_name.upper()
                assert grant.securable.var_schema == test_schema_for_grant_name.upper()
                assert grant.securable.name is not None
    assert len(grants) >= 3


@pytest.mark.use_accountadmin
def test_grant_future_privileges(
    database_roles_in_test_database,
    test_database_role_name,
    test_database_for_grant_name,
    test_schema_for_grant_name,
    backup_database_schema,
    schemas_in_test_database,
    tables_in_test_database,
):
    del backup_database_schema
    # all future schemas in a database
    database_roles_in_test_database[test_database_role_name].grant_future_privileges(
        privileges=["USAGE"],
        securable_type="SCHEMA",
        containing_scope=ContainingScope(database=test_database_for_grant_name),
    )

    # all future tables in a schema
    database_roles_in_test_database[test_database_role_name].grant_future_privileges(
        privileges=["INSERT"],
        securable_type="TABLE",
        containing_scope=ContainingScope(database=test_database_for_grant_name, schema=test_schema_for_grant_name),
    )

    assert len(list(database_roles_in_test_database[test_database_role_name].iter_grants_to())) == 1

    # create a new schema and table
    try:
        schema_name = random_string(4, "test_grant_future_privileges_schema_")
        schemas_in_test_database.create(Schema(name=schema_name))
        table_name = random_string(5, "test_grant_future_privileges_table_")
        columns = [TableColumn(name="col1", datatype="int"), TableColumn(name="col2", datatype="string")]
        test_table = Table(name=table_name, columns=columns)
        tables_in_test_database.create(test_table)

        assert len(list(database_roles_in_test_database[test_database_role_name].iter_grants_to())) == 3
    finally:
        schemas_in_test_database[schema_name].drop()
        tables_in_test_database[table_name].drop()
