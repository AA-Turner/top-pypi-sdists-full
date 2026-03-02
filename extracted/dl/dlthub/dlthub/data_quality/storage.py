from __future__ import annotations

from typing import TYPE_CHECKING

from dlt.common.schema.utils import dlt_id_column, dlt_load_id_column, new_table
from dlt.common.schema.typing import (
    TTableSchema,
    TTableReferenceInline,
    C_DLT_LOAD_ID,
    LOADS_TABLE_NAME,
    C_DLT_LOADS_TABLE_LOAD_ID,
)

if TYPE_CHECKING:
    from dlt.common.data_types import TDataType


DLT_DATA_QUALITY_PIPELINE_NAME_TEMPLATE = "_dlt_dq_{dataset_name}"
TABLE_CHECKS_RESOURCE_NAME_TEMPLATE = "_dlt_checks_{table_name}"
DLT_CHECKS_TABLE_NAME = "_dlt_checks"
DLT_DATA_QUALITY_SCHEMA_NAME = "_dlt_data_quality"
QUALIFIED_CHECK_NAME_COL = "check_qualified_name"

TABLE_NAME_COL = "table_name"
COLUMN_NAME_COL = "column_name"
ROW_COUNT_COL = "row_count"
CHECK_COUNT_COL = "check_count"
CHECK_SUCCESS_COUNT_COL = "success_count"
CHECK_SUCCESS_RATE_COL = "success_rate"

DLT_METRICS_TABLE_NAME = "_dlt_dq_metrics"
DLT_COLUMN_METRICS_RESOURCE_NAME = "_dlt_column_metrics"
DLT_TABLE_METRICS_RESOURCE_NAME = "_dlt_table_metrics"
DLT_DATASET_METRICS_RESOURCE_NAME = "_dlt_dataset_metrics"
METRIC_LEVEL_COL = "level"
METRIC_NAME_COL = "metric_name"
METRIC_VALUE_COL = "metric_value"
METRIC_VALUE_COL_BASE_DATA_TYPE: TDataType = "bigint"


def checks_results_table() -> TTableSchema:
    table = new_table(
        table_name=DLT_CHECKS_TABLE_NAME,
        columns=[
            dlt_load_id_column(),
            {
                "name": QUALIFIED_CHECK_NAME_COL,
                "data_type": "text",
                "description": (
                    "Unique identifier for the check. It is typically composed of a table"
                    " name, a column name, a check name, and check argument identifier."
                ),
            },
            {
                "name": TABLE_NAME_COL,
                "data_type": "text",
                "description": ("Table for which results apply. Is null for dataset-level checks"),
                "nullable": True,
            },
            {
                "name": ROW_COUNT_COL,
                "data_type": "bigint",
                "description": (
                    "Number of rows involved in this check. Is null for dataset-level checks."
                ),
                "nullable": True,
            },
            {
                "name": CHECK_SUCCESS_COUNT_COL,
                "data_type": "bigint",
                "description": (
                    "Number of rows succeeding the check."
                    " Is null for table and dataset-level checks."
                ),
                "nullable": True,
            },
            {
                "name": CHECK_SUCCESS_RATE_COL,
                "data_type": "double",
                "description": (
                    "Number of rows succeeding the check."
                    " Is null for table and dataset-level checks."
                ),
                "nullable": False,
            },
            # {
            #     "name": LOAD_IDS_CHECKED_COL,
            #     "data_type": "json",
            #     "description": (
            #         "List of `_dlt_load_id` values that were included when running checks."
            #     ),
            #     "nullable": False,
            # },
        ],
        write_disposition="append",
    )

    return table


def metrics_results_table() -> TTableSchema:
    """Return a basic schema for metrics tables

    NOTE the `metric_value` column has base type `double`. Other metric types
    will produce variants like `metric_value__v_text`, `metric_value__v_bool`
    """
    table_name = DLT_METRICS_TABLE_NAME
    table = new_table(
        table_name=table_name,
        columns=[
            dlt_load_id_column(),
            dlt_id_column(),
            {
                "name": METRIC_LEVEL_COL,
                "data_type": "text",
                "description": "Level of the metric (column, table, dataset)",
                "nullable": False,
            },
            {
                "name": TABLE_NAME_COL,
                "data_type": "text",
                "description": "Name of the table associated with the metric",
                "nullable": True,
            },
            {
                "name": COLUMN_NAME_COL,
                "data_type": "text",
                "description": "Name of the entity associated with the metric",
                "nullable": True,
            },
            {
                "name": METRIC_NAME_COL,
                "data_type": "text",
                "description": "Name of the metric",
                "nullable": False,
            },
            {
                "name": METRIC_VALUE_COL,
                "data_type": METRIC_VALUE_COL_BASE_DATA_TYPE,
                "description": "Value of the metric",
                "nullable": True,
                "variant": True,
            },
        ],
        write_disposition="append",
        schema_contract="freeze",
        references=[
            TTableReferenceInline(
                label="_dlt_dq_metrics",
                cardinality="one_to_many",
                table=table_name,
                columns=[C_DLT_LOAD_ID],
                referenced_table=LOADS_TABLE_NAME,
                referenced_columns=[C_DLT_LOADS_TABLE_LOAD_ID],
            )
        ],
    )

    return table
