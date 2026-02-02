"""Corvic system op graph executeor protocol."""

from __future__ import annotations

import dataclasses
from collections.abc import Mapping, Sequence
from typing import Any, Protocol

import pyarrow as pa

from corvic import op_graph
from corvic.result import InternalError, InvalidArgumentError, Ok


@dataclasses.dataclass(frozen=True)
class TableSliceArgs:
    """Arguments for defining a slice of a table."""

    offset: int
    length: int


@dataclasses.dataclass
class TableComputeContext:
    """Parameters needed to compute one table."""

    table_op_graph: op_graph.Op
    output_url_prefix: str
    sql_output_slice_args: TableSliceArgs | None = None
    """When provided, slice the output of the SQL backend and compute on that slice.

    Callers are guaranteed to get all of the results as long as they execute all of the
    slices, (and there aren't joins in the post sql part of the graph).

    Callers can use planning functions exported by executors to assist in picking
    reasonable slice arguments:
        OpGraphExecutor.find_maximal_sql_offload_subgraphs()
        OpGraphExecutor.find_row_count_upperbound()
        OpGraphExecutor.sql_output_can_be_sliced()
    """

    def with_slice_args(self, offset: int, length: int) -> TableComputeContext:
        return dataclasses.replace(
            self, sql_output_slice_args=TableSliceArgs(offset=offset, length=length)
        )


@dataclasses.dataclass
class ExecutionContext:
    """Description of the computation to be completed."""

    tables_to_compute: list[TableComputeContext]
    """A list of tables that the caller wants in addition to table_to_compute.

    This has advantages over multimple invocations of OpGraphExecutor when those
    additional tables would be computed to compute tables_to_compute anyway; i.e.,
    they are nodes in the tables_to_compute op graph.
    """


class TableComputeResult(Protocol):
    """Opaque container for the results of computing an OpGraph."""

    def to_batch_reader(self) -> pa.RecordBatchReader:
        """Render the results as a stream of RecordBatches."""
        ...

    @property
    def metrics(self) -> Mapping[str, Any]:
        """Metrics computed by metrics operations during computation."""
        ...

    def to_urls(self) -> list[str]:
        """Render the results as a list of urls pointing to parquet files."""
        ...

    @property
    def context(self) -> TableComputeContext:
        """The context this table was computed for."""
        ...


class ExecutionResult(Protocol):
    """Opaque container for the results of an execution."""

    @property
    def tables(self) -> Sequence[TableComputeResult]:
        """Results for the executed op graphs.

        Ordered according to the how their TableComputeContexts were ordered in the
        ExecutionContext.
        """
        ...

    @property
    def context(self) -> ExecutionContext:
        """The context this table was computed for."""
        ...


class OpGraphExecutor(Protocol):
    """Execute table op graphs."""

    def execute(
        self, context: ExecutionContext
    ) -> Ok[ExecutionResult] | InvalidArgumentError | InternalError:
        """Execute all the OpGraphs described by the context."""
        ...
