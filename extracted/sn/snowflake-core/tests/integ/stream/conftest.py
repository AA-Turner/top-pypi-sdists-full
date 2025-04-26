import copy

import pytest as pytest

from snowflake.core.table import Table, TableColumn
from snowflake.core.view import View, ViewColumn
from tests.integ.utils import random_string


temp_table_template = Table(
    name="ToBeSet",
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
    ]
)


@pytest.fixture(scope='module')
def src_temp_table(tables):
    table_name = random_string(10, 'stream_src_table_')
    table_template = copy.deepcopy(temp_table_template)
    table_template.name = table_name
    table_handle = tables.create(table_template)
    try:
        yield table_handle
    finally:
        tables[table_name].drop()


@pytest.fixture(scope='module')
def src_temp_view(views, src_temp_table):
    view_name = random_string(10, 'stream_src_view_')
    view_handle = views.create(View(
        name=view_name,
        columns=[
            ViewColumn(name="c1"), ViewColumn(name="c2"),
        ],
        query = f"SELECT * FROM {src_temp_table.name}"
    ))
    try:
        yield view_handle
    finally:
        views[view_name].drop()


@pytest.fixture(scope='module')
def src_temp_view_with_multiple_base_tables(views, tables, src_temp_table):
    view_name = random_string(10, 'stream_src_view_')
    other_table_name = random_string(10, 'stream_src_other_table_')

    table_template = copy.deepcopy(temp_table_template)
    table_template.name = other_table_name
    table_handle = tables.create(table_template)


    view_handle = views.create(View(
        name=view_name,
        columns=[
            ViewColumn(name="c1"), ViewColumn(name="c2"),
        ],
        query = f"""\
            SELECT
                {src_temp_table.name}.c1,
                {table_handle.name}.c2
            FROM {src_temp_table.name}
            JOIN {table_handle.name}
            ON {src_temp_table.name}.c2 = {table_handle.name}.c1
        """
    ))

    try:
        yield view_handle, src_temp_table.name, table_handle.name
    finally:
        views[view_name].drop()
        tables[other_table_name].drop()
