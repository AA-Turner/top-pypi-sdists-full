# SPDX-FileCopyrightText: Copyright (c) 2026 General Sequences Company
# SPDX-License-Identifier: Apache-2.0
"""
One policy server over two or more of a robot's uplinks - a Starlink terminal and a cellular modem, say: each act is
packed once and sent on every line at once, and the first answer is the one used.

    from sequence_ai.network import lines

    robot = lines.connect("http://your-gpu:8000", lines=["eth0", "wwan0"])   # a connection by each interface
    robot = lines.connect(url, lines={"eth0": "http://[2001:db8::7]:8000", "wwan0": "http://203.0.113.7:8000"})
    robot.wait_until_ready()
    response = robot.act({"image": frame, "state": state})                  # as Link.act()
    robot.stats()["lines"]                                                   # each line's acts, wins and errors

sequence_ai.connect(url, lines=...) and sequence_ai.network.connect(url, lines=...) make the same.

In one sentence: each line is a Link of its own (its connection, its pings, its first act's longer wait), bound to its
interface (network.bind) or to its address → act() packs the observation once, with the line that heard the server
last → the same body goes on every line that is free, each on its own thread, with one request id (REQUEST_HEADER) →
the server runs the act once and answers every copy (serve() does, and says so: X-Seq-Reads names "once") → the first
answer is returned; the others are read when they come, and how much later is counted.

What it does, and why:
    one act, one run    the copies carry one request id, and a server that says "once" runs the policy once for
                        them. To a server that does not say so, each act goes on one line alone - the first that is
                        free - and on the next only when that one could not connect: an act is never run twice.
    a line behind       a line still carrying the act before is not given this one: a line that has stopped answering
                        does not collect a queue of acts behind it
    the first answer    returned as soon as it comes; a line that fails leaves the act to the others, and the act
                        fails only when every line has, with the first line's error
    each line's pings   each line keeps its own connection warm (Link's pings): a connection's window is its own
    the uplink's cost   the compression's estimate of the uplink takes the answer used alone

The cost: every act's body is sent on each line - two lines, twice the upload. Two cameras' pictures as JPEG are about
24 KB an act (frames.py), so a policy asked every 533 ms (pi0.5's) sends about 160 MB an hour on each line.

Needs httpx, which sequence-ai installs; a line bound to an interface needs Linux 5.7 or later, or macOS
(network.bind).
"""
from __future__ import annotations

import concurrent.futures
import threading
import time
from typing import Any, Optional, Sequence

from .latency_stats import LatencyStats
from .link import ONCE, Link, _request_id

__all__ = ["Lines", "connect", "same_server"]


class Lines:
    """One policy server over each of `links` (two or more), each its own uplink: act() sends each act on every line and
    returns the first answer (the module's docstring)."""

    _NONE: Any = Link._NONE

    def __init__(self, links: Sequence[Link]) -> None:
        self._links = list(links)
        if len(self._links) < 2:
            raise ValueError(f"Lines takes two links or more, one an uplink; it was given {len(self._links)}")
        self._executors = [concurrent.futures.ThreadPoolExecutor(max_workers=1, thread_name_prefix=f"sequence-ai-line{i}")
                           for i in range(len(self._links))]
        self._carrying: list = [None] * len(self._links)     # each line's request in flight
        self._lock = threading.Lock()
        self._wins = [0] * len(self._links)
        self._errors = [0] * len(self._links)
        self._passed_over = [0] * len(self._links)           # acts a line was not given: it carried the act before
        self._stats = LatencyStats(counters=["acts", "acts_on_one_line"], latencies=["behind_us"])
        self._observed: Any = Lines._NONE
        # lines to more than one address: their servers must be one (same_server), or each copy runs on its own
        self._addresses = len({line._url for line in self._links}) > 1

    # ── what the server says ──────────────────────────────────────────────────────────────────────────────────────
    @property
    def once(self) -> bool:
        """Whether the server runs an act's copies once: every line that has heard it says ONCE in X-Seq-Reads."""
        heard = [line.reads for line in self._links if line.reads is not None]
        return bool(heard) and all(ONCE in said for said in heard)

    @property
    def reads(self) -> Optional[frozenset]:
        """What the server last said it reads, on the first line that has heard it; None before any answer."""
        return next((line.reads for line in self._links if line.reads is not None), None)

    @property
    def server(self) -> Optional[dict]:
        """What the server says it is, from the first line that has heard it (Link.server)."""
        return next((line.server for line in self._links if line.server), None)

    @property
    def links(self) -> list:
        """The lines, as Links, in the order given."""
        return list(self._links)

    # ── the robot's calls ─────────────────────────────────────────────────────────────────────────────────────────
    def wait_until_ready(self, timeout_s: float = 600.0, *, poll_s: float = 0.5, example: Any = _NONE) -> None:
        """Wait, up to `timeout_s`, until one line's ping says the server is ready (Link.wait_until_ready); the others
        are waited for on their own threads and join as they get there. Then, given an `example`, act on it once. The
        first line's error when no line got there."""
        waits = {self._executors[i].submit(line.wait_until_ready, timeout_s, poll_s=poll_s): i
                 for i, line in enumerate(self._links)}
        for future, i in waits.items():
            self._carrying[i] = future
        failed: list = []
        for future in concurrent.futures.as_completed(waits):
            if future.exception() is None:
                break
            failed.append((waits[future], future.exception()))
        else:
            raise min(failed, key=lambda f: f[0])[1]
        if example is not Lines._NONE:
            self.act(example)

    def observe(self, observation: Any) -> None:
        """Hold `observation` for the next act(); nothing is sent (Link.observe)."""
        self._observed = observation

    def act(self, observation: Any = _NONE, *, path: Optional[str] = None) -> Any:
        """Send `observation` - given none, the one observe() was handed last - on every free line at once, with one
        request id, and return the first answer (Link.act's, its errors included): on one line alone, to a server
        that does not run an act's copies once. ValueError with no observation given and none observed."""
        if observation is Lines._NONE:
            if self._observed is Lines._NONE:
                raise ValueError("act() was given no observation and observe() has not been called: hand one to either")
            observation = self._observed
        packer = next((line for line in self._links if line.reads is not None), self._links[0])
        packed = packer.pack(observation)
        if not self.once:
            return self._on_one_line(packed, path)
        if self._addresses and not same_server(self):
            raise ValueError("the addresses given are not one server: their pings name another process, version or "
                             f"start ({[line.server for line in self._links]}), and an act sent to each would run on each")
        free = [i for i in range(len(self._links)) if self._free(i)] or list(range(len(self._links)))
        with self._lock:
            for i in set(range(len(self._links))) - set(free):
                self._passed_over[i] += 1
        rid = _request_id()
        sent = {self._send(i, packed, path, rid): i for i in free}
        failed: list = []
        pending = set(sent)
        while pending:
            done, pending = concurrent.futures.wait(pending, return_when=concurrent.futures.FIRST_COMPLETED)
            for future in sorted(done, key=lambda f: sent[f]):
                i = sent[future]
                if future.exception() is not None:
                    failed.append((i, future.exception()))
                    with self._lock:
                        self._errors[i] += 1
                    continue
                answered = time.perf_counter()
                with self._lock:
                    self._wins[i] += 1
                self._stats.count("acts")
                if packed.squeeze is not None:          # the uplink is the one that answered
                    packed.squeeze.uplink.note(len(packed.body), self._links[i].last_carried_s or 0.0)
                for later in pending:
                    later.add_done_callback(lambda f, j=sent[later], at=answered: self._behind(j, f, at))
                return future.result()
        raise min(failed, key=lambda f: f[0])[1]

    def _on_one_line(self, packed: Any, path: Optional[str]) -> Any:
        """An act to a server that runs each copy it gets: on the first free line, and on the next only when a line
        could not connect at all (the act never reached the server there)."""
        self._stats.count("acts_on_one_line")
        order = sorted(range(len(self._links)), key=lambda i: not self._free(i))
        refused: Optional[BaseException] = None
        for i in order:
            try:
                value = self._send(i, packed, path, None).result()
            except self._links[i]._refused as error:   # not connected: the act was not sent
                with self._lock:
                    self._errors[i] += 1
                refused = refused or error
                continue
            with self._lock:
                self._wins[i] += 1
            self._stats.count("acts")
            return value
        raise refused  # type: ignore[misc]

    def _send(self, i: int, packed: Any, path: Optional[str], rid: Optional[str]) -> concurrent.futures.Future:
        future = self._executors[i].submit(self._links[i].post, packed, path=path, request_id=rid, note=False)
        self._carrying[i] = future
        return future

    def _free(self, i: int) -> bool:
        carrying = self._carrying[i]
        return carrying is None or carrying.done()

    def _behind(self, i: int, future: concurrent.futures.Future, answered: float) -> None:
        """A copy answered after the one used: how far behind it came, or that its line failed."""
        if future.exception() is not None:
            with self._lock:
                self._errors[i] += 1
            return
        self._stats.sample("behind_us", (time.perf_counter() - answered) * 1e6)

    def stats(self) -> dict:
        """{"lines": [each line's own Link.stats() with "bind", "url", "wins" (the acts whose answer it gave first),
        "errors" and "passed_over" (the acts it was not given: it carried the act before)], and over all, as
        LatencyStats.snapshot() says them, the counters "acts" and "acts_on_one_line" and the latency "behind_us": how
        far behind the answer used each other copy's came}."""
        with self._lock:
            each = [{"bind": line.bind, "url": line._url, "wins": self._wins[i], "errors": self._errors[i],
                     "passed_over": self._passed_over[i], **line.stats()} for i, line in enumerate(self._links)]
        return {"lines": each, **self._stats.snapshot()}

    def close(self) -> None:
        """Close every line, and stop their threads."""
        for line in self._links:
            line.close()
        for executor in self._executors:
            executor.shutdown(wait=False)

    def __enter__(self) -> "Lines":
        return self

    def __exit__(self, *exc: object) -> None:
        self.close()


def connect(url: str, *, lines: Any, **options: Any) -> Lines:
    """The server at `url` over each of this robot's network interfaces in `lines`, two or more: a list (["eth0",
    "wwan0"]), or {interface: address} where the server has another address by each ({"eth0": url_v6, "wwan0":
    url_v4}; an address left None is `url`). A Link bound to each (network.bind), with Link's `options`. OSError, naming
    this machine's interfaces, for a name it has not."""
    by = dict(lines) if isinstance(lines, dict) else {name: None for name in lines}
    if len(by) < 2:
        raise ValueError(f"lines= names two network interfaces or more, one each uplink; it was given {list(by)}")
    return Lines([Link(address or url, bind=name, **options) for name, address in by.items()])


def same_server(lines: Lines) -> bool:
    """Whether the lines' servers, as each line's ping said (Link.server), are one: the same process (pid) and version,
    started at the same moment (now less its up_s, within 5 s). True while any line has not said."""
    said = [line.server for line in lines.links]
    if any(not s or "pid" not in s or "up_s" not in s for s in said):
        return True
    now = time.time()
    began = [now - float(s["up_s"]) for s in said]
    return (len({s["pid"] for s in said}) == 1 and len({s.get("version") for s in said}) == 1
            and max(began) - min(began) <= 5.0)
