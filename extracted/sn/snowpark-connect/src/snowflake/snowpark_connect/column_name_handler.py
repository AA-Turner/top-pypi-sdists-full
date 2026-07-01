#
# Copyright (c) 2012-2025 Snowflake Computing Inc. All rights reserved.
#

from __future__ import annotations

import re
from collections import defaultdict, deque
from collections.abc import Callable
from dataclasses import dataclass
from functools import cached_property

from pyspark.errors.exceptions.base import AnalysisException

from snowflake.snowpark import DataFrame
from snowflake.snowpark._internal.analyzer.analyzer_utils import unquote_if_quoted
from snowflake.snowpark._internal.utils import quote_name
from snowflake.snowpark.types import StructType
from snowflake.snowpark_connect.column_qualifier import ColumnQualifier
from snowflake.snowpark_connect.config import global_config
from snowflake.snowpark_connect.error.error_codes import ErrorCodes
from snowflake.snowpark_connect.error.error_utils import attach_custom_error_code
from snowflake.snowpark_connect.type_support import emulate_integral_types
from snowflake.snowpark_connect.utils.context import (
    get_current_operation_scope,
    get_is_processing_order_by,
)
from snowflake.snowpark_connect.utils.identifiers import (
    split_fully_qualified_spark_name,
)
from snowflake.snowpark_connect.utils.sequence import next_unique_num

ALREADY_QUOTED = re.compile('^(".+")$', re.DOTALL)


def union_restorable_name(name: str) -> str:
    """
    Convert a spark column name to a normalized key for the columns_to_restore dict in unionByName.
    Handles column names containing double quotes by escaping and quoting them.
    SNOW-3340914
    """
    should_uppercase = not global_config.spark_sql_caseSensitive
    updated_name = quote_and_escape_double_quotes(name)
    return updated_name.upper() if should_uppercase else updated_name


def quote_and_escape_double_quotes(name: str) -> str:
    if ALREADY_QUOTED.match(name):
        return name
    escaped_name = name.replace('"', '""')
    return f'"{escaped_name}"'


def schema_getter(df: DataFrame) -> Callable[[], StructType]:
    schema_property = type(df).schema
    getter = schema_property.func
    return lambda: getter(df)


def set_schema_getter(df: DataFrame, get_schema: Callable[[], StructType]) -> None:
    class PatchedDataFrame(type(df)):
        @cached_property
        def schema(self):
            return emulate_integral_types(get_schema())

    df.__class__ = PatchedDataFrame

    # If schema was already cached before the class change, update it with emulate_integral_types
    if df.__dict__.get("schema"):
        df.__dict__["schema"] = emulate_integral_types(df.__dict__["schema"])


# TODO replace plan_id-offset with single unique value
def make_column_names_snowpark_compatible(
    names: list[str], plan_id: int, offset: int = 0
) -> list[str]:
    """
    Create Snowpark column names for the given Spark column names. We have several requirements for Snowpark names:
    - need to be unique even if Spark names have duplicates
    - need to be unique across different dataframes, to handle correlated subqueries correctly
    - should contain Spark names for debugging purposes
    To satisfy these, we append the plan ID and the column index to the Spark column name.

    For example: Spark columns [a, b, c] in plan ID 5 will be converted to ["a-00000005-0", "b-00000005-1", "c-00000005-2"].

    The offset argument is used to offset the column index. It should be set to non-zero when generating new column
    names for an existing dataframe to avoid potential naming conflict.

    For example: Suppose we have a dataframe `df` with plan_id=5 that contains column a and b.
        Now we need to append a few more columns to the dataframe, which is very common in unpivot and withColumn.
        `df.unpivot(['a', 'b'], None, 'a', 'b')` will result in this Spark dataframe:
        +---+---+---+---+
        |  a|  b|  a|  b|
        +---+---+---+---+
        ...
        +---+---+---+---+
        To avoid duplicated column names, the corresponding Snowpark dataframe should be:
        +-------------+-------------+-------------+-------------+
        | a-00000005-0| b-00000005-1| a-00000005-2| b-00000005-3|
        +-------------+-------------+-------------+-------------+
        ...
        +-------------+-------------+-------------+-------------+
        In this case the function call should be `make_column_names_snowpark_compatible(['a', 'b'], 5, 2)`,
        to avoid naming conflicts between the new columns and the old columns.
    """
    from snowflake.snowpark_connect.relation.read.metadata_utils import (
        METADATA_FILENAME_COLUMN,
    )

    return [
        # Skip METADATA$FILENAME - preserve original name without quoting
        name if name == METADATA_FILENAME_COLUMN else
        # Use `-` in the name to force df.column to return double-quoted names
        quote_name(f"{unquote_if_quoted(name)}-{plan_id:08x}-{i + offset}")
        for i, name in enumerate(names)
    ]


def make_unique_snowpark_name(spark_name: str) -> str:
    """
    Returns a snowpark column name that's guaranteed to be unique in this session,
    by appending "#<unique number>" to the given spark name.
    """
    return quote_name(f"{spark_name}-{next_unique_num():x}")


@dataclass(frozen=True)
class ColumnNames:
    spark_name: str
    snowpark_name: str
    qualifiers: set[ColumnQualifier]
    equivalent_snowpark_names: set[str] | None = ((None,),)
    catalog_info: str | None = None  # Catalog from fully qualified name
    database_info: str | None = None  # Database from fully qualified name
    is_internal: bool = (
        False  # Internal scaffolding columns (e.g. __DUMMY); never accessible to users
    )
    is_qualified_access_only: bool = False  # Only accessible via qualified reference (e.g. USING-join source-side columns)

    @property
    def is_hidden(self) -> bool:
        """True if this column is excluded from unqualified user-visible projections.

        Hidden columns are either internal scaffolding (`is_internal`) or only
        reachable via a qualified reference (`is_qualified_access_only`).
        """
        return self.is_internal or self.is_qualified_access_only

    @property
    def is_visible(self) -> bool:
        """Inverse of `is_hidden`; convenience for `not c.is_hidden`."""
        return not self.is_hidden

    def all_spark_names_including_qualified_names(self):
        all_names = [self.spark_name]
        for qualifier in self.qualifiers:
            all_names.extend(qualifier.all_qualified_names(self.spark_name))
        return all_names


class ColumnNameMap:
    def __init__(
        self,
        spark_column_names: list[str],
        snowpark_column_names: list[str],
        is_case_sensitive: Callable[
            [], bool
        ] = lambda: global_config.spark_sql_caseSensitive,
        column_metadata: dict | None = None,
        column_qualifiers: list[set[ColumnQualifier]] = None,
        parent_column_name_map: ColumnNameMap | None = None,
        equivalent_snowpark_names: list[set[str]] | None = None,
        column_is_internal: list[bool] | None = None,
        column_is_qualified_access_only: list[bool] | None = None,
    ) -> None:
        """
        spark_column_names: Original spark column names
        snowpark_column_names: Snowpark column names
        column_metadata: This field is used to store metadata related to columns. Since Snowpark's Struct type does not support metadata,
        we use this attribute to store any metadata related to the columns.
        The key is the original Spark column name, and the value is the metadata.
        example: Dict('age', {'foo': 'bar'})
        column_qualifiers: Optional qualifiers for the columns, used to handle table aliases or DataFrame aliases.
        parent_column_name_map: parent ColumnNameMap
        column_is_internal: Optional list of booleans indicating whether each column is internal scaffolding (never user-accessible)
        column_is_qualified_access_only: Optional list of booleans indicating whether each column is only accessible via a qualified reference
        """
        self.columns: list[ColumnNames] = []
        self.spark_to_col: defaultdict[str, list[ColumnNames]] = defaultdict(list)
        self.uppercase_spark_to_col = defaultdict(list)
        self.snowpark_to_col = defaultdict(list)
        self.is_case_sensitive = is_case_sensitive
        self.column_metadata = column_metadata

        # Rename chain dictionary to track column renaming history
        self.rename_chains: dict[str, str] = {}  # old_name -> new_name mapping
        self.current_columns: set[str] = set()  # current column names

        # Parent ColumnNameMap classes
        self._parent_column_name_map = parent_column_name_map

        assert len(spark_column_names) == (
            len(column_qualifiers) if column_qualifiers else len(snowpark_column_names)
        ), (
            "Number of Spark column names must match number of Snowpark column names and "
            "number of column qualifiers if provided."
        )

        for i in range(len(spark_column_names)):
            # Extract catalog/database info from fully qualified spark column names
            spark_name = spark_column_names[i]
            catalog_info = None
            database_info = None

            # Parse fully qualified names to extract catalog.database.table.column format
            name_parts = split_fully_qualified_spark_name(spark_name)
            if len(name_parts) >= 4:
                # Format: catalog.database.table.column[.field...]
                # Only extract if this looks like a valid SQL table reference
                # Catalog.database.column (3 parts) is invalid - missing table
                # Only catalog.database.table.column (4+ parts) is potentially valid
                catalog_info = name_parts[0]
                database_info = name_parts[1]

            c = ColumnNames(
                spark_name=spark_name,
                snowpark_name=snowpark_column_names[i],
                qualifiers=column_qualifiers[i]
                if column_qualifiers and column_qualifiers[i]
                else set(),
                equivalent_snowpark_names=equivalent_snowpark_names[i]
                if equivalent_snowpark_names and equivalent_snowpark_names[i]
                else set(),
                catalog_info=catalog_info,
                database_info=database_info,
                is_internal=column_is_internal[i] if column_is_internal else False,
                is_qualified_access_only=column_is_qualified_access_only[i]
                if column_is_qualified_access_only
                else False,
            )
            self.columns.append(c)

            for spark_name in c.all_spark_names_including_qualified_names():
                # the same spark name can map to multiple snowpark names
                self.spark_to_col[spark_name].append(c)
                self.uppercase_spark_to_col[spark_name.upper()].append(c)

            # the same snowpark name can map to multiple spark column
            # e.g. df.select(date_format('dt', 'yyy'), date_format('dt', 'yyyy')) ->
            # [
            #   to_char( TRY_CAST (to_char("dt-0") AS TIMESTAMP), 'YYYY'),
            #   to_char( TRY_CAST (to_char("dt-0") AS TIMESTAMP), 'YYYY'),
            # ]
            self.snowpark_to_col[c.snowpark_name].append(c)

            self.current_columns.add(c.spark_name)

        if not global_config.spark_sql_caseSensitive:
            # Store the current column names in lowercase for case-insensitive lookups
            self.current_columns = {col.lower() for col in self.current_columns}

    def get_parent_column_name_map(self) -> ColumnNameMap | None:
        return self._parent_column_name_map

    def get_current_column_name(self, historical_name: str) -> str:
        """
        Follow the rename chain to get the most current name for a column.

        Args:
            historical_name: A possibly historical column name

        Returns:
            The most current name for this column after following the rename chain
        """
        current = (
            historical_name
            if global_config.spark_sql_caseSensitive
            else historical_name.lower()
        )
        visited = set()  # Prevent infinite loops in case of circular references

        while current in self.rename_chains and current not in visited:
            visited.add(current)
            current = self.rename_chains[current]

        return current

    @staticmethod
    def _allows_historical_name_lookup(operation: str) -> bool:
        """
        Determines if an operation should use historical name resolution based on
        observed Spark behavior.

        Args:
            operation: The operation type (e.g., 'filter', 'select', 'join')
            expr_context: Optional context about the expression (e.g., 'function_arg')

        Returns:
            True if historical name lookup should be used
        """
        # Operations that can use historical name lookup
        # Add more operations to this as needed.
        ops_with_history_lookup_support = [
            "filter",  # filter(col("old_name") === lit("value"))
            "sort",  # sort(col("old_name"))
            "orderBy",  # orderBy(col("old_name"))
            "with_columns_renamed",  # .withColumnRenamed("name", "new_name")
        ]
        return operation in ops_with_history_lookup_support

    def resolve_column_name(self, column_name: str) -> str | None:
        """
        Resolve a column name based on operation context, applying historical
        name lookup when appropriate according to Spark's behavior.
        Returns:
            The resolved column name or original column name if column name is not found in the rename history.
        """
        column_name = (
            column_name
            if global_config.spark_sql_caseSensitive
            else column_name.lower()
        )
        if column_name in self.current_columns:
            return column_name

        operation = get_current_operation_scope()
        if self._allows_historical_name_lookup(operation):
            current_name = self.get_current_column_name(column_name)
            if current_name != column_name:
                if current_name in self.current_columns:
                    return current_name

        return column_name

    def get_snowpark_column_names_from_spark_column_names(
        self,
        spark_column_names: list[str],
        return_first: bool = False,
        original_snowpark_names: list[str] | None = None,
    ) -> list[str]:
        snowpark_column_names = self._get_snowpark_column_names_from_spark_column_names(
            spark_column_names, return_first, original_snowpark_names
        )
        if snowpark_column_names:
            return snowpark_column_names

        current_operation = get_current_operation_scope()

        # If Spark column name was not found in the current ColumnNameMap and current operation
        # allows it, perform a reverse DFS lookup
        if (
            self._allows_historical_name_lookup(current_operation)
            and self._parent_column_name_map is not None
        ):
            snowpark_column_names = self._parent_column_name_map.get_snowpark_column_names_from_spark_column_names(
                spark_column_names, return_first, original_snowpark_names
            )

        return snowpark_column_names

    def _get_snowpark_column_names_from_spark_column_names(
        self,
        spark_column_names: list[str],
        return_first: bool = False,
        original_snowpark_names: list[str] | None = None,
    ) -> list[str]:
        snowpark_column_names = []
        for i, name in enumerate(spark_column_names):
            if not global_config.spark_sql_caseSensitive:
                name = name.upper()
                mapping = self.uppercase_spark_to_col
            else:
                mapping = self.spark_to_col
            if name not in mapping:
                # column may still be prefixed with df alias, but we don't know that here
                continue

            columns = mapping[name]

            # make sure the column matches the original snowpark name, if given
            if original_snowpark_names:
                oname = original_snowpark_names[i]
                columns = [
                    c
                    for c in columns
                    if c.snowpark_name == oname or oname in c.equivalent_snowpark_names
                ]

            # Filter out columns according to visibility rules.
            # - is_internal columns are scaffolding (e.g. __DUMMY); never accessible.
            # - is_qualified_access_only columns are only accessible via a
            #   qualified reference (e.g., "b.id"); they must be filtered on
            #   unqualified lookups but allowed through on qualified lookups so
            #   the caller's qualifier-matching logic can check them.
            is_qualified_lookup = "." in name or original_snowpark_names
            if is_qualified_lookup:
                columns = [c for c in columns if not c.is_internal]
            else:
                columns = [c for c in columns if c.is_visible]

            if return_first:
                if columns:  # Only append if we have columns after filtering
                    snowpark_column_names.append(columns[0].snowpark_name)
            else:
                snowpark_column_names.extend([c.snowpark_name for c in columns])

        return snowpark_column_names

    def get_snowpark_column_name_from_spark_column_name(
        self,
        spark_column_name: str,
        *,
        allow_non_exists: bool = False,
        return_first: bool = False,
        original_snowpark_name: str | None = None,
    ) -> str | None:
        assert isinstance(spark_column_name, str)
        resolved_name = (
            self.resolve_column_name(spark_column_name)
            if self.rename_chains
            else spark_column_name
        )
        snowpark_names = self.get_snowpark_column_names_from_spark_column_names(
            [resolved_name],
            return_first,
            [original_snowpark_name] if original_snowpark_name else None,
        )

        snowpark_names_len = len(snowpark_names)
        if snowpark_names_len > 1:
            # Check if this is a case where we have identical expressions that can be safely resolved to the first one
            # This commonly happens with GROUP BY expressions that also appear in SELECT clauses
            if (
                get_is_processing_order_by()
                and self._can_resolve_ambiguous_identical_expressions(
                    resolved_name, snowpark_names
                )
            ):
                # All the ambiguous columns represent the same expression, so we can safely use the first one
                return snowpark_names[0]
            else:
                exception = AnalysisException(
                    f"Ambiguous spark column name {spark_column_name}, potential snowpark column names {snowpark_names}"
                )
                attach_custom_error_code(exception, ErrorCodes.AMBIGUOUS_COLUMN_NAME)
                raise exception
        elif snowpark_names_len == 0:
            if allow_non_exists:
                return None
            else:
                exception = AnalysisException(
                    f"Spark column name {spark_column_name} does not exist"
                )
                attach_custom_error_code(exception, ErrorCodes.COLUMN_NOT_FOUND)
                raise exception
        return snowpark_names[0]

    def _can_resolve_ambiguous_identical_expressions(
        self, spark_column_name: str, snowpark_names: list[str]
    ) -> bool:
        """
        Determine if ambiguous columns represent identical expressions that can be safely resolved to the first one.

        This handles the common case where the same expression (like a UDF call) appears multiple times
        in a SELECT clause within a GROUP BY query. Since they're the same expression operating on the
        same grouped data, they will have identical values, so we can safely resolve to any of them.

        Args:
            spark_column_name: The Spark column name that has multiple mappings, make sure resolve this reforehand
            snowpark_names: List of Snowpark column names that map to this Spark column name

        Returns:
            True if we can safely resolve to the first snowpark column, False otherwise
        """
        if spark_column_name not in self.spark_to_col:
            return False

        columns: list[ColumnNames] = self.spark_to_col[spark_column_name]

        # If we don't have multiple columns, there's no ambiguity to resolve
        if len(columns) <= 1:
            return False

        # Check if all the snowpark names correspond to columns that have identical underlying expressions
        # We'll compare the actual column objects to see if they represent the same computation
        first_column = columns[0]

        for column in columns[1:]:
            if first_column.qualifiers != column.qualifiers:
                return False

        # Additional safety check: ensure all snowpark names are actually in our mapping
        for snowpark_name in snowpark_names:
            if snowpark_name not in self.snowpark_to_col:
                return False

        # If we reach here, the columns appear to be identical expressions from the same context
        # This commonly happens in GROUP BY scenarios where the same expression appears in both
        # the grouping clause and the select clause
        return True

    def get_spark_column_names_from_snowpark_column_names(
        self,
        snowpark_column_names: list[str],
    ) -> list[str]:
        assert isinstance(snowpark_column_names, list)
        spark_column_names = []
        for n in snowpark_column_names:
            if n not in self.snowpark_to_col:
                continue

            spark_column_names.extend([c.spark_name for c in self.snowpark_to_col[n]])
        return spark_column_names

    def get_spark_column_name_from_snowpark_column_name(
        self,
        snowpark_column_name: str,
        allow_non_exists: bool = False,
    ) -> str | None:
        assert isinstance(snowpark_column_name, str)

        spark_names = self.get_spark_column_names_from_snowpark_column_names(
            [snowpark_column_name]
        )
        spark_names_len = len(spark_names)
        if spark_names_len > 1:
            exception = AnalysisException(
                f"Ambiguous snowpark column name {snowpark_column_name}, potential spark column names {spark_names}"
            )
            attach_custom_error_code(exception, ErrorCodes.AMBIGUOUS_COLUMN_NAME)
            raise exception
        elif spark_names_len == 0:
            if allow_non_exists:
                return None
            else:
                exception = AnalysisException(
                    f"Snowpark column name {snowpark_column_name} does not exist"
                )
                attach_custom_error_code(exception, ErrorCodes.COLUMN_NOT_FOUND)
                raise exception
        return spark_names[0]

    def get_spark_column_name(self, idx: int) -> str:
        return self.columns[idx].spark_name

    def get_spark_columns(self) -> list[str]:
        return [c.spark_name for c in self.columns if c.is_visible]

    def column_matches_qualifier(
        self, col: ColumnNames, target_qualifier: ColumnQualifier
    ) -> bool:
        """
        Returns True if `col` has a qualifier matching `target_qualifier`, honoring
        the map's case-sensitivity setting.
        """
        case_sensitive = self.is_case_sensitive()
        normalized_target = (
            target_qualifier if case_sensitive else target_qualifier.to_upper()
        )
        column_qualifiers: set[ColumnQualifier] = (
            col.qualifiers if case_sensitive else {q.to_upper() for q in col.qualifiers}
        )
        return any(q.matches(normalized_target) for q in column_qualifiers)

    def get_spark_and_snowpark_columns_with_qualifier_for_qualifier(
        self, target_qualifier: ColumnQualifier
    ) -> tuple[list[str], list[str], list[set[ColumnQualifier]]]:
        """
        Returns the Spark and Snowpark column names along with their qualifiers for the specified qualifier.
        """
        spark_columns: list[str] = []
        snowpark_columns: list[str] = []
        qualifiers: list[set[ColumnQualifier]] = []

        for column in self.columns:
            if self.column_matches_qualifier(column, target_qualifier):
                spark_columns.append(column.spark_name)
                snowpark_columns.append(column.snowpark_name)
                qualifiers.append(column.qualifiers)

        return spark_columns, snowpark_columns, qualifiers

    def get_snowpark_columns(self, with_hidden: bool = False) -> list[str]:
        if with_hidden:
            return [c.snowpark_name for c in self.columns]
        return [c.snowpark_name for c in self.columns if c.is_visible]

    def get_snowpark_columns_after_drop(
        self, cols_to_drop: list[str]
    ) -> list[ColumnNames]:
        return [
            c
            for c in self.columns
            if self._quote_if_unquoted(c.snowpark_name) not in cols_to_drop
        ]

    def get_qualifiers(self) -> list[set[ColumnQualifier]]:
        """
        Returns the qualifiers for the columns.
        """
        return [c.qualifiers for c in self.columns if c.is_visible]

    def get_qualifiers_for_columns_after_drop(
        self, cols_to_drop: list[str]
    ) -> list[set[ColumnQualifier]]:
        """
        Returns the qualifiers for the columns after dropping the specified columns.
        """
        return [
            c.qualifiers
            for c in self.columns
            if self._quote_if_unquoted(c.snowpark_name) not in cols_to_drop
        ]

    def get_qualifiers_for_snowpark_column(
        self,
        snowpark_name: str,
    ) -> set[ColumnQualifier]:
        """
        Returns the qualifier for the specified snowpark column name.
        If the column does not exist, returns empty ColumnQualifier.
        """
        for c in self.columns:
            if c.snowpark_name == snowpark_name:
                return c.qualifiers

        return set()

    def get_equivalent_snowpark_names(self) -> list[set[str]]:
        return [c.equivalent_snowpark_names for c in self.columns]

    def get_equivalent_snowpark_names_for_snowpark_name(
        self, snowpark_name: str | None
    ) -> set[str]:
        """
        Helper method to get the set of old, equivalent snowpark names for the given column. Used to pass
        this information to child column maps.
        """
        if not snowpark_name:
            return set()

        name = self._quote_if_unquoted(snowpark_name)
        for c in self.columns:
            if name == c.snowpark_name:
                return c.equivalent_snowpark_names

        # no equivalent names found
        return set()

    @staticmethod
    def _quote_if_unquoted(s: str) -> str:
        if not ALREADY_QUOTED.match(s):
            s = s.replace('"', '\\"')
            return f'"{s}"'
        return s

    def has_spark_column(self, spark_column_name: str) -> bool:
        if self.is_case_sensitive():
            return spark_column_name in self.spark_to_col
        else:
            return spark_column_name.upper() in self.uppercase_spark_to_col

    def get_canonical_spark_name(self, spark_column_name: str) -> str:
        """Resolve a spark column name to the exact casing stored in this column map.

        When caseSensitive is false, the lookup is case-insensitive, so
        ``"yEAr"`` resolves to ``"year"`` if that is how the column was
        originally defined.  When caseSensitive is true, an exact match
        is required.

        Returns spark column name
        """
        if self.is_case_sensitive():
            mapping = self.spark_to_col
            key = spark_column_name
        else:
            mapping = self.uppercase_spark_to_col
            key = spark_column_name.upper()
        columns = mapping.get(key)
        if not columns:
            exception = AnalysisException(
                f"Spark column name `{spark_column_name}` does not exist. Session is in case sensitive mode: `{self.is_case_sensitive()}`"
            )
            attach_custom_error_code(exception, ErrorCodes.COLUMN_NOT_FOUND)
            raise exception

        if len(columns) > 1:
            snowpark_names = [c.snowpark_name for c in columns]
            exception = AnalysisException(
                f"Ambiguous snowpark column name `{spark_column_name}`, potential snowpark column names {snowpark_names}. Session is in case sensitive mode: `{self.is_case_sensitive()}`"
            )
            attach_custom_error_code(exception, ErrorCodes.AMBIGUOUS_COLUMN_NAME)
            raise exception
        return columns[0].spark_name

    def snowpark_to_spark_map(self) -> dict[str, str]:
        return {c.snowpark_name: c.spark_name for c in self.columns}

    def get_columns_matching_pattern(self, pattern: str) -> list[ColumnNames]:
        try:
            pattern_regex = re.compile(
                pattern, 0 if self.is_case_sensitive() else re.IGNORECASE
            )
            return [c for c in self.columns if pattern_regex.fullmatch(c.spark_name)]
        except re.error as e:
            exception = AnalysisException(f"Invalid regex pattern '{pattern}': {e}")
            attach_custom_error_code(exception, ErrorCodes.INVALID_FUNCTION_ARGUMENT)
            raise exception

    def with_columns(
        self, new_spark_columns: list[str], new_snowpark_columns: list[str]
    ) -> tuple[list[str], list[str], list[set[ColumnQualifier]], list[set[str]]]:
        """
        Returns an ordered list of spark and snowpark column names after adding the new columns through a withColumns call.
        All replaced columns retain their ordering in the dataframe. The new columns are added to the end of the list.
        """

        assert len(new_spark_columns) == len(new_snowpark_columns)

        spark_name_to_snowpark_name_map: dict[str, deque[int]] = {}

        for i, c in enumerate(new_spark_columns):
            column_name = self._normalized_spark_name(c)
            if column_name in spark_name_to_snowpark_name_map:
                spark_name_to_snowpark_name_map[column_name].append(i)
            else:
                spark_name_to_snowpark_name_map[column_name] = deque([i])

        spark_columns = []
        snowpark_columns = []
        removed_index: set[int] = set()
        qualifiers = []
        equivalent_snowpark_names = []

        for c in self.columns:
            column_name = self._normalized_spark_name(c.spark_name)
            if column_name in spark_name_to_snowpark_name_map:
                pending = spark_name_to_snowpark_name_map[column_name]
                if not pending:
                    # The visible occurrence of this column was already replaced by an
                    # earlier iteration.  This is a hidden duplicate introduced by a
                    # using-style join (e.g. left.join(right, on="id")), which tracks
                    # both the left- and right-hand copies of the join key internally.
                    # Drop the hidden duplicate so the replacement is not emitted twice.
                    continue
                index = pending.popleft()
                removed_index.add(index)
                spark_columns.append(new_spark_columns[index])
                snowpark_columns.append(new_snowpark_columns[index])
                qualifiers.append(set())
                equivalent_snowpark_names.append(set())
            else:
                spark_columns.append(c.spark_name)
                snowpark_columns.append(c.snowpark_name)
                qualifiers.append(c.qualifiers)
                equivalent_snowpark_names.append(c.equivalent_snowpark_names)

        for i, _ in enumerate(new_spark_columns):
            if i not in removed_index:
                spark_columns.append(new_spark_columns[i])
                snowpark_columns.append(new_snowpark_columns[i])
                qualifiers.append(set())
                equivalent_snowpark_names.append(set())

        return spark_columns, snowpark_columns, qualifiers, equivalent_snowpark_names

    def _normalized_spark_name(self, spark_name: str) -> str:
        if self.is_case_sensitive():
            return spark_name
        else:
            return spark_name.upper()

    def get_columns_after_join(
        self, right: ColumnNameMap, join_columns: list[str], join_type: str
    ) -> list[ColumnNames]:
        """
        Returns a list of columns (names and qualifiers) after a using_columns join with the given column map
        """

        # first, let's gather right-side join columns for qualifier lookup
        # and the remaining columns to append them to the result.
        # Mirror Spark's `commonNaturalJoinProcessing`: USING/NATURAL join keys
        # are looked up only among visible columns (Spark's `output`, which
        # excludes `metadataOutput`/QAO and internal scaffolding). Pre-existing
        # QAO/internal columns are propagated as-is via the remaining list.
        join_column_names = [self._normalized_spark_name(c) for c in join_columns]
        right_join_columns: dict[str, ColumnNames] = {}
        right_remaining_columns: list[ColumnNames] = []
        for oc in right.columns:
            if oc.is_hidden:
                right_remaining_columns.append(oc)
                continue
            col_name = self._normalized_spark_name(oc.spark_name)
            # only take the first matching column
            if col_name in join_column_names and col_name not in right_join_columns:
                right_join_columns[col_name] = oc
            else:
                right_remaining_columns.append(oc)

        # now gather left-side columns
        left_join_columns: dict[str, ColumnNames] = {}
        left_remaining_columns: list[ColumnNames] = []
        for c in self.columns:
            if c.is_hidden:
                left_remaining_columns.append(c)
                continue
            col_name = self._normalized_spark_name(c.spark_name)
            if col_name in join_column_names and col_name not in left_join_columns:
                equivalent_snowpark_names = set()
                # only assign join-side qualifier for outer joins
                match join_type:
                    case "left":
                        qualifiers = c.qualifiers
                    case "right":
                        qualifiers = right_join_columns[col_name].qualifiers
                    case _:
                        qualifiers = (
                            c.qualifiers | right_join_columns[col_name].qualifiers
                        )
                        equivalent_snowpark_names.update(
                            c.equivalent_snowpark_names,
                            right_join_columns[col_name].equivalent_snowpark_names,
                            {right_join_columns[col_name].snowpark_name},
                        )

                left_join_columns[col_name] = ColumnNames(
                    c.spark_name, c.snowpark_name, qualifiers, equivalent_snowpark_names
                )
            else:
                left_remaining_columns.append(c)

        # join columns go first in the user-given order,
        # then the remaining left-side columns, then remaining right-side columns
        match join_type:
            case "right":
                ordered_join_columns = [
                    right_join_columns[name] for name in join_column_names
                ]
            case _:
                ordered_join_columns = [
                    left_join_columns[name] for name in join_column_names
                ]
        return ordered_join_columns + left_remaining_columns + right_remaining_columns

    def get_conflicting_snowpark_columns(self, other: ColumnNameMap) -> set[str]:
        conflicting_columns = set()
        snowpark_names = {c.snowpark_name for c in self.columns}

        for c in other.columns:
            if c.snowpark_name in snowpark_names:
                conflicting_columns.add(c.snowpark_name)

        return conflicting_columns


class JoinColumnNameMap(ColumnNameMap):
    def __init__(
        self,
        left_colmap: ColumnNameMap,
        right_colmap: ColumnNameMap,
    ) -> None:
        self.left_column_mapping: ColumnNameMap = left_colmap
        self.right_column_mapping: ColumnNameMap = right_colmap

    def get_snowpark_column_name_from_spark_column_name(
        self,
        spark_column_name: str,
        *,
        allow_non_exists: bool = False,
        return_first: bool = False,
        original_snowpark_name: str | None = None,
    ) -> str | None:
        snowpark_column_name_in_left = (
            self.left_column_mapping.get_snowpark_column_name_from_spark_column_name(
                spark_column_name,
                allow_non_exists=True,
                original_snowpark_name=original_snowpark_name,
            )
        )
        snowpark_column_name_in_right = (
            self.right_column_mapping.get_snowpark_column_name_from_spark_column_name(
                spark_column_name,
                allow_non_exists=True,
                original_snowpark_name=original_snowpark_name,
            )
        )

        if (
            snowpark_column_name_in_left is None
            and snowpark_column_name_in_right is None
        ):
            if allow_non_exists:
                return None
            else:
                exception = AnalysisException(
                    f"Spark column name {spark_column_name} does not exist in either left or right DataFrame"
                )
                attach_custom_error_code(exception, ErrorCodes.COLUMN_NOT_FOUND)
                raise exception

        # special case for join conditions, if the column has a match on both sides, and exactly one of those
        # matches is the original snowpark name, that match should be used
        if (snowpark_column_name_in_right is not None) and (
            snowpark_column_name_in_left is not None
        ):
            if (
                snowpark_column_name_in_left == original_snowpark_name
                and snowpark_column_name_in_right != original_snowpark_name
            ):
                snowpark_column_name_in_right = None

            if (
                snowpark_column_name_in_right == original_snowpark_name
                and snowpark_column_name_in_left != original_snowpark_name
            ):
                snowpark_column_name_in_left = None

        if (snowpark_column_name_in_right is not None) and (
            snowpark_column_name_in_left is not None
        ):
            exception = AnalysisException(
                f"Ambiguous column name `{spark_column_name}` in join condition"
            )
            attach_custom_error_code(exception, ErrorCodes.AMBIGUOUS_COLUMN_NAME)
            raise exception

        snowpark_name = (
            snowpark_column_name_in_right
            if snowpark_column_name_in_left is None
            else snowpark_column_name_in_left
        )

        return snowpark_name

    def get_snowpark_column_names_from_spark_column_names(
        self,
        spark_column_names: list[str],
        return_first: bool = False,
        original_snowpark_names: list[str] | None = None,
    ) -> list[str]:
        exception = NotImplementedError("Method not implemented!")
        attach_custom_error_code(exception, ErrorCodes.INTERNAL_ERROR)
        raise exception

    def get_spark_column_names_from_snowpark_column_names(
        self,
        snowpark_column_names: list[str],
    ) -> list[str]:
        exception = NotImplementedError("Method not implemented!")
        attach_custom_error_code(exception, ErrorCodes.INTERNAL_ERROR)
        raise exception

    def get_spark_column_name_from_snowpark_column_name(
        self,
        snowpark_column_name: str,
        allow_non_exists: bool = False,
    ) -> str:
        exception = NotImplementedError("Method not implemented!")
        attach_custom_error_code(exception, ErrorCodes.INTERNAL_ERROR)
        raise exception

    def get_spark_columns(self) -> list[str]:
        exception = NotImplementedError("Method not implemented!")
        attach_custom_error_code(exception, ErrorCodes.INTERNAL_ERROR)
        raise exception

    def get_snowpark_columns(self) -> list[str]:
        exception = NotImplementedError("Method not implemented!")
        attach_custom_error_code(exception, ErrorCodes.INTERNAL_ERROR)
        raise exception

    def get_snowpark_columns_after_drop(
        self, cols_to_drop: list[str]
    ) -> list[ColumnNames]:
        exception = NotImplementedError("Method not implemented!")
        attach_custom_error_code(exception, ErrorCodes.INTERNAL_ERROR)
        raise exception

    def get_renamed_nested_column_name(self, name) -> str | None:
        exception = NotImplementedError("Method not implemented!")
        attach_custom_error_code(exception, ErrorCodes.INTERNAL_ERROR)
        raise exception

    def has_spark_column(self, spark_column_name: str) -> bool:
        exception = NotImplementedError("Method not implemented!")
        attach_custom_error_code(exception, ErrorCodes.INTERNAL_ERROR)
        raise exception

    def get_canonical_spark_name(self, spark_column_name: str) -> str | None:
        exception = NotImplementedError("Method not implemented!")
        attach_custom_error_code(exception, ErrorCodes.INTERNAL_ERROR)
        raise exception

    def snowpark_to_spark_map(self) -> dict[str, str]:
        exception = NotImplementedError("Method not implemented!")
        attach_custom_error_code(exception, ErrorCodes.INTERNAL_ERROR)
        raise exception

    def get_columns_matching_pattern(self, pattern: str) -> list[tuple[str, str]]:
        exception = NotImplementedError("Method not implemented!")
        attach_custom_error_code(exception, ErrorCodes.INTERNAL_ERROR)
        raise exception

    def with_columns(
        self, new_spark_columns: list[str], new_snowpark_columns: list[str]
    ) -> tuple[list[str], list[str], list[set[ColumnQualifier]]]:
        exception = NotImplementedError("Method not implemented!")
        attach_custom_error_code(exception, ErrorCodes.INTERNAL_ERROR)
        raise exception

    def get_qualifiers(self) -> list[set[ColumnQualifier]]:
        exception = NotImplementedError("Method not implemented!")
        attach_custom_error_code(exception, ErrorCodes.INTERNAL_ERROR)
        raise exception

    def get_qualifiers_for_columns_after_drop(
        self, cols_to_drop: list[str]
    ) -> list[set[ColumnQualifier]]:
        exception = NotImplementedError("Method not implemented!")
        attach_custom_error_code(exception, ErrorCodes.INTERNAL_ERROR)
        raise exception

    def get_spark_and_snowpark_columns_with_qualifier_for_qualifier(
        self, target_qualifier: list[str]
    ) -> tuple[list[str], list[str], list[set[ColumnQualifier]]]:
        exception = NotImplementedError("Method not implemented!")
        attach_custom_error_code(exception, ErrorCodes.INTERNAL_ERROR)
        raise exception

    def get_qualifiers_for_snowpark_column(
        self, snowpark_name: str
    ) -> set[ColumnQualifier]:
        qualifiers_left = self.left_column_mapping.get_qualifiers_for_snowpark_column(
            snowpark_name
        )
        qualifiers_right = self.right_column_mapping.get_qualifiers_for_snowpark_column(
            snowpark_name
        )

        if (len(qualifiers_left) > 0) and (len(qualifiers_right) > 0):
            exception = AnalysisException(f"Ambiguous column name {snowpark_name}")
            attach_custom_error_code(exception, ErrorCodes.AMBIGUOUS_COLUMN_NAME)
            raise exception

        return qualifiers_right if len(qualifiers_left) == 0 else qualifiers_left

    def get_columns_after_join(
        self, right: ColumnNameMap, join_columns: list[str], join_type: str
    ) -> list[ColumnNames]:
        exception = NotImplementedError("Method not implemented!")
        attach_custom_error_code(exception, ErrorCodes.INTERNAL_ERROR)
        raise exception

    def get_equivalent_snowpark_names_for_snowpark_name(self, snowpark_name: str):
        exception = NotImplementedError("Method not implemented!")
        attach_custom_error_code(exception, ErrorCodes.INTERNAL_ERROR)
        raise exception

    def get_equivalent_snowpark_names(self):
        exception = NotImplementedError("Method not implemented!")
        attach_custom_error_code(exception, ErrorCodes.INTERNAL_ERROR)
        raise exception
