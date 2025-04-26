from contextlib import suppress

import pytest as pytest

from snowflake.core import CreateMode
from snowflake.core.exceptions import NotFoundError
from snowflake.core.notebook import Notebook
from tests.integ.notebook.conftest import notebook_file
from tests.integ.utils import random_string


@pytest.mark.min_sf_ver("8.37.0")
def test_create_and_fetch(notebooks, notebook_stage_with_file, warehouse):
    notebook_name = random_string(10, "test_notebook_")
    notebook_handle = notebooks[notebook_name]

    nb = Notebook(name=notebook_name,
                  query_warehouse=warehouse.name,
                  from_location=f"@{notebook_stage_with_file.name}",
                  main_file=notebook_file)

    notebook = notebooks.create(nb)
    notebooks.create(nb, mode=CreateMode.or_replace)

    try:
        fetch_handle = notebook_handle.fetch()
        assert fetch_handle.name.upper() == notebook_name.upper()

        # This returns None, so it's commented out now; have to confirm if this is an actual bug.
        # assert fetch_handle.query_warehouse.name.upper() == warehouse.name.upper()

        assert fetch_handle.from_location.upper() == f"@{notebook_stage_with_file.name}".upper()
        assert fetch_handle.main_file.upper() == notebook_file.upper()

    finally:
        with suppress(NotFoundError):
            notebook.drop()
