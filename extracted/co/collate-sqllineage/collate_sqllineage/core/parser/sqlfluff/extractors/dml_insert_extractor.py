from typing import Any, Optional

from sqlfluff.core.parser import BaseSegment

from collate_sqllineage.core.holders import SubQueryLineageHolder
from collate_sqllineage.core.models import AnalyzerContext, Column, Schema, Table
from collate_sqllineage.core.parser.sqlfluff.extractors.dml_select_extractor import (
    DmlSelectExtractor,
)
from collate_sqllineage.core.parser.sqlfluff.extractors.lineage_holder_extractor import (
    LineageHolderExtractor,
)
from collate_sqllineage.core.parser.sqlfluff.models import (
    SqlFluffColumn,
    SqlFluffSubQuery,
    SqlFluffTable,
)
from collate_sqllineage.core.parser.sqlfluff.utils import (
    get_child,
    get_identifier,
    get_innermost_bracketed,
    get_subqueries,
    is_union,
    retrieve_segments,
)


class DmlInsertExtractor(LineageHolderExtractor):
    """
    DML Insert queries lineage extractor
    """

    SUPPORTED_STMT_TYPES = [
        "insert_statement",
        "create_table_statement",
        "create_table_as_statement",
        "create_view_statement",
        "create_materialized_view_statement",
        "update_statement",
        "copy_statement",
        "insert_overwrite_directory_hive_fmt_statement",
        "copy_into_statement",
        "copy_into_table_statement",
        "copy_into_location_statement",
        "create_stream_statement",
    ]

    def __init__(self, dialect: str):
        super().__init__(dialect)

    def extract(
        self,
        statement: BaseSegment,
        context: AnalyzerContext,
        is_sub_query: bool = False,
    ) -> SubQueryLineageHolder:
        """
        Extract lineage for a given statement.
        :param statement: a sqlfluff segment with a statement
        :param context: 'AnalyzerContext'
        :param is_sub_query: determine if the statement is bracketed or not
        :return 'SubQueryLineageHolder' object
        """
        handlers, conditional_handlers = self._init_handlers()

        holder = self._init_holder(context)

        set_clause_list_segment = None
        where_clause_segment = None
        segments = retrieve_segments(statement)
        for segment in segments:
            for current_handler in handlers:
                current_handler.handle(segment, holder)

            if segment.type == "with_compound_statement":
                from .cte_extractor import DmlCteExtractor

                holder |= DmlCteExtractor(self.dialect).extract(
                    segment,
                    AnalyzerContext(
                        prev_cte=holder.cte,
                        prev_write=holder.write,
                        target_columns=holder.target_columns,
                    ),
                )
            elif segment.type == "bracketed" and any(
                s.type == "with_compound_statement" for s in segment.segments
            ):
                for sgmt in segment.segments:
                    if sgmt.type == "with_compound_statement":
                        from .cte_extractor import DmlCteExtractor

                        holder |= DmlCteExtractor(self.dialect).extract(
                            sgmt,
                            AnalyzerContext(
                                prev_cte=holder.cte,
                                prev_write=holder.write,
                                target_columns=holder.target_columns,
                            ),
                        )

            elif segment.type == "bracketed" and (
                self.parse_subquery(segment) or is_union(segment)
            ):
                # note regular subquery within SELECT statement is handled by DmlSelectExtractor, this is only to handle
                # top-level subquery in DML like: 1) create table foo as (subquery); 2) insert into foo (subquery)
                # subquery here isn't added as read source, and it inherits DML-level target_columns if parsed
                subquery_segment_select = get_child(segment, "select_statement")
                subquery_segment_set = get_child(segment, "set_expression")
                if subquery_segment_select:
                    self._extract_select(holder, subquery_segment_select)
                elif subquery_segment_set:
                    self._extract_set(holder, subquery_segment_set)
            elif segment.type == "select_statement":
                self._extract_select(holder, segment)
            elif segment.type == "set_expression":
                self._extract_set(holder, segment)
            elif segment.type == "set_clause_list":
                self._extract_set_clause_list(holder, segment)
                set_clause_list_segment = segment
            elif segment.type == "where_clause":
                where_clause_segment = segment
            else:
                for conditional_handler in conditional_handlers:
                    if conditional_handler.indicate(segment):
                        conditional_handler.handle(segment, holder)

        if statement.type == "update_statement":
            self._resolve_update_aliased_target(
                statement, holder, conditional_handlers[0]
            )

        self._handle_source_tables(holder, conditional_handlers[0])

        if set_clause_list_segment is not None:
            self._extract_update_set_columns(
                holder, set_clause_list_segment, conditional_handlers[0]
            )

        if where_clause_segment is not None:
            self._extract_where_subquery_tables(holder, where_clause_segment)

        return holder

    def _extract_set(self, holder: SubQueryLineageHolder, set_segment: BaseSegment):
        for sub_segment in retrieve_segments(set_segment):
            if sub_segment.type == "select_statement":
                self._extract_select(holder, sub_segment, set_segment)

    def _extract_select(
        self,
        holder: SubQueryLineageHolder,
        select_segment: BaseSegment,
        set_segment: Optional[BaseSegment] = None,
    ):
        holder |= DmlSelectExtractor(self.dialect).extract(
            select_segment,
            AnalyzerContext(
                SqlFluffSubQuery.of(
                    set_segment if set_segment else select_segment, None
                ),
                prev_cte=holder.cte,
                prev_write=holder.write,
                target_columns=holder.target_columns,
            ),
        )

    def _handle_source_tables(
        self,
        holder: SubQueryLineageHolder,
        conditional_handlers: Any,
    ):
        """
        Method to handle update from select type of queries
        for example,
        update xyz set a=a1 from abc;
        """
        if hasattr(conditional_handlers, "tables") and conditional_handlers.tables:
            for table in conditional_handlers.tables:
                holder.add_read(table)

    def _extract_set_clause_list(
        self, holder: SubQueryLineageHolder, segment: BaseSegment
    ):
        """
        Extract subqueries within SET clauses list
        :param segment: SET clause list segment
        :param holder: lineage holder to update
        """
        for set_clause in retrieve_segments(segment):
            if set_clause.type != "set_clause":
                continue

            bracketed = get_innermost_bracketed(set_clause)
            if not bracketed:
                continue

            select_stmt = self._extract_select_from_bracketed(bracketed)
            if select_stmt:
                self._extract_select(holder, select_stmt)

    def _extract_update_set_columns(
        self,
        holder: SubQueryLineageHolder,
        set_clause_list: BaseSegment,
        source_handler: Any,
    ):
        """
        Build column lineage for an UPDATE SET clause. Each `target = expr`
        assignment maps the expression's source columns onto the target column,
        resolved through the same alias mapping the SELECT extractor uses so an
        alias like `s` lands on its real table.
        """
        if not holder.write:
            return
        write_table = list(holder.write)[0]
        read_tables = set(holder.read)
        source_tables = getattr(source_handler, "tables", [])
        alias_mapping = source_handler.get_alias_mapping_from_table_group(
            source_tables, holder
        )
        for set_clause in retrieve_segments(set_clause_list):
            if set_clause.type != "set_clause":
                continue
            bracketed = get_innermost_bracketed(set_clause)
            if bracketed is not None and self._extract_select_from_bracketed(bracketed):
                # `SET col = (subquery)` is already handled by _extract_set_clause_list
                continue
            segments = retrieve_segments(set_clause)
            # tsql uses `assignment_operator`, other dialects (e.g. snowflake) parse
            # the SET `=` as a `comparison_operator`.
            operator_index = next(
                (
                    i
                    for i, s in enumerate(segments)
                    if s.type in ("assignment_operator", "comparison_operator")
                ),
                None,
            )
            if operator_index is None or operator_index + 1 >= len(segments):
                continue
            target_segment = segments[operator_index - 1]
            source_segment = segments[operator_index + 1]
            if target_segment.type != "column_reference":
                continue
            source_columns = SqlFluffColumn._extract_source_columns(source_segment)
            if not source_columns:
                continue
            target_column = Column(
                get_identifier(target_segment), source_columns=source_columns
            )
            target_column.parent = write_table
            for source_column in target_column.to_source_columns(alias_mapping):
                # Only emit when the source resolves to a real table in the
                # statement, never to a phantom default-schema alias.
                if source_column.parent in read_tables:
                    holder.add_column_lineage(source_column, target_column)

    def _resolve_update_aliased_target(
        self,
        statement: BaseSegment,
        holder: SubQueryLineageHolder,
        source_handler: Any,
    ):
        """
        `UPDATE alias SET ... FROM real_table alias ...` (T-SQL, Postgres) writes
        to a table declared in the FROM clause under an alias. Rewrite the write
        target to that real table and drop it from the sources.
        """
        target_ref = statement.get_child("table_reference")
        if target_ref is None:
            return
        target_table = SqlFluffTable.of(target_ref)
        if str(target_table.schema) != Schema.unknown:
            return
        matched = next(
            (
                tbl
                for tbl in getattr(source_handler, "tables", [])
                if isinstance(tbl, Table)
                and tbl.alias != tbl.raw_name
                and target_table.raw_name == tbl.alias
            ),
            None,
        )
        if matched is None:
            return
        for write_table in list(holder.write):
            if write_table in holder.graph:
                holder.graph.remove_node(write_table)
        holder.add_write(matched)
        source_handler.tables = [
            tbl for tbl in source_handler.tables if tbl is not matched
        ]

    def _extract_where_subquery_tables(
        self, holder: SubQueryLineageHolder, where_clause: BaseSegment
    ):
        """
        Tables referenced only inside a WHERE subquery are still sources. Each
        subquery is resolved through the SELECT extractor so nested subqueries
        and set operations contribute all their real tables.
        """
        for subquery, _alias in get_subqueries(where_clause):
            select_stmt = next(subquery.recursive_crawl("select_statement"), None)
            if select_stmt is None:
                continue
            subquery_holder = DmlSelectExtractor(self.dialect).extract(
                select_stmt, AnalyzerContext(), True
            )
            for table in subquery_holder.read:
                if isinstance(table, Table):
                    holder.add_read(table)

    def _extract_select_from_bracketed(self, segment: BaseSegment):
        """
        Extract SELECT statement from a bracketed segment
        :param segment: Bracketed segment
        :return: SELECT statement segment or None
        """
        expression = get_child(segment, "expression")
        if not expression:
            return None

        return get_child(expression, "select_statement")
