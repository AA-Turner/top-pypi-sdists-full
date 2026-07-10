#
# Copyright (c) 2012-2025 Snowflake Computing Inc. All rights reserved.
#
import io
import json
import re
from datetime import timedelta
from json import JSONDecodeError

import numpy as np
import pyarrow as pa
import pyspark.sql.connect.proto.relations_pb2 as relation_proto
from pyspark.errors.exceptions.connect import SparkConnectGrpcException

from snowflake import snowpark
from snowflake.snowpark._internal.analyzer.analyzer import ARRAY_BIND_THRESHOLD
from snowflake.snowpark._internal.analyzer.analyzer_utils import unquote_if_quoted
from snowflake.snowpark._internal.utils import is_in_stored_procedure
from snowflake.snowpark.types import LongType, StringType, StructField, StructType
from snowflake.snowpark_connect import tcm
from snowflake.snowpark_connect.column_name_handler import (
    make_column_names_snowpark_compatible,
)
from snowflake.snowpark_connect.config import global_config
from snowflake.snowpark_connect.dataframe_container import DataFrameContainer
from snowflake.snowpark_connect.error.error_codes import ErrorCodes
from snowflake.snowpark_connect.error.error_utils import attach_custom_error_code
from snowflake.snowpark_connect.execute_plan.utils import _relax_pa_schema_for_nulls
from snowflake.snowpark_connect.type_mapping import (
    _parse_ddl_with_spark_scala,
    map_json_schema_to_snowpark,
    map_pyarrow_to_snowpark_types,
    map_simple_types,
)
from snowflake.snowpark_connect.typed_column import FieldType
from snowflake.snowpark_connect.utils.session import get_or_create_snowpark_session
from snowflake.snowpark_connect.utils.snowpark_connect_logging import logger
from snowflake.snowpark_connect.utils.telemetry import (
    SnowparkConnectNotImplementedError,
)


def parse_local_relation_schema_string(rel: relation_proto.Relation):
    # schema_str can be a dict, or just a type string, e.g. INTEGER.
    schema_str = rel.local_relation.schema
    assert schema_str
    try:
        schema_dict = json.loads(schema_str)
    except JSONDecodeError:
        # Legacy scala clients sends unparsed struct type strings like "struct<id:bigint,a:int,b:double>"
        spark_datatype = _parse_ddl_with_spark_scala(schema_str)
        schema_dict = json.loads(spark_datatype.json())

    column_metadata = {}
    if isinstance(schema_dict, dict):
        spark_column_names = [field["name"] for field in schema_dict["fields"]]
        new_columns = make_column_names_snowpark_compatible(
            spark_column_names, rel.common.plan_id
        )

        fields = schema_dict.get("fields", None)
        if fields is not None:
            for field, new_name in zip(fields, new_columns):
                if field.get("metadata") is not None:
                    column_metadata[field["name"]] = field["metadata"]

                # Capture UDT information for later use
                field_type = field.get("type")
                if isinstance(field_type, dict) and field_type.get("type") == "udt":
                    udt_info = {
                        "__udt_info__": {
                            "pyClass": field_type.get("pyClass"),
                            "class": field_type.get("class"),
                            "sqlType": field_type.get("sqlType"),
                            "serializedClass": field_type.get("serializedClass"),
                        }
                    }
                    logger.debug(
                        f"Found UDT field: {field['name']}, storing UDT info: {udt_info}"
                    )

                    # Merge with existing metadata or create new
                    if field["name"] in column_metadata:
                        column_metadata[field["name"]].update(udt_info)
                    else:
                        column_metadata[field["name"]] = udt_info

                field["name"] = new_name
            schema_dict["fields"] = fields

        snowpark_schema = map_json_schema_to_snowpark(
            schema_dict, quote_struct_fields_names=False
        )
    else:
        # the schema_dict is just a type string without field name.
        spark_column_names = [
            "value"
        ]  # give a default name "value" when no name is provided
        new_columns = make_column_names_snowpark_compatible(
            spark_column_names, rel.common.plan_id
        )
        snowpark_type = map_simple_types(
            schema_dict
        )  # schema_dict should be a simple type string, like "STRING"

        snowpark_schema = snowpark.types.StructType(
            [
                snowpark.types.StructField(
                    new_columns[0], snowpark_type, _is_column=False
                ),
            ]
        )
    return snowpark_schema, spark_column_names, new_columns, column_metadata


def map_pylist_cell_to_python_object(cell, type: pa.lib.DataType):
    """
    Pylist means python list, which comes from pyarrow column.to_pylist(). Pylist is preferred over pandas_df in the
    conversion from pyarrow table to snowpark_df because it keeps more accurate information. E.g., NaN and None are
    untouched in pylist_df, but are both NaN in pandas_df. Though to_pylist may have lower performance when data size is
    large, map_local_relation usually applies to small data size.
    """
    match type:
        case struct_type if cell is not None and isinstance(type, pa.lib.StructType):
            if isinstance(cell, dict):
                # Handle struct types by recursively processing each field
                # Example:
                #   Input:  {'a': 1, 'b': [1, 2], 'c': [('k1', 'v1'), ('k2', 'v2')]}
                #   Output: {'a': 1, 'b': [1, 2], 'c': {'k1': 'v1', 'k2': 'v2'}}
                # where field 'c' has MapType and gets converted from list to dict.
                return {
                    field.name: map_pylist_cell_to_python_object(
                        cell[field.name], field.type
                    )
                    for field in struct_type
                }
            else:
                # If cell is not a dict (unexpected for struct), return as-is
                return cell
        case list_type if cell is not None and isinstance(type, pa.lib.ListType):
            return [
                map_pylist_cell_to_python_object(obj, list_type.value_type)
                for obj in cell
            ]
        case map_type if cell is not None and isinstance(type, pa.lib.MapType) and all(
            isinstance(obj, tuple) and len(obj) == 2 for obj in cell
        ):
            # the MapType in arrow becomes list in pylist_df,
            # e.g. {"Car": "Honda", "Bike": "Yamaha"} --> [("Car", "Honda"), ("Bike", "Yamaha")] , and causes some
            # trouble in the following snowpark dataframe creation, which expects MapType but pylist_df only provides
            # list (not dict).
            return {
                map_pylist_cell_to_python_object(
                    k, map_type.key_type
                ): map_pylist_cell_to_python_object(v, map_type.item_type)
                for k, v in cell
            }
        case _:
            return cell


def _ymi_total_months_to_string(total_months: int) -> str:
    sign = ""
    if total_months < 0:
        sign = "-"
        total_months = abs(total_months)
    years = total_months // 12
    months = total_months % 12
    return f"{sign}{years}-{months}"


def _dti_total_us_to_string(total_us: int) -> str:
    sign = ""
    if total_us < 0:
        sign = "-"
        total_us = abs(total_us)
    days = total_us // 86_400_000_000
    remaining = total_us % 86_400_000_000
    hours = remaining // 3_600_000_000
    remaining %= 3_600_000_000
    minutes = remaining // 60_000_000
    remaining %= 60_000_000
    seconds = remaining // 1_000_000
    microseconds = remaining % 1_000_000
    time_part = f"{hours:02d}:{minutes:02d}:{seconds:02d}"
    if microseconds:
        time_part += f".{microseconds:06d}"
    return f"{sign}{days} {time_part}"


def _convert_interval_to_string(cell, snowpark_type):
    """Convert Arrow-deserialized interval values to the string format
    that Snowflake can parse when casting to interval types.

    Arrow serializes intervals as:
      - YearMonthIntervalType: int32 (total months) from Scala client
      - DayTimeIntervalType: int64 (total microseconds) from Scala client,
        or pa.duration[us] -> timedelta from PySpark client

    Snowflake accepts these string formats for interval casting:
      - YMI: "Y-M" (e.g. "1-2" for 1 year 2 months)
      - DTI: "D HH:MM:SS[.ffffff]" (e.g. "1 00:00:01")
    """
    if cell is None:
        return cell

    if isinstance(snowpark_type, snowpark.types.YearMonthIntervalType):
        if isinstance(cell, (int, float)):
            return _ymi_total_months_to_string(int(cell))

    elif isinstance(snowpark_type, snowpark.types.DayTimeIntervalType):
        if isinstance(cell, (int, float)):
            return _dti_total_us_to_string(int(cell))
        elif isinstance(cell, timedelta):
            return _dti_total_us_to_string(int(cell / timedelta(microseconds=1)))

    return cell


def _convert_arrow_table_intervals(
    table: pa.Table, snowpark_schema: StructType
) -> pa.Table:
    """Convert interval columns in an Arrow table to string columns.

    The PyArrow path passes the Arrow table directly to Snowpark's
    create_dataframe, which writes it to a stage and reads it back.
    Arrow duration[us] columns become numeric in Snowflake. A direct
    CAST(numeric AS INTERVAL) fails, but CAST(varchar AS INTERVAL)
    works. This function converts interval columns to string arrays
    so the subsequent .cast(IntervalType()) produces a valid string→interval cast.
    """
    if not isinstance(snowpark_schema, StructType):
        return table

    new_columns = []
    changed = False
    for i, field in enumerate(snowpark_schema.fields):
        if i >= table.num_columns:
            break
        if isinstance(
            field.datatype,
            (snowpark.types.YearMonthIntervalType, snowpark.types.DayTimeIntervalType),
        ):
            pylist = table.column(i).to_pylist()
            str_values = [
                _convert_interval_to_string(v, field.datatype) for v in pylist
            ]
            new_columns.append(pa.array(str_values, type=pa.string()))
            changed = True
        else:
            new_columns.append(table.column(i))

    if not changed:
        return table

    return pa.table(dict(zip(table.column_names, new_columns)))


def map_pandas_cell_to_python_object(cell):
    match cell:
        case arr if isinstance(arr, np.ndarray):
            res = [map_pandas_cell_to_python_object(obj) for obj in cell]
        case [*_] if all(isinstance(obj, tuple) and len(obj) == 2 for obj in cell):
            # The conversion from arrow_table to pandas_df loses information. we need to re-think what's the correct way, e.g. skip pandas_df?
            #
            # 1. For the MapType in arrow, it becomes list in pandas_df,
            # e.g. {"Car": "Honda", "Bike": "Yamaha"} --> [("Car", "Honda"), ("Bike", "Yamaha")] , and causes some
            # trouble in the following snowpark dataframe creation, which expects MapType but pandas_df only provides
            # list (not dict).
            #
            # 2. For null in arrow, it becomes nan in pandas_df

            # pyspark MapType becomes a list of tuples with two elements each. Other pyspark type doesn't seem to use list, e.g. ArrayType becomes np.ndarray
            res = {
                map_pandas_cell_to_python_object(k): map_pandas_cell_to_python_object(v)
                for k, v in cell
            }
        case _:
            # Snowpark doesn't accept numpy generic type, e.g. numpy.int32
            res = cell.item() if isinstance(cell, np.generic) else cell
    # when NaN (NaN != NaN), res = None, cause Snowpark doesn't support NaN in Row objects
    return res if res == res else None


def map_local_relation(
    rel: relation_proto.Relation,
) -> DataFrameContainer:
    has_schema = (
        rel.local_relation.HasField("schema") and rel.local_relation.schema != ""
    )
    if rel.local_relation.HasField("data"):
        data = io.BytesIO(rel.local_relation.data)
        with pa.ipc.open_stream(data) as reader:
            table = reader.read_all()

        if table.num_columns == 0 and table.num_rows == 0:
            # For some reason, we can get a payload that deserializes to
            # 0 columns and 0 rows. This should not be possible and Spark Connect
            # does throw an error here.
            exception = SparkConnectGrpcException(
                "Input data for LocalRelation does not produce a schema."
            )
            attach_custom_error_code(exception, ErrorCodes.INVALID_INPUT)
            raise exception

        if table.num_columns == 0:
            # 0-column dataframe with rows
            return _create_zero_column_relation(table.num_rows)

        session = get_or_create_snowpark_session()
        if not has_schema:
            snowpark_schema = {}
            column_metadata = {}
            spark_column_names = table.column_names
            new_columns = make_column_names_snowpark_compatible(
                spark_column_names, rel.common.plan_id
            )
            if not all(len(col) == 0 for col in spark_column_names):
                unquoted_new_columns = [column[1:-1] for column in new_columns]
                table = table.rename_columns(unquoted_new_columns)
        else:
            (
                snowpark_schema,
                spark_column_names,
                new_columns,
                column_metadata,
            ) = parse_local_relation_schema_string(rel)
        # Snowpark ignores the schema when you pass in a pandas DataFrame, so
        # unfortunately we have to convert it to a list of tuples and pass the schema
        # so that Snowpark respects this schema. This is particularly problematic for
        # array type columns, which always because variants due to the conversion from
        # pandas "object" dtype.
        if all(len(col) == 0 for col in table.column_names):
            # Only create the pandas dataframe for empty dataframe cases.
            pandas_df = table.to_pandas()
            snowpark_df: snowpark.DataFrame = session.create_dataframe(pandas_df)
            return DataFrameContainer.create_with_column_mapping(
                dataframe=snowpark_df,
                spark_column_names=spark_column_names,
                snowpark_column_names=new_columns,
                column_metadata=column_metadata,
            )
        if snowpark_schema == {}:
            # If we don't have a provided schema, we'll try to determine the schema using the PyArrow table schema.
            # This isn't a perfect schema as we can't distinguish between StructTypes and MapTypes. This is because
            # when we have a numpy array input, map and struct are somewhat synoynmous. This means that we can't tell
            # them apart. Therefore, we simply cast both of them to VariantType for now until have a better solution.
            snowpark_schema = StructType(
                [
                    StructField(
                        field.name,
                        map_pyarrow_to_snowpark_types(field.type),
                        field.nullable,
                    )
                    for field in table.schema
                ],
                structured=True,
            )

        # Special characters in the schema currently break create_dataframe with arrow
        # https://snowflakecomputing.atlassian.net/browse/SNOW-2199291
        current_schema = session.get_current_schema()

        # _create_temp_stage() changes were not ported to the internal connector, leading to this
        # error on TCM and in notebooks (sproc):
        # TypeError: _create_temp_stage() takes 7 positional arguments but 8 were given
        #
        # For large local relations (rows * cols >= ARRAY_BIND_THRESHOLD), use PyArrow path for better performance.
        # PyArrow uses stage operations (5-6 queries) which is more efficient for large data than batch inserts.

        enable_optimization = global_config._get_config_setting(
            "snowpark.connect.localRelation.optimizeSmallData"
        )
        # Always use the vectorized scanner for the Parquet staging path used by
        # createDataFrame; the non-vectorized path has correctness issues with
        # MAP columns (SNOW-3390852) and is no longer user-configurable.
        use_vectorized_scanner = True
        use_pyarrow = (
            not is_in_stored_procedure()
            # TODO: SNOW-2220726 investigate why use_pyarrow failed in TCM:
            and not tcm.TCM_MODE
            and re.match(
                # See https://docs.snowflake.com/en/sql-reference/identifiers-syntax
                r"[A-Za-z_][A-Za-z0-9_\$]*",
                # Schema may be double-quoted.
                current_schema.strip('"') if current_schema is not None else "",
            )
            is not None
            and (
                # When optimization is disabled, always use PyArrow (preserves row ordering that some tests rely on)
                not enable_optimization
                # When optimization is enabled, use PyArrow only for large data for better performance.
                or (table.num_rows * table.num_columns >= ARRAY_BIND_THRESHOLD)
            )
        )

        if use_pyarrow:
            table = _convert_arrow_table_intervals(table, snowpark_schema)

            # The embedded LocalRelation Arrow schema follows Spark's convention: a
            # non-nullable primitive can still receive null slots when its parent
            # struct/array element is null. PyArrow >= 18 rejects a non-nullable
            # field that contains nulls, so widen (recursively, including nested
            # struct/list/map fields) only the fields whose data actually carries
            # nulls; declared nullability is preserved everywhere else.
            table = table.cast(_relax_pa_schema_for_nulls(table, table.schema))

            snowpark_df: snowpark.DataFrame = session.create_dataframe(
                # Rename the columns to match the Snowpark schema before creating.
                data=table.rename_columns([unquote_if_quoted(c) for c in new_columns]),
                use_vectorized_scanner=use_vectorized_scanner,
            )

            # Cast the columns to the correct types based on the schema as create_dataframe will
            # infer the schema.
            casted_columns = [
                snowpark_df[snowpark_df.columns[i]]
                .cast(field.datatype)
                .alias(field.name)
                for i, field in enumerate(snowpark_schema.fields)
            ]

            snowpark_df = snowpark_df.select(*casted_columns)

        else:
            # For small datasets (< ARRAY_BIND_THRESHOLD), use List[Row] path.
            # Snowpark's SnowflakeValues will use inline VALUES clause (lazy, no queries) for small data,
            # or temp table with batch insert (lazy, 3 queries on action) if it grows larger.
            pylist_df = [
                list(row)
                for row in zip(*(col.to_pylist() for col in table.itercolumns()))
            ]
            schema_fields = (
                snowpark_schema.fields
                if isinstance(snowpark_schema, StructType)
                else []
            )
            data_for_snowpark = [
                snowpark.Row(
                    **dict(
                        zip(
                            new_columns,
                            [
                                _convert_interval_to_string(
                                    map_pylist_cell_to_python_object(
                                        cell, table.schema.types[i]
                                    ),
                                    schema_fields[i].datatype
                                    if i < len(schema_fields)
                                    else None,
                                )
                                for i, cell in enumerate(row)
                            ],
                        )
                    )
                )
                for row in pylist_df
            ]
            snowpark_df: snowpark.DataFrame = session.create_dataframe(
                data_for_snowpark,
                snowpark_schema,
            )

        container = DataFrameContainer.create_with_column_mapping(
            dataframe=snowpark_df,
            spark_column_names=spark_column_names,
            snowpark_column_names=new_columns,
            column_metadata=column_metadata,
            snowpark_column_types=[
                FieldType(f.datatype, f.nullable) for f in snowpark_schema.fields
            ],
        )

        # SNOW-3242008: Cache the Arrow table for DDL/DML sql_command results so
        # that map_execution_root can return it directly without executing a VALUES
        # query against Snowflake. These results are always a single row with a
        # single column, e.g.:
        #   - DDL: "Statement executed successfully." (string)
        #   - DML: number of rows inserted = 1 (integer)
        if (
            table.num_rows == 1
            and table.num_columns == 1
            and (
                pa.types.is_string(table.schema.field(0).type)
                or pa.types.is_integer(table.schema.field(0).type)
            )
        ):
            container._cached_local_relation_arrow_table = table
        return container
    elif has_schema:
        (
            snowpark_schema,
            spark_column_names,
            new_columns,
            column_metadata,
        ) = parse_local_relation_schema_string(rel)

        if len(spark_column_names) == 0:
            return _create_zero_column_relation()

        session = get_or_create_snowpark_session()
        snowpark_df: snowpark.DataFrame = session.create_dataframe(
            [],
            snowpark_schema,
        )
        return DataFrameContainer.create_with_column_mapping(
            dataframe=snowpark_df,
            spark_column_names=spark_column_names,
            snowpark_column_names=new_columns,
            column_metadata=column_metadata,
            snowpark_column_types=[
                FieldType(f.datatype, f.nullable) for f in snowpark_schema.fields
            ],
        )
    else:
        exception = SnowparkConnectNotImplementedError(
            "LocalRelation without data & schema is not supported"
        )
        attach_custom_error_code(exception, ErrorCodes.UNSUPPORTED_OPERATION)
        raise exception


def _create_zero_column_relation(rows: int = 0) -> DataFrameContainer:
    """
    Handles an edge case where the user wants to create a 0-column dataframe.
    Returns a DataframeContainer representing a 0-column df, backed by a Snowpark dataframe
    with a hidden dummy column.
    """
    session = get_or_create_snowpark_session()
    snowpark_df: snowpark.DataFrame = session.create_dataframe(
        [(None,) for _ in range(rows)],
        StructType([StructField("__DUMMY", StringType())]),
    )
    container = DataFrameContainer.create_with_column_mapping(
        dataframe=snowpark_df,
        spark_column_names=["__DUMMY"],
        snowpark_column_names=["__DUMMY"],
        column_is_internal=[True],
    )
    # SNOW-3242008: Row count is known at creation time; avoid a Snowflake query later.
    container._known_row_count = rows
    return container


def map_range(
    rel: relation_proto.Relation,
) -> DataFrameContainer:
    session = get_or_create_snowpark_session()
    new_columns = make_column_names_snowpark_compatible(["id"], rel.common.plan_id)
    result = session.range(
        rel.range.start, rel.range.end, rel.range.step
    ).with_column_renamed("ID", new_columns[0])
    return DataFrameContainer.create_with_column_mapping(
        dataframe=result,
        spark_column_names=["id"],
        snowpark_column_names=new_columns,
        snowpark_column_types=[FieldType(LongType(), nullable=False)],
    )
