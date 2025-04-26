import typing

import pytest

from snowflake.core.user import User, UserCollection
from tests.utils import random_string


if typing.TYPE_CHECKING:
    from snowflake.snowpark import Session


# TODO: SNOW-1542604 Grant accountadmin to Jenkins account
# pytestmark = pytest.mark.jenkins

@pytest.mark.snowpark
@pytest.mark.use_accountadmin
@pytest.mark.min_sf_ver("8.32.0")
def test_create_or_alter_user(users: UserCollection, session: "Session"):
    user_name = random_string(5, "test_create_user_1")
    test_user_basic = User(
        name=user_name,
        password="test",
    )
    test_user_props = User(
        name=user_name,
        display_name="test_name",
        first_name="firstname",
        last_name="lastname",
        email="test@snowflake.com",
        must_change_password=False,
        disabled=False,
        days_to_expiry=1,
        mins_to_unlock=10,
        mins_to_bypass_mfa=60,
        default_warehouse="test",
        default_namespace="test",
        default_role="public",
        default_secondary_roles="ALL",
        comment="test_comment",
    )

    try:
        users[user_name].create_or_alter(test_user_basic)

        user = users[user_name].fetch()

        assert user.name.lower() == user_name
        assert user.first_name is None
        assert user.last_name is None
        assert user.email is None
        assert user.created_on is not None
        assert user.comment is None

        users[user_name].create_or_alter(test_user_props)

        user = users[user_name].fetch()
        assert user.name.lower() == user_name
        assert user.first_name.lower() == "firstname"
        assert user.last_name.lower() == "lastname"
        assert user.email.lower() == "test@snowflake.com"
        assert user.created_on is not None
        assert user.comment.lower() == "test_comment"

        users[user_name].drop()
    finally:
        session.sql(f"DROP USER IF EXISTS {user_name}").collect()
