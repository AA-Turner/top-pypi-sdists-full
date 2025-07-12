import logging
import os
import time
from dataclasses import dataclass
from typing import Any
from typing import Dict
from typing import Iterable
from typing import List
from typing import Optional
from typing import Tuple
from typing import Union

import attrs
import pandas
import pyarrow
import pyarrow.dataset


os.environ["RAY_DEDUP_LOGS"] = "0"
import ray
from ray import runtime_context

from tecton_core import conf
from tecton_core import duckdb_factory
from tecton_core import query_consts
from tecton_core import specs
from tecton_core.compute_mode import ComputeMode
from tecton_core.duckdb_factory import DuckDBConfig
from tecton_core.embeddings.model_artifacts import DEFAULT_MODEL_PROVIDER
from tecton_core.embeddings.model_artifacts import ModelArtifactProvider
from tecton_core.errors import TectonInternalError
from tecton_core.offline_store import DEFAULT_OPTIONS_PROVIDERS
from tecton_core.offline_store import OfflineStoreOptionsProvider
from tecton_core.offline_store import get_s3_options_for_fd
from tecton_core.query.data_sources import FileDataSourceScanNode
from tecton_core.query.data_sources import PushTableSourceScanNode
from tecton_core.query.data_sources import RedshiftDataSourceScanNode
from tecton_core.query.dialect import Dialect
from tecton_core.query.duckdb.compute import DuckDBCompute
from tecton_core.query.duckdb.nodes import DeltaOfflineStoreScanNode
from tecton_core.query.duckdb.nodes import IcebergOfflineStoreScanNode
from tecton_core.query.duckdb.rewrite import DuckDBTreeRewriter
from tecton_core.query.errors import UserDefinedTransformationError
from tecton_core.query.executor_params import ExecutionContext
from tecton_core.query.executor_params import QueryTreeStep
from tecton_core.query.executor_utils import DebugOutput
from tecton_core.query.executor_utils import QueryTreeMonitor
from tecton_core.query.node_interface import JoinKeyHashPartitioning
from tecton_core.query.node_interface import JoinKeyRangePartitioning
from tecton_core.query.node_interface import NodeRef
from tecton_core.query.node_interface import Partitioning
from tecton_core.query.node_interface import PartitionSelector
from tecton_core.query.node_interface import SinglePartition
from tecton_core.query.node_utils import get_first_input_node_of_class
from tecton_core.query.node_utils import get_pipeline_dialect
from tecton_core.query.node_utils import get_staging_nodes
from tecton_core.query.node_utils import tree_contains
from tecton_core.query.nodes import AddPartitionColumn
from tecton_core.query.nodes import AsofJoinFullAggNode
from tecton_core.query.nodes import AsofJoinNode
from tecton_core.query.nodes import AsofSecondaryKeyExplodeNode
from tecton_core.query.nodes import DataSourceScanNode
from tecton_core.query.nodes import EntityFilterNode
from tecton_core.query.nodes import FeatureViewPipelineNode
from tecton_core.query.nodes import JoinNode
from tecton_core.query.nodes import MultiOdfvPipelineNode
from tecton_core.query.nodes import OfflineStoreScanNode
from tecton_core.query.nodes import RenameColsNode
from tecton_core.query.nodes import Repartition
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
from tecton_core.query.query_tree_compute import QueryTreeCompute
from tecton_core.query.query_tree_compute import SQLCompute
from tecton_core.query.tecton_ray.dataset import RayDataset
from tecton_core.query.tecton_ray.dataset import TaskResources
from tecton_core.schema_validation import tecton_schema_to_arrow_schema
from tecton_core.secret_management import SecretResolver
from tecton_core.snowflake_context import SnowflakeContext


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
    output: pyarrow.RecordBatchReader

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


def rewrite_offline_scan_node(
    plan: NodeRef, offline_store_options_providers: Iterable[OfflineStoreOptionsProvider]
) -> None:
    staging_nodes = get_staging_nodes(plan, QueryTreeStep.OFFLINE_STORE, as_ref=True)
    if not staging_nodes:
        return

    for _, staging_node in staging_nodes.items():
        offline_scan_node = get_first_input_node_of_class(staging_node, OfflineStoreScanNode)
        if not offline_scan_node:
            continue

        if offline_scan_node.feature_definition_wrapper.has_iceberg_offline_store:
            physical_node = IcebergOfflineStoreScanNode.from_query_node(
                query_node=offline_scan_node,
                offline_store_options_providers=offline_store_options_providers,
            )
            staging_node.node = attrs.evolve(
                staging_node.node,
                input_node=physical_node.as_ref(),
                dialect=Dialect.DUCKDB if conf.get_bool("DUCKDB_OFFLINE_STORE_READ") else Dialect.ARROW,
            )
        elif offline_scan_node.feature_definition_wrapper.has_delta_offline_store and conf.get_bool(
            "DELTA_OFFLINE_STORE_RANGE_PARTITION_ENABLED"
        ):
            physical_node = DeltaOfflineStoreScanNode.from_query_node(
                query_node=offline_scan_node,
                offline_store_options_providers=offline_store_options_providers,
            )

            # if entity_filter is set, means a spine has been provided
            # this is a roundabout optimization for gffe using the Delta offline store.
            # TLDR: Delta offline store uses Pyarrow reader because the DuckDB/Parquet reader is non-performant for many files.
            # As a result of the additional Pyarrow compute, the offline store reader is unaware of the spine.
            # In small spine cases, we end up repartitioning the Delta offline store even for partitions where the spine is empty.
            # By adding an entity filter node, we add an additional pyarrow compute layer that allows us to provide context of the
            # spine to the offline store and only repartition the Delta offline store for the partitions that are not empty.
            # This leads to a significant performance improvement for small spines.
            # Additional details can be found here: https://www.notion.so/tecton/RFC-Performance-in-Rift-how-we-made-DuckDB-even-faster-1ee76e9ad04080d78e1fccfa8ad29c2b?pvs=4#1fc76e9ad04080db8c93d5f4daef9261
            # "Small Spine Optimizations for NDD"
            if offline_scan_node.entity_filter is not None:
                entity_filter = EntityFilterNode(
                    dialect=offline_scan_node.dialect,
                    compute_mode=offline_scan_node.compute_mode,
                    feature_data=physical_node.as_ref(),
                    entities=offline_scan_node.entity_filter,
                    entity_cols=offline_scan_node.feature_definition_wrapper.join_keys,
                )

                staging_node.node = attrs.evolve(
                    staging_node.node,
                    input_node=entity_filter.as_ref(),
                )
            else:
                staging_node.node = attrs.evolve(
                    staging_node.node,
                    input_node=physical_node.as_ref(),
                )


def _rewrite_pandas_pipeline(plan: NodeRef) -> None:
    def traverse(tree: NodeRef) -> None:
        if isinstance(tree.node, FeatureViewPipelineNode):
            pipeline_node = tree.node
            # We don't need to rewrite inputs, because we assume that all inputs are StagingNodes
            assert all(isinstance(input_ref.node, StagingNode) for input_ref in pipeline_node.inputs_map.values()), (
                "All inputs to FeatureViewPipelineNode are expected to be StagingNode"
            )

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


def check_partitioning_compatibility(plan: NodeRef) -> None:
    def get_all_join_nodes(node_ref: NodeRef) -> Iterable[NodeRef]:
        for child in node_ref.inputs:
            yield from get_all_join_nodes(child)

        if isinstance(
            node_ref.node, (JoinNode, AsofJoinNode, AsofJoinFullAggNode, EntityFilterNode, AsofSecondaryKeyExplodeNode)
        ):
            yield node_ref

    def determine_side_to_repartition(
        left: NodeRef, right: NodeRef
    ) -> Tuple[Optional[NodeRef], Optional[Partitioning]]:
        left_partitioning = left.output_partitioning
        right_partitioning = right.output_partitioning

        if (
            left_partitioning
            and right_partitioning
            and (
                left_partitioning.is_equivalent(right_partitioning)
                or (
                    left_partitioning.number_of_partitions == right_partitioning.number_of_partitions
                    and left_partitioning.number_of_partitions == 1
                )
            )
        ):
            return None, None

        left_not_partitioned = left_partitioning is None or isinstance(left_partitioning, SinglePartition)
        right_not_partitioned = right_partitioning is None or isinstance(right_partitioning, SinglePartition)

        # if both side are partitioned
        if not left_not_partitioned and not right_not_partitioned:
            # select the side with fewer partitions to repartition
            # (assuming fewer partitions means less data)
            if left_partitioning.number_of_partitions > right_partitioning.number_of_partitions:
                return right, left_partitioning
            else:
                return left, right_partitioning

        if left_not_partitioned:
            return left, right_partitioning

        return right, left_partitioning

    for join_node in get_all_join_nodes(plan):
        left_input, right_input = join_node.inputs

        repartition_side, partitioning = determine_side_to_repartition(left_input, right_input)
        if not repartition_side:
            continue

        repartition_side.node = RenameColsNode(
            dialect=repartition_side.node.dialect,
            compute_mode=repartition_side.node.compute_mode,
            drop=[query_consts.partition_key()],
            input_node=repartition_side.node.as_ref(),
        )

        repartition_side_input_node = repartition_side.node.input_node
        repartition_attr = Repartition(partitioning=partitioning, key=query_consts.partition_key())

        if (
            isinstance(repartition_side_input_node.node, StagingNode)
            and repartition_side_input_node.node.dialect == Dialect.DUCKDB
        ):
            repartition_side_input_node.node = attrs.evolve(
                repartition_side_input_node.node,
                repartition=repartition_attr,
            )
        else:
            repartition_side_input_node.node = StagingNode(
                dialect=Dialect.DUCKDB,
                compute_mode=ComputeMode.RIFT,
                input_node=repartition_side_input_node.node.as_ref(),
                repartition=repartition_attr,
                staging_table_name="repartition",
            )

        if isinstance(join_node.node, JoinNode):
            partition_by_column = join_node.node.join_cols[0]
        elif isinstance(partitioning, (JoinKeyRangePartitioning, JoinKeyHashPartitioning)):
            partition_by_column = partitioning._join_keys[0]
        else:
            msg = f"Couldn't determine column for partitioning {partitioning}"
            raise RuntimeError(msg)

        staging_input = repartition_side_input_node.node.input_node
        staging_input.node = AddPartitionColumn(
            dialect=staging_input.node.dialect,
            compute_mode=staging_input.node.compute_mode,
            input_node=staging_input.node.as_ref(),
            partition_output_column=query_consts.partition_key(),
            partition_by_column=partition_by_column,
            partition_expr=partitioning.partition_expression,
        )


def logical_plan_to_physical_plan(
    logical_plan: NodeRef,
    use_optimized_full_agg: bool = False,
    offline_store_options_providers: Optional[Iterable[OfflineStoreOptionsProvider]] = None,
) -> NodeRef:
    physical_plan = logical_plan.deepcopy()

    # replace some generic nodes with Rift specific
    # ToDo: this can be removed when Athena and Snowflake are removed
    # and the code can be moved to generic nodes
    rewriter = DuckDBTreeRewriter()
    rewriter.rewrite(physical_plan, use_optimized_full_agg)

    rewrite_data_sources(physical_plan)
    rewrite_offline_scan_node(physical_plan, offline_store_options_providers)
    rewrite_pipeline_nodes(physical_plan)
    rewrite_rtfvs(physical_plan)
    rewrite_user_input(physical_plan)
    rewrite_embedding_nodes(physical_plan)
    check_partitioning_compatibility(physical_plan)

    return physical_plan


def _execute_stage(
    context: ExecutionContext,
    output_node_ref: NodeRef,
    input_nodes_refs: List[NodeRef],
    inputs: List[Union[pyarrow.Table, pyarrow.RecordBatchReader]],
    partition_selector: Optional[PartitionSelector] = None,
    duckdb_home_dir: Optional[str] = None,
    snowflake_connection_params: Optional[Dict[str, Any]] = None,
    return_as_reader: bool = False,  # If True, returns a pyarrow.RecordBatchReader instead of a pyarrow.Table
) -> Union[pyarrow.Table, pyarrow.RecordBatchReader]:
    conf.set("TECTON_OFFLINE_RETRIEVAL_COMPUTE_MODE", "rift")
    conf.set("DUCKDB_ALLOW_CACHE_EXTENSION", "true")

    if duckdb_home_dir:
        duckdb_factory.set_home_dir_override(duckdb_home_dir)

    if snowflake_connection_params:
        SnowflakeContext.set_connection_params(snowflake_connection_params)

    if context.duckdb_config:
        logger.warning(f"Setting task resources {context.duckdb_config}")
    compute = _get_or_create_compute_by_dialect(output_node_ref.node.dialect, context, output_node_ref)

    if isinstance(compute, ArrowCompute):
        if context.duckdb_config:
            pyarrow.set_cpu_count(context.duckdb_config.num_threads)

        reader = compute.run(
            output_node_ref, input_nodes_refs, input_data=inputs, context=context, partition_selector=partition_selector
        )
    elif isinstance(compute, SQLCompute):
        with compute:
            for input_node_ref, input_table in zip(input_nodes_refs, inputs):
                assert isinstance(input_node_ref.node, StagedTableScanNode)

                table_name = input_node_ref.node.staging_table_name
                compute.register_temp_table(table_name, input_table)

            node = output_node_ref.node
            sql_string = node.with_dialect(compute.get_dialect())._to_staging_query_sql(partition_selector)
            expected_output_schema = node.output_schema if node.output_schema and len(node.output_schema) else None

            if isinstance(compute, DuckDBCompute):
                offline_store_scan_node = get_first_input_node_of_class(output_node_ref, OfflineStoreScanNode)
                s3_options = (
                    get_s3_options_for_fd(
                        offline_store_scan_node.feature_definition_wrapper, context.offline_store_options_providers
                    )
                    if offline_store_scan_node
                    and offline_store_scan_node.feature_definition_wrapper.materialized_data_path.startswith("s3")
                    else None
                )

                reader = compute.run_sql(
                    sql_string,
                    return_dataframe=True,
                    expected_output_schema=expected_output_schema,
                    monitor=None,
                    checkpoint_as=None,
                    s3_options=s3_options,
                )
            else:
                reader = compute.run_sql(
                    sql_string,
                    return_dataframe=True,
                    expected_output_schema=expected_output_schema,
                    monitor=None,
                    checkpoint_as=None,
                )
    else:
        msg = f"Unrecognized type of compute: {type(compute)}"
        raise TectonInternalError(msg)

    if return_as_reader:
        return reader
    return reader.read_all()


def _emit_stage_runtime_log(
    func_name: str,
    node_ref_string: NodeRef,
    start_time: time.time,
    end_time: time.time,
    partition_selector: Optional[PartitionSelector] = None,
    dag_depth: Optional[int] = None,
) -> None:
    prefix = partition_selector.as_str() if partition_selector is not None else ""
    if dag_depth is not None:
        prefix += f" (depth: {dag_depth}) - "

    logger.warning(f"{prefix}{func_name}: [{node_ref_string}]  took {end_time - start_time:.2f} secs.")


def find_inputs(input_: NodeRef, output: StagingNode) -> Iterable[NodeRef]:
    if (
        isinstance(input_.node, StagingNode)
        and input_.node != output
        and (input_.node.dialect != output.dialect or input_.node.checkpoint or input_.node.repartition)
    ):
        # Only staging nodes of different dialect count as input to the current stage
        # or we encountered a staging node with "checkpoint" enabled
        yield input_
        return

    for input_ in input_.inputs:
        yield from find_inputs(input_, output)


#### QT LOCAL (aka not ray) MODE
@attrs.define
class Stage:
    """
    Stage is subtree of a physical plan, where all nodes can be executed in one go in the same dialect.
    The dialect is set by the dialect of the StagingNode at the root of the stage.
    """

    dialect: Dialect
    output_node_ref: NodeRef
    input_nodes_refs: List[NodeRef]


def _execute_staging_nodes(
    stages: List[Stage],
    inputs: Dict[str, pyarrow.RecordBatchReader],
    context: ExecutionContext,
) -> Dict[str, pyarrow.RecordBatchReader]:
    """
    Execute a list of stages for a given level, where each stage is a subtree of the query tree.

    Each input node ref is a StagedTableScanNode, and the output node ref of each stage is a StagingNode.
    The output of each stage is a pyarrow.RecordBatchReader which is stored in dict where the key is the staging table name.
    This dict becomes the input for the next level.
    """
    staging_table_name_to_reader = {}
    for idx, stage in enumerate(stages):
        assert isinstance(stage.output_node_ref.node, StagingNode)
        if conf.get_bool("DUCKDB_DEBUG"):
            logger.warning(
                f"---------------------------------- Executing stage {idx + 1} ----------------------------------"
            )
            logger.warning(f"QT: \n{stage.output_node_ref.pretty_str()}")
        stage_inputs = [inputs[node_ref.node.staging_table_name] for node_ref in stage.input_nodes_refs]
        start = time.time()
        result_reader = _execute_stage(
            context=context,
            output_node_ref=stage.output_node_ref,
            input_nodes_refs=stage.input_nodes_refs,
            inputs=stage_inputs,
            partition_selector=None,
            return_as_reader=True,
        )

        if conf.get_bool("DUCKDB_DEBUG"):
            _emit_stage_runtime_log(
                func_name=f"execute_non_dag_stage_{idx + 1}",
                node_ref_string=stage.output_node_ref.as_str(),
                start_time=start,
                end_time=time.time(),
            )
        staging_table_name_to_reader[stage.output_node_ref.node.staging_table_name_unique()] = result_reader
    return staging_table_name_to_reader


def _split_plan_into_levels_for_local_execution(plan: NodeRef) -> List[List[Stage]]:
    """
    Split the plan into stages using StagingNodes as splitting points.

    The query tree is split into stages, where each subtree always has one output node, and this node is always a StagingNode.
    A stage can have from 0 to N inputs, where all input nodes are replaced with a StagedTableScanNode.
    StagedTableScanNode instructs a compute to feed data into a query tree, and StagingNode to offload data from a tree.
    StagingNode's dialect defines what compute (DuckDB/Arrow/Snowflake/etc) will be used to execute a particular stage.

    In addition to splitting the QT into stages, run breadth-first traverse over the plan to also split stages into levels.
    A stage on given level cannot be executed until all stages on the lower level are completed, since they can be inputs to the given stage.
    Stages on the same level, however, can be executed in parallel.

    :return: stages grouped by levels
    """
    assert isinstance(plan.node, StagingNode), "Plan must always start with StagingNode"

    def traverse():
        while True:
            current_level = levels[-1]
            next_level = []

            for stage in current_level:
                for input_ in stage.input_nodes_refs:
                    next_stage_output = input_.node
                    assert isinstance(next_stage_output, StagingNode)
                    assert next_stage_output.dialect, f"Dialect must be set on StagingNode: {next_stage_output}"

                    input_node_refs = list(find_inputs(next_stage_output.as_ref(), next_stage_output))
                    next_level.append(
                        Stage(
                            dialect=next_stage_output.dialect,
                            output_node_ref=next_stage_output.as_ref(),
                            input_nodes_refs=input_node_refs,
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

    levels = [
        [
            Stage(
                dialect=plan.node.dialect,
                output_node_ref=plan,
                input_nodes_refs=list(find_inputs(plan, plan.node)),
            )
        ]
    ]
    traverse()
    return levels


def execute_plan_for_local_execution(
    plan: NodeRef,
    context: ExecutionContext,
    duckdb_home_dir: Optional[str] = None,
    snowflake_connection_params: Optional[Dict[str, Any]] = None,
) -> List[pyarrow.RecordBatchReader]:
    """
    Execute the QT by splitting the plan up into stages and executing each stage sequentially.
    """
    if duckdb_home_dir:
        duckdb_factory.set_home_dir_override(duckdb_home_dir)

    if snowflake_connection_params:
        SnowflakeContext.set_connection_params(snowflake_connection_params)

    stage_levels = _split_plan_into_levels_for_local_execution(plan)
    inputs = {}

    # Processing levels from bottom to top
    for idx, stages in enumerate(reversed(stage_levels)):
        start_time = time.time()
        if conf.get_bool("DUCKDB_DEBUG"):
            logger.warning(
                f"---------------------------------- Executing stage level {idx + 1} (reverse order) -----------------------------"
            )

        inputs = _execute_staging_nodes(stages, inputs, context)
        if conf.get_bool("DUCKDB_DEBUG"):
            _emit_stage_runtime_log(
                func_name=f"execute_plan_for_local_execution_{idx + 1}",
                node_ref_string=f"stage_level_{idx + 1}",
                start_time=start_time,
                end_time=time.time(),
            )

    return [reader for _, reader in inputs.items()]


#### QT PARALLELIZATION MODE
def convert_plan_to_ray_dag(
    node_ref: NodeRef, context: ExecutionContext, dag_depth: Optional[int], **kwargs: Any
) -> RayDataset:
    """
    Split the plan into a RayDataset using StagingNodes as splitting points.

    Inputs in each stage, which are StagingNodes in the original plan, are replaced with StagedTableScanNode.
    Output is a RayDataset where each stage is executed as a Ray task.
    :return: RayDataset
    """
    assert isinstance(node_ref.node, StagingNode), "node_ref must always be a StagingNode"
    inputs = list(find_inputs(node_ref, node_ref.node))

    # if dag_depth is not set, it is the root of the plan
    if dag_depth is None:
        dag_depth = 1
    else:
        dag_depth += 1

    child_ray_datasets = [
        convert_plan_to_ray_dag(
            input_node.node.as_ref(),  # create a copy
            context,
            dag_depth,
            **kwargs,
        )
        for input_node in inputs
    ]

    for input_node_ref in inputs:
        input_node_ref.node = StagedTableScanNode.from_staging_node(
            dialect=input_node_ref.node.dialect, compute_mode=ComputeMode.RIFT, query_node=input_node_ref.node
        )

    # Checking if we're already inside Ray task
    current_task_id = runtime_context.get_runtime_context().get_task_id()
    inside_ray_task = current_task_id is not None

    if (
        not isinstance(node_ref.output_partitioning, SinglePartition)
        or any(not isinstance(child.partitioning, SinglePartition) for child in child_ray_datasets)
        or inside_ray_task
    ):
        # IF at least one of the inputs or current stage is partitioned
        # OR this code is already executed in Ray task (and we just need to propagate resources request)
        # THEN we can run sub-tasks in parallel, and we should allocate resources (possibly configured by user)
        task_resources = (
            TaskResources(
                num_cpus=context.duckdb_config.num_threads, memory_bytes=context.duckdb_config.memory_limit_in_bytes
            )
            if context.duckdb_config
            else TaskResources()
        )
    else:
        # OTHERWISE give the sub-task all available resources
        task_resources = TaskResources.all_available()
        context = attrs.evolve(context, duckdb_config=task_resources.to_duckdb_config())

    node_ref_string = node_ref.as_str()

    if not child_ray_datasets:
        # QT node may have reference to a large spine dataframe
        node_ref_ray_obj = ray.put(node_ref)

        def _partition_generator(partition_selector: PartitionSelector) -> pyarrow.Table:
            start = time.time()
            out = _execute_stage(
                context,
                ray.get(node_ref_ray_obj),
                inputs,
                partition_selector=partition_selector,
                inputs=[],
                **kwargs,
            )
            if conf.get_bool("DUCKDB_DEBUG"):
                _emit_stage_runtime_log(
                    func_name="_partition_generator",
                    dag_depth=dag_depth,
                    node_ref_string=node_ref_string,
                    start_time=start,
                    end_time=time.time(),
                    partition_selector=partition_selector,
                )
            return out

        # This still needs a partition selection
        dataset = RayDataset.from_partition_generator(
            _partition_generator, node_ref.output_partitioning, task_resources
        )

    elif len(child_ray_datasets) == 1:
        input_ray_dataset = child_ray_datasets.pop()

        def _map_fn(partition_selector: PartitionSelector, input_table: pyarrow.Table) -> pyarrow.Table:
            start = time.time()
            if input_table.num_rows == 0:
                if conf.get_bool("DUCKDB_DEBUG"):
                    _emit_stage_runtime_log(
                        func_name="_map_fn",
                        dag_depth=dag_depth,
                        node_ref_string=node_ref_string,
                        start_time=start,
                        end_time=time.time(),
                        partition_selector=partition_selector,
                    )
                output_schema = tecton_schema_to_arrow_schema(node_ref.output_schema)
                return output_schema.empty_table()

            out = _execute_stage(
                context, node_ref, inputs, inputs=[input_table], partition_selector=partition_selector, **kwargs
            )
            if conf.get_bool("DUCKDB_DEBUG"):
                _emit_stage_runtime_log(
                    func_name="_map_fn",
                    dag_depth=dag_depth,
                    node_ref_string=node_ref_string,
                    start_time=start,
                    end_time=time.time(),
                    partition_selector=partition_selector,
                )
            return out

        dataset = input_ray_dataset.map(_map_fn, task_resources)
    else:

        def _co_group_fn(partition_selector: PartitionSelector, *input_tables: Tuple[pyarrow.Table]) -> pyarrow.Table:
            assert len(inputs) == len(input_tables), (
                f"Number of actual inputs doesn't match expected {len(inputs)} != {len(input_tables)}"
            )

            start = time.time()
            out = _execute_stage(
                context, node_ref, inputs, inputs=list(input_tables), partition_selector=partition_selector, **kwargs
            )
            if conf.get_bool("DUCKDB_DEBUG"):
                _emit_stage_runtime_log(
                    func_name="_co_group_fn",
                    dag_depth=dag_depth,
                    node_ref_string=node_ref_string,
                    start_time=start,
                    end_time=time.time(),
                    partition_selector=partition_selector,
                )
            return out

        left = child_ray_datasets[0]
        others = child_ray_datasets[1:]

        dataset = left.co_group(others, _co_group_fn, task_resources)

    repartition = node_ref.node.repartition
    if repartition:
        dataset = dataset.repartition_by(repartition.partitioning, repartition.key)

    return dataset


def _should_use_partitioned_execution(physical_plan: NodeRef) -> bool:
    """
    Determines whether to use partitioned execution (Ray Dag) for the given physical plan.
    """
    return conf.QUERYTREE_ENABLE_PARTITIONED_EXECUTION.enabled() or tree_contains(
        physical_plan, IcebergOfflineStoreScanNode
    )


@attrs.define
class QueryTreeExecutor:
    offline_store_options_providers: Iterable[OfflineStoreOptionsProvider] = DEFAULT_OPTIONS_PROVIDERS
    secret_resolver: Optional[SecretResolver] = None
    model_artifact_provider: Optional[ModelArtifactProvider] = DEFAULT_MODEL_PROVIDER
    monitor: QueryTreeMonitor = attrs.field(factory=DebugOutput)
    is_debug: bool = attrs.field(init=False)
    # TODO: Put duckdb_config in a map when we have more configs for different dialects.
    duckdb_config: Optional[DuckDBConfig] = None

    def __attrs_post_init__(self):
        self.is_debug = conf.get_bool("DUCKDB_DEBUG")

    def exec_qt(self, logical_plan: NodeRef) -> QueryTreeOutput:
        logging_level = "INFO" if self.is_debug else "ERROR"

        # ensure Ray is running
        ray.init(ignore_reinit_error=True, logging_level=logging_level)

        # init connection to download & install extension
        duckdb_factory.create_connection(self.duckdb_config)

        # Make copy so the execution doesn't mutate the original QT visible to users
        physical_plan = logical_plan_to_physical_plan(
            logical_plan,
            use_optimized_full_agg=should_use_optimized_full_aggregate_node(logical_plan),
            offline_store_options_providers=self.offline_store_options_providers,
        )

        if not isinstance(physical_plan.node, StagingNode):
            # for simplicity plan should always have StagingNode at the root
            physical_plan = StagingNode(
                dialect=Dialect.DUCKDB,
                compute_mode=ComputeMode.RIFT,
                input_node=physical_plan,
                staging_table_name="",
            ).as_ref()

        if self.is_debug:
            logger.warning("---------------------------------- Executing overall QT ----------------------------------")
            logger.warning(f"QT: \n{logical_plan.pretty_str()}")
            logger.warning("---------------------------------- Physical plan -----------------------------------------")
            logger.warning(f"QT: \n{physical_plan.pretty_str()}")

        context = ExecutionContext(
            offline_store_options_providers=self.offline_store_options_providers,
            secret_resolver=self.secret_resolver,
            model_artifact_provider=self.model_artifact_provider,
            duckdb_config=self.duckdb_config,
        )

        if _should_use_partitioned_execution(physical_plan):
            if self.is_debug:
                logger.info("Executing QT using Ray + partitioned execution")

            ray_dataset = convert_plan_to_ray_dag(
                physical_plan,
                context,
                duckdb_home_dir=os.environ.get("TEST_TMPDIR"),
                snowflake_connection_params=SnowflakeContext.get_instance().get_connection_params()
                if SnowflakeContext.is_initialized()
                else None,
                dag_depth=None,
            )
            outputs = ray_dataset.execute()
        else:
            if self.is_debug:
                logger.info("Executing QT locally (aka without ray)")
            output_list = execute_plan_for_local_execution(
                physical_plan,
                context,
                duckdb_home_dir=os.environ.get("TEST_TMPDIR"),
                snowflake_connection_params=SnowflakeContext.get_instance().get_connection_params()
                if SnowflakeContext.is_initialized()
                else None,
            )
            outputs = next(iter(output_list))

        return QueryTreeOutput(output=outputs)


_dialect_to_compute_map = {}


def _get_or_create_compute_by_dialect(
    dialect: Dialect,
    context: ExecutionContext,
    qt_root: Optional[NodeRef] = None,
) -> QueryTreeCompute:
    if dialect in _dialect_to_compute_map:
        return _dialect_to_compute_map[dialect]

    compute = QueryTreeCompute.for_dialect(dialect, context, qt_root)
    _dialect_to_compute_map[dialect] = compute
    return compute
