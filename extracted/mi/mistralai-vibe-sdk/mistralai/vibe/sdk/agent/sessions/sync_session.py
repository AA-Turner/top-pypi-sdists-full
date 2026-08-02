"""SyncSession — synchronous session backed by an async session via thread bridge."""

import asyncio
import contextlib
import queue
import threading
from collections.abc import Coroutine, Generator, Sequence
from concurrent.futures import Future
from contextvars import copy_context
from types import TracebackType
from typing import Any, TypeVar

import structlog

from mistralai.vibe.sdk.agent.config import AgentConfig
from mistralai.vibe.sdk.agent.sessions.async_session import AsyncSession
from mistralai.vibe.sdk.agent.sessions.helpers import IdFactory
from mistralai.vibe.sdk.agent.tasks.agent_task import AgentTaskConfig
from mistralai.vibe.sdk.agent.tasks.helpers import AgentTaskFactory
from mistralai.vibe.sdk.capabilities.registry import ClientToolRegistry
from mistralai.vibe.sdk.execution_record.state import HistoryEntry, TaskState
from mistralai.vibe.sdk.observability import ObservabilityAttributes
from mistralai.vibe.sdk.transports.events import DownstreamMessage, UpstreamMessage

logger = structlog.get_logger()
_T = TypeVar("_T")


class SyncSession:
    """Synchronous session wrapper backed by an async session.

    Each instance owns a dedicated thread with an event loop for
    bridging async-to-sync calls. Call close() or use as a context
    manager to release the thread and event loop.
    """

    def __init__(
        self,
        *,
        task_config: AgentTaskConfig,
        agent_task_factory: AgentTaskFactory,
        history: Sequence[HistoryEntry] | None = None,
        id_factory: IdFactory | None = None,
        client_tool_registry: ClientToolRegistry | None = None,
        conversation_id: str | None = None,
        observability_attributes: ObservabilityAttributes | None = None,
    ) -> None:
        """Create a sync session."""
        self._async_session = AsyncSession(
            task_config=task_config,
            agent_task_factory=agent_task_factory,
            history=history,
            id_factory=id_factory,
            client_tool_registry=client_tool_registry,
            conversation_id=conversation_id,
            observability_attributes=observability_attributes,
        )
        self._loop = asyncio.new_event_loop()
        self._thread = threading.Thread(target=self._loop.run_forever, daemon=True)
        self._thread.start()
        self._closed = False

    @classmethod
    def _from_async_session(cls, async_session: AsyncSession) -> "SyncSession":
        session = cls.__new__(cls)
        session._async_session = async_session
        session._loop = asyncio.new_event_loop()
        session._thread = threading.Thread(target=session._loop.run_forever, daemon=True)
        session._thread.start()
        session._closed = False
        return session

    def _check_closed(self) -> None:
        if self._closed:
            raise RuntimeError("Session is closed")

    def _submit(self, coro: Coroutine[Any, Any, _T]) -> Future[_T]:
        return copy_context().run(asyncio.run_coroutine_threadsafe, coro, self._loop)

    def _run_sync(self, coro: Coroutine[Any, Any, _T]) -> _T:
        """Submit a coroutine and block until it completes."""
        return self._submit(coro).result()

    @property
    def session_id(self) -> str:
        return self._async_session.session_id

    @property
    def conversation_id(self) -> str | None:
        return self._async_session.conversation_id

    @property
    def history(self) -> list[HistoryEntry]:
        return self._async_session.history

    def set_config(self, config: AgentConfig) -> None:
        """Replace the SDK config used for future turns in this session."""
        self._check_closed()
        self._async_session.set_config(config)

    def run(self, prompt: str) -> Generator[DownstreamMessage, None, None]:
        """Stream protocol task-progress events synchronously."""
        self._check_closed()
        messages: queue.Queue[
            tuple[DownstreamMessage, asyncio.Future[None]] | BaseException | None
        ] = queue.Queue()

        async def stream_messages() -> None:
            try:
                async for message in self._async_session.run(prompt):
                    ack: asyncio.Future[None] = self._loop.create_future()
                    messages.put((message, ack))
                    await ack
            except BaseException as exc:
                messages.put(exc)
            finally:
                messages.put(None)

        future = self._submit(stream_messages())
        try:
            while True:
                item = messages.get()
                if item is None:
                    break

                if isinstance(item, BaseException):
                    raise item

                message, ack = item
                try:
                    yield message
                finally:
                    if not ack.done():
                        self._loop.call_soon_threadsafe(ack.set_result, None)

            future.result()
        finally:
            if not future.done():
                future.cancel()
                with contextlib.suppress(Exception):
                    future.result(timeout=5)

    def run_to_completion(self, prompt: str) -> TaskState:
        """Run a single turn and return the final state."""
        self._check_closed()
        return self._run_sync(self._async_session.run_to_completion(prompt))

    def send_message(self, message: UpstreamMessage) -> None:
        """Send an upstream message to the active run."""
        self._check_closed()
        self._run_sync(self._async_session.send_message(message))

    def fork(self, *, conversation_id: str | None = None) -> "SyncSession":
        """Create a new session branching from the current history."""
        self._check_closed()
        return self._from_async_session(self._async_session.fork(conversation_id=conversation_id))

    def close(self) -> None:
        """Stop the event loop, join the thread, and release resources."""
        if self._closed:
            return
        self._closed = True
        try:
            self._submit(self._async_session.close()).result()
        finally:
            self._loop.call_soon_threadsafe(self._loop.stop)
            self._thread.join(timeout=5)
            if self._thread.is_alive():
                logger.warning(
                    "session.sync.close.thread_alive",
                    join_timeout=5,
                    session_id=self.session_id,
                )
            else:
                self._loop.close()

    def __enter__(self) -> "SyncSession":
        self._check_closed()
        self._run_sync(self._async_session.__aenter__())
        return self

    def __exit__(
        self,
        exc_type: type[BaseException] | None,
        exc_val: BaseException | None,
        exc_tb: TracebackType | None,
    ) -> None:
        self.close()
