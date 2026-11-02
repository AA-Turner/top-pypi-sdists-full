"""A named node under the current run: keyed child work with one outcome and no worker of its own."""

from __future__ import annotations

import asyncio
from dataclasses import dataclass, field
from types import TracebackType
from typing import TYPE_CHECKING, ParamSpec, TypeVar

from labqoat.authoring.resources import Resources
from labqoat.compute.child_run_handle import ChildRunHandle
from labqoat.compute.function import Function
from labqoat.compute.run_submissions import RunSubmissions
from labqoat.compute.value_codec import ValueCodec
from labqoat.compute.worker.failure_report import FailureReport
from labqoat.json_document import JsonDocument, JsonValue

if TYPE_CHECKING:
    from labqoat.compute.function_calls import FunctionCalls

P = ParamSpec("P")
R = TypeVar("R")
T = TypeVar("T")


@dataclass
class RunGroup:
    """Open on entry, closed on exit: completed, failed with the escaping exception, or cancelled.

    Children are submitted by the owning run under ``<group>/<key>``, so the owner awaits them directly and a
    retried owner finds the same group and the same children. What a failure means for sibling groups is the
    author's code: catch it, gather with ``return_exceptions``, or let it propagate.
    """

    submissions: RunSubmissions
    path: str
    name: str | None = None
    id: str = ""
    outcome: JsonValue = field(default=None, repr=False)

    def with_options(
        self,
        *,
        key: str,
        seed: int = 0,
        resources: Resources | None = None,
        location: str | None = None,
    ) -> RunSubmissions:
        """Child dispatch whose permanent key lives inside this group."""
        return self.submissions.with_options(
            key=f"{self.path}/{key}",
            seed=seed,
            resources=resources,
            location=location,
        )

    def group(self, name: str) -> RunGroup:
        """A group nested in this one."""
        return RunGroup(self.submissions, f"{self.path}/{name}")

    def calls(self, function: Function[P, R], key: str | None = None) -> FunctionCalls[P, R]:
        """Bind a function for ``map_async`` and repeated calls inside this group, under ``key`` or its own name."""
        from labqoat.compute.function_calls import FunctionCalls

        return FunctionCalls(function, self.with_options(key=key or function.local.__name__))

    async def submit(self, function: Function[P, R], *args: P.args, **kwargs: P.kwargs) -> ChildRunHandle[R]:
        """Accept one child keyed by the function's name; use ``with_options`` to call a function twice."""
        return await self.with_options(key=function.local.__name__).submit_async(function, *args, **kwargs)

    async def run(self, function: Function[P, R], *args: P.args, **kwargs: P.kwargs) -> R:
        """Accept one child keyed by the function's name and await its result."""
        handle = await self.submit(function, *args, **kwargs)
        return await handle.result_async()

    def result(self, value: T) -> T:
        """Record a small value as this group's result and hand it back."""
        self.outcome = ValueCodec(type(value)).encode(value)
        return value

    async def __aenter__(self) -> RunGroup:
        """Open the group; the same path under the same owner is always the same group."""
        record = await self.submissions.api.json_async("POST", "/api/v1/worker/groups", self._opening())
        self.id = JsonDocument.expect_scalar(record["id"], str)
        return self

    async def __aexit__(
        self, kind: type[BaseException] | None, error: BaseException | None, trace: TracebackType | None
    ) -> None:
        """Close with what happened in the block; the exception, if any, continues to the caller."""
        await self.submissions.api.json_async("POST", f"/api/v1/worker/groups/{self.id}/close", self._closure(error))

    def __enter__(self) -> RunGroup:
        """Open the group from synchronous code."""
        record = self.submissions.api.json("POST", "/api/v1/worker/groups", self._opening())
        self.id = JsonDocument.expect_scalar(record["id"], str)
        return self

    def __exit__(
        self, kind: type[BaseException] | None, error: BaseException | None, trace: TracebackType | None
    ) -> None:
        """Close the group from synchronous code."""
        self.submissions.api.json("POST", f"/api/v1/worker/groups/{self.id}/close", self._closure(error))

    def _opening(self) -> dict[str, JsonValue]:
        """The permanent key and an optional display name."""
        body: dict[str, JsonValue] = {"key": self.path}
        if self.name is not None:
            body["name"] = self.name
        return body

    def _closure(self, error: BaseException | None) -> dict[str, JsonValue]:
        """Completed with any recorded result, cancelled with its task, or failed with the cause."""
        if error is None:
            return {"status": "completed", "result": self.outcome}
        if isinstance(error, (asyncio.CancelledError, KeyboardInterrupt)):
            return {"status": "cancelled"}
        return {"status": "failed", "detail": FailureReport.summary(error)}
