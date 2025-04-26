import pytest

from snowflake.core.exceptions import NotFoundError
from snowflake.core.user import Securable


pytestmark = pytest.mark.min_sf_ver("8.39.0")


@pytest.mark.use_accountadmin
def test_grant_user(users, test_user_name, test_role_name):
    users[test_user_name].grant_role(role_type="ROLE", role=Securable(name=test_role_name))

    assert len(list(users[test_user_name].iter_grants_to())) == 1

    # running the same grant again should not be an issue
    users[test_user_name].grant_role(role_type="ROLE", role=Securable(name=test_role_name))

    assert len(list(users[test_user_name].iter_grants_to())) == 1

    # granting a RANDOM ROLE which does not exist
    with pytest.raises(NotFoundError):
        users[test_user_name].grant_role(role_type="ROLE", role=Securable(name="random_role"))

    # granting a ROLE to a user which does not exist
    with pytest.raises(NotFoundError):
        users["RANDOM"].grant_role(role_type="ROLE", role=Securable(name=test_role_name))
