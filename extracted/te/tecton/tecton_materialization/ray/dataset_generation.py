import json
import logging
import multiprocessing
import os
import uuid
from pathlib import Path
from typing import List
from typing import Union

import attrs
import boto3
import pyarrow
import pyarrow.dataset
import pyarrow.fs
import pyarrow.parquet as pq


os.environ["RAY_DEDUP_LOGS"] = "0"
import ray
from pyarrow._dataset import WrittenFile

from tecton_core import conf
from tecton_core import duckdb_factory
from tecton_core import offline_store
from tecton_core.arrow import PARQUET_WRITE_OPTIONS
from tecton_core.compute_mode import ComputeMode
from tecton_core.data_processing_utils import pyarrow_split_spine
from tecton_core.duckdb_factory import DuckDBConfig
from tecton_core.offline_store import DATASET_PARTITION_SIZE
from tecton_core.query.dialect import Dialect
from tecton_core.query.executor_params import QueryTreeStep
from tecton_core.query.node_interface import NodeRef
from tecton_core.query.nodes import PyarrowDataframeWrapper
from tecton_core.query.nodes import StagingNode
from tecton_core.query.query_tree_executor import QueryTreeExecutor
from tecton_core.query.retrieval_params import GetFeaturesForEventsParams
from tecton_core.query.retrieval_params import GetFeaturesInRangeParams
from tecton_core.query.rewrite import rewrite_tree_for_spine
from tecton_core.query_consts import valid_to
from tecton_materialization.common.dataset_generation import get_features_from_params
from tecton_materialization.common.job_metadata import JobMetadataClient
from tecton_materialization.common.task_params import feature_definition_from_feature_service_task_params
from tecton_materialization.common.task_params import feature_definition_from_task_params
from tecton_materialization.common.task_params import get_features_params_from_task_params
from tecton_materialization.ray.delta import DeltaWriter
from tecton_materialization.ray.delta import OfflineStoreParams
from tecton_materialization.ray.delta import write
from tecton_materialization.ray.job_status import JobStatusClient
from tecton_materialization.ray.materialization_utils import get_delta_writer
from tecton_materialization.ray.materialization_utils import get_secret_resolver
from tecton_materialization.ray.nodes import AddTimePartitionNode
from tecton_materialization.ray.nodes import TimeSpec
from tecton_proto.materialization.materialization_task__client_pb2 import DatasetGenerationParameters
from tecton_proto.materialization.params__client_pb2 import MaterializationTaskParams
from tecton_proto.materialization.params__client_pb2 import SecretMaterializationTaskParams
from tecton_proto.offlinestore.delta import transaction_writer__client_pb2 as transaction_writer_pb2


# fewer threads means more memory per thread
DEFAULT_NUM_THREADS = multiprocessing.cpu_count() // 2

DEFAULT_SPINE_SPLIT_DIR_STR = "/tmp/spine_split"
# Default output buffer dir for storing output results before uploading to S3 Delta table.
DEFAULT_OUTPUT_BUFFER_DIR_STR = "/tmp/output_buffer"
# Default chunk size for merging and uploading output files to S3 Delta table.
DEFAULT_OUTPUT_CHUNK_SIZE = 30

# With the default setting, a m5.2xlarge instance(8 cpu, 32G memory) can run 4 subtasks in parallel.
# Worth noting that by default only 70% of memory (32G*0.7=~22G) can be used by Ray subtasks.
DEFAULT_RAY_THREAD_CPU = 2
DEFAULT_RAY_THREAD_MEMORY_IN_BYTES = 5 * 1024 * 1024 * 1024  # 5G


logger = logging.getLogger(__name__)


def run_dataset_generation(
    materialization_task_params: MaterializationTaskParams,
    secret_materialization_task_params: SecretMaterializationTaskParams,
    job_status_client: JobStatusClient,
):
    # retrieve current region
    conf.set("CLUSTER_REGION", boto3.Session().region_name)
    conf.set("DUCKDB_NTHREADS", DEFAULT_NUM_THREADS)

    assert materialization_task_params.dataset_generation_task_info.HasField("dataset_generation_parameters")
    dataset_generation_params = materialization_task_params.dataset_generation_task_info.dataset_generation_parameters
    params = get_features_params_from_task_params(materialization_task_params, compute_mode=ComputeMode.RIFT)

    config_overrides = json.loads(dataset_generation_params.extra_config.get("tecton_config", "{}"))
    for k, v in config_overrides.items():
        conf.set(k, v)

    store_params = OfflineStoreParams(
        feature_view_id=params.fco.id,
        feature_view_name=params.fco.name,
        schema=dataset_generation_params.expected_schema,
        time_spec=None,
        feature_store_format_version=None,
        batch_schedule=None,
    )

    writer = get_delta_writer(
        materialization_task_params,
        store_params=store_params,
        table_uri=dataset_generation_params.result_path,
        join_keys=params.join_keys,
        partition_type=offline_store.PartitionType.NONE,
    )

    if not use_legacy_spine_split(dataset_generation_params):
        logger.info("Using QT parallelization for dataset generation")
        run_dataset_generation_with_qt_parallelization(
            secret_materialization_task_params,
            dataset_generation_params,
            job_status_client,
            params,
            writer,
        )
    else:
        logger.info("Using Ray threads for dataset generation")
        run_dataset_generation_with_enforced_spine_splitting(
            materialization_task_params,
            secret_materialization_task_params,
            dataset_generation_params,
            job_status_client,
            params,
            writer,
        )
    logger.info(f"Dataset generation for dataset_name={dataset_generation_params.dataset_name} completed.")


def use_legacy_spine_split(dataset_generation_params: DatasetGenerationParameters) -> bool:
    # Whether to use legacy spine splitting or or qt parallelizatio for RDG.
    use_spine_split = str(dataset_generation_params.extra_config.get("use_legacy_spine_split", "true")).lower()
    return use_spine_split == "true"


def run_dataset_generation_with_enforced_spine_splitting(
    materialization_task_params: MaterializationTaskParams,
    secret_materialization_task_params: SecretMaterializationTaskParams,
    dataset_generation_params: DatasetGenerationParameters,
    job_status_client: JobStatusClient,
    params: Union[GetFeaturesInRangeParams, GetFeaturesForEventsParams],
    writer: DeltaWriter,
):
    if "ray_thread_cpu" in dataset_generation_params.extra_config:
        cpu_per_task = int(dataset_generation_params.extra_config["ray_thread_cpu"])
    else:
        cpu_per_task = DEFAULT_RAY_THREAD_CPU

    if "ray_thread_memory_in_bytes" in dataset_generation_params.extra_config:
        memory_per_task_in_bytes = int(dataset_generation_params.extra_config["ray_thread_memory_in_bytes"])
    else:
        memory_per_task_in_bytes = DEFAULT_RAY_THREAD_MEMORY_IN_BYTES

    target_scanned_offline_rows_per_partition = None
    if "target_scanned_offline_rows_per_partition" in dataset_generation_params.extra_config:
        target_scanned_offline_rows_per_partition = int(
            dataset_generation_params.extra_config.get("target_scanned_offline_rows_per_partition")
        )

    tasks = []
    qt_prep_monitor = job_status_client.create_stage_monitor(
        "Prepare query tree and Ray tasks",
    )
    with qt_prep_monitor():
        if isinstance(params, GetFeaturesForEventsParams):
            time_column = params.timestamp_key
            spine_data = _load_user_provided_data(params.events)
            spine_split_tables = pyarrow_split_spine(
                spine_data,
                params.join_keys,
                _extract_fdw_list(materialization_task_params),
                time_column,
                target_scanned_offline_rows_per_partition,
            )
            spine_split_files = write_split_tables_to_files(spine_split_tables)
            num_tasks = len(spine_split_files)
            for idx, spine_split_file in enumerate(spine_split_files):
                spine_chunk = read_table_from_file(spine_split_file)
                logger.info(
                    f"Creating Ray task {idx} for dataset generation: num_cpus={cpu_per_task} memory={memory_per_task_in_bytes}"
                )
                tasks.append(
                    run_one_dataset_generation_ray_task.options(
                        num_cpus=cpu_per_task, memory=memory_per_task_in_bytes
                    ).remote(
                        idx,
                        num_tasks,
                        spine_chunk,
                        time_column,
                        materialization_task_params,
                        secret_materialization_task_params,
                        os.environ.get("TEST_TMPDIR", None),
                        cpu_per_task,
                        memory_per_task_in_bytes,
                    )
                )
        elif isinstance(params, GetFeaturesInRangeParams):
            time_column = valid_to()
            idx = 0
            num_tasks = 1  # Adjust if needed for parallelism
            tasks.append(
                run_one_dataset_generation_ray_task.options(
                    num_cpus=cpu_per_task, memory=memory_per_task_in_bytes
                ).remote(
                    idx,
                    num_tasks,
                    None,  # No spine chunk needed
                    time_column,
                    materialization_task_params,
                    secret_materialization_task_params,
                    os.environ.get("TEST_TMPDIR", None),
                    cpu_per_task,
                    memory_per_task_in_bytes,
                )
            )
        else:
            error = f"Unsupported params type: {type(params)}"
            raise ValueError(error)

    upload_tasks = []
    qt_exec_monitor = job_status_client.create_stage_monitor(
        f"Execute {len(tasks)} query task(s)",
    )
    with qt_exec_monitor():
        remaining_tasks = tasks
        while remaining_tasks:
            ready_tasks, remaining_tasks = ray.wait(
                remaining_tasks, num_returns=min(DEFAULT_OUTPUT_CHUNK_SIZE, len(remaining_tasks)), timeout=None
            )

            files_list = ray.get(ready_tasks)
            local_files_list = []
            for sublist in files_list:
                local_files_list.extend(sublist)

            upload_tasks.append(
                upload_to_delta_table.options(num_cpus=cpu_per_task, memory=memory_per_task_in_bytes).remote(
                    local_files_list, dataset_generation_params.result_path, params.join_keys
                )
            )

    write_monitor = job_status_client.create_stage_monitor(
        "Upload files to dataset location",
    )
    with write_monitor():
        files_list = ray.get(upload_tasks)

        # Each Ray task returns a list of AddFile objects. We need to commit all of them to the Delta table.
        files = [file for sublist in files_list for file in sublist]
        writer.add_files(files)
        writer.commit()


@ray.remote
def run_one_dataset_generation_ray_task(
    idx,
    num_tasks,
    spine_chunk,
    time_column,
    materialization_task_params,
    secret_materialization_task_params,
    test_tmpdir,
    cpu_per_task,
    memory_per_task_in_bytes,
) -> List[transaction_writer_pb2.AddFile]:
    logger.info(f"Running dataset generation with Ray task {idx} of {num_tasks}")

    # All these confs are set within the ray task and do not affect the top-level session.
    conf.set("DUCKDB_DEBUG", "true")
    conf.set("TECTON_OFFLINE_RETRIEVAL_COMPUTE_MODE", "rift")
    conf.set("TECTON_RUNTIME_MODE", "MATERIALIZATION")
    conf.set("DELTA_OFFLINE_STORE_RANGE_PARTITION_ENABLED", "false")
    conf.set(conf.QUERYTREE_ENABLE_PARTITIONED_EXECUTION.key, "false")

    if test_tmpdir:
        duckdb_factory.set_home_dir_override(test_tmpdir)

    pyarrow.set_cpu_count(cpu_per_task)

    job_status_client = JobStatusClient(JobMetadataClient.for_params(materialization_task_params))
    job_status_client.set_query_index(idx, num_tasks)
    secret_resolver = get_secret_resolver(secret_materialization_task_params.secret_service_params)
    executor = QueryTreeExecutor(
        monitor=job_status_client,
        secret_resolver=secret_resolver,
        duckdb_config=DuckDBConfig(
            num_threads=cpu_per_task,
            memory_limit_in_bytes=memory_per_task_in_bytes,
            use_unique_extension_path=False,
        ),
    )
    params = get_features_params_from_task_params(materialization_task_params, compute_mode=ComputeMode.RIFT)
    if isinstance(params, GetFeaturesForEventsParams):
        qt = get_features_from_params(params, spine=PyarrowDataframeWrapper(spine_chunk))
    elif isinstance(params, GetFeaturesInRangeParams):
        entities = PyarrowDataframeWrapper(pq.read_table(params.entities)) if params.entities is not None else None
        qt = get_features_from_params(params, entities=entities)
    else:
        error = f"Unsupported params type: {type(params)}"
        raise ValueError(error)

    rewrite_tree_for_spine(qt)
    reader = executor.exec_qt(qt).result_table
    return write_to_tmp_buffer_table(reader)


def write_to_delta_table(
    reader: Union[pyarrow.Table, pyarrow.RecordBatchReader],
    table_uri: str,
    join_keys: List[str],
) -> List[transaction_writer_pb2.AddFile]:
    fs, base_path = pyarrow.fs.FileSystem.from_uri(table_uri)
    partitioning = pyarrow.dataset.partitioning(
        pyarrow.schema([(offline_store.TIME_PARTITION, pyarrow.string())]), flavor="hive"
    )
    return write(reader, base_path, table_uri, join_keys, fs, partitioning)


def _load_user_provided_data(path: str) -> pyarrow.Table:
    spine = pq.read_table(path)
    logger.info(f"Reading spine with shape {spine.shape} and memory usage {spine.nbytes}")
    logger.info(f"Spine schema:\n{spine.schema}")
    return spine


def run_dataset_generation_with_qt_parallelization(
    secret_materialization_task_params: SecretMaterializationTaskParams,
    dataset_generation_params: DatasetGenerationParameters,
    job_status_client: JobStatusClient,
    params: Union[GetFeaturesInRangeParams, GetFeaturesForEventsParams],
    writer: DeltaWriter,
):
    # Turn on qt parallelization for the query tree executor
    conf.set("DELTA_OFFLINE_STORE_RANGE_PARTITION_ENABLED", "true")
    conf.set(conf.QUERYTREE_ENABLE_PARTITIONED_EXECUTION.key, "true")

    if "ray_thread_cpu" in dataset_generation_params.extra_config:
        cpu_per_task = int(dataset_generation_params.extra_config["ray_thread_cpu"])
    else:
        cpu_per_task = DEFAULT_RAY_THREAD_CPU

    if "ray_thread_memory_in_bytes" in dataset_generation_params.extra_config:
        memory_per_task_in_bytes = int(dataset_generation_params.extra_config["ray_thread_memory_in_bytes"])
    else:
        memory_per_task_in_bytes = DEFAULT_RAY_THREAD_MEMORY_IN_BYTES

    duckdb_config = DuckDBConfig(
        num_threads=cpu_per_task,
        memory_limit_in_bytes=memory_per_task_in_bytes,
        use_unique_extension_path=False,
    )
    duckdb_factory.create_connection(duckdb_config)  # init connection to download & install extension

    secret_resolver = get_secret_resolver(secret_materialization_task_params.secret_service_params)
    executor = QueryTreeExecutor(
        monitor=job_status_client,
        secret_resolver=secret_resolver,
        duckdb_config=duckdb_config,
    )

    qt_prep_monitor = job_status_client.create_stage_monitor(
        "Prepare query tree",
    )
    with qt_prep_monitor():
        if isinstance(params, GetFeaturesForEventsParams):
            time_column = params.timestamp_key
            spine_data = _load_user_provided_data(params.events)

            qt = get_features_from_params(params, spine=PyarrowDataframeWrapper(spine_data))
        elif isinstance(params, GetFeaturesInRangeParams):
            time_column = valid_to()
            entities = (
                PyarrowDataframeWrapper(_load_user_provided_data(params.entities))
                if params.entities is not None
                else None
            )
            qt = get_features_from_params(params, entities=entities)
        else:
            error = f"Unsupported params type: {type(params)}"
            raise ValueError(error)
        rewrite_tree_for_spine(qt)

    qt_exec_monitor = job_status_client.create_stage_monitor(
        "Execute query tree",
    )
    with qt_exec_monitor():
        reader = executor.exec_qt(qt).result_table

    write_monitor = job_status_client.create_stage_monitor(
        "Compute and upload dataset",
    )
    with write_monitor():
        writer.write(reader)

    writer.commit()


def _extract_fdw_list(materialization_task_params: MaterializationTaskParams):
    if materialization_task_params.HasField("feature_view"):
        fdw_list = [feature_definition_from_task_params(materialization_task_params)]
    else:
        fdw_list = feature_definition_from_feature_service_task_params(materialization_task_params)
    return fdw_list


def _add_partition_column(qt: NodeRef, time_column) -> NodeRef:
    """
    Injects AddTimePartitionNode either before StagingNode(step=AGGREGATION) or at the top of the tree.
    The aim is to run this node before ODFV (if it is present) to make it part of DuckDB query.
    """

    def create_node(input_node: NodeRef) -> NodeRef:
        return AddTimePartitionNode(
            dialect=Dialect.DUCKDB,
            compute_mode=ComputeMode.RIFT,
            input_node=input_node,
            time_spec=TimeSpec(
                timestamp_key=time_column,
                time_column=time_column,
                partition_size=DATASET_PARTITION_SIZE,
                partition_is_anchor=False,
            ),
        ).as_ref()

    def inject(tree: NodeRef) -> bool:
        """
        Traverse over the tree and return True if AddTimePartitionNode was injected before StagingNode(step=AGGREGATION)
        """
        injected = False

        if isinstance(tree.node, StagingNode) and QueryTreeStep.AGGREGATION == tree.node.query_tree_step:
            prev_input = tree.node.input_node
            new_input = create_node(prev_input)
            tree.node = attrs.evolve(tree.node, input_node=new_input)
            injected = True

        return injected or any(inject(tree=i) for i in tree.inputs)

    if inject(qt):
        return qt

    # add node at the top
    return create_node(qt)


def write_split_tables_to_files(split_tables: List[pyarrow.Table]) -> List[Path]:
    # Generate a unique directory name
    split_dir = Path(f"{DEFAULT_SPINE_SPLIT_DIR_STR}_{uuid.uuid4()}")
    split_dir.mkdir(exist_ok=True)

    # Write each split table to a file using Arrow IPC format, which has a better performance than Parquet for Inter Process Communication.
    split_files = []
    for table in split_tables:
        file_path = split_dir / f"split_{uuid.uuid4()}.arrow"
        with pyarrow.ipc.RecordBatchFileWriter(str(file_path), table.schema) as writer:
            writer.write_table(table)
        split_files.append(file_path)

    return split_files


def read_table_from_file(file_path: Path) -> pyarrow.Table:
    if not file_path.exists():
        msg = f"File not found: {file_path}"
        raise FileNotFoundError(msg)

    with pyarrow.ipc.RecordBatchFileReader(str(file_path)) as reader:
        table = reader.read_all()

    return table


def write_to_tmp_buffer_table(
    reader: Union[pyarrow.Table, pyarrow.RecordBatchReader],
) -> List[Path]:
    adds = []
    failed = False

    def local_visit_file(f: WrittenFile):
        try:
            adds.append(Path(f.path))
        except Exception as e:
            # Log and raise exceptions for debugging
            nonlocal failed
            failed = True
            raise e

    pyarrow.dataset.write_dataset(
        data=reader,
        filesystem=pyarrow.fs.LocalFileSystem(),
        base_dir=DEFAULT_OUTPUT_BUFFER_DIR_STR,
        format=pyarrow.dataset.ParquetFileFormat(),
        file_options=PARQUET_WRITE_OPTIONS,
        basename_template=f"{uuid.uuid4()}-part-{{i}}.parquet",
        file_visitor=local_visit_file,
        existing_data_behavior="overwrite_or_ignore",
    )

    if failed:
        msg = "file visitor failed"
        raise Exception(msg)

    return adds


@ray.remote
def upload_to_delta_table(file_list, result_path, join_keys):
    dataset = pyarrow.dataset.dataset(file_list, format=pyarrow.dataset.ParquetFileFormat())
    reader = dataset.scanner().to_reader()

    output_files = write_to_delta_table(reader, result_path, join_keys)

    for file_path in file_list:
        os.remove(file_path)

    return output_files
