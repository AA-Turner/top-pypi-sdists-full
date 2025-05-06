import enum
from dataclasses import dataclass
from typing import Callable
from typing import List
from typing import Optional
from typing import Type

from pypika import Field
from pypika.analytics import AnalyticFunction
from pypika.analytics import Avg
from pypika.analytics import Count
from pypika.analytics import Max
from pypika.analytics import Min
from pypika.analytics import Sum
from pypika.analytics import WindowFrameAnalyticFunction
from pypika.functions import Cast
from pypika.functions import Coalesce
from pypika.functions import NullIf
from pypika.functions import Sqrt
from pypika.terms import Array
from pypika.terms import Case
from pypika.terms import Criterion
from pypika.terms import Function
from pypika.terms import IgnoreNullsAnalyticFunction
from pypika.terms import LiteralValue
from pypika.terms import Term
from pypika.terms import Tuple
from pypika.utils import format_alias_sql

from tecton_core.aggregation_utils import QueryWindowSpec
from tecton_core.aggregation_utils import get_materialization_aggregation_column_prefixes
from tecton_core.aggregation_utils import get_simple_window_query
from tecton_core.query.dialect import Dialect
from tecton_core.query.sql_compat import CompatFunctions
from tecton_proto.common import aggregation_function__client_pb2 as afpb


@dataclass
class AggregationPlan:
    """
    An AggregationPlan contains all the methods required to compute feature values for a specific Tecton aggregation.

    The order of the columns must be the same in:
    * the return list in partial_aggregation_query
    * the arguments list in full_aggregation_query
    * materialized_column_prefixes

    Attributes:
        partial_aggregation_query: A method that maps an input column name to a list of output pypika columns containing the partial aggregates.
        full_aggregation_query: A method that maps a list of input partial aggregate columns and a QueryWindowSpec to an output pypika column containing the full aggregates.
        full_aggregation_with_filter_query_term: A method that maps a list of input partial aggregate columns and a condition for FILTER clause to an output pypika column containing the full aggregates.
        materialized_column_prefixes: The list of prefixes that should be applied to the columns produced by `partial_aggregation_transform`.
        continuous_aggregation_query_terms: (Optional) A method that maps an input columns to a list of output pypika columns containing the partial aggregates for continuous mode.
        supported_dialects: (Optional) List of dialects, which work with this aggregation plan.
        full_aggregation_default_value: (Optional) Default value for this aggregation, which will be returned to a user in case there are no data point.
    """

    partial_aggregation_query_terms: Callable[[str], List[Term]]
    full_aggregation_with_filter_query_term: Callable[[List[str], Term], Term]
    full_aggregation_query_term: Callable[[List[str], QueryWindowSpec, CompatFunctions], Term]
    materialized_column_prefixes: List[str]
    continuous_aggregation_query_terms: Optional[Callable[[str], List[Term]]] = None
    supported_dialects: Optional[List[Dialect]] = None
    full_aggregation_default_value: Optional[Term] = None

    def materialized_column_names(self, input_column_name: str) -> List[str]:
        return [f"{prefix}_{input_column_name}" for prefix in self.materialized_column_prefixes]

    def is_supported(self, dialect: Dialect) -> bool:
        return self.supported_dialects is None or dialect in self.supported_dialects


def _simple_aggregation_plan(
    aggregation_function: afpb.AggregationFunction,
    analytic_function: Type[WindowFrameAnalyticFunction],
    supported_dialects: Optional[List[Dialect]] = None,
    ignore_nulls: bool = False,
) -> AggregationPlan:
    return AggregationPlan(
        partial_aggregation_query_terms=lambda col: [analytic_function(Field(col))],
        full_aggregation_with_filter_query_term=lambda cols, filter_: (
            FilterAggregationInput(analytic_function(Field(cols[0])), filter_)
        ),
        full_aggregation_query_term=lambda cols, query_window_spec, compat_funcs: get_simple_window_query(
            cols[0], query_window_spec, analytic_function, compat_funcs, ignore_nulls
        ),
        materialized_column_prefixes=get_materialization_aggregation_column_prefixes(aggregation_function),
        continuous_aggregation_query_terms=lambda col: [Field(col)],
        supported_dialects=supported_dialects,
    )


def _wrap_aggregation_in_window(query_window_spec: QueryWindowSpec) -> Callable[[Term], Term]:
    def wrapper(agg: Term) -> Term:
        return (
            agg.over(*[Field(x) for x in query_window_spec.partition_cols])
            .orderby(*[Field(query_window_spec.order_by_col)])
            .range(query_window_spec.range_start, query_window_spec.range_end)
        )

    return wrapper


def _wrap_aggregation_in_filter(filter_: Criterion) -> Callable[[Term], Term]:
    def wrapper(agg: Term) -> Term:
        return FilterAggregationInput(agg, filter_)

    return wrapper


def _mean_full_aggregation(cols: List[str], aggregation_wrapper: Callable[[Term], Term]) -> Term:
    mean_col, count_col = cols
    sum_query_term = aggregation_wrapper(Sum(Field(mean_col) * Field(count_col)))
    count_query_term = aggregation_wrapper(Sum(Field(count_col)))
    return sum_query_term / count_query_term


# sample variation equation: (Σ(x^2) - (Σ(x)^2)/N)/N-1
def _var_samp_full_aggregation(cols: List[str], aggregation_wrapper: Callable[[Term], Term]) -> Term:
    sum_of_squares_col, count_col, sum_col = cols
    count_query_term = Cast(
        (aggregation_wrapper(Sum(Field(count_col)))),
        "double",
    )
    sum_of_squares_query_term = Cast(
        (aggregation_wrapper(Sum(Field(sum_of_squares_col)))),
        "double",
    )
    sum_query_term = Cast(
        (aggregation_wrapper(Sum(Field(sum_col)))),
        "double",
    )
    # check if count is equal to 0 for divide by 0 errors
    var_samp_col = (sum_of_squares_query_term - (sum_query_term**2) / count_query_term) / NullIf(
        count_query_term - 1, 0
    )
    # Due to floating-point error `var_samp` can be negative when sum of squares is too close to square of sums.
    # This might happen when feature values are too close (or identical) and variance is essentially zero.
    return Case().when(var_samp_col.isnotnull(), Function("greatest", var_samp_col, LiteralValue("0")))


def _var_pop_full_aggregation(cols: List[str], aggregation_wrapper: Callable[[Term], Term]) -> Term:
    sum_of_squares_col, count_col, sum_col = cols
    count_query_term = Cast(
        (aggregation_wrapper(Sum(Field(count_col)))),
        "double",
    )
    sum_of_squares_query_term = Cast(
        (aggregation_wrapper(Sum(Field(sum_of_squares_col)))),
        "double",
    )
    sum_query_term = Cast(
        (aggregation_wrapper(Sum(Field(sum_col)))),
        "double",
    )
    var_pop = (sum_of_squares_query_term / count_query_term) - (sum_query_term / count_query_term) ** 2
    # Due to floating-point error `var_pop` can be negative when sum of squares is too close to square of sums.
    # This might happen when feature values are too close (or identical) and variance is essentially zero.
    return Case().when(var_pop.isnotnull(), Function("greatest", var_pop, LiteralValue("0")))


def _stddev_samp_full_aggregation(cols: List[str], aggregation_wrapper: Callable[[Term], Term]) -> Term:
    return Sqrt(_var_samp_full_aggregation(cols, aggregation_wrapper))


def _stddev_pop_full_aggregation(cols: List[str], aggregation_wrapper: Callable[[Term], Term]) -> Term:
    return Sqrt(_var_pop_full_aggregation(cols, aggregation_wrapper))


def _mean_aggregation_plan() -> AggregationPlan:
    return AggregationPlan(
        partial_aggregation_query_terms=lambda col: [Avg(Field(col)), Count(Field(col))],
        full_aggregation_with_filter_query_term=lambda cols, filter_: (
            _mean_full_aggregation(cols, _wrap_aggregation_in_filter(filter_))
        ),
        full_aggregation_query_term=lambda cols, query_window_spec, compat_funcs: (
            _mean_full_aggregation(cols, lambda term: compat_funcs.over_window(term, query_window_spec))
        ),
        materialized_column_prefixes=get_materialization_aggregation_column_prefixes(afpb.AGGREGATION_FUNCTION_MEAN),
        continuous_aggregation_query_terms=lambda col: [Cast(Field(col), "double"), Cast(LiteralValue("1"), "bigint")],
    )


class ListReverse(WindowFrameAnalyticFunction):
    def __init__(self, *args, **kwargs):
        super(ListReverse, self).__init__("list_reverse", *args, **kwargs)


class FirstLastAggregateFunctions(enum.Enum):
    FIRST_N = "arg_min"
    LAST_N = "arg_max"
    FIRST_DISTINCT_N = "arg_min_distinct"
    LAST_DISTINCT_N = "arg_max_distinct"


def _first_last_n_partial_agg(type_: FirstLastAggregateFunctions, col: str, anchor_term: Term, param_n: str) -> Term:
    return Function(type_.value, Field(col), anchor_term, LiteralValue(param_n))


def _first_last_n_full_agg(
    type_: FirstLastAggregateFunctions,
    col: str,
    anchor_term: Term,
    param_n: str,
    aggregation_wrapper: Callable[[Term], Term],
) -> Term:
    agg = Function(type_.value, Field(col), anchor_term, LiteralValue(param_n))
    agg = aggregation_wrapper(agg)
    agg = Function("flatten", agg)
    agg = Function("list_slice", agg, 1, LiteralValue(param_n))
    return Coalesce(
        agg,
        LiteralValue("[]"),
    )


def _first_last_distinct_n_full_agg(
    type_: FirstLastAggregateFunctions,
    col: str,
    anchor_term: Term,
    param_n: str,
    aggregation_wrapper: Callable[[Term], Term],
) -> Term:
    fun_name = type_.value + "_unnest"
    agg = Function(fun_name, Field(col), anchor_term, LiteralValue(param_n))
    return Coalesce(
        aggregation_wrapper(agg),
        LiteralValue("[]"),
    )


class ApproxCountDistinctPartial(AnalyticFunction):
    def __init__(self, input_term, precision_term, **kwargs):
        super(ApproxCountDistinctPartial, self).__init__(
            "approx_count_distinct_partial", *[input_term, precision_term], **kwargs
        )


class ApproxCountDistinctCombine(WindowFrameAnalyticFunction):
    def __init__(self, input_term, precision_term, **kwargs):
        super(ApproxCountDistinctCombine, self).__init__(
            "approx_count_distinct_combine", *[input_term, precision_term], **kwargs
        )


class ApproxCountDistinctContinuous(Function):
    def __init__(self, input_term, precision_term, **kwargs):
        super(ApproxCountDistinctContinuous, self).__init__(
            "approx_count_distinct_continuous", *[input_term, precision_term], **kwargs
        )


class StructExtract(Function):
    def __init__(self, input_term, field_name_term, **kwargs):
        super(StructExtract, self).__init__("struct_extract", *[input_term, field_name_term], **kwargs)


class FilterAggregationInput(Term):
    def __init__(self, aggregation: Term, filter_: Criterion) -> None:
        self.aggregation = aggregation
        self.filter_ = filter_
        super(FilterAggregationInput, self).__init__()

    def get_sql(self, **kwargs):
        agg_sql = self.aggregation.get_sql(**kwargs)
        filter_sql = self.filter_.get_sql(**kwargs)
        sql = f"{agg_sql} FILTER ({filter_sql})"
        return format_alias_sql(sql, self.alias)


class Last(WindowFrameAnalyticFunction, IgnoreNullsAnalyticFunction):
    def __init__(self, *terms, **kwargs):
        super(Last, self).__init__("LAST", *terms, **kwargs)


class ApproxQuantilePartial(WindowFrameAnalyticFunction):
    def __init__(self, input_term, precision_term, **kwargs):
        super().__init__("approx_quantile_partial", *[input_term, precision_term], **kwargs)


class ApproxQuantileCombine(WindowFrameAnalyticFunction):
    def __init__(self, input_term, quantile_term, precision_term, **kwargs):
        super().__init__("approx_quantile_combine", *[input_term, quantile_term, precision_term], **kwargs)


AGGREGATION_PLANS = {
    afpb.AGGREGATION_FUNCTION_SUM: _simple_aggregation_plan(afpb.AGGREGATION_FUNCTION_SUM, Sum),
    afpb.AGGREGATION_FUNCTION_MIN: _simple_aggregation_plan(afpb.AGGREGATION_FUNCTION_MIN, Min),
    afpb.AGGREGATION_FUNCTION_MAX: _simple_aggregation_plan(afpb.AGGREGATION_FUNCTION_MAX, Max),
    afpb.AGGREGATION_FUNCTION_COUNT: AggregationPlan(
        partial_aggregation_query_terms=lambda col: [Count(Field(col))],
        full_aggregation_query_term=lambda cols, query_window_spec, compat_funcs: Coalesce(
            get_simple_window_query(cols[0], query_window_spec, Sum, compat_funcs), LiteralValue("0")
        ),
        full_aggregation_default_value=LiteralValue("0"),
        full_aggregation_with_filter_query_term=lambda cols, filter_: FilterAggregationInput(
            Sum(Field(cols[0])), filter_
        ),
        materialized_column_prefixes=get_materialization_aggregation_column_prefixes(afpb.AGGREGATION_FUNCTION_COUNT),
        continuous_aggregation_query_terms=lambda col: [Cast(LiteralValue("1"), "bigint")],
    ),
    afpb.AGGREGATION_FUNCTION_MEAN: _mean_aggregation_plan(),
    afpb.AGGREGATION_FUNCTION_VAR_SAMP: AggregationPlan(
        partial_aggregation_query_terms=lambda col: [Sum(Field(col) ** 2), Count(Field(col)), Sum(Field(col))],
        full_aggregation_with_filter_query_term=lambda cols, filter_: (
            _var_samp_full_aggregation(cols, _wrap_aggregation_in_filter(filter_))
        ),
        full_aggregation_query_term=lambda cols, query_window_spec, compat_funcs: (
            _var_samp_full_aggregation(cols, lambda term: compat_funcs.over_window(term, query_window_spec))
        ),
        materialized_column_prefixes=get_materialization_aggregation_column_prefixes(
            afpb.AGGREGATION_FUNCTION_VAR_SAMP
        ),
        continuous_aggregation_query_terms=lambda col: [
            Cast(Field(col) ** 2, "double"),
            Cast(LiteralValue("1"), "bigint"),
            Cast(Field(col), "double"),
        ],
    ),
    afpb.AGGREGATION_FUNCTION_VAR_POP: AggregationPlan(
        partial_aggregation_query_terms=lambda col: [Sum(Field(col) ** 2), Count(Field(col)), Sum(Field(col))],
        full_aggregation_with_filter_query_term=lambda cols, filter_: (
            _var_pop_full_aggregation(cols, _wrap_aggregation_in_filter(filter_))
        ),
        full_aggregation_query_term=lambda cols, query_window_spec, compat_funcs: (
            _var_pop_full_aggregation(cols, lambda term: compat_funcs.over_window(term, query_window_spec))
        ),
        materialized_column_prefixes=get_materialization_aggregation_column_prefixes(afpb.AGGREGATION_FUNCTION_VAR_POP),
        continuous_aggregation_query_terms=lambda col: [
            Cast(Field(col) ** 2, "double"),
            Cast(LiteralValue("1"), "bigint"),
            Cast(Field(col), "double"),
        ],
    ),
    afpb.AGGREGATION_FUNCTION_STDDEV_SAMP: AggregationPlan(
        partial_aggregation_query_terms=lambda col: [Sum(Field(col) ** 2), Count(Field(col)), Sum(Field(col))],
        full_aggregation_with_filter_query_term=lambda cols, filter_: _stddev_samp_full_aggregation(
            cols, _wrap_aggregation_in_filter(filter_)
        ),
        full_aggregation_query_term=lambda cols, query_window_spec, compat_funcs: _stddev_samp_full_aggregation(
            cols, lambda term: compat_funcs.over_window(term, query_window_spec)
        ),
        materialized_column_prefixes=get_materialization_aggregation_column_prefixes(
            afpb.AGGREGATION_FUNCTION_STDDEV_SAMP
        ),
        continuous_aggregation_query_terms=lambda col: [
            Cast(Field(col) ** 2, "double"),
            Cast(LiteralValue("1"), "bigint"),
            Cast(Field(col), "double"),
        ],
    ),
    afpb.AGGREGATION_FUNCTION_STDDEV_POP: AggregationPlan(
        partial_aggregation_query_terms=lambda col: [Sum(Field(col) ** 2), Count(Field(col)), Sum(Field(col))],
        full_aggregation_with_filter_query_term=lambda cols, filter_: _stddev_pop_full_aggregation(
            cols, _wrap_aggregation_in_filter(filter_)
        ),
        full_aggregation_query_term=lambda cols, query_window_spec, compat_funcs: _stddev_pop_full_aggregation(
            cols, lambda term: compat_funcs.over_window(term, query_window_spec)
        ),
        materialized_column_prefixes=get_materialization_aggregation_column_prefixes(
            afpb.AGGREGATION_FUNCTION_STDDEV_POP
        ),
        continuous_aggregation_query_terms=lambda col: [
            Cast(Field(col) ** 2, "double"),
            Cast(LiteralValue("1"), "bigint"),
            Cast(Field(col), "double"),
        ],
    ),
    afpb.AGGREGATION_FUNCTION_FIRST_NON_DISTINCT_N: lambda time_term, params, is_continuous: AggregationPlan(
        partial_aggregation_query_terms=lambda col: [
            _first_last_n_partial_agg(
                FirstLastAggregateFunctions.FIRST_N, col, Cast(time_term, "TIMESTAMP"), str(params.first_n.n)
            )
        ],
        full_aggregation_with_filter_query_term=lambda cols, filter_: _first_last_n_full_agg(
            FirstLastAggregateFunctions.FIRST_N,
            cols[0],
            time_term,
            str(params.first_n.n),
            _wrap_aggregation_in_filter(filter_),
        ),
        full_aggregation_default_value=LiteralValue("[]"),
        full_aggregation_query_term=lambda cols, query_window_spec, compat_funcs: _first_last_n_full_agg(
            FirstLastAggregateFunctions.FIRST_N,
            cols[0],
            time_term,
            str(params.first_n.n),
            lambda term: compat_funcs.over_window(term, query_window_spec),
        ),
        materialized_column_prefixes=get_materialization_aggregation_column_prefixes(
            afpb.AGGREGATION_FUNCTION_FIRST_NON_DISTINCT_N,
            function_params=params,
            is_continuous=is_continuous,
        ),
        continuous_aggregation_query_terms=lambda col: [Array(Field(col))],
        supported_dialects=[Dialect.DUCKDB],
    ),
    afpb.AGGREGATION_FUNCTION_LAST_NON_DISTINCT_N: lambda time_term, params, is_continuous: AggregationPlan(
        partial_aggregation_query_terms=lambda col: [
            ListReverse(
                _first_last_n_partial_agg(
                    FirstLastAggregateFunctions.LAST_N, col, Cast(time_term, "TIMESTAMP"), str(params.last_n.n)
                )
            )
        ],
        full_aggregation_with_filter_query_term=lambda cols, filter_: _first_last_n_full_agg(
            FirstLastAggregateFunctions.LAST_N,
            cols[0],
            time_term,
            str(params.last_n.n),
            _wrap_aggregation_in_filter(filter_),
        ),
        full_aggregation_default_value=LiteralValue("[]"),
        full_aggregation_query_term=lambda cols, query_window_spec, compat_funcs: _first_last_n_full_agg(
            FirstLastAggregateFunctions.LAST_N,
            cols[0],
            time_term,
            str(params.last_n.n),
            lambda term: compat_funcs.over_window(term, query_window_spec),
        ),
        materialized_column_prefixes=get_materialization_aggregation_column_prefixes(
            afpb.AGGREGATION_FUNCTION_LAST_NON_DISTINCT_N,
            function_params=params,
            is_continuous=is_continuous,
        ),
        continuous_aggregation_query_terms=lambda col: [Array(Field(col))],
        supported_dialects=[Dialect.DUCKDB],
    ),
    afpb.AGGREGATION_FUNCTION_FIRST_DISTINCT_N: lambda time_term, params, is_continuous: AggregationPlan(
        partial_aggregation_query_terms=lambda col: [
            _first_last_n_partial_agg(
                FirstLastAggregateFunctions.FIRST_DISTINCT_N, col, Cast(time_term, "TIMESTAMP"), str(params.first_n.n)
            )
        ],
        full_aggregation_with_filter_query_term=lambda cols, filter_: _first_last_distinct_n_full_agg(
            FirstLastAggregateFunctions.FIRST_DISTINCT_N,
            cols[0],
            time_term,
            str(params.first_n.n),
            _wrap_aggregation_in_filter(filter_),
        ),
        full_aggregation_default_value=LiteralValue("[]"),
        full_aggregation_query_term=lambda cols, query_window_spec, compat_funcs: _first_last_distinct_n_full_agg(
            FirstLastAggregateFunctions.FIRST_DISTINCT_N,
            cols[0],
            time_term,
            str(params.first_n.n),
            lambda term: compat_funcs.over_window(term, query_window_spec),
        ),
        materialized_column_prefixes=get_materialization_aggregation_column_prefixes(
            afpb.AGGREGATION_FUNCTION_FIRST_DISTINCT_N,
            function_params=params,
            is_continuous=is_continuous,
        ),
        continuous_aggregation_query_terms=lambda col: [Array(Field(col))],
        supported_dialects=[Dialect.DUCKDB],
    ),
    afpb.AGGREGATION_FUNCTION_LAST_DISTINCT_N: lambda time_term, params, is_continuous: AggregationPlan(
        partial_aggregation_query_terms=lambda col: [
            ListReverse(
                _first_last_n_partial_agg(
                    FirstLastAggregateFunctions.LAST_DISTINCT_N, col, Cast(time_term, "TIMESTAMP"), str(params.last_n.n)
                )
            )
        ],
        full_aggregation_with_filter_query_term=lambda cols, filter_: ListReverse(
            _first_last_distinct_n_full_agg(
                FirstLastAggregateFunctions.LAST_DISTINCT_N,
                cols[0],
                time_term,
                str(params.last_n.n),
                _wrap_aggregation_in_filter(filter_),
            )
        ),
        full_aggregation_default_value=LiteralValue("[]"),
        full_aggregation_query_term=lambda cols, query_window_spec, compat_funcs: ListReverse(
            _first_last_distinct_n_full_agg(
                FirstLastAggregateFunctions.LAST_DISTINCT_N,
                cols[0],
                time_term,
                str(params.last_n.n),
                lambda term: compat_funcs.over_window(term, query_window_spec),
            )
        ),
        materialized_column_prefixes=get_materialization_aggregation_column_prefixes(
            afpb.AGGREGATION_FUNCTION_LAST_DISTINCT_N,
            function_params=params,
            is_continuous=is_continuous,
        ),
        continuous_aggregation_query_terms=lambda col: [Array(Field(col))],
        supported_dialects=[Dialect.DUCKDB],
    ),
    afpb.AGGREGATION_FUNCTION_APPROX_COUNT_DISTINCT: lambda time_term, params, is_continuous: AggregationPlan(
        partial_aggregation_query_terms=lambda col: [
            # There's no way to unpack struct returned by the function completely (ie, struct.*) in the same select query.
            # (Alternatively we can run the function in the subquery).
            # Instead, we're calling ApproxCountDistinctPartial twice.
            # This will be optimized in DuckDB, which will run the function just once (inferred during debugging).
            StructExtract(
                ApproxCountDistinctPartial(Field(col), LiteralValue(str(params.approx_count_distinct.precision))),
                "indices",
            ),
            StructExtract(
                ApproxCountDistinctPartial(Field(col), LiteralValue(str(params.approx_count_distinct.precision))),
                "registers",
            ),
        ],
        full_aggregation_with_filter_query_term=lambda cols, filter_: FilterAggregationInput(
            ApproxCountDistinctCombine(
                Tuple(Cast(Field(cols[0]), "USMALLINT[]"), Cast(Field(cols[1]), "UTINYINT[]")),
                LiteralValue(str(params.approx_count_distinct.precision)),
            ),
            filter_,
        ),
        full_aggregation_query_term=lambda cols, query_window_spec, compat_funcs: compat_funcs.over_window(
            ApproxCountDistinctCombine(
                Tuple(Cast(Field(cols[0]), "USMALLINT[]"), Cast(Field(cols[1]), "UTINYINT[]")),
                LiteralValue(str(params.approx_count_distinct.precision)),
            ),
            query_window_spec,
        ),
        materialized_column_prefixes=get_materialization_aggregation_column_prefixes(
            afpb.AGGREGATION_FUNCTION_APPROX_COUNT_DISTINCT,
            function_params=params,
            is_continuous=is_continuous,
        ),
        continuous_aggregation_query_terms=lambda col: [
            StructExtract(
                ApproxCountDistinctContinuous(Field(col), LiteralValue(str(params.approx_count_distinct.precision))),
                "indices",
            ),
            StructExtract(
                ApproxCountDistinctContinuous(Field(col), LiteralValue(str(params.approx_count_distinct.precision))),
                "registers",
            ),
        ],
        full_aggregation_default_value=LiteralValue("0"),
        supported_dialects=[Dialect.DUCKDB],
    ),
    afpb.AGGREGATION_FUNCTION_LAST: lambda time_term, _, is_continuous: AggregationPlan(
        partial_aggregation_query_terms=lambda col: [Function("ARG_MAX", Field(col), time_term)],
        full_aggregation_with_filter_query_term=lambda cols, filter_: _wrap_aggregation_in_filter(filter_)(
            Function("ARG_MAX", Field(cols[0]), time_term)
        ),
        full_aggregation_query_term=lambda cols, query_window_spec, compat_funcs: get_simple_window_query(
            cols[0], query_window_spec, Last, compat_funcs, ignore_nulls=True
        ),
        materialized_column_prefixes=get_materialization_aggregation_column_prefixes(
            afpb.AGGREGATION_FUNCTION_LAST,
            function_params=None,
            is_continuous=is_continuous,
        ),
        continuous_aggregation_query_terms=lambda col: [Field(col)],
        supported_dialects=[Dialect.DUCKDB],
    ),
    afpb.AGGREGATION_FUNCTION_APPROX_PERCENTILE: lambda time_key, params, is_continuous: AggregationPlan(
        partial_aggregation_query_terms=lambda col: [
            StructExtract(
                ApproxQuantilePartial(Field(col), LiteralValue(str(params.approx_percentile.precision))),
                "means",
            ),
            StructExtract(
                ApproxQuantilePartial(Field(col), LiteralValue(str(params.approx_percentile.precision))),
                "weights",
            ),
        ],
        full_aggregation_with_filter_query_term=lambda cols, filter_: FilterAggregationInput(
            aggregation=ApproxQuantileCombine(
                Tuple(Field(cols[0]), Field(cols[1])),
                LiteralValue(str(params.approx_percentile.percentile)),
                LiteralValue(str(params.approx_percentile.precision)),
            ),
            filter_=filter_,
        ),
        full_aggregation_query_term=lambda cols, query_window_spec, compat_funcs: compat_funcs.over_window(
            ApproxQuantileCombine(
                Tuple(Field(cols[0]), Field(cols[1])),
                LiteralValue(str(params.approx_percentile.percentile)),
                LiteralValue(str(params.approx_percentile.precision)),
            ),
            query_window_spec,
        ),
        materialized_column_prefixes=get_materialization_aggregation_column_prefixes(
            afpb.AGGREGATION_FUNCTION_APPROX_PERCENTILE,
            function_params=params,
            is_continuous=is_continuous,
        ),
        continuous_aggregation_query_terms=lambda col: [Array(Field(col)), Array(LiteralValue("1.0"))],
        supported_dialects=[Dialect.DUCKDB],
    ),
}
