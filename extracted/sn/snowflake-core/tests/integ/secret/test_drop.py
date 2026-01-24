import copy

import pytest

from snowflake.core.exceptions import NotFoundError
from tests.integ.utils import random_string

from .conftest import test_generic_string_secret_template


def test_drop(secrets):
    prefix = "test_secret_drop_"
    pre_create_count = len(list(secrets.iter(like=prefix + "%")))

    name = random_string(10, prefix)
    secret_handle = secrets[name]

    secret = copy.deepcopy(test_generic_string_secret_template)
    secret.name = name
    secrets.create(secret)

    created_count = len(list(secrets.iter(like=prefix + "%")))
    assert pre_create_count + 1 == created_count

    secret_handle.drop()

    after_drop_count = len(list(secrets.iter(like=prefix + "%")))
    assert pre_create_count == after_drop_count

    with pytest.raises(NotFoundError):
        secret_handle.drop()
        secret_handle.drop(if_exists=False)

    secret_handle.drop(if_exists=True)
