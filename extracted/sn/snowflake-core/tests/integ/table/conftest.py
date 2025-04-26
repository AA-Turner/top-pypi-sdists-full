import copy
import datetime

from collections.abc import Generator
from contextlib import suppress

import pytest as pytest

from snowflake.core._internal.utils import normalize_and_unquote_name, normalize_datatype
from snowflake.core.database import DatabaseResource
from snowflake.core.exceptions import NotFoundError
from snowflake.core.schema import SchemaResource
from snowflake.core.table import PrimaryKey, Table, TableColumn, TableResource, UniqueKey
from tests.integ.utils import array_equal_comparison, random_string


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
    cluster_by=["c1>1", "c2"],
    enable_schema_evolution=True,
    change_tracking=True,
    data_retention_time_in_days=1,
    max_data_extension_time_in_days=1,
    default_ddl_collation="en",
    constraints=[PrimaryKey(name="pk1", column_names=["c1"]), UniqueKey(name="uk1", column_names=["c2"])],
    comment="test table",
)


@pytest.fixture
def table_postfix() -> str:
    return random_string(10)

@pytest.fixture
def table_handle(table_postfix, tables, session) -> Generator[TableResource, None, None]:
    # Use bridge to bring handles.
    table_name = f"test_table_{table_postfix}_case_insensitive"
    test_table = copy.deepcopy(test_table_template)
    test_table.name = table_name
    test_table_handle = tables.create(test_table)
    session.sql(f"use database {tables.database.name}").collect()
    session.sql(f"use schema {tables.schema.name}").collect()
    sql_string = "insert into " + table_name + " values (1, 'random_string_1', 'random_string_2')"
    session.sql(sql_string).collect()
    sql_string = "insert into " + table_name + " values (2, 'random_string_3', 'random_string_4')"
    session.sql(sql_string).collect()
    try:
        yield test_table_handle
    finally:
        with suppress(NotFoundError):
            test_table_handle.drop()


@pytest.fixture
def table_handle_case_senstitive(table_postfix, tables, session) -> Generator[TableResource, None, None]:
    # Use bridge to bring handles.
    table_name = f'"test_table_{table_postfix}_case_sensitive"'
    test_table = copy.deepcopy(test_table_template)
    test_table.name = table_name
    test_table_handle = tables.create(test_table)
    session.sql(f"use database {tables.database.name}").collect()
    session.sql(f"use schema {tables.schema.name}").collect()
    sql_string = "insert into " + table_name + " values (1, 'random_string_1', 'random_string_2')"
    session.sql(sql_string).collect()
    sql_string = "insert into " + table_name + " values (2, 'random_string_3', 'random_string_4')"
    session.sql(sql_string).collect()
    try:
        yield test_table_handle
    finally:
        with suppress(NotFoundError):
            test_table_handle.drop()


def assert_table(
    table: Table,
    name: str,
    database: DatabaseResource,
    schema: SchemaResource,
    deep: bool = False,
    rows: int = 2,
) -> None:
    # `Table` is fetched from the server and its attributes are checked.
    assert table.name == normalize_and_unquote_name(name)
    if deep:
        for i in range(len(table.columns)):
            assert table.columns[i].name == normalize_and_unquote_name(test_table_template.columns[i].name)
            assert normalize_datatype(table.columns[i].datatype) == normalize_datatype(
                test_table_template.columns[i].datatype
            )
            assert bool(table.columns[i].nullable) == bool(test_table_template.columns[i].nullable)
            assert table.columns[i].default == test_table_template.columns[i].default
            assert table.columns[i].autoincrement_start == test_table_template.columns[i].autoincrement_start
            assert table.columns[i].autoincrement_increment == test_table_template.columns[i].autoincrement_increment
            assert bool(table.columns[i].autoincrement) == bool(test_table_template.columns[i].autoincrement)
            assert table.columns[i].comment == test_table_template.columns[i].comment
        assert table.columns[2].collate.upper() == "FR"

        fetched_constraints = sorted(table.constraints, key=lambda x: x.name)
        original_constraints = sorted(test_table_template.constraints, key=lambda x: x.name)
        for i in range(len(fetched_constraints)):
            assert fetched_constraints[i].__class__ == original_constraints[i].__class__
            assert normalize_and_unquote_name(fetched_constraints[i].name) == normalize_and_unquote_name(
                original_constraints[i].name
            )
            assert [normalize_and_unquote_name(x) for x in fetched_constraints[i].column_names] == [
                normalize_and_unquote_name(x) for x in original_constraints[i].column_names
            ]
    else:
        assert table.columns is None
        assert table.constraints is None

    """Test behavior change between Client Bridge Vs Rest
    REST would always return these basic information
    """
    assert array_equal_comparison(table.cluster_by, test_table_template.cluster_by)
    assert table.comment == test_table_template.comment
    assert table.enable_schema_evolution is test_table_template.enable_schema_evolution
    assert table.change_tracking is test_table_template.change_tracking
    assert table.data_retention_time_in_days == test_table_template.data_retention_time_in_days
    assert table.max_data_extension_time_in_days == test_table_template.max_data_extension_time_in_days
    assert table.default_ddl_collation.upper() == test_table_template.default_ddl_collation.upper()
    assert table.automatic_clustering is True
    assert table.owner_role_type is not None
    assert table.rows == rows

    assert isinstance(table.created_on, datetime.datetime)
    assert table.dropped_on is None
    assert table.database_name == normalize_and_unquote_name(database.name)
    assert table.schema_name == normalize_and_unquote_name(schema.name)
    assert table.search_optimization is False
    assert table.search_optimization_bytes is None
    assert table.search_optimization_progress is None
