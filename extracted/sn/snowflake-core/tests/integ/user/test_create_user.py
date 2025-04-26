import typing

import pytest

from snowflake.core import CreateMode
from snowflake.core.exceptions import ConflictError
from snowflake.core.user import User, UserCollection
from tests.utils import random_string


if typing.TYPE_CHECKING:
    from snowflake.snowpark import Session


@pytest.mark.snowpark
@pytest.mark.use_accountadmin
def test_create_user(users: UserCollection, session: "Session"):
    user_name = random_string(5, "test_create_user_1")
    test_user = User(
        name=user_name,
        password="test",
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
        user_ref = users.create(test_user, mode=CreateMode.error_if_exists)
        assert user_ref.name == user_name

        user = user_ref.fetch()

        assert user_ref.name.lower() == user_name
        assert user.first_name.lower() == "firstname"
        assert user.last_name.lower() == "lastname"
        assert user.email.lower() == "test@snowflake.com"
        assert user.created_on is not None
        assert user.comment.lower() == "test_comment"

        with pytest.raises(ConflictError):
            # assert throws error if user already exists
            users.create(test_user, mode=CreateMode.error_if_exists)

        user_ref.drop()
    finally:
        session.sql(f"DROP USER IF EXISTS {user_name}").collect()
