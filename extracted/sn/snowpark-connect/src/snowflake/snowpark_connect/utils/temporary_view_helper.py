#
# Copyright (c) 2012-2025 Snowflake Computing Inc. All rights reserved.
#
import re
import uuid
from collections import Counter
from typing import Optional, Tuple

from pyspark.errors import AnalysisException
from pyspark.errors.exceptions.base import TempTableAlreadyExistsException

from snowflake.snowpark import DataFrame, Session
from snowflake.snowpark._internal.analyzer.analyzer_utils import unquote_if_quoted
from snowflake.snowpark.exceptions import SnowparkSQLException
from snowflake.snowpark.types import StructField, StructType
from snowflake.snowpark_connect.column_name_handler import ColumnNames
from snowflake.snowpark_connect.config import (
    global_config,
    sessions_config,
    should_create_temporary_view_in_snowflake,
)
from snowflake.snowpark_connect.dataframe_container import DataFrameContainer
from snowflake.snowpark_connect.utils.concurrent import SynchronizedDict
from snowflake.snowpark_connect.utils.context import get_spark_session_id
from snowflake.snowpark_connect.utils.identifiers import (
    spark_to_sf_single_id,
    spark_to_sf_single_id_with_unquoting,
)

_INTERNAL_VIEW_PREFIX = "__SC_RENAMED_V_"

_CREATE_VIEW_PATTERN = re.compile(r"create\s+or\s+replace\s+view", re.IGNORECASE)

_temp_views = SynchronizedDict[Tuple[str, str], DataFrameContainer]()


def register_temp_view(name: str, df: DataFrameContainer, replace: bool) -> None:
    normalized_name = _normalize(name)
    current_session_id = get_spark_session_id()
    for key in list(_temp_views.keys()):
        if _normalize(key[0]) == normalized_name and key[1] == current_session_id:
            if replace:
                _temp_views.remove(key)
                break
            else:
                raise TempTableAlreadyExistsException(
                    f"[TEMP_TABLE_OR_VIEW_ALREADY_EXISTS] Cannot create the temporary view `{name}` because it already exists."
                )

    _temp_views[(name, current_session_id)] = df


def unregister_temp_view(name: str) -> bool:
    normalized_name = _normalize(name)

    for key in _temp_views.keys():
        normalized_key = _normalize(key[0])
        if normalized_name == normalized_key and key[1] == get_spark_session_id():
            pop_result = _temp_views.remove(key)
            return pop_result is not None
    return False


def get_temp_view(name: str) -> Optional[DataFrameContainer]:
    normalized_name = _normalize(name)
    for key in _temp_views.keys():
        normalized_key = _normalize(key[0])
        if normalized_name == normalized_key and key[1] == get_spark_session_id():
            return _temp_views.get(key)
    return None


def get_temp_view_normalized_names() -> list[str]:
    return [
        _normalize(key[0])
        for key in _temp_views.keys()
        if key[1] == get_spark_session_id()
    ]


def _normalize(name: str) -> str:
    return name if global_config.spark_sql_caseSensitive else name.lower()


def assert_snowflake_view_does_not_exist_in_cache(name: str, replace: bool):
    temp_view = get_temp_view(name)
    if temp_view is not None and not replace:
        raise AnalysisException(
            f"[TEMP_TABLE_OR_VIEW_ALREADY_EXISTS] Cannot create the temporary view `{name}` because it already exists."
        )


def assert_cached_view_does_not_exist_in_snowflake(
    snowflake_view_name: list[str], replace: bool
):
    if len(snowflake_view_name) == 1:
        name = unquote_if_quoted(snowflake_view_name[0])
        sql_statement = f"SHOW VIEWS LIKE '{name}'"
    else:
        name = unquote_if_quoted(snowflake_view_name[1])
        sql_statement = f"SHOW VIEWS LIKE '{name}' IN SCHEMA {snowflake_view_name[0]}"
    if (
        not replace
        and len(Session.get_active_session().sql(sql_statement).collect()) > 0
    ):
        raise AnalysisException(
            f"[TEMP_TABLE_OR_VIEW_ALREADY_EXISTS] Cannot create the temporary view `{name}` because it already exists."
        )


def create_temporary_view_from_dataframe(
    input_df_container: DataFrameContainer,
    request_view_name: str,
    is_global: bool,
    replace: bool,
) -> None:
    if is_global:
        view_name = [global_config.spark_sql_globalTempDatabase, request_view_name]
    else:
        view_name = [request_view_name]
    case_sensitive_view_name = ".".join(
        [spark_to_sf_single_id_with_unquoting(part) for part in view_name]
    )
    snowflake_view_name = [
        spark_to_sf_single_id_with_unquoting(part, True) for part in view_name
    ]

    if should_create_temporary_view_in_snowflake():
        _create_snowflake_temporary_view(
            input_df_container, snowflake_view_name, case_sensitive_view_name, replace
        )
    else:
        store_temporary_view_as_dataframe(
            input_df_container,
            input_df_container.column_map.get_spark_columns(),
            input_df_container.column_map.get_snowpark_columns(),
            case_sensitive_view_name,
            snowflake_view_name,
            replace,
        )


def _create_snowflake_temporary_view(
    input_df_container: DataFrameContainer,
    snowflake_view_name: list[str],
    stored_view_name: str,
    replace: bool,
):
    column_map = input_df_container.column_map
    input_df = input_df_container.dataframe

    session_config = sessions_config[get_spark_session_id()]
    duplicate_column_names_handling_mode = session_config[
        "snowpark.connect.views.duplicate_column_names_handling_mode"
    ]

    # rename columns to match spark names
    if duplicate_column_names_handling_mode == "rename":
        # deduplicate column names by appending _DEDUP_1, _DEDUP_2, etc.
        rename_map = _create_column_rename_map(column_map.columns, True)
        input_df = input_df.rename(rename_map)
    elif duplicate_column_names_handling_mode == "drop":
        # Drop duplicate column names by removing all but the first occurrence.
        duplicated_columns, remaining_columns = _find_duplicated_columns(
            column_map.columns
        )
        rename_map = _create_column_rename_map(remaining_columns, False)
        if len(duplicated_columns) > 0:
            input_df = input_df.drop(*duplicated_columns)
        input_df = input_df.rename(rename_map)
    else:
        # rename columns without deduplication
        rename_map = _create_column_rename_map(column_map.columns, False)
        input_df = input_df.rename(rename_map)

    try:
        create_snowflake_temporary_view(
            input_df, snowflake_view_name, stored_view_name, replace
        )
    except SnowparkSQLException as exc:
        if _is_error_caused_by_view_referencing_itself(exc) and replace:
            # This error is caused by statement with self reference like `CREATE VIEW A AS SELECT X FROM A`.
            _create_chained_view(input_df, snowflake_view_name)
        else:
            raise


def _create_column_rename_map(
    columns: list[ColumnNames], rename_duplicated: bool
) -> dict:
    if rename_duplicated is False:
        # if we are not renaming duplicated columns, we can just return the original names
        return {
            col.snowpark_name: spark_to_sf_single_id(col.spark_name, is_column=True)
            for col in columns
        }

    column_counts = Counter()
    not_renamed_cols = []
    renamed_cols = []

    for col in columns:
        new_column_name = col.spark_name
        normalized_name = new_column_name.lower()
        column_counts[normalized_name] += 1

        if column_counts[normalized_name] > 1:
            new_column_name = (
                f"{new_column_name}_DEDUP_{column_counts[normalized_name] - 1}"
            )
            renamed_cols.append(ColumnNames(new_column_name, col.snowpark_name, []))
        else:
            not_renamed_cols.append(ColumnNames(new_column_name, col.snowpark_name, []))

    if len(renamed_cols) == 0:
        return {
            col.snowpark_name: spark_to_sf_single_id(col.spark_name, is_column=True)
            for col in not_renamed_cols
        }

    # we need to make sure that we don't have duplicated names after renaming
    # columns that were not renamed in this iteration should have priority over renamed duplicates
    return _create_column_rename_map(not_renamed_cols + renamed_cols, True)


def _find_duplicated_columns(
    columns: list[ColumnNames],
) -> (list[str], list[ColumnNames]):
    duplicates = []
    remaining_columns = []
    seen = set()
    for col in columns:
        if col.spark_name in seen:
            duplicates.append(col.snowpark_name)
        else:
            seen.add(col.spark_name)
            remaining_columns.append(col)
    return duplicates, remaining_columns


def _generate_random_builtin_view_name() -> str:
    return _INTERNAL_VIEW_PREFIX + str(uuid.uuid4()).replace("-", "")


def _is_error_caused_by_view_referencing_itself(exc: Exception) -> bool:
    return "view definition refers to view being defined" in str(exc).lower()


def _create_chained_view(input_df: DataFrame, view_name: list[str]) -> None:
    """
    In order to create a view, which references itself, Spark would here take the previous
    definition of A and paste it in place of `FROM A`. Snowflake would fail in such case, so
    as a workaround, we create a chain of internal views instead. This function:
    1. Renames previous definition of A to some internal name (instead of deleting).
    2. Adjusts the DDL of a new statement to reference the name of a renmaed internal view, instead of itself.
    """

    session = Session.get_active_session()

    view_name = ".".join(view_name)

    tmp_name = _generate_random_builtin_view_name()
    old_name_replacement = _generate_random_builtin_view_name()

    input_df.create_or_replace_temp_view(tmp_name)

    session.sql(f"ALTER VIEW {view_name} RENAME TO {old_name_replacement}").collect()

    ddl: str = session.sql(f"SELECT GET_DDL('VIEW', '{tmp_name}')").collect()[0][0]

    ddl = ddl.replace(view_name, old_name_replacement)

    # GET_DDL result doesn't contain `TEMPORARY`, it's likely a bug.
    ddl = _CREATE_VIEW_PATTERN.sub("create or replace temp view", ddl)

    session.sql(ddl).collect()

    session.sql(f"ALTER VIEW {tmp_name} RENAME TO {view_name}").collect()


def store_temporary_view_as_dataframe(
    input_container: DataFrameContainer,
    spark_columns: list[str],
    snowpark_columns: list[str],
    view_name: str,
    snowflake_view_name: list[str],
    replace: bool,
):
    assert_cached_view_does_not_exist_in_snowflake(snowflake_view_name, replace)

    if not input_container.has_zero_columns():
        input_df = input_container.dataframe
        schema = StructType(
            [
                StructField(field.name, field.datatype)
                for field in input_df.schema.fields
            ]
        )
        input_df_container = DataFrameContainer.create_with_column_mapping(
            dataframe=input_df,
            spark_column_names=spark_columns,
            snowpark_column_names=snowpark_columns,
            parent_column_name_map=input_container.column_map,
            cached_schema_getter=lambda: schema,
        )
    else:
        # just use the current container
        input_df_container = input_container

    if replace:
        try:
            Session.get_active_session().sql(
                "DROP VIEW IF EXISTS " + ".".join(snowflake_view_name)
            ).collect()
        except SnowparkSQLException as e:
            # Spark allows for both table and temporary view to exist with the same name.
            # Snowflake throws exception if we try to drop the view with doesn't exist but a table with the same name exists.
            if (
                "SQL compilation error: Object found is of type 'TABLE', not specified type 'VIEW'"
                not in str(e)
            ):
                raise

    register_temp_view(view_name, input_df_container, replace)


def create_snowflake_temporary_view(
    input_df: DataFrame,
    snowflake_view_name: list[str],
    stored_view_name: str,
    replace: bool,
    comment: Optional[str] = None,
) -> None:
    assert_snowflake_view_does_not_exist_in_cache(stored_view_name, replace)
    if replace:
        unregister_temp_view(stored_view_name)
        input_df.create_or_replace_temp_view(snowflake_view_name, comment=comment)
    else:
        input_df.create_temp_view(snowflake_view_name, comment=comment)
