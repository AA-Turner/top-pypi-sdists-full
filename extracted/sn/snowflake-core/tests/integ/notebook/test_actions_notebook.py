from contextlib import suppress

import pytest as pytest

from snowflake.core.exceptions import NotFoundError
from snowflake.core.notebook import Notebook
from tests.utils import random_string


@pytest.mark.min_sf_ver("8.37.0")
def test_execute_notebook(cursor,
                          executable_notebook,
                          tables,
                          table_name_for_execute_notebook_test):
    test_table_handle = tables[table_name_for_execute_notebook_test]

    try:
        assert len(list(tables.iter(
            like=table_name_for_execute_notebook_test))) == 0

        # Now, execute the notebook; it should create the test table
        executable_notebook.execute()

        # Now, the table should be there
        assert len(list(tables.iter(
            like=table_name_for_execute_notebook_test))) == 1
    finally:
        with suppress(NotFoundError):
            test_table_handle.drop()


@pytest.mark.min_sf_ver("8.37.0")
def test_live_versions_and_commit_notebook(notebooks):
    notebook_name = random_string(5, "test_notebook_stage_")
    notebook = Notebook(name=notebook_name)
    notebook_handle = notebooks[notebook.name]

    notebooks.create(notebook)

    try:
        # Initially, there should be no live version
        assert notebook_handle.fetch().live_version_location_uri is None

        # This should add a LIVE version
        notebook_handle.add_live_version(from_last=True)
        assert notebook_handle.fetch().live_version_location_uri is not None

        # Committing sets the LIVE version to null
        notebook_handle.commit()
        assert notebook_handle.fetch().live_version_location_uri is None

    finally:
        with suppress(NotFoundError):
            notebook_handle.drop()
