import typing

import pytest

from snowflake.core import CreateMode
from snowflake.core.exceptions import NotFoundError
from snowflake.core.user import User, UserCollection
from tests.utils import random_string


if typing.TYPE_CHECKING:
    from snowflake.snowpark import Session


@pytest.mark.snowpark
@pytest.mark.use_accountadmin
def test_delete_user(users: UserCollection, session: "Session"):
    user_name = random_string(5, "test_create_user_1")
    try:
        test_user = User(name=user_name, comment="test_comment")

        user_ref = users.create(test_user, mode=CreateMode.error_if_exists)
        assert user_ref.name == user_name
        user_ref.drop()

        with pytest.raises(
            NotFoundError,
        ):
            users[user_name].drop(if_exists=False)
            users[user_name].fetch()

        user_ref.drop(if_exists=True)
    finally:
        session.sql(f"DROP USER IF EXISTS {user_name}").collect()
