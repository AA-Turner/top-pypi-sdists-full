from contextlib import suppress

from snowflake.core.dynamic_table import DownstreamLag, DynamicTable
from snowflake.core.exceptions import NotFoundError
from tests.utils import random_string


def test_swap(dynamic_tables, table_handle, db_parameters):
    table1_name = random_string(10, "test_table_")
    table2_name = random_string(10, "test_table_")

    test_table1 = DynamicTable(
        name=table1_name,
        warehouse=db_parameters["warehouse"],
        target_lag=DownstreamLag(),
        query=f"SELECT c1 FROM {table_handle.name}",
    )
    test_table2 = DynamicTable(
        name=table2_name,
        warehouse=db_parameters["warehouse"],
        target_lag=DownstreamLag(),
        query=f"SELECT c2 FROM {table_handle.name}",
    )

    try:
        test_table1_handle = dynamic_tables.create(test_table1)
        test_table2_handle = dynamic_tables.create(test_table2)

        test_table1_handle.swap_with(table2_name)
        dynamic_tables["dummy___table"].swap_with(table2_name, if_exists=True)

        fetched_table1 = test_table1_handle.fetch()
        fetched_table2 = test_table2_handle.fetch()

        assert fetched_table1.query == f"SELECT c2 FROM {table_handle.name}"
        assert fetched_table2.query == f"SELECT c1 FROM {table_handle.name}"
    finally:
        with suppress(NotFoundError):
            test_table1_handle.drop()
        with suppress(NotFoundError):
            test_table2_handle.drop()
