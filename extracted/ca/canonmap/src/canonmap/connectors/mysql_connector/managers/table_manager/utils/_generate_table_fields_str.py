from typing import List

from canonmap.connectors.mysql_connector.utils.mysql_data_types import MySQLDataType
from canonmap.connectors.mysql_connector.managers.table_manager.validators.requests import NewTableField

def generate_table_fields_str(fields: List[NewTableField]) -> str:
    if not fields:
        return "id INT AUTO_INCREMENT PRIMARY KEY"

    col_defs = []
    primary_keys = []

    for field in fields:
        col_defs.append(_generate_column_definition(field))
        if field.is_primary_key:
            primary_keys.append(f"`{field.name}`")

    # If no PK specified, add id INT AUTO_INCREMENT PRIMARY KEY as first column
    if not primary_keys:
        col_defs.insert(0, "id INT AUTO_INCREMENT PRIMARY KEY")
        fields_str = ", ".join(col_defs)
        return fields_str

    # If only one PK, append PRIMARY KEY inline, else add at table level for composite PK
    if len(primary_keys) > 1:
        pk_str = f"PRIMARY KEY ({', '.join(primary_keys)})"
        fields_str = ", ".join(col_defs + [pk_str])
    else:
        # If only one, ensure the inline PRIMARY KEY is present in its col_def
        # (already handled in generate_column_definition)
        fields_str = ", ".join(col_defs)

    return fields_str


def _generate_column_definition(field: NewTableField) -> str:
    # Base type and length
    dtype_sql = field.data_type.value

    # Length specifier if needed
    if MySQLDataType.needs_length_specification(field.data_type.value) and "(" not in field.data_type.value:
        dtype_sql += MySQLDataType.get_default_length(field.data_type.value)
    # Column definition
    col = f"`{field.name}` {dtype_sql}"

    # Column constraints
    constraints = []
    if field.is_not_null:
        constraints.append("NOT NULL")
    if field.is_unique and not field.is_primary_key:
        constraints.append("UNIQUE")
    if field.is_primary_key:
        if MySQLDataType.supports_auto_increment(field.data_type.value):
            constraints.append("AUTO_INCREMENT")
        # We'll declare PRIMARY KEY at the table level if composite, so don't append here

    return f"{col} {' '.join(constraints)}".strip()



