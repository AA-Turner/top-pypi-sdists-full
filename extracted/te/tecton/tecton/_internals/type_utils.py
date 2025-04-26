from typing import Sequence

from pyspark.sql import types as spark_types

from tecton import types as sdk_types
from tecton_core import data_types as tecton_types
from tecton_proto.common import schema__client_pb2 as schema_pb2
from tecton_spark.spark_schema_wrapper import SparkSchemaWrapper


def to_column(field: sdk_types.Field) -> schema_pb2.Column:
    data_type = field.tecton_type().proto.data_type
    return schema_pb2.Column(name=field.name, offline_data_type=data_type)


def to_tecton_schema(fields: Sequence[sdk_types.Field]) -> schema_pb2.Schema:
    columns = [to_column(field) for field in fields]
    return schema_pb2.Schema(columns=columns)


def to_spark_schema_wrapper(field_list: Sequence[sdk_types.Field]) -> SparkSchemaWrapper:
    s = spark_types.StructType([field.spark_type() for field in field_list])
    return SparkSchemaWrapper(s)


def sdk_type_from_tecton_type(data_type: tecton_types.DataType) -> sdk_types.SdkDataType:
    if isinstance(data_type, tecton_types.Int32Type):
        return sdk_types.Int32
    elif isinstance(data_type, tecton_types.Int64Type):
        return sdk_types.Int64
    elif isinstance(data_type, tecton_types.Float32Type):
        return sdk_types.Float32
    elif isinstance(data_type, tecton_types.Float64Type):
        return sdk_types.Float64
    elif isinstance(data_type, tecton_types.StringType):
        return sdk_types.String
    elif isinstance(data_type, tecton_types.BoolType):
        return sdk_types.Bool
    elif isinstance(data_type, tecton_types.TimestampType):
        return sdk_types.Timestamp
    elif isinstance(data_type, tecton_types.ArrayType):
        return sdk_types.Array(sdk_type_from_tecton_type(data_type.element_type))
    elif isinstance(data_type, tecton_types.StructType):
        fields = [sdk_types.Field(field.name, sdk_type_from_tecton_type(field.data_type)) for field in data_type.fields]
        return sdk_types.Struct(fields)
    elif isinstance(data_type, tecton_types.MapType):
        return sdk_types.Map(
            sdk_type_from_tecton_type(data_type.key_type), sdk_type_from_tecton_type(data_type.value_type)
        )
    else:
        msg = f"{data_type} is not a recognized data types."
        raise NotImplementedError(msg)


def _schema_pretty_str_helper(schema, indent=0, schema_str=""):
    if isinstance(schema, Sequence):
        schema_str += (" " * indent) + "[\n"
        for item in schema:
            schema_str += _schema_pretty_str_helper(item, indent + 4)
        schema_str = schema_str[:-2] + "\n"  # remove trailing comma
        schema_str += " " * indent + "]\n"
    elif isinstance(schema, sdk_types.Field):
        schema_str += (" " * indent) + f"Field('{schema.name}', "
        schema_str += _schema_pretty_str_helper(schema.dtype, indent + 4)
        schema_str += "),\n"
    elif isinstance(schema, sdk_types.Struct):
        schema_str += "Struct(\n"
        schema_str += _schema_pretty_str_helper(schema.fields, indent + 4)
        schema_str += " " * indent + ")"
    elif isinstance(schema, sdk_types.Array):
        schema_str += "Array("
        schema_str += _schema_pretty_str_helper(schema.element_type, indent + 4)
        schema_str += ")"
    elif isinstance(schema, sdk_types.Map):
        schema_str += f"Map({_schema_pretty_str_helper(schema.key_type, indent)}, {_schema_pretty_str_helper(schema.value_type, indent)})"
    elif isinstance(schema, sdk_types.SdkDataType):
        schema_str += repr(schema)
    else:
        msg = f"Unknown type: {type(schema)}"
        raise ValueError(msg)

    return schema_str


def schema_pretty_str(schema: Sequence[sdk_types.Field]) -> str:
    """Returns a pretty, multi-line formatted string"""
    return _schema_pretty_str_helper(schema)[:-1]  # remove trailing new line character
