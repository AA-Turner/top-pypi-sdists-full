# SPDX-FileCopyrightText: Copyright (c) 2026 General Sequences Company
# SPDX-License-Identifier: Apache-2.0
"""
Each episode's observation stream on the server: every observation a robot made, sent as it was made (POST /observe),
kept here until it goes on to its policy. The same code serves a robot on a GPU of your own (serve()) and on the hosted
platform.

    store = StreamStore()
    through = store.put(episode_id, [(seq, inputs), ...], skipped, size)       # a post: how far the episode is whole
    await store.forward(episode_id, observe)                                   # each whole frame on, in order
    await store.before(episode_id, n)                                          # an act after n observations

In one sentence: a post's frames are kept by episode, in order of their numbers, and answered with how far the episode
is whole (`through`) → each goes on to the copy of the policy that serves its episode in order as it comes (`forward`) →
an act, which says how many came before it (seq), waits until every one of them went, STREAM_WAIT_S at most (`before`) →
one that never comes refuses the act (409 frames_missing, details.from: the first missing, which the robot sends again
from); an episode past what a server keeps refuses the post (413 frames_over_limit) - but for a post that may shed
(`put`'s shed: a robot a person drives, whose policy is reading nothing), which lets the episode's oldest unread
observations go in its place, so the picture its operators watch and what its recorders keep go on.
An observation whose large arrays, bytes and text came as references to blocks (sequence_base.codec.blocks: a post's
blocks, kept by episode) is turned back as its turn comes, in order, before anything reads it - what each episode holds
counted as its robot counts it (blocks.Retention) - and one naming a block this server does not hold refuses its
episode's next act at once, from it (409 frames_missing): its robot sends it again with every block.

WHY on the server's event loop: the act and the posts of one episode meet here whichever copy serves it, and the
server's requests all run on this one loop, so nothing here takes a lock.
WHY an episode is whole from the first frame it is sent: a robot moved to this server sends what it kept since its last
served act, not the episode from 0 - what came before went to its policy on the server it left.

The robot's side is sequence_ai/_core/observe_stream.py: it numbers each observation, keeps several posts on their way,
and sends again from what an act's refusal names.
"""
from __future__ import annotations

import asyncio
import time
from typing import Awaitable, Callable

from sequence_base.codec import blocks as blocks_codec
from sequence_base.constants.limits import (
    MAX_STREAM_BYTES,
    MAX_STREAM_FRAMES,
    MAX_WORKER_BLOCK_BYTES,
    MAX_WORKER_STREAM_BYTES,
    STREAM_WAIT_S,
)

__all__ = ["Deferred", "StreamError", "StreamStore"]


class StreamError(Exception):
    """A post or an act the stream refuses: `missing` (409 frames_missing, from `first`), `busy` (every observation
    before the act is here, and its copy has not taken them - still in an earlier call) or over a limit (413)."""

    def __init__(self, message: str, *, missing: bool = False, first: int | None = None, busy: bool = False,
                 no_place: bool = False) -> None:
        super().__init__(message)
        self.missing, self.first, self.busy, self.no_place = missing, first, busy, no_place


def _busy(episode_id: str, ep: "_Episode") -> "StreamError":
    """An act whose observations are all here and not yet taken by its copy: busy, which its robot waits out - saying
    why: no copy here takes the episode yet (its frames deferred: Deferred's words), else its copy is still in an
    earlier call."""
    if ep.deferred:
        return StreamError(f"the observations before this act are here, but no copy of the policy here can take "
                           f"episode {episode_id} yet: {ep.deferred}", busy=True, no_place=ep.deferred_no_place)
    return StreamError(f"the copy of the policy serving episode {episode_id} is still busy with an earlier call; the "
                       "observations before this act are here", busy=True)


class Deferred(Exception):
    """An episode's frames its copy cannot take yet - its server still starting, no copy with room for the episode yet:
    they stay, and go again in a moment (StreamStore.forward), never the end of the episode's stream. `no_place`: no
    copy here will take the episode at all (the server is full for it), not a copy busy for a moment - its act is
    answered no_place, which sends its robot to a server with room, not copy_busy, which waits."""

    def __init__(self, message: str, *, no_place: bool = False) -> None:
        super().__init__(message)
        self.no_place = no_place


# How soon frames a copy could not take yet go again (Deferred): soon, then less often, while their episode is here.
_DEFERRED_FIRST_S, _DEFERRED_MAX_S = 0.05, 0.5


class _Episode:
    __slots__ = ("frames", "skipped", "through", "bytes", "used", "arrived", "forwarded", "handed",
                 "forwarding", "failed", "deferred", "deferred_no_place", "blocks", "block_bytes", "retention",
                 "missing", "fresh", "pins", "posted", "shed")

    def __init__(self, now: float) -> None:
        self.frames: dict[int, tuple[object, int]] = {}   # seq -> (inputs, the bytes counted for it)
        self.skipped: set[int] = set()
        self.through = -1                 # every number up to this one is here, or skipped
        self.bytes = 0
        self.used = now
        self.arrived = asyncio.Event()    # set at each post, for the act that waits
        self.forwarded: int | None = None  # the last number its copy has observed
        # ... or that is in its copy's queue, in order, ahead of any act of the episode that reaches the copy after
        # (forward's `handed`: a copy whose frames go with its batches)
        self.handed: int | None = None
        self.forwarding = False
        self.failed = False               # its copy answered {"ok": False}: no frame goes to it any more
        # why its frames wait for a copy (Deferred's words: no copy here with room for it yet, its server starting) -
        # None once one took them: what an act waiting for them is told in place of "an earlier call"
        self.deferred: str | None = None
        # whether that deferral said no copy here can take the episode at all (the server full for it), not a copy busy
        # for a moment: its act is answered no_place, so its robot goes to a server with room rather than wait out a
        # copy that will not free
        self.deferred_no_place = False
        # its blocks (codec.blocks): each content by id, their bytes, what it holds as its robot counts it, the first
        # observation that named one it does not hold, and the observations turned back since they were last read
        self.blocks: dict[bytes, bytes] = {}
        self.block_bytes = 0
        self.retention = blocks_codec.Retention()
        self.missing: int | None = None
        self.fresh: list[tuple[int, object]] = []
        # each block a post brought, by id: that post's last number, until which it is kept whatever the count says
        self.pins: dict[bytes, int] = {}
        self.posted = 0                   # its posts' bytes as they came, since an act of it last said them (posted)
        self.shed = 0                     # its observations let go unread, room made for newer ones (put's shed)


def _gone_to(ep: _Episode) -> int:
    """The last number of the episode that went to its copy - observed there, or in its copy's queue ahead of what comes
    after (handed) - a number before what this server began from counting as gone; -1 for none."""
    went = [s for s in (ep.forwarded, ep.handed) if s is not None]
    return max(went, default=-1)


def _first_unobserved(ep: _Episode, n: int) -> int | None:
    """The first observation of the episode before `n` its copy has not observed yet (StreamStore.before), or None: the
    one after the last forwarded - a number before what this server began from counting as had. A number its robot said
    it left out (a post's `skipped`: refused 413, dropped from its buffer) is never sent, so counts as had either way -
    else the act would wait for it, and be refused, for good."""
    first = 1 + _gone_to(ep)
    while first < n and first in ep.skipped and first not in ep.frames:
        first += 1
    return first if first < n else None


class StreamStore:
    """
    The observations of the episodes a server serves, on their way to their policy (the module's docstring).

    max_frames, max_bytes  what one episode may hold unread: observations, and their bytes
    max_worker_bytes       what the whole server may hold unread
    wait_s                 how long an act waits for the observations before it
    max_worker_block_bytes what the whole server may hold of blocks' contents
    ttl_s                  how long an episode with no post and no act is kept
    refuse_gap_early       an act whose observation is missing while later ones of its episode are here is refused at
                           once rather than after `wait_s`: on a robot's stream observations come in order, so the
                           missing one is not on its way
    """

    def __init__(self, *, max_frames: int = MAX_STREAM_FRAMES, max_bytes: int = MAX_STREAM_BYTES,
                 max_worker_bytes: int = MAX_WORKER_STREAM_BYTES, wait_s: float = STREAM_WAIT_S,
                 max_worker_block_bytes: int = MAX_WORKER_BLOCK_BYTES,
                 ttl_s: float = 300.0, clock: Callable[[], float] = time.monotonic,
                 refuse_gap_early: bool = False) -> None:
        self._max_frames, self._max_bytes, self._max_worker = max_frames, max_bytes, max_worker_bytes
        self._wait_s, self._ttl_s, self._clock = wait_s, ttl_s, clock
        self._eps: dict[str, _Episode] = {}
        self._bytes = 0
        self._block_bytes, self._max_blocks = 0, max_worker_block_bytes
        self._refuse_gap_early = refuse_gap_early

    def __len__(self) -> int:
        return len(self._eps)

    def __contains__(self, episode_id: object) -> bool:
        """Whether anything of `episode_id` is kept here: a frame or an act of it came, and it neither ended nor
        went."""
        return episode_id in self._eps

    @property
    def bytes(self) -> int:
        """The bytes of observations kept and not yet read, over every episode."""
        return self._bytes

    def put(self, episode_id: str, frames: list[tuple[int, object]], skipped: list[int], size: int,
            blocks: dict[bytes, bytes] | None = None, sent: int = 0, shed: bool = False) -> int:
        """Keep a post's frames - (seq, inputs), in the order the robot made them - the numbers it says it left out, and
        the contents of the blocks it carries (`blocks`, by id); `size`: the post's bytes, counted evenly over its
        frames; `sent`: its bytes as they came, which the episode's next act says (posted). Each frame is turned back as
        the episode is whole up to it (_advance). Returns how far the episode is whole. A number already had (sent
        again, or before what this server began from) is answered, never kept twice - but for one kept and not yet
        turned back, which the robot's sending again replaces (it sends from where its server lacked a block). Refused,
        keeping none of the post, when the episode or the server would hold more than it keeps (StreamError) - or,
        `shed`, the episode's oldest observations its policy has not read let go to make room (_shed): for a robot a
        person drives, whose policy reads none of them while its operators watch every one."""
        self._expire()
        ep = self._eps.get(episode_id)
        if ep is None:
            ep = self._eps[episode_id] = _Episode(self._clock())
        ep.used = self._clock()
        ep.posted += sent
        if ep.through < 0:
            # whole from the first number this server is sent: what came before went to the policy elsewhere
            first = min([s for s, _ in frames] + list(skipped), default=None)
            if first is not None:
                ep.through = first - 1
        each = size // max(1, len(frames)) if frames else 0
        new = [(s, v) for s, v in frames if s > ep.through and s not in ep.frames and s not in ep.skipped]
        again = [(s, v) for s, v in frames if s > ep.through and s in ep.frames]
        if shed:
            self._shed(ep, len(new), each * len(new))
        if len(ep.frames) + len(new) > self._max_frames:
            raise StreamError(f"episode {episode_id} would hold {len(ep.frames) + len(new)} observations its policy "
                              f"has not read, more than the {self._max_frames} a server keeps")
        if ep.bytes + each * len(new) > self._max_bytes:
            raise StreamError(f"episode {episode_id} would hold {ep.bytes + each * len(new)} bytes of observations "
                              f"its policy has not read, more than the {self._max_bytes} a server keeps")
        if self._bytes + each * len(new) > self._max_worker:
            raise StreamError(f"this server would hold {self._bytes + each * len(new)} bytes of observations, more "
                              f"than the {self._max_worker} it keeps")
        if blocks:
            self._keep_blocks(episode_id, ep, blocks)
            # kept until the post's last frame is turned back: its robot carried one again for a later frame of it,
            # counting it no longer held there, which the count drops on the way (_advance)
            last = max((s for s, _ in frames), default=ep.through)
            for bid in blocks:
                ep.pins[bytes(bid)] = max(ep.pins.get(bytes(bid), last), last)
        for s, v in new:
            ep.frames[s] = (v, each)
        for s, v in again:
            ep.frames[s] = (v, ep.frames[s][1])           # the same observation, its bytes counted once
        ep.bytes += each * len(new)
        self._bytes += each * len(new)
        ep.skipped.update(s for s in skipped if s > ep.through)
        if again or blocks:
            ep.missing = None                             # sent again, or blocks came: turned back once more
        self._advance(ep)
        ep.arrived.set()
        return ep.through

    def _shed(self, ep: _Episode, count: int, size: int) -> None:
        """Room in `ep`, and in this server, for `count` more observations of `size` bytes, made by letting go the
        episode's oldest kept here - never what the post brings. One let go is as good as its policy having had it: an
        act waits for none of them (each counted as gone, or left out: _first_unobserved), and what comes after goes
        on; a video's frames after one let go are decoded from its next keyframe, a second away at most."""
        for s in sorted(ep.frames):
            if (len(ep.frames) + count <= self._max_frames and ep.bytes + size <= self._max_bytes
                    and self._bytes + size <= self._max_worker):
                return
            kept = ep.frames.pop(s)
            ep.bytes -= kept[1]
            self._bytes -= kept[1]
            ep.shed += 1
            if s <= ep.through:
                ep.forwarded = s if ep.forwarded is None else max(ep.forwarded, s)
            else:
                ep.skipped.add(s)

    def shed(self, episode_id: str | None) -> int:
        """How many of the episode's observations were let go unread (put's shed): 0 for none, or for an episode
        gone."""
        ep = self._eps.get(episode_id) if episode_id else None
        return ep.shed if ep is not None else 0

    def posted(self, episode_id: str | None) -> int | None:
        """The bytes the episode's posts came in since this was last asked - what its robot sent for the act that asks,
        an act carrying no data of its own - or None for none."""
        ep = self._eps.get(episode_id) if episode_id else None
        if ep is None or not ep.posted:
            return None
        sent, ep.posted = ep.posted, 0
        return sent

    def resolved(self, episode_id: str) -> list[tuple[int, object]]:
        """The episode's observations turned back since this was last asked, (seq, inputs) in order: each as its robot
        built it - what a recorder and a standby's saves keep of each step."""
        ep = self._eps.get(episode_id)
        if ep is None or not ep.fresh:
            return []
        out, ep.fresh = ep.fresh, []
        return out

    def _advance(self, ep: _Episode) -> None:
        """The episode whole as far as it goes: each next number skipped, or kept and turned back (its blocks'
        references made what its robot built, what the episode holds then counted as its robot counts it) - stopping at
        the first that names a block this server does not hold, which its next act is refused from (ep.missing). A block
        the count lets go is kept while a later frame of the post that brought it is still to come (ep.pins), and goes
        once that post is turned back, if the count still lets it go."""
        while ep.missing is None:
            s = ep.through + 1
            if s in ep.frames:
                raw, size = ep.frames[s]
                ids = blocks_codec.ids_of(raw)
                if ids:
                    try:
                        value = blocks_codec.decode(raw, ep.blocks)
                    except blocks_codec.MissingBlock:
                        ep.missing = s
                        break
                    for bid in ep.retention.use(ids):
                        if ep.pins.get(bid, s) <= s:
                            self._drop_block(ep, bid)
                    ep.frames[s] = (value, size)
                ep.fresh.append((s, ep.frames[s][0]))
            elif s not in ep.skipped:
                break
            ep.through = s
        for bid in [b for b, last in ep.pins.items() if last <= ep.through]:
            del ep.pins[bid]
            if not ep.retention.holds(bid):
                self._drop_block(ep, bid)

    def _keep_blocks(self, episode_id: str, ep: _Episode, blocks: dict[bytes, bytes]) -> None:
        """A post's block contents into its episode's table, those it holds already left as they are: the episode past
        what one keeps refused (StreamError); the server past max_worker_block_bytes makes room by dropping the table of
        the episode idle longest - its robot sends again what it then lacks."""
        add = {bytes(bid): bytes(c) for bid, c in blocks.items() if bytes(bid) not in ep.blocks}
        grow = sum(len(c) for c in add.values())
        if ep.block_bytes + grow > self._max_bytes:
            raise StreamError(f"episode {episode_id} would hold {ep.block_bytes + grow} bytes of blocks, more than the "
                              f"{self._max_bytes} a server keeps")
        for other in sorted((e for e in self._eps.values() if e is not ep and e.blocks), key=lambda e: e.used):
            if self._block_bytes + grow <= self._max_blocks:
                break
            for bid in list(other.blocks):
                self._drop_block(other, bid)
        if self._block_bytes + grow > self._max_blocks:
            raise StreamError(f"this server would hold {self._block_bytes + grow} bytes of blocks, more than the "
                              f"{self._max_blocks} it keeps")
        ep.blocks.update(add)
        ep.block_bytes += grow
        self._block_bytes += grow

    def _drop_block(self, ep: _Episode, bid: bytes) -> None:
        content = ep.blocks.pop(bid, None)
        if content is not None:
            ep.block_bytes -= len(content)
            self._block_bytes -= len(content)

    async def forward(self, episode_id: str,
                      observe: Callable[[str, list, Callable[[], None]], Awaitable[list]]) -> None:
        """For a policy that takes its inputs by observe: the frames of the episode that are whole and not yet sent go
        to its copy in order, all there are at once (`observe(episode_id, [(seq, inputs), ...], handed)`, its answer
        to each in order) - `handed()` said once they are in its copy's queue ahead of any act of the episode that
        reaches the copy after, which an act waits for (before); a frame it answers {"ok": False} on ends it - no frame
        of the episode goes to it any more, and the copy names that frame to every act of the episode. Frames it cannot
        take yet (Deferred) stay and go again in a moment, while the episode is here. One forwarding at a time an
        episode: what a post brings while it runs goes in its next round."""
        ep = self._eps.get(episode_id)
        if ep is None or ep.forwarding or ep.failed:
            return
        ep.forwarding = True
        wait = _DEFERRED_FIRST_S
        try:
            while not ep.failed and self._eps.get(episode_id) is ep:
                done = _gone_to(ep)
                if done >= ep.through:
                    break
                last, frames, taken = ep.through, [], []
                for s in range(done + 1, last + 1):
                    kept = ep.frames.pop(s, None)
                    if kept is not None:
                        ep.bytes -= kept[1]
                        self._bytes -= kept[1]
                        frames.append((s, kept[0]))
                        taken.append((s, kept))

                def handed(last: int = last) -> None:
                    ep.handed = last if ep.handed is None else max(ep.handed, last)
                    ep.arrived.set()

                try:
                    answers = await observe(episode_id, frames, handed) if frames else []
                except Deferred as exc:
                    ep.deferred = str(exc) or "no copy here can take it yet"
                    ep.deferred_no_place = exc.no_place   # no copy here can take it, not one busy for a moment
                    for s, kept in taken:                 # kept as they were, to go again
                        ep.frames[s] = kept
                        ep.bytes += kept[1]
                        self._bytes += kept[1]
                    await asyncio.sleep(wait)
                    wait = min(2 * wait, _DEFERRED_MAX_S)
                    continue
                wait = _DEFERRED_FIRST_S
                ep.deferred, ep.deferred_no_place = None, False  # a copy took them
                if any(not (isinstance(a, dict) and a.get("ok")) for a in answers):
                    ep.failed = True
                ep.forwarded = last if ep.forwarded is None else max(ep.forwarded, last)
                handed()
        finally:
            ep.forwarding = False
            ep.arrived.set()

    async def before(self, episode_id: str, n: int) -> None:
        """For the act of a policy that takes its inputs by observe: once its copy observed, in order, every observation
        of the episode before `n` - or has it in its copy's queue ahead of the act (forward's `handed`: the act's batch
        takes them first) - how many its robot sent before the act, the number its next takes - STREAM_WAIT_S at most,
        else StreamError (missing) naming the first not yet observed, which the robot sends again from there. The act
        is no observation and takes no number, so nothing is consumed, and another act may come at the same `n`; a frame
        before `n` sent again is answered and not kept. A copy that refused a frame waits for nothing: the act says
        which."""
        self._expire()
        ep = self._eps.get(episode_id)
        if ep is None:
            ep = self._eps[episode_id] = _Episode(self._clock())
        deadline = self._clock() + self._wait_s
        while True:
            ep.used = self._clock()
            first = _first_unobserved(ep, n)
            if ep.failed or first is None:
                break
            if ep.missing is not None and ep.missing < n:
                raise self._lacking(episode_id, ep)       # a block not held: no wait brings it
            if self._refuse_gap_early and ep.through + 1 < n and any(s > ep.through + 1 for s in ep.frames):
                # a later observation is here and this one is not: on the robot's stream they come in order, so it is
                # not on its way - sent again now, not after the wait
                raise StreamError(f"observation {ep.through + 1} of episode {episode_id} did not come, and later ones "
                                  f"did", missing=True, first=ep.through + 1)
            left = deadline - self._clock()
            if left <= 0:
                if ep.through >= n - 1:
                    # every one came, and the copy has not taken them: it is still in an earlier call - busy, which its
                    # robot waits out, never "did not come", which would send them again for nothing
                    raise _busy(episode_id, ep)
                raise StreamError(f"the observations of episode {episode_id} from {first} to {n - 1} did not reach its "
                                  f"policy within {self._wait_s:.0f} s", missing=True, first=first)
            ep.arrived.clear()
            try:
                await asyncio.wait_for(ep.arrived.wait(), timeout=left)
            except asyncio.TimeoutError:
                pass

    async def caught_up(self, episode_id: str) -> None:
        """For a planner's read of the episode: every observation of it that came before the read handed to its copy
        first - the wait an act makes for the ones its robot sent before it (before) -, so the read is never of the copy
        as it was before the newest of them, nor of no copy at all for an episode whose first frames are still on their
        way to one. STREAM_WAIT_S at most; past it - a copy that cannot take them yet, one still in an earlier call -
        the read is of what its copy has."""
        ep = self._eps.get(episode_id)
        if ep is None or ep.through < 0:
            return
        try:
            await self.before(episode_id, ep.through + 1)
        except StreamError:
            pass

    def stalled(self, episode_id: str) -> bool:
        """Whether the episode holds frames that never went on to its copy, with nothing forwarding them: they came
        while no copy here was ready to take them - its policy still loading - and forwarding starts on a post, while a
        robot that waits for a plan of its own posts nothing more. Its act or its planner's read forwards them then."""
        ep = self._eps.get(episode_id)
        return ep is not None and not ep.failed and not ep.forwarding and _gone_to(ep) < ep.through

    def waiting(self, episode_id: str) -> str | None:
        """Why the episode's frames wait for a copy here - its server still starting, no copy with room for it yet
        (forward's Deferred) -, None when they do not, or when no copy here will take it at all (no_place)."""
        ep = self._eps.get(episode_id)
        if ep is None or ep.failed or ep.deferred_no_place:
            return None
        return ep.deferred

    def resume(self, episode_id: str, through: int) -> None:
        """An episode read back on this copy from its saved state (a switch to its standby): its observations up to
        `through` went to its policy on the copy it left, and the state it was read back with holds them - so here it
        begins at through + 1: what was observed and taken is `through` - the next forward and act wait on the frames
        after it alone; and a frame at or before it, sent again by its robot from its last answered act, is answered and
        not kept. Called once its state is read back, before its first call here."""
        self._expire()
        ep = self._eps.get(episode_id)
        if ep is None:
            ep = self._eps[episode_id] = _Episode(self._clock())
        ep.used = self._clock()
        through = int(through)
        # whole and observed through it - and on over the frames after it already here
        ep.through = max(ep.through, through)
        ep.forwarded = through if ep.forwarded is None else max(ep.forwarded, through)
        # what this copy kept at or before it (frames sent before the state was read back): its policy has them
        for s in [s for s in ep.frames if s <= through]:
            kept = ep.frames.pop(s)
            ep.bytes -= kept[1]
            self._bytes -= kept[1]
        ep.skipped = {s for s in ep.skipped if s > through}
        self._advance(ep)
        ep.arrived.set()

    def _lacking(self, episode_id: str, ep: _Episode) -> StreamError:
        """The refusal of an act after an observation that names a block this server does not hold: from it, which its
        robot sends again with every block's content (409 frames_missing)."""
        return StreamError(f"observation {ep.missing} of episode {episode_id} names a block this server does not "
                           f"hold", missing=True, first=ep.missing)

    def end(self, episode_id: str) -> None:
        """The episode ended: everything kept of it goes, its blocks too."""
        ep = self._eps.pop(episode_id, None)
        if ep is not None:
            self._bytes -= ep.bytes
            self._block_bytes -= ep.block_bytes
            ep.arrived.set()

    def _expire(self) -> None:
        """Drop an episode with no post or act for its TTL (a robot that went without ending it)."""
        now = self._clock()
        for eid in [e for e, ep in self._eps.items() if now - ep.used > self._ttl_s and not ep.forwarding]:
            self.end(eid)
