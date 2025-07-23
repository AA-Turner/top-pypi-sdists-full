import itertools
import logging
import multiprocessing
import time
import typing
from os import environ
from typing import Optional

import attrs
import pyarrow


environ["RAY_DEDUP_LOGS"] = "0"
import ray

from tecton_core import conf
from tecton_core.data_processing_utils import sort_pyarrow_table_using_duckdb
from tecton_core.duckdb_factory import DuckDBConfig
from tecton_core.errors import TectonInternalError
from tecton_core.query.node_interface import EmptyPartition
from tecton_core.query.node_interface import Partitioning
from tecton_core.query.node_interface import PartitionSelector


logger = logging.getLogger(__name__)

PROPAGATE_ENV_VARS = (
    "DUCKDB_EXTENSION_REPO",
    "DUCKDB_DEBUG",
    "QUERYTREE_VERBOSE",
    "TECTON_DEBUG",
    "SNOWFLAKE_USER",
    "SNOWFLAKE_PASSWORD",
    "SNOWFLAKE_PRIVATE_KEY",
    "REDSHIFT_USER",
    "REDSHIFT_PASSWORD",
    "GOOGLE_APPLICATION_CREDENTIALS",
    "OVERRIDE_CUSTOM_MODEL_PATHS",
    "CLUSTER_REGION",
    # We need the Auth credentials here in order to retrieve temp s3 credentials from GetOfflineStoreCredentials.
    "API_SERVICE",
    "TECTON_API_KEY",
    "OAUTH_ACCESS_TOKEN",
    "OAUTH_ACCESS_TOKEN_EXPIRATION",
    "OAUTH_REFRESH_TOKEN",
)


def _get_runtime() -> typing.Dict[str, typing.Any]:
    env_vars = {}
    for var in PROPAGATE_ENV_VARS:
        try:
            val = conf.get_or_none(var)
        except TectonInternalError:
            val = environ.get(var)

        if not val:
            continue
        env_vars[var] = str(val)  # Values must be str to be passed to env

    if conf.get_bool("DUCKDB_DEBUG"):
        logger.warning(f"Configuring Env vars for Ray tasks: {env_vars.keys()}")

    return {"env_vars": env_vars}


@ray.remote
def _write_fragments(input_: pyarrow.Table, partition_key: str, target_partitions: int) -> typing.List[pyarrow.Table]:
    """
    This is the write part of the repartitioning operation.
    For each input partition this function creates N fragments, where N equals to number of target (output) partitions.

    Fragments are smaller pieces of data created by splitting each input partition. These fragments
    will later be recombined by the _read_fragments function to create the final output partitions.
    This approach enables redistributing data across a different number of partitions.

    Example:
        Repartitioning from 3 partitions to 4 partitions:
            Input partitions: p0, p1, p2
            Fragments: p0_0, p0_1, p0_2, p0_3, p1_0, p1_1, p1_2, p1_3, p2_0, p2_1, p2_2, p2_3 (total 3 * 4 fragments)
            Output partitions will be compiled from fragments by `_read_fragments` task:
                p0: [p0_0, p1_0, p2_0]
                p1: [p0_1, p1_1, p2_1]
                p2: [p0_2, p1_2, p2_2]
                p3: [p0_3, p1_3, p2_3]
    """
    input_sorted = sort_pyarrow_table_using_duckdb(input_, [partition_key])

    count_per_partition = input_sorted.group_by(partition_key).aggregate([(partition_key, "count")]).to_pylist()
    count_per_partition = sorted(count_per_partition, key=lambda r: r[partition_key])
    cumsum = 0
    slices = {}
    for row in count_per_partition:
        partition = row[partition_key]
        count = row[f"{partition_key}_count"]
        slices[partition] = (cumsum, count)
        cumsum += count

    return [
        input_sorted.slice(offset=slices[index][0], length=slices[index][1])
        if index in slices
        else input_.schema.empty_table()
        for index in range(target_partitions)
    ]


@ray.remote
def _read_fragments(*inputs: typing.List[pyarrow.Table]) -> pyarrow.Table:
    """
    Read part of the repartitioning operation.
    Merges fragments into output partition.
    See _write_fragments task
    """
    return pyarrow.concat_tables(inputs).combine_chunks()


@attrs.define
class TaskResources:
    num_cpus: float = attrs.field(factory=lambda: min(2, ray.available_resources().get("CPU", 1)))
    memory_bytes: int = attrs.field(factory=lambda: min(1_000_000_000, int(ray.available_resources().get("memory", 0))))

    def to_options(self):
        return {"num_cpus": self.num_cpus, "memory": self.memory_bytes}

    @classmethod
    def all_available(cls):
        available = ray.available_resources()
        return TaskResources(
            num_cpus=max(int(available.get("CPU", multiprocessing.cpu_count())) - 1, 1),
            memory_bytes=int(available.get("memory", 0)),
        )

    def to_duckdb_config(self):
        return DuckDBConfig(num_threads=int(self.num_cpus), memory_limit_in_bytes=self.memory_bytes)


class DAGNode:
    def __init__(self, args):
        self._args = args

    def execute(self):
        return self._execute_recursively()

    def _execute_recursively(self):
        evaluated_args = [arg._execute_recursively() if isinstance(arg, DAGNode) else arg for arg in self._args]

        return self._execute_impl(evaluated_args)

    def _execute_impl(self, args):
        raise NotImplementedError


class FunctionNode(DAGNode):
    def __init__(self, remote_fun, *args, **kwargs):
        self._remote_fun = remote_fun
        super().__init__(*args, **kwargs)

    def _execute_impl(self, args):
        # Unlike Ray's DAG implementation, this simplified version:
        # 1. Doesn't cache execution outputs
        # 2. Doesn't rewrite the DAG on-the-fly
        # 3. Doesn't copy node instances
        # This avoids potential memory leaks from accumulated cached results
        # or orphaned node references
        return self._remote_fun.remote(*args)


@attrs.define
class RayDataset:
    partitions: typing.List[DAGNode]
    partitioning: Partitioning
    resources: TaskResources

    @classmethod
    def from_partition_generator(
        cls,
        fun: typing.Callable[[PartitionSelector], pyarrow.Table],
        partitioning: Partitioning,
        resources: Optional[TaskResources] = None,
    ) -> "RayDataset":
        partitions = []
        resources = resources or TaskResources()
        remote_fun = ray.remote(fun).options(
            runtime_env=_get_runtime(), **resources.to_options(), retry_exceptions=True
        )
        for p in range(partitioning.number_of_partitions):
            partitions.append(
                FunctionNode(remote_fun, args=[PartitionSelector([p], partitioning.number_of_partitions)])
            )

        return cls(partitions, partitioning, resources)

    def map(
        self,
        fun: typing.Callable[[PartitionSelector, pyarrow.Table], pyarrow.Table],
        resources: Optional[TaskResources] = None,
    ) -> "RayDataset":
        output_partitions = []
        resources = resources or TaskResources()
        remote_fun = ray.remote(fun).options(
            runtime_env=_get_runtime(), **resources.to_options(), retry_exceptions=True
        )
        for partition_idx, input_partition in enumerate(self.partitions):
            output_partitions.append(
                FunctionNode(
                    remote_fun, args=[PartitionSelector([partition_idx], len(self.partitions)), input_partition]
                )
            )

        return RayDataset(output_partitions, self.partitioning, resources)

    def repartition_by(
        self,
        new_partitioning: Partitioning,
        partition_column: str,
    ) -> "RayDataset":
        write_branches = []
        _write_fragments_with_options = _write_fragments.options(
            num_returns=new_partitioning.number_of_partitions,
            runtime_env=_get_runtime(),
            **TaskResources().to_options(),
        )
        for input_partition in self.partitions:
            write_branches.append(
                FunctionNode(
                    _write_fragments_with_options,
                    args=[input_partition, partition_column, new_partitioning.number_of_partitions],
                )
            )

        fragment_batches = _execute_in_batches(write_branches, self._parallelization_level)
        fragments = [f for batch in fragment_batches for f in batch]
        output_partitions = []
        _read_fragments_with_options = _read_fragments.options(runtime_env=_get_runtime())
        transposed_fragments = (
            [list(row) for row in zip(*fragments)] if new_partitioning.number_of_partitions > 1 else [fragments]
        )
        for output_partition_fragments in transposed_fragments:
            ray.wait(output_partition_fragments, num_returns=len(output_partition_fragments))

            output_partitions.append(FunctionNode(_read_fragments_with_options, args=output_partition_fragments))

        return RayDataset(output_partitions, new_partitioning, TaskResources())

    def co_group(
        self,
        others: typing.Union[typing.List["RayDataset"], "RayDataset"],
        fun: typing.Callable[[PartitionSelector, pyarrow.Table, pyarrow.Table], pyarrow.Table],
        resources: Optional[TaskResources] = None,
    ) -> "RayDataset":
        resources = resources or TaskResources()

        if isinstance(others, RayDataset):
            others = [others]

        assert all(self.partitioning.is_equivalent(other.partitioning) for other in others), (
            f"Partitioning must match for all datasets. Actual: {[self.partitioning, *[o.partitioning for o in others]]}"
        )
        output_partitions = []
        remote_fun = ray.remote(fun).options(
            runtime_env=_get_runtime(), **resources.to_options(), retry_exceptions=True
        )

        for partition_idx, co_partitions in enumerate(zip(*[self.partitions, *[other.partitions for other in others]])):
            output_partitions.append(
                FunctionNode(
                    remote_fun, args=[PartitionSelector([partition_idx], len(self.partitions)), *co_partitions]
                )
            )

        return RayDataset(output_partitions, self.partitioning, resources)

    @property
    def _parallelization_level(self):
        # Parallelization level controls how many partitions are executed in parallel.
        # This impacts how much of intermediate storage (Ray plasma) we would need, since each partition writes to it.
        return max(
            int(max(ray.available_resources().get("CPU", multiprocessing.cpu_count()), 1) // self.resources.num_cpus), 1
        )

    def execute(self) -> pyarrow.RecordBatchReader:
        if conf.get_bool("DUCKDB_DEBUG"):
            logger.warning(f"Available resources: {ray.available_resources()}")
            logger.warning(f"Dataset requested resources: {self.resources}")
            logger.warning(f"Executing {len(self.partitions)} with {self._parallelization_level} parallelization level")

        partition_batches = _execute_in_batches(self.partitions, self._parallelization_level)

        # need to find first non-empty result to extract schema
        while True:
            try:
                first_batch_with_result = next(partition_batches)
            except StopIteration:
                msg = "Execution returned empty result"
                raise RuntimeError(msg)

            table = _first_non_empty_result(first_batch_with_result)
            if table is not None:
                schema = table.schema
                break

        def wait_tasks(in_progress: typing.List[ray.ObjectRef]) -> typing.Iterable[pyarrow.RecordBatch]:
            task_timings = []

            if conf.get_bool("DUCKDB_DEBUG"):
                logger.warning(f"[Ray] Waiting for batch with {len(in_progress)} tasks")

            task_idx = 1
            while in_progress:
                # time ray.wait, not ray.get because wait is how long the task is actually taking to finish executing
                # ray.get just prepares an arrow reader to read the result from the ObjectStore
                task_start_time = time.time()

                ready_tasks, in_progress = ray.wait(in_progress, num_returns=1)

                task_end_time = time.time()
                task_duration = task_end_time - task_start_time
                task_timings.append((task_idx, task_duration))

                assert len(ready_tasks) == 1
                ready_task = ready_tasks[0]
                try:
                    yield from ray.get(ready_task).to_batches()
                except ray.exceptions.RayTaskError as exc:
                    if isinstance(exc.cause, EmptyPartition):
                        continue
                    raise exc.cause

                task_idx += 1

            if conf.get_bool("DUCKDB_DEBUG") and task_timings:
                timings_str = "\n".join([f"   - Task {idx}: {duration:.2f}s" for idx, duration in task_timings])
                logger.warning(f"[Ray] Batch detailed task timings:\n{timings_str}")

        def wait_tasks_in_batches() -> typing.Iterable[pyarrow.RecordBatch]:
            batch_ct = 1
            batch_start_time = time.time()
            yield from wait_tasks(first_batch_with_result)
            batch_end_time = time.time()
            batch_duration = batch_end_time - batch_start_time
            if conf.get_bool("DUCKDB_DEBUG"):
                task_count = len(first_batch_with_result)
                logger.warning(
                    f"[Ray] Batch #{batch_ct} execution completed in {batch_duration:.2f}s (contains {task_count} tasks)"
                )

            for batch in partition_batches:
                batch_start_time = time.time()
                batch_ct += 1
                yield from wait_tasks(batch)
                batch_end_time = time.time()
                batch_duration = batch_end_time - batch_start_time

                if conf.get_bool("DUCKDB_DEBUG"):
                    task_count = len(batch)
                    logger.warning(
                        f"[Ray] Batch #{batch_ct} execution completed in {batch_duration:.2f}s (contains {task_count} tasks)"
                    )

            if conf.get_bool("DUCKDB_DEBUG"):
                logger.warning("[Ray] all tasks completed")

        return pyarrow.RecordBatchReader.from_batches(schema, wait_tasks_in_batches())


def _first_non_empty_result(tasks: typing.List[ray.ObjectRef]) -> Optional[pyarrow.Table]:
    while tasks:
        ready_tasks, tasks = ray.wait(tasks, num_returns=1)
        try:
            return ray.get(ready_tasks[0])
        except ray.exceptions.RayTaskError as exc:
            if isinstance(exc.cause, EmptyPartition):
                logger.warning("Empty partition")
                continue

            raise exc.cause


def _execute_in_batches(
    partitions: typing.List[DAGNode], batch_size: int
) -> typing.Iterable[typing.List[ray.ObjectRef]]:
    assert batch_size > 0

    iterator = iter(partitions)
    current_batch = tuple(itertools.islice(iterator, batch_size))
    current_tasks = [node.execute() for node in current_batch]

    while True:
        # Start next batch to minimize the wait time
        # First two batches will be run in parallel, but all subsequent will be executed sequentially
        next_batch = tuple(itertools.islice(iterator, batch_size))
        if not next_batch:
            break

        next_tasks = [node.execute() for node in next_batch]

        yield current_tasks
        current_tasks = next_tasks

    # Don't forget the last one
    yield current_tasks
