from __future__ import annotations

import dlt
from dlt.common.libs.ibis import ibis, ir

from dlthub.data_quality.metrics import _base


class total_row_count(_base.DatasetMetricDefinition):
    """Total row count in dataset"""

    def expr(self, dataset: dlt.Dataset) -> int:
        count = 0
        for table_name in dataset.schema.data_table_names():
            table = dataset.table(table_name).to_ibis()
            count += table.count().to_pyarrow().as_py()

        return count


class load_row_count(_base.DatasetMetricDefinition):
    """Load row count across all tables in dataset.

    NOTE this is computed after the load phase. The meaning
    of this value depends on the `write_disposition` used.
    """

    def expr(self, dataset: dlt.Dataset) -> int:
        count = 0
        latest_load_id = dataset.latest_load_id()
        for table_name in dataset.schema.data_table_names():
            table = dataset.table(table_name, load_ids=[latest_load_id]).to_ibis()
            count += table.count().to_pyarrow().as_py()

        return count


class latest_loaded_at(_base.DatasetMetricDefinition):
    """Latest loaded at timestamp"""

    def expr(self, dataset: dlt.Dataset) -> ir.TimestampScalar:
        query = (
            dataset.loads_table()
            .to_ibis()
            .filter(ibis._.schema_name == dataset.schema.name)
            .inserted_at.max()
        )
        return query
