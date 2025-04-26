import pytest

from snowflake.core.user import Securable


pytestmark = pytest.mark.min_sf_ver("8.39.0")


@pytest.mark.use_accountadmin
def test_iter_grant(users, test_user_name, test_role_name, test_role_name_2):
    users[test_user_name].grant_role(role_type="ROLE", role=Securable(name=test_role_name))

    assert len(list(users[test_user_name].iter_grants_to())) == 1

    users[test_user_name].grant_role(role_type="ROLE", role=Securable(name=test_role_name_2))

    assert len(list(users[test_user_name].iter_grants_to())) == 2

    users[test_user_name].revoke_role(role_type="ROLE", role=Securable(name=test_role_name_2))

    assert len(list(users[test_user_name].iter_grants_to())) == 1
