# SPDX-FileCopyrightText: Copyright (c) 2026 General Sequences Company
# SPDX-License-Identifier: Apache-2.0
"""
The observation format on the copy of a policy that serves an episode: each observed frame's marked items - the robot's
sequence_ai.Video, Depth and Tactile - turned back into the arrays the robot marked before the policy's observe function
reads the frame; and each episode's latest observation, which an act of a policy with no observe function of its own is
handed (an act carries no data: every observation comes by observe). The same code serves a robot on a GPU of your own
(serve()) and on the hosted platform.

    observed = Observed()
    value = observed.take(episode_id, seq, frame)      # the frame as the robot built it, or DROPPED
    latest = observed.latest(episode_id)               # what an act is handed

In one sentence: a frame comes in (its episode and its step) → take() turns its marked items back with the episode's
decoders (sequence_base.codec.marked.Streams) - the rest of it untouched, the same objects - and keeps it as the
episode's latest observation → latest() is that observation, for the act function; end() drops both. A frame one of
whose video items follows a gap in its stream and is no keyframe is left out (DROPPED) until that stream's next
keyframe: nothing before it to decode it from - frames the robot left out, a post the server refused - and its episode
goes on.

WHY the latest alone: the server keeps the one observation an act needs and nothing more - what a policy wants of the
ones before it, it keeps itself (episode.state).
WHY a gap is left out, not the episode's end: a robot sends an episode's video several posts at a time, and a later
post's frames can be kept before an earlier one is refused; it then forces a keyframe, so about a round trip's frames
are left out, where ending the episode would stop the robot.

Needs sequence-base's codecs where a frame holds a marked item (sequence-ai installs them on Python 3.10 or later).
"""
from __future__ import annotations

import collections
import logging
from typing import Any, Callable, Optional

from sequence_base.codec import marked

__all__ = ["DROPPED", "EPISODES_KEPT", "NO_FRAME", "NoObservation", "Observed", "holds_mark", "no_frame"]

log = logging.getLogger("sequence_ai.serve")

EPISODES_KEPT = 64            # episodes a copy keeps decoders and a latest observation for, the least recently observed
                              # dropped (an episode's end drops them at once)


def holds_mark(value: Any) -> bool:
    """Whether `value` holds a marked item's map, in dicts and lists at any depth."""
    if isinstance(value, dict):
        return marked.is_marked(value) or any(holds_mark(v) for v in value.values())
    if isinstance(value, list):
        return any(holds_mark(v) for v in value)
    return False


# What take() returns for a frame it left out: its policy is handed nothing of it, and the episode's latest stays.
DROPPED = object()
# A frame of a robot connected through a planner that held nothing but what its planner reads, in place of its inputs:
# its copy makes the episode, which a plan needs to land in, and hands its policy nothing.
NO_FRAME = {"__seq_no_frame__": True}


def no_frame(value: Any) -> bool:
    """Whether a frame is NO_FRAME, as it comes over the copy's channel: by its shape, never `==`, which an array the
    robot observed would answer element by element."""
    return isinstance(value, dict) and len(value) == 1 and value.get("__seq_no_frame__") is True


class NoObservation(LookupError):
    """An act of an episode no observation has come for: there is nothing for its act function yet."""

    def __init__(self, episode_id: Optional[str]) -> None:
        self.episode_id = episode_id
        super().__init__(f"episode {episode_id} has no observation yet: observe(x) before act()")


class Observed:
    """One copy's episodes: their decoders and their latest observation. `say(line)`: where a gap in an episode's video
    is told, where it began and where it was whole again (the server's log unless given)."""

    def __init__(self, say: Optional[Callable[[str], None]] = None) -> None:
        # episode -> [its Streams, its latest, the frames left out since its video was last whole]
        self._episodes: collections.OrderedDict = collections.OrderedDict()
        self._say = say if say is not None else log.info

    def take(self, episode_id: Optional[str], step: Optional[int], frame: Any) -> Any:
        """`frame` with its marked items turned back into their arrays - the same objects where nothing is marked -
        kept as the episode's latest observation; DROPPED, the latest as it was, for one with a video item that follows
        a gap in its stream and is no keyframe (marked.NeedsKeyframe). Raises marked.MarkedError for an item that does
        not read. Each gap is told twice, where it began and where its video was whole again."""
        ep = self._episodes.get(episode_id)
        if ep is None:
            ep = self._episodes[episode_id] = [marked.Streams(), _NONE, 0]
            while len(self._episodes) > EPISODES_KEPT:
                self._episodes.popitem(last=False)
        else:
            self._episodes.move_to_end(episode_id)
        if holds_mark(frame):
            gaps: list = []
            out = _decoded(frame, ep[0], (), gaps)
            if gaps:
                if not ep[2]:
                    named = ", ".join(".".join(str(k) for k in path) or "the frame" for path in gaps)
                    self._say(f"episode {episode_id}: frame {step}'s {named} follows a gap in its stream and is no "
                              "keyframe - frames left out until its next keyframe")
                ep[2] += 1
                return DROPPED
            if ep[2]:
                self._say(f"episode {episode_id}: whole again at frame {step}, {ep[2]} left out")
                ep[2] = 0
        else:
            out = frame
        ep[1] = out
        return out

    def latest(self, episode_id: Optional[str]) -> Any:
        """The episode's newest observation, as its observe function would be handed it. NoObservation for an episode
        none has come for."""
        ep = self._episodes.get(episode_id)
        if ep is None or ep[1] is _NONE:
            raise NoObservation(episode_id)
        return ep[1]

    def end(self, episode_id: Optional[str]) -> None:
        """The episode ended: its decoders and its latest observation go."""
        self._episodes.pop(episode_id, None)


_NONE = object()             # an episode no observation has come for


def _decoded(value: Any, streams: marked.Streams, path: tuple, gaps: list) -> Any:
    """marked.decode, each marked item on its own: one that follows a gap in its stream and is no keyframe noted in
    `gaps` (its path), and the others decoded all the same - a stream with no gap of its own fed every frame, so it goes
    on without a keyframe. Decoded only up to the first item that needs one, another camera of the same frame would
    have had a gap of its own, and waited for its own keyframe, up to a second of the robot's clock."""
    if isinstance(value, dict):
        if marked.is_marked(value):
            try:
                return streams.decoder(path, value).decode(value)
            except marked.NeedsKeyframe:
                gaps.append(path)
                return None
        if not holds_mark(value):
            return value
        return {k: _decoded(v, streams, path + (k,), gaps) for k, v in value.items()}
    if isinstance(value, list):
        if not holds_mark(value):
            return value
        return [_decoded(v, streams, path + (i,), gaps) for i, v in enumerate(value)]
    return value
