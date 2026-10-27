"""The tables a connector's `schema()` declares, as plain values, and the registry the operations read column types from.

The checks and messages are the same as on Fivetran.
"""
from fivetran_connector_sdk_core.model import Column, DataType, DecimalParams, Table

from fivetran_connector_sdk_common.helpers import _validate_table_name, _validate_schema
from fivetran_connector_sdk_cli import wire

__all__ = ["Column", "DataType", "DecimalParams", "Table", "TABLES", "TABLES_COLUMNS_TYPES", "process_tables", "reset"]


# Keyed by (the schema `schema()` names for the table or None, the table's name)
TABLES = {}
TABLES_COLUMNS_TYPES = {}


def reset():
    """Forgets every declared table (a runner calls this before each sync)."""
    TABLES.clear()
    TABLES_COLUMNS_TYPES.clear()


def _new_column(column_name):
    return Column(name=wire.text(column_name))


def process_tables(response, table_list):
    for entry in response:
        if 'table' not in entry:
            raise ValueError(f"Entry missing table name: {entry}")

        table_name = entry['table']
        raw_schema = entry.get('schema')

        _validate_table_name(table_name)
        _validate_schema(raw_schema)
        schema_table_key = (raw_schema, table_name)

        if schema_table_key in table_list:
            raise ValueError(f"Table {table_name} already exists in {raw_schema}" if raw_schema else f"Table already defined: {table_name}")

        table = Table(name=wire.text(table_name), schema=wire.optional_text(raw_schema))
        columns = {}

        if "primary_key" in entry:
            process_primary_keys(columns, entry)

        if "columns" in entry:
            process_columns(columns, entry)

        table.columns.extend(columns.values())
        TABLES[schema_table_key] = table
        table_list[schema_table_key] = table


def process_primary_keys(columns, entry):
    for column_name in entry["primary_key"]:
        column = columns[column_name] if column_name in columns else _new_column(column_name)
        column.primary_key = True
        columns[column_name] = column


def process_columns(columns, entry):
    for column_name, type in entry["columns"].items():
        column = columns[column_name] if column_name in columns else _new_column(column_name)

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
            missing = [key for key in ("precision", "scale") if key not in type]
            if missing:
                raise ValueError(
                    f"DECIMAL column '{column_name}' is missing {' and '.join(repr(key) for key in missing)}. "
                    "Give both its precision and its scale, as in: {'type': 'DECIMAL', 'precision': 15, 'scale': 2}"
                )
            column.type = DataType.DECIMAL
            column.decimal = column.decimal or DecimalParams()
            column.decimal.precision = wire.integer(type['precision'], bits=32, signed=False, unset_if_none=False)
            column.decimal.scale = wire.integer(type['scale'], bits=32, signed=False, unset_if_none=False)

        else:
            raise ValueError(
                f"Unrecognized column type for column: {column_name} in entry: {entry}. Got: {str(type)}"
            )

        if "primary_key" in entry and column_name in entry["primary_key"]:
            column.primary_key = True

        columns[column_name] = column


_SIMPLE_TYPES = {
    "BOOLEAN": DataType.BOOLEAN, "SHORT": DataType.SHORT, "INT": DataType.INT, "LONG": DataType.LONG,
    "FLOAT": DataType.FLOAT, "DOUBLE": DataType.DOUBLE, "NAIVE_DATE": DataType.NAIVE_DATE,
    "NAIVE_DATETIME": DataType.NAIVE_DATETIME, "UTC_DATETIME": DataType.UTC_DATETIME, "BINARY": DataType.BINARY,
    "XML": DataType.XML, "STRING": DataType.STRING, "JSON": DataType.JSON,
}


def process_data_type(column, type):
    if type.upper() in _SIMPLE_TYPES:
        column.type = _SIMPLE_TYPES[type.upper()]
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
    else:
        raise ValueError("Unrecognized column type encountered:: ", str(type))
