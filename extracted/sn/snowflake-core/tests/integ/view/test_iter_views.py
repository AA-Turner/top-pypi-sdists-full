import copy

from contextlib import suppress

import pytest as pytest

from snowflake.core.exceptions import NotFoundError
from tests.integ.utils import random_string

from ...utils import ensure_snowflake_version
from .conftest import test_view_template


@pytest.fixture(scope="module")
def views_extended(views, temp_table, snowflake_version):
    ensure_snowflake_version(snowflake_version, "8.33.0")

    names_list = []
    for _ in range(5):
        names_list.append(random_string(10, "test_view_iter_a_"))
    for _ in range(7):
        names_list.append(random_string(10, "test_view_iter_b_"))
    for _ in range(3):
        names_list.append(random_string(10, "test_view_iter_c_"))

    try:
        for view_name in names_list:
            view_temp = copy.deepcopy(test_view_template)
            view_temp.name = view_name
            view_temp.query = f"SELECT * FROM {temp_table.name}"
            views.create(view_temp)

        yield views
    finally:
        for view_name in names_list:
            with suppress(NotFoundError):
                views[view_name].drop()


def test_iter_raw(views_extended):
    assert len(list(views_extended.iter())) >= 15


def test_iter_like(views_extended):
    assert len(list(views_extended.iter(like="test_view_iter_"))) == 0
    assert len(list(views_extended.iter(like="test_view_iter_a_%%"))) == 5
    assert len(list(views_extended.iter(like="test_view_iter_b_%%"))) == 7
    assert len(list(views_extended.iter(like="test_view_iter_c_%%"))) == 3


def test_iter_show_limit(views_extended):
    assert len(list(views_extended.iter(like="test_view_iter_a_%%"))) == 5
    assert len(list(views_extended.iter(like="test_view_iter_a_%%", show_limit=2))) == 2
    assert len(list(views_extended.iter(show_limit=2))) == 2


def test_iter_starts_with(views_extended):
    assert len(list(views_extended.iter(starts_with="test_view_iter_a_".upper()))) == 5


def test_iter_from_name(views_extended):
    assert len(list(views_extended.iter(from_name='test_view_iter_b_'))) >= 10


def test_iter_deep(views_extended):
    for v in views_extended.iter(show_limit=10):
        assert v.columns == []

    for v in views_extended.iter(show_limit=10, deep=True):
        assert len(v.columns) > 0

