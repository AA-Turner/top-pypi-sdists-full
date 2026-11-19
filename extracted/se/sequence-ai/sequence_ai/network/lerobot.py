# SPDX-FileCopyrightText: Copyright (c) 2026 General Sequences Company
# SPDX-License-Identifier: Apache-2.0
"""
LeRobot's remote inference (lerobot 0.7.0, which uses Zenoh), kept from going idle between observations.

    from sequence_ai.network import lerobot

    path = lerobot.keep_alive_file("zenoh-keep-alive.json5")     # a Zenoh configuration: a frame every 100 ms when idle
    # on both the robot and the server, pass it to LeRobot's Zenoh transport:
    #     ZenohConfig(config_file=path, connect_endpoints=[...])     or     --zenoh.config_file=zenoh-keep-alive.json5

In one sentence: LeRobot's ZenohConfig loads `config_file` first and sets only the topology over it, so a transport
setting written there stays → `transport/link/tx/keep_alive` is how many keep-alive frames a Zenoh link sends in one
lease (10 s unless changed): at 100 an idle link sends one every 100 ms, from each side → the robot's kernel never
counts the connection idle, which is what restarts its send window (window.py).

What was verified: Zenoh 1.10.2 accepts the setting, and two idle peers on one machine then sent a frame every 102 ms
each way, where without it they sent one every 1.5 s or less often. Measured between two Zenoh peers on two cloud
machines (bench/zenoh_bench.py, docs/measurements.md): a 100 KB request 0.53 s after each response took 38.1, 44.8, 82.8
and 164.3 ms at RTTs of 11, 21, 41 and 81 ms, and 13.9, 23.2, 42.3 and 82.2 ms with the file on both ends, 40 requests
per cell. bench/ measures your link.

What it does not do: BBR. Zenoh opens its own sockets, so only the machine's default congestion control reaches them
(`sysctl net.ipv4.tcp_congestion_control`, which needs root).

The lease is unchanged: it is how long a silent peer is waited for before the link is dropped, and a short one drops a
robot whose Wi-Fi stalls for a moment.

Standard library only.
"""
from __future__ import annotations

import json
from typing import Optional

LEASE_MS = 10_000      # Zenoh's own default: how long a silent peer is waited for


def keep_alive_settings(every_ms: float = 100.0, lease_ms: int = LEASE_MS) -> dict:
    """The Zenoh settings that make an idle link send a frame every `every_ms`, for a link whose lease is `lease_ms`:
    as a nested map, the shape a Zenoh configuration file has."""
    if not every_ms > 0 or not lease_ms > 0 or every_ms > lease_ms:
        raise ValueError(f"a frame every {every_ms!r} ms in a lease of {lease_ms!r} ms: both must be positive, "
                         "and the first no more than the second")
    tx = {"keep_alive": max(1, round(lease_ms / every_ms))}
    if lease_ms != LEASE_MS:
        tx["lease"] = int(lease_ms)
    return {"transport": {"link": {"tx": tx}}}


def keep_alive_file(path: str, every_ms: float = 100.0, lease_ms: int = LEASE_MS, base: Optional[dict] = None) -> str:
    """Write those settings to `path` as a Zenoh configuration (JSON, which JSON5 reads; name it *.json5) and return
    `path`. `base`: your own settings to keep alongside them (TLS, access control), as a nested map."""
    settings = dict(base or {})
    transport = dict(settings.get("transport") or {})
    link = dict(transport.get("link") or {})
    link["tx"] = {**(link.get("tx") or {}), **keep_alive_settings(every_ms, lease_ms)["transport"]["link"]["tx"]}
    transport["link"] = link
    settings["transport"] = transport
    with open(path, "w") as f:
        json.dump(settings, f, indent=2)
        f.write("\n")
    return path
