"""
Your own recorder of a robot's steps (sequence_ai.record, `seq robot record`): every step it runs, straight from the
workers that serve it, to write wherever you keep your data - the platform keeps none of it. Turn on the robot's Record,
in the console by its name or `seq robot set <name> record=on`: it says the robot's steps may be read this way, nothing
more.

In one sentence: record() asks the platform for the robot's workers (POST /v1/record/connect {"robot": its name}, with
your account's key - or the robot's own key, which reads that robot alone) → one connection to each worker's /record,
with a token that opens that robot's records alone → each worker sends every record of it it keeps from where this
recorder last was - the robot's observations, its acts and what they answered, its labels, its episodes' ends - and a
gap, how many it lost, where this recorder was away too long → steps() yields one item an act (the observations the
robot sent since its last act), one a label, one an episode's end, one a gap; the platform is asked again every
refresh_s, so the worker the robot moves to is read, and while the robot is not connected (connected false) none is,
until it connects.

What a worker keeps for you is in its memory alone: the newest minute of the steps it records (60 s), 32 MiB at most for
all its robots together - less than a minute of each where it serves several
. A recorder away longer loses the
oldest and is told how many (a "gap" item). A worker hears the Record turned on or off within a minute; turned
off, the platform answers 409 record_off and steps() ends with it. write()/read() keep the items in a file, one msgpack
map after another - what `seq robot record` writes and sequence_ai.read_record reads, the same items steps() gives.



"""
from __future__ import annotations

import logging
import queue
import threading
import time
from typing import IO, Any, Iterator, Optional

from ..errors import AuthError, Conflict, Gone, NotFound, PermissionDenied
from . import msgpack_io
from . import worker_stream as _stream
from .pinned_tls import build_pinned_ssl_context
from .worker_transport import _keepalive_options

CONNECT = "/v1/record/connect"
PATH = "/record"


_OPEN_S = 10.0
_REFRESH_S = 10.0
_log = logging.getLogger("sequence_ai.record")


class _Feed:
    """One worker's connection, and where this recorder is in its records."""

    def __init__(self, entry: dict, *, at_start: bool) -> None:
        self.label = str(entry.get("worker") or "")
        self.entry = entry
        self.after: Optional[int] = None
        self.at_start = at_start
        self.stream = None
        self.listed = True
        self.done = False
        self.refused = False


class Recorder:
    """A recorder of one robot's steps (module docstring) - from sequence_ai.record(), not made directly. Use it as a
    context manager, or close() it. `robot` its name as the platform says it; `connected` whether the robot was
    connected at the platform's newest answer, and `teleop_only` whether to teleop alone then - which no worker serves,
    so none of its steps come here: its own SDK writes them to a file on its machine (teleop_record)."""

    def __init__(self, gateway: Any, robot: Optional[str], *, timeout_s: float = _OPEN_S) -> None:
        self.robot = robot
        self.connected = False
        self.teleop_only = False
        self._gateway = gateway
        self._timeout_s = timeout_s
        self._lock = threading.Lock()
        self._raw: queue.Queue = queue.Queue()
        self._feeds: dict[str, _Feed] = {}
        self._opening = threading.Lock()
        self._closed = threading.Event()
        self._failed: Optional[BaseException] = None
        self._refresh_s = _REFRESH_S


        self._options = _keepalive_options()
        self.dropped = 0
        answer = self._ask()
        self._take(answer, at_start=True)
        self._thread = threading.Thread(target=self._keep, daemon=True, name="seq-record")
        self._thread.start()


    def _ask(self) -> dict:
        return self._gateway.post(CONNECT, {"robot": self.robot} if self.robot else {}) or {}

    def _take(self, answer: dict, *, at_start: bool = False) -> None:
        listed = {str(w.get("worker")): w for w in answer.get("workers") or [] if w.get("worker")}
        with self._lock:
            self.robot = str(answer.get("robot") or self.robot or "") or None
            self.connected = bool(answer.get("connected", bool(listed)))
            self.teleop_only = bool(answer.get("teleop_only"))
            self._refresh_s = float(answer.get("refresh_s") or _REFRESH_S)
            for label, entry in listed.items():
                feed = self._feeds.get(label)
                if feed is None:
                    self._feeds[label] = _Feed(entry, at_start=at_start)
                else:
                    feed.entry, feed.listed = entry, True
            for label, feed in list(self._feeds.items()):
                if label not in listed:
                    feed.listed = False
        self._open_all(refresh=True)

    def _open_all(self, *, refresh: bool = False) -> None:
        """A connection to each worker listed with none open, from where this recorder was; a worker no longer listed
        whose connection ended is let go - said as a gap where it ended while this recorder was away from it. One that
        said record is off there, or that it stops serving, is tried again at a refresh alone: never at once, in a loop
        of openings it would turn away."""
        with self._opening:
            with self._lock:
                feeds = list(self._feeds.values())
            for feed in feeds:
                alive = feed.stream is not None and feed.stream.alive
                if alive or self._closed.is_set():
                    continue
                if not feed.listed:
                    with self._lock:
                        self._feeds.pop(feed.label, None)
                    if not feed.done:
                        self._raw.put((feed.label, {"t": "gap", "count": None,
                                                    "why": "the worker ended while this recorder was not reading it: "
                                                           "what it kept after the last record read is not known"}))
                    continue
                if refresh or not (feed.done or feed.refused):
                    self._open(feed)

    def _open(self, feed: _Feed) -> None:
        entry = feed.entry
        feed.refused = False
        path = PATH if feed.after is None else f"{PATH}?after={feed.after}"
        try:
            feed.stream = _stream.open_stream(
                entry["worker_url"], build_pinned_ssl_context(entry.get("cert_fingerprint")),
                {"Authorization": f"Bearer {entry['token']}"}, timeout_s=self._timeout_s, path=path,
                options=self._options, on_push=lambda record, label=feed.label: self._said(label, record),
                on_end=lambda why, label=feed.label: self._ended(label, why))
        except Exception as exc:
            _log.warning("worker %s of %s not reached: %s", feed.label, self.robot, exc)
            feed.stream = None

    def _said(self, label: str, record: dict) -> None:
        """A record of one worker's, on its connection's thread: kept in its order, its number noted."""
        n, kind, feed = record.get("n"), record.get("t"), self._feeds.get(label)
        if feed is not None:
            if isinstance(n, int):
                feed.after, feed.done = n, False
            elif kind == "gap" and isinstance(record.get("next"), int):
                feed.after = record["next"] - 1
            elif kind == "bye":
                feed.done = True
            elif kind == "refused":
                feed.refused = True
        self._raw.put((label, record))

    def _ended(self, label: str, why: str) -> None:
        if not self._closed.is_set():
            _log.info("worker %s of %s: its connection ended (%s); read again from where it was", label, self.robot,
                      why)
            self._raw.put((label, {"t": "_ended"}))

    def _keep(self) -> None:
        while not self._closed.wait(self._refresh_s):
            try:
                self._take(self._ask())
            except (AuthError, PermissionDenied, NotFound, Conflict, Gone) as exc:
                self._failed = exc
                self._raw.put((None, {"t": "_failed"}))
                return
            except Exception as exc:
                _log.warning("the platform's answer for %s did not come: %s; asked again", self.robot, exc)


    def steps(self) -> Iterator[dict]:
        """Every step of the robot as it comes, one dict an item, `kind` saying which:

            "step"   one act: {"robot" (its name), "session", "episode", "step",
                     "observations": [[step, observation], ...] - each the robot sent since its last act, as it sent
                     it (a Video, Depth or Tactile item as its map, never decoded) - "action" (what the act answered),
                     "params" (the inference parameters it ran with), "driver" ("model", or "human" through teleop,
                     with "operator"), "path" (the way its action reached the robot: "worker", or "direct" - a person's
                     chunk sent straight from their console), "at" (the epoch second its worker had it), "worker", "n"
                     (the worker's number of it); a person's chunk the robot said what became of also "did" - "played",
                     or why it never was: "superseded" (a newer one came before any act took it), "old", "stale",
                     "not_driving" - and "command" (its "id", "sent_us" by its console's clock, "ref_us" and "ref_n"
                     the step it was made from, "got_us" and "played_us" by the robot's, in microseconds)}
            "label"  how a robot said its episode went (policy.label): {"robot", "episode", "success", "notes", "at"}
            "end"    a robot ended its episode: {"robot", "episode", "at", "observations": those after its last act}
            "driver" who drives a robot from now, through teleop: {"robot", "episode", "driver" ("model", "human" or
                     "stopped"), "by" (the operator's name), "event" ("take", "release", "stop" or "timeout"), "at"}
            "help"   a robot's plan asked for a person (seq.ask_human): {"robot", "episode", "id", "reason", "hold",
                     "asked_at", "frame" (its newest frame as a JPEG, or None)}
            "gap"    a worker let records go before this recorder read them: {"worker", "count" (None when it cannot be
                     told: the worker ended), "why"} - or, its "count" None, steps of an episode that came to its worker
                     while its Record was not on there yet (it comes on within a minute of being turned on), never
                     recorded: {"robot", "session", "episode", "observations" and "acts" (the [first, last] steps of
                     each that came then, None for none), "at", "worker", "n", "why"}, before that episode's first item

        Every item but a worker's gap says its worker and that worker's number of it ("worker", "n"): a recorder
        started again reads what each worker still keeps - its newest minute at most - again, and those two tell which
        it had.
        Ends at close(); raises what the platform refused it with (its Record turned off: Conflict, details.reason
        "record_off"; the key revoked; the robot gone)."""
        pending: dict = {}
        while True:
            label, record = self._raw.get()
            kind = record.get("t")
            if kind == "_closed":
                return
            if kind == "_failed":
                raise self._failed
            if kind == "_ended":
                if not self._closed.is_set():
                    self._open_all()
                continue
            if kind == "gap":
                if isinstance(record.get("count"), int):
                    self.dropped += record["count"]
                item = {"kind": "gap", "worker": label, "count": record.get("count"),
                        "why": record.get("why") or "the worker let them go before this recorder read them: it keeps "
                                                    "the newest minute of what it records, 32 MiB at most for all its "
                                                    "robots"}
                if "episode" in record:
                    item.update({"robot": self.robot, "session": record.get("session"), "episode": record["episode"],
                                 "observations": record.get("observations"), "acts": record.get("acts"),
                                 "at": record.get("at"), "n": record.get("n")})
                yield item
                continue
            if kind == "hello":
                feed = self._feeds.get(label)
                first = record.get("first")
                if feed is not None and not feed.at_start and feed.after is None and isinstance(first, int) \
                        and first > 1:
                    self.dropped += first - 1
                    yield {"kind": "gap", "worker": label, "count": first - 1,
                           "why": "the worker kept them for a minute and this recorder reached it after"}
                continue
            if kind not in ("observe", "act", "label", "end", "driver", "help"):
                continue
            session, episode = record.get("session"), record.get("episode")
            if kind == "observe":
                pending.setdefault(episode, []).append([record.get("step"), record.get("observation")])
                continue
            base = {"robot": self.robot, "session": session, "episode": episode,
                    "at": record.get("at"), "worker": label, "n": record.get("n")}
            if kind == "act":
                seen = pending.pop(episode, []) if record.get("driver") != "human" else []
                if "observation" in record:
                    seen.append([record.get("step"), record["observation"]])
                yield {"kind": "step", **base, "step": record.get("step"), "observations": seen,
                       "action": record.get("action"), "params": record.get("params"),
                       "driver": record.get("driver") or "model",

                       "path": record.get("path") or "worker",
                       **({"operator": record["operator"]} if record.get("operator") else {}),

                       **{k: record[k] for k in ("did", "command") if record.get(k) is not None}}
            elif kind == "label":
                yield {"kind": "label", **base, "success": record.get("success"), "notes": record.get("notes")}
            elif kind == "driver":
                yield {"kind": "driver", **base, "driver": record.get("driver"), "by": record.get("by"),
                       "event": record.get("event")}
            elif kind == "help":
                yield {"kind": "help", **base, "id": record.get("id"), "reason": record.get("reason"),
                       "hold": record.get("hold"), "asked_at": record.get("asked_at"), "frame": record.get("frame")}
            else:
                yield {"kind": "end", **base, "observations": pending.pop(episode, [])}

    @property
    def workers(self) -> list[str]:
        """The workers this recorder reads now, by their names (a0001)."""
        with self._lock:
            return [label for label, feed in self._feeds.items() if feed.stream is not None and feed.stream.alive]

    def close(self) -> None:
        """Stop reading: every worker's connection closed, steps() ended."""
        if self._closed.is_set():
            return
        self._closed.set()
        with self._lock:
            feeds = list(self._feeds.values())
        for feed in feeds:
            if feed.stream is not None:
                try:
                    feed.stream.close("the recorder closed")
                except Exception:
                    pass
        self._raw.put((None, {"t": "_closed"}))
        try:
            self._gateway.close()
        except Exception:
            pass

    def __enter__(self) -> "Recorder":
        return self

    def __exit__(self, *exc: Any) -> None:
        self.close()



FORMAT = 1
_READ_CHUNK = 4 * 1024 * 1024
_ITEM_MOST = 1024 * 1024 * 1024


def header(robot: Optional[str]) -> dict:
    """A recording file's first map: what it is, its format, its robot, and when it began (epoch seconds)."""
    return {"kind": "recording", "format": FORMAT, "robot": robot, "began_at": time.time()}


def write(out: IO[bytes], item: dict) -> int:
    """`item` - the header, or an item as steps() gave it - at the end of a recording file, one msgpack map after
    another, as any msgpack reader reads them; the bytes written."""
    data = msgpack_io.pack(item)
    out.write(data)
    return len(data)


def read(path: str) -> Iterator[dict]:
    """The items of a recording file, in order, as steps() gave them: its header (its first map, "kind" "recording")
    checked, not given. Read a chunk at a time: an item that does not read whole from what is read so far is read on,
    twice as much each time it still does not - so an item of any size is read once more, not once a chunk - and only at
    the file's end is one that never does said: MsgpackError, for a file cut short inside an item (a recorder stopped as
    it wrote: those before it are given first) or no recording at all."""
    with open(path, "rb") as f:
        buf, first, end, want = b"", True, False, _READ_CHUNK
        while True:
            at, short = 0, False
            view = memoryview(buf)
            while at < len(buf):
                try:
                    value, at_next = msgpack_io._Reader(view).read(at, 0)
                except msgpack_io.MsgpackError:
                    if end:
                        raise
                    short = True
                    break
                at = at_next
                if first:
                    first = False
                    if not (isinstance(value, dict) and value.get("kind") == "recording"):
                        raise msgpack_io.MsgpackError(f"{path} is no recording: it begins with no header")
                    continue
                yield value
            buf = buf[at:]
            if end:
                return
            if len(buf) > _ITEM_MOST:
                raise msgpack_io.MsgpackError(f"{path} holds no whole item in {_ITEM_MOST} bytes: it is no recording "
                                              "past here")
            want = want * 2 if short and at == 0 else _READ_CHUNK
            chunk = f.read(want)
            end = not chunk
            if end and not buf:
                return
            buf += chunk
