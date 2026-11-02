"""
What a robot connected with teleop=True holds of who drives it: its worker pushes who drives and
a person's action chunks on the robot's stream, and act() answers from them here,
waiting for no network while a person drives it or it is stopped.

In one sentence: connect(..., teleop=True) → the robot's stream opens saying so (X-Seq-Teleop: 1) → its worker pushes
{"t": "driver"} as it opens and at each change, and {"t": "chunk"} for each chunk the person who drives it sends → act()
while its model drives goes to its worker as ever; while a person drives, it hands back the newest chunk not yet handed
back - once: with none newer, it is `hold`, the robot staying where it is; while stopped, `hold` → the stream ending
while a person drives it or it is stopped stops it here, and its next stream says so (X-Seq-Teleop: stopped), which a
worker new to it - one a move took it to - keeps until a console releases it.
WHY once: what an answer means is the policy's own - a dict of arrays, a list - so the SDK cannot take the steps a robot
played off it; handed back twice, a chunk's first steps would be played again.

WHY `hold` is by default the model's last answer emptied (each array's first axis cut to nothing, each list empty): a
loop that plays out["actions"] plays nothing and stays where it is, its code and act()'s answer's form unchanged; {} before
any. {the user 10-27: "just dot he way that is most cofirtable to teleoperator but not changing the act"}
WHY an act's answer is held to who drove as it went (after): a stop, or a person's taking the robot, while an act is on
its way reaches the robot first - its worker pushes it ahead of the answer, on the same stream - and the answer that
comes after it is no one's: act() hands back a person's chunk or `hold` in its place, a release since included, as it
would have answered the act asked a moment later.

"""
from __future__ import annotations

import threading
from typing import Any, Optional


HEADER = "X-Seq-Teleop"
DRIVERS = ("model", "human", "stopped")
_EMPTY = object()


def emptied(value: Any) -> Any:
    """`value` with nothing in it, in its own form: a dict's every value emptied, a list or tuple empty, an array cut to
    none along its first axis; anything else None."""
    if isinstance(value, dict):
        return {k: emptied(v) for k, v in value.items()}
    if isinstance(value, (list, tuple)):
        return type(value)() if type(value) in (list, tuple) else []
    shape = getattr(value, "shape", None)
    if isinstance(shape, tuple) and len(shape) >= 1:
        try:
            return value[:0]
        except Exception:
            return None
    return None


class Driven:
    """A teleop robot's say of who drives it (module docstring), kept across its worker connections: what its stream's
    pushes said (push), the stream's end (ended), act()'s answer here (answer), the model's last answer (answered), and
    what of an act's answer act() hands back, for who drove as it went (after)."""

    def __init__(self, hold: Any = _EMPTY) -> None:
        self._lock = threading.Lock()
        self.driver = "model"
        self.by: Optional[str] = None
        self._chunk: Any = None
        self._fresh = False
        self._hold = hold
        self._last: Any = _EMPTY
        self.chunks = 0
        self.changes = 0

    @property
    def said(self) -> str:
        """What the robot's next stream says (HEADER): "stopped" while it holds itself stopped, else "1"."""
        return "1" if self.driver == "model" else "stopped"

    def push(self, message: dict) -> None:
        """A message its worker pushed on its stream (WorkerStream on_push, the stream's thread)."""
        kind = message.get("t")
        with self._lock:
            if kind == "driver":
                driver = message.get("driver")
                driver = driver if driver in DRIVERS else "stopped"
                self.changes += driver != self.driver
                self.driver = driver
                self.by = message.get("by")
                self._chunk, self._fresh = None, False
            elif kind == "chunk" and self.driver == "human":
                self._chunk, self._fresh = message.get("chunk"), True

    def ended(self, why: str) -> None:
        """Its stream ended (WorkerStream on_end): a robot a person drove, or stopped, is stopped here until a worker
        says otherwise - no chunk can come."""
        with self._lock:
            if self.driver != "model":
                self.changes += self.driver != "stopped"
                self.driver, self.by = "stopped", None
                self._chunk, self._fresh = None, False

    def answer(self) -> tuple:
        """(whether act() answers here, what): its model's - (False, None) - else a person's newest chunk not handed
        back yet, or `hold`."""
        with self._lock:
            return self._answer()

    def after(self, asked: int) -> tuple:
        """What act() hands back of its model's answer to an act that went at `asked` (`changes` as it went), as
        answer() says it: (False, None) - the answer - while its model drove all along; else a person's newest chunk not
        handed back yet, or `hold` - `hold` too once its model drives again: that answer was asked before a stop, or a
        person's taking it, and is no one's."""
        with self._lock:
            if self.changes == asked:
                return False, None
            here, out = self._answer()
            return True, out if here else self._held()

    def _answer(self) -> tuple:
        """answer(), under the lock."""
        if self.driver == "model":
            return False, None
        if self.driver == "human" and self._fresh:
            self._fresh = False
            self.chunks += 1
            return True, self._chunk
        return True, self._held()

    def _held(self) -> Any:
        """`hold`, under the lock: the one given, else the model's last answer emptied - {} before any."""
        if self._hold is not _EMPTY:
            return self._hold
        return {} if self._last is _EMPTY else emptied(self._last)

    def answered(self, outputs: Any) -> None:
        """Its model's answer to an act: what the default hold is made from."""
        with self._lock:
            self._last = outputs
