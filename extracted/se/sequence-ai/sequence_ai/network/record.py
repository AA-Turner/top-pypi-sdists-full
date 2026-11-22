# SPDX-FileCopyrightText: Copyright (c) 2026 General Sequences Company
# SPDX-License-Identifier: Apache-2.0
"""
Your own recorder of the robots' steps on a policy server of your own: every observation a robot streams to it and every
act and what it answered, as they come (serve()'s GET /record, engine.recorder), to keep where you keep your data. The
server keeps the last minute in memory and writes nothing to its disk.

    from sequence_ai.network import record

    with record.connect("http://your-gpu:8000") as recorder:              # token=..., robot=... where needed
        for item in recorder:                                              # {"t": "observe" | "act" | "gap", ...}
            ...
    record.save("http://your-gpu:8000", "run.rec", seconds=60)            # the same, into a file
    record.video("run.rec", "head", "head.mp4")                           # one camera's video, playable, as it was sent

    python -m sequence_ai.network.record http://your-gpu:8000 run.rec [--seconds 60] [--robot ID] [--token T]

In one sentence: connect() opens one WebSocket to the server's GET /record (the token on it), from the record after the
last one this recorder had where it is given one → the server sends {"t": "hello"} and then each record as it comes, a
gap where its window let some go first → each is a dict as msgpack reads it: an observation as the robot sent it - a
sequence_ai.Video item still the map of its H.264 access unit - or an act with its answer → save() writes them to a file
one msgpack map after another, behind a header (the format sequence_ai.read_record reads), and video() takes one
camera's access units from a file, in order, into an MP4 container without encoding them again.

WHY the video as it was sent: it plays as it is, a few KB a frame, the same pictures the policy was handed; turned back
into arrays, a minute of two cameras would be gigabytes.

The WebSocket is sequence_ai/_core/worker_stream.py's, the one a robot's stream runs on; video() needs PyAV
(sequence-ai installs it on Python 3.10 or later).
"""
from __future__ import annotations

import argparse
import queue
import ssl
import sys
import threading
import time
from fractions import Fraction
from typing import Any, Iterator, Optional
from urllib.parse import quote, urlsplit

__all__ = ["Recorder", "connect", "items", "save", "video"]

PATH = "/record"
OPEN_S = 10.0


class Recorder:
    """One recorder's connection to a server's GET /record (the module's docstring): iterate it for each record as it
    comes; `last` is the number of the last one read, `dropped` how many the server's window let go before they were
    read. Use it as a context manager, or close() it."""

    def __init__(self, url: str, *, token: Optional[str] = None, robot: Optional[str] = None,
                 after: Optional[int] = None, timeout_s: float = OPEN_S) -> None:
        from .._core import worker_stream

        self._ws_mod = worker_stream
        self._items: queue.Queue = queue.Queue()
        self._ended = threading.Event()
        self.last: Optional[int] = None
        self.dropped = 0
        headers = {"Authorization": f"Bearer {token}"} if token else {}
        query = [f"after={int(after)}"] if after is not None else []
        if robot:
            query.append(f"robot={quote(robot)}")
        path = PATH + ("?" + "&".join(query) if query else "")
        context = ssl.create_default_context() if urlsplit(url).scheme == "https" else None
        sock, said, rest = worker_stream.open_websocket(url.rstrip("/"), context, headers, timeout_s=timeout_s,
                                                        path=path)
        self._stream = worker_stream.WorkerStream(sock, said, rest, on_push=self._items.put, on_end=self._end)

    def _end(self, why: str) -> None:
        self._ended.set()
        self._items.put(None)

    def __iter__(self) -> Iterator[dict]:
        """Each record as it comes - {"t": "observe" | "act" | "gap", ...}; the server's hello is not one - until the
        connection ends or close() is called."""
        while True:
            item = self._items.get()
            if item is None:
                return
            kind = item.get("t")
            if kind == "hello":
                continue
            if kind == "gap":
                self.dropped += int(item.get("count") or 0)
            if isinstance(item.get("n"), int):
                self.last = item["n"]
            yield item

    def get(self, timeout_s: float) -> Optional[dict]:
        """The next record, waited for `timeout_s` at most: None when none came by then, or the connection ended."""
        while True:
            try:
                item = self._items.get(timeout=timeout_s)
            except queue.Empty:
                return None
            if item is None:
                self._items.put(None)
                return None
            if item.get("t") == "hello":
                continue
            if item.get("t") == "gap":
                self.dropped += int(item.get("count") or 0)
            if isinstance(item.get("n"), int):
                self.last = item["n"]
            return item

    def close(self) -> None:
        """Close the connection: iterating it ends."""
        self._stream.close()
        self._items.put(None)

    def __enter__(self) -> "Recorder":
        return self

    def __exit__(self, *exc: Any) -> None:
        self.close()


def connect(url: str, *, token: Optional[str] = None, robot: Optional[str] = None,
            after: Optional[int] = None) -> Recorder:
    """A Recorder of the server at `url`: every robot's records, or `robot`'s alone; from the record after `after` (the
    `last` of a recorder before), else from the oldest the server keeps."""
    return Recorder(url, token=token, robot=robot, after=after)


def save(url: str, path: str, *, seconds: Optional[float] = None, token: Optional[str] = None,
         robot: Optional[str] = None) -> int:
    """Record the server at `url` into the file at `path` - for `seconds`, or until the connection ends (Ctrl-C stops
    it): one msgpack map after another behind a header, as sequence_ai.read_record reads them. The records written."""
    from .._core import recorder as _file

    written = 0
    end = None if seconds is None else time.monotonic() + seconds
    with connect(url, token=token, robot=robot) as recorder, open(path, "wb") as out:
        _file.write(out, _file.header(robot))
        try:
            while end is None or time.monotonic() < end:
                item = recorder.get(0.5 if end is None else max(0.0, min(0.5, end - time.monotonic())))
                if item is None:
                    if recorder._ended.is_set():
                        break
                    continue
                _file.write(out, item)
                written += 1
        except KeyboardInterrupt:
            pass
    return written


def items(path: str) -> Iterator[dict]:
    """The records of a file save() wrote, in order (sequence_ai.read_record reads the same)."""
    from .._core import recorder as _file

    yield from _file.read(path)


def video(path: str, key: str, out: str, *, robot: Optional[str] = None, fps: float = 15.0) -> int:
    """One camera's video from a file save() wrote - the sequence_ai.Video item under `key` (a top-level key of the
    observation, or a path with dots: "cams.head") of `robot`'s observations, or of every robot's when it streamed
    alone - into an MP4 at `out`, its access units as they were sent, timed `fps` frames a second. Frames before its
    first keyframe, which nothing decodes, are left out. The frames written."""
    try:
        import av
    except ImportError:
        raise ImportError("video() writes an MP4 with PyAV: pip install -U sequence-ai, on Python 3.10 or later "
                          "(3.11 or later on Windows on ARM)") from None
    import io

    units = []
    for item in items(path):
        if item.get("t") != "observe" or (robot is not None and item.get("robot") != robot):
            continue
        value: Any = item.get("observation")
        for part in key.split("."):
            value = value.get(part) if isinstance(value, dict) else None
        if isinstance(value, dict) and value.get("codec") == "h264":
            if not units and not value.get("kf"):
                continue
            units.append(bytes(value["data"]))
    if not units:
        return 0
    source = av.open(io.BytesIO(b"".join(units)), format="h264")
    written = 0
    with av.open(out, "w", format="mp4") as sink:
        made = getattr(sink, "add_stream_from_template", None)     # PyAV 17 on; add_stream(template=) before
        stream = made(source.streams.video[0]) if made else sink.add_stream(template=source.streams.video[0])
        stream.time_base = Fraction(1, 90000)
        step = int(90000 / fps)
        for packet in source.demux(source.streams.video[0]):
            if packet.size == 0:
                continue
            packet.stream = stream
            packet.pts = packet.dts = written * step
            packet.time_base = stream.time_base
            sink.mux(packet)
            written += 1
    source.close()
    return written


def _main(argv: Optional[list] = None) -> int:
    ap = argparse.ArgumentParser(prog="python -m sequence_ai.network.record",
                                 description="Record a policy server's robot steps into a file.")
    ap.add_argument("url")
    ap.add_argument("path")
    ap.add_argument("--seconds", type=float, default=None, help="stop after this long (default: until Ctrl-C)")
    ap.add_argument("--robot", default=None, help="one robot's records alone")
    ap.add_argument("--token", default=None, help="the server's token, where it asks for one")
    a = ap.parse_args(argv)
    n = save(a.url, a.path, seconds=a.seconds, token=a.token, robot=a.robot)
    print(f"{n} records written to {a.path}", file=sys.stderr)
    return 0


if __name__ == "__main__":
    sys.exit(_main())
