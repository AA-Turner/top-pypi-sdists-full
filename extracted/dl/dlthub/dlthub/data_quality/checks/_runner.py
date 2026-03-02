from __future__ import annotations

import functools
import tempfile
from collections.abc import Collection, Mapping
from typing import Any, Iterator, Optional, Sequence, TYPE_CHECKING, Union, overload
from typing_extensions import Self

import dlt
from dlt.common.destination.reference import TDestinationReferenceArg
from dlt.common.exceptions import ValueErrorWithKnownValues
from dlt.common.pipeline import LoadInfo
from dlt.common.schema.typing import C_DLT_ID
from sqlglot import exp as sge

import dlthub
import dlthub.transformations
from dlthub.common.license.decorators import require_license
from dlthub.data_quality.storage import (
    DLT_DATA_QUALITY_PIPELINE_NAME_TEMPLATE,
    DLT_DATA_QUALITY_SCHEMA_NAME,
    DLT_CHECKS_TABLE_NAME,
    QUALIFIED_CHECK_NAME_COL,
    TABLE_NAME_COL,
    ROW_COUNT_COL,
    CHECK_COUNT_COL,
    CHECK_SUCCESS_COUNT_COL,
    CHECK_SUCCESS_RATE_COL,
    checks_results_table,
)
from dlthub.data_quality.checks._definitions import _check_hints_to_def
from dlthub.data_quality.checks._definitions import get_schema_check_hints
from dlthub.data_quality.storage import TABLE_CHECKS_RESOURCE_NAME_TEMPLATE
from dlthub.data_quality.typing import TCheckLevel, TSourceChecksDefinitions

if TYPE_CHECKING:
    from dlthub.data_quality.checks._base import LazyCheck


_DATASET_LEVEL_CTE_TEMPLATE = cte_name = "_reduced{idx}"


# TODO chose better name
# TODO CheckSuite could store some cache row-level results in memory
class CheckSuite:
    def __init__(self, dataset: dlt.Dataset, *, checks: dict[str, Sequence[LazyCheck]]) -> None:
        self.dataset = dataset
        self._checks: dict[str, list[LazyCheck]] = {}
        for table_name, table_checks in checks.items():
            self.add_checks(table_name=table_name, checks=table_checks)

        # TODO in the future, this will also hold `metrics` query
        self._planned_queries: dict[str, dlt.Relation] = {}

    @property
    def checks(self) -> dict[str, list[LazyCheck]]:
        """Get all registered checks per table."""
        return self._checks

    def add_checks(self, table_name: str, checks: Sequence[LazyCheck]) -> Self:
        """Add a check for a specific table to the CheckSuite."""
        if table_name not in self.dataset.tables:
            raise ValueErrorWithKnownValues("table_name", table_name, self.dataset.tables)

        for new_check in checks:
            if any(
                new_check.qualified_name == check.qualified_name
                for check in self.checks.get(table_name, [])
            ):
                raise ValueError(
                    f"Check with `qualified_name={new_check.qualified_name}`"
                    f" is already registered for table `{table_name}`."
                )

        self._checks[table_name] = self._checks.get(table_name, []) + list(checks)
        return self

    # TODO allow to filter tables by load_id; this creates incremental checks
    @require_license("dlthub.data_quality")
    def prepare(self, *, load_ids: Optional[Sequence[str]] = None) -> dlt.Relation:
        return prepare_checks__dataset(self.dataset, checks=self.checks)

    def get_successes(self, table_name: str, check: str) -> dlt.Relation:
        """Retrieve records that succeeded the row-level check specified by (table_name, check)"""
        from dlt.common.libs.ibis import ibis

        table_ibis = self.dataset.table(table_name).to_ibis()
        row_level_ibis = row_level_checks(
            self.dataset.table(table_name), checks=self._checks.get(table_name, [])
        ).to_ibis()
        query = table_ibis.join(
            row_level_ibis.filter(ibis._[check] == True).select("_dlt_id"),  # noqa: E712
            "_dlt_id",
        )
        return self.dataset(query)

    def get_failures(self, table_name: str, check: str) -> dlt.Relation:
        """Retrieve records that failed the row-level check specified by (table_name, check)"""
        from dlt.common.libs.ibis import ibis

        table_ibis = self.dataset.table(table_name).to_ibis()
        row_level_ibis = row_level_checks(
            self.dataset.table(table_name), checks=self._checks.get(table_name, [])
        ).to_ibis()
        query = table_ibis.join(
            row_level_ibis.filter(ibis._[check] == False).select("_dlt_id"),  # noqa: E712
            "_dlt_id",
        )
        return self.dataset(query)


# type overloads for prepare_checks to preserve signatures for type checkers
@overload
def prepare_checks(
    data: dlt.Dataset, checks: Mapping[str, Collection[LazyCheck]], **kwargs: Any
) -> dlt.Relation: ...


@overload
def prepare_checks(
    data: Union[dlt.Relation, dlthub.transformations.DltTransformationResource],
    checks: Collection[LazyCheck],
    *,
    level: TCheckLevel = ...,
    **kwargs: Any,
) -> dlt.Relation: ...


# NOTE the license check must wrap "above" the `functools.singledispatch`
# this will add license to all registered implementations;
# This won't catch direct use of individual implementations
@require_license("dlthub.data_quality")
def prepare_checks(data: Any, checks: Any, **kwargs: Any) -> dlt.Relation:
    raise NotImplementedError(
        f"No implementation of `prepare_checks` found for type `{type(data).__name__}`"
    )


prepare_checks = prepare_checks_ = functools.singledispatch(prepare_checks)  # type: ignore[assignment]


@prepare_checks_.register(dlt.Dataset)
@require_license("dlthub.data_quality")
def prepare_checks__dataset(
    data: dlt.Dataset, checks: Mapping[str, Collection[LazyCheck]], **kwargs: Any
) -> dlt.Relation:
    reduced_queries = []
    for table_name, table_checks in checks.items():
        row_level = row_level_checks(data.table(table_name), table_checks)
        table_level = aggregate_row_to_table_level_checks(row_level, table_name=table_name)
        reduced_queries.append(table_level)

    summary = unstack_table_to_dataset_level_checks(reduced_queries)
    return summary


@prepare_checks_.register(dlt.Relation)
@require_license("dlthub.data_quality")
def prepare_checks__relation(
    data: dlt.Relation,
    checks: Collection[LazyCheck],
    *,
    level: TCheckLevel = "table",
    **kwargs: Any,
) -> dlt.Relation:
    """Create a relation that produces a data quality results table."""
    table_name = data._table_name
    row_level = row_level_checks(relation=data, checks=checks)
    if level == "row":
        return row_level
    elif level == "table":
        return aggregate_row_to_table_level_checks(row_level, table_name=table_name)
    elif level == "dataset":
        return unstack_table_to_dataset_level_checks([
            aggregate_row_to_table_level_checks(row_level, table_name=table_name)
        ])
    else:
        raise ValueError


@prepare_checks_.register(dlthub.transformations.DltTransformationResource)
@require_license("dlthub.data_quality")
def prepare_checks__transformation(
    data: dlthub.transformations.DltTransformationResource,
    checks: Collection[LazyCheck],
    *,
    level: TCheckLevel = "table",
    **kwargs: Any,
) -> dlt.Relation:
    # `dlt_plus.transformation.DltTransformation` is a generator that yields `dlt.Relation`
    relation = list(data)[0]
    return prepare_checks(relation, checks, level=level, **kwargs)


def _get_data_quality_checks_transform() -> dlthub.transformations.DltTransformationResource:
    checks_results_table_schema = checks_results_table()

    # TODO user needs both license scopes: `dlthub.data_quality`, `dlthub.transformation`
    @dlthub.transformation(
        table_name=checks_results_table_schema["name"],
        columns=checks_results_table_schema["columns"],
        write_disposition=checks_results_table_schema["write_disposition"],
    )
    def _dlt_checks_results(
        dataset: dlt.Dataset,
        checks: Mapping[str, Collection[LazyCheck]],
    ) -> Iterator[dlt.Relation]:
        """Transformation used to write the data quality checks results"""
        yield prepare_checks(dataset, checks=checks)

    return _dlt_checks_results


# TODO use `dlt.Dataset.write (see https://github.com/dlt-hub/dlt/pull/3092)
def _get_dq_pipeline(
    dataset_name: str,
    destination: TDestinationReferenceArg,
    pipelines_dir: str = None,
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


def _run_dq_pipeline(
    dq_pipeline: dlt.Pipeline, *, dataset: dlt.Dataset, checks: Mapping[str, Collection[LazyCheck]]
) -> LoadInfo:
    """Run the internal data quality checks pipeline. Used by `run_checks()`."""
    dq_schema = dlt.Schema(name=DLT_DATA_QUALITY_SCHEMA_NAME)
    transform = _get_data_quality_checks_transform()
    load_info = dq_pipeline.run([transform(dataset, checks=checks)], schema=dq_schema)
    return load_info


# type overloads for run_checks to preserve signatures for type checkers
@overload
def run_checks(obj: dlt.Pipeline, *, checks: dict[str, list[LazyCheck]]) -> LoadInfo: ...


@overload
def run_checks(obj: dlt.Dataset, *, checks: dict[str, list[LazyCheck]]) -> LoadInfo: ...


@require_license("dlthub.data_quality")
def run_checks(obj: Any, *, checks: Mapping[str, Collection[LazyCheck]], **kwargs: Any) -> LoadInfo:
    """Execute the checks and write results to a `dlt.Dataset`."""
    raise NotImplementedError(
        f"No implementation of `run_checks` found for type `{type(obj).__name__}`"
    )


# export overloaded run_checks, keep dispatch for register
run_checks = run_checks_ = functools.singledispatch(run_checks)  # type: ignore[assignment]


@run_checks_.register(dlt.Pipeline)
@require_license("dlthub.data_quality")
def run_checks__pipeline(obj: dlt.Pipeline, *, checks: dict[str, list[LazyCheck]]) -> LoadInfo:
    """Execute the checks against the dataset produced by the input `dlt.Pipeline`
    and write checks results to it.
    """
    with tempfile.TemporaryDirectory() as tmp_dir:
        dq_pipeline = _get_dq_pipeline(
            dataset_name=obj.dataset_name,
            destination=obj.destination,
            pipelines_dir=tmp_dir,
        )
        load_info = _run_dq_pipeline(dq_pipeline, dataset=obj.dataset(), checks=checks)

    return load_info


@run_checks_.register(dlt.Dataset)
@require_license("dlthub.data_quality")
def run_checks__dataset(obj: dlt.Dataset, *, checks: dict[str, list[LazyCheck]]) -> LoadInfo:
    """Execute the checks against the input `dlt.Dataset` and write checks results to it."""
    with tempfile.TemporaryDirectory() as tmp_dir:
        dq_pipeline = _get_dq_pipeline(
            dataset_name=obj.dataset_name,
            destination=obj._destination_reference,
            pipelines_dir=tmp_dir,
        )
        load_info = _run_dq_pipeline(dq_pipeline, dataset=obj, checks=checks)

    return load_info


def row_level_checks(
    relation: dlt.Relation,
    checks: Collection[LazyCheck],
) -> dlt.Relation:
    """Create a `dlt.Relation` of shape (n records, m checks).

    Each row is associated with a record in the table. The column `_dlt_id` is
    included if available.
    """
    # TODO should check that all `checks` are associated with the same table
    check_expressions: list[sge.ExpOrStr] = [
        check.expr.as_(check.qualified_name) for check in checks
    ]
    from_: sge.ExpOrStr = (
        relation._table_name if relation._table_name else relation.sqlglot_expression.subquery()
    )
    # TODO a relation may not have a `_dlt_id` column
    _dlt_id_cols: list[sge.ExpOrStr] = [C_DLT_ID] if C_DLT_ID in relation.columns else []

    query = sge.select(*_dlt_id_cols, *check_expressions).from_(from_)
    return relation._dataset.query(query)


def aggregate_row_to_table_level_checks(
    row_level_results: dlt.Relation, table_name: Optional[str] = None
) -> dlt.Relation:
    """Aggregate row-level checks result."""

    selection = [
        sge.Count(this=sge.Star()).as_(ROW_COUNT_COL),
        *(
            sge.cast(
                sge.Sum(this=sge.cast(col, to=sge.DataType.Type.INT)),
                to=sge.DataType.Type.INT,
            ).as_(col)
            for col in row_level_results.columns
            if col != C_DLT_ID
        ),
    ]
    if table_name:
        selection.insert(0, sge.Literal(this=table_name, is_string=True).as_(TABLE_NAME_COL))

    reduced_expr = sge.select(*selection).from_(row_level_results.sqlglot_expression.subquery())
    return row_level_results._dataset.query(reduced_expr)


def reduce_over_columns(relation: dlt.Relation) -> dlt.Relation:
    """Return a column containing the ratio of check successes across all checks for each row."""
    n_columns = len(relation.columns) - 1

    sum_expr: sge.Expression = None
    for col in relation.columns:
        if col == C_DLT_ID:
            continue

        col_as_int = sge.cast(col, to=sge.DataType.Type.INT)
        if sum_expr is None:
            sum_expr = col_as_int
        else:
            sum_expr = sge.Add(this=sum_expr, expression=col_as_int)

    if sum_expr is None:
        raise ValueError("No check columns found")

    reduced_expr = sge.select(
        sge.column(C_DLT_ID),
        sum_expr.as_(alias=CHECK_SUCCESS_COUNT_COL),
        sge.Literal.number(n_columns).as_(CHECK_COUNT_COL),
    ).from_(relation.sqlglot_expression.subquery())

    return relation._dataset.query(reduced_expr)


def _unstack_single_table(
    reduced_over_rows: dlt.Relation,
    row_level_cte_name: str = _DATASET_LEVEL_CTE_TEMPLATE.format(idx=""),
) -> sge.Expression:
    has_table_name_column = any(
        col.output_name == TABLE_NAME_COL for col in reduced_over_rows.sqlglot_expression.selects
    )

    union_all_expr = None
    for col in reduced_over_rows.sqlglot_expression.selects:
        column_name = col.output_name
        if column_name in [ROW_COUNT_COL, TABLE_NAME_COL]:
            continue

        selection: list[sge.ExpOrStr]
        if has_table_name_column:
            selection = [TABLE_NAME_COL]
        else:
            selection = []

        selection += [
            sge.Literal.string(column_name).as_(QUALIFIED_CHECK_NAME_COL),
            ROW_COUNT_COL,
            sge.to_column(column_name).as_(CHECK_SUCCESS_COUNT_COL),
        ]

        unstacked_check_expr = sge.select(*selection).from_(row_level_cte_name)
        if union_all_expr is None:
            union_all_expr = unstacked_check_expr
        else:
            union_all_expr = sge.Union(
                this=union_all_expr, expression=unstacked_check_expr, distinct=False
            )

    assert isinstance(union_all_expr, sge.Expression)
    return union_all_expr


def unstack_table_to_dataset_level_checks(
    reduced_over_rows: Sequence[dlt.Relation],
) -> dlt.Relation:
    if len(reduced_over_rows) < 1:
        raise ValueError(
            "Expected at least one relation in `reduced_over_rows` kwarg."
            f" Received `{len(reduced_over_rows)}`"
        )

    UNSTACKED_CTE_NAME = "checks_summary"

    final_selection: list[sge.ExpOrStr]
    if TABLE_NAME_COL in reduced_over_rows[0].columns:
        final_selection = [TABLE_NAME_COL]
    else:
        final_selection = []

    final_selection += [
        QUALIFIED_CHECK_NAME_COL,
        ROW_COUNT_COL,
        CHECK_SUCCESS_COUNT_COL,
    ]

    success_rate_expr = sge.Div(
        this=sge.Column(this=CHECK_SUCCESS_COUNT_COL), expression=sge.Column(this=ROW_COUNT_COL)
    ).as_(CHECK_SUCCESS_RATE_COL)
    final_selection += [success_rate_expr]

    table_summary_expr = sge.select(*final_selection).from_(UNSTACKED_CTE_NAME)

    full_result_expr = None
    for idx, query in enumerate(reduced_over_rows):
        cte_name = _DATASET_LEVEL_CTE_TEMPLATE.format(idx=idx)
        table_summary_expr = table_summary_expr.with_(cte_name, as_=query.sqlglot_expression)

        # TODO support row-level and table-level queries
        unstacked_query = _unstack_single_table(query, cte_name)
        if full_result_expr is None:
            full_result_expr = unstacked_query
        else:
            full_result_expr = sge.Union(
                this=unstacked_query, expression=full_result_expr, distinct=False
            )

    assert isinstance(full_result_expr, sge.Expression)
    table_summary_expr = table_summary_expr.with_(UNSTACKED_CTE_NAME, as_=full_result_expr)
    return query._dataset.query(table_summary_expr)


# NOTE for some reason, importing `dlthub` in this file creates a circular import
def _create_resource(
    dataset: dlt.Dataset, table_name: str, checks_definitions: Sequence[LazyCheck]
) -> dlthub.transformations.DltTransformationResource:
    @dlthub.transformation(
        name=TABLE_CHECKS_RESOURCE_NAME_TEMPLATE.format(table_name=table_name),
        table_name=DLT_CHECKS_TABLE_NAME,
    )
    def checks_resource(
        dataset: dlt.Dataset, *, table_name: str, checks_definitions: Sequence[LazyCheck]
    ) -> Iterator[dlt.Relation]:
        yield prepare_checks__relation(
            dataset.table(table_name), checks=checks_definitions, level="dataset"
        )

    return checks_resource(dataset, table_name=table_name, checks_definitions=checks_definitions)


@dlt.source(name=DLT_DATA_QUALITY_SCHEMA_NAME)
def data_quality_checks(
    dataset: dlt.Dataset,
    *,
    checks_definitions: TSourceChecksDefinitions | None = None,
) -> Iterator[dlthub.transformations.DltTransformationResource]:
    if checks_definitions is None:
        checks_definitions = {
            "dataset": [],
            "tables": {},
        }
        checks_hints = get_schema_check_hints(dataset.schema)
        for table_name, table_checks_hint in checks_hints["tables"].items():
            if (table_name not in checks_definitions["tables"]) and table_checks_hint:
                checks_definitions["tables"][table_name] = []

            for check_hint in table_checks_hint:
                checks_definitions["tables"][table_name].append(_check_hints_to_def(check_hint))

    for table_name, table_checks_definitions in checks_definitions["tables"].items():
        yield _create_resource(
            dataset, table_name=table_name, checks_definitions=table_checks_definitions
        )
