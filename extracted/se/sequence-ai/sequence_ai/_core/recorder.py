"""
Your own recorder of a policy's steps (sequence_ai.record): every step each of its robots runs, straight from the
workers that served them, to write wherever you keep your data - the platform keeps none of it. Turn it on with
`seq policy set <name> record=on`; it is apart from capture, which is the platform keeping your episodes.

In one sentence: record() asks the platform for the policy's workers (POST /v1/record/connect, with a record key of the
policy - `seq record add --policy <name>`) → one connection to each worker's /record, with a token that opens that
alone → each worker sends every record it keeps from where this recorder last was - a robot's observations, its acts
and what they answered, its labels, its episodes' ends - and a gap, how many it lost, where it was away too long →
steps() yields one item an act (the observations its robot sent since its last act with it), one a label, one an
episode's end, one a gap; the platform is asked again every refresh_s, so a worker started since is read and a gone one
let go.

What a worker keeps for you is in its memory alone, its newest minute (60 s, 32 MiB at most): a recorder away longer
loses the oldest and is told how many (a "gap" item). One that must have no gap keeps capture on as well.


"""
from __future__ import annotations

import logging
import queue
import threading
import time
from typing import Any, Iterator, Optional

from ..errors import AuthError, Conflict, NotFound, PermissionDenied
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
    """A recorder of one policy's steps (module docstring) - from sequence_ai.record(), not made directly. Use it as a
    context manager, or close() it."""

    def __init__(self, gateway: Any, policy: str, *, timeout_s: float = _OPEN_S) -> None:
        self.policy = policy
        self._gateway = gateway
        self._timeout_s = timeout_s
        self._lock = threading.Lock()
        self._raw: queue.Queue = queue.Queue()
        self._feeds: dict[str, _Feed] = {}
        self._robots: dict[str, str] = {}
        self._asked: set = set()
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
        return self._gateway.post(CONNECT, {"policy": self.policy}) or {}

    def _take(self, answer: dict, *, at_start: bool = False) -> None:
        listed = {str(w.get("worker")): w for w in answer.get("workers") or [] if w.get("worker")}
        with self._lock:
            self._robots.update(answer.get("robots") or {})
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
            _log.warning("worker %s of %s not reached: %s", feed.label, self.policy, exc)
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
            _log.info("worker %s of %s: its connection ended (%s); read again from where it was", label, self.policy,
                      why)
            self._raw.put((label, {"t": "_ended"}))

    def _keep(self) -> None:
        while not self._closed.wait(self._refresh_s):
            try:
                self._take(self._ask())
            except (AuthError, PermissionDenied, NotFound, Conflict) as exc:
                self._failed = exc
                self._raw.put((None, {"t": "_failed"}))
                return
            except Exception as exc:
                _log.warning("the platform's answer for %s did not come: %s; asked again", self.policy, exc)


    def steps(self) -> Iterator[dict]:
        """Every step of the policy's robots as it comes, one dict an item, `kind` saying which:

            "step"   one act: {"robot", "robot_key", "session", "episode", "step", "observations": [[step,
                     observation], ...] - each its robot sent since its last act, as it sent it (a Video, Depth or
                     Tactile item as its map, never decoded) - "action" (what the act answered), "params" (the inference
                     parameters it ran with), "driver" ("model", or "human" through teleop, with "operator"), "at"
                     (the epoch second its worker had it), "worker", "n" (the worker's number of it)}
            "label"  how a robot said its episode went (policy.label): {"robot", "episode", "success", "notes", "at"}
            "end"    a robot ended its episode: {"robot", "episode", "at", "observations": those after its last act}
            "driver" who drives a robot from now, through teleop: {"robot", "episode", "driver" ("model", "human" or
                     "stopped"), "by" (the operator's name), "event" ("take", "release", "stop" or "timeout"), "at"}
            "help"   a robot's plan asked for a person (seq.ask_human): {"robot", "episode", "id", "reason", "hold",
                     "asked_at", "frame" (its newest frame as a JPEG, or None)}
            "gap"    a worker let records go before this recorder read them: {"worker", "count" (None when it cannot be
                     told: the worker ended), "why"}

        Every item but a gap says its worker and that worker's number of it ("worker", "n"): a recorder started again
        reads what each worker still keeps - its newest minute - again, and those two tell which it had. Ends at close();
        raises what the platform refused it with (record turned off, the key revoked)."""
        pending: dict = {}
        robots_of: dict = {}
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
                yield {"kind": "gap", "worker": label, "count": record.get("count"),
                       "why": record.get("why") or "the worker let them go before this recorder read them: it keeps "
                                                   "its newest minute"}
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
            if record.get("robot"):
                robots_of[session] = record["robot"]
            key = record.get("robot") or robots_of.get(session)
            if kind == "observe":
                pending.setdefault(episode, []).append([record.get("step"), record.get("observation")])
                continue
            base = {"robot": self._name(key), "robot_key": key, "session": session, "episode": episode,
                    "at": record.get("at"), "worker": label, "n": record.get("n")}
            if kind == "act":
                seen = pending.pop(episode, []) if record.get("driver") != "human" else []
                if "observation" in record:
                    seen.append([record.get("step"), record["observation"]])
                yield {"kind": "step", **base, "step": record.get("step"), "observations": seen,
                       "action": record.get("action"), "params": record.get("params"),
                       "driver": record.get("driver") or "model",
                       **({"operator": record["operator"]} if record.get("operator") else {})}
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

    def _name(self, key: Optional[str]) -> Optional[str]:
        if not key:
            return None
        with self._lock:
            name = self._robots.get(key)
        if name is None and key not in self._asked:
            self._asked.add(key)
            try:
                self._take(self._ask())
            except Exception:
                pass
            with self._lock:
                name = self._robots.get(key)
        return name

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
