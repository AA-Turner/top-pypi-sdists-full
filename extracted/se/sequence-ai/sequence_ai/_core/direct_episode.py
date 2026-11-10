"""
A DirectConnection's episodes, mixed into it (_Episodes): the caller's episode id mapped to the one its worker sees
(_apply_episode) - a new one when a reconnect moved the robot or the copy that held it stopped (_rotate_episode,
_lose_episode) - its end told to the worker, where a move the platform asked for happens (end_episode), how it went kept
with the captured field data (label_episode), and the session's parameters taking effect at its boundaries. The
connection, its worker and its lock are DirectConnection's (direct.py), whose move-notice words these read.

"""
from __future__ import annotations

import sys
import time
import uuid
from typing import Optional

from ..errors import Unavailable
from .names import segment
from .warn import warn
from .worker_transport import _EPISODE_END_S, _WorkerTransport








_COPY_STOPPED = frozenset({"gpu_out_of_memory", "host_out_of_memory", "crashed", "hung"})
_EPISODE_LOST = "episode_lost"




_BATCH_FAILED = "batch_failed"
_STATE_GONE = _COPY_STOPPED | {_BATCH_FAILED}



_MOVE_HOLD_S = 15.0
_MOVE_HOLD_GRACE_S = 5.0
_MOVE_HOLD_ASK_S = 1.0


def _hold_s(notice: Optional[dict]) -> Optional[float]:
    """How long a robot waits at its episode boundary for a worker with room coming up, as its move notice says how
    soon (`up_in_s`): that and _MOVE_HOLD_GRACE_S when it is within _MOVE_HOLD_S, else None - no hold."""
    up = notice.get("up_in_s") if isinstance(notice, dict) else None
    if not isinstance(up, (int, float)) or isinstance(up, bool) or not 0 <= up <= _MOVE_HOLD_S:
        return None
    return float(up) + _MOVE_HOLD_GRACE_S


class _Episodes:
    """DirectConnection's episodes (the module's docstring)."""

    def end_episode(self, episode_id: str) -> Optional[str]:
        """The robot's episode is over: the worker frees its state now (a stateful policy's @seq.on_episode runs
        and its replica returns to the pool) instead of after its TTL with no act. Never raises. Returns the id its
        worker ended: the one it went on under after a reset (_rotate_episode), its policy's episode.id.

 When the platform asked the
        robot to move (its worker is leaving), this boundary is where it does: the next episode starts on a worker
        already up - the one started beside the worker it leaves - and nothing is cut. The worker it leaves is told the episode ended while the move's connect goes, not before it;
        kept on that worker after all, its next episode starts once the worker has been told, as with no move.
        """
        from .direct import _ready
        with self._lock:
            worker = None if self._closed else self._worker
            wid = self._worker_episode if episode_id == self._caller_episode else episode_id
            self._episode_open = False
            if episode_id == self._caller_episode:
                self._drop_resumed()
            self._settle_params()

            self._numbers.pop(episode_id, None)
            self._held.pop(episode_id, None)
            self._last_seen.pop(episode_id, None)
            if self._stream is not None and wid:
                self._stream.end(wid)
            moving = worker is not None and self._rotate is not None and _ready(self._rotate)
        told = None
        if worker is not None and wid:
            if moving:
                told = worker.end_episode_behind(wid)
            else:
                worker.post_episode_end(wid)
        try:
            with self._lock:
                if self._rotate is None or self._closed or self._worker is None:
                    return wid
                hold = None if _ready(self._rotate) else _hold_s(self._rotate)
                if not _ready(self._rotate) and hold is None:




                    return wid
            if hold is not None and not self._room_within(hold):
                return wid
            with self._lock:
                if self._rotate is None or self._closed or self._worker is None or not _ready(self._rotate):
                    return wid

                self._caller_episode = self._worker_episode = None
                try:
                    self._connect(renew=False, move=True)
                except Unavailable:





                    if self._worker is not None:
                        self._worker.gone = True
                except Exception:
                    pass
        finally:
            if told is not None:
                with self._lock:
                    stays = self._worker is worker and not worker.gone
                if stays:



                    told.join(2 * _EPISODE_END_S)
        return wid

    def _room_within(self, hold_s: float) -> bool:
        """At an episode boundary, told a worker with room for this robot is coming up soon (_hold_s): ask the platform
        every _MOVE_HOLD_ASK_S, for up to `hold_s`, whether a move would take it off its worker now - True once one would,
        and the move is made then. False when the hold runs out, its seat went or the connection closed: the next
        episode starts on the worker it is on, as with no hold, and it moves at a later boundary. Said once a hold, on
        stderr, as the move's notice is.
"""
        from .direct import _ready
        print(f"[sequences] {self._model}: the worker it moves to is coming up; the next episode waits up to "
              f"{hold_s:.0f} s for it", file=sys.stderr, flush=True)
        end = time.monotonic() + hold_s
        while True:
            said = self._keep_seat()
            with self._lock:
                if self._closed or said == "gone":
                    return False
                if _ready(self._rotate):
                    return True
            left = end - time.monotonic()
            if left <= 0:
                return False
            time.sleep(min(_MOVE_HOLD_ASK_S, left))

    def label_episode(self, episode_id: str, *, success: bool, notes: str = "") -> str:
        """How the robot's episode went, kept with the deployment's captured field data
        (`seq policy set <name> capture=on`): written for the id the workers saw it under — and every id it carried after a reconnect moved it. Raises on
        failure. Returns the last of them, the one it went on under (end_episode).
        """
        with self._lock:
            ids = [episode_id, *self._aliases.get(episode_id, [])]
            worker = None if self._closed else self._worker
        for wid in ids:

            self._gateway.post(f"/v1/deployments/{segment(self._model)}/episodes/{segment(wid)}/label",
                               {"success": bool(success), "notes": notes})


        if worker is not None:
            worker.post_episode_label(ids[-1], success=success, notes=notes)
        return ids[-1]

    def _take_params(self, answered: dict) -> None:
        """What the platform answered the session runs with: at once, or — while an episode runs and they differ —
        at its boundary, so one episode never runs on two sets of parameters."""
        if self._episode_open and (answered or None) != self._params:
            self._pending_params = answered
        else:
            self._params, self._pending_params = answered or None, None

    def _settle_params(self) -> None:
        """An episode boundary: parameters a renewal answered during the episode take effect now."""
        if self._pending_params is not None:
            self._params, self._pending_params = self._pending_params or None, None

    def _apply_episode(self, payload: dict) -> None:
        """Remap the caller's episode id to the current worker-side id (in place)."""
        with self._lock:
            caller = payload.get("episode_id")
            if caller is None:
                return
            if caller != self._caller_episode:

                self._drop_resumed()
                self._caller_episode = caller
                self._worker_episode = caller
                self._settle_params()
            self._episode_open = True
            payload["episode_id"] = self._worker_episode

    def _rotate_episode(self, notice: Optional[dict] = None, *, stopped: Optional[str] = None,
                        standby: Optional[str] = None) -> Optional[str]:
        """New worker → the episode restarts there; surface it, do not continue silently - with why, when the platform
        had said the robot was to move (`notice`, its `rotate`). `stopped`: the copy of the policy that held it stopped
        (its cause, _COPY_STOPPED), or ended it for a batch that raised (_BATCH_FAILED), on the same worker. The new
        episode is handed none of the old one's observations and counts its steps from 0 - the act on its way its first
        (Window.restart, post) - as the policy's Episode does; a run's counts go on. Returns the worker-side id it leaves,
        None on a stateless path. `standby`: why the worker the robot was on failed when its act went to its standby
        copy (_switch), said once a switch, an episode or none.
"""
        self._drop_resumed()
        if self._caller_episode is None:
            if standby is not None:
                warn(f"this robot's act went to its standby copy: the copy it was on {standby}")
            return None
        left = self._worker_episode
        self._worker_episode = uuid.uuid4().hex
        self._aliases.setdefault(self._caller_episode, []).append(self._worker_episode)
        self.episode_resets += 1
        if self._stream is not None and left:
            self._stream.end(left)
        if self._caller_episode in self._numbers:
            self._number_anew(self._caller_episode)
        if standby is not None:
            warn(f"this robot's act went to its standby copy: the copy it was on {standby}; its episode goes on there as "
                 "a new one, and what the policy kept of the last one did not carry over")
            return left
        if stopped == _BATCH_FAILED:
            warn("episode was reset: a batch it was in failed, so what the policy kept of it may be half changed and was "
                 "given up; the robot goes on in a new episode")
            return left
        if stopped is not None:
            warn(f"episode was reset: the copy of the policy that held it stopped ({stopped}); its next act starts a new "
                 "episode, and what the policy kept of this one did not carry over")
            return left
        from .direct import _moving_words
        why = f" ({_moving_words(notice, moved=True)})" if notice else ""
        warn("episode was reset after a reconnect to a new worker" + why + "; what the policy kept of this episode "
             "on the previous worker did not carry over")
        return left

    def _resumes_on(self, standby: "_WorkerTransport") -> bool:
        """Whether the robot's episode goes on under its id on `standby`: its worker said, on an answer, that it reads an
        episode's state back (RESUME_FORMAT, plan 99 U8) - one that has not, or reads none (a policy that takes no
        stream), starts it anew."""
        return standby.resumes is True and self._caller_episode is not None

    def _resume_episode(self, standby: "_WorkerTransport", why: str) -> None:
        """The robot's act went to its standby copy (_switch), which reads its episode back from its state as saved, at
        most 2 s before (plan 99 U6, U8): the episode goes on there under the same id. The observations kept go to it
        again first - a stream to it posts what this one kept - and it takes those after that state. Each post and act of it there says it switched (SWITCHED_HEADER) - read back even
        from its 0, its every frame kept - until one is answered, and then it is said, once (_resumed_answered): one
        that read back less than is kept starts the episode anew instead, said so (_rotate_episode) - one word a
        switch, and a true one. Under _lock.
        """
        standby.switched = self._worker_episode
        self._resumed = (why, standby)

    def _resumed_answered(self) -> None:
        """An act answered on the standby the robot's episode went on on (_resume_episode): said once, in U8's words."""
        with self._lock:
            why = self._drop_resumed()
        if why is not None:
            warn(f"this robot's act went to its standby copy: the copy it was on {why}; its episode goes on there from "
                 "its state as saved, at most 2 s before")

    def _drop_resumed(self) -> Optional[str]:
        """The robot's episode is no longer one going on on a standby that reads it back (_resume_episode) - an act of it
        answered there, a new episode, its end: why its worker failed, else None, and its posts and acts say nothing of
        a switch from here - a new episode under the same name ("ep-1" each time) is never read back as the last.
        Under _lock."""
        if self._resumed is None:
            return None
        (why, standby), self._resumed = self._resumed, None
        standby.switched = None
        return why

    def _lose_episode(self, worker: "_WorkerTransport", cause: Optional[str]) -> None:
        """The copy that held the caller's episode stopped, or ended it for a batch that raised (_STATE_GONE): a new
        worker-side episode, said with the cause (_rotate_episode), and the one it leaves ended on the worker - its lost
        mark cleared, nothing else to free - so the act goes again under the new id. Best effort: an end that does not
        arrive leaves the mark to run out."""
        with self._lock:
            left = self._rotate_episode(stopped=cause or "unknown cause")
        if left:
            worker.post_episode_end(left)
