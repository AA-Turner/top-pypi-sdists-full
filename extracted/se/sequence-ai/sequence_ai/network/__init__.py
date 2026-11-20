# SPDX-FileCopyrightText: Copyright (c) 2026 General Sequences Company
# SPDX-License-Identifier: Apache-2.0
"""
The network layer of sequence-ai: components for the connection between a robot and the GPU its policy runs on, each
usable on its own in your code. The robot's own connection is sequence_ai.connect(url): the platform's Policy, on the
robot's stream, to a policy server of yours (serve(), seq serve) as to a deployed policy.

Client side (the robot):
    window          keeps the connection's send window through the robot's pauses: BBR, TCP keepalive, a ping when idle
                    (where the server answers it)
    frames          resizes a camera frame to the size its policy takes, and encodes it as JPEG: openpi's image_tools
                    on the robot (openpi)
    wifi_power      detects Wi-Fi power saving and reports how to disable it
    bind            a connection that leaves by one network interface, whatever the default route: each of a robot's
                    lines (connect(url, lines=["eth0", "wwan0"]))
    loop            play(): a robot's control loop that plays each answer's steps while it asks for the next one
    record          a server's robots' steps read as they come (GET /record) into a file, and a camera's video out of it

Server side (the GPU), for a uvicorn server:
    websocket       the WebSocket a robot's stream comes on, for uvicorn (serve() runs it)
    one_write       sends each response in one write, not three
    tcp_link        reads each client's link from the kernel: RTT, retransmitted segments, congestion window
    ping            a server-side ping, so the robot's connection is not left idle while the server's event loop
                    is free: the options to pass, or websockets' own server with them (ping.serve)
    frames.decode   a picture sent as JPEG, back into the array its policy reads (openpi)

Both sides:
    msgpack_io      observations and responses as msgpack, numpy arrays as their raw data; reads openpi's layout too
    latency_stats   counters, gauges and latencies with their p50, p95 and p99, read as one snapshot
    lerobot         LeRobot's remote inference kept from going idle: a Zenoh configuration both ends take, which sends
                    a frame every 100 ms on an idle link (keep_alive_file)

Adapters:
    openpi          openpi's own client and server with the components on them: its client made once the server answers
                    (connect), the connection it holds kept warm, pictures sent as JPEG (image_tools), and its server
                    pinging each robot and decoding them (patch, or python -m sequence_ai.network.openpi with openpi's
                    scripts/serve_policy.py)

`python -m sequence_ai.check http://<gpu>:8000` says what is on between your robot and your server, and bench/ (beside
this package) measures your own link.
"""
from .loop import play

__all__ = ["play"]

# Each component, imported as first used: sequence_ai.network.frames without importing it first.
_COMPONENTS = ("bind", "frames", "latency_stats", "lerobot", "msgpack_io", "one_write", "openpi", "ping", "record",
               "tcp_link", "websocket", "wifi_power", "window")


def __getattr__(name: str) -> object:
    """A component of this package by its name, imported as it is first used."""
    if name in _COMPONENTS:
        import importlib

        return importlib.import_module(f".{name}", __name__)
    raise AttributeError(f"module {__name__!r} has no attribute {name!r}")
