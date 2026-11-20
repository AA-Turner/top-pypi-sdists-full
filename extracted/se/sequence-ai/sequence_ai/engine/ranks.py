# SPDX-FileCopyrightText: Copyright (c) 2026 General Sequences Company
# SPDX-License-Identifier: Apache-2.0
"""
One model across several processes, as torchrun starts them - RANK, WORLD_SIZE, MASTER_ADDR and MASTER_PORT in each
process's environment: rank 0 serves the robots as one process does, and every call of the policy goes to every rank,
each running it on its own part of the model; rank 0 answers with its own result.

    torchrun --nproc-per-node 2 my_server.py        # each process calls serve(policy, ...), unchanged

In one sentence: every rank runs the same program and calls serve() → serve() finds WORLD_SIZE above 1 (from_env) →
rank 0 takes the other ranks on MASTER_PORT + 1 (RANKS_PORT_ENV names another port) and serves robots, its warm-up and
/ping waiting until every rank has joined; each other rank builds the same server, opens no port of robots', joins rank
0 and waits (Group.follow) → each call of the policy on rank 0 - a batch of acts, the warm-up's - is sent to every rank
first, runs on rank 0, and rank 0 waits for each rank's word that it ran it (Group.run) → a rank that left, or whose
call raised where rank 0's did not, halts the group (GroupHalted): every act after is refused, saying which rank and
why.

WHY the engine's own connection and not torch.distributed: a JAX model, or one of no framework, is served the same way;
what the ranks say to each other inside a call - torch.distributed, jax.distributed, NCCL - is the model's own.
WHY each call reaches every rank before rank 0 runs its own: a model split across ranks runs collectives inside a call -
an all-gather, a send and its receive - which wait until every rank is in it; rank 0 alone in one would wait forever.
WHY the group halts where a dead replica is replaced (engine.replicas): the model is split across the ranks, so the loss
of one leaves no rank able to answer alone; the launcher restarts the group (torchrun --max-restarts).
WHY a rank runs each call on its own policy thread: CUDA and JAX keep state per thread, as on rank 0.

Standard library only, beside the package's msgpack (each call's observations carried with their arrays as arrays).
"""
from __future__ import annotations

import concurrent.futures
import functools
import os
import socket
import struct
import threading
import time
from typing import Any, Callable, Mapping, Optional

from ..network import msgpack_io
from .replicas import PoolHalted

__all__ = ["GroupHalted", "Group", "Mirrored", "from_env", "RANKS_PORT_ENV", "JOIN_S"]

RANKS_PORT_ENV = "SEQ_SERVE_RANKS_PORT"   # the port rank 0 takes the other ranks on, where MASTER_PORT + 1 is not free
JOIN_S = 600.0                            # how long rank 0 waits for every rank, and a rank for rank 0: a model's load
_RETRY_S = 0.5                            # how often a rank tries rank 0 again while rank 0 is not listening yet
_LENGTH = struct.Struct("!Q")             # each message: its length, then its msgpack


class GroupHalted(PoolHalted):
    """A rank of the group left, or its call raised where rank 0's did not: the group answers no more - as a pool with
    no replica left (engine.replicas), told apart by its rank and why."""


def from_env(environ: Mapping[str, str] = os.environ) -> Optional["Group"]:
    """The group this process is a rank of, as a launcher's environment says it (torchrun's: WORLD_SIZE above 1, RANK,
    MASTER_ADDR, MASTER_PORT); None for a process alone. ValueError for one that names a group but not its place in it
    or the way to rank 0."""
    size = environ.get("WORLD_SIZE", "").strip()
    if not size or size == "1":
        return None
    try:
        world = int(size)
        rank = int(environ["RANK"])
        port = int(environ.get(RANKS_PORT_ENV) or int(environ["MASTER_PORT"]) + 1)
    except (KeyError, ValueError) as e:
        raise ValueError(f"serve() runs as one rank of {size} where WORLD_SIZE says so, and needs RANK and MASTER_PORT "
                         f"(or {RANKS_PORT_ENV}) to reach rank 0, as torchrun sets them: {type(e).__name__}: {e}") \
            from None
    if world < 1 or not 0 <= rank < world:
        raise ValueError(f"RANK {rank} is not one of the {world} ranks WORLD_SIZE says")
    return Group(rank, world, environ.get("MASTER_ADDR") or "127.0.0.1", port)


class Group:
    """
    This process's rank in a group of `size` (from_env), rank 0 reached at `host`:`port`.

    rank 0      listen(), then wait_joined() before its first call; each call of the policy through run()
    any other   follow(run_one): join rank 0, then run each call it sends, until it is gone
    `join_s`: how long rank 0 waits for every rank to join, and a rank to reach rank 0. `halted`: why the group
    answers no more, once it does not.
    """

    def __init__(self, rank: int, size: int, host: str, port: int, *, join_s: float = JOIN_S) -> None:
        self.rank, self.size, self.host, self.port, self.join_s = rank, size, host, port, join_s
        self.halted: Optional[str] = None
        self._peers: "dict[int, socket.socket]" = {}       # rank 0: each other rank's connection, by its rank
        self._joined = threading.Event()
        self._n = 0                                          # rank 0: the calls sent, each message's number

    @property
    def leads(self) -> bool:
        """Whether this is rank 0: the rank that serves the robots."""
        return self.rank == 0

    def __repr__(self) -> str:
        return f"rank {self.rank} of {self.size}"

    # ── rank 0 ────────────────────────────────────────────────────────────────────────────────────────────────────────
    def listen(self) -> None:
        """Rank 0: take each other rank as it joins, on a thread of its own, on every address of this machine (the
        ranks may run on others). OSError when the port is taken."""
        server = socket.create_server(("", self.port), reuse_port=False)
        threading.Thread(target=self._take, args=(server,), daemon=True, name="sequence_ai-ranks").start()

    def _take(self, server: socket.socket) -> None:
        server.settimeout(self.join_s)
        try:
            while len(self._peers) < self.size - 1:
                conn, _ = server.accept()
                conn.settimeout(self.join_s)
                hello = _recv(conn)
                rank = hello.get("rank") if isinstance(hello, dict) else None
                if not isinstance(rank, int) or not 0 < rank < self.size or rank in self._peers:
                    conn.close()
                    continue
                conn.settimeout(None)
                conn.setsockopt(socket.IPPROTO_TCP, socket.TCP_NODELAY, 1)
                self._peers[rank] = conn
        except (OSError, EOFError, ValueError) as e:
            missing = sorted(set(range(1, self.size)) - set(self._peers))
            self.halted = (f"ranks {', '.join(map(str, missing))} of {self.size} did not join rank 0 on port "
                           f"{self.port} within {self.join_s:g} s ({type(e).__name__}: {e})")
        finally:
            server.close()
            self._joined.set()

    def joined(self) -> int:
        """How many ranks have joined, rank 0 among them."""
        return 1 + len(self._peers)

    def wait_joined(self) -> None:
        """Rank 0: block until every rank has joined. GroupHalted where one did not within join_s."""
        self._joined.wait()
        if self.halted is not None:
            raise GroupHalted(self.halted)

    def run(self, op: str, args: list, local: Callable[[], Any]) -> Any:
        """Rank 0, on its policy thread: `op` with `args` sent to every other rank, then `local()` run here, then every
        rank's word that it ran it; what `local()` returned, or raised. GroupHalted - and the group halted - where a
        rank left, or raised where rank 0 did not; where rank 0 raised, so does this, whatever the others did."""
        if self.halted is not None:
            raise GroupHalted(self.halted)
        self._n += 1
        message = msgpack_io.pack({"n": self._n, "op": op, "args": args})
        for rank, conn in sorted(self._peers.items()):
            try:
                _send(conn, message)
            except OSError as e:
                raise GroupHalted(self._halt(f"rank {rank} left ({type(e).__name__}: {e})")) from None
        error: Optional[BaseException] = None
        result = None
        try:
            result = local()
        except Exception as e:  # noqa: BLE001 - the ranks' words first, then this raised
            error = e
        for rank, conn in sorted(self._peers.items()):
            try:
                word = _recv(conn)
            except (OSError, EOFError, ValueError) as e:
                raise GroupHalted(self._halt(f"rank {rank} left ({type(e).__name__}: {e})")) from None
            if isinstance(word, dict) and word.get("error") is not None and error is None:
                raise GroupHalted(self._halt(f"rank {rank} raised where rank 0 did not: {word['error']}"))
        if error is not None:
            raise error
        return result

    def _halt(self, why: str) -> str:
        """The group answers no more, for `why`: each rank told to stop and let go."""
        self.halted = self.halted or why
        for conn in self._peers.values():
            try:
                conn.close()
            except OSError:
                pass
        return self.halted

    def close(self) -> None:
        """Rank 0: every rank told the server stopped, and let go - each returns from follow()."""
        stop = msgpack_io.pack({"n": self._n + 1, "op": "stop", "args": []})
        for conn in self._peers.values():
            try:
                _send(conn, stop)
                conn.close()
            except OSError:
                pass
        self._peers = {}

    # ── every other rank ──────────────────────────────────────────────────────────────────────────────────────────────
    def follow(self, run_one: Callable[[str, list], Any], *, stop: Optional[threading.Event] = None) -> None:
        """A rank other than 0: join rank 0 - trying again while it is not listening yet, join_s at most - then run each
        call it sends (`run_one(op, args)`, on this rank's policy thread), saying whether it raised, until rank 0 says
        it stopped or is gone. ConnectionError where rank 0 could not be reached."""
        conn = self._join(stop)
        try:
            while stop is None or not stop.is_set():
                try:
                    message = _recv(conn)
                except (OSError, EOFError):
                    return                                   # rank 0 is gone: so is its server
                if not isinstance(message, dict) or message.get("op") == "stop":
                    return
                try:
                    run_one(message["op"], list(message.get("args") or []))
                    word = {"n": message.get("n"), "ok": True}
                except Exception as e:  # noqa: BLE001 - rank 0 compares it with its own
                    word = {"n": message.get("n"), "error": f"{type(e).__name__}: {e}"[:2000]}
                try:
                    _send(conn, msgpack_io.pack(word))
                except OSError:
                    return
        finally:
            conn.close()

    def _join(self, stop: Optional[threading.Event]) -> socket.socket:
        deadline, last = time.monotonic() + self.join_s, None
        while time.monotonic() < deadline and (stop is None or not stop.is_set()):
            try:
                conn = socket.create_connection((self.host, self.port), timeout=10.0)
            except OSError as e:
                last = e
                time.sleep(_RETRY_S)
                continue
            conn.settimeout(None)
            conn.setsockopt(socket.IPPROTO_TCP, socket.TCP_NODELAY, 1)
            _send(conn, msgpack_io.pack({"rank": self.rank}))
            return conn
        raise ConnectionError(f"rank {self.rank} of {self.size} could not reach rank 0 at {self.host}:{self.port} "
                              f"within {self.join_s:g} s: {last}")


class Mirrored(concurrent.futures.Executor):
    """Rank 0's policy thread as a copy of the policy's own sees it (episodes.PolicyCopy.attach): a call of one of `ops`
    - {its name: the bound method} - sent to every rank by `group` before it runs here (Group.run), any other call run
    as it is."""

    def __init__(self, thread: concurrent.futures.Executor, group: Group, ops: Mapping[str, Callable]) -> None:
        self._thread, self._group = thread, group
        self._names = {_key(fn): name for name, fn in ops.items()}

    def submit(self, fn: Callable, /, *args: Any, **kwargs: Any) -> concurrent.futures.Future:
        """`fn(*args, **kwargs)` on the policy thread - sent to every rank first where it is one of the ops."""
        name = self._names.get(_key(fn))
        if name is None:
            return self._thread.submit(fn, *args, **kwargs)
        return self._thread.submit(self._group.run, name, list(args), functools.partial(fn, *args, **kwargs))

    def shutdown(self, wait: bool = True, *, cancel_futures: bool = False) -> None:
        """The policy thread's own shutdown."""
        self._thread.shutdown(wait=wait, cancel_futures=cancel_futures)


def _key(fn: Callable) -> tuple:
    """A bound method by what it is bound to and its function - each access to a method makes a new bound one."""
    return id(getattr(fn, "__self__", None)), getattr(fn, "__func__", fn)


def _send(conn: socket.socket, body: bytes) -> None:
    conn.sendall(_LENGTH.pack(len(body)) + body)


def _recv(conn: socket.socket) -> Any:
    """One message, read back. EOFError where the other side closed."""
    (length,) = _LENGTH.unpack(_exactly(conn, _LENGTH.size))
    return msgpack_io.unpack(_exactly(conn, length))


def _exactly(conn: socket.socket, n: int) -> bytes:
    parts, left = [], n
    while left:
        part = conn.recv(min(left, 1 << 20))
        if not part:
            raise EOFError("the other rank closed its connection")
        parts.append(part)
        left -= len(part)
    return b"".join(parts)
