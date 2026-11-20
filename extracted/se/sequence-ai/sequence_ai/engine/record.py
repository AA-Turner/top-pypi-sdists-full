# SPDX-FileCopyrightText: Copyright (c) 2026 General Sequences Company
# SPDX-License-Identifier: Apache-2.0
"""
The robot's record in its episode: episode.state["seq.observations"] - {step: the observation as the robot sent it,
its video, depth and tactile still compressed} - and episode.state["seq.actions"] - {step: what the act after that
step's observation answered} - kept as the episode goes, for a policy whose functions are handed `episode`: about its
last minute. A policy reads its own robot's recent history there; a frame of it is decoded with
sequence_base.codec.marked.frames. A deployment's worker and a policy server of your own keep it alike, this one module
in both.

In one sentence: a frame reaches the server (an observation streamed) → frame() keeps it at its step and notes when →
an act's answer → answer() keeps it at the step of the newest observation before it → trim() lets the steps kept longer than RECORD_S go, oldest first, and the steps after them up to their video's next
keyframe (a frame there has nothing to decode from) → what a server saves of an episode takes the rest of
episode.state as state_of() makes it storable - what the policy kept, and seq.plans, neither of them cut.

WHY the record lives in episode.state: the observations are the robot's state, and each answer is appended to it as it
leaves, so a policy and its plan read the robot's recent history where they read everything else of the episode.
Compressed, not decoded: a minute of decoded camera frames is hundreds of megabytes, and a policy decodes the frames it
reads. The policy's own keys are made storable once, at the episode's end: copying them off a GPU every step would hold
up the act.

WHY a minute, counted in time: the record keeps only the recent past - a recorder that wants every step reads each as it
comes - and neither the machine's memory nor a size decides it.
"""
from __future__ import annotations

import sys
import time
from collections import OrderedDict
from typing import Any

import numpy as np

OBSERVATIONS, ACTIONS, PLANS = "seq.observations", "seq.actions", "seq.plans"
# How long a step stays in the record: about the episode's last minute, its oldest steps going first.
RECORD_S = 60.0
# How many steps past those the record lets go at most while it looks for a keyframe to begin at.
_ANCHOR_STEPS = 120
# torch's float types numpy has no dtype for: stored as float32 (torch is looked up, never imported, here)
_NARROW_FLOATS = ("bfloat16", "float8_e4m3fn", "float8_e5m2", "float8_e4m3fnuz", "float8_e5m2fnuz")


class Record:
    """One episode's record kept count of: its steps in order, each with when it was first kept (time.monotonic()), and
    the newest observation's step."""

    __slots__ = ("kept_at", "last_step")

    def __init__(self) -> None:
        self.kept_at: OrderedDict = OrderedDict()
        self.last_step: int | None = None


# What a key of the server's starts with: seq.observations, seq.actions, seq.plans and any it adds. An observation
# holding one would read as the server's.
RESERVED_PREFIX = "seq."


def reserved_refused(value: Any) -> str | None:
    """Why an observation cannot be taken, holding a top-level key of the platform's, or None."""
    if isinstance(value, dict):
        for key in value:
            if isinstance(key, str) and key.startswith(RESERVED_PREFIX):
                return (f'"{key}" is the platform\'s: keys that start with "{RESERVED_PREFIX}" cannot be observed, '
                        "so name it something else")
    return None


def frame(episode: Any, rec: Record, step: int, value: Any) -> None:
    """An observation of the episode at `step`, as the robot sent it; a step sent again (the robot resends what a worker
    missed) keeps the newer, in its place."""
    episode.state.setdefault(OBSERVATIONS, {})[step] = value
    rec.kept_at.setdefault(step, time.monotonic())
    rec.last_step = step if rec.last_step is None else max(rec.last_step, step)
    trim(episode, rec)


def answer(episode: Any, rec: Record, value: Any) -> None:
    """What an act of the episode answered, at the step of the newest observation before it (0 before any); a second act
    at one step keeps the newer answer."""
    step = rec.last_step if rec.last_step is not None else 0
    episode.state.setdefault(ACTIONS, {})[step] = storable(value)[0]
    rec.kept_at.setdefault(step, time.monotonic())
    trim(episode, rec)


def restored(episode: Any, rec: Record, observations: dict, actions: dict) -> None:
    """The record of an episode that began on another server, as it was saved there (a standby's checkpoint): each
    step's observation and answer back in place, in order, kept from now - its minute counted again from here."""
    now = time.monotonic()
    for step in sorted(set(observations) | set(actions)):
        if step in observations:
            episode.state.setdefault(OBSERVATIONS, {})[step] = observations[step]
            rec.last_step = step if rec.last_step is None else max(rec.last_step, step)
        if step in actions:
            episode.state.setdefault(ACTIONS, {})[step] = actions[step]
        rec.kept_at.setdefault(step, now)


def from_keyframe(observations: dict, through: int) -> list:
    """The steps of `observations` a decoder begins at to stand where it stood after `through`: from the newest at or
    before it whose video frames are all keyframes, in order - all of them up to it when none is."""
    steps = sorted(s for s in observations if s <= through)
    for i in range(len(steps) - 1, -1, -1):
        if not _mid_stream(observations[steps[i]]):
            return steps[i:]
    return steps


def trim(episode: Any, rec: Record) -> None:
    """The steps kept longer than RECORD_S let go, oldest first - never the newest - then the steps after them whose
    video starts mid-stream, until one begins at a keyframe (at most _ANCHOR_STEPS more)."""
    now, old = time.monotonic(), 0
    while len(rec.kept_at) > 1 and now - next(iter(rec.kept_at.values())) > RECORD_S:
        _drop(episode, rec, next(iter(rec.kept_at)))
        old += 1
    if not old:
        return
    for _ in range(_ANCHOR_STEPS):
        if len(rec.kept_at) <= 1:
            return
        first = next(iter(rec.kept_at))
        if not _mid_stream(episode.state.get(OBSERVATIONS, {}).get(first)):
            return
        _drop(episode, rec, first)


def _mid_stream(value: Any) -> bool:
    """Whether an observation holds a video frame that is no keyframe: one a decoder cannot begin at."""
    if isinstance(value, dict):
        if value.get("codec") == "h264" and "kf" in value:
            return not value.get("kf")
        return any(_mid_stream(v) for v in value.values())
    if isinstance(value, list):
        return any(_mid_stream(v) for v in value)
    return False


def _drop(episode: Any, rec: Record, step) -> None:
    episode.state.get(OBSERVATIONS, {}).pop(step, None)
    episode.state.get(ACTIONS, {}).pop(step, None)
    rec.kept_at.pop(step, None)


def storable(value: Any, path: str = "") -> tuple[Any, list[str]]:
    """`value` as storage carries it - JSON values, numpy arrays and bytes - and the paths of what it cannot carry, left
    out: a torch tensor as a numpy array of its dtype (copied off its device once; bfloat16 and the float8 types as
    float32, complex32 as complex64), a model's fields as a dict, a map's keys as strings; a model object, an open file
    or anything else that is no data is skipped and named."""
    if value is None or isinstance(value, (bool, int, float, str)):
        return value, []
    if isinstance(value, (bytes, bytearray, memoryview)):
        return bytes(value), []
    if isinstance(value, np.ndarray):
        return (np.array(value, copy=True), []) if value.dtype != object else (None, [path or "."])
    if isinstance(value, np.generic):
        return value, []
    torch = sys.modules.get("torch")
    if torch is not None and isinstance(value, torch.Tensor):
        t = value.detach()
        if any(t.dtype == getattr(torch, n, None) for n in _NARROW_FLOATS):
            t = t.float()
        elif t.dtype == getattr(torch, "complex32", None):
            t = t.to(torch.complex64)
        return t.cpu().numpy(), []
    dump = getattr(value, "model_dump", None)
    if callable(dump) and hasattr(type(value), "model_fields"):
        return storable(dump(mode="python"), path)
    if isinstance(value, dict):
        out, skipped = {}, []
        for k, v in value.items():
            kept, more = storable(v, f"{path}.{k}" if path else str(k))
            skipped += more
            if not more or kept is not None:
                out[str(k)] = kept
        return out, skipped
    if isinstance(value, (list, tuple)):
        out, skipped = [], []
        for i, v in enumerate(value):
            kept, more = storable(v, f"{path}[{i}]")
            skipped += more
            out.append(kept)
        return out, skipped
    return None, [path or "."]


def state_of(episode: Any) -> dict:
    """What storage keeps of an episode at its end: {"state": every key of episode.state but the record's own two - what
    the user's code kept, and seq.plans - made storable, none of it cut, "skipped": the paths of what could not be}. The
    record's observations and answers were stored step by step already."""
    out, skipped = {}, []
    for k, v in list(episode.state.items()):
        if k in (OBSERVATIONS, ACTIONS):
            continue
        kept, more = storable(v, str(k))
        skipped += more
        if not more or kept is not None:
            out[str(k)] = kept
    return {"state": out, "skipped": skipped}
