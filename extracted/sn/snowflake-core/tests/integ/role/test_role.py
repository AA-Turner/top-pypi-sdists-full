import pytest

from tests.utils import random_string

from snowflake.core._common import CreateMode
from snowflake.core.exceptions import ConflictError, NotFoundError
from snowflake.core.role import Role


@pytest.mark.use_accountadmin
def test_create(roles, root, session):
    role_name = random_string(4, "test_create_role_")
    try:
        test_role = Role(name=role_name, comment="test_comment")
        created_role = roles.create(test_role)
        assert created_role.name == role_name

        # create role with already existing name with mode or_replace
        test_role.comment = "new comment"
        roles.create(test_role, mode=CreateMode.or_replace)
        replaced_roles = list(roles.iter(like=role_name))
        assert len(replaced_roles) == 1
        replaced_role = replaced_roles[0]
        assert replaced_role is not None
        assert replaced_role.name == role_name.upper()
        assert replaced_role.comment == "new comment"

        with pytest.raises(ConflictError):
            # throws error if test_role is already present.
            roles.create(test_role, mode=CreateMode.error_if_exists)

        # will succeed without any errors.
        roles.create(test_role, mode=CreateMode.if_not_exists)

    finally:
        roles[role_name].drop(if_exists=True)


@pytest.mark.use_accountadmin
def test_drop(roles, root, session):
    role_name = random_string(4, "test_drop_role_")
    try:
        test_role = Role(name=role_name, comment="test drop role")

        created_role = roles.create(test_role)
        assert created_role.name == role_name
        roles[role_name].drop()
        created_role = None

        with pytest.raises(NotFoundError):
            # throws error as test_role is already dropped
            roles[role_name].drop()

        roles[role_name].drop(if_exists=True)
    finally:
        roles[role_name].drop(if_exists=True)
