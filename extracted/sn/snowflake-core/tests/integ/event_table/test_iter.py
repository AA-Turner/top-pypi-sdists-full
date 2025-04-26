from contextlib import suppress

import pytest

from snowflake.core.event_table import EventTable
from snowflake.core.exceptions import NotFoundError
from tests.utils import random_string

from ...utils import ensure_snowflake_version


@pytest.fixture(scope="session")
def event_tables_extended(event_tables, snowflake_version):
    ensure_snowflake_version(snowflake_version, "8.35.0")

    name_list = []
    for _ in range(5):
        name_list.append(random_string(10, "test_event_table_iter_a_"))
    for _ in range(7):
        name_list.append(random_string(10, "test_event_table_iter_b_"))
    for _ in range(3):
        name_list.append(random_string(10, "test_event_table_iter_c_"))

    try:
        for event_table_name in name_list:
            event_tables.create(
                EventTable(
                    name=event_table_name,
                )
            )

        yield event_tables
    finally:
        for event_table_name in name_list:
            with suppress(NotFoundError):
                event_tables[event_table_name].drop(if_exists=True)


def test_iter_raw(event_tables_extended):
    assert len(list(event_tables_extended.iter())) >= 15


def test_iter_like(event_tables_extended):
    assert len(list(event_tables_extended.iter(like="test_event_table_iter_"))) == 0
    assert len(list(event_tables_extended.iter(like="test_event_table_iter_a_%%"))) == 5
    assert len(list(event_tables_extended.iter(like="test_event_table_iter_b_%%"))) == 7
    assert len(list(event_tables_extended.iter(like="test_event_table_iter_c_%%"))) == 3


def test_iter_show_limit(event_tables_extended):
    assert len(list(event_tables_extended.iter(like="test_event_table_iter_a_%%"))) == 5

    for event_table in event_tables_extended.iter(like="test_event_table_iter_a_%%", show_limit=10):
        assert event_table.name.lower().startswith("test_event_table")
    assert len(list(event_tables_extended.iter(like="test_event_table_iter_a_%%", show_limit=2))) == 2
    assert len(list(event_tables_extended.iter(show_limit=2))) == 2


def test_iter_starts_with(event_tables_extended):
    assert len(list(event_tables_extended.iter(starts_with="test_event_table_iter_a_".upper()))) == 5


def test_iter_from_name(event_tables_extended):
    assert len(list(event_tables_extended.iter(from_name="test_event_table_iter_b_"))) >= 10
