# SPDX-FileCopyrightText: Copyright (c) 2026 General Sequences Company
# SPDX-License-Identifier: Apache-2.0
"""
A policy server in one call: your model as a function, served to robots elsewhere.

    import sequence_ai

    def policy(observation):                     # your model: one observation in, what the robot needs out
        return {"actions": model(observation["image"], observation["state"])}

    sequence_ai.serve(policy, port=8000, example=observation)

On the robot, sequence_ai.connect("http://<this machine>:8000") acts on it (sequence_ai.network.link).

In one sentence: serve() listens on every address of this machine → a robot POSTs an observation to /act as msgpack →
the server restores what the robot compressed and turns each picture the robot sent as JPEG back into its array → the
policy is called with it on a thread of its own, one call at a time (with `batch`, on a list of the observations
waiting) → its output goes back as msgpack, numpy arrays as arrays, in one write, with how long the server took
(Server-Timing).

What each part does by default, and how to change it:

    one call at a time   the policy runs on one thread of its own, one call at a time; requests that   -
                         arrive meanwhile wait their turn, in order
    batching             off                                                                          batch=[1, 2, 4, 8]
    addresses            every address of this machine: 0.0.0.0, and :: where it has IPv6             host="127.0.0.1"
    pictures as JPEG     says it reads them (X-Seq-Reads), so a robot's connect() sends each HxWx3    jpeg=False
                         uint8 picture as JPEG; each is turned back into its array before the policy
    compression          says it reads zstd and zlib, so a robot's connect() compresses its large     compress=False
                         arrays where that saves time; they are restored byte for byte
    ping                 GET /ping is answered at once, even while the policy runs: 503 with          -
                         Retry-After until the warm-up is done, then 200 with what it is, as JSON
                         (server, version, up_s, pid, policy)
    identity             X-Seq-Server: sequence-ai/<version> on every response, so a robot can tell   -
                         serve() from another program at the address it was given
    once per act         copies of one act - a robot's over each of its uplinks (network.lines),      -
                         each with the act's X-Seq-Request-Id - run the policy once: each copy gets
                         that answer, kept 30 s, and X-Seq-Reads says "once"
    halves               an act a robot sends in two halves, each on a connection of its own          -
                         (X-Seq-Half), is joined and run as one: the first half gets the answer, the
                         second 202 when it is here; X-Seq-Reads says "split"
    warm-up              with `example`, the policy runs on it twice at each batch size before        example=None
                         /ping says ready, and GET /example hands it out
    inputs               numpy arrays as arrays, each the policy's own to write into                  -
    outputs              torch tensors and JAX arrays come back as numpy arrays (bfloat16 as          -
                         float32), copied on the policy's thread
    one write            each response leaves in one write (one_write)                                -
    server time          Server-Timing: act;dur= the ms from the request's last byte to its           -
                         response, model;dur= the ms of the policy call that served it
    token                none, unless $SEQ_SERVE_TOKEN is set                                         token="..."
    keep-alive           an idle connection is kept open 5 minutes                                    -

Only the switches above change what the server says it reads: whatever arrives compressed or as JPEG is restored all
the same, since restoring it is what the robot that sent it asked for.

WHY a thread of its own: a model's forward pass blocks for tens of milliseconds, and on the event loop it would hold
every ping and every upload in progress for as long: with a 200 ms stand-in model, a ping's p50 was 153 ms with the
model on the event loop and 1.0 ms with it on its own thread. It makes no request faster: with one policy, requests
wait their turn either way (316 ms against 320 ms there), and what serves several robots sooner is `batch`. CUDA and
JAX keep state per thread (the current device and stream, a trace's context), so the policy always runs on the same
one, its warm-up included.
WHY /ping answers from the event loop: a robot pings its idle connection to keep its window open, and waits for the
answer before its next request when the two meet (link.py); a ping queued behind the model would cost that request the
model's time.
WHY torch and JAX outputs are copied to numpy on the policy's thread: copying a GPU tensor waits for the GPU to finish
it, which must not happen on the event loop; msgpack carries numpy arrays.

`App` is the ASGI app serve() runs, for an ASGI server of your own: uvicorn.run(WholeResponse(App(policy)),
http=one_write_http()) is serve() without its listening sockets and logging.

Standard library and sequence-ai's own modules; uvicorn, which sequence-ai installs, is imported when serve() starts.
"""
from __future__ import annotations

import asyncio
import collections
import concurrent.futures
import errno
import hmac
import inspect
import json
import logging
import os
import socket
import time
from typing import Any, Callable, Iterable, Optional

from ..network import compressed, frames, msgpack_io
from ..network.link import (COPY_HEADER, HALF_HEADER, HALF_MISSING, ONCE, READS_HEADER, REQUEST_HEADER, SERVER_HEADER,
                            SPLIT)
from .batcher import Batcher

__all__ = ["App", "serve", "TOKEN_ENV", "LIMIT", "KEEP_ALIVE_S"]

log = logging.getLogger("sequence_ai.serve")

TOKEN_ENV = "SEQ_SERVE_TOKEN"     # read where serve() is given no token, as the check command reads it for --token
LIMIT = 64 << 20                  # the most bytes a request's body, and each item in it restored, may hold
KEEP_ALIVE_S = 300                # how long an idle connection is kept open: a robot paused for minutes resumes on it
RETRY_AFTER_S = 1                 # what a ping during the warm-up says to wait
# How long, and for how many acts, an act's answer is kept for another copy of it (REQUEST_HEADER): a robot's copies
# of one act, one over each of its uplinks, reach the server within the slower uplink's delay of each other.
ONCE_KEEP_S = 30.0
ONCE_KEEP_N = 256
# An act's halves (HALF_HEADER): how long its first half waits for its second before it is answered HALF_MISSING, and
# for how many acts halves are kept while they wait. Two halves sent at once over one path come within its jitter of
# each other, a lost packet's resend within a few hundred milliseconds.
HALF_WAIT_S = 2.0
HALF_KEEP_N = 64

_TEXT = b"text/plain; charset=utf-8"
_REQUEST = REQUEST_HEADER.lower().encode()
_HALF = HALF_HEADER.lower().encode()
_FIRST, _SECOND = b"1/2", b"2/2"
_COPY = (COPY_HEADER.lower().encode(), b"1")


class _Halves:
    """One act's halves as they come (App._half): each half's bytes, when the first of them came, the act's answer and
    when its body was whole once both are here (joined), and whether a first half has taken that answer."""

    __slots__ = ("first", "second", "came", "joined", "taken")

    def __init__(self) -> None:
        self.first: Optional[bytes] = None
        self.second: Optional[bytes] = None
        self.came = time.monotonic()
        self.joined: asyncio.Future = asyncio.get_running_loop().create_future()
        self.taken = False


class App:
    """
    The ASGI app serve() runs (the module's docstring has what each part does): POST /act, GET /ping, GET /example.
    The policy is warmed up when the server starts (its lifespan) or, with no lifespan, at the first request.

    policy     a function: an observation in, the response's value out. With `batch`, a function from a list of
               observations to a list of outputs, one for each, in order
    batch      None: one observation per call. A list of sizes, 1 among them: the observations waiting are passed as
               a list of the largest listed size they fill (engine.batcher)
    wait_ms    with `batch`, how long a batch that is not full waits for more while the policy is free
    token      requests must carry Authorization: Bearer <token>; None or "": no token is asked for
    example    an observation: the warm-up runs the policy on it, and GET /example hands it out
    jpeg       whether the server says it reads pictures sent as JPEG
    compress   whether it says it reads compressed arrays
    limit      the most bytes a body may hold, and each compressed item or picture in it once restored
    """

    def __init__(self, policy: Callable[[Any], Any], *, batch: Optional[Iterable[int]] = None, wait_ms: float = 2.0,
                 token: Optional[str] = None, example: Any = None, jpeg: bool = True, compress: bool = True,
                 limit: int = LIMIT) -> None:
        if not callable(policy):
            hint = ": an openpi Policy is served as policy.infer" if hasattr(policy, "infer") else ""
            raise TypeError(f"serve() takes the policy as a function, an observation in and its output out; it was "
                            f"given a {type(policy).__name__}{hint}")
        if inspect.iscoroutinefunction(policy) or inspect.iscoroutinefunction(type(policy).__call__):
            raise TypeError("the policy is an async function: serve() calls it on a thread of its own, so pass a plain "
                            "function")
        self._policy = policy
        self._sizes = None if batch is None else sorted({int(n) for n in batch})
        if self._sizes is not None and self._sizes[0] < 1:
            raise ValueError(f"batch sizes {self._sizes}: each is a number of observations, 1 or more")
        self._batcher = Batcher(self._run, sizes=self._sizes or (1,), wait_ms=wait_ms, runners=1)
        self._token = token.encode() if token else None
        self._limit = int(limit)
        self._example_body = None if example is None else msgpack_io.pack(example)
        # what it restores, that it runs an act once by its request id (ONCE) and that it joins an act's halves (SPLIT):
        # a robot sends an act over two uplinks, or in two halves, only to a server that says so
        said = ([frames.PICTURE_KIND] if jpeg else []) + (list(compressed.CODECS) if compress else []) + [ONCE, SPLIT]
        self._reads, self._jpeg = ", ".join(said).encode(), bool(jpeg)
        # each act's answer by its request id, while its copies may still come: (when it was first seen, its answer)
        self._once: "collections.OrderedDict[bytes, tuple[float, asyncio.Future]]" = collections.OrderedDict()
        # the halves of each act by its request id, while the other half may still come (_half)
        self._halves: "collections.OrderedDict[bytes, _Halves]" = collections.OrderedDict()
        # what it says it is, on every response and, at more length, in its ping's answer (link.SERVER_HEADER)
        self._version, self._began = _version(), time.monotonic()
        self._name = getattr(policy, "__qualname__", None) or type(policy).__name__
        self._identity = f"sequence-ai/{self._version}".encode()
        self._thread = concurrent.futures.ThreadPoolExecutor(max_workers=1, thread_name_prefix="sequence_ai-policy")
        # "starting" until the server starts, "warming" while the policy runs on the example, then "ready" or "failed"
        self._state = "starting"
        self._warming: Optional[asyncio.Future] = None
        self.failure: Optional[BaseException] = None      # what the policy raised on the example, if it did
        self.on_failure: Optional[Callable[[], None]] = None

    @property
    def ready(self) -> bool:
        """Whether /ping says 200: the server has started and the warm-up, if any, is done."""
        return self._state == "ready"

    # ── the policy, on its own thread ────────────────────────────────────────────────────────────────────────────────
    def _call(self, items: list) -> list:
        """On the policy's thread: the policy's outputs for `items`, each with arrays of other libraries as numpy
        arrays, and how long that took, as [(output, seconds)]."""
        started = time.perf_counter()
        if self._sizes is None:
            outputs = [self._policy(items[0])]
        else:
            got = self._policy(items)
            if isinstance(got, dict) or not hasattr(got, "__len__"):
                raise TypeError(f"the batch function returned a {type(got).__name__} for a batch of {len(items)}: it "
                                "returns a list, one output for each observation, in order")
            outputs = list(got)
            if len(outputs) != len(items):
                raise ValueError(f"the batch function returned {len(outputs)} outputs for a batch of {len(items)}: "
                                 "one output for each observation, in order")
        outputs = [_numpy(output) for output in outputs]
        took = time.perf_counter() - started
        return [(output, took) for output in outputs]

    async def _run(self, items: list) -> list:
        return await asyncio.get_running_loop().run_in_executor(self._thread, self._call, items)

    def _start(self) -> None:
        if self._state != "starting":
            return
        if self._example_body is None:
            self._state = "ready"
            return
        self._state = "warming"
        self._warming = asyncio.ensure_future(self._warm_up())

    async def _warm_up(self) -> None:
        """The policy on the example, twice at each batch size: the first call compiles what it compiles, the second
        shows the time it settles at. The example reaches it as a robot's observation does: read back from msgpack and,
        where the server reads JPEG, its pictures sent as JPEG and restored - so the first robot's request does not pay
        for loading the JPEG decoder, which it would on the event loop."""
        loop = asyncio.get_running_loop()
        try:
            body = self._example_body                 # the body a robot sends: its pictures as JPEG, where read
            if self._jpeg:
                body = msgpack_io.pack(frames.pack_pictures(msgpack_io.unpack(body))[0])
            example = _own(self._restore(body))
        except Exception as e:  # noqa: BLE001 (Pillow missing or broken: the robots' pictures would fail the same way)
            self._fail(e)
            return
        try:
            for n in self._sizes or [1]:
                took = []
                for _ in range(2):
                    started = time.perf_counter()
                    answered = await loop.run_in_executor(self._thread, self._call, [example] * n)
                    for output, _ in answered:
                        msgpack_io.pack(output)       # an output that cannot be sent fails here, not at a robot
                    took.append(time.perf_counter() - started)
                what = "one observation" if self._sizes is None else f"a batch of {n}"
                log.info("warm-up: %s took %s, then %s", what, _duration(took[0]), _duration(took[1]))
        except Exception as e:  # noqa: BLE001 (whatever the policy raised: serve() raises it once the server stops)
            self._fail(e)
            return
        self._state = "ready"
        log.info("ready")

    def _fail(self, e: BaseException) -> None:
        self.failure = e
        self._state = "failed"
        log.error("the policy failed on the example (%s): stopping", _said(e))
        if self.on_failure is not None:
            self.on_failure()

    def close(self) -> None:
        """Stop the warm-up and the policy's thread; a call in progress finishes on it."""
        if self._warming is not None and not self._warming.done():
            self._warming.cancel()
        self._thread.shutdown(wait=False, cancel_futures=True)

    # ── HTTP ──────────────────────────────────────────────────────────────────────────────────────────────────────────
    async def __call__(self, scope, receive, send) -> None:
        if scope["type"] == "lifespan":
            await self._lifespan(receive, send)
            return
        if scope["type"] != "http":
            return                                       # serve() runs uvicorn with no WebSocket protocol
        self._start()
        path, method = scope["path"], scope["method"]
        if self._token is not None and not self._authorized(scope):
            await self._respond(send, 401, b"this server needs its token: Authorization: Bearer <token>",
                                extra=[(b"www-authenticate", b"Bearer")])
        elif path == "/act":
            if method == "POST":
                await self._act(scope, receive, send)
            else:
                await self._respond(send, 405, b"POST /act", extra=[(b"allow", b"POST")])
        elif path == "/ping":
            if method in ("GET", "HEAD"):
                await self._ping(send)
            else:
                await self._respond(send, 405, b"GET /ping", extra=[(b"allow", b"GET, HEAD")])
        elif path == "/example":
            if method != "GET":
                await self._respond(send, 405, b"GET /example", extra=[(b"allow", b"GET")])
            elif self._example_body is None:
                await self._respond(send, 404, b"no example: this server was started without one (serve(example=...))")
            else:
                await self._respond(send, 200, self._example_body, content_type=msgpack_io.MEDIA_TYPE.encode())
        else:
            await self._respond(send, 404, b"this server answers POST /act, GET /ping and GET /example")

    async def _lifespan(self, receive, send) -> None:
        while True:
            message = await receive()
            if message["type"] == "lifespan.startup":
                self._start()
                await send({"type": "lifespan.startup.complete"})
            elif message["type"] == "lifespan.shutdown":
                self.close()
                await send({"type": "lifespan.shutdown.complete"})
                return

    def _restore(self, body: bytes) -> Any:
        """A request's body as its observation: msgpack read, what the robot compressed restored, each picture it sent
        as JPEG turned back into its array. ValueError for a body that is none of these."""
        return frames.unpack_pictures(compressed.expand(msgpack_io.unpack(body), limit=self._limit)[0],
                                      limit=self._limit)

    def _authorized(self, scope) -> bool:
        scheme, _, credential = _header(scope, b"authorization").partition(b" ")
        return scheme.lower() == b"bearer" and hmac.compare_digest(credential.strip(), self._token or b"")

    async def _ping(self, send) -> None:
        if self._state == "ready":
            said = {"server": "sequence-ai", "version": self._version, "up_s": round(time.monotonic() - self._began, 1),
                    "pid": os.getpid(), "policy": self._name}
            await self._respond(send, 200, json.dumps(said).encode(), content_type=b"application/json")
        elif self._state == "failed":
            await self._respond(send, 500, f"the policy failed on the example: {_said(self.failure)}".encode())
        else:
            await self._respond(send, 503, b"warming up: the policy is running on the example",
                                extra=[(b"retry-after", str(RETRY_AFTER_S).encode())])

    async def _act(self, scope, receive, send) -> None:
        declared = _header(scope, b"content-length")
        if declared.isdigit() and int(declared) > self._limit:
            await self._too_large(send)
            return
        body = await _body(receive, self._limit)
        if body is None:
            await self._too_large(send)
            return
        began = time.perf_counter()
        rid, half = _header(scope, _REQUEST), _header(scope, _HALF)
        if half:
            await self._half(send, rid, half, body)
            return
        held = self._held(rid) if rid else None
        extra: list = []
        if held is not None:
            # another copy of this act came in first (REQUEST_HEADER): its answer, the policy run for that one alone
            extra.append(_COPY)
        else:
            held = asyncio.ensure_future(self._reply(body))
            if rid:
                self._hold(rid, held)
        await self._answer(send, held, began, extra)

    async def _half(self, send, rid: bytes, half: bytes, body: bytes) -> None:
        """One half of an act (HALF_HEADER), in either order: kept until the other is here, then the act's body joined
        and run as an act of its own - its answer to the first half, 202 to the second as soon as it is here. The first
        half waits HALF_WAIT_S at most from when either came, then is answered HALF_MISSING: the robot sends the act
        whole. A half of an act already run (its copy came whole, over another uplink) gets what that act got."""
        if half not in (_FIRST, _SECOND) or not rid:
            await self._respond(send, 400, f"{HALF_HEADER} is 1/2 or 2/2, beside the act's {REQUEST_HEADER}".encode())
            return
        held, halves, extra = self._held(rid), None, []
        if held is not None:
            extra.append(_COPY)
        else:
            halves = self._halves.get(rid)
            if halves is None:
                self._let_go_of_halves()
                halves = self._halves[rid] = _Halves()
            if half == _FIRST:
                halves.first = body
            else:
                halves.second = body
            if halves.first is not None and halves.second is not None:
                held = asyncio.ensure_future(self._reply(halves.first + halves.second))
                self._hold(rid, held, joined=True)
        if half == _SECOND:
            await self._respond(send, 202, b"")
            return
        began = time.perf_counter()
        if held is None:
            try:
                held, began, copy = await asyncio.wait_for(asyncio.shield(halves.joined),
                                                           max(0.0, HALF_WAIT_S - (time.monotonic() - halves.came)))
            except asyncio.TimeoutError:
                if self._halves.get(rid) is halves:
                    del self._halves[rid]
                await self._respond(send, HALF_MISSING, f"the second half of this act ({HALF_HEADER} 2/2) did not "
                                    f"come within {HALF_WAIT_S:g} s: send the act whole".encode())
                return
            if copy:                                 # a whole copy of the act ran it while this half waited
                extra.append(_COPY)
        if halves is not None:
            if halves.taken and not extra:           # another copy's first half took the answer first
                extra.append(_COPY)
            halves.taken = True
        await self._answer(send, held, began, extra)

    async def _answer(self, send, held: asyncio.Future, began: float, extra: list) -> None:
        """An act's answer, from `held`, with how long the server took from `began` (the act's last byte) to it."""
        # shielded: a copy whose robot is gone takes nothing from the other copy's answer
        status, payload, content_type, model_s = await asyncio.shield(held)
        timing = None if model_s is None else (f"act;dur={(time.perf_counter() - began) * 1000:.1f}, "
                                               f"model;dur={model_s * 1000:.1f}")
        await self._respond(send, status, payload, content_type=content_type, timing=timing, extra=extra)

    async def _reply(self, body: bytes) -> tuple:
        """What /act answers `body` with: (status, body, its content type, the policy's seconds - None where the policy
        did not answer it)."""
        if len(body) > self._limit:                  # an act's two halves joined, each of them within it
            return 413, f"the act's halves are over this server's limit of {self._limit} bytes".encode(), _TEXT, None
        try:
            observation = _own(self._restore(body))
        except ValueError as e:                      # MsgpackError, CompressedError, a picture that is not a JPEG
            return 400, f"not an observation this server can read: {e}".encode(), _TEXT, None
        try:
            output, model_s = await self._batcher(observation)
        except Exception as e:  # noqa: BLE001 (whatever the policy raised: the robot is told, and the log has where)
            log.exception("the policy raised on an observation")
            return 500, f"the policy raised {_said(e)}".encode(), _TEXT, None
        try:
            payload = msgpack_io.pack(output)
        except msgpack_io.MsgpackError as e:
            log.error("the policy's output cannot be sent: %s", e)
            return 500, f"the policy's output cannot be sent as msgpack: {e}".encode(), _TEXT, None
        return 200, payload, msgpack_io.MEDIA_TYPE.encode(), model_s

    def _held(self, rid: bytes) -> Optional[asyncio.Future]:
        """The answer, done or coming, of the act with request id `rid` if it came within ONCE_KEEP_S; else None."""
        kept = self._once.get(rid)
        if kept is None or time.monotonic() - kept[0] > ONCE_KEEP_S:
            return None
        return kept[1]

    def _hold(self, rid: bytes, answer: asyncio.Future, *, joined: bool = False) -> None:
        """Keep `answer` for the other copies of the act `rid` names, and hand it to a first half of that act waiting
        for it: the act its halves made (`joined`), or a copy of it that came whole. The oldest answers kept are let go
        once past ONCE_KEEP_S or ONCE_KEEP_N, never one still being worked out."""
        now = time.monotonic()
        self._once[rid] = (now, answer)
        self._once.move_to_end(rid)
        while self._once:
            oldest, (seen, kept) = next(iter(self._once.items()))
            if not (now - seen > ONCE_KEEP_S or len(self._once) > ONCE_KEEP_N) or not kept.done():
                break
            del self._once[oldest]
        halves = self._halves.pop(rid, None)         # its halves: `joined` here, or waiting while a whole copy ran it
        if halves is not None and not halves.joined.done():
            halves.joined.set_result((answer, time.perf_counter(), not joined))

    def _let_go_of_halves(self) -> None:
        """Before another act's halves are kept: those kept past HALF_WAIT_S let go, and the oldest until fewer than
        HALF_KEEP_N acts' are - a first half that waited for them is answered HALF_MISSING at its wait's end."""
        now = time.monotonic()
        while self._halves:
            rid, halves = next(iter(self._halves.items()))
            if now - halves.came <= HALF_WAIT_S and len(self._halves) < HALF_KEEP_N:
                break
            del self._halves[rid]

    async def _too_large(self, send) -> None:
        await self._respond(send, 413, f"the body is over this server's limit of {self._limit} bytes".encode(),
                            close=True)

    async def _respond(self, send, status: int, body: bytes, *, content_type: bytes = _TEXT,
                       timing: Optional[str] = None, close: bool = False, extra: Iterable = ()) -> None:
        headers = [(b"content-type", content_type), (b"content-length", str(len(body)).encode()),
                   (READS_HEADER.lower().encode(), self._reads), (SERVER_HEADER.lower().encode(), self._identity),
                   *extra]
        if timing is not None:
            headers.append((b"server-timing", timing.encode()))
        if close:
            headers.append((b"connection", b"close"))  # the rest of a body over the limit is not read
        await send({"type": "http.response.start", "status": status, "headers": headers})
        await send({"type": "http.response.body", "body": body})


def _header(scope, name: bytes) -> bytes:
    for key, value in scope.get("headers", ()):
        if key.lower() == name:
            return value
    return b""


async def _body(receive, limit: int) -> Optional[bytes]:
    """The request's body, or None once it is over `limit` bytes (what is left of it is not read)."""
    chunks, size = [], 0
    while True:
        message = await receive()
        if message["type"] == "http.disconnect":
            break
        chunk = message.get("body", b"")
        size += len(chunk)
        if size > limit:
            return None
        chunks.append(chunk)
        if not message.get("more_body"):
            break
    return b"".join(chunks)


def _own(value: Any) -> Any:
    """`value` with each read-only numpy array in it - in dicts, lists and tuples - as a writable copy, the policy's
    own.
    WHY: msgpack hands out arrays that read the request's bytes in place, and torch.from_numpy warns about each of them
    (and torch.as_tensor on the CPU), while a policy that writes into its observation fails; a copy costs a few
    microseconds for a camera frame."""
    if isinstance(value, dict):
        return {key: _own(item) for key, item in value.items()}
    if type(value) in (list, tuple):
        return type(value)(_own(item) for item in value)
    flags = getattr(value, "flags", None)
    if flags is not None and hasattr(value, "copy") and not getattr(flags, "writeable", True):
        return value.copy()
    return value


def _numpy(value: Any) -> Any:
    """`value` with each torch tensor and JAX array in it - in dicts, lists and tuples - as a numpy array, a dtype numpy
    or msgpack does not carry (bfloat16) as float32. Everything else is returned as it is: msgpack_io.pack names what it
    cannot send."""
    if isinstance(value, dict):
        return {key: _numpy(item) for key, item in value.items()}
    if type(value) in (list, tuple):
        return type(value)(_numpy(item) for item in value)
    if value is None or isinstance(value, (str, bytes, bytearray, bool, int, float)):
        return value
    import numpy as np

    if isinstance(value, np.generic):
        return value
    if not isinstance(value, np.ndarray):
        if callable(getattr(value, "detach", None)) and callable(getattr(value, "cpu", None)):   # a torch tensor
            tensor = value.detach().cpu()
            try:
                return tensor.numpy()
            except TypeError:                         # a dtype numpy has no counterpart for: bfloat16, float8
                return tensor.float().numpy()
        if not hasattr(value, "__array__"):
            return value
        value = np.asarray(value)                     # a JAX array, or another library's that numpy can read
    if value.dtype.kind == "V" and value.dtype.fields is None:
        try:
            return value.astype(np.float32)           # ml_dtypes' bfloat16, as a JAX array reads into numpy
        except (TypeError, ValueError):
            return value                              # raw bytes: msgpack_io.pack names the dtype it cannot send
    return value


def _version() -> str:
    """sequence-ai's version as installed; "dev" in a source checkout that was never installed."""
    try:
        from importlib.metadata import version

        return version("sequence-ai")
    except Exception:  # noqa: BLE001 (no installed metadata: a checkout run as it is)
        return "dev"


def _said(e: BaseException) -> str:
    return f"{type(e).__name__}: {e}" if str(e) else type(e).__name__


def _duration(seconds: float) -> str:
    return f"{seconds:.1f} s" if seconds >= 1 else f"{seconds * 1000:.1f} ms"


# ── serve() ───────────────────────────────────────────────────────────────────────────────────────────────────────────
def serve(policy: Callable[[Any], Any], *, host: Optional[str] = None, port: int = 8000,
          batch: Optional[Iterable[int]] = None, wait_ms: float = 2.0, token: Optional[str] = None,
          example: Any = None, jpeg: bool = True, compress: bool = True, limit: int = LIMIT,
          log_level: str = "info") -> None:
    """
    Serve `policy` to robots elsewhere until the process is stopped (Ctrl-C), the module's docstring having what each
    part does by default:

        sequence_ai.serve(policy, port=8000, example=observation)                        # one observation per call
        sequence_ai.serve(policy_on_a_list, batch=[1, 2, 4, 8], example=observation)     # a list per call

    policy     a function: an observation in - a dict, as the robot sent it, numpy arrays as arrays, each its own to
               write into - and what the robot gets back out: a dict, an array, a list; torch tensors and JAX arrays
               are sent as numpy
    host       None: every address of this machine (0.0.0.0, and :: where it has IPv6). "127.0.0.1": this machine only
    port       the port, 8000
    batch      None: one observation per call. A list of batch sizes, 1 among them: `policy` takes a list of
               observations and returns a list of outputs, one for each, in order, and is called with the largest
               listed number of the observations waiting; with an openpi policy, engine.openpi.batched(policy)
    wait_ms    with `batch`, how long a batch that is not full waits for more while the policy is free (2 ms)
    token      a robot must send Authorization: Bearer <token> (connect(url, token=...)); None: $SEQ_SERVE_TOKEN if
               it is set, else no token; "": no token
    example    an observation the policy is run on before /ping says ready, at each batch size, and that GET /example
               hands out (the check command uses it)
    jpeg       False: the server does not say it reads JPEG, so a robot's connect() sends pictures as arrays, exactly
    compress   False: it does not say it reads compressed arrays, so a robot's connect() sends them as they are
    limit      the most bytes a request's body may hold, and each compressed item or picture in it restored: 64 MB
    log_level  uvicorn's and this module's: "info" says where it listens and how the warm-up went

    Raises what the policy raised on the example, once the server has stopped; OSError when the port is taken.
    """
    if token is None:
        token = os.environ.get(TOKEN_ENV) or None
    app = App(policy, batch=batch, wait_ms=wait_ms, token=token, example=example, jpeg=jpeg, compress=compress,
              limit=limit)
    server = _uvicorn(app, log_level)
    sockets = _listen(host, port)
    app.on_failure = lambda: setattr(server, "should_exit", True)
    _log_with(log_level)

    where = " and ".join(_url(sock) for sock in sockets)
    paths = "POST /act, GET /ping" + (", GET /example" if example is not None else "")
    calls = "one observation per call" if batch is None else \
        f"batches of {', '.join(str(n) for n in sorted({int(n) for n in batch}))}"
    restores = ", ".join(word for word in app._reads.decode().split(", ") if word and word not in (ONCE, SPLIT))
    log.info("serving %s on %s (%s); %s; reads %s; an act's copies run it once, its halves joined",
             getattr(policy, "__qualname__", type(policy).__name__), where, paths, calls,
             restores or "nothing but plain msgpack")
    if token:
        log.info("a robot needs the token: connect(url, token=...)")
    elif not all(_loopback(sock) for sock in sockets):
        log.warning("no token: anyone who can reach port %d can run the policy (serve(token=...) or $%s asks for one)",
                    sockets[0].getsockname()[1], TOKEN_ENV)
    try:
        server.run(sockets=sockets)
    except KeyboardInterrupt:
        pass                                          # Ctrl-C: uvicorn has shut down, and says so; as uvicorn.run()
    finally:
        app.close()
        for sock in sockets:
            sock.close()
    if app.failure is not None:
        raise app.failure


def _uvicorn(app: App, log_level: Optional[str]) -> Any:
    """The uvicorn server serve() runs `app` on: each response in one write, the app's lifespan for its warm-up, no
    WebSocket protocol, no line per request, idle connections kept KEEP_ALIVE_S."""
    try:
        import uvicorn
    except ImportError as missing:
        raise ImportError("serve() runs uvicorn, which sequence-ai installs and this environment lacks: "
                          "pip install sequence-ai") from missing
    from ..network.one_write import WholeResponse, one_write_http

    config = uvicorn.Config(WholeResponse(app), http=one_write_http(), lifespan="on", ws="none", log_level=log_level,
                            access_log=False, timeout_keep_alive=KEEP_ALIVE_S, server_header=False)
    return uvicorn.Server(config)


def _listen(host: Optional[str], port: int) -> list:
    """The bound sockets serve() listens on: for `host` None, 0.0.0.0 and, where this machine has IPv6, :: (IPv6 only,
    beside the first, on the same port); else the first address `host` resolves to. OSError when the port is taken."""
    loopbacks = [(socket.AF_INET, "127.0.0.1")] + ([(socket.AF_INET6, "::1")] if socket.has_ipv6 else [])
    if host is not None:
        family, _, _, _, address = socket.getaddrinfo(host, port, type=socket.SOCK_STREAM, flags=socket.AI_PASSIVE)[0]
        if address[0] in ("0.0.0.0", "::"):
            _unanswered(port, [(f, a) for f, a in loopbacks if f == family])
        return [_bind(family, address[0], port)]
    _unanswered(port, loopbacks)
    sockets = [_bind(socket.AF_INET, "0.0.0.0", port)]
    if socket.has_ipv6:
        try:
            sockets.append(_bind(socket.AF_INET6, "::", sockets[0].getsockname()[1], v6only=True))
        except OSError as e:
            if e.errno not in (errno.EAFNOSUPPORT, errno.EADDRNOTAVAIL, errno.EPROTONOSUPPORT):
                sockets[0].close()
                raise
            log.debug("no IPv6 address to listen on: %s", e)
    return sockets


def _unanswered(port: int, loopbacks: list) -> None:
    """OSError when a server already answers at `port` on this machine's loopback.
    WHY: macOS lets a socket bind every address (0.0.0.0) at a port another program holds on 127.0.0.1, and a robot on
    this machine then reaches the other program; a server that started all the same would never see its requests."""
    if not port:
        return
    for family, address in loopbacks:
        with socket.socket(family, socket.SOCK_STREAM) as probe:
            probe.settimeout(0.5)
            if probe.connect_ex((address, port)) != 0:
                continue                              # refused, or no such address here: nothing answers there
        where = f"[{address}]:{port}" if family == socket.AF_INET6 else f"{address}:{port}"
        raise OSError(errno.EADDRINUSE, f"port {port} is taken: a server already answers at {where} on this machine "
                                        "(an earlier serve() still running?); stop it, or pass another port")


def _bind(family: int, address: str, port: int, *, v6only: Optional[bool] = None) -> socket.socket:
    sock = socket.socket(family, socket.SOCK_STREAM)
    try:
        if os.name != "nt":
            sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)   # a restarted server takes its port at once
        if v6only is not None:
            sock.setsockopt(socket.IPPROTO_IPV6, socket.IPV6_V6ONLY, int(v6only))
        sock.bind((address, port))
    except OSError as e:
        sock.close()
        if e.errno == errno.EADDRINUSE:
            raise OSError(e.errno, f"port {port} on {address} is taken: another server listens there (an earlier "
                                   "serve() still running?); stop it, or pass another port") from e
        raise
    return sock


def _url(sock: socket.socket) -> str:
    address, port = sock.getsockname()[:2]
    return f"http://[{address}]:{port}" if sock.family == socket.AF_INET6 else f"http://{address}:{port}"


def _loopback(sock: socket.socket) -> bool:
    address = sock.getsockname()[0]
    return address == "::1" or address.startswith("127.")


def _log_with(level: Optional[str]) -> None:
    """This module's lines through uvicorn's own handler, at its level, where nothing else is set up to show them. A root
    logger that would drop them counts as nothing: one a library set up at WARNING on import, as absl does for a JAX
    policy, would hide the warm-up and "ready" lines."""
    if level is None or log.handlers or logging.getLogger("sequence_ai").handlers:
        return
    wanted = logging.getLevelName(level.upper()) if isinstance(level, str) else level
    root = logging.getLogger()
    if root.handlers and root.isEnabledFor(wanted):
        return
    for handler in logging.getLogger("uvicorn").handlers:
        log.addHandler(handler)
    log.setLevel(wanted)
    log.propagate = False
