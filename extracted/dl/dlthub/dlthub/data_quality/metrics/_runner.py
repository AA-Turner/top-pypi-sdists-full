from __future__ import annotations

import functools
import tempfile
from collections.abc import Sequence
from typing import Any, TYPE_CHECKING, Mapping, Iterator

import dlt
from dlt.common.libs.ibis import ibis, ir
from dlt.common.destination.reference import TDestinationReferenceArg
from dlt.common.pipeline import LoadInfo

import dlthub
from dlthub.data_quality.storage import (
    DLT_COLUMN_METRICS_RESOURCE_NAME,
    DLT_DATA_QUALITY_PIPELINE_NAME_TEMPLATE,
    DLT_DATA_QUALITY_SCHEMA_NAME,
    DLT_DATASET_METRICS_RESOURCE_NAME,
    DLT_TABLE_METRICS_RESOURCE_NAME,
    metrics_results_table,
)
from dlthub.data_quality.metrics._definitions import get_metric_definitions_from_schema
from dlthub.data_quality.typing import TSourceMetricsDefinitions, TMetricsResult
from dlthub.data_quality.metrics._base import (
    ColumnMetricDefinition,
    TableMetricDefinition,
    DatasetMetricDefinition,
)

if TYPE_CHECKING:
    import dlthub.transformations


# TODO add a function to include "table-level" metrics that aren't tied to a specific column
# they could included in the same `aggregate` call
def _collect_column_metrics_as_table(
    table: ir.Table,
    *,
    metrics_per_column: Mapping[str, Sequence[ColumnMetricDefinition]],
) -> ir.Table:
    """This collects the metrics for all columns of the table.

    Outputs a table with a single row where each column containts a dictionary of metric values.
    The column names matches the column names of the input table from which metrics were computed.

    `metrics_per_column` expects an exhaustive list of metrics per column. It allows
    to include/exclude metrics and columns with high granularity.
    """
    columns_metrics_exprs = {}
    for column_name, metric_defs in metrics_per_column.items():
        column_metrics_exprs = {}
        for metric_def in metric_defs:
            column_metrics_exprs[metric_def.name] = metric_def.expr(table[column_name])

        columns_metrics_exprs[column_name] = ibis.struct(column_metrics_exprs)

    # NOTE doing all metrics in one `.aggregate()` pass is key to apply them
    # in a single table scan
    return table.aggregate(**columns_metrics_exprs)


def _collect_table_metrics_as_table(
    table: ir.Table,
    *,
    table_metrics: Sequence[TableMetricDefinition],
) -> ir.Table:
    table_metrics_exprs = {metric_def.name: metric_def.expr(table) for metric_def in table_metrics}
    return table.aggregate(**table_metrics_exprs)


@dlthub.transformation(
    name=DLT_COLUMN_METRICS_RESOURCE_NAME,
    table_name=metrics_results_table()["name"],
    columns=metrics_results_table()["columns"],
    write_disposition=metrics_results_table()["write_disposition"],
    schema_contract=metrics_results_table()["schema_contract"],
    references=metrics_results_table()["references"],
)
def column_metrics_resource(
    dataset: dlt.Dataset,
    *,
    metrics: dict[str, dict[str, list[ColumnMetricDefinition]]] | None = None,
) -> Iterator[TMetricsResult]:
    if metrics is None:
        metrics = get_metric_definitions_from_schema(dataset.schema)["columns"]

    for table_name, column_metrics in metrics.items():
        column_metrics_for_table_query = _collect_column_metrics_as_table(
            table=dataset.table(table_name).to_ibis(),
            metrics_per_column=column_metrics,
        )
        column_metrics_for_table: list[dict[str, dict[str, Any]]] = (
            column_metrics_for_table_query.to_pyarrow().to_pylist()
        )

        for column_name, column_metrics in column_metrics_for_table[0].items():
            for metric_name, metric_value in column_metrics.items():
                yield {
                    "level": "column",
                    "table_name": table_name,
                    "column_name": column_name,
                    "metric_name": metric_name,
                    "metric_value": metric_value,
                }


@dlthub.transformation(
    name=DLT_TABLE_METRICS_RESOURCE_NAME,
    table_name=metrics_results_table()["name"],
    columns=metrics_results_table()["columns"],
    write_disposition=metrics_results_table()["write_disposition"],
    schema_contract=metrics_results_table()["schema_contract"],
    references=metrics_results_table()["references"],
)
def table_metrics_resource(
    dataset: dlt.Dataset,
    *,
    metrics: dict[str, list[TableMetricDefinition]] | None = None,
) -> Iterator[TMetricsResult]:
    if metrics is None:
        metrics = get_metric_definitions_from_schema(dataset.schema)["tables"]

    for table_name, table_metrics in metrics.items():
        if not table_metrics:
            continue

        table_metrics_query = _collect_table_metrics_as_table(
            table=dataset.table(table_name).to_ibis(),
            table_metrics=table_metrics,
        )
        table_metrics_data: list[dict[str, Any]] = table_metrics_query.to_pyarrow().to_pylist()
        for metric_name, metric_value in table_metrics_data[0].items():
            yield {
                "level": "table",
                "table_name": table_name,
                "column_name": None,
                "metric_name": metric_name,
                "metric_value": metric_value,
            }


@dlthub.transformation(
    name=DLT_DATASET_METRICS_RESOURCE_NAME,
    table_name=metrics_results_table()["name"],
    columns=metrics_results_table()["columns"],
    write_disposition=metrics_results_table()["write_disposition"],
    schema_contract=metrics_results_table()["schema_contract"],
    references=metrics_results_table()["references"],
)
def dataset_metrics_resource(
    dataset: dlt.Dataset,
    *,
    metrics: list[DatasetMetricDefinition] | None = None,
) -> Iterator[TMetricsResult]:
    if metrics is None:
        metrics = get_metric_definitions_from_schema(dataset.schema)["dataset"]

    for metric in metrics:
        yield {
            "level": "dataset",
            "table_name": None,
            "column_name": None,
            "metric_name": metric.name,
            "metric_value": metric.expr(dataset),
        }


@dlt.source(name=DLT_DATA_QUALITY_SCHEMA_NAME)
def data_quality_metrics(
    dataset: dlt.Dataset,
    *,
    metrics_definitions: TSourceMetricsDefinitions | None = None,
) -> list[dlthub.transformations.DltTransformationResource]:
    if metrics_definitions is None:
        metrics_definitions = get_metric_definitions_from_schema(dataset.schema)

    return [
        column_metrics_resource(dataset, metrics=metrics_definitions["columns"]),
        table_metrics_resource(dataset, metrics=metrics_definitions["tables"]),
        dataset_metrics_resource(dataset, metrics=metrics_definitions["dataset"]),
    ]


# TODO use `dlt.Dataset.write (see https://github.com/dlt-hub/dlt/pull/3092)
def _get_dq_pipeline(
    dataset_name: str,
    destination: TDestinationReferenceArg,
    pipelines_dir: str | None = None,
) -> dlt.Pipeline:
    """Setup the internal data quality checks pipeline. Used by `run_checks()`."""
    pipeline = dlt.pipeline(
        pipeline_name=DLT_DATA_QUALITY_PIPELINE_NAME_TEMPLATE.format(dataset_name=dataset_name),
        dataset_name=dataset_name,
        destination=destination,
        pipelines_dir=pipelines_dir,
    )
    # the internal write pipeline should be stateless; it is limited to the data passed
    # it shouldn't persist state (e.g. incremental cursor) and interfere with other `pipeline.run()`
    pipeline.config.restore_from_destination = False
    return pipeline


# NOTE the license check must wrap "above" the `functools.singledispatch`
# this will add license to all registered implementations;
# This won't catch direct use of individual implementations
# @require_license("dlthub.data_quality")
@functools.singledispatch
def run_metrics(obj: Any, **kwargs: Any) -> LoadInfo:
    raise NotImplementedError(
        f"No implementation of `run_metrics` found for type `{type(obj).__name__}`"
    )


@run_metrics.register(dlt.Pipeline)
def run_metrics__pipeline(
    obj: dlt.Pipeline,
    *,
    metrics_definitions: TSourceMetricsDefinitions | None = None,
) -> LoadInfo:
    """Execute the metrics against the dataset produced by the input `dlt.Pipeline`
    and write metrics results to it.
    """
    with tempfile.TemporaryDirectory() as tmp_dir:
        dq_pipeline = _get_dq_pipeline(
            dataset_name=obj.dataset_name,
            destination=obj.destination,
            pipelines_dir=tmp_dir,
        )
        load_info = dq_pipeline.run(
            data_quality_metrics(dataset=obj.dataset(), metrics_definitions=metrics_definitions)
        )

    return load_info


@run_metrics.register(dlt.Dataset)
def run_metrics__dataset(
    obj: dlt.Dataset,
    *,
    metrics_definitions: TSourceMetricsDefinitions | None = None,
) -> LoadInfo:
    """Execute the checks against the dataset produced by the input `dlt.Dataset`
    and write checks results to it.
    """
    with tempfile.TemporaryDirectory() as tmp_dir:
        dq_pipeline = _get_dq_pipeline(
            dataset_name=obj.dataset_name,
            destination=obj._destination_reference,
            pipelines_dir=tmp_dir,
        )
        load_info = dq_pipeline.run(
            data_quality_metrics(dataset=obj, metrics_definitions=metrics_definitions)
        )

    return load_info
