import logging
from functools import reduce
from operator import add
from typing import List, Optional, Union

import sqlparse
from sqlparse.sql import (
    Comparison,
    Function,
    Identifier,
    IdentifierList,
    Parenthesis,
    Statement,
    TokenList,
    Values,
    Where,
)

from collate_sqllineage.core.analyzer import LineageAnalyzer
from collate_sqllineage.core.holders import (
    StatementLineageHolder,
    SubQueryLineageHolder,
)
from collate_sqllineage.core.models import (
    AnalyzerContext,
    Column,
    Schema,
    SubQuery,
    Table,
)
from collate_sqllineage.core.parser import SourceHandlerMixin
from collate_sqllineage.core.parser.sqlparse.handlers.base import (
    CurrentTokenBaseHandler,
    NextTokenBaseHandler,
)
from collate_sqllineage.core.parser.sqlparse.holder_utils import (
    get_dataset_from_identifier,
)
from collate_sqllineage.core.parser.sqlparse.models import (
    SqlParseColumn,
    SqlParseSubQuery,
    SqlParseTable,
)
from collate_sqllineage.core.parser.sqlparse.utils import (
    get_subquery_parentheses,
    is_subquery,
    is_token_negligible,
)
from collate_sqllineage.utils.constant import NodeTag
from collate_sqllineage.utils.helpers import trim_comment

logger = logging.getLogger(__name__)


class SqlParseLineageAnalyzer(LineageAnalyzer):
    """SQL Statement Level Lineage Analyzer."""

    def analyze(self, sql: str) -> StatementLineageHolder:
        try:
            # get rid of comments, which cause inconsistencies in sqlparse output
            stmt = sqlparse.parse(trim_comment(sql))[0]
            self.parsed_result = stmt
            if (
                stmt.get_type() == "DELETE"
                or stmt.token_first(skip_cm=True).normalized == "TRUNCATE"
                or stmt.token_first(skip_cm=True).normalized.upper() == "REFRESH"
                or stmt.token_first(skip_cm=True).normalized == "CACHE"
                or stmt.token_first(skip_cm=True).normalized.upper() == "UNCACHE"
                or stmt.token_first(skip_cm=True).normalized == "SHOW"
            ):
                holder = StatementLineageHolder()
            elif stmt.get_type() == "DROP":
                holder = self._extract_from_ddl_drop(stmt)
            elif (
                stmt.get_type() == "ALTER"
                or stmt.token_first(skip_cm=True).normalized == "RENAME"
            ):
                holder = self._extract_from_ddl_alter(stmt)
            elif stmt.get_type() == "MERGE":
                holder = self._extract_from_dml_merge(stmt)
            elif stmt.get_type() == "UPDATE":
                holder = self._extract_from_dml_update(stmt)
            else:
                # DML parsing logic also applies to CREATE DDL
                holder = StatementLineageHolder.of(
                    self._extract_from_dml(stmt, AnalyzerContext())
                )
            return holder
        except RecursionError as e:
            logger.warning(f"RecursionError occurred: {e}. Using simplified handling.")
            # Return empty holder when recursion limit exceeded
            return StatementLineageHolder()

    @classmethod
    def _extract_from_ddl_drop(cls, stmt: Statement) -> StatementLineageHolder:
        holder = StatementLineageHolder()
        for table in {
            SqlParseTable.of(t) for t in stmt.tokens if isinstance(t, Identifier)
        }:
            holder.add_drop(table)
        return holder

    @classmethod
    def _extract_from_ddl_alter(cls, stmt: Statement) -> StatementLineageHolder:
        holder = StatementLineageHolder()
        tables = []
        for t in stmt.tokens:
            if isinstance(t, Identifier):
                tables.append(SqlParseTable.of(t))
            elif isinstance(t, IdentifierList):
                for identifier in t.get_identifiers():
                    tables.append(SqlParseTable.of(identifier))
        keywords = [t for t in stmt.tokens if t.is_keyword]
        if any(k.normalized == "RENAME" for k in keywords):
            if stmt.get_type() == "ALTER" and len(tables) == 2:
                holder.add_rename(tables[0], tables[1])
            elif (
                stmt.token_first(skip_cm=True).normalized == "RENAME"
                and len(tables) % 2 == 0
            ):
                for i in range(0, len(tables), 2):
                    holder.add_rename(tables[i], tables[i + 1])
        if any(k.normalized == "EXCHANGE" for k in keywords) and len(tables) == 2:
            holder.add_write(tables[0])
            holder.add_read(tables[1])
        return holder

    @classmethod
    def _extract_from_dml_update(cls, stmt: Statement) -> StatementLineageHolder:
        # Reuse the generic DML pass to collect source/target tables and their aliases,
        # then map each SET assignment onto its real source table, the same way the
        # SELECT column lineage is resolved. The SET clause is walked after the tables
        # are known because in `UPDATE ... SET ... FROM ...` the FROM comes last.
        holder = cls._extract_from_dml(stmt, AnalyzerContext())
        write_table = cls._get_update_target(holder)
        if write_table is not None:
            cls._resolve_aliased_update_target(holder)
            write_table = cls._get_update_target(holder) or write_table
            alias_mapping = SourceHandlerMixin.get_alias_mapping_from_table_group(
                sorted(holder.read, key=str), holder
            )
            SourceHandlerMixin.add_write_target_to_alias_mapping(
                alias_mapping, write_table, write_table.alias
            )
            resolvable = set(holder.read) | {write_table}
            for comparison in cls._get_update_set_comparisons(stmt):
                if not isinstance(comparison.left, Identifier):
                    continue
                target_column = Column(
                    comparison.left.get_real_name(),
                    source_columns=SqlParseColumn._extract_source_columns(
                        comparison.right
                    ),
                )
                target_column.parent = write_table
                for source_column in target_column.to_source_columns(alias_mapping):
                    # Only emit when the qualifier resolved to a dataset the
                    # statement references. sqlparse cannot tokenize a three part
                    # name with a space alias, so an unresolved qualifier would
                    # otherwise create a phantom default-schema table.
                    if source_column.parent in resolvable:
                        holder.add_column_lineage(source_column, target_column)
        return StatementLineageHolder.of(holder)

    @staticmethod
    def _get_update_target(holder) -> Optional[Table]:
        """
        Return the real table an UPDATE writes to.

        holder.write is a set that can also carry the SubQuery a `FROM (SELECT ...) s`
        clause writes into, so indexing it directly picks a different element per
        interpreter run. Keep only real tables and pick the first by name.

        :param holder: the holder built for the UPDATE statement
        :return: the write target, or None when the statement writes to no table
        """
        write_tables = sorted(
            (tbl for tbl in holder.write if isinstance(tbl, Table)), key=str
        )
        return write_tables[0] if write_tables else None

    @staticmethod
    def _resolve_aliased_update_target(holder) -> None:
        """
        `UPDATE alias SET ... FROM real_table alias ...` writes to a table declared
        in the FROM clause under an alias. Rewrite the write target to that real
        table and drop it from the sources so it is not also reported as a source.
        The target is matched only against an explicit alias, never a table's own
        name, so a self-join source is not misread as the target.
        """
        write_table = SqlParseLineageAnalyzer._get_update_target(holder)
        if write_table is not None and str(write_table.schema) == Schema.unknown:
            matched = next(
                (
                    tbl
                    for tbl in sorted(holder.read, key=str)
                    if isinstance(tbl, Table)
                    and tbl.alias != tbl.raw_name
                    and write_table.raw_name == tbl.alias
                ),
                None,
            )
            if matched is not None and matched != write_table:
                for alias in list(holder.graph.successors(matched)):
                    if not isinstance(alias, (Table, SubQuery)):
                        holder.graph.remove_node(alias)
                if write_table in holder.graph:
                    holder.graph.remove_node(write_table)
                holder.add_write(matched)
                holder.graph.nodes[matched][NodeTag.READ] = False

    @staticmethod
    def _get_update_set_comparisons(stmt: Statement) -> List[Comparison]:
        comparisons: List[Comparison] = []
        set_flag = False
        for token in stmt.tokens:
            if is_token_negligible(token):
                continue
            if token.is_keyword:
                if token.normalized == "SET":
                    set_flag = True
                elif set_flag:
                    break
                continue
            if set_flag:
                if isinstance(token, Comparison):
                    comparisons.append(token)
                elif isinstance(token, IdentifierList):
                    comparisons.extend(
                        t for t in token.get_identifiers() if isinstance(t, Comparison)
                    )
                break
        return comparisons

    @classmethod
    def _extract_from_dml_merge(cls, stmt: Statement) -> StatementLineageHolder:
        holder = StatementLineageHolder()
        src_flag = tgt_flag = update_flag = insert_flag = False
        insert_columns = []
        direct_source = None
        for token in stmt.tokens:
            if is_token_negligible(token):
                continue
            if token.is_keyword:
                if token.normalized in {"INTO", "MERGE"}:
                    tgt_flag = True
                elif token.normalized == "USING":
                    src_flag = True
                elif token.normalized == "SET":
                    update_flag = True
                elif token.normalized == "INSERT":
                    insert_flag = True
                elif token.normalized == "WHEN":
                    update_flag = False
                continue

            if tgt_flag:
                if isinstance(token, Identifier):
                    holder.add_write(get_dataset_from_identifier(token, holder))
                tgt_flag = False
            elif src_flag:
                if isinstance(token, Identifier):
                    direct_source = get_dataset_from_identifier(token, holder)
                    holder.add_read(direct_source)
                    subqueries = cls.parse_subquery(token)
                    if subqueries:
                        for sq in subqueries:
                            holder |= cls._extract_from_dml(
                                sq.query, AnalyzerContext(sq, holder.cte)
                            )
                src_flag = False
            elif update_flag:
                comparisons = []
                if isinstance(token, Comparison):
                    comparisons = [token]
                elif isinstance(token, IdentifierList):
                    comparisons = [
                        t for t in token.get_identifiers() if isinstance(t, Comparison)
                    ]
                for c in comparisons:
                    right = c.right
                    if isinstance(right, Identifier):
                        src_col = Column(right.get_real_name())
                        if direct_source is not None:
                            src_col.parent = direct_source
                        tgt_col = Column(c.left.get_real_name())
                        tgt_col.parent = list(holder.write)[0]
                        holder.add_column_lineage(src_col, tgt_col)
            elif insert_flag:
                if isinstance(token, Parenthesis):
                    t = token.tokens[1]
                    identifiers = []
                    if isinstance(t, Identifier):
                        identifiers.append(t)
                    elif isinstance(t, IdentifierList):
                        identifiers.extend(t.get_identifiers())
                    for identifier in identifiers:
                        if not isinstance(identifier, Identifier):
                            continue
                        tgt_col = Column(identifier.get_real_name())
                        tgt_col.parent = list(holder.write)[0]
                        insert_columns.append(tgt_col)
                elif insert_columns and isinstance(token, Values):
                    for sub_token in token.tokens:
                        if isinstance(sub_token, Parenthesis):
                            t = sub_token.tokens[1]
                            identifiers = []
                            if isinstance(t, Identifier):
                                identifiers.append(t)
                            elif isinstance(t, IdentifierList):
                                identifiers.extend(t.get_identifiers())
                            for i, identifier in enumerate(identifiers):
                                if isinstance(identifier, Identifier):
                                    src_col = Column(identifier.get_real_name())
                                    if direct_source is not None:
                                        src_col.parent = direct_source
                                    holder.add_column_lineage(
                                        src_col, insert_columns[i]
                                    )
                    insert_flag = False
        return holder

    @classmethod
    def _extract_from_dml(
        cls, token: TokenList, context: AnalyzerContext
    ) -> SubQueryLineageHolder:
        holder = SubQueryLineageHolder()
        if context.prev_cte is not None:
            # CTE can be referenced by subsequent CTEs
            for cte in context.prev_cte:
                holder.add_cte(cte)
        if context.subquery is not None:
            # If within subquery, then manually add subquery as target table
            holder.add_write(context.subquery)
        current_handlers = [
            handler_cls() for handler_cls in CurrentTokenBaseHandler.__subclasses__()
        ]
        next_handlers = [
            handler_cls() for handler_cls in NextTokenBaseHandler.__subclasses__()
        ]

        subqueries = []
        for sub_token in token.tokens:
            if is_token_negligible(sub_token):
                continue

            for sq in cls.parse_subquery(sub_token):
                # Collecting subquery on the way, hold on parsing until last
                # so that each handler don't have to worry about what's inside subquery
                subqueries.append(sq)

            for current_handler in current_handlers:
                current_handler.handle(sub_token, holder)

            if sub_token.is_keyword:
                for next_handler in next_handlers:
                    next_handler.indicate(sub_token)
                continue

            for next_handler in next_handlers:
                if next_handler.indicator:
                    next_handler.handle(sub_token, holder)
        else:
            # call end of query hook here as loop is over
            for next_handler in next_handlers:
                next_handler.end_of_query_cleanup(holder)
        # By recursively extracting each subquery of the parent and merge, we're doing Depth-first search
        for sq in subqueries:
            holder |= cls._extract_from_dml(sq.query, AnalyzerContext(sq, holder.cte))
        return holder

    @classmethod
    def parse_subquery(cls, token: TokenList) -> List[SubQuery]:
        result = []
        if isinstance(token, (Identifier, Function, Where)):
            # usually SubQuery is an Identifier, but not all Identifiers are SubQuery
            # Function for CTE without AS keyword
            result = cls._parse_subquery(token)
        elif isinstance(token, IdentifierList):
            # IdentifierList for SQL89 style of JOIN or multiple CTEs, this is actually SubQueries
            result = reduce(
                add,
                [
                    cls._parse_subquery(identifier)
                    for identifier in token.get_sublists()
                ],
                [],
            )
        elif is_subquery(token) and isinstance(token, Parenthesis):
            # Parenthesis for SubQuery without alias, this is valid syntax for certain SQL dialect
            result = [SqlParseSubQuery.of(token, None)]
        return result

    @classmethod
    def _parse_subquery(
        cls, token: Union[Identifier, Function, Where]
    ) -> List[SubQuery]:
        """
        convert SubQueryTuple to sqllineage.core.models.SubQuery
        """
        return [
            SqlParseSubQuery.of(parenthesis, alias)
            for parenthesis, alias in get_subquery_parentheses(token)
        ]
