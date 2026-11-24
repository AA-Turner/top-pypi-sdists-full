

"""
What is on, and what is not, between this machine and a policy server: run it on the robot.

    python -m sequence_ai.check http://<gpu>:8000
    python -m sequence_ai.check http://<gpu>:8000 --token "$TOKEN" --observation observation.npz

It reaches the server as a robot does - sequence_ai.connect(url, token=...), then wait_until_ready() - and each line is
one thing that changes how long the robot waits for its answers, marked `ok` (on), `no` (off: the line says how to turn
it on) or `--` (not something this machine or this server has, or nothing to measure it with):

    server              the server answers its ping with 200; what it says it is (its ping's JSON: version, process
                        id, how long it has run, policy, the speed-ups it kept) - a server that says nothing of it
                        may be another program at that address; and whether it takes the robot's stream
                        (x-seq-stream/3 in X-Seq-Act-Formats), which connect() sends observations and acts on
    round trip          pings on a kept connection, and a TCP connect, timed: the network's own part, which the
                        pings in inference are held to
    send window         whether a connection keeps its send window through the robot's pauses between requests: macOS
                        does; Linux does with BBR or net.ipv4.tcp_slow_start_after_idle 0, and otherwise restarts it,
                        so each upload after a pause takes several round trips
    BBR                 whether this machine's connections use BBR (Linux)
    Wi-Fi power saving  whether the Wi-Fi this machine uses saves power, which holds its packets back (read on Linux;
                        on macOS the line says it was not checked, and whether the machine is on Wi-Fi)
    pings when idle     the robot's stream pings after each 100 ms it has sent nothing, from its first observation
                        until 60 s after its last observation or act, which keeps the connection, and the Wi-Fi radio,
                        from going idle; on where the server answers its ping with 200
    pings in inference  whether the server answers pings while its model runs: a server that does not leaves the
                        robot's connection silent for the whole inference
    server time         whether the server says how long it took (handler_ms in each act's answer) of an act, the
                        rest of which was outside it: the network, and this machine
    first act           how long the first act took, against the next ones: a model compiled on its first inference

The lines that send an act - pings in inference, server time, first act - send it as a robot does, on its stream: the
observation handed over (policy.observe), then the act (policy.act). They need an observation - `--observation` (a file
of msgpack as msgpack_io.pack writes it, a .npz of arrays, or .json), else the one the server hands out at GET /example
(serve(example=...) does) - and a server that takes the robot's stream. Without either they say so.

Exit status: 0 when no line is `no`, 1 when one is, 2 when the server cannot be reached, is not ready within --wait, or
refuses this machine.
"""
from __future__ import annotations

import argparse
import json
import os
import socket
import statistics
import sys
import threading
import time
from typing import Any, List, NamedTuple, Optional
from urllib.parse import urlsplit

from .network import msgpack_io, wifi_power, window

__all__ = ["Row", "main", "run"]



PING = "/ping"


class Row(NamedTuple):
    """One line: `status` "ok", "no" or "--", the thing checked, and what was found."""
    status: str
    name: str
    detail: str


def _ms(seconds: float) -> str:
    return f"{seconds * 1000:.1f} ms"


def _identity(response: Any) -> Optional[str]:
    """What the server says it is, from its ping's JSON alone - serve() names its server, version, up_s, pid and policy
    there: "sequence-ai 0.63.0, pid 4242, up 3.2 min, policy pi05"; None when the ping holds no JSON that names a
    server."""
    said: dict = {}
    if "json" in response.headers.get("content-type", ""):
        try:
            body = response.json()
            said = body if isinstance(body, dict) and body.get("server") else {}
        except ValueError:
            said = {}
    if not said:
        return None
    parts = [f"{said.get('server')} {said.get('version') or ''}".strip()]
    if said.get("pid") is not None:
        parts.append(f"pid {said['pid']}")
    up = said.get("up_s")
    if isinstance(up, (int, float)):
        parts.append(f"up {up / 3600:.1f} h" if up >= 3600 else f"up {up / 60:.1f} min" if up >= 60 else f"up {up:.0f} s")
    if said.get("policy"):
        parts.append(f"policy {said['policy']}")
    if isinstance(said.get("optimized"), list):
        on = [str(name) for name in said["optimized"]]
        parts.append(f"speed-ups on: {' and '.join(on)}" if on else "no speed-up on")
    return ", ".join(parts)


def _observation_from(path: str) -> Any:
    """An observation from a file: .npz (its arrays, by name), .json, or anything else as msgpack."""
    if path.endswith(".npz"):
        import numpy as np

        with np.load(path, allow_pickle=False) as held:
            return {name: held[name] for name in held.files}
    with open(path, "rb") as f:
        raw = f.read()
    if path.endswith(".json"):
        return json.loads(raw)
    return msgpack_io.unpack(raw)


def _tcp_connect_s(url: str, n: int = 3) -> Optional[float]:
    """The median time of `n` TCP connects to the server's host and port: one network round trip, with nothing of
    the server's in it. None when it cannot connect."""
    parts = urlsplit(url)
    port = parts.port or (443 if parts.scheme == "https" else 80)
    took = []
    for _ in range(n):
        began = time.perf_counter()
        try:
            with socket.create_connection((parts.hostname, port), timeout=5):
                took.append(time.perf_counter() - began)
        except OSError:
            return None
    return statistics.median(took)


def _window_rows() -> List[Row]:
    """The send window and BBR, from this machine's own settings."""
    bbr = window.bbr_options() is not None
    if sys.platform == "darwin":
        return [Row("ok", "send window", "macOS keeps a connection's send window through pauses"),
                Row("--", "BBR", "macOS has no BBR, and needs none for the window")]
    if not sys.platform.startswith("linux"):
        return [Row("--", "send window", f"not read on {sys.platform}"), Row("--", "BBR", f"not read on {sys.platform}")]
    restarts = window.restarts_after_idle()
    if bbr:
        rows = [Row("ok", "send window", "kept through pauses: BBR is on this machine's connections")]
    elif not restarts:
        rows = [Row("ok", "send window", "kept through pauses: net.ipv4.tcp_slow_start_after_idle is 0")]
    else:
        rows = [Row("no", "send window", "Linux restarts it after each pause (net.ipv4.tcp_slow_start_after_idle is "
                                         "1): `sudo modprobe tcp_bbr`, or `sudo sysctl -w "
                                         "net.ipv4.tcp_slow_start_after_idle=0`")]
    if bbr:
        rows.append(Row("ok", "BBR", "on this machine's connections"))
    else:
        rows.append(Row("no" if restarts else "--", "BBR",
                        "not available: the tcp_bbr module is not loaded (`sudo modprobe tcp_bbr`)"))
    return rows


def _wifi_row() -> Row:
    if sys.platform == "darwin":
        iface = wifi_power.mac_wifi_iface()
        return Row("--", "Wi-Fi power saving", "not checked: macOS gives nothing to read it from"
                   + (f"; this machine's requests go over Wi-Fi ({iface}), and a wired connection takes the question "
                      "away" if iface else "; this machine is not on Wi-Fi"))
    if not sys.platform.startswith("linux"):
        return Row("--", "Wi-Fi power saving", f"not checked on {sys.platform}")
    iface = wifi_power.default_iface()
    if iface is None or not os.path.isdir(os.path.join("/sys/class/net", iface, "wireless")):
        return Row("ok", "Wi-Fi power saving", "this machine is not on Wi-Fi" + (f" ({iface})" if iface else ""))
    on = wifi_power.power_save_on(iface)
    if on is None:
        return Row("--", "Wi-Fi power saving", f"{iface} is Wi-Fi, and neither iw nor iwconfig reports its power saving")
    return Row("no", "Wi-Fi power saving", wifi_power.words(iface)) if on else \
        Row("ok", "Wi-Fi power saving", f"off for {iface}")


def _pings_in_inference(url: str, headers: dict, ping_path: str, act: Any, idle_s: float,
                        acts: int = 3, every_s: float = 0.01) -> "tuple[Row, list]":
    """Pings on a connection of their own while acts run on the robot's. A server that answers none while its model runs
    holds one of them for most of the inference: an act whose slowest ping took half of what the act took past the idle
    round trip (and 20 ms more than that round trip) had its pings held, and the server holds them when most acts did.
    A ping answered before the act's request reached the server says nothing either way, so the median would not do.
    `act()` returns the time its server says it took (None where it says none); one ping each `every_s` at most, so a
    server on this machine is not kept busy answering them. Returns the row and each act's (time, server's time)."""
    import httpx

    slowest, held, during, totals = [], 0, [], []
    with httpx.Client(base_url=url, headers=headers, timeout=30.0) as probe:
        probe.get(ping_path)
        for _ in range(acts):
            finished, box = threading.Event(), {}

            def run() -> None:
                try:
                    box["began"] = time.perf_counter()
                    box["server"] = act()
                except Exception as e:
                    box["error"] = e
                finally:
                    box["ended"] = time.perf_counter()
                    finished.set()

            thread = threading.Thread(target=run, daemon=True)
            thread.start()
            pings = []
            while not finished.is_set():
                began = time.perf_counter()
                probe.get(ping_path)
                pings.append((began, time.perf_counter()))
                finished.wait(max(0.0, began + every_s - time.perf_counter()))
            thread.join()
            if "server" not in box:
                raise box.get("error") or RuntimeError("the act did not end")
            total = box["ended"] - box["began"]
            totals.append((total, box["server"]))

            these = [end - began for began, end in pings if began + 2 * idle_s < box["ended"]]
            if these:
                during += these
                slowest.append(max(these))
                held += max(these) >= max(idle_s + 0.02, 0.5 * (total - idle_s))
    if not slowest:
        return Row("--", "pings in inference", f"each act took {_ms(statistics.median(t for t, _ in totals))}, too "
                                               "short to tell"), totals
    if 2 * held <= len(slowest):
        return Row("ok", "pings in inference", f"answered while the model ran ({len(during)} pings in "
                                               f"{len(slowest)} acts)"), totals
    return Row("no", "pings in inference", f"held while the model ran: the slowest ping of {held} of {len(slowest)} "
                                           "acts waited for the act - the robot's connection is silent for the whole "
                                           "inference; serve() runs the model on a thread of its own"), totals


def _ping_status(url: str, headers: dict) -> int | None:
    """The status the server answers one ping with now, as this machine asks it (its token, where given); None when
    nothing answers: what a server that was not ready by the end of the wait says."""
    import httpx

    try:
        return httpx.get(url.rstrip("/") + PING, headers=headers, timeout=5.0).status_code
    except httpx.HTTPError:
        return None


def _not_ready(url: str, wait_s: float, status: int | None, token: str | None) -> Row:
    """The server's line when the robot cannot act on it: its ping refused (401, 403: the token, with how to give one
    where none was), else not ready within `wait_s` - what its ping answered then, or that nothing did."""
    if status in (401, 403):
        hint = ": give it with --token" if not token else ""
        return Row("no", "server", f"refused this machine's ping ({status}){hint}")
    return Row("no", "server", f"{url} was not ready in {wait_s:g} s: "
                               + (f"its ping's answer is {status}" if status is not None else "nothing answered"))


def run(url: str, *, token: Optional[str] = None, observation: Any = None, pings: int = 10,
        wait_s: float = 60.0) -> "tuple[List[Row], int]":
    """Check the server at `url` (the module's docstring): its rows, and the exit status they give. The server is
    reached as a robot reaches it - connect(url, token=...), wait_until_ready(), each act an observe() and the act()
    after it on the robot's stream - so what is measured is what the robot's own loop meets."""
    import httpx

    from . import connect
    from ._core.worker_stream import FORMAT as STREAM_FORMAT
    from ._core.worker_transport import FORMATS_HEADER
    from .errors import AuthError, InvalidRequest, PermissionDenied, SequencesError, Unavailable

    if "://" not in url:

        return [Row("no", "server", f"{url} is not an address: give it as http://<host>:<port>")], 2
    headers = {"Authorization": f"Bearer {token}"} if token else {}
    rows: List[Row] = []
    policy = connect(url, token=token)
    try:
        try:
            policy.wait_until_ready(timeout_s=wait_s)
        except (AuthError, PermissionDenied) as e:
            return [_not_ready(url, wait_s, e.status, token)], 2
        except InvalidRequest as e:
            return [Row("no", "server", str(e))], 2
        except Unavailable:

            return [_not_ready(url, wait_s, _ping_status(url, headers), token)], 2

        with httpx.Client(base_url=url, headers=headers, timeout=10.0,
                          transport=httpx.HTTPTransport(socket_options=window.socket_options())) as client:
            answered = []
            for _ in range(max(1, pings)):
                began = time.perf_counter()
                response = client.get(PING)
                answered.append(time.perf_counter() - began)
        idle, status, identity = statistics.median(answered), response.status_code, _identity(response)


        named = {part.strip().lower() for part in response.headers.get(FORMATS_HEADER, "").split(",")}
        streams = STREAM_FORMAT in named
        stream = (f"takes the robot's stream ({STREAM_FORMAT})" if streams else
                  f"does not take the robot's stream (no {STREAM_FORMAT} in {FORMATS_HEADER}), which connect() sends "
                  "observations and acts on: serve() takes it where sequence-base is installed (Python 3.10 or later)")
        if identity:
            rows.append(Row("ok" if status == 200 and streams else "no", "server",
                            f"{identity}; it answers {PING} with {status} and {stream}"))
        else:
            rows.append(Row("no", "server", f"answers {PING} with {status} but does not say it is serve() (no server "
                                            "named in its JSON): if serve() was started there, another program answers "
                                            f"at this address; it {stream}"))
        tcp = _tcp_connect_s(url)
        rows.append(Row("ok", "round trip", f"{len(answered)} pings answered on a kept connection"
                                            + (", and a TCP connect" if tcp is not None else "")))
        rows += _window_rows()
        rows.append(_wifi_row())
        rows.append(Row("ok", "pings when idle", f"connect() pings after each {_ms(0.1)} of idle time, and the server "
                                                 f"answers {PING} with 200: the pings go on the robot's stream, from "
                                                 "its first observation until 60 s after its last observation or act, "
                                                 "and keep the connection, and the Wi-Fi radio, from going idle")
                    if status == 200 else
                    Row("no", "pings when idle", f"the server answers {PING} with {status}, not 200: serve() answers "
                                                 "200 while its policy is ready"))

        source = "--observation"
        if observation is None:
            try:
                with httpx.Client(base_url=url, headers=headers, timeout=10.0) as client:
                    response = client.get("/example")
                if response.status_code == 200:
                    observation, source = msgpack_io.unpack(response.content), "GET /example"
            except (httpx.HTTPError, msgpack_io.MsgpackError):
                observation = None

        if observation is None or not streams:
            why = ("needs an observation: --observation FILE, or a server that hands one out at GET /example"
                   if observation is None else "needs a server that takes the robot's stream")
            rows += [Row("--", "pings in inference", why), Row("--", "server time", why), Row("--", "first act", why)]
        else:
            def act() -> float | None:
                """One act, and the seconds its server says it took - handler_ms of the answer's perf, from the act's
                last byte to its answer, which the robot's client keeps as the last act's - or None where it says
                none."""
                policy.observe(observation)
                policy.act()
                said = policy._last_perf.get("handler_ms")
                return said / 1000.0 if isinstance(said, (int, float)) else None

            try:
                began = time.perf_counter()
                act()
                first = time.perf_counter() - began
                row, totals = _pings_in_inference(url, headers, PING, act, idle)
            except SequencesError as e:

                rows.append(Row("no", "act", f"an act on the observation from {source} failed: {e}"))
                return rows, 1
            rows.append(row)
            took = statistics.median(t for t, _ in totals)
            said = sorted((t, server) for t, server in totals if server is not None)
            if said:
                t, server = said[len(said) // 2]
                rows.append(Row("ok", "server time", f"the server says it took {_ms(server)} of a {_ms(t)} act; "
                                                     "the rest was outside it, on the network and in this machine"))
            else:
                rows.append(Row("no", "server time", "the server does not say how long it took (no handler_ms in "
                                                     "its answers' perf): the robot cannot tell its time from the "
                                                     "network's"))
            rows.append(Row("ok", "first act", f"{_ms(first)}, the next ones {_ms(took)} (observation from {source})"))
    except httpx.HTTPError as e:
        rows.append(Row("no", "server", f"{type(e).__name__}: {e}"))
        return rows, 2
    finally:
        policy.close()
    return rows, (1 if any(row.status == "no" for row in rows) else 0)


def main(argv: Optional[List[str]] = None) -> None:
    """`python -m sequence_ai.check URL [--token TOKEN] [--observation FILE]`: the module's docstring."""
    parser = argparse.ArgumentParser(prog="python -m sequence_ai.check",
                                     description="What is on, and what is not, between this machine and a policy "
                                                 "server.")
    parser.add_argument("url", help="the server, e.g. http://<gpu>:8000")
    parser.add_argument("--token", help="the server's token: sent to the address given, and nowhere else")
    parser.add_argument("--observation", help="an observation to send: msgpack, .npz or .json")
    parser.add_argument("--wait", type=float, default=60.0, help="seconds to wait for the server to be ready")
    args = parser.parse_args(argv)
    observation = _observation_from(args.observation) if args.observation else None
    rows, status = run(args.url, token=args.token, observation=observation, wait_s=args.wait)
    width = max(len(row.name) for row in rows)
    print(f"sequence-ai check: {args.url}\n")
    for row in rows:
        print(f"  {row.status:<3} {row.name:<{width}}  {row.detail}")
    raise SystemExit(status)


if __name__ == "__main__":
    main()
