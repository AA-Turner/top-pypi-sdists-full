"""Base executor class for streaming execution with optional tracing."""

import typing as t
from abc import ABC, abstractmethod
from contextlib import asynccontextmanager, nullcontext

from pydantic import ConfigDict

from dreadnode.core.meta import Config, Model

if t.TYPE_CHECKING:
    import asyncio

    from dreadnode.tracing.span import TaskSpan

# Type variables for generic executor
EventT = t.TypeVar("EventT")
ResultT = t.TypeVar("ResultT")


class Executor(Model, ABC, t.Generic[EventT, ResultT]):
    """
    Abstract base class for streaming executors.

    Provides a consistent pattern for:
    - Streaming execution via async generators
    - Optional tracing integration
    - Cloning and configuration

    Subclasses must implement:
    - _stream(): Core execution logic yielding events
    - _extract_result(): Extract final result from events (optional)

    For tracing, override:
    - _create_span(): Return a context manager yielding TaskSpan or None
    - _should_trace(): Return False to disable tracing

    Example:
        class MyExecutor(Executor[MyEvent, MyResult]):
            async def _stream(self) -> AsyncGenerator[MyEvent, None]:
                yield MyStartEvent()
                # ... do work ...
                yield MyEndEvent(result=result)

            def _extract_result(self, event: MyEvent) -> MyResult | None:
                if isinstance(event, MyEndEvent):
                    return event.result
                return None
    """

    model_config = ConfigDict(arbitrary_types_allowed=True, use_attribute_docstrings=True)

    name: str
    description: str = ""
    tags: list[str] = Config(default_factory=list)
    label: str | None = Config(default=None)
    concurrency: int = Config(default=1, ge=1)
    """Maximum number of concurrent operations."""

    @abstractmethod
    async def _stream(self) -> t.AsyncGenerator[EventT, None]:
        """
        Core execution logic yielding events.

        This is the main execution method that subclasses must implement.
        It should yield events as execution progresses.

        Yields:
            Events describing execution progress.
        """
        yield

    @abstractmethod
    async def _stream_batch(self, batch: list[t.Any]) -> t.AsyncGenerator[EventT, None]:
        """
        Core batch execution logic yielding events.

        Args:
            batch: A list of items to process in the batch.

        Yields:
            Events describing execution progress for the batch.
        """
        yield

    @asynccontextmanager
    async def stream(self) -> t.AsyncIterator[t.AsyncGenerator[EventT, None]]:
        """
        Create an async context manager for the event stream.

        Usage:
            async with executor.stream() as events:
                async for event in events:
                    process(event)

        Yields:
            An async generator producing events.
        """
        with self._create_span():
            yield self._stream()

    def _create_span(self) -> t.ContextManager["TaskSpan[t.Any] | None"]:
        """
        Create the tracing span for this executor.

        Override to return a span factory from dreadnode.tracing.spans.
        By default, returns nullcontext() (no tracing).

        Returns:
            A context manager yielding TaskSpan or None.
        """
        return nullcontext()

    def _extract_result(self, event: EventT) -> ResultT | None:  # noqa: ARG002
        """
        Extract a result from an event.

        Override in subclasses to extract final results from specific event types.

        Args:
            event: The event to extract a result from.

        Returns:
            The result if this event represents completion, None otherwise.
        """
        return None

    async def run(self) -> ResultT:
        """
        Execute to completion and return the final result.

        Returns:
            The execution result.

        Raises:
            RuntimeError: If execution completes without producing a result.
        """
        async with self.stream() as events:
            async for event in events:
                if (result := self._extract_result(event)) is not None:
                    return result

        raise RuntimeError(f"{self.__class__.__name__} '{self.name}' failed to complete")

    def _create_semaphore(self) -> "asyncio.Semaphore":
        """Create a semaphore for concurrency control."""
        import asyncio

        return asyncio.Semaphore(self.concurrency)

    async def _stream(self) -> t.AsyncGenerator[EventT, None]:
        """
        Stream execution by processing items in batches.

        Yields:
            Events describing execution progress.
        """
        # Example batching logic; subclasses may override as needed
        items_to_process = []  # This should be populated with actual items
        batch_size = self.concurrency

        for i in range(0, len(items_to_process), batch_size):
            batch = items_to_process[i : i + batch_size]
            async for event in self._stream_batch(batch):
                yield event

    async def batch(self, batch: list[t.Any]) -> t.AsyncGenerator[EventT, None]:
        """
        Public method to process a specific batch.

        Args:
            batch: A list of items to process in the batch.

        Yields:
            Events describing execution progress for the batch.
        """
        async for event in self._stream_batch(batch):
            yield event

    async def stream_batch(self, batch: list[t.Any]) -> t.AsyncGenerator[EventT, None]:
        """
        Public method to stream execution for a specific batch.

        Args:
            batch: A list of items to process in the batch.
        Yields:
            Events describing execution progress for the batch.
        """
        async with self._create_span():  # ty: ignore[invalid-context-manager]
            async for event in self._stream_batch(batch):
                yield event

    async def map(self, items: list[t.Any]) -> t.AsyncGenerator[EventT, None]:
        """
        Public method to process a list of items.

        Args:
            items: A list of items to process.

        Yields:
            Events describing execution progress.
        """
        batch_size = self.concurrency

        for i in range(0, len(items), batch_size):
            batch = items[i : i + batch_size]
            async for event in self.batch(batch):
                yield event


class ConsoleAdapter(t.Protocol[EventT, ResultT]):
    """Protocol for console display adapters."""

    def __init__(self, executor: Executor[EventT, ResultT]) -> None: ...

    async def run(self) -> ResultT: ...
