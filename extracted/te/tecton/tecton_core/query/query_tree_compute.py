import contextlib
import logging
from abc import ABC
from abc import abstractmethod
from typing import Callable
from typing import Iterable
from typing import List
from typing import Optional
from typing import Union

import attrs
import pyarrow

from tecton_core.query.dialect import Dialect
from tecton_core.query.executor_params import ExecutionContext
from tecton_core.query.node_interface import NodeRef
from tecton_core.query.node_interface import PartitionSelector
from tecton_core.query.pandas.nodes import ArrowDataNode
from tecton_core.schema import Schema


logger = logging.getLogger(__name__)


@attrs.define
class QueryTreeCompute(ABC):
    """
    Base class for compute (e.g. DWH compute or Python compute) which can be
    used for different stages of executing the query tree.
    """

    @staticmethod
    def for_dialect(
        dialect: Dialect,
        context: ExecutionContext,
        qt_root: Optional[NodeRef] = None,
    ) -> "QueryTreeCompute":
        # Conditional imports are used so that optional dependencies such as the Snowflake connector are only imported
        # if they're needed for a query
        if dialect == Dialect.SNOWFLAKE:
            from tecton_core.query.snowflake.compute import SnowflakeCompute
            from tecton_core.query.snowflake.compute import create_snowflake_connection

            if SnowflakeCompute.is_context_initialized():
                return SnowflakeCompute.from_context()
            return SnowflakeCompute.for_connection(create_snowflake_connection(qt_root, context.secret_resolver))
        if dialect == Dialect.DUCKDB:
            from tecton_core.query.duckdb.compute import DuckDBCompute

            return DuckDBCompute.from_context(duckdb_config=context.duckdb_config)

        if dialect == Dialect.BIGQUERY:
            from tecton_core.query.bigquery.compute import BigqueryCompute

            return BigqueryCompute()

        if dialect == Dialect.ARROW:
            return ArrowCompute()

        msg = f"Dialect {dialect} is not supported"
        raise ValueError(msg)


@attrs.define
class ComputeMonitor:
    set_completed: Callable[[], None] = lambda _: _
    set_query: Callable[[str], None] = lambda _: _

    def monitored_arrow_reader(self, reader: pyarrow.RecordBatchReader) -> pyarrow.RecordBatchReader:
        def monitor_reader(_reader: pyarrow.RecordBatchReader) -> Iterable[pyarrow.RecordBatch]:
            while True:
                try:
                    yield next(_reader)
                except StopIteration:
                    break

            self.set_completed()

        return pyarrow.RecordBatchReader.from_batches(reader.schema, monitor_reader(reader))


@attrs.define
class SQLCompute(QueryTreeCompute, contextlib.AbstractContextManager):
    """
    Base class for compute backed by a SQL engine (e.g. Snowflake and DuckDB).
    """

    @abstractmethod
    def get_dialect(self) -> Dialect:
        pass

    @abstractmethod
    def run_sql(
        self,
        sql_string: str,
        return_dataframe: bool = False,
        expected_output_schema: Optional[Schema] = None,
        monitor: Optional[ComputeMonitor] = None,
        checkpoint_as: Optional[str] = None,
    ) -> Optional[pyarrow.RecordBatchReader]:
        pass

    @abstractmethod
    def register_temp_table(
        self, table_name: str, table_or_reader: Union[pyarrow.Table, pyarrow.RecordBatchReader]
    ) -> None:
        pass

    @abstractmethod
    def unregister_temp_table(self, table_name: str) -> None:
        pass

    def cleanup_temp_tables(self):
        pass

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.cleanup_temp_tables()


@attrs.define
class ArrowCompute(QueryTreeCompute, contextlib.AbstractContextManager):
    def run(
        self,
        output_node_ref: NodeRef,
        input_node_refs: List[NodeRef],
        input_data: List[Union[pyarrow.Table, pyarrow.RecordBatchReader]],
        context: ExecutionContext,
        partition_selector: Optional[PartitionSelector] = None,
        monitor: Optional[ComputeMonitor] = None,
    ) -> "pyarrow.Table":
        for input_node, data in zip(input_node_refs, input_data):
            input_node.node = ArrowDataNode(
                input_reader=data.to_reader() if isinstance(data, pyarrow.Table) else data,
                input_node=None,
                columns=input_node.node.columns,
                column_name_updater=lambda x: x,
                output_schema=input_node.node.output_schema,
            )

        reader = output_node_ref.to_arrow_reader(context, partition_selector)

        return monitor.monitored_arrow_reader(reader) if monitor else reader

    def __exit__(self, exc_type, exc_val, exc_tb):
        pass
