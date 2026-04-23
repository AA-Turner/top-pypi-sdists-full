#
# Copyright (c) 2012-2025 Snowflake Computing Inc. All rights reserved.
#

from __future__ import annotations

from dataclasses import dataclass
from typing import TYPE_CHECKING, Callable

import pyarrow as pa

from snowflake import snowpark
from snowflake.snowpark.types import (
    ArrayType,
    DataType,
    MapType,
    StructField,
    StructType,
)
from snowflake.snowpark_connect.column_qualifier import ColumnQualifier
from snowflake.snowpark_connect.typed_column import FieldType


# TODO: remove once snowpark version has the following fix: https://github.com/snowflakedb/snowpark-python/pull/4151 (version 1.49.0)
def _restore_map_value_contains_null(current: DataType, original: DataType) -> None:
    """Recursively restore MapType.value_contains_null lost by Snowpark's _as_nested()."""
    if isinstance(current, MapType) and isinstance(original, MapType):
        current.value_contains_null = original.value_contains_null
        _restore_map_value_contains_null(current.value_type, original.value_type)
    elif isinstance(current, ArrayType) and isinstance(original, ArrayType):
        _restore_map_value_contains_null(current.element_type, original.element_type)
    elif isinstance(current, StructType) and isinstance(original, StructType):
        for cur_field, orig_field in zip(current.fields, original.fields):
            _restore_map_value_contains_null(cur_field.datatype, orig_field.datatype)


if TYPE_CHECKING:
    import pyspark.sql.connect.proto.expressions_pb2 as expressions_proto

    from snowflake.snowpark_connect.column_name_handler import ColumnNameMap
    from snowflake.snowpark_connect.typed_column import TypedColumn


@dataclass
class AggregateMetadata:
    """
    Metadata about aggregation for resolving expressions in ORDER BY.

    When a Sort operation follows an Aggregate operation, ORDER BY expressions
    may reference:
    1. Grouping columns from the GROUP BY clause
    2. Aggregate result columns (aliases)
    3. Expressions on pre-aggregation columns (e.g., year(date) where date existed before GROUP BY)

    This metadata enables hybrid resolution similar to HAVING clause.
    """

    input_column_map: ColumnNameMap
    input_dataframe: snowpark.DataFrame
    grouping_expressions: list[expressions_proto.Expression]
    aggregate_expressions: list[expressions_proto.Expression]
    spark_columns: list[str]
    raw_aggregations: list[tuple[str, TypedColumn]]


class DataFrameContainer:
    """
    A container class that wraps a Snowpark DataFrame along with additional metadata.

    This class provides a unified interface for managing Snowpark DataFrames along with
    their column mappings, schema information, and metadata.
    """

    def __init__(
        self,
        dataframe: snowpark.DataFrame,
        column_map: ColumnNameMap | None = None,
        table_name: str | None = None,
        alias: str | None = None,
        cached_schema_getter: Callable[[], StructType] | None = None,
        partition_hint: int | None = None,
        dataframe_hint: str | None = None,
        can_be_cached: bool = True,
        can_be_materialized: bool = True,
        aggregate_metadata: AggregateMetadata | None = None,
        cached_local_relation_arrow_table: pa.Table | None = None,
    ) -> None:
        """
        Initialize a new DataFrameContainer.

        Args:
            dataframe: The underlying Snowpark DataFrame
            column_map: Optional column name mapping
            table_name: Optional table name for the DataFrame
            alias: Optional alias for the DataFrame
            cached_schema_getter: Optional function to get cached schema
            partition_hint: Optional partition count from repartition() operations
            dataframe_hint: Optional hint name (e.g. "directed") from DataFrame.hint()
            aggregate_metadata: Optional metadata about aggregation for ORDER BY resolution
            cached_local_relation_arrow_table: SNOW-3242008 — Performance optimization
                for the DDL sql_command round-trip case. When a DDL statement (USE DATABASE,
                ALTER SESSION SET, etc.) is executed via spark.sql(), the server returns
                a SqlCommandResult containing a LocalRelation with the result (e.g.,
                "Statement executed successfully."). The client then sends this LocalRelation
                back to the server for materialization. Without this cache, the server would
                create a Snowpark DataFrame and execute a VALUES query against Snowflake
                just to return this static string. By carrying the already-deserialized Arrow
                table from map_local_relation to map_execution_root, we skip the Snowflake
                round trip entirely and return the data directly from memory.
        """
        self._dataframe = dataframe
        self._column_map = self._create_default_column_map(column_map)
        self._table_name = table_name
        self._alias = alias
        self._partition_hint = partition_hint
        self._dataframe_hint = dataframe_hint
        self._can_be_cached = can_be_cached
        self._can_be_materialized = can_be_materialized
        self._aggregate_metadata = aggregate_metadata
        self._cached_local_relation_arrow_table = cached_local_relation_arrow_table
        self._known_row_count: int | None = None

        if cached_schema_getter is not None:
            self._apply_cached_schema_getter(cached_schema_getter)

    @classmethod
    def create_with_column_mapping(
        cls,
        dataframe: snowpark.DataFrame,
        spark_column_names: list[str],
        snowpark_column_names: list[str],
        snowpark_column_types: list | None = None,
        column_metadata: dict | None = None,
        column_qualifiers: list[set[ColumnQualifier]] | None = None,
        parent_column_name_map: ColumnNameMap | None = None,
        table_name: str | None = None,
        alias: str | None = None,
        cached_schema_getter: Callable[[], StructType] | None = None,
        partition_hint: int | None = None,
        equivalent_snowpark_names: list[set[str]] | None = None,
        column_is_hidden: list[bool] | None = None,
        can_be_cached: bool = True,
        aggregate_metadata: AggregateMetadata | None = None,
    ) -> DataFrameContainer:
        """
        Create a new container with complete column mapping configuration.

        Args:
            dataframe: The underlying Snowpark DataFrame
            spark_column_names: List of Spark column names
            snowpark_column_names: List of corresponding Snowpark column names
            snowpark_column_types: Optional list of column types
            column_metadata: Optional metadata dictionary
            column_qualifiers: Optional column qualifiers
            parent_column_name_map: Optional parent column name map
            table_name: Optional table name
            alias: Optional alias
            cached_schema_getter: Optional function to get cached schema
            partition_hint: Optional partition count from repartition() operations
            equivalent_snowpark_names: list of sets with old snowpark names that can be resolved with an existing column
            column_is_hidden: Optional list of booleans indicating whether each column is hidden
            can_be_cached: Optional boolean indicating if the dataframe can be cached
            aggregate_metadata: Optional metadata about aggregation for ORDER BY resolution

        Returns:
            A new DataFrameContainer instance

        Raises:
            AssertionError: If column names and types don't match expected lengths
        """
        # Validate inputs
        cls._validate_column_mapping_inputs(
            spark_column_names, snowpark_column_names, snowpark_column_types
        )

        column_map = cls._create_column_map(
            spark_column_names,
            snowpark_column_names,
            column_metadata,
            column_qualifiers,
            parent_column_name_map,
            equivalent_snowpark_names,
            column_is_hidden,
        )

        # Determine the schema getter to use
        final_schema_getter = None

        if cached_schema_getter is not None:
            # Use the provided schema getter
            final_schema_getter = cached_schema_getter
        elif snowpark_column_types is not None:
            # Create schema from types and wrap in function
            schema = cls._create_schema_from_types(
                snowpark_column_names, snowpark_column_types
            )
            if schema is not None:

                def get_schema():
                    return schema

                final_schema_getter = get_schema

        return cls(
            dataframe=dataframe,
            column_map=column_map,
            table_name=table_name,
            alias=alias,
            cached_schema_getter=final_schema_getter,
            partition_hint=partition_hint,
            can_be_cached=can_be_cached,
            aggregate_metadata=aggregate_metadata,
        )

    @property
    def can_be_cached(self) -> bool:
        """Indicate if the DataFrame can be cached in df_cache"""
        return self._can_be_cached

    @property
    def can_be_materialized(self) -> bool:
        """Indicate if the DataFrame can be materialized in df_cache"""
        return self._can_be_materialized

    def without_materialization(self):
        """Prevent the DataFrame from being materialized in df_cache"""
        self._can_be_materialized = False
        return self

    @property
    def cached_local_relation_arrow_table(self) -> pa.Table | None:
        """SNOW-3242008: Arrow table carried from map_local_relation for DDL result short-circuit."""
        return self._cached_local_relation_arrow_table

    @property
    def known_row_count(self) -> int | None:
        """SNOW-3242008: Pre-known row count to avoid a Snowflake count query."""
        return self._known_row_count

    @property
    def dataframe(self) -> snowpark.DataFrame:
        """Get the underlying Snowpark DataFrame."""
        # Ensure the DataFrame has the _column_map attribute for backward compatibility
        # Some of the snowpark code needs references to _column_map
        self._dataframe._column_map = self._column_map
        return self._dataframe

    @property
    def column_map(self) -> ColumnNameMap:
        """Get the column name mapping."""
        return self._column_map

    @column_map.setter
    def column_map(self, value: ColumnNameMap) -> None:
        """Set the column name mapping."""
        self._column_map = value

    @property
    def table_name(self) -> str | None:
        """Get the table name."""
        return self._table_name

    @table_name.setter
    def table_name(self, value: str | None) -> None:
        """Set the table name."""
        self._table_name = value

    @property
    def alias(self) -> str | None:
        """Get the alias name."""
        return self._alias

    @alias.setter
    def alias(self, value: str | None) -> None:
        """Set the alias name."""
        self._alias = value

    @property
    def partition_hint(self) -> int | None:
        """Get the partition hint count."""
        return self._partition_hint

    @partition_hint.setter
    def partition_hint(self, value: int | None) -> None:
        """Set the partition hint count."""
        self._partition_hint = value

    @property
    def dataframe_hint(self) -> str | None:
        """Get the uppercased hint name (e.g. 'DIRECTED')."""
        return self._dataframe_hint.upper() if self._dataframe_hint else None

    @dataframe_hint.setter
    def dataframe_hint(self, value: str | None) -> None:
        """Set the hint name."""
        self._dataframe_hint = value

    def _create_default_column_map(
        self, column_map: ColumnNameMap | None
    ) -> ColumnNameMap:
        """Create a default column map if none provided."""
        if column_map is not None:
            return column_map

        from snowflake.snowpark_connect.column_name_handler import ColumnNameMap

        return ColumnNameMap([], [])

    def _apply_cached_schema_getter(
        self,
        schema_getter: Callable[[], StructType],
    ) -> None:
        """Apply a cached schema getter to the dataframe."""
        from snowflake.snowpark_connect.column_name_handler import set_schema_getter

        set_schema_getter(self._dataframe, schema_getter)

    @staticmethod
    def _validate_column_mapping_inputs(
        spark_column_names: list[str],
        snowpark_column_names: list[str],
        snowpark_column_types: list | None = None,
    ) -> None:
        """
        Validate inputs for column mapping creation.

        Raises:
            AssertionError: If validation fails
        """
        assert len(snowpark_column_names) == len(
            spark_column_names
        ), "Number of Spark column names must match number of columns in DataFrame"

        if snowpark_column_types is not None:
            assert len(snowpark_column_names) == len(
                snowpark_column_types
            ), "Number of Snowpark column names and types must match"

    @staticmethod
    def _create_column_map(
        spark_column_names: list[str],
        snowpark_column_names: list[str],
        column_metadata: dict | None = None,
        column_qualifiers: list[set[ColumnQualifier]] | None = None,
        parent_column_name_map: ColumnNameMap | None = None,
        equivalent_snowpark_names: list[set[str]] | None = None,
        column_is_hidden: list[bool] | None = None,
    ) -> ColumnNameMap:
        """Create a ColumnNameMap with the provided configuration."""
        from snowflake.snowpark_connect.column_name_handler import ColumnNameMap

        return ColumnNameMap(
            spark_column_names,
            snowpark_column_names,
            column_metadata=column_metadata,
            column_qualifiers=column_qualifiers,
            parent_column_name_map=parent_column_name_map,
            equivalent_snowpark_names=equivalent_snowpark_names,
            column_is_hidden=column_is_hidden,
        )

    @staticmethod
    def _create_schema_from_types(
        snowpark_column_names: list[str],
        snowpark_column_types: list | None,
    ) -> StructType | None:
        """
        Create a StructType schema from column names and types.

        Accepts DataType or FieldType elements in snowpark_column_types.
        When a FieldType is provided, its nullable is preserved; plain DataType
        elements default to nullable=True (legacy behaviour).

        Returns:
            StructType if types are provided, None otherwise
        """
        if snowpark_column_types is None:
            return None

        original_datatypes = []
        fields = []
        for name, column_type in zip(snowpark_column_names, snowpark_column_types):
            if isinstance(column_type, FieldType):
                original_datatypes.append(column_type.datatype)
                fields.append(
                    StructField(
                        name,
                        column_type.datatype,
                        column_type.nullable,
                        _is_column=False,
                    )
                )
            else:
                original_datatypes.append(column_type)
                fields.append(StructField(name, column_type, _is_column=False))
        schema = StructType(fields)

        # Workaround: Snowpark's StructType.add() calls _as_nested() which
        # recreates MapType without preserving value_contains_null.
        # Recursively restore it from the original types.
        for field, orig_dt in zip(schema.fields, original_datatypes):
            _restore_map_value_contains_null(field.datatype, orig_dt)

        return schema

    def without_hidden_columns(self) -> DataFrameContainer:
        from snowflake.snowpark_connect.column_name_handler import ColumnNameMap

        if not any(c.is_hidden for c in self._column_map.columns):
            return self

        hidden_column_names = [
            c.snowpark_name for c in self._column_map.columns if c.is_hidden
        ]
        visible_columns = [c for c in self._column_map.columns if not c.is_hidden]

        filtered_df = self._dataframe.drop(hidden_column_names)
        filtered_column_map = ColumnNameMap(
            spark_column_names=[c.spark_name for c in visible_columns],
            snowpark_column_names=[c.snowpark_name for c in visible_columns],
            column_metadata=self._column_map.column_metadata,
            column_qualifiers=[c.qualifiers for c in visible_columns],
            parent_column_name_map=self._column_map._parent_column_name_map,
            equivalent_snowpark_names=[
                c.equivalent_snowpark_names for c in visible_columns
            ],
        )

        return DataFrameContainer(
            dataframe=filtered_df,
            column_map=filtered_column_map,
            table_name=self._table_name,
            alias=self._alias,
            cached_schema_getter=lambda: StructType(
                [
                    field
                    for field in self._dataframe.schema.fields
                    if field.name not in hidden_column_names
                ]
            ),
            partition_hint=self._partition_hint,
        )

    def has_zero_columns(self) -> bool:
        """
        Returns True if this is a 0-column dataframe. Since the underlying Snowpark dataframe must contain a
        dummy column, this needs to be checked whenever we need specific handling for 0-column dataframes,
        for example when showing or collecting the df.
        """
        return not any(not c.is_hidden for c in self._column_map.columns)
