"""
What a robot connected to "teleop" alone keeps while its Record is on: no worker sees its steps, so it writes them itself,
to a file on the machine it runs on - the file `seq robot record` writes (sequence_ai._core.recorder: a header, then one
msgpack map an item), which sequence_ai.read_record reads back. The platform keeps none of it.

In one sentence: its link says whether its Record is on (settings.record) and the robot's name (settings.robot) → on, a
file is opened in $SEQUENCES_RECORD_DIR, else the folder the robot runs in: <robot>-<when>.msgpack → each observation it
makes is an "observe" item, each chunk of a person's it played a "step", each label a "label" - packed as they come and
handed to a writer thread through a bounded queue → turned off, or as its connect closes, what waits is written and the
file closed; turned on again, a new file.
WHY "observe" items: no worker joins a teleop robot's observations to its acts, as one does a policy's (Recorder.steps):
each is kept as it was made, the step after it what was played.
WHY packed as they come: a robot may reuse an array it observed with; what is written is what it observed then.
WHY a thread and a bound: a write never slows the robot's loop - a disk behind its cameras drops items, counted and said.


WHY a person's played chunks alone: a chunk never played is no step the robot took.



"""
from __future__ import annotations

import logging
import os
import queue
import threading
import time
from typing import IO, Any, Optional

from sequence_ai._core import msgpack_io, recorder

FOLDER_ENV = "SEQUENCES_RECORD_DIR"
QUEUE_MOST = 1024
_SAY_DROPS_S = 10.0
_CLOSE_S = 60.0
_log = logging.getLogger("sequence_ai.teleop")


class Recording:
    """One connect()'s recording (module docstring). `path` the file being written while one is; `written` and `dropped`
    the items each so far."""

    def __init__(self, folder: Optional[str] = None) -> None:
        self._lock = threading.Lock()
        self.on = False
        self.robot: Optional[str] = None
        self._folder = folder
        self._queue: queue.Queue = queue.Queue(maxsize=QUEUE_MOST)
        self._writer: Optional[threading.Thread] = None
        self.path: Optional[str] = None
        self._where: Optional[str] = None
        self.written = 0
        self.dropped = 0
        self._said_drops = 0.0

    def configure(self, on: Any, robot: Any = None) -> None:
        """What a round of its link says: whether its Record is on, and the robot's name. On, a file is opened; off, the
        one open is finished and closed."""
        on = bool(on)
        with self._lock:
            if isinstance(robot, str) and robot:
                self.robot = robot
            if on == self.on:
                return
            if self._writer is None or not self._writer.is_alive():
                self._writer = threading.Thread(target=self._write, daemon=True, name="seq-teleop-record")
                self._writer.start()
            if not on:
                self.on = False

        self._queue.put(("open" if on else "shut", None))
        if on:
            with self._lock:
                self.on = True

    def observed(self, episode: str, step: int, observation: Any, driver: str, by: Optional[str]) -> None:
        """One step it observed, as it goes: its Video, Depth and Tactile items already their encoders' maps."""
        self._push({"kind": "observe", "robot": self.robot, "episode": episode, "step": step, "observation": observation,
                    "driver": driver, **({"operator": by} if by else {}), "at": time.time()})

    def played(self, said: dict) -> None:
        """A person's chunk the robot played (teleop_robot.Driven's say of it): a step, as Recorder.steps() says one, its
        observations those before it in the file."""
        self._push({"kind": "step", "robot": self.robot, "episode": said.get("episode"), "step": said.get("step"),
                    "observations": [], "action": said.get("chunk"), "params": None, "driver": "human",
                    **({"operator": said["by"]} if said.get("by") else {}), "path": "direct", "did": "played",
                    "at": time.time()})

    def executed(self, episode: Any, step: Any, action: Any) -> None:
        """What the robot's code wrote to its motors of the chunk it played at `step` (TeleopHandle.teleop_written's
        `executed`): the action it took, beside the person's own inputs that step's item keeps."""
        self._push({"kind": "executed", "robot": self.robot, "episode": episode, "step": step, "action": action,
                    "at": time.time()})

    def label(self, episode: str, success: bool, notes: str) -> None:
        """How the robot said its episode went."""
        self._push({"kind": "label", "robot": self.robot, "episode": episode, "success": bool(success), "notes": notes,
                    "at": time.time()})

    def _push(self, item: dict) -> None:
        if not self.on:
            return
        try:
            data = msgpack_io.pack(item)
            self._queue.put_nowait(("item", data))
            return
        except queue.Full:
            why = "its disk is behind its cameras"
        except msgpack_io.MsgpackError as exc:
            why = f"an item msgpack cannot carry ({exc})"
        say = None
        with self._lock:
            self.dropped += 1
            now = time.monotonic()
            if now - self._said_drops >= _SAY_DROPS_S:
                self._said_drops, say = now, self.dropped
        if say is not None:
            _log.warning("this robot's recording is dropping items - %s; dropped so far: %d", why, say)

    def _open(self) -> IO[bytes]:
        """A new file for its steps, in its folder, never one there already, its header first."""
        folder = self._folder or os.environ.get(FOLDER_ENV) or os.getcwd()
        self._where = folder
        os.makedirs(folder, exist_ok=True)
        stem = os.path.join(folder, f"{self.robot or 'teleop'}-{time.strftime('%Y%m%d-%H%M%S')}")
        n = 1
        while True:
            path = f"{stem}.msgpack" if n == 1 else f"{stem}-{n}.msgpack"
            try:
                f = open(path, "xb")
                break
            except FileExistsError:
                n += 1
        recorder.write(f, {**recorder.header(self.robot), "source": "teleop"})
        f.flush()
        self.path = path
        _log.info("this robot's Record is on: its steps go to %s", path)
        return f

    def _write(self) -> None:
        """The writer: each item into the open file, as it comes; a file opened as Record comes on and closed as it goes
        off, or as the connect closes ("end")."""
        f: Optional[IO[bytes]] = None
        while True:
            what, data = self._queue.get()
            try:
                if what == "open" and f is None:
                    f = self._open()
                elif what == "item" and f is not None:
                    f.write(data)
                    f.flush()
                    self.written += 1
                elif what in ("shut", "end") and f is not None:
                    f.close()
                    _log.info("this robot's recording %s is closed: %d items", self.path, self.written)
                    f, self.path = None, None
            except OSError as exc:
                _log.warning("this robot's recording could not be written to %s: %s - it stops",
                             self.path or self._where, exc)
                with self._lock:
                    self.on = False
                if f is not None:
                    try:
                        f.close()
                    except OSError:
                        pass
                f, self.path = None, None
            if what == "end":
                return

    def close(self) -> None:
        """As its connect closes: what waits written and the file closed, within _CLOSE_S - said where it was not."""
        with self._lock:
            writer, self.on = self._writer, False
        if writer is None or not writer.is_alive():
            return
        self._queue.put(("end", None))
        writer.join(_CLOSE_S)
        if writer.is_alive():
            _log.warning("this robot's recording %s was not finished within %d s: its last items may be missing",
                         self.path, int(_CLOSE_S))
