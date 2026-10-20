from fivetran_connector_sdk.protos import common_pb2
from fivetran_connector_sdk_common import constants
from fivetran_connector_sdk_common.constants import TABLES
from fivetran_connector_sdk_common.helpers import _validate_table_name, _validate_schema


def process_tables(response, table_list):
    # `client.schema()` is called independently from both standardConfig() and update(), so the qualification
    # state is recomputed on every call rather than inherited from an earlier one.
    # schema() and operations may freely mix entries with and without 'schema': entries without it belong to the
    # connection's own schema. Whether any entry is schema-qualified decides the shape of the schema response.
    table_definitions = list(response)
    raw_schemas = [table_definition.get('schema') for table_definition in table_definitions]
    constants.SCHEMA_QUALIFIED = any(raw_schema is not None for raw_schema in raw_schemas)

    for table_definition, raw_schema in zip(table_definitions, raw_schemas):
        if 'table' not in table_definition:
            raise ValueError(f"Entry missing table name: {table_definition}")

        table_name = table_definition['table']

        _validate_table_name(table_name)
        _validate_schema(raw_schema)
        schema_table_key = (raw_schema, table_name)

        if schema_table_key in table_list:
            raise ValueError(f"Table {table_name} already exists in {raw_schema}" if raw_schema else f"Table already defined: {table_name}")

        table = common_pb2.Table(name=table_name)
        columns = {}

        if "primary_key" in table_definition:
            process_primary_keys(columns, table_definition)

        if "columns" in table_definition:
            process_columns(columns, table_definition)

        table.columns.extend(columns.values())
        TABLES[schema_table_key] = table
        table_list[schema_table_key] = table


def process_primary_keys(columns, table_definition):
    for column_name in table_definition["primary_key"]:
        column = columns[column_name] if column_name in columns else common_pb2.Column(name=column_name)
        column.primary_key = True
        columns[column_name] = column


def process_columns(columns, table_definition):
    for column_name, type in table_definition["columns"].items():
        column = columns[column_name] if column_name in columns else common_pb2.Column(name=column_name)

        if isinstance(type, str):
            process_data_type(column, type)

        elif isinstance(type, dict):
            if type['type'].upper() != "DECIMAL":
                error_message = (
                    f"Expecting DECIMAL data type for dictionary column entry, but got: {type['type']} in entry: {table_definition} "
                    f"for column: {column_name}. "
                    "Dictionary type is only allowed for DECIMAL columns with 'precision' and 'scale' fields, "
                    "as in: {'type': 'DECIMAL', 'precision': <int>, 'scale': <int>}. "
                    "For all other data types, use a string as the column type."
                )
                raise ValueError(error_message)
            column.type = common_pb2.DataType.DECIMAL
            column.params.decimal.precision = type['precision']
            column.params.decimal.scale = type['scale']

        else:
            raise ValueError(
                f"Unrecognized column type for column: {column_name} in entry: {table_definition}. Got: {str(type)}"
            )

        if "primary_key" in table_definition and column_name in table_definition["primary_key"]:
            column.primary_key = True

        columns[column_name] = column


def process_data_type(column, type):
    if type.upper() == "BOOLEAN":
        column.type = common_pb2.DataType.BOOLEAN
    elif type.upper() == "SHORT":
        column.type = common_pb2.DataType.SHORT
    elif type.upper() == "INT":
        column.type = common_pb2.DataType.INT
    elif type.upper() == "LONG":
        column.type = common_pb2.DataType.LONG
    elif type.upper() == "DECIMAL":
        raise ValueError(
            "DECIMAL data type missing precision and scale. "
            "Use a dictionary for DECIMAL column type like: "
            '''"col_name": {  # Decimal data type with precision and scale.\n'''
            '''    "type": "DECIMAL",\n'''
            '''    "precision": 15,\n'''
            '''    "scale": 2\n'''
            '''}'''
        )
    elif type.upper() == "FLOAT":
        column.type = common_pb2.DataType.FLOAT
    elif type.upper() == "DOUBLE":
        column.type = common_pb2.DataType.DOUBLE
    elif type.upper() == "NAIVE_DATE":
        column.type = common_pb2.DataType.NAIVE_DATE
    elif type.upper() == "NAIVE_DATETIME":
        column.type = common_pb2.DataType.NAIVE_DATETIME
    elif type.upper() == "UTC_DATETIME":
        column.type = common_pb2.DataType.UTC_DATETIME
    elif type.upper() == "BINARY":
        column.type = common_pb2.DataType.BINARY
    elif type.upper() == "XML":
        column.type = common_pb2.DataType.XML
    elif type.upper() == "STRING":
        column.type = common_pb2.DataType.STRING
    elif type.upper() == "JSON":
        column.type = common_pb2.DataType.JSON
    else:
        raise ValueError("Unrecognized column type encountered:: ", str(type))
