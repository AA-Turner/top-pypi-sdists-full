from collections.abc import Iterator

import pytest

from snowflake.core.dynamic_table import (
    DownstreamLag,
    DynamicTable,
    DynamicTableCollection,
    DynamicTableColumn,
    DynamicTableResource,
)
from snowflake.core.table import Table, TableColumn, TableResource
from tests.utils import random_string


pytestmark = pytest.mark.usefixtures("setup_rest_api_parameters_for_dynamic_table")


@pytest.fixture(scope="module")
def dynamic_tables(schema) -> DynamicTableCollection:
    return schema.dynamic_tables


@pytest.fixture
def table_handle(schema) -> Iterator[TableResource]:
    table_name = '"' + random_string(5, "test_table_") + '"'
    test_table = schema.tables.create(
        Table(
            name=table_name,
            columns=[
                TableColumn(name="c1", datatype="int"),
                TableColumn(name="c2", datatype="varchar"),
            ],
        )
    )
    try:
        yield test_table
    finally:
        test_table.drop()


@pytest.fixture
def dynamic_table_handle(dynamic_tables, db_parameters, table_handle) -> Iterator[DynamicTableResource]:
    table_name = random_string(10, "test_dynamic_table_")
    test_table = dynamic_tables.create(
        DynamicTable(
            name=table_name,
            warehouse=db_parameters["warehouse"],
            target_lag=DownstreamLag(),
            columns=[
                DynamicTableColumn(name="a"),
                DynamicTableColumn(name="b", datatype="varchar", comment="comment"),
            ],
            query=f"SELECT * FROM {table_handle.name}",
            initialize="ON_SCHEDULE",
            cluster_by=["b"],
            data_retention_time_in_days=1,
            max_data_extension_time_in_days=2,
            comment="test table",
        ),
        mode="errorifexists",
    )
    try:
        yield test_table
    finally:
        test_table.drop()
