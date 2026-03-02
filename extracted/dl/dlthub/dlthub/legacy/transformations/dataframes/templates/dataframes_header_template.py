# dataframe transformations for {{ project_name }}

from typing import Callable, Any, List, Generator

import duckdb

from dlthub.legacy.transformations.const import (
    ACTIVE_LOADS_ID_TABLE,
    PROCESSED_LOAD_IDS_TABLE,
    LOADS_TABLE,
)
from dlthub.legacy.transformations.dataframes.decorators import (
    TransformationUtils,
    transformation,
    transformation_group,
)

DEFAULT_CHUNKSIZE = 500


# table for keeping track of active load ids
@transformation(table_name=ACTIVE_LOADS_ID_TABLE, materialization="table")
def prepare_active_load_ids(
    connection: duckdb.DuckDBPyConnection, utils: TransformationUtils
) -> str:
    loads_table_name = utils.make_qualified_input_table_name(LOADS_TABLE)

    where_clause = "status = 0"
    if PROCESSED_LOAD_IDS_TABLE in utils.existing_output_tables():
        processed_load_ids_table = utils.make_qualified_output_table_name(PROCESSED_LOAD_IDS_TABLE)
        where_clause += f"""
            AND load_id NOT IN (
                SELECT load_id
                FROM {processed_load_ids_table}
            )
        """

    return f"""
        SELECT load_id
        FROM {loads_table_name}
        WHERE {where_clause}
        AND status = 0
    """


@transformation(
    table_name=PROCESSED_LOAD_IDS_TABLE, materialization="table", write_disposition="append"
)
def update_processed_load_ids(
    connection: duckdb.DuckDBPyConnection, utils: TransformationUtils
) -> str:
    active_load_ids_table = utils.make_qualified_output_table_name(ACTIVE_LOADS_ID_TABLE)

    return f"""
        SELECT load_id, NOW() as inserted_at
        FROM {active_load_ids_table}
    """
