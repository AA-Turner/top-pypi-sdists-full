import copy

import pytest as pytest

from snowflake.core.exceptions import NotFoundError
from tests.integ.utils import random_string

from .conftest import test_view_template


@pytest.mark.min_sf_ver("8.33.0")
def test_drop(views, temp_table):
    prefix = "test_view_"
    pre_create_count = len(list(views.iter(like = prefix+'%%')))
    view_name = random_string(10, prefix)
    view_handle = views[view_name]
    test_view = copy.deepcopy(test_view_template)
    test_view.name = view_name
    test_view.query = f"SELECT * FROM {temp_table.name}"
    views.create(test_view)
    created_count = len(list(views.iter(like = prefix+'%%')))
    view_handle.drop()
    after_drop_count = len(list(views.iter(like = prefix+'%%')))

    with pytest.raises(NotFoundError):
        view_handle.drop(if_exists=False)

    assert pre_create_count + 1 == created_count == after_drop_count + 1

    views.create(test_view)
    created_count = len(list(views.iter(like = prefix+'%%')))
    view_handle.drop(if_exists=True)
    after_drop_count = len(list(views.iter(like = prefix+'%%')))
    assert pre_create_count + 1 == created_count == after_drop_count + 1
