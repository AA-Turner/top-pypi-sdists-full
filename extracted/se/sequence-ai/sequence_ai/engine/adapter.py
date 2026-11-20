# SPDX-FileCopyrightText: Copyright (c) 2026 General Sequences Company
# SPDX-License-Identifier: Apache-2.0
"""
A `@seq.policy` class as the server runs it: its class built, its acts answered, each robot's episode kept from its
start to its end, its observations handed to its observe function, its plans run - a deployment's worker and a policy
server of your own (`seq serve`) alike, this one class in both.

    adapter = RegisteredAdapter(cls, registered)     # registered.registration: what @seq.policy attached to cls
    adapter.load(weights_dir)                        # the class built by its init=, its weights' folder filled in
    adapter.observe(frame, episode_id="e1", seq=0)   # each observation of an episode, in order
    adapter.infer(episode_id="e1")                   # an act, which carries no data
    adapter.episode_reset("e1")                      # the episode's end: its on_episode run with phase "end"

In one sentence: its methods are the ones its decorators mark - @seq.infer (its act function), @seq.observe,
@seq.on_episode, @seq.shutdown, @seq.plan, @seq.sample - recovered by SeqFlags bit, never by name → each episode's
seq.Episode made at its first act or frame, on_episode run as it begins (phase "start") and as it ends ("end"), the same
object between → each frame kept as the episode's latest observation, its marked items turned back (engine.obs_format),
handed to the observe function where there is one, kept in the episode's record (engine.record) → an act calls the act
function with none beside an observe function, else hands it the episode's latest observation - whole to one argument,
by name to two or more without a default - its inputs converted as its annotations say (engine.convert), a
@seq.concurrent batch stacked (engine.stack) → its plan, on its clock (engine.plan_clock), reads a view of the episode
(engine.robot_view).

Two things a host may replace, as module attributes: `say(line)`, how a line for the server's log is said (printed,
unless set), and, through engine.plan_clock, `plan_clock.described(exc)`, how an error is said.
"""
from __future__ import annotations

import asyncio
import inspect
import os
import sys
import threading
import time
from collections import OrderedDict
from typing import Any

from sequence_base import ActionChunk, Observation, SeqFlags
from sequence_base.by_name import INFER_PLATFORM, OBSERVE_PLATFORM, RESET_GONE, plan_refused, wake_on_refused
from sequence_base.episode import Episode, answered, at

from . import convert, obs_format, plan_clock, record
from . import robot_view as robot
from . import thumbnails as view
from .convert import ConversionError


def io_mode_of(infer: Any) -> str:
    """Which I/O a policy's infer speaks. "robot_arm": it is written against the preset — its first argument annotated
    `Observation` or its return annotated `ActionChunk` — so the worker parses its episode's latest observation into an
    Observation and sends the chunk back. "raw": anything else — the worker hands it the observation untouched and
    returns whatever it answers."""
    try:
        sig = inspect.signature(infer)
    except (TypeError, ValueError):
        return "robot_arm"
    positional = [p for p in sig.parameters.values()
                  if p.kind in (inspect.Parameter.POSITIONAL_ONLY, inspect.Parameter.POSITIONAL_OR_KEYWORD)]
    first = positional[0].annotation if positional else inspect.Parameter.empty

    def _names(annotation, cls) -> bool:
        # `from __future__ import annotations` leaves strings; a dotted or bare name both count.
        # A quoted annotation under `from __future__ import annotations` arrives with its quotes: "'ActionChunk'".
        return annotation is cls or (isinstance(annotation, str)
                                     and annotation.strip("'\"").rsplit(".", 1)[-1] == cls.__name__)

    return "robot_arm" if _names(first, Observation) or _names(sig.return_annotation, ActionChunk) else "raw"


# The most calls a sample episode may hold: as many as a worker keeps of an episode's observations between two acts -
# an episode of every observation and an act every few, played whole by the build check.
MAX_SAMPLE_CALLS = 1024


def sample_of(method: Any) -> list | None:
    """A policy's sample episode (SeqFlags.SAMPLE): what its sample= method returns - one episode's calls, in order, as
    a robot makes them: ("observe", what its observe() hands over) and ("act",) for its act(), which carries nothing -
    every input goes through observe - checked to be a list of 1 to MAX_SAMPLE_CALLS holding an act; None when it names
    none. An act that carries something, and an act's inputs alone as sample= took them before, are refused saying to
    hand them to an observe before the act."""
    if method is None:
        return None
    got = method()
    if not isinstance(got, (list, tuple)) or not got:
        what = "an empty list" if isinstance(got, (list, tuple)) else f"a {type(got).__name__}"
        raise TypeError(f"sample= returned {what}: it returns one episode's calls, in order - {_CALLS_SAID}")
    if len(got) > MAX_SAMPLE_CALLS:
        raise TypeError(f"sample= returned {len(got)} calls: a sample episode holds at most {MAX_SAMPLE_CALLS}")
    calls = []
    for i, call in enumerate(got):
        kind = call[0] if isinstance(call, (list, tuple)) and call and isinstance(call[0], str) else None
        if kind == "act" and len(call) > 1:
            raise TypeError(f'sample= returned [{i}] as ("act", ...): an act carries nothing - put what it carries in '
                            'an ("observe", ...) just before it, and write the act ("act",)')
        if kind is None or SAMPLE_CALLS.get(kind) != len(call):
            alone = "" if kind is not None else \
                ' - an act\'s inputs alone, as sample= took them before: write each ("observe", ...) and then ("act",)'
            raise TypeError(f"sample= returned [{i}] as {_call_said(call)}{alone}; each call is {_CALLS_SAID}")
        calls.append(tuple(call))
    if not any(call[0] == "act" for call in calls):
        raise TypeError('sample= returned no act: the check times its acts - give it at least one ("act",)')
    return calls


# The calls a sample episode is made of, each with its length: the two a robot's code calls - an observe with what it
# hands over, an act with nothing.
SAMPLE_CALLS = {"observe": 2, "act": 1}
_CALLS_SAID = '("observe", what observe() is handed) or ("act",) for an act(), which carries nothing'


def _call_said(call) -> str:
    if isinstance(call, (list, tuple)):
        return f"a {type(call).__name__} of {len(call)}" + (f" starting {call[0]!r}" if call else "")
    return f"a {type(call).__name__}"


class RegisteredAdapter:
    """A `@seq.policy` class presented as the one lifecycle surface its server calls - load, infer, infer_batch,
    observe, plan, sample, episode_reset, shutdown - one runtime for every shape, with no policy-specific branch.

    Its methods are the ones its decorators mark - @seq.infer (its act function), @seq.observe, @seq.on_episode,
    @seq.shutdown, @seq.plan, @seq.sample - recovered by SeqFlags bit, never by name, so the author may call them
    anything (a policy's @seq.reset is refused: RESET_GONE): the binding is the contract. Its constructor is its load:
    it is built at load(), its weights staged, by `cls()` - or, a class whose constructor takes the author's arguments
    (init=, PolicyConstructor), by its constructor, its config files read and its weights filled
    (sequence_base.construct.build) - and its methods keep their own names, so a subclass of a class from the author's
    repository runs here as it runs on the author's machine.

    What the server hands its functions beside their inputs is the episode (seq.Episode) and an eval's seed, each only
    when the function takes it. A policy that keeps its episodes - handed them (PolicySpec.episodes "shared": a copy
    serves several in turn) or keeping them on itself ("own": its observe function or @seq.on_episode beside an act
    function that takes no episode; an episode holds a copy of its own) - has each episode's Episode made at its
    first act or frame on this copy, @seq.on_episode handed it then (episode.phase "start") and at its end ("end"),
    the same object between; any other act is handed an Episode of its own.

    Its inputs come by observe: each frame of an episode to its observe function, oldest first, and kept as the
    episode's latest observation (obs_format); an act carries no data - it calls its act function with none beside an
    observe function, else hands it the episode's latest - whole to one argument, by name to two or more without a
    default (sequence_base.by_name)."""

    observes = False                 # whether it takes its inputs by observe, set once it is bound
    takes_latest = False             # whether a call hands its act function its episode's latest observation (_bind)

    def __init__(self, target: Any, reg: Any) -> None:
        registration = reg.registration
        self._names = dict(registration.bindings)
        self._constructor = registration.constructor
        self._spec, self._convert = registration.spec, None
        self._cls = target if isinstance(target, type) else type(target)
        if SeqFlags.RESET in self._names:
            raise TypeError(f"{self._cls.__name__}.{self._names[SeqFlags.RESET]}: {RESET_GONE}")
        module = sys.modules.get(self._cls.__module__)
        # its config files' paths are written from its file's folder, as on the author's machine
        self._base_dir = (os.path.dirname(os.path.abspath(module.__file__)) if getattr(module, "__file__", None)
                          else os.getcwd())
        self.episodes = registration.spec.episodes          # how it keeps an episode's state (PolicySpec.episodes)
        self.plan_every_s = registration.plan_every_s
        # what it is until it is built: no plan. The clock that plans this copy's episodes (its server sets it once it
        # is made): an episode's end stops its planning before anything else of it ends (_stop_planning), and an async
        # plan outside every clock runs on its loop. A plan asked for by its eval or its check, by episode (plan_start).
        self.plan_is_async, self.plan_wake_on, self.clock = False, None, None
        self._plan, self._asked = None, {}
        # how its answers play, as it declares them flat on itself - hz, action_chunk_valid_len, action_chunk_replan_at,
        # max_wait_for_batch, those it declares - which its server times a copy's robots by
        self.declared_plays = {k: getattr(registration.spec, k, None)
                               for k in ("hz", "action_chunk_valid_len", "action_chunk_replan_at", "max_wait_for_batch")
                               if getattr(registration.spec, k, None) is not None} or None
        # Each episode on this copy: its seq.Episode, the least recently used first - one beyond what the worker places
        # on this copy (an act's `keep`) going, an episode whose end never reached it; its decoders and latest
        # observation (obs_format); and the frame of it that failed - (its number, why), said by every act of the
        # episode until it ends.
        self._episodes: OrderedDict = OrderedDict()
        self._new_episode, self._answered = Episode, answered
        self._obs = obs_format.Observed(say=_say)
        self._failed: OrderedDict = OrderedDict()
        # what it is until it is built (one built by its constructor at load): one act a call, its own I/O
        self._inst = None
        self.io_mode, self.batch, self.observes = "raw", None, False
        self._sample = None
        if not isinstance(target, type):
            self._bind(target)               # an instance built elsewhere, as it is; a class is built at its load

    def _bind(self, instance: object) -> None:
        """Its methods off the built instance, and what each takes - decided once, from their signatures."""
        self._inst = instance
        method = self._method
        # @seq.infer alone is required
        self._infer = method(SeqFlags.INFER)
        self._observe = method(SeqFlags.OBSERVE)
        self._on_episode, self._shutdown = method(SeqFlags.ON_EPISODE), method(SeqFlags.SHUTDOWN)
        self._sample = method(SeqFlags.SAMPLE)
        # @seq.plan: beside its act function, called on each robot's clock with the robot alone,
        # what it returns kept in its episode's state - a plain one on a thread of its own, an async one on the clock's
        # event loop. `wake_on`, the keys whose arrival plans at once, is stashed on the method (no wire field).
        self._plan = method(SeqFlags.PLAN)
        self.plan_is_async = self._plan is not None and inspect.iscoroutinefunction(self._plan)
        named = self._names.get(SeqFlags.PLAN)
        wake = getattr(getattr(type(instance), named, None), "__seq_plan_wake_on__", None) if named else None
        said = wake_on_refused(wake)
        if said:
            raise TypeError(said)                   # in the SDK's words (sequence_base.by_name)
        self.plan_wake_on = frozenset(wake) if wake else None
        # What the platform hands each function, when it takes it, by name or **kwargs: an act function its episode and
        # an eval's seed - an `infer(self, obs)` without a seed is valid authoring, and passing it anyway raised
        # TypeError on every /act - an observe function its episode and the frame's step; @seq.on_episode its episode
        # always.
        self._infer_kw = _accepts(self._infer, ("seed", "episode"))
        self._observe_kw = _accepts(self._observe, ("step", "episode")) if self._observe is not None else set()
        # Its act function's annotations decide the I/O it speaks (io_mode_of): a PolicySpec holds no robot-arm contract
        # since contract 0.5.31, a kept one dropped as it is read (sequence_base contract.policy).
        self.io_mode = io_mode_of(self._infer)
        # It keeps its episodes - handed them, or on itself by its observe function or its hooks - each one's Episode
        # kept on this copy from its first act or frame to its end.
        self._keeps_episodes = (self.episodes is not None or self._observe is not None
                                or self._on_episode is not None)
        if self._plan is not None:
            # its plans are kept in its episode's Episode, which its act function must be handed and this copy keep
            why = plan_refused(self._plan, infer_takes_episode="episode" in self._infer_kw and self._keeps_episodes)
            if why:
                raise TypeError(why)                # in the SDK's words (sequence_base.by_name)
        # Handed its episodes by one of its functions: the robot's record is kept in each one's state, its observations
        # as they came and its acts' answers - none for a class that
        # never reads an Episode, which would only hold it.
        self._records = self._keeps_episodes and ("episode" in self._infer_kw or "episode" in self._observe_kw
                                                  or self._on_episode is not None)
        self._record: dict = {}                    # episode id -> its record.Record
        # What the Machines page is shown of an episode (robot_view): its newest step
        self._last_seq: dict = {}
        # An episode read back with no record of it (restore_episode: capture off, a standby's checkpoint keeps no frame
        # of a robot's) -> its state's newest frame: the frames its robot sends again up to it begin this copy's
        # decoders and record, never observed again (observe, _prime)
        self._primed: dict = {}
        # `@seq.concurrent(sizes=[...])`: what it stashed on the act function, {"sizes"} (the SDK restores the raw
        # function on the class, attribute and all), else None - one act per call. A batch hands it each act's inputs,
        # or a policy handed its episodes its episodes, as a list (infer_batch); never one that keeps them on itself:
        # each episode holds a copy of its own.
        raw_infer = getattr(type(instance), self._names[SeqFlags.INFER], None)
        self.batch = None if self.episodes == "own" else getattr(raw_infer, "__seq_concurrent__", None)
        # Whether a batch reaches its infer stacked (_stacked): what @seq.concurrent says (its `collate`, True by
        # default), since sequence-ai stacks no more itself.
        self._collated = bool(self.batch and self.batch["collate"])
        try:
            self._infer_defaults = {n: p.default for n, p in inspect.signature(self._infer).parameters.items()
                                    if p.default is not inspect.Parameter.empty}
        except (TypeError, ValueError):
            self._infer_defaults = {}
        # a function of its own I/O that takes two or more arguments without a default is handed what it takes by name,
        # each key to its argument (sequence_base.by_name, the SDK's rule when it was declared); None: whole - a
        # robot-arm preset's act function its Observation, always
        self._infer_by = _by_name(self._infer, INFER_PLATFORM) if self._observe is None and self.io_mode == "raw" \
            else None
        self._observe_by = _by_name(self._observe, OBSERVE_PLATFORM) if self._observe is not None else None
        # The inference parameters its observe function takes - its keyword arguments beside the frame and the
        # platform's step and episode (seq.registry.infer_params) - each episode's, as its act function gets them: None
        # for one that takes **kwargs (every one), none for one that takes its inputs by name - a camera's crop applied
        # as each frame comes, say
        self._observe_params = (_keywords(self._observe, OBSERVE_PLATFORM, skip_first=True) if self._observe is not None
                                and self._observe_by is None else frozenset())
        # ... and its act function's, beside its inputs when it takes them (none beside an observe function): one an
        # observe function alone declares never reaches it
        self._infer_params = (_keywords(self._infer, INFER_PLATFORM, skip_first=self._observe is None)
                              if self._infer_by is None else frozenset())
        # every input comes by observe - to its observe function, or kept as its episode's latest for its act function,
        # which a call hands it (one act at a time, or a batch of them each its own episode's; a robot-arm preset's as
        # its Observation) - and its server says it takes calls; a batch's episodes keep to their copies ("shared", as
        # the SDK seats every @seq.concurrent class)
        self.observes = True
        # its act function handed its episode's latest observation at a call (_act; a robot-arm preset's read by its
        # server first)
        self.takes_latest = self._observe is None

    def _method(self, flag: SeqFlags):
        """The method of the built instance its decorator marks for `flag`, or None for none marked."""
        name = self._names.get(flag)
        if not name:
            return None
        method = getattr(self._inst, name, None)
        if not callable(method):
            raise TypeError(f"{type(self._inst).__name__} has no method {name!r} ({_ARG.get(flag, 'a decorator')})")
        return method

    def _what(self, flag: SeqFlags) -> str:
        """The method its decorator marks for `flag`, as its errors say it: "Model.get_action"."""
        return f"{type(self._inst).__name__}.{self._names.get(flag)}"

    def load(self, weights_dir: Any) -> None:
        """Built now - its constructor is its load, run where the weights are staged: by `cls()`, or by its constructor
        with the author's arguments when it declares them (init=, construct)."""
        if self._inst is None:
            self._bind(construct(self._cls, self._constructor, base_dir=self._base_dir, weights=weights_dir))
        # what it declares of its inputs and answers, done where its code runs, last before its code (engine.convert)
        self._convert = convert.of(self._infer, io_mode=self.io_mode, observe=self._observe)

    def sample(self) -> list | None:
        """Its sample episode, when it names one (sample_of); played as an episode of its own, so its
        @seq.on_episode runs as it begins and as it ends."""
        return sample_of(self._sample)

    @property
    def has_sample(self) -> bool:
        """Whether it names a sample episode (@seq.sample): what its server's ready word says, so nothing asks for one
        of a policy that names none."""
        return self._sample is not None

    def infer(self, *, seed: int | None = None, episode_id: str | None = None, params: dict | None = None,
              keep: int | None = None, latest: Any = None) -> ActionChunk:
        """An act: it carries no data - its episode's observations came by observe, as they were made - and its act
        function is called as _act says. `latest`: its episode's latest observation as its server read it (a robot-arm
        preset's Observation), for an act function with no observe function; None, read here."""
        if self._inst is None:
            raise RuntimeError("the policy is not built yet: an act came before its load")
        # A @seq.concurrent infer that takes its acts stacked takes an act alone as a batch of one, as the batcher hands
        # it several: one shape, whatever path an act comes by - a build check's sample, a robot's act alone - so its
        # code reads one batch, never a lone observation beside it.
        if self._collated:
            return self.infer_batch(seeds=[seed], episode_ids=[episode_id], params=[params],
                                    keeps=[keep] if self._keeps_episodes else None,
                                    latest=None if latest is None else [latest])[0]
        # its episode's Episode, kept on this copy for a policy that keeps its episodes - any other's an episode of its
        # own
        episode = self._episode_of(episode_id, keep) if self._keeps_episodes else None
        if self._observe is not None:
            self._raise_failed(episode_id)
        # The request's inference parameters: the transport already refused any name the policy does not declare
        # and cast each to its declared type, so those its act function takes go straight to it as keyword arguments.
        kwargs: dict = self._taking(params, self._infer_params)
        if "seed" in self._infer_kw:
            kwargs["seed"] = seed
        # Handed only to an infer that takes it: a @seq.concurrent class seats "shared" (each act's place on a copy)
        # whether its infer takes `episode` or not, and an infer(obs, *, seed) handed one would fail with "unexpected
        # keyword argument 'episode'"
        if "episode" in self._infer_kw:
            kwargs["episode"] = episode if episode is not None else self._new_episode(episode_id or "")
        out = self._act(latest, kwargs, episode_id)
        answer = self._convert.answer(out) if self._convert is not None else out
        if episode is not None:
            if self._records:
                record.answer(episode, self._rec(episode_id), answer)
            self._answered(episode)
        return answer

    def observe(self, frame: Any, *, episode_id: str | None = None, seq: int | None = None,
                params: dict | None = None) -> dict:
        """One frame of an episode as the stream brings it, in order: kept as its
        episode's latest observation, its marked items turned back (obs_format), and handed to its observe function,
        when it has one, now, off its act's path - an episode's first frame, which may come before any act, making its
        Episode and running its @seq.on_episode start.
        A frame that does not read, or that its observe function raises on, is kept and named by every act of the
        episode until it ends, and later frames are observed no more: {"ok": False, "error": ...} tells the worker to
        stop sending them. One whose video follows a gap in its stream and is no keyframe is left out (obs_format
        DROPPED): {"ok": True, "dropped": True}, its observe function handed nothing, the episode going on. `params`:
        the episode's inference parameters, of which its observe function is handed the ones it takes."""
        if self._inst is None:
            raise RuntimeError("the policy is not built yet: a frame came before its load")
        said = record.reserved_refused(frame)
        if said:
            # said by its next act, as any frame that does not read, and its later frames are not sent
            failed = self._fail(episode_id, seq, ConversionError(said, "reserved_key"))
            return {"ok": False, "error": self._said(*failed)}
        try:
            episode = self._episode_of(episode_id, None) if self._keeps_episodes else None
        except RuntimeError:
            # its @seq.on_episode raised as it began (_begin): this frame's answer, never the other episodes' frames
            # this call carries (op "frames")
            return {"ok": False, "error": self._said(*self._failed[episode_id])}
        primed = self._primed.get(episode_id) if seq is not None else None
        if primed is not None:
            if int(seq) <= primed:
                return self._prime(episode, episode_id, int(seq), frame)
            self._primed.pop(episode_id, None)
        if seq is not None:
            self._last_seq[episode_id] = int(seq)
        if obs_format.no_frame(frame):
            return {"ok": True, "dropped": True}
        if self._records and episode is not None and seq is not None:
            record.frame(episode, self._rec(episode_id), int(seq), frame)   # as it came: compressed
        failed = self._failed.get(episode_id)
        if failed is None:
            try:
                # its marked items (sequence_ai.Video, Depth, Tactile) back to the arrays the robot marked - the frame
                # the robot built, item for item - kept as the episode's latest observation
                frame = self._obs.take(episode_id, seq, frame)
                if frame is obs_format.DROPPED:
                    return {"ok": True, "dropped": True}
                if self._observe is not None:
                    self._call(self._observe, self._observe_by, SeqFlags.OBSERVE, self._converted(frame),
                               {**self._at(episode_id, seq, episode), **self._observing(params)})
                return {"ok": True}
            except Exception as exc:  # noqa: BLE001 - the robot's frame or the policy's own error, said by the next act
                failed = self._fail(episode_id, seq, exc)
        return {"ok": False, "error": self._said(*failed)}

    def _act(self, latest, kwargs: dict, episode_id: str | None):
        """An act, which carries no data - every input came by observe: beside an observe function the act function is
        called with none, its observations had as they came; without, it is handed its episode's latest observation
        (`latest`, else read here) - whole to one argument, by name to two or more without a default - and an episode
        with none yet is the caller's (400), as a call its signature does not take is."""
        what = self._what(SeqFlags.INFER)
        if self._observe is None:
            if latest is None:
                latest = self._latest_of(episode_id)
            inputs = self._convert.observation(latest) if self._convert is not None else latest
            return self._call(self._infer, self._infer_by, SeqFlags.INFER, inputs, kwargs)
        try:
            sig = inspect.signature(self._infer)
        except (TypeError, ValueError):
            return self._infer(**kwargs)                 # a builtin's: called as it comes
        try:
            sig.bind(**kwargs)
        except TypeError as exc:
            raise ConversionError(f"{what}{sig} is called with no data beside its @seq.observe function, its "
                                  f"observations went there: {exc}") from None
        return self._infer(**kwargs)

    def latest(self, episode_id: str | None) -> Any:
        """Its episode's latest observation as it came (takes_latest): a robot-arm preset's server reads it as an act's
        Observation before its act function is handed it."""
        return self._latest_of(episode_id)

    def _latest_of(self, episode_id: str | None):
        """Its episode's latest observation, for an act function with no observe function (an act of no data): the
        frame that failed said first, and an episode with none yet the caller's (400)."""
        self._raise_failed(episode_id)
        try:
            return self._obs.latest(episode_id)
        except obs_format.NoObservation as exc:
            raise ConversionError(str(exc), "no_observation") from None

    def _call(self, method, by_name, flag: SeqFlags, handed, kwargs: dict):
        """`method` handed what an act or a frame carries: whole, or - `by_name`, a method that takes two or more
        arguments without a default - each key to its argument of that name; a key it needs missing, or one it takes
        no argument for, is the caller's (400), named."""
        if by_name is None:
            return method(handed, **kwargs)
        try:
            args, named = by_name.call(handed, self._what(flag))
        except ValueError as exc:
            raise ConversionError(str(exc)) from None
        return method(*args, **named, **kwargs)

    def _converted(self, observation):
        """`observation` as the policy's methods take it (torch tensors where annotated so, engine.convert)."""
        return self._convert.observation(observation) if self._convert is not None else observation

    def _at(self, episode_id: str | None, step, episode) -> dict:
        """What its observe function is handed beside a frame: {"step": its step in the episode, from 0 - the frame's
        seq} when it takes `step`, {"episode": its seq.Episode} when it takes `episode`."""
        if "episode" in self._observe_kw and episode is None:
            episode = self._new_episode(episode_id or "")
        return {**({"step": step} if "step" in self._observe_kw else {}),
                **({"episode": episode} if "episode" in self._observe_kw else {})}

    def _observing(self, params: dict | None) -> dict:
        """Of an episode's inference parameters, the ones its observe function takes (_observe_params)."""
        return self._taking(params, self._observe_params)

    @staticmethod
    def _taking(params: dict | None, names: frozenset | None) -> dict:
        """Of `params`, the ones a method takes: `names`, or every one (None, its **kwargs)."""
        if not params:
            return {}
        return dict(params) if names is None else {k: v for k, v in params.items() if k in names}

    def _fail(self, episode_id: str | None, seq, exc: BaseException) -> tuple:
        """Its episode's frame `seq` failed: kept - the episodes kept no more than obs_format keeps - and said by every
        act of the episode until it ends."""
        failed = self._failed[episode_id] = (seq, exc)
        while len(self._failed) > obs_format.EPISODES_KEPT:
            self._failed.popitem(last=False)
        return failed

    def _said(self, seq, exc: BaseException) -> str:
        """What an act says of its episode's frame that failed: one its observe function raised on, or one that did not
        read - or of its @seq.on_episode that raised as it began (_BEGAN)."""
        if seq is _BEGAN:
            return f"@seq.on_episode raised as the episode began: {type(exc).__name__}: {exc}"
        return _frame_failed(seq, exc) if self._observe is not None else _unread(seq, exc)

    def _raise_failed(self, episode_id: str | None) -> None:
        """Its episode's frame that failed, said: one that did not hold what the policy reads, or a marked item that
        does not decode, is the caller's (400); one its observe function raised on, its own."""
        failed = self._failed.get(episode_id)
        if failed is None:
            return
        seq, exc = failed
        caller = seq is not _BEGAN and (isinstance(exc, ConversionError) if self._observe is not None
                                        else isinstance(exc, ValueError))
        if caller:
            # the caller's, said with why the frame was refused: a key of the platform's (reserved_key), one that did
            # not read as the policy reads it (observation)
            raise ConversionError(self._said(seq, exc), getattr(exc, "reason", None)) from exc
        raise RuntimeError(self._said(seq, exc)) from exc

    def _forget(self, episode_id: str | None) -> None:
        """An episode's latest observation and its decoders, its frame that failed, its step count and its record's,
        gone with it."""
        self._obs.end(episode_id)
        self._failed.pop(episode_id, None)
        self._record.pop(episode_id, None)
        self._last_seq.pop(episode_id, None)
        self._primed.pop(episode_id, None)

    def robot_view(self, episode_id: str) -> dict | None:
        """What this copy holds of an episode now, for the Machines page: its newest step, each
        camera's newest frame as a small JPEG, and its plans - None for an episode it holds nothing of. Made only while
        someone looks, off any act's path."""
        try:
            latest = self._obs.latest(episode_id)
        except obs_format.NoObservation:
            latest = None
        episode = self._episodes.get(episode_id)
        if latest is None and episode is None:
            return None
        if hasattr(latest, "model_dump"):
            latest = latest.model_dump(mode="json")
        plans = (episode.state.get(record.PLANS) or [])[-32:] if episode is not None else []
        step = self._last_seq.get(episode_id)
        if step is None and self._record.get(episode_id) is not None:
            step = self._record[episode_id].last_step
        return {"episode": episode_id, "step": step, "cameras": view.frames(latest) if latest is not None else [],
                "plans": record.storable(plans)[0]}

    def _prime(self, episode, episode_id: str, seq: int, frame) -> dict:
        """A frame of an episode read back with no record of it (restore_episode), at or before the newest frame its
        state holds, which its robot sent again as it switched here - every frame it kept, from before that state was
        saved:
        kept in its record as it came and turned back by its decoders, so a video's next frames decode from its keyframe
        and an act reads it, never handed to its observe function again - the state read back holds it already. A video
        frame before its stream's first keyframe here is left out (obs_format DROPPED), as any after a gap."""
        if obs_format.no_frame(frame):
            return {"ok": True, "dropped": True}
        if self._records and episode is not None:
            record.frame(episode, self._rec(episode_id), seq, frame)        # as it came: compressed
        try:
            taken = self._obs.take(episode_id, seq, frame)
        except Exception:  # noqa: BLE001 - one that does not decode leaves its stream waiting for a keyframe
            taken = obs_format.DROPPED
        return {"ok": True, "primed": True, **({"dropped": True} if taken is obs_format.DROPPED else {})}

    def state_snapshot(self, episode_ids: list) -> dict:
        """What is saved of each of these episodes as it goes: {episode_id:
        {"state", "skipped", "steps", "through"}} - its state but the record's own two, made storable as at its end
        (record.state_of), how many of its acts were answered, and the newest frame this copy observed of it (None for
        one whose frames come with its acts); one this copy holds no Episode of is left out.
        WHY the copy's newest frame: a frame its worker took a moment ago may not have reached this copy yet, and a
        state read back as holding it would never be handed that frame again."""
        out = {}
        for eid in episode_ids or ():
            episode = self._episodes.get(eid) if eid else None
            if episode is not None:
                out[eid] = {**record.state_of(episode), "steps": episode.steps, "through": self._last_seq.get(eid)}
        return out

    def restore_episode(self, episode_id: str, *, state: dict | None = None, steps: int = 0, through: int | None = None,
                        observations: dict | None = None, actions: dict | None = None) -> bool:
        """An episode that began on another worker, handed to this copy before anything else of it
: its Episode made with what was saved of it - the policy's own keys and seq.plans,
        its count of answered acts, its record put back step by step - with no @seq.on_episode, as it goes on rather
        than begins, its episode.local empty; and its observations from their last keyframe up to `through` taken as
        its frames were (obs_format), so an act reads the newest saved and a video frame after it decodes as it would
        have there. False when this copy holds it already."""
        if not episode_id or episode_id in self._episodes:
            return False
        observations = {int(k): v for k, v in (observations or {}).items()}   # a JSON channel names its keys as strings
        actions = {int(k): v for k, v in (actions or {}).items()}
        if self._keeps_episodes:
            episode = self._episodes[episode_id] = self._new_episode(episode_id)
            episode.state.update(state or {})
            object.__setattr__(episode, "_steps", int(steps or 0))    # the server's count, as answered() keeps it
            if self._records:
                record.restored(episode, self._rec(episode_id), observations, actions)
        if through is not None and not observations:
            # no record read back - capture off, a standby's checkpoint keeps no frame of a robot's: the frames its
            # robot sends again up to `through` begin this copy's decoders and record (_prime)
            self._primed[episode_id] = int(through)
        if through is not None:
            self._last_seq[episode_id] = int(through)
            for step in record.from_keyframe(observations, int(through)):
                try:
                    self._obs.take(episode_id, step, observations[step])
                except Exception:  # noqa: BLE001 - one that does not decode leaves its stream waiting for a keyframe
                    pass
        return True

    def plan_episode(self, episode_id: str) -> Any:
        """The episode's seq.Episode on this copy, for its plan - None when it holds none (no act or frame of it came
        yet, or it ended or was pushed out). Read alone, from the plan's own thread: the order of the episodes kept,
        which an act moves, is never touched here."""
        return self._episodes.get(episode_id) if episode_id else None

    def plan(self, episode: Any) -> Any:
        """Its @seq.plan once, on the robot of `episode` as it is now → what it returns, any object (None keeps the
        plans as they are), or, for an async one, its coroutine, which the caller awaits on the clock's loop. Never on
        the act path: the model's round trip it wraps must stay off every act."""
        if self._plan is None:
            raise RuntimeError("policy has no @seq.plan binding")
        try:
            latest = self._obs.latest(episode.id)
        except obs_format.NoObservation:
            latest = None
        if hasattr(latest, "model_dump"):
            latest = latest.model_dump(mode="json")
        return self._plan(robot=robot.view(episode, latest))

    def plan_start(self, episode_id: str, at: int | None = None) -> dict:
        """One plan of the episode now, asked for by its eval, on the eval's clock, or by its build's check: begun on a
        thread of its own, since this copy answers one op at a time and its other episodes' acts go on meanwhile; its
        answer by plan_result. {"waiting": True} while the copy has not had observation `at` yet - a post is answered
        before its frames reach the copy, and a plan begun now would read the one before - {"unknown": True} for an
        episode it holds no state of, else {"started": True}."""
        episode = self._episodes.get(episode_id)
        if episode is None:
            return {"unknown": True}
        step = self._step_of(episode_id)
        if at is not None and (step is None or step < int(at)):
            return {"waiting": True}
        if episode_id not in self._asked:
            self._asked[episode_id] = None
            threading.Thread(target=self._plan_asked, args=(episode_id, episode, step), name="seq-plan-asked",
                             daemon=True).start()
        return {"started": True}

    def plan_result(self, episode_id: str) -> dict:
        """The answer to plan_start, once: {"pending": True} while it runs; {"unknown": True} for no plan asked; else
        {"plan": {"step", "value"}, "ms"} kept in its plans, {"none": True, "ms"} for a plan that returned None or
        handed the robot to a person, or {"failed", "kind", "ms"}."""
        if episode_id not in self._asked:
            return {"unknown": True}
        said = self._asked[episode_id]
        if said is None:
            return {"pending": True}
        del self._asked[episode_id]
        return said

    def _plan_asked(self, episode_id: str, episode, step: int | None) -> None:
        """One plan asked for, on its own thread: kept and noted as a plan on its clock is (plan_clock). Nothing
        escapes."""
        t0 = time.perf_counter()
        try:
            got = self.plan(episode)
            if inspect.isawaitable(got):
                # on the clock's loop, where its plans after it run: a client the plan keeps is of that loop
                got = self.clock.run(got) if self.clock is not None else asyncio.run(plan_clock._awaited(got))
            ms = round((time.perf_counter() - t0) * 1000)
            if got is None or plan_clock.asks_human(got):
                said = {"none": True, "ms": ms}
            else:
                plan_clock._keep_plan(episode, step, got)
                said = {"plan": {"step": step, "value": record.storable(got)[0]}, "ms": ms}
            plan_clock._planned(episode_id, got, ms)
        except Exception as exc:  # noqa: BLE001 - the plan's own error, its caller's to say
            plan_clock._failed(episode_id, exc)
            said = {"failed": plan_clock.described(exc), "kind": plan_clock.classify_plan_error(exc),
                    "ms": round((time.perf_counter() - t0) * 1000)}
        if episode_id in self._asked:           # not an episode that ended while it ran (_stop_planning)
            self._asked[episode_id] = said

    def _stop_planning(self, episode_id: str) -> None:
        """An episode's end, first: no plan of it starts again and what one in flight returns is dropped, so nothing is
        appended to its plans once its end - its on_episode, its state's last record - is under way."""
        self._asked.pop(episode_id, None)
        if self.clock is not None and episode_id:
            self.clock.forget(episode_id)

    def _step_of(self, episode_id: str) -> int | None:
        step = self._last_seq.get(episode_id)
        if step is None and self._record.get(episode_id) is not None:
            step = self._record[episode_id].last_step
        return step

    def _rec(self, episode_id: str | None) -> "record.Record":
        rec = self._record.get(episode_id)
        if rec is None:
            rec = self._record[episode_id] = record.Record()
        return rec

    def _episode_of(self, episode_id: str | None, keep: int | None, *, fresh: bool = False,
                    held: frozenset = frozenset()) -> Any:
        """The episode's seq.Episode on this copy: made at its first act or frame here - its @seq.on_episode start run
        then (_begin) - the same object after. An act sent with no episode is an episode of its own, kept nowhere.
        `fresh`: made anew whatever is kept - the router's act again, alone, of a batch that raised at its episode's
        first act, whose call may have written into the state it was handed; dropped, not ended, as its episode goes
        on. `held`: the episodes of the batch it is in, which no new episode of that batch pushes out."""
        if not episode_id:
            return self._new_episode("")
        if fresh:
            self._episodes.pop(episode_id, None)
        episode = self._episodes.get(episode_id)
        if episode is not None:
            self._episodes.move_to_end(episode_id)
        else:
            episode = self._new_episode(episode_id)
            self._begin(episode_id, episode)
            self._episodes[episode_id] = episode
        # (an episode its frames made, before any act said how many this copy keeps, counted at its first act)
        while keep and len(self._episodes) > keep:
            # More than the worker places on this copy: the least recently used one ended without its end reaching
            # this copy (the worker's notice is best-effort) - ended now, as it would have been; never one of this
            # batch.
            gone = next((e for e in self._episodes if e not in held and e != episode_id), None)
            if gone is None:
                break
            self._stop_planning(gone)
            dropped = self._episodes.pop(gone)
            self._forget(gone)
            self._end(gone, dropped)                 # never raises: its own act does not fail for another's end
        return episode

    def _episodes_of(self, episode_ids: list, keeps: list, fresh: list) -> list:
        """A batch's episodes, one for each of its acts in order: each act's _episode_of, every episode of the batch
        held first, so that a new one never pushes out another of the same batch. A batch holds one act of an episode at
        most (the router sends an episode's acts one at a time): two would be handed the same state at once."""
        named = [e for e in episode_ids if e]
        if len(set(named)) != len(named):
            twice = sorted({e for e in named if named.count(e) > 1})
            raise RuntimeError(f"a batch holds two acts of episode {twice[0]}: an episode's acts are answered one at a "
                               "time")
        held = frozenset(named)
        for eid in named:
            if eid in self._episodes:
                self._episodes.move_to_end(eid)
        keep = max((int(k) for k in keeps if k), default=0) or None
        return [self._episode_of(eid, keep, fresh=bool(f), held=held) for eid, f in zip(episode_ids, fresh)]

    def infer_batch(self, *, seeds: list, episode_ids: list, params: list, keeps: list | None = None,
                    fresh: list | None = None, latest: list | None = None) -> list:
        """A whole batch (@seq.concurrent), answered one ActionChunk an act, in order. As its infer takes it:
        collated - the default - one call for each set of inference parameters its acts share, its acts' inputs stacked
        into one batch (_stacked); with collate=False, one call where every argument it declares receives a list, one
        entry per request in order - the observations, the seeds, and each inference parameter (a request that did not
        send one gets the infer's own default).
        Its acts carry no data: without an observe function each is handed its episode's latest observation, as one act
        is (_act; `latest`, as its server read them, else read here); beside one, the observations went there and the
        act function is called with its lists alone.
        A policy handed its episodes gets them so too - `episode`, each act's seq.Episode (_episodes_of; `keeps` and
        `fresh` its acts' _keep and _fresh) - each one step on once the call has answered them all; a call that raises
        moves none, and the router decides what becomes of them (rerun alone fresh, or ended)."""
        names = {n for n in (set().union(*(set(p or {}) for p in params)) if params else ())
                 if self._infer_params is None or n in self._infer_params}
        kwargs: dict = {name: [(p or {}).get(name, self._infer_defaults.get(name)) for p in params] for name in names}
        if "seed" in self._infer_kw:
            kwargs["seed"] = list(seeds)
        observations = None
        if self._observe is None:
            observations = list(latest) if latest is not None else [self._latest_of(e) for e in episode_ids]
            if self._convert is not None:  # each act's inputs as one act's are, and each answer - its list the batch
                observations = [self._convert.observation(o, alone=False) for o in observations]
        n = len(episode_ids)
        episodes = None
        if self.episodes == "shared":
            episodes = self._episodes_of(list(episode_ids), list(keeps or [None] * n), list(fresh or [False] * n))
            if "episode" in self._infer_kw:            # kept on the copy either way; handed only to an infer taking it
                kwargs["episode"] = episodes
        if self._observe is not None:
            for episode_id in episode_ids:
                self._raise_failed(episode_id)
        if self._collated:
            out = self._stacked(observations, kwargs, names, n)
        elif observations is not None:
            out = self._infer(observations, **kwargs)
        else:
            out = self._infer(**kwargs)
        if not isinstance(out, (list, tuple)) or len(out) != n:
            got = f"{type(out).__name__} of {len(out)}" if isinstance(out, (list, tuple)) else type(out).__name__
            raise TypeError(f"a @seq.concurrent infer returns one ActionChunk per observation: {n} in, {got} out")
        answers = [self._convert.answer(a, alone=False) for a in out] if self._convert is not None else list(out)
        for eid, episode, answer in zip(episode_ids, episodes or (), answers):
            if self._records:
                record.answer(episode, self._rec(eid), answer)
            self._answered(episode)
        return answers

    def _stacked(self, observations: list | None, kwargs: dict, names: set, n: int) -> list:
        """A collated batch's answers, one an act: its acts grouped by the inference parameters they set, one call a
        group, its acts' inputs stacked into one batch (stack.stack: (B, ...) a key, `<key>_mask` where a first axis
        differs) - padded to the smallest size infer is called with that holds them, the last act's inputs and seed
        again in the rows past its own, and those rows left out of the answer - each parameter one value, `seed` a list
        of the batch's rows, and `episode` the group's acts' own episodes alone, never a stateful one handed twice. Its
        answer is split back (stack.unstack). The batcher sends a listed size, so a batch whose acts all set the same
        parameters is never padded. A policy with an observe function is handed no inputs: its `episode` list says whose
        acts. Acts that do not stack raise in words, and the batcher runs them again one by one, each a batch of its
        own."""
        import json

        from . import stack

        sizes = sorted({int(s) for s in (self.batch or {}).get("sizes") or ()} | {1})
        groups: dict[str, list[int]] = {}
        for i in range(n):
            # the values its infer would be handed, a parameter it did not send at the infer's default
            key = json.dumps({name: kwargs[name][i] for name in sorted(names)}, sort_keys=True, default=repr)
            groups.setdefault(key, []).append(i)
        out: list = [None] * n
        for part in groups.values():
            # its rows: the group's acts, then the last of them again up to a listed size (never past the batch's own)
            size = min((s for s in sizes if s >= len(part)), default=len(part))
            rows = part + [part[-1]] * (size - len(part))
            kw = {name: kwargs[name][part[0]] for name in names}
            if "seed" in kwargs:
                kw["seed"] = [kwargs["seed"][i] for i in rows]
            if "episode" in kwargs:
                kw["episode"] = [kwargs["episode"][i] for i in part]
            if observations is None:
                got = self._infer(**kw)
            else:
                got = self._call(self._infer, self._infer_by, SeqFlags.INFER,
                                 stack.stack([observations[i] for i in rows]), kw)
            # a list of the group's own answers is taken as it is; anything else answers every row
            answers = got if isinstance(got, list) and len(got) == len(part) else stack.unstack(got, size)
            for i, answer in zip(part, answers):
                out[i] = answer
        return out

    def episode_reset(self, episode_id: str) -> None:
        """Episode boundary: the policy's @seq.on_episode if declared (optional hook), handed the episode's seq.Episode,
        its phase "end", then the Episode dropped - for an episode that began on this copy or was restored to it alone:
        one that never began here, or whose end ran already (pushed out, _episode_of), has no end of its own here.
        Its planning stops before anything of it ends (_stop_planning). Nothing of it is stored."""
        self._stop_planning(episode_id)
        self._forget(episode_id)
        episode = self._episodes.pop(episode_id, None)
        if episode is not None:
            self._end(episode_id, episode)

    def _begin(self, episode_id: str, episode) -> None:
        """@seq.on_episode as `episode` begins on this copy, before its first act or frame: handed its Episode, its
        phase "start" (an episode a standby takes on goes on rather than begins: restore_episode runs none). One it
        raises on did not begin: it is kept as the episode's failure (_fail, at _BEGAN) and raised, said by this act or
        frame and every later one of the episode until it ends, its hook not run again - in an eval the episode is an
        error."""
        failed = self._failed.get(episode_id)
        if failed is not None and failed[0] is _BEGAN:
            self._raise_failed(episode_id)
        if self._on_episode is None:
            return
        at(episode, "start")
        try:
            self._on_episode(episode=episode)
        except Exception as exc:  # noqa: BLE001 - the episode's, kept and said
            self._fail(episode_id, _BEGAN, exc)
            self._raise_failed(episode_id)
        finally:
            at(episode, None)

    def _end(self, episode_id: str, episode) -> None:
        """@seq.on_episode at `episode_id`'s end: handed its Episode, `episode`, its phase "end" - its id is episode.id
        (sequence_base.by_name.ends). What it raises is said on the server's log (say) and goes no further: the episode
        has ended."""
        if self._on_episode is None:
            return
        at(episode, "end")
        try:
            self._on_episode(episode=episode)
        except Exception as exc:  # noqa: BLE001 - the episode ended whatever its hook did
            say(f"@seq.on_episode for episode {episode_id} raised {type(exc).__name__}: {exc}")
        finally:
            at(episode, None)

    def shutdown(self) -> None:
        """The server's teardown: the policy's @seq.shutdown, if it declares one (an optional hook)."""
        if self._shutdown is not None:
            self._shutdown()


def say(line: str) -> None:
    """A line for the server's log - an episode's on_episode that raised as it ended, a video frame left out after a gap
    (engine.obs_format) - printed, unless a host replaces this (adapter.say = its own)."""
    print(line, flush=True)


def _say(line: str) -> None:
    """say, looked up as each line is said: a host's own reaches what was made before it was set."""
    say(line)


def construct(cls: type, constructor: Any, *, base_dir: str, weights: Any) -> object:
    """A policy's instance, as its load builds it: `cls()`, or - a class that declares its constructor's arguments
    (init=, a PolicyConstructor) - its constructor called with them, its config files read from `base_dir` and
    "{weights}" filled with `weights` (sequence_base.construct.build)."""
    if constructor is None:
        return cls()
    from sequence_base.construct import build

    return build(cls, constructor, base_dir=base_dir, weights=weights)




def _frame_failed(seq, exc: BaseException) -> str:
    """What an episode's acts say of the frame that failed: one that did not hold what the policy declares it reads,
    or one its observe method raised on."""
    if isinstance(exc, ConversionError):
        which = f"frame {seq}" if seq is not None else "an act's observation"
        return f"{which} was refused: {exc}"
    where = f"at frame {seq}" if seq is not None else "on an act's observation"
    return f"observe raised {where}: {type(exc).__name__}: {exc}"


def _unread(seq, exc: BaseException) -> str:
    """What an episode's calls say of its frame that did not read, on a policy with no observe function of its own: a
    marked item the robot sent that does not decode (marked.MarkedError, a ValueError), or a failure of the copy's."""
    if isinstance(exc, ValueError):
        return f"frame {seq} was refused: {exc}"
    return f"frame {seq} could not be read: {type(exc).__name__}: {exc}"


# The decorator that marks each method, as its errors say it.
_ARG = {SeqFlags.INFER: "@seq.infer", SeqFlags.OBSERVE: "@seq.observe", SeqFlags.ON_EPISODE: "@seq.on_episode",
        SeqFlags.SHUTDOWN: "@seq.shutdown", SeqFlags.PLAN: "@seq.plan", SeqFlags.SAMPLE: "@seq.sample"}
# Where an episode's failure is kept in place of a frame's number: its @seq.on_episode raised as it began (_begin).
_BEGAN = "start"


def _by_name(method, platform: frozenset):
    """How `method` (bound) takes what it is handed (sequence_base.by_name): its ByName, or None - whole."""
    from sequence_base.by_name import takes_by_name

    try:
        params = inspect.signature(method).parameters.values()
    except (TypeError, ValueError):
        return None                                  # a builtin's: handed it whole
    return takes_by_name(params, platform)


def _keywords(fn, platform: frozenset, *, skip_first: bool) -> frozenset | None:
    """The names `fn` takes by keyword beside `platform`'s - and beside its first argument, `skip_first`, its inputs
    (the SDK's rule, seq.params.keyword_params); None when it takes **kwargs."""
    try:
        params = list(inspect.signature(fn).parameters.values())
    except (TypeError, ValueError):
        return frozenset()
    if any(p.kind is inspect.Parameter.VAR_KEYWORD for p in params):
        return None
    positional = (inspect.Parameter.POSITIONAL_ONLY, inspect.Parameter.POSITIONAL_OR_KEYWORD)
    first = next((p for p in params if p.kind in positional), None) if skip_first else None
    return frozenset(p.name for p in params if p is not first and p.name not in platform
                     and p.kind in (inspect.Parameter.POSITIONAL_OR_KEYWORD, inspect.Parameter.KEYWORD_ONLY))


def _accepts(fn, names: tuple[str, ...]) -> set[str]:
    """Which of `names` `fn` takes as keywords: all of them when it takes **kwargs."""
    try:
        params = inspect.signature(fn).parameters
    except (TypeError, ValueError):
        return set()
    if any(p.kind is inspect.Parameter.VAR_KEYWORD for p in params.values()):
        return set(names)
    return {n for n in names if n in params}
