from fivetran_connector_sdk.protos import common_pb2
from fivetran_connector_sdk_common.constants import TABLES
from fivetran_connector_sdk_common.helpers import _validate_table_name


def process_tables(response, table_list):
    for entry in response:
        if 'table' not in entry:
            raise ValueError("Entry missing table name: " + entry)

        table_name = entry['table']

        _validate_table_name(table_name)

        if table_name in table_list:
            raise ValueError("Table already defined: " + table_name)

        table = common_pb2.Table(name=table_name)
        columns = {}

        if "primary_key" in entry:
            process_primary_keys(columns, entry)

        if "columns" in entry:
            process_columns(columns, entry)

        table.columns.extend(columns.values())
        TABLES[table_name] = table
        table_list[table_name] = table


def process_primary_keys(columns, entry):
    for column_name in entry["primary_key"]:
        column = columns[column_name] if column_name in columns else common_pb2.Column(name=column_name)
        column.primary_key = True
        columns[column_name] = column


def process_columns(columns, entry):
    for column_name, type in entry["columns"].items():
        column = columns[column_name] if column_name in columns else common_pb2.Column(name=column_name)

        if isinstance(type, str):
            process_data_type(column, type)

        elif isinstance(type, dict):
            if type['type'].upper() != "DECIMAL":
                error_message = (
                    f"Expecting DECIMAL data type for dictionary column entry, but got: {type['type']} in entry: {entry} "
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
                f"Unrecognized column type for column: {column_name} in entry: {entry}. Got: {str(type)}"
            )

        if "primary_key" in entry and column_name in entry["primary_key"]:
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
