"""Batched sampling admission and shared, bounded completion transport."""

from __future__ import annotations

import asyncio
import math
import threading
import time
import uuid
from collections.abc import AsyncIterator, Callable
from concurrent.futures import Executor
from concurrent.futures import TimeoutError as FutureTimeout
from dataclasses import dataclass
from typing import Any

import grpc

from ._proto import pb2
from .types import RiverConnectionError, RiverError, RiverTimeoutError, Sample

MAX_SAMPLING_BATCH = 128


def submit_batch(
    session,
    source,
    *,
    timeout: float,
    idempotency_key: str | None = None,
    pinned_policy_id: str | None = None,
    policy_selection: str = "ordered",
    retained_kv_groups: list[str] | None = None,
    kv_cache_policy: dict | None = None,
) -> tuple[str, ...]:
    """Retry the same immutable admission envelope, including a lost ack."""
    if not math.isfinite(timeout) or not 0 < timeout <= 24 * 3600:
        raise ValueError("sampling timeout must be positive and at most 24 hours")
    field = {
        pb2.SampleFromTrainingRequest: "training",
        pb2.InferenceGenerateRequest: "base",
        pb2.SampleFromCheckpointRequest: "checkpoint",
    }[type(source)]
    if not 1 <= len(source.prompts) <= MAX_SAMPLING_BATCH:
        raise ValueError(
            f"submit_sampling_batch accepts 1..{MAX_SAMPLING_BATCH} samples"
        )
    selections = {
        "ordered": pb2.SAMPLING_POLICY_SELECTION_ORDERED,
        "latest_snapshot": pb2.SAMPLING_POLICY_SELECTION_LATEST_SNAPSHOT,
    }
    if policy_selection not in selections:
        raise ValueError("policy_selection must be ordered or latest_snapshot")
    if policy_selection == "latest_snapshot" and (
        field != "training" or pinned_policy_id
    ):
        raise ValueError(
            "latest_snapshot requires a training source and no explicit policy pin"
        )
    if kv_cache_policy is not None and retained_kv_groups is None:
        raise ValueError("kv_cache_policy requires retained_kv_groups")
    if retained_kv_groups is not None:
        if (
            kv_cache_policy is None
            or field != "training"
            or pinned_policy_id
            or len(retained_kv_groups) != len(source.prompts)
        ):
            raise ValueError(
                "retained_kv_groups requires a bounded kv_cache_policy, one group per training prompt, and no pinned_policy_id"
            )
        retained_kv_groups = [str(uuid.UUID(group)) for group in retained_kv_groups]
    key = uuid.uuid4() if idempotency_key is None else uuid.UUID(idempotency_key)
    request = pb2.SubmitSamplingBatchRequest(
        idempotency_key=str(key),
        pinned_policy_id=pinned_policy_id or "",
        policy_selection=selections[policy_selection],
        retained_kv_groups=retained_kv_groups or [],
        kv_cache_policy=None
        if kv_cache_policy is None
        else pb2.KvCachePolicy(**kv_cache_policy),
        **{field: source},
    )
    from .client import _GRPC_MAX_MESSAGE_SIZE_BYTES

    if request.ByteSize() > _GRPC_MAX_MESSAGE_SIZE_BYTES:
        raise ValueError(
            "Sampling submission exceeds the message limit; reduce the batch size"
        )
    deadline = time.monotonic() + timeout
    delay = 0.5
    while True:
        session._check_heartbeat_health()
        remaining = deadline - time.monotonic()
        if remaining <= 0:
            raise RiverTimeoutError("Sampling submission timed out")
        try:
            if policy_selection == "latest_snapshot":
                session._require_latest_snapshot_sampling()
            response = session._client._rpc(
                lambda remaining=remaining: session._live_stub.SubmitSamplingBatch(
                    request,
                    metadata=session._live_metadata,
                    timeout=min(30.0, remaining),
                ),
                context="Submitting independent samples",
            )
            ids = tuple(response.request_ids)
            if (
                len(ids) != len(source.prompts)
                or len(set(ids)) != len(ids)
                or any(not id for id in ids)
            ):
                raise RiverError("Invalid sampling batch acknowledgement")
            return ids
        except RiverConnectionError as error:
            if not session._client._enable_retries or error.status_code not in {
                "UNAVAILABLE",
                "DEADLINE_EXCEEDED",
                "ABORTED",
                "RESOURCE_EXHAUSTED",
            }:
                raise
            time.sleep(min(delay, max(0.0, deadline - time.monotonic())))
            delay = min(5.0, delay * 2)


@dataclass(frozen=True)
class SamplingCompletion:
    """One sample or failure, identified in the original prompt/sample grid."""

    prompt_index: int
    sample_index: int
    request_id: str
    sample: Sample | None = None
    error: Exception | None = None


@dataclass
class PendingSamplingBatch:
    """Independent operations accepted together; results arrive in completion order.

    ``as_completed`` reports failures per sample. Cancelling local waiting does
    not cancel accepted server operations. Retain request_ids to retrieve them.
    """

    request_ids: tuple[str, ...]
    _session: Any
    _deadline: float
    _parse_result: Callable[[int, Any], Sample]
    _num_samples: int
    _model_id: str | None = None
    _poll_interval: float = 0.1

    async def as_completed(
        self,
        *,
        executor: Executor | None = None,
        collector: SamplingResultCollector | None = None,
    ) -> AsyncIterator[SamplingCompletion]:
        """Consume independently; share a collector across concurrent batches."""
        owned = collector is None
        if collector is None:
            collector = SamplingResultCollector(executor=executor)
        futures = collector.register(self)
        indices = {future: index for index, future in enumerate(futures)}
        remaining = set(futures)
        try:
            while remaining:
                done, remaining = await asyncio.wait(
                    remaining, return_when=asyncio.FIRST_COMPLETED
                )
                for future in done:
                    index = indices[future]
                    try:
                        sample, error = future.result(), None
                    except Exception as exc:
                        sample, error = None, exc
                    yield SamplingCompletion(
                        index // self._num_samples,
                        index % self._num_samples,
                        self.request_ids[index],
                        sample,
                        error,
                    )
        finally:
            for future in futures:
                if not future.done():
                    future.cancel()
                elif not future.cancelled():
                    future.exception()  # consume failures if the iterator closed early
            collector.wake()
            if owned:
                await collector.aclose()


@dataclass
class _Entry:
    batch: PendingSamplingBatch
    index: int
    future: asyncio.Future
    next_poll: float = 0.0
    busy: bool = False
    retries: int = 0
    delay: float = 0.5


class SamplingResultCollector:
    """Coalesce result snapshots across batches on one event loop.

    At most max_poll_rpcs short streams run concurrently, each querying up to
    128 handles. Backpressure permits one decoded result buffered per stream.
    Executors are caller-owned; no thread is occupied between snapshots.
    """

    def __init__(self, *, executor: Executor | None = None, max_poll_rpcs: int = 4):
        if max_poll_rpcs < 1:
            raise ValueError("max_poll_rpcs must be positive")
        self.executor = executor
        self.max_poll_rpcs = max_poll_rpcs
        self._entries: dict[str, _Entry] = {}
        self._event = asyncio.Event()
        self._task = None
        self._closed = False
        self._next_heartbeat = {}
        self.snapshot_rpcs = 0
        self.polled_handles = 0

    def register(self, batch: PendingSamplingBatch) -> list[asyncio.Future]:
        if self._closed:
            raise RuntimeError("sampling collector is closed")
        if any(id in self._entries for id in batch.request_ids):
            raise ValueError("sample already registered with this collector")
        loop = asyncio.get_running_loop()
        futures = []
        for index, id in enumerate(batch.request_ids):
            future = loop.create_future()
            futures.append(future)
            self._entries[id] = _Entry(batch, index, future)
        if self._task is None:
            self._task = asyncio.create_task(self._run())
        self.wake()
        return futures

    def wake(self):
        self._event.set()

    async def aclose(self):
        self._closed = True
        if self._task is not None:
            self._task.cancel()
            await asyncio.gather(self._task, return_exceptions=True)
        for entry in self._entries.values():
            entry.future.cancel()
        self._entries.clear()

    async def _run(self):
        active = set()
        try:
            while True:
                self._event.clear()
                now = time.monotonic()
                for id, entry in list(self._entries.items()):
                    if not entry.future.done() and now >= entry.batch._deadline:
                        entry.future.set_exception(
                            RiverTimeoutError("Sampling timed out", request_id=id)
                        )
                    if entry.future.done():
                        del self._entries[id]
                active = {task for task in active if not task.done()}
                eligible: dict[tuple, dict[str, _Entry]] = {}
                for id, entry in self._entries.items():
                    if not entry.busy and entry.next_poll <= now:
                        key = (entry.batch._session, entry.batch._model_id)
                        eligible.setdefault(key, {})[id] = entry
                for entries in eligible.values():
                    items = list(entries.items())
                    for start in range(0, len(items), MAX_SAMPLING_BATCH):
                        if len(active) >= self.max_poll_rpcs:
                            break
                        chunk = dict(items[start : start + MAX_SAMPLING_BATCH])
                        for entry in chunk.values():
                            entry.busy = True
                        task = asyncio.create_task(self._snapshot(chunk))
                        task.add_done_callback(lambda completed: self.wake())
                        active.add(task)
                try:
                    await asyncio.wait_for(self._event.wait(), 0.05)
                except TimeoutError:
                    pass
        finally:
            for task in active:
                task.cancel()
            await asyncio.gather(*active, return_exceptions=True)

    async def _snapshot(self, entries: dict[str, _Entry]):
        loop = asyncio.get_running_loop()
        queue = asyncio.Queue(maxsize=1)
        stopped = threading.Event()
        calls = []
        session = next(iter(entries.values())).batch._session
        from .client import _HEARTBEAT_POLL_INTERVAL_SECS

        now = time.monotonic()
        next_heartbeat = self._next_heartbeat.setdefault(
            session, now + _HEARTBEAT_POLL_INTERVAL_SECS
        )
        heartbeat_due = now >= next_heartbeat
        if heartbeat_due:
            self._next_heartbeat[session] = now + _HEARTBEAT_POLL_INTERVAL_SECS
        self.snapshot_rpcs += 1
        self.polled_handles += len(entries)

        def emit(item):
            delivery = asyncio.run_coroutine_threadsafe(queue.put(item), loop)
            while not stopped.is_set():
                try:
                    delivery.result(timeout=0.1)
                    return
                except FutureTimeout:
                    pass
            delivery.cancel()

        def pump():
            if stopped.is_set():
                return
            from .client import _POLL_TERMINAL_STATUS_CODES

            seen = set()
            try:
                first = next(iter(entries.values()))
                session._check_heartbeat_health()
                if heartbeat_due:
                    session._attempt_heartbeat()
                if session._before_poll is not None:
                    session._before_poll()
                remaining = (
                    max(entry.batch._deadline for entry in entries.values())
                    - time.monotonic()
                )
                if remaining <= 0:
                    raise RiverTimeoutError(
                        "Sampling timed out before result retrieval"
                    )
                request = pb2.RetrieveSamplingResultsRequest(request_ids=list(entries))
                if first.batch._model_id is not None:
                    request.model_id = first.batch._model_id
                call = session._live_stub.RetrieveSamplingResults(
                    request,
                    metadata=session._live_metadata,
                    timeout=min(30.0, remaining),
                )
                calls.append(call)
                for item in call:
                    if stopped.is_set():
                        return
                    id = item.request_id
                    if id not in entries or id in seen:
                        raise RiverError(
                            "Invalid sampling snapshot: unknown or duplicate handle"
                        )
                    seen.add(id)
                    kind = item.WhichOneof("response")
                    if kind == "pending":
                        continue
                    try:
                        if kind == "failed":
                            raise RiverError(
                                f"{item.failed.error_category}: {item.failed.message}"
                            )
                        if kind == "error":
                            code = next(
                                (
                                    code.name
                                    for code in grpc.StatusCode
                                    if code.value[0] == item.error.code
                                ),
                                "UNKNOWN",
                            )
                            error = RiverConnectionError(
                                item.error.message, status_code=code
                            )
                            if code not in _POLL_TERMINAL_STATUS_CODES:
                                emit((id, None, error, True))
                                continue
                            raise error
                        if kind != "inference":
                            raise RiverError("Missing sampling result")
                        entry = entries[id]
                        sample = entry.batch._parse_result(entry.index, item.inference)
                        emit((id, sample, None, False))
                    except Exception as error:
                        emit((id, None, error, False))
                if len(seen) != len(entries):
                    raise RiverError("Incomplete sampling snapshot")
                emit((None, None, None, False))
            except grpc.RpcError as error:
                emit(
                    (
                        None,
                        None,
                        RiverConnectionError.from_grpc_error(
                            error, "Retrieving samples"
                        ),
                        True,
                    )
                )
            except Exception as error:
                emit((None, None, error, False))
            finally:
                for call in calls:
                    call.cancel()

        worker = loop.run_in_executor(self.executor, pump)
        retrying = set()
        try:
            while True:
                id, sample, error, retry = await queue.get()
                if id is None:
                    if error is not None:
                        for key, entry in entries.items():
                            if not entry.future.done():
                                self._fail_or_retry(entry, error, retry)
                                retrying.add(key)
                    break
                entry = entries[id]
                if not entry.future.done():
                    if error is None:
                        entry.future.set_result(sample)
                    else:
                        self._fail_or_retry(entry, error, retry)
                        retrying.add(id)
        except Exception as error:
            for entry in entries.values():
                if not entry.future.done():
                    entry.future.set_exception(error)
        finally:
            stopped.set()
            for call in calls:
                call.cancel()
            # The queue producer observes stopped even if cancellation happens
            # while it is blocked handing a result to a consumer that has gone.
            await asyncio.shield(worker)
            for id, entry in entries.items():
                entry.busy = False
                if id not in retrying:
                    entry.retries, entry.delay = 0, 0.5
                    entry.next_poll = time.monotonic() + entry.batch._poll_interval
            self.wake()

    @staticmethod
    def _fail_or_retry(entry, error, retry):
        from .client import (
            _POLL_MAX_RETRIES,
            _POLL_TERMINAL_STATUS_CODES,
            _is_transient_connection_error,
        )

        if (
            retry
            and isinstance(error, RiverConnectionError)
            and error.status_code not in _POLL_TERMINAL_STATUS_CODES
        ):
            if not _is_transient_connection_error(error):
                entry.retries += 1
            if entry.retries <= _POLL_MAX_RETRIES:
                entry.next_poll = time.monotonic() + entry.delay
                entry.delay = min(5.0, entry.delay * 2)
                return
        entry.future.set_exception(error)
