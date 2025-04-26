import logging
import traceback
from typing import Union

from sqlfluff.core.parser import BaseSegment

from collate_sqllineage.core.holders import SubQueryLineageHolder
from collate_sqllineage.core.models import AnalyzerContext, Path, SubQuery, Table
from collate_sqllineage.core.parser import SourceHandlerMixin
from collate_sqllineage.core.parser.sqlfluff.handlers.base import (
    ConditionalSegmentBaseHandler,
)
from collate_sqllineage.core.parser.sqlfluff.holder_utils import (
    retrieve_holder_data_from,
)
from collate_sqllineage.core.parser.sqlfluff.models import (
    SqlFluffColumn,
    SqlFluffFunction,
    SqlFluffSubQuery,
)
from collate_sqllineage.core.parser.sqlfluff.utils import (
    find_table_identifier,
    get_grandchild,
    get_grandchildren,
    get_inner_from_expression,
    get_multiple_identifiers,
    get_subqueries,
    is_union,
    is_values_clause,
    retrieve_extra_segment,
    retrieve_segments,
)

logger = logging.getLogger(__name__)

RESERVED_FUNCTIONS = ("table",)


class SourceHandler(SourceHandlerMixin, ConditionalSegmentBaseHandler):
    """
    Source table and column handler
    """

    def __init__(self, dialect: str):
        self.columns = []
        self.tables = []
        self.union_barriers = []
        self.dialect = dialect

    def indicate(self, segment: BaseSegment) -> bool:
        """
        Indicates if the handler can handle the segment
        :param segment: segment to be processed
        :return: True if it can be handled
        """
        return (
            self._indicate_column(segment)
            or self._indicate_table(segment)
            or is_union(segment)
        )

    def handle(self, segment: BaseSegment, holder: SubQueryLineageHolder) -> None:
        """
        Handle the segment, and update the lineage result accordingly in the holder
        :param segment: segment to be handled
        :param holder: 'SubQueryLineageHolder' to hold lineage
        """
        if self._indicate_table(segment):
            self._handle_table(segment, holder)
        elif is_union(segment):
            self._handle_union(segment, holder)
        if self._indicate_column(segment):
            self._handle_column(segment, holder)

    def _handle_table(
        self, segment: BaseSegment, holder: SubQueryLineageHolder
    ) -> None:
        """
        Table handler method
        :param segment: segment to be handled
        :param holder: 'SubQueryLineageHolder' to hold lineage
        """
        identifiers = get_multiple_identifiers(segment)
        if identifiers and len(identifiers) > 1:
            for identifier in identifiers:
                self._add_dataset_from_expression_element(identifier, holder)
        from_segment = get_inner_from_expression(segment)
        if from_segment.type == "from_expression_element":
            self._add_dataset_from_expression_element(from_segment, holder)
        for extra_segment in retrieve_extra_segment(segment):
            self._handle_table(extra_segment, holder)

    def _handle_table_from_select_statement(
        self, sub_segment: BaseSegment, holder: SubQueryLineageHolder
    ) -> None:
        """
        Handle table from select statement
        :param segment: segment to be handled
        """
        select_bracked_statement = get_grandchild(
            sub_segment, "expression", "bracketed"
        )
        select_statement = None
        if select_bracked_statement:
            select_statement = get_grandchild(
                select_bracked_statement, "expression", "select_statement"
            )
        else:
            select_statement = get_grandchild(
                sub_segment, "expression", "select_statement"
            )

        if select_statement:
            from collate_sqllineage.core.parser.sqlfluff.extractors.dml_select_extractor import (
                DmlSelectExtractor,
            )

            dml_select_extractor = DmlSelectExtractor(self.dialect)
            read = dml_select_extractor.extract(
                select_statement, AnalyzerContext(), True
            )
            holder |= read

    def _handle_column(
        self, segment: BaseSegment, holder: SubQueryLineageHolder
    ) -> None:
        """
        Column handler method
        :param segment: segment to be handled
        """
        sub_segments = retrieve_segments(segment)
        for sub_segment in sub_segments:
            if sub_segment.type == "select_clause_element":
                try:
                    self.columns.append(SqlFluffColumn.of(sub_segment))
                    self._handle_table_from_select_statement(sub_segment, holder)
                except Exception as err:
                    logger.warning(
                        f"Failed to parse column {str(sub_segment)} due to {err}"
                    )
                    logger.debug(traceback.format_exc())

    def _handle_union(
        self, segment: BaseSegment, holder: SubQueryLineageHolder
    ) -> None:
        """
        Union handler method
        :param segment: segment to be handled
        """
        subqueries = get_subqueries(segment)
        if subqueries:
            for idx, sq in enumerate(subqueries):
                if idx != 0:
                    self.union_barriers.append((len(self.columns), len(self.tables)))
                subquery, alias = sq
                table_identifier = find_table_identifier(subquery)
                if table_identifier:
                    segments = retrieve_segments(subquery)
                    for seg in segments:
                        if seg.type == "select_clause":
                            self._handle_column(seg, holder=holder)
                    dataset = retrieve_holder_data_from(
                        segments, holder, table_identifier, alias=alias
                    )
                    self.tables.append(dataset)

    def _data_function_handler(self, function: BaseSegment):
        """
        Handle function as table
        :param function: function segment
        """
        if function:
            function_name = function.get_child("function_name")
            if (
                function_name is not None
                and function_name.raw.lower() not in RESERVED_FUNCTIONS
            ):
                self.tables.append(SqlFluffFunction.of(function_name))
            expressions = get_grandchildren(function, "bracketed", "expression")
            try:
                sub_expressions = get_grandchild(
                    function, "function_contents", "bracketed"
                )
                if sub_expressions:
                    expressions += sub_expressions.get_children("expression")
            except Exception:
                pass
            for expression in expressions or []:
                self._data_function_handler(expression.get_child("function"))

    def _add_dataset_from_expression_element(
        self, segment: BaseSegment, holder: SubQueryLineageHolder
    ) -> None:
        """
        Append tables and subqueries identified in the 'from_expression_element' type segment to the table and
        holder extra subqueries sets
        :param segment: 'from_expression_element' type segment
        :param holder: 'SubQueryLineageHolder' to hold lineage
        """
        dataset: Union[Path, Table, SubQuery]
        all_segments = [
            seg for seg in retrieve_segments(segment) if seg.type != "keyword"
        ]
        first_segment = all_segments[0]
        function_as_table = get_grandchild(segment, "table_expression", "function")
        if first_segment.type == "function":
            # function()
            self._data_function_handler(first_segment)
        elif function_as_table:
            # function()
            self._data_function_handler(function_as_table)
        elif first_segment.type == "bracketed" and is_values_clause(first_segment):
            # (VALUES ...) AS alias, no dataset involved
            return
        elif is_union(segment):
            subqueries = get_subqueries(segment)
            subquery, alias = subqueries[0]
            self.tables.append(SqlFluffSubQuery.of(subquery, alias))
        else:
            subqueries = get_subqueries(segment)
            if subqueries:
                for sq in subqueries:
                    bracketed, alias = sq
                    read_sq = SqlFluffSubQuery.of(bracketed, alias)
                    holder.extra_subqueries.add(read_sq)
                    self.tables.append(read_sq)
            else:
                table_identifier = find_table_identifier(segment)
                if table_identifier:
                    dataset = retrieve_holder_data_from(
                        all_segments, holder, table_identifier
                    )
                    self.tables.append(dataset)

    @staticmethod
    def _indicate_column(segment: BaseSegment) -> bool:
        """
        Check if it is a column
        :param segment: segment to be checked
        :return: True if type is 'select_clause'
        """
        return bool(segment.type == "select_clause")

    @staticmethod
    def _indicate_table(segment: BaseSegment) -> bool:
        """
        Check if it is a table
        :param segment: segment to be checked
        :return: True if type is 'from_clause'
        """
        return bool(segment.type == "from_clause")
