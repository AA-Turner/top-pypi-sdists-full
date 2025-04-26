from contextlib import suppress

import pytest

from pydantic import ValidationError

from tests.integ.table.conftest import (
    assert_table,
)
from tests.utils import random_string


def test_iter_like(tables, table_postfix, table_handle, table_handle_case_senstitive, database, schema):
    listed_tables_deep = list(tables.iter(like=table_handle.name, deep=True))
    assert_table(listed_tables_deep[0], table_handle.name, database, schema, True)

    listed_tables_not_deep = list(tables.iter(like=table_handle.name, deep=False))
    assert_table(listed_tables_not_deep[0], table_handle.name, database, schema, False)

    listed_tables_deep = list(tables.iter(like=f"test_table_{table_postfix}_case_sens%e", deep=True))
    assert_table(
        listed_tables_deep[0], table_handle_case_senstitive.name, database, schema, True
    )

    listed_tables_deep = list(tables.iter(like=f"test_table_{table_postfix}%", deep=True))
    assert len(listed_tables_deep) == 2


def test_iter_starts_with(tables, table_postfix, table_handle, table_handle_case_senstitive, database, schema):
    listed_tables_deep = list(tables.iter(starts_with=f"test_table_{table_postfix}_case_s", deep=True))
    assert len(listed_tables_deep) == 1
    assert_table(listed_tables_deep[0], table_handle_case_senstitive.name, database, schema, True)

    listed_tables_deep = list(tables.iter(starts_with=f"test_table_{table_postfix}_case_i".upper(), deep=True))
    assert len(listed_tables_deep) == 1
    assert_table(listed_tables_deep[0], table_handle.name, database, schema, True)


# The LIMIT keyword is required for the FROM keyword to function, limit=10 was chosen arbitrarily
# as it does not affect the test
def test_iter_from_name(tables, table_postfix, table_handle, table_handle_case_senstitive, database, schema):
    listed_tables_deep = list(tables.iter(limit=10, from_name="test_table", deep=True))
    assert len(listed_tables_deep) == 1
    assert_table(
        listed_tables_deep[0], table_handle_case_senstitive.name, database, schema, True
    )

    listed_tables_deep = list(tables.iter(limit=10, from_name=f"test_table_{table_postfix}_case_i".upper(), deep=True))
    assert 10 >= len(listed_tables_deep) >= 2
    assert_table(listed_tables_deep[0], table_handle.name, database, schema, True)


def test_iter_limit(tables):
    data = list(tables.iter(limit=10))
    assert len(data) <= 10

    with pytest.raises(
        ValidationError,
    ):
        data = list(tables.iter(limit=10001))


def test_iter_history(tables, table_handle):
    table_name = random_string(10, "test_table_")
    created_handle = tables.create(
        table_name, like_table=f"{table_handle.name}", copy_grants=True, mode="errorifexists"
    )
    try:
        assert created_handle.name == table_name
    finally:
        with suppress(Exception):
            created_handle.drop()

    data = list(tables.iter(history=True))
    assert len(data) >= 3
