# SPDX-FileCopyrightText: Copyright (c) 2026 General Sequences Company
# SPDX-License-Identifier: Apache-2.0
"""
A `@seq.policy` class as the copy of the policy on serve(): its adapter (engine.adapter) handed each episode's frames in
order by the data plane (engine.data_plane), each act, each episode's end, and its plans on their clock
(engine.plan_clock) - what a deployment's worker does in the process that holds a copy, on a policy server of your own.

    adapter = RegisteredAdapter(cls, registered)      # engine.adapter: registered.registration, @seq.policy's
    adapter.load(weights_dir)
    copy = PolicyCopy(adapter)
    serve(copy.call, batch=copy.batch, copy=copy)        # engine.serve, as `seq serve` runs it

In one sentence: the data plane hands an episode's frames in order (observe) → each goes to the adapter on the policy's
thread - kept as the episode's latest observation, handed to its observe function - and each it took tells the plan
clock (one holding a key of wake_on plans at once) → an act's latest() is a handle on its episode, which call() hands
the adapter on the policy's thread - infer, or infer_batch for a batch - so its act function reads what its episode
holds → an episode's end runs its on_episode there ("end") → the clock stops with the server.

What it does, and why:
    one thread         every call of the policy's code - its observe function, its act function, its on_episode - runs
                       on the server's policy thread, as in a worker's copy: CUDA and JAX keep state per thread
    an act's input     what latest() returns is the act's handle on its episode, not an observation: the adapter
                       hands the act function its episode's latest observation, or nothing beside an observe function
    no observation     an act of a policy that reads its latest observation, before any came, is refused as the data
                       plane refuses one (409, no_observation)
    an act of its own  an act that carries its observation (a robot that sends none apart, the warm-up's example) is an
                       episode of its own, "seq-once-<n>": begun, acted on and ended at once, on_episode run as for any
    the server's own   an episode whose id starts with "seq-" is the server's own, and nothing is planned for it
    each plan said     what each plan returned, or raised, is said in the server's log as frames and acts come (the
                       clock notes them; drain_events) - a plan that raises fails no act, and says so here

Needs sequence-base (Python 3.10 and later), as engine.adapter does.
"""
from __future__ import annotations

import asyncio
import concurrent.futures
import itertools
import logging
from typing import Any, Callable, Optional

from sequence_base import SeqFlags

from . import obs_format
from .convert import ConversionError
from .plan_clock import PlanClock, drain_events

__all__ = ["PLATFORM_EPISODES", "PolicyCopy"]

log = logging.getLogger("sequence_ai.serve")

# What the id of an episode of the server's own starts with: its warm-up's, an act of its own. None is planned for.
PLATFORM_EPISODES = "seq-"
# How long close() waits for the plans under way: a stopped server does not hang on a model's slow answer.
PLAN_STOP_S = 2.0


class _Act:
    """What an act hands the policy on serve() when it carries no data: its episode, which the adapter acts on."""

    __slots__ = ("episode_id",)

    def __init__(self, episode_id: str) -> None:
        self.episode_id = episode_id

    def __repr__(self) -> str:
        return f"<act of {self.episode_id}>"


class PolicyCopy:
    """A loaded adapter as serve()'s copy of the policy (the module's docstring): the data plane's
    observe(episode_id, frames, handed), latest(episode_id), end(episode_id) and close(); call(), the function serve()
    calls on its policy thread; `batch`, the sizes it is called with; and `checked`, what serve() tries its speed-ups
    on.

    adapter    a loaded engine.adapter.RegisteredAdapter
    executor   the server's policy thread (serve() attaches it: attach); every call of the policy's code goes there
    checked    the call serve() tries its speed-ups on (engine.optimize), taking what `call` takes: the policy's act
               function called directly, as the platform tries a version's (seq serve's: seq.serve_local.checked_call);
               None: `call`. engine.optimize looks for a policy's torch modules a few attributes down from what its
               call holds, and `call` holds this copy, which holds the adapter, which holds the policy: a model the
               policy keeps two attributes down (self.policy.model) is beyond its reach from `call`"""

    def __init__(self, adapter: Any, *, executor: Optional[concurrent.futures.Executor] = None,
                 checked: Optional[Callable[..., Any]] = None) -> None:
        self._adapter = adapter
        self._executor = executor
        # what serve()'s speed-ups are tried on, where not `call`; they change the policy's modules in place, so `call`
        # then runs what they kept
        self.checked: Optional[Callable[..., Any]] = checked
        self.on_frame: Optional[Callable[[str, int, Any], None]] = None   # each frame as sent, in order: a recorder
        self._once = itertools.count()
        sizes = (adapter.batch or {}).get("sizes")
        # the sizes serve() calls it with, 1 among them; None: one act a call
        self.batch: Optional[list] = sorted({int(n) for n in sizes} | {1}) if sizes else None
        # its plans' clock, begun as it is made - after the adapter's load, as in a worker's copy
        self._clock: Optional[PlanClock] = None
        # how often each episode is planned for, in seconds start to start; None for a policy with no @seq.plan
        self.plan_every_s: Optional[float] = getattr(adapter, "plan_every_s", None) or None
        # what serve() calls - its start line and its ping's answer name it - by the policy's own class and act function
        self.call: Callable[[Any], Any] = self._named_call()
        if self.plan_every_s:
            self._clock = PlanClock(adapter, every_s=adapter.plan_every_s)
            adapter.clock = self._clock          # a plan asked for outside every clock runs on its loop
            self._clock.start()
            log.info("plans for each episode every %g s (%s)", adapter.plan_every_s,
                     "async" if adapter.plan_is_async else "a thread a plan")

    @property
    def plays(self) -> dict:
        """How the policy declares its answers play (@seq.policy): its hz, action_chunk_valid_len,
        action_chunk_replan_at and max_wait_for_batch, those it declares - what serve() says on /ping where it seats no
        robot by them."""
        declared = getattr(self._adapter, "declared_plays", None) or {}
        return {k: v for k, v in declared.items() if v is not None}

    def attach(self, executor: concurrent.futures.Executor) -> None:
        """The server's policy thread, where every call of the policy's code runs."""
        self._executor = executor

    # ── one rank of several (engine.ranks) ────────────────────────────────────────────────────────────────────────────
    def mirrored(self) -> "dict[str, Callable]":
        """The calls of the policy's code, other than its acts, that rank 0 of a group sends every rank before it runs
        its own, by name: each episode's frames to its observe function, and each episode's end to its on_episode - so
        every rank's copy holds what rank 0's does. ValueError for a policy that plans: its plans run on a clock of
        their own, which the ranks do not share."""
        if self._clock is not None:
            raise ValueError("a policy with @seq.plan plans on a clock of its own on each copy, and a group's ranks do "
                             "not share one: serve it as one process, or plan in its act function")
        return {"observe": self._observed, "end": self._adapter.episode_reset}

    @staticmethod
    def wire(items: Any) -> Any:
        """An act's input, or a batch's, as it is sent to the other ranks: an act's handle on its episode as
        {"seq.act": its episode}, an observation an act carried as it is."""
        def one(item: Any) -> Any:
            return {"seq.act": item.episode_id} if isinstance(item, _Act) else item
        return [one(item) for item in items] if isinstance(items, list) else one(items)

    @staticmethod
    def unwire(items: Any) -> Any:
        """wire's, read back on a rank: each {"seq.act": episode} the act's handle on that episode again."""
        def one(item: Any) -> Any:
            return _Act(item["seq.act"]) if isinstance(item, dict) and set(item) == {"seq.act"} else item
        return [one(item) for item in items] if isinstance(items, list) else one(items)

    # ── the data plane's copy ────────────────────────────────────────────────────────────────────────────────────────
    async def observe(self, episode_id: str, frames: list, handed: Callable[[], None]) -> list:
        """An episode's frames, (seq, inputs) in order, each to the adapter on the policy's thread; their answers, in
        order ({"ok": True}, {"ok": True, "dropped": True} for a video frame after a gap, {"ok": False, "error"}). Each
        it took tells the plan clock - at once for one that holds a key of wake_on."""
        if self.on_frame is not None:
            for seq, inputs in frames:
                self.on_frame(episode_id, seq, inputs)
        self._say_plans()
        answers = await self._on_policy_thread(self._observed, episode_id, frames)
        if self._clock is not None and not episode_id.startswith(PLATFORM_EPISODES):
            wake_on = getattr(self._adapter, "plan_wake_on", None)
            for (seq, inputs), took in zip(frames, answers):
                if took.get("ok") and not took.get("dropped"):
                    wake = bool(wake_on) and isinstance(inputs, dict) and not wake_on.isdisjoint(inputs)
                    self._clock.observe(episode_id, seq, wake=wake)
        return answers

    def latest(self, episode_id: str) -> Any:
        """An act's input: a handle on its episode, which call() hands the adapter. obs_format.NoObservation for an act
        of a policy that reads its latest observation when none came yet, as the data plane refuses one."""
        self._say_plans()
        if getattr(self._adapter, "takes_latest", False):
            try:
                self._adapter.latest(episode_id)
            except ConversionError as exc:
                if getattr(exc, "reason", None) == "no_observation":
                    raise obs_format.NoObservation(str(exc)) from None
                # a frame that failed: the act says it, from the adapter, when call() hands it the episode
        return _Act(episode_id)

    def end(self, episode_id: str) -> None:
        """The episode ended: its on_episode run with phase "end", on the policy's thread after any call of it already
        there, and the episode dropped; its plans end with it."""
        if self._executor is None:
            self._adapter.episode_reset(episode_id)
            return
        future = self._executor.submit(self._adapter.episode_reset, episode_id)
        future.add_done_callback(_said_if_raised)

    def close(self) -> None:
        """Its plans stop, PLAN_STOP_S at most for one under way."""
        if self._clock is not None:
            self._clock.stop(grace=PLAN_STOP_S)
            self._say_plans()

    def _say_plans(self) -> None:
        """Each plan's outcome the clock noted since the last time, said in the server's log: a plan's answer at info,
        one that raised or handed its robot to a person - whom nobody takes here - as a warning."""
        if self._clock is None:
            return
        for ev in drain_events():
            kind, env = ev.get("ev"), ev.get("env")
            if kind == "plan.done":
                if ev.get("step") is None:
                    log.info("plan of episode %s returned None in %s ms: its plans are as they were", env, ev.get("ms"))
                else:
                    log.info("plan of episode %s in %s ms: %s", env, ev.get("ms"), ev.get("step"))
            elif kind == "plan.error":
                log.warning("plan of episode %s raised (%s): %s; it plans again at its next tick, its acts unchanged",
                            env, ev.get("kind"), ev.get("error"))
            elif kind == "plan.ask_human":
                log.warning("plan of episode %s handed its robot to a person (seq.ask_human: %s): a server of your own "
                            "has no one to take it, so nothing is kept", env, ev.get("reason"))

    # ── what serve() calls, on its policy thread ─────────────────────────────────────────────────────────────────────
    def _named_call(self) -> Callable[[Any], Any]:
        """call, named as the policy's own act function is - "MyModel_user.get_action_user" - where serve() names what
        it serves."""
        def call(handed: Any, seed: Any = None) -> Any:
            return self._call(handed, seed)

        cls = getattr(self._adapter, "_cls", None)
        act = (getattr(self._adapter, "_names", None) or {}).get(SeqFlags.INFER)
        call.__doc__ = self._call.__doc__
        if cls is not None and act:
            call.__name__, call.__qualname__ = act, f"{cls.__name__}.{act}"
        return call

    def _call(self, handed: Any, seed: Any = None) -> Any:
        """One act's answer - `handed` an act's handle on its episode, or an observation an act carried - or, with
        `batch`, a list of them, answered in order. `seed`: what the speed-ups' checks pass (engine.optimize), one or a
        list of them, so a policy's noise repeats from one run to the next; a robot's act has none."""
        if self.batch is None:
            return self._one(handed, seed)
        items = list(handed)
        # one batch, as the adapter stacks it: an act of its episode handed nothing, one that carried its observation
        # (the warm-up's example) that observation observed in an episode of its own, begun here and ended once the
        # batch answered
        own = [None if isinstance(item, _Act) else f"{PLATFORM_EPISODES}once-{next(self._once)}" for item in items]
        try:
            for item, eid in zip(items, own):
                if eid is not None:
                    self._adapter.observe(item, episode_id=eid, seq=0)
            return self._adapter.infer_batch(
                seeds=list(seed) if seed is not None else [None] * len(items),
                episode_ids=[item.episode_id if isinstance(item, _Act) else eid for item, eid in zip(items, own)],
                params=[None] * len(items))
        finally:
            for eid in own:
                if eid is not None:
                    self._adapter.episode_reset(eid)

    def _one(self, handed: Any, seed: Any = None) -> Any:
        if isinstance(handed, _Act):
            return self._adapter.infer(seed=seed, episode_id=handed.episode_id)
        # an act that carried its observation (the warm-up's example): an episode of its own, the observation observed,
        # then acted on, and ended
        episode_id = f"{PLATFORM_EPISODES}once-{next(self._once)}"
        try:
            self._adapter.observe(handed, episode_id=episode_id, seq=0)
            return self._adapter.infer(seed=seed, episode_id=episode_id)
        finally:
            self._adapter.episode_reset(episode_id)

    def _observed(self, episode_id: str, frames: list) -> list:
        return [self._adapter.observe(inputs, episode_id=episode_id, seq=seq) for seq, inputs in frames]

    async def _on_policy_thread(self, fn: Callable, *args: Any) -> Any:
        if self._executor is None:
            return fn(*args)
        return await asyncio.get_running_loop().run_in_executor(self._executor, fn, *args)


def _said_if_raised(future: concurrent.futures.Future) -> None:
    """An episode's end that raised past its adapter, said in the log: the episode has ended whatever it raised."""
    exc = future.exception()
    if exc is not None:
        log.error("an episode's end raised %s: %s", type(exc).__name__, exc)
