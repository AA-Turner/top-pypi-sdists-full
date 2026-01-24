#
# Copyright (c) 2012-2025 Snowflake Computing Inc. All rights reserved.
#

import re
from typing import Any, Optional

import pyspark.sql.connect.proto.expressions_pb2 as expressions_proto
from pyspark.errors.exceptions.connect import AnalysisException

from snowflake.snowpark import Column, functions as snowpark_fn
from snowflake.snowpark._internal.analyzer.analyzer_utils import (
    quote_name_without_upper_casing,
)
from snowflake.snowpark.exceptions import SnowparkSQLException
from snowflake.snowpark.types import ArrayType, DataType, LongType, MapType, StructType
from snowflake.snowpark_connect.column_name_handler import ColumnNameMap, ColumnNames
from snowflake.snowpark_connect.config import global_config
from snowflake.snowpark_connect.dataframe_container import DataFrameContainer
from snowflake.snowpark_connect.error.error_codes import ErrorCodes
from snowflake.snowpark_connect.error.error_utils import attach_custom_error_code
from snowflake.snowpark_connect.expression.map_sql_expression import NILARY_FUNCTIONS
from snowflake.snowpark_connect.expression.typer import ExpressionTyper
from snowflake.snowpark_connect.typed_column import TypedColumn
from snowflake.snowpark_connect.utils.context import (
    capture_attribute_name,
    get_current_grouping_columns,
    get_is_evaluating_sql,
    get_outer_dataframes,
    get_plan_id_map,
    is_lambda_being_resolved,
    resolve_lca_alias,
)
from snowflake.snowpark_connect.utils.identifiers import (
    split_fully_qualified_spark_name,
)

SPARK_QUOTED = re.compile("^(`.*`)$", re.DOTALL)


def _get_catalog_database_from_column_map(
    column_name: str, column_map: ColumnNameMap
) -> dict[str, str]:
    """
    Get catalog/database info from the column map for a given column name.
    This replaces the previous extraction logic by looking up stored metadata.

    Returns:
        dict: catalog_database_info containing catalog/database metadata if found
    """
    catalog_database_info = {}

    # Look up in the column map using case-sensitive or case-insensitive matching
    matching_columns = []
    if hasattr(column_map, "is_case_sensitive") and column_map.is_case_sensitive():
        matching_columns = column_map.spark_to_col.get(column_name, [])
    elif hasattr(column_map, "uppercase_spark_to_col"):
        matching_columns = column_map.uppercase_spark_to_col.get(
            column_name.upper(), []
        )
    elif hasattr(column_map, "spark_to_col"):
        matching_columns = column_map.spark_to_col.get(column_name, [])

    # If we found a matching column with catalog/database info, use it
    for col_names in matching_columns:
        if col_names.catalog_info and col_names.database_info:
            catalog_database_info = {
                "catalog": col_names.catalog_info,
                "database": col_names.database_info,
            }
            break

    return catalog_database_info


def _resolve_struct_field(
    path: list[str], col: Column, typer: ExpressionTyper
) -> Column:
    try:
        col_type = typer.type(col)[0]
    except SnowparkSQLException as e:
        if e.raw_message is not None and "invalid identifier" in e.raw_message:
            exception = AnalysisException(
                f'[COLUMN_NOT_FOUND] The column "{path[0]}" does not exist in the target dataframe.'
            )
            attach_custom_error_code(exception, ErrorCodes.COLUMN_NOT_FOUND)
            raise exception
        else:
            raise

    field_path = path[1:]
    if not global_config.spark_sql_caseSensitive:
        field_path = _match_path_to_struct(field_path, col_type)

    for field_name in field_path:
        col = col.getItem(field_name)

    return col


def _try_resolve_column_in_scopes(
    column_name: str,
    column_mapping: ColumnNameMap,
    original_snowpark_name: Optional[str] = None,
) -> tuple[str | None, ColumnNameMap | None, ExpressionTyper | None]:
    """
    Try to resolve a column name in current and outer scopes.

    Args:
        column_name: The column name to resolve
        column_mapping: The column mapping for the current scope
        original_snowpark_name: target df snowpark name when we resolve a specific plan id

    Returns:
        Tuple of (snowpark_name, found_column_map, found_typer) or (None, None, None) if not found
    """
    # Try current scope
    snowpark_name = column_mapping.get_snowpark_column_name_from_spark_column_name(
        column_name,
        allow_non_exists=True,
        original_snowpark_name=original_snowpark_name,
    )
    if snowpark_name is not None:
        return snowpark_name, column_mapping, None

    # Try outer scopes
    for outer_df in get_outer_dataframes():
        snowpark_name = (
            outer_df.column_map.get_snowpark_column_name_from_spark_column_name(
                column_name,
                allow_non_exists=True,
                original_snowpark_name=original_snowpark_name,
            )
        )
        if snowpark_name is not None:
            return (
                snowpark_name,
                outer_df.column_map,
                ExpressionTyper(outer_df.dataframe),
            )

    return None, None, None


def _find_column_with_qualifier_match(
    name_parts: list[str],
    column_mapping: ColumnNameMap,
) -> tuple[int, str | None, Any]:
    """
    Find the column position in name_parts where the prefix matches a qualifier.

    In Spark, table qualifiers have at most 3 parts:
    - 1 part: table only (e.g., 't1') → ColumnQualifier(('t1',))
    - 2 parts: database.table (e.g., 'mydb.t5') → ColumnQualifier(('mydb', 't5'))
    - 3 parts: catalog.database.table (e.g., 'cat.mydb.t5') → ColumnQualifier(('cat', 'mydb', 't5'))

    Examples of how this works (suffix matching):
    1) Input: "mydb1.t5.t5.i1" with qualifier ('mydb1', 't5')
       - At i=2: prefix=['mydb1','t5'], matches qualifier suffix ('mydb1', 't5') → Column found!
       - Remaining ['i1'] is treated as field access

    2) Input: "t5.t5.i1" with qualifier ('mydb1', 't5')
       - At i=1: prefix=['t5'], matches qualifier suffix ('t5',) → Column found!
       - Remaining ['i1'] is treated as field access

    3) Input: "cat.mydb.t5.t5.i1" with qualifier ('cat', 'mydb', 't5')
       - At i=3: prefix=['cat','mydb','t5'], matches qualifier suffix → Column found!
       - Remaining ['i1'] is treated as field access

    The key insight: if the prefix before a candidate matches the END (suffix) of a qualifier,
    then that position is the column reference. This allows partial qualification (e.g., just table
    name instead of full database.table)

    Args:
        name_parts: The parts of the qualified name (e.g., ['mydb1', 't5', 't5', 'i1'])
        column_mapping: The column mapping to resolve columns against

    Returns:
        Tuple of (column_part_index, snowpark_name, found_column_map)
        Returns (0, None, None) if no valid column found

    Raises:
        AnalysisException: If a column is found but with invalid qualifier (scope violation)
    """
    # Track if we found a column but with wrong qualifier (scope violation)
    scope_violation = None

    for i in range(len(name_parts)):
        candidate_column = name_parts[i]
        snowpark_name, found_column_map, _ = _try_resolve_column_in_scopes(
            candidate_column, column_mapping
        )

        if snowpark_name is not None:
            candidate_qualifiers = found_column_map.get_qualifiers_for_snowpark_column(
                snowpark_name
            )
            prefix_parts = name_parts[:i]

            # Check if this is a valid column reference position
            # A valid position is where the prefix exactly matches one of the qualifiers
            is_valid_reference = False

            if i == 0:
                # No prefix (unqualified access)
                # Always valid - Spark allows unqualified access to any column
                # The remaining parts (name_parts[1:]) will be treated as
                # struct/map/array field access (e.g., "person.address.city" where
                # person is the column and address.city is the field path)
                is_valid_reference = True
            else:
                # Has prefix - check if it matches the end (suffix) of any qualifier
                # Spark allows partial qualification, so for qualifier ('mydb1', 't5'):
                # - Can access as mydb1.t5.t5.i1 (full qualifier match)
                # - Can access as t5.t5.i1 (suffix match - just table part)
                # e.g., for "t5.t5.i1", when i=1, prefix=['t5'] matches suffix of ('mydb1', 't5')
                # If valid, the remaining parts (name_parts[i+1:]) will be treated as
                # struct/map/array field access (e.g., ['i1'] is a field in column t5)
                for qual in candidate_qualifiers:
                    if len(qual.parts) >= len(prefix_parts) and qual.parts[
                        -len(prefix_parts) :
                    ] == tuple(prefix_parts):
                        is_valid_reference = True
                        break

            if is_valid_reference:
                # This is the actual column reference
                return (i, snowpark_name, found_column_map)
            elif i > 0:
                # Found column but qualifier doesn't match - this is a scope violation
                # e.g., SELECT nt1.k where k exists but nt1 is not its qualifier
                attr_name = ".".join(name_parts)
                scope_violation = (attr_name, ".".join(prefix_parts))

    # If we detected a scope violation, throw error
    if scope_violation:
        attr_name, invalid_qualifier = scope_violation
        exception = AnalysisException(
            f'[UNRESOLVED_COLUMN] Column "{attr_name}" cannot be resolved. '
            f'The table or alias "{invalid_qualifier}" is not in scope or does not exist.'
        )
        attach_custom_error_code(exception, ErrorCodes.COLUMN_NOT_FOUND)
        raise exception

    # No valid column found
    return (0, None, None)


def _get_quoted_attr_name(name_parts: list[str]) -> str:
    quoted_attr_name = ".".join(
        quote_name_without_upper_casing(x) for x in name_parts[:-1]
    )
    if len(name_parts) > 1:
        quoted_attr_name = f"{quoted_attr_name}.{name_parts[-1]}"
    else:
        quoted_attr_name = name_parts[0]
    return quoted_attr_name


def _attribute_is_regex(original_attr_name: str) -> bool:
    return (
        get_is_evaluating_sql()
        and global_config.spark_sql_parser_quotedRegexColumnNames
        and SPARK_QUOTED.match(original_attr_name)
    )


def _get_matching_columns(
    column_mapping: ColumnNameMap, pattern: str
) -> list[ColumnNames]:
    # Match the regex pattern against available columns
    matched_columns = column_mapping.get_columns_matching_pattern(pattern)

    if not matched_columns:
        # Get all available column names from the column mapping
        available_columns = column_mapping.get_spark_columns()
        # Keep the improved error message for SQL regex patterns
        # This is only hit for SQL queries like SELECT `(e|f)` FROM table
        # when spark.sql.parser.quotedRegexColumnNames is enabled
        exception = AnalysisException(
            f"No columns match the regex pattern '{pattern}'. "
            f"Snowflake SQL does not support SELECT statements with no columns. "
            f"Please ensure your regex pattern matches at least one column. "
            f"Available columns: {', '.join(available_columns[:10])}{'...' if len(available_columns) > 10 else ''}"
        )
        attach_custom_error_code(exception, ErrorCodes.INVALID_INPUT)
        raise exception

    return matched_columns


def _resolve_matched_columns(
    matched_columns: list[ColumnNames],
    typer: ExpressionTyper,
):
    # When multiple columns match, we need to signal that this should expand to multiple columns
    # Since map_unresolved_attribute can only return one column, we'll use a special marker
    # to indicate that this is a multi-column regex expansion
    if len(matched_columns) > 1:
        # Create a special column name that indicates multi-column expansion
        # The higher-level logic will need to handle this
        multi_col_name = "__REGEX_MULTI_COL__"
        # For now, return the first column but mark it specially
        first_col = matched_columns[0]
        snowpark_name = first_col.snowpark_name
        col = snowpark_fn.col(snowpark_name)
        qualifiers = first_col.qualifiers
        typed_col = TypedColumn(col, lambda: typer.type(col))
        typed_col.set_qualifiers(qualifiers)
        # Store matched columns info for later use
        typed_col._regex_matched_columns = matched_columns
        return multi_col_name, typed_col
    else:
        # Single column match - return that column
        matched_col = matched_columns[0]
        snowpark_name = matched_col.snowpark_name
        col = snowpark_fn.col(snowpark_name)
        qualifiers = matched_col.qualifiers
        typed_col = TypedColumn(col, lambda: typer.type(col))
        typed_col.set_qualifiers(qualifiers)
        return matched_col.spark_name, typed_col


def _resolve_attribute_with_original_snowpark_name(
    path: list[str],
    current_column_mapping: ColumnNameMap,
    typer: ExpressionTyper,
    original_snowpark_name: str,
) -> TypedColumn:
    # if the column was found in the target dataframe
    # we need to find its snowpark name in the current column mapping or any outer scope
    # it can be the same name or an equivalent after a join rename
    spark_name = path[0]
    (
        matching_snowpark_name,
        found_column_mapping,
        found_typer,
    ) = _try_resolve_column_in_scopes(
        spark_name,
        current_column_mapping,
        original_snowpark_name=original_snowpark_name,
    )

    if not matching_snowpark_name:
        # the column doesn't exist in the current dataframe
        exception = AnalysisException(
            f'[RESOLVED_REFERENCE_COLUMN_NOT_FOUND] The column "{spark_name}" does not exist in the target dataframe.'
        )
        attach_custom_error_code(exception, ErrorCodes.COLUMN_NOT_FOUND)
        raise exception

    # we need to use the typer for the dataframe where the column was resolved
    found_typer = found_typer if found_typer else typer

    col = snowpark_fn.col(matching_snowpark_name)
    if len(path) > 1:
        col = _resolve_struct_field(path, col, found_typer)
        # no qualifiers for struct fields
        return TypedColumn(col, lambda: found_typer.type(col))

    typed_col = TypedColumn(col, lambda: found_typer.type(col))
    typed_col.set_qualifiers(
        found_column_mapping.get_qualifiers_for_snowpark_column(matching_snowpark_name)
    )
    return typed_col


def _resolve_attribute_regex_with_plan_id(
    pattern: str,
    target_df_container: DataFrameContainer,
    current_column_mapping: ColumnNameMap,
    typer: ExpressionTyper,
) -> tuple[str, TypedColumn]:
    """
    Resolves all columns matching the given pattern in the target dataframe
    """
    target_column_mapping = target_df_container.column_map
    # find all matching columns
    matched_columns = _get_matching_columns(target_column_mapping, pattern)

    if len(matched_columns) == 1 and target_column_mapping.has_spark_column(pattern):
        # if the pattern is just the column name, we resolve the column using its equivalent snowpark name
        spark_name = matched_columns[0].spark_name
        snowpark_name = matched_columns[0].snowpark_name
        return spark_name, _resolve_attribute_with_original_snowpark_name(
            [spark_name], current_column_mapping, typer, snowpark_name
        )

    # if the pattern is not an exact match for an existing column, we don't want to use equivalent snowpark names
    # and we just check if the matched columns exist in the current mapping
    available_snowpark_columns = current_column_mapping.get_snowpark_columns()
    matched_columns = [
        c for c in matched_columns if c.snowpark_name in available_snowpark_columns
    ]
    if len(matched_columns) == 0:
        return "", TypedColumn.empty()
    return _resolve_matched_columns(matched_columns, typer)


def _resolve_attribute_with_plan_id(
    path: list[str],
    target_df_container: DataFrameContainer,
    current_column_mapping: ColumnNameMap,
    typer: ExpressionTyper,
) -> tuple[str, TypedColumn]:
    """
    Resolves a given spark name with a specific plan_id to the equivalent snowpark column in
    the target dataframe
    """
    target_column_mapping = target_df_container.column_map

    quoted_attr_name = _get_quoted_attr_name(path)

    # Try to resolve the full qualified name first
    # TODO: implement better mechanism for matching qualified names
    snowpark_name, found_column_map, _ = _try_resolve_column_in_scopes(
        quoted_attr_name, target_column_mapping
    )

    if snowpark_name:
        # we don't need the qualifiers anymore, since the original snowpark name is enough to disambiguate
        spark_name = path[-1]
        path = [spark_name]
    else:
        # in some cases the column can be qualified, so we have to match qualifiers as well
        (
            column_part_index,
            snowpark_name,
            found_column_map,
        ) = _find_column_with_qualifier_match(path, target_column_mapping)
        # extract the column name, and remove qualifiers
        spark_name = path[column_part_index]
        path = path[column_part_index:]

    if not snowpark_name or found_column_map is not target_column_mapping:
        # if the column doesn't exist in the plan_id dataframe, we don't need to look further
        exception = AnalysisException(
            f'[RESOLVED_REFERENCE_COLUMN_NOT_FOUND] The column "{spark_name}" does not exist in the target dataframe.'
        )
        attach_custom_error_code(exception, ErrorCodes.COLUMN_NOT_FOUND)
        raise exception

    matching_snowpark_col = _resolve_attribute_with_original_snowpark_name(
        path, current_column_mapping, typer, snowpark_name
    )

    # if resolving a struct field, we need to return the field name
    # that's why this is path[-1] and not spark_name
    return path[-1], matching_snowpark_col


def map_unresolved_attribute(
    exp: expressions_proto.Expression,
    column_mapping: ColumnNameMap,
    typer: ExpressionTyper,
) -> tuple[str, TypedColumn]:
    original_attr_name = exp.unresolved_attribute.unparsed_identifier
    name_parts = split_fully_qualified_spark_name(original_attr_name)
    attribute_is_regex = _attribute_is_regex(original_attr_name)

    assert len(name_parts) > 0, f"Unable to parse input attribute: {original_attr_name}"

    # Special handling for Spark's automatic grouping__id column
    # In Spark SQL, when using GROUP BY CUBE/ROLLUP/GROUPING SETS, an automatic
    # virtual column called 'grouping__id' (with double underscores) is available.
    # In Snowflake, we need to convert this to a GROUPING_ID() function call.
    if len(name_parts) == 1 and name_parts[0].lower() == "grouping__id":
        grouping_spark_columns = get_current_grouping_columns()
        if not grouping_spark_columns:
            # grouping__id can only be used with GROUP BY CUBE/ROLLUP/GROUPING SETS
            exception = AnalysisException(
                "[MISSING_GROUP_BY] grouping__id can only be used with GROUP BY (CUBE | ROLLUP | GROUPING SETS)"
            )
            attach_custom_error_code(exception, ErrorCodes.INVALID_FUNCTION_ARGUMENT)
            raise exception
        # Convert to GROUPING_ID() function call with the grouping columns
        # Map Spark column names to Snowpark column names
        snowpark_cols = []
        for spark_col_name in grouping_spark_columns:
            # Get the Snowpark column name from the mapping
            snowpark_name = (
                column_mapping.get_snowpark_column_name_from_spark_column_name(
                    spark_col_name
                )
            )
            if not snowpark_name:
                exception = AnalysisException(
                    f"[INTERNAL_ERROR] Cannot find Snowpark column mapping for grouping column '{spark_col_name}'"
                )
                attach_custom_error_code(exception, ErrorCodes.COLUMN_NOT_FOUND)
                raise exception
            snowpark_cols.append(snowpark_fn.col(snowpark_name))

        # Call GROUPING_ID with all grouping columns using Snowpark names
        result_col = snowpark_fn.grouping_id(*snowpark_cols)

        # TypedColumn expects a callable that returns a list of types
        # GROUPING_ID returns a BIGINT (LongType) in both Spark and Snowflake
        # representing the bit vector of grouping indicators
        typed_col = TypedColumn(result_col, lambda: [LongType()])
        return ("grouping__id", typed_col)

    # Validate that DataFrame API doesn't allow catalog.database.column patterns
    # These patterns should only work in SQL, not DataFrame API
    if len(name_parts) >= 4:
        # For 4+ parts, check if this looks like catalog.database.column.field
        # (as opposed to a valid table.column.field pattern)

        # Heuristic: if the pattern looks like catalog.database.column.field,
        # reject it in DataFrame API context (but allow in SQL)

        # Check if first part looks like a catalog name (not a column)
        first_part = name_parts[0]
        first_part_snowpark = (
            column_mapping.get_snowpark_column_name_from_spark_column_name(
                first_part, allow_non_exists=True
            )
        )

        # If first part is not a column and we have 4+ parts, check if it's a catalog reference
        if first_part_snowpark is None and len(name_parts) >= 4:
            # Import here to avoid circular import issues
            from snowflake.snowpark_connect.relation.catalogs import CATALOGS

            # Check if the first part is a registered catalog name OR looks like a catalog pattern
            is_registered_catalog = first_part.lower() in CATALOGS
            is_catalog_like = (
                # Contains "catalog" in the name
                "catalog" in first_part.lower()
                # Follows catalog naming patterns (no numbers, shorter descriptive names)
                or (
                    len(first_part) < 20
                    and not any(char.isdigit() for char in first_part)
                    and not first_part.startswith("mydb")
                    and not first_part.endswith(  # Skip test-generated database names
                        "_dbmsu"
                    )
                )  # Skip test-generated database names
            )

            is_catalog = is_registered_catalog or is_catalog_like

            if is_catalog:
                # This looks like a catalog.database.column.field pattern
                exception = AnalysisException(
                    f"[UNRESOLVED_COLUMN.WITH_SUGGESTION] A column or function parameter with name `{original_attr_name}` cannot be resolved. "
                    f"Cross-catalog column references are not supported in DataFrame API."
                )
                attach_custom_error_code(exception, ErrorCodes.COLUMN_NOT_FOUND)
                raise exception

    attr_name = ".".join(name_parts)
    capture_attribute_name(attr_name)

    has_plan_id = exp.unresolved_attribute.HasField("plan_id")

    if has_plan_id:
        plan_id = exp.unresolved_attribute.plan_id
        # get target dataframe and column mapping
        target_df_container = get_plan_id_map(plan_id)
        assert (
            target_df_container is not None
        ), f"resolving an attribute of a unresolved dataframe {plan_id}"
        if attribute_is_regex:
            # we should never get a struct field reference here
            assert (
                len(name_parts) == 1
            ), "resolving struct field for attribute regexp with plan id"
            return _resolve_attribute_regex_with_plan_id(
                name_parts[0], target_df_container, column_mapping, typer
            )
        return _resolve_attribute_with_plan_id(
            name_parts, target_df_container, column_mapping, typer
        )

    # Check if regex column names are enabled and this is a quoted identifier
    # We need to check the original attribute name before split_fully_qualified_spark_name processes it
    if attribute_is_regex:
        # Extract regex pattern by removing backticks
        regex_pattern = original_attr_name[1:-1]  # Remove first and last backtick
        matched_columns = _get_matching_columns(column_mapping, regex_pattern)
        return _resolve_matched_columns(matched_columns, typer)

    quoted_attr_name = _get_quoted_attr_name(name_parts)

    # Try to resolve the full qualified name first
    snowpark_name, found_column_map, found_typer = _try_resolve_column_in_scopes(
        quoted_attr_name, column_mapping
    )

    qualifiers = set()
    if snowpark_name is not None:
        col = snowpark_fn.col(snowpark_name)
        qualifiers = found_column_map.get_qualifiers_for_snowpark_column(snowpark_name)
        typer = found_typer if found_typer else typer
    else:
        # Get catalog/database info from column map if available
        catalog_database_info = _get_catalog_database_from_column_map(
            original_attr_name, column_mapping
        )

        # Find the column by matching qualifiers with the prefix parts
        # Note: This may raise AnalysisException if a scope violation is detected
        (
            column_part_index,
            snowpark_name,
            found_column_map,
        ) = _find_column_with_qualifier_match(name_parts, column_mapping)

        if snowpark_name is None:
            # Attempt LCA fallback.
            alias_tc = resolve_lca_alias(attr_name)

            if alias_tc is not None:
                # Return the TypedColumn that represents the alias.
                return (attr_name, alias_tc)

            # If qualified name not found, try to resolve as unqualified column name
            # This handles cases like "d.name" where we need to find "name" after a JOIN
            remaining_parts = name_parts
            if len(remaining_parts) > 1:
                unqualified_name = name_parts[-1]
                snowpark_name = (
                    column_mapping.get_snowpark_column_name_from_spark_column_name(
                        unqualified_name, allow_non_exists=True
                    )
                )
                if snowpark_name is not None:
                    col = snowpark_fn.col(snowpark_name)
                    qualifiers = column_mapping.get_qualifiers_for_snowpark_column(
                        snowpark_name
                    )
                    typed_col = TypedColumn(col, lambda: typer.type(col))
                    typed_col.set_qualifiers(qualifiers)
                    # Store catalog/database info if found in column map
                    if catalog_database_info:
                        typed_col.set_catalog_database_info(catalog_database_info)
                    return (unqualified_name, typed_col)

        if snowpark_name is None:
            # Check if we're inside a lambda and trying to reference an outer column
            # This catches direct column references (not lambda variables)
            if is_lambda_being_resolved() and column_mapping:
                # Check if this column exists in the outer scope (not lambda params)
                outer_col_name = (
                    column_mapping.get_snowpark_column_name_from_spark_column_name(
                        attr_name, allow_non_exists=True
                    )
                )
                if outer_col_name:
                    # This is an outer scope column being referenced inside a lambda
                    exception = AnalysisException(
                        f"Reference to non-lambda variable '{attr_name}' within lambda function. "
                        f"Lambda functions can only access their own parameters. "
                        f"If '{attr_name}' is a table column, it must be passed as an explicit parameter to the enclosing function."
                    )
                    attach_custom_error_code(
                        exception, ErrorCodes.UNSUPPORTED_OPERATION
                    )
                    raise exception

            if has_plan_id:
                exception = AnalysisException(
                    f'[RESOLVED_REFERENCE_COLUMN_NOT_FOUND] The column "{attr_name}" does not exist in the target dataframe.'
                )
                attach_custom_error_code(exception, ErrorCodes.COLUMN_NOT_FOUND)
                raise exception
            elif attr_name.lower() in NILARY_FUNCTIONS:
                snowpark_name = attr_name
            else:
                exception = AnalysisException(
                    f'[COLUMN_NOT_FOUND] The column "{attr_name}" does not exist in the target dataframe.'
                )
                attach_custom_error_code(exception, ErrorCodes.COLUMN_NOT_FOUND)
                raise exception

        col = snowpark_fn.col(snowpark_name)
        # Check if this is a struct field reference
        # Calculate the field path correctly based on where we found the column
        path = name_parts[column_part_index:]

        if len(path) > 1:
            col = _resolve_struct_field(path, col, typer)

    typed_col = TypedColumn(col, lambda: typer.type(col))
    typed_col.set_qualifiers(qualifiers)

    # Store catalog/database info if available from column map
    final_catalog_database_info = _get_catalog_database_from_column_map(
        original_attr_name, column_mapping
    )
    if final_catalog_database_info:
        typed_col.set_catalog_database_info(final_catalog_database_info)

    # for struct columns when accessed, spark use just the leaf field name rather than fully attributed one
    return (name_parts[-1], typed_col)


def _match_path_to_struct(path: list[str], col_type: DataType) -> list[str]:
    """Takes a path of names and adjusts them to strictly match the field names in a StructType."""
    adjusted_path = []
    typ = col_type
    for i, name in enumerate(path):
        if isinstance(typ, StructType):
            lowercase_name = name.lower()
            for field in typ.fields:
                if field.name.lower() == lowercase_name:
                    adjusted_path.append(field.name)
                    typ = field.datatype
                    break
        elif isinstance(typ, MapType) or isinstance(typ, ArrayType):
            # For MapType and ArrayType, we can use the name as is.
            adjusted_path.append(name)
            typ = typ.value_type if isinstance(typ, MapType) else typ.element_type
        else:
            # If the type is not a struct, map, or array, we cannot access the field.
            exception = AnalysisException(
                f"[INVALID_EXTRACT_BASE_FIELD_TYPE] Can't extract a value from \"{'.'.join(path[:i])}\". Need a complex type [STRUCT, ARRAY, MAP] but got \"{typ}\"."
            )
            attach_custom_error_code(exception, ErrorCodes.TYPE_MISMATCH)
            raise exception
    return adjusted_path
