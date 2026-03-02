import dlt
from dlt.common.libs.sqlglot import normalize_query_identifiers
from dlt.common.schema.typing import C_DLT_LOAD_ID, C_DLT_LOADS_TABLE_LOAD_ID
from sqlglot import expressions as sge

from dlthub.data_quality.storage import (
    DLT_CHECKS_TABLE_NAME,
    TABLE_NAME_COL,
    QUALIFIED_CHECK_NAME_COL,
    ROW_COUNT_COL,
    CHECK_SUCCESS_COUNT_COL,
    CHECK_SUCCESS_RATE_COL,
)


# TODO implement filtering and selection options;
# should be simpler once we can execute query via `dataset.table(...)`
def read_check(
    dataset: dlt.Dataset,
    *,
    table: str | None = None,
) -> dlt.Relation:
    """Read check results from the _dlt_checks table.

    Args:
        dataset: The dlt.Dataset to query
        table: Table name for table-level checks, None for all checks
    """
    naming = dataset.schema.naming
    where_condition = None
    if table:
        where_condition = sge.Column(this=TABLE_NAME_COL).eq(sge.Literal.string(table))

    loads_table = dataset.schema.loads_table_name
    query = sge.select(
        C_DLT_LOAD_ID,
        sge.Column(this="inserted_at").as_("loaded_at"),
        TABLE_NAME_COL,
        QUALIFIED_CHECK_NAME_COL,
        ROW_COUNT_COL,
        CHECK_SUCCESS_COUNT_COL,
        CHECK_SUCCESS_RATE_COL,
    ).from_(DLT_CHECKS_TABLE_NAME)

    if where_condition:
        query = query.where(where_condition)

    query = query.join(
        loads_table,
        on=sge.Column(this=C_DLT_LOADS_TABLE_LOAD_ID, table=loads_table).eq(
            sge.Column(this=C_DLT_LOAD_ID, table=DLT_CHECKS_TABLE_NAME)
        ),
        join_type="left",
    ).order_by(sge.Column(this=C_DLT_LOAD_ID, table=DLT_CHECKS_TABLE_NAME).desc())

    # normalize identifiers for the destination's naming convention
    normalized_query = normalize_query_identifiers(query, naming)
    # bypass schema binding since data quality tables are not in the dataset schema
    return dataset.query(normalized_query, _execute_raw_query=True)
