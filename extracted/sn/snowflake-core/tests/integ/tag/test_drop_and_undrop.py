import copy

import pytest

from snowflake.core.exceptions import APIError, ConflictError, NotFoundError
from tests.integ.utils import random_string

from .conftest import test_tag_template


def test_drop(tags):
    prefix = "test_tag_drop_"
    pre_create_count = len(list(tags.iter(like=prefix + "%")))

    name = random_string(10, prefix)
    tag_handle = tags[name]

    tag = copy.deepcopy(test_tag_template)
    tag.name = name
    tags.create(tag)

    created_count = len(list(tags.iter(like=prefix + "%")))
    assert pre_create_count + 1 == created_count

    tag_handle.drop()

    after_drop_count = len(list(tags.iter(like=prefix + "%")))
    assert pre_create_count == after_drop_count

    with pytest.raises(NotFoundError):
        tag_handle.drop()
        tag_handle.drop(if_exists=False)

    tag_handle.drop(if_exists=True)


def test_undrop(tags):
    name = random_string(10, "test_tag_drop_undrop_")
    tag_handle = tags[name]

    tag = copy.deepcopy(test_tag_template)
    tag.name = name

    # attempting to undrop when the object never existed results in 400
    with pytest.raises(APIError):
        tag_handle.undrop()

    tags.create(tag)

    tag_handle.drop()
    tag_handle.undrop()
    assert tag_handle.fetch() is not None

    # attempting to undrop an existing object results in 409
    with pytest.raises(ConflictError):
        tag_handle.undrop()

    tag_handle.drop(if_exists=True)
