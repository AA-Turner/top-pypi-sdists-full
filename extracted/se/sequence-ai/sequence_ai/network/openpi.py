# SPDX-FileCopyrightText: Copyright (c) 2026 General Sequences Company
# SPDX-License-Identifier: Apache-2.0
"""
openpi's own client and server, with the network components on them: on the robot, the connection openpi's client
already holds kept warm (keep) and each picture sent as JPEG (image_tools); on the GPU, openpi's own server pinging each
robot and handing its policy each JPEG picture as the array it reads (patch).

On the robot:

    from sequence_ai.network import openpi
    from sequence_ai.network.openpi import image_tools     # in place of openpi_client's: pictures go as JPEG

    policy = openpi.connect(host, port)    # openpi_client's WebsocketClientPolicy, once the server answers
    kept = openpi.keep(policy)             # BBR and TCP keepalive on its socket; a WebSocket ping while it is idle
    observation["observation/image"] = image_tools.convert_to_uint8(image_tools.resize_with_pad(frame, 224, 224))
    action = policy.infer(observation)     # as before: the client, its protocol and its responses are openpi's own
    kept.close()

On the GPU, openpi's scripts/serve_policy.py run unchanged, from openpi's repository and in its environment:

    uv run python -m sequence_ai.network.openpi scripts/serve_policy.py --env=DROID

or, in a server script of your own, one line before it makes openpi's server:

    openpi.patch()

In one sentence: keep() takes the WebSocket connection the client opened → requests BBR on its socket and enables TCP
keepalive (window.keep, window.keepalive_options), each where this machine allows it → pings the connection after each
`every_s` of idle time and waits for the pong (window.Warm), so a dead connection is detected before the next
observation is sent on it → marks each infer() as a use. image_tools fits a frame as openpi's resize_with_pad does and
returns it as base64 JPEG (frames.resize_image, frames.encode) → patch()
makes openpi's server ping each connection every 100 ms (ping.websockets_options) and hands the policy it is given to
Pictures, whose infer() turns each picture back into the array the policy reads (frames.decode).

WHY on openpi's own client and server: nothing of openpi's is replaced. The msgpack layout, the protocol and the policy
are unchanged; only the socket's options, the idle time between two infer() calls and the pictures' encoding change. A
robot that still sends arrays is served as before.
WHY no ping while infer() runs, and no pong timeout on either end: openpi's server runs its policy on its event loop,
which sends and answers no ping while an inference runs, and a first inference compiles the model for tens of seconds.
A late pong then means a long inference, not a dead connection: keep() pings only an idle connection and lifts the
client library's own pong timeout, and patch() has the server wait for each pong as long as it takes. A robot that
connects while another robot's first inference runs waits as long for its handshake, which openpi_client gives up on
at once (TimeoutError): connect() waits for it.
WHY JPEG: a 224 x 224 picture is 150,528 bytes as an array, and its JPEG at frames.DEFAULT_JPEG_QUALITY a small part of
that (the run below has two of them in each request), at a quality that moves a π0.5 policy's actions by about a tenth
of what its own sampling noise does (frames.DEFAULT_JPEG_QUALITY has the measurement).

Verified against openpi-client 0.1.2 on a local connection (tests/network/test_openpi.py), and patch() against a server
module built as openpi's websocket_policy_server.py is (tests/network/test_openpi_server.py). Measured on a WebSocket
connection of the kind openpi's client holds (the websockets library on both ends, a stand-in for the client, two cloud
machines; bench/ws_bench.py, docs/measurements.md): a 100 KB upload 0.53 s after each response took 37.6, 44.4, 82.4 and
163.8 ms at RTTs of 11, 21, 41 and 81 ms, and 12.7, 22.7, 41.8 and 82.6 ms with keep(), 40 uploads per cell. With
openpi's own server and client (π0.5 on an L4, the client in a Linux virtual machine on a home connection, 301 KB per
request, one 45 s episode each): the time a request spent outside inference had a median of 181 and 152 ms without
keep(); with it, 92 ms; with the BBR module loaded as well, 86 and 91 ms. With openpi's own server and client again
(π0.5 on an L4, the robot a simulated arm on a Mac on a home connection, one 45 s episode each), the pictures as JPEG
and the server's pings as patch() and image_tools make them: each request's upload went from 301.5 KB to 18.8 KB, and
the time it spent outside the server from a median of 153.8 to 58.1 ms, over RTTs of 56.5 and 37.5 ms. From a Linux
robot 30 ms from openpi's own server (CUBIC, 301 KB per request, six 45 s episodes each), keep() cut the time outside
inference from 91.2 to 37.1 ms. With openpi's own server on Linux, also load BBR (`sudo modprobe tcp_bbr`, which keep()
then puts on the connection) so the window holds across a pause (window.py).
bench/ measures your link.

keep() reads the client's `_ws`, the connection it keeps, and patch() the server module's `_server` and
WebsocketPolicyServer: a client or a server built otherwise (another version, another transport) raises TypeError
with that reason.

Adapted from Physical-Intelligence/openpi packages/openpi-client/src/openpi_client/image_tools.py (Apache-2.0):
image_tools.convert_to_uint8, for an array (THIRD_PARTY_NOTICES.md).
"""
from __future__ import annotations

import functools
import os
import runpy
import sys
import threading
import time
from dataclasses import dataclass
from typing import Any, Optional

from . import frames, ping, window

PONG_S = 5.0       # how long a pong may take: past it the connection is considered dead and the pings stop
RETRY_S = 1.0      # connect(): between two handshakes the server did not answer


@dataclass
class Kept:
    """What keep() applied to a client's connection: whether its socket accepted BBR, the congestion control it now
    uses, the keepalive options it accepted, and the pings that keep it warm (`warm.pings`: those answered so far)."""

    bbr: bool
    congestion: Optional[str]
    keepalive: list
    warm: window.Warm

    def close(self) -> None:
        """Stop the pings. The connection is the client's, and stays open."""
        self.warm.close()


def connect(host: str = "0.0.0.0", port: Optional[int] = None, *, api_key: Optional[str] = None,
            wait_s: float = 600.0) -> Any:
    """openpi_client's WebsocketClientPolicy(host, port, api_key), made once its server answers the handshake.
    openpi_client waits for a server that is not listening yet; this waits as well for one that listens and has not
    answered yet - loading its policy, or running another robot's first inference on its event loop - which
    openpi_client gives up on at once with TimeoutError. TimeoutError past `wait_s` seconds."""
    from openpi_client import websocket_client_policy

    end = time.monotonic() + wait_s
    while True:
        try:
            return websocket_client_policy.WebsocketClientPolicy(host, port, api_key=api_key)
        except TimeoutError:
            if time.monotonic() >= end:
                raise
            time.sleep(RETRY_S)


def keep(policy: Any, *, every_s: float = 0.1, for_s: float = 60.0) -> Kept:
    """Apply the client-side components to `policy`'s connection (the module's docstring). `every_s`: the idle time
    after which a ping is sent; `for_s`: how long the pings continue after the last infer()."""
    ws = getattr(policy, "_ws", None)
    sock = getattr(ws, "socket", None)
    if ws is None or sock is None or not callable(getattr(ws, "ping", None)):
        raise TypeError("this client keeps no WebSocket connection at `_ws` (openpi_client's WebsocketClientPolicy "
                        "does): nothing to keep warm")
    bbr = window.keep(sock)
    took = []
    for level, name, value in window.keepalive_options():
        try:
            sock.setsockopt(level, name, value)
        except OSError:
            continue
        took.append((level, name, value))

    flying = threading.Event()     # an infer() in flight: the connection is not idle, and its server pongs no ping

    def ping() -> bool:
        if flying.is_set():
            return False
        if ws.ping().wait(PONG_S):
            return True
        if flying.is_set():
            return False           # an infer() began meanwhile: its server answers the ping once it is done
        raise TimeoutError(f"no pong in {PONG_S:g} s")

    warm = window.Warm(ping, every_s=every_s, for_s=for_s)
    ws.ping_timeout = None         # the library's own keepalive waits for each pong as long as an inference takes
    infer = policy.infer

    def infer_and_mark(obs):
        flying.set()
        try:
            return infer(obs)
        finally:
            flying.clear()
            warm.used()

    policy.infer = infer_and_mark
    warm.used()                    # the connection was just used to connect: idle time is counted from now
    return Kept(bbr=bbr, congestion=window.congestion_of(sock), keepalive=took, warm=warm)


# ── on the robot: pictures as JPEG ────────────────────────────────────────────────────────────────────────────────────
class image_tools:  # noqa: N801 - named as the openpi_client module it stands in for
    """
    openpi_client's image_tools for a robot whose pictures go to the server as JPEG: imported in place of openpi's,
    the robot's code is unchanged.

        from sequence_ai.network.openpi import image_tools     # was: from openpi_client import image_tools

        image = image_tools.convert_to_uint8(image_tools.resize_with_pad(frame, 224, 224))

    resize_with_pad fits one frame exactly as openpi's does (frames.resize_image, mode "pad", the same filter) and
    returns it as base64 JPEG text at frames.DEFAULT_JPEG_QUALITY; convert_to_uint8 returns that text as it is, and
    converts an array as openpi's does. The server turns the text back into the array: openpi's own server after
    patch(), or any server with frames.decode.
    """

    @staticmethod
    def resize_with_pad(images: Any, height: int, width: int, method: Any = None) -> str:
        """One frame - an HxWx3 uint8 array or a PIL image - fitted into `height` x `width` as openpi's resize_with_pad
        fits it, as base64 JPEG. `method` is a Pillow resampling filter, bilinear when not given, as openpi's default
        is. A batch of frames is refused: each picture is its own JPEG."""
        if getattr(images, "ndim", 3) != 3:
            raise ValueError(f"one picture at a time, an HxWx3 frame: not one of shape {tuple(images.shape)}")
        name = "bilinear"
        if method is not None:
            from PIL import Image

            name = Image.Resampling(method).name.lower()
        return frames.encode(frames.resize_image(images, width, height, mode="pad", filter=name))

    @staticmethod
    def convert_to_uint8(img: Any) -> Any:
        """A picture resize_with_pad made, unchanged; an array as openpi's convert_to_uint8 returns it: a float array
        scaled from 0-1 to 0-255 and converted to uint8, any other array as it is."""
        if isinstance(img, str):
            return img
        import numpy as np

        if np.issubdtype(img.dtype, np.floating):
            img = (255 * img).astype(np.uint8)
        return img


# ── on the GPU: openpi's own server ───────────────────────────────────────────────────────────────────────────────────
def decode_pictures(observation: Any) -> Any:
    """`observation` with each picture sent as text or bytes turned into the array its policy reads (frames.decode),
    in a new dict. A picture is a value under a key that names an image: "observation/image",
    "observation/wrist_image_left", or any key inside "images" ({"cam_high": ...}). Arrays and every other value are
    returned as they are. Raises ValueError, naming the key, for text or bytes there that are not a JPEG or PNG
    image."""
    return _pictures(observation, False, "")


def _pictures(value: Any, picture: bool, path: str) -> Any:
    if isinstance(value, dict):
        return {key: _pictures(item, picture or (isinstance(key, str) and "image" in key.lower()),
                               f"{path}/{key}" if path else str(key))
                for key, item in value.items()}
    if picture and isinstance(value, (str, bytes, bytearray)):
        try:
            return frames.decode(value)
        except ValueError as e:
            raise ValueError(f"{path}: {e}") from e
    return value


class Pictures:
    """
    A policy whose robot may send its pictures as JPEG: infer() hands it each one as the array it reads
    (decode_pictures()).
    Every other attribute is the policy's own, its metadata and reset() included.

        policy = openpi.Pictures(policy)       # what patch() does with the policy openpi's server is given
    """

    def __init__(self, policy: Any) -> None:
        self.policy = policy

    def infer(self, obs: Any, *args: Any, **kwargs: Any) -> Any:
        """The policy's own infer() on `obs` with its pictures decoded (decode_pictures), its other arguments as
        given."""
        return self.policy.infer(decode_pictures(obs), *args, **kwargs)

    def __getattr__(self, name: str) -> Any:
        if name == "policy":                # not set yet (a copy being made): never the policy's own
            raise AttributeError(name)
        return getattr(self.policy, name)


class _Pinging:
    """websockets.asyncio.server as openpi's server module reads it, with serve() pinging each connection: the rest is
    the library's own."""

    def __init__(self, library: Any, options: dict) -> None:
        self.library, self.options = library, options

    def serve(self, *args: Any, **kwargs: Any) -> Any:
        return self.library.serve(*args, **{**self.options, **kwargs})

    def __getattr__(self, name: str) -> Any:
        if name in ("library", "options"):
            raise AttributeError(name)
        return getattr(self.library, name)


def patch(*, every_s: float = ping.EVERY_S, timeout_s: Optional[float] = None, server: Any = None) -> None:
    """
    openpi's own policy server, from now on in this process: each connection pinged every `every_s` (ping.py has why
    100 ms), and the policy each WebsocketPolicyServer is then made with handed to Pictures, so a picture a robot sends
    as JPEG reaches it as the array it reads. A robot that sends arrays is served as before. Call it before the server
    is made; a second call only changes the interval. `timeout_s`: how long the server waits for a pong before it drops
    the connection - None, the default, as long as it takes, since openpi's server answers no ping while its policy
    infers (the module's docstring).

    `server` is the module that defines openpi's WebsocketPolicyServer, openpi.serving.websocket_policy_server when not
    given. Raises TypeError for a module not built as that one is, a WebsocketPolicyServer started through the
    websockets library's `serve` at the module's `_server`.
    """
    if server is None:
        try:
            from openpi.serving import websocket_policy_server as server
        except ImportError as e:
            raise ImportError("patch() changes openpi's own policy server, which is not installed here: run it in "
                              "openpi's environment") from e
    library, made = getattr(server, "_server", None), getattr(server, "WebsocketPolicyServer", None)
    if not isinstance(made, type) or not callable(getattr(library, "serve", None)):
        raise TypeError("this server is not built as openpi's websocket_policy_server.py is (a WebsocketPolicyServer "
                        "started through the websockets library's serve, at `_server`): nothing to change")
    options = (ping.websockets_options(every_s, timeout_s) if timeout_s is not None
               else {"ping_interval": ping.websockets_options(every_s)["ping_interval"], "ping_timeout": None})
    if isinstance(library, _Pinging):
        library.options = options
        return
    server._server = _Pinging(library, options)
    init = made.__init__

    @functools.wraps(init)
    def __init__(self: Any, policy: Any, *args: Any, **kwargs: Any) -> None:
        init(self, policy if isinstance(policy, Pictures) else Pictures(policy), *args, **kwargs)

    made.__init__ = __init__


USAGE = """usage: python -m sequence_ai.network.openpi SCRIPT [ARGUMENTS...]

Runs SCRIPT - openpi's scripts/serve_policy.py, unchanged - as `python SCRIPT ARGUMENTS...` runs it, with openpi's
policy server changed first (patch()): each robot pinged every 100 ms while no inference runs, and each picture a robot
sends as JPEG handed to the policy as the array it reads. Run it where openpi's server runs, from its repository and in
its environment:

    uv run python -m sequence_ai.network.openpi scripts/serve_policy.py --env=DROID"""


def main(argv: Optional[list] = None) -> None:
    """`python -m sequence_ai.network.openpi SCRIPT [ARGUMENTS...]`: USAGE."""
    argv = sys.argv[1:] if argv is None else list(argv)
    if not argv or argv[0] in ("-h", "--help"):
        print(USAGE)
        raise SystemExit(0 if argv else 2)
    script = argv[0]
    if not os.path.isfile(script):
        raise SystemExit(f"no script at {script}: run this from openpi's repository, as the script itself is run")
    patch()
    sys.argv = argv
    if not getattr(sys.flags, "safe_path", False):
        sys.path[0] = os.path.dirname(os.path.abspath(script))     # as `python SCRIPT` puts the script's folder first
    _frames_known()
    runpy.run_path(script, run_name="__main__")


def _frames_known() -> None:
    """Each frame under this one that runs from no file on disk told to inspect by its module's name: `python -m`'s
    own, from runpy, which Python 3.11 and later runs frozen ("<frozen runpy>") - and so runpy.run_path's frames under
    the script, from the same file.
    WHY: inspect looks the module of such a frame up through every module loaded, each time it meets one
    (inspect.getmodule), and openpi's typecheck calls inspect.stack() at each Observation it makes
    (openpi/shared/array_typing.py). Measured on an L4 with pi05_droid and 2,400 modules loaded, 60 acts each: an act
    served under runpy took 23 ms longer than the same script run as `python SCRIPT` (server infer p50 220.03 ms,
    against 195.46 and 197.99 before and after it), all of it in Observation.from_dict (27.75 ms against 4.41)."""
    import inspect

    frame = sys._getframe()
    while frame is not None:
        name, file = frame.f_globals.get("__name__"), frame.f_code.co_filename
        if isinstance(name, str) and name in sys.modules and not os.path.exists(file):
            inspect.modulesbyfile.setdefault(file, name)
        frame = frame.f_back


if __name__ == "__main__":
    # the module as imported, so a script that imports it as well finds the same Pictures and the same patch
    from sequence_ai.network.openpi import main as _main

    _main()
