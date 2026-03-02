import dlt
from dlt.common.libs.sqlglot import normalize_query_identifiers
from dlt.common.schema.typing import C_DLT_LOAD_ID, C_DLT_LOADS_TABLE_LOAD_ID
from sqlglot import expressions as sge

from dlthub.data_quality.storage import (
    DLT_METRICS_TABLE_NAME,
    METRIC_LEVEL_COL,
    METRIC_NAME_COL,
    METRIC_VALUE_COL,
    METRIC_VALUE_COL_BASE_DATA_TYPE,
    TABLE_NAME_COL,
    COLUMN_NAME_COL,
)
from dlthub.data_quality.metrics._definitions import get_schema_metric_hints


# TODO add an interface to read multiple metrics at once; they must share the same data type

# TODO add kwarg to select specific load_ids; need to add a `main_pipeline_load_id` column
# to the storage


def read_metric(
    dataset: dlt.Dataset,
    *,
    table: str | None = None,
    column: str | None = None,
    metric: str,
) -> dlt.Relation:
    all_metrics_hints = get_schema_metric_hints(dataset.schema)
    naming = dataset.schema.naming

    # TODO handle IterationError if `next()` has no match
    _col = sge.Column
    _lit = sge.Literal.string
    if table is None and column is None:
        metric_hints = next(m for m in all_metrics_hints["dataset"] if m["name"] == metric)
        where_condition = (
            _col(this=METRIC_LEVEL_COL)
            .eq(_lit("dataset"))
            .and_(_col(this=METRIC_NAME_COL).eq(_lit(metric)))
        )
    elif table is not None and column is None:
        metric_hints = next(m for m in all_metrics_hints["tables"][table] if m["name"] == metric)
        where_condition = (
            _col(this=METRIC_LEVEL_COL)
            .eq(_lit("table"))
            .and_(_col(this=TABLE_NAME_COL).eq(_lit(table)))
            .and_(_col(this=METRIC_NAME_COL).eq(_lit(metric)))
        )
    elif table is not None and column is not None:
        metric_hints = next(
            m for m in all_metrics_hints["columns"][table][column] if m["name"] == metric
        )
        where_condition = (
            _col(this=METRIC_LEVEL_COL)
            .eq(_lit("column"))
            .and_(_col(this=TABLE_NAME_COL).eq(_lit(table)))
            .and_(_col(this=COLUMN_NAME_COL).eq(_lit(column)))
            .and_(_col(this=METRIC_NAME_COL).eq(_lit(metric)))
        )
    else:
        raise ValueError("Invalid combination of `table` and `column`")

    if metric_hints["is_variant"]:
        # if variant, return type == input data type
        # notable exception `median()` can convert int to float
        return_type = dataset.schema.tables[table]["columns"][column]["data_type"]
    else:
        return_type = metric_hints["return_type"]

    # TODO implement proper normalization using `dlt.Schema`
    # the variant column name normalization doesn't seem to be publicly exposed
    if return_type == METRIC_VALUE_COL_BASE_DATA_TYPE:
        metric_value_col_name = METRIC_VALUE_COL
    else:
        metric_value_col_name = f"{METRIC_VALUE_COL}__v_{return_type}"

    loads_table = dataset.schema.loads_table_name
    query = (
        sge.select(
            C_DLT_LOAD_ID,
            sge.Column(this="inserted_at").as_("loaded_at"),
            TABLE_NAME_COL,
            COLUMN_NAME_COL,
            METRIC_NAME_COL,
            sge.Column(this=metric_value_col_name).as_(METRIC_VALUE_COL),
        )
        .from_(DLT_METRICS_TABLE_NAME)
        .where(where_condition)
        .join(
            loads_table,
            on=sge.Column(this=C_DLT_LOADS_TABLE_LOAD_ID, table=loads_table).eq(
                sge.Column(this=C_DLT_LOAD_ID, table=DLT_METRICS_TABLE_NAME)
            ),
            join_type="left",
        )
        .order_by(sge.Column(this=C_DLT_LOAD_ID, table=DLT_METRICS_TABLE_NAME).desc())
    )
    # normalize identifiers for the destination's naming convention
    normalized_query = normalize_query_identifiers(query, naming)
    # bypass schema binding since data quality tables are not in the dataset schema
    return dataset.query(normalized_query, _execute_raw_query=True)
