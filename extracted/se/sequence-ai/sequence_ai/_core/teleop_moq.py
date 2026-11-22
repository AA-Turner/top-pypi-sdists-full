"""
Media over QUIC for the people watching a robot (the teleop plan, 3b): its cameras and its steps published once, to a
MoQ relay, and any number of consoles watching them there - the relay makes the copies, so a robot uploads one stream
however many watch.

In one sentence: seq teleop serve --moq-port 4443 (a relay in the server's own process, Relay) or --moq URL (a relay of
your own, moq-relay) → each round of the robot's link says where (settings "moq": {"url", "broadcast", "fingerprints"})
→ the robot's Driven publishes there (Publisher): each step's arrays on its broadcast's track "state", one message a
group, packed as WebRTC's state channel packs them, and its catalog naming its cameras; each camera a broadcast of its
own beneath it ("<broadcast>/<camera>"), H.264 - its frames made I420 by PyAV, as the WebRTC tracks' are, and encoded only
while someone watches it → a console asks the server where (GET /v1/teleop/moq) and watches (Watch): stream() and
states() as a WebRTC console's, each camera's frames decoded to RGB → one person still drives, over WebRTC, straight to
the robot.
WHY a relay: N people watching straight were N uploads from the robot; through a relay they are one.


WHY watching alone: one person drives at a time, and their commands go faster straight than through a hop more.
WHY I420 by PyAV: the binding's own conversion from RGBA cost each frame 5.1 ms of the robot's time; PyAV's to I420
0.5 ms, and the encoder fed I420 3.0 ms.

WHY a camera is encoded only while watched: a robot no one watches through the relay spends nothing on it - its track's
demand says so - and a viewer that comes starts at a keyframe made then (cut), not at the relay's copy of the last one.
WHY a broadcast a camera: a broadcast's video renditions are one picture at several sizes, a player showing the one
that fits (MoQ's browser player, @moq/watch); a robot's cameras are several pictures, each its own broadcast.
WHY one version: MoQ is an IETF draft and its wire changes between releases. The binding is pinned (pyproject.toml, the
extra moq), and a relay of your own speaks its version: moq-relay 0.17, the one tested.
Depth and Tactile items do not go this way: their streams decode from a keyframe the robot makes when a console asks for
one, and a watcher here asks the robot nothing. They go to WebRTC consoles as before.
"""
from __future__ import annotations

import asyncio
import collections
import concurrent.futures
import hmac
import http.server
import json
import logging
import queue
import secrets
import socket
import threading
import time
import urllib.parse
import urllib.request
from typing import Any, Optional

from sequence_ai.errors import InvalidRequest, MissingPackage, Unavailable
from sequence_ai._core import latency_stats as _stats
from sequence_ai._core import msgpack_io as _msgpack
from sequence_ai._core import teleop_clock as _clock
from sequence_ai._core.teleop import Views

INSTALL = "pip install 'sequence-ai[moq]'"
MOQ = "/v1/teleop/moq"
STATE = "state"
CAMERAS = "cameras"
GOP_S = 2.0
_AGAIN_MOST_S = 5.0
_STEPS_KEPT = 512
_GAP_FRAMES = 2
_CLOSE_S = 3.0
_CAMERA_S = 5.0
log = logging.getLogger("sequence_ai.teleop")


def require() -> Any:
    """The binding (moq-rs), or MissingPackage saying what to install."""
    try:
        import moq
    except ImportError:
        raise MissingPackage("a robot's watchers through a MoQ relay need moq-rs, Python 3.10 or later",
                             hint=INSTALL) from None
    return moq


def shown(url: str) -> str:
    """A relay's address as it may be printed: its token, and anything else after the path, left out."""
    parts = urllib.parse.urlsplit(url)
    return urllib.parse.urlunsplit((parts.scheme, parts.netloc, parts.path, "", ""))


def external(url: str, timeout_s: float = 5.0) -> dict:
    """A relay of your own (seq teleop serve --moq URL), as its clients reach it: https:// with a certificate they
    trust; http:// for one that made its own, its fingerprint read from it (moq-relay's /certificate.sha256, as MoQ's
    browser library reads it) and its clients sent to https:// on the same port, the certificate pinned."""
    parts = urllib.parse.urlsplit(url)
    if parts.scheme not in ("http", "https") or not parts.hostname:
        raise InvalidRequest(f"--moq is a relay's address, https://HOST:PORT/ - not {shown(url)!r}")
    if parts.scheme == "https":
        return {"url": url, "fingerprints": []}
    at = urllib.parse.urlunsplit(("http", parts.netloc, "/certificate.sha256", "", ""))
    try:
        with urllib.request.urlopen(at, timeout=timeout_s) as answer:
            printed = answer.read().decode().strip()
    except OSError as exc:
        raise Unavailable(f"the MoQ relay at {shown(url)} did not say its certificate's fingerprint ({at}): {exc}",
                          hint="start the relay first, or give its https:// address") from None
    return {"url": urllib.parse.urlunsplit(("https",) + tuple(parts[1:])), "fingerprints": [printed]}


def _client(moq: Any, where: dict) -> Any:
    """A client of the relay `where` names: its certificate pinned by the fingerprints given, else checked as any."""
    prints = [str(p) for p in where.get("fingerprints") or ()]
    return moq.Client(str(where["url"]), websocket_enabled=False, **({"tls_fingerprints": prints} if prints else {}))


class _Loop:
    """An asyncio loop on a thread of its own: the binding's calls are coroutines, and a robot's observe() and a
    console's caller are threads."""

    def __init__(self, name: str) -> None:
        self.loop = asyncio.new_event_loop()
        self._thread = threading.Thread(target=self.loop.run_forever, daemon=True, name=name)
        self._thread.start()

    def submit(self, coro: Any) -> concurrent.futures.Future:
        return asyncio.run_coroutine_threadsafe(coro, self.loop)

    def call(self, fn: Any, *args: Any) -> None:
        if self.loop.is_running():
            self.loop.call_soon_threadsafe(fn, *args)

    def stop(self) -> None:
        self.call(self.loop.stop)
        self._thread.join(_CLOSE_S)
        if not self._thread.is_alive():
            self.loop.close()


def _bind(host: str, port: int) -> str:
    """Where a relay listens, as the binding takes it: the HTTP server's host, every address for every address."""
    if host in ("", "0.0.0.0", "::"):
        return f"[::]:{port}"
    try:
        socket.inet_pton(socket.AF_INET6, host)
        return f"[{host}]:{port}"
    except OSError:
        pass
    try:
        socket.inet_pton(socket.AF_INET, host)
        return f"{host}:{port}"
    except OSError:
        return f"{socket.gethostbyname(host)}:{port}"


def _cameras_of(catalog: Any) -> list:
    """The cameras a robot's catalog names (CAMERAS): [] where it names none, or not as a list of names."""
    try:
        named = json.loads((getattr(catalog, "sections", None) or {}).get(CAMERAS) or "[]")
    except ValueError:
        return []
    return [str(k) for k in named] if isinstance(named, list) else []


def _token_of(query: Optional[str]) -> str:
    return (urllib.parse.parse_qs(query or "").get("token") or [""])[0]


class _Http(http.server.ThreadingHTTPServer):
    daemon_threads = True
    allow_reuse_address = True


class _Http6(_Http):
    address_family = socket.AF_INET6


class Relay:
    """A MoQ relay in this process (seq teleop serve --moq-port): the binding's server on a loop of its own, with a
    certificate it makes itself - each client pins it by the fingerprint the teleop server hands out with its address -
    and a session taken only with the relay's token in its address (?token=), every other turned away (403). The
    fingerprint is also on TCP at the relay's port, /certificate.sha256, as moq-relay has it: where MoQ's browser library
    reads it for a relay addressed http:// (the page's watchers, teleop_console/console.js)."""

    def __init__(self, host: str, port: int) -> None:
        self.host, self.port = host, int(port)
        self.token = secrets.token_urlsafe(18)
        self.fingerprints: list = []
        self._loop: Optional[_Loop] = None
        self._stop: Optional[asyncio.Event] = None
        self._done: Optional[concurrent.futures.Future] = None
        self._http: Optional[_Http] = None

    def start(self, timeout_s: float = 10.0) -> "Relay":
        """Listening, or the reason it is not."""
        require()
        self._loop = _Loop("seq-teleop-moq-relay")
        ready = threading.Event()
        self._done = self._loop.submit(self._serve(ready))
        ready.wait(timeout_s)
        if self.fingerprints:
            self._serve_fingerprint()
            return self
        try:
            self._done.result(1.0)
        except concurrent.futures.TimeoutError:
            pass
        except Exception as exc:
            self.close()
            raise InvalidRequest(f"no MoQ relay at {_bind(self.host, self.port)}: {exc}") from None
        self.close()
        raise Unavailable(f"the MoQ relay at {_bind(self.host, self.port)} did not start within {timeout_s} s")

    async def _serve(self, ready: threading.Event) -> None:
        moq = require()
        self._stop = asyncio.Event()
        held: set = set()
        try:
            async with moq.Server(_bind(self.host, self.port), tls_generate=["localhost"]) as server:
                self.port = int(str(server.local_addr).rsplit(":", 1)[1])
                self.fingerprints = list(server.cert_fingerprints())
                ready.set()
                accepting = asyncio.ensure_future(self._accept(server, held))
                await self._stop.wait()
                accepting.cancel()
                for session in list(held):
                    session.shutdown()
        finally:
            ready.set()

    async def _accept(self, server: Any, held: set) -> None:
        async for request in server:
            if not hmac.compare_digest(_token_of(request.query), self.token):
                try:
                    await request.reject(403)
                except Exception:
                    pass
                continue
            asyncio.ensure_future(self._hold(request, held))

    def _serve_fingerprint(self) -> None:
        """/certificate.sha256 on TCP at the relay's port, the hex of its certificate's SHA-256 and nothing else, to any
        page (Access-Control-Allow-Origin: *): it is no secret, the token is. A port taken: said, and a browser cannot
        watch through this relay; a Python watcher still can, its fingerprint handed out by the teleop server."""
        printed = (self.fingerprints[0] if self.fingerprints else "").encode()

        class Handler(http.server.BaseHTTPRequestHandler):
            def do_GET(self) -> None:
                if urllib.parse.urlsplit(self.path).path != "/certificate.sha256":
                    self.send_error(404)
                    return
                self.send_response(200)
                self.send_header("Content-Type", "text/plain; charset=utf-8")
                self.send_header("Content-Length", str(len(printed)))
                self.send_header("Access-Control-Allow-Origin", "*")
                self.send_header("Cache-Control", "no-store")
                self.end_headers()
                self.wfile.write(printed)

            def log_message(self, format: str, *args: Any) -> None:
                pass

        host = "" if self.host in ("", "0.0.0.0") else self.host
        try:
            self._http = (_Http6 if ":" in host else _Http)((host, self.port), Handler)
        except OSError as exc:
            log.warning("the MoQ relay's certificate is not served on TCP port %d (%s): a browser cannot watch through "
                        "it, a Python watcher can", self.port, exc)
            return
        threading.Thread(target=self._http.serve_forever, kwargs={"poll_interval": 0.2}, daemon=True,
                         name="seq-teleop-moq-certificate").start()

    @staticmethod
    async def _hold(request: Any, held: set) -> None:
        """One session taken, held until it ends: the binding drops a session no one holds."""
        try:
            session = await request.accept()
        except Exception:
            return
        held.add(session)
        try:
            await session.closed()
        except Exception:
            pass
        finally:
            held.discard(session)

    def where(self, host: str) -> dict:
        """The relay as a client that reached the teleop server at `host` (its Host, no port) reaches it: the same
        name, on the relay's port - localhost as the address bound, where only a loopback is."""
        if host == "localhost" and self.host in ("127.0.0.1", "::1"):
            host = "127.0.0.1" if self.host == "127.0.0.1" else "[::1]"
        return {"url": f"https://{host}:{self.port}/?token={self.token}", "fingerprints": list(self.fingerprints)}

    def close(self) -> None:
        loop, self._loop = self._loop, None
        if loop is None:
            return
        served, self._http = self._http, None
        if served is not None:
            served.shutdown()
            served.server_close()
        if self._stop is not None:
            loop.call(self._stop.set)
        if self._done is not None:
            try:
                self._done.result(_CLOSE_S)
            except Exception:
                pass
        loop.stop()


class _Camera:
    """One camera's broadcast at the relay, and its video."""

    def __init__(self, broadcast: Any, producer: Any, shape: tuple) -> None:
        self.broadcast = broadcast
        self.producer = producer
        self.demand = producer.demand()
        self.shape = shape
        self.last_us: Optional[int] = None


def _i420(frame: Any) -> bytes:
    """An RGB frame (height x width x 3, uint8, both even) as I420: Y, then U, then V, each packed - PyAV's swscale, as
    the WebRTC tracks' frames are made (teleop_video.FrameTrack)."""
    import av

    return av.VideoFrame.from_ndarray(frame, format="rgb24").reformat(format="yuv420p").to_ndarray().tobytes()


def _even(frame: Any) -> Any:
    """`frame` cut to an even height and width, as 4:2:0 takes it; None for one that is no RGB picture."""
    import numpy as np

    if not isinstance(frame, np.ndarray) or frame.dtype != np.uint8 or frame.ndim != 3 or frame.shape[2] != 3:
        return None
    h, w = frame.shape[0] - frame.shape[0] % 2, frame.shape[1] - frame.shape[1] % 2
    if h < 2 or w < 2:
        return None
    return np.ascontiguousarray(frame[:h, :w])


class Publisher:
    """A robot's broadcast at a MoQ relay (module docstring): made by its Driven from its link's settings, fed from the
    robot's observe() thread - frames() and step() return at once, a thread of its own encoding - and closed with it."""

    def __init__(self, url: str, broadcast: str, fingerprints: Any = (), hz: float = 30.0) -> None:
        self.where = (str(url), str(broadcast), tuple(str(p) for p in fingerprints or ()))
        self.hz = float(hz or 30.0)
        self._lock = threading.Condition()
        self._latest: dict = {}
        self._cameras: dict = {}
        self._left_out: set = set()
        self._client: Any = None
        self._broadcast: Any = None
        self._state: Any = None
        self._state_demand: Any = None
        self._stepped = False
        self._closed = False
        self.counts = {"frames_encoded": 0, "frames_unwatched": 0, "frames_replaced": 0, "keyframes_cut": 0,
                       "states_sent": 0}
        self._stop: Optional[asyncio.Event] = None
        self._loop = _Loop("seq-teleop-moq")
        self._done = self._loop.submit(self._run())
        threading.Thread(target=self._encode, daemon=True, name="seq-teleop-moq-encode").start()

    async def _run(self) -> None:
        """Connected to the relay, its broadcast announced, until it closes: a relay that went away asked again."""
        moq = require()
        url, broadcast, prints = self.where
        self._stop = asyncio.Event()
        again_s = 0.0
        while not self._closed:
            try:
                async with _client(moq, {"url": url, "fingerprints": prints}) as client:
                    produced = client.create_broadcast(broadcast)
                    state = produced.publish_track(STATE)
                    produced.announce()
                    with self._lock:
                        self._client, self._broadcast, self._state = client, produced, state
                        self._state_demand, self._stepped = state.demand(), False
                        self._cameras.clear()
                        self._lock.notify_all()
                    log.info("this robot publishes its cameras and steps to the MoQ relay at %s", shown(url))
                    again_s = 0.0
                    stop, gone = asyncio.ensure_future(self._stop.wait()), asyncio.ensure_future(client.session.closed())
                    await asyncio.wait({stop, gone}, return_when=asyncio.FIRST_COMPLETED)
                    stop.cancel()
                    if gone.done() and not self._closed:
                        why = gone.exception() if not gone.cancelled() else None
                        raise ConnectionError(f"its connection ended{f': {why}' if why else ''}")
                    gone.cancel()
            except Exception as exc:
                if self._closed:
                    break
                if not again_s:
                    log.warning("this robot could not publish to the MoQ relay at %s: %s - asked again; its watchers "
                                "see nothing meanwhile", shown(url), exc)
                again_s = min(_AGAIN_MOST_S, again_s * 2 or 0.5)
                try:
                    await asyncio.wait_for(self._stop.wait(), again_s)
                except asyncio.TimeoutError:
                    pass
            finally:
                with self._lock:
                    cameras = list(self._cameras.values())
                    self._client = self._broadcast = self._state = self._state_demand = None
                    self._cameras.clear()
                for camera in cameras:
                    for end in (camera.producer.finish, camera.broadcast.close):
                        try:
                            end()
                        except Exception:
                            pass

    def watched(self) -> bool:
        """Whether its steps should come: connected, and someone watches - or its first step since it connected has
        not come, its cameras' tracks being made from it."""
        if self._broadcast is None:
            return False
        if not self._stepped:
            return True
        demand = self._state_demand
        if demand is not None and demand.is_used():
            return True
        return any(c.demand.is_used() for c in list(self._cameras.values()))

    def frames(self, raw: dict, t_us: int) -> None:
        """A step's camera frames, each camera's newest kept for its thread to encode - one it has not encoded yet
        replaced (frames_replaced)."""
        with self._lock:
            if self._closed:
                return
            for key, frame in raw.items():
                if key in self._latest:
                    self.counts["frames_replaced"] += 1
                self._latest[key] = (frame, int(t_us))
            self._lock.notify_all()

    def step(self, packed: bytes, t_us: int) -> None:
        """One step's arrays, packed: a group of its own on the state track."""
        self._stepped = True
        state = self._state
        if state is None:
            return
        try:
            state.write_frame(packed, timestamp_us=int(t_us))
            self.counts["states_sent"] += 1
        except Exception:
            pass

    def _encode(self) -> None:
        moq = None
        while True:
            with self._lock:
                while not self._closed and (not self._latest or self._broadcast is None):
                    self._lock.wait()
                if self._closed:
                    return
                latest, self._latest = self._latest, {}
            moq = moq or require()
            for key, (frame, t_us) in latest.items():
                try:
                    self._write(moq, key, frame, t_us)
                except Exception as exc:
                    self._leave_out(key, f"its frames could not be encoded: {exc}")

    def _write(self, moq: Any, key: str, frame: Any, t_us: int) -> None:
        if key in self._left_out:
            return
        camera, first = self._cameras.get(key), False
        if camera is None:
            camera, first = self._camera(moq, key, frame), True
            if camera is None:
                return
        if not first and not camera.demand.is_used():
            self.counts["frames_unwatched"] += 1
            return
        picture = _even(frame)
        if picture is None or picture.shape[:2] != camera.shape:
            self._leave_out(key, "its frames changed size" if picture is not None else "its frames are no RGB "
                            "pictures (height x width x 3, uint8)")
            return
        if camera.last_us is not None and t_us - camera.last_us >= _GAP_FRAMES * 1e6 / self.hz:


            try:
                camera.producer.cut()
                self.counts["keyframes_cut"] += 1
            except Exception:
                pass
        camera.producer.write(moq.VideoFrame(timestamp_us=int(t_us), data=_i420(picture)))
        camera.last_us = int(t_us)
        self.counts["frames_encoded"] += 1

    def _camera(self, moq: Any, key: str, frame: Any) -> Optional[_Camera]:
        """Camera `key`'s broadcast, beneath its own, made at its first frame - the size of that frame its size - and
        that frame written whoever watches, its codec then in its catalog; its name added to the robot's (CAMERAS)."""
        from sequence_ai._core.teleop_video import bitrate_cap

        client, broadcast, picture = self._client, self._broadcast, _even(frame)
        if client is None or broadcast is None:
            return None
        if picture is None:
            self._leave_out(key, "its frames are no RGB pictures (height x width x 3, uint8)")
            return None
        h, w = picture.shape[:2]
        own = client.create_broadcast(f"{self.where[1]}/{key}")
        producer = own.encode_video(
            moq.VideoEncoderInput(format=moq.VideoPixelFormat.I420, width=w, height=h,
                                  framerate=max(1, round(self.hz))),
            moq.VideoEncoderOutput(codec=moq.VideoCodec.H264, bitrate=bitrate_cap(w, h, self.hz),
                                   gop=max(1, round(self.hz * GOP_S)), kind=moq.VideoEncoderKind.AUTO()))
        own.announce()
        camera = self._cameras[key] = _Camera(own, producer, (h, w))
        broadcast.set_catalog_section(CAMERAS, sorted(self._cameras))
        return camera

    def _leave_out(self, key: str, why: str) -> None:
        if key not in self._left_out:
            self._left_out.add(key)
            log.warning("camera %r is not sent to the MoQ relay: %s", key, why)

    def stats(self) -> dict:
        """What it did: frames encoded, frames no one watched, frames a newer one replaced, steps sent; bytes sent
        to the relay, all told; its cameras' tracks."""
        sent = None
        client = self._client
        try:
            sent = client.session.stats().bytes_sent if client is not None and client.session is not None else None
        except Exception:
            pass
        return {**self.counts, "bytes_sent": sent, "cameras": sorted(self._cameras)}

    def close(self) -> None:
        with self._lock:
            if self._closed:
                return
            self._closed = True
            self._lock.notify_all()
        if self._stop is not None:
            self._loop.call(self._stop.set)
        try:
            self._done.result(_CLOSE_S)
        except Exception:
            pass
        self._loop.stop()


class _SameClock:
    """A watcher's view of the robot's clock: unknown until the robot's steps come live, and then the same as its own
    (NTP's), as nothing passes between them to say otherwise - frame_us and state_us are as true as the two machines'
    clocks agree. Unknown until then: the step the relay held as the watch began, its last group, is how long ago the
    robot made it, not how late anything came, and is in neither."""

    def __init__(self) -> None:
        self.offset_us: Optional[int] = None
        self.error_us = None


class Watch(Views):
    """One console watching one robot through a MoQ relay (module docstring): sequence_ai.teleop(url, token=...,
    via="moq"). stream(), states() and metrics() as a WebRTC console's (teleop.Teleop); it takes nothing and sends
    nothing - one person drives, over WebRTC. Use it as a context manager, or close() it."""

    def __init__(self, gateway: Any, *, timeout_s: float) -> None:
        require()
        said = gateway.get(MOQ)
        self.robot: Optional[str] = said.get("robot")
        self.path = "moq"
        self._frames: queue.Queue = queue.Queue()
        self._states: queue.Queue = queue.Queue()
        self.stats = _stats.LatencyStats(**_stats.CONSOLE)
        self._clock = _SameClock()
        self._steps: "collections.OrderedDict[int, tuple]" = collections.OrderedDict()
        self._newest: Optional[tuple] = None
        self._newest_us: Optional[int] = None
        self._joined_us: Optional[int] = None
        self._client: Any = None
        self._closed: Optional[str] = None
        self._failed: list = []
        self._stop: Optional[asyncio.Event] = None
        self._loop = _Loop("seq-teleop-moq-watch")
        ready = threading.Event()
        self._done = self._loop.submit(self._watch(said, ready, time.monotonic() + timeout_s))
        if not ready.wait(timeout_s + _CLOSE_S) or self._failed:
            failed = self._failed[0] if self._failed else Unavailable(
                f"the MoQ relay at {shown(str(said.get('url')))} did not answer within {timeout_s} s")
            self.close()
            raise failed

    async def _watch(self, said: dict, ready: threading.Event, end: float) -> None:
        """Its broadcast found - again each time it ends, the robot connecting anew - and followed until it closes."""
        moq = require()
        self._stop = asyncio.Event()
        try:
            async with _client(moq, said) as client:
                self._client = client
                name = str(said["broadcast"])
                while not self._stop.is_set():
                    found = await self._found(moq, client, name, end if not ready.is_set() else None)
                    if found is None:
                        return
                    ready.set()
                    await self._follow(moq, client, name, *found)
        except Exception as exc:
            if not ready.is_set():
                self._failed.append(exc if isinstance(exc, (Unavailable, InvalidRequest)) else Unavailable(
                    f"the MoQ relay at {shown(str(said.get('url')))} could not be watched: {exc}"))
        finally:
            ready.set()
            self._ended("its watch of the robot ended")

    async def _found(self, moq: Any, client: Any, name: str, end: Optional[float]) -> Optional[tuple]:
        """The robot's broadcast and its first catalog, once the relay serves it - Unavailable past `end`."""
        last: Any = None
        while not self._stop.is_set():


            left = 1.0 if end is None else min(1.0, max(0.1, end - time.monotonic()))
            try:
                broadcast = await asyncio.wait_for(client.request_broadcast(name), left)
                catalogs = await asyncio.wait_for(broadcast.subscribe_catalog(), left)
                return broadcast, catalogs
            except (moq.Error, asyncio.TimeoutError) as exc:
                last = exc
            if end is not None and time.monotonic() > end:
                raise Unavailable(f"the robot is not publishing at the MoQ relay ({last})",
                                  hint="connect the robot to the teleop server first: sequence_ai.connect(\"http://"
                                       "ADDRESS:8200\", token=...)")
            try:
                await asyncio.wait_for(self._stop.wait(), 0.2)
            except asyncio.TimeoutError:
                pass
        return None

    async def _follow(self, moq: Any, client: Any, name: str, broadcast: Any, catalogs: Any) -> None:
        """Its steps and every camera its catalog names, until the broadcast ends or it closes."""
        jobs = [asyncio.ensure_future(self._read_states(await broadcast.subscribe_track(STATE)))]
        cameras: dict = {}
        stop = asyncio.ensure_future(self._stop.wait())

        async def follow_catalog() -> None:
            async for catalog in catalogs:
                for key in _cameras_of(catalog):
                    if key not in cameras:
                        cameras[key] = asyncio.ensure_future(self._camera(moq, client, f"{name}/{key}", key))

        following = asyncio.ensure_future(follow_catalog())
        try:
            await asyncio.wait({following, stop}, return_when=asyncio.FIRST_COMPLETED)
            if following.done() and not following.cancelled() and following.exception() is not None:
                log.info("the robot's broadcast at the MoQ relay ended: %s - waiting for it again", following.exception())
        finally:
            for job in [following, stop, *jobs, *cameras.values()]:
                job.cancel()

    async def _read_states(self, track: Any) -> None:
        while True:
            frame = await track.read_frame()
            if frame is None:
                return
            self._said_state(frame.payload)

    def _said_state(self, payload: bytes) -> None:
        """One step's arrays, as the robot's Driven packed them (teleop_robot.Driven.observed)."""
        try:
            message = _msgpack.unpack(payload)
        except Exception:
            return
        if not isinstance(message, dict) or not isinstance(message.get("n"), int):
            return
        episode, n, made = message.get("e"), message["n"], _clock._micros(message.get("t_us"))
        if made is not None:
            self._steps[made] = (episode, n)
            while len(self._steps) > _STEPS_KEPT:
                self._steps.popitem(last=False)
        self._newest = (episode, n)
        if made is not None:
            self._newest_us = made if self._newest_us is None else max(self._newest_us, made)
            if self._joined_us is None:
                self._joined_us = made
            elif made != self._joined_us and self._clock.offset_us is None:
                self._clock.offset_us = 0
        self._state(episode, n, made, message.get("v"), _clock.now_us())
        self._put(self._frames, {"episode": episode, "steps": [[n, message.get("v")]], "t_us": {n: made}})

    async def _camera(self, moq: Any, client: Any, path: str, key: str) -> None:
        """Camera `key`'s broadcast, once the relay serves it, and its video decoded once its catalog says its codec."""
        try:
            found = await self._found(moq, client, path, time.monotonic() + _CAMERA_S)
            if found is None:
                return
            broadcast, catalogs = found
            async for catalog in catalogs:
                for rendition, video in catalog.video.items():
                    await self._decode(moq, broadcast, key, rendition, video)
                    return
        except asyncio.CancelledError:
            raise
        except Exception as exc:
            log.warning("camera %r through the MoQ relay could not be watched: %s", key, exc)

    async def _decode(self, moq: Any, broadcast: Any, key: str, rendition: str, video: Any) -> None:
        """Camera `key`'s frames, each as an RGB array at the step whose capture time it carries."""
        import numpy as np

        output = moq.VideoDecoderOutput(format=moq.VideoPixelFormat.RGBA)
        try:
            async for frame in await broadcast.decode_video(rendition, video, output):
                made = int(frame.timestamp_us)
                if made == self._joined_us and self._clock.offset_us is not None:

                    self.stats.count("frames_expired")
                    continue
                at = self._steps.get(made)
                if at is None and self._newest_us is not None and made < self._newest_us:


                    self.stats.count("frames_expired")
                    continue
                at = at or self._newest
                if at is None:
                    self.stats.count("frames_dropped")
                    continue
                rgb = np.frombuffer(frame.data, np.uint8).reshape(frame.height, frame.width, 4)[:, :, :3].copy()
                self._put(self._frames, {"episode": at[0], "steps": [[at[1], {key: rgb}]], "t_us": {at[1]: made}})
        except asyncio.CancelledError:
            raise
        except Exception as exc:
            log.warning("camera %r through the MoQ relay could not be decoded: %s", key, exc)

    def metrics(self) -> dict:
        """How this watch does, as Teleop.metrics() says a WebRTC console's: {"path": "moq", "latency_us": {frame_us,
        state_us, ...}, "counters", "gauges"} and "bytes_received" from the relay. frame_us and state_us are the robot's
        capture time to here, by the two machines' clocks (_SameClock)."""
        received = None
        client = self._client
        try:
            received = client.session.stats().bytes_received if client is not None and client.session else None
        except Exception:
            pass
        return {"path": self.path, "bytes_received": received, **self.stats.snapshot()}

    def _ended(self, why: str) -> None:
        if self._closed is not None:
            return
        self._closed = why
        self._frames.put(None)
        self._states.put(None)

    def close(self) -> None:
        """End this watch: nothing of the robot changes."""
        self._ended("this console closed its watch")
        if self._stop is not None:
            self._loop.call(self._stop.set)
        try:
            self._done.result(_CLOSE_S)
        except Exception:
            pass
        self._loop.stop()

    def __enter__(self) -> "Watch":
        return self

    def __exit__(self, *exc: Any) -> None:
        self.close()
