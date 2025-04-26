import pytest

from snowflake.core.event_table import EventTable
from snowflake.core.exceptions import NotFoundError
from tests.utils import random_string


@pytest.mark.min_sf_ver("8.35.0")
def test_drop(event_tables):
    event_table_name = random_string(10, 'test_drop_event_table_')

    event_table_handle = event_tables.create(EventTable(
        name=event_table_name
    ))

    event_table_handle.fetch()

    event_table_handle.drop()

    with pytest.raises(
        NotFoundError
    ):
        event_table_handle.fetch()

    with pytest.raises(
        NotFoundError
    ):
        event_table_handle.drop()

    event_table_handle.drop(if_exists=True)
