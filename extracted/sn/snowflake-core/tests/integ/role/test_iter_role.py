import pytest

from tests.utils import random_string

from snowflake.core.role import Role


@pytest.mark.use_accountadmin
def test_iter(roles, session):
    role_name_1 = random_string(5, "test_role_1")
    role_name_2 = random_string(5, "test_role_2")
    try:
        test_role = Role(name=role_name_1, comment="test role 1")
        test_role_1 = roles.create(test_role)
        test_role = Role(name=role_name_2, comment="test role 2")
        test_role_2 = roles.create(test_role)

        test_roles = [role.name for role in roles.iter()]

        assert test_role_1.name.upper() in test_roles
        assert test_role_2.name.upper() in test_roles

        # checking the fields of the role
        test_role_random = [role for role in roles.iter()][0]
        assert test_role_random.created_on is not None
        assert test_role_random.assigned_to_users is not None
        assert test_role_random.granted_to_roles is not None
        assert test_role_random.granted_roles is not None
        assert test_role_random.is_default is not None
        assert test_role_random.is_inherited is not None
        assert test_role_random.is_current is not None
        assert test_role_random.comment is not None

        test_roles = [role.name for role in roles.iter(like="TEST_ROLE_%")]

        assert test_role_1.name.upper() in test_roles
        assert test_role_2.name.upper() in test_roles

        test_roles = [role.name for role in roles.iter(like="TEST_ROLE_1%")]

        assert test_role_1.name.upper() in test_roles
        assert test_role_2.name.upper() not in test_roles

        test_roles = roles.iter(limit=1)
        assert len(list(test_roles)) == 1

        # show roles starts_with has a bug and isn't filtering the output as expected.
        # test_roles = roles.iter(starts_with="TEST_ROLE")
        # assert len(list(test_roles)) == 1

    finally:
        roles[test_role_1.name].drop(if_exists=True)
        roles[test_role_2.name].drop(if_exists=True)
