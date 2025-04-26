import pytest

from snowflake.core.event_table import EventTable
from snowflake.core.exceptions import NotFoundError
from tests.utils import random_string


@pytest.mark.min_sf_ver("8.35.0")
def test_rename(event_tables):
    event_table_name = random_string(10, 'test_original_event_table_')
    event_table_other_name = random_string(10, 'test_other_event_table_')

    event_table_handle = event_tables.create(EventTable(
        name=event_table_name
    ))

    event_table_handle.fetch()

    event_table_handle.rename(event_table_other_name)

    assert event_table_handle.fetch().name.upper() == event_table_other_name.upper()

    with pytest.raises(
        NotFoundError
    ):
        event_tables[event_table_name].fetch()

    with pytest.raises(
        NotFoundError
    ):
        event_tables[event_table_name].rename(event_table_other_name)

    event_tables[event_table_name].rename(event_table_other_name, if_exists=True)
    event_table_handle.drop(if_exists=True)
