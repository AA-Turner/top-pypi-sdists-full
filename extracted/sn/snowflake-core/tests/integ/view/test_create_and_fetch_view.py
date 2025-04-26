import copy

from contextlib import suppress

import pytest as pytest

from snowflake.core.exceptions import NotFoundError
from tests.integ.utils import random_string

from .conftest import test_view_template


@pytest.mark.min_sf_ver("8.33.0")
def test_create_and_fetch_view(views, temp_table):
    view_name = random_string(10, "test_view_")
    view_handle = views[view_name]
    try:
        test_view = copy.deepcopy(test_view_template)
        test_view.name = view_name
        test_view.query = f"SELECT * FROM {temp_table.name}"
        views.create(test_view)

        fetch_handle = view_handle.fetch()
        assert fetch_handle.name.upper() == view_name.upper()
        assert len(fetch_handle.columns) == 3
        assert fetch_handle.columns[0].name == "C1"
        assert fetch_handle.columns[0].datatype.upper() == "NUMBER(38,0)"
        assert fetch_handle.columns[1].name == "C2"
        assert fetch_handle.columns[1].datatype.upper() == "VARCHAR(16777216)"
        assert fetch_handle.columns[2].name == "C3"
        assert fetch_handle.columns[2].datatype.upper() == "VARCHAR(16777216)"

    finally:
        with suppress(NotFoundError):
            view_handle.drop()
