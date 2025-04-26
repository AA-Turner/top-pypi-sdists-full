import re
from typing import Dict, List, Tuple

from tinybird_cdk.schema import Schema

datetime64_type_pattern = r"^DateTime64(\([1-9](, ?'.+')?\))?$"
datetime_type_pattern = r"^DateTime(\(('.+')?)?\)?$"


class NonSupportedMigrationException(Exception):
    pass


def parse_path(sql_query: str) -> Tuple[str, str, str]:
    path = re.search(
        r'.*\s+FROM\s+`?([^\s`]+)\.([^\s`]+)\.([^\s`]+)`?', sql_query, re.IGNORECASE).groups()
    return (path[0], path[1], path[2])


def get_migration(tb_schema, bq_schema) -> Tuple[str, List[str]]:
    tb_columns = tb_schema['columns']
    tb_schema_sql = tb_schema['sql_schema']
    tb_columns_sql = tb_schema_sql.split(', ')
    for c, sql, idx in zip(tb_columns, tb_columns_sql, range(len(tb_columns))):
        c['sql'] = sql
        c['index'] = idx

    tb_external_columns = list(
        filter(lambda x: not x.get('auto', False), tb_columns))

    alter_schema, columns = _build_alter_schema(tb_external_columns, bq_schema)

    if alter_schema is not None:
        new_tb_schema_sql = (', ').join(alter_schema)
    else:
        new_tb_schema_sql = None

    return (new_tb_schema_sql, columns)


def _is_type_datetime64(type_to_check):
    return re.match(datetime64_type_pattern, type_to_check) is not None


def _is_type_datetime(type_to_check):
    return re.match(datetime_type_pattern, type_to_check) is not None


def _normalize_type(type):
    type_to_check = type
    if _is_type_datetime64(type):
        type_to_check = 'DateTime64'
    elif _is_type_datetime(type):
        type_to_check = 'DateTime'
    return type_to_check


def _are_columns_equivalent(tb_c, bq_c) -> bool:
    tb_type = _normalize_type(tb_c['type'])
    schema_compatible = tb_c['name'].lower() == bq_c.name.lower() \
        and tb_type == bq_c.ch_type.base_name
    return schema_compatible


def _is_changes_in_schema(tb_columns, bq_schema):
    if len(tb_columns) != len(bq_schema.columns):
        return True

    is_changes = False
    for tb_c, bq_c in zip(tb_columns, bq_schema.columns):
        if not _are_columns_equivalent(tb_c, bq_c):
            is_changes = True
            break
    return is_changes


def _build_alter_schema(tb_columns: List[Dict], bq_schema: Schema) -> Tuple[str, List[str]]:

    if not _is_changes_in_schema(tb_columns, bq_schema):
        return None, None

    if len(tb_columns) > len(bq_schema.columns):
        raise NonSupportedMigrationException("Remove columns is not supported")

    def build_column_sql(new_column):
        return f"`{new_column.name}` {new_column.ch_type.name}"

    # All columns in tb should exist in bq
    # Not delete supported
    bq_columns = {c.name.lower(): c for c in bq_schema.columns}
    for c in tb_columns:
        if c['name'].lower() not in [c.name.lower() for c in bq_schema.columns]:
            raise NonSupportedMigrationException(
                f"The field {c['name']} from the Tinybird data source is not on the external table")
        if not _are_columns_equivalent(c, bq_columns[c['name'].lower()]):
            raise NonSupportedMigrationException(
                f"The field {c['name']} from the Tinybird data source is not equivalent to the one on the external table")

    final_column_list = []
    tb_columns_dict = {c['name'].lower(): c for c in tb_columns}
    columns = []
    for bq_column in bq_schema.columns:
        if bq_column.name.lower() in tb_columns_dict:
            tb_column = tb_columns_dict[bq_column.name.lower()]
            final_column_list.append(tb_column['sql'])
        else:
            final_column_list.append(build_column_sql(bq_column))
        columns.append(bq_column.name)
    return (final_column_list, columns)
