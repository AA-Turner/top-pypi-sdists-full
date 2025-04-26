import typing

import pytest

from snowflake.core import CreateMode
from snowflake.core.user import User, UserCollection

from ..utils import random_string


if typing.TYPE_CHECKING:
    from snowflake.snowpark import Session


@pytest.mark.snowpark
@pytest.mark.use_accountadmin
def test_iter(users: UserCollection, session: "Session"):
    user_name_one = random_string(5, "test_create_user_1")
    user_name_two = random_string(5, "test_create_user_")
    user_name_three = random_string(5, "test_create_user_")

    def create_user(user_name) -> User:
        test_user = User(user_name)
        return users.create(test_user, mode=CreateMode.error_if_exists)

    try:
        test_user_one = create_user(user_name_one)
        test_user_two = create_user(user_name_two)
        test_user_three = create_user(user_name_three)

        user_names = [user.name for user in users.iter()]

        assert test_user_one.name.upper() in user_names
        assert test_user_two.name.upper() in user_names
        assert test_user_three.name.upper() in user_names

        user_names_filtered = [user.name for user in users.iter(like="test_create_user_%")]
        assert len(user_names_filtered) < len(user_names)

        user_names_filtered = [user.name for user in users.iter(like="test_create_user_1%")]
        assert test_user_one.name.upper() in user_names_filtered
        assert test_user_two.name.upper() not in user_names_filtered
        assert test_user_three.name.upper() not in user_names_filtered

        user_names_filtered = [user.name for user in users.iter(like="test_create_user_%", limit=2)]
        assert len(user_names_filtered) == 2

        user_names_filtered = [
            user.name for user in users.iter(starts_with="TEST_CREATE_USER_1", like="test_create_user_%")
        ]
        assert test_user_one.name.upper() in user_names_filtered
        assert test_user_two.name.upper() not in user_names_filtered
        assert test_user_three.name.upper() not in user_names_filtered

        users[user_name_one].drop()
        users[user_name_two].drop()
        users[user_name_three].drop()
    finally:
        for name in [user_name_one, user_name_two, user_name_three]:
            session.sql(f"DROP USER IF EXISTS {name}").collect()
