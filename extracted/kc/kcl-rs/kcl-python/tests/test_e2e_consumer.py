# Copyright 2024 Amazon.com, Inc. or its affiliates. All Rights Reserved.
# SPDX-License-Identifier: Apache-2.0
"""
End-to-end tests for the ``kcl_rs`` Python bindings against a real Kinesis +
DynamoDB backend (LocalStack by default; also works against real AWS).

**Opt-in, like the Rust ``#[ignore]`` integration suites** (``kcl/tests/*_it.rs``
— see CLAUDE.md's "Running integration tests"): this whole module is skipped
unless ``AWS_ENDPOINT_URL`` is set. Region defaults to ``us-east-1`` if
``AWS_REGION``/``AWS_DEFAULT_REGION`` aren't set; credentials always come from
the standard AWS env vars / credential chain — nothing is hardcoded here.

Run against a local LocalStack instance::

    AWS_ENDPOINT_URL=http://localhost:4566 AWS_REGION=us-east-1 \\
    AWS_ACCESS_KEY_ID=test AWS_SECRET_ACCESS_KEY=test \\
        pytest kcl-python/tests/ -v

Each ``Scheduler`` cold start against LocalStack (lease table creation, shard
sync, and for FANOUT mode, ``RegisterStreamConsumer``) takes roughly 30-90s,
so every poll-until-condition wait here is bounded by ``KCLRS_E2E_AWAIT_SECS``
(default 300s; see ``conftest.await_budget_secs``) rather than fixed sleeps.
"""
from __future__ import annotations

import os
import threading
import time
import uuid

import pytest

from kcl_rs import CheckpointError, RecordProcessorBase, Scheduler

pytestmark = pytest.mark.skipif(
    not os.environ.get("AWS_ENDPOINT_URL"),
    reason=(
        "kcl-python e2e suite is opt-in: set AWS_ENDPOINT_URL (e.g. "
        "http://localhost:4566 for LocalStack) to run it, like the Rust "
        "`cargo test -p kcl -- --ignored` integration suites"
    ),
)

# Bound on scheduler.shutdown() itself: it should return promptly once the
# scheduler is running, but a hang here shouldn't wedge the whole CI job.
_SHUTDOWN_TIMEOUT_SECS = 60.0


class Recorder:
    """Thread-safe collection point for callbacks fired by a Scheduler's
    record processors.

    A Scheduler creates one processor per shard via the factory; every
    instance forwards into one shared Recorder so the test thread has a
    single place to poll from.
    """

    def __init__(self) -> None:
        self._lock = threading.Lock()
        self.payloads: set[bytes] = set()
        self.initialized = False
        self.shard_ids: set[str] = set()
        self.lease_lost_calls = 0
        self.shard_ended_calls = 0
        self.shutdown_requested_calls = 0
        self.errors: list[str] = []

    def note_initialize(self, shard_id: str | None) -> None:
        with self._lock:
            self.initialized = True
            if shard_id is not None:
                self.shard_ids.add(shard_id)

    def note_records(self, payloads) -> None:
        with self._lock:
            self.payloads.update(payloads)

    def note_lease_lost(self) -> None:
        with self._lock:
            self.lease_lost_calls += 1

    def note_shard_ended(self) -> None:
        with self._lock:
            self.shard_ended_calls += 1

    def note_shutdown_requested(self) -> None:
        with self._lock:
            self.shutdown_requested_calls += 1

    def note_error(self, message: str) -> None:
        with self._lock:
            self.errors.append(message)

    def payload_snapshot(self) -> set[bytes]:
        with self._lock:
            return set(self.payloads)


class RecordingProcessor(RecordProcessorBase):
    """Forwards every lifecycle callback into a shared ``Recorder``.

    Checkpoints after every batch (and at shard-ended / shutdown-requested),
    following the sample app's pattern (see
    ``kcl-python/samples/sample_kclrs_app.py``) but recording instead of
    logging, and swallowing ``CheckpointError`` into the recorder rather than
    retrying — these tests only run once per stream/app pair so a single
    checkpoint attempt is enough.
    """

    def __init__(self, recorder: Recorder) -> None:
        self._recorder = recorder
        self._shard_id: str | None = None

    def initialize(self, initialize_input) -> None:
        self._shard_id = initialize_input.shard_id
        self._recorder.note_initialize(self._shard_id)

    def process_records(self, process_records_input) -> None:
        try:
            payloads = [r.data for r in process_records_input.records]
            self._recorder.note_records(payloads)
            process_records_input.checkpointer.checkpoint()
        except CheckpointError as e:
            self._recorder.note_error(f"checkpoint error on shard {self._shard_id}: {e}")
        except Exception as e:  # noqa: BLE001 - a processor callback must never raise
            self._recorder.note_error(f"process_records error on shard {self._shard_id}: {e}")

    def lease_lost(self, lease_lost_input) -> None:
        self._recorder.note_lease_lost()

    def shard_ended(self, shard_ended_input) -> None:
        self._recorder.note_shard_ended()
        try:
            shard_ended_input.checkpointer.checkpoint()
        except CheckpointError as e:
            self._recorder.note_error(f"shard_ended checkpoint error: {e}")

    def shutdown_requested(self, shutdown_requested_input) -> None:
        self._recorder.note_shutdown_requested()
        try:
            shutdown_requested_input.checkpointer.checkpoint()
        except CheckpointError as e:
            self._recorder.note_error(f"shutdown_requested checkpoint error: {e}")


def _poll_until(condition, budget_secs: float, interval: float = 1.0) -> bool:
    """Poll ``condition()`` every ``interval``s until true or the budget elapses."""
    deadline = time.monotonic() + budget_secs
    while time.monotonic() < deadline:
        if condition():
            return True
        time.sleep(interval)
    return condition()


def _shutdown_with_timeout(scheduler: Scheduler, timeout: float = _SHUTDOWN_TIMEOUT_SECS) -> None:
    """Call ``scheduler.shutdown()`` off-thread so a hang fails the test
    instead of wedging the whole suite."""
    outcome: dict[str, BaseException] = {}

    def _do() -> None:
        try:
            scheduler.shutdown()
        except BaseException as e:  # noqa: BLE001 - surfaced to the test thread below
            outcome["error"] = e

    t = threading.Thread(target=_do, daemon=True)
    t.start()
    t.join(timeout)
    if t.is_alive():
        raise TimeoutError(f"scheduler.shutdown() did not return within {timeout}s")
    if "error" in outcome:
        raise outcome["error"]


def _run_scheduler_and_collect(
    *,
    stream_name: str,
    application_name: str,
    worker_identifier: str,
    region: str,
    endpoint_url: str,
    retrieval_mode: str,
    expected_count: int,
    budget_secs: float,
    initial_position: str = "TRIM_HORIZON",
    max_records: int | None = None,
    idle_time_between_reads_millis: int | None = None,
) -> Recorder:
    """Start a Scheduler, poll until ``expected_count`` distinct payloads have
    been recorded (or the budget elapses), then shut it down cleanly.

    Deliberately does NOT pass access_key_id/secret_access_key — credentials
    come from the ambient AWS env vars, matching the task's "env supplies
    them" requirement and CLAUDE.md's no-hardcoded-creds rule.
    """
    recorder = Recorder()
    scheduler = Scheduler(
        stream_name=stream_name,
        application_name=application_name,
        record_processor_factory=lambda: RecordingProcessor(recorder),
        worker_identifier=worker_identifier,
        region=region,
        endpoint_url=endpoint_url,
        initial_position=initial_position,
        retrieval_mode=retrieval_mode,
        max_records=max_records,
        idle_time_between_reads_millis=idle_time_between_reads_millis,
    )

    scheduler.start()
    try:
        _poll_until(
            lambda: len(recorder.payload_snapshot()) >= expected_count,
            budget_secs=budget_secs,
        )
    finally:
        # Clean shutdown is itself part of what these tests assert: if this
        # raises or hangs, the test fails with a clear cause rather than the
        # suite wedging.
        _shutdown_with_timeout(scheduler)

    return recorder


@pytest.mark.parametrize("retrieval_mode", ["FANOUT", "POLLING"])
def test_roundtrip_and_checkpoint_resume(
    stream_app_factory, aws_region, endpoint_url, await_budget_secs, retrieval_mode
):
    """(a) Roundtrip: 10 records in, one Scheduler, all 10 payloads observed,
    clean shutdown. (b) Checkpoint resume: 5 MORE records, a second Scheduler
    with the same application name (fresh worker id) sees ONLY the 5 new
    payloads — the strongest e2e signal that checkpointing actually works.
    """
    app = stream_app_factory()

    initial_payloads = [
        f"roundtrip-{retrieval_mode}-{i}-{uuid.uuid4().hex[:6]}".encode()
        for i in range(10)
    ]
    app.put_records(initial_payloads)

    recorder = _run_scheduler_and_collect(
        stream_name=app.stream_name,
        application_name=app.application_name,
        worker_identifier=f"worker-a-{uuid.uuid4().hex[:8]}",
        region=aws_region,
        endpoint_url=endpoint_url,
        retrieval_mode=retrieval_mode,
        expected_count=len(initial_payloads),
        budget_secs=await_budget_secs,
    )

    received = recorder.payload_snapshot()
    missing = set(initial_payloads) - received
    assert not missing, (
        f"[{retrieval_mode}] roundtrip: missing {len(missing)}/{len(initial_payloads)} "
        f"payloads after {await_budget_secs}s: {sorted(missing)}; "
        f"got {len(received)} payloads; processor errors: {recorder.errors}"
    )
    assert recorder.initialized, f"[{retrieval_mode}] initialize() never fired"
    assert not recorder.errors, f"[{retrieval_mode}] processor callback errors: {recorder.errors}"

    # --- (b) checkpoint resume ---
    more_payloads = [
        f"resume-{retrieval_mode}-{i}-{uuid.uuid4().hex[:6]}".encode() for i in range(5)
    ]
    app.put_records(more_payloads)

    recorder2 = _run_scheduler_and_collect(
        stream_name=app.stream_name,
        application_name=app.application_name,
        worker_identifier=f"worker-b-{uuid.uuid4().hex[:8]}",
        region=aws_region,
        endpoint_url=endpoint_url,
        retrieval_mode=retrieval_mode,
        expected_count=len(more_payloads),
        budget_secs=await_budget_secs,
    )

    received2 = recorder2.payload_snapshot()
    missing2 = set(more_payloads) - received2
    assert not missing2, (
        f"[{retrieval_mode}] resume: missing {len(missing2)}/{len(more_payloads)} new "
        f"payloads after {await_budget_secs}s: {sorted(missing2)}; "
        f"processor errors: {recorder2.errors}"
    )
    replayed = received2 & set(initial_payloads)
    assert not replayed, (
        f"[{retrieval_mode}] resume: checkpoint not respected — replayed "
        f"{len(replayed)} old payload(s) from run (a): {sorted(replayed)}"
    )
    assert not recorder2.errors, (
        f"[{retrieval_mode}] resume: processor callback errors: {recorder2.errors}"
    )


def test_polling_knobs_smoke(stream_app_factory, aws_region, endpoint_url, await_budget_secs):
    """POLLING-only smoke test for the max_records/idle_time_between_reads_millis knobs."""
    app = stream_app_factory()

    payloads = [f"knobs-{i}-{uuid.uuid4().hex[:6]}".encode() for i in range(10)]
    app.put_records(payloads)

    recorder = _run_scheduler_and_collect(
        stream_name=app.stream_name,
        application_name=app.application_name,
        worker_identifier=f"worker-knobs-{uuid.uuid4().hex[:8]}",
        region=aws_region,
        endpoint_url=endpoint_url,
        retrieval_mode="POLLING",
        expected_count=len(payloads),
        budget_secs=await_budget_secs,
        max_records=100,
        idle_time_between_reads_millis=500,
    )

    received = recorder.payload_snapshot()
    missing = set(payloads) - received
    assert not missing, (
        f"POLLING (max_records=100, idle_time_between_reads_millis=500): missing "
        f"{len(missing)}/{len(payloads)} payloads after {await_budget_secs}s: "
        f"{sorted(missing)}; processor errors: {recorder.errors}"
    )
    assert recorder.initialized, "initialize() never fired"
    assert not recorder.errors, f"processor callback errors: {recorder.errors}"
