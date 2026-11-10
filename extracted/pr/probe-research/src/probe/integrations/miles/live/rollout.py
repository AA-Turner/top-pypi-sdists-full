"""Rollout: one try of one Miles sample, named before its first model request, and what a command asked of it. The
rollout's event loop writes it; Probe's command thread reads it and asks it to stop. Why: DESIGN.md beside this file."""

from __future__ import annotations

import asyncio
import secrets
import threading
from dataclasses import dataclass, field
from typing import Any

#: This process's mark in every request id: two rollout processes on one engine never send the same id (a try key is
#: unique only within its process).
PROCESS_TOKEN = secrets.token_hex(4)


@dataclass(eq=False)
class Rollout:
    """``key`` is the attempt key: `{Sample.index}:{try}` (train), `eval:{call}:{Sample.index}:{try}` (eval)."""

    key: str
    prefix: str
    index: Any
    try_number: int
    #: `Sample.group_index` of a train sample (Miles' filter drops a group with an aborted member); None for eval.
    group: Any
    is_agent: bool
    #: Its generate function's `/generate` requests carry Probe's request id (`RidStamp`), so an abort can name them.
    can_abort: bool
    #: Miles can run its Sample again (`Sample.reset_for_retry`) and Probe can rebuild its generate call.
    can_retry: bool
    #: Miles' router (`http://ip:port`): the abort finds every engine through its `/workers`.
    router: str | None
    loop: asyncio.AbstractEventLoop
    retry_of: str | None = None
    #: A train try's step: the one its group's first try began under (`RolloutSchedule`); None for eval or unknown.
    scheduled_step: int | None = None
    #: Model calls made (Miles' `post` of a `/generate`), sends of them (a retried send counts again: the next request
    #: id is `probe:{process}:{key}:{requests}`), and tokens generated.
    calls: int = 0
    requests: int = 0
    tokens: int = 0
    #: An agent rollout's Miles session (`OpenAIEndpointTracer`): its server and id, for a watch.
    session_url: str | None = None
    session_id: str | None = None
    #: What the try's generate function returned (Miles samples).
    outputs: list = field(default_factory=list)
    #: "cancel" or "retry" once a command asked; `stopping` wakes its requests on the loop.
    stop: str | None = None
    stopping: asyncio.Event = field(default_factory=asyncio.Event)
    #: Its end was sent: `outcome`; or a retry replaced it: `retried_as`. `done` tells a waiting command.
    outcome: str | None = None
    retried_as: str | None = None
    is_scoring: bool = False
    done: threading.Event = field(default_factory=threading.Event)

    @property
    def is_eval(self) -> bool:
        return self.prefix.startswith("eval:")

    @property
    def is_ended(self) -> bool:
        return self.done.is_set()

    @property
    def rid_prefix(self) -> str:
        """Every request of this try: an SGLang abort of `rid` with this prefix stops them all."""
        return f"probe:{PROCESS_TOKEN}:{self.key}:"

    @property
    def next_key(self) -> str:
        """The key a retry of this try gets."""
        return f"{self.prefix}{self.try_number + 1}"

    def take_rid(self) -> str:
        """The next request's id (on the loop)."""
        self.requests += 1
        return f"{self.rid_prefix}{self.requests}"

    def ask_stop(self, kind: str) -> None:
        """From the command thread: stop this try's requests (an abort on the loop, `RidStamp`)."""
        self.stop = kind
        self.loop.call_soon_threadsafe(self.stopping.set)
