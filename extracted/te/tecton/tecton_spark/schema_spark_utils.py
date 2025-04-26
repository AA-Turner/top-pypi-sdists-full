from typing import List
from typing import Tuple

import pyspark.sql.types as spark_types

from tecton_core import schema as core_schema
from tecton_core.data_types import ArrayType
from tecton_core.data_types import BoolType
from tecton_core.data_types import DataType
from tecton_core.data_types import Float32Type
from tecton_core.data_types import Float64Type
from tecton_core.data_types import Int32Type
from tecton_core.data_types import Int64Type
from tecton_core.data_types import MapType
from tecton_core.data_types import StringType
from tecton_core.data_types import StructField
from tecton_core.data_types import StructType
from tecton_core.data_types import TimestampType
from tecton_core.schema import Schema
from tecton_proto.common.schema__client_pb2 import Schema as SchemaProto


SUPPORTED_DATA_TYPES_DOCUMENTATION_LINK = "https://docs.tecton.ai/docs/sdk-reference/data-types"

# Keep in sync with DataTypeUtils.kt and tecton_core/schema_derivation_utils. . Use "simple strings" as the keys so that fields like "nullable" are ignored.
PRIMITIVE_SPARK_TYPE_SIMPLE_STRING_TO_TECTON_TYPE = {
    spark_types.StringType().simpleString(): StringType(),
    spark_types.LongType().simpleString(): Int64Type(),
    spark_types.FloatType().simpleString(): Float32Type(),
    spark_types.DoubleType().simpleString(): Float64Type(),
    spark_types.BooleanType().simpleString(): BoolType(),
    spark_types.IntegerType().simpleString(): Int32Type(),
    spark_types.TimestampType().simpleString(): TimestampType(),
}

# Map from simple (i.e non-complex) Tecton data types to Spark Types.
PRIMITIVE_TECTON_DATA_TYPE_TO_SPARK_DATA_TYPE = {
    Int32Type(): spark_types.IntegerType(),
    Int64Type(): spark_types.LongType(),
    Float32Type(): spark_types.FloatType(),
    Float64Type(): spark_types.DoubleType(),
    StringType(): spark_types.StringType(),
    BoolType(): spark_types.BooleanType(),
    TimestampType(): spark_types.TimestampType(),
}


def schema_from_spark(spark_schema: spark_types.StructType) -> Schema:
    proto = SchemaProto()
    for field in spark_schema:
        column = proto.columns.add()
        spark_datatype = field.dataType
        try:
            tecton_type = tecton_data_type_from_spark_data_type(spark_datatype)
        except ValueError:
            # Re-raise this error here because
            # a) we have the feature column name and
            # b) in the case of complex data type with a nested type error, can show the full data type.
            raise ValueError(
                f"Field {field.name} is of type {spark_datatype.simpleString()}, which is not a supported type for features. "
                + f"Please change {field.name} to be one of our supported types: {SUPPORTED_DATA_TYPES_DOCUMENTATION_LINK}"
            )
        column.CopyFrom(core_schema.column_from_tecton_data_type(tecton_type))
        column.name = field.name

    return Schema(proto)


def tecton_data_type_from_spark_data_type(spark_datatype: spark_types.DataType) -> DataType:
    if isinstance(spark_datatype, spark_types.StructType):
        struct_fields = []
        for field in spark_datatype:
            tecton_type = tecton_data_type_from_spark_data_type(field.dataType)
            struct_fields.append(StructField(field.name, tecton_type))
        return StructType(struct_fields)
    elif isinstance(spark_datatype, spark_types.ArrayType):
        return ArrayType(tecton_data_type_from_spark_data_type(spark_datatype.elementType))
    elif isinstance(spark_datatype, spark_types.MapType):
        return MapType(
            tecton_data_type_from_spark_data_type(spark_datatype.keyType),
            tecton_data_type_from_spark_data_type(spark_datatype.valueType),
        )
    elif spark_datatype.simpleString() in PRIMITIVE_SPARK_TYPE_SIMPLE_STRING_TO_TECTON_TYPE:
        return PRIMITIVE_SPARK_TYPE_SIMPLE_STRING_TO_TECTON_TYPE[spark_datatype.simpleString()]
    else:
        msg = f"{spark_datatype.simpleString()} is not a supported type for features. Please review our supported feature types: {SUPPORTED_DATA_TYPES_DOCUMENTATION_LINK}"
        raise ValueError(msg)


def spark_data_type_from_tecton_data_type(tecton_data_type: DataType) -> spark_types.DataType:
    if tecton_data_type in PRIMITIVE_TECTON_DATA_TYPE_TO_SPARK_DATA_TYPE:
        return PRIMITIVE_TECTON_DATA_TYPE_TO_SPARK_DATA_TYPE[tecton_data_type]
    elif isinstance(tecton_data_type, ArrayType):
        element_type = spark_data_type_from_tecton_data_type(tecton_data_type.element_type)
        return spark_types.ArrayType(element_type)
    elif isinstance(tecton_data_type, StructType):
        spark_struct = spark_types.StructType()
        for field in tecton_data_type.fields:
            spark_struct.add(field.name, spark_data_type_from_tecton_data_type(field.data_type))
        return spark_struct
    elif isinstance(tecton_data_type, MapType):
        return spark_types.MapType(
            spark_data_type_from_tecton_data_type(tecton_data_type.key_type),
            spark_data_type_from_tecton_data_type(tecton_data_type.value_type),
        )
    else:
        assert False, f"Unsupported type: {tecton_data_type}"


def schema_to_spark(schema: Schema) -> spark_types.StructType:
    ret = spark_types.StructType()
    for col_name, col_spark_data_type in column_name_spark_data_types(schema):
        ret.add(col_name, col_spark_data_type)
    return ret


def column_name_spark_data_types(schema: Schema) -> List[Tuple[str, spark_types.DataType]]:
    return [(c[0], spark_data_type_from_tecton_data_type(c[1])) for c in schema.column_name_and_data_types()]
