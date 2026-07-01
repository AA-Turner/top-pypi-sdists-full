import asyncio
import time
import typing as t
from collections import deque
from contextlib import suppress
from dataclasses import dataclass, field
from uuid import uuid4

EventPayload = dict[str, t.Any]


class TurnEventStream:
    """Own the transport-facing event stream for a single queued turn."""

    def __init__(self) -> None:
        self._queue: asyncio.Queue[EventPayload | None] = asyncio.Queue()
        self._closed = False

    @property
    def queue(self) -> asyncio.Queue[EventPayload | None]:
        return self._queue

    async def publish(self, event: EventPayload) -> None:
        if self._closed:
            return
        await self._queue.put(event)

    async def close(self) -> None:
        if self._closed:
            return
        self._closed = True
        await self._queue.put(None)


@dataclass(slots=True)
class QueuedTurnRequest:
    """Single chat turn waiting to be processed for a session."""

    message: str
    model: str | None
    agent: str | None
    reset: bool
    generate_params_extra: dict[str, t.Any] | None = None
    stream: TurnEventStream = field(default_factory=TurnEventStream)
    turn_id: str = field(default_factory=lambda: f"turn_{uuid4().hex}")
    queued_at_monotonic: float = field(default_factory=time.perf_counter)


@dataclass(slots=True)
class TurnExecutionContext:
    """Mutable execution state for one active or queued turn."""

    request: QueuedTurnRequest
    status: str = "accepted"
    started_at_monotonic: float | None = None
    agent_name: str | None = None
    model: str | None = None

    @property
    def turn_id(self) -> str:
        return self.request.turn_id

    def mark_started(self, *, agent_name: str | None, model: str | None) -> None:
        self.status = "running"
        self.started_at_monotonic = time.perf_counter()
        self.agent_name = agent_name
        self.model = model

    def finish(self, status: str) -> None:
        self.status = status


class SessionTurnCoordinator:
    """Own serial turn execution state for one session."""

    def __init__(self, session_id: str) -> None:
        self._session_id = session_id
        self._queue: deque[TurnExecutionContext] = deque()
        self._queue_lock = asyncio.Lock()
        self._processing_task: asyncio.Task[None] | None = None
        self._active_turn: TurnExecutionContext | None = None

    @property
    def active_turn_id(self) -> str | None:
        if self._active_turn is None:
            return None
        return self._active_turn.turn_id

    @property
    def processing_task(self) -> asyncio.Task[None] | None:
        return self._processing_task

    async def attach_processor(self, task: asyncio.Task[None]) -> None:
        """Attach an externally-created processor task.

        Used by callers that own task creation themselves (notably test
        fixtures that need to inject a fake processor without going through
        :meth:`enqueue`). Acquires the queue lock to maintain the same
        invariant as ``enqueue``: only one processor task may be active per
        coordinator at a time. Raises ``RuntimeError`` if a live processor
        task is already attached.
        """
        async with self._queue_lock:
            if self._processing_task is not None and not self._processing_task.done():
                raise RuntimeError(
                    f"SessionTurnCoordinator({self._session_id}) already has an "
                    "active processing task"
                )
            self._processing_task = task

    @property
    def is_busy(self) -> bool:
        return self._processing_task is not None and not self._processing_task.done()

    @property
    def queue_depth(self) -> int:
        return len(self._queue)

    @property
    def has_pending_turns(self) -> bool:
        return bool(self._queue)

    async def enqueue(
        self,
        request: QueuedTurnRequest,
        *,
        processor_factory: t.Callable[[], t.Coroutine[t.Any, t.Any, None]],
    ) -> tuple[TurnExecutionContext, int]:
        context = TurnExecutionContext(request=request)
        async with self._queue_lock:
            self._queue.append(context)
            if self._processing_task is None or self._processing_task.done():
                self._processing_task = asyncio.create_task(processor_factory())
            return context, len(self._queue)

    async def dequeue_next(self) -> TurnExecutionContext | None:
        async with self._queue_lock:
            if not self._queue:
                self._processing_task = None
                return None
            context = self._queue.popleft()
            self._active_turn = context
            return context

    def mark_started(
        self,
        context: TurnExecutionContext,
        *,
        agent_name: str | None,
        model: str | None,
    ) -> None:
        if self._active_turn is context:
            context.mark_started(agent_name=agent_name, model=model)

    def finish_turn(self, context: TurnExecutionContext, *, status: str) -> None:
        context.finish(status)
        if self._active_turn is context:
            self._active_turn = None

    async def cancel_active(self) -> bool:
        if self._processing_task is None or self._processing_task.done():
            return False

        self._processing_task.cancel()
        with suppress(asyncio.CancelledError):
            await self._processing_task
        return True

    async def ensure_processing(
        self,
        *,
        processor_factory: t.Callable[[], t.Coroutine[t.Any, t.Any, None]],
    ) -> None:
        async with self._queue_lock:
            if not self._queue:
                self._processing_task = None
                return
            if self._processing_task is None or self._processing_task.done():
                self._processing_task = asyncio.create_task(processor_factory())

    def close(self) -> None:
        if self._processing_task is not None and not self._processing_task.done():
            self._processing_task.cancel()
