from typing import Any
from typing import Optional

import pypika
from pypika import queries
from pypika import terms
from pypika import utils

from tecton_core.query import sql_compat


# Custom functions used in Snowflake queries
ArraySlice = pypika.CustomFunction("ARRAY_SLICE", ["array", "from", "to"])
ArraySize = pypika.CustomFunction("ARRAY_SIZE", ["array"])
ArrayAgg = pypika.CustomFunction("ARRAY_AGG", ["value"])
ZeroIfNull = pypika.CustomFunction("ZEROIFNULL", ["value"])


def ArrayAggWithinGroup(col, key):
    return sql_compat.CustomQuery(f"ARRAYAGG({col}) WITHIN GROUP (ORDER BY {key})")


class SnowflakeQuery(queries.Query):
    @classmethod
    def _builder(cls, **kwargs: Any) -> "SnowflakeQuery":
        return SnowflakeQueryBuilder(**kwargs)


class SnowflakeQueryBuilder(sql_compat.CaseInsensitiveSnowflakeQueryBuilder):
    """
    Subclass of pypika SnowflakeQueryBuilder to implement Snowflake specific syntax
    """

    def __init__(self, **kwargs: Any):
        super().__init__(**kwargs)
        self._lateral = None

    @utils.builder
    def lateral(self, criterion: terms.Criterion) -> "queries.QueryBuilder":
        self._lateral = criterion

    def _lateral_sql(self, quote_char: Optional[str] = None, **kwargs: Any) -> str:
        """
        https://docs.snowflake.com/en/sql-reference/constructs/join-lateral
        In a FROM clause, the LATERAL keyword allows an inline view to reference columns from a table expression that precedes that inline view.

        Syntax:
        SELECT ...
        FROM <left_hand_table_expression>, LATERAL ( <inline_view> )
        ...
        """
        return " ,LATERAL {lateral}".format(
            lateral=self._lateral.get_sql(quote_char=quote_char, subquery=True, **kwargs)
        )

    def get_sql(self, with_alias: bool = False, subquery: bool = False, **kwargs: Any) -> str:
        """
        This is a full copy of the get_sql method from pypika.queries.QueryBuilder except adding _lateral to the querystring
        pypika 0.48.9
        https://github.com/kayak/pypika/blob/master/pypika/queries.py#L1218
        """
        self._set_kwargs_defaults(kwargs)
        if not (self._selects or self._insert_table or self._delete_from or self._update_table):
            return ""
        if self._insert_table and not (self._selects or self._values):
            return ""
        if self._update_table and not self._updates:
            return ""

        has_joins = bool(self._joins)
        has_multiple_from_clauses = 1 < len(self._from)
        has_subquery_from_clause = 0 < len(self._from) and isinstance(self._from[0], queries.QueryBuilder)
        has_reference_to_foreign_table = self._foreign_table
        has_update_from = self._update_table and self._from

        kwargs["with_namespace"] = any(
            [
                has_joins,
                has_multiple_from_clauses,
                has_subquery_from_clause,
                has_reference_to_foreign_table,
                has_update_from,
            ]
        )

        if self._update_table:
            if self._with:
                querystring = self._with_sql(**kwargs)
            else:
                querystring = ""

            querystring += self._update_sql(**kwargs)

            if self._joins:
                querystring += " " + " ".join(join.get_sql(**kwargs) for join in self._joins)

            querystring += self._set_sql(**kwargs)

            if self._from:
                querystring += self._from_sql(**kwargs)

            if self._wheres:
                querystring += self._where_sql(**kwargs)

            if self._limit is not None:
                querystring += self._limit_sql()

            return querystring

        if self._delete_from:
            querystring = self._delete_sql(**kwargs)

        elif not self._select_into and self._insert_table:
            if self._with:
                querystring = self._with_sql(**kwargs)
            else:
                querystring = ""

            if self._replace:
                querystring += self._replace_sql(**kwargs)
            else:
                querystring += self._insert_sql(**kwargs)

            if self._columns:
                querystring += self._columns_sql(**kwargs)

            if self._values:
                querystring += self._values_sql(**kwargs)
                return querystring
            else:
                querystring += " " + self._select_sql(**kwargs)

        else:
            if self._with:
                querystring = self._with_sql(**kwargs)
            else:
                querystring = ""

            querystring += self._select_sql(**kwargs)

            if self._insert_table:
                querystring += self._into_sql(**kwargs)

        if self._from:
            querystring += self._from_sql(**kwargs)

        if self._using:
            querystring += self._using_sql(**kwargs)

        if self._force_indexes:
            querystring += self._force_index_sql(**kwargs)

        if self._use_indexes:
            querystring += self._use_index_sql(**kwargs)

        if self._joins:
            querystring += " " + " ".join(join.get_sql(**kwargs) for join in self._joins)

        if self._prewheres:
            querystring += self._prewhere_sql(**kwargs)

        if self._lateral:
            querystring += self._lateral_sql(**kwargs)

        if self._wheres:
            querystring += self._where_sql(**kwargs)

        if self._groupbys:
            querystring += self._group_sql(**kwargs)
            if self._mysql_rollup:
                querystring += self._rollup_sql()

        if self._havings:
            querystring += self._having_sql(**kwargs)

        if self._orderbys:
            querystring += self._orderby_sql(**kwargs)

        querystring = self._apply_pagination(querystring)

        if self._for_update:
            querystring += self._for_update_sql(**kwargs)

        if subquery:
            querystring = "({query})".format(query=querystring)

        if with_alias:
            kwargs["alias_quote_char"] = (
                self.ALIAS_QUOTE_CHAR if self.QUERY_ALIAS_QUOTE_CHAR is None else self.QUERY_ALIAS_QUOTE_CHAR
            )
            return utils.format_alias_sql(querystring, self.alias, **kwargs)

        return querystring
