

"""
What is on, and what is not, between this machine and a policy server: run it on the robot.

    python -m sequence_ai.check http://<gpu>:8000
    python -m sequence_ai.check http://<gpu>:8000 --token "$TOKEN" --observation observation.npz
    python -m sequence_ai.check http://<gpu>:8000 --lines eth0,wwan0      # each uplink too (network.lines)

Each line is one thing that changes how long the robot waits for its answers, marked `ok` (on), `no` (off: the line says
how to turn it on) or `--` (not something this machine or this server has, or nothing to measure it with):

    server              the server answers its ping with 200; what it says it is (X-Seq-Server, and its ping's JSON:
                        version, process id, how long it has run, policy) - a server that says nothing of it may be
                        another program at that address; and what it says it restores (X-Seq-Reads)
    round trip          the median time of a ping on a kept connection, and of a TCP connect: the network's own part
    send window         whether a connection keeps its send window through the robot's pauses between requests: macOS
                        does; Linux does with BBR or net.ipv4.tcp_slow_start_after_idle 0, and otherwise restarts it,
                        so each upload after a pause takes several round trips
    BBR                 whether this machine's connections use BBR (Linux)
    Wi-Fi power saving  whether the Wi-Fi this machine uses saves power, which holds its packets back (read on Linux;
                        on macOS the line says it was not checked, and whether the machine is on Wi-Fi)
    pings when idle     whether the server answers the ping the robot's connection sends after each 100 ms of idle
                        time, which keeps the connection, and the Wi-Fi radio, from going idle
    pings in inference  whether the server answers pings while its model runs: a server that does not leaves the
                        robot's connection silent for the whole inference
    pictures as JPEG    whether the server restores pictures sent as JPEG, so connect() sends them so; with an
                        observation, its pictures' size as arrays and as JPEG
    compression         whether the server restores compressed items, so connect() compresses large arrays where that
                        saves time
    server time         whether the server says how long it took (Server-Timing), and how much of an act was
                        outside it: the network, and this machine
    first act           how long the first act took, against the next ones: a model compiled on its first inference

With --lines, a robot's uplinks, by their network interfaces (connect(url, lines=[...])):

    line <interface>    the median time of a ping on a connection that leaves by that interface alone (network.bind),
                        or that nothing answered by it; an interface this machine has not is named with the ones it has
    lines               whether the server runs an act's copies once ("once" in X-Seq-Reads), so each act goes on
                        every line; one that does not gets each act on one line
    lines' answers      with an observation, 5 acts sent on every line: how many each line answered first, and the
                        bytes each act sends on each line - at one act a second, how many MB an hour that is

The lines that send an act - pings in inference, server time, first act - need an observation: `--observation` (a file
of msgpack as msgpack_io.pack writes it, a .npz of arrays, or .json), else the one the server hands out at GET /example
(serve(example=...) does). Without either they say so.

Exit status: 0 when no line is `no`, 1 when one is, 2 when the server cannot be reached or refuses this machine.
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

from .network import compress as _compress
from .network import compressed as _compressed
from .network import frames, msgpack_io, wifi_power, window
from .network.link import FIRST_TIMEOUT_S, READS_HEADER, SERVER_HEADER, Link, reads_of

__all__ = ["Row", "main", "run"]


class Row(NamedTuple):
    """One line: `status` "ok", "no" or "--", the thing checked, and what was found."""
    status: str
    name: str
    detail: str


def _ms(seconds: float) -> str:
    return f"{seconds * 1000:.1f} ms"


def _identity(response: Any) -> Optional[str]:
    """What the server says it is, from its ping's answer: "sequence-ai 0.63.0, pid 4242, up 3.2 min, policy pi05" from
    its JSON, else the name and version in its X-Seq-Server header; None when it says neither."""
    said: dict = {}
    if response is not None and "json" in response.headers.get("content-type", ""):
        try:
            body = response.json()
            said = body if isinstance(body, dict) and body.get("server") else {}
        except ValueError:
            said = {}
    header = response.headers.get(SERVER_HEADER) if response is not None else None
    if not said and header:
        name, _, version = header.partition("/")
        said = {"server": name.strip(), "version": version.strip()}
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
        return Row("ok", "pings in inference", f"answered while the model ran: {_ms(statistics.median(during))} "
                                               f"against {_ms(idle_s)} idle ({len(during)} pings in {len(slowest)} "
                                               "acts)"), totals
    return Row("no", "pings in inference", f"held while the model ran: the slowest ping of {held} of {len(slowest)} "
                                           f"acts took {_ms(statistics.median(slowest))} against {_ms(idle_s)} idle - "
                                           "the robot's connection is silent for the whole inference; serve() runs "
                                           "the model on a thread of its own"), totals


def run(url: str, *, token: Optional[str] = None, observation: Any = None, ping_path: str = "/ping",
        act_path: str = "/act", pings: int = 10, wait_s: float = 60.0,
        lines: Optional[List[str]] = None) -> "tuple[List[Row], int]":
    """Check the server at `url` (the module's docstring): its rows, and the exit status they give."""
    import httpx

    headers = {"Authorization": f"Bearer {token}"} if token else {}
    rows: List[Row] = []
    link = Link(url, token=token, act_path=act_path, ping_path=ping_path, check=False)
    try:
        try:
            link.wait_until_ready(timeout_s=wait_s)
        except TimeoutError as e:
            return [Row("no", "server", str(e))], 2
        except httpx.HTTPStatusError as e:
            code = e.response.status_code
            hint = ": give it with --token" if code in (401, 403) and not token else ""
            return [Row("no", "server", f"refused this machine's ping ({code}){hint}")], 2

        with httpx.Client(base_url=url, headers=headers, timeout=10.0,
                          transport=httpx.HTTPTransport(socket_options=window.socket_options())) as client:
            answered = []
            status, said, response = None, None, None
            for _ in range(max(1, pings)):
                began = time.perf_counter()
                response = client.get(ping_path)
                answered.append(time.perf_counter() - began)
                status, said = response.status_code, response.headers.get(READS_HEADER)
        reads = reads_of(said)
        idle = statistics.median(answered)
        restores = ", ".join(sorted(reads)) if reads else "nothing (no X-Seq-Reads)"
        identity = _identity(response)
        if status == 200 and identity:
            rows.append(Row("ok", "server", f"{identity}; it answers {ping_path} with 200 and restores {restores}"))
        elif status == 200:
            rows.append(Row("no", "server", f"answers {ping_path} with 200 but does not say it is serve() (no "
                                            f"{SERVER_HEADER}): if serve() was started there, another program answers "
                                            f"at this address; it restores {restores}"))
        else:
            rows.append(Row("no", "server", f"answers {ping_path} with {status}: it has no ping, so nothing keeps the "
                                            "robot's connection busy between requests; serve() answers it"))
        tcp = _tcp_connect_s(url)
        rows.append(Row("ok", "round trip", f"{_ms(idle)} for a ping on a kept connection (median of {len(answered)})"
                                            + (f"; {_ms(tcp)} for a TCP connect" if tcp is not None else "")))
        rows += _window_rows()
        rows.append(_wifi_row())
        rows.append(Row("ok", "pings when idle", f"connect() pings after each {_ms(0.1)} of idle time, and the server "
                                                 "answers them") if status == 200 else
                    Row("no", "pings when idle", f"the server does not answer {ping_path}: connect() pings it, and "
                                                 "they keep nothing busy"))

        source = "--observation"
        if observation is None:
            try:
                with httpx.Client(base_url=url, headers=headers, timeout=10.0) as client:
                    response = client.get("/example")
                if response.status_code == 200:
                    observation, source = msgpack_io.unpack(response.content), "GET /example"
            except (httpx.HTTPError, msgpack_io.MsgpackError):
                observation = None

        pictures, packed_bytes, array_bytes = 0, None, None
        if observation is not None:
            packed, pictures = frames.pack_pictures(observation)
            array_bytes, packed_bytes = len(msgpack_io.pack(observation)), len(msgpack_io.pack(packed))
        if frames.PICTURE_KIND in reads:
            detail = "the server restores them, so connect() sends each HxWx3 uint8 array as JPEG"
            if observation is not None:
                detail += (f": {pictures} in this observation, {array_bytes:,} bytes as arrays, {packed_bytes:,} with "
                           "them as JPEG" if pictures else ": this observation holds none")
            rows.append(Row("ok", "pictures as JPEG", detail))
        elif observation is not None and not pictures:
            rows.append(Row("--", "pictures as JPEG", "this observation holds no picture (an HxWx3 uint8 array)"))
        else:
            rows.append(Row("no", "pictures as JPEG", "the server does not restore them (no \"jpeg\" in X-Seq-Reads): "
                                                      "pictures go as arrays; serve() restores them"
                            + (f" - this observation would go from {array_bytes:,} to {packed_bytes:,} bytes"
                               if pictures else "")))
        codecs = frozenset(_compressed.CODECS) & reads
        codec = _compress.codec_for(codecs) if codecs else None
        if codec is not None:
            rows.append(Row("ok", "compression", f"the server restores {', '.join(sorted(codecs))}, so connect() "
                                                 f"compresses large arrays with {codec} where that saves time"))
        elif codecs:
            rows.append(Row("no", "compression", f"the server restores {', '.join(sorted(codecs))} only, which this "
                                                 "machine does not have: `pip install zstandard`"))
        else:
            rows.append(Row("no", "compression", "the server does not restore compressed items (no codec in "
                                                 "X-Seq-Reads); serve() restores them"))

        if observation is None:
            why = "needs an observation: --observation FILE, or a server that hands one out at GET /example"
            rows += [Row("--", "pings in inference", why), Row("--", "server time", why), Row("--", "first act", why)]
        else:
            try:
                began = time.perf_counter()
                link.act(observation)
                first = time.perf_counter() - began
                row, totals = _pings_in_inference(url, headers, ping_path,
                                                  lambda: (link.act(observation), link.last_server_s)[1], idle)
            except httpx.HTTPStatusError as e:
                rows.append(Row("no", "act", f"the server refused the observation from {source} "
                                             f"({e.response.status_code}): {e.response.text[:200]}"))
                return rows, 1
            rows.append(row)
            took = statistics.median(t for t, _ in totals)
            said = sorted((t, server) for t, server in totals if server is not None)
            if said:
                t, server = said[len(said) // 2]
                rows.append(Row("ok", "server time", f"the server says it took {_ms(server)} of a {_ms(t)} act: "
                                                     f"{_ms(max(0.0, t - server))} outside it, on the network and in "
                                                     "this machine"))
            else:
                rows.append(Row("no", "server time", "the server does not say how long its model took (Server-Timing):"
                                                     " connect() counts that time as the link's"))
            rows.append(Row("ok", "first act", f"{_ms(first)}, the next ones {_ms(took)} (observation from {source}); "
                                               f"connect() waits up to {FIRST_TIMEOUT_S:g} s for the first"))
        if lines:
            rows += _lines_rows(url, lines, token=token, observation=observation, act_path=act_path,
                                ping_path=ping_path, pings=pings)
    except httpx.HTTPError as e:
        rows.append(Row("no", "server", f"{type(e).__name__}: {e}"))
        return rows, 2
    finally:
        link.close()
    return rows, (1 if any(row.status == "no" for row in rows) else 0)


LINES_ACTS = 5


def _lines_rows(url: str, names: List[str], *, token: Optional[str], observation: Any, act_path: str,
                ping_path: str, pings: int) -> List[Row]:
    """--lines' rows (the module's docstring): each line's ping by its own interface, whether the server runs an act's
    copies once, and with an observation, which line answered first and what each act sends on each."""
    import httpx

    from .network import bind as _bind
    from .network.lines import Lines

    headers = {"Authorization": f"Bearer {token}"} if token else {}
    try:
        robot = Lines([Link(url, token=token, act_path=act_path, ping_path=ping_path, check=False, bind=name)
                       for name in names])
    except (OSError, ValueError) as e:
        return [Row("no", "lines", str(e))]
    rows: List[Row] = []
    try:
        for name, line in zip(names, robot.links):
            try:
                line.wait_until_ready(timeout_s=10.0)
                transport = _bind.transport(httpx, name, socket_options=window.socket_options())
                with httpx.Client(base_url=url, headers=headers, timeout=10.0, transport=transport) as client:
                    answered = []
                    for _ in range(max(1, pings)):
                        began = time.perf_counter()
                        client.get(ping_path)
                        answered.append(time.perf_counter() - began)
            except (httpx.HTTPError, TimeoutError, OSError) as e:
                rows.append(Row("no", f"line {name}", f"nothing answered by {name}: {type(e).__name__}: {e}"))
                continue
            rows.append(Row("ok", f"line {name}", f"{_ms(statistics.median(answered))} for a ping by {name} alone "
                                                  f"(median of {len(answered)})"))
        if robot.once:
            rows.append(Row("ok", "lines", "the server runs an act's copies once (\"once\" in X-Seq-Reads), so each "
                                           "act goes on every line and the first answer is used"))
        else:
            rows.append(Row("no", "lines", "the server does not say it runs an act's copies once (no \"once\" in "
                                           "X-Seq-Reads): each act goes on one line, the next only when it could not "
                                           "connect; serve() runs them once"))
        if observation is not None and robot.once:
            for _ in range(LINES_ACTS):
                robot.act(observation)
            each = robot.stats()["lines"]
            body = len(robot.links[0].pack(observation).body)
            firsts = ", ".join(f"{line['bind']} {line['wins']}" for line in each)
            rows.append(Row("ok", "lines' answers", f"of {LINES_ACTS} acts sent on every line, first by {firsts}; "
                                                    f"each act sends {body:,} bytes on each line - at one act a second, "
                                                    f"{body * 3600 / 1e6:,.0f} MB an hour on each"))
    except httpx.HTTPError as e:
        rows.append(Row("no", "lines", f"{type(e).__name__}: {e}"))
    finally:
        robot.close()
    return rows


def main(argv: Optional[List[str]] = None) -> None:
    """`python -m sequence_ai.check URL [--token TOKEN] [--observation FILE]`: the module's docstring."""
    parser = argparse.ArgumentParser(prog="python -m sequence_ai.check",
                                     description="What is on, and what is not, between this machine and a policy "
                                                 "server.")
    parser.add_argument("url", help="the server, e.g. http://<gpu>:8000")
    parser.add_argument("--token", help="the server's token: sent to the address given, and nowhere else")
    parser.add_argument("--observation", help="an observation to send: msgpack, .npz or .json")
    parser.add_argument("--act-path", default="/act")
    parser.add_argument("--ping-path", default="/ping")
    parser.add_argument("--wait", type=float, default=60.0, help="seconds to wait for the server to be ready")
    parser.add_argument("--lines", help="the robot's uplinks by network interface, two or more: eth0,wwan0")
    args = parser.parse_args(argv)
    observation = _observation_from(args.observation) if args.observation else None
    rows, status = run(args.url, token=args.token, observation=observation, act_path=args.act_path,
                       ping_path=args.ping_path, wait_s=args.wait,
                       lines=[name.strip() for name in args.lines.split(",") if name.strip()] if args.lines else None)
    width = max(len(row.name) for row in rows)
    print(f"sequence-ai check: {args.url}\n")
    for row in rows:
        print(f"  {row.status:<3} {row.name:<{width}}  {row.detail}")
    raise SystemExit(status)


if __name__ == "__main__":
    main()
