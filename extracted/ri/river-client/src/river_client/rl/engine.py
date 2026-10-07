"""Global turn/segment batching with bounded RPC and environment concurrency."""

from __future__ import annotations

import asyncio
import copy
import hashlib
import heapq
import inspect
import math
import time
import uuid
import warnings
from concurrent.futures import ThreadPoolExecutor
from contextlib import asynccontextmanager
from dataclasses import dataclass, field
from functools import partial

from river_client.client import (
    _IMAGE_PAD_TOKEN_CANDIDATES,
    _image_placeholder_token_id,
    _submit_sampling_batch_async,
)
from river_client.images import ImageHandle
from river_client.renderers import Renderer
from river_client.sampling import MAX_SAMPLING_BATCH, SamplingResultCollector

from .config import Budget, GroupCompletion, KVCache, Schedule, _integer
from .env import Env, InfrastructureError, elide_middle
from .progress import Activities
from .rendering import continuation_chunks, prompt_chunks, sample_stop
from .trajectory import Trajectory, decode_state, encode_state


async def call(function, *args, **kwargs):
    """Adapt today's blocking primitives without one thread per trajectory."""
    if inspect.iscoroutinefunction(function):
        return await function(*args, **kwargs)
    return await asyncio.to_thread(function, *args, **kwargs)


class _RolloutStopped(Exception):
    pass


def _image_placeholder(tokenizer):
    """Return a multimodal tokenizer's image placeholder as ``(id, text)``.

    Returns ``(None, None)`` for a text-only tokenizer, in which the client
    resolver finds no placeholder.
    """
    convert = getattr(tokenizer, "convert_tokens_to_ids", None)
    if not callable(convert):
        return None, None
    try:
        token_id = _image_placeholder_token_id(tokenizer)
    except ValueError:
        return None, None
    for text in _IMAGE_PAD_TOKEN_CANDIDATES:  # the candidate the resolver matched
        try:
            if convert(text) == token_id:
                return token_id, text
        except (KeyError, ValueError):
            continue
    return token_id, None


def _message_texts(messages):
    """Yield the free text of chat messages that renderers render.

    String content, text parts, thinking parts and ``reasoning_content``:
    DeepSeek V4.1's renderer refuses the image placeholder in any of them,
    including the reasoning of past assistant turns.
    """
    for message in messages:
        reasoning = message.get("reasoning_content")
        if isinstance(reasoning, str):
            yield reasoning
        content = message.get("content")
        if isinstance(content, str):
            yield content
        elif isinstance(content, list):
            for part in content:
                if not isinstance(part, dict):
                    continue
                for key in ("text", "thinking"):
                    if isinstance(part.get(key), str):
                        yield part[key]


class _PrioritySlots:
    """Bound whole trajectories without making older reservations wait behind newer ones."""

    def __init__(self, capacity):
        self.available = capacity
        self.waiters = []
        self.counter = 0

    def _wake(self):
        while self.available and self.waiters:
            future = heapq.heappop(self.waiters)[2]
            if not future.done():
                self.available -= 1
                future.set_result(None)

    @asynccontextmanager
    async def hold(self, priority):
        future = asyncio.get_running_loop().create_future()
        heapq.heappush(self.waiters, (priority, self.counter, future))
        self.counter += 1
        self._wake()
        try:
            await future
        except BaseException:
            # Cancellation after a grant must return its reserved permit too.
            if not future.cancelled():
                self.available += 1
            self._wake()
            raise
        try:
            yield
        finally:
            self.available += 1
            self._wake()


@dataclass
class CompletedGroup:
    """Rollout trajectories collected for one dataset row.

    Attributes:
        id: Group identifier.
        row: Source dataset row.
        trajectories: Completed or truncated member trajectories.
        final: Whether this group has no further members to emit.
        closed_by_deadline: Whether the group's token deadline ended collection.
        wait_seconds: Time spent waiting for the group to complete.
    """

    id: str
    row: object
    trajectories: list[Trajectory]
    final: bool = True
    closed_by_deadline: bool = False
    wait_seconds: float = 0.0


@dataclass
class _Member:
    seed: int
    traj: Trajectory | None = None
    env: Env | None = None
    stop: asyncio.Event = field(default_factory=asyncio.Event)
    lock: asyncio.Lock = field(default_factory=asyncio.Lock)
    cause: str | None = None
    recovery_state: object = None
    # Loaded from a checkpoint but not yet restored into a live environment.
    restore_pending: bool = False
    started: float | None = None


@dataclass
class _Group:
    id: str
    row: object
    members: list[_Member]
    completion: GroupCompletion
    priority: int = 0
    admission_order: int = 0
    changed: asyncio.Event = field(default_factory=asyncio.Event)
    elapsed: float = 0.0
    quorum_elapsed: float | None = None
    quorum_tokens: list[int] = field(default_factory=list)
    emitted: set[int] = field(default_factory=set)
    closed: bool = False
    finished: bool = False
    task: asyncio.Task | None = None
    started: float | None = None


@dataclass
class _Request:
    member: _Member
    cap: int
    future: asyncio.Future
    prompt: list[dict]
    seed: int
    expected_length: int
    images: bool
    priority: float
    queued_at: float = field(default_factory=time.monotonic)

    @property
    def pinned_policy_id(self):
        for span in self.member.traj.spans:
            if span.kind == "generated":
                return None if span.policy_version is None else span.policy_version.id
        return None

    @property
    def previous_policy_id(self):
        for span in reversed(
            self.member.traj.spans[self.member.traj._kv_cache_start :]
        ):
            if span.kind == "generated":
                return None if span.policy_version is None else span.policy_version.id
        return None

    @property
    def kv_anchor_id(self):
        for span in reversed(
            self.member.traj.spans[self.member.traj._kv_cache_start :]
        ):
            if span.kind == "generated":
                return (
                    None
                    if span.kv_cache_policy_version is None
                    else span.kv_cache_policy_version.id
                )
        return None

    @property
    def estimated_bytes(self):
        # Include bytes materialized at ingress, even for compact wire handles.
        # Token ids use a conservative eight-byte estimate plus prompt overhead.
        return 256 + sum(
            8 * len(chunk["tokens"])
            if chunk["type"] == "text"
            else chunk["data"].byte_count
            if isinstance(chunk["data"], ImageHandle)
            else len(chunk["data"])
            for chunk in self.prompt
        )


# Frozen configuration values are safe to share as defaults.
_DEFAULT_BUDGET = Budget()
_DEFAULT_SCHEDULE = Schedule()
_DEFAULT_KV_CACHE = KVCache()


class RolloutEngine:
    """Generate multi-turn trajectories from an environment and sampling model.

    Coordinates rollout groups, sampling concurrency, and policy/KV-cache
    continuity. Use it directly for custom algorithms or pass it to
    ``AsyncTrainer`` for managed training.
    """

    def __init__(
        self,
        model,
        *,
        env,
        renderer,
        budget: Budget = _DEFAULT_BUDGET,
        schedule: Schedule = _DEFAULT_SCHEDULE,
        sampling_policy: str = "trajectory",
        kv_cache: KVCache = _DEFAULT_KV_CACHE,
        temperature: float = 1.0,
        top_p: float = 1.0,
        top_k: int = -1,
        seed: int = 0,
        sample_timeout: float = 1800.0,
        environment_timeout: float | None = None,
        return_expert_routing: bool = False,
    ):
        """Configure rollout generation.

        Args:
            model: Training model or checkpoint-pinned sampler.
            env: ``Env`` instance for stateless tasks, or a factory that makes
                one instance per trajectory for stateful tasks. A shared
                instance must manage its own state by trajectory id.
            renderer: Model-specific chat renderer that supports continuation.
            budget: Per-trajectory token, turn, and image limits.
            schedule: Client-side admission and sampling submission limits.
            sampling_policy: ``"trajectory"`` pins one policy for every turn;
                ``"segment"`` allows a newer policy between turns.
            kv_cache: Maximum retained KV age and behavior at that limit.
            temperature: Sampling temperature; training requires a positive value.
            top_p: Nucleus sampling threshold.
            top_k: Top-k sampling limit; -1 disables it.
            seed: Base sampling seed.
            sample_timeout: Timeout for one sampling request in seconds.
            environment_timeout: Optional timeout for an environment call in seconds.
            return_expert_routing: Request expert routing for supported models.
        """
        if not inspect.iscoroutinefunction(getattr(model, "sample", None)) and not any(
            callable(getattr(model, name, None))
            for name in ("submit_sample", "submit_sampling_batch")
        ):
            raise TypeError(
                "sampler must provide submit_sampling_batch(), submit_sample() or an async sample()"
            )
        if sampling_policy not in {"trajectory", "segment"}:
            raise ValueError("sampling_policy must be trajectory or segment")
        if not isinstance(kv_cache, KVCache):
            raise TypeError(
                "kv_cache must be rl.KVCache(max_staleness=..., on_limit=...)"
            )
        kv_cache.validate_sampling_policy(sampling_policy)
        self._retained_kv = sampling_policy == "segment" and kv_cache.max_staleness > 0
        self.kv_cache = kv_cache
        self.sampling_policy = sampling_policy
        self._latest_snapshot_sampling = (
            sampling_policy == "segment"
            and getattr(model, "checkpoint", None) is None
            and callable(getattr(model, "submit_sampling_batch", None))
        )
        stops = renderer.get_stop_strings()
        if not stops or any(not stop for stop in stops):
            raise ValueError("RL requires nonempty renderer stop strings")
        continuation = getattr(renderer, "build_continuation_prompt", None)
        if (
            continuation is None
            or getattr(continuation, "__func__", None)
            is Renderer.build_continuation_prompt
        ):
            raise ValueError(
                "renderer must implement build_continuation_prompt for token-exact RL"
            )
        if environment_timeout is not None and (
            not math.isfinite(environment_timeout) or environment_timeout <= 0
        ):
            raise ValueError("environment_timeout must be finite and positive, or None")
        if temperature < 0 or not math.isfinite(temperature):
            raise ValueError("sampling requires a finite nonnegative temperature")
        _integer(top_k, "top_k", -1)
        _integer(seed, "seed", None)
        if (
            not 0 < top_p <= 1
            or not math.isfinite(sample_timeout)
            or sample_timeout <= 0
        ):
            raise ValueError("invalid sampling configuration")
        if type(return_expert_routing) is not bool:
            raise TypeError("return_expert_routing must be a boolean")
        self.return_expert_routing = return_expert_routing
        self.model, self.env, self.renderer = model, env, renderer
        # Only image chunks may carry the image placeholder. The API rejects a
        # whole sampling batch over one stray placeholder, and training must not
        # see one in text, so a sampled placeholder id, or environment text that
        # carries the placeholder, ends only its own rollout. Text-only tokenizers
        # resolve to None, which disables the checks.
        self._image_placeholder_id, self._image_placeholder_text = _image_placeholder(
            getattr(renderer, "tokenizer", None)
        )
        self.budget, self.schedule = budget, schedule
        self.temperature, self.top_p, self.top_k = temperature, top_p, top_k
        self.seed, self.sample_timeout = seed, sample_timeout
        self.environment_timeout = environment_timeout
        self.length_history: dict[str, float] = {}
        self._groups: dict[str, _Group] = {}
        self._ready = None
        self._completed = None
        self._dispatcher = None
        self.server_capabilities = None
        self._batches: set[asyncio.Task] = set()
        self._counter = 0
        self._outbox: list[CompletedGroup] = []
        self._started_at = 0.0
        self._stopped_at = None
        self._activities = Activities()
        self.recovery_metrics = {
            "trajectories_recovered": 0,
            "kv_generations_restarted": 0,
            "trajectories_dropped_on_resume": 0,
        }

    async def __aenter__(self):
        if self._dispatcher is not None:
            raise RuntimeError("engine is already running")
        read = getattr(self.model, "get_server_capabilities", None)
        self.server_capabilities = await call(read) if read is not None else None
        if self.server_capabilities is not None:
            self.server_capabilities.require("sampling_batch_v1")
            if self.sampling_policy == "trajectory":
                self.server_capabilities.require(
                    "policy_versions_v1", "sampling_policy_pinning_v1"
                )
            if self._latest_snapshot_sampling:
                self.server_capabilities.require("sampling_latest_snapshot_v1")
            if self._retained_kv:
                self.server_capabilities.require("policy_versions_v1")
                self.server_capabilities.require_model(
                    self.model.base_model, "retained_kv_v1", "bounded_kv_v1"
                )
        self._ready, self._completed = asyncio.PriorityQueue(), asyncio.Queue()
        self._ready_counter = 0
        self._slots = _PrioritySlots(self.schedule.concurrency)
        self._operation_slots = asyncio.Semaphore(self.schedule.sample_request_limit)
        self._pool = ThreadPoolExecutor(
            max_workers=self.schedule.max_rpc_workers,
            thread_name_prefix="river-rl-sample",
        )
        self._independent_samples = callable(
            getattr(self.model, "submit_sampling_batch", None)
        )
        self._collector = SamplingResultCollector(
            executor=self._pool,
            max_poll_rpcs=max(1, min(4, self.schedule.max_rpc_workers // 2)),
        )
        self._sampling = {
            "requests": 0,
            "prompts": 0,
            "submitted_requests": 0,
            "submit_seconds": 0.0,
            "generated_tokens": 0,
            "prompt_tokens": 0,
            "cached_prompt_tokens": 0,
            "kv_refreshes": 0,
            "queue_seconds": 0.0,
            "request_seconds": 0.0,
            "inflight_requests": 0,
            "inflight_prompts": 0,
            "peak_inflight_prompts": 0,
            "peak_batch_bytes_estimate": 0,
        }
        self._activities = Activities()
        self._stopped_at = None
        self._started_at = time.monotonic()
        self._dispatcher = asyncio.create_task(self._dispatch())
        return self

    async def __aexit__(self, exc_type, exc, tb):
        tasks = [g.task for g in self._groups.values() if g.task is not None]
        tasks += list(self._batches) + [self._dispatcher]
        for task in tasks:
            task.cancel()
        try:
            await asyncio.gather(*tasks, return_exceptions=True)
            await self._collector.aclose()
        finally:
            self._pool.shutdown(wait=False, cancel_futures=True)
            self._dispatcher = None
            self._groups.clear()
            self._stopped_at = time.monotonic()

    def submit(
        self,
        row,
        *,
        group_size: int,
        completion: GroupCompletion,
        id: str | None = None,
        priority: int = 0,
    ):
        """Start a rollout group for one dataset row and return its group id.

        Call inside ``async with engine``. Each member gets an independent
        sampling seed. Lower priorities start first at both trajectory admission
        and sampling; ties at admission follow the original group submission order.
        Running trajectories are never preempted.
        """
        if self._dispatcher is None:
            raise RuntimeError("use 'async with engine' before submit")
        _integer(group_size, "group_size", 1)
        if completion.min_members > group_size:
            raise ValueError("group_size must be positive and at least min_members")
        if completion.on_stragglers == "discard" and completion.mode == "deadline":
            warnings.warn(
                "discarding deadline stragglers biases training toward faster trajectories",
                stacklevel=2,
            )
        group_id = id or f"{self._counter}:{uuid.uuid4().hex}"
        if group_id in self._groups:
            raise ValueError("duplicate rollout group id")
        # No shared seed within a group; segment seeds also advance on resume.
        base = (self.seed + self._counter * 1000003) % (2**31)
        admission_order = self._counter
        self._counter += 1
        group = _Group(
            group_id,
            copy.deepcopy(row),
            [_Member((base + i) % (2**31)) for i in range(group_size)],
            completion,
            priority=priority,
            admission_order=admission_order,
        )
        self._groups[group_id] = group
        group.task = asyncio.create_task(self._run_group(group))
        return group_id

    def resubmit(self, group_id, row):
        """Start a fresh stage of a consumed, complete group in its original queue position.

        Membership size, completion policy, id and priority are retained; sampling
        seeds are fresh. The caller must first accept all results from this group.
        Replacement is synchronous so checkpoints cannot capture a missing group.
        """
        previous = self._groups[group_id]
        if any(result.id == group_id for result in self._outbox):
            raise RuntimeError("cannot resubmit a group with unconsumed results")
        self.acknowledge(group_id)
        self.submit(
            row,
            group_size=len(previous.members),
            completion=previous.completion,
            id=group_id,
            priority=previous.priority,
        )
        self._groups[group_id].admission_order = previous.admission_order
        return group_id

    async def next_group(self) -> CompletedGroup:
        """Wait for the next completed group or deadline partial result."""
        result = await self._completed.get()
        if isinstance(result, Exception):
            raise result
        return result

    def accept(self, result):
        """Mark a delivered result as consumed by the caller."""
        self._outbox.remove(result)

    def _emit(self, result):
        self._outbox.append(result)
        self._completed.put_nowait(result)

    def acknowledge(self, group_id):
        """Release a group only after all of its emitted portions are consumed."""
        group = self._groups.get(group_id)
        if group is None:
            return
        if not group.finished and not all(
            m.traj is not None and m.traj.done for m in group.members
        ):
            raise RuntimeError("cannot acknowledge an unfinished group")
        del self._groups[group_id]

    async def rollout(self, rows, *, group_size: int, completion: GroupCompletion):
        """Yield completed trajectory groups; custom algorithms can own updates."""
        async with self:
            iterator, exhausted, active = iter(rows), False, set()
            capacity = max(1, self.schedule.concurrency // group_size)
            while active or not exhausted:
                while not exhausted and len(active) < capacity:
                    try:
                        row = next(iterator)
                    except StopIteration:
                        exhausted = True
                        break
                    active.add(
                        self.submit(row, group_size=group_size, completion=completion)
                    )
                if not active:
                    break
                result = await self.next_group()
                self.accept(result)
                if result.trajectories:
                    yield result.trajectories
                if result.final:
                    active.remove(result.id)
                    self.acknowledge(result.id)

    def _env_instance(self):
        env = self.env if isinstance(self.env, Env) else self.env()
        if not isinstance(env, Env) or env.recovery not in {
            "drop",
            "stateless",
            "snapshot",
        }:
            raise TypeError(
                "env must be an Env instance or factory with a valid recovery contract"
            )
        names = [t.spec["name"] for t in env.tools]
        if len(names) != len(set(names)):
            raise ValueError("environment tool names must be unique")
        return env

    def progress(self):
        """Return current rollout and environment activity counters.

        Operation seconds include in-flight work and sum across concurrent
        calls. They must not be added together as elapsed wall-clock time.
        """
        return {
            "running": self._dispatcher is not None,
            "groups": len(self._groups),
            "sampling": self.sampling_metrics() if self._started_at else {},
            "environment": self._activities.snapshot(),
        }

    def sampling_metrics(self):
        """Cumulative sampling counters and current admission pressure."""
        return {
            **self._sampling,
            "ready_prompts": self._ready.qsize(),
            "max_sample_requests": self.schedule.sample_request_limit,
            "max_rpc_workers": self.schedule.max_rpc_workers,
            "max_batch": self.schedule.max_batch,
            "max_batch_bytes": self.schedule.max_batch_bytes,
            "completion_rpcs": self._collector.snapshot_rpcs,
            "polled_handles": self._collector.polled_handles,
            "elapsed_seconds": (self._stopped_at or time.monotonic())
            - self._started_at,
        }

    async def _dispatch(self):
        while True:
            # Native transport admission counts outstanding prompts, not RPCs.
            # Completed prompts release capacity immediately for continuations.
            await self._operation_slots.acquire()
            transferred = False
            deferred = []
            try:
                first = (await self._ready.get())[2]
                requests = [first]
                batch_bytes = first.estimated_bytes
                deadline = time.monotonic() + self.schedule.window
                batch_limit = (
                    min(self.schedule.max_batch, MAX_SAMPLING_BATCH)
                    if self._independent_samples
                    else self.schedule.max_batch
                )
                while (
                    len(requests) < batch_limit
                    and batch_bytes < self.schedule.max_batch_bytes
                    and (
                        not self._independent_samples
                        or not self._operation_slots.locked()
                    )
                ):
                    try:
                        item = self._ready.get_nowait()
                    except asyncio.QueueEmpty:
                        remaining = deadline - time.monotonic()
                        if remaining <= 0:
                            break
                        try:
                            item = await asyncio.wait_for(self._ready.get(), remaining)
                        except TimeoutError:
                            break
                    request = item[2]
                    if request.future.cancelled():
                        continue
                    if request.cap == first.cap and (
                        (
                            self.sampling_policy == "segment"
                            and (
                                not self._retained_kv
                                or (request.kv_anchor_id, request.previous_policy_id)
                                == (first.kv_anchor_id, first.previous_policy_id)
                            )
                        )
                        or (
                            self.sampling_policy == "trajectory"
                            and request.pinned_policy_id == first.pinned_policy_id
                        )
                    ):
                        request_bytes = request.estimated_bytes
                        if batch_bytes + request_bytes > self.schedule.max_batch_bytes:
                            deferred.append(item)
                            break
                        batch_bytes += request_bytes
                        requests.append(request)
                        if self._independent_samples:
                            await self._operation_slots.acquire()
                    else:
                        deferred.append(item)
                if self._independent_samples:
                    for request in requests:
                        request.future.add_done_callback(self._release_sample_slot)
                task = asyncio.create_task(self._sample(requests))
                self._batches.add(task)
                task.add_done_callback(self._sample_finished)
                transferred = True
            finally:
                for item in deferred:
                    self._ready.put_nowait(item)
                if not transferred:
                    self._operation_slots.release()

    def _release_sample_slot(self, future):
        self._operation_slots.release()

    def _sample_finished(self, task):
        self._batches.discard(task)
        if not self._independent_samples:
            self._operation_slots.release()

    async def _sample(self, requests):
        started = None
        count = 0
        try:
            for request in requests:
                if request.member.cause and not request.future.done():
                    request.future.set_exception(_RolloutStopped())
            requests = [r for r in requests if not r.future.done()]
            if not requests:
                return
            started = time.monotonic()
            count = len(requests)
            self._sampling["requests"] += 1
            self._sampling["prompts"] += count
            self._sampling["peak_batch_bytes_estimate"] = max(
                self._sampling["peak_batch_bytes_estimate"],
                sum(request.estimated_bytes for request in requests),
            )
            self._sampling["queue_seconds"] += sum(
                started - r.queued_at for r in requests
            )
            self._sampling["inflight_requests"] += 1
            self._sampling["inflight_prompts"] += count
            self._sampling["peak_inflight_prompts"] = max(
                self._sampling["peak_inflight_prompts"],
                self._sampling["inflight_prompts"],
            )
            kwargs = {
                "model_input": [r.prompt for r in requests],
                "num_samples": 1,
                "max_tokens": requests[0].cap,
                "temperature": self.temperature,
                "top_p": self.top_p,
                "top_k": self.top_k,
                "stop": self.renderer.get_stop_strings(),
                "seeds": [r.seed for r in requests],
                "return_prompt_token_ids": any(r.images for r in requests),
                "timeout": self.sample_timeout,
            }
            if self.return_expert_routing:
                kwargs["return_expert_routing"] = True
            if self._retained_kv:
                kwargs["retained_kv_groups"] = [
                    r.member.traj._kv_cache_group for r in requests
                ]
                kwargs["kv_cache_policy"] = {
                    "max_staleness": self.kv_cache.max_staleness,
                    "anchor_policy_id": requests[0].kv_anchor_id or "",
                    "previous_policy_id": requests[0].previous_policy_id or "",
                    "refill_on_limit": self.kv_cache.on_limit == "refill",
                }
            if (
                self.sampling_policy == "trajectory"
                and requests[0].pinned_policy_id
                and getattr(self.model, "checkpoint", None) is None
            ):
                kwargs["pinned_policy_id"] = requests[0].pinned_policy_id
            elif self._latest_snapshot_sampling:
                # Select a snapshot on the first turn; trajectory continuations
                # keep its explicit pin instead of selecting newer weights.
                kwargs["policy_selection"] = "latest_snapshot"
            if self._independent_samples:
                pending = await _submit_sampling_batch_async(
                    self.model.submit_sampling_batch, self._collector, **kwargs
                )
                self._sampling["submitted_requests"] += 1
                self._sampling["submit_seconds"] += time.monotonic() - started
                async for completion in pending.as_completed(collector=self._collector):
                    request = requests[completion.prompt_index]
                    try:
                        if completion.error is not None:
                            raise completion.error
                        self._accept_sample(request, completion.sample)
                    except Exception as error:
                        if not request.future.done():
                            request.future.set_exception(error)
                    count -= 1
                    self._sampling["inflight_prompts"] -= 1
                return
            if inspect.iscoroutinefunction(getattr(self.model, "sample", None)):
                results = await self.model.sample(**kwargs)
            else:
                pending = await asyncio.get_running_loop().run_in_executor(
                    self._pool, partial(self.model.submit_sample, **kwargs)
                )
                self._sampling["submitted_requests"] += 1
                self._sampling["submit_seconds"] += time.monotonic() - started
                results = await pending.result_async(executor=self._pool)
            if len(results) != len(requests) or any(
                len(group) != 1 for group in results
            ):
                raise ValueError(
                    "sample response does not match the submitted prompt batch"
                )
            for request, samples in zip(requests, results, strict=True):
                try:
                    self._accept_sample(request, samples[0])
                except _RolloutStopped as stopped:
                    # Stop only this member; the rest of the batch still completes.
                    if not request.future.done():
                        request.future.set_exception(stopped)
        except Exception as exc:
            for request in requests:
                if not request.future.done():
                    request.future.set_exception(exc)
        finally:
            if started is not None:
                self._sampling["request_seconds"] += time.monotonic() - started
                self._sampling["inflight_requests"] -= 1
                self._sampling["inflight_prompts"] -= count

    def _accept_sample(self, request, sample):
        if (
            self.server_capabilities is not None
            and callable(getattr(self.model, "get_policy_version", None))
            and sample.policy_version is None
        ):
            raise RuntimeError("versioned sampling returned no policy provenance")
        if self._retained_kv and not sample.retained_kv:
            raise RuntimeError(
                "serving engine did not acknowledge retained-KV mode; upgrade the inference workers"
            )
        if not self._retained_kv and sample.retained_kv:
            raise RuntimeError("serving engine used retained KV without opting in")
        if self._retained_kv:
            anchor = sample.kv_cache_policy_version
            policy = sample.policy_version
            if anchor is None or policy is None:
                raise RuntimeError(
                    "bounded KV sampling returned no cache policy provenance"
                )
            if (
                anchor.lineage_id != policy.lineage_id
                or not 0 <= policy.step - anchor.step <= self.kv_cache.max_staleness
            ):
                raise RuntimeError("sampler exceeded the KV age bound")
            if (
                request.kv_anchor_id
                and self.kv_cache.on_limit == "hold"
                and anchor.id != request.kv_anchor_id
            ):
                raise RuntimeError("sampler refreshed KV despite on_limit='hold'")
            self._sampling["kv_refreshes"] += int(
                bool(request.kv_anchor_id) and anchor.id != request.kv_anchor_id
            )
        self._sampling["prompt_tokens"] += sample.prompt_tokens
        self._sampling["cached_prompt_tokens"] += sample.cached_prompt_tokens
        if self.sampling_policy == "trajectory":
            previous = next(
                (s for s in request.member.traj.spans if s.kind == "generated"), None
            )
            if previous is not None and (
                sample.policy_version != previous.policy_version
                or (
                    sample.policy_version is None
                    and sample.model_step != previous.policy_step
                )
            ):
                raise RuntimeError("sampler changed the pinned trajectory policy")
        self._sampling["generated_tokens"] += len(sample.tokens)
        if len(sample.tokens) > request.cap:
            raise ValueError("sampler exceeded the requested segment cap")
        if request.images:
            if (
                sample.prompt_token_ids is None
                or len(sample.prompt_token_ids) != request.expected_length
            ):
                raise ValueError(
                    "image expansion disagrees with expected_tokens; refusing misaligned training data"
                )
            offset = 0
            for chunk in request.prompt:
                length = (
                    len(chunk["tokens"])
                    if chunk["type"] == "text"
                    else chunk["expected_tokens"]
                )
                if (
                    chunk["type"] == "text"
                    and sample.prompt_token_ids[offset : offset + length]
                    != chunk["tokens"]
                ):
                    raise ValueError("image expansion shifted the echoed text tokens")
                offset += length
        elif sample.prompt_token_ids is not None:
            if sample.prompt_token_ids != [
                t for c in request.prompt for t in c["tokens"]
            ]:
                raise ValueError("sampler echoed a different token prefix")
        if (
            self._image_placeholder_id is not None
            and self._image_placeholder_id in sample.tokens
        ):
            # A sampled placeholder can be neither continued nor trained on, so end
            # this rollout before the sample joins it. A stop already requested
            # (e.g. a group deadline or discard) keeps its own cause.
            request.member.cause = request.member.cause or "sampled_image_placeholder"
            raise _RolloutStopped
        if not request.future.done():
            request.future.set_result(sample)

    def _carries_image_placeholder(self, messages):
        """Whether environment text spells the image placeholder.

        Renderers either encode it to the placeholder id or refuse the text, so
        such a rollout ends before rendering.
        """
        text = self._image_placeholder_text
        return text is not None and any(text in t for t in _message_texts(messages))

    def _truncate_cause(self, member):
        traj = member.traj
        if member.cause:
            return member.cause
        if traj.generated_tokens >= self.budget.max_generated_tokens:
            return "generated_tokens"
        if traj.context_tokens >= self.budget.max_context_tokens:
            return "context"
        return None

    async def _environment_call(self, awaitable, member=None, *, operation="on_turn"):
        with self._activities.measure(operation):
            task = asyncio.create_task(awaitable)
            stop = (
                asyncio.create_task(member.stop.wait()) if member is not None else None
            )
            tasks = (task,) if stop is None else (task, stop)
            try:
                done = (
                    await asyncio.wait(
                        tasks,
                        timeout=self.environment_timeout,
                        return_when=asyncio.FIRST_COMPLETED,
                    )
                )[0]
                if task in done:
                    return task.result()
                if stop in done:
                    raise _RolloutStopped
                raise InfrastructureError(
                    "environment watchdog expired; rollout remains unscored"
                )
            except (TimeoutError, ConnectionError) as exc:
                raise InfrastructureError(
                    "environment operation failed; rollout remains unscored"
                ) from exc
            finally:
                for pending_task in tasks:
                    if not pending_task.done():
                        pending_task.cancel()
                await asyncio.gather(*tasks, return_exceptions=True)

    async def _finish(self, member, row, cause=None):
        traj = member.traj
        if traj.pending_tokens:
            traj.final_text = self.renderer.tokenizer.decode(traj.pending_tokens)
            traj.messages.append({"role": "assistant", "content": traj.final_text})
            traj.pending_tokens.clear()
            traj.turns += 1
        traj.truncated = cause
        # A reward/verifier is customer code too: it must not hang the trainer.
        score = (
            member.env.reward(traj, row)
            if cause is None
            else member.env.on_truncated(traj, row, cause)
        )
        reward = float(await self._environment_call(score, operation="reward"))
        if not math.isfinite(reward):
            raise ValueError("environment reward must be finite")
        traj.reward, traj.done, traj.phase = reward, True, "done"

    async def _run_member(self, group, member):
        if member.traj is not None and member.traj.done:
            group.changed.set()
            return
        async with self._slots.hold((group.priority, group.admission_order)):
            started = time.monotonic()
            member.started = started
            member.env = self._env_instance()
            try:
                if member.traj is None:
                    messages = await self._environment_call(
                        member.env.reset(group.row), operation="reset"
                    )
                    if self._carries_image_placeholder(messages):
                        # Never rendered or sampled: the scored, untrained
                        # trajectory keeps only the placeholder as its prompt.
                        member.traj = Trajectory(
                            [{"type": "text", "tokens": [self._image_placeholder_id]}],
                            messages=messages,
                        )
                        await self._finish(
                            member, group.row, "prompt_image_placeholder"
                        )
                    else:
                        chunks = prompt_chunks(
                            self.renderer,
                            messages,
                            tools=[t.spec for t in member.env.tools],
                        )
                        member.traj = Trajectory(chunks, messages=messages)
                elif member.env.recovery == "snapshot":
                    await self._environment_call(
                        member.env.restore(member.traj, member.recovery_state),
                        operation="restore",
                    )
                elif member.env.recovery == "stateless":
                    # Rebind per-row tool availability without replacing the
                    # recorded prompt or replaying completed tool calls.
                    await self._environment_call(
                        member.env.reset(group.row), operation="reset"
                    )
                # Checkpoints snapshot the live environment from here on.
                member.restore_pending, member.recovery_state = False, None
                traj = member.traj
                while not traj.done:
                    cause = self._truncate_cause(member)
                    if cause:
                        await self._finish(member, group.row, cause)
                        break
                    if traj.phase == "sample":
                        prompt = traj.model_input()
                        if self._image_placeholder_id is not None and any(
                            chunk["type"] == "text"
                            and self._image_placeholder_id in chunk["tokens"]
                            for chunk in prompt
                        ):
                            # Context that reached the id without placeholder text
                            # (e.g. chunks from traj.rewrite, or restored state).
                            await self._finish(
                                member, group.row, "prompt_image_placeholder"
                            )
                            break
                        if self.server_capabilities is not None and any(
                            isinstance(chunk.get("data"), ImageHandle)
                            for chunk in prompt
                        ):
                            self.server_capabilities.require("session_image_handles_v1")
                        if (
                            self.budget.max_images is not None
                            and sum(c["type"] == "image" for c in prompt)
                            > self.budget.max_images
                        ):
                            raise ValueError(
                                "image budget exceeded; call traj.rewrite explicitly to evict images (cache miss and datum split)"
                            )
                        if self.server_capabilities is not None and any(
                            c["type"] == "image" for c in prompt
                        ):
                            self.server_capabilities.require_model(
                                self.model.base_model, "prompt_token_echo_v1"
                            )
                        cap = self.budget.next_segment(traj)
                        future = asyncio.get_running_loop().create_future()
                        key = hashlib.sha256(repr(group.row).encode()).hexdigest()
                        priority = (
                            self.length_history.get(key, 0)
                            if self.schedule.priority == "predicted_length"
                            else 0
                        )
                        request = _Request(
                            member,
                            cap,
                            future,
                            prompt,
                            (member.seed + traj.sample_index * 104729) % (2**31),
                            traj.context_tokens,
                            any(c["type"] == "image" for c in prompt),
                            priority,
                        )
                        self._ready_counter += 1
                        await self._ready.put(
                            ((group.priority, -priority), self._ready_counter, request)
                        )

                        try:
                            sample = await future
                        except _RolloutStopped:
                            await self._finish(member, group.row, member.cause)
                            break
                        async with member.lock:
                            if not sample.tokens:
                                await self._finish(member, group.row, "empty_sample")
                                break
                            traj.append_span(sample)
                            traj.sample_index += 1
                            traj.pending_tokens.extend(sample.tokens)
                            group.changed.set()
                            terminated = (
                                sample_stop(self.renderer, traj.pending_tokens)
                                is not None
                            )
                            turn_limit = (
                                self.budget.max_turn_tokens is not None
                                and len(traj.pending_tokens)
                                >= self.budget.max_turn_tokens
                            )
                            if (
                                sample.stop_reason == "length"
                                and not terminated
                                and not turn_limit
                            ):
                                remaining = min(
                                    self.budget.max_generated_tokens
                                    - traj.generated_tokens,
                                    self.budget.max_context_tokens
                                    - traj.context_tokens,
                                )
                                if (
                                    self.budget.final_answer_reserve
                                    and not traj.wrap_up
                                    and remaining <= self.budget.final_answer_reserve
                                ):
                                    text = self.renderer.tokenizer.decode(
                                        traj.pending_tokens
                                    )
                                    traj.final_text = text
                                    traj.messages.append(
                                        {"role": "assistant", "content": text}
                                    )
                                    traj.pending_tokens.clear()
                                    traj.turns += 1
                                    if traj.turns >= self.budget.max_turns:
                                        await self._finish(member, group.row, "turns")
                                        break
                                    messages = [
                                        {
                                            "role": "user",
                                            "content": "Use the remaining budget to give your final answer now, without more tool calls.",
                                        }
                                    ]
                                    chunks = continuation_chunks(
                                        self.renderer, traj, messages
                                    )
                                    length = sum(
                                        len(c["tokens"])
                                        if c["type"] == "text"
                                        else c["expected_tokens"]
                                        for c in chunks
                                    )
                                    if (
                                        traj.context_tokens + length
                                        >= self.budget.max_context_tokens
                                    ):
                                        await self._finish(member, group.row, "context")
                                        break
                                    traj.append_framing(chunks)
                                    traj.messages.extend(messages)
                                    traj.wrap_up = True
                                continue
                            if sample.stop_reason not in {"stop", "eos", "length"}:
                                raise ValueError(
                                    f"unknown sampler stop reason: {sample.stop_reason!r}"
                                )
                            # Decoding is solely an environment/reward view. These
                            # strings never replace sampled tokens in the prompt.
                            text = self.renderer.tokenizer.decode(traj.pending_tokens)
                            parsed = self.renderer.parse_response(
                                text, tools=[t.spec for t in member.env.tools]
                            )
                            traj.messages.append(parsed.message)
                            traj.final_text = text
                            traj.last_stop_reason = sample.stop_reason
                            traj.pending_tokens.clear()
                            traj.turns += 1
                            traj.phase = "environment"
                    if traj.phase == "environment":
                        async with member.lock:
                            history, old_run = copy.deepcopy(traj.messages), traj.run
                            if member.cause:
                                await self._finish(member, group.row, member.cause)
                                break
                            if traj.messages[-1].get("tool_calls") and (
                                traj.turns >= self.budget.max_turns or traj.wrap_up
                            ):
                                await self._finish(
                                    member,
                                    group.row,
                                    "turns" if not traj.wrap_up else "final_answer",
                                )
                                break
                            try:
                                messages = await self._environment_call(
                                    member.env.on_turn(traj), member
                                )
                            except _RolloutStopped:
                                await self._finish(member, group.row, member.cause)
                                break
                            if traj.run == old_run and traj.messages != history:
                                raise ValueError(
                                    "Env.on_turn rewrote history; return new messages or call traj.rewrite(). Rewriting costs a full prefix-cache miss and a datum split."
                                )
                            if messages is None:
                                await self._finish(member, group.row)
                                break
                            if traj.turns >= self.budget.max_turns or traj.wrap_up:
                                await self._finish(
                                    member,
                                    group.row,
                                    "turns" if not traj.wrap_up else "final_answer",
                                )
                                break
                            if traj.run != old_run:
                                if messages:
                                    raise ValueError(
                                        "after traj.rewrite, return [] to sample the new prompt directly"
                                    )
                                traj.phase = "sample"
                                continue
                            if not messages:
                                raise ValueError(
                                    "a continuation needs new environment messages or an explicit traj.rewrite"
                                )
                            messages = copy.deepcopy(messages)
                            for message in messages:
                                if message["role"] not in {"tool", "user", "system"}:
                                    raise ValueError(
                                        "on_turn may return only environment-authored messages"
                                    )
                                if message["role"] == "tool" and isinstance(
                                    message["content"], str
                                ):
                                    message["content"], elided = elide_middle(
                                        message["content"],
                                        self.renderer.tokenizer,
                                        self.budget.tool_output_tokens,
                                    )
                                    traj.metrics["tool_elisions"] = traj.metrics.get(
                                        "tool_elisions", 0
                                    ) + int(elided)
                            if self._carries_image_placeholder(messages):
                                await self._finish(
                                    member, group.row, "prompt_image_placeholder"
                                )
                                break
                            reserve = self.budget.final_answer_reserve
                            if (
                                reserve
                                and min(
                                    self.budget.max_context_tokens
                                    - traj.context_tokens,
                                    self.budget.max_generated_tokens
                                    - traj.generated_tokens,
                                )
                                <= reserve + self.budget.segment_tokens
                            ):
                                messages.append(
                                    {
                                        "role": "user",
                                        "content": "The remaining budget is reserved for your final answer. Answer now using the available information; no more tool calls.",
                                    }
                                )
                                traj.wrap_up = True
                            chunks = continuation_chunks(self.renderer, traj, messages)
                            length = sum(
                                len(c["tokens"])
                                if c["type"] == "text"
                                else c["expected_tokens"]
                                for c in chunks
                            )
                            if (
                                traj.context_tokens + length
                                >= self.budget.max_context_tokens
                            ):
                                await self._finish(member, group.row, "context")
                                break
                            traj.append_framing(chunks)
                            traj.messages.extend(messages)
                            traj.phase = "sample"
                key = hashlib.sha256(repr(group.row).encode()).hexdigest()
                self.length_history[key] = traj.generated_tokens
            finally:
                if member.traj is not None:
                    member.traj.elapsed += time.monotonic() - started
                member.started = None
                if not isinstance(self.env, Env):
                    with self._activities.measure("close"):
                        await member.env.close()
                group.changed.set()

    async def _run_group(self, group):
        started = time.monotonic()
        group.started = started
        tasks = [
            asyncio.create_task(self._run_member(group, member))
            for member in group.members
        ]
        try:
            while True:
                group.changed.clear()
                done = [i for i, task in enumerate(tasks) if task.done()]
                for i in done:
                    tasks[i].result()
                elapsed = group.elapsed + time.monotonic() - started
                if (
                    len(done) >= group.completion.min_members
                    and group.quorum_elapsed is None
                ):
                    group.quorum_elapsed = elapsed
                    group.quorum_tokens = [
                        m.traj.generated_tokens if m.traj else 0 for m in group.members
                    ]
                policy = group.completion
                due = (
                    policy.mode == "deadline"
                    and not group.closed
                    and group.quorum_elapsed is not None
                    and any(
                        m.traj is not None
                        and m.traj.generated_tokens - group.quorum_tokens[i]
                        >= policy.max_straggler_tokens
                        for i, m in enumerate(group.members)
                        if i not in done
                    )
                )
                if due and len(done) < len(tasks):
                    group.closed = True
                    if policy.on_stragglers != "carry_over":
                        for i, member in enumerate(group.members):
                            if i not in done:
                                member.cause = (
                                    "group_discard"
                                    if policy.on_stragglers == "discard"
                                    else "group_deadline"
                                )
                                member.stop.set()
                    if policy.on_stragglers in {"carry_over", "discard"} and done:
                        group.emitted.update(done)
                        self._emit(
                            CompletedGroup(
                                group.id,
                                group.row,
                                [group.members[i].traj for i in done],
                                False,
                                True,
                                elapsed,
                            )
                        )
                if len(done) == len(tasks):
                    remaining = [
                        m.traj
                        for i, m in enumerate(group.members)
                        if i not in group.emitted
                        and m.traj.truncated != "group_discard"
                    ]
                    group.finished = True
                    self._emit(
                        CompletedGroup(
                            group.id, group.row, remaining, True, group.closed, elapsed
                        )
                    )
                    return
                await group.changed.wait()
        except Exception as exc:
            self._completed.put_nowait(exc)
        finally:
            for task in tasks:
                if not task.done():
                    task.cancel()
            await asyncio.gather(*tasks, return_exceptions=True)
            group.elapsed += time.monotonic() - started
            group.started = None

    async def state_dict(self):
        """Capture rollout state for a checkpoint.

        An in-flight sample may replay one segment after restore. Stateful
        environments are snapshotted at stable boundaries; work inside a tool
        or reset call cannot be resumed from its partial side effects.
        """
        groups = []
        for group in list(self._groups.values()):
            members = []
            for member in group.members:
                recoverable, env_state = True, None
                if member.restore_pending:
                    # Still waiting for a slot or inside Env.restore: the new
                    # environment holds nothing to snapshot yet, so keep the
                    # state this rollout was loaded with.
                    env_state = member.recovery_state
                    trajectory = member.traj.state_dict()
                elif member.traj is not None and not member.traj.done:
                    contract = member.env.recovery if member.env else "drop"
                    recoverable = contract == "stateless" or (
                        contract == "snapshot"
                        and not member.lock.locked()
                        and member.traj.phase == "sample"
                    )
                    if recoverable and contract == "snapshot":
                        async with member.lock:
                            env_state = await member.env.snapshot(member.traj)
                            trajectory = member.traj.state_dict()
                    else:
                        trajectory = member.traj.state_dict()
                else:
                    trajectory = (
                        None if member.traj is None else member.traj.state_dict()
                    )
                if trajectory is not None and member.started is not None:
                    trajectory["elapsed"] += time.monotonic() - member.started
                members.append(
                    {
                        "seed": member.seed,
                        "traj": trajectory,
                        "recoverable": recoverable,
                        "env_state": encode_state(env_state),
                        "cause": member.cause,
                    }
                )
            # Re-emit completed groups on restore. The trainer separately records
            # consumed portions, so they are never used twice.
            groups.append(
                {
                    "id": group.id,
                    "row": encode_state(group.row),
                    "members": members,
                    "completion": vars(group.completion),
                    "priority": group.priority,
                    "admission_order": group.admission_order,
                    "elapsed": group.elapsed
                    + (
                        0 if group.started is None else time.monotonic() - group.started
                    ),
                    "quorum_elapsed": group.quorum_elapsed,
                    "quorum_tokens": group.quorum_tokens,
                    "emitted": sorted(group.emitted),
                    "closed": group.closed,
                    "finished": group.finished,
                }
            )
        return {
            "version": 1,
            "counter": self._counter,
            "length_history": self.length_history.copy(),
            "groups": groups,
            "outbox": [group_state(g) for g in self._outbox],
        }

    def load_state_dict(self, state):
        """Restore saved rollout state into a fresh engine before starting it."""
        if state["version"] != 1 or self._groups:
            raise ValueError(
                "restore requires a fresh engine and supported state version"
            )
        self._counter, self.length_history = (
            state["counter"],
            dict(state["length_history"]),
        )
        for result in state.get("outbox", []):
            self._emit(group_from_state(result))
        completed_ids = {g["id"] for g in state.get("outbox", []) if g["final"]}
        returned = {
            traj.id: traj for result in self._outbox for traj in result.trajectories
        }
        for admission_order, saved in enumerate(state["groups"]):
            # Outbox serialization happens after awaited environment snapshots.
            # A final result can therefore be newer than the saved members. It
            # authoritatively completes even discarded/already-emitted members
            # absent from that final result; none of this group may run again.
            finished = saved["id"] in completed_ids or saved.get("finished", False)
            members = []
            for item in saved["members"]:
                traj = (
                    None
                    if item["traj"] is None
                    else _trajectory_from_state(item["traj"])
                )
                if traj is not None and traj.id in returned:
                    traj = returned[traj.id]
                if traj is not None and not traj.done and not finished:
                    if item["recoverable"]:
                        if self._retained_kv:
                            # Recovery may replay updates onto a sibling policy
                            # branch. Keep historical sample provenance untouched,
                            # but prefill the saved prefix into a fresh generation.
                            # Even a repeated crash before the next sample must
                            # never reopen a namespace containing newer KV.
                            traj._kv_cache_group = uuid.uuid4().hex
                            traj._kv_cache_start = len(traj.spans)
                            self.recovery_metrics["kv_generations_restarted"] += 1
                        self.recovery_metrics["trajectories_recovered"] += 1
                    else:
                        self.recovery_metrics["trajectories_dropped_on_resume"] += 1
                        traj = None  # regenerate this member; preserve group membership
                member = _Member(
                    item["seed"],
                    traj=traj,
                    cause=item["cause"],
                    recovery_state=decode_state(item["env_state"]),
                    restore_pending=traj is not None and not traj.done and not finished,
                )
                if member.cause:
                    member.stop.set()
                members.append(member)
            group = _Group(
                saved["id"],
                decode_state(saved["row"]),
                members,
                GroupCompletion(**saved["completion"]),
                priority=saved.get("priority", 0),
                # Older checkpoints retain their saved group order. New snapshots
                # also retain the original position across assistance stages.
                admission_order=saved.get("admission_order", admission_order),
                elapsed=saved["elapsed"],
                quorum_elapsed=saved["quorum_elapsed"],
                quorum_tokens=saved["quorum_tokens"],
                emitted=set(saved["emitted"]),
                closed=saved["closed"],
                finished=finished,
            )
            self._groups[group.id] = group
        # Register older reservations first, before any initially free slots
        # can be granted. Dictionary order changes when a stage is resubmitted.
        for group in sorted(
            self._groups.values(), key=lambda g: (g.priority, g.admission_order)
        ):
            # Keep completed metadata for acknowledgement or stage replacement,
            # but the saved outbox already contains its result: do not emit twice.
            if not group.finished:
                group.task = asyncio.create_task(self._run_group(group))


def group_state(group):
    return {
        "id": group.id,
        "row": encode_state(group.row),
        "trajectories": [t.state_dict() for t in group.trajectories],
        "final": group.final,
        "closed_by_deadline": group.closed_by_deadline,
        "wait_seconds": group.wait_seconds,
    }


def _trajectory_from_state(state):
    trajectory = Trajectory.from_state_dict(state)
    # Only trainer recovery opts into expiry fallback. Public trajectory
    # roundtrips preserve the original data and routing handles unchanged.
    trajectory._routing_recovery_start = len(trajectory.spans)
    return trajectory


def group_from_state(state):
    return CompletedGroup(
        state["id"],
        decode_state(state["row"]),
        [_trajectory_from_state(t) for t in state["trajectories"]],
        state["final"],
        state["closed_by_deadline"],
        state["wait_seconds"],
    )
