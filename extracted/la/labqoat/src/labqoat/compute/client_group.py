"""A group opened from the submitting machine: one node above the runs a launcher starts."""

from __future__ import annotations

import re
from dataclasses import dataclass, field, replace
from types import TracebackType
from typing import TYPE_CHECKING, ParamSpec, TypeVar

from labqoat.compute.value_codec import ValueCodec
from labqoat.compute.worker.failure_report import FailureReport
from labqoat.json_document import JsonDocument, JsonValue

if TYPE_CHECKING:
    from labqoat.client import Client
    from labqoat.compute.function import Function
    from labqoat.compute.function_calls import FunctionCalls

P = ParamSpec("P")
R = TypeVar("R")
T = TypeVar("T")


@dataclass
class ClientGroup:
    """Open on entry, closed on exit; every run submitted through ``client`` in between is a member.

    The group has no worker and no cost. It gives the launch one thing to watch, cancel and link to, and
    a nested ``group.client.group(...)`` becomes a group inside it.
    """

    owner: Client
    name: str
    id: str = ""
    client: Client = field(init=False, repr=False)
    outcome: JsonValue = field(default=None, repr=False)

    def calls(self, function: Function[P, R]) -> FunctionCalls[P, R]:
        """Bind a function so its ``remote``, ``spawn`` and ``map`` calls join this group."""
        return function.with_client(self.client)

    def run(self, function: Function[P, R], *args: P.args, **kwargs: P.kwargs) -> R:
        """Submit one member run and wait for its result."""
        return self.calls(function).remote(*args, **kwargs)

    def result(self, value: T) -> T:
        """Record a small value as this group's result and hand it back."""
        self.outcome = ValueCodec(type(value)).encode(value)
        return value

    def __enter__(self) -> ClientGroup:
        """Open the group and scope a client to it."""
        from labqoat.client import Client

        path = "/api/v1/groups"
        record = self.owner.decode_body(self.owner.send_json("POST", path, {"name": self.name}), path)
        self.id = JsonDocument.expect_scalar(record["id"], str)
        scoped = replace(self.owner.transport, group=self.id, _client=None)
        client = Client(scoped.base_url, scoped.username, scoped.password, transport=scoped)
        self.client = client.with_uploads(self.owner.uploads)
        return self

    def __exit__(
        self, kind: type[BaseException] | None, error: BaseException | None, trace: TracebackType | None
    ) -> None:
        """Close with what happened in the block; the exception, if any, continues to the caller."""
        path = f"/api/v1/groups/{self.id}/close"
        try:
            self.owner.decode_body(self.owner.send_json("POST", path, self._closure(error)), path)
        finally:
            self.client.close()

    def _closure(self, error: BaseException | None) -> dict[str, JsonValue]:
        """Completed with any recorded result, cancelled on interruption, or failed with the cause."""
        if error is None:
            return {"status": "completed", "result": self.outcome}
        if isinstance(error, KeyboardInterrupt):
            return {"status": "cancelled"}
        located = re.sub(r" at (?:.*/)?([^/]+:\d+)$", r" at \1", FailureReport.summary(error))
        return {"status": "failed", "detail": located}
