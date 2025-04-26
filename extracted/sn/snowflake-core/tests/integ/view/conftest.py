import copy

from collections.abc import Generator

import pytest as pytest

from snowflake.core.table import Table, TableColumn, TableResource
from snowflake.core.view import View, ViewColumn
from tests.integ.utils import random_string


test_table_template = Table(
    name="<to be set>",
    columns=[
        TableColumn(
            name="c1",
            datatype="int",
            nullable=False,
            autoincrement=True,
            autoincrement_start=0,
            autoincrement_increment=1,
        ),
        TableColumn(name="c2", datatype="string"),
        TableColumn(name="c3", datatype="string", collate="FR"),
    ],
)

test_view_template = View(
    name="<to be set>",
    columns=[
        ViewColumn(name="c1"), ViewColumn(name="c2"), ViewColumn(name="c3"),
    ],
    query="<to be set>",
)

@pytest.fixture(scope="module")
def temp_table(tables) -> Generator[TableResource, None, None]:
    table_name = f"test_table_for_view_{random_string(10)}"
    test_table = copy.deepcopy(test_table_template)
    test_table.name = table_name
    test_table_handle = tables.create(test_table)
    try:
        yield test_table_handle
    finally:
        test_table_handle.drop()

