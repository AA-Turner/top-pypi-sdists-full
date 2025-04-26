from typing import Callable
from typing import List
from typing import Optional
from typing import Union

import attrs
import pyspark.sql.functions as F
from pyspark import SparkContext
from pyspark.sql import Column
from pyspark.sql import WindowSpec
from pyspark.sql import functions
from pyspark.sql.functions import expr

from tecton_core.aggregation_utils import get_materialization_aggregation_column_prefixes
from tecton_core.data_types import DataType
from tecton_core.data_types import Int64Type
from tecton_core.data_types import StringType
from tecton_proto.common import aggregation_function__client_pb2 as afpb
from tecton_spark.jars.class_loader import get_or_create_udf_jar_class_loader


# WARNING: If you're changing this class there's a good chance you need to change
# AggregationPlans.kt. Please look over that file carefully.


@attrs.define(auto_attribs=True)
class AggregationPlan(object):
    """
    An AggregationPlan contains all the methods required to compute feature values for a specific Tecton aggregation.

    Partial aggregates are returned as a list of pyspark columns. A single column is insufficient since certain
    aggregations require multiple intermediate columns. For example, the mean aggregation needs sum and count columns.

    Full aggregates use the partial aggregate columns as inputs and are returned as a single pyspark column.

    The order of the columns must be the same in:
    * the return list in partial_aggregation_transform
    * the return list in continuous_partial_aggregation_transform
    * the arguments list in full_aggregation_transform
    * materialized_column_prefixes

    Similarly, if there exists a partial_aggregation_preprocessor, the order of the columns must be the same in:
    * the output columns of partial_aggregation_preprocessor
    * the input columns to partial_aggregation_transform
    * intermediate_column_prefixes

    Attributes:
        partial_aggregation_transform: A method that maps a list of input column names to a list of output pyspark columns containing the partial aggregates.
        continuous_partial_aggregation_transform: Maps a list of input column names to a list of output pyspark columns.
        full_aggregation_transform: A method that maps a list of input partial aggregate columns and a WindowSpec to an output pyspark column containing the full aggregates.
        reduce_partial_aggregation_transform: A method that maps a list of input partial aggregate columns and a WindowSpec to output pyspark columns containing the partial aggregate columns aggregated over the window.
        materialized_column_prefixes: The list of prefixes that should be applied to the pyspark columns produced by `partial_aggregation_transform`.
            containing the partial aggregates for continuous mode.
        partial_aggregation_preprocessor: Creates intermediate columns to be used by the partial_aggregation_transform.
            This should only be necessary when the partial aggregation computation needs to be split across pyspark and
            a UDAF, as is the case for the approx count distinct aggregation. If it exists, it is applied in both
            continuous and non-continuous mode.
        intermediate_column_prefixes: The list of prefixes that should be applied to the pyspark columns produced by `partial_aggregation_preprocessor`.
    """

    partial_aggregation_transform: Callable[[List[str]], List[Column]]
    continuous_partial_aggregation_transform: Callable[[List[str]], List[Column]]
    full_aggregation_transform: Callable[[List[str], WindowSpec], Column]
    reduce_partial_aggregation_transform: Callable[[List[str], WindowSpec], List[Column]]
    materialized_column_prefixes: List[str]
    partial_aggregation_preprocessor: Optional[Callable[[str], List[Column]]] = None
    intermediate_column_prefixes: Optional[List[str]] = None

    def materialized_column_names(self, input_column_name: str) -> List[str]:
        return [f"{prefix}_{input_column_name}" for prefix in self.materialized_column_prefixes]

    def intermediate_column_names(self, input_column_name: str) -> List[str]:
        return [f"{prefix}_{input_column_name}" for prefix in self.intermediate_column_prefixes]


def get_aggregation_plan(
    aggregation_function: afpb.AggregationFunction,
    function_params: afpb.AggregationFunctionParams,
    is_continuous: bool,
    time_key: str,
    col_datatype: DataType = None,
) -> AggregationPlan:
    plan = AGGREGATION_PLANS.get(aggregation_function, None)
    if plan is None:
        msg = f"Unsupported aggregation function {aggregation_function}"
        raise ValueError(msg)

    if callable(plan):
        return plan(time_key, function_params, is_continuous, col_datatype)
    else:
        return plan


def _simple_partial_aggregation_transform(spark_transform):
    return lambda cols: [spark_transform(cols[0])]


def _simple_continuous_partial_aggregation_transform():
    return lambda cols: [F.col(cols[0])]


def _simple_full_aggregation_transform(spark_transform):
    return lambda cols, window: spark_transform(cols[0]).over(window)


def _simple_partial_aggregation_transform_for_window(spark_transform):
    return lambda cols, window: [spark_transform(cols[0]).over(window)]


def _simple_aggregation_plan(
    aggregation_function: afpb.AggregationFunction, spark_transform: Callable[[Union[Column, str]], Column]
) -> AggregationPlan:
    return AggregationPlan(
        partial_aggregation_transform=_simple_partial_aggregation_transform(spark_transform),
        continuous_partial_aggregation_transform=_simple_continuous_partial_aggregation_transform(),
        full_aggregation_transform=_simple_full_aggregation_transform(spark_transform),
        materialized_column_prefixes=get_materialization_aggregation_column_prefixes(aggregation_function),
        reduce_partial_aggregation_transform=_simple_partial_aggregation_transform_for_window(spark_transform),
    )


def ApproxPercentilePartialAgg(col: str, precision: int) -> List[Column]:
    sc = SparkContext._active_spark_context
    udf_name = f"tecton_approx_percentile_partial_{precision}"
    get_or_create_udf_jar_class_loader().load_class(
        sc, "com.tecton.udfs.spark3.ApproxPercentilePartialRegister"
    ).newInstance().register(udf_name, precision)
    columns = expr(f"{udf_name}({col})")
    return [columns.processedMeans, columns.processedWeights]


def _make_approx_percentile_partial_aggregation(precision: int) -> Callable[[List[str]], List[Column]]:
    def _approx_percentile_partial_aggregation(cols: List[str]) -> List[Column]:
        return ApproxPercentilePartialAgg(cols[0], precision)

    return _approx_percentile_partial_aggregation


def ApproxPercentileFullAgg(
    processed_means: str,
    processed_weights: str,
    percentile: float,
    precision: int,
) -> Column:
    sc = SparkContext._active_spark_context
    percentile_str = str(percentile).replace(".", "_")
    udf_name = f"tecton_approx_percentile_full_{percentile_str}"
    get_or_create_udf_jar_class_loader().load_class(
        sc, "com.tecton.udfs.spark3.ApproxPercentileFullRegister"
    ).newInstance().register(udf_name, precision, percentile)
    return expr(f"{udf_name}({processed_means}, {processed_weights})")


def _make_approx_percentile_full_aggregation(percentile: float, precision: int) -> Callable[[List[str]], WindowSpec]:
    def _approx_percentile_full_aggregation(cols: List[str], window: WindowSpec) -> Column:
        processed_means, processed_weights = cols
        return (
            ApproxPercentileFullAgg(processed_means, processed_weights, percentile, precision).over(window).percentile
        )

    return _approx_percentile_full_aggregation


def _make_approx_percentile_continuous_partial() -> Callable[[List[str]], List[Column]]:
    def _approx_percentile_continuous_partial(cols: List[str]) -> List[Column]:
        input_col = F.col(cols[0])

        # The partial aggregate tiles for approx_percentile do not allow nulls, so we replace nulls with NaNs, which will be filtered out of the eventual result.
        mean_col = F.when(input_col.isNull(), F.lit(float("nan"))).otherwise(input_col)
        return [F.array(mean_col), F.array(F.lit(1.0))]

    return _approx_percentile_continuous_partial


def ApproxCountDistinctFullAgg(indices: str, registers: str, precision: int) -> Column:
    sc = SparkContext._active_spark_context
    udf_name = "tecton_approx_count_distinct_full"
    get_or_create_udf_jar_class_loader().load_class(
        sc, "com.tecton.udfs.spark3.ApproxCountDistinctFullRegister"
    ).newInstance().register(udf_name, precision)
    return expr(f"{udf_name}({indices}, {registers})")


def _make_approx_count_distinct_full_aggregation(precision: int) -> Callable:
    def _approx_count_distinct_full_aggregation(cols: List[str], window: WindowSpec) -> Column:
        indices, registers = cols[0], cols[1]
        return ApproxCountDistinctFullAgg(indices, registers, precision).over(window).count

    return _approx_count_distinct_full_aggregation


def ApproxCountDistinctPartialAgg(index: str, register: str) -> List[Column]:
    sc = SparkContext._active_spark_context
    udf_name = "tecton_approx_count_distinct_partial"
    get_or_create_udf_jar_class_loader().load_class(
        sc, "com.tecton.udfs.spark3.ApproxCountDistinctPartialRegister"
    ).newInstance().register(udf_name)
    columns = expr(f"{udf_name}({index}, {register})")
    return [columns.indices, columns.registers]


def _make_approx_count_distinct_partial_aggregation() -> Callable[[List[str]], Column]:
    def _approx_count_distinct_partial_aggregation(cols: List[str]) -> List[Column]:
        index, register = cols[0], cols[1]
        return ApproxCountDistinctPartialAgg(index, register)

    return _approx_count_distinct_partial_aggregation


def _make_approx_count_distinct_partial_aggregation_helper(precision: int) -> Callable[[str], List[Column]]:
    def _add_index_and_register_column(input_column: str) -> List[Column]:
        """Computes the index and register values and returns them as bigint columns.

        The input column is first hashed with the SHA256 hash function and truncated to 64 bits. Then:
        * The index is the first 'precision' bits of the hash.
        * The register value is 1 + (number of leading zeros in the final 64 - 'precision' bits of the hash).

        For example, if the the input column has an entry "foo" and the precision is 8:
        * The SHA256 hash is '2c26b46b68ffc68ff99b453c1d30413413422d706483bfa0f98a5e886266e7ae'.
        * The first 64 bits are '2c26b46b68ffc68f', or '0010110000100110101101000110101101101000111111111100011010001111' in binary.
        * The first 8 bits are '00101100', or 44 in decimal. This is the index.
        * The last 56 bits are '00100110101101000110101101101000111111111100011010001111'. The register value is 3.
        """
        # The input column must be cast since the pyspark sha256 function only operates on binary columns.
        c = F.col(input_column).cast("binary")
        c = F.sha2(c, 256)

        # Take first 16 hex characters. The pyspark substring method is 1-indexed.
        c = F.substring(c, 1, 16)

        # Convert the hex string to binary. This operation is done as if the input column represented an integer, so
        # the resulting column might not contain 64 bits.
        c = F.conv(c, 16, 2)

        # Left pad the binary string with 0s to 64 characters, since the column might not have 64 bits.
        c = F.lpad(c, 64, "0")

        # Take the first 'precision' bits of the hash, convert to decimal, and cast to bigint.
        index = F.substring(c, 1, precision)
        index = F.conv(index, 2, 10).cast("bigint")

        # Take the final 64 - 'precision' bits of the hash. Then find the index of the first instance of '1' in the
        # column. The index starts at 1, so we do not need to modify it.
        register = F.substring(c, precision + 1, 64)
        register = F.instr(register, "1").cast("bigint")

        return [index, register]

    def _approx_count_distinct_partial_aggregation_helper(col: str) -> List[Column]:
        return _add_index_and_register_column(col)

    return _approx_count_distinct_partial_aggregation_helper


def _mean_partial_aggregation_for_window(cols: List[str], window: WindowSpec) -> List[Column]:
    mean_col, count_col = cols
    return [_mean_full_aggregation(cols, window), functions.sum(count_col).over(window)]


def _mean_full_aggregation(cols: List[str], window: WindowSpec) -> Column:
    # Window aggregation doesn't work with more than one built-in function like this
    #   sum(mean_clicked * count_clicked) / sum(count_clicked)
    # And it does not support UDFs on bounded windows (the kind we use)
    #   https://issues.apache.org/jira/browse/SPARK-22239
    # We work around this limitations by calculating ratio over two window aggregations
    mean_col, count_col = cols
    return functions.sum(functions.col(mean_col) * functions.col(count_col)).over(window) / functions.sum(
        count_col
    ).over(window)


# Partial aggregator used by first distinct N.
def FirstNAgg(timestamp: str, col: str, n: int, col_datatype: DataType) -> Column:
    sc = SparkContext._active_spark_context
    udf_name = f"tecton_{repr(col_datatype).lower()}_first_distinct_{n}_partial_aggregation"
    if col_datatype == StringType():
        get_or_create_udf_jar_class_loader().load_class(
            sc, "com.tecton.udfs.spark3.FirstNRegister"
        ).newInstance().register(n, udf_name, True)
    elif col_datatype == Int64Type():
        get_or_create_udf_jar_class_loader().load_class(
            sc, "com.tecton.udfs.spark3.FirstDistinctNRegisterForLongType"
        ).newInstance().register(n, udf_name)
    else:
        msg = f"Unsupported data type {col_datatype} for column {col} for first/last distinct aggregation."
        raise ValueError(msg)
    return expr(f"{udf_name}({timestamp},{col}).values")


def _make_first_distinct_n_partial_aggregation(time_key: str, n: int, col_datatype: DataType) -> Callable:
    def _first_distinct_n_partial_aggregation(cols: List[str]) -> List[Column]:
        return [FirstNAgg(time_key, cols[0], n, col_datatype)]

    return _first_distinct_n_partial_aggregation


# Partial aggregator used by last distinct N.
def LastDistinctNAgg(col1: str, col2: str, n: int, col_datatype: DataType) -> Column:
    sc = SparkContext._active_spark_context
    udf_name = f"tecton_{repr(col_datatype).lower()}_last_distinct_{n}_partial_aggregation"
    if col_datatype == StringType():
        get_or_create_udf_jar_class_loader().load_class(
            sc, "com.tecton.udfs.spark3.LastNRegister"
        ).newInstance().register(n, udf_name, True)
    elif col_datatype == Int64Type():
        get_or_create_udf_jar_class_loader().load_class(
            sc, "com.tecton.udfs.spark3.LastDistinctNRegisterForLongType"
        ).newInstance().register(n, udf_name)
    else:
        msg = f"Unsupported data type {col_datatype} for column {col1} for first/last distinct aggregation."
        raise ValueError(msg)
    return expr(f"{udf_name}({col1}, {col2}).values")


def _make_last_distinct_n_partial_aggregation(
    time_key: str, n: int, col_datatype: DataType
) -> Callable[[List[str]], List[Column]]:
    def _last_distinct_n_partial_aggregation(cols: List[str]) -> List[Column]:
        return [LastDistinctNAgg(time_key, cols[0], n, col_datatype)]

    return _last_distinct_n_partial_aggregation


def _make_first_and_last_n_continuous_partial() -> Callable[[List[str]], List[Column]]:
    def _first_and_last_n_continuous_partial(cols: List[str]) -> List[Column]:
        return [F.array(F.col(cols[0]))]

    return _first_and_last_n_continuous_partial


# Full aggregator used by both last and first distinct N.
def LimitedListConcatAgg(col1: str, n: int, keep_last_items: bool, col_datatype: Optional[DataType]) -> Column:
    sc = SparkContext._active_spark_context
    udf_name = (
        f"tecton_{repr(col_datatype).lower()}_last_distinct_{n}_full_aggregation"
        if keep_last_items
        else f"tecton_{repr(col_datatype).lower()}_first_distinct_{n}_full_aggregation"
    )

    if col_datatype == StringType():
        get_or_create_udf_jar_class_loader().load_class(
            sc, "com.tecton.udfs.spark3.LimitedListConcatRegister"
        ).newInstance().register(n, udf_name, keep_last_items)
    elif col_datatype == Int64Type():
        get_or_create_udf_jar_class_loader().load_class(
            sc, "com.tecton.udfs.spark3.LimitedListConcatRegisterForLongType"
        ).newInstance().register(n, udf_name, keep_last_items)
    else:
        msg = f"Unsupported data type {col_datatype} for column {col1} for first/last distinct aggregation."
        raise ValueError(msg)
    return expr(f"{udf_name}({col1})")


def _make_fixed_size_n_full_aggregation(
    n: int, keep_last_items: bool, col_datatype: Optional[DataType]
) -> Callable[[List[str], WindowSpec], Column]:
    def _fixed_size_n_full_aggregation(column_name: List[str], window: WindowSpec) -> Column:
        col = (LimitedListConcatAgg(column_name[0], n, keep_last_items, col_datatype).over(window)).values
        return col

    return _fixed_size_n_full_aggregation


def _make_fixed_size_n_intermediate_partial_aggregation(
    n: int, keep_last_items: bool, col_datatype: Optional[DataType]
) -> Callable[[List[str], WindowSpec], List[Column]]:
    def _fixed_size_n_intermediate_partial_aggregation(columns: List[str], window: WindowSpec) -> List[Column]:
        col = (LimitedListConcatAgg(columns[0], n, keep_last_items, col_datatype).over(window)).values
        return [col]

    return _fixed_size_n_intermediate_partial_aggregation


# Full aggregator used by last non-distinct N.
def _make_last_non_distinct_n_full_aggregation(n: int) -> Callable[[List[str], WindowSpec], Column]:
    def _last_non_distinct_n_full_aggregation(cols: List[str], window: WindowSpec) -> Column:
        return functions.reverse(
            functions.slice(functions.reverse(functions.flatten(functions.collect_list(cols[0]).over(window))), 1, n)
        )

    return _last_non_distinct_n_full_aggregation


def _make_last_non_distinct_n_intermediate_partial_aggregation(
    n: int,
) -> Callable[[List[str], WindowSpec], List[Column]]:
    def _last_non_distinct_n_intermediate_partial_aggregation(cols: List[str], window: WindowSpec) -> List[Column]:
        return [
            functions.reverse(
                functions.slice(
                    functions.reverse(functions.flatten(functions.collect_list(cols[0]).over(window))), 1, n
                )
            )
        ]

    return _last_non_distinct_n_intermediate_partial_aggregation


# Full aggregator used by first non-distinct N.
def _make_first_non_distinct_n_full_aggregation(n: int) -> Callable[[List[str], WindowSpec], Column]:
    def _first_non_distinct_n_full_aggregation(cols: List[Column], window: WindowSpec) -> Column:
        return functions.slice(functions.flatten(functions.collect_list(cols[0]).over(window)), 1, n)

    return _first_non_distinct_n_full_aggregation


def _make_first_non_distinct_n_intermediate_partial_aggregation(
    n: int,
) -> Callable[[List[str], WindowSpec], List[Column]]:
    def _first_non_distinct_n_intermediate_partial_aggregation(cols: List[Column], window: WindowSpec) -> List[Column]:
        return [functions.slice(functions.flatten(functions.collect_list(cols[0]).over(window)), 1, n)]

    return _first_non_distinct_n_intermediate_partial_aggregation


# Partial aggregator used by last non-distinct N.
def _make_last_non_distinct_n_partial_aggregation(time_key: str, n: int) -> Callable[[List[str]], List[Column]]:
    def last_non_distinct_n_partial_aggregation(cols: List[str]) -> List[Column]:
        # Sort items in descending order based on timestamp.
        col = cols[0]
        sort_function = f"(left, right) -> case when left.{time_key} < right.{time_key} then 1 when left.{time_key} > right.{time_key} then -1 else 0 end)"
        return [
            functions.reverse(
                functions.slice(
                    functions.expr(f"array_sort(collect_list(struct({col}, {time_key})), {sort_function}"),
                    1,
                    n,
                ).getItem(col)
            )
        ]

    return last_non_distinct_n_partial_aggregation


# Partial aggregator used by last N.
def _make_last_partial_aggregation(time_key: str) -> Callable[[List[str]], List[Column]]:
    def last_partial_aggregation(cols: List[str]) -> List[Column]:
        # Sort items in descending order based on timestamp.
        col = cols[0]
        filter_condition = f" x -> x.{col} IS NOT NULL"
        sort_function = f"(left, right) -> case when left.{time_key} < right.{time_key} then 1 when left.{time_key} > right.{time_key} then -1 else 0 end)"
        return [
            functions.expr(
                f"filter(array_sort(collect_list(struct({col}, {time_key})), {sort_function},{filter_condition})"
            )
            .getItem(0)
            .getItem(col)
        ]

    return last_partial_aggregation


# Partial aggregator used by first non-distinct N.
def _make_first_non_distinct_n_partial_aggregation(time_key: str, n: int) -> Callable[[List[str]], List[Column]]:
    def first_non_distinct_n_partial_aggregation(cols: List[str]) -> List[Column]:
        # Sort items in ascending order based on timestamp.
        col = cols[0]
        sort_function = f"(left,right) -> case when left.{time_key} < right.{time_key} then -1 when left.{time_key} > right.{time_key} then 1 else 0 end)"
        return [
            functions.slice(
                functions.expr(f"array_sort(collect_list(struct({col}, {time_key})), {sort_function}"),
                1,
                n,
            ).getItem(col)
        ]

    return first_non_distinct_n_partial_aggregation


def _sum_with_default(columns: List[str], window: WindowSpec) -> Column:
    col = functions.sum(columns[0]).over(window)
    # Fill null
    col = functions.when(col.isNull(), functions.lit(0)).otherwise(col)
    return col


# population variation equation: Σ(x^2)/n - μ^2
def _var_pop_full_aggregation(cols: List[str], window: WindowSpec) -> Column:
    sum_of_squares_col, count_col, sum_col = cols
    return functions.sum(sum_of_squares_col).over(window) / functions.sum(count_col).over(window) - functions.pow(
        functions.sum(sum_col).over(window) / functions.sum(count_col).over(window), 2
    )


def _stddev_pop_full_aggregation(cols: List[str], window: WindowSpec) -> Column:
    return functions.sqrt(_var_pop_full_aggregation(cols, window))


# sample variation equation: (Σ(x^2) - (Σ(x)^2)/N)/N-1
def _var_samp_full_aggregation(cols: List[str], window: WindowSpec) -> Column:
    sum_of_squares_col, count_col, sum_col = cols
    total_count_col = functions.sum(count_col).over(window)
    # check if count is equal to 0 for divide by 0 errors
    var_samp_col = functions.when(
        total_count_col != 1,
        (
            functions.sum(sum_of_squares_col).over(window)
            - functions.pow(functions.sum(sum_col).over(window), 2) / total_count_col
        )
        / (total_count_col - functions.lit(1)),
    )
    return var_samp_col


def _stddev_samp_full_aggregation(cols: List[str], window: WindowSpec) -> Column:
    return functions.sqrt(_var_samp_full_aggregation(cols, window))


def _stddev_var_partial(col: List[str]) -> List[Column]:
    return [
        functions.sum(functions.pow(col, 2)),
        functions.count(col),
        functions.sum(functions.col(col)),
    ]


def _stddev_var_partial_for_window(cols: List[str], window: WindowSpec) -> List[Column]:
    sum_of_squares_col, count_col, sum_col = cols
    return [
        functions.sum(sum_of_squares_col).over(window),
        functions.sum(count_col).over(window),
        functions.sum(sum_col).over(window),
    ]


def _make_stddev_var_continuous_partial() -> Callable[[List[str]], List[Column]]:
    def _stddev_var_continuous_partial(cols: List[str]) -> List[Column]:
        col = cols[0]
        return [
            F.pow(col, 2),
            *_count_continuous_partial_aggregation([col]),
            F.col(col),
        ]

    return _stddev_var_continuous_partial


def _make_approx_count_distinct_continuous_partial() -> Callable[[List[str]], List[Column]]:
    def _approx_count_distinct_continuous_partial(cols: List[str]) -> List[Column]:
        index, register = cols[0], cols[1]
        return [
            F.when(F.col(index).isNull(), F.lit(None)).otherwise(F.array(F.col(index))),
            F.when(F.col(register).isNull(), F.lit(None)).otherwise(F.array(F.col(register))),
        ]

    return _approx_count_distinct_continuous_partial


def _count_continuous_partial_aggregation(cols: List[str]) -> List[Column]:
    return [F.when(F.col(cols[0]).isNull(), F.lit(0).cast("long")).otherwise(F.lit(1).cast("long"))]


def _mean_continuous_partial_aggregation(cols: List[str]) -> List[Column]:
    return [F.col(cols[0]).cast("double"), *_count_continuous_partial_aggregation([cols[0]])]


def _unsupported_reduce_partial_aggregation_transform(cols: List[str], window: WindowSpec) -> List[Column]:
    msg = "Reduce partial aggregation transform is not supported for this aggregation function type."
    raise NotImplementedError(msg)


_approx_count_distinct_intermediate_column_prefixes = ["approx_count_distinct_index", "approx_count_distinct_register"]

AGGREGATION_PLANS = {
    afpb.AGGREGATION_FUNCTION_SUM: _simple_aggregation_plan(afpb.AGGREGATION_FUNCTION_SUM, functions.sum),
    afpb.AGGREGATION_FUNCTION_MIN: _simple_aggregation_plan(afpb.AGGREGATION_FUNCTION_MIN, functions.min),
    afpb.AGGREGATION_FUNCTION_MAX: _simple_aggregation_plan(afpb.AGGREGATION_FUNCTION_MAX, functions.max),
    afpb.AGGREGATION_FUNCTION_LAST: lambda time_key, params, is_continuous, _: AggregationPlan(
        partial_aggregation_transform=_make_last_partial_aggregation(time_key),
        continuous_partial_aggregation_transform=_simple_continuous_partial_aggregation_transform(),
        full_aggregation_transform=_simple_full_aggregation_transform(
            lambda col: functions.last(col, ignorenulls=True)
        ),
        materialized_column_prefixes=get_materialization_aggregation_column_prefixes(afpb.AGGREGATION_FUNCTION_LAST),
        reduce_partial_aggregation_transform=_simple_partial_aggregation_transform_for_window(
            lambda col: functions.last(col, ignorenulls=True)
        ),
    ),
    # Needs to use COUNT for partial and SUM for full aggregation
    afpb.AGGREGATION_FUNCTION_COUNT: AggregationPlan(
        partial_aggregation_transform=_simple_partial_aggregation_transform(functions.count),
        continuous_partial_aggregation_transform=_count_continuous_partial_aggregation,
        full_aggregation_transform=_sum_with_default,
        materialized_column_prefixes=get_materialization_aggregation_column_prefixes(afpb.AGGREGATION_FUNCTION_COUNT),
        reduce_partial_aggregation_transform=_simple_partial_aggregation_transform_for_window(functions.sum),
    ),
    afpb.AGGREGATION_FUNCTION_MEAN: AggregationPlan(
        partial_aggregation_transform=lambda cols: [functions.mean(cols[0]), functions.count(cols[0])],
        continuous_partial_aggregation_transform=_mean_continuous_partial_aggregation,
        full_aggregation_transform=_mean_full_aggregation,
        materialized_column_prefixes=get_materialization_aggregation_column_prefixes(afpb.AGGREGATION_FUNCTION_MEAN),
        reduce_partial_aggregation_transform=_mean_partial_aggregation_for_window,
    ),
    afpb.AGGREGATION_FUNCTION_LAST_DISTINCT_N: lambda time_key, params, is_continuous, col_datatype: AggregationPlan(
        partial_aggregation_transform=_make_last_distinct_n_partial_aggregation(
            time_key, params.last_n.n, col_datatype
        ),
        continuous_partial_aggregation_transform=_make_first_and_last_n_continuous_partial(),
        full_aggregation_transform=_make_fixed_size_n_full_aggregation(params.last_n.n, True, col_datatype),
        materialized_column_prefixes=get_materialization_aggregation_column_prefixes(
            afpb.AGGREGATION_FUNCTION_LAST_DISTINCT_N, function_params=params, is_continuous=is_continuous
        ),
        reduce_partial_aggregation_transform=_make_fixed_size_n_intermediate_partial_aggregation(
            params.last_n.n, True, col_datatype
        ),
    ),
    afpb.AGGREGATION_FUNCTION_LAST_NON_DISTINCT_N: lambda time_key, params, is_continuous, _: AggregationPlan(
        partial_aggregation_transform=_make_last_non_distinct_n_partial_aggregation(time_key, params.last_n.n),
        continuous_partial_aggregation_transform=_make_first_and_last_n_continuous_partial(),
        full_aggregation_transform=_make_last_non_distinct_n_full_aggregation(params.last_n.n),
        materialized_column_prefixes=get_materialization_aggregation_column_prefixes(
            afpb.AGGREGATION_FUNCTION_LAST_NON_DISTINCT_N, function_params=params, is_continuous=is_continuous
        ),
        reduce_partial_aggregation_transform=_make_last_non_distinct_n_intermediate_partial_aggregation(
            params.last_n.n
        ),
    ),
    afpb.AGGREGATION_FUNCTION_VAR_POP: AggregationPlan(
        partial_aggregation_transform=lambda cols: _stddev_var_partial(cols[0]),
        continuous_partial_aggregation_transform=_make_stddev_var_continuous_partial(),
        full_aggregation_transform=_var_pop_full_aggregation,
        materialized_column_prefixes=get_materialization_aggregation_column_prefixes(afpb.AGGREGATION_FUNCTION_VAR_POP),
        reduce_partial_aggregation_transform=_stddev_var_partial_for_window,
    ),
    afpb.AGGREGATION_FUNCTION_STDDEV_POP: AggregationPlan(
        partial_aggregation_transform=lambda cols: _stddev_var_partial(cols[0]),
        continuous_partial_aggregation_transform=_make_stddev_var_continuous_partial(),
        full_aggregation_transform=_stddev_pop_full_aggregation,
        materialized_column_prefixes=get_materialization_aggregation_column_prefixes(
            afpb.AGGREGATION_FUNCTION_STDDEV_POP
        ),
        reduce_partial_aggregation_transform=_stddev_var_partial_for_window,
    ),
    afpb.AGGREGATION_FUNCTION_VAR_SAMP: AggregationPlan(
        partial_aggregation_transform=lambda cols: _stddev_var_partial(cols[0]),
        continuous_partial_aggregation_transform=_make_stddev_var_continuous_partial(),
        full_aggregation_transform=_var_samp_full_aggregation,
        materialized_column_prefixes=get_materialization_aggregation_column_prefixes(
            afpb.AGGREGATION_FUNCTION_VAR_SAMP
        ),
        reduce_partial_aggregation_transform=_stddev_var_partial_for_window,
    ),
    afpb.AGGREGATION_FUNCTION_STDDEV_SAMP: AggregationPlan(
        partial_aggregation_transform=lambda cols: _stddev_var_partial(cols[0]),
        continuous_partial_aggregation_transform=_make_stddev_var_continuous_partial(),
        full_aggregation_transform=_stddev_samp_full_aggregation,
        materialized_column_prefixes=get_materialization_aggregation_column_prefixes(
            afpb.AGGREGATION_FUNCTION_STDDEV_SAMP
        ),
        reduce_partial_aggregation_transform=_stddev_var_partial_for_window,
    ),
    afpb.AGGREGATION_FUNCTION_APPROX_COUNT_DISTINCT: lambda time_key, params, _, __: AggregationPlan(
        partial_aggregation_transform=_make_approx_count_distinct_partial_aggregation(),
        continuous_partial_aggregation_transform=_make_approx_count_distinct_continuous_partial(),
        full_aggregation_transform=_make_approx_count_distinct_full_aggregation(params.approx_count_distinct.precision),
        materialized_column_prefixes=get_materialization_aggregation_column_prefixes(
            afpb.AGGREGATION_FUNCTION_APPROX_COUNT_DISTINCT
        ),
        partial_aggregation_preprocessor=_make_approx_count_distinct_partial_aggregation_helper(
            params.approx_count_distinct.precision
        ),
        intermediate_column_prefixes=_approx_count_distinct_intermediate_column_prefixes,
        reduce_partial_aggregation_transform=_unsupported_reduce_partial_aggregation_transform,
    ),
    afpb.AGGREGATION_FUNCTION_APPROX_PERCENTILE: lambda time_key, params, _, __: AggregationPlan(
        partial_aggregation_transform=_make_approx_percentile_partial_aggregation(params.approx_percentile.precision),
        materialized_column_prefixes=get_materialization_aggregation_column_prefixes(
            afpb.AGGREGATION_FUNCTION_APPROX_PERCENTILE
        ),
        continuous_partial_aggregation_transform=_make_approx_percentile_continuous_partial(),
        full_aggregation_transform=_make_approx_percentile_full_aggregation(
            params.approx_percentile.percentile, params.approx_percentile.precision
        ),
        reduce_partial_aggregation_transform=_unsupported_reduce_partial_aggregation_transform,
    ),
    afpb.AGGREGATION_FUNCTION_FIRST_NON_DISTINCT_N: lambda time_key, params, is_continuous, _: AggregationPlan(
        partial_aggregation_transform=_make_first_non_distinct_n_partial_aggregation(time_key, params.first_n.n),
        continuous_partial_aggregation_transform=_make_first_and_last_n_continuous_partial(),
        full_aggregation_transform=_make_first_non_distinct_n_full_aggregation(params.first_n.n),
        materialized_column_prefixes=get_materialization_aggregation_column_prefixes(
            afpb.AGGREGATION_FUNCTION_FIRST_NON_DISTINCT_N, function_params=params, is_continuous=is_continuous
        ),
        reduce_partial_aggregation_transform=_make_first_non_distinct_n_intermediate_partial_aggregation(
            params.first_n.n
        ),
    ),
    afpb.AGGREGATION_FUNCTION_FIRST_DISTINCT_N: lambda time_key, params, is_continuous, col_datatype: AggregationPlan(
        partial_aggregation_transform=_make_first_distinct_n_partial_aggregation(
            time_key, params.first_n.n, col_datatype
        ),
        continuous_partial_aggregation_transform=_make_first_and_last_n_continuous_partial(),
        full_aggregation_transform=_make_fixed_size_n_full_aggregation(params.first_n.n, False, col_datatype),
        materialized_column_prefixes=get_materialization_aggregation_column_prefixes(
            afpb.AGGREGATION_FUNCTION_FIRST_DISTINCT_N, function_params=params, is_continuous=is_continuous
        ),
        reduce_partial_aggregation_transform=_make_fixed_size_n_intermediate_partial_aggregation(
            params.first_n.n, False, col_datatype
        ),
    ),
}
