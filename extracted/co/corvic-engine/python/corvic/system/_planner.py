from typing import ClassVar

from more_itertools import flatten

from corvic import op_graph, sql
from corvic.result import InternalError, InvalidArgumentError, Ok
from corvic.system.op_graph_executor import (
    ExecutionContext,
    ExecutionResult,
    OpGraphExecutor,
)


class OpGraphPlanner:
    # list is a whitelist on purpose so that ops are assumed unsafe by default
    NonSliceConfoundingOp: ClassVar = (
        op_graph.op.RenameColumns
        | op_graph.op.SelectColumns
        | op_graph.op.LimitRows
        | op_graph.op.FilterRows
        | op_graph.op.UpdateMetadata
        | op_graph.op.SetMetadata
        | op_graph.op.RemoveFromMetadata
        | op_graph.op.UpdateFeatureTypes
        | op_graph.op.Concat
        | op_graph.op.UnnestStruct
        | op_graph.op.AddLiteralColumn
        | op_graph.op.CombineColumns
        | op_graph.op.EmbedColumn
        | op_graph.op.NestIntoStruct
        | op_graph.op.ConvertColumnToString
        | op_graph.op.AddRowIndex
        | op_graph.op.TruncateList
    )

    @classmethod
    def find_maximal_sql_offload_subgraphs(cls, op: op_graph.Op) -> list[op_graph.Op]:
        """Return the parts of the graph which can be offloaded to SQL backends."""
        offload_subgraph_lists = [
            cls.find_maximal_sql_offload_subgraphs(source_op)
            for source_op in op.sources()
        ]

        for source_op, offload_subgraph_list in zip(
            op.sources(), offload_subgraph_lists, strict=True
        ):
            if not offload_subgraph_list:
                break
            if len(offload_subgraph_list) != 1:
                break
            if offload_subgraph_list[0] != source_op:
                break
        else:
            # all the sources are compatible, so if this op is compatible its the
            # maximal offload subgraph
            if sql.can_be_sql_computed(op):
                return [op]
        return list(flatten(offload_subgraph_lists))

    @classmethod
    def sql_result_can_be_sliced(cls, op: op_graph.Op) -> bool:
        """Return True if the output of the op's SQL offload can be sliced.

        For example, slicing is possible if op has one maximal subgraph that will be
        offloaded and the downstream ops don't have inter-row data dependences.

        The analysis is best-effort and may return False even if the op could be
        offloaded and sliced.
        """
        offload_subgraphs = cls.find_maximal_sql_offload_subgraphs(op)
        if len(offload_subgraphs) != 1:
            return False

        offloaded_op = offload_subgraphs[0]

        def has_slice_confounding_op(op: op_graph.Op) -> bool:
            if op == offloaded_op:
                return False
            if not isinstance(op, cls.NonSliceConfoundingOp):
                return True
            return any(
                has_slice_confounding_op(source_op) for source_op in op.sources()
            )

        return not has_slice_confounding_op(op)

    @classmethod
    def _join_rows_upperbound(cls, op: op_graph.op.Join) -> int:
        match op.how:
            case op_graph.JoinType.JOIN_TYPE_INNER:
                left_rows = cls.count_rows_upperbound(op.left_source)
                right_rows = cls.count_rows_upperbound(op.right_source)
                return min(left_rows, right_rows)
            case op_graph.JoinType.JOIN_TYPE_LEFT_OUTER:
                return cls.count_rows_upperbound(op.left_source)
            case _:
                return cls.count_rows_upperbound(
                    op.left_source
                ) + cls.count_rows_upperbound(op.right_source)

    @classmethod
    def _concat_rows_upperbound(cls, op: op_graph.op.Concat) -> int:
        match op.how:
            case "vertical" | "vertical_relaxed" | "diagonal" | "diagonal_relaxed":
                return sum(cls.count_rows_upperbound(source) for source in op.sources())
            case "horizontal" | "align":
                return max(cls.count_rows_upperbound(source) for source in op.sources())

    @classmethod
    def count_rows_upperbound(cls, op: op_graph.Op) -> int:
        match op:
            case (
                op_graph.op.SelectFromStaging()
                | op_graph.op.ReadFromParquet()
                | op_graph.op.SelectFromVectorStaging()
            ):
                num_rows = op.expected_rows
            case (
                op_graph.op.SelectColumns()
                | op_graph.op.RenameColumns()
                | op_graph.op.UpdateMetadata()
                | op_graph.op.SetMetadata()
                | op_graph.op.RemoveFromMetadata()
                | op_graph.op.UpdateFeatureTypes()
                | op_graph.op.UnnestStruct()
                | op_graph.op.AddLiteralColumn()
                | op_graph.op.OrderBy()
                | op_graph.op.FilterRows()
                | op_graph.op.DistinctRows()
                | op_graph.op.RollupByAggregation()
                | op_graph.op.EmbeddingCoordinates()
                | op_graph.op.EmbeddingMetrics()
                # a large over-estimation for node2vec the but the best
                # we can do without looking at the data
                | op_graph.op.EmbedNode2vecFromEdgeLists()
                | op_graph.op.CombineColumns()
                | op_graph.op.EmbedColumn()
                | op_graph.op.EncodeColumn()
                | op_graph.op.NestIntoStruct()
                | op_graph.op.CorrelateColumns()
                | op_graph.op.HistogramColumn()
                | op_graph.op.ConvertColumnToString()
                | op_graph.op.AddRowIndex()
                | op_graph.op.OutputCsv()
                | op_graph.op.TruncateList()
                | op_graph.op.Union()
                | op_graph.op.EmbedImageColumn()
                | op_graph.op.AddDecisionTreeSummary()
                | op_graph.op.UnnestList()
            ):
                num_rows = sum(
                    cls.count_rows_upperbound(source) for source in op.sources()
                )

            case op_graph.op.Concat():
                num_rows = cls._concat_rows_upperbound(op)
            case op_graph.op.Join():
                num_rows = cls._join_rows_upperbound(op)
            case op_graph.op.LimitRows() | op_graph.op.SampleRows():
                source_rows = cls.count_rows_upperbound(op.source)
                num_rows = min(op.num_rows, source_rows)
            case op_graph.op.Empty():
                num_rows = 0
            case op_graph.op.AggregateColumns():
                return 1
        return num_rows


class ValidateFirstExecutor(OpGraphExecutor):
    """An executor that validates compute contexts before executing them."""

    def __init__(self, wrapped_executor: OpGraphExecutor):
        self._wrapped_executor = wrapped_executor

    def execute(
        self, context: ExecutionContext
    ) -> Ok[ExecutionResult] | InvalidArgumentError | InternalError:
        """Execute all the OpGraphs described by the context."""
        for table_context in context.tables_to_compute:
            if (
                table_context.sql_output_slice_args is not None
                and not OpGraphPlanner.sql_result_can_be_sliced(
                    table_context.table_op_graph
                )
            ):
                return InvalidArgumentError(
                    "sql_output_slice_args set but impossible on a given op_graph"
                )
        return self._wrapped_executor.execute(context)
