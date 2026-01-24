import copy

import pytest

from snowflake.core.exceptions import NotFoundError
from tests.integ.utils import random_string

from .conftest import test_password_policy_template


def test_drop(password_policies):
    prefix = "test_password_policy_drop_"
    pre_create_count = len(list(password_policies.iter(like=prefix + "%")))

    name = random_string(10, prefix)
    password_policy_handle = password_policies[name]

    password_policy = copy.deepcopy(test_password_policy_template)
    password_policy.name = name
    password_policies.create(password_policy)

    created_count = len(list(password_policies.iter(like=prefix + "%")))
    assert pre_create_count + 1 == created_count

    password_policy_handle.drop()

    after_drop_count = len(list(password_policies.iter(like=prefix + "%")))
    assert pre_create_count == after_drop_count

    with pytest.raises(NotFoundError):
        password_policy_handle.drop()
        password_policy_handle.drop(if_exists=False)

    password_policy_handle.drop(if_exists=True)
