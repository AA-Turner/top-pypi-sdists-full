# "micro" bench for common operations to get a sense of where overhead is

import functools
import io

import dill
import pyarrow as pa
from pytest_benchmark.fixture import BenchmarkFixture

_BATCH = pa.RecordBatch.from_pydict(
    {
        "a": list(range(1024)),
        "b": list(range(1024)),
    }
)


def test_dill_pickle_record_batch(benchmark: BenchmarkFixture) -> None:
    """
    Test the performance of pickling a record batch with dill.
    """
    benchmark(functools.partial(dill.dumps, _BATCH))


def test_dill_unpickle_record_batch(benchmark: BenchmarkFixture) -> None:
    """
    Test the performance of pickling a record batch with dill.
    """
    benchmark(functools.partial(dill.loads, dill.dumps(_BATCH)))


def test_ipc_file_serialized_record_batch(benchmark: BenchmarkFixture) -> None:
    """
    Test the performance of pickling a record batch with dill.
    """

    def _func() -> None:
        buf = io.BytesIO()
        with pa.ipc.new_file(buf, schema=_BATCH.schema) as f:
            f.write_batch(_BATCH)

    benchmark(_func)


def test_ipc_stream_serialized_record_batch(benchmark: BenchmarkFixture) -> None:
    """
    Test the performance of pickling a record batch with dill.
    """

    def _func() -> None:
        buf = io.BytesIO()
        with pa.ipc.new_stream(buf, schema=_BATCH.schema) as f:
            f.write_batch(_BATCH)

    benchmark(_func)


def test_ipc_file_deserialized_record_batch(benchmark: BenchmarkFixture) -> None:
    """
    Test the performance of pickling a record batch with dill.
    """
    buf = io.BytesIO()
    with pa.ipc.new_file(buf, schema=_BATCH.schema) as f:
        f.write_batch(_BATCH)

    def _func() -> None:
        buf.seek(0)
        with pa.ipc.open_file(buf) as f:
            f.read_all()

    benchmark(_func)


def test_ipc_stream_deserialized_record_batch(benchmark: BenchmarkFixture) -> None:
    """
    Test the performance of pickling a record batch with dill.
    """
    buf = io.BytesIO()
    with pa.ipc.new_stream(buf, schema=_BATCH.schema) as f:
        f.write_batch(_BATCH)

    def _func() -> None:
        buf.seek(0)
        with pa.ipc.open_stream(buf) as f:
            f.read_all()

    benchmark(_func)
