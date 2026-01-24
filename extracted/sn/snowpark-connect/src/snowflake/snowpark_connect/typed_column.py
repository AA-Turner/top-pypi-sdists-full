#
# Copyright (c) 2012-2025 Snowflake Computing Inc. All rights reserved.
#

from collections.abc import Callable
from functools import cached_property

import snowflake.snowpark.functions as snowpark_fn
from snowflake import snowpark
from snowflake.snowpark.column import Column
from snowflake.snowpark_connect.column_qualifier import ColumnQualifier

_EMPTY_COLUMN = Column("")


class TypedColumn:
    def __init__(
        self,
        col: Column,
        type_resolver: Callable[[], list[snowpark.types.DataType] | None],
    ) -> None:
        self.col = col
        self._regex_matched_columns: list = list()
        self._type_resolver = type_resolver
        self._catalog_database_info: dict[str, str] = {}

    def __iter__(self):
        return iter((self.col, self._type_resolver))

    @property
    def typ(self) -> snowpark.types.DataType | None:
        assert (
            len(self.types) == 1
        ), f"Expected exactly single column expression, got {self.col} with types {self.types}"
        return self.types[0]

    @cached_property
    def types(self) -> list[snowpark.types.DataType] | None:
        return self._type_resolver()

    @classmethod
    def empty(cls):
        return TypedColumn(_EMPTY_COLUMN, lambda: None)

    def alias(self, alias_name: str):
        return TypedColumn(self.col.alias(alias_name), self._type_resolver)

    def set_qualifiers(self, qualifiers: set[ColumnQualifier]) -> None:
        self.qualifiers = qualifiers

    def get_qualifiers(self) -> set[ColumnQualifier]:
        return getattr(self, "qualifiers", set())

    def set_catalog_database_info(self, catalog_database_info: dict[str, str]) -> None:
        self._catalog_database_info = catalog_database_info

    def get_catalog_database_info(self) -> dict[str, str]:
        """Get catalog and database information for this column."""
        return self._catalog_database_info

    def get_catalog(self) -> str | None:
        return self._catalog_database_info.get("catalog")

    def get_database(self) -> str | None:
        return self._catalog_database_info.get("database")

    def set_multi_col_qualifiers(self, qualifiers: list[set[ColumnQualifier]]) -> None:
        self.multi_col_qualifiers = qualifiers

    def get_multi_col_qualifiers(self, num_columns) -> list[set[ColumnQualifier]]:
        if not hasattr(self, "multi_col_qualifiers"):

            return [set() for i in range(num_columns)]
        assert (
            len(self.multi_col_qualifiers) == num_columns
        ), f"Expected {num_columns} multi-column qualifiers, got {len(self.multi_col_qualifiers)}"
        return self.multi_col_qualifiers

    def is_empty(self) -> bool:
        return (
            isinstance(self.col, Column)
            and self.col._expression == _EMPTY_COLUMN._expression
        )

    def column(self, to_semi_structure: bool = False) -> Column:
        if to_semi_structure and len(self.types) <= 1:
            match self.typ:
                case snowpark.types.StructType() if self.typ.structured:
                    return snowpark_fn.cast(self.col, snowpark.types.StructType())
                case snowpark.types.MapType() if self.typ.structured:
                    # no more semi-structured map, use semi-structured struct instead
                    return snowpark_fn.cast(self.col, snowpark.types.StructType())
                case snowpark.types.ArrayType() if self.typ.structured:
                    return snowpark_fn.cast(self.col, snowpark.types.ArrayType())
        return self.col

    def over(self, window: snowpark.window.WindowSpec) -> Column:
        return self.col.over(window)


class TypedColumnWithDeferredCast(TypedColumn):
    def __init__(
        self,
        col: Column,
        type_resolver: Callable[[], list[snowpark.types.DataType] | None],
    ) -> None:
        super().__init__(col, type_resolver)

    def over(self, window: snowpark.window.WindowSpec) -> Column:
        return self.col.over(window).cast(self.typ)
