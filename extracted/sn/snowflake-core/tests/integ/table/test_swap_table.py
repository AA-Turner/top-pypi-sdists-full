from contextlib import suppress

import pytest

from snowflake.core.exceptions import NotFoundError
from snowflake.core.schema import Schema
from snowflake.core.table import Table, TableColumn
from tests.utils import random_string


def test_swap(tables, temp_db):
    table1_name = random_string(10, "test_table_")
    table2_name = random_string(10, "test_table_")
    test_table1_handle = tables[table1_name]
    test_table2_handle = tables[table2_name]

    test_table1 = Table(
        name=table1_name,
        columns=[
            TableColumn(name="c1", datatype="int"),
        ],
    )
    try:
        _ = tables.create(test_table1)
        test_table2 = Table(
            name=table2_name,
            columns=[
                TableColumn(name="c2", datatype="int"),
            ],
        )
        _ = tables.create(test_table2)
        test_table1_handle.swap_with(table2_name)
        fetched_table1 = test_table1_handle.fetch()
        fetched_table2 = test_table2_handle.fetch()
        assert fetched_table1.columns[0].name == "C2"
        assert fetched_table2.columns[0].name == "C1"

        # swap with random name
        with pytest.raises(
            NotFoundError,
        ):
            test_table1_handle.swap_with("RANDOM")

        # swap with non-existent table but with if_exists=True
        tables["RANDOM"].swap_with(table2_name, if_exists=True)
    finally:
        with suppress(NotFoundError):
            test_table1_handle.drop()
        with suppress(NotFoundError):
            test_table2_handle.drop()


def test_swap_across_database(tables, temp_db):
    table1_name = random_string(10, "test_table_")
    table2_name = random_string(10, "test_table_")
    test_table1_handle = tables[table1_name]

    test_table1 = Table(
        name=table1_name,
        columns=[
            TableColumn(name="c1", datatype="int"),
        ],
    )
    try:
        _ = tables.create(test_table1)

        schema_name = random_string(10, "test_create_clone_across_schema_")
        temp_db.schemas.create(Schema(name=schema_name))

        test_table2 = Table(
            name=table2_name,
            columns=[
                TableColumn(name="c2", datatype="int"),
            ],
        )
        _ = temp_db.schemas[schema_name].tables.create(test_table2)
        test_table1_handle.swap_with(table2_name, target_database=temp_db.name, target_schema=schema_name)
        fetched_table1 = test_table1_handle.fetch()
        test_table2_handle = temp_db.schemas[schema_name].tables[table2_name]
        fetched_table2 = test_table2_handle.fetch()
        assert fetched_table1.columns[0].name == "C2"
        assert fetched_table2.columns[0].name == "C1"
    finally:
        with suppress(NotFoundError):
            test_table1_handle.drop()
        with suppress(NotFoundError):
            test_table2_handle.drop()
