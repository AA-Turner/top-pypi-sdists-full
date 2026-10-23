#
# Copyright (c) 2012-2025 Snowflake Computing Inc. All rights reserved.
#

from functools import cached_property

from snowflake import snowpark
from snowflake.snowpark import Column, DataFrame
from snowflake.snowpark._internal.analyzer.expression import (
    Attribute,
    Literal,
    UnresolvedAttribute,
)
from snowflake.snowpark.exceptions import SnowparkClientException
from snowflake.snowpark.functions import col
from snowflake.snowpark.types import LongType, StructField, StructType
from snowflake.snowpark_connect.config import global_config
from snowflake.snowpark_connect.typed_column import FieldType
from snowflake.snowpark_connect.utils.context import (
    get_df_before_projection,
    get_outer_dataframes,
)
from snowflake.snowpark_connect.utils.session import get_or_create_snowpark_session


class ExpressionTyper:
    # Window inputs computed in a select under the projection, or None when the
    # caller does not add that select.
    _window_inputs: list[Column] | None = None

    def __init__(self, df: DataFrame, *, lift_window_inputs: bool = False) -> None:
        self.df = df
        if lift_window_inputs:
            self._window_inputs = []

    @property
    def lifts_window_inputs(self) -> bool:
        """True when this typer's caller adds the select for lifted inputs."""
        return self._window_inputs is not None

    def lift_window_input(self, column: Column) -> Column | None:
        """Compute ``column`` in a select under the projection; return a reference.

        Snowflake does not nest window functions, so a window over another
        window's result reads it from that select. Returns None when this
        typer's caller does not add the select.
        """
        if self._window_inputs is None:
            return None
        # Unique within one projection, which selects only its own outputs. A
        # fixed name keeps the SQL text stable for the describe and result caches.
        name = f'"__SAS_WINDOW_INPUT_{len(self._window_inputs)}"'
        self._window_inputs.append(column.alias(name))
        return col(name)

    def with_window_inputs(self, df: DataFrame) -> DataFrame:
        """``df`` with the lifted window inputs added in a select of their own."""
        if not self._window_inputs:
            return df
        lifted = df.select("*", *self._window_inputs)
        if getattr(lifted, "_select_statement", None) is not None:
            lifted._select_statement.flatten_disabled = True
        return lifted

    def type(self, column: Column) -> list[FieldType]:
        types = self._try_to_type_attribute_or_literal(self.df, column)
        if not types and get_df_before_projection():
            types = self._try_to_type_attribute_or_literal(
                get_df_before_projection().dataframe, column
            )
        if not types:
            # df.select().schema results in DESCRIBE call to Snowflake, so avoid it if possible
            types = self._type_using_select(self._df_for(column), column)
        return types

    def _df_for(self, column: Column) -> DataFrame:
        """The input, with the lifted window inputs only if ``column`` reads one."""
        if not self._window_inputs:
            return self.df
        names = column._expression.dependent_column_names()
        lifted = {lifted._expression.name for lifted in self._window_inputs}
        if names is not None and not names & lifted:
            return self.df
        return self.with_window_inputs(self.df)

    def _type_using_select(self, df: DataFrame, column: Column) -> list[FieldType]:
        df = self._join_df_with_outer_dataframes(df)

        try:
            return self._get_df_field_types(df, column)
        except SnowparkClientException:  # Fallback to the df before projection
            df_container = get_df_before_projection()
            if df_container is None:
                raise

            df = self._join_df_with_outer_dataframes(df_container.dataframe)
            return self._get_df_field_types(df, column)

    @staticmethod
    def _join_df_with_outer_dataframes(df: DataFrame) -> DataFrame:
        """Widen ``df`` with the outer scopes so a correlated reference can be typed.

        An outer DataFrame that is already part of ``df`` is skipped. Row-level
        DML publishes its target container under the statement's plan_id and
        types the predicate against that same container, so for
        ``DELETE FROM t WHERE EXISTS (SELECT 1 FROM s WHERE t.id = s.id)`` the
        target turns up as both the base and the only outer DataFrame. Snowpark
        rejects ``df.join(df)`` outright (SnowparkJoinException 1103, "cannot
        join a DataFrame with itself"), and the join would contribute no columns
        anyway -- they are already in ``df``.
        """
        joined_ids = {id(df)}
        for outer_df_container in get_outer_dataframes():
            outer_df = outer_df_container.dataframe
            if id(outer_df) in joined_ids:
                continue
            joined_ids.add(id(outer_df))
            df = df.join(outer_df)

        return df

    @staticmethod
    def _get_df_field_types(df: DataFrame, column: Column) -> list[FieldType]:
        return [
            FieldType(f.datatype, f.nullable) for f in df.select(column).schema.fields
        ]

    def _try_to_type_attribute_or_literal(
        self, df: DataFrame, column: Column
    ) -> list[FieldType] | None:
        types = None
        expr = column._expression if hasattr(column, "_expression") else None
        match expr:
            case UnresolvedAttribute() | Attribute():
                # there is a chance that df.schema is already evaluated
                types = [
                    FieldType(f.datatype, f.nullable)
                    for f in df.schema.fields
                    if (
                        f.name == expr.name
                        or (
                            (not global_config.spark_sql_caseSensitive)
                            and f.name.lower() == expr.name.lower()
                        )
                    )
                ]  # doesn't work for nested attributes e.g. `"properties-3":"salary"`
            case Literal():
                types = [FieldType(expr.datatype, nullable=expr.nullable)]
        return types

    @staticmethod
    def dummy_typer(session: snowpark.Session = None):
        """
        Get a dummy typer, which can be used to get expression types. Since typer requires a dataframe,
        the dummy typer is mainly used when there is no existing handy dataframe.

        Example:
            (_, typed_column) = map_single_column_expression(
                    expression, column_map, ExpressionTyper.dummy_typer(session)
                )
        """
        if session is None:
            session = get_or_create_snowpark_session()
        empty_df = session.create_dataframe(
            [], schema=StructType([StructField("id", LongType(), True)])
        )
        typer = ExpressionTyper(empty_df)
        return typer


class JoinExpressionTyper(ExpressionTyper):
    def __init__(self, left: DataFrame, right: DataFrame) -> None:
        self.left = left
        self.right = right

    def type(self, column: Column) -> list[FieldType]:
        types = self._try_to_type_attribute_or_literal(self.left, column)
        if not types:
            types = self._try_to_type_attribute_or_literal(self.right, column)
        if not types:
            types = self._type_using_select(self.df, column)
        return types

    @cached_property
    def df(self) -> DataFrame:
        return self.left.join(
            self.right,
            lsuffix="_left",
            rsuffix="_right",
        )


class LambdaExpressionTyper(ExpressionTyper):
    """Typer for lambda bodies that falls back to the outer scope typer for columns
    not found in the lambda's artificial DataFrame (i.e., outer column references)."""

    def __init__(self, artificial_df: DataFrame, outer_typer: ExpressionTyper) -> None:
        super().__init__(artificial_df)
        self._outer_typer = outer_typer

    def type(self, column: Column) -> list[FieldType]:
        types = self._try_to_type_attribute_or_literal(self.df, column)
        if types:
            return types
        expr = column._expression if hasattr(column, "_expression") else None
        if isinstance(expr, (UnresolvedAttribute, Attribute)):
            return self._outer_typer.type(column)
        try:
            return self._type_using_select(self.df, column)
        except Exception:
            return self._outer_typer.type(column)
