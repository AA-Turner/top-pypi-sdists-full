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
from snowflake.snowpark.types import DataType, LongType, StructField, StructType
from snowflake.snowpark_connect.config import global_config
from snowflake.snowpark_connect.utils.context import (
    get_df_before_projection,
    get_outer_dataframes,
)
from snowflake.snowpark_connect.utils.session import get_or_create_snowpark_session


class ExpressionTyper:
    def __init__(self, df: DataFrame) -> None:
        self.df = df

    def type(self, column: Column) -> list[DataType]:
        types = self._try_to_type_attribute_or_literal(self.df, column)
        if not types and get_df_before_projection():
            types = self._try_to_type_attribute_or_literal(
                get_df_before_projection().dataframe, column
            )
        if not types:
            # df.select().schema results in DESCRIBE call to Snowflake, so avoid it if possible
            types = self._type_using_select(self.df, column)
        return types

    def _type_using_select(self, df: DataFrame, column: Column) -> list[DataType]:
        df = self._join_df_with_outer_dataframes(df)

        try:
            return self._get_df_datatypes(df, column)
        except SnowparkClientException:  # Fallback to the df before projection
            df_container = get_df_before_projection()
            if df_container is None:
                raise

            df = self._join_df_with_outer_dataframes(df_container.dataframe)
            return self._get_df_datatypes(df, column)

    @staticmethod
    def _join_df_with_outer_dataframes(df: DataFrame) -> DataFrame:
        for outer_df_container in get_outer_dataframes():
            df = df.join(outer_df_container.dataframe)

        return df

    @staticmethod
    def _get_df_datatypes(df: DataFrame, column: Column) -> list[DataType]:
        return [f.datatype for f in df.select(column).schema.fields]

    def _try_to_type_attribute_or_literal(
        self, df: DataFrame, column: Column
    ) -> list[DataType] | None:
        types = None
        expr = column._expression if hasattr(column, "_expression") else None
        match expr:
            case UnresolvedAttribute() | Attribute():
                # there is a chance that df.schema is already evaluated
                types = [
                    f.datatype
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
                types = [expr.datatype]
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

    def type(self, column: Column) -> list[DataType]:
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
