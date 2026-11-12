"""
A console and its robot connected straight to each other (WebRTC, by aiortc), the worker that serves the robot pairing
them and still saying who drives it.


In one sentence: the console offers a connection on its connection to the robot's worker (GET /teleop) - its
candidates, host and server-reflexive alone, and its certificate's fingerprint, in the offer's SDP → the worker hands
it to the robot on the robot's stream, and the robot's answer back the same way → each side's DTLS handshake checks the
other's certificate against the fingerprint the worker handed over → a person's commands go console to robot on a
channel unordered and never sent again, each numbered and timed, the robot playing the newest alone; the robot's cameras
come back as video tracks, each frame named on the control channel, and the rest of each step on two channels - its arrays
on one, the step with its Depth and Tactile items on the other, in pieces → a pair that finds no way to each other fails
saying why, and nothing goes through the worker in its place.

WHY the worker pairs them: the console and the robot already hold connections to it that each checked the other end of
(the worker's pinned certificate, the robot's key) - so the fingerprints it hands over are the ones the two ends sent,
and no new address faces the internet.

WHY host and server-reflexive candidates alone: a relay (TURN) would carry every frame through a third machine - the
hop this saves - and a pair that cannot meet must say so, not go another way.

WHY the cameras on video tracks: on the same association as the commands, a frame of a camera held every message queued behind
it, and with no buffer of its own the network's jitter was its delay. Across a real network a track's p95 was half the
data channel's and the commands' round trip shorter.
 It costs an encode of its own on the robot, which keeps
one too for its worker when it has a policy.
WHY in pieces of PIECE_BYTES, paced: a channel's message is lost whole when any of its packets is, and a camera frame
handed whole to the connection holds every message queued behind it; in pieces, handed on only while the connection
has little unsent (LOW_BYTES), a step's arrays wait behind one piece at most.

WHY the STUN servers are named under our own domain: users are not shown which provider serves anything.


Needs aiortc (`pip install 'sequence-ai[teleop]'`, Python 3.10 or later); imported where a direct connection is first
made, so a robot or console that makes none needs none of it.
"""
from __future__ import annotations

import asyncio
import importlib.util
import itertools
import logging
import os
import socket
import struct
import sys
import threading
import time
import weakref
from collections import deque
from functools import partial
from typing import Any, Callable, Optional

from ..errors import MissingPackage
from . import msgpack_io as _msgpack



STUN = ("stun.generalsequences.com", 3478)
STUN_SECOND = ("stun2.generalsequences.com", 3478)

GATHER_GRACE_S = 0.25




CHANNELS = {
    "seq-cmd": {"ordered": False, "maxRetransmits": 0},
    "seq-ctl": {"ordered": False, "maxRetransmits": 0},
    "seq-state": {"ordered": False, "maxRetransmits": 0},
    "seq-video": {"ordered": False, "maxPacketLifeTime": 150},
    "seq-who": {},
}

_HEAD = struct.Struct("!IHH")
PIECE_BYTES = 16 * 1024


HIGH_BYTES = 64 * 1024
LOW_BYTES = 32 * 1024



_QUEUED = {"seq-state": 1, "seq-video": 3, "seq-cmd": 1, "seq-ctl": 64, "seq-who": 1 << 16}

_PARTIALS = 32
PARTIAL_S = 2.0

OPEN_S = 15.0


MOST_TRACKS = 8








MOST_PEERS = 4



_GONE_S = 30
_INSTALL = "pip install 'sequence-ai[teleop]'"
_NEEDS = "a direct connection between a console and its robot needs Python 3.10 or later and aiortc"
_MAGIC = 0x2112A442
_ENCODER_IN = False
_GATHER_IN = False
_RECEIVING_IN = False
_log = logging.getLogger("sequence_ai.teleop")


def available() -> bool:
    """Whether this install can make a direct connection: Python 3.10+ and aiortc present (not imported here)."""
    return sys.version_info >= (3, 10) and importlib.util.find_spec("aiortc") is not None


def _install_encoder() -> None:
    """teleop_video's encoder in aiortc's place, once a process."""
    global _ENCODER_IN
    if not _ENCODER_IN:
        from . import teleop_video as _video

        _video.install_encoder()
        _ENCODER_IN = True


def _install_gather() -> None:
    """Once a process: an interface's STUN question given up GATHER_GRACE_S after another interface has its answer. aioice
    waits 5 s for every interface, and one with no way to the internet (a VPN's, a tailnet's) never hears: 5 s on each
    side of every connection. Answers that do come arrive together, so they are all kept; with none, the 5 s stand. Left
    as it is by an aioice with no such function: that wait is all this shortens. {dev 11-11: "GATHER 5.00S", two interfaces,
    the tailnet's unanswered; a console took 11.12 s to connect}"""
    global _GATHER_IN
    if _GATHER_IN:
        return
    _GATHER_IN = True
    from aioice import ice

    ask = getattr(ice, "server_reflexive_candidate", None)
    if ask is None:
        return
    answered: "weakref.WeakKeyDictionary[Any, asyncio.Event]" = weakref.WeakKeyDictionary()

    async def asked_with_the_others(protocol: Any, stun_server: Any) -> Any:
        one_came = answered.setdefault(protocol.receiver, asyncio.Event())
        own, other = asyncio.ensure_future(ask(protocol, stun_server)), asyncio.ensure_future(one_came.wait())
        try:
            await asyncio.wait({own, other}, return_when=asyncio.FIRST_COMPLETED)
            if not own.done():
                await asyncio.wait({own}, timeout=GATHER_GRACE_S)
            if not own.done():
                raise asyncio.TimeoutError
            candidate = own.result()
            one_came.set()
            return candidate
        finally:
            own.cancel()
            other.cancel()

    ice.server_reflexive_candidate = asked_with_the_others


def install_receiving() -> None:
    """teleop_video's patches of aiortc's video receiver, once a process."""
    global _RECEIVING_IN
    if not _RECEIVING_IN:
        from . import teleop_video as _video

        _video.install_jitterbuffer_marker_release()
        _video.install_nack_retransmit()
        _video.install_wire_timestamps()
        _RECEIVING_IN = True


def require() -> None:
    """MissingPackage, saying how to install it, where this install cannot make a direct connection."""
    if not available():
        raise MissingPackage(_NEEDS, hint=_INSTALL)




_LOOP_LOCK = threading.Lock()
_LOOP: Optional[asyncio.AbstractEventLoop] = None


def loop() -> asyncio.AbstractEventLoop:
    """The one event loop of this process's direct connections, on a thread of its own (aiortc is asyncio's; the SDK's
    callers are threads)."""
    global _LOOP
    with _LOOP_LOCK:
        if _LOOP is None or _LOOP.is_closed():
            made = asyncio.new_event_loop()
            ready = threading.Event()

            def run() -> None:
                asyncio.set_event_loop(made)
                made.call_soon(ready.set)
                made.run_forever()

            threading.Thread(target=run, daemon=True, name="seq-teleop-direct").start()
            ready.wait(5.0)
            _LOOP = made
        return _LOOP


def run(coro: Any, timeout_s: float) -> Any:
    """`coro` run on the direct connections' loop, waited for `timeout_s` at most (TimeoutError past it)."""
    return asyncio.run_coroutine_threadsafe(coro, loop()).result(timeout_s)


def soon(fn: Callable, *args: Any) -> None:
    """fn(*args) on the direct connections' loop: at once when called from it, else handed to it."""
    here = loop()
    try:
        running = asyncio.get_running_loop()
    except RuntimeError:
        running = None
    if running is here:
        fn(*args)
    else:
        here.call_soon_threadsafe(fn, *args)




def pieces(number: int, data: bytes) -> list:
    """`data` as the pieces message `number` goes in: each its head (_HEAD) and PIECE_BYTES at most of it."""
    count = max(1, -(-len(data) // PIECE_BYTES))
    if count > 0xFFFF:
        raise ValueError(f"a message of {len(data)} bytes is past what one goes in ({0xFFFF * PIECE_BYTES} bytes)")
    return [_HEAD.pack(number & 0xFFFFFFFF, i, count) + data[i * PIECE_BYTES:(i + 1) * PIECE_BYTES]
            for i in range(count)]


class Assembly:
    """One channel's pieces put back together as they come, in any order: a message whole once its every piece is here
    (add); one whose pieces stopped coming is dropped (PARTIAL_S, _PARTIALS)."""

    def __init__(self) -> None:
        self._partial: dict = {}
        self.dropped = 0

    def add(self, piece: bytes, now: Optional[float] = None) -> Optional[bytes]:
        """One piece: the message it completes, else None. A piece that does not read is dropped."""
        now = time.monotonic() if now is None else now
        if len(piece) < _HEAD.size:
            return None
        number, index, count = _HEAD.unpack_from(piece)
        if not count or index >= count:
            return None
        body = piece[_HEAD.size:]
        if count == 1:
            return bytes(body)
        got = self._partial.get(number)
        if got is None or got[0] != count:
            got = self._partial[number] = [count, {}, now]
        got[1][index] = body
        if len(got[1]) == count:
            del self._partial[number]
            return b"".join(got[1][i] for i in range(count))
        self._prune(now)
        return None

    def _prune(self, now: float) -> None:
        """Messages whose pieces stopped coming: the oldest past _PARTIALS, any past PARTIAL_S."""
        for number in [n for n, (_, _, at) in self._partial.items() if now - at > PARTIAL_S]:
            del self._partial[number]
            self.dropped += 1
        while len(self._partial) > _PARTIALS:
            del self._partial[min(self._partial, key=lambda n: self._partial[n][2])]
            self.dropped += 1




_MARK = "__seq__"


def marked(value: Any) -> bool:
    """Whether `value` holds a Video, Depth or Tactile item as its encoder wrote it, at any depth."""
    if isinstance(value, dict):
        return _MARK in value or any(marked(v) for v in value.values())
    if isinstance(value, (list, tuple)):
        return any(marked(v) for v in value)
    return False


def split_step(value: Any) -> tuple:
    """A step as the robot sends it straight to its consoles: (its arrays - every item that is no Video, Depth or Tactile
    one, None when there are none - and whether it has such items, which then go whole on the video channel)."""
    if isinstance(value, dict):
        state = {k: v for k, v in value.items() if not marked(v)}
        return state, len(state) < len(value)
    return (None, True) if marked(value) else (value, False)


def without_video(value: Any) -> Any:
    """A step with its Video items taken out, for a console that gets them as video tracks: the rest of it - its depth and
    tactile items - goes on the video channel as ever."""
    if not isinstance(value, dict):
        return value
    return {k: v for k, v in value.items() if not (isinstance(v, dict) and v.get("__seq__") == "video")}


def without_cameras(inputs: Any) -> Any:
    """A step as observe() was handed it, less its Video items: a robot with no worker to keep them for and no Record encodes
    them for its video tracks alone. {change table V5}"""
    from ..markers import Video

    if not isinstance(inputs, dict):
        return inputs
    return {k: v for k, v in inputs.items() if not isinstance(v, Video)}


def videos(inputs: Any) -> dict:
    """The camera frames of a step as observe() was handed them: each Video item's array, a copy of its own (it is read
    later, on the connection's thread, and a robot may fill the same buffer for its next frame)."""
    from ..markers import Video

    if not isinstance(inputs, dict):
        return {}
    return {str(k): v.value.copy() for k, v in inputs.items() if isinstance(v, Video)}


def video_lines(sdp: str) -> int:
    """How many video tracks an offer asks the robot for: its m=video lines, a console that plays them natively."""
    return sum(1 for line in sdp.splitlines() if line.startswith("m=video "))




class _Probe(asyncio.DatagramProtocol):
    """One UDP socket's STUN answers, by transaction id."""

    def __init__(self) -> None:
        self.transport: Any = None
        self.waiting: dict = {}

    def connection_made(self, transport: Any) -> None:
        self.transport = transport

    def datagram_received(self, data: bytes, addr: Any) -> None:
        fut = self.waiting.pop(bytes(data[8:20]), None)
        if fut is not None and not fut.done():
            fut.set_result(bytes(data))


def _mapped(data: bytes) -> Optional[tuple]:
    """The address a STUN answer says the request came from (XOR-MAPPED-ADDRESS, IPv4), else None."""
    pos = 20
    while pos + 4 <= len(data):
        kind, size = struct.unpack_from("!HH", data, pos)
        value = data[pos + 4:pos + 4 + size]
        if kind == 0x0020 and len(value) >= 8 and value[1] == 0x01:
            port = struct.unpack_from("!H", value, 2)[0] ^ (_MAGIC >> 16)
            ip = socket.inet_ntoa(bytes(b ^ m for b, m in zip(value[4:8], struct.pack("!I", _MAGIC))))
            return ip, port
        pos += 4 + size + (-size % 4)
    return None


async def nat_probe(servers: tuple = (STUN, STUN_SECOND), timeout_s: float = 1.5) -> dict:
    """What NAT this machine is behind, from one UDP socket's STUN binding to each of `servers` - two at different
    addresses: {"kind": "independent" (one public port whatever the peer: a pair can meet through it) | "dependent" (a
    port of its own for each peer - symmetric) | "one" (one server answered) | "no_udp" (none did) | "unknown", "public":
    the public address it was seen at}. Each binding is asked twice, half a second apart."""
    here = asyncio.get_running_loop()
    try:
        transport, probe = await here.create_datagram_endpoint(_Probe, local_addr=("0.0.0.0", 0))
    except OSError:
        return {"kind": "unknown", "public": None}

    unnamed = []

    async def one(host: str, port: int) -> Optional[tuple]:
        try:
            ip = (await here.getaddrinfo(host, port, family=socket.AF_INET, type=socket.SOCK_DGRAM))[0][4][0]
        except (OSError, IndexError):
            unnamed.append(host)
            return None
        tid = os.urandom(12)
        fut = here.create_future()
        probe.waiting[tid] = fut
        ask = struct.pack("!HHI", 0x0001, 0, _MAGIC) + tid
        for attempt in range(2):
            transport.sendto(ask, (ip, port))
            try:
                return _mapped(await asyncio.wait_for(asyncio.shield(fut), timeout_s / 2 if attempt == 0 else timeout_s))
            except asyncio.TimeoutError:
                continue
        probe.waiting.pop(tid, None)
        return None

    try:
        got = await asyncio.gather(*(one(h, p) for h, p in servers))
    finally:
        transport.close()
    seen = [g for g in got if g]
    if not seen and unnamed:
        return {"kind": "unknown", "public": None}
    kind = ("no_udp" if not seen else "one" if len(seen) < len(got) else
            "independent" if len(set(seen)) == 1 else "dependent")
    return {"kind": kind, "public": seen[0][0] if seen else None}




def only_host_srflx(sdp: str) -> str:
    """`sdp` with every candidate but host and server-reflexive ones taken out - a relay's above all.
"""
    kept = []
    for line in sdp.splitlines():
        if line.startswith("a=candidate:") and _candidate_type(line) not in ("host", "srflx"):
            continue
        kept.append(line)
    return "\r\n".join(kept) + "\r\n"


def _candidate_type(line: str) -> Optional[str]:
    parts = line.split()
    return parts[parts.index("typ") + 1] if "typ" in parts and parts.index("typ") + 1 < len(parts) else None


def candidate_types(sdp: Optional[str]) -> list:
    """The kinds of candidate `sdp` offers (host, srflx), each once."""
    return sorted({t for t in (_candidate_type(l) for l in (sdp or "").splitlines() if l.startswith("a=candidate:"))
                   if t})


def fingerprint(sdp: Optional[str]) -> Optional[str]:
    """The certificate fingerprint `sdp` names ("sha-256 AB:CD:..."), else None."""
    for line in (sdp or "").splitlines():
        if line.startswith("a=fingerprint:"):
            return line[len("a=fingerprint:"):].strip()
    return None




class _Channel:
    """One data channel's sending side, paced (module docstring): messages queued whole, handed on a piece at a time
    while the connection holds little unsent; the oldest not yet begun dropped past _QUEUED."""

    def __init__(self, channel: Any) -> None:
        self.channel = channel
        self.most = _QUEUED.get(channel.label, 8)
        self.queue: deque = deque()
        self.numbers = itertools.count()
        self.dropped = 0
        channel.bufferedAmountLowThreshold = LOW_BYTES
        channel.on("bufferedamountlow", self.pump)

    def put(self, data: bytes) -> None:
        """One message, queued and pumped (on the loop)."""
        self.queue.append([pieces(next(self.numbers), data), 0])
        begun = 1 if self.queue[0][1] > 0 else 0
        while len(self.queue) - begun > self.most:
            del self.queue[begun]
            self.dropped += 1
        self.pump()

    def pump(self) -> None:
        if self.channel.readyState != "open":
            return
        while self.queue and self.channel.bufferedAmount < HIGH_BYTES:
            head = self.queue[0]
            self.channel.send(head[0][head[1]])
            head[1] += 1
            if head[1] == len(head[0]):
                self.queue.popleft()


class _Side:
    """One end of a direct connection: its RTCPeerConnection, its channels' sending sides and their pieces put back
    together - each whole message handed to `on_message(label, data, at_us)`, `at_us` when its last piece came - and
    its state, told to `on_state(state)`."""

    def __init__(self, on_message: Callable, on_state: Optional[Callable] = None) -> None:
        from aiortc import RTCConfiguration, RTCIceServer, RTCPeerConnection

        _install_gather()

        self.pc = RTCPeerConnection(RTCConfiguration(iceServers=[RTCIceServer(urls=f"stun:{STUN[0]}:{STUN[1]}")]))
        self.on_message, self.on_state = on_message, on_state
        self.on_open: Optional[Callable] = None
        self.tracks: list = []
        self.track_of: dict = {}
        self.left_out: set = set()
        self.episode: Optional[str] = None
        self.out: dict = {}
        self.assembly: dict = {label: Assembly() for label in CHANNELS}
        self.opened = asyncio.Event()
        self.ended = asyncio.Event()
        self.state = "new"
        self.local_sdp: Optional[str] = None
        self.remote_sdp: Optional[str] = None
        self.pc.on("connectionstatechange", self._changed)

    def _changed(self) -> None:
        self.state = self.pc.connectionState
        if self.state in ("failed", "closed"):
            self.ended.set()
        if self.on_state is not None:
            self.on_state(self.state)

    def wire(self, channel: Any) -> None:
        """One of CHANNELS, opened by the console or as the robot heard of it: its sending side and its pieces in."""
        if channel.label not in CHANNELS:
            return
        self.out[channel.label] = _Channel(channel)
        assembly = self.assembly[channel.label]

        def message(data: Any) -> None:
            if isinstance(data, str):
                return
            whole = assembly.add(bytes(data))
            if whole is not None:

                self.on_message(channel.label, whole, time.time_ns() // 1000)

        channel.on("message", message)
        channel.on("open", self._opened)
        if channel.readyState == "open":
            self._opened()

    def _opened(self) -> None:
        if len(self.out) == len(CHANNELS) and all(c.channel.readyState == "open" for c in self.out.values()):
            for c in self.out.values():
                c.pump()
            if not self.opened.is_set():
                self.opened.set()
                if self.on_open is not None:
                    self.on_open()

    def add_tracks(self, count: int, hz: float) -> None:
        """The video tracks this console's offer asked for, H.264 (teleop_video's encoder) - on the loop, between its
        offer and its answer."""
        from . import teleop_video as _video

        _install_encoder()
        for i in range(count):
            track = _video.FrameTrack(f"video-{i}", hz=hz, send_meta=partial(self._told_frame, i))
            self.tracks.append(track)
            self.pc.addTrack(track)
        for transceiver in self.pc.getTransceivers():
            if transceiver.kind == "video":
                h264 = {c.payloadType for c in transceiver._codecs if c.name == "H264"}
                kept = [c for c in transceiver._codecs
                        if c.payloadType in h264 or (c.name == "rtx" and c.parameters.get("apt") in h264)]
                transceiver._codecs = kept or transceiver._codecs

    def _told_frame(self, i: int, meta: dict) -> None:
        """What a video track's frame is, on the control channel: RTP's own timestamp starts anywhere. {teleop_video
        FrameTrack}"""
        self.send("seq-ctl", _msgpack.pack({"t": "vm", "i": i, "key": self.tracks[i].key, "e": self.episode, **meta}))

    def frames(self, episode: str, raw: dict, n: int, t_us: int) -> None:
        """A step's camera frames to the video tracks (on the loop): each camera a track, in the order they first came;
        those past the tracks it asked for go to no one, and the robot's owner is told which.
"""
        self.episode = episode
        new_left = []
        for key, frame in raw.items():
            track = self.track_of.get(key)
            if track is None:
                if len(self.track_of) >= len(self.tracks):
                    if key not in self.left_out:
                        new_left.append(key)
                    continue
                track = self.track_of[key] = self.tracks[len(self.track_of)]
                track.key = key
            track.put(frame, n=n, capture_us=t_us)
        if new_left:
            self.left_out.update(new_left)
            _log.warning("a console takes %d cameras of this robot's: %s not sent to it", len(self.tracks),
                         ", ".join(sorted(self.left_out)))

    def send(self, label: str, data: bytes) -> bool:
        """One message on `label` (on the loop): False while that channel is not open."""
        channel = self.out.get(label)
        if channel is None or channel.channel.readyState != "open":
            return False
        channel.put(data)
        return True

    async def close(self) -> None:
        try:
            await self.pc.close()
        except Exception:
            pass

    def facts(self) -> dict:
        """What a failure is explained by: each side's candidate kinds and how far the connection got."""
        dtls = getattr(getattr(self.pc, "sctp", None), "transport", None)
        return {"connection": self.pc.connectionState, "ice": self.pc.iceConnectionState,
                "dtls": getattr(dtls, "state", None), "mine": candidate_types(self.local_sdp),
                "theirs": candidate_types(self.remote_sdp)}




class ConsoleLink:
    """A console's direct connection to its robot (module docstring): offer() its SDP and NAT, accept() the robot's
    answer, wait_open(); command() and control() send; what the robot sends is handed to `on_message(label, data, at)`
    on the loop's thread, and the connection's end to `on_state(state)`. Every call but the callbacks from the console's
    own threads."""

    def __init__(self, on_message: Callable, on_state: Callable) -> None:
        require()
        self._side: Optional[_Side] = None
        self._on_message, self._on_state = on_message, on_state
        self.nat: dict = {}

    def offer(self, timeout_s: float, *, tracks: int = 0, on_track: Optional[Callable] = None) -> dict:
        """The console's offer: {"sdp": its candidates host and server-reflexive alone, "nat": its nat_probe()}. `tracks`:
        the robot's cameras it takes as video tracks, each handed to `on_track` on the loop."""
        async def make() -> dict:
            self._side = side = _Side(self._on_message, self._on_state)
            for label, options in CHANNELS.items():
                side.wire(side.pc.createDataChannel(label, **options))
            for _ in range(tracks):
                side.pc.addTransceiver("video", direction="recvonly")
            if on_track is not None:
                side.pc.on("track", on_track)
            probing = asyncio.ensure_future(nat_probe())
            await side.pc.setLocalDescription(await side.pc.createOffer())
            side.local_sdp = only_host_srflx(side.pc.localDescription.sdp)
            self.nat = await probing
            return {"sdp": side.local_sdp, "nat": self.nat}

        return run(make(), timeout_s)

    def accept(self, sdp: str, timeout_s: float) -> None:
        """The robot's answer, as its worker handed it on."""
        from aiortc import RTCSessionDescription

        async def take() -> None:
            self._side.remote_sdp = only_host_srflx(sdp)
            await self._side.pc.setRemoteDescription(RTCSessionDescription(sdp=self._side.remote_sdp, type="answer"))

        run(take(), timeout_s)

    def wait_open(self, timeout_s: float) -> bool:
        """Whether the connection and its every channel opened within `timeout_s`."""
        async def wait() -> bool:
            side = self._side

            done, pending = await asyncio.wait([asyncio.ensure_future(side.opened.wait()),
                                                asyncio.ensure_future(side.ended.wait())], timeout=timeout_s,
                                               return_when=asyncio.FIRST_COMPLETED)
            for task in pending:
                task.cancel()
            return side.opened.is_set()

        return bool(self._side is not None and run(wait(), timeout_s + 1.0))

    def facts(self) -> dict:
        return run(_facts_of(self._side), 2.0) if self._side is not None else {}

    @property
    def open(self) -> bool:
        side = self._side
        return bool(side is not None and side.opened.is_set() and side.state not in ("failed", "closed"))

    def command(self, data: bytes) -> None:
        """A person's command, packed (on the loop, at once)."""
        soon(self._send, "seq-cmd", data)

    def control(self, message: dict) -> None:
        """A tick or a keyframe ask (on the loop, at once)."""
        soon(self._send, "seq-ctl", _msgpack.pack(message))

    def who(self, message: dict) -> None:
        """A take, a release, a stop or a heartbeat, on the reliable channel (on the loop, at once)."""
        soon(self._send, "seq-who", _msgpack.pack(message))

    def _send(self, label: str, data: bytes) -> None:
        if self._side is not None:
            self._side.send(label, data)

    def close(self) -> None:
        side, self._side = self._side, None
        if side is not None:
            try:
                run(side.close(), 5.0)
            except Exception:
                pass


async def _facts_of(side: _Side) -> dict:
    return side.facts()




class RobotLinks:
    """A robot's direct connections, one per console that asked (module docstring): answer() each offer its worker
    handed on - its answer said back through the worker (`say(peer, message)`) - step() each step it observed to every
    console connected, reply() a receipt or a tock to one; what a console sends goes to `on_message(peer, label, data,
    at)` on the loop's thread."""

    def __init__(self, on_message: Callable, say: Callable, on_peer: Optional[Callable] = None) -> None:
        self._on_message, self._say = on_message, say
        self._on_peer = on_peer
        self._sides: dict = {}
        self._lock = threading.Lock()

    @property
    def peers(self) -> int:
        """Consoles connected straight to this robot now."""
        with self._lock:
            return sum(1 for s in self._sides.values() if s.opened.is_set() and s.state not in ("failed", "closed"))

    @property
    def tracks(self) -> int:
        """Consoles connected straight to this robot that take its cameras as video tracks."""
        with self._lock:
            return sum(1 for s in self._sides.values() if s.tracks and s.opened.is_set())

    def answer(self, peer: str, sdp: str, hz: float = 30.0) -> None:
        """A console's offer (`peer`, as the platform names it): answered on the loop - {"t": "rtc", "sdp", "nat"} said
        back to it, or {"t": "rtc", "error"} - never waited for here. `hz`: its video tracks' rate."""
        if not isinstance(peer, str) or not isinstance(sdp, str):
            return
        loop().call_soon_threadsafe(lambda: asyncio.ensure_future(self._answer(peer, sdp, hz)))

    async def _answer(self, peer: str, sdp: str, hz: float) -> None:
        from aiortc import RTCSessionDescription

        try:
            with self._lock:
                old = self._sides.pop(peer, None)
                if len(self._sides) >= MOST_PEERS:
                    raise RuntimeError(f"the robot has {MOST_PEERS} console{'' if MOST_PEERS == 1 else 's'} connected "
                                       f"straight to it already; one that went without closing gives its place up in "
                                       f"about {_GONE_S} s")
            if old is not None:
                await old.close()

            def on_state(state: str) -> None:
                if state in ("failed", "closed"):
                    with self._lock:
                        gone = self._sides.get(peer) is side
                        if gone:
                            del self._sides[peer]
                    if gone and self._on_peer is not None:
                        self._on_peer(peer, "gone")

            side = _Side(lambda label, data, at: self._on_message(peer, label, data, at), on_state)
            if self._on_peer is not None:
                side.on_open = lambda: self._on_peer(peer, "open")
            side.pc.on("datachannel", side.wire)
            with self._lock:
                self._sides[peer] = side
            side.remote_sdp = only_host_srflx(sdp)
            await side.pc.setRemoteDescription(RTCSessionDescription(sdp=side.remote_sdp, type="offer"))
            if video_lines(side.remote_sdp):
                side.add_tracks(min(video_lines(side.remote_sdp), MOST_TRACKS), hz)
            probing = asyncio.ensure_future(nat_probe())
            await side.pc.setLocalDescription(await side.pc.createAnswer())
            side.local_sdp = only_host_srflx(side.pc.localDescription.sdp)
            self._say(peer, {"t": "rtc", "sdp": side.local_sdp, "nat": await probing})
        except Exception as exc:
            _log.warning("a console's direct connection was not answered: %s", exc)
            self._say(peer, {"t": "rtc", "error": f"{type(exc).__name__}: {exc}"[:300]})

    def step(self, data: dict) -> None:
        """One step to every console connected straight to it (`data`: {"state": its arrays packed, or None; "rest": the
        step with its Depth and Tactile items packed, or None for one with neither}) - from the robot's observe() thread,
        handed to the loop."""
        soon(self._fan, data)

    def _fan(self, data: dict) -> None:
        with self._lock:
            sides = [s for s in self._sides.values() if s.opened.is_set()]
        for side in sides:
            if data.get("state") is not None:
                side.send("seq-state", data["state"])
            if data.get("rest") is not None:
                side.send("seq-video", data["rest"])

    def frames(self, episode: str, raw: dict, n: int, t_us: int) -> None:
        """A step's camera frames, as observe() was handed them, to every console that takes them as video tracks."""
        soon(self._fan_frames, episode, raw, n, t_us)

    def _fan_frames(self, episode: str, raw: dict, n: int, t_us: int) -> None:
        with self._lock:
            sides = [s for s in self._sides.values() if s.tracks and s.opened.is_set()]
        for side in sides:
            side.frames(episode, raw, n, t_us)

    def reply(self, peer: str, message: dict, *, label: str = "seq-ctl") -> bool:
        """A message to the console `peer` - a receipt or a tock on the control channel, who drives on the reliable one
        (`label`): False when it is not connected straight here."""
        with self._lock:
            side = self._sides.get(peer)
        if side is None or not side.opened.is_set():
            return False
        soon(side.send, label, _msgpack.pack(message))
        return True

    def tell_all(self, message: dict) -> None:
        """`message` to every console connected straight here, on the reliable channel."""
        with self._lock:
            peers = [p for p, s in self._sides.items() if s.opened.is_set()]
        for peer in peers:
            self.reply(peer, message, label="seq-who")

    def connected(self) -> list:
        """The consoles connected straight here now."""
        with self._lock:
            return [p for p, s in self._sides.items() if s.opened.is_set() and s.state not in ("failed", "closed")]

    def close(self) -> None:
        with self._lock:
            sides, self._sides = list(self._sides.values()), {}
        for side in sides:
            try:
                run(side.close(), 5.0)
            except Exception:
                pass




def why_not(mine: Optional[dict], theirs: Optional[dict], facts: dict) -> str:
    """What stopped a console's direct connection to its robot, from each side's NAT probe and how far the connection
    got - in words that name no address of anyone's and no provider."""
    mine, theirs = mine or {}, theirs or {}
    if facts.get("ice") in ("completed", "connected") and facts.get("dtls") not in ("connected", None):
        return ("the two reached each other, but the robot's certificate was not the one its worker handed over, so "
                "the connection was refused")
    if facts.get("ice") in ("completed", "connected"):
        return "the two reached each other, but the connection's channels did not open in time"
    kinds = (mine.get("kind"), theirs.get("kind"))
    if "no_udp" in kinds:
        side = "this machine's" if kinds[0] == "no_udp" else "the robot's"
        return (f"{side} network lets no UDP out (no answer to it from the internet), so only a machine on its own "
                "network could reach it, and none did")
    if (mine.get("public") and mine.get("public") == theirs.get("public")
            and "host" in facts.get("mine", ()) and "host" in facts.get("theirs", ())):
        return ("both are behind the same public address, yet no address on that network reached the other: the "
                "network keeps its devices apart (client isolation), or a firewall on one of them drops UDP")
    if kinds == ("dependent", "dependent"):
        return ("both are behind NATs that give every new peer a port of their own (symmetric NAT), so neither can "
                "reach the other")
    if "dependent" in kinds:
        side = "this machine's" if kinds[0] == "dependent" else "the robot's"
        return (f"{side} NAT gives every new peer a port of its own (symmetric NAT), and the other side lets no packet "
                "in that it did not ask for")
    return "a firewall between the two networks lets no UDP through"
