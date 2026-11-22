"""
Teleop's transports: what the teleop core - the robot's Driven (teleop_robot.py) and a console's Teleop (teleop.py) -
calls to send a robot's frames and steps to its consoles and their commands back, one interface each side, an
implementation behind a name: "webrtc" (aiortc, teleop_direct.py), and "gstreamer" (GStreamer's webrtcbin, teleop_gst.py:
a robot's side alone - its consoles are aiortc's or a browser's, the wire the same); Media over QUIC would stand where
they stand, the core and the wire format unchanged.

In one sentence: the core asks robot(name) or console(name) for a transport's maker → makes one with its callbacks →
calls only the methods below: the robot's side answers each console's offer, sends each step and each camera's frames,
replies to one console or tells all of them; a console's side offers, accepts the robot's answer, waits for it to open,
and sends commands (latest only), control (ticks, keyframe asks) and who drives (reliable) → `path` says which way a
connection went.
WHY the methods the core already calls, and no more: an interface drawn from use is one a second implementation can
meet; one drawn from a guess at what a transport might need is the first thing to change.


The pairing is the other interface, met by the platform's gateway and seq teleop serve alike (teleop_link.py,
teleop_serve.py); the encoder the third, in teleop_video.py.
"""
from __future__ import annotations

from typing import Any, Callable, Dict, Optional, Protocol

DEFAULT = "webrtc"


class RobotTransport(Protocol):
    """A robot's connections to the consoles that reach it. Made with `on_message(peer, label, data, at_us)` - what a
    console sent -, `say(peer, message)` - an answer to an offer, said back through its pairing server - and
    `on_peer(peer, "open" | "gone")`."""

    @property
    def peers(self) -> int:
        """Consoles connected now."""

    @property
    def tracks(self) -> int:
        """Consoles connected now that take its cameras as video."""

    def answer(self, peer: str, sdp: str, hz: float = 30.0, ice_servers: Any = None) -> None:
        """A console's offer, answered - never waited for here."""

    def path(self, peer: str) -> str:
        """The way one console's connection went: "direct" or "relay"."""

    def step(self, data: dict) -> None:
        """One step to every console: {"state": its arrays packed, or None; "rest": the rest packed, or None}."""

    def frames(self, episode: str, raw: dict, n: int, t_us: int) -> None:
        """A step's camera frames, as observe() was handed them, to every console that takes them as video."""

    def reply(self, peer: str, message: dict, *, label: str = "seq-ctl") -> bool:
        """A message to one console - a receipt or a tock, or who drives on the reliable channel."""

    def tell_all(self, message: dict) -> None:
        """A message to every console, reliably."""

    def connected(self) -> list:
        """The consoles connected now."""

    def close(self) -> None:
        ...


class ConsoleTransport(Protocol):
    """A console's connection to its robot. Made with `on_message(label, data, at_us)` - what the robot sent - and
    `on_state(state)` - the connection's end."""

    @property
    def open(self) -> bool:
        ...

    def offer(self, timeout_s: float, *, tracks: int = 0, on_track: Optional[Callable] = None,
              ice_servers: Any = None, direct_only: bool = False) -> dict:
        """Its offer: {"sdp", "nat"}, its cameras as `tracks` video tracks handed to `on_track`."""

    def accept(self, sdp: str, timeout_s: float) -> None:
        """The robot's answer."""

    def wait_open(self, timeout_s: float) -> bool:
        """Whether it opened, every channel of it, within `timeout_s`."""

    def facts(self) -> dict:
        """How far a connection that did not open got: what why_not explains."""

    def path(self) -> str:
        """"direct" or "relay"."""

    def command(self, data: bytes) -> None:
        """A person's command, packed: the newest alone counts, none is sent again."""

    def control(self, message: dict) -> None:
        """A tick or a keyframe ask."""

    def who(self, message: dict) -> None:
        """A take, a release, a stop or a heartbeat: reliable, in order."""

    def close(self) -> None:
        ...


_ROBOT: Dict[str, Callable[..., RobotTransport]] = {}
_CONSOLE: Dict[str, Callable[..., ConsoleTransport]] = {}


def register(name: str, *, robot: Optional[Callable[..., RobotTransport]] = None,
             console: Optional[Callable[..., ConsoleTransport]] = None) -> None:
    """A transport's makers, by its name: a robot's side, a console's, or both."""
    if robot is not None:
        _ROBOT[name] = robot
    if console is not None:
        _CONSOLE[name] = console


def _builtin() -> None:
    """aiortc's, made known as first asked for: imported with what it needs, aiortc itself only as a connection opens;
    GStreamer's robot side by name alone, imported as a robot makes one (_gstreamer)."""
    if DEFAULT not in _ROBOT or DEFAULT not in _CONSOLE:
        from sequence_ai._core import teleop_direct

        _ROBOT.setdefault(DEFAULT, teleop_direct.RobotLinks)
        _CONSOLE.setdefault(DEFAULT, teleop_direct.ConsoleLink)
    _ROBOT.setdefault("gstreamer", _gstreamer)


def _gstreamer(*args: Any, **kwargs: Any) -> RobotTransport:
    """GStreamer's robot side (teleop_gst.RobotLinks): its module imported here, so a robot that never names it imports
    none of it; MissingPackage, saying what to install, where GStreamer or its bindings are not here."""
    from sequence_ai._core import teleop_gst

    return teleop_gst.RobotLinks(*args, **kwargs)


def robot(name: Optional[str] = None) -> Callable[..., RobotTransport]:
    """The maker of a robot's side of the transport `name` (DEFAULT unnamed): ValueError naming the known ones."""
    _builtin()
    try:
        return _ROBOT[name or DEFAULT]
    except KeyError:
        raise ValueError(f"no teleop transport {name!r}: {', '.join(sorted(_ROBOT))}") from None


def console(name: Optional[str] = None) -> Callable[..., ConsoleTransport]:
    """The maker of a console's side of the transport `name` (DEFAULT unnamed): ValueError naming the known ones."""
    _builtin()
    try:
        return _CONSOLE[name or DEFAULT]
    except KeyError:
        raise ValueError(f"no teleop transport {name!r}: {', '.join(sorted(_CONSOLE))}") from None
