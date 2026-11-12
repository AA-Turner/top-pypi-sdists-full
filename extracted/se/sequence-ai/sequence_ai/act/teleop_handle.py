"""
What connect() hands back for the name "teleop": observe() and act() as any name's, with no policy
behind them and no worker - a robot that only a person drives, costing no machine.

In one sentence: observe(x) → its Video, Depth and Tactile items encoded here, while a console watches or its Record is
on, and the step sent straight to every console connected, and kept (_core/teleop_record.py) while its Record is on →
act() → the newest chunk its person sent not yet handed back, once; `hold` with none, while it is stopped and while no
one drives it.
WHY the names of Policy's: a robot's loop goes on calling observe() and act() whichever name it holds, and which handle it
uses is its own code's to decide.
WHY nothing is encoded while no one watches or keeps it: an encoder that runs for no one costs the robot's CPU; a console
that comes later asks for the keyframe it needs (teleop_robot.Driven._keyframe), and a Record that comes on forces one.
"""
from __future__ import annotations

import threading
import time
import uuid
from typing import Any, Optional

from .._core import marked_observe as _marked
from .._core import teleop_direct as _direct
from ..errors import InvalidRequest
from .policy import _reserved_keys

_NOTHING = object()


class TeleopHandle:
    """connect("teleop")'s handle (module docstring); use it as a context manager, or close() it."""

    model = "teleop"

    def __init__(self, driven: Any, link: Any) -> None:
        self.teleop = driven
        self._link = link
        self._lock = threading.Lock()
        self._worker_episode: Optional[str] = None
        self._caller_episode: Optional[str] = None
        self._episode: Optional[str] = None
        self._numbers: dict = {}
        self._recording = False
        self._closed = False
        driven.bind(self)

    def _assert_open(self) -> None:
        if self._closed:
            raise InvalidRequest("this handle was closed: connect again")

    def _episode_for(self, episode_id: Optional[str]) -> str:
        """The episode a call goes under: the one named, this handle's current one from now on, else its current one
        (as Policy goes by it)."""
        with self._lock:
            if episode_id is not None:
                self._episode = episode_id
            elif self._episode is None:
                self._episode = uuid.uuid4().hex
            return self._episode

    def observe(self, inputs: Any, *, episode_id: Optional[str] = None) -> int:
        """One observation, as the robot makes it, straight to every console connected: its number in the episode, at
        once. `episode_id`: as Policy's."""
        self._assert_open()
        self.teleop.check()
        _reserved_keys(inputs)
        episode = self._episode_for(episode_id)
        at_us = time.time_ns() // 1000
        with self._lock:
            n = self._numbers.get(episode, 0)
            self._numbers[episode] = n + 1
        recording, watched = self._link.recording, self.teleop.watched()
        kept = recording.on
        if kept and not self._recording:
            _marked.force(self)
        self._recording = kept
        if watched or kept:
            self.teleop.frames(episode, inputs, n, at_us)
            value = inputs if kept else _direct.without_cameras(inputs)
            if _marked.holds(value):
                marks = _marked.of(self)
                value, video, _ = marks.encode(episode, value)
                marks.note(episode, n, video)
            if kept:
                recording.observed(episode, n, value, self.teleop.driver, self.teleop.by)
            self.teleop.observed(episode, n, at_us, value, self._record)
        return n

    def act(self, observation: Any = _NOTHING, *, episode_id: Optional[str] = None, seed: Optional[int] = None) -> Any:
        """What the robot plays: the newest chunk its person sent, once - a dict of arrays in the form its console sent
        it - else `hold` (connect(hold=); {} by default), the robot staying where it is. `seed` means nothing here."""
        self._assert_open()
        self.teleop.check()
        if observation is not _NOTHING:
            raise InvalidRequest("act() carries no data: every input goes through observe()")
        episode = self._episode_for(episode_id)
        with self._lock:
            n = self._numbers.get(episode, 0)
        here, out = self.teleop.answer((episode, n, self._record))
        return out if here else self.teleop.held()

    def _record(self, message: dict) -> bool:
        """What became of a chunk (teleop_robot.Driven.flush): one it played, kept while the robot's Record is on."""
        if message.get("did") == "played":
            self._link.recording.played(message)
        return True

    def label(self, success: bool, notes: str = "", *, episode_id: Optional[str] = None) -> str:
        """Record how an episode went - this handle's current one, unless `episode_id` names another - with what its
        Record keeps; nothing while it is off. Returns the episode id it labelled."""
        with self._lock:
            episode = episode_id or self._episode
        if not episode:
            raise InvalidRequest("no episode to label: observe() in one first, or pass episode_id=")
        self._link.recording.label(episode, success, notes)
        return episode

    @property
    def driver(self) -> str:
        """Who drives this robot now: "human" (a person, from their console), "stopped", or "model" - no one."""
        return self.teleop.driver

    def end_episode(self, episode_id: Optional[str] = None) -> Optional[str]:
        """End an episode - this handle's current one, unless `episode_id` names another; the next call opens a new one.
        Returns the id it ended, None when none was open."""
        with self._lock:
            episode = episode_id or self._episode
            if episode_id is None or episode == self._episode:
                self._episode = None
            if episode is not None:
                self._numbers.pop(episode, None)
        return episode

    def wait_until_ready(self, timeout_s: Optional[float] = None, poll_s: float = 5.0) -> float:
        """Until the platform has heard this robot, so a console can reach it: the seconds it took. The platform's
        refusal raised; Unavailable past `timeout_s`. `poll_s` means nothing here."""
        began = time.monotonic()
        self._link.wait_ready(timeout_s)
        self.teleop.check()
        return time.monotonic() - began

    def teleop_metrics(self) -> dict:
        """As Policy.teleop_metrics."""
        return self.teleop.metrics()

    def teleop_written(self) -> None:
        """As Policy.teleop_written."""
        self.teleop.written()

    def close(self) -> None:
        """Close this handle: the robot's consoles and its link go with the last handle of its connect."""
        if not self._closed:
            self._closed = True
            self.teleop.unbind()

    def __enter__(self) -> "TeleopHandle":
        return self

    def __exit__(self, *exc: Any) -> None:
        self.close()
