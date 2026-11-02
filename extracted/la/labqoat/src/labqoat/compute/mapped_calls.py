"""Stable per-element operation keys for bounded bulk calls on host or worker transports."""

import asyncio
from dataclasses import dataclass, field
from typing import Generic, TypeVar

from labqoat.compute.child_run_handle import ChildRunHandle
from labqoat.compute.function import Function
from labqoat.compute.run_submissions import RunSubmissions
from labqoat.compute.prepared_submission import PreparedSubmission
from labqoat.runs.run_handle import RunHandle
from labqoat.runs_client import RunsClient

R = TypeVar("R")


@dataclass(frozen=True)
class MappedCalls(Generic[R]):
    """Dispatch scalar or tuple inputs through the same captured function and explicit authority."""

    function: Function[..., R]
    dispatcher: RunsClient | RunSubmissions
    key: str
    unpack: bool = False
    _prepared: PreparedSubmission[R] | None = field(init=False, default=None)

    def __post_init__(self) -> None:
        """Share one lazy publication only for host-owned dispatch."""
        if isinstance(self.dispatcher, RunsClient):
            object.__setattr__(self, "_prepared", self.dispatcher.prepare(self.function))

    def _arguments(self, value: object) -> tuple[object, ...]:
        """Require positional tuples for starmap instead of silently expanding arbitrary objects."""
        if not self.unpack:
            return (value,)
        if not isinstance(value, tuple):
            raise ValueError("starmap inputs must be tuples of positional arguments")
        return value

    def _dispatcher(self, index: int) -> RunsClient | RunSubmissions:
        """Preserve seed, resource and location overrides while giving every element its own retry key."""
        options = self.dispatcher.options
        return self.dispatcher.with_options(
            key=f"{self.key}/{index}",
            seed=options.seed,
            resources=options.resources,
            location=options.location,
        )

    def spawn(self, item: tuple[int, object]) -> RunHandle[R] | ChildRunHandle[R]:
        """Accept one input and return its independently reconnectable handle."""
        index, value = item
        dispatcher = self._dispatcher(index)
        arguments = self._arguments(value)
        if self._prepared is not None:
            return self._prepared.submit(arguments, dispatcher.options)
        return dispatcher.submit(self.function, *arguments)

    async def spawn_async(self, item: tuple[int, object]) -> RunHandle[R] | ChildRunHandle[R]:
        """Accept one input without blocking other operations in the async window."""
        index, value = item
        if self._prepared is not None:
            return await asyncio.to_thread(self.spawn, item)
        return await self._dispatcher(index).submit_async(self.function, *self._arguments(value))

    def result(self, item: tuple[int, object]) -> R:
        """Keep the element in flight until its accepted Run has a validated result."""
        return self.spawn(item).result()

    async def result_async(self, item: tuple[int, object]) -> R:
        """Await a typed result under the same per-element durable identity."""
        handle = await self.spawn_async(item)
        return await handle.result_async()
