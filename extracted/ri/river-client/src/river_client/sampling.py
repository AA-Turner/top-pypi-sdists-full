"""Batched sampling admission and shared, bounded completion transport."""

from __future__ import annotations

import asyncio
import math
import time
import uuid
from collections.abc import AsyncIterator, Callable
from concurrent.futures import Executor
from dataclasses import dataclass
from typing import Any

import grpc

from ._proto import pb2, pb2_grpc
from .types import RiverConnectionError, RiverError, RiverTimeoutError, Sample

MAX_SAMPLING_BATCH = 128
# Default ceiling on concurrent result snapshots: 64 x 128 = 8,192 handles
# polled per sweep. Streams open only for handles that are due.
MAX_POLL_RPCS = 64
# Per-stream HTTP/2 read-ahead before gRPC's bandwidth-delay probe grows it:
# several typical results (0.3-1 MB with top-k logprobs) in one round trip.
STREAM_WINDOW_BYTES = 4 << 20
# gRPC reads channel arguments as C ints.
_MAX_STREAM_WINDOW_BYTES = 2**31 - 1
_STREAMS_PER_CONNECTION = 8
# Results a stream has read and handed to the executor but not yet settled.
_DECODE_AHEAD = 2


def _submission_request(
    source,
    *,
    timeout: float,
    idempotency_key: str | None = None,
    pinned_policy_id: str | None = None,
    policy_selection: str = "ordered",
    retained_kv_groups: list[str] | None = None,
    kv_cache_policy: dict | None = None,
) -> pb2.SubmitSamplingBatchRequest:
    """Build and validate the envelope shared by both sampling transports."""
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
    return request


def _acknowledged_ids(response, source):
    ids = tuple(response.request_ids)
    if (
        len(ids) != len(source.prompts)
        or len(set(ids)) != len(ids)
        or any(not id for id in ids)
    ):
        raise RiverError("Invalid sampling batch acknowledgement")
    return ids


_SUBMISSION_RETRY_CODES = {
    "UNAVAILABLE",
    "DEADLINE_EXCEEDED",
    "ABORTED",
    "RESOURCE_EXHAUSTED",
}


def submit_batch(session, source, *, timeout, **kwargs) -> tuple[str, ...]:
    """Retry the same immutable admission envelope, including a lost ack."""
    request = _submission_request(source, timeout=timeout, **kwargs)
    deadline = time.monotonic() + timeout
    delay = 0.5
    while True:
        session._check_heartbeat_health()
        remaining = deadline - time.monotonic()
        if remaining <= 0:
            raise RiverTimeoutError("Sampling submission timed out")
        try:
            if (
                request.policy_selection
                == pb2.SAMPLING_POLICY_SELECTION_LATEST_SNAPSHOT
            ):
                session._require_latest_snapshot_sampling()
            response = session._client._rpc(
                lambda remaining=remaining: session._live_stub.SubmitSamplingBatch(
                    request,
                    metadata=session._live_metadata,
                    timeout=min(30.0, remaining),
                ),
                context="Submitting independent samples",
            )
            return _acknowledged_ids(response, source)
        except RiverConnectionError as error:
            if (
                not session._client._enable_retries
                or error.status_code not in _SUBMISSION_RETRY_CODES
            ):
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
        indices = {
            future: index for index, future in enumerate(collector.register(self))
        }
        remaining = set(indices)

        def completion(future):
            index = indices.pop(future)
            try:
                sample, error = future.result(), None
            except Exception as exc:
                sample, error = None, exc
            return SamplingCompletion(
                index // self._num_samples,
                index % self._num_samples,
                self.request_ids[index],
                sample,
                error,
            )

        try:
            while remaining:
                done, remaining = await asyncio.wait(
                    remaining, return_when=asyncio.FIRST_COMPLETED
                )
                while done:
                    yield completion(done.pop())
        finally:
            for future in indices:
                if not future.done():
                    future.cancel()
                elif not future.cancelled():
                    future.exception()  # consume failures if the iterator closed early
            collector.wake()
            if owned:
                await collector.aclose()


@dataclass
class _Connection:
    channel: Any
    stub: Any
    streams: int = 0


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

    Each snapshot is a short stream querying up to 128 handles, and one opens
    for every 128 handles due for a poll, up to max_poll_rpcs at once, so by
    default every outstanding handle is asked after in one sweep. Streams
    spread over connections of at most eight streams each. Each stream reads
    on while the result before it decodes on the executor.
    Channels are owned by this collector; executors are caller-owned and only
    run preparation, decoding, and synchronous hooks, never sampling RPC waits.

    The defaults assume a client with the memory and bandwidth to take every
    finished result at once. Each stream buffers up to stream_window_bytes
    gRPC has received but the collector has not read (gRPC's bandwidth probe
    may grow this on a fast link, within its memory quota) and up to two
    results waiting on the executor, so memory peaks near max_poll_rpcs x
    (window + 2 results): 64 x (4 MiB + 2 x 10 MB) is about 1.5 GB for
    10 MB results at 32k generated tokens, about 0.3 GB for 0.6 MB results.
    Lower max_poll_rpcs, or stream_window_bytes, only on a client that cannot
    afford that.
    """

    def __init__(
        self,
        *,
        executor: Executor | None = None,
        max_poll_rpcs: int = MAX_POLL_RPCS,
        stream_window_bytes: int = STREAM_WINDOW_BYTES,
    ):
        if type(max_poll_rpcs) is not int or max_poll_rpcs < 1:
            raise ValueError("max_poll_rpcs must be a positive integer")
        if (
            type(stream_window_bytes) is not int
            or not 0 < stream_window_bytes <= _MAX_STREAM_WINDOW_BYTES
        ):
            raise ValueError(
                f"stream_window_bytes must be an integer in 1..{_MAX_STREAM_WINDOW_BYTES}"
            )
        self.executor = executor
        self.max_poll_rpcs = max_poll_rpcs
        self.stream_window_bytes = stream_window_bytes
        self._connections: dict[Any, list[_Connection]] = {}
        self._latest_snapshot_capable = set()
        self._entries: dict[str, _Entry] = {}
        self._event = asyncio.Event()
        self._task = None
        self._closed = False
        self.snapshot_rpcs = 0
        self.polled_handles = 0

    def _connection(self, session, *, stream=False) -> _Connection:
        """Submissions use a client's first connection; a snapshot the least busy.

        Each connection is its own channel with a local subchannel pool, so it
        owns a TCP connection instead of sharing one by target.
        """
        if self._closed:
            raise RuntimeError("sampling collector is closed")
        connections = self._connections.setdefault(session._client, [])
        if stream and connections:
            least = min(connections, key=lambda connection: connection.streams)
            if least.streams < _STREAMS_PER_CONNECTION:
                return least
        elif connections:
            return connections[0]
        channel = session._client._new_async_channel(
            (
                ("grpc.use_local_subchannel_pool", 1),
                ("grpc.http2.lookahead_bytes", self.stream_window_bytes),
            )
        )
        connections.append(_Connection(channel, pb2_grpc.RiverServiceStub(channel)))
        return connections[-1]

    async def submit(self, session, source, *, timeout, **kwargs):
        request = _submission_request(source, timeout=timeout, **kwargs)
        stub = self._connection(session).stub
        deadline = time.monotonic() + timeout
        delay = 0.5
        while True:
            session._check_heartbeat_health()
            remaining = deadline - time.monotonic()
            if remaining <= 0:
                raise RiverTimeoutError("Sampling submission timed out")
            try:
                if (
                    request.policy_selection
                    == pb2.SAMPLING_POLICY_SELECTION_LATEST_SNAPSHOT
                    and stub not in self._latest_snapshot_capable
                ):
                    capabilities = await stub.GetServerCapabilities(
                        pb2.GetServerCapabilitiesRequest(),
                        metadata=session._live_metadata,
                        timeout=min(30.0, remaining),
                    )
                    if "sampling_latest_snapshot_v1" not in capabilities.features:
                        raise RiverError("Server requires sampling_latest_snapshot_v1")
                    self._latest_snapshot_capable.add(stub)
                    continue  # Recompute the remaining deadline after negotiation.
                response = await stub.SubmitSamplingBatch(
                    request,
                    metadata=session._live_metadata,
                    timeout=min(30.0, remaining),
                )
                return _acknowledged_ids(response, source)
            except grpc.RpcError as error:
                error = RiverConnectionError.from_grpc_error(
                    error, "Submitting independent samples"
                )
                if (
                    not session._client._enable_retries
                    or error.status_code not in _SUBMISSION_RETRY_CODES
                ):
                    raise error from None
                await asyncio.sleep(min(delay, max(0.0, deadline - time.monotonic())))
                delay = min(5.0, delay * 2)

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
        await asyncio.gather(
            *(
                connection.channel.close()
                for connections in self._connections.values()
                for connection in connections
            )
        )
        self._connections.clear()
        self._latest_snapshot_capable.clear()

    async def _run(self):
        active = set()
        try:
            while True:
                self._event.clear()
                active = {task for task in active if not task.done()}
                self._poll_due(active)
                try:
                    await asyncio.wait_for(self._event.wait(), 0.05)
                except TimeoutError:
                    pass
        finally:
            for task in active:
                task.cancel()
            await asyncio.gather(*active, return_exceptions=True)

    def _poll_due(self, active):
        # Scheduling locals must not retain completed futures across RPC waits.
        now = time.monotonic()
        for id, entry in list(self._entries.items()):
            if not entry.future.done() and now >= entry.batch._deadline:
                entry.future.set_exception(
                    RiverTimeoutError("Sampling timed out", request_id=id)
                )
            if entry.future.done():
                del self._entries[id]
        eligible: dict[tuple, dict[str, _Entry]] = {}
        # Due retries must not starve samples that have never been polled,
        # including when a slow snapshot outlasts the polling interval.
        for id, entry in sorted(
            self._entries.items(), key=lambda item: item[1].next_poll
        ):
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

    async def _snapshot(self, entries: dict[str, _Entry]):
        loop = asyncio.get_running_loop()
        session = next(iter(entries.values())).batch._session
        self.snapshot_rpcs += 1
        self.polled_handles += len(entries)

        from .client import _POLL_TERMINAL_STATUS_CODES

        seen, retrying = set(), set()
        call = connection = None
        # Results read from the stream and not yet settled; each settles as
        # soon as its decode finishes, even while the stream waits.
        decoding: set[asyncio.Task] = set()
        try:
            model_id = next(iter(entries.values())).batch._model_id
            session._check_heartbeat_health()
            if session._before_poll is not None:
                await loop.run_in_executor(self.executor, session._before_poll)
            remaining = (
                max(entry.batch._deadline for entry in entries.values())
                - time.monotonic()
            )
            if remaining <= 0:
                raise RiverTimeoutError("Sampling timed out before result retrieval")
            request = pb2.RetrieveSamplingResultsRequest(request_ids=list(entries))
            if model_id is not None:
                request.model_id = model_id
            connection = self._connection(session, stream=True)
            connection.streams += 1
            call = connection.stub.RetrieveSamplingResults(
                request,
                metadata=session._live_metadata,
                timeout=min(30.0, remaining),
            )
            async for item in call:
                id = item.request_id
                if id not in entries or id in seen:
                    raise RiverError(
                        "Invalid sampling snapshot: unknown or duplicate handle"
                    )
                seen.add(id)
                kind = item.WhichOneof("response")
                if kind == "pending":
                    continue
                entry = entries[id]
                if entry.future.done():
                    del entries[id], entry, item
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
                            self._fail_or_retry(entry, error, True)
                            retrying.add(id)
                            continue
                        raise error
                    if kind != "inference":
                        raise RiverError("Missing sampling result")
                    # Keep reading while earlier results decode, but bound how
                    # many a stream holds to retain backpressure.
                    decoding.add(
                        asyncio.create_task(
                            self._settle(
                                entries,
                                id,
                                entry,
                                loop.run_in_executor(
                                    self.executor,
                                    entry.batch._parse_result,
                                    entry.index,
                                    item.inference,
                                ),
                            )
                        )
                    )
                except Exception as error:
                    if not entry.future.done():
                        entry.future.set_exception(error)
                finally:
                    if entry.future.done():
                        del entries[id]
                        self.wake()
                    del entry, item
                if len(decoding) >= _DECODE_AHEAD:
                    _, decoding = await asyncio.wait(
                        decoding, return_when=asyncio.FIRST_COMPLETED
                    )
            await asyncio.gather(*decoding)
            if len(seen) != len(request.request_ids):
                raise RiverError("Incomplete sampling snapshot")
        except Exception as error:
            # Results already read are delivered, not retried.
            await asyncio.gather(*decoding)
            retry = isinstance(error, grpc.RpcError)
            if retry:
                error = RiverConnectionError.from_grpc_error(
                    error, "Retrieving samples"
                )
            for id, entry in entries.items():
                if not entry.future.done():
                    self._fail_or_retry(entry, error, retry)
                    retrying.add(id)
        finally:
            for task in decoding:
                task.cancel()
            await asyncio.gather(*decoding, return_exceptions=True)
            decoding.clear()
            if call is not None:
                call.cancel()
            if connection is not None:
                connection.streams -= 1
            for id, entry in entries.items():
                entry.busy = False
                if id not in retrying:
                    entry.retries, entry.delay = 0, 0.5
                    entry.next_poll = time.monotonic() + entry.batch._poll_interval
            self.wake()

    async def _settle(self, entries, id, entry, decode):
        try:
            sample = await decode
        except Exception as error:
            if not entry.future.done():
                entry.future.set_exception(error)
        else:
            if not entry.future.done():
                entry.future.set_result(sample)
            del sample
        finally:
            if entry.future.done():
                entries.pop(id, None)
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
