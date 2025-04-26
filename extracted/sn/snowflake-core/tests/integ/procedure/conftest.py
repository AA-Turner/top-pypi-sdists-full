from contextlib import suppress

import pytest

from snowflake.core.exceptions import NotFoundError
from snowflake.core.table import Table, TableColumn


@pytest.fixture()
def populate_tables_for_procedure_call(tables, cursor):
    sql_test_table = "invoices"
    test_table = Table(
        name=sql_test_table,
        columns=[
            TableColumn(name="id", datatype="int"),
            TableColumn(name="price", datatype="int"),
        ],
    )
    test_table_handle = tables.create(test_table)
    cursor.execute(f"insert into {sql_test_table} (id, price) values (1, 1), (1, 2), (2, 3), (3, 10)")
    try:
        yield test_table_handle
    finally:
        with suppress(NotFoundError):
            test_table_handle.drop()
