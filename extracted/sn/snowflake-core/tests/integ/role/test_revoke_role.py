import pytest

from snowflake.core.exceptions import NotFoundError
from snowflake.core.role import ContainingScope, Securable


pytestmark = pytest.mark.min_sf_ver("8.39.0")


@pytest.mark.use_accountadmin
def test_revoke_role(roles, test_role_name, test_database_role_name, test_database_for_grant_name):
    roles[test_role_name].grant_role(
        role_type="DATABASE ROLE", role=Securable(name=test_database_role_name, database=test_database_for_grant_name)
    )

    assert len(list(roles[test_role_name].iter_grants_to())) == 1

    roles[test_role_name].revoke_role(
        role_type="DATABASE ROLE", role=Securable(name=test_database_role_name, database=test_database_for_grant_name)
    )

    assert len(list(roles[test_role_name].iter_grants_to())) == 0


@pytest.mark.use_accountadmin
def test_revoke_privileges(
    roles, test_role_name, test_database_for_grant_name, test_schema_for_grant_name, test_table_for_grant_name
):
    # grant on a table
    roles[test_role_name].grant_privileges(
        privileges=["SELECT"],
        securable_type="TABLE",
        securable=Securable(
            database=test_database_for_grant_name, schema=test_schema_for_grant_name, name=test_table_for_grant_name
        ),
    )

    assert len(list(roles[test_role_name].iter_grants_to())) == 1

    roles[test_role_name].revoke_privileges(
        privileges=["SELECT"],
        securable_type="TABLE",
        securable=Securable(
            database=test_database_for_grant_name, schema=test_schema_for_grant_name, name=test_table_for_grant_name
        ),
    )

    assert len(list(roles[test_role_name].iter_grants_to())) == 0

    # check we can revoke again

    roles[test_role_name].revoke_privileges(
        privileges=["SELECT"],
        securable_type="TABLE",
        securable=Securable(
            database=test_database_for_grant_name, schema=test_schema_for_grant_name, name=test_table_for_grant_name
        ),
    )

    # revoke on a random table
    with pytest.raises(NotFoundError):
        roles[test_role_name].revoke_privileges(
            privileges=["SELECT"],
            securable_type="TABLE",
            securable=Securable(
                database=test_database_for_grant_name, schema=test_schema_for_grant_name, name="RANDOM_TABLE"
            ),
        )


@pytest.mark.use_accountadmin
def test_revoke_privileges_on_all(roles, test_role_name, test_database_for_grant_name):
    # all schemas in a database
    roles[test_role_name].grant_privileges_on_all(
        privileges=["USAGE"],
        securable_type="SCHEMA",
        containing_scope=ContainingScope(database=test_database_for_grant_name),
    )

    # there would be more than one schema in the database
    assert len(list(roles[test_role_name].iter_grants_to())) >= 1

    roles[test_role_name].revoke_privileges_on_all(
        privileges=["USAGE"],
        securable_type="SCHEMA",
        containing_scope=ContainingScope(database=test_database_for_grant_name),
    )

    assert len(list(roles[test_role_name].iter_grants_to())) == 0


@pytest.mark.use_accountadmin
def test_revoke_future_privileges(roles, test_role_name, test_database_for_grant_name):
    # all future schemas in a database
    roles[test_role_name].grant_future_privileges(
        privileges=["USAGE"],
        securable_type="SCHEMA",
        containing_scope=ContainingScope(database=test_database_for_grant_name),
    )

    assert len(list(roles[test_role_name].iter_future_grants_to())) == 1

    roles[test_role_name].revoke_future_privileges(
        privileges=["USAGE"],
        securable_type="SCHEMA",
        containing_scope=ContainingScope(database=test_database_for_grant_name),
    )

    assert len(list(roles[test_role_name].iter_future_grants_to())) == 0


@pytest.mark.use_accountadmin
def test_revoke_grant_option_for_privileges(
    roles, test_role_name, test_database_for_grant_name, test_schema_for_grant_name, test_table_for_grant_name
):
    # grant on a table
    roles[test_role_name].grant_privileges(
        privileges=["SELECT"],
        securable_type="TABLE",
        securable=Securable(
            database=test_database_for_grant_name, schema=test_schema_for_grant_name, name=test_table_for_grant_name
        ),
        grant_option=True,
    )

    grants_list = list(roles[test_role_name].iter_grants_to())
    assert len(grants_list) == 1
    assert grants_list[0].grant_option

    roles[test_role_name].revoke_grant_option_for_privileges(
        privileges=["SELECT"],
        securable_type="TABLE",
        securable=Securable(
            database=test_database_for_grant_name, schema=test_schema_for_grant_name, name=test_table_for_grant_name
        ),
    )

    grants_list = list(roles[test_role_name].iter_grants_to())
    assert len(grants_list) == 1
    assert not grants_list[0].grant_option

    # revoke grant option on a grant which does not have grant option
    roles[test_role_name].revoke_grant_option_for_privileges(
        privileges=["SELECT"],
        securable_type="TABLE",
        securable=Securable(
            database=test_database_for_grant_name, schema=test_schema_for_grant_name, name=test_table_for_grant_name
        ),
    )

    grants_list = list(roles[test_role_name].iter_grants_to())
    assert len(grants_list) == 1
    assert not grants_list[0].grant_option


@pytest.mark.use_accountadmin
def test_revoke_grant_option_for_privileges_on_all(roles, test_role_name, test_database_for_grant_name):
    # all schemas in a database
    roles[test_role_name].grant_privileges_on_all(
        privileges=["USAGE"],
        securable_type="SCHEMA",
        containing_scope=ContainingScope(database=test_database_for_grant_name),
        grant_option=True,
    )

    # there would be more than one schema in the database
    grants_list = list(roles[test_role_name].iter_grants_to())
    number_of_previleges = len(grants_list)
    assert number_of_previleges >= 1
    for grant in grants_list:
        assert grant.grant_option

    roles[test_role_name].revoke_grant_option_for_privileges_on_all(
        privileges=["USAGE"],
        securable_type="SCHEMA",
        containing_scope=ContainingScope(database=test_database_for_grant_name),
    )

    grants_list = list(roles[test_role_name].iter_grants_to())
    assert len(grants_list) == number_of_previleges
    for grant in grants_list:
        assert not grant.grant_option


@pytest.mark.use_accountadmin
def test_revoke_grant_option_for_future_privileges(roles, test_role_name, test_database_for_grant_name):
    # all future schemas in a database
    roles[test_role_name].grant_future_privileges(
        privileges=["USAGE"],
        securable_type="SCHEMA",
        containing_scope=ContainingScope(database=test_database_for_grant_name),
        grant_option=True,
    )

    grants_list = list(roles[test_role_name].iter_future_grants_to())
    assert len(grants_list) == 1
    for grant in grants_list:
        assert grant.grant_option

    roles[test_role_name].revoke_grant_option_for_future_privileges(
        privileges=["USAGE"],
        securable_type="SCHEMA",
        containing_scope=ContainingScope(database=test_database_for_grant_name),
    )

    grants_list = list(roles[test_role_name].iter_future_grants_to())
    assert len(grants_list) == 1
    for grant in grants_list:
        assert not grant.grant_option
