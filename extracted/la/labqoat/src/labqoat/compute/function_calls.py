"""Explicitly bound remote calls and bounded bulk dispatch for a typed declaration."""

from collections.abc import AsyncGenerator, Generator, Iterable
from dataclasses import dataclass
from typing import Generic, ParamSpec, TypeVar
from uuid import uuid4

from labqoat.authoring.resources import Resources
from labqoat.compute.async_parallel_map import AsyncParallelMap
from labqoat.compute.child_run_handle import ChildRunHandle
from labqoat.compute.function import Function
from labqoat.compute.mapped_calls import MappedCalls
from labqoat.compute.parallel_map import ParallelMap
from labqoat.compute.run_options import RunOptions
from labqoat.compute.run_submissions import RunSubmissions
from labqoat.runs.run_handle import RunHandle
from labqoat.runs_client import RunsClient

P = ParamSpec("P")
R = TypeVar("R")


@dataclass(frozen=True)
class FunctionCalls(Generic[P, R]):
    """Bind credentials explicitly; no client or RunContext is discovered globally."""

    function: Function[P, R]
    dispatcher: RunsClient | RunSubmissions

    def with_options(
        self,
        *,
        key: str,
        seed: int = 0,
        resources: Resources | None = None,
        location: str | None = None,
    ) -> "FunctionCalls[P, R]":
        """Select a stable operation namespace, independent execution overrides and an optional location."""
        dispatcher = self.dispatcher.with_options(key=key, seed=seed, resources=resources, location=location)
        return FunctionCalls(self.function, dispatcher)

    def spawn(self, *args: P.args, **kwargs: P.kwargs) -> RunHandle[R] | ChildRunHandle[R]:
        """Accept a durable job and return immediately with its typed handle."""
        return self.dispatcher.submit(self.function, *args, **kwargs)

    async def spawn_async(self, *args: P.args, **kwargs: P.kwargs) -> RunHandle[R] | ChildRunHandle[R]:
        """Accept a durable job using the asynchronous dispatch boundary."""
        return await self.dispatcher.submit_async(self.function, *args, **kwargs)

    def remote(self, *args: P.args, **kwargs: P.kwargs) -> R:
        """Accept one invocation and await its validated result."""
        return self.spawn(*args, **kwargs).result()

    async def remote_async(self, *args: P.args, **kwargs: P.kwargs) -> R:
        """Await one remote result without blocking the caller's event loop."""
        handle = await self.spawn_async(*args, **kwargs)
        return await handle.result_async()

    def map(
        self, inputs: Iterable[object], *, max_in_flight: int = 32, order_outputs: bool = True
    ) -> Generator[R, None, None]:
        """Lazily map scalar inputs with at most max_in_flight outstanding invocations."""
        operation = self._mapped(False)
        return ParallelMap(operation.result, max_in_flight, order_outputs).iterate(enumerate(inputs))

    def map_async(
        self, inputs: Iterable[object], *, max_in_flight: int = 32, order_outputs: bool = True
    ) -> AsyncGenerator[R, None]:
        """Stream bounded scalar results from an async workflow or host client."""
        operation = self._mapped(False)
        return AsyncParallelMap(operation.result_async, max_in_flight, order_outputs).iterate(enumerate(inputs))

    def starmap(
        self,
        inputs: Iterable[tuple[object, ...]],
        *,
        max_in_flight: int = 32,
        order_outputs: bool = True,
    ) -> Generator[R, None, None]:
        """Expand each positional tuple into a separately identified bounded invocation."""
        operation = self._mapped(True)
        return ParallelMap(operation.result, max_in_flight, order_outputs).iterate(enumerate(inputs))

    def starmap_async(
        self,
        inputs: Iterable[tuple[object, ...]],
        *,
        max_in_flight: int = 32,
        order_outputs: bool = True,
    ) -> AsyncGenerator[R, None]:
        """Stream positional-tuple results with asynchronous bounded dispatch."""
        operation = self._mapped(True)
        return AsyncParallelMap(operation.result_async, max_in_flight, order_outputs).iterate(enumerate(inputs))

    def spawn_map(
        self, inputs: Iterable[object], *, max_in_flight: int = 32
    ) -> Generator[RunHandle[R] | ChildRunHandle[R], None, None]:
        """Consume to accept jobs in a bounded window, yielding handles without waiting for execution."""
        operation = self._mapped(False)
        return ParallelMap(operation.spawn, max_in_flight, True).iterate(enumerate(inputs))

    def spawn_map_async(
        self, inputs: Iterable[object], *, max_in_flight: int = 32
    ) -> AsyncGenerator[RunHandle[R] | ChildRunHandle[R], None]:
        """Consume asynchronously to accept independently reconnectable background jobs."""
        operation = self._mapped(False)
        return AsyncParallelMap(operation.spawn_async, max_in_flight, True).iterate(enumerate(inputs))

    def _mapped(self, unpack: bool) -> MappedCalls[R]:
        """Reserve space for indexed keys and require replayable worker-owned map namespaces."""
        key = self.dispatcher.options.key
        if key is None and isinstance(self.dispatcher, RunSubmissions):
            raise ValueError("Worker maps require an explicit stable operation key")
        namespace = key or str(uuid4())
        RunOptions(key=namespace + "/" + "0" * 20)
        return MappedCalls(self.function, self.dispatcher, namespace, unpack)
