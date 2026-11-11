"""
A DirectConnection's observations between acts, mixed into it (_ObservationStream): what a robot hands over as it makes
it (observe) - posted on the robot's stream to its worker, every one, in order - and the act that follows them,
numbered by how many went before it. The connection they ride, its worker and its lock are DirectConnection's
(direct.py). A policy that declared what it read (observations=seq.Observations, a window kept here by step) is no
more: one that reads more than the newest keeps them in an @seq.observe method.

"""
from __future__ import annotations

from typing import Any, Optional

from ..errors import InvalidRequest, Unavailable
from . import blocks as _blocks
from . import compress as _compress
from . import marked_observe as _marked
from . import observe_stream as _observe
from .warn import warn
from .worker_transport import _WorkerTransport



PROMPT_KEYS = ("instruction", "task", "prompt", "language_instruction")


class _ObservationStream:
    """DirectConnection's observe(), its episodes' windows and the act that reads them (the module's docstring)."""

    def observe(self, inputs: Any, episode_id: str) -> int:
        """One observation of the caller's episode `episode_id`, handed over as the robot makes it: its number in the
        episode, at once. Packed here, on the robot's own thread (what msgpack cannot carry is refused to this call), then
        posted on the robot's stream to its worker (observe_stream). The next act of the episode is the next number.
        Mid-episode, its worker gone and the one in its place starting (or the robot in line for one), the observation is
        kept for the episode's next act, which waits for that worker as an act does and sends it: never waited for here.
        """
        self._assert_open()
        try:
            self._ensure_connected()
            reachable = True
        except Unavailable as exc:
            if self.contract is None or not (exc.warming or exc.queued):
                raise


            reachable = False



        cut = _blocks.Cut(_compress.of(self)) if reachable else None
        try:

            packed, marks = _marked.packed(self, inputs, episode_id, cut)
        except ValueError as exc:
            raise InvalidRequest(f"observe(): this observation cannot be sent - {exc}") from None
        with self._lock:
            n = self._numbers.get(episode_id, 0)
            self._numbers[episode_id] = n + 1
            self._last_seen[episode_id] = inputs
            if marks is not None:
                packed = marks.settle(self, episode_id, n, packed)
            worker = self._worker if reachable else None
            wid = self._worker_episode if episode_id == self._caller_episode and self._worker_episode else episode_id
            stream = self._stream_for(worker) if worker is not None else None
            held = self._held.pop(episode_id, []) if worker is not None else []
            if worker is None:
                held_frame = _observe.frame(n, packed)
                if cut is not None and cut.last is not None:
                    held_frame = _blocks.inline(held_frame, cut.last[1])
                self._held.setdefault(episode_id, []).append((n, held_frame))
        cut_out = cut.last[1] if cut is not None and cut.last is not None else {}
        if worker is not None:
            worker.keep_warm()



            worker.say_restart(len(packed) + sum(len(c) for c in cut_out.values()))
        if stream is not None:
            for s, f in held:
                stream.put(wid, s, f)
            stream.put(wid, n, _observe.frame(n, packed), blocks=cut.last if cut is not None else None)
            self._say_refusals(stream)
        return n

    def _observed(self) -> list:
        """Under the lock: the worker-side ids of the episodes observed and not ended here - what close() ends with the
        connection. An episode a person drove from its first step reached its worker in observations alone, and its
        worker's copy held it from the next robot for up to its 300 s. {dev 11-10: a worker's second robot, "all replicas
        bound to active episodes (1): a replica frees when its episode ends (episode_end) or has had no act for 300 s"}"""
        return [self._worker_episode if e == self._caller_episode and self._worker_episode else e for e in self._numbers]

    def _stream_for(self, worker: "_WorkerTransport") -> "_observe.ObserveStream":
        """The stream posting to `worker` - made the first time it is asked for, and anew for another worker, posting
        again what the one before kept since each episode's last served act. Called under self._lock."""
        if self._stream is None or self._stream_to is not worker:
            carried, carried_blocks = {}, {}
            if self._stream is not None:
                carried, carried_blocks = self._stream.carry(), self._stream.carry_blocks()
                self._stream.close()
            squeeze = _compress.of(self)
            self._stream, self._stream_to = _observe.ObserveStream(
                worker.post_observe, carried, on_left_out=_marked.left_out_of(self), on_put=self._observation_sizes,
                keep=self._keep, on_posted=squeeze.uplink.note, content=squeeze.content,

                carried_blocks=carried_blocks,



                submit=getattr(worker, "submit_observe", None), room=getattr(worker, "room", None),
                ask=getattr(worker, "ask_taken", None),
                latest=(lambda: worker.latest_only) if hasattr(worker, "latest_only") else None,
                video=_marked.video_of(self)), worker
            if hasattr(worker, "frames_first"):
                worker.frames_first = self._stream.picked
        return self._stream

    def _own_act(self, episode_id: str) -> tuple:
        """For an act of an episode (L0): (the next number, which it takes none of, and the frames held for it): the
        observations before it are the episode's every one so far - and, the episode gone on anew since the robot's latest
        observation (its connect here reached another worker: _rotate_episode), that observation first, sent again as
        its step 0, as _own_anew sends it. {dev acceptance 10-27, the preempt signal: the reconnect waited in line, and
        the next act, numbered 0 on the worker it moved to, was refused "episode f1a44379… has no observation yet"}"""
        self._ensure_connected()
        replay = self._replayed(episode_id) if self._unobserved(episode_id) else None
        with self._lock:


            n, held = self._numbers.get(episode_id, 0), self._held.pop(episode_id, [])
            if not n and not held and replay is not None:
                n, held = 1, self._step_0(episode_id, replay)
            return n, held

    def _own_anew(self, episode_id: str) -> tuple:
        """An act going on under a new episode (_rotate_episode): after the observations held, numbered from 0 and sent
        first - and, none held, after the robot's latest observation, sent again as the new episode's step 0: its copy
        has none of the old episode's, and a call
        of nothing observed is refused (no_observation).

"""
        replay = self._replayed(episode_id)
        with self._lock:
            self._number_anew(episode_id)
            held = self._held.pop(episode_id, [])
            if not held and replay is not None:
                held = self._step_0(episode_id, replay)
            return len(held), held

    def _unobserved(self, episode_id: str) -> bool:
        """Whether `episode_id` went on anew since the robot's latest observation of it: nothing numbered or held in it,
        and one seen (_last_seen) - a call of it would go with nothing observed."""
        with self._lock:
            return (not self._numbers.get(episode_id, 0) and not self._held.get(episode_id)
                    and episode_id in self._last_seen)

    def _step_0(self, episode_id: str, replay: tuple) -> list:
        """The robot's latest observation, packed again (_replayed), as the new episode's step 0 - held for the act, the
        episode numbered on from it. Under _lock."""
        packed, marks = replay
        if marks is not None:
            packed = marks.settle(self, episode_id, 0, packed)
        self._numbers[episode_id] = 1
        return [(0, _observe.frame(0, packed))]

    def _replayed(self, episode_id: str) -> "Optional[tuple[bytes, Any]]":
        """The robot's latest observation of `episode_id` packed again for the new episode it goes on in (_own_anew),
        outside the connection's lock: whole - no block a worker would have to hold under the new id - and its marked
        items from a keyframe, the new episode's encoders being new. None when the episode has seen none, or it does
        not pack now."""
        inputs = self._last_seen.get(episode_id)
        if inputs is None:
            return None
        try:
            return _marked.packed(self, inputs, episode_id)
        except ValueError:
            return None

    def _number_anew(self, episode_id: str) -> None:
        """An episode whose observations are numbered by the call begins again (called under self._lock): those held -
        sent to no worker yet - numbered from 0."""
        held = self._held.get(episode_id, [])
        if held:
            self._held[episode_id] = [(i, _observe.frame(i, f[len(_observe.frame(n, b"")):]))
                                      for i, (n, f) in enumerate(held)]
        self._numbers[episode_id] = len(held)

    def _observed_act(self, payload: dict, worker: "_WorkerTransport", own: tuple) -> None:
        """The act's body, each try, in place: its number (`seq`), the frames held for it posted first. It carries no
        observation."""
        n, held = own
        with self._lock:
            stream = self._stream_for(worker)
        for s, f in held:
            stream.put(payload["episode_id"], s, f)
        held.clear()
        payload["seq"] = n
        self._say_refusals(stream)

    def _say_refusals(self, stream: "_observe.ObserveStream") -> None:
        """What the worker refused to keep of an episode's observations (more than it keeps between two acts), said once
        an episode on the robot's own thread: those were left out, and its acts read the ones it kept."""
        for why in stream.refusals():
            warn(f"observations left out: the worker refused them ({why}); the episode's acts read the ones it kept")
