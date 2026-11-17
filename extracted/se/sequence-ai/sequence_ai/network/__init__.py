# SPDX-FileCopyrightText: Copyright (c) 2026 General Sequences Company
# SPDX-License-Identifier: Apache-2.0
"""
The network layer of sequence-ai: components for the connection between a robot and the GPU its policy runs on, each
usable on its own in your code.

Client side (the robot):
    window          keeps the connection's send window through the robot's pauses: BBR, TCP keepalive, a ping when idle
                    (where the server answers it)
    compress        compresses an observation's large arrays only where that saves more upload time than it costs
    frames          resizes a camera frame to the size its policy takes, and encodes it as JPEG, before upload
    wifi_power      detects Wi-Fi power saving and reports how to disable it

Server side (the GPU), for a uvicorn server:
    one_write       sends each response in one write, not three
    tcp_link        reads each client's link from the kernel: RTT, retransmitted segments, congestion window
    compressed      decompresses what the robot compressed, byte for byte

    ping            a server-side ping, so the robot's connection is not left idle while the server's event loop
                    is free: the options to pass, or websockets' own server with them (ping.serve)
    frames.decode   a picture the robot sent as JPEG, back into the array its policy reads

Both sides:
    msgpack_io      observations and responses as msgpack, numpy arrays as their raw data; reads openpi's layout too
    latency_stats   counters, gauges and latencies with their p50, p95 and p99, read as one snapshot

Combined:
    connect         the client-side components on one connection to your own server (link.py)
    openpi          openpi's own client and server with the components on them: the connection its client holds kept
                    warm, pictures sent as JPEG (image_tools), and its server pinging each robot and decoding them
                    (patch, or python -m sequence_ai.network.openpi with openpi's scripts/serve_policy.py)

bench/ (beside this package) measures your own link, so you add what helps on it.
"""
from .link import Link, connect

__all__ = ["Link", "connect"]
