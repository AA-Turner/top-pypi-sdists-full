# SPDX-License-Identifier: PROPRIETARY
# SPDX-FileCopyrightText: Copyright The Geneva Authors
"""A UDF raising ``FatalWorkerHardwareError`` escapes worker-side retry and
null-fill, parks its whole-GPU actor, and is retried on a healthy worker.

Real-Ray tests use two fake GPUs; the GPU that runs the first batch is the
faulted one, identified by ``CUDA_VISIBLE_DEVICES``.
"""

import fcntl
import logging
import os
import uuid
from collections import Counter
from collections.abc import Callable, Iterator
from pathlib import Path
from types import SimpleNamespace
from typing import NoReturn

import lance
import pyarrow as pa
import pyarrow.compute as pc
import pytest

import geneva
from geneva import FatalWorkerHardwareError, Retry, Skip, retry_all, skip_on_error, udf
from geneva.apply.error_handling import (
    BatchStrategy,
    ErrorHandlingContext,
    FailFastStrategy,
    has_hardware_fault,
    promote_hardware_fault,
)
from geneva.apply.multiprocess import _picklable_worker_error
from geneva.apply.task import BackfillUDFTask
from geneva.db import Connection
from geneva.debug.error_store import (
    FaultIsolation,
    Outcome,
    get_exception_outcome,
)
from geneva.errors import CheckpointCoverageError, FatalWorkerCrashError
from geneva.runners.ray import pipeline as pipeline_module
from geneva.runners.ray._mgr import ray_cluster
from geneva.runners.ray.pipeline import (
    DEFAULT_FATAL_WORKER_MAX_ATTEMPTS,
    _attribute_hardware_fault,
    _default_worker_loss_policy,
    _normalize_fatal_worker_error,
    _picklable_remote_error,
)

SIZE = 20
N = 16
ALL_ROWS = list(range(N))
FAULT_ROW = 11


def _raise_fault(gpu: str, *, wrapped: bool) -> NoReturn:
    fault = FatalWorkerHardwareError(f"GPU {gpu} requires reset")
    if wrapped:
        raise RuntimeError("model setup failed") from fault
    raise fault


def _wrapped_fault() -> RuntimeError:
    try:
        _raise_fault("0", wrapped=True)
    except RuntimeError as exc:
        return exc


# =============================================================================
# Type plumbing (no Ray)
# =============================================================================


def test_has_hardware_fault_sees_wrapped_cause() -> None:
    assert has_hardware_fault(FatalWorkerHardwareError("x"))
    assert has_hardware_fault(_wrapped_fault())
    assert not has_hardware_fault(RuntimeError("CUDA out of memory"))
    assert not has_hardware_fault(FatalWorkerCrashError("multiprocess worker stalled"))


def test_promote_hardware_fault_is_canonical_and_keeps_message() -> None:
    direct = FatalWorkerHardwareError("gpu dead")
    assert promote_hardware_fault(direct) is direct
    promoted = promote_hardware_fault(_wrapped_fault())
    assert type(promoted) is FatalWorkerHardwareError
    assert "model setup failed" in str(promoted)
    assert "GPU 0 requires reset" in str(promoted)


def test_multiprocess_error_keeps_only_the_hardware_type() -> None:
    direct = _picklable_worker_error(FatalWorkerHardwareError("gpu dead"))
    assert type(direct) is FatalWorkerHardwareError
    wrapped = _picklable_worker_error(_wrapped_fault())
    assert type(wrapped) is FatalWorkerHardwareError
    assert "GPU 0 requires reset" in str(wrapped)
    promoted = _picklable_worker_error(promote_hardware_fault(_wrapped_fault()))
    assert str(promoted).count("GPU 0 requires reset") == 1
    assert type(_picklable_worker_error(ValueError("bad row"))) is RuntimeError
    coverage = CheckpointCoverageError(3, gap_start=1, gap_end=2)
    assert type(_picklable_worker_error(coverage)) is RuntimeError


def test_ray_boundary_and_normalization_keep_the_type() -> None:
    remote = _picklable_remote_error(FatalWorkerHardwareError("gpu dead"))
    assert type(remote) is FatalWorkerHardwareError
    assert str(remote) == "gpu dead"
    normalized = _normalize_fatal_worker_error(_wrapped_fault())
    assert type(normalized) is FatalWorkerHardwareError


def test_attribution_never_raises_when_ray_lookups_fail(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    def _unavailable(*_args: object) -> NoReturn:
        raise RuntimeError("not connected")

    # Stubbed: calling these outside a cluster would auto-init Ray without
    # the fake GPUs the later fixtures need.
    monkeypatch.setattr(pipeline_module.ray, "get_runtime_context", _unavailable)
    monkeypatch.setattr(pipeline_module.ray, "get_gpu_ids", _unavailable)
    err = _attribute_hardware_fault(promote_hardware_fault(_wrapped_fault()))
    assert type(err) is FatalWorkerHardwareError
    assert str(err).count("GPU 0 requires reset") == 1
    assert "[node=" in str(err)
    assert "gpu=" in str(err)


def test_default_policy_retries_elsewhere_and_never_null_fills() -> None:
    error = FatalWorkerHardwareError("gpu dead")
    config = _default_worker_loss_policy(error)
    assert config is not None
    assert get_exception_outcome(error, config) == Outcome.RETRY
    assert config.fault_isolation == FaultIsolation.FAIL_BATCH
    assert config.retry_config.stop.max_attempt_number == (  # type: ignore[attr-defined]
        DEFAULT_FATAL_WORKER_MAX_ATTEMPTS
    )


# =============================================================================
# Worker-side strategies let the fault escape (no Ray)
# =============================================================================


def _batch(n: int = N) -> pa.RecordBatch:
    return pa.RecordBatch.from_arrays(
        [pa.array(range(n), type=pa.int64()), pa.array(range(n), type=pa.uint64())],
        ["a", "_rowaddr"],
    )


def _strategy(target: Callable, error_logger: object | None = None) -> BatchStrategy:
    task = BackfillUDFTask(udfs={"b": target})
    ctx = ErrorHandlingContext(
        job_id="hw-fault-test",
        task_context={
            "table_uri": "memory:///test.lance",
            "table_version": 1,
            "fragment_id": 0,
        },
        seq=0,
        udf_name="b",
        udf_version="hw-fault-test-version",
        error_config=target.error_handling,
    )
    return BatchStrategy.from_context(ctx, task, error_logger)  # type: ignore[arg-type]


def _make_udf(
    on_error: object | None,
    *,
    fault_on: str,
    wrapped: bool,
) -> tuple[Callable, list[list[int]]]:
    """``fault_on="batch"``: any segment holding FAULT_ROW raises the hardware
    fault. ``fault_on="leaf"``: multi-row segments holding FAULT_ROW raise a
    plain ``ValueError`` (so bisection starts) and only the single-row leaf
    raises the hardware fault. ``fault_on="plain"``: ordinary ``ValueError``."""
    calls: list[list[int]] = []

    @udf(data_type=pa.int64(), on_error=on_error)  # type: ignore[arg-type]
    def target(a: pa.Array) -> pa.Array:
        rows = a.to_pylist()
        calls.append(rows)
        if FAULT_ROW in rows:
            if fault_on == "plain" or (fault_on == "leaf" and len(rows) > 1):
                raise ValueError(f"poison row {FAULT_ROW}")
            _raise_fault("0", wrapped=wrapped)
        return pc.multiply(a, 2)

    return target, calls


@pytest.mark.parametrize("wrapped", [False, True])
def test_retry_all_runs_hardware_fault_once(wrapped: bool) -> None:
    target, calls = _make_udf(
        retry_all(max_attempts=3), fault_on="batch", wrapped=wrapped
    )
    with pytest.raises(FatalWorkerHardwareError):
        _strategy(target).apply(_batch())
    assert calls == [ALL_ROWS]


def test_retry_all_still_retries_ordinary_errors() -> None:
    target, calls = _make_udf(
        retry_all(max_attempts=3), fault_on="plain", wrapped=False
    )
    with pytest.raises(ValueError, match="poison row"):
        _strategy(target).apply(_batch())
    assert calls == [ALL_ROWS, ALL_ROWS, ALL_ROWS]


@pytest.mark.parametrize("wrapped", [False, True])
def test_skip_on_error_does_not_bisect_hardware_fault(wrapped: bool) -> None:
    target, calls = _make_udf(skip_on_error(), fault_on="batch", wrapped=wrapped)
    with pytest.raises(FatalWorkerHardwareError):
        _strategy(target).apply(_batch())
    assert calls == [ALL_ROWS]


@pytest.mark.parametrize("wrapped", [False, True])
@pytest.mark.parametrize(
    "on_error",
    [
        pytest.param(skip_on_error(), id="skip-only"),
        pytest.param(
            [Retry(Exception, max_attempts=3), Skip(Exception)], id="retry-then-skip"
        ),
    ],
)
def test_leaf_hardware_fault_escapes_bisection(on_error: object, wrapped: bool) -> None:
    """A plain error starts bisection; a hardware fault at the isolated row must
    still escape instead of being null-filled by the row handlers."""
    target, calls = _make_udf(on_error, fault_on="leaf", wrapped=wrapped)
    with pytest.raises(FatalWorkerHardwareError):
        _strategy(target).apply(_batch())
    assert len(calls) > 1, "bisection never started"
    assert calls.count([FAULT_ROW]) == 1, "the faulting leaf ran more than once"


@pytest.mark.parametrize("wrapped", [False, True])
def test_fail_fast_logs_canonical_type(wrapped: bool) -> None:
    target, _calls = _make_udf(None, fault_on="batch", wrapped=wrapped)
    records: list = []
    strategy = _strategy(target, SimpleNamespace(log_error=records.append))
    assert isinstance(strategy, FailFastStrategy)
    with pytest.raises(FatalWorkerHardwareError):
        strategy.apply(_batch())
    assert [r.error_type for r in records] == ["FatalWorkerHardwareError"]


# =============================================================================
# Real Ray with two fake GPUs
# =============================================================================


def _attempts(state: Path) -> list[tuple[str, str]]:
    """``(gpu, rows)`` per UDF invocation, in order."""
    log = state / "attempts.log"
    if not log.exists():
        return []
    return [
        (gpu, rows)
        for gpu, rows in (
            line.split("|") for line in log.read_text().strip().splitlines()
        )
    ]


def _bad_gpu(state: Path) -> str:
    return (state / "bad_gpu").read_text()


def _gpu_udf(
    state: Path,
    *,
    on_error: object | None = None,
    wrapped: bool = False,
    num_gpus: float = 1.0,
    fault_rows: set[int] | None = None,
) -> Callable:
    """Array UDF failing on the faulted GPU (or on ``fault_rows`` on any GPU).

    Helpers are closures: Ray workers cannot import this test module."""
    log = state / "attempts.log"
    marker = state / "bad_gpu"

    def append(line: str) -> None:
        with open(log, "a") as f:
            fcntl.flock(f.fileno(), fcntl.LOCK_EX)
            f.write(line + "\n")
            fcntl.flock(f.fileno(), fcntl.LOCK_UN)

    def gpu_is_bad(gpu: str) -> bool:
        try:
            fd = os.open(marker, os.O_CREAT | os.O_EXCL | os.O_WRONLY)
            os.write(fd, gpu.encode())
            os.close(fd)
            return True
        except FileExistsError:
            return marker.read_text() == gpu

    def raise_fault(gpu: str) -> NoReturn:
        fault = FatalWorkerHardwareError(f"GPU {gpu} requires reset")
        if wrapped:
            raise RuntimeError("model setup failed") from fault
        raise fault

    @udf(  # type: ignore[arg-type]
        data_type=pa.int64(),
        num_gpus=num_gpus,
        on_error=on_error,
        version=uuid.uuid4().hex,
    )
    def times_two(a: pa.Array) -> pa.Array:
        gpu = os.environ.get("CUDA_VISIBLE_DEVICES", "")
        rows = a.to_pylist()
        append(f"{gpu}|{rows[0]}-{rows[-1]}")
        if fault_rows is not None:
            if fault_rows & set(rows):
                raise_fault(gpu)
        elif gpu_is_bad(gpu):
            raise_fault(gpu)
        return pc.multiply(a, 2)

    return times_two


def _lazy_setup_udf(state: Path, *, on_error: object | None, wrapped: bool) -> object:
    """Stateful UDF whose first call runs the device check in ``setup()``."""
    log = state / "attempts.log"
    marker = state / "bad_gpu"

    def append(line: str) -> None:
        with open(log, "a") as f:
            fcntl.flock(f.fileno(), fcntl.LOCK_EX)
            f.write(line + "\n")
            fcntl.flock(f.fileno(), fcntl.LOCK_UN)

    def gpu_is_bad(gpu: str) -> bool:
        try:
            fd = os.open(marker, os.O_CREAT | os.O_EXCL | os.O_WRONLY)
            os.write(fd, gpu.encode())
            os.close(fd)
            return True
        except FileExistsError:
            return marker.read_text() == gpu

    @udf(  # type: ignore[arg-type]
        data_type=pa.int64(),
        num_gpus=1.0,
        on_error=on_error,
        version=uuid.uuid4().hex,
    )
    class ShotDetector:
        def __init__(self) -> None:
            self.ready = False

        def setup(self) -> None:
            gpu = os.environ.get("CUDA_VISIBLE_DEVICES", "")
            if gpu_is_bad(gpu):
                fault = FatalWorkerHardwareError(f"GPU {gpu} requires reset")
                if wrapped:
                    raise RuntimeError("model setup failed") from fault
                raise fault
            self.ready = True

        def __call__(self, a: pa.Array) -> pa.Array:
            rows = a.to_pylist()
            gpu = os.environ.get("CUDA_VISIBLE_DEVICES", "")
            append(f"{gpu}|{rows[0]}-{rows[-1]}")
            if not self.ready:
                self.setup()
            return pc.multiply(a, 2)

    # ``@udf`` on a class returns a factory; the instance is the UDF.
    return ShotDetector()


@pytest.fixture(scope="module")
def two_gpu_ray() -> Iterator[None]:
    # 8 CPUs: parked actors keep their CPUs; multiprocess appliers take 2 each.
    with ray_cluster(
        local=True,
        log_to_driver=True,
        logging_level=logging.INFO,
        ray_init_kwargs={"num_gpus": 2, "num_cpus": 8},
    ):
        yield


@pytest.fixture
def db(tmp_path: Path) -> Iterator[Connection]:
    lance.write_dataset(
        pa.Table.from_pydict({"a": pa.array(range(SIZE))}),
        tmp_path / "test.lance",
        max_rows_per_file=10,
    )
    conn = geneva.connect(str(tmp_path))
    yield conn
    conn.close()


def _run(
    db: Connection, state: Path, target: object, **backfill_kwargs: object
) -> tuple[BaseException | None, object, list[int | None]]:
    state.mkdir(exist_ok=True)
    tbl = db.open_table("test")
    tbl.add_columns({"b": target}, batch_size=4)
    exc: BaseException | None = None
    result = None
    try:
        result = tbl.backfill("b", **backfill_kwargs)  # type: ignore[arg-type]
    except Exception as e:  # noqa: BLE001
        exc = e
    values = db.open_table("test").to_arrow().sort_by("a")["b"].to_pylist()
    return exc, result, values


EXPECTED = [a * 2 for a in range(SIZE)]


@pytest.mark.ray
@pytest.mark.timeout(300)
@pytest.mark.parametrize("wrapped", [False, True])
def test_fault_reschedules_onto_healthy_gpu(
    db: Connection, two_gpu_ray, tmp_path: Path, wrapped: bool
) -> None:
    state = tmp_path / "state"
    exc, result, values = _run(
        db, state, _gpu_udf(state, wrapped=wrapped), concurrency=2
    )
    assert exc is None, exc
    assert values == EXPECTED
    assert db.open_table("test").get_failed_row_addresses(result.job_id, "b") == []  # type: ignore[union-attr]

    bad = _bad_gpu(state)
    attempts = _attempts(state)
    on_bad = [rows for gpu, rows in attempts if gpu == bad]
    on_good = {rows for gpu, rows in attempts if gpu != bad}
    assert len(on_bad) == 1
    assert on_bad[0] in on_good, "the failed task never re-ran on the healthy GPU"


@pytest.mark.ray
@pytest.mark.timeout(300)
def test_single_actor_recovers_on_spare_gpu(
    db: Connection, two_gpu_ray, tmp_path: Path
) -> None:
    """concurrency=1: the only actor's GPU faults; the replacement must land on
    the spare GPU rather than the job terminating."""
    state = tmp_path / "state"
    exc, _result, values = _run(db, state, _gpu_udf(state), concurrency=1)
    assert exc is None, exc
    assert values == EXPECTED
    bad = _bad_gpu(state)
    gpus = Counter(gpu for gpu, _ in _attempts(state))
    assert gpus[bad] == 1
    assert len(gpus) == 2, f"replacement never ran on another GPU: {gpus}"


@pytest.mark.ray
@pytest.mark.timeout(300)
def test_retry_all_moves_to_healthy_gpu_without_local_retry(
    db: Connection, two_gpu_ray, tmp_path: Path
) -> None:
    state = tmp_path / "state"
    exc, _result, values = _run(
        db, state, _gpu_udf(state, on_error=retry_all(max_attempts=3)), concurrency=2
    )
    assert exc is None, exc
    assert values == EXPECTED
    bad = _bad_gpu(state)
    assert sum(1 for gpu, _ in _attempts(state) if gpu == bad) == 1


@pytest.mark.ray
@pytest.mark.timeout(300)
def test_skip_on_error_recovers_rows_on_healthy_gpu(
    db: Connection, two_gpu_ray, tmp_path: Path
) -> None:
    """With a GPU-keyed fault the driver's bisected halves succeed elsewhere,
    so no row is null-filled and the faulted actor is parked."""
    state = tmp_path / "state"
    exc, result, values = _run(
        db, state, _gpu_udf(state, on_error=skip_on_error()), concurrency=2
    )
    assert exc is None, exc
    assert values == EXPECTED
    assert db.open_table("test").get_failed_row_addresses(result.job_id, "b") == []  # type: ignore[union-attr]
    bad = _bad_gpu(state)
    assert sum(1 for gpu, _ in _attempts(state) if gpu == bad) == 1


@pytest.mark.ray
@pytest.mark.timeout(300)
def test_skip_on_error_nulls_a_single_row_fault(
    db: Connection, two_gpu_ray, tmp_path: Path
) -> None:
    """A one-row task that faults on every GPU is null-filled once under the
    user's Skip policy, with a hardware-typed error record. Multi-row tasks are
    not asserted here: bisection would park every GPU first."""
    state = tmp_path / "state"
    exc, result, values = _run(
        db,
        state,
        _gpu_udf(state, on_error=skip_on_error(), fault_rows={0}),
        concurrency=2,
        task_size=1,
    )
    assert exc is None, exc
    assert values == [None, *EXPECTED[1:]]
    tbl = db.open_table("test")
    assert tbl.get_failed_row_addresses(result.job_id, "b") == [0]  # type: ignore[union-attr]
    errors = tbl.get_errors(job_id=result.job_id, column_name="b")  # type: ignore[union-attr]
    assert any(e.error_type == "FatalWorkerHardwareError" for e in errors)


@pytest.mark.ray
@pytest.mark.timeout(300)
@pytest.mark.parametrize("wrapped", [False, True])
def test_lazy_setup_fault_crosses_multiprocess_boundary(
    db: Connection, two_gpu_ray, tmp_path: Path, wrapped: bool
) -> None:
    """The incident shape end to end: a stateful UDF whose setup() raises on
    the faulted GPU, inside a real child process, under a user retry policy.
    The task must finish on the healthy GPU with no local retry and a typed
    error record."""
    state = tmp_path / "state"
    exc, result, values = _run(
        db,
        state,
        _lazy_setup_udf(state, on_error=retry_all(max_attempts=3), wrapped=wrapped),
        concurrency=2,
        intra_applier_concurrency=2,
    )
    assert exc is None, exc
    assert values == EXPECTED
    bad = _bad_gpu(state)
    # Several child batches may run setup() in one attempt; none may repeat.
    on_bad = Counter(rows for gpu, rows in _attempts(state) if gpu == bad)
    assert on_bad
    assert max(on_bad.values()) == 1, on_bad
    errors = db.open_table("test").get_errors(job_id=result.job_id, column_name="b")  # type: ignore[union-attr]
    assert any(e.error_type == "FatalWorkerHardwareError" for e in errors)


@pytest.mark.ray
@pytest.mark.timeout(300)
def test_lazy_setup_fault_default_policy_multiprocess(
    db: Connection, two_gpu_ray, tmp_path: Path
) -> None:
    state = tmp_path / "state"
    exc, _result, values = _run(
        db,
        state,
        _lazy_setup_udf(state, on_error=None, wrapped=False),
        concurrency=2,
        intra_applier_concurrency=2,
    )
    assert exc is None, exc
    assert values == EXPECTED
