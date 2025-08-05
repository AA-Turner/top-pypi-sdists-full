import copy
import inspect
import os
from functools import lru_cache
from typing import Any, Optional, Tuple

from logger_local.LoggerLocal import Logger
from logger_local.MetaLogger import module_wrapper
from python_sdk_remote.utilities import get_environment_name
from python_sdk_remote.utilities import our_get_env
from url_remote.environment_name_enum import EnvironmentName

from .constants_src import LOGGER_CONNECTOR_CODE_OBJECT
from .table_columns import table_columns
from .table_definition import table_definition
# from .to_sql_interface import ToSQLInterface
from database_infrastructure_local.to_sql_interface import ToSQLInterface

logger = Logger.create_logger(object=LOGGER_CONNECTOR_CODE_OBJECT)


def get_sql_hostname() -> str:
    sql_hostname = our_get_env("RDS_HOSTNAME")
    return sql_hostname


def get_sql_username() -> str:
    sql_username = our_get_env("RDS_USERNAME")
    return sql_username


def get_sql_password() -> str:
    sql_password = our_get_env("RDS_PASSWORD")
    return sql_password


def get_sql_port() -> str:
    sql_port = our_get_env("RDS_PORT", default="3306")
    return sql_port


def get_ssh_hostname() -> str:
    return our_get_env("SSH_HOSTNAME", raise_if_not_found=False)


def get_ssh_username() -> str:
    ssh_username = our_get_env("SSH_USERNAME", raise_if_empty=True)
    return ssh_username


def get_ssh_port() -> str:
    ssh_port = our_get_env("SSH_PORT", raise_if_empty=True)
    return ssh_port


def get_private_key_file_path() -> str:
    private_key_file_path = our_get_env("PRIVATE_KEY_FILE_PATH", raise_if_empty=True)
    return private_key_file_path


# TODO: class DatabaseMysqlUtils(metaclass=MetaLogger, object=object_database):
def validate_select_table_name(view_table_name: str, is_ignore_duplicate: bool = False) -> None:
    # TODO: try to detect the table name from the view name (with warning)
    if (get_environment_name() not in (EnvironmentName.DVLP1.value, EnvironmentName.PROD1.value)
            and not view_table_name.endswith("_view") and not is_ignore_duplicate):
        raise Exception(
            f"View name must end with '_view' in this environment (got {view_table_name})")


def validate_none_select_table_name(table_name: str) -> None:
    if (get_environment_name() not in (EnvironmentName.DVLP1.value, EnvironmentName.PROD1.value)
            and not table_name.endswith("_table")):
        raise Exception(
            f"Table name must end with '_table' in this environment  (got {table_name})")


# TODO Shall we change it from a function to a method in GenericCrud
def process_insert_data_dict(data_dict: dict | None) -> Tuple[str, str, tuple]:
    """Example:
    Input: {"name": "John", "coordinate": Point(1, 2)}
    Output: ("`name`, `coordinate`",
             "%s, Point(1, 2)",
            ("John", ))
    """
    if not data_dict:
        columns_str, values_str, params = '', '', ()
        return columns_str, values_str, params

    columns = []
    values = []
    params = tuple()

    for key, value in data_dict.items():
        # new_key = f'`{key}`' if '.' in key else key
        if key.startswith("`") and key.endswith("`"):
            new_key = key
        else:
            new_key = f"`{key}`"

        columns.append(new_key)

        is_instance = isinstance(value, ToSQLInterface)

        if is_instance:
            values.append(value.to_sql())
        else:
            values.append('%s')
            params += (value,)

    columns_str = ','.join(columns)
    values_str = ','.join(values)

    return columns_str, values_str, params


def process_upsert_data_dict(data_dict: dict | None, compare_with_or: bool,
                             where_compare: str | None = None,
                             params_compare: tuple | None = None) -> Tuple[str, tuple]:

    where_clauses = []
    params = []
    for column, value in data_dict.items():
        if isinstance(value, list):
            where_clauses.append(f"({' OR '.join([f'{column}=%s' for _ in value])})")
            params.extend(value)
        elif isinstance(value, ToSQLInterface):
            where_clauses.append(f"{column}={value.to_sql()}")
        elif value is None:
            where_clauses.append(f"{column} IS NULL")
        else:
            where_clauses.append(f"{column}=%s")
            params.append(value)

    where_clause = " OR " if compare_with_or else " AND "
    where_clause = where_clause.join(where_clauses)
    if where_compare and params_compare:
        if where_clause:
            where_clause = f"({where_clause}) AND ({where_compare})"
        else:
            where_clause = where_compare
        params += params_compare
    return where_clause, params


def process_update_data_dict(data_dict: dict | None) -> Tuple[str, tuple]:
    """Example:
    Input: {"name": "John", "coordinate": Point(1, 2)}
    Output: ("name=%s, coordinate=Point(1, 2)", ("John", ))
    """
    if not data_dict:
        set_values_str, params = '', {}
        return set_values_str, params

    set_values = []
    params = tuple()
    for key, value in data_dict.items():
        if isinstance(value, ToSQLInterface):
            set_values.append(f"`{key}`={value.to_sql()}")
        else:
            set_values.append(f"`{key}`=%s")
            params += (value,)

    # + "," because we add updated_timestamp in the update query
    set_values_str = ', '.join(set_values) + ","
    return set_values_str, params


def process_select_data_dict(data_dict: dict | None, select_with_or: bool = False) -> Tuple[str, tuple]:
    """Example:
    Input: {"name": "John", "coordinate": Point(1, 2)}
    Output: ("name=%s AND coordinate=Point(1, 2)", ("John", ))
    """
    if not data_dict:
        where_clause, params = '', {}
        return where_clause, params

    where_clauses = []
    params = tuple()
    for key, value in data_dict.items():
        if isinstance(value, list):
            where_clauses.append(f"({' OR '.join([f'{key}=%s' for _ in value])})")
            params += tuple(value)
        elif isinstance(value, ToSQLInterface):
            where_clauses.append(f"{key}={value.to_sql()}")
        elif value is None:
            where_clauses.append(f"{key} IS NULL")
        else:
            where_clauses.append(f"{key}=%s")
            params += (value,)

    where_clause = " OR " if select_with_or else " AND "
    where_clause = where_clause.join(where_clauses)
    return where_clause, params


@lru_cache
def detect_if_is_test_data() -> bool:
    """Check if running from a Unit Test file."""
    possible_current_files = [os.path.basename(frame.filename) for frame in inspect.stack()]
    is_test_data = any(file_name.startswith('test_') or file_name.endswith('_test.py') or "pytest" in file_name
                       for file_name in possible_current_files)
    return is_test_data


def get_entity_type_ids_by_table_name(table_name: str) -> int | None:
    """Get the entity_type_id1 and entity_type_id2 from the table_definition by table_name **IF** the table is many-to-many.

    :param table_name: The name of the table.
    :return: A tuple of entity_type_id1 and entity_type_id2 if the table is many-to-many, otherwise None.
    """
    entity_type_id1 = get_entity_type_id1_by_table_name(table_name)
    entity_type_id2 = get_entity_type_id2_by_table_name(table_name)

    if entity_type_id1 is not None and entity_type_id2 is not None:
        return entity_type_id1, entity_type_id2
    else:
        logger.warning(f"Table {table_name} is not a many-to-many table, "
                       f"entity_type_id1: {entity_type_id1}, entity_type_id2: {entity_type_id2}. ")
        return None


def get_entity_type_id1_by_table_name(table_name: str) -> int | None:
    """
    get the entity_type_id1 from the table_definition by table_name.

    :param table_name: The name of the table.
    :return: The entity_type_id1 of the table, or None if not found.
    """
    # TODO Should we search for it in entity_type_table or table_definition?

    entity_type_table = table_definition.get(table_name, {})
    entity_type_id1 = entity_type_table.get("entity_type_id1")

    return entity_type_id1


def get_entity_type_id2_by_table_name(table_name: str) -> int | None:
    """
    get the entity_type_id2 from the table_definition by table_name.

    :param table_name: The name of the table.
    :return: The entity_type_id2 of the table, or None if not found.
    """
    entity_type_table = table_definition.get(table_name, {})

    entity_type_id2 = entity_type_table.get("entity_type_id2")
    return entity_type_id2


# def generate_table_name(entity_name: Optional[str],
#                         schema_name: Optional[str]) -> Optional[str]:
#     if entity_name:
#         table_name = entity_name + "_table"
#         return table_name
#     if schema_name:
#         table_name = schema_name + "_table"
#         return table_name


def generate_table_name(entity_name: str = None,
                        schema_name: str = None,
                        ml_table_name: str = None) -> str:
    if ml_table_name:
        table_name = (ml_table_name or "").replace("_ml", "")
    elif entity_name:
        table_name = entity_name + "_table"
    elif schema_name:
        table_name = schema_name + "_table"
    else:
        # Sometime we create GenericCrudMl with no parameters
        # print("Could not generate table name", file=sys.stderr)
        table_name = None
    return table_name


def generate_view_name(table_name: Optional[str]) -> Optional[str]:
    if table_name:
        view_name = table_name.replace("_table", "_view")
    else:
        view_name = table_name
    return view_name


def generate_id_column_name(table_name: Optional[str]) -> Optional[str]:
    if table_name:
        column_name = table_name.replace("_table", "_id")
        return column_name


def validate_single_clause_value(select_clause_value: str = None) -> None:
    if not select_clause_value or "," in select_clause_value or select_clause_value == "*":
        raise ValueError(f"select value requires a single column name, got {select_clause_value}")


def get_where_params(column_name: str, column_value: Any) -> tuple:
    # If we use "if column_value:" it will not work for 0, False, etc.
    if not column_name:
        raise ValueError(f"column_name is required, got {column_name}")
    if isinstance(column_value, ToSQLInterface):
        where = f"`{column_name}`={column_value.to_sql()}"
        params = None
    elif column_value is not None:
        if isinstance(column_value, (list, tuple, set)):
            where = f"`{column_name}` IN (" + ",".join(["%s"] * len(column_value)) + ")"
            params = tuple(column_value)
        else:
            where = f"`{column_name}`=%s"
            params = (column_value,)
    else:
        where = f"`{column_name}` IS NULL"
        params = None
    return where, params


def where_skip_null_values(where: str | None, select_clause_value: str,
                           skip_null_values: bool = True) -> str:
    if skip_null_values:
        validate_single_clause_value(select_clause_value)
        where_skip = f"`{select_clause_value}` IS NOT NULL"
        if where:
            where += f" AND {where_skip}"
        else:
            where = where_skip
    return where


@lru_cache(maxsize=64)
def replace_view_with_table(view_table_name: str, select_clause_value: str = None) -> str:
    # test data does not appear in the view, but we still wants to access it in tests.
    if not view_table_name:
        return view_table_name
    # Guess the table name from the view name:
    table_name = remove_tag(view_table_name.replace("_view", "_table"))
    scan_table_definition_for_table_name = table_definition.get(table_name, {}).get("view_name") != view_table_name
    if scan_table_definition_for_table_name:
        for table, values in table_definition.items():
            if values["view_name"] == view_table_name:
                table_name = table  # got a better guess
                break
    if select_clause_value and select_clause_value != "*":
        required_columns = tuple(col.strip() for col in select_clause_value.split(","))  # if columns are specified
    else:
        required_columns = table_columns.get(view_table_name, [])  # all columns in the view

    # Replace 'ST_X(coordinate)' and 'ST_Y(coordinate)' with 'coordinate'
    required_columns = tuple('coordinate' if col in ('ST_X(coordinate)', 'ST_Y(coordinate)') else
                             remove_tag(col) for col in required_columns)

    # TODO if (is_debug) # Less optimized for runtime, better for debug
    if table_name in table_columns:
        all_columns_present = True
        for col in required_columns:
            if remove_tag(col) not in table_columns.get(table_name, []):
                all_columns_present = False
                logger.warning(f"Column {col} not found in table {table_name}. check the columns in select clause value if they exist in the table.")
                break

        if all_columns_present:
            view_table_name = table_name

    # if !is_debug # More optimized for runtime, less for debug
    # if table_name in table_columns and all(  # if all required columns from the view present in the table.
    #         remove_tag(col) in table_columns.get(table_name, []) for col in requiered_columns):
    #     view_table_name = table_name

    return view_table_name  # appropriate table not found


def remove_tag(name: str) -> str:
    name_without_tag = name.replace("`", "")
    return name_without_tag


def insert_is_undelete(table_name: str) -> bool:
    is_undelete = table_definition.get(table_name, {}).get("insert_is_undelete")
    return is_undelete


def is_end_timestamp_in_table(table_name: str) -> bool:
    # table_definition outdated for now.
    # is_end_timestamp_in_table = table_definition.get(table_name, {}).get("end_timestamp")
    is_end_timestamp_in_table = is_column_in_table(table_name, "end_timestamp")
    return is_end_timestamp_in_table


def is_column_in_table(table_name: str, column_name: str) -> bool:
    columns = table_columns.get(table_name, [])
    column_in_table = remove_tag(column_name) in columns
    return column_in_table


def get_table_columns(table_name: str = None) -> tuple:
    table_columns_tuple = table_columns.get(table_name, [])
    return table_columns_tuple


def group_list_by_columns(list_of_dicts: list, group_by: str, condense: bool = True) -> dict[tuple | str, list]:
    """if condense is True and there is only one column left in the dict, return the value instead of the dict.
    Examples:
    Input: [{"name": "John", "age": 25}, {"name": "John", "age": 26}], group_by="name"
            -> {"John": [25, 26]}
    Input: [{"name": "John", "age": 25}, {"name": "John", "age": 26}], group_by="name", condense=False
            -> {"John": [{"age": 25}, {"age": 26}]}
    Input: [{"a": 1, "b": 2, "c": 3}, {"a": 1, "b": 2, "c": 4}, {"a": 2, "b": 2, "c": 5}], group_by="a"
            -> {1: [{"b": 2, "c": 3}, {"b": 2, "c": 4}], 2: [{"b": 2, "c": 5}]}
    Input: [{"a": 1, "b": 2, "c": 3}, {"a": 1, "b": 2, "c": 4}, {"a": 2, "b": 2, "c": 5}], group_by="a,b", condense=False
            -> {(1, 2): [{"c": 3}, {"c": 4}], (2, 2): [{"c": 5}]}
    """
    group_by = tuple(map(str.strip, group_by.split(",")))
    grouped = {}
    if not list_of_dicts:
        return grouped
    list_of_dicts = copy.deepcopy(list_of_dicts)
    if any(col not in list_of_dicts[0] for col in group_by):
        raise ValueError(f"{group_by} should be a subset of {tuple(list_of_dicts[0].keys())}")
    if len(group_by) == len(list_of_dicts[0]):
        raise ValueError("Column names in group_by must be less than the number of columns in the list of dicts")

    for dict_row in list_of_dicts:
        key = tuple(dict_row[col] for col in group_by) if len(group_by) > 1 else dict_row[group_by[0]]
        if key not in grouped:
            grouped[key] = []
        for col in group_by:
            dict_row.pop(col)
        grouped[key].append(dict_row if not condense or len(dict_row) > 1 else next(iter(dict_row.values())))
    return grouped


# Not used anymore:
# def extract_duplicated_from_error(error: Exception) -> (Any, str):
# """Error examples:
# - Duplicate entry '1' for key 'test_mysql_table.PRIMARY'  - in such case return the duplicated value, otherwise the column
# - Duplicate entry '7263200721327371865' for key 'test_mysql_table.number_UNIQUE
# - IntegrityError(1062, "1062 (23000): Duplicate entry '202-405-3018' for key 'person_table.person.main_full_number_normalized_UNIQUE'", '23000')
# - Duplicate entry 'test@gmail.com' for key 'email_address_table.email_address.unique'
# - 1062 (23000): Duplicate entry 'tal@circlez.ai' for key 'person_table.person_table.main_email_person.unique'
# - TODO (index can have any name): 1062 (23000): Duplicate entry '1-2' for key 'test_location_profile_table.idx_location_id_profile_id'
# """
# pattern = r'Duplicate entry \'(.+?)\' for key \'(.+?)\''
# match = re.search(pattern, str(error))
# if not match:  # a different error
#     raise error
# duplicate_value = match.group(1)
# key = match.group(2)
# if key.endswith("PRIMARY"):
#     return int(duplicate_value), ""
# elif key.endswith("_UNIQUE"):
#     # all but last
#     duplicate_column_name = "_".join(key.split(".")[-1].split('_')[:-1])
# elif key.count(".") > 1:
#     duplicate_column_name = key.split(".")[-2]
# else:
#     raise Exception(f"GenericCRUD._get_existing_duplicate_id: please report the following error,"
#                     f" so we can add support to this case: insert error: {error}")
# return duplicate_value, duplicate_column_name

def generate_where_clause_for_ignore_duplicate(data_dict: dict, constraint_columns: list[list[str]]) -> Tuple[str, tuple]:
    where_clauses = []
    values = tuple()

    for constraint_column in constraint_columns:
        # Handle special case for 'point' or 'coordinate'
        formatted_columns = []
        temp_values = []

        for column in constraint_column:
            if column in data_dict:
                if column == 'point' or column == 'coordinate':
                    formatted_columns.append('ST_X(coordinate) = %s')
                    temp_values.append(data_dict[column])
                    formatted_columns.append('ST_Y(coordinate) = %s')
                    temp_values.append(data_dict[column])
                else:
                    formatted_columns.append(f"{column} = %s")
                    temp_values.append(data_dict[column])

        if (len(temp_values) == len(constraint_column) *
                (2 if 'point' in constraint_column or 'coordinate' in constraint_column else 1)):
            where_clauses.append(f"({' AND '.join(formatted_columns)})")
            values += tuple(temp_values)

    where = ' OR '.join(where_clauses)
    return where, values


# process field with dot in it
def fix_select_clause_value(select_clause_value: str) -> str:
    """If some fields in select_clause_value have "." in them, we have to surround them with ``."""
    # Split the select clause value by commas to handle multiple fields
    if select_clause_value is None:
        return select_clause_value
    fields = select_clause_value.split(',')

    # Process each field
    fixed_fields = []
    for field in fields:
        field = field.strip()
        if '.' in field and field[0] != '`' and field[-1] != '`':
            field = f'`{field}`'
        fixed_fields.append(field)

    # Join the fixed fields back into a single string
    fixed_select_clause_value = ', '.join(fixed_fields)
    return fixed_select_clause_value


def fix_where_clause_value(where_clause_value: str) -> str:
    """If some fields in where_clause_value have "." in them, we have to surround them with ``."""
    # Split the where clause value by AND or OR to handle multiple conditions
    if where_clause_value is None:
        return where_clause_value
    conditions = where_clause_value.split()

    # Process each condition
    fixed_conditions = []
    for condition in conditions:
        condition_column = condition.split('=')[0].strip()  # Get the column name part of the condition
        if '.' in condition_column and condition_column[0] != '`' and condition_column[-1] != '`':
            condition = condition.replace(condition_column, f'`{condition_column}`')  # Surround the column name with `
        fixed_conditions.append(condition)

    # Join the fixed conditions back into a single string
    fixed_where_clause_value = ' '.join(fixed_conditions)
    return fixed_where_clause_value

# TODO: run this with cache decorator if the above get_table_columns doesn't find anything.
# def get_table_columns(schema_name: str = None, table_name: str = None) -> tuple:
#     select_query = "SELECT column_name " \
#                    "FROM information_schema.columns " \
#                    "WHERE TABLE_SCHEMA = %s " \
#                    "AND TABLE_NAME = %s;"
#     params = (schema_name, table_name)
#
#     self.connection.commit()
#     self.cursor.execute(select_query, params)
#     result = self.cursor.fetchall()
#
#     columns_tuple = tuple(x[0] for x in result)
#     self.logger.debug(object=locals())
#     return columns_tuple


module_wrapper(logger)
