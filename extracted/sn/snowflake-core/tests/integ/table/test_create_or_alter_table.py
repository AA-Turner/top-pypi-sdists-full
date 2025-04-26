import copy

from contextlib import suppress

import pytest as pytest

from snowflake.core.exceptions import APIError, NotFoundError
from snowflake.core.table import TableColumn, UniqueKey
from tests.utils import random_string

from .conftest import assert_table, test_table_template


def test_create_or_alter(tables, database, schema, root):
    table_name = random_string(10, "test_table_")
    table_handle = tables[table_name]
    try:
        test_table = copy.deepcopy(test_table_template)
        test_table.name = table_name
        table_handle.create_or_alter(test_table)  # new table is created for the first time.
        fetched = table_handle.fetch()
        assert_table(fetched, table_name, database, schema, True, rows=0)
        assert fetched.comment == "test table"

        test_table_v2 = copy.deepcopy(test_table_template)
        test_table_v2.name = table_name
        test_table_v2.enable_schema_evolution = False
        test_table_v2.change_tracking = False
        test_table_v2.data_retention_time_in_days = None
        test_table_v2.max_data_extension_time_in_days = None
        test_table_v2.default_ddl_collation = "en"
        test_table_v2.columns[1].nullable = False
        test_table_v2.columns.append(TableColumn(name="c4", datatype="text"))
        test_table_v2.constraints[0].name = "pk2"
        test_table_v2.constraints[1].name = "uk2"
        test_table_v2.comment = "test table 2"
        table_handle.create_or_alter(test_table_v2)
        fetched2 = table_handle.fetch()
        assert fetched2.enable_schema_evolution is False
        assert fetched2.change_tracking is False
        assert len(fetched2.columns) == 4
        assert fetched2.columns[3].name == "C4"
        assert fetched2.columns[3].datatype.upper() in ["TEXT", 'VARCHAR(16777216)']
        assert fetched2.columns[3].nullable is True
        assert fetched2.columns[3].autoincrement_start is None
        assert fetched2.columns[3].autoincrement_increment is None
        if isinstance(fetched2.constraints[0], UniqueKey):
            # Order might swaped
            fetched2.constraints[0], fetched2.constraints[1] = fetched2.constraints[1], fetched2.constraints[0]
        assert fetched2.constraints[0].name == "PK2"
        assert fetched2.constraints[1].name == "UK2"
        assert fetched2.data_retention_time_in_days == 1
        assert fetched2.max_data_extension_time_in_days == 14
        assert fetched2.columns[3].autoincrement is None

        # Make sure that issuing an empty alter doesn't create a malformed SQL
        table_handle.create_or_alter(test_table_v2)
    finally:
        with suppress(NotFoundError):
            table_handle.drop()


def test_create_or_alter_table_negative_no_columns(table_handle):
    fetched_table = table_handle.fetch()
    fetched_table.columns = None
    with pytest.raises(APIError):
        table_handle.create_or_alter(fetched_table)
    # assert error.match("Columns must be provided for create_or_alter")


def test_create_or_alter_table_negative_remove_columns(table_handle):
    deep_fetched = table_handle.fetch()
    deep_fetched.columns.pop(-1)

    table_handle.create_or_alter(deep_fetched)
    deep_fetched = table_handle.fetch()
    assert len(deep_fetched.columns) == 2


def test_create_or_update_deprecated(tables, database, schema, root):
    with pytest.warns(DeprecationWarning, match="method is deprecated; use"):
        table_name = random_string(10, "test_table_")
        table_handle = tables[table_name]
        try:
            test_table = copy.deepcopy(test_table_template)
            test_table.name = table_name
            table_handle.create_or_alter(test_table)  # new table is created for the first time.
            fetched = table_handle.fetch()
            assert_table(fetched, table_name, database, schema, True, rows=0)
            assert fetched.comment == "test table"

            test_table_v2 = copy.deepcopy(test_table_template)
            test_table_v2.name = table_name
            test_table_v2.enable_schema_evolution = False
            test_table_v2.change_tracking = False
            test_table_v2.data_retention_time_in_days = None
            test_table_v2.max_data_extension_time_in_days = None
            test_table_v2.default_ddl_collation = "en"
            test_table_v2.columns[1].nullable = False
            test_table_v2.columns.append(TableColumn(name="c4", datatype="text"))
            test_table_v2.constraints[0].name = "pk2"
            test_table_v2.constraints[1].name = "uk2"
            test_table_v2.comment = "test table 2"
            table_handle.create_or_alter(test_table_v2)
            fetched2 = table_handle.fetch()
            assert fetched2.enable_schema_evolution is False
            assert fetched2.change_tracking is False
            assert len(fetched2.columns) == 4
            assert fetched2.columns[3].name == "C4"
            assert fetched2.columns[3].datatype.upper() in ["TEXT", 'VARCHAR(16777216)']
            assert fetched2.columns[3].nullable is True
            assert fetched2.columns[3].autoincrement_start is None
            assert fetched2.columns[3].autoincrement_increment is None
            if isinstance(fetched2.constraints[0], UniqueKey):
                # Order might swaped
                fetched2.constraints[0], fetched2.constraints[1] = fetched2.constraints[1], fetched2.constraints[0]
            assert fetched2.constraints[0].name == "PK2"
            assert fetched2.constraints[1].name == "UK2"
            assert fetched2.data_retention_time_in_days == 1
            assert fetched2.max_data_extension_time_in_days == 14
            assert fetched2.columns[3].autoincrement is None

            # Make sure that issuing an empty alter doesn't create a malformed SQL
            table_handle.create_or_update(test_table_v2)
        finally:
            with suppress(NotFoundError):
                table_handle.drop()
