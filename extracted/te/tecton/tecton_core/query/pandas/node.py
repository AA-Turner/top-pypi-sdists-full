from __future__ import annotations

import typing
from abc import abstractmethod
from typing import Callable
from typing import List
from typing import Optional
from typing import Tuple

import attrs
import pandas
import pyarrow

from tecton_core.query import node_interface
from tecton_core.query.executor_params import ExecutionContext
from tecton_core.query.node_interface import NodeRef
from tecton_core.query.node_interface import PartitionSelector
from tecton_core.query.pandas.sql import SqlExecutor
from tecton_core.schema import Schema


# SqlExecNodes are responsible for executing the sql string produced by the query node and using its SqlExecutor to
# output a pandas dataframe


@attrs.frozen
class SqlExecNode:
    columns: List[str]
    sql_string: str
    sql_executor: SqlExecutor

    @classmethod
    def from_sql_inputs(
        cls, query_node: node_interface.QueryNode, sql_executor: SqlExecutor, pretty_sql: bool = False
    ) -> "SqlExecNode":
        return cls(
            columns=query_node.columns, sql_string=query_node.to_sql(pretty_sql=pretty_sql), sql_executor=sql_executor
        )  # type: ignore

    def to_dataframe(self) -> pandas.DataFrame:
        df = self._to_dataframe()
        # TODO(TEC-15985): Because we do not refresh schemas on data sources, we can sometimes get different columns than what we have
        # cached.
        if {c.lower() for c in df.columns} != {c.lower() for c in self.columns}:
            pass
            # Because we do not refresh schemas on data sources, we can sometimes get different columns than what we have
            # cached. This is problematic but will require separate solution; don't fail for now
            # raise RuntimeError(f"Returned mismatch of columns: received: {df.columns}, expected: {self.columns}")
        return df

    def _to_dataframe(self) -> pandas.DataFrame:
        pandas_df = self.sql_executor.read_sql(self.sql_string)
        return pandas_df


# PandasExecNodes are responsible for taking in a pandas dataframe, performing some pandas operation and outputting a
# pandas dataframe


@attrs.frozen
class ArrowExecNode:
    columns: Tuple[str]
    output_schema: Schema
    input_node: Optional[NodeRef]
    column_name_updater: Optional[Callable[[str], str]]  # Snowflake uses this method to uppercase all column names

    @classmethod
    def from_node_inputs(
        cls,
        query_node: node_interface.QueryNode,
        input_node: Optional[NodeRef],
        column_name_updater: Optional[Callable[[str], str]] = lambda x: x,
    ) -> "ArrowExecNode":
        kwargs = attrs.asdict(query_node, recurse=False)
        kwargs["input_node"] = input_node
        kwargs["columns"] = query_node.columns
        kwargs["output_schema"] = query_node.output_schema
        kwargs["column_name_updater"] = column_name_updater
        del kwargs["dialect"]
        del kwargs["compute_mode"]
        del kwargs["func"]
        del kwargs["node_id"]
        return cls(**kwargs)

    def to_dataframe(self) -> pandas.DataFrame:
        df = self._to_dataframe()
        if {c.lower() for c in df.columns} != {c.lower() for c in self.columns}:
            pass
            # Because we do not refresh schemas on data sources, we can sometimes get different columns than what we have
            # cached. This is problematic but will require separate solution; don't fail for now
            # raise RuntimeError(f"Returned mismatch of columns: received: {df.columns}, expected: {self.columns}")
        return df

    @abstractmethod
    def to_arrow_reader(
        self, context: ExecutionContext, partition_selector: Optional["PartitionSelector"] = None
    ) -> "pyarrow.RecordBatchReader":
        raise NotImplementedError

    def _to_dataframe(self) -> pandas.DataFrame:
        raise NotImplementedError

    @property
    def inputs(self) -> typing.Sequence[NodeRef]:
        return (self.input_node,) if self.input_node else ()

    @property
    def input_names(self) -> Optional[List[str]]:
        return None

    @property
    def output_partitioning(self):
        assert self.input_node is not None, f"{self.__class__} must implement output_partitioning property"
        return self.input_node.output_partitioning

    def as_ref(self) -> NodeRef:
        return NodeRef(self)
