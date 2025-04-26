from dataclasses import dataclass
from typing import Callable
from typing import List

import pypika
from pypika import analytics
from pypika import functions
from pypika import terms

from tecton_core.aggregation_utils import get_materialization_aggregation_column_prefixes
from tecton_core.query import aggregation_plans
from tecton_proto.common import aggregation_function__client_pb2 as afpb
from tecton_snowflake.query import queries


@dataclass
class AggregationPlan:
    """
    An AggregationPlan contains all the methods required to compute feature values for a specific Tecton aggregation.
    Snowflake does not support RANGE BETWEEN on sliding window, so all the full aggregation terms and some of the partial aggregation terms are different from the tecton_core implementation.

    The order of the columns must be the same in:
    * the return list in partial_aggregation_query
    * the arguments list in full_aggregation_query
    * materialized_column_prefixes

    Attributes:
        full_aggregation_join_query_term: A method that maps a list of input partial aggregate columns and a QueryWindowSpec to an output pypika column containing the full aggregates.
        materialized_column_prefixes: The list of prefixes that should be applied to the columns produced by `partial_aggregation_transform`.
    """

    partial_aggregation_query_terms: Callable[[str], List[terms.Term]]
    full_aggregation_join_query_term: Callable[[List[str]], terms.Term]
    materialized_column_prefixes: List[str]

    def materialized_column_names(self, input_column_name: str) -> List[str]:
        return [f"{prefix}_{input_column_name}" for prefix in self.materialized_column_prefixes]


def get_aggregation_plan(
    aggregation_function: afpb.AggregationFunction,
    function_params: afpb.AggregationFunctionParams,
    time_key: str,
) -> AggregationPlan:
    plan = _SNOWFLAKE_AGGREGATION_PLANS.get(aggregation_function)
    if plan is None:
        msg = f"Unsupported aggregation function {aggregation_function}"
        raise ValueError(msg)

    if callable(plan):
        return plan(time_key, function_params)
    else:
        return plan


def _default_partial_aggregation_query_terms(
    function: afpb.AggregationFunction, input_column_name: str
) -> List[terms.Term]:
    return aggregation_plans.AGGREGATION_PLANS.get(function).partial_aggregation_query_terms(input_column_name)


def _simple_aggregation_plan(
    aggregation_function: afpb.AggregationFunction,
    row_function: terms.AggregateFunction,
):
    return AggregationPlan(
        partial_aggregation_query_terms=lambda col: _default_partial_aggregation_query_terms(aggregation_function, col),
        full_aggregation_join_query_term=lambda cols: row_function(pypika.Field(cols[0])),
        materialized_column_prefixes=get_materialization_aggregation_column_prefixes(aggregation_function),
    )


def _mean_full_aggregation_join(cols: List[str]):
    mean_col, count_col = cols
    sum_query_term = analytics.Sum(pypika.Field(mean_col) * pypika.Field(count_col))
    count_query_term = analytics.Sum(pypika.Field(count_col))
    return sum_query_term / count_query_term


# sample variation equation: (Σ(x^2) - (Σ(x)^2)/N)/N-1
def _var_samp_full_aggregation_join(cols: List[str]):
    sum_of_squares_col, count_col, sum_col = cols
    count_query_term = functions.Cast(analytics.Sum(pypika.Field(count_col)), "double")
    sum_of_squares_query_term = functions.Cast(analytics.Sum(pypika.Field(sum_of_squares_col)), "double")
    sum_query_term = functions.Cast(analytics.Sum(pypika.Field(sum_col)), "double")
    # check if count is equal to 0 for divide by 0 errors
    var_samp_col = (sum_of_squares_query_term - (sum_query_term**2) / count_query_term) / functions.NullIf(
        count_query_term - 1, 0
    )
    return var_samp_col


def _var_pop_full_aggregation_join(cols: List[str]):
    sum_of_squares_col, count_col, sum_col = cols
    count_query_term = functions.Cast(analytics.Sum(pypika.Field(count_col)), "double")
    sum_of_squares_query_term = functions.Cast(analytics.Sum(pypika.Field(sum_of_squares_col)), "double")
    sum_query_term = functions.Cast(analytics.Sum(pypika.Field(sum_col)), "double")
    return (sum_of_squares_query_term / count_query_term) - (sum_query_term / count_query_term) ** 2


def _stddev_samp_full_aggregation_join(cols: List[str]):
    return functions.Sqrt(_var_samp_full_aggregation_join(cols))


def _stddev_pop_full_aggregation_join(cols: List[str]):
    return functions.Sqrt(_var_pop_full_aggregation_join(cols))


def _mean_aggregation_plan():
    return AggregationPlan(
        partial_aggregation_query_terms=lambda col: _default_partial_aggregation_query_terms(
            afpb.AGGREGATION_FUNCTION_MEAN, col
        ),
        full_aggregation_join_query_term=lambda cols: _mean_full_aggregation_join(cols),
        materialized_column_prefixes=get_materialization_aggregation_column_prefixes(afpb.AGGREGATION_FUNCTION_MEAN),
    )


def _make_last_non_distinct_n_partial_aggregation(time_key: str, n: int) -> Callable:
    def last_non_distinct_n_partial_aggregation(col: str) -> List[terms.Term]:
        # Sort items in ascending order based on timestamp.
        return [queries.ArraySlice(queries.ArrayAggWithinGroup(col, time_key), 0, n)]

    return last_non_distinct_n_partial_aggregation


def _make_first_non_distinct_n_partial_aggregation(time_key: str, n: int) -> Callable:
    def first_non_distinct_n_partial_aggregation(col: str) -> List[terms.Term]:
        # Sort items in ascending order based on timestamp.
        return [
            queries.ArraySlice(queries.ArrayAggWithinGroup(col, time_key), -n, queries.ArraySize(queries.ArrayAgg(col)))
        ]

    return first_non_distinct_n_partial_aggregation


def _make_last_non_distinct_n_full_aggregation(time_key: str, n: int) -> Callable:
    def _last_non_distinct_n_full_aggregation(cols: List[str]) -> terms.Term:
        return queries.ArraySlice(
            queries.ArrayAggWithinGroup("VALUE", f"{time_key}, INDEX"), -n, queries.ArraySize(queries.ArrayAgg(cols[0]))
        )

    return _last_non_distinct_n_full_aggregation


def _make_first_non_distinct_n_full_aggregation(time_key: str, n: int) -> Callable:
    def _first_non_distinct_n_full_aggregation(cols: List[str]) -> terms.Term:
        return queries.ArraySlice(queries.ArrayAggWithinGroup("VALUE", f"{time_key}, INDEX"), 0, n)

    return _first_non_distinct_n_full_aggregation


_SNOWFLAKE_AGGREGATION_PLANS = {
    afpb.AGGREGATION_FUNCTION_SUM: _simple_aggregation_plan(afpb.AGGREGATION_FUNCTION_SUM, functions.Sum),
    afpb.AGGREGATION_FUNCTION_MIN: _simple_aggregation_plan(afpb.AGGREGATION_FUNCTION_MIN, functions.Min),
    afpb.AGGREGATION_FUNCTION_MAX: _simple_aggregation_plan(afpb.AGGREGATION_FUNCTION_MAX, functions.Max),
    afpb.AGGREGATION_FUNCTION_COUNT: AggregationPlan(
        partial_aggregation_query_terms=lambda col: _default_partial_aggregation_query_terms(
            afpb.AGGREGATION_FUNCTION_COUNT, col
        ),
        full_aggregation_join_query_term=lambda cols: functions.Sum(pypika.Field(cols[0])),
        materialized_column_prefixes=get_materialization_aggregation_column_prefixes(afpb.AGGREGATION_FUNCTION_COUNT),
    ),
    afpb.AGGREGATION_FUNCTION_MEAN: _mean_aggregation_plan(),
    afpb.AGGREGATION_FUNCTION_VAR_SAMP: AggregationPlan(
        partial_aggregation_query_terms=lambda col: _default_partial_aggregation_query_terms(
            afpb.AGGREGATION_FUNCTION_VAR_SAMP, col
        ),
        full_aggregation_join_query_term=lambda cols: _var_samp_full_aggregation_join(cols),
        materialized_column_prefixes=get_materialization_aggregation_column_prefixes(
            afpb.AGGREGATION_FUNCTION_VAR_SAMP
        ),
    ),
    afpb.AGGREGATION_FUNCTION_VAR_POP: AggregationPlan(
        partial_aggregation_query_terms=lambda col: _default_partial_aggregation_query_terms(
            afpb.AGGREGATION_FUNCTION_VAR_POP, col
        ),
        full_aggregation_join_query_term=lambda cols: _var_pop_full_aggregation_join(cols),
        materialized_column_prefixes=get_materialization_aggregation_column_prefixes(afpb.AGGREGATION_FUNCTION_VAR_POP),
    ),
    afpb.AGGREGATION_FUNCTION_STDDEV_SAMP: AggregationPlan(
        partial_aggregation_query_terms=lambda col: _default_partial_aggregation_query_terms(
            afpb.AGGREGATION_FUNCTION_STDDEV_SAMP, col
        ),
        full_aggregation_join_query_term=lambda cols: _stddev_samp_full_aggregation_join(cols),
        materialized_column_prefixes=get_materialization_aggregation_column_prefixes(
            afpb.AGGREGATION_FUNCTION_STDDEV_SAMP
        ),
    ),
    afpb.AGGREGATION_FUNCTION_STDDEV_POP: AggregationPlan(
        partial_aggregation_query_terms=lambda col: _default_partial_aggregation_query_terms(
            afpb.AGGREGATION_FUNCTION_STDDEV_POP, col
        ),
        full_aggregation_join_query_term=lambda cols: _stddev_pop_full_aggregation_join(cols),
        materialized_column_prefixes=get_materialization_aggregation_column_prefixes(
            afpb.AGGREGATION_FUNCTION_STDDEV_POP
        ),
    ),
    afpb.AGGREGATION_FUNCTION_FIRST_NON_DISTINCT_N: lambda time_key, params: AggregationPlan(
        partial_aggregation_query_terms=_make_first_non_distinct_n_partial_aggregation(time_key, params.first_n.n),
        full_aggregation_join_query_term=_make_first_non_distinct_n_full_aggregation(time_key, params.first_n.n),
        materialized_column_prefixes=get_materialization_aggregation_column_prefixes(
            afpb.AGGREGATION_FUNCTION_FIRST_NON_DISTINCT_N, function_params=params
        ),
    ),
    afpb.AGGREGATION_FUNCTION_LAST_NON_DISTINCT_N: lambda time_key, params: AggregationPlan(
        partial_aggregation_query_terms=_make_last_non_distinct_n_partial_aggregation(time_key, params.last_n.n),
        full_aggregation_join_query_term=_make_last_non_distinct_n_full_aggregation(time_key, params.last_n.n),
        materialized_column_prefixes=get_materialization_aggregation_column_prefixes(
            afpb.AGGREGATION_FUNCTION_LAST_NON_DISTINCT_N, function_params=params
        ),
    ),
}
