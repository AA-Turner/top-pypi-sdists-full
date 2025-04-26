import contextlib
import logging
from abc import ABC
from abc import abstractmethod
from typing import TYPE_CHECKING
from typing import Callable
from typing import Dict
from typing import Optional
from typing import Union

import attrs
import pyarrow

from tecton_core.query.dialect import Dialect
from tecton_core.query.executor_params import ExecutionContext
from tecton_core.query.node_interface import NodeRef
from tecton_core.query.nodes import StagedTableScanNode
from tecton_core.query.pandas.nodes import ArrowDataNode
from tecton_core.schema import Schema


if TYPE_CHECKING:
    from tecton_core.query.query_tree_executor import QueryTreeExecutor


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
        executor: "QueryTreeExecutor",
        qt_root: Optional[NodeRef] = None,
    ) -> "QueryTreeCompute":
        # Conditional imports are used so that optional dependencies such as the Snowflake connector are only imported
        # if they're needed for a query
        if dialect == Dialect.SNOWFLAKE:
            from tecton_core.query.snowflake.compute import SnowflakeCompute
            from tecton_core.query.snowflake.compute import create_snowflake_connection

            if SnowflakeCompute.is_context_initialized():
                return SnowflakeCompute.from_context()
            return SnowflakeCompute.for_connection(create_snowflake_connection(qt_root, executor.secret_resolver))
        if dialect == Dialect.DUCKDB:
            from tecton_core.query.duckdb.compute import DuckDBCompute

            return DuckDBCompute.from_context(
                offline_store_options=executor.offline_store_options_providers, duckdb_config=executor.duckdb_config
            )

        if dialect == Dialect.BIGQUERY:
            from tecton_core.query.bigquery.compute import BigqueryCompute

            return BigqueryCompute()

        if dialect == Dialect.ARROW:
            return ArrowCompute()

        msg = f"Dialect {dialect} is not supported"
        raise ValueError(msg)


@attrs.define
class ComputeMonitor:
    log_progress: Callable[[float], None] = lambda _: _
    set_query: Callable[[str], None] = lambda _: _


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
        qt_node: NodeRef,
        input_data: Dict[str, pyarrow.RecordBatchReader],
        context: ExecutionContext,
        monitor: Optional[ComputeMonitor] = None,
    ) -> "pyarrow.RecordBatchReader":
        def replace_staging_scan_nodes(tree: NodeRef) -> None:
            if isinstance(tree.node, StagedTableScanNode):
                staged_table_name = tree.node.staging_table_name
                if staged_table_name not in input_data:
                    msg = f"Missing input {staged_table_name}"
                    raise ValueError(msg)

                tree.node = ArrowDataNode(
                    input_reader=input_data[staged_table_name],
                    input_node=None,
                    columns=tree.node.columns,
                    column_name_updater=lambda x: x,
                    output_schema=tree.node.output_schema,
                )
                return

            for i in tree.inputs:
                replace_staging_scan_nodes(i)

        replace_staging_scan_nodes(qt_node)

        return qt_node.to_arrow_reader(context)

    def __exit__(self, exc_type, exc_val, exc_tb):
        pass
