#
# Copyright (c) 2012-2025 Snowflake Computing Inc. All rights reserved.
#

import pyspark.sql.connect.proto.relations_pb2 as relation_proto
from pyspark.sql.connect.proto.expressions_pb2 import CommonInlineUserDefinedFunction

import snowflake.snowpark.functions as snowpark_fn
from snowflake import snowpark
from snowflake.snowpark.types import StructField, StructType
from snowflake.snowpark_connect.config import get_artifact_repository, global_config
from snowflake.snowpark_connect.constants import MAP_IN_ARROW_EVAL_TYPE
from snowflake.snowpark_connect.dataframe_container import DataFrameContainer
from snowflake.snowpark_connect.expression.map_unresolved_star import (
    map_unresolved_star_as_single_column,
)
from snowflake.snowpark_connect.expression.typer import ExpressionTyper
from snowflake.snowpark_connect.relation.map_relation import map_relation
from snowflake.snowpark_connect.relation.output_struct_utils import (
    unpack_java_udtf_output_to_container,
)
from snowflake.snowpark_connect.type_mapping import proto_to_snowpark_type
from snowflake.snowpark_connect.typed_column import FieldType
from snowflake.snowpark_connect.utils.context import get_spark_session_id
from snowflake.snowpark_connect.utils.java_udtf_utils import (
    JAVA_UDTF_PREFIX,
    create_java_udtf,
)
from snowflake.snowpark_connect.utils.jvm_udf_utils import (
    is_decomposable_struct,
    is_native_sql_type,
)
from snowflake.snowpark_connect.utils.pandas_udtf_utils import (
    create_pandas_udtf,
    create_pandas_udtf_with_arrow,
)
from snowflake.snowpark_connect.utils.udf_helper import udf_check
from snowflake.snowpark_connect.utils.udtf_helper import (
    create_pandas_udtf_in_sproc,
    require_creating_udtf_in_sproc,
)
from snowflake.snowpark_connect.utils.udxf_import_utils import (
    get_python_udxf_import_files,
)
from snowflake.snowpark_connect.utils.variant_utils import scala_udf_arg_to_variant


def map_map_partitions(
    rel: relation_proto.Relation,
) -> DataFrameContainer:
    """
    Map a function over the partitions of the input DataFrame.

    This is a simple wrapper around the `mapInPandas` method in Snowpark.
    """
    input_container = map_relation(rel.map_partitions.input)
    udf_proto = rel.map_partitions.func
    udf_check(udf_proto)

    return _map_with_udtf(input_container, udf_proto)


def _call_udtf(
    udtf_name: str, input_df: snowpark.DataFrame, return_type: StructType | None = None
) -> DataFrameContainer:
    # Add a dummy column with random 1-10 values for partitioning
    input_df_with_dummy = input_df.withColumn(
        "_DUMMY_PARTITION_KEY",
        (
            snowpark_fn.uniform(
                snowpark_fn.lit(1), snowpark_fn.lit(10), snowpark_fn.random()
            )
            * 10
        ).cast("int"),
    )

    udtf_columns = [f"snowflake_jtf_{column}" for column in input_df.columns] + [
        "_DUMMY_PARTITION_KEY"
    ]

    tfc = snowpark_fn.call_table_function(udtf_name, *udtf_columns).over(
        partition_by=[snowpark_fn.col("_DUMMY_PARTITION_KEY")]
    )

    # Overwrite the input_df columns to prevent name conflicts with UDTF output columns
    result_df_with_dummy = input_df_with_dummy.to_df(udtf_columns).join_table_function(
        tfc
    )

    output_cols = [field.name for field in return_type.fields]

    # Only return the output columns.
    result_df = result_df_with_dummy.select(*output_cols)

    return DataFrameContainer.create_with_column_mapping(
        dataframe=result_df,
        spark_column_names=output_cols,
        snowpark_column_names=output_cols,
        snowpark_column_types=[
            FieldType(field.datatype, field.nullable) for field in return_type.fields
        ],
    )


def _call_scala_udtf_partitioned(
    input_df: snowpark.DataFrame,
    udtf_name: str,
    partition_hint: int,
    *udtf_args,
) -> snowpark.DataFrame:
    """
    Call a Scala UDTF with OVER(PARTITION BY ...) so that Snowflake groups rows
    into partitions before invoking the UDTF. The UDTF accumulates rows in
    process() and applies the function in endPartition().
    """
    partition_col_name = "_DUMMY_PARTITION_KEY"
    if partition_hint == 1:
        input_df_with_key = input_df.withColumn(partition_col_name, snowpark_fn.lit(1))
    else:
        input_df_with_key = input_df.withColumn(
            partition_col_name,
            (
                snowpark_fn.uniform(
                    snowpark_fn.lit(0),
                    snowpark_fn.lit(partition_hint - 1),
                    snowpark_fn.random(),
                )
            ).cast("int"),
        )

    tfc = snowpark_fn.call_table_function(udtf_name, *udtf_args).over(
        partition_by=[snowpark_fn.col(partition_col_name)]
    )
    return input_df_with_key.join_table_function(tfc)


def _map_with_udtf(
    input_df_container: DataFrameContainer,
    udf_proto: CommonInlineUserDefinedFunction,
) -> DataFrameContainer:
    input_df = input_df_container.dataframe
    input_schema = input_df.schema
    spark_column_names = input_df_container.column_map.get_spark_columns()
    return_type = proto_to_snowpark_type(
        udf_proto.python_udf.output_type
        if udf_proto.WhichOneof("function") == "python_udf"
        else udf_proto.scalar_scala_udf.outputType
    )

    if udf_proto.WhichOneof("function") == "scalar_scala_udf":
        assert (
            len(udf_proto.scalar_scala_udf.inputTypes) == 1
        ), "len(inputTypes) should be 1 for map and flatMap operations"

        if udf_proto.scalar_scala_udf.inputTypes[0].WhichOneof("kind") == "struct":
            arg_types = [
                StructType(
                    [
                        StructField(
                            spark_column_names[i],
                            f.datatype,
                            f.nullable,
                            _is_column=f._is_column,
                        )
                        for i, f in enumerate(input_schema.fields)
                    ]
                )
            ]
            # Resolve the output column name (needed for the output unpack below).
            spark_col_name, typed_col = map_unresolved_star_as_single_column(
                udf_proto.arguments[0],
                input_df_container.column_map,
                ExpressionTyper(input_df),
            )
            if is_decomposable_struct(arg_types[0]):
                # Decompose struct fields: native fields passed as their SQL type,
                # non-native fields (Timestamp, Date, Array, …) passed as VARIANT.
                # Applies to both flatMap and mapPartitions (batch_mode).
                snowpark_cols = input_df_container.column_map.get_snowpark_columns()
                udtf_arg_columns = [
                    snowpark_fn.col(snowpark_cols[i])
                    if is_native_sql_type(f.datatype)
                    else scala_udf_arg_to_variant(
                        snowpark_fn.col(snowpark_cols[i]), f.datatype
                    )
                    for i, f in enumerate(arg_types[0].fields)
                ]
            else:
                # Non-decomposable struct: pass the whole struct as a single VARIANT arg.
                # Computed only here to avoid the eager analyzer call on the decomposed path.
                udtf_arg_columns = [
                    scala_udf_arg_to_variant(typed_col.col, typed_col.typ)
                ]
        else:
            snowpark_col = snowpark_fn.col(
                input_df_container.column_map.get_snowpark_columns()[0]
            )
            spark_col_name = input_df_container.column_map.get_spark_columns()[0]
            arg_types = [input_schema.fields[0].datatype]
            udtf_arg_columns = (
                [snowpark_col]
                if is_native_sql_type(arg_types[0])
                else [scala_udf_arg_to_variant(snowpark_col, arg_types[0])]
            )

        partition_hint = input_df_container.partition_hint

        if partition_hint is not None and partition_hint > 0:
            udtf_name = create_java_udtf(udf_proto, arg_types, batch_mode=True)
            df = _call_scala_udtf_partitioned(
                input_df, udtf_name, partition_hint, *udtf_arg_columns
            )
        else:
            udtf_name = create_java_udtf(udf_proto, arg_types, batch_mode=False)
            df = input_df.join_table_function(
                snowpark_fn.call_table_function(udtf_name, *udtf_arg_columns)
            )

        return unpack_java_udtf_output_to_container(
            df=df,
            output_type=return_type,
            non_struct_spark_name=spark_col_name,
            java_udtf_prefix=JAVA_UDTF_PREFIX,
        )

    # Check if this is mapInArrow (eval_type == 207)
    map_in_arrow = (
        udf_proto.WhichOneof("function") == "python_udf"
        and udf_proto.python_udf.eval_type == MAP_IN_ARROW_EVAL_TYPE
    )
    udtf_packages = global_config.get("snowpark.connect.udf.packages", "")
    udtf_imports = get_python_udxf_import_files(snowpark.Session.get_active_session())
    artifact_repository = get_artifact_repository()
    session_id = get_spark_session_id()
    if require_creating_udtf_in_sproc(udf_proto):
        udtf_name = create_pandas_udtf_in_sproc(
            udf_proto,
            spark_column_names,
            input_schema,
            return_type,
            udtf_packages,
            udtf_imports,
            artifact_repository=artifact_repository,
            session_id=session_id,
        )
    else:
        if map_in_arrow:
            map_udtf = create_pandas_udtf_with_arrow(
                udf_proto,
                spark_column_names,
                input_schema,
                return_type,
                udtf_packages,
                udtf_imports,
                artifact_repository=artifact_repository,
                session_id=session_id,
            )
        else:
            map_udtf = create_pandas_udtf(
                udf_proto,
                spark_column_names,
                input_schema,
                return_type,
                udtf_packages,
                udtf_imports,
                artifact_repository=artifact_repository,
                session_id=session_id,
            )
        udtf_name = map_udtf.name
    return _call_udtf(udtf_name, input_df, return_type)
