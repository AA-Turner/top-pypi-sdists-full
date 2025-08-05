from datetime import datetime, timezone
from functools import lru_cache
import sys
from typing import Any, Optional

import mysql.connector
from database_infrastructure_local.number_generator import NumberGenerator
from database_infrastructure_local.generic_crud_abstract import GenericCrudAbstract
from database_infrastructure_local.constants import DEFAULT_SQL_SELECT_LIMIT
from logger_local.MetaLogger import ABCMetaLogger
from user_context_remote.user_context import UserContext
from python_sdk_remote.our_object import OurObject

from .connector import Connector
# from .generic_crud_abstract import DEFAULT_SQL_SELECT_LIMIT
from .constants_src import CRUD_MYSQL_CODE_LOGGER_OBJECT
from .cursor import Cursor
from .table_definition import table_definition
from .utils import (detect_if_is_test_data, generate_id_column_name,
                    generate_table_name, generate_view_name,
                    get_entity_type_id1_by_table_name, get_where_params,
                    process_insert_data_dict, process_update_data_dict,
                    process_upsert_data_dict,
                    replace_view_with_table, validate_none_select_table_name,
                    validate_select_table_name, validate_single_clause_value,
                    where_skip_null_values, insert_is_undelete,
                    is_column_in_table,
                    is_end_timestamp_in_table, get_table_columns,
                    group_list_by_columns,
                    process_select_data_dict,
                    generate_where_clause_for_ignore_duplicate,
                    fix_select_clause_value, fix_where_clause_value)

# TODO General question about the overhead of the packages GenericCrud? GenericCrudMl? Mapping? comapring to working directly with the database.


# TODO General question about the overhead of the packages GenericCrud? GenericCrudMl? Mapping? comapring to working directly with the database.

class GenericCRUD(GenericCrudAbstract, metaclass=ABCMetaLogger,
                  object=CRUD_MYSQL_CODE_LOGGER_OBJECT):
    """A class that provides generic CRUD functionality.
    There are 4 main functions to create, read, update, and delete data from the database.
    The rest of the functions are helper functions or wrappers around the main functions."""

    # TODO add default_select_clause_value and default_where in all functions not only in select_multi_tuple_by_where
    #   (no need to add to the the selects, as they all call select_multi_tuple_by_where)
    def __init__(self, *,
                 # TODO Make sure eventyone send this param
                 default_entity_name: str = "Unknown entity in database-mysql",
                 default_schema_name: str,
                 default_table_name: str = None,
                 default_view_table_name: str = None,
                 default_view_with_deleted_and_test_data: str = None,
                 default_column_name: str = None,
                 default_select_clause_value: str = "*",
                 default_where: str = None,
                 is_test_data: bool = False,
                 # For backward compatability we have added is_latest_version optional parameter. A better way will be to rename the name of the Class and create new Class in the original name  # noqa
                 is_latest_version=False) -> None:
        """Initializes the GenericCRUD class. If a connection is not provided, a new connection will be created."""
        if (not is_latest_version):
            # "Please import GenericCrudMysql instead of GenericCRUD",
            self.logger.deprecation_warning(old_name="GenericCRUD",
                                            new_name="GenericCrudMysql")
        self.default_entity_name = default_entity_name
        self.default_schema_name = default_schema_name
        # We do not need a connection per schema, and it makes terrible performance.
        # In special cases, you can always use set_schema.
        self.connection = Connector.connect(schema_name=default_schema_name)
        self._cursor = self.connection.cursor()
        self.default_table_name = default_table_name or \
            generate_table_name(entity_name=default_entity_name,
                                schema_name=default_schema_name)
        self.default_view_table_name = default_view_table_name or generate_view_name(
            self.default_table_name)
        self.default_column_name = default_column_name or generate_id_column_name(
            self.default_table_name)
        self.default_view_with_deleted_and_test_data = default_view_with_deleted_and_test_data
        self.default_select_clause_value = default_select_clause_value
        self.default_where = default_where
        self.is_test_data = is_test_data or detect_if_is_test_data()
        self.is_ignore_duplicate = False
        self.user_context = UserContext()

    # TODO ignore_duplicate -> is_ignore_duplicate
    # ignore_duplicate means no error is found duplicate when inserting to the database
    # Please note that we have is_ignore_duplicate/ignore_duplicate both in the class level and method level (parameter)
    def insert(self, *, schema_name: str = None, table_name: str = None, data_dict: dict = None,
               ignore_duplicate: bool = False, commit_changes: bool = True) -> int:
        # TODO raise_if_database_raise: bool = True, insert_is_undelete
        #   get_id_of_existing_exact_match: bool = True) -> int:
        """Inserts a new row into the table and returns the id of the new row or -1 if an error occurred.
        ignore_duplicate should be False as default, because for example if a user register with existing name,
            he should get an error and not existing id
        """
        # if ignore_duplicate is not None:
        #     self.logger.warning("GenericCRUD.insert: ignore_duplicate is deprecated")

        table_name = table_name or self.default_table_name
        schema_name = schema_name or self.default_schema_name
        self._validate_args(args=locals())
        if ignore_duplicate:
            self.logger.info(f"GenericCRUD.insert({schema_name}.{table_name}) using ignore_duplicate, is it needed? - Not recommended",
                             object={"data_dict": data_dict})

        # if table_name in table_definition: if table_definition[table_name]["is_number_column"]: view_name =
        # self._get_view_name(table_name) number = NumberGenerator.get_random_number(schema_name=schema_name,
        # view_name=view_name) data_dict["number"] = number else: self.logger.warning(f"database-mysql-local-python
        # generic_crud.py Table {table_name} not found in " f"database-mysql-local.table_definition_table data
        # structure, we might need to run sql2code")

        # TODO: In the future we may want to check this with table_definition
        #   and not with self.is_column_in_table for better performance
        data_dict = self.__add_create_updated_user_profile_ids(
            data_dict=data_dict, add_created_user_id=True, schema_name=schema_name, table_name=table_name)

        columns, values, params = process_insert_data_dict(data_dict=data_dict)

        # We removed the IGNORE from the SQL Statement as we want to return the id of the existing row
        insert_query = "INSERT " + \
                       f"INTO `{schema_name}`.`{table_name}` ({columns}) " \
                       f"VALUES ({values});"
        try:
            self.logger.info("insert_query=" + insert_query)
            self.cursor.execute(insert_query, params)
            if commit_changes:
                # TODO: test if it works when schema_name != self.default_schema_name
                self.connection.commit()
            inserted_id = self.cursor.lastrowid()
        except mysql.connector.errors.IntegrityError as exception:
            if ignore_duplicate:
                # TODO Add the values we are trying to insert
                self.logger.warning(f"GenericCRUD.insert({schema_name}.{table_name}) using ignore_duplicate, is it needed? - Trying to insert a duplicate value",  # noqa
                                    object={"data_dict": data_dict})
                self.is_ignore_duplicate = True
                self.logger.warning("GenericCRUD.insert: existing record found, selecting it's id."
                                    f"(table_name={table_name}, data_dict={data_dict})")
                inserted_id = self._get_existing_duplicate_id(
                    schema_name, table_name, exception, data_dict=data_dict)
            else:
                raise exception
        finally:
            self.is_ignore_duplicate = False
            self.logger.debug(object=locals())
        return inserted_id

    def insert_if_not_exists(self, *, schema_name: str = None, table_name: str = None, data_dict: dict = None,
                             data_dict_compare: dict = None, view_table_name: str = None,
                             commit_changes: bool = True, compare_with_or: bool = False) -> int:
        """Inserts a new row into the table if a row with the same values does not exist,
        and returns the id of the new row | None if an error occurred."""
        schema_name = schema_name or self.default_schema_name
        table_name = table_name or self.default_table_name
        view_table_name = view_table_name or self.default_view_table_name
        data_dict_compare = data_dict_compare or data_dict
        self._validate_args(args=locals())

        # Try to select
        where_clause, params = process_upsert_data_dict(
            data_dict=data_dict_compare, compare_with_or=compare_with_or)
        row_tuple = self.select_one_tuple_by_where(
            schema_name=schema_name, view_table_name=view_table_name, select_clause_value="*",
            where=where_clause, params=params)
        if row_tuple:
            entity_id = row_tuple[0]
            self.logger.info(f"GenericCRUD.insert_if_not_exists: row already exists, returning id {entity_id}",
                             object={"id": entity_id})
        else:
            # If we use self instead of GenericCRUD in the following line, this will fail when called by classes
            # that inherit from GenericCRUD and override the insert method, because the overridden method will be called
            # for example when we call person_local.insert_if_not_exists, it will call person_local.insert
            # but we want to call GenericCRUD.insert
            entity_id = GenericCRUD.insert(self, schema_name=schema_name, table_name=table_name, data_dict=data_dict,
                                           commit_changes=commit_changes, ignore_duplicate=True)
            self.logger.info(f"GenericCRUD.insert_if_not_exists: row inserted with id {entity_id}",
                             object={"id": entity_id})
        return entity_id

    def insert_many_dicts(self, *, schema_name: str = None, table_name: str = None, data_dicts: list[dict],
                          commit_changes: bool = True) -> int:
        """Inserts multiple rows into the table.
        data_dicts should be in the following format: [{col1: val1, col2: val2}, {col1: val3, col2: val4}, ...]
        Returns the number of inserted rows.
        """
        if not data_dicts:
            self.logger.warning(
                "GenericCRUD.insert_many_dicts: data_dicts is empty")
            inserted_rows = 0
        else:
            converted_data_dicts = {
                col: [row[col] for row in data_dicts] for col in data_dicts[0]}
            inserted_rows = self.insert_many(schema_name=schema_name, table_name=table_name,
                                             data_dict=converted_data_dicts, commit_changes=commit_changes)

        return inserted_rows

    def insert_many(self, *, schema_name: str = None, table_name: str = None, data_dict: dict[str, list | tuple],
                    commit_changes: bool = True) -> int:
        """Inserts multiple rows into the table.
        data_dict should be in the following format: {col1: [val1, val2], col2: [val3, val4], ...}
        Returns the number of inserted rows.
        """
        if not data_dict:
            self.logger.warning("GenericCRUD.insert_many: data_dict is empty")
            inserted_rows = 0
            return inserted_rows
        schema_name = schema_name or self.default_schema_name
        table_name = table_name or self.default_table_name

        self._validate_args(args=locals())
        # TODO: I am not sure we can use process_insert_data_dict here

        len_rows = len(next(v for v in data_dict.values()))
        data_dict = self.__add_create_updated_user_profile_ids(
            data_dict=data_dict, add_created_user_id=True, schema_name=schema_name, table_name=table_name)
        # Fix values from __add_create_updated_user_profile_ids
        for k, v in data_dict.items():
            if not isinstance(v, list) and not isinstance(v, tuple):
                data_dict[k] = [v] * len_rows  # TODO: number should be unique

        columns = ", ".join(f"`{key}`" for key in data_dict)
        values = ", ".join(["%s"] * len(data_dict))
        sql_statement = f"""
        INSERT INTO `{schema_name}`.`{table_name}` ({columns})
        VALUES ({values});
        """
        sql_parameters = list(zip(*data_dict.values()))
        self.cursor.executemany(
            sql_statement=sql_statement, sql_parameters=sql_parameters)
        if commit_changes:
            self.connection.commit()
        inserted_rows = self.cursor.get_affected_row_count()
        return inserted_rows

    # TODO Why we change upsert to upsert_with_select_clause? This might break things ...
    def upsert_with_select_clause(self, *, schema_name: str = None, table_name: str = None, view_table_name: str = None,
                                  data_dict: dict = None, where_compare: str = None, params_compare: tuple = None,
                                  data_dict_compare: dict = None, order_by: str = None, compare_with_or: bool = False,
                                  select_clause_value: str = "*") -> dict:
        """
        Inserts a new row into the table if a row with the same values does not exist,
        the logic:
        1. If data_dict_compare is empty, insert the row and return the id.
        2. If data_dict_compare is not empty, select the row with the same values as data_dict_compare.

            a. If the row exists, update it with data_dict and return the id.

            b. If the row does not exist, insert it with data_dict and return the id.
        """
        schema_name = schema_name or self.default_schema_name
        table_name = table_name or self.default_table_name
        view_table_name = view_table_name or self.default_view_table_name
        id_column_name = generate_id_column_name(table_name)
        self._validate_args(args=locals())
        result_dict = {}
        if not data_dict:
            self.logger.warning(
                log_message="GenericCRUD.upsert_with_select_clause: data_dict is empty")
            return result_dict
        if not data_dict_compare:
            inserted_id = GenericCRUD.insert(self, schema_name=schema_name,
                                             table_name=table_name, data_dict=data_dict)
            data_dict[id_column_name] = inserted_id
            result_dict = data_dict
            # TODO Changing return inserted_id to result_dict might break things?
            return result_dict  # upser() was returning inserted_id

        where_clause, params = process_upsert_data_dict(data_dict=data_dict_compare, compare_with_or=compare_with_or,
                                                        where_compare=where_compare, params_compare=params_compare)
        # Add table_id if it's not in select_clause_value
        if select_clause_value != "*" and id_column_name not in select_clause_value:
            select_clause_value += f", {id_column_name}"
        row_dict = self.select_one_dict_by_where(
            schema_name=schema_name, view_table_name=view_table_name, select_clause_value=select_clause_value,
            where=where_clause, params=params, order_by=order_by)
        if row_dict:
            table_id = row_dict[id_column_name]
            try:
                self.update_by_column_and_value(
                    schema_name=schema_name, table_name=table_name, column_name=id_column_name, column_value=table_id,
                    data_dict=data_dict)
            except Exception as exception:
                self.logger.error(
                    "GenericCRUD.upsert_with_select_clause: error updating row",
                    object={"data_dict": data_dict,
                            "row_dict": row_dict, "exception": exception}
                )
                raise exception
        else:
            try:
                table_id = GenericCRUD.insert(
                    self, schema_name=schema_name, table_name=table_name, data_dict=data_dict)
            except Exception as exception:
                self.logger.error(
                    "GenericCRUD.upsert_with_select_clause: error inserting row",
                    object={"data_dict": data_dict, "exception": exception}
                )
                raise exception
        result_dict = data_dict
        result_dict.update({k: v for k, v in row_dict.items()
                           if k not in result_dict}) if row_dict else None
        result_dict[id_column_name] = table_id
        self.logger.debug(object=locals())
        return result_dict

    # We want upsert to call upsert_with_select_clause, and return only the id
    def upsert(self, *, schema_name: str = None, table_name: str = None, view_table_name: str = None,
               data_dict: dict = None, where_compare: str = None,
               params_compare: tuple = None, data_dict_compare: dict = None,
               order_by: str = None, compare_with_or: bool = False) -> Optional[int]:
        """
        Inserts a new row into the table if a row with the same values does not exist,
        the "same values" are extracted from data_dict_compare.
        data_dict_compare is a dictionary with the same keys as data_dict, but with the values to compare.

        **you don't need to have the full fields in data_dict_compare, only the fields you want to compare.**
        """
        table_name = table_name or self.default_table_name
        column_name = generate_id_column_name(table_name)
        inserted_id_per_column_dict = self.upsert_with_select_clause(
            schema_name=schema_name, table_name=table_name,
            view_table_name=view_table_name, data_dict=data_dict,
            where_compare=where_compare, params_compare=params_compare,
            data_dict_compare=data_dict_compare, order_by=order_by,
            compare_with_or=compare_with_or, select_clause_value=column_name)
        inserted_id = inserted_id_per_column_dict[column_name]
        return inserted_id

    def _get_existing_duplicate_id(self, schema_name: str, table_name: str, error: Exception,
                                   data_dict: dict) -> int | None:
        if is_end_timestamp_in_table(table_name=table_name) and insert_is_undelete(table_name=table_name):
            existing_duplicate_id = self.__get_existing_duplicate_id_with_undelete(
                schema_name=schema_name, table_name=table_name, data_dict=data_dict)
        else:
            existing_duplicate_id = self.__get_existing_duplicate_id_without_undelete(
                schema_name=schema_name, table_name=table_name, data_dict=data_dict)
        if existing_duplicate_id is None:
            self.logger.error(
                f"GenericCRUD._get_existing_duplicate_id_without_timestamp: no existing row found for {schema_name}.{table_name}.{data_dict}",
                object={"data_dict": data_dict, "error": error}
            )
            raise error
        self.logger.debug(object=locals())
        return existing_duplicate_id

    '''
    # old version
    def _get_existing_duplicate_id(self, schema_name: str, table_name: str, error: Exception) -> int | None:
        # When inserting a deleted entity and insert_is_undelete=false, we should null all the unique fields of the deleted entity
        duplicate_value, duplicate_column_name = extract_duplicated_from_error(error)
        if not duplicate_column_name:
            return duplicate_value  # found the duplicated id

        column_name = self.get_primary_key(schema_name=schema_name, table_name=table_name)
        if not column_name:
            raise error  # Column name for constraint not found
        if is_end_timestamp_in_table(table_name=table_name) and insert_is_undelete(table_name=table_name):
            existing_duplicate_id = self.__get_existing_duplicate_id_with_timestamp(
                schema_name=schema_name, table_name=table_name, duplicate_column_name=duplicate_column_name,
                duplicate_value=duplicate_value, column_name=column_name)
        else:
            existing_duplicate_id = self.__get_existing_duplicate_id_without_timestamp(
                schema_name=schema_name, table_name=table_name, duplicate_column_name=duplicate_column_name,
                duplicate_value=duplicate_value, column_name=column_name)
        if existing_duplicate_id is None:
            self.logger.error(
                f"GenericCRUD._get_existing_duplicate_id_without_timestamp: no existing row found for "
                f"{schema_name}.{table_name}.{duplicate_column_name}={duplicate_value}",
                object={"duplicate_column_name": duplicate_column_name, "duplicate_value": duplicate_value}
            )
            raise error
        self.logger.debug(object=locals())
        return existing_duplicate_id
    '''

    def __get_existing_duplicate_id_with_undelete(
            self, schema_name: str, table_name: str, data_dict: dict) -> int | None:
        column_name = generate_id_column_name(table_name)
        where, params = self.get_constraint_where_clause(schema_name=schema_name, table_name=table_name,
                                                         data_dict=data_dict)
        row = self.select_one_tuple_by_where(
            schema_name=schema_name, view_table_name=table_name,
            select_clause_value=f"{column_name}, end_timestamp",
            where=where, params=params
        )
        if not row:
            existing_duplicate_id = None
            return existing_duplicate_id
        else:
            existing_duplicate_id, end_timestamp = row
        if end_timestamp and datetime.now(timezone.utc) > end_timestamp.replace(tzinfo=timezone.utc):
            self.undelete_by_column_and_value(
                schema_name=schema_name, table_name=table_name,
                column_name=column_name, column_value=existing_duplicate_id)
        return existing_duplicate_id

    # TODO: test
    def __get_existing_duplicate_id_without_undelete(
            self, *, schema_name: str, table_name: str, data_dict: dict) -> int | None:
        column_name = generate_id_column_name(table_name)
        where, params = self.get_constraint_where_clause(schema_name=schema_name, table_name=table_name,
                                                         data_dict=data_dict)
        if is_end_timestamp_in_table(table_name=table_name):
            row = self.select_one_tuple_by_where(
                schema_name=schema_name, view_table_name=table_name,
                select_clause_value=f"{column_name}, end_timestamp",
                where=where, params=params)
            if not row:
                existing_duplicate_id = None
                return existing_duplicate_id
            else:
                existing_duplicate_id, end_timestamp = row
                if end_timestamp is not None:
                    self.logger.error(
                        f"GenericCRUD.__get_existing_duplicate_id_without_timestamp: existing row found for "
                        f"{schema_name}.{table_name}.{data_dict} but it is deleted",
                        object={"data_dict": data_dict, "existing_duplicate_id": existing_duplicate_id,
                                "end_timestamp": end_timestamp}
                    )
                    existing_duplicate_id = None
        else:
            existing_duplicate_id = self.select_one_value_by_where(
                schema_name=schema_name, view_table_name=table_name, select_clause_value=column_name,
                where=where, params=params)
        return existing_duplicate_id

    '''
    # Old version
    def __get_existing_duplicate_id_with_timestamp(
            self, schema_name: str, table_name: str, duplicate_column_name: str,
            duplicate_value: Any, column_name: str) -> int or None:
        select_query = (
            f"SELECT {column_name}, end_timestamp "
            f"FROM `{schema_name}`.`{table_name}` "
            f"WHERE {duplicate_column_name} = %s LIMIT 1;"
        )
        self.connection.commit()
        self.cursor.execute(select_query, (duplicate_value,))
        row = self.cursor.fetchone()
        if row is None:
            existing_duplicate_id = None
            return existing_duplicate_id
        else:
            existing_duplicate_id, end_timestamp = row
        if end_timestamp and datetime.now(timezone.utc) > end_timestamp.replace(tzinfo=timezone.utc):
            self.undelete_by_column_and_value(
                schema_name=schema_name, table_name=table_name,
                column_name=column_name, column_value=existing_duplicate_id)
        return existing_duplicate_id

    # TODO: test
    def __get_existing_duplicate_id_without_timestamp(
            self, *, schema_name: str, table_name: str, duplicate_column_name: str,
            duplicate_value: Any, column_name: str) -> int or None:
        select_query = (
            f"SELECT {column_name} "
            f"FROM `{schema_name}`.`{table_name}` "
            f"WHERE {duplicate_column_name} = %s LIMIT 1;"
        )
        self.connection.commit()
        self.cursor.execute(select_query, (duplicate_value,))
        existing_duplicate_id = (self.cursor.fetchone() or [None])[0]
        return existing_duplicate_id
    '''

    def undelete_by_column_and_value(self, *, schema_name: str = None, table_name: str = None,
                                     column_name: str = None, column_value: Any) -> None:
        """Undeletes a row by setting the end_timestamp to NULL."""
        schema_name = schema_name or self.default_schema_name
        table_name = table_name or self.default_table_name
        column_name = column_name or self.default_column_name
        self._validate_args(args=locals())
        self.update_by_column_and_value(
            schema_name=schema_name, table_name=table_name,
            column_name=column_name, column_value=column_value,
            data_dict={"end_timestamp": None})

    def update_by_column_and_value(
            self, *, schema_name: str = None, table_name: str = None,
            column_name: str = None, column_value: Any,
            data_dict: dict = None,
            limit: int = DEFAULT_SQL_SELECT_LIMIT, order_by: str = None,
            commit_changes: bool = True) -> int:
        """Updates data in the table by ID."""

        table_name = table_name or self.default_table_name
        column_name = column_name or self.default_column_name

        if column_name:
            where, params = get_where_params(column_name, column_value)
            updated_rows = self.update_by_where(
                schema_name=schema_name, table_name=table_name, where=where, data_dict=data_dict,
                params=params, limit=limit, order_by=order_by, commit_changes=commit_changes)
            return updated_rows

        else:
            raise Exception("Update by id requires an column_name")

    def update_by_where(self, *, schema_name: str = None,
                        table_name: str = None, where: str = None,
                        params: tuple = None, data_dict: dict = None,
                        limit: int = DEFAULT_SQL_SELECT_LIMIT,
                        order_by: str = None,
                        commit_changes: bool = True) -> int:
        """Updates data in the table by WHERE.
        Example:
        "UPDATE table_name SET A=A_val, B=B_val WHERE C=C_val AND D=D_val"
        translates into:
        update_by_where(table_name="table_name",
                        data_dict={"A": A_val, "B": B_val},
                        where="C=%s AND D=%s",
                        params=(C_val, D_val)"""

        table_name = table_name or self.default_table_name
        schema_name = schema_name or self.default_schema_name
        self._validate_args(args=locals())

        data_dict = self.__add_create_updated_user_profile_ids(data_dict=data_dict, add_created_user_id=False,
                                                               schema_name=schema_name, table_name=table_name)

        set_values, data_dict_params = process_update_data_dict(data_dict)
        if not where:
            raise Exception("update_by_where requires a 'where'")

        if 'mapping' in self.default_table_name:
            update_query = f"UPDATE `{schema_name}`.`{table_name}` " \
                f"SET {set_values} " \
                f"WHERE {where} " + \
                (f"ORDER BY {order_by} " if order_by else "") + \
                f"LIMIT {limit};"
        else:
            update_query = f"UPDATE `{schema_name}`.`{table_name}` " \
                f"SET {set_values} updated_timestamp=CURRENT_TIMESTAMP() " \
                f"WHERE {where} " + \
                (f"ORDER BY {order_by} " if order_by else "") + \
                f"LIMIT {limit};"
        where_params = params or tuple()

        self.cursor.execute(update_query, data_dict_params + where_params)
        if commit_changes:
            self.connection.commit()
        updated_rows = self.cursor.get_affected_row_count()
        return updated_rows

    def delete_by_column_and_value(self, *, schema_name: str = None, table_name: str = None,
                                   column_name: str = None, column_value: Any) -> int:
        """Deletes data from the table by id.
        Returns the number of deleted rows."""
        # checks are done inside delete_by_where
        column_name = column_name or self.default_column_name

        if column_name:  # column_value can be empty
            where, params = get_where_params(column_name, column_value)
            deleted_rows = self.delete_by_where(schema_name=schema_name, table_name=table_name, where=where,
                                                params=params)
            return deleted_rows
        else:
            raise Exception(
                "Delete by id requires an column_name and column_value.")

    def delete_by_where(self, *, schema_name: str = None, table_name: str = None, where: str = None,
                        params: tuple = None) -> int:
        """Deletes data from the table by WHERE.
        Returns the number of deleted rows."""

        table_name = table_name or self.default_table_name
        schema_name = schema_name or self.default_schema_name
        self._validate_args(args=locals())
        if not where:
            raise Exception("delete_by_where requires a 'where'")
        if "end_timestamp" not in where and is_end_timestamp_in_table(table_name):
            where += " AND end_timestamp IS NULL "

        update_query = f"UPDATE `{schema_name}`.`{table_name}` " \
            f"SET end_timestamp=CURRENT_TIMESTAMP() " \
            f"WHERE {where};"

        self.cursor.execute(update_query, params)
        self.connection.commit()
        deleted_rows = self.cursor.get_affected_row_count()
        return deleted_rows

    # Main select function
    def select_multi_tuple_by_where(
            self, *, schema_name: str = None, view_table_name: str = None, select_clause_value: str = None,
            where: str = None, params: tuple = None, distinct: bool = False, limit: int = DEFAULT_SQL_SELECT_LIMIT,
            order_by: str = None) -> list:
        """Selects multiple rows from the table based on a WHERE clause and returns them as a list of tuples."""

        schema_name = schema_name or self.default_schema_name
        view_table_name = view_table_name or self.default_view_table_name
        select_clause_value = select_clause_value or self.default_select_clause_value
        select_clause_value = fix_select_clause_value(
            select_clause_value=select_clause_value)
        where = where or self.default_where
        where = fix_where_clause_value(where_clause_value=where)
        where = self.__where_security(where=where, view_name=view_table_name)
        self._validate_args(args=locals())

        # TODO: add ` to column names if they are not reserved words (like COUNT, ST_X(point), etc.)
        # select_clause_value = ",".join([f"`{x.strip()}`" for x in select_clause_value.split(",") if x != "*"])

        if self.is_test_data and not self.is_ignore_duplicate:
            # TODO: auto detect with entity table (save in memory first)
            # once done, we prefer not to send it as parameter, to allow changing the name later without changing the code.
            # In the future we will change to default_view_with_test_data that does not show deleted data, so that
            # we can select-delete-select in a similar way and verify the deletion.
            # Will we ever have a case where there will be a view with no assosiated table that we will need to see deleted data in there? It appears no.  # noqa E501

            # TODO: auto detect with entity table (save in memory first) once done, we prefer not to send it as
            #  parameter, to allow changing the name later without changing the code. In the future we will change to
            #  default_view_with_test_data that does not show deleted data, so that we can select-delete-select in a
            #  similar way and verify the deletion. Will we ever have a case where there will be a view with no
            #  assosiated table that we will need to see deleted data in there? It appears no.

            if self.default_view_with_deleted_and_test_data:
                view_table_name = self.default_view_with_deleted_and_test_data
            else:
                view_table_name = replace_view_with_table(view_table_name=view_table_name,
                                                          select_clause_value=select_clause_value)
        elif is_column_in_table(table_name=view_table_name, column_name="is_test_data"):
            if not where:
                where = "(is_test_data <> 1 OR is_test_data IS NULL)"
            elif not self.is_test_data and "is_test_data" not in where:
                # hide test data from real users.
                where += " AND (is_test_data <> 1 OR is_test_data IS NULL)"
            # TODO: Shall we add the following elif?
            '''
            elif self.is_test_data and "is_test_data" not in where:
                where += " AND (is_test_data = 1)"  # show only test data to developers.
            '''

        if where and "end_timestamp" not in where and is_end_timestamp_in_table(
                view_table_name) and not self.is_ignore_duplicate:
            # The () around the where is important, because we might have a where with AND and OR
            where = f"({where}) AND end_timestamp IS NULL "  # not deleted
        select_query = f"SELECT {'DISTINCT' if distinct else ''} {select_clause_value} " \
            f"FROM `{schema_name}`.`{view_table_name}` " + \
            (f"WHERE {where} " if where else "") + \
            (f"ORDER BY {order_by} " if order_by else "") + \
            f"LIMIT {limit};"

        self.connection.commit()  # https://bugs.mysql.com/bug.php?id=102053
        if isinstance(params, int):
            params = [params]
        self.cursor.execute(select_query, params)
        result = self.cursor.fetchall()

        self.logger.debug(object=locals())
        return result

    def select_multi_dict_by_where(
            self, *, schema_name: str = None, view_table_name: str = None, select_clause_value: str = None,
            where: str = None, params: tuple = None, distinct: bool = False, group_by: str = None,
            limit: int = DEFAULT_SQL_SELECT_LIMIT, order_by: str = None) -> list | dict[tuple | str, list]:
        """Selects multiple rows from the table based on a WHERE clause and returns them as a list of dictionaries."""
        result = self.select_multi_tuple_by_where(
            schema_name=schema_name, view_table_name=view_table_name, select_clause_value=select_clause_value,
            where=where, params=params, distinct=distinct, limit=limit, order_by=order_by)
        result_as_dicts = self.convert_multi_to_dict(
            result, select_clause_value)
        if group_by:
            result_as_dicts = group_list_by_columns(
                list_of_dicts=result_as_dicts, group_by=group_by)
        return result_as_dicts

    # TODO: test distinct
    def select_one_tuple_by_column_and_value(
            self, *, schema_name: str = None, view_table_name: str = None, select_clause_value: str = None,
            column_name: str = None, column_value: Any,
            distinct: bool = False, order_by: str = None) -> tuple:
        """Selects one row from the table by ID and returns it as a tuple."""
        result = self.select_multi_tuple_by_column_and_value(
            schema_name=schema_name, view_table_name=view_table_name, select_clause_value=select_clause_value,
            column_name=column_name, column_value=column_value, distinct=distinct, limit=1, order_by=order_by)
        if result:
            one_tuple_result = result[0]
        else:
            one_tuple_result = tuple()  # or None?
        return one_tuple_result

    def select_one_dict_by_column_and_value(
            self, *, schema_name: str = None, view_table_name: str = None, select_clause_value: str = None,
            column_name: str = None, column_value: Any,
            distinct: bool = False, order_by: str = None) -> dict:
        """Selects one row from the table by ID and returns it as a dictionary (column_name: value)"""
        result = self.select_one_tuple_by_column_and_value(
            schema_name=schema_name, view_table_name=view_table_name, select_clause_value=select_clause_value,
            column_name=column_name, column_value=column_value, distinct=distinct, order_by=order_by)
        result = self.convert_to_dict(
            row=result, select_clause_value=select_clause_value)
        return result

    # TODO Why we need to send "select_clause_value" if we provided "default_select_clause_value" in the constructor. Added "= None" to try and resolve it.  # noqa E501
    # TODO Add ASC/DESC parameter to all methods which have order_by parameter
    def select_one_value_by_column_and_value(
            self, *, select_clause_value: str = None, schema_name: str = None, view_table_name: str = None,
            column_name: str = None, column_value: Any,
            distinct: bool = False, order_by: str = None, skip_null_values: bool = True) -> Any:
        """Selects one value from the table by ID and returns it."""

        column_name = column_name or self.default_column_name
        select_clause_value = select_clause_value or self.default_select_clause_value
        validate_single_clause_value(select_clause_value)
        where, params = get_where_params(column_name, column_value)
        where = where_skip_null_values(
            where, select_clause_value, skip_null_values)
        result = self.select_one_tuple_by_where(
            schema_name=schema_name, view_table_name=view_table_name, select_clause_value=select_clause_value,
            where=where, params=params, distinct=distinct, order_by=order_by)
        if result:  # TODO: the caller can't tell if not found, or found null
            value = result[0]
        else:
            value = None
        return value

    def select_one_tuple_by_where(
            self, *, schema_name: str = None, view_table_name: str = None, select_clause_value: str = None,
            where: str = None, params: tuple = None, distinct: bool = False, order_by: str = None) -> tuple:
        """Selects one row from the table based on a WHERE clause and returns it as a tuple."""
        result = self.select_multi_tuple_by_where(
            schema_name=schema_name, view_table_name=view_table_name, select_clause_value=select_clause_value,
            where=where, params=params, distinct=distinct, limit=1, order_by=order_by)
        if result:
            tuple_result = result[0]
        else:
            tuple_result = tuple()
        return tuple_result

    def select_one_dict_by_where(
            self, *, schema_name: str = None, view_table_name: str = None, select_clause_value: str = None,
            where: str = None, params: tuple = None, distinct: bool = False, order_by: str = None) -> dict:
        """Selects one row from the table based on a WHERE clause and returns it as a dictionary."""
        result = self.select_one_tuple_by_where(
            schema_name=schema_name, view_table_name=view_table_name, select_clause_value=select_clause_value,
            where=where, params=params, distinct=distinct, order_by=order_by)
        result = self.convert_to_dict(
            row=result, select_clause_value=select_clause_value)
        return result

    def select_one_value_by_where(
            self, *, select_clause_value: str, schema_name: str = None, view_table_name: str = None,
            where: str = None, params: tuple = None, distinct: bool = False, order_by: str = None,
            skip_null_values: bool = True) -> Any:
        """Selects one value from the table based on a WHERE clause and returns it."""
        select_clause_value = select_clause_value or self.default_select_clause_value
        validate_single_clause_value(select_clause_value)
        where = where_skip_null_values(
            where, select_clause_value, skip_null_values)
        result = self.select_one_tuple_by_where(
            schema_name=schema_name, view_table_name=view_table_name, select_clause_value=select_clause_value,
            where=where, params=params, distinct=distinct, order_by=order_by)
        if result:
            value = result[0]
        else:
            value = None
        return value

    def select_multi_value_by_column_and_value(
            self, *, schema_name: str = None, view_table_name: str = None,
            select_clause_value: str = None,
            column_name: str = None, column_value: Any,
            distinct: bool = False, limit: int = DEFAULT_SQL_SELECT_LIMIT, order_by: str = None,
            skip_null_values: bool = True) -> tuple:
        """Selects multiple values from the table by ID and returns them as a list."""

        column_name = column_name or self.default_column_name
        select_clause_value = select_clause_value or self.default_select_clause_value
        validate_single_clause_value(select_clause_value)
        where, params = get_where_params(column_name, column_value)
        where = where_skip_null_values(
            where, select_clause_value, skip_null_values)
        result = self.select_multi_tuple_by_where(
            schema_name=schema_name, view_table_name=view_table_name, select_clause_value=select_clause_value,
            where=where, params=params, distinct=distinct, limit=limit, order_by=order_by)
        values = tuple(row[0] for row in result)
        return values

    def select_multi_value_by_where(
            self, *, schema_name: str = None, view_table_name: str = None, select_clause_value: str = None,
            where: str = None, params: tuple = None, distinct: bool = False, limit: int = DEFAULT_SQL_SELECT_LIMIT,
            order_by: str = None, skip_null_values: bool = True) -> tuple:
        select_clause_value = select_clause_value or self.default_select_clause_value
        validate_single_clause_value(select_clause_value)
        where = where_skip_null_values(
            where, select_clause_value, skip_null_values)
        result = self.select_multi_tuple_by_where(
            schema_name=schema_name, view_table_name=view_table_name, select_clause_value=select_clause_value,
            where=where, params=params, distinct=distinct, limit=limit, order_by=order_by)
        values = tuple(row[0] for row in result)
        return values

    def select_multi_tuple_by_column_and_value(
            self, *, schema_name: str = None, view_table_name: str = None, select_clause_value: str = None,
            column_name: str = None, column_value: Any,
            distinct: bool = False, limit: int = DEFAULT_SQL_SELECT_LIMIT, order_by: str = None) -> list:
        """Selects multiple rows from the table by ID and returns them as a list of tuples.
        If column_value is list / tuple, it will be used as multiple values for the column_name (SQL IN)."""

        column_name = column_name or self.default_column_name

        where, params = get_where_params(column_name, column_value)
        result = self.select_multi_tuple_by_where(
            schema_name=schema_name, view_table_name=view_table_name, select_clause_value=select_clause_value,
            where=where, params=params, distinct=distinct, limit=limit, order_by=order_by)
        return result

    def select_multi_dict_by_column_and_value(
            self, *, schema_name: str = None, view_table_name: str = None, select_clause_value: str = None,
            column_name: str = None, column_value: Any,
            distinct: bool = False, limit: int = DEFAULT_SQL_SELECT_LIMIT, order_by: str = None,
            group_by: str = None) -> list | dict[tuple | str, list]:
        """Selects multiple rows from the table by ID and returns them as a list of dictionaries."""
        result = self.select_multi_tuple_by_column_and_value(
            schema_name=schema_name, view_table_name=view_table_name, select_clause_value=select_clause_value,
            column_name=column_name, column_value=column_value, distinct=distinct, limit=limit, order_by=order_by)
        result_as_dicts = self.convert_multi_to_dict(
            result, select_clause_value)
        if group_by:
            result_as_dicts = group_list_by_columns(
                list_of_dicts=result_as_dicts, group_by=group_by)
        return result_as_dicts

    def select_one_value_by_dict(
            self, *, select_clause_value: str, schema_name: str = None, view_table_name: str = None,
            data_dict: dict, distinct: bool = False, order_by: str = None, skip_null_values: bool = True) -> Any:
        """Selects one value from the table based on a WHERE clause and returns it."""
        select_clause_value = select_clause_value or self.default_select_clause_value
        validate_single_clause_value(select_clause_value)
        where, params = process_select_data_dict(data_dict)
        where = where_skip_null_values(
            where, select_clause_value, skip_null_values)
        result = self.select_one_value_by_where(
            schema_name=schema_name, view_table_name=view_table_name, select_clause_value=select_clause_value,
            where=where, params=params, distinct=distinct, order_by=order_by)
        return result

    def select_multi_values_by_dict(  # TODO: test
            self, *, select_clause_value: str, schema_name: str = None, view_table_name: str = None,
            data_dict: dict, distinct: bool = False, limit: int = DEFAULT_SQL_SELECT_LIMIT, order_by: str = None,
            skip_null_values: bool = True) -> tuple:
        """Selects multiple values from the table based on a WHERE clause from the data_dict and returns them as a
        list."""
        select_clause_value = select_clause_value or self.default_select_clause_value
        validate_single_clause_value(select_clause_value)
        where, params = process_select_data_dict(data_dict)
        where = where_skip_null_values(
            where, select_clause_value, skip_null_values)
        result = self.select_multi_value_by_where(
            schema_name=schema_name, view_table_name=view_table_name, select_clause_value=select_clause_value,
            where=where, params=params, distinct=distinct, limit=limit, order_by=order_by)
        return result

    def select_one_tuple_by_dict(
            self, *, schema_name: str = None, view_table_name: str = None, select_clause_value: str = None,
            data_dict: dict, distinct: bool = False, order_by: str = None) -> tuple:
        """Selects one row from the table based on a WHERE clause and returns it as a tuple."""
        select_clause_value = select_clause_value or self.default_select_clause_value
        validate_single_clause_value(select_clause_value)
        where, params = process_select_data_dict(data_dict)
        result = self.select_one_tuple_by_where(
            schema_name=schema_name, view_table_name=view_table_name, select_clause_value=select_clause_value,
            where=where, params=params, distinct=distinct, order_by=order_by)
        return result

    @lru_cache
    def get_primary_key(self, schema_name: str = None, table_name: str = None) -> str | None:
        schema_name = schema_name or self.default_schema_name
        table_name = table_name or self.default_table_name
        query = """
            SELECT COLUMN_NAME
            FROM INFORMATION_SCHEMA.KEY_COLUMN_USAGE
            WHERE TABLE_SCHEMA = %s AND TABLE_NAME = %s AND CONSTRAINT_NAME = "PRIMARY"
            LIMIT 1;"""

        self.connection.commit()
        self.cursor.execute(query, (schema_name, table_name))
        column_name = (self.cursor.fetchone() or [None])[0]
        return column_name

    @lru_cache
    def get_constraint_columns(self, schema_name: str, table_name: str) -> list[list[str]]:
        schema_name = schema_name or self.default_schema_name
        table_name = table_name or self.default_table_name
        query = """
        SELECT CONSTRAINT_NAME, COLUMN_NAME
        FROM INFORMATION_SCHEMA.KEY_COLUMN_USAGE
        WHERE TABLE_SCHEMA = %s AND TABLE_NAME = %s;
        """
        self.connection.commit()
        self.cursor.execute(query, (schema_name, table_name))
        results = self.cursor.fetchall()
        constraints = {}
        for constraint_name, column_name in results:
            if constraint_name not in constraints:
                constraints[constraint_name] = []
            constraints[constraint_name].append(column_name)
        result = list(constraints.values())
        return result

    def get_constraint_where_clause(self, schema_name: str, table_name: str, data_dict: dict):
        constraint_columns = self.get_constraint_columns(
            schema_name, table_name)
        if constraint_columns:
            where, params = generate_where_clause_for_ignore_duplicate(
                data_dict=data_dict, constraint_columns=constraint_columns)
        else:
            where, params = None, None
        return where, params

    # helper functions:
    def convert_to_dict(self, row: tuple, select_clause_value: str = None) -> dict:
        """Returns a dictionary of the column names and their values."""
        select_clause_value = select_clause_value or self.default_select_clause_value
        if select_clause_value == "*":
            column_names = self.cursor.column_names()
        else:
            column_names = [x.strip() for x in select_clause_value.split(",")]
        dict_result = dict(zip(column_names, row or tuple()))
        self.logger.debug(object=locals())
        return dict_result

    def convert_multi_to_dict(self, rows: list[tuple], select_clause_value: str = None) -> list[dict]:
        """Converts multiple rows to dictionaries."""
        multiple_dict_result = [self.convert_to_dict(row=row, select_clause_value=select_clause_value)
                                for row in rows]
        return multiple_dict_result

    def _validate_args(self, args: dict) -> None:
        # args = locals() of the calling function
        required_args = ("table_name", "view_table_name", "schema_name",
                         "select_clause_value", "data_dict")
        for arg_name, arg_value in args.items():
            message = ""
            if arg_name in ("self", "__class__"):
                continue
            elif arg_name in required_args and not arg_value:
                message = f"Invalid value for {arg_name}: {arg_value}"
            elif arg_name == "table_name":
                validate_none_select_table_name(arg_value)
            elif arg_name == "view_table_name":
                validate_select_table_name(
                    view_table_name=arg_value, is_ignore_duplicate=self.is_ignore_duplicate)

            # data_dict values are allowed to contain ';', as we use them with %s (TODO: unless it's ToSQLInterface)
            if ((arg_name.startswith("data_") and arg_value and any(
                    # check columns
                    ";" in str(x) for x in arg_value.keys())) or
                    (not arg_name == "data_dict" and arg_name != "params" and ";" in str(arg_value))):
                message = f"Invalid value for {arg_name}: {arg_value} (contains ';')"

            if message:
                raise Exception(message)

    def __add_identifier(self, data_dict: dict, table_name: str) -> None:
        # If there's an "identifier" column in the table, we want to insert a random identifier
        #  to the identifier_table and use it in the data_dict.
        identifier_entity_type_id = get_entity_type_id1_by_table_name(
            table_name)
        if not identifier_entity_type_id:
            return
        identifier = NumberGenerator.get_random_identifier(
            schema_name="identifier", view_name="identifier_view", identifier_column_name="identifier")
        data_dict["identifier"] = identifier
        # We can't use self.insert, as it would cause an infinite loop
        insert_query = "INSERT " + \
                       "INTO `identifier`.`identifier_table` (identifier, entity_type_id) " \
                       "VALUES (%s, %s);"

        self.cursor.execute(
            insert_query, (identifier, identifier_entity_type_id))
        self.connection.commit()

    # TODO: add warning logs
    def __add_create_updated_user_profile_ids(self, data_dict: dict, add_created_user_id: bool = False,
                                              schema_name: str = None, table_name: str = None) -> dict:
        """Adds created_user_id and updated_user_id to data_dict."""
        # if get_environment_name() not in (EnvironmentName.DVLP1.value, EnvironmentName.PROD1.value):
        data_dict = data_dict or {}
        schema_name = schema_name or self.default_schema_name
        table_name = table_name or self.default_table_name
        table_columns = get_table_columns(table_name=table_name)
        if len(table_columns) == 0:
            self.logger.warning(f"Table {schema_name}.{table_name} was not generated by the generate_table_columns.py script. You need to publish the database-mysql-python package again.")  # noqa E501
            return data_dict
        if add_created_user_id:
            if "created_user_id" in table_columns:
                data_dict["created_user_id"] = self.user_context.get_effective_user_id()
            else:
                self.__log_warning("created_user_id", schema_name, table_name)
            if "created_real_user_id" in table_columns:
                data_dict["created_real_user_id"] = self.user_context.get_real_user_id()
            else:
                self.__log_warning("created_real_user_id",
                                   schema_name, table_name)
            if "created_effective_user_id" in table_columns:
                data_dict["created_effective_user_id"] = self.user_context.get_effective_user_id(
                )
            else:
                self.__log_warning("created_effective_user_id",
                                   schema_name, table_name)
            if "created_effective_profile_id" in table_columns:
                data_dict["created_effective_profile_id"] = self.user_context.get_effective_profile_id(
                )
            else:
                self.__log_warning(
                    "created_effective_profile_id", schema_name, table_name)
            if "is_test_data" in table_columns:
                data_dict["is_test_data"] = self.is_test_data
            else:
                self.__log_warning("is_test_data", schema_name, table_name)

            if "number" in table_columns:
                # TODO: the commented line caused errors, we need to check it
                # view_name = self.default_view_table_name or self._get_view_name(table_name)
                view_name = table_name
                number = NumberGenerator.get_random_number(
                    schema_name=schema_name, view_name=view_name)
                data_dict["number"] = number
            else:
                self.__log_warning("number", schema_name, table_name)

            if "identifier" in table_columns:
                self.__add_identifier(
                    data_dict=data_dict, table_name=table_name)
            else:
                self.__log_warning("identifier", schema_name, table_name)
        if "updated_user_id" in table_columns:
            data_dict["updated_user_id"] = self.user_context.get_effective_user_id()
        else:
            self.__log_warning("updated_user_id", schema_name, table_name)
        if "updated_real_user_id" in table_columns:
            data_dict["updated_real_user_id"] = self.user_context.get_real_user_id()
        else:
            self.__log_warning("updated_real_user_id", schema_name, table_name)
        if "updated_effective_user_id" in table_columns:
            data_dict["updated_effective_user_id"] = self.user_context.get_effective_user_id()
        else:
            self.__log_warning("updated_effective_user_id",
                               schema_name, table_name)
        if "updated_effective_profile_id" in table_columns:
            data_dict["updated_effective_profile_id"] = self.user_context.get_effective_profile_id()
        else:
            self.__log_warning("updated_effective_profile_id",
                               schema_name, table_name)

        #  TODO if (is_important_field_missing_in_table_columns)
            # self.logger.warning(f"The field is_test_data {schema_name}.{table_name} was not generated by the generate_table_columns.py script. You need to publish the database-mysql-python package again.")  # noqa E501

        # TODO: later we may want to add a check for the table_definition to see if there is a column for is_test_data
        # else:
        #     schema_name = schema_name or self.schema_name
        #     table_name = table_name or self.default_table_name
        #     if add_created_user_id:
        #         data_dict["created_user_id"] = self.user_context.get_effective_user_id()
        #         data_dict["created_real_user_id"] = self.user_context.get_real_user_id()
        #         data_dict["created_effective_user_id"] = self.user_context.get_effective_user_id()
        #         data_dict["created_effective_profile_id"] = self.user_context.get_effective_profile_id()
        #         # TODO: the commented line caused errors, we need to check it
        #         # view_name = self._get_view_name(table_name)
        #         view_name = table_name
        #         number = NumberGenerator.get_random_number(schema_name=schema_name, view_name=view_name)
        #         data_dict["number"] = number
        #
        #         # self.__add_identifier(data_dict=data_dict)
        #     data_dict["updated_user_id"] = self.user_context.get_effective_user_id()
        #     data_dict["updated_real_user_id"] = self.user_context.get_real_user_id()
        #     data_dict["updated_effective_user_id"] = self.user_context.get_effective_user_id()
        #     data_dict["updated_effective_profile_id"] = self.user_context.get_effective_profile_id()
        #     data_dict["is_test_data"] = self.is_test_data
        self.logger.debug(object=locals())
        return data_dict

    @lru_cache(maxsize=64)  # Don't show the same warning twice
    def __log_warning(self, column_name: str, schema_name: str, table_name: str):
        # TODO Add static is_important_field_missing_in_table_columns boolean field
        """Generates a warning log message and logs it."""
        self.logger.warning(f"{schema_name}.{table_name}.{column_name} not found in table_columns. Please run python -m src.generate_table_columns.py and publish database-mysql-local-python")  # noqa E501

    def __where_security(self, where: str, view_name: str) -> str:
        """Adds security to the where clause."""
        '''
        if self.is_column_in_table(column_name="visibility_id", schema_name=self.schema_name, table_name=view_name):
            effective_profile_id = self.user_context.get_effective_profile_id()
            where_security = f"(visibility_id > 1 OR created_effective_profile_id = {effective_profile_id})"
            if not (where == "" or where is None):
                where_security += f" AND ({where})"
            return where_security
        '''
        if view_name in table_definition:
            if table_definition[view_name].get("is_visibility"):
                effective_profile_id = self.user_context.get_effective_profile_id()
                where_security = f"(visibility_id > 1 OR created_effective_profile_id = {effective_profile_id})"
                if where:
                    where_security += f" AND ({where})"
                return where_security
        return where

    def set_schema(self, schema_name: Optional[str]):
        """Sets the given schema to be the default schema.
        In most cases you do not have to call this directly - you can pass schema_name to most functions"""
        if schema_name and self.default_schema_name != schema_name:
            self.connection.set_schema(schema_name)
            self.default_schema_name = schema_name

    def close(self) -> None:
        """Closes the connection to the database (we usually do not have to call this)"""
        try:
            self.connection.close()
        except Exception as e:
            self.logger.error(f"Error while closing the connection: {e}")

    @property
    def cursor(self) -> Cursor:
        """Get a new cursor"""
        if self._cursor.is_closed():
            self._cursor = self.connection.cursor()
        cursor = self._cursor
        return cursor

    @cursor.setter
    def cursor(self, value: Cursor) -> None:
        """Set the cursor"""
        self._cursor = value

    def get_test_entity_id(self, *, entity_name: str = None, insert_function: callable, insert_kwargs: dict = None,
                           entity_creator: callable = None, create_kwargs: dict = None,
                           schema_name: str = None, view_name: str = None,
                           select_clause_value: str = None) -> int:
        """
        1. Check if there's an entity with is `is_test_data=True`.
        2. If there is, return its id.
        3. If not, create a new entity with `is_test_data=True` and return its id.
        (assuming entity_creator expects `is_test_data` as parameters,
            and returns the expected argument for insert_function)

        Example: get_test_entity_id(entity_name='person', entity_creator=Person, insert_function=PersonsLocal.insert)
        """
        schema_name = schema_name or self.default_schema_name
        entity_name = entity_name or schema_name
        view_name = view_name or self.default_view_table_name
        select_clause_value = select_clause_value or entity_name + "_id"
        test_entity_id = self.select_one_value_by_column_and_value(
            schema_name=schema_name or self.default_schema_name, view_table_name=view_name,
            column_name='is_test_data', column_value='1', select_clause_value=select_clause_value,
            # To bring alway the 1st is_test_data so the test can relay on the value.
            order_by=select_clause_value)
        # TODO Make is implicit ASC
        if not test_entity_id:  # TODO: test
            insert_kwargs = insert_kwargs or {}
            create_kwargs = create_kwargs or {}
            # is_test_data from the constructor should be used in the sons to avoid duplications
            if entity_creator:
                entity_result = entity_creator(**create_kwargs)
                test_entity_id = insert_function(
                    entity_result, **insert_kwargs)
            else:
                test_entity_id = insert_function(**insert_kwargs)
        self.logger.debug(object=locals())
        return test_entity_id

    def create_view(self, schema_name=None, table_name=None, view_name=None):
        if table_name is not None and '_view' in table_name:
            return
        if schema_name is None:
            schema_name = self.default_schema_name

        if table_name is None:
            table_name = self.default_table_name

        if view_name is None:
            view_name = self.default_view_table_name

        print(f"Creating view {view_name} from {table_name}")
        create_view_query = f"""
        CREATE OR REPLACE VIEW `{schema_name}`.`{view_name}` AS
        SELECT * FROM `{schema_name}`.`{table_name}`;
        """

        self.cursor.execute(create_view_query)

    def create_column(self, schema_name: str, table_name: str, column_name: str, data_type: str, after_column: str = None, default_value: str = None):
        query = 'ALTER TABLE ' + schema_name + "." + table_name + \
            " ADD COLUMN " + column_name + " " + data_type + " NULL"
        if default_value is not None:
            query += " DEFAULT " + str(default_value)
        if after_column:
            query += " AFTER " + after_column
        self.cursor.execute(query)

    def merge_entities(self, entity_id1: int, entity_id2: int):
        table_name = self.default_table_name
        if 'ml' in table_name:
            table_prefix = table_name.replace("_ml_table", "")
        else:
            table_prefix = table_name.replace("_table", "")
            table_prefix = table_name[:-6]

        # establish which id is being merged/ended and which one it is being merged into
        end_id = entity_id1
        main_id = entity_id2

        # Data to update
        old_id = end_id
        new_id = main_id

        self.update_by_column_and_value(
            schema_name=self.default_schema_name,
            table_name=self.default_table_name,
            column_name=self.default_column_name,
            column_value=old_id,
            data_dict={f'new_{table_prefix}_id': new_id},
        )

    def foreach(self, where, limit, function, id_column_name, select_function: callable = None, **kwargs):
        # TODO: method select_multi_value_by_where() is not working as expected

        # result = self.select_multi_dict_by_where(where=where, limit=limit, select_clause_value="*")  # select_clause_value="test_mysql_id, number, name") # noqa
        select_function = select_function or self.select_multi_dict_by_where
        results = select_function(where=where, limit=limit, select_clause_value="*")  # select_clause_value="test_mysql_id, number, name") # noqa

        # self, *, schema_name: str = None, view_table_name: str = None, select_clause_value: str = None,
        # where: str = None, params: tuple = None, distinct: bool = False, limit: int = DEFAULT_SQL_SELECT_LIMIT,
        # order_by: str = None, skip_null_values: bool = True) -> tuple:
        function_results_dict = {}
        print(f"GenericCRUD.foreach() id_column_name={id_column_name}")
        for result in results:
            print(f"GenericCRUD.foreach() r={result}")
            if result[id_column_name]:
                id = result[id_column_name]
                r_our = OurObject(entity_name=self.default_entity_name,
                                  id_column_name=id_column_name,
                                  id=id,
                                  **result)
            else:
                print(f"There is no id in the row {result}", file=sys.stderr)
                r_our = OurObject(entity_name=self.default_entity_name,
                                  id_column_name=id_column_name,
                                  **result)
            kwargs["object"] = r_our

            # print(f"our r:{r_our}")
            # response = function(r_our)
            function_result = function(**kwargs)
            function_results_dict[id] = function_result
        return function_results_dict

    def get_view_name(self, schema_name: str) -> str:

        if self.default_view_with_deleted_and_test_data:
            view_table_name = self.default_view_with_deleted_and_test_data
        else:
            if schema_name == "test":
                view_table_name = f"{schema_name}_mysql_general_view"
            else:
                view_table_name = f"{schema_name}_view"

            # select_clause_value=select_clause_value)
            view_table_name = replace_view_with_table(
                view_table_name=view_table_name)

        return view_table_name
    
    # counts number of rows in the table - used in generic_crud_test.py
    # TODO Add a parameter is_my_records_only to count only the records created by the UserContect.get_effective_user_id - So we can use it in the tests
    def get_num_of_rows(self, schema_name: str = None, table_name: str = None) -> int:
        """Returns the total number of rows in the specified table."""
        schema_name = schema_name or self.default_schema_name
        table_name = table_name or self.default_table_name

        query = f"""
            SELECT COUNT(*) FROM {schema_name}.{table_name};
        """
        self.cursor.execute(query)
        total_rows = self.cursor.fetchone()[0]  # fetchone() gets the single row result, which is a tuple like (123,)
        return total_rows
