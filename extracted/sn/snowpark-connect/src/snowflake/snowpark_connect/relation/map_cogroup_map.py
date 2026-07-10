#
# Copyright (c) 2012-2025 Snowflake Computing Inc. All rights reserved.
#

import pyspark.sql.connect.proto.expressions_pb2 as expressions_proto
import pyspark.sql.connect.proto.relations_pb2 as relation_proto

import snowflake.snowpark.functions as snowpark_fn
from snowflake import snowpark
from snowflake.snowpark.types import ArrayType, MapType, StructType, VariantType
from snowflake.snowpark_connect.config import get_artifact_repository, global_config
from snowflake.snowpark_connect.dataframe_container import DataFrameContainer
from snowflake.snowpark_connect.expression.map_expression import (
    map_single_column_expression,
)
from snowflake.snowpark_connect.expression.typer import ExpressionTyper
from snowflake.snowpark_connect.relation.output_struct_utils import (
    unpack_java_udtf_output_to_container,
)
from snowflake.snowpark_connect.type_mapping import proto_to_snowpark_type
from snowflake.snowpark_connect.utils.udf_helper import require_creating_udf_in_sproc
from snowflake.snowpark_connect.utils.udxf_import_utils import (
    get_python_udxf_import_files,
)
from snowflake.snowpark_connect.utils.variant_utils import jvm_udf_arg_to_variant

KEY_COL_PREFIX = "__SC_COGROUP_KEY_"
VALUE_COL_NAME = "__SC_COGROUP_VALUE__"
SOURCE_COL_NAME = "__SC_COGROUP_SOURCE__"
ROW_NUM_COL_NAME = "__SC_COGROUP_ROW_NUM__"


def _key_col_name(i: int) -> str:
    return f"{KEY_COL_PREFIX}{i}__"


def map_co_group_map(
    rel: relation_proto.Relation,
) -> DataFrameContainer:
    """
    Maps a function over co-grouped data from two DataFrames.

    Supports both Scala UDFs (cogroup) and Python UDFs (applyInPandas).
    Uses UNION ALL with source markers to combine both DataFrames, then applies
    a UDTF that separates rows by source and processes them together.
    """
    from snowflake.snowpark_connect.relation.map_relation import map_relation

    input_container = map_relation(rel.co_group_map.input)
    other_container = map_relation(rel.co_group_map.other)

    input_typer = ExpressionTyper(input_container.dataframe)
    other_typer = ExpressionTyper(other_container.dataframe)

    snowpark_input_grouping_exprs, input_group_names = _map_grouping_expressions(
        rel.co_group_map.input_grouping_expressions,
        input_container,
        input_typer,
    )

    snowpark_other_grouping_exprs, _ = _map_grouping_expressions(
        rel.co_group_map.other_grouping_expressions,
        other_container,
        other_typer,
    )

    if len(snowpark_input_grouping_exprs) != len(snowpark_other_grouping_exprs):
        raise ValueError(
            f"co_group_map requires the same number of grouping columns for each dataset. "
            f"Got {len(snowpark_input_grouping_exprs)} for input and "
            f"{len(snowpark_other_grouping_exprs)} for other."
        )

    func_proto = rel.co_group_map.func
    function_type = func_proto.WhichOneof("function")

    if function_type == "python_udf":
        return _map_co_group_map_python(
            func_proto,
            input_container,
            other_container,
            snowpark_input_grouping_exprs,
            snowpark_other_grouping_exprs,
            input_group_names=input_group_names,
        )

    if function_type == "scalar_scala_udf":
        return _map_co_group_map_scala(
            rel,
            func_proto,
            input_container,
            other_container,
            snowpark_input_grouping_exprs,
            snowpark_other_grouping_exprs,
            input_group_names,
            input_typer,
            other_typer,
        )

    raise NotImplementedError(
        f"Co-group map only supports scalar_scala_udf or python_udf, got {function_type}"
    )


def _map_grouping_expressions(
    grouping_expressions,
    container: DataFrameContainer,
    typer: ExpressionTyper,
) -> tuple[list[snowpark.Column], list[str]]:
    """Map grouping expressions to Snowpark columns and names."""
    from snowflake.snowpark_connect.utils.context import grouping_by_scala_udf_key

    snowpark_exprs: list[snowpark.Column] = []
    name_list: list[str] = []

    for exp in grouping_expressions:
        with grouping_by_scala_udf_key(
            exp.WhichOneof("expr_type") == "common_inline_user_defined_function"
            and exp.common_inline_user_defined_function.scalar_scala_udf is not None
        ):
            name, snowpark_column = map_single_column_expression(
                exp, container.column_map, typer
            )
        snowpark_exprs.append(snowpark_column.col)
        name_list.append(name)

    return snowpark_exprs, name_list


def _key_columns_select(
    grouping_exprs: list[snowpark.Column],
) -> list[snowpark.Column]:
    """Build aliased key columns for SELECT."""
    return [expr.alias(_key_col_name(i)) for i, expr in enumerate(grouping_exprs)]


def _key_columns_refs(num_keys: int) -> list[snowpark.Column]:
    """Get column references to key columns."""
    return [snowpark_fn.col(_key_col_name(i)) for i in range(num_keys)]


def _build_value_expression(
    container: DataFrameContainer,
    value_type_kind: str,
    expected_type=None,
    proto_type: StructType | None = None,
) -> snowpark.Column:
    """Build a value expression based on the value type, preserving nulls in arrays."""
    snowpark_cols = container.column_map.get_snowpark_columns()
    col_type_lookup = {f.name: f.datatype for f in container.dataframe.schema.fields}

    if value_type_kind == "struct":
        # Typed datasets (e.g. as[K, (String, Int)]) encode values with proto
        # field names (_1, _2) that the Java UDTF deserializer expects. Untyped
        # Row values have an empty proto struct, so we fall back to DataFrame
        # column names which the UDTF accesses via getAs("colName").
        if proto_type is not None and len(proto_type.fields) > 0:
            field_names = [f.name for f in proto_type.fields]
        else:
            field_names = container.column_map.get_spark_columns()
        expr = snowpark_fn.object_construct_keep_null(
            *[
                item
                for field_name, snowpark_name in zip(field_names, snowpark_cols)
                for item in (
                    snowpark_fn.lit(field_name),
                    jvm_udf_arg_to_variant(
                        snowpark_fn.col(snowpark_name),
                        col_type_lookup.get(snowpark_name, VariantType()),
                    ),
                )
            ]
        )
        return snowpark_fn.to_variant(expr)

    if value_type_kind in ("map", "array"):
        col_type = col_type_lookup.get(snowpark_cols[0], VariantType())
        return jvm_udf_arg_to_variant(snowpark_fn.col(snowpark_cols[0]), col_type)

    expr = snowpark_fn.col(snowpark_cols[0])
    return expr.cast(expected_type) if expected_type else expr


def _prepare_input_for_scala(
    container: DataFrameContainer,
    grouping_exprs: list[snowpark.Column],
    value_expr: snowpark.Column,
    source_marker: int,
    sorting_cols: list[snowpark.Column] | None,
) -> snowpark.DataFrame:
    """Prepare a DataFrame for Scala co-group with keys, value, source, and row number."""
    if sorting_cols:
        from snowflake.snowpark import Window

        window = Window.partition_by(*grouping_exprs).order_by(*sorting_cols)
        row_num_expr = snowpark_fn.row_number().over(window)
    else:
        row_num_expr = snowpark_fn.lit(0)

    return container.dataframe.select(
        *_key_columns_select(grouping_exprs),
        value_expr.alias(VALUE_COL_NAME),
        snowpark_fn.lit(source_marker).alias(SOURCE_COL_NAME),
        row_num_expr.alias(ROW_NUM_COL_NAME),
    )


def _prepare_input_for_python(
    container: DataFrameContainer,
    grouping_exprs: list[snowpark.Column],
    source_marker: int,
) -> snowpark.DataFrame:
    """Prepare a DataFrame for Python co-group with keys, value (as JSON), and source."""
    snowpark_cols = container.column_map.get_snowpark_columns()
    spark_names = container.column_map.get_spark_columns()

    value_expr = snowpark_fn.object_construct_keep_null(
        *[
            item
            for spark_name, snowpark_name in zip(spark_names, snowpark_cols)
            for item in (
                snowpark_fn.lit(spark_name),
                snowpark_fn.to_variant(snowpark_fn.col(snowpark_name)),
            )
        ]
    )

    return container.dataframe.select(
        *_key_columns_select(grouping_exprs),
        value_expr.alias(VALUE_COL_NAME),
        snowpark_fn.lit(source_marker).alias(SOURCE_COL_NAME),
    )


def _map_co_group_map_scala(
    rel: relation_proto.Relation,
    func_proto: expressions_proto.CommonInlineUserDefinedFunction,
    input_container: DataFrameContainer,
    other_container: DataFrameContainer,
    snowpark_input_grouping_exprs: list[snowpark.Column],
    snowpark_other_grouping_exprs: list[snowpark.Column],
    input_group_names: list[str],
    input_typer: ExpressionTyper,
    other_typer: ExpressionTyper,
) -> DataFrameContainer:
    """Handle co_group_map for Scala UDFs."""
    from snowflake.snowpark_connect.relation.map_column_ops import (
        _map_sorting_expressions,
    )
    from snowflake.snowpark_connect.utils.java_udtf_utils import (
        JAVA_UDTF_PREFIX,
        create_java_udtf_for_scala_co_group_map_handling,
    )

    udtf_name = create_java_udtf_for_scala_co_group_map_handling(func_proto)
    output_type = proto_to_snowpark_type(func_proto.scalar_scala_udf.outputType)

    input_types = func_proto.scalar_scala_udf.inputTypes
    assert (
        len(input_types) == 3
    ), "Co-group map function should have exactly 3 input types"

    key_expected_type = proto_to_snowpark_type(input_types[0])
    value1_type_kind = input_types[1].WhichOneof("kind")
    value2_type_kind = input_types[2].WhichOneof("kind")

    num_keys = len(snowpark_input_grouping_exprs)

    value1_proto_type = proto_to_snowpark_type(input_types[1])
    value2_proto_type = proto_to_snowpark_type(input_types[2])

    value1_expected = (
        value1_proto_type
        if value1_type_kind not in ("struct", "map", "array")
        else None
    )
    value2_expected = (
        value2_proto_type
        if value2_type_kind not in ("struct", "map", "array")
        else None
    )

    value1_expr = _build_value_expression(
        input_container,
        value1_type_kind,
        value1_expected,
        proto_type=value1_proto_type if value1_type_kind == "struct" else None,
    )
    value2_expr = _build_value_expression(
        other_container,
        value2_type_kind,
        value2_expected,
        proto_type=value2_proto_type if value2_type_kind == "struct" else None,
    )

    input_sorting_cols = _map_sorting_expressions(
        rel.co_group_map.input_sorting_expressions,
        input_container.column_map,
        input_typer,
    )
    other_sorting_cols = _map_sorting_expressions(
        rel.co_group_map.other_sorting_expressions,
        other_container.column_map,
        other_typer,
    )

    input_prepared = _prepare_input_for_scala(
        input_container,
        snowpark_input_grouping_exprs,
        value1_expr,
        1,
        input_sorting_cols,
    )
    other_prepared = _prepare_input_for_scala(
        other_container,
        snowpark_other_grouping_exprs,
        value2_expr,
        2,
        other_sorting_cols,
    )

    combined_df = input_prepared.union_all(other_prepared)

    order_by_arg = (
        [snowpark_fn.col(SOURCE_COL_NAME), snowpark_fn.col(ROW_NUM_COL_NAME)]
        if (input_sorting_cols or other_sorting_cols)
        else None
    )

    key_cols = _key_columns_refs(num_keys)

    # The Scala function signature is Function3[K, Iterator[V1], Iterator[V2], R] and
    # requires the key to be passed. For single-key grouping, we pass the column directly.
    # For multi-key grouping, we must construct a composite key using object_construct
    # because the Scala function expects a single key value (tuple/struct), not multiple
    # separate values.
    if num_keys == 1:
        if isinstance(key_expected_type, (ArrayType, MapType, StructType, VariantType)):
            key_for_udtf = snowpark_fn.to_variant(key_cols[0])
        else:
            key_for_udtf = key_cols[0].cast(key_expected_type)
    else:
        key_for_udtf = snowpark_fn.object_construct(
            *[
                item
                for name, col in zip(input_group_names, key_cols)
                for item in (snowpark_fn.lit(name), col)
            ]
        )

    tfc = snowpark_fn.call_table_function(
        udtf_name,
        key_for_udtf,
        snowpark_fn.col(VALUE_COL_NAME),
        snowpark_fn.col(SOURCE_COL_NAME),
    ).over(partition_by=key_cols, order_by=order_by_arg)

    result = combined_df.join_table_function(tfc)

    return unpack_java_udtf_output_to_container(
        df=result,
        output_type=output_type,
        non_struct_spark_name="value",
        java_udtf_prefix=JAVA_UDTF_PREFIX,
    )


def _map_co_group_map_python(
    func_proto: expressions_proto.CommonInlineUserDefinedFunction,
    input_container: DataFrameContainer,
    other_container: DataFrameContainer,
    snowpark_input_grouping_exprs: list[snowpark.Column],
    snowpark_other_grouping_exprs: list[snowpark.Column],
    input_group_names: list[str] | None = None,
) -> DataFrameContainer:
    """Handle co_group_map for Python UDFs (applyInPandas)."""
    from snowflake.snowpark_connect.utils.context import get_spark_session_id
    from snowflake.snowpark_connect.utils.pandas_udtf_utils import (
        create_cogroup_pandas_udtf,
    )
    from snowflake.snowpark_connect.utils.udtf_helper import (
        create_cogroup_udtf_in_sproc,
    )

    output_type = proto_to_snowpark_type(func_proto.python_udf.output_type)

    input1_spark_columns = input_container.column_map.get_spark_columns()
    input2_spark_columns = other_container.column_map.get_spark_columns()

    udtf_packages = global_config.get("snowpark.connect.udf.packages", "")
    udtf_imports = get_python_udxf_import_files(snowpark.Session.get_active_session())
    artifact_repository = get_artifact_repository()
    session_id = get_spark_session_id()

    grouping_column_names = input_group_names or []

    if require_creating_udf_in_sproc(func_proto):
        cogroup_udtf_name = create_cogroup_udtf_in_sproc(
            func_proto,
            input1_spark_columns,
            input2_spark_columns,
            output_type,
            udtf_packages,
            udtf_imports,
            artifact_repository=artifact_repository,
            session_id=session_id,
        )
    else:
        cogroup_udtf = create_cogroup_pandas_udtf(
            func_proto,
            input1_spark_columns,
            input2_spark_columns,
            output_type,
            udtf_packages,
            udtf_imports,
            artifact_repository=artifact_repository,
            session_id=session_id,
            grouping_column_names=grouping_column_names,
        )
        cogroup_udtf_name = cogroup_udtf.name

    num_keys = len(snowpark_input_grouping_exprs)

    input_prepared = _prepare_input_for_python(
        input_container, snowpark_input_grouping_exprs, 1
    )
    other_prepared = _prepare_input_for_python(
        other_container, snowpark_other_grouping_exprs, 2
    )

    combined_df = input_prepared.union_all(other_prepared)

    key_cols = _key_columns_refs(num_keys)

    # Unlike Scala cogroup (which has signature Function3[K, Iterator[V1], Iterator[V2], R]),
    # Python's applyInPandas has signature (df1: DataFrame, df2: DataFrame) -> DataFrame.
    # The key is not passed to the Python function - it only receives the grouped DataFrames.
    # Therefore, no key construction is needed here, only partitioning by key columns.
    tfc = snowpark_fn.call_table_function(
        cogroup_udtf_name,
        snowpark_fn.col(VALUE_COL_NAME).cast(VariantType()),
        snowpark_fn.col(SOURCE_COL_NAME),
    ).over(partition_by=key_cols)

    cols_to_drop = [_key_col_name(i) for i in range(num_keys)] + [
        VALUE_COL_NAME,
        SOURCE_COL_NAME,
    ]

    result = combined_df.join_table_function(tfc).drop(*cols_to_drop)

    return DataFrameContainer.create_with_column_mapping(
        dataframe=result,
        spark_column_names=[field.name for field in output_type],
        snowpark_column_names=result.columns,
        column_qualifiers=None,
        parent_column_name_map=input_container.column_map,
        equivalent_snowpark_names=None,
    )
