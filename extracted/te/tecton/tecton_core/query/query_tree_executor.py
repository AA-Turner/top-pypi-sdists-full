import contextlib
import logging
from dataclasses import dataclass
from datetime import datetime
from typing import Dict
from typing import Iterable
from typing import Iterator
from typing import List
from typing import Optional
from typing import Tuple

import attrs
import pandas
import pyarrow
import pyarrow.dataset

from tecton_core import conf
from tecton_core import specs
from tecton_core.compute_mode import ComputeMode
from tecton_core.duckdb_factory import DuckDBConfig
from tecton_core.embeddings.model_artifacts import DEFAULT_MODEL_PROVIDER
from tecton_core.embeddings.model_artifacts import ModelArtifactProvider
from tecton_core.offline_store import DEFAULT_OPTIONS_PROVIDERS
from tecton_core.offline_store import OfflineStoreOptionsProvider
from tecton_core.query.data_sources import FileDataSourceScanNode
from tecton_core.query.data_sources import PushTableSourceScanNode
from tecton_core.query.data_sources import RedshiftDataSourceScanNode
from tecton_core.query.dialect import Dialect
from tecton_core.query.duckdb.rewrite import DuckDBTreeRewriter
from tecton_core.query.errors import UserDefinedTransformationError
from tecton_core.query.executor_params import ExecutionContext
from tecton_core.query.executor_params import QueryTreeStep
from tecton_core.query.executor_utils import DebugOutput
from tecton_core.query.executor_utils import QueryTreeMonitor
from tecton_core.query.executor_utils import get_stage_type_for_dialect
from tecton_core.query.node_interface import NodeRef
from tecton_core.query.node_utils import get_first_input_node_of_class
from tecton_core.query.node_utils import get_pipeline_dialect
from tecton_core.query.node_utils import get_staging_nodes
from tecton_core.query.nodes import DataSourceScanNode
from tecton_core.query.nodes import FeatureViewPipelineNode
from tecton_core.query.nodes import JoinNode
from tecton_core.query.nodes import MultiOdfvPipelineNode
from tecton_core.query.nodes import RenameColsNode
from tecton_core.query.nodes import StagedTableScanNode
from tecton_core.query.nodes import StagingNode
from tecton_core.query.nodes import TextEmbeddingInferenceNode
from tecton_core.query.nodes import UserSpecifiedDataNode
from tecton_core.query.optimize.adaptive import should_use_optimized_full_aggregate_node
from tecton_core.query.pandas.node import ArrowExecNode
from tecton_core.query.pandas.nodes import PandasDataSourceScanNode
from tecton_core.query.pandas.nodes import PandasFeatureViewPipelineNode
from tecton_core.query.pandas.nodes import PandasMultiOdfvPipelineNode
from tecton_core.query.pandas.nodes import PandasRenameColsNode
from tecton_core.query.pandas.nodes import PyArrowDataSourceScanNode
from tecton_core.query.query_tree_compute import ArrowCompute
from tecton_core.query.query_tree_compute import ComputeMonitor
from tecton_core.query.query_tree_compute import QueryTreeCompute
from tecton_core.query.query_tree_compute import SQLCompute
from tecton_core.secret_management import SecretResolver


logger = logging.getLogger(__name__)


def _pyarrow_type_contains_map_type(pyarrow_type: pyarrow.DataType) -> bool:
    if isinstance(pyarrow_type, pyarrow.MapType):
        return True
    elif isinstance(pyarrow_type, pyarrow.StructType):
        return any(_pyarrow_type_contains_map_type(field.type) for field in pyarrow_type)
    elif isinstance(pyarrow_type, pyarrow.ListType):
        return _pyarrow_type_contains_map_type(pyarrow_type.value_type)
    return False


@dataclass
class QueryTreeOutput:
    output: Optional[pyarrow.RecordBatchReader] = None

    @property
    def result_df(self) -> pandas.DataFrame:
        contains_map_type = any(_pyarrow_type_contains_map_type(field.type) for field in self.output.schema)
        if contains_map_type:
            # The `maps_as_pydicts` parameter for pyarrow.Table.to_pandas is only supported starting in pyarrow 13.0.0.
            if pyarrow.__version__ < "13.0.0":
                msg = f"Rift requires pyarrow>=13.0.0 to perform feature retrieval for Map features. You have version {pyarrow.__version__}."
                raise RuntimeError(msg)
            return self.output.read_pandas(maps_as_pydicts="strict")

        return self.output.read_pandas()

    @property
    def result_table(self) -> "pyarrow.RecordBatchReader":
        return self.output


UserErrors = (UserDefinedTransformationError,)


def get_data_source_dialect_and_physical_node(
    node: DataSourceScanNode,
) -> Tuple[Dialect, Optional[ArrowExecNode]]:
    batch_source = node.ds.batch_source
    if isinstance(batch_source, specs.PandasBatchSourceSpec):
        exec_node = PandasDataSourceScanNode.from_node_inputs(query_node=node, input_node=None)
        return Dialect.ARROW, exec_node
    elif isinstance(batch_source, specs.PyArrowBatchSourceSpec):
        exec_node = PyArrowDataSourceScanNode.from_node_inputs(query_node=node, input_node=None)
        return Dialect.ARROW, exec_node
    elif isinstance(batch_source, specs.FileSourceSpec):
        exec_node = FileDataSourceScanNode.from_node_input(node)
        return Dialect.ARROW, exec_node
    elif isinstance(
        batch_source,
        specs.PushTableSourceSpec,
    ):
        exec_node = PushTableSourceScanNode.from_node_input(node)
        return Dialect.ARROW, exec_node
    elif isinstance(batch_source, specs.SnowflakeSourceSpec):
        return Dialect.SNOWFLAKE, None
    elif isinstance(batch_source, specs.BigquerySourceSpec):
        return Dialect.BIGQUERY, None
    elif isinstance(batch_source, specs.RedshiftSourceSpec):
        return Dialect.ARROW, RedshiftDataSourceScanNode.from_node_input(node)

    msg = f"Unexpected data source type encountered: {batch_source.__class__}"
    raise Exception(msg)


def rewrite_data_sources(plan: NodeRef) -> None:
    """
    Inferring dialect for data source nodes and propagating it to the closest StagingNode.
    There are two kinds of data sources: sql-based and arrow-based.
    For arrow-based sources DataSourceScanNode is replaced with concrete implementation based on source type.
    """
    staging_nodes = get_staging_nodes(plan, QueryTreeStep.DATA_SOURCE, as_ref=True)
    if not staging_nodes:
        return

    for _, staging_node in staging_nodes.items():
        scan_node = get_first_input_node_of_class(staging_node, DataSourceScanNode)
        if not scan_node:
            continue

        dialect, physical_node = get_data_source_dialect_and_physical_node(scan_node)
        if physical_node:
            # replacing DataSourceScanNode
            staging_node.node = attrs.evolve(staging_node.node, dialect=dialect, input_node=physical_node.as_ref())
        else:
            # data source has SQL-based dialect
            # just need to propagate correct dialect to the StagingNode
            staging_node.node = attrs.evolve(staging_node.node, dialect=dialect)


def _rewrite_pandas_pipeline(plan: NodeRef) -> None:
    def traverse(tree: NodeRef) -> None:
        if isinstance(tree.node, FeatureViewPipelineNode):
            pipeline_node = tree.node
            # We don't need to rewrite inputs, because we assume that all inputs are StagingNodes
            assert all(
                isinstance(input_ref.node, StagingNode) for input_ref in pipeline_node.inputs_map.values()
            ), "All inputs to FeatureViewPipelineNode are expected to be StagingNode"

            physical_node = PandasFeatureViewPipelineNode.from_node_inputs(
                query_node=pipeline_node,
                input_node=None,
            )

            tree.node = StagingNode(
                dialect=Dialect.ARROW,
                compute_mode=ComputeMode.RIFT,
                input_node=physical_node.as_ref(),
                staging_table_name=f"pandas_pipeline_{pipeline_node.feature_definition_wrapper.name}",
            )
            return

        for i in tree.inputs:
            traverse(tree=i)

    traverse(plan)


def rewrite_pipeline_nodes(plan: NodeRef) -> None:
    """
    When pipeline mode is "pandas"/"python" the logical node is replaced with PandasFeatureViewPipelineNode + StagingNode.
    The latter is needed to indicate that this should be executed by ArrowCompute.

    In other cases (sql-based transformations): propagate correct dialect to the closest staging node.
    For now, all pipeline nodes are expected to have the same dialect.
    """
    pipeline_dialect = get_pipeline_dialect(plan)
    if pipeline_dialect == Dialect.PANDAS:
        _rewrite_pandas_pipeline(plan)
        return

    if not pipeline_dialect:
        return

    staging_nodes = get_staging_nodes(plan, QueryTreeStep.PIPELINE, as_ref=True)
    for _, staging_node in staging_nodes.items():
        staging_node.node = attrs.evolve(staging_node.node, dialect=pipeline_dialect)


def rewrite_rtfvs(plan: NodeRef) -> None:
    """
    Logical node MultiOdfvPipelineNode is replaced with PandasMultiOdfvPipelineNode,
    which handles both "pandas" and "python" modes.

    If MultiOdfvPipelineNode is succeeded by RenameColsNode it should as well replaced by PandasRenameColsNode
    to minimize switching between Arrow and DuckDB computes.
    """

    def create_physical_odfv_pipeline_node(logical_node: MultiOdfvPipelineNode) -> ArrowExecNode:
        return PandasMultiOdfvPipelineNode.from_node_inputs(logical_node, logical_node.input_node)

    def create_physical_rename_node(logical_node: RenameColsNode, odfv_pipeline_node: NodeRef) -> ArrowExecNode:
        return PandasRenameColsNode.from_node_inputs(logical_node, odfv_pipeline_node)

    def traverse(tree: NodeRef) -> None:
        if isinstance(tree.node, RenameColsNode) and isinstance(tree.node.input_node.node, MultiOdfvPipelineNode):
            tree.node = StagingNode(
                dialect=Dialect.ARROW,
                compute_mode=ComputeMode.RIFT,
                input_node=create_physical_rename_node(
                    tree.node, create_physical_odfv_pipeline_node(tree.node.input_node.node).as_ref()
                ).as_ref(),
                staging_table_name="rtfv_output",
            )
            return

        if isinstance(tree.node, MultiOdfvPipelineNode):
            tree.node = StagingNode(
                dialect=Dialect.ARROW,
                compute_mode=ComputeMode.RIFT,
                input_node=create_physical_odfv_pipeline_node(tree.node).as_ref(),
                staging_table_name="rtfv_output",
            )
            return

        for i in tree.inputs:
            traverse(tree=i)

    traverse(plan)


def rewrite_user_input(plan: NodeRef) -> None:
    """
    UserSpecifiedDataNode is wrapped into StagingNode with Arrow dialect
    to force executor use ArrowCompute and call .to_arrow_reader() instead of .to_sql()
    """

    def traverse(tree: NodeRef) -> None:
        if isinstance(tree.node, UserSpecifiedDataNode):
            tree.node = StagingNode(
                dialect=Dialect.ARROW,
                compute_mode=ComputeMode.RIFT,
                input_node=tree.node.as_ref(),
                staging_table_name=tree.node.data._temp_table_name,
            )
            return

        for i in tree.inputs:
            traverse(tree=i)

    traverse(plan)


def rewrite_embedding_nodes(plan: NodeRef) -> None:
    """
    UserSpecifiedDataNode is wrapped into StagingNode with Arrow dialect
    to force executor use ArrowCompute and call .to_arrow_reader() instead of .to_sql()
    """

    def traverse(tree: NodeRef) -> None:
        if isinstance(tree.node, TextEmbeddingInferenceNode):
            from tecton_core.embeddings.nodes import ArrowExecTextEmbeddingInferenceNode

            tree.node = ArrowExecTextEmbeddingInferenceNode.from_node_input(tree.node)
            return

        for i in tree.inputs:
            traverse(tree=i)

    traverse(plan)


def rewrite_cross_feature_views_joins(plan: NodeRef) -> None:
    """
    Inserts StagingNode with checkpoint=True:
    1) after each feature view's aggregations are calculated and before join with other feature views
    2) in between every N join
        eg, when N is 3 and number of batch feature views is 12, there will be 3 additional checkpoints
        (there should be no checkpoints at the top of the QT)
    """
    if not conf.DUCKDB_ENABLE_CHECKPOINTING.enabled():
        return

    checkpoint_every_n_joins = int(conf.get_or_raise("DUCKDB_CHECKPOINT_EVERY_N_JOIN"))

    def traverse(node_ref: NodeRef, depth: int = 1) -> None:
        if not isinstance(node_ref.node, JoinNode):
            for i in node_ref.inputs:
                traverse(i, depth)
            return

        join_node = node_ref.node
        assert isinstance(join_node, JoinNode)

        # right side of join is next feature view retrieval
        right_branch = join_node.right
        # always staging results of right side
        right_branch = StagingNode(
            right_branch.node.dialect,
            right_branch.node.compute_mode,
            right_branch,
            staging_table_name=f"checkpoint_feature_view_{depth}",
            checkpoint=True,
        ).as_ref()

        # left side of join is the result of previous joins
        left_branch = join_node.left
        if isinstance(left_branch.node, JoinNode) and depth and depth % checkpoint_every_n_joins == 0:
            left_branch = StagingNode(
                left_branch.node.dialect,
                left_branch.node.compute_mode,
                left_branch,
                staging_table_name=f"checkpoint_join_output_{depth}",
                checkpoint=True,
            ).as_ref()

        node_ref.node = attrs.evolve(node_ref.node, right=right_branch, left=left_branch)

        traverse(left_branch, depth=depth + 1)

    traverse(plan)


def logical_plan_to_physical_plan(logical_plan: NodeRef, use_optimized_full_agg: bool = False) -> NodeRef:
    physical_plan = logical_plan.deepcopy()

    # replace some generic nodes with Rift specific
    # ToDo: this can be removed when Athena and Snowflake are removed
    # and the code can be moved to generic nodes
    rewriter = DuckDBTreeRewriter()
    rewriter.rewrite(physical_plan, use_optimized_full_agg)

    rewrite_data_sources(physical_plan)
    rewrite_pipeline_nodes(physical_plan)
    rewrite_rtfvs(physical_plan)
    rewrite_user_input(physical_plan)
    rewrite_embedding_nodes(physical_plan)
    rewrite_cross_feature_views_joins(physical_plan)

    return physical_plan


@attrs.define
class Stage:
    """
    Stage is subtree of a physical plan, where all nodes have the same dialect and thus can be executed in one go
    """

    dialect: Dialect
    output: NodeRef
    inputs: List[NodeRef]
    description: Optional[str] = None


def split_plan_into_stages(plan: NodeRef) -> List[List[Stage]]:
    """
    Split the plan into stages using StagingNodes as splitting points.
    Inputs in each stage, which are StagingNodes in the original plan, are replaced with StagedTableScanNode.

    Run breadth-first traverse over the plan to also split stages into levels. Such that a stage on certain level
    cannot be executed until all stages on the lower level are completed, since they can be inputs to the current stage.
    Stages on the same level, however, can be executed in parallel.

    :return: stages grouped by levels
    """

    def find_inputs(tree: NodeRef, output: StagingNode) -> Iterable[NodeRef]:
        if (
            isinstance(tree.node, StagingNode)
            and tree.node != output
            and (tree.node.dialect != output.dialect or tree.node.checkpoint)
        ):
            # Only staging nodes of different dialect count as input to the current stage
            # or we encountered a staging node with "checkpoint" enabled
            yield tree
            return

        for input_ in tree.inputs:
            yield from find_inputs(input_, output)

    def traverse():
        while True:
            current_level = levels[-1]
            next_level = []

            for stage in current_level:
                for input_ in stage.inputs:
                    next_stage_output = input_.node
                    assert isinstance(next_stage_output, StagingNode)
                    assert next_stage_output.dialect, f"Dialect must be set on StagingNode: {next_stage_output}"
                    next_level.append(
                        Stage(
                            dialect=next_stage_output.dialect,
                            output=next_stage_output.as_ref(),
                            inputs=list(find_inputs(next_stage_output.as_ref(), next_stage_output)),
                            description=next_stage_output.stage_description,
                        )
                    )

                    input_.node = StagedTableScanNode(
                        input_.node.dialect,
                        input_.node.compute_mode,
                        staged_schema=input_.node.output_schema,
                        staging_table_name=input_.node.staging_table_name_unique(),
                    )
            if not next_level:
                return

            levels.append(next_level)

    if not isinstance(plan.node, StagingNode):
        # for simplicity plan should always have StagingNode at the root
        plan = StagingNode(
            dialect=Dialect.DUCKDB,
            compute_mode=ComputeMode.RIFT,
            input_node=plan,
            staging_table_name="",
        ).as_ref()

    levels = [
        [
            Stage(
                dialect=plan.node.dialect,
                output=plan,
                inputs=list(find_inputs(plan, plan.node)),
                description=plan.node.stage_description,
            )
        ]
    ]
    traverse()
    return levels


@attrs.define
class QueryTreeExecutor:
    offline_store_options_providers: Iterable[OfflineStoreOptionsProvider] = DEFAULT_OPTIONS_PROVIDERS
    secret_resolver: Optional[SecretResolver] = None
    model_artifact_provider: Optional[ModelArtifactProvider] = DEFAULT_MODEL_PROVIDER
    monitor: QueryTreeMonitor = DebugOutput()
    is_debug: bool = attrs.field(init=False)
    # TODO: Put duckdb_config in a map when we have more configs for different dialects.
    duckdb_config: Optional[DuckDBConfig] = None
    _dialect_to_compute_map: Dict[Dialect, QueryTreeCompute] = {}
    # Used to track temp tables per dialect so we can clean them up appropriately & avoid re-registering duplicates
    _dialect_to_temp_table_name: Optional[Dict[Dialect, set]] = attrs.field(init=False)

    def __attrs_post_init__(self):
        # TODO(danny): Expose as configs
        self.is_debug = conf.get_bool("DUCKDB_DEBUG")
        self._dialect_to_temp_table_name = None

    @contextlib.contextmanager
    def _monitor_stage(
        self,
        step: str,
        type_: Optional[int] = None,
        dialect: Optional[Dialect] = None,
    ) -> Iterator[ComputeMonitor]:
        assert type_ or dialect, "Either type or dialect must be provided"
        if not type_:
            type_ = get_stage_type_for_dialect(dialect)

        monitor_stage_id = self.monitor.create_stage(type_, step)

        try:
            self.monitor.update_progress(monitor_stage_id, 0)
            yield ComputeMonitor(
                log_progress=lambda p: self.monitor.update_progress(monitor_stage_id, p),
                set_query=lambda q: self.monitor.set_query(monitor_stage_id, q),
            )
        except UserErrors:
            self.monitor.set_failed(monitor_stage_id, user_error=True)
            raise
        except Exception:
            self.monitor.set_failed(monitor_stage_id, user_error=False)
            raise
        else:
            self.monitor.update_progress(monitor_stage_id, 1)
            self.monitor.set_completed(monitor_stage_id)

    def exec_qt(self, logical_plan: NodeRef) -> QueryTreeOutput:
        # Make copy so the execution doesn't mutate the original QT visible to users

        physical_plan = logical_plan_to_physical_plan(
            logical_plan,
            use_optimized_full_agg=should_use_optimized_full_aggregate_node(logical_plan),
        )
        if self.is_debug:
            logger.warning("---------------------------------- Executing overall QT ----------------------------------")
            logger.warning(f"QT: \n{logical_plan.pretty_str()}")
            logger.warning("---------------------------------- Physical plan -----------------------------------------")
            logger.warning(f"QT: \n{physical_plan.pretty_str()}")

        stage_levels = split_plan_into_stages(physical_plan)
        inputs = {}

        # Processing levels from bottom to top
        for stages in reversed(stage_levels):
            inputs = self._process_staging_nodes(stages, inputs)

        return QueryTreeOutput(output=next(iter(inputs.values())))

    def _process_staging_nodes(
        self,
        stages: List[Stage],
        inputs: Dict[str, pyarrow.RecordBatchReader],
    ) -> Dict[str, pyarrow.RecordBatchReader]:
        readers = {}
        for stage in stages:
            assert isinstance(stage.output.node, StagingNode)
            compute = self._get_or_create_compute_by_dialect(stage.dialect, stage.output)

            if self.is_debug:
                logger.warning("---------------------------------- Executing stage ----------------------------------")
                logger.warning(f"QT: \n{stage.output.pretty_str()}")

            input_names = {node_ref.node.staging_table_name for node_ref in stage.inputs}
            stage_inputs = {table: reader for table, reader in inputs.items() if table in input_names}

            with compute:
                name, reader = self._process_staging_node(
                    stage.output.node,
                    inputs=stage_inputs,
                    compute=compute,
                    monitor=None,
                )
            readers[name] = reader
        return readers

    def _process_staging_node(
        self,
        staging_node: StagingNode,
        inputs: Dict[str, pyarrow.RecordBatchReader],
        compute: QueryTreeCompute,
        monitor: ComputeMonitor,
    ) -> Tuple[str, pyarrow.RecordBatchReader]:
        start_time = datetime.now()
        staging_table_name = staging_node.staging_table_name_unique()

        if isinstance(compute, ArrowCompute):
            context = ExecutionContext(
                offline_store_options_providers=self.offline_store_options_providers,
                secret_resolver=self.secret_resolver,
                model_artifact_provider=self.model_artifact_provider,
            )
            reader = compute.run(staging_node.as_ref(), inputs, context, monitor=monitor)
            return staging_table_name, reader

        assert isinstance(compute, SQLCompute)
        for table_name, pa_reader in inputs.items():
            if pa_reader:
                compute.register_temp_table(table_name, pa_reader)

        sql_string = staging_node.with_dialect(compute.get_dialect())._to_staging_query_sql()
        expected_output_schema = staging_node.output_schema if len(staging_node.output_schema) else None
        checkpoint_as = staging_node.staging_table_name_unique() if staging_node.checkpoint else None
        return_dataframe = True if not checkpoint_as else False

        reader = compute.run_sql(
            sql_string,
            return_dataframe=return_dataframe,
            expected_output_schema=expected_output_schema,
            monitor=monitor,
            checkpoint_as=checkpoint_as,
        )

        # Cleaning up checkpointed tables
        checkpointed_inputs = [table for table, reader in inputs.items() if not reader]
        for table_name in checkpointed_inputs:
            compute.unregister_temp_table(table_name)

        staging_done_time = datetime.now()
        if self.is_debug:
            elapsed_staging_time = (staging_done_time - start_time).total_seconds()
            logger.warning(f"STAGE_{staging_table_name}_TIME_SEC: {elapsed_staging_time}")

        return staging_table_name, reader

    def _get_or_create_compute_by_dialect(
        self,
        dialect: Dialect,
        qt_root: Optional[NodeRef] = None,
    ) -> QueryTreeCompute:
        if dialect in self._dialect_to_compute_map:
            return self._dialect_to_compute_map[dialect]

        compute = QueryTreeCompute.for_dialect(dialect, self, qt_root)
        self._dialect_to_compute_map[dialect] = compute
        return compute
