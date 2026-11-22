# SPDX-FileCopyrightText: Copyright (c) 2026 General Sequences Company
# SPDX-License-Identifier: Apache-2.0
"""
The switches that split a policy's model between the processes of one server - cfg_parallel and pipeline_parallel -
as serve() runs them (engine.serve.App): each one's trial, on rank 0's policy thread during its warm-up, every call of
the policy and every toggle of the split sent to every rank first (engine.ranks.Group.run); and each toggle, run on
every rank alike.

    tried = split_trials.cfg_trial(app, examples)       # rank 0: the report its warm-up keeps
    split_trials.cfg_toggle(app, paths, on)             # every rank, as rank 0 sends it

WHY apart from serve.py: what a group's ranks try together is its own part of the server, which serve.py calls.
"""
from __future__ import annotations

import logging
from typing import Any, Callable

log = logging.getLogger("sequence_ai.serve")      # the server's own log: these lines are its warm-up's


def _say(line: str) -> None:
    log.info("%s", line)


def _caller(app: Any) -> Callable[[Any], Any]:
    """`call(item)` for a trial: the policy on one run's observation (or list of them) on every rank, rank 0's output
    back."""
    batched = app._sizes is not None

    def call(item: Any) -> Any:
        got = app._call(list(item) if batched else [item])
        return [output for output, _ in got] if batched else got[0][0]

    return call


def cfg_trial(app: Any, examples: list) -> dict:
    """On rank 0's policy thread: cfg_parallel tried on `examples` (engine.cfg_parallel.trial), each call of the policy
    and each toggle of the split sent to every rank first; its report. Off, saying why, for a server that is not two
    processes."""
    from . import cfg_parallel

    size = 1 if app._group is None else app._group.size
    if size != cfg_parallel.WORLD:
        why = (f"it cuts a batch between {cfg_parallel.WORLD} processes, and this server is {size}: start it as "
               f"{cfg_parallel.WORLD} (torchrun --nproc-per-node {cfg_parallel.WORLD})")
        _say(f"optimize: cfg_parallel off - {why}")
        return {"on": [], "switches": {"cfg_parallel": {"on": False, "why": why}}}

    def toggle(paths: list, on: bool) -> None:
        app._group.run("cfg_parallel", [list(paths), bool(on)], lambda: cfg_toggle(app, list(paths), bool(on)))

    return cfg_parallel.trial(app._checked(), _caller(app), toggle, examples, sizes=app._sizes,
                              limits=app._speedups["tolerance"], say=_say)


def cfg_toggle(app: Any, paths: list, on: bool) -> None:
    """cfg_parallel put in place on `paths` of this rank's policy, or taken out (engine.cfg_parallel) - on every rank
    alike, rank 0 sending it to the others (Group.run)."""
    from . import cfg_parallel
    from .optimize import _namespace

    if on and not app._cfg_patches:
        app._cfg_patches = cfg_parallel.install(_namespace(app._checked()), paths, say=_say)
    elif not on and app._cfg_patches:
        cfg_parallel.uninstall(app._cfg_patches)
        app._cfg_patches = []


def pp_trial(app: Any, examples: list) -> dict:
    """On rank 0's policy thread: pipeline_parallel tried on `examples` (engine.pipeline_parallel.trial), each call of
    the policy and each toggle of the split sent to every rank first; its report. Off, saying why, for a server of one
    process, or one where cfg_parallel is on."""
    from . import pipeline_parallel

    def off(why: str) -> dict:
        _say(f"optimize: pipeline_parallel off - {why}")
        return {"on": [], "switches": {"pipeline_parallel": {"on": False, "why": why}}}

    size = 1 if app._group is None else app._group.size
    if size < 2:
        return off(f"it splits a model's blocks between processes, and this server is {size}: start it as 2 or more "
                   "(torchrun --nproc-per-node 2)")
    if "cfg_parallel" in (app.optimized.get("on") or []):
        return off("cfg_parallel is on, and the two do not split one model together")

    def toggle(spec: dict, on: bool) -> Any:
        return app._group.run("pipeline_parallel", [dict(spec), bool(on)],
                              lambda: pp_toggle(app, dict(spec), bool(on)))

    return pipeline_parallel.trial(app._checked(), _caller(app), toggle, examples, size=size, sizes=app._sizes,
                                   limits=app._speedups["tolerance"], say=_say)


def pp_toggle(app: Any, spec: dict, on: bool) -> Any:
    """pipeline_parallel put in place on this rank's policy as `spec` says, or taken out (engine.pipeline_parallel) -
    on every rank alike, rank 0 sending it to the others (Group.run); this rank's split. A spec that differs from the
    split's only in naming the stages it timed puts the same split back, its schedules made already."""
    from . import pipeline_parallel
    from .optimize import _namespace

    split, before = app._pp_split, app._pp_spec
    same = split is not None and before is not None and \
        {k: v for k, v in spec.items() if k != "stages"} == {k: v for k, v in before.items() if k != "stages"} \
        and spec.get("stages") in (None, split.stages)
    if not on:
        if split is not None:
            split.off()
        return split
    if same:
        split.on()
        return split
    if split is not None:
        split.off()
    app._pp_split = pipeline_parallel.install(_namespace(app._checked()), spec["path"], form=spec["form"],
                                              parts=int(spec["parts"]), stages=spec.get("stages"),
                                              slot=spec.get("slot", 0), out=spec.get("out"))
    app._pp_spec = dict(spec)
    return app._pp_split
