import asyncio
import gc
from dataclasses import dataclass, field
from time import perf_counter
from uuid import uuid4

import icechunk as ic
import zarr
from rich.console import Console
from rich.panel import Panel
from rich.progress import Progress, TaskID
from zarr.buffer import default_buffer_prototype

from arraylake import Client

BITS_PER_BYTE = 8
# how many more chunks than async tasks to use
CHUNK_FACTOR = 4
CONSOLE = Console()


@dataclass(frozen=True)
class ThroughputBenchResult:
    total_chunks: int
    chunksize_bytes: int
    async_concurrency: int
    write_time: float | None = None
    read_time: float | None = None
    write_io_error: bool | None = None
    read_io_error: bool | None = None

    @property
    def read_throughput_mbps(self) -> float:
        assert self.read_time is not None, "read_time must be set to calculate read throughput"
        return (self.total_chunks * BITS_PER_BYTE * self.chunksize_bytes) / (self.read_time * 1_000_000)

    @property
    def write_throughput_mbps(self) -> float:
        assert self.write_time is not None, "write_time must be set to calculate write throughput"
        return (self.total_chunks * BITS_PER_BYTE * self.chunksize_bytes) / (self.write_time * 1_000_000)


@dataclass(frozen=True)
class IOConfig:
    async_concurrency: int
    chunksize_bytes: int
    throughput_mbps: float


@dataclass(frozen=True)
class OptimalIOConfig:
    read: IOConfig
    write: IOConfig


@dataclass(frozen=True)
class ResultSet:
    results: list[ThroughputBenchResult] = field(default_factory=list)

    def _best_result(self, key: str, thresh: float = 0.05) -> IOConfig:
        max_throughput = max(getattr(result, key) for result in self.results if getattr(result, key) is not None)
        acceptable = [
            result for result in self.results if getattr(result, key) is not None and getattr(result, key) > max_throughput * (1 - thresh)
        ]
        acceptable.sort(key=lambda r: r.async_concurrency)
        return IOConfig(
            async_concurrency=acceptable[0].async_concurrency,
            chunksize_bytes=acceptable[0].chunksize_bytes,
            throughput_mbps=getattr(acceptable[0], key),
        )

    def best_read(self) -> IOConfig:
        return self._best_result("read_throughput_mbps")

    def best_write(self) -> IOConfig:
        return self._best_result("write_throughput_mbps")


@dataclass
class ThroughputBenchmarker:
    repo: ic.Repository
    async_concurrency: int
    chunksize_bytes: int
    sem: asyncio.Semaphore = field(init=False)
    console: Console = field(default_factory=Console)
    nchunks: int = field(init=False)
    store: ic.IcechunkStore = field(init=False)
    array_name: str = field(init=False, default="dummy_array")
    # for rich progress bar
    write_task: int = field(init=False, default=0)
    read_task: int = field(init=False, default=0)

    def __post_init__(self):
        self.sem = asyncio.Semaphore(self.async_concurrency)
        self.nchunks = self.async_concurrency * CHUNK_FACTOR

        session = self.repo.writable_session("main")
        store = session.store
        self.store = store
        group = zarr.group(store=store, zarr_format=3)
        # we need to create an array in order for Icechunk to let us write chunks
        group.create_array(self.array_name, shape=self.nchunks, chunks=(1,), dtype="int64")  # doesn't matter what dtype we use here

    async def get_chunk(self, key: str, progress: Progress, task: TaskID) -> None:
        async with self.sem:
            _ = await self.store.get(key, default_buffer_prototype())
        progress.update(task, advance=1)

    async def set_chunk(self, key: str, buf: zarr.core.buffer.BufferPrototype, progress: Progress, task: TaskID):
        async with self.sem:
            await self.store.set(key, buf)  # type: ignore[arg-type]
        progress.update(task, advance=1)

    async def get_all_chunks(self) -> None:
        keys = [f"{self.array_name}/c/{n}" for n in range(self.nchunks)]
        message = f"Reading {self.nchunks * self.chunksize_bytes} bytes in {self.nchunks} chunks"
        with Progress(console=self.console, transient=True) as progress:
            task = progress.add_task(message, total=self.nchunks)
            await asyncio.gather(*[self.get_chunk(key, progress, task) for key in keys])
        gc.collect()

    async def write_all_chunks(self) -> None:
        raw_bytes = self.chunksize_bytes * b"\x00"
        buf = default_buffer_prototype().buffer.from_bytes(raw_bytes)
        keys = [f"{self.array_name}/c/{n}" for n in range(self.nchunks)]
        message = f"Writing {self.nchunks * self.chunksize_bytes} bytes in {self.nchunks} chunks"
        with Progress(console=self.console, transient=True) as progress:
            task = progress.add_task(message, total=self.nchunks)
            await asyncio.gather(*[self.set_chunk(key, buf, progress, task) for key in keys])  # type: ignore[arg-type]
        del buf
        gc.collect()


async def benchmark_io(repo: ic.Repository, async_concurrency: int, chunksize_bytes: int) -> ThroughputBenchResult:
    bencher = ThroughputBenchmarker(repo, async_concurrency, chunksize_bytes, console=CONSOLE)

    write_io_error = False
    read_io_error = False
    t0 = perf_counter()
    try:
        await bencher.write_all_chunks()
    except ic.IcechunkError as ice:
        CONSOLE.log("IcechunkError detected")
        # TODO: make this format correctly with Rich
        CONSOLE.out(str(ice))
        write_io_error = True
    t1 = perf_counter()
    if not write_io_error:
        try:
            await bencher.get_all_chunks()
        except ic.IcechunkError as ice:
            CONSOLE.log("IcechunkError detected")
            CONSOLE.out(str(ice))
            read_io_error = True
    t2 = perf_counter()

    write_time = t1 - t0
    read_time = t2 - t1

    return ThroughputBenchResult(
        total_chunks=bencher.nchunks,
        chunksize_bytes=bencher.chunksize_bytes,
        async_concurrency=async_concurrency,
        write_time=write_time,
        read_time=read_time,
        write_io_error=write_io_error,
        read_io_error=read_io_error,
    )


async def benchmark_run(repo: ic.Repository, concurrency_trials: list[int], chunksize: int) -> list[ThroughputBenchResult]:
    results = []
    for concurrency in concurrency_trials:
        message = f"Concurrency {concurrency} | chunksize {chunksize} bytes"
        result = await benchmark_io(repo, concurrency, chunksize)
        results.append(result)
        if not result.write_io_error:
            message += f"| Write {result.write_throughput_mbps:3.2f} Mbps"
        if not result.read_io_error and not result.write_io_error:
            message += f"| Read {result.read_throughput_mbps:3.2f} Mbps"
        if result.write_io_error or result.read_io_error:
            message += "| Stopping benchmarks due to IO errors."
            break
        CONSOLE.log(message)
    return results


async def tune_repo(repo: ic.Repository):
    # this first run will always be fast even on very slow internet connections
    chunksize_bytes = 10_000
    concurrency = [1, 2, 4, 8]
    tiny_result_set = ResultSet(await benchmark_run(repo, concurrency, chunksize_bytes))

    if tiny_result_set.best_read().throughput_mbps < 1:
        CONSOLE.print("Read throughput is too low, skipping further benchmarks.")
        return tiny_result_set

    # now we can do a more thorough benchmark
    chunksize_bytes = 100_000
    concurrency = [4, 8, 16]
    result_set_small = ResultSet(await benchmark_run(repo, concurrency, chunksize_bytes))

    if result_set_small.best_read().throughput_mbps < 50:
        CONSOLE.print("Read throughput is too low, skipping further benchmarks.")
        return result_set_small

    chunksize_bytes = 1_000_000
    concurrency = [4, 8, 16, 32]
    result_set_med = ResultSet(await benchmark_run(repo, concurrency, chunksize_bytes))

    if result_set_med.best_read().throughput_mbps < 500:
        CONSOLE.print("Read throughput is too low, skipping further benchmarks.")
        return result_set_med

    chunksize_bytes = 10_000_000
    concurrency = [8, 16, 32, 64, 128]
    result_set_large = ResultSet(await benchmark_run(repo, concurrency, chunksize_bytes))
    return result_set_large


async def tune_org(org: str, bucket_config_nickname: str | None = None) -> OptimalIOConfig:
    client = Client()
    repo_name = f"{org}/_benchmark_{uuid4()}"

    CONSOLE.print(
        Panel(
            (
                "This utility will create a temporary repo to measure the I/O performance of this host. "
                "It will perform a series of experiments which write and read data to find the optimal chunk size and concurrency."
            ),
            title="[green bold] Arraylake Repo I/O Benchmarker",
        )
    )

    config = ic.RepositoryConfig.default()
    config.inline_chunk_threshold_bytes = 0
    config.caching = ic.CachingConfig(num_bytes_chunks=0)
    with CONSOLE.status(f"Creating temporary repo [yellow]{repo_name}"):
        repo = client.create_repo(repo_name, bucket_config_nickname=bucket_config_nickname, config=config)
    try:
        results = await tune_repo(repo)
        optimal_config = OptimalIOConfig(read=results.best_read(), write=results.best_write())
    finally:
        with CONSOLE.status("Cleaning up temporary repo"):
            client.delete_repo(repo_name, imsure=True, imreallysure=True)
    CONSOLE.print("Optimal I/O configuration found:")
    CONSOLE.print(optimal_config)
    return optimal_config
