"""
A robot's observations posted to its worker as it makes them (POST /observe), on the robot's stream (worker_stream.py),
so the act that reads them carries only the newest.

In one sentence: Policy.observe() packs each observation of its episode on the robot's own thread, numbers it and hands
it here, never waiting → up to IN_FLIGHT posts go on their way at once, each queued on the stream in the order picked
and each with what came and is not on its way yet, in one msgpack body (a slow upload still batches by itself) → the
worker keeps them by number and hands them on in order, whichever post brought them first, so only an episode's first
post here goes alone, and each of an episode whose frames hold video → an act carries the next number (DirectConnection)
and the worker gives the policy every observation before it → what an act was served with is forgotten here, and
everything since is kept, so a worker that is missing some (a post lost, another worker after a reconnect) is sent them
again from the first it names (resend) → ones the worker refuses to keep (more than it keeps for an episode) are never
posted again: their numbers go as left out (`skipped`), so no act waits for them, and the robot is told once an episode
(refusals).

WHY several posts on their way at once: one at a time, a frame made while a post is on its way waits for that post's
answer - a round trip - before it goes, and every frame does once the round trip passes the frame interval.

WHY an episode's first post goes alone: the worker counts an episode whole from the first number it is sent - a robot
moved to it sends what it kept since its last served act - so a later post of it that came first would have it count
from there and drop those before; once that first post is
answered the worker knows where the episode begins. A post that did not land, and a resend, make the next post of the
episode go alone again: the worker may be another one (restarted).
WHY an episode whose frames hold video posts as any other, several at once: its worker drops the frames after a refused
or missing one up to the next keyframe, its episode going on, and the robot forces that keyframe as the refusal comes back (marked_observe.left_out), so about one round trip of
frames goes.

WHY a frame handed again as it is goes once: a stream to another worker posts what the one before kept - the same
frames. Handed while the first went, the second
was dropped as the first was answered; handed after, it went again, saying the robot switched after an act there was
answered (tests/test_standby.py, 8 of 10 once that first post went on an open connection).
{worker 6 10-25}
WHY everything since the last served act is kept, not only what the worker has not said it has: a worker that restarts,
or another one after a reconnect, has none of them, and the next act's frames must still be whole there.
WHY packed when handed over: what msgpack cannot carry is refused to the robot's own call, as an act's inputs are, and
the thread that posts never meets it - a post that can never be made would otherwise be tried for good, and hold back
every observation behind it.
"""
from __future__ import annotations

import struct
import threading
import time
from typing import Any, Callable, Optional

from ..errors import AuthError, SequencesError
from . import blocks as _blocks
from . import msgpack_io as _msgpack






RESUME_FORMAT = "x-seq-resume/1"





SWITCHED_HEADER = "X-Seq-Switched"




LATEST_FORMAT = "x-seq-latest/1"
FRAMES_MISSING = "frames_missing"
FRAMES_OVER_LIMIT = "frames_over_limit"
PATH = "/observe"

MAX_BATCH = 64





IN_FLIGHT = 8

_ROOM_WAIT_S = 0.05


RETRY_S, RETRY_CAP_S = 0.05, 2.0



KEEP_SERVED_S = 5.0


class Keep:
    """How long more what a worker was served is kept - KEEP_SERVED_S once the robot has a standby, else 0: forgotten at
    once - shared by a connection with its streams, and holding nothing of the connection: a stream's
    thread holds it, and a connection the robot dropped must still be collected."""

    __slots__ = ("s",)

    def __init__(self) -> None:
        self.s = 0.0


def packed(inputs: Any) -> bytes:
    """One observation as msgpack, for frame(): msgpack_io.MsgpackError (a ValueError) for what msgpack cannot carry."""
    return _msgpack.pack(inputs)


def frame(seq: int, inputs: bytes) -> bytes:
    """One ObserveFrame, {"seq", "inputs"}, as msgpack - `inputs` already packed (packed())."""
    return b"\x82" + _msgpack.pack("seq") + _msgpack.pack(seq) + _msgpack.pack("inputs") + inputs


def _body(episode: str, batch: list[tuple[int, Optional[bytes]]], blocks: Optional[dict] = None) -> bytes:
    """One POST /observe body, ObserveRequest as msgpack: the batch's frames as they were packed when handed over (never
    packed again), its numbers left out, and - `blocks`, by id - the contents of the blocks its frames name that its
    worker does not hold (ObserveRequest.blocks)."""
    frames = [f for _, f in batch if f is not None]
    head = bytes((0x90 | len(frames),)) if len(frames) <= 15 else struct.pack(">BH", 0xDC, len(frames))
    tail = (_msgpack.pack("blocks"), _msgpack.pack(blocks)) if blocks else ()
    return b"".join((b"\x84" if blocks else b"\x83", _msgpack.pack("episode_id"), _msgpack.pack(episode),
                     _msgpack.pack("frames"), head, *frames, _msgpack.pack("skipped"),
                     _msgpack.pack([s for s, f in batch if f is None]), *tail))


def _refused(exc: BaseException) -> bool:
    """Whether a post's failure is the worker saying it will not keep it - past what it keeps for an episode, a body it
    cannot read - which no later try changes, as opposed to one that did not land or a busy or restarting worker."""
    return isinstance(exc, SequencesError) and not exc.retryable and not isinstance(exc, AuthError)


class ObserveStream:
    """The observations one robot posts to one worker (module docstring). `post(body, episode)`: one POST /observe of a
    msgpack body of `episode`'s, called from up to `in_flight` threads at once; it raises when the post did not land or
    was refused. `carried`: what a stream to another worker kept (carry()), posted again here first."""

    def __init__(self, post: Callable[[bytes, str], Any],
                 carried: Optional[dict[str, dict[int, Optional[bytes]]]] = None,
                 on_left_out: Optional[Callable[[str, set], set]] = None,
                 on_put: Optional[Callable[[int], None]] = None, keep: Optional[Keep] = None,
                 in_flight: int = IN_FLIGHT,
                 on_posted: Optional[Callable[[int, float], None]] = None,
                 content: Optional[Callable[[tuple, bytes], Any]] = None,
                 carried_blocks: Optional[dict[str, dict[int, tuple]]] = None,
                 submit: Optional[Callable[..., Optional[Callable[[], Any]]]] = None,
                 room: Optional[Callable[[float], bool]] = None, latest: Optional[Callable[[], bool]] = None,
                 video: Optional[Callable[[str], bool]] = None, ask: Optional[Callable[[], None]] = None) -> None:
        self._post = post








        self._submit, self._room, self._latest, self._video = submit, room, latest, video

        self._ask = ask
        self._tickets = self._turn = 0
        self.dropped = 0



        self._content = content


        self._infos: dict[str, dict[int, tuple]] = {}
        self._retention: dict[str, _blocks.Retention] = {}
        self._counted: dict[str, set[int]] = {}

        self._on_posted = on_posted

        self._keep = keep if keep is not None else Keep()

        self._on_put = on_put


        self._on_left_out = on_left_out
        self._cv = threading.Condition()


        self._pending: dict[str, list[tuple[int, Optional[bytes]]]] = {}

        self._kept: dict[str, dict[int, Optional[bytes]]] = {}

        self._handed: dict[str, dict[int, float]] = {}

        self._flying: dict[str, set[int]] = {}


        self._got: dict[str, set[int]] = {}


        self._open: set[str] = set()
        self._busy = 0
        self._refused: dict[str, str] = {}
        self._said: set[str] = set()


        self._wait, self._hold = RETRY_S, 0.0
        self._closed = False
        for episode, kept in (carried or {}).items():
            infos = (carried_blocks or {}).get(episode, {})
            for seq, packed_frame in sorted(kept.items()):
                self._queue(episode, seq, packed_frame, infos.get(seq))
        self._threads = [threading.Thread(target=self._run, name="seq-observe", daemon=True)
                         for _ in range(max(1, in_flight))]
        for thread in self._threads:
            thread.start()

    def put(self, episode: str, seq: int, packed_frame: bytes, blocks: Optional[tuple] = None) -> None:
        """One observation of `episode`, its number `seq` and its frame packed (frame()), to be posted as soon as a post
        is free to take it - once: handed again as it is while it waits, is on its way or was answered (a stream after
        a switch posts what the one before kept), it is not posted again. `blocks`: what its frame's references name
        (blocks.Cut's used, contents, paths), its contents kept with it until it is forgotten."""
        if self._on_put is not None:

            self._on_put(len(packed_frame) + (sum(len(c) for c in blocks[1].values()) if blocks else 0))
        with self._cv:
            if self._kept.get(episode, {}).get(seq) == packed_frame and (
                    seq in self._got.get(episode, ()) or any(s == seq for s, _ in self._pending.get(episode, ()))):
                return
            self._queue(episode, seq, packed_frame, blocks)
            self._cv.notify_all()

    def _queue(self, episode: str, seq: int, packed_frame: Optional[bytes], blocks: Optional[tuple] = None) -> None:
        self._kept.setdefault(episode, {})[seq] = packed_frame
        if blocks is not None:
            self._infos.setdefault(episode, {})[seq] = blocks
        self._handed.setdefault(episode, {})[seq] = time.monotonic()
        self._pending.setdefault(episode, []).append((seq, packed_frame))

    def served(self, episode: str, seq: int) -> None:
        """An act numbered `seq` was served: what came before it, and it, is the worker's to forget - and ours once it
        was handed over the Keep's seconds before this answer, for a standby that reads the episode back from a little
        before. Nothing is forgotten while no answer comes."""
        with self._cv:
            kept, handed = self._kept.get(episode), self._handed.get(episode, {})
            if kept:
                old = time.monotonic() - self._keep.s
                got = self._got.get(episode, set())
                infos = self._infos.get(episode, {})
                for s in [s for s in kept if s <= seq and handed.get(s, 0.0) <= old]:
                    del kept[s]
                    handed.pop(s, None)
                    got.discard(s)
                    infos.pop(s, None)

    def resend(self, episode: str, first: int, timeout_s: float) -> bool:
        """The worker named `first` the first observation it is missing: every one kept from there (from the oldest
        kept, when it names one already forgotten) goes again, ahead of what is waiting, its first post alone - the
        worker may begin the episode anew from it; returns once they are posted, or False when that took past
        `timeout_s`."""
        with self._cv:
            kept = self._kept.get(episode, {})
            again = sorted((s, v) for s, v in kept.items() if s >= first) or sorted(kept.items())
            resent = {s for s, _ in again}
            waiting = [(s, v) for s, v in self._pending.get(episode, []) if s not in resent]
            self._pending[episode] = [*again, *waiting]
            self._got.get(episode, set()).difference_update(resent)
            self._open.discard(episode)
            self._forget_held(episode)
            self._hold = 0.0
            self._cv.notify_all()
        return self.flush(timeout_s)

    def flush(self, timeout_s: float) -> bool:
        """Wait until everything handed here is posted and answered - or, on the robot's stream, taken: the worker asked
        which it took (`ask`), as no act may come to say it - again whenever more were queued since it was last asked,
        and every half second - `timeout_s` at most."""
        end, asked, at = time.monotonic() + timeout_s, None, 0.0
        with self._cv:
            while (self._busy or any(self._pending.values())) and not self._closed:
                if self._busy and self._ask is not None and (asked != self._tickets or time.monotonic() - at >= 0.5):
                    asked, at = self._tickets, time.monotonic()
                    self._ask()
                left = end - time.monotonic()
                if left <= 0:
                    return False
                self._cv.wait(min(left, 0.5))
            return True

    def refusals(self) -> list[str]:
        """Why the worker refused observations, for each episode it refused some of since this was last asked - once an
        episode: the robot's own thread says them (DirectConnection)."""
        with self._cv:
            said = list(self._refused.values())
            self._said.update(self._refused)
            self._refused.clear()
            return said

    def move(self, old: str, new: str) -> None:
        """The robot's episode goes on under another id (a reconnect, a copy that stopped): what is kept and waiting of
        it is the new id's, posted under it - what the worker had under the old one is not there."""
        with self._cv:
            kept, pending = self._kept.pop(old, {}), self._pending.pop(old, [])
            self._handed.setdefault(new, {}).update(self._handed.pop(old, {}))


            self._flying.pop(old, None)
            self._got.pop(old, None)
            self._open.difference_update((old, new))

            self._infos.setdefault(new, {}).update(self._infos.pop(old, {}))
            self._forget_held(old)
            self._forget_held(new)
            if kept or pending:
                self._kept.setdefault(new, {}).update(kept)
                self._pending[new] = sorted({**dict(self._pending.get(new, [])), **kept, **dict(pending)}.items())
                self._cv.notify_all()

    def oldest(self, episode: str) -> Optional[int]:
        """The first number kept of `episode`: None when none is."""
        with self._cv:
            kept = self._kept.get(episode)
            return min(kept) if kept else None

    def carry(self) -> dict[str, dict[int, Optional[bytes]]]:
        """Everything kept, by episode, for a stream to another worker to post again (it has none of it)."""
        with self._cv:
            return {e: dict(k) for e, k in self._kept.items() if k}

    def carry_blocks(self) -> dict[str, dict[int, tuple]]:
        """What each kept frame's references name, by episode and number, carried with carry()."""
        with self._cv:
            return {e: {s: i for s, i in infos.items() if s in self._kept.get(e, {})}
                    for e, infos in self._infos.items() if infos}

    def end(self, episode: str) -> None:
        """The episode ended (or moved to another id): nothing of it is posted or kept any more."""
        with self._cv:
            self._pending.pop(episode, None)
            self._kept.pop(episode, None)
            self._handed.pop(episode, None)
            self._flying.pop(episode, None)
            self._got.pop(episode, None)
            self._open.discard(episode)
            self._refused.pop(episode, None)
            self._said.discard(episode)
            self._infos.pop(episode, None)
            self._forget_held(episode)

    def close(self) -> None:
        with self._cv:
            self._closed = True
            self._cv.notify_all()

    def _left_out(self, episode: str, batch: list[tuple[int, Optional[bytes]]], why: str) -> None:
        """The worker refused `batch` (under self._cv): its frames are never posted again - their numbers go as left
        out, ahead of what waits, so no act waits for them - and why is said to the robot once the episode. Numbers left
        out that are refused as well are dropped: nothing more can be said of them."""
        pending = self._pending.get(episode)
        if pending is None:
            return
        numbers = {s for s, _ in batch}
        rest = [(s, f) for s, f in pending if s not in numbers]
        self._forget_held(episode)
        if all(f is None for _, f in batch):
            self._pending[episode] = rest
            return
        if self._on_left_out is not None:
            more = set(self._on_left_out(episode, {s for s, f in batch if f is not None}))
            flying = self._flying.get(episode, set())
            more &= {s for s, f in rest if f is not None and s not in flying}
            numbers |= more
            rest = [(s, f) for s, f in rest if s not in more]
        kept = self._kept.get(episode, {})
        for s in numbers & kept.keys():
            kept[s] = None
        self._pending[episode] = [*((s, None) for s in sorted(numbers)), *rest]
        if episode not in self._said:
            self._refused.setdefault(episode, why)

    def _next(self) -> Optional[tuple[str, list[tuple[int, Optional[bytes]]], bool]]:
        """What a free post takes (under self._cv): of the first episode with numbers waiting that are not on their way,
        those, MAX_BATCH at most, and whether it goes alone - an episode not open goes one post at a time, and only once
        nothing of it is on its way (module docstring); None when no post may go. Nothing of it counted yet: the blocks
        it carries are counted once it goes (_carries) - a pick the stream has no room for is picked again, and counted
        then."""
        for episode, items in self._pending.items():
            flying = self._flying.get(episode)
            alone = episode not in self._open
            if flying and alone:
                continue
            batch = [(s, f) for s, f in items if not flying or s not in flying][:MAX_BATCH]
            if batch and self._latest is not None and not (self._video is not None and self._video(episode)) \
                    and self._latest():
                batch = self._newest(episode, batch)
            if batch:
                return episode, batch, alone
        return None

    def _newest(self, episode: str, batch: list[tuple[int, Optional[bytes]]]) -> list[tuple[int, Optional[bytes]]]:
        """`batch` with every frame but its newest left out (under self._cv), for a worker whose policy reads each act's
        latest observation alone (latest): a frame a newer one stood behind before it was posted is none it reads - its
        number goes as left out, so no act waits for it, and it is kept as left out for a worker that asks for it again.
        Only frames not yet posted: one on its way, or posted, goes as it is.
"""
        framed = [s for s, f in batch if f is not None]
        if len(framed) < 2:
            return batch
        stale = set(framed[:-1])
        if not stale:
            return batch
        kept = self._kept.get(episode, {})
        for s in stale & kept.keys():
            kept[s] = None
        self._pending[episode] = [(s, None if s in stale else f) for s, f in self._pending[episode]]
        self.dropped += len(stale)
        return [(s, None if s in stale else f) for s, f in batch]

    def picked(self, episode: Optional[str], timeout_s: float) -> bool:
        """Wait until every observation of `episode` handed over is queued on the robot's stream - behind what came
        before it, in the order handed over - `timeout_s` at most, so an act goes behind them on the same connection
        (worker_transport.post_act). Not while posts are held back after one did not land: the act goes, and meets what
        is wrong. True once none waits."""
        end = time.monotonic() + timeout_s
        with self._cv:
            while not self._closed:
                flying = self._flying.get(episode, set())
                waiting = any(s not in flying for s, _ in self._pending.get(episode, ()))
                if not waiting and self._turn == self._tickets:
                    return True
                left = end - time.monotonic()
                if left <= 0 or self._hold > time.monotonic():
                    return False
                self._cv.wait(left)
            return True

    def _carries(self, episode: str, batch: list[tuple[int, Optional[bytes]]]) -> dict:
        """The blocks a batch of `episode` carries (under self._cv), id -> (content, path): of each frame posted here
        the first time, in order, those its worker does not hold as both count it (blocks.Retention); of one posted
        before - sent again, or a post that did not land - every one: its worker may lack them."""
        infos = self._infos.get(episode)
        if not infos:
            return {}
        held = self._retention.setdefault(episode, _blocks.Retention())
        counted = self._counted.setdefault(episode, set())
        out: dict = {}
        for s, f in batch:
            info = infos.get(s) if f is not None else None
            if info is None:
                continue
            used, contents, paths = info
            if s in counted:
                need = used
            else:
                counted.add(s)
                need = [b for b in used if not held.holds(b)]
                held.use(used)
            for b in need:
                out.setdefault(b, (contents[b], paths.get(b, ())))
        return out

    def _forget_held(self, episode: str) -> None:
        """What `episode`'s worker holds, counted from nothing again (under self._cv): its next frames carry every
        block they name - a post that did not land or was refused, a worker that said it lacks some."""
        self._retention.pop(episode, None)
        self._counted.pop(episode, None)

    def _queue_in_turn(self, ticket: int, body: Optional[bytes], episode: str, alone: bool,
                       numbers: set[int], batch: list[tuple[int, Optional[bytes]]]) -> bool:
        """Queue a picked post on the robot's stream once every one picked before it was queued (its `ticket`), so the
        worker reads them in the order picked: True, the post done once taken or answered (_after, from the stream's
        thread) - False when no stream is open now, or there is no body: the post goes by `post`. An episode's first
        post queued there opens it at once: the worker reads it first."""
        with self._cv:
            while self._turn != ticket and not self._closed:
                self._cv.wait()
            queued = False
            if body is not None and not self._closed:
                size = len(body)

                def done(exc: Optional[BaseException], took: Optional[float]) -> None:
                    self._after(episode, batch, numbers, alone, size, exc, took)
                try:
                    queued = bool(self._submit(body, episode, done=done))
                except Exception:
                    queued = False
            if queued and alone:
                self._open.add(episode)
            self._turn += 1
            self._cv.notify_all()
            return queued

    def _landed(self, episode: str, numbers: set[int]) -> None:
        """A post came back, answered or not (under self._cv): its numbers are no longer on their way."""
        self._busy -= 1
        flying = self._flying.get(episode)
        if flying is not None:
            flying -= numbers
            if not flying:
                del self._flying[episode]

    def _run(self) -> None:
        """One of the stream's IN_FLIGHT threads: a post at a time."""
        while True:
            with self._cv:
                while True:
                    if self._closed:
                        return
                    held = self._hold - time.monotonic()
                    picked = self._next() if held <= 0 else None
                    if picked is not None:
                        break
                    self._cv.wait(held if held > 0 else None)


                full = self._room is not None and not self._room(0.0)
                if not full:
                    episode, batch, alone = picked



                    carries = self._carries(episode, batch)
                    numbers = {s for s, _ in batch}
                    self._flying.setdefault(episode, set()).update(numbers)
                    self._busy += 1
                    ticket = None
                    if self._submit is not None:
                        ticket, self._tickets = self._tickets, self._tickets + 1
            if full:
                self._room(_ROOM_WAIT_S)
                continue
            queued, body = False, None
            try:

                body = _body(episode, batch, {b: (self._content(p, c) if self._content is not None else c)
                                              for b, (c, p) in carries.items()} or None)
            finally:
                if ticket is not None:
                    queued = self._queue_in_turn(ticket, body, episode, alone, numbers, batch)
            if queued:
                continue
            t0 = time.monotonic()
            try:
                self._post(body, episode)
            except Exception as exc:
                self._after(episode, batch, numbers, alone, len(body), exc, None)
                continue
            self._after(episode, batch, numbers, alone, len(body), None, time.monotonic() - t0)

    def _after(self, episode: str, batch: list[tuple[int, Optional[bytes]]], numbers: set[int], alone: bool,
               size: int, exc: Optional[BaseException], took: Optional[float]) -> None:
        """A post done - answered, or taken on the robot's stream (from its thread), its writing having taken `took` -
        or refused (`exc`: left out) or lost (kept, and tried again)."""
        if exc is None and took is not None and self._on_posted is not None:
            self._on_posted(size, took)
        with self._cv:
            self._landed(episode, numbers)
            if exc is not None:
                if _refused(exc):
                    self._left_out(episode, batch, str(exc))
                else:


                    self._open.discard(episode)
                    self._forget_held(episode)
                    self._hold = time.monotonic() + self._wait
                    self._wait = min(self._wait * 2, RETRY_CAP_S)
                self._cv.notify_all()
                return
            self._wait, self._hold = RETRY_S, 0.0
            kept = self._kept.get(episode)
            if kept:
                self._got.setdefault(episode, set()).update(s for s, f in batch if f is not None and s in kept)
            if episode in self._pending:
                self._pending[episode] = [(s, f) for s, f in self._pending[episode] if s not in numbers]
                if alone:


                    self._open.add(episode)
            self._cv.notify_all()
