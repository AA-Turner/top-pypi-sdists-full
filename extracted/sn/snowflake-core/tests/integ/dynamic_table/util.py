import datetime

from snowflake.core._internal.utils import normalize_and_unquote_name, normalize_datatype
from snowflake.core.database import DatabaseResource
from snowflake.core.dynamic_table import DownstreamLag, DynamicTable
from snowflake.core.schema import SchemaResource
from snowflake.core.table import TableResource


def assert_dynamic_table(
    dynamic_table: DynamicTable,
    name: str,
    table: TableResource,
    database: DatabaseResource,
    schema: SchemaResource,
    db_parameters: dict[str, str],
    deep: bool = False,
) -> None:
    assert dynamic_table.name == normalize_and_unquote_name(name)
    assert dynamic_table.target_lag == DownstreamLag()
    assert dynamic_table.warehouse == normalize_and_unquote_name(db_parameters["warehouse"])

    if deep:
        assert len(dynamic_table.columns) == 2
        assert dynamic_table.columns[0].name == 'A'
        assert dynamic_table.columns[0].datatype == normalize_datatype('int')
        assert dynamic_table.columns[0].comment is None
        assert dynamic_table.columns[1].name == 'B'
        assert dynamic_table.columns[1].datatype == normalize_datatype('varchar')
        assert dynamic_table.columns[1].comment == 'comment'
    else:
        assert dynamic_table.columns is None

    assert dynamic_table.query == f"SELECT * FROM {table.name}"
    assert dynamic_table.initialize == 'ON_SCHEDULE'
    assert dynamic_table.scheduling_state == 'RUNNING'
    assert dynamic_table.data_retention_time_in_days == 1
    assert dynamic_table.max_data_extension_time_in_days == 2
    assert dynamic_table.automatic_clustering is True
    assert dynamic_table.cluster_by == ['B']
    assert dynamic_table.comment == "test table", dynamic_table.comment

    assert dynamic_table.owner_role_type is not None
    assert isinstance(dynamic_table.created_on, datetime.datetime)
    assert dynamic_table.database_name == normalize_and_unquote_name(database.name)
    assert dynamic_table.schema_name == normalize_and_unquote_name(schema.name)
