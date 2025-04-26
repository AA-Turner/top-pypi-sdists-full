import pytest

from snowflake.core.exceptions import NotFoundError
from snowflake.core.user import Securable


pytestmark = pytest.mark.min_sf_ver("8.39.0")


@pytest.mark.use_accountadmin
def test_revoke_user(users, test_user_name, test_role_name):
    users[test_user_name].grant_role(role_type="ROLE", role=Securable(name=test_role_name))

    assert len(list(users[test_user_name].iter_grants_to())) == 1

    users[test_user_name].revoke_role(role_type="ROLE", role=Securable(name=test_role_name))

    assert len(list(users[test_user_name].iter_grants_to())) == 0

    # revoking the same role again should not be an issue
    users[test_user_name].revoke_role(role_type="ROLE", role=Securable(name=test_role_name))

    # revoking a random role from a user
    with pytest.raises(NotFoundError):
        users[test_user_name].revoke_role(role_type="ROLE", role=Securable(name="RANDOM"))

    # revoking a role from a random user
    with pytest.raises(NotFoundError):
        users["RANDOM"].revoke_role(role_type="ROLE", role=Securable(name=test_role_name))
