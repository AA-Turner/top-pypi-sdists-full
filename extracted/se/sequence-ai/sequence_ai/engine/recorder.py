# SPDX-FileCopyrightText: Copyright (c) 2026 General Sequences Company
# SPDX-License-Identifier: Apache-2.0
"""
The robots' steps as a policy server of your own serves them, streamed to whoever records them (GET /record): every
observation a robot streams - its video still as the H.264 it was sent as - and every act and what it answered, kept in
the server's memory for the last minute and nothing written to its disk. Record them where you keep your data
(network.record).

    python -m sequence_ai.network.record http://your-gpu:8000 run.rec     # on any machine that reaches the server

In one sentence: each observation a robot streams, as it goes on to its policy in order (engine.observed), and each act
with its answer becomes one record, numbered for the server, packed as msgpack - the observation as the robot sent it, a
sequence_ai.Video item as its H.264 access unit - and kept in memory, the newest WINDOW_S seconds and at most
WINDOW_BYTES of them → a recorder opens GET /record (the server's token on it), optionally `?after=<the last record it
had>` and `&robot=<one robot's id>` → it is sent {"t": "hello", "first", "next"}, then every record from there on as it
comes; records the window let go before it read them are said first, how many, as {"t": "gap"}.

A record: {"t": "observe", "n", "at", "robot", "episode", "step", "observation"} - or {"t": "act", "n", "at", "robot",
"episode", "step" (the newest observation it was answered from, None for an act that carried its own), "action"}.

WHY in memory: a robot's frames and its policy's answers are already on the server, and where they are kept is the
owner's choice - a step goes from here to their recorder in one hop, and nothing of it is written on the server.
WHY as the robot sent it: its video stays the H.264 it was, a few KB a frame, which plays as it is; turned back into
arrays, a minute of two cameras would be gigabytes.

Standard library and sequence-ai's own modules.
"""
from __future__ import annotations

import asyncio
import collections
import time
from typing import Any, Callable, Optional
from urllib.parse import parse_qs

from ..network import msgpack_io

__all__ = ["PATH", "WINDOW_BYTES", "WINDOW_S", "Window", "serve_recorder"]

PATH = "/record"
# What the server keeps for its recorders: the newest WINDOW_S seconds of records and at most WINDOW_BYTES of them,
# whichever is reached first. Two cameras' video comes to about 0.25 MB a second, so a minute is about 15 MB.
WINDOW_S = 60.0
WINDOW_BYTES = 32 << 20
# How many records one recorder is sent before it is looked at again whether more came.
_BATCH = 64


class Window:
    """The records a server keeps for its recorders (the module's docstring), kept and read on its event loop."""

    def __init__(self, *, seconds: float = WINDOW_S, most: int = WINDOW_BYTES,
                 clock: Callable[[], float] = time.time) -> None:
        self.seconds, self.most, self._clock = float(seconds), int(most), clock
        self._kept: collections.deque = collections.deque()       # (n, at, robot, packed)
        self._next = 1
        self._bytes = 0
        self._waiters: set = set()
        self.unpacked = 0                     # records that did not pack (an answer msgpack cannot carry): not kept

    @property
    def next(self) -> int:
        """The number the next record takes."""
        return self._next

    def observe(self, robot: str, episode: str, step: int, observation: Any) -> None:
        """One observation of a robot's stream, as it sent it."""
        self._keep({"t": "observe", "robot": robot, "episode": episode, "step": step, "observation": observation})

    def act(self, robot: str, episode: Optional[str], step: Optional[int], action: Any) -> None:
        """One act and what it answered: `step`, the newest observation of `episode` it was answered from (None for an
        act that carried its own)."""
        self._keep({"t": "act", "robot": robot, "episode": episode, "step": step, "action": action})

    def _keep(self, record: dict) -> None:
        at = self._clock()
        try:
            data = msgpack_io.pack({**record, "n": self._next, "at": at})
        except ValueError:
            self.unpacked += 1
            return
        self._kept.append((self._next, at, record.get("robot") or "", data))
        self._next += 1
        self._bytes += len(data)
        self._trim()
        for event in list(self._waiters):
            event.set()

    def _trim(self) -> None:
        oldest = self._clock() - self.seconds
        while len(self._kept) > 1 and (self._bytes > self.most or self._kept[0][1] < oldest):
            self._bytes -= len(self._kept.popleft()[3])

    def first(self) -> int:
        """The number of the oldest record kept: `next` when none is."""
        self._trim()
        return self._kept[0][0] if self._kept else self._next

    def since(self, n: int, robot: Optional[str] = None, most: int = _BATCH) -> tuple[int, list[tuple[int, bytes]]]:
        """(the number of the oldest record kept, up to `most` records from number `n` on - of `robot` alone, given
        one) - the first may be past `n`: those between went."""
        first = self.first()
        out = []
        for m, _, who, data in self._kept:
            if m >= n and (robot is None or who == robot):
                out.append((m, data))
                if len(out) >= most:
                    break
        return first, out

    def waiter(self) -> asyncio.Event:
        """An event set when the next record is kept."""
        event = asyncio.Event()
        self._waiters.add(event)
        return event

    def unwait(self, event: asyncio.Event) -> None:
        """Stop setting an event waiter() made: its recorder went."""
        self._waiters.discard(event)


def _query(scope: dict) -> dict:
    try:
        return {k: v[0] for k, v in parse_qs((scope.get("query_string") or b"").decode("latin-1")).items()}
    except (ValueError, UnicodeDecodeError):
        return {}


async def serve_recorder(scope: dict, receive: Callable, send: Callable, window: Window,
                         authorized: Optional[Callable[[dict], bool]] = None) -> None:
    """GET /record: one recorder's connection (the module's docstring). Refused at its upgrade (403) when `authorized`
    says no."""
    if (await receive()).get("type") != "websocket.connect":
        return
    if authorized is not None and not authorized(scope):
        await send({"type": "websocket.close", "code": 1008})
        return
    await send({"type": "websocket.accept"})
    asked = _query(scope)
    robot = asked.get("robot") or None
    try:
        after = int(asked["after"]) if "after" in asked else None
    except ValueError:
        after = None
    first = window.first()
    cursor = first if after is None or after < 0 else after + 1
    if cursor > window.next:                  # read further than this server has numbered: it restarted
        await send({"type": "websocket.send", "bytes": msgpack_io.pack(
            {"t": "gap", "count": None, "after": after, "next": first,
             "why": "this server numbered its records anew: what came after the last one read is not known"})})
        cursor = first
    closed = asyncio.Event()

    async def listen() -> None:
        while True:
            if (await receive()).get("type") == "websocket.disconnect":
                closed.set()
                return

    listener = asyncio.ensure_future(listen())
    event = window.waiter()
    try:
        await send({"type": "websocket.send", "bytes": msgpack_io.pack({"t": "hello", "first": first,
                                                                       "next": window.next})})
        while not closed.is_set():
            event.clear()
            oldest, records = window.since(cursor, robot)
            if oldest > cursor:                   # went before it was read: said, then what is kept from there
                await send({"type": "websocket.send", "bytes": msgpack_io.pack(
                    {"t": "gap", "count": oldest - cursor, "after": cursor - 1, "next": oldest})})
                cursor = oldest
                continue
            for n, data in records:
                await send({"type": "websocket.send", "bytes": data})
                cursor = n + 1
            if records:
                continue
            if robot is not None:
                cursor = max(cursor, window.next)     # the other robots' records, passed
            try:
                await asyncio.wait_for(event.wait(), 1.0)
            except asyncio.TimeoutError:
                pass
    except Exception:  # noqa: BLE001 - the recorder went
        pass
    finally:
        closed.set()
        window.unwait(event)
        listener.cancel()
        await asyncio.gather(listener, return_exceptions=True)
        try:
            await send({"type": "websocket.close", "code": 1000})
        except Exception:  # noqa: BLE001 - already gone
            pass
