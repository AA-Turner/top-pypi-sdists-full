import itertools
import time
import warnings
from collections.abc import Callable, Iterator

import attrs
import numpy as np
import pyarrow as pa
import pytest
from pytest_benchmark.fixture import BenchmarkFixture
from typing_extensions import override

from geneva.apply.applier import BatchApplier
from geneva.apply.multiprocess import MultiProcessBatchApplier
from geneva.apply.simple import SimpleApplier
from geneva.apply.task import MapTask, ReadTask
from geneva.checkpoint_utils import format_checkpoint_key
from geneva.debug.logger import NoOpErrorLogger
from geneva.tqdm import tqdm

_BATCH = pa.RecordBatch.from_pydict(
    {
        "a": list(range(1024)),
        "b": list(range(1024)),
    }
)


@attrs.define
class InMemoryReadTask(ReadTask):
    """
    A read task that reads from an in-memory table.
    """

    n: int

    batch: pa.RecordBatch = attrs.field(default=_BATCH)
    batch_size: int = attrs.field(init=False, default=32)

    @override
    def to_batches(self, *, batch_size=32) -> Iterator[pa.RecordBatch]:
        self.batch_size = batch_size
        for _ in range(self.n):
            yield self.batch

    # below are the required methods for the ReadTask interface
    # but they are not used in this test
    @override
    def checkpoint_key(self) -> str:
        return "in_memory"

    @override
    def dest_frag_id(self) -> int:
        return 0

    @override
    def dest_offset(self) -> int:
        return 0

    @override
    def num_rows(self) -> int:
        return self.batch_size

    @override
    def table_uri(self) -> str:
        return "memory://in-memory"


@attrs.define
class SimulateLatency(MapTask):
    """
    A map task that simulates a latency distribution.
    """

    generator: Iterator[int] = attrs.field(
        default=itertools.cycle([10000]),
    )

    @override
    def apply(self, batch: pa.RecordBatch) -> pa.RecordBatch:
        n_iters = next(self.generator)
        while n_iters := n_iters - 1:
            ...
        return batch

    @override
    def batch_size(self) -> int:
        # not used, but need to return something
        return 1

    @override
    def checkpoint_key(
        self,
        *,
        dataset_uri: str,
        start: int,
        end: int,
        dataset_version=None,
        frag_id=None,
        where=None,
        src_files_hash: str | None = None,
    ) -> str:
        if frag_id is not None:
            return format_checkpoint_key(
                "benchmark_task", frag_id=frag_id, start=start, end=end
            )
        return "benchmark_task"

    def checkpoint_prefix(
        self,
        *,
        dataset_uri: str,
        where=None,
        column: str | None = None,
        src_files_hash: str | None = None,
    ) -> str:
        return "benchmark_task"

    def legacy_map_task_key(self, *, where: str | None = None) -> str:
        return "benchmark_task"

    @override
    def name(self) -> str:
        return "benchmark_task"

    @override
    def input_columns(self) -> list[str] | None:
        return None

    @override
    def output_schema(self) -> pa.Schema:
        raise NotImplementedError("output_schema not needed for benchmarks")

    @override
    def is_cuda(self) -> bool:
        return False

    @override
    def num_cpus(self) -> float | None:
        return None

    @override
    def num_gpus(self) -> float | None:
        return None

    @override
    def memory(self) -> int | None:
        return None


_APPLIERS = [
    (SimpleApplier(), "simple"),
    *[(MultiProcessBatchApplier(num_processes=n), f"n_proc={n}") for n in (4, 8, 16)],
]


@pytest.mark.parametrize(
    "applier",
    [applier for applier, _ in _APPLIERS],
    ids=[applier_name for _, applier_name in _APPLIERS],
)
def test_applier_overhead(
    benchmark: BenchmarkFixture,
    applier: BatchApplier,
) -> None:
    read_task = InMemoryReadTask(0)
    map_task = SimulateLatency()
    error_logger = NoOpErrorLogger()

    def _bench_fn() -> None:
        applier.run(
            read_task=read_task,
            map_task=map_task,
            error_logger=error_logger,
        )

    benchmark(_bench_fn)


_TASKS = [(InMemoryReadTask(n), f"n_batch={n}") for n in (2**i for i in range(5, 11))]

_PRODUCT = [
    ((applier, read_task), f"{applier_name} + {read_task_name}")
    for (applier, applier_name), (read_task, read_task_name) in itertools.product(
        _APPLIERS,
        _TASKS,
    )
]


@pytest.mark.parametrize(
    ("applier", "read_task"),
    [param for param, _ in _PRODUCT],
    ids=[param_name for _, param_name in _PRODUCT],
)
def test_applier_simple(
    benchmark: BenchmarkFixture,
    applier: BatchApplier,
    read_task: InMemoryReadTask,
) -> None:
    map_task = SimulateLatency()
    error_logger = NoOpErrorLogger()

    def _bench_fn() -> None:
        applier.run(
            read_task=read_task,
            map_task=map_task,
            error_logger=error_logger,
        )

    benchmark(_bench_fn)


@attrs.define
class _StandardNormalLatencyGenerator(Iterator[int]):
    mean: int
    std: int

    def __iter__(self) -> Iterator[int]:
        return self

    def __next__(self) -> int:
        # using the global method is much faster than pickling the generator
        return int(np.random.standard_normal(1)[0] * self.std + self.mean)  # noqa: NPY002


@pytest.mark.parametrize(
    ("applier", "read_task"),
    [param for param, _ in _PRODUCT],
    ids=[param_name for _, param_name in _PRODUCT],
)
def test_applier_standard_normal(
    benchmark: BenchmarkFixture,
    applier: BatchApplier,
    read_task: InMemoryReadTask,
) -> None:
    map_task = SimulateLatency(generator=_StandardNormalLatencyGenerator(10000, 0))
    error_logger = NoOpErrorLogger()

    def _bench_fn() -> None:
        applier.run(
            read_task=read_task,
            map_task=map_task,
            error_logger=error_logger,
        )

    benchmark(_bench_fn)


class FakeBenmark:
    def __call__(self, func: Callable) -> None:
        """
        Fake benchmark class to simulate the behavior of pytest-benchmark.
        """
        func()


def main() -> None:
    """
    Run the benchmarks.
    """
    n_warups = 5
    n_benchmarks = 10
    # make the most-minimal map task
    map_task = SimulateLatency(generator=itertools.cycle([1]))
    warnings.filterwarnings("ignore", message=".*lance is not fork-safe.*")

    for n_procs in (8,):
        applier = MultiProcessBatchApplier(num_processes=n_procs)
        for n_batches in (2**i for i in range(5, 10)):
            # pass tiny amount of data so we avoid pickling cost
            read_task = InMemoryReadTask(
                n_batches,
                batch=pa.RecordBatch.from_pydict(
                    {
                        "a": list(range(1)),
                    }
                ),
            )
            with tqdm(range(n_warups), leave=False) as pbar:
                suffix = f"nproc: {n_procs}, n_batches: {n_batches}"
                pbar.set_description(f"warmup -- {suffix}")
                for _ in pbar:
                    applier.run(
                        read_task=read_task,
                        map_task=map_task,
                        error_logger=NoOpErrorLogger(),
                    )
            start = time.perf_counter()
            with tqdm(range(n_benchmarks), leave=False) as pbar:
                suffix = f"nproc: {n_procs}, n_batches: {n_batches}"
                pbar.set_description(f"bench -- {suffix}")
                for _ in pbar:
                    applier.run(
                        read_task=read_task,
                        map_task=map_task,
                        error_logger=NoOpErrorLogger(),
                    )
            end = time.perf_counter()

            elapsed = end - start
            throughput = n_batches / elapsed * n_benchmarks
            print(  # noqa: T201
                f"nproc: {n_procs}, n_batches: {n_batches}"
                f" elapsed: {elapsed:.2f}s, "
                f"throughput: {throughput:.2f} batches/s"
            )


if __name__ == "__main__":
    main()
