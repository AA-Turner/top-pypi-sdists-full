#
# Copyright (c) 2012-2025 Snowflake Computing Inc. All rights reserved.
#

import json
import re
import typing
from contextlib import suppress
from datetime import datetime
from functools import cache
from typing import Union

import jpype
import pyarrow as pa
import pyarrow.lib
import pyspark.sql.connect.proto.types_pb2 as types_proto
import pyspark.sql.types
from pyspark.errors.exceptions.base import AnalysisException
from pyspark.sql.connect.proto import expressions_pb2

from snowflake import snowpark
from snowflake.snowpark import types as snowpark_type
from snowflake.snowpark._internal.utils import quote_name
from snowflake.snowpark.types import TimestampTimeZone, TimestampType
from snowflake.snowpark_connect.column_name_handler import ColumnNameMap
from snowflake.snowpark_connect.config import get_timestamp_type
from snowflake.snowpark_connect.constants import (
    COLUMN_METADATA_COLLISION_KEY,
    STRUCTURED_TYPES_ENABLED,
)
from snowflake.snowpark_connect.date_time_format_mapping import (
    convert_spark_format_to_snowflake,
)
from snowflake.snowpark_connect.error.error_codes import ErrorCodes
from snowflake.snowpark_connect.error.error_utils import attach_custom_error_code
from snowflake.snowpark_connect.expression.literal import get_literal_field_and_name
from snowflake.snowpark_connect.expression.map_sql_expression import (
    _INTERVAL_DAYTIME_PATTERN_RE,
    _INTERVAL_YEARMONTH_PATTERN_RE,
)
from snowflake.snowpark_connect.utils.context import (
    get_is_evaluating_sql,
    get_is_python_client,
    get_jpype_jclass_lock,
)
from snowflake.snowpark_connect.utils.snowpark_connect_logging import logger
from snowflake.snowpark_connect.utils.telemetry import (
    SnowparkConnectNotImplementedError,
)

SNOWPARK_TYPE_NAME_TO_PYSPARK_TYPE_NAME = {
    snowpark.types.ArrayType.__name__: pyspark.sql.types.ArrayType.typeName(),
    snowpark.types.BinaryType.__name__: pyspark.sql.types.BinaryType.typeName(),
    snowpark.types.BooleanType.__name__: pyspark.sql.types.BooleanType.typeName(),
    snowpark.types.DateType.__name__: pyspark.sql.types.DateType.typeName(),
    snowpark.types.DecimalType.__name__: pyspark.sql.types.DecimalType.typeName(),
    snowpark.types.DoubleType.__name__: pyspark.sql.types.DoubleType.typeName(),
    snowpark.types.FloatType.__name__: pyspark.sql.types.FloatType.typeName(),
    snowpark.types.IntegerType.__name__: pyspark.sql.types.IntegerType.typeName(),
    snowpark.types.LongType.__name__: pyspark.sql.types.LongType.typeName(),
    snowpark.types.MapType.__name__: pyspark.sql.types.MapType.typeName(),
    snowpark.types.NullType.__name__: pyspark.sql.types.NullType.typeName(),
    snowpark.types.ShortType.__name__: pyspark.sql.types.ShortType.typeName(),
    snowpark.types.StringType.__name__: pyspark.sql.types.StringType.typeName(),
    snowpark.types.StructType.__name__: pyspark.sql.types.StructType.typeName(),
    snowpark.types.TimestampType.__name__: pyspark.sql.types.TimestampType.typeName(),
}


@cache
def _get_struct_type_class():
    with get_jpype_jclass_lock():
        return jpype.JClass("org.apache.spark.sql.types.StructType")


@cache
def get_python_sql_utils_class():
    with get_jpype_jclass_lock():
        return jpype.JClass("org.apache.spark.sql.api.python.PythonSQLUtils")


def _parse_ddl_with_spark_scala(ddl_string: str) -> pyspark.sql.types.DataType:
    """
    Parse DDL string using PySpark's Scala StructType.fromDDL() method.

    This mimics pysparks.ddl parsing logic pyspark.sql.types._py_parse_datatype_string
    """
    struct_type_class = _get_struct_type_class()
    python_sql_utils = get_python_sql_utils_class()

    try:
        # DDL format, "fieldname datatype, fieldname datatype".
        spark_struct_type = struct_type_class.fromDDL(ddl_string)
        return pyspark.sql.types._parse_datatype_json_string(spark_struct_type.json())
    except jpype.JException:
        try:
            # For backwards compatibility, "integer", "struct<fieldname: datatype>" and etc.
            # Parse as a single data type using PythonSQLUtils.parseDataType()
            spark_datatype = python_sql_utils.parseDataType(ddl_string)
            return pyspark.sql.types._parse_datatype_json_string(spark_datatype.json())
        except jpype.JException:
            # For backwards compatibility, "fieldname: datatype, fieldname: datatype" case.
            legacy_ddl = f"struct<{ddl_string.strip()}>"
            spark_datatype = python_sql_utils.parseDataType(legacy_ddl)
            return pyspark.sql.types._parse_datatype_json_string(spark_datatype.json())


def snowpark_to_proto_type(
    data_type: snowpark.types.DataType,
    column_name_map: ColumnNameMap | None = None,
    df: snowpark.DataFrame = None,  # remove this param after SNOW-1857090
    depth: int = 0,
) -> dict[str, types_proto.DataType]:
    """
    Map a Snowpark data type to a Proto data type.
    """
    match type(data_type):
        case snowpark.types.ArrayType:
            # in the case of semi-structured array, the element_type is None.
            # Before we finish structured type casting rewriting, we fall back to StringType.
            return {
                "array": types_proto.DataType.Array(
                    element_type=types_proto.DataType(
                        **dict(
                            snowpark_to_proto_type(
                                (
                                    data_type.element_type
                                    if data_type.element_type
                                    else snowpark.types.StringType()
                                ),
                                column_name_map,
                                df,
                                depth + 1,
                            )
                        )
                    ),
                    contains_null=data_type.contains_null,
                )
            }
        case snowpark.types.BinaryType:
            return {"binary": types_proto.DataType.Binary()}
        case snowpark.types.BooleanType:
            return {"boolean": types_proto.DataType.Boolean()}
        case snowpark.types.ByteType:
            return {"byte": types_proto.DataType.Byte()}
        case snowpark.types.DateType:
            return {"date": types_proto.DataType.Date()}
        case snowpark.types.DecimalType:
            return {
                "decimal": types_proto.DataType.Decimal(
                    precision=data_type.precision, scale=data_type.scale
                )
            }
        case snowpark.types.DoubleType:
            return {"double": types_proto.DataType.Double()}
        case snowpark.types.FloatType:
            return {"float": types_proto.DataType.Float()}
        case snowpark.types.IntegerType:
            return {"integer": types_proto.DataType.Integer()}
        case snowpark.types.LongType:
            return {"long": types_proto.DataType.Long()}
        case snowpark.types.MapType:
            if not data_type.structured:
                return {"string": types_proto.DataType.String()}
            # In the case of semi-structured Map, the key_type and data_type are None.
            # Before we finish structured type casting rewriting, we fall back to StringType.
            return {
                "map": types_proto.DataType.Map(
                    key_type=types_proto.DataType(
                        **snowpark_to_proto_type(
                            (
                                data_type.key_type
                                if data_type.key_type
                                else snowpark.types.StringType()
                            ),
                            column_name_map,
                            df,
                            depth + 1,
                        )
                    ),
                    value_type=types_proto.DataType(
                        **snowpark_to_proto_type(
                            (
                                data_type.value_type
                                if data_type.value_type
                                else snowpark.types.StringType()
                            ),
                            column_name_map,
                            df,
                            depth + 1,
                        )
                    ),
                    value_contains_null=data_type.value_contains_null,
                )
            }
        case snowpark.types.NullType:
            return {"null": types_proto.DataType.NULL()}
        case snowpark.types.ShortType:
            return {"short": types_proto.DataType.Short()}
        case snowpark.types.StringType:
            return {"string": types_proto.DataType.String()}
        case snowpark.types.StructType:
            if not data_type.structured:
                return {"string": types_proto.DataType.String()}

            def map_field(index, field):
                # For attributes inside struct type (depth > 0), they don't get renamed as normal dataframe column names. Thus no need to do the conversion from snowpark column name to spark column name.
                spark_name = (
                    column_name_map.get_spark_column_name(index)
                    if depth == 0 and column_name_map
                    else field.name
                )

                udt_info = None
                column_metadata_str = None
                if column_name_map and column_name_map.column_metadata:
                    metadata = column_name_map.column_metadata.get(spark_name, None)
                    if (
                        metadata is None
                        and df
                        and field.name in column_name_map.get_snowpark_columns()
                    ):
                        try:
                            # check for collision using expr_id
                            expr_id = df[field.name]._expression.expr_id
                            new_key = COLUMN_METADATA_COLLISION_KEY.format(
                                expr_id=expr_id, key=spark_name
                            )
                            metadata = column_name_map.column_metadata.get(
                                new_key, None
                            )
                        except snowpark.exceptions.SnowparkColumnException:
                            # TODO remove try/catch after SNOW-1857090
                            pass
                    if metadata is not None:
                        column_metadata_str = json.dumps(metadata)
                        udt_info = metadata.get("__udt_info__")

                # If this field has UDT info, return a StructField with UDT type
                if udt_info:
                    python_class = udt_info.get("pyClass")
                    logger.debug(
                        f"Creating UDT proto type for field: {spark_name} with class: {python_class}"
                    )

                    # Create a UDT proto type
                    udt_type = types_proto.DataType(
                        udt=types_proto.DataType.UDT(
                            type="udt",
                            python_class=python_class,
                            serialized_python_class=udt_info.get("serializedClass"),
                            jvm_class=udt_info.get("class"),
                            sql_type=types_proto.DataType(
                                **snowpark_to_proto_type(
                                    field.datatype, column_name_map, df, depth + 1
                                )
                            ),
                        )
                    )

                    return types_proto.DataType.StructField(
                        name=spark_name,
                        data_type=udt_type,
                        nullable=field.nullable,
                        metadata=column_metadata_str,
                    )

                return types_proto.DataType.StructField(
                    name=spark_name,
                    data_type=types_proto.DataType(
                        **snowpark_to_proto_type(
                            field.datatype, column_name_map, df, depth + 1
                        )
                    ),
                    nullable=field.nullable,
                    metadata=column_metadata_str,
                )

            fields = [map_field(i, field) for i, field in enumerate(data_type.fields)]

            return {"struct": types_proto.DataType.Struct(fields=fields)}
        case snowpark.types.TimestampType:
            match data_type.tz:
                case snowpark.types.TimestampTimeZone.NTZ:
                    return {"timestamp_ntz": types_proto.DataType.TimestampNTZ()}
                case _:
                    return {"timestamp": types_proto.DataType.Timestamp()}
        case snowpark.types.VariantType:
            # For now we are returning a string type for variant types.
            return {"string": types_proto.DataType.String()}
        case snowpark.types.YearMonthIntervalType:
            return {
                "year_month_interval": types_proto.DataType.YearMonthInterval(
                    start_field=data_type.start_field, end_field=data_type.end_field
                )
            }
        case snowpark.types.DayTimeIntervalType:
            return {
                "day_time_interval": types_proto.DataType.DayTimeInterval(
                    start_field=data_type.start_field, end_field=data_type.end_field
                )
            }
        case _:
            exception = SnowparkConnectNotImplementedError(
                f"Unsupported snowpark data type: {data_type}"
            )
            attach_custom_error_code(exception, ErrorCodes.UNSUPPORTED_OPERATION)
            raise exception


def cast_to_match_snowpark_type(
    data_type: snowpark.types.DataType, content: typing.Any, dateFormat: str = None
) -> typing.Any:
    """
    Cast data to Snowpark type
    """
    if content is None:
        return None

    match type(data_type):
        case snowpark.types.BooleanType:
            return (
                content.lower() == "true" if isinstance(content, str) else bool(content)
            )
        case snowpark.types.ByteType:
            return bytes(content)
        case snowpark.types.DecimalType:
            return float(content)
        case snowpark.types.DoubleType:
            return float(content)
        case snowpark.types.FloatType:
            return float(content)
        case snowpark.types.IntegerType:
            return int(content)
        case snowpark.types.LongType:
            return int(content)
        case snowpark.types.NullType:
            return None
        case snowpark.types.DateType:
            if not isinstance(content, str):
                return content
            if dateFormat is not None and dateFormat != "auto":
                return datetime.strptime(content, dateFormat)
            for format in ["%Y-%m-%d", "%d-%m-%Y", "%Y/%m/%d", "%m/%d/%Y"]:
                with suppress(TypeError):
                    date = datetime.strptime(content, format)
                    return date
            exception = ValueError(f"Date casting error for {str(content)}")
            attach_custom_error_code(exception, ErrorCodes.INVALID_CAST)
            raise exception
        case snowpark.types.ShortType:
            return int(content)
        case snowpark.types.StringType:
            if isinstance(content, dict):
                return json.dumps(content, separators=(",", ":"))
            return str(content)
        case snowpark.types.VariantType:
            return str(content)
        case snowpark.types.TimestampType:
            return str(content)
        case snowpark.types.YearMonthIntervalType:
            if isinstance(content, (int, float)):
                total_months = int(content)
                years = total_months // 12
                months = total_months % 12
                return f"INTERVAL '{years}-{months}' YEAR TO MONTH"
            elif isinstance(content, str) and content.startswith(("+", "-")):
                # Handle Snowflake's native interval format (e.g., "+11-08" or "-2-3")
                # Convert to Spark's format: "INTERVAL 'Y-M' YEAR TO MONTH"
                sign = content[0]
                interval_part = content[1:]  # Remove sign
                if sign == "-":
                    return f"INTERVAL '-{interval_part}' YEAR TO MONTH"
                else:
                    return f"INTERVAL '{interval_part}' YEAR TO MONTH"
            return str(content)
        case snowpark.types.DayTimeIntervalType:
            return str(content)
        case snowpark.types.MapType:
            return content
        case _:
            exception = SnowparkConnectNotImplementedError(
                f"Unsupported snowpark data type in casting: {data_type}"
            )
            attach_custom_error_code(exception, ErrorCodes.UNSUPPORTED_OPERATION)
            raise exception


def snowpark_to_iceberg_type(data_type: snowpark.types.DataType) -> str:
    """
    Map a Snowpark data type to a Snowflake iceberg data type.
    """
    match type(data_type):
        case snowpark.types.ArrayType:
            return f"array({snowpark_to_iceberg_type(data_type.element_type)})"
        case snowpark.types.BooleanType:
            return "boolean"
        case snowpark.types.DateType:
            return "date"
        case snowpark.types.DecimalType:
            return f"decimal({data_type.precision}, {data_type.scale})"
        case snowpark.types.DoubleType:
            return "double"
        case snowpark.types.FloatType:
            return "float"
        case snowpark.types.IntegerType:
            return "int"
        case snowpark.types.LongType:
            return "long"
        case snowpark.types.MapType:
            return f"map({snowpark_to_iceberg_type(data_type.key_type)}, {snowpark_to_iceberg_type(data_type.value_type)})"
        case snowpark.types.StringType:
            return "string"
        case snowpark.types.StructType:
            return f"""object({",".join([f'"{field.name}" {snowpark_to_iceberg_type(field.datatype)} {"" if field.nullable is True else "NOT NULL"}' for field in data_type.fields])})"""
        case snowpark.types.TimestampType:
            return "timestamp"
        case _:
            exception = SnowparkConnectNotImplementedError(
                f"Unsupported snowpark data type for iceber: {data_type}"
            )
            attach_custom_error_code(exception, ErrorCodes.UNSUPPORTED_OPERATION)
            raise exception


def proto_to_snowpark_type(
    data_type: types_proto.DataType,
) -> snowpark.types.DataType:
    """
    Map a Proto data type to a Snowpark data type.
    """
    match data_type.WhichOneof("kind"):
        case "array":
            return snowpark.types.ArrayType(
                proto_to_snowpark_type(data_type.array.element_type),
                structured=STRUCTURED_TYPES_ENABLED,
                contains_null=data_type.array.contains_null,
            )
        case "map":
            return snowpark.types.MapType(
                key_type=proto_to_snowpark_type(data_type.map.key_type),
                value_type=proto_to_snowpark_type(data_type.map.value_type),
                structured=STRUCTURED_TYPES_ENABLED,
                value_contains_null=data_type.map.value_contains_null,
            )
        case "struct":
            return snowpark.types.StructType(
                [
                    snowpark.types.StructField(
                        # NOTE: The column names are not mapped to the Spark column names here.
                        field.name,
                        proto_to_snowpark_type(field.data_type),
                        field.nullable,
                        _is_column=False,
                    )
                    for field in data_type.struct.fields
                ],
                structured=STRUCTURED_TYPES_ENABLED,
            )
        case "decimal":
            return snowpark.types.DecimalType(
                int(data_type.decimal.precision), int(data_type.decimal.scale)
            )
        case "udt":
            # For UDT types, return the underlying SQL type
            logger.debug("Returning underlying sql type for udt")
            return proto_to_snowpark_type(data_type.udt.sql_type)
        case "year_month_interval":
            # Preserve start_field and end_field from protobuf
            return snowpark.types.YearMonthIntervalType(
                start_field=data_type.year_month_interval.start_field,
                end_field=data_type.year_month_interval.end_field,
            )
        case "day_time_interval":
            # Preserve start_field and end_field from protobuf
            return snowpark.types.DayTimeIntervalType(
                start_field=data_type.day_time_interval.start_field,
                end_field=data_type.day_time_interval.end_field,
            )
        case _:
            return map_simple_types(data_type.WhichOneof("kind"))


def map_snowpark_types_to_pyarrow_types(
    snowpark_type: snowpark.types.DataType,
    pa_type: pa.DataType,
    rename_struct_columns: bool = False,
    for_empty_table: bool = False,
) -> pa.lib.DataType:
    """
    Map a Snowpark data type to a pyarrow data type.
    """
    assert pa_type is not None, "arrow type can't be None"

    # for structured types, we validate the pa_type matches snowpark_type,
    # with a exception for empty tables (schema might be inferred from data, and thus be null type)
    allow_null_pa_type = pa.types.is_null(pa_type) and for_empty_table

    match type(snowpark_type):
        case snowpark.types.ArrayType:
            if (
                not snowpark_type.structured
                or snowpark_type.element_type is None
                or pa_type == pa.string()
            ):
                # in the case of unstructured & semi-structured types, e.g. semi-structured array's element_type is None.
                # Before structured type is fully supported, we fall back to string type.
                return pa.string()
            if pa.types.is_list(pa_type) or allow_null_pa_type:
                return pa.list_(
                    map_snowpark_types_to_pyarrow_types(
                        snowpark_type.element_type,
                        pa.null() if allow_null_pa_type else pa_type.value_type,
                        for_empty_table=for_empty_table,
                    )
                )
            else:
                exception = AnalysisException(
                    f"Unsupported arrow type {pa_type} for snowpark ArrayType."
                )
                attach_custom_error_code(exception, ErrorCodes.UNSUPPORTED_TYPE)
                raise exception
        case snowpark.types.BinaryType:
            return pa.binary()
        case snowpark.types.BooleanType:
            return pa.bool_()
        case snowpark.types.ByteType:
            return pa.int8()
        case snowpark.types.DateType:
            return pa.date32()
        case snowpark.types.DecimalType:
            # PyArrow optimizes storage for decimal types with scale=0:
            # - Decimals with scale=0 and precision≤18 are stored as int64
            # - Decimals with scale=0 and 18<precision≤38 use int128
            # When attempting to cast int64 to Decimal128(precision,0), PyArrow requires
            # precision ≥ 19 regardless of actual value magnitude, including NULL values and it leads to casting error for None.
            # For Java/Scala, we want to preserve the Decimal since the client won't accept different type during deserialization.
            if snowpark_type.scale == 0 and get_is_python_client():
                if snowpark_type.precision <= 18:
                    return pa.int64()
            return pa.decimal128(snowpark_type.precision, snowpark_type.scale)
        case snowpark.types.DoubleType:
            return pa.float64()
        case snowpark.types.FloatType:
            return pa.float32()
        case snowpark.types.IntegerType:
            return pa.int32()
        case snowpark.types.LongType:
            return pa.int64()
        case snowpark.types.MapType:
            if not snowpark_type.structured:
                # semi-structured value
                return pa.string()
            if pa.types.is_map(pa_type) or pa.types.is_null(pa_type):
                return pa.map_(
                    key_type=map_snowpark_types_to_pyarrow_types(
                        snowpark_type.key_type,
                        pa.null() if allow_null_pa_type else pa_type.key_type,
                        for_empty_table=for_empty_table,
                    ),
                    item_type=map_snowpark_types_to_pyarrow_types(
                        snowpark_type.value_type,
                        pa.null() if allow_null_pa_type else pa_type.item_type,
                        for_empty_table=for_empty_table,
                    ),
                )
            else:
                exception = AnalysisException(
                    f"Unsupported arrow type {pa_type} for snowpark MapType."
                )
                attach_custom_error_code(exception, ErrorCodes.UNSUPPORTED_TYPE)
                raise exception
        case snowpark.types.NullType:
            return pa.string()
        case snowpark.types.ShortType:
            return pa.int16()
        case snowpark.types.StringType:
            return pa.string()
        case snowpark.types.StructType:
            if not snowpark_type.structured:
                # semi-structured value
                return pa.string()
            if pa.types.is_struct(pa_type) or pa.types.is_null(pa_type):
                return pa.struct(
                    [
                        pa.field(
                            field.name if not rename_struct_columns else str(i),
                            map_snowpark_types_to_pyarrow_types(
                                field.datatype,
                                pa.null() if allow_null_pa_type else pa_type[i].type,
                                for_empty_table=for_empty_table,
                            ),
                            nullable=True,
                        )
                        for i, field in enumerate(snowpark_type.fields)
                    ]
                )
            else:
                exception = AnalysisException(
                    f"Unsupported arrow type {pa_type} for snowpark StructType."
                )
                attach_custom_error_code(exception, ErrorCodes.UNSUPPORTED_TYPE)
                raise exception
        case snowpark.types.TimestampType:
            # Check if pa_type has unit attribute (it should be a timestamp type)
            unit = pa_type.unit if hasattr(pa_type, "unit") else "us"
            tz = pa_type.tz if hasattr(pa_type, "tz") else None

            # Spark truncates nanosecond precision to microseconds
            if unit == "ns":
                unit = "us"

            return pa.timestamp(unit, tz=tz)
        case snowpark.types.VariantType:
            return pa.string()
        case snowpark.types.YearMonthIntervalType:
            # Return string type so formatted intervals are preserved in display
            return pa.string()
        case snowpark.types.DayTimeIntervalType:
            # Return string type so formatted intervals are preserved in display
            return pa.string()
        case _:
            exception = SnowparkConnectNotImplementedError(
                f"Unsupported snowpark data type: {snowpark_type}"
            )
            attach_custom_error_code(exception, ErrorCodes.UNSUPPORTED_OPERATION)
            raise exception


def map_pyarrow_to_snowpark_types(pa_type: pa.DataType) -> snowpark.types.DataType:
    """
    Map a PyArrow data type (e.g., pa.string(), pa.int16()) to a Snowpark data type.
    """
    if pa.types.is_string(pa_type):
        return snowpark.types.StringType()
    elif pa.types.is_int8(pa_type):
        return snowpark.types.ByteType()
    elif pa.types.is_int16(pa_type):
        return snowpark.types.ShortType()
    elif pa.types.is_int32(pa_type):
        return snowpark.types.IntegerType()
    elif pa.types.is_int64(pa_type):
        return snowpark.types.LongType()
    elif pa.types.is_float32(pa_type):
        return snowpark.types.FloatType()
    elif pa.types.is_float64(pa_type):
        return snowpark.types.DoubleType()
    elif pa.types.is_binary(pa_type):
        return snowpark.types.BinaryType()
    elif pa.types.is_boolean(pa_type):
        return snowpark.types.BooleanType()
    elif pa.types.is_decimal(pa_type):
        return snowpark.types.DecimalType(
            precision=pa_type.int_precision, scale=pa_type.int_scale
        )
    elif pa.types.is_list(pa_type):
        return snowpark.types.ArrayType(
            element_type=map_pyarrow_to_snowpark_types(pa_type.value_type),
            structured=STRUCTURED_TYPES_ENABLED,
        )
    # TODO: Re-enable these for MapType
    # elif pa.types.is_map(pa_type):
    #     return snowpark.types.MapType(
    #         key_type=map_pyarrow_to_snowpark_types(pa_type.key_type),
    #         value_type=map_pyarrow_to_snowpark_types(pa_type.item_type),
    #         structured=STRUCTURED_TYPES_ENABLED
    #     )
    elif pa.types.is_struct(pa_type):
        return snowpark.types.VariantType()
        # TODO: Re-enable these for MapType
        # return snowpark.types.StructType(
        #     [
        #         snowpark.types.StructField(
        #             field.name,
        #             map_pyarrow_to_snowpark_types(field.type),
        #             field.nullable,
        #             _is_column=False
        #         )
        #         for field in pa_type
        #     ],
        #     structured=STRUCTURED_TYPES_ENABLED
        # )
    elif pa.types.is_date32(pa_type):
        return snowpark.types.DateType()
    elif pa.types.is_date64(pa_type):
        return snowpark.types.DateType()
    elif pa.types.is_timestamp(pa_type):
        tz = pa_type.tz
        if tz is None:
            return snowpark.types.TimestampType(
                timezone=snowpark.types.TimestampTimeZone.NTZ
            )
        return snowpark.types.TimestampType()
    elif pa.types.is_null(pa_type):
        return snowpark.types.NullType()
    elif pa.types.is_duration(pa_type):
        # Map PyArrow duration[us] to DayTimeIntervalType
        return snowpark.types.DayTimeIntervalType()
    else:
        exception = SnowparkConnectNotImplementedError(
            f"Unsupported PyArrow data type: {pa_type}"
        )
        attach_custom_error_code(exception, ErrorCodes.UNSUPPORTED_OPERATION)
        raise exception


def map_pyspark_types_to_snowpark_types(
    type_to_map: pyspark.sql.types.DataType,
) -> snowpark.types.DataType:
    """
    Map a PySpark data type to a Snowpark data type.

    This function is used to map the data types of columns in a PySpark DataFrame
    to the data types used in Snowpark. This is used in, for example, UDFs, where
    the client passes a serialized version of the client type (which will be a Pyspark
    type) and we need to map this to the Snowpark type.
    """
    # Handle UserDefinedType by extracting its underlying SQL type
    if hasattr(type_to_map, "sqlType") and callable(type_to_map.sqlType):
        underlying_type = type_to_map.sqlType()
        return map_pyspark_types_to_snowpark_types(underlying_type)

    if isinstance(type_to_map, pyspark.sql.types.ArrayType):
        return snowpark.types.ArrayType(
            map_pyspark_types_to_snowpark_types(type_to_map.elementType),
            structured=STRUCTURED_TYPES_ENABLED,
            contains_null=type_to_map.containsNull,
        )
    if isinstance(type_to_map, pyspark.sql.types.BinaryType):
        return snowpark.types.BinaryType()
    if isinstance(type_to_map, pyspark.sql.types.BooleanType):
        return snowpark.types.BooleanType()
    if isinstance(type_to_map, pyspark.sql.types.ByteType):
        return snowpark.types.ByteType()
    if isinstance(type_to_map, pyspark.sql.types.DateType):
        return snowpark.types.DateType()
    if isinstance(type_to_map, pyspark.sql.types.DecimalType):
        if type_to_map.hasPrecisionInfo:
            precision = type_to_map.precision
            scale = type_to_map.scale
            return snowpark.types.DecimalType(precision=precision, scale=scale)
        else:
            return snowpark.types.DecimalType()
    if isinstance(type_to_map, pyspark.sql.types.DoubleType):
        return snowpark.types.DoubleType()
    if isinstance(type_to_map, pyspark.sql.types.FloatType):
        return snowpark.types.FloatType()
    if isinstance(type_to_map, pyspark.sql.types.IntegerType):
        return snowpark.types.IntegerType()
    if isinstance(type_to_map, pyspark.sql.types.LongType):
        return snowpark.types.LongType()
    if isinstance(type_to_map, pyspark.sql.types.MapType):
        return snowpark.types.MapType(
            key_type=map_pyspark_types_to_snowpark_types(type_to_map.keyType),
            value_type=map_pyspark_types_to_snowpark_types(type_to_map.valueType),
            structured=STRUCTURED_TYPES_ENABLED,
            value_contains_null=type_to_map.valueContainsNull,
        )
    if isinstance(type_to_map, pyspark.sql.types.NullType):
        return snowpark.types.NullType()
    if isinstance(type_to_map, pyspark.sql.types.ShortType):
        return snowpark.types.ShortType()
    if isinstance(type_to_map, pyspark.sql.types.StringType):
        return snowpark.types.StringType()
    if isinstance(type_to_map, pyspark.sql.types.StructType):
        return snowpark.types.StructType(
            [
                snowpark.types.StructField(
                    field.name,
                    map_pyspark_types_to_snowpark_types(field.dataType),
                    field.nullable,
                    _is_column=False,
                )
                for field in type_to_map.fields
            ],
            structured=STRUCTURED_TYPES_ENABLED,
        )
    if isinstance(type_to_map, pyspark.sql.types.TimestampType):
        return snowpark.types.TimestampType()
    if isinstance(type_to_map, pyspark.sql.types.TimestampNTZType):
        return snowpark.types.TimestampType(timezone=TimestampTimeZone.NTZ)
    if isinstance(type_to_map, pyspark.sql.types.YearMonthIntervalType):
        return snowpark.types.YearMonthIntervalType(
            type_to_map.startField, type_to_map.endField
        )
    if isinstance(type_to_map, pyspark.sql.types.DayTimeIntervalType):
        return snowpark.types.DayTimeIntervalType(
            type_to_map.startField, type_to_map.endField
        )
    exception = SnowparkConnectNotImplementedError(
        f"Unsupported spark data type: {type_to_map}"
    )
    attach_custom_error_code(exception, ErrorCodes.UNSUPPORTED_OPERATION)
    raise exception


def map_snowpark_to_pyspark_types(
    type_to_map: snowpark.types.DataType,
) -> pyspark.sql.types.DataType:
    """
    Map a Snowpark data type to a PySpark data type.

    This function is used to map the data types of columns in a Snowpark DataFrame
    to the data types used in PySpark. This is used in converting a Snowpark schema
    into the expected JSON schema for LocalRelation.
    """
    if isinstance(type_to_map, snowpark.types.ArrayType):
        return pyspark.sql.types.ArrayType(
            elementType=map_snowpark_to_pyspark_types(type_to_map.element_type),
            containsNull=type_to_map.contains_null,
        )
    if isinstance(type_to_map, snowpark.types.BinaryType):
        return pyspark.sql.types.BinaryType()
    if isinstance(type_to_map, snowpark.types.BooleanType):
        return pyspark.sql.types.BooleanType()
    if isinstance(type_to_map, snowpark.types.ByteType):
        return pyspark.sql.types.ByteType()
    if isinstance(type_to_map, snowpark.types.DateType):
        return pyspark.sql.types.DateType()
    if isinstance(type_to_map, snowpark.types.DecimalType):
        precision = type_to_map.precision
        scale = type_to_map.scale
        return pyspark.sql.types.DecimalType(precision=precision, scale=scale)
    if isinstance(type_to_map, snowpark.types.DoubleType):
        return pyspark.sql.types.DoubleType()
    if isinstance(type_to_map, snowpark.types.FloatType):
        return pyspark.sql.types.FloatType()
    if isinstance(type_to_map, snowpark.types.IntegerType):
        return pyspark.sql.types.IntegerType()
    if isinstance(type_to_map, snowpark.types.LongType):
        return pyspark.sql.types.LongType()
    if isinstance(type_to_map, snowpark.types.MapType):
        return pyspark.sql.types.MapType(
            keyType=map_snowpark_to_pyspark_types(type_to_map.key_type),
            valueType=map_snowpark_to_pyspark_types(type_to_map.value_type),
            valueContainsNull=type_to_map.value_contains_null,
        )
    if isinstance(type_to_map, snowpark.types.NullType):
        return pyspark.sql.types.NullType()
    if isinstance(type_to_map, snowpark.types.ShortType):
        return pyspark.sql.types.ShortType()
    if isinstance(type_to_map, snowpark.types.StringType):
        return pyspark.sql.types.StringType()
    if isinstance(type_to_map, snowpark.types.StructType):
        return pyspark.sql.types.StructType(
            [
                pyspark.sql.types.StructField(
                    field.name,
                    map_snowpark_to_pyspark_types(field.datatype),
                    field.nullable,
                )
                for field in type_to_map.fields
            ]
        )
    if isinstance(type_to_map, snowpark.types.TimestampType):
        if type_to_map.tz == snowpark.types.TimestampTimeZone.NTZ:
            return pyspark.sql.types.TimestampNTZType()
        return pyspark.sql.types.TimestampType()
    if isinstance(type_to_map, snowpark.types.YearMonthIntervalType):
        return pyspark.sql.types.YearMonthIntervalType(
            type_to_map.start_field, type_to_map.end_field
        )
    if isinstance(type_to_map, snowpark.types.DayTimeIntervalType):
        return pyspark.sql.types.DayTimeIntervalType(
            type_to_map.start_field, type_to_map.end_field
        )
    exception = SnowparkConnectNotImplementedError(
        f"Unsupported data type: {type_to_map}"
    )
    attach_custom_error_code(exception, ErrorCodes.UNSUPPORTED_OPERATION)
    raise exception


def map_pyspark_types_to_pyarrow_types(
    pyspark_type: pyspark.sql.types.DataType,
) -> pa.DataType:
    """
    Map a PySpark data type to a PyArrow data type.

    This function converts PySpark types to PyArrow types for generating
    Parquet metadata files with correct schema structure.

    Args:
        pyspark_type: PySpark data type to convert

    Returns:
        Corresponding PyArrow data type
    """
    if isinstance(pyspark_type, pyspark.sql.types.StringType):
        return pa.string()
    elif isinstance(pyspark_type, pyspark.sql.types.LongType):
        return pa.int64()
    elif isinstance(pyspark_type, pyspark.sql.types.IntegerType):
        return pa.int32()
    elif isinstance(pyspark_type, pyspark.sql.types.ShortType):
        return pa.int16()
    elif isinstance(pyspark_type, pyspark.sql.types.ByteType):
        return pa.int8()
    elif isinstance(pyspark_type, pyspark.sql.types.DoubleType):
        return pa.float64()
    elif isinstance(pyspark_type, pyspark.sql.types.FloatType):
        return pa.float32()
    elif isinstance(pyspark_type, pyspark.sql.types.BooleanType):
        return pa.bool_()
    elif isinstance(pyspark_type, pyspark.sql.types.DateType):
        return pa.date32()
    elif isinstance(pyspark_type, pyspark.sql.types.TimestampType):
        return pa.timestamp("us")
    elif isinstance(pyspark_type, pyspark.sql.types.TimestampNTZType):
        return pa.timestamp("us")
    elif isinstance(pyspark_type, pyspark.sql.types.BinaryType):
        return pa.binary()
    elif isinstance(pyspark_type, pyspark.sql.types.DecimalType):
        return pa.decimal128(pyspark_type.precision, pyspark_type.scale)
    elif isinstance(pyspark_type, pyspark.sql.types.ArrayType):
        element_type = map_pyspark_types_to_pyarrow_types(pyspark_type.elementType)
        return pa.list_(element_type)
    elif isinstance(pyspark_type, pyspark.sql.types.MapType):
        key_type = map_pyspark_types_to_pyarrow_types(pyspark_type.keyType)
        value_type = map_pyspark_types_to_pyarrow_types(pyspark_type.valueType)
        return pa.map_(key_type, value_type)
    elif isinstance(pyspark_type, pyspark.sql.types.StructType):
        fields = [
            pa.field(
                f.name,
                map_pyspark_types_to_pyarrow_types(f.dataType),
                nullable=f.nullable,
            )
            for f in pyspark_type.fields
        ]
        return pa.struct(fields)
    else:
        return pa.string()  # Default fallback


def map_simple_types(simple_type: str) -> snowpark.types.DataType:
    """
    Map a simple type string to z Snowpark data type.
    """
    match simple_type.lower():
        case "null":
            return snowpark.types.NullType()
        case "binary":
            return snowpark.types.BinaryType()
        case "boolean" | "bool":
            return snowpark.types.BooleanType()
        case "byte":
            return snowpark.types.ByteType()
        case "number":
            return snowpark.types.DoubleType()
        case "short":
            return snowpark.types.ShortType()
        case "integer" | "int":
            return snowpark.types.IntegerType()
        case "long":
            return snowpark.types.LongType()
        case "float":
            return snowpark.types.FloatType()
        case "double":
            return snowpark.types.DoubleType()
        case "string" | "str":
            return snowpark.types.StringType()
        case "char":
            return snowpark.types.StringType()
        case "var_char":
            return snowpark.types.StringType()
        case "date":
            return snowpark.types.DateType()
        case "timestamp":
            return snowpark.types.TimestampType()
        case "timestamp_ntz":
            return snowpark.types.TimestampType(snowpark.types.TimestampTimeZone.NTZ)
        case "timestamp_ltz":
            return snowpark.types.TimestampType(snowpark.types.TimestampTimeZone.LTZ)
        case "year_month_interval":
            return snowpark.types.YearMonthIntervalType()
        case "day_time_interval":
            return snowpark.types.DayTimeIntervalType()
        case type_name if _INTERVAL_YEARMONTH_PATTERN_RE.match(type_name):
            return snowpark.types.YearMonthIntervalType()
        case type_name if _INTERVAL_DAYTIME_PATTERN_RE.match(type_name):
            return snowpark.types.DayTimeIntervalType()
        # Year-Month interval cases
        case "interval year":
            return snowpark.types.YearMonthIntervalType(0)
        case "interval month":
            return snowpark.types.YearMonthIntervalType(1)
        case "interval year to month":
            return snowpark.types.YearMonthIntervalType(0, 1)
        case "interval day":
            return snowpark.types.DayTimeIntervalType(0)
        case "interval hour":
            return snowpark.types.DayTimeIntervalType(1)
        case "interval minute":
            return snowpark.types.DayTimeIntervalType(2)
        case "interval second":
            return snowpark.types.DayTimeIntervalType(3)
        case "interval day to hour":
            return snowpark.types.DayTimeIntervalType(0, 1)
        case "interval day to minute":
            return snowpark.types.DayTimeIntervalType(0, 2)
        case "interval day to second":
            return snowpark.types.DayTimeIntervalType(0, 3)
        case "interval hour to minute":
            return snowpark.types.DayTimeIntervalType(1, 2)
        case "interval hour to second":
            return snowpark.types.DayTimeIntervalType(1, 3)
        case "interval minute to second":
            return snowpark.types.DayTimeIntervalType(2, 3)
        case _:
            if simple_type.startswith("decimal"):
                precision = int(simple_type.split("(")[1].split(",")[0])
                scale = int(simple_type.split(",")[1].split(")")[0])
                return snowpark.types.DecimalType(precision, scale)
            exception = SnowparkConnectNotImplementedError(
                f"Unsupported simple type: {simple_type}"
            )
            attach_custom_error_code(exception, ErrorCodes.UNSUPPORTED_OPERATION)
            raise exception


def map_json_schema_to_snowpark(
    schema: dict | str, quote_struct_fields_names: bool = True
) -> snowpark.types.StructType:
    """
    Map a JSON schema to a Snowpark schema.

    Because of inconsistencies in how the schema is represented in the JSON,
    we need to handle both the case where the schema is a string and the case
    where it is a dictionary. We have a separate function to handle the string
    case, but it is necessary to handle both cases here because types can be nested
    json objects or strings.
    """
    if isinstance(schema, str):
        return map_simple_types(schema)
    match schema.get("type", None):
        case "struct":
            return snowpark.types.StructType(
                [
                    snowpark.types.StructField(
                        # quote the names to escape any special charaters in the field names.
                        (
                            quote_name(field["name"], True)
                            if quote_struct_fields_names
                            else field["name"]
                        ),
                        map_json_schema_to_snowpark(
                            field["type"],
                            quote_struct_fields_names=quote_struct_fields_names,
                        ),
                        field.get("nullable", True),
                        _is_column=False,
                    )
                    for field in schema["fields"]
                ],
                structured=STRUCTURED_TYPES_ENABLED,
            )
        case "array":
            return snowpark.types.ArrayType(
                map_json_schema_to_snowpark(
                    schema["elementType"],
                    quote_struct_fields_names=quote_struct_fields_names,
                ),
                structured=STRUCTURED_TYPES_ENABLED,
                contains_null=schema["containsNull"],
            )
        case "map":
            return snowpark.types.MapType(
                key_type=map_json_schema_to_snowpark(
                    schema["keyType"],
                    quote_struct_fields_names=quote_struct_fields_names,
                ),
                value_type=map_json_schema_to_snowpark(
                    schema["valueType"],
                    quote_struct_fields_names=quote_struct_fields_names,
                ),
                structured=STRUCTURED_TYPES_ENABLED,
                value_contains_null=schema["valueContainsNull"],
            )
        case "udt":
            # UDT schemas typically include sqlType field with the underlying type
            if "sqlType" in schema:
                return map_json_schema_to_snowpark(
                    schema["sqlType"],
                    quote_struct_fields_names=quote_struct_fields_names,
                )
            else:
                # Fall back
                return snowpark.types.StringType()
        case _:
            return map_simple_types(schema["type"])


def _map_type_string(
    type_string: str,
) -> tuple[pyspark.sql.types.DataType, snowpark.types.DataType]:
    """
    Map a ddl-string type to a tuple of PySpark data type and a Snowpark data type.
    """

    pyspark_type = _parse_ddl_with_spark_scala(type_string)
    match type_string:
        case "timestamp" if not get_is_evaluating_sql():
            return pyspark_type, get_timestamp_type()
        case "timestamp" | "timestamp_ltz":
            return pyspark_type, TimestampType(TimestampTimeZone.LTZ)
        case _:
            return pyspark_type, map_pyspark_types_to_snowpark_types(pyspark_type)


def map_type_string_to_snowpark_type(type_string: str) -> snowpark.types.DataType:
    _, snowpark_type = _map_type_string(type_string)
    return snowpark_type


def map_type_string_to_proto(
    ddl_string: str,
) -> types_proto.DataType | snowpark.types.DataType:
    """
    Parse a DDL string and return the Proto data type.
    """
    pyspark_type, snowpark_type = _map_type_string(ddl_string)

    column_name_map = None
    if isinstance(pyspark_type, pyspark.sql.types.StructType):
        spark_column_names = [field.name for field in pyspark_type.fields]
        snowpark_column_names = [field.name for field in snowpark_type.fields]

        if len(spark_column_names) == len(snowpark_column_names):
            column_name_map = ColumnNameMap(spark_column_names, snowpark_column_names)

    struct_proto = list(
        snowpark_to_proto_type(snowpark_type, column_name_map).values()
    )[0]

    if isinstance(snowpark_type, snowpark.types.StructType):
        return types_proto.DataType(struct=struct_proto)
    else:
        # Handle non-struct types (arrays, maps, primitives, etc.)
        proto_type_mapping = snowpark_to_proto_type(snowpark_type, column_name_map)
        proto_field_name = list(proto_type_mapping.keys())[0]
        return types_proto.DataType(**{proto_field_name: struct_proto})


def map_spark_timestamp_format_expression(
    arguments: expressions_pb2.Expression,
    timestamp_input_type: snowpark.types.DataType | None = None,
) -> str:
    """
    Converts a Spark date-time format expression to a Snowflake date-time format string.

    :param arguments: Spark date-time format literal expression
    :return: Equivalent Snowflake date-time format string
    """
    match arguments.WhichOneof("expr_type"):
        case "literal":
            lit_value, _ = get_literal_field_and_name(arguments.literal)
            return convert_spark_format_to_snowflake(lit_value, timestamp_input_type)
        case other:
            exception = SnowparkConnectNotImplementedError(
                f"Unsupported expression type {other} in timestamp format argument"
            )
            attach_custom_error_code(exception, ErrorCodes.UNSUPPORTED_OPERATION)
            raise exception


def map_spark_number_format_expression(
    arguments: expressions_pb2.Expression | str,
) -> str:
    """
    Converts a Spark Number format expression to a Snowflake Number format string.

    :param arguments: Spark Number format literal expression or a literal String
    :return: Equivalent Snowflake Number format string
    """
    if isinstance(arguments, str):
        lit_value = arguments
    else:
        match arguments.WhichOneof("expr_type"):
            case "literal":
                lit_value, _ = get_literal_field_and_name(arguments.literal)
            case other:
                exception = SnowparkConnectNotImplementedError(
                    f"Unsupported expression type {other} in number format argument"
                )
                attach_custom_error_code(exception, ErrorCodes.UNSUPPORTED_OPERATION)
                raise exception

    return _map_spark_to_snowflake_number_format(lit_value)


TIMESTAMP_FORMAT_RE = re.compile(r"(\w)\1*")
NUMBER_FORMAT_RE = re.compile(r"(\w)\1*")


def _map_spark_to_snowflake_number_format(spark_format: str) -> str:
    """
    Converts a Spark Number format string to a Snowflake number format string.

    :param spark_format: Spark Number format string
    :return: Equivalent Snowflake Number format string
    """
    # Mapping of Spark format to Snowflake format
    format_mapping = {
        "S": "MI",  # Optional number sign
    }

    def _replace(m: re.Match) -> str:
        ret = format_mapping.get(m.group(0))
        if ret is None:
            ret = m.group(0)
        return ret

    return NUMBER_FORMAT_RE.sub(_replace, spark_format)


def map_type_to_snowflake_type(
    t: Union[snowpark_type.DataType, types_proto.DataType]
) -> str:
    """Maps a Snowpark or Spark protobuf type to a Snowflake type string."""
    if not t:
        return "VARCHAR"
    is_snowpark_type = isinstance(t, snowpark_type.DataType)
    condition = type(t) if is_snowpark_type else t.WhichOneof("kind")
    match condition:
        case snowpark_type.ArrayType | "array":
            return (
                f"ARRAY({map_type_to_snowflake_type(t.element_type)})"
                if is_snowpark_type
                else f"ARRAY({map_type_to_snowflake_type(t.array.element_type)})"
            )
        case snowpark_type.BinaryType | "binary":
            return "BINARY"
        case snowpark_type.BooleanType | "boolean":
            return "BOOLEAN"
        case snowpark_type.ByteType | "byte":
            return "TINYINT"
        case snowpark_type.DateType | "date":
            return "DATE"
        case snowpark_type.DecimalType | "decimal":
            return "NUMBER"
        case snowpark_type.DoubleType | "double":
            return "DOUBLE"
        case snowpark_type.FloatType | "float":
            return "FLOAT"
        case snowpark_type.GeographyType:
            return "GEOGRAPHY"
        case snowpark_type.IntegerType | "integer":
            return "INT"
        case snowpark_type.LongType | "long":
            return "BIGINT"
        case snowpark_type.MapType | "map":
            # Maps to OBJECT in Snowflake if key and value types are not specified.
            key_type = (
                map_type_to_snowflake_type(t.key_type)
                if is_snowpark_type
                else map_type_to_snowflake_type(t.map.key_type)
            )
            value_type = (
                map_type_to_snowflake_type(t.value_type)
                if is_snowpark_type
                else map_type_to_snowflake_type(t.map.value_type)
            )
            return (
                f"MAP({key_type}, {value_type})"
                if key_type and value_type
                else "OBJECT"
            )
        case snowpark_type.NullType | "null":
            return "VARCHAR"
        case snowpark_type.ShortType | "short":
            return "SMALLINT"
        case snowpark_type.StringType | "string" | "char" | "varchar":
            return "VARCHAR"
        case snowpark_type.TimestampType | "timestamp" | "timestamp_ntz":
            return "TIMESTAMP"
        case snowpark_type.StructType | "struct":
            return "VARIANT"
        case snowpark_type.VariantType:
            return "VARIANT"
        case _:
            exception = ValueError(f"Unsupported Snowpark type: {t}")
            attach_custom_error_code(exception, ErrorCodes.UNSUPPORTED_TYPE)
            raise exception


def merge_different_types(
    type1: snowpark_type.DataType,
    type2: snowpark_type.DataType,
) -> snowpark_type.DataType:
    """
    Merge two different Snowpark data types.
    """
    # If one type is NullType, return the other
    if isinstance(type1, snowpark_type.NullType) or type1 is None:
        return type2
    if isinstance(type2, snowpark_type.NullType) or type2 is None:
        return type1

    if type1 == type2:
        return type2
    # Define type hierarchy - from narrowest to widest scope
    # Each set contains types that can be merged to a common type
    numeric_type_hierarchy = [
        # Numeric hierarchy: byte -> short -> int -> long -> decimal -> float -> double
        snowpark_type.ByteType,
        snowpark_type.ShortType,
        snowpark_type.IntegerType,
        snowpark_type.LongType,
        snowpark_type.DecimalType,
        snowpark_type.FloatType,
        snowpark_type.DoubleType,
    ]

    type1_index = next(
        (i for i, t in enumerate(numeric_type_hierarchy) if isinstance(type1, t)), -1
    )
    type2_index = next(
        (i for i, t in enumerate(numeric_type_hierarchy) if isinstance(type2, t)), -1
    )

    if type1_index >= 0 and type2_index >= 0:
        broader_index = max(type1_index, type2_index)
        return numeric_type_hierarchy[broader_index]()

    # No common type found, default to StringType
    return snowpark_type.StringType()
