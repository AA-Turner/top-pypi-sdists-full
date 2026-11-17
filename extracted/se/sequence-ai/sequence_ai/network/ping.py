# SPDX-FileCopyrightText: Copyright (c) 2026 General Sequences Company
# SPDX-License-Identifier: Apache-2.0
"""
A server-side ping, so that the robot's connection is never idle, with nothing changed on the robot.

    import websockets
    from sequence_ai.network import ping

    async with ping.serve(handler, host, port) as server:      # websockets' own server, with a ping every 100 ms
        await server.serve_forever()

    async with websockets.serve(handler, host, port, **ping.websockets_options()):    # the same, as its options
        ...

    uvicorn.run(app, **ping.uvicorn_options())                                         # the same, under uvicorn

WHY from the server: what restarts a robot's send window is the robot's own silence: on Linux, nothing sent for longer
than its retransmission timeout (window.py). A WebSocket library answers a ping with a pong by itself, so a server that
pings makes the robot send a few bytes each interval, and its kernel never counts the connection idle. The robot's
program does not change, and neither does its library.

WHY 100 ms: the robot's silence must stay shorter than its retransmission timeout, which is about its RTT plus 200 ms. A
WebSocket server sends its next ping one interval after the last one's pong came back, so the robot is silent for the
interval plus one RTT: an interval under 200 ms is sufficient on a link of any length, and at 100 ms a ping that is lost
still leaves the next one inside the limit. Measured between machines of one cloud provider at an RTT of 11.7 ms: pings
190 ms apart still kept the window (an upload after a pause took 1.18 round trips) and pings 250 ms apart did not
(2.04); 25 to 190 ms apart measured the same.

When it helps: uploads after a pause went from 3.0 round trips to 1.1 (100 KB and 500 KB) and 1.25 (1 MB), between
machines of one cloud provider at RTTs of 11.7 and 69.2 ms.

When it does not: on a home connection with a cellular uplink, about 36 ms from the GPU, 921,600-byte uploads after 10 s
of silence took a median of 264 ms without the pings and 368 ms with them (six each, alternating): no benefit there. A
window that the pings do not fill still shrinks; BBR on the robot keeps that one (window.keep). bench/ measures your own
link.

What it cannot do: a server that answers one HTTP/1.1 request with one response cannot send anything unsolicited. There
the ping must come from the robot: window.Warm, which sequence_ai.network.connect() puts on its connection.

Standard library only: this gives each server the options it already takes, and serve() imports websockets when it is
called.
"""
from __future__ import annotations

from typing import Any

EVERY_S = 0.1          # interval between two pings
TIMEOUT_S = 20.0       # how long a pong may take before the server drops a connection: slow is not dead


def _checked(every_s: float, timeout_s: float) -> tuple:
    if not every_s > 0 or not timeout_s > 0:
        raise ValueError(f"a ping's interval and timeout must be positive seconds, not {every_s!r} and {timeout_s!r}")
    return float(every_s), float(timeout_s)


def websockets_options(every_s: float = EVERY_S, timeout_s: float = TIMEOUT_S) -> dict:
    """The options `websockets.serve(handler, host, port, **these)` takes to ping each connection every `every_s`."""
    every_s, timeout_s = _checked(every_s, timeout_s)
    return {"ping_interval": every_s, "ping_timeout": timeout_s}


def serve(handler: Any, host: Any = None, port: Any = None, *, every_s: float = EVERY_S, timeout_s: float = TIMEOUT_S,
          **options: Any) -> Any:
    """`websockets.asyncio.server.serve(handler, host, port, **options)`, with each connection pinged every `every_s`:
    the same server, used the same way (`async with ping.serve(...) as server:`). An option passed in `options` is used
    in place of this function's own (`ping_interval`, `ping_timeout`). Requires the websockets library, version 14 or
    later."""
    try:
        from websockets.asyncio.server import serve as _serve
    except ImportError as e:
        raise ImportError("ping.serve() runs websockets' own server, version 14 or later: "
                          "pip install websockets") from e
    return _serve(handler, host, port, **{**websockets_options(every_s, timeout_s), **options})


def uvicorn_options(every_s: float = EVERY_S, timeout_s: float = TIMEOUT_S) -> dict:
    """The options `uvicorn.run(app, **these)` and `uvicorn.Config(app, **these)` take to ping each WebSocket connection
    every `every_s`. Verified with uvicorn 0.54 on its `auto`, `websockets-sansio` and `websockets` implementations;
    uvicorn 0.39's `websockets-sansio` sends no pings, so on an older uvicorn leave `ws` at `auto` or pass
    `ws="websockets"`."""
    every_s, timeout_s = _checked(every_s, timeout_s)
    return {"ws_ping_interval": every_s, "ws_ping_timeout": timeout_s}
