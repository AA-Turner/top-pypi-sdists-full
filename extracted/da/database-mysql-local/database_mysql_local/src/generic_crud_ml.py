import datetime
import re
from functools import lru_cache
from typing import Optional
from typing import Tuple
from language_remote.lang_code import LangCode
from logger_local.MetaLogger import MetaLogger
from user_context_remote.user_context import UserContext

# PyCham on MacOS need . before
from database_infrastructure_local.constants import DEFAULT_SQL_SELECT_LIMIT
from src.constants_src import IsTestData
from .constants_src import CRUD_ML_CODE_LOGGER_OBJECT
from .generic_crud import GenericCRUD
from .table_definition import table_definition
from .utils import generate_id_column_name, generate_table_name, generate_view_name, is_column_in_table

IS_MAIN_COLUMN_NAME = "is_main"


# TODO If I understand, there are two things:
#   - is_main in data_ml_dict
#   - table_definition_table.is_main_column
#   I'm not sure we need additional parameter.
class GenericCRUDML(GenericCRUD, metaclass=MetaLogger, object=CRUD_ML_CODE_LOGGER_OBJECT):
    """A class that provides generic CRUD functionality for tables with multi-language support."""

    # TODO: allow overiding all default values in all methods
    # TODO Shall we add same_entity method as parameter?
    def __init__(self, default_entity_name: str = None,
                 default_schema_name: str = None,
                 default_table_name: str = None,
                 default_view_table_name: str = None,
                 default_ml_table_name: str = None,
                 default_ml_view_table_name: str = None,
                 default_view_with_deleted_and_test_data: str = None,
                 default_column_name: str = None,  # default_select_clause_value: str = "*"
                 is_main_column_name: str = IS_MAIN_COLUMN_NAME, is_test_data: bool = False) -> None:
        """Initializes the GenericCRUDML class. If connection is not provided,
        a new connection will be created."""
        self.default_schema_name = default_schema_name or default_entity_name
        self.default_table_name = default_table_name or generate_table_name(entity_name=default_entity_name,
                                                                                 schema_name=default_schema_name,
                                                                                 ml_table_name=default_ml_table_name)
        self.default_ml_table_name = default_ml_table_name or self.generate_ml_table_name(default_table_name)
        self.default_ml_view_table_name = default_ml_view_table_name or generate_view_name(self.default_ml_table_name)
        self.default_view_with_deleted_and_test_data = default_view_with_deleted_and_test_data
        self.logger.info("GenericCRUDML.__init__", object={
            "default_ml_table_name": self.default_ml_table_name,
            "default_ml_view_table_name": self.default_ml_view_table_name})
        super().__init__(default_entity_name=default_entity_name,
                         default_schema_name=default_schema_name,
                         default_table_name=self.default_table_name,
                         default_view_table_name=default_view_table_name,
                         default_view_with_deleted_and_test_data=default_view_with_deleted_and_test_data,
                         default_column_name=default_column_name,
                         is_test_data=is_test_data)
        self.user_context = UserContext()
        # TODO: we may have to change it to a list when we will have multiple is_main columns
        self.is_main_column_name = is_main_column_name

    @lru_cache
    def sql_in_list_by_entity_list_id(self, *, schema_name: str = None, entity_name: str = None,
                                      entity_list_id: int) -> str:
        """Example: select group_id from group.group_list_member_table WHERE group_list_id=1"""
        schema_name = schema_name or self.default_schema_name
        entity_name = entity_name or schema_name
        ids = super().select_multi_dict_by_column_and_value(
            schema_name=schema_name, view_table_name=f"{entity_name}_list_member_view",
            select_clause_value=f"{entity_name}_id",
            column_name=f"{entity_name}_list_id", column_value=entity_list_id)
        if ids:
            result = f" IN ({','.join([str(_id[f'{entity_name}_id']) for _id in ids])})"
        else:
            result = " = TRUE"

        return result

    # TODO: should we rename all those methode similar to CRUD? (select, etc.)
    def add_value(self, *, schema_name: str = None, data_dict: dict = None, data_ml_dict: dict,
                  column_name: str = None,
                  table_id: int = None, lang_code: LangCode = None,
                  is_main: bool | None = None, table_name: str = None,
                  ml_table_name: str = None) -> Optional[tuple]:
        schema_name = schema_name or self.default_schema_name

        lang_code_str = self._get_lang_code_str(lang_code=lang_code, data_ml_dict=data_ml_dict)
        table_name = table_name or self.default_table_name
        # TODO Shall we also add "or self.default_column_name"?
        column_name = column_name or generate_id_column_name(table_name)
        ml_view_name = generate_view_name(ml_table_name) if ml_table_name else self.default_ml_view_table_name
        ml_table_name = ml_table_name or self.default_ml_table_name

        old_cursor = self.cursor
        try:
            self.cursor = self.connection.cursor()
            # if this is the first insert of this data, is_main should be True
            if table_id is None:
                is_main = True
            elif is_main:
                self._update_old_main_value_to_false(
                    schema_name=schema_name, table_name=table_name, table_id=table_id,
                    ml_table_name=ml_table_name)
            # TODO Why we have _column suffix?
            if table_definition.get(ml_table_name, {}).get("is_main_column"):
                data_ml_dict[self.is_main_column_name] = is_main

            # id is the id value of the row in the table_name table
            table_id = table_id or super().insert(
                schema_name=schema_name, table_name=table_name, data_dict=data_dict,
                ignore_duplicate=True, commit_changes=False)
            if table_id is None:  # TODO: delete?
                self.logger.error("Error inserting data_dict", object={"data_dict": data_dict})
                self.connection.rollback()
                return

            if not data_ml_dict:
                self.connection.commit()
                ml_table_id = None
                return table_id, ml_table_id

            data_ml_dict[column_name] = table_id
            data_ml_dict["lang_code"] = lang_code_str

            # ml_id is the id value of the row in the ml_table_name table
            # we do not allow inserting a new value if exist and there's not is_main column
            if not is_main and not table_definition.get(ml_table_name, {}).get("is_main_column"):
                already_exists = super().select_one_value_by_where(
                    schema_name=schema_name, view_table_name=ml_view_name,
                    where=f"{column_name}=%s AND lang_code=%s", params=(table_id, lang_code_str),
                    select_clause_value=column_name)
                if already_exists:
                    raise Exception(f"Value already exists in {ml_table_name} table. Use delete / update.")
            ml_table_id = super().insert(schema_name=schema_name, data_dict=data_ml_dict, table_name=ml_table_name,
                                         ignore_duplicate=True, commit_changes=False)

            self.connection.commit()
        except Exception as e:
            # TODO Shall we add retry mechanism?
            self.connection.rollback()
            raise e
        finally:
            self.cursor.close()
            self.cursor = old_cursor
        return table_id, ml_table_id

    # TODO add parameter if_same_even_deleted_return_existing_id=true - When inserting a deleted entity (all entities except person and tables of codes i.e. country, state, county, city, neighbourhood, street ...) and table_definition.insert_is_undelete=false, we should null all the unique fields of the deleted entity  # noqa
    def add_value_if_not_exist(
            self, *, data_dict: dict = None, data_ml_dict: dict,
            table_id: int = None, lang_code: LangCode = None,
            is_main: bool = None, table_name: str = None, ml_table_name: str = None, schema_name: str = None,
            order_by: str = None) -> Tuple[int, int]:

        schema_name = schema_name or self.default_schema_name
        table_name = table_name or self.default_table_name
        ml_table_name = ml_table_name or self.default_ml_table_name
        column_name = generate_id_column_name(table_name)
        ml_column_name = generate_id_column_name(ml_table_name)

        # check if the row exists in the ml_table
        if data_dict:
            name = data_dict.get("name") or data_dict.get("title")
        else:
            name = data_ml_dict.get("name") or data_ml_dict.get("title")
        # name = data_dict.get("name") or data_ml_dict.get("title")
        title = data_ml_dict.get("title") or data_dict.get("name")
        if not name:
            raise ValueError("name or title is required for add_value_if_not_exist")
        table_id = table_id or self.get_id_by_name(
            schema_name=schema_name, table_name=table_name, ml_table_name=ml_table_name, name=name,
            lang_code=lang_code, column_name=column_name, order_by=order_by)
        ml_table_id = self.get_ml_id_by_title(
            schema_name=schema_name, ml_table_name=ml_table_name, name=title, lang_code=lang_code,
            column_name=ml_column_name, order_by=order_by)
        if not table_id:
            table_id, ml_table_id = self.add_value(
                schema_name=schema_name, data_ml_dict=data_ml_dict, table_id=table_id, lang_code=lang_code,
                is_main=is_main, data_dict=data_dict, table_name=table_name, ml_table_name=ml_table_name,
                column_name=column_name)
        return table_id, ml_table_id

    def update_value_by_id(
            self, *, data_dict: dict = None, data_ml_dict: dict,
            ml_table_id: int, table_id: int, lang_code: LangCode = None,
            is_main: bool = None, table_name: str = None, ml_table_name: str = None, schema_name: str = None,
            limit: int = DEFAULT_SQL_SELECT_LIMIT, order_by: str = None) -> Tuple[int, int]:

        schema_name = schema_name or self.default_schema_name
        lang_code_str = self._get_lang_code_str(lang_code=lang_code, data_ml_dict=data_ml_dict)
        table_name = table_name or self.default_table_name
        ml_table_name = ml_table_name or self.default_ml_table_name
        column_name = generate_id_column_name(table_name)

        if table_id is None:
            raise ValueError("table_id is required for update_value")
        if ml_table_id is None:
            raise ValueError("ml_table_id is required for update_value")
        old_cursor = self.cursor
        try:
            self.cursor = self.connection.cursor()
            if is_main:
                self._update_old_main_value_to_false(schema_name=schema_name, table_name=table_name,
                                                     table_id=table_id, ml_table_name=ml_table_name)
            if table_definition.get(ml_table_name, {}).get("is_main_column"):
                data_ml_dict[self.is_main_column_name] = is_main
            if data_dict:
                super().update_by_column_and_value(schema_name=schema_name, table_name=table_name,
                                                   column_name=column_name,
                                                   column_value=table_id, data_dict=data_dict, limit=limit,
                                                   order_by=order_by,
                                                   commit_changes=False)

            data_ml_dict[column_name] = table_id
            data_ml_dict["lang_code"] = lang_code_str
            column_name = generate_id_column_name(ml_table_name)

            super().update_by_column_and_value(schema_name=schema_name, table_name=ml_table_name,
                                               data_dict=data_ml_dict,
                                               column_name=column_name, column_value=ml_table_id, limit=limit,
                                               order_by=order_by,
                                               commit_changes=False)

            self.connection.commit()
        except Exception as e:
            self.connection.rollback()
            raise e
        finally:
            self.cursor.close()
            self.cursor = old_cursor
        return table_id, ml_table_id

    def upsert_value(
            self, *, data_dict: dict = None, data_ml_dict: dict, data_dict_compare: dict = None,
            table_id: int = None, lang_code: LangCode = None, is_main: bool = None, table_name: str = None,
            ml_table_name: str = None, schema_name: str = None, compare_view_name: str = None,
            limit: int = DEFAULT_SQL_SELECT_LIMIT, order_by: str = None) -> Tuple[int, int]:
        compare_view_name = compare_view_name or self.default_ml_view_table_name

        schema_name = schema_name or self.default_schema_name
        table_name = table_name or self.default_table_name
        ml_table_name = ml_table_name or self.default_ml_table_name
        column_name = generate_id_column_name(table_name)
        ml_column_name = generate_id_column_name(ml_table_name)

        # check if the row exists in the ml_table
        name = data_dict.get("name") or data_ml_dict.get("title")
        title = data_ml_dict.get("title") or data_dict.get("name")
        name_compare = name
        title_to_compare = title
        if not name:
            raise ValueError("name or title is required for upsert_value")
        if data_dict_compare:
            name_compare = data_dict_compare.get("name") or data_dict_compare.get("title")
            title_to_compare = data_dict_compare.get("title") or data_dict_compare.get("name")

        table_id = table_id or self.get_id_by_name(
            schema_name=schema_name, table_name=table_name, ml_table_name=ml_table_name,
            name=name_compare, compare_view_name=compare_view_name,
            column_name=column_name, order_by=order_by)
        ml_table_id = self.get_ml_id_by_title(
            schema_name=schema_name, ml_table_name=ml_table_name, name=title_to_compare, lang_code=lang_code,
            compare_view_name=compare_view_name, column_name=ml_column_name, order_by=order_by)
        if not table_id or not ml_table_id:
            table_id, ml_table_id = self.add_value(
                schema_name=schema_name, data_ml_dict=data_ml_dict, table_id=table_id, lang_code=lang_code,
                is_main=is_main, data_dict=data_dict, table_name=table_name, ml_table_name=ml_table_name,
                column_name=column_name)
        else:
            table_id, ml_table_id = self.update_value_by_id(
                schema_name=schema_name, data_ml_dict=data_ml_dict, ml_table_id=ml_table_id, table_id=table_id,
                lang_code=lang_code, is_main=is_main, data_dict=data_dict, table_name=table_name,
                ml_table_name=ml_table_name, limit=limit, order_by=order_by)
        return table_id, ml_table_id

    def upsert_value_with_abbreviations(
            self, *, data_dict: dict = None, data_ml_dict: dict,

            data_dict_compare: dict = None, table_id: int = None, order_by: str = None,
            table_name: str = None, ml_table_name: str = None, schema_name: str = None, lang_code: LangCode = None,
            compare_view_name: str = None, limit: int = DEFAULT_SQL_SELECT_LIMIT) -> Tuple[int, list[int]]:
        compare_view_name = compare_view_name or self.default_ml_view_table_name
        schema_name = schema_name or self.default_schema_name
        table_name = table_name or self.default_table_name
        ml_table_name = ml_table_name or self.default_ml_table_name
        column_name = generate_id_column_name(table_name)
        ml_column_name = generate_id_column_name(ml_table_name)

        # check if the row exists in the ml_table
        name_and_abbreviations = data_ml_dict.get("title") or data_dict.get("name")
        if not name_and_abbreviations:
            raise ValueError("name or title is required for upsert_value")
        if data_dict_compare:
            name_and_abbreviations_compare = data_dict_compare.get("title") or data_dict_compare.get("name")
        else:
            name_and_abbreviations_compare = name_and_abbreviations

        name = name_and_abbreviations.split(" (")[0]
        name_compare = name_and_abbreviations_compare.split(" (")[0]
        abbreviations = name_and_abbreviations.split(" (")[1][:-1]
        abbreviations_list = abbreviations.split(", ")
        data_ml_dict_with_name = data_ml_dict.copy()
        data_ml_dict_with_name["title"] = name
        data_ml_dict_with_abbreviation_list = []
        for abbreviation in abbreviations_list:
            data_ml_dict_with_abbreviation = data_ml_dict.copy()
            data_ml_dict_with_abbreviation["title"] = abbreviation
            data_ml_dict_with_abbreviation_list.append(data_ml_dict_with_abbreviation)

        table_id = table_id or self.get_id_by_name(
            schema_name=schema_name, table_name=table_name, ml_table_name=ml_table_name,
            name=name_compare, lang_code=lang_code, compare_view_name=compare_view_name,
            column_name=column_name, order_by=order_by)
        ml_table_id = self.get_ml_id_by_title(
            schema_name=schema_name, ml_table_name=ml_table_name, name=name_compare, lang_code=lang_code,
            compare_view_name=compare_view_name, column_name=ml_column_name, order_by=order_by)
        ml_ids_list = []
        if not table_id:
            table_id, ml_table_id = self.add_value(
                schema_name=schema_name, data_ml_dict=data_ml_dict_with_name, table_id=table_id,
                lang_code=lang_code, is_main=True, data_dict=data_dict, table_name=table_name,
                ml_table_name=ml_table_name)
            ml_ids_list.append(ml_table_id)
            for data_ml_dict_with_abbreviation in data_ml_dict_with_abbreviation_list:
                table_id, ml_table_id = self.add_value(
                    schema_name=schema_name, data_ml_dict=data_ml_dict_with_abbreviation, table_id=table_id,
                    lang_code=lang_code, is_main=None, data_dict=data_dict, table_name=table_name,
                    ml_table_name=ml_table_name)
                ml_ids_list.append(ml_table_id)
        else:
            ml_ids_list = list(self.get_ml_ids_by_id(
                schema_name=schema_name, table_id=table_id, ml_table_name=ml_table_name, lang_code=lang_code,
                column_name=column_name, ml_column_name=ml_column_name, compare_view_name=compare_view_name,
                order_by=order_by))
            ml_ids_list.remove(ml_table_id)
            table_id, main_ml_table_id = self.update_value_by_id(
                schema_name=schema_name, data_ml_dict=data_ml_dict_with_name, ml_table_id=ml_table_id,
                table_id=table_id, lang_code=lang_code, is_main=True, data_dict=data_dict,
                table_name=table_name, ml_table_name=ml_table_name, limit=limit, order_by=order_by)
            for index, data_ml_dict_with_abbreviation in enumerate(data_ml_dict_with_abbreviation_list):
                if index < len(ml_ids_list):
                    table_id, ml_table_id = self.update_value_by_id(
                        data_ml_dict=data_ml_dict_with_abbreviation, ml_table_id=ml_ids_list[index],
                        table_id=table_id, lang_code=lang_code, is_main=None, data_dict=data_dict,
                        table_name=table_name, ml_table_name=ml_table_name, schema_name=schema_name,
                        limit=limit, order_by=order_by)
                else:
                    table_id, ml_table_id = self.add_value(
                        schema_name=schema_name, data_ml_dict=data_ml_dict_with_abbreviation, table_id=table_id,
                        lang_code=lang_code, is_main=None, data_dict=data_dict, table_name=table_name,
                        ml_table_name=ml_table_name)
                ml_ids_list.append(ml_table_id)
            ml_ids_list.append(main_ml_table_id)
        return table_id, ml_ids_list

    def get_values_tuple(self, *, table_id: int, schema_name: str = None, ml_view_table_name: str = None,
                         lang_code: LangCode = None, column_name: str = None,
                         select_clause_value: str = "*", order_by: str = None) -> Tuple[int, int]:
        lang_code_str = self._get_lang_code_str(lang_code=lang_code)
        ml_view_table_name = ml_view_table_name or self.default_ml_view_table_name
        column_name = column_name or self.default_column_name
        schema_name = schema_name or self.default_schema_name
        result = super().select_one_tuple_by_where(
            schema_name=schema_name, view_table_name=ml_view_table_name,
            where=f"{column_name}=%s AND lang_code=%s", params=(table_id, lang_code_str),
            select_clause_value=select_clause_value, order_by=order_by)

        return result

    def get_values_dict(self, table_id: int, lang_code: LangCode = None,
                        column_name: str = None, order_by: str = None) -> dict:

        lang_code_str = self._get_lang_code_str(lang_code=lang_code)
        column_name = column_name or generate_id_column_name(self.default_table_name)
        result = super().select_one_dict_by_where(
            view_table_name=self.default_ml_view_table_name, order_by=order_by,
            where=f"{column_name}=%s AND lang_code=%s", params=(table_id, lang_code_str))

        return result

    def get_values_dict_list(self, *, table_id: int, lang_code: LangCode = None,
                             column_name: str = None, order_by: str = None, schema_name: str = None, limit: int = DEFAULT_SQL_SELECT_LIMIT) -> list:
        schema_name = schema_name or self.default_schema_name

        column_name = column_name or self.default_column_name
        lang_code_str = self._get_lang_code_str(lang_code=lang_code)

        result = self.select_multi_dict_by_where(
            schema_name=schema_name, view_table_name=self.default_ml_view_table_name,
            where=f"{column_name}=%s AND lang_code=%s", params=(table_id, lang_code_str),
            order_by=order_by, limit=limit)
        return result

    def get_values_dict_list_by_where(self, *, lang_code: LangCode = None,  # table_id: int,
                                      column_name: str = None, order_by: str = None, schema_name: str = None,
                                      limit: int = DEFAULT_SQL_SELECT_LIMIT, where: str, select_clause_value: str) -> list:
        schema_name = schema_name or self.default_schema_name

        view_table_name = self.get_view_name(schema_name=schema_name)

        column_name = column_name or self.default_column_name
        lang_code_str = self._get_lang_code_str(lang_code=lang_code)

        result = self.select_multi_dict_by_where(
            schema_name=schema_name, view_table_name=view_table_name, select_clause_value=select_clause_value,
            where=f"{where} AND lang_code=%s", params=(lang_code_str,),
            order_by=order_by, limit=limit)
        return result

    def get_main_values_tuple(self, *, table_id: int, column_name: str = None,
                              select_clause_value: str = "*", order_by: str = None, schema_name: str = None) -> Tuple[int, int]:
        schema_name = schema_name or self.default_schema_name

        column_name = column_name or generate_id_column_name(self.default_table_name)
        result = self.select_one_tuple_by_where(
            schema_name=schema_name, view_table_name=self.default_ml_view_table_name,
            where=f"{column_name}=%s AND is_main=True", params=(table_id,),
            select_clause_value=select_clause_value, order_by=order_by)

        return result

    def get_main_values_dict(self, *, table_id: int, column_name: str = None,
                             select_clause_value: str = "*", order_by: str = None, schema_name: str = None) -> dict:
        schema_name = schema_name or self.default_schema_name

        column_name = column_name or self.default_column_name
        result = super().select_one_dict_by_where(
            schema_name=schema_name, view_table_name=self.default_ml_view_table_name,
            where=f"{column_name}=%s AND is_main=True", params=(table_id,),
            select_clause_value=select_clause_value, order_by=order_by)

        return result

    def get_id_by_name(self, *, name: str, schema_name: str = None, table_name: str = None, ml_table_name: str = None,
                       lang_code: LangCode = None,
                       column_name: str = None, order_by: str = None,
                       compare_view_name: str = None) -> Optional[int]:
        schema_name = schema_name or self.default_schema_name

        lang_code_str = self._get_lang_code_str(lang_code=lang_code, name=name)
        table_name = table_name or self.default_table_name
        ml_table_name = ml_table_name or self.default_ml_table_name
        compare_view_name = compare_view_name or generate_view_name(ml_table_name)
        column_name = column_name or generate_id_column_name(table_name)
        if is_column_in_table(table_name=ml_table_name, column_name="title"):
            where = "`title`=%s"
            params = (name,)
            if lang_code:
                where += " AND lang_code=%s"
                params += (lang_code_str,)
        else:
            where = "`name`=%s"
            params = (name,)
            if lang_code:
                where += " AND lang_code=%s"
                params += (lang_code_str,)
        result = super().select_one_value_by_where(
            schema_name=schema_name, view_table_name=compare_view_name,
            where=where, params=params,
            select_clause_value=column_name, order_by=order_by)
        return result

    def get_ml_id_by_title(self, *, name: str, schema_name: str = None, ml_table_name: str = None,
                           lang_code: LangCode = None,
                           column_name: str = None, order_by: str = None,
                           compare_view_name: str = None) -> Optional[int]:

        lang_code_str = self._get_lang_code_str(lang_code=lang_code, name=name)
        ml_table_name = ml_table_name or self.default_ml_table_name
        schema_name = schema_name or self.default_schema_name
        compare_view_name = compare_view_name or generate_view_name(ml_table_name)
        ml_column_name = column_name or generate_id_column_name(ml_table_name)
        if is_column_in_table(table_name=ml_table_name, column_name="title"):
            where = "title=%s"
            params = (name,)
            if lang_code:
                where += " AND lang_code=%s"
                params += (lang_code_str,)
        else:
            where = "`name`=%s"
            params = (name,)
            if lang_code:
                where += " AND lang_code=%s"
                params += (lang_code_str,)
        result = super().select_one_value_by_where(
            schema_name=schema_name, view_table_name=compare_view_name,
            select_clause_value=ml_column_name, order_by=order_by,
            where=where, params=(name, lang_code_str))
        return result

    def get_ml_ids_by_id(self, table_id: int, ml_table_name: str = None, lang_code: LangCode = None,
                         column_name: str = None, ml_column_name: str = None,
                         order_by: str = None, compare_view_name: str = None, schema_name: str = None) -> tuple:
        schema_name = schema_name or self.default_schema_name

        lang_code_str = None if lang_code is None else lang_code.value
        compare_view_name = compare_view_name or generate_view_name(ml_table_name)
        result = super().select_multi_value_by_where(
            schema_name=schema_name, view_table_name=compare_view_name,
            select_clause_value=ml_column_name, order_by=order_by,
            where=f"{column_name}=%s AND lang_code=%s", params=(table_id, lang_code_str))
        return result

    def get_all_ml_ids_by_id(self, table_id: int, ml_table_name: str = None,
                             column_name: str = None, ml_column_name: str = None,
                             order_by: str = None, compare_view_name: str = None, schema_name: str = None) -> tuple:
        schema_name = schema_name or self.default_schema_name

        compare_view_name = compare_view_name or generate_view_name(ml_table_name)
        result = super().select_multi_value_by_where(
            schema_name=schema_name, view_table_name=compare_view_name,
            select_clause_value=ml_column_name, order_by=order_by,
            where=f"{column_name}=%s", params=(table_id))
        return result

    def delete_by_name(self, *, name: str, lang_code: LangCode = None) -> int:
        lang_code_str = self._get_lang_code_str(lang_code=lang_code, name=name)
        if is_column_in_table(table_name=self.default_ml_view_table_name, column_name="title"):
            where = "title=%s AND lang_code=%s"
        else:
            where = "`name`=%s AND lang_code=%s"
        deleted_id = super().delete_by_where(table_name=self.default_ml_table_name, where=where,
                                             params=(name, lang_code_str))
        return deleted_id


    @staticmethod
    def generate_ml_table_name(table_name: str) -> str:
        if table_name:
            ml_table_name = re.sub(r'(_table)$', '_ml_table', table_name)
            return ml_table_name

    # Change the old row with is_main=True to is_main=None
    def _update_old_main_value_to_false(self, *, schema_name: str, table_id: int, table_name: str,
                                        ml_table_name: str) -> int:
        data_ml_dict = {self.is_main_column_name: False}
        column_name = generate_id_column_name(table_name)
        where = f"{column_name}=%s AND {self.is_main_column_name} = True"
        updated_id = super().update_by_where(schema_name=schema_name, table_name=ml_table_name,
                                             data_dict=data_ml_dict, where=where, params=(table_id,))
        return updated_id

    def _get_lang_code_str(self, *, name: str = None, lang_code: LangCode = None,
                           data_ml_dict: dict = None) -> str:

        if lang_code is None and name is not None:
            lang_code_str = LangCode.detect_lang_code_str(name)
        elif lang_code is None and data_ml_dict is not None:
            text = data_ml_dict.get("title") or data_ml_dict.get("name")
            lang_code_str = LangCode.detect_lang_code_str(text)
        elif lang_code is None:
            lang_code_str = self.user_context.get_effective_profile_preferred_lang_code_string()
        else:
            lang_code_str = lang_code.value
        return lang_code_str

    def merge_ml_entities(self, entity_id1: int, entity_id2: int, main_entity_ml_id: int = None):
        DEFAULT_ORDER_BY = "updated_timestamp DESC"
        schema_name = self.default_schema_name
        table_name = self.default_table_name
        table_prefix = table_name.replace("_ml_table", "")
        generated_ml_table_name = table_prefix + '_ml_table'
        generated_ml_view_name = table_prefix + '_ml_view'
        generated_table_name = table_prefix + '_table'
        gcrml = GenericCRUDML(default_schema_name=schema_name,
                              default_ml_table_name=generated_ml_table_name,
                              is_test_data=IsTestData.TEMP_DATA.value,
                              default_table_name=generated_table_name,
                              default_ml_view_table_name=generated_ml_view_name,
                              is_main_column_name='is_main_title')
        # establish which id is being merged/ended and which one it is being merged into
        end_id = entity_id1
        main_id = entity_id2

        # Data to update
        old_id = end_id
        new_id = main_id
        # get the ml ids of the city id which is being merged

        generated_ml_column_name = table_prefix + '_ml_id'
        generated_column_name = table_prefix + '_id'
        ml_ids = gcrml.get_all_ml_ids_by_id(table_id=old_id, ml_column_name=generated_ml_column_name, order_by=DEFAULT_ORDER_BY,
                                            ml_table_name=generated_ml_table_name,
                                            column_name=generated_column_name, compare_view_name=generated_ml_view_name)

        # get a list of existing langcodes for the id which is being merged into
        langcode_list = self.get_lang_codes_by_table_id(table_id=new_id, ml_view_table_name=generated_ml_view_name,
                                                        schema_name=self.default_schema_name)

        for id in ml_ids:
            # get the langcode of the ml id being merged. if it already exists in the id being merged into, then set this one to false.
            langcode = gcrml.select_one_value_by_column_and_value(select_clause_value='lang_code', column_name=generated_ml_column_name,
                                                                  column_value=id, view_table_name=generated_ml_view_name)
            if langcode in langcode_list:
                gcrml.update_by_column_and_value(
                    table_name=generated_ml_table_name,
                    column_name=generated_ml_column_name,
                    column_value=id,
                    data_dict={'is_main_title': None}, )
            # update the id for the ml_id to the new id
            gcrml.update_by_column_and_value(
                table_name=generated_ml_table_name,
                column_name=generated_ml_column_name,
                column_value=id,
                data_dict={generated_column_name: new_id, }
            )

        gcrml.update_by_column_and_value(
            table_name=generated_table_name,
            column_name=generated_column_name,
            column_value=old_id,
            data_dict={"end_timestamp": datetime.datetime.now()},
        )
        # Set the main id
        if main_entity_ml_id is not None:
            gcrml.update_by_column_and_value(
                table_name=generated_ml_table_name,
                column_name=generated_ml_column_name,
                column_value=main_entity_ml_id,
                data_dict={'is_main_title': True},)

    def get_lang_codes_by_table_id(self, table_id: int, schema_name: str = None, ml_view_table_name: str = None) -> list:
        schema_name = schema_name or self.default_schema_name
        ml_view_table_name = ml_view_table_name or self.default_ml_view_table_name
        table_name = self.default_table_name
        table_prefix = table_name.replace("_ml_table", "")
        generated_column_name = table_prefix + '_id'

        result = self.select_multi_dict_by_where(
            schema_name=schema_name,
            view_table_name=ml_view_table_name,
            where=f"{generated_column_name}=%s",
            params=(table_id,),
            select_clause_value="lang_code"
        )

        return [entry['lang_code'] for entry in result if 'lang_code' in entry]
