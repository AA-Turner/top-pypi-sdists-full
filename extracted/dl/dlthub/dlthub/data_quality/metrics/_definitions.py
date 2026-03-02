from __future__ import annotations

import functools
from collections.abc import Sequence
from typing import Any, Callable, overload, Literal, TypeVar

import dlt
from dlt.common.libs.ibis import ir
from dlt.common.data_types import TDataType, py_type_to_sc_type
from dlt.common.schema import utils as schema_utils
from dlt.common.typing import ParamSpec
from dlt.extract import DltResource, DltSource
from dlt.extract.decorators import (
    DltSourceFactoryWrapper,
    ResourceFactory,
    TResourceFunParams,
    TDltResourceImpl,
    SourceFactory,
    TDltSourceImpl,
    TSourceFunParams,
)

from dlthub.data_quality.typing import (
    TMetricHint,
    TResourceMetricsHints,
    TSourceMetricsHints,
    TSourceMetricsDefinitions,
    METRICS_HINT_KEY,
)
from dlthub.data_quality.metrics._base import (
    _BaseMetricDefinition,
    DatasetMetricDefinition,
    TableMetricDefinition,
    ColumnMetricDefinition,
)

P = ParamSpec("P")
R = TypeVar("R")
TDltSourceOrResource = TypeVar("TDltSourceOrResource", DltSource, DltResource)


def get_schema_metric_hints(schema: dlt.Schema) -> TSourceMetricsHints:
    """Get all metric hints stored on the schema.

    This excludes internal dlt tables and columns, and metrics defined on
    incomplete* tables and columns.

    *An incomplete table or column is typically the result of hints defined
    via `@dlt.resource` but not having received data yet.
    """
    metrics_hints: TSourceMetricsHints = {
        "dataset": [],
        "tables": {},
        "columns": {},
    }

    if schema.settings.get(METRICS_HINT_KEY):
        # TODO add `METRICS_HINT_KEY` to `dlt.Schema.settings` typing in `dlt-hub/dlt`
        metrics_hints["dataset"] = schema.settings[METRICS_HINT_KEY]["dataset"]  # type: ignore[literal-required]

    for table_schema in schema.data_tables(seen_data_only=True):
        table_name = table_schema["name"]
        if table_schema.get(METRICS_HINT_KEY) is None:
            continue

        # TODO add `METRICS_HINT_KEY` to `dlt.Schema.settings` typing in `dlt-hub/dlt`
        metrics_hints["tables"][table_name] = table_schema[METRICS_HINT_KEY]["table"]  # type: ignore[literal-required]
        for column_name in schema.get_table_columns(table_name):
            if schema_utils.is_dlt_table_or_column(column_name, schema._dlt_tables_prefix):
                continue

            column_metrics = table_schema[METRICS_HINT_KEY]["columns"].get(column_name)  # type: ignore[literal-required]
            if column_metrics is None:
                continue

            if table_name not in metrics_hints["columns"]:
                metrics_hints["columns"][table_name] = {}

            metrics_hints["columns"][table_name][column_name] = column_metrics

    return metrics_hints


def get_metric_definitions_from_schema(schema: dlt.Schema) -> TSourceMetricsDefinitions:
    return _source_metric_hints_to_defs(get_schema_metric_hints(schema))


# TODO implement a `get_metric_definitions_from_destination()`
# this would read the `_dlt_version` table to retrieve the schema and parse the schema


def _metric_def_to_hints(metric: _BaseMetricDefinition) -> TMetricHint:
    return_type = _determine_return_type(metric.return_type)
    return TMetricHint(
        name=metric.name,
        level=metric.level,
        return_type=return_type if return_type != "variant" else None,
        is_variant=return_type == "variant",
        # TODO ensure `.arguments` are safe to serialize with `dlt.Schema`
        # enforce this at the _BaseMetricDefinition level
        args=metric.arguments,  # type: ignore[typeddict-item]
    )


def _metric_hint_to_def(
    metric_hint: TMetricHint,
    table_name: str | None = None,
    column_name: str | None = None,
) -> TableMetricDefinition | ColumnMetricDefinition | DatasetMetricDefinition:
    # TODO need to implement way to lookup custom metrics
    # option 1: serialize metric SQLGlot to schema
    # option 2: register Python path / module dependencies required at runtime
    from dlthub.data_quality.metrics import (
        dataset as dataset_module,
        table as table_module,
        column as column_module,
    )

    if metric_hint["level"] == "dataset":
        dataset_metric_def: DatasetMetricDefinition = getattr(dataset_module, metric_hint["name"])(
            **metric_hint["args"]
        )
        return dataset_metric_def
    elif metric_hint["level"] == "table":
        table_metric_def: TableMetricDefinition = getattr(table_module, metric_hint["name"])(
            **metric_hint["args"]
        )
        return table_metric_def
    elif metric_hint["level"] == "column":
        column_metric_def: ColumnMetricDefinition = getattr(column_module, metric_hint["name"])(
            column=column_name, **metric_hint["args"]
        )
        return column_metric_def
    else:
        raise ValueError(
            f"Invalid metric level `{metric_hint['level']}` for metric `{metric_hint['name']}`."
        )


def _source_metric_hints_to_defs(metric_hints: TSourceMetricsHints) -> TSourceMetricsDefinitions:
    return {
        "dataset": [_metric_hint_to_def(metric_hint) for metric_hint in metric_hints["dataset"]],  # type: ignore[misc]
        "tables": {
            table_name: [
                _metric_hint_to_def(metric_hint)  # type: ignore[misc]
                for metric_hint in metric_hints["tables"][table_name]
            ]
            for table_name in metric_hints["tables"]
        },
        "columns": {
            table_name: {
                column_name: [
                    _metric_hint_to_def(metric_hint)  # type: ignore[misc]
                    for metric_hint in metric_hints["columns"][table_name][column_name]
                ]
                for column_name in metric_hints["columns"][table_name]
            }
            for table_name in metric_hints["columns"]
        },
    }


# TODO enable table-level metric specify the table name at definition
# when applied to `@dlt.resource`, the table name is implicit
def _metric_defs_to_source_hints(metrics: Sequence[_BaseMetricDefinition]) -> TSourceMetricsHints:
    metric_hints: TSourceMetricsHints = {
        "dataset": [],
        "tables": {},
        "columns": {},
    }
    for metric in metrics:
        if metric.level == "dataset":
            metric_hints["dataset"].append(_metric_def_to_hints(metric))
        else:
            # TODO implement table and column level metrics on `@dlt.source`
            raise NotImplementedError(
                f"Only dataset-level metrics can be set on `@dlt.source`. Received `{metric}`."
            )

    return metric_hints


def _metric_defs_to_resource_hints(
    metrics: Sequence[_BaseMetricDefinition],
) -> TResourceMetricsHints:
    metric_hints: TResourceMetricsHints = {
        "table": [],
        "columns": {},
    }
    for metric in metrics:
        if metric.level == "dataset":
            raise ValueError(
                "Dataset metrics can only be used on `@dlt.source` objects."
                f" Received resource metric `{metric}`."
            )
        elif metric.level == "table":
            metric_hints["table"].append(_metric_def_to_hints(metric))
        elif metric.level == "column":
            assert isinstance(metric, ColumnMetricDefinition)
            if metric.column not in metric_hints["columns"]:
                metric_hints["columns"][metric.column] = []

            metric_hints["columns"][metric.column].append(_metric_def_to_hints(metric))
        else:
            raise ValueError(f"Invalid metric level `{metric.level}` for metric `{metric}`.")

    return metric_hints


@overload
def with_metrics(
    *metrics: _BaseMetricDefinition,
) -> Callable[[R], R]:
    # decorator pattern
    pass


@overload
def with_metrics(
    source_or_resource: SourceFactory[TSourceFunParams, TDltSourceImpl],
    *metrics: _BaseMetricDefinition,
) -> SourceFactory[TSourceFunParams, TDltSourceImpl]:
    # adapter pattern for source factory (@dlt.source before call)
    pass


@overload
def with_metrics(
    source_or_resource: ResourceFactory[TResourceFunParams, TDltResourceImpl],
    *metrics: _BaseMetricDefinition,
) -> ResourceFactory[TResourceFunParams, TDltResourceImpl]:
    # adapter pattern for resource factory (@dlt.resource before call)
    pass


@overload
def with_metrics(
    source_or_resource: TDltSourceOrResource,
    *metrics: _BaseMetricDefinition,
) -> TDltSourceOrResource:
    # adapter pattern for instantiated source or resource
    pass


def with_metrics(
    source_or_resource: Any = None,
    *metrics: _BaseMetricDefinition,
) -> Any:
    """Register metrics on the source, resource, transformer or transformation."""

    # this function receives arguments from all overloads. we support both decorator and adapter
    # use so the first argument can be a metric (decorate) -  in this case we return a wrapper
    # that receives decorated object
    if isinstance(source_or_resource, _BaseMetricDefinition):
        return functools.partial(_with_metrics, metrics=(source_or_resource,) + metrics)

    if source_or_resource is None and not metrics:
        raise ValueError(
            "`with_metrics()` requires at least one metric definition or a source/resource "
            "argument."
        )

    # if first argument is not a metric, we have adapter pattern where we assume source or resource
    return _with_metrics(source_or_resource=source_or_resource, metrics=metrics)


def _with_metrics(
    source_or_resource: Any,
    metrics: Sequence[_BaseMetricDefinition],
) -> Any:
    if isinstance(source_or_resource, DltSource):
        source_metric_hints = _metric_defs_to_source_hints(metrics)
        source_or_resource.schema._settings[METRICS_HINT_KEY] = source_metric_hints  # type: ignore[literal-required]

    elif isinstance(source_or_resource, DltSourceFactoryWrapper):
        # resolving metrics outside `wrapper()` allows to fail early
        source_metric_hints = _metric_defs_to_source_hints(metrics)

        def _postprocess(source: DltSource) -> DltSource:
            source.schema._settings[METRICS_HINT_KEY] = source_metric_hints  # type: ignore[literal-required]
            return source

        source_or_resource.add_postprocessor(_postprocess)

    elif isinstance(source_or_resource, DltResource):
        # resolving metrics outside `wrapper()` allows to fail early
        resource_metric_hints = _metric_defs_to_resource_hints(metrics)
        # NOTE could store metrics hints under `additional_table_hints`
        # which would prevent rewriting the whole `_hints` and avoid `dlt` typing complaining
        source_or_resource._set_hints(
            source_or_resource._hints | {METRICS_HINT_KEY: resource_metric_hints}  # type: ignore[arg-type]
        )

    else:
        raise ValueError(
            f"`with_metrics()` is applied on unsupported object type `{type(source_or_resource)}`"
        )

    return source_or_resource


def _determine_return_type(return_type: type) -> TDataType | Literal["variant"]:
    if issubclass(return_type, ir.IntegerScalar):
        return "bigint"
    elif issubclass(return_type, ir.NumericScalar):
        return "double"
    elif issubclass(return_type, ir.StringScalar):
        return "text"
    elif issubclass(return_type, ir.BooleanScalar):
        return "bool"
    elif issubclass(return_type, ir.TimestampScalar):
        return "timestamp"
    elif issubclass(return_type, ir.DateScalar):
        return "date"
    elif issubclass(return_type, ir.TimeScalar):
        return "time"
    elif issubclass(return_type, ir.Scalar):
        return "variant"
    else:
        return py_type_to_sc_type(return_type)
