# SPDX-FileCopyrightText: Copyright (c) 2026 General Sequences Company
# SPDX-License-Identifier: Apache-2.0
"""
A policy made faster on its own GPU, each speed-up turned on only once it is checked on observations of yours.

    import sequence_ai

    fast = sequence_ai.engine.optimize(policy, examples)     # 32 or more of your robot's own observations
    print(fast.report["on"])                                 # ["cuda_graphs", "whole_graph"]
    sequence_ai.serve(fast, example=examples[0])

serve() and `seq serve` run it by default, on the observations they warm up on (serve(examples=...) takes more).

Each technique is a switch of its own name. On by default, the two that leave the outputs exactly as they are:

    cuda_graphs    every module the model calls more than once a run with the same shapes (a denoiser), replayed from
                   a CUDA graph of its own kernels (cuda_graphs.py)
    whole_graph    a run's whole call into the model - its denoising loop and the noise it draws included - replayed as
                   one graph where it can be captured; where it cannot, cuda_graphs' modules alone

Off unless you turn them on, the four that change the outputs - each needs `tolerance`, the difference you accept:

    torch_compile  the modules the act spends its time in, compiled by torch.compile (compiled.py)
    fused_kernels  their norms, gated activations and rotary embeddings, each one kernel (fused.py)
    tensorrt       those modules built by TensorRT, TF32 off (compiled.py; pip install sequence-ai[tensorrt])
    precision      "fp16" or "fp32": those modules in that dtype (with tensorrt, its engines); "fp8": their linear
                   layers in 8-bit floating point, on a GPU of compute capability 8.9 or later (fp8.py); None, the
                   default: the model's own dtype, whatever it is

    fast = sequence_ai.engine.optimize(policy, examples, torch_compile=True, tolerance=1e-3)
    fast = sequence_ai.engine.optimize(policy, examples, precision="fp8", tolerance={"max_abs": 0.02, "cosine": 0.999})

`tolerance` is the largest difference you accept between an output with the switch and eager mode's: a number (the
largest absolute difference of any value), or a dict of max_abs, mean_abs and cosine (the least cosine similarity).

A JAX policy (one whose model jax.jit compiles) gets each switch's counterpart in XLA (xla.py):
cuda_graphs and whole_graph are XLA's command buffers, for straight-line work and for loops too - tried only when asked
(True), as they saved about nothing on the JAX models measured and a try compiles the model again for each;
precision is the dtype of the parameters its jitted functions are given; torch_compile and fused_kernels are what XLA
does already; tensorrt has none. Each is judged the same way.

A policy served by several processes can be checked in one and what it kept put in place in the others, with no
examples run there - apply() takes the report (JSON carries it):

    from sequence_ai.engine.optimize import apply

    report = sequence_ai.engine.optimize(policy, examples).report      # in one process
    apply(policy, report)                                              # in each other, the policy built the same way

In one sentence: the policy runs eagerly on each example with a fixed random state, and again, to see that the same
inputs give the same outputs (eager mode's outputs are what every switch is held to) → its torch modules' calls are
counted (cuda_graphs.Census, cuda_graphs.Calls) → the switches that change the outputs are turned on one at a time, in
the order precision, tensorrt, fused_kernels, torch_compile, each judged on every example against eager mode within
`tolerance` → then cuda_graphs and whole_graph, on top of what is on, each judged bit for bit against it → every switch
timed with and without it, in turns - one that changes the outputs with cuda_graphs on in both turns, where cuda_graphs
is to be tried, as it will run - and kept only when its outputs pass and the act is at least 10% faster (min_speedup);
taken out otherwise, the report saying why.

WHY a fixed random state for each run of an example: a flow or diffusion policy draws its noise on every act, and two
runs compare only when they draw the same noise; seeded alike, eager mode and each switch begin from the same noise,
so the whole sampling loop is compared and not one step of it. A policy that takes `seed=` (as `seq serve`'s call
does, for a template that derives its noise from a seed) is given each run's seed too.
WHY eager mode twice before anything is turned on: a value that changes from one run to the next with the same random
state is either a measurement of the run (a timing the policy reports), which is then left out of every comparison,
or an output of kernels that add in no fixed order, which no switch can be shown to keep exactly; either is said.
WHY each switch on its own, timed against the policy without it: a switch is worth running only for what it adds to the
ones already on, and one that fails takes nothing else down with it.
WHY a switch that changes the outputs is timed with cuda_graphs on in both turns, where cuda_graphs is to be tried: it
will run under the graphs, which take away the time each kernel takes to launch. Timed without them, a switch that
launches more kernels than the model did (fp8's scaling, for one) is judged by a cost the graphs remove, and one that
saves only launches by a saving the graphs make anyway. Its outputs are still held to eager mode's alone: timing and
accuracy are judged apart.
WHY the switches that change the outputs before the graphs: a graph replays the kernels it captured, so it is captured
of what runs - the compiled module, the fused kernels, the float16 copy - and checked bit for bit against that.
WHY at least 10% faster: a speed-up within the noise of the timing is no reason to run anything but the model's own
kernels.
WHY the random states are put back afterwards: the checks draw from the global generators, and the policy's own draws
after them should be what they would have been.

Standard library only at import; torch, where the policy uses it, is imported when the checks run.
"""
from __future__ import annotations

import copy
import hashlib
import inspect
import math
import random
import statistics
import struct
import sys
import time
import types
from typing import Any, Callable, Iterable, NamedTuple, Optional

__all__ = ["optimize", "apply", "Optimized", "check_switches", "differences", "SWITCHES", "MIN_SPEEDUP"]

SWITCHES = ("cuda_graphs", "whole_graph", "torch_compile", "fused_kernels", "tensorrt", "precision")
EXACT = ("cuda_graphs", "whole_graph")
CHANGING = ("precision", "tensorrt", "fused_kernels", "torch_compile")     # the order they are tried in
PRECISIONS = (None, "fp32", "fp16", "fp8")
MIN_SPEEDUP = 1.10    # how much faster an act must be for a switch to stay on
MIN_RUNS = 8          # the runs each switch is checked on, at the least: the examples again, each with its own seed
TIMED = 12            # the acts timed with and without a switch, at the most
BUDGET_S = 120.0      # no timed act is begun after this long on one switch; 3 are timed at the least
FEW = 32              # fewer examples than this, and the report says the check was a small one
WHOLE_TRIES = 4       # the calls tried as a whole graph, at the most, the outermost first


class Optimized:
    """The policy optimize() made faster: calling it calls the policy, whose modules now run what the switches turned
    on (in place: the policy itself runs it too). `report` says what is on, what is not and why, and the act's times;
    `on` is its list of the switches on."""

    def __init__(self, policy: Callable[..., Any], report: dict) -> None:
        self.policy, self.report = policy, report
        self.__wrapped__ = policy
        self.__qualname__ = getattr(policy, "__qualname__", None) or type(policy).__name__
        self.__name__ = getattr(policy, "__name__", None) or self.__qualname__

    @property
    def on(self) -> list[str]:
        return list(self.report["on"])

    def __call__(self, *args, **kwargs):
        return self.policy(*args, **kwargs)

    def __repr__(self) -> str:
        return f"Optimized({self.__qualname__}, on={self.on})"


class _Run(NamedTuple):
    item: Any        # what the policy is called with: an observation, or a list of them for a batch function
    seed: int        # the random state it runs from
    timed: bool      # one of the runs the act is timed on (a batch function's smallest size)


def check_switches(*, cuda_graphs: Optional[bool] = None, whole_graph: Optional[bool] = None,
                   torch_compile: bool = False, fused_kernels: bool = False, tensorrt: bool = False, precision: Optional[str] = None,
                   tolerance: Any = None) -> dict:
    """The switches asked for, as optimize() takes them, and `tolerance` as a dict of its limits; ValueError naming
    what is wrong: a switch that changes the outputs without `tolerance`, a precision that is none of None, "fp32",
    "fp16", "fp8", or fp8 with tensorrt. serve() checks them before it starts, so a mistake is said at once."""
    if precision not in PRECISIONS:
        raise ValueError(f"precision={precision!r}: it is None (the model's own dtype), \"fp32\", \"fp16\" or "
                         "\"fp8\"")
    changing = [name for name, on in (("torch_compile", torch_compile), ("fused_kernels", fused_kernels),
                                      ("tensorrt", tensorrt), (f"precision={precision!r}", precision is not None))
                if on]
    limits = _tolerance(tolerance)
    if changing and limits is None:
        said = " and ".join(changing)
        raise ValueError(f"{said} change{'s' if len(changing) == 1 else ''} the policy's outputs: give tolerance=, "
                         "the largest difference you accept from eager mode's - a number (the largest absolute "
                         "difference of any value), or {\"max_abs\": ..., \"mean_abs\": ..., \"cosine\": ...}")
    if tensorrt and precision == "fp8":
        raise ValueError("precision=\"fp8\" runs on torch's own FP8 multiply: with tensorrt, precision is None, "
                         "\"fp32\" or \"fp16\"")
    return {"cuda_graphs": None if cuda_graphs is None else bool(cuda_graphs),
            "whole_graph": None if whole_graph is None else bool(whole_graph), "torch_compile": bool(torch_compile),
            "fused_kernels": bool(fused_kernels), "tensorrt": bool(tensorrt), "precision": precision,
            "tolerance": limits}


def _tolerance(tolerance: Any) -> Optional[dict]:
    """`tolerance` as {"max_abs", "mean_abs", "cosine"}: a number is the largest absolute difference."""
    if tolerance is None:
        return None
    if isinstance(tolerance, bool) or not isinstance(tolerance, (int, float, dict)):
        raise ValueError(f"tolerance={tolerance!r}: a number (the largest absolute difference), or a dict of max_abs, "
                         "mean_abs and cosine")
    limits = {"max_abs": float(tolerance)} if isinstance(tolerance, (int, float)) else dict(tolerance)
    unknown = sorted(set(limits) - {"max_abs", "mean_abs", "cosine"})
    if unknown or not limits:
        raise ValueError(f"tolerance={tolerance!r}: its limits are max_abs, mean_abs and cosine"
                         + (f", not {', '.join(unknown)}" if unknown else ""))
    for name, value in limits.items():
        if isinstance(value, bool) or not isinstance(value, (int, float)) or not value > 0 or \
                (name == "cosine" and value > 1):
            raise ValueError(f"tolerance's {name}={value!r}: a number above 0" + (", 1 at most" if name == "cosine"
                                                                                 else ""))
        limits[name] = float(value)
    return limits


def optimize(policy: Callable[..., Any], examples: Any = None, *, batch: Optional[Iterable[int]] = None,
             cuda_graphs: Optional[bool] = None, whole_graph: Optional[bool] = None, torch_compile: bool = False,
             fused_kernels: bool = False, tensorrt: bool = False, precision: Optional[str] = None,
             tolerance: Any = None,
             min_speedup: float = MIN_SPEEDUP, seed: int = 0, budget_s: float = BUDGET_S,
             say: Callable[[str], Any] = print, capture: Optional[Callable[..., Any]] = None) -> Optimized:
    """
    `policy` made faster, each switch turned on only when the outputs on `examples` pass - bit for bit for
    cuda_graphs and whole_graph, within `tolerance` for the others - and the act is `min_speedup` faster with it (the
    module's docstring says what each switch does):

        fast = optimize(policy, examples)
        fast.report["switches"]["cuda_graphs"]    # {"on": True, "modules": [...], "speedup": 1.28, ...}: GR00T N1.7
                                                  # on an L4

    policy         the function serve() calls: an observation in, its output out; with `batch`, a list of
                   observations in and a list of outputs out, one for each
    examples       observations to check the outputs on: a list (32 or more of your robot's own are best), or one
    batch          the batch sizes serve() calls a batch function with: each is checked, its graphs captured here
    cuda_graphs, whole_graph   None: tried on a PyTorch policy, not on a JAX one (JAX_GRAPHS); True: tried; False:
                   not tried
    torch_compile, fused_kernels, tensorrt   True: tried, each needing `tolerance`
    precision      "fp16", "fp32" or "fp8": tried, needing `tolerance`; None: the model's own dtype
    tolerance      the largest difference accepted from eager mode's outputs: a number, or a dict of max_abs,
                   mean_abs and cosine; refused when a switch that changes the outputs is on without it
    min_speedup    how much faster the act must be for a switch to stay on: 1.1, 10%
    seed           the random state of the first run; each run has its own from there
    budget_s       the most seconds of timed acts for one switch
    say            where each switch's line goes (print); serve() sends them to its log
    capture        for tests: a stand-in for a CUDA graph (cuda_graphs.install's), so the checks run with no GPU

    The policy's modules are changed in place, so the policy itself runs what is on; the returned Optimized calls it
    and holds the report. A JAX policy has nothing for these switches (XLA compiles its whole run already), and is
    returned as it is, its report saying so. An Optimized is returned as it is: its policy was optimized already.
    """
    if isinstance(policy, Optimized):
        return policy
    asked = check_switches(cuda_graphs=cuda_graphs, whole_graph=whole_graph, torch_compile=torch_compile,
                           fused_kernels=fused_kernels, tensorrt=tensorrt, precision=precision, tolerance=tolerance)
    limits = asked.pop("tolerance")
    on = {name: (value is not None if name == "precision" else value) for name, value in asked.items()}
    examples = _examples(examples)
    sizes = None if batch is None else sorted({int(n) for n in batch})
    report: dict = {"on": [], "switches": {}, "examples": len(examples)}

    def off_all(why: str) -> Optimized:
        for name in SWITCHES:
            report["switches"][name] = {"on": False, "why": why if on[name] or on[name] is None else "turned off"}
        if any(on[name] or on[name] is None for name in SWITCHES):
            say(f"optimize: nothing turned on - {why}")
        return Optimized(policy, report)

    if not any(on[name] or on[name] is None for name in SWITCHES):
        return off_all("every switch is turned off")
    names = _namespace(policy)
    from . import cuda_graphs as graphs

    roots = graphs.modules_of(names) if "torch" in sys.modules else {}
    found = None
    if not roots and "jax" in sys.modules:
        from . import xla

        found = xla.find(names)                    # a JAX policy: the functions jax.jit made, where it holds them
    if not roots and not (found and found.jitted):
        return off_all("the policy holds no torch module" + (", and no function jax.jit made" if found else ""))
    if not examples:
        return off_all("no observation to check the outputs on: give examples=, or the policy a @seq.sample method")
    if not roots:
        return _jax(policy, found, examples, sizes, on, asked, limits, report, off_all,
                    dict(min_speedup=min_speedup, seed=seed, budget_s=budget_s, say=say))
    on.update({name: True for name in EXACT if on[name] is None})       # a PyTorch policy: the exact two by default
    import torch

    gpu = capture is not None or torch.cuda.is_available()
    if not gpu and not any(on[name] for name in CHANGING):
        return off_all("this machine has no CUDA GPU")
    runs = _runs(examples, sizes, seed)
    report["runs"] = len(runs)
    if len(examples) < FEW:
        report["note"] = (f"checked on {len(examples)} observation{'s' if len(examples) != 1 else ''}, each with "
                          f"several random states; {FEW} or more of your robot's own check more")
    kept_rng = _states()
    try:
        trial = _Trial(policy, runs, budget_s, min_speedup, say, limits, _digest(examples))
        trial.baseline(roots, graphs)
        if trial.skip:
            report["not_compared"] = sorted(trial.skip)
        if on["cuda_graphs"] and gpu and trial.exact_why is None:
            # cuda_graphs will be tried: each switch that changes the outputs is timed under its graphs, as it will run
            trial.stack = _Stack(trial, names, graphs, capture)
        try:
            for name in CHANGING:
                if not on[name]:
                    report["switches"][name] = {"on": False, "why": "turned off"}
                else:
                    report["switches"][name] = trial.changing(name, names, graphs, asked)
        finally:
            if trial.stack is not None:
                trial.stack.close()              # its graphs let go of: cuda_graphs captures and checks its own
                trial.stack = None
        for name in EXACT:
            if not on[name]:
                report["switches"][name] = {"on": False, "why": "turned off"}
            elif not gpu:
                report["switches"][name] = trial._off(name, "this machine has no CUDA GPU")
            elif trial.reference() is not None:
                report["switches"][name] = trial._off(name, trial.reference())
            elif name == "cuda_graphs":
                report["switches"][name], trial.graphed = trial.cuda_graphs(names, graphs, capture)
            else:
                report["switches"][name] = trial.whole_graph(names, graphs, capture, set(trial.graphed))
        if trial.now_stacked:
            # a switch kept under graphs that did not stay on (its graphs no faster, or not the same): the act as it
            # runs now, timed as it is
            trial.now_ms = round(trial.turns([lambda: None])[0], 2)
        report["on"] = [name for name in SWITCHES if report["switches"][name]["on"]]
        report["act_ms"] = {"eager": trial.eager_ms, "optimized": trial.now_ms}
    finally:
        _put_states(kept_rng)
    return Optimized(policy, report)


# What a JAX policy's switches that have no counterpart in XLA say (xla.py)
# Why the exact two are not tried on a JAX policy unless asked (True): on the JAX models measured, XLA's own programs
# left its command buffers about nothing to save, and a try compiles the model again for each switch - minutes
JAX_GRAPHS = ("a JAX policy: tried only when asked (True) - XLA's own programs leave its command buffers little to "
              "save, and a try compiles the model again")
_JAX_NONE = {"torch_compile": "a JAX model: XLA compiles each jitted function whole already",
             "fused_kernels": "a JAX model: XLA fuses its kernels already",
             "tensorrt": "a JAX model: TensorRT builds torch modules, and has no counterpart for JAX"}


def apply(policy: Callable[..., Any], report: dict, *, say: Callable[[str], Any] = print,
          capture: Optional[Callable[..., Any]] = None) -> Optimized:
    """
    The switches an earlier optimize() of this policy kept that leave its outputs exactly the same, put in place again
    without its checks: in another process that serves the policy built the same way - each replica of a policy
    served by many, or a server started again - once one process checked it.

        report = optimize(policy, examples).report      # where the policy is checked, once (JSON carries it)
        apply(policy, report)                           # where it is served again: no examples run, nothing timed

    cuda_graphs goes on the modules the report names and whole_graph on the call it names, and each new shape is still
    run in eager mode once, captured, and kept only where its graph answers byte for byte as eager mode did; a JAX
    policy's jitted functions are compiled with the command-buffer options it names. The switches that change the
    outputs are left off: each is checked where it is turned on. The Optimized it returns says what is on, and why
    each other switch is not.

    WHY optimize()'s checks are not run again: they run the policy on examples and time it, which a server cannot wait
    for at each start; what stays checked is each shape a graph is captured for, at its first call, as in optimize().
    """
    switches = dict((report or {}).get("switches") or {})
    out: dict = {"on": [], "switches": {}, "applied": True}
    for name in SWITCHES:
        kept = switches.get(name) or {}
        why = "turned off" if not kept.get("on") else "it changes the outputs: optimize() turns it on where it checks it"
        out["switches"][name] = {"on": False, "why": why}
    wanted = [name for name in EXACT if (switches.get(name) or {}).get("on")]
    if not wanted:
        return Optimized(policy, out)
    names = _namespace(policy)
    options = next((switches[name].get("xla_options") for name in reversed(wanted) if switches[name].get("xla_options")),
                   None)
    if options is not None:
        from . import xla

        found = xla.find(names)
        if not found.jitted:
            for name in wanted:
                out["switches"][name] = {"on": False, "why": "no function jax.jit made was found"}
            return Optimized(policy, out)
        for place in found.jitted:
            place.set(xla.Buffered(place.value, options))
        for name in wanted:
            out["switches"][name] = {"on": True, "xla_options": dict(switches[name].get("xla_options") or options)}
    else:
        import torch

        from . import cuda_graphs as graphs

        gpu = capture is not None or torch.cuda.is_available()
        for name in wanted:                                   # cuda_graphs before whole_graph, as optimize() puts them
            whole = name == "whole_graph"
            named = switches[name].get("call") if whole else switches[name].get("modules")
            paths = ([named] if named else []) if whole else list(named or [])
            installed = graphs.install(names, paths, say=say, capture=capture, whole=whole) if paths and gpu else {}
            if installed:
                out["switches"][name] = {"on": True, **({"call": paths[0]} if whole else {"modules": list(installed)})}
            else:
                why = ("the report names nothing to graph" if not paths else "this machine has no CUDA GPU" if not gpu
                       else "nothing it names could be graphed here")
                out["switches"][name] = {"on": False, "why": why}
    out["on"] = [name for name in SWITCHES if out["switches"][name]["on"]]
    if out["on"]:
        say(f"optimize: {', '.join(out['on'])} on, as an earlier check kept them")
    return Optimized(policy, out)


def _jax(policy, found, examples: list, sizes, on: dict, asked: dict, limits, report: dict, off_all,
         options: dict) -> Optimized:
    """optimize() for a JAX policy: each switch's counterpart in XLA (xla.py), judged as a torch switch is."""
    from . import xla

    say = options["say"]
    gpu = xla.gpu()

    def off(name: str, why: str) -> dict:
        say(f"optimize: {name} off - {why}")
        return {"on": False, "why": why}

    for name in ("tensorrt", "fused_kernels", "torch_compile"):
        report["switches"][name] = off(name, _JAX_NONE[name]) if on[name] else {"on": False, "why": "turned off"}
    for name in EXACT:
        if on[name] is None:                     # not asked for: left off, and said why (JAX_GRAPHS)
            report["switches"][name] = off(name, JAX_GRAPHS)
            on[name] = False
    cast = on["precision"] and asked["precision"] != "fp8"
    if on["precision"] and not cast:
        report["switches"]["precision"] = off("precision", "a JAX model: fp8 needs scaled multiplies its own code "
                                              "would make; precision=\"fp16\" changes its dtype alone")
    elif not on["precision"]:
        report["switches"]["precision"] = {"on": False, "why": "turned off"}
    graphs = [name for name in EXACT if on[name]]
    if not gpu:
        for name in EXACT:
            report["switches"][name] = off(name, "JAX runs on no GPU here") if on[name] else \
                {"on": False, "why": "turned off"}
        graphs = []
    if not cast and not graphs:
        for name in EXACT:
            report["switches"].setdefault(name, {"on": False, "why": "turned off"})
        return Optimized(policy, report)
    runs = _runs(examples, sizes, options["seed"])
    report["runs"] = len(runs)
    if len(examples) < FEW:
        report["note"] = (f"checked on {len(examples)} observation{'s' if len(examples) != 1 else ''}, each with "
                          f"several random states; {FEW} or more of your robot's own check more")
    kept = _states()
    trial = _Trial(policy, runs, options["budget_s"], options["min_speedup"], say, limits, _digest(examples),
                   seed_with=found.seed)
    try:
        trial.baseline(None, None)
        if trial.skip:
            report["not_compared"] = sorted(trial.skip)
        if cast:
            report["switches"]["precision"] = trial.jax_precision(found, asked["precision"])
        for name in ("cuda_graphs", "whole_graph"):
            options = xla.GRAPHS if name == "cuda_graphs" else xla.whole()
            if name not in graphs:
                report["switches"].setdefault(name, {"on": False, "why": "turned off"})
            elif trial.reference() is not None:
                report["switches"][name] = trial._off(name, trial.reference())
            elif options is None:
                report["switches"][name] = trial._off(name, "no way of naming loops puts one in a command buffer with "
                                                            "this version of XLA")
            else:
                report["switches"][name] = trial.jax_graphs(name, found, options)
        report["on"] = [name for name in SWITCHES if report["switches"][name]["on"]]
        report["act_ms"] = {"eager": trial.eager_ms, "optimized": trial.now_ms}
    finally:
        found.put_back_keys()
        _put_states(kept)
    return Optimized(policy, report)


class _Runs:
    """How one module the act spends its time in runs now: itself, or its float16 copy (`half`), by its own forward or
    by an engine (compiled, or built by TensorRT)."""

    def __init__(self, target, module=None, half: bool = False, engine=None, dtype=None, to=None) -> None:
        self.target, self.module, self.half, self.engine = target, module or target, half, engine
        self.dtype, self.to = dtype, to          # with a copy in another dtype (`half`): the module's, the copy's

    def but(self, **changed) -> "_Runs":
        fields = dict(target=self.target, module=self.module, half=self.half, engine=self.engine, dtype=self.dtype,
                      to=self.to)
        fields.update(changed)
        return _Runs(**fields)

    def forward(self) -> Optional[Callable]:
        """What the target's forward is: None for its class's own."""
        from .compiled import cast_around

        if not self.half and self.engine is None:
            return None
        run = self.engine if self.engine is not None else self.module
        return cast_around(run, self.dtype, self.to) if self.half else run


class _Trial:
    """The checks of one optimize(): the eager outputs every switch is held to, and each switch's check and timing."""

    def __init__(self, policy, runs: list[_Run], budget_s: float, min_speedup: float, say, limits, key: str,
                 seed_with: Optional[Callable[[int], Any]] = None) -> None:
        self.policy, self.runs, self.budget_s, self.min_speedup, self.say = policy, runs, budget_s, min_speedup, say
        self.limits, self.key, self.seed_with = limits, key, seed_with     # seed_with: a JAX policy's keys, each run
        self.takes_seed = _takes_seed(policy)    # a policy that takes seed=: given each run's, its noise from it
        self.eager: list = []
        self.skip: set = set()                   # values that change from run to run with the same random state
        self.exact_why: Optional[str] = None     # why no exact switch can be checked, when none can
        self.census = self.calls = None
        self.eager_ms: Optional[float] = None    # the act's median time in eager mode, and with what is on now
        self.now_ms: Optional[float] = None
        self.now_stacked = False                 # now_ms was timed under a _Stack's graphs, which are not on (yet)
        self.changed: list[str] = []             # the switches kept that change the outputs
        self.runs_of: dict = {}                  # each target module's path: how it runs (_Runs)
        self.engines: set = set()                # the targets TensorRT runs
        self.graphed: list = []                  # the modules cuda_graphs kept
        self.stack: Optional[_Stack] = None      # the graphs a switch that changes the outputs is timed under, if any
        self._reference: Optional[list] = None
        self._reference_why: Any = False

    # ── running ─────────────────────────────────────────────────────────────────────────────────────────────────────
    def play(self, run: _Run) -> tuple[Any, float]:
        """The policy on one run: its output, as the robot would get it, and the act's milliseconds."""
        try:
            item = copy.deepcopy(run.item)        # each call its own observation: a policy may write into it
        except Exception:  # noqa: BLE001 (an observation holding what cannot be copied is passed as it is)
            item = run.item
        _seed_all(run.seed)
        if self.seed_with is not None:
            self.seed_with(run.seed)
        kwargs = {}
        if self.takes_seed:                       # a batch function's acts each their own seed, as an eval's are
            kwargs["seed"] = [run.seed * 1000 + j for j in range(len(item))] if isinstance(item, list) else run.seed
        started = time.perf_counter()
        out = _host(self.policy(item, **kwargs))  # copied off the GPU, so its time is in the act's
        return out, (time.perf_counter() - started) * 1e3

    def baseline(self, roots: dict, graphs) -> None:
        """Eager mode's outputs on every run, its modules' calls counted the while; then every run again: a value
        that changed is a measurement of the run, left out of every comparison, unless it is an array - then no exact
        switch can be checked. With no torch module (`roots` None: a JAX model), nothing is counted."""
        if roots is None:
            self.eager = [self.play(run)[0] for run in self.runs]
        else:
            self.census, self.calls = graphs.Census(roots), graphs.Calls(roots)
            try:
                for run in self.runs:
                    self.eager.append(self.play(run)[0])
                    self.census.end_act()
            finally:
                self.census.close()
            for run in self.runs[:2]:
                with self.calls.run():
                    self.play(run)
        varying: set = set()
        for run, first in zip(self.runs, self.eager):
            varying |= _varying(first, self.play(run)[0])
        arrays = sorted(path for path in varying if path.startswith("array:"))
        self.skip = {path.split(":", 1)[1] for path in varying if path.startswith("scalar:")}
        if arrays:
            leaf = arrays[0].split(":", 1)[1] or "its output"
            self.exact_why = (f"its outputs ({leaf}) differ from one eager run to the next with the same random state, "
                              "so no switch can be shown to keep them exactly")

    def reference(self) -> Optional[str]:
        """Why the exact switches cannot be checked, or None: then `_reference` holds the outputs they are held to,
        eager mode's or, with switches that change them on, those of what runs now (seen to repeat)."""
        if self._reference_why is not False:
            return self._reference_why
        self._reference_why = self.exact_why
        if self.exact_why is None:
            self._reference = self.eager
            if self.changed:
                first = [self.play(run)[0] for run in self.runs]
                for run, want in zip(self.runs, first):
                    if not _same(self.play(run)[0], want, self.skip):
                        self._reference_why = (f"with {' and '.join(self.changed)} on, its outputs differ from one run "
                                               "to the next with the same random state, so no graph can be shown to "
                                               "keep them exactly")
                        break
                self._reference = first
        return self._reference_why

    def check(self, toggle: Callable[[bool], Any], exact: bool) -> tuple[Optional[str], Optional[dict]]:
        """Every run with the switch on, its outputs against what they are held to - bit for bit (`exact`), or eager
        mode's within the tolerance: (why they do not pass, or None; the largest differences found). A policy whose
        own code raises with the switch on refuses it."""
        toggle(True)
        held = self._reference if exact else self.eager
        worst: dict = {}
        for i, (run, want) in enumerate(zip(self.runs, held)):
            try:
                got = self.play(run)[0]
            except Exception as exc:  # noqa: BLE001 (its own code refused the switch: the switch is taken out)
                return f"the policy raised with it on: {type(exc).__name__}: {str(exc)[:160]}", None
            where = f"on run {i + 1} of {len(self.runs)}"
            if exact:
                if not _same(got, want, self.skip):
                    return f"its outputs differed from {'eager mode' if not self.changed else 'what ran before it'}'s " \
                           f"{where}{_largest(want, got, self.skip)}", None
                continue
            found = differences(want, got, self.skip)
            if found is None:
                return f"its outputs were not shaped as eager mode's {where}", None
            for name, value in found.items():
                worst[name] = min(worst.get(name, 1.0), value) if name == "cosine" else max(worst.get(name, 0.0), value)
            for name, limit in self.limits.items():
                value = found[name]
                if (value < limit) if name == "cosine" else (value > limit):
                    return (f"its {name} from eager mode's was {value:.3g} {where}, past the {limit:g} of the "
                            "tolerance"), _rounded(worst)
        return None, _rounded(worst) if worst else None

    def timed(self, toggle: Callable[[bool], Any]) -> tuple[float, float]:
        """The act's median milliseconds without the switch and with it, timed in turns on the timed runs."""
        before, after = self.turns([lambda: toggle(False), lambda: toggle(True)])
        return before, after

    def turns(self, arms: list) -> list[float]:
        """The act's median milliseconds with each of `arms` in place - each a callable that puts its own in place -
        timed in turns on the timed runs, so that a machine that slows or speeds up slows or speeds up each alike."""
        runs = [run for run in self.runs if run.timed]
        times: list = [[] for _ in arms]
        started = time.perf_counter()
        for k in range(TIMED):
            if k >= 3 and time.perf_counter() - started > self.budget_s:
                break
            run = runs[k % len(runs)]
            for arm, got in zip(arms, times):
                arm()                                  # its own switches in place, then one act timed with them
                got.append(self.play(run)[1])
        return [statistics.median(got) for got in times]

    def verdict(self, name: str, toggle: Callable[[bool], Any], detail: dict, said: Any, *, exact: bool = True,
                kept: Callable[[], Optional[str]] = lambda: None, stack: Optional["_Stack"] = None) -> dict:
        """A switch already in place, checked and timed: on, with its times; or off, with why. `kept`, once its outputs
        passed: why it is not in place after all (a graph that kept no shape), or None. `stack`: the graphs it is timed
        under in both turns (_Stack), or None to time it as it is; its outputs are checked without them either way."""
        why, worst = self.check(toggle, exact)
        if worst:
            detail = {**detail, "differences": worst}
        why = why or kept()
        if why is not None:
            toggle(False)
            return self._off(name, why, detail)
        before, after = self.timed(toggle) if stack is None else stack.timed(toggle)
        speedup = before / after if after > 0 else math.inf
        times = {"act_ms": {"before": round(before, 2), "after": round(after, 2)}, "speedup": round(speedup, 2)}
        act = f"act {before:.1f} → {after:.1f} ms"
        if stack is not None:                      # its times are under the graphs: the report and its line say so
            times["timed_with"] = "cuda_graphs"
            act += " with cuda_graphs on in both"
        if speedup < self.min_speedup:
            toggle(False)
            faster = round((speedup - 1) * 100)
            needs = round((self.min_speedup - 1) * 100)
            return self._off(name, f"{faster}% faster ({act}), under the {needs}% it needs" if faster > 0
                             else f"no faster with it ({act})", {**detail, **times})
        if self.eager_ms is None and stack is None:      # under graphs, `before` is not eager mode's (_Stack times it)
            self.eager_ms = round(before, 2)
        self.now_ms = round(after, 2)
        self.now_stacked = stack is not None
        said = said() if callable(said) else said
        held = "the same outputs, bit for bit," if exact else "its outputs within the tolerance"
        found = detail.get("differences")         # a switch that changes them: its largest differences, on its line too
        largest = f" (largest differences: {', '.join(f'{k} {v:g}' for k, v in found.items())})" if found else ""
        self.say(f"optimize: {name} on - {said}: {held} on {len(self.runs)} runs{largest}; {act}")
        return {"on": True, **detail, **times, "checked": len(self.runs)}

    def _off(self, name: str, why: str, detail: Optional[dict] = None) -> dict:
        self.say(f"optimize: {name} off - {why}")
        return {"on": False, "why": why, **(detail or {})}

    # ── the switches that change the outputs ────────────────────────────────────────────────────────────────────────
    def targets(self, names: dict, graphs) -> dict:
        """The modules the act spends its time in, by path: those called more than once a run (the census'
        candidates), or else the outermost it calls."""
        if not self.runs_of:
            rows = self.census.candidates(most=None) or self.census.called()
            for row in rows:
                try:
                    module, method = graphs._target(names, row["path"])
                except (LookupError, TypeError):
                    continue
                if method == "forward":
                    self.runs_of[row["path"]] = _Runs(module)
        return self.runs_of

    def changing(self, name: str, names: dict, graphs, asked: dict) -> dict:
        """One switch that changes the outputs, tried on the target modules: its verdict."""
        targets = self.targets(names, graphs)
        if not targets:
            return self._off(name, "no module of the policy runs with one shape a run to apply it to")
        try:
            if name == "precision":
                found = self._precision(asked["precision"])
            elif name == "tensorrt":
                found = self._tensorrt()
            elif name == "fused_kernels":
                found = self._fused()
            else:
                found = self._compiled()
        except Exception as exc:  # noqa: BLE001 (a switch that cannot be put in place is off, said why)
            return self._off(name, f"it could not be put in place: {type(exc).__name__}: {str(exc)[:200]}")
        if isinstance(found, str):
            return self._off(name, found)
        patches, after, detail, said = found
        from . import fused

        def toggle(on: bool) -> None:
            (fused.reapply if on else fused.uninstall)(patches)

        stack = self.stack if self.stack is not None and self.stack.paths else None
        result = self.verdict(name, toggle, detail, said, exact=False, stack=stack)
        if stack is not None:
            stack.settle(result["on"])            # what runs from now on: what was timed with the switch, or without it
        if result["on"]:
            self.runs_of.update(after)
            self.changed.append(name if name != "precision" else f"precision={asked['precision']!r}")
            if name == "tensorrt":
                self.engines |= set(after)
        else:
            fused.uninstall(patches)
        return result

    def _forward_patches(self, after: dict) -> list:
        """The patches putting each target's new way of running in front of its forward."""
        from .fused import _ABSENT, Patch

        patches = []
        for path, runs in after.items():
            target = runs.target
            patches.append(Patch(target, "forward", runs.forward(), vars(target).get("forward", _ABSENT), path))
        return patches

    def _precision(self, precision: str):
        import torch

        from . import compiled, fp8

        if precision in ("fp16", "fp32"):
            to = torch.float16 if precision == "fp16" else torch.float32
            after, already = {}, []
            for path, runs in self.runs_of.items():
                dtype = next((p.dtype for p in runs.module.parameters() if p.is_floating_point()), None)
                if dtype == to:
                    already.append(path)
                    continue
                after[path] = runs.but(module=compiled.dtype_copy(runs.module, to), half=True, dtype=dtype, to=to)
            if not after:
                return f"the modules run in {str(to).replace('torch.', '')} already"
            return self._forward_patches(after), after, {"precision": precision, "modules": list(after)}, \
                f"{', '.join(after)} in {str(to).replace('torch.', '')}"
        why = fp8.unsupported()
        if why is not None:
            return why
        patches = fp8.install(self._held(self.runs_of), calibrate=self._calibrate, key=self.key, say=self.say)
        fp8.uninstall(patches)                    # in place again by the verdict's toggle
        if not patches:
            return "no linear layer of its modules keeps its outputs close in fp8, or none can run in it"
        return patches, {}, {"precision": "fp8", "layers": len(patches)}, f"{len(patches)} linear layers in fp8"

    def _tensorrt(self):
        from . import compiled

        inputs = self._inputs()
        after, whys = {}, []
        for path, runs in self.runs_of.items():
            if path not in inputs:
                whys.append(f"{path} was not called")
                continue
            args, kwargs = inputs[path]
            if runs.half:
                args, kwargs = _to_dtype(args, runs.to), _to_dtype(kwargs, runs.to)
            try:
                engine = compiled.tensorrt(runs.module, args, kwargs, say=self.say)
            except Exception as exc:  # noqa: BLE001 (a module TensorRT cannot build is left as it runs)
                whys.append(f"{path}: {type(exc).__name__}: {str(exc)[:160]}")
                continue
            after[path] = runs.but(engine=engine)
        if not after:
            return "; ".join(whys) or "no module could be built"
        return self._forward_patches(after), after, {"modules": list(after)}, f"{', '.join(after)} in TensorRT"

    def _fused(self):
        from . import fused

        running = {path: runs for path, runs in self.runs_of.items() if path not in self.engines}
        if not running:
            return "the modules run in TensorRT, whose engines take no other kernel"
        patches = fused.install(self._held(running), say=lambda line: None)
        fused.uninstall(patches)                  # in place again by the verdict's toggle
        if not patches:
            return "no norm, gated activation or rotary embedding of its modules is one the fused kernels compute alike"
        return patches, {}, {"replaced": [patch.what for patch in patches]}, f"{len(patches)} replaced"

    def _compiled(self):
        from . import compiled

        after = {path: runs.but(engine=compiled.torch_compile(runs.module))
                 for path, runs in self.runs_of.items() if path not in self.engines}
        if not after:
            return "the modules run in TensorRT already"
        return self._forward_patches(after), after, {"modules": list(after)}, f"{', '.join(after)} compiled"

    def _held(self, runs_of: dict):
        """The modules that run, together under one module (each by its path), for fused and fp8 to walk once."""
        import torch

        return torch.nn.ModuleDict({path.replace(".", "/") or "model": runs.module for path, runs in runs_of.items()})

    def _calibrate(self) -> None:
        for run in self.runs:
            self.play(run)

    def _inputs(self) -> dict:
        """Each target module's inputs on one run, as it got them: (args, kwargs) copied, for TensorRT to build on."""
        from .cuda_graphs import _static

        found: dict = {}
        hooks = []
        for path, runs in self.runs_of.items():
            def hook(module, args, kwargs, path=path):
                found.setdefault(path, (_static(tuple(args)), _static(dict(kwargs))))
            hooks.append(runs.target.register_forward_pre_hook(hook, with_kwargs=True))
        try:
            self.play(self.runs[0])
        finally:
            for hook in hooks:
                hook.remove()
        return found

    # ── a JAX policy's ──────────────────────────────────────────────────────────────────────────────────────────────
    def jax_graphs(self, name: str, found, options: dict) -> dict:
        """Each jitted function compiled with XLA `options` added to its defaults, in place of what runs now: kept
        when the outputs stay the same and the act is faster."""
        from . import xla

        before = [place.get() for place in found.jitted]
        after = [xla.Buffered(place.value, options) for place in found.jitted]

        def toggle(on: bool) -> None:
            for place, old, new in zip(found.jitted, before, after):
                place.set(new if on else old)

        said = "XLA command buffers " + ("with its loops in them, " if "xla_gpu_enable_command_buffer" in options
                                         else "") + "down to graphs of one operation"
        result = self.verdict(name, toggle, {"xla_options": dict(options)}, said)
        if not result["on"]:
            toggle(False)
        return result

    def jax_precision(self, found, precision: str) -> dict:
        """The parameter trees its jitted functions close over, cast to `precision`'s dtype: kept within the
        tolerance and faster."""
        from . import xla

        if not found.trees:
            return self._off("precision", "no parameter tree was found beside its jitted functions")
        import jax.numpy as jnp

        dtype = jnp.float16 if precision == "fp16" else jnp.float32
        cast = [xla.cast(place.value, dtype) for place in found.trees]

        def toggle(on: bool) -> None:
            for place, new in zip(found.trees, cast):
                place.set(new if on else place.value)

        result = self.verdict("precision", toggle, {"precision": precision, "trees": len(cast)},
                              f"its parameters in {jnp.dtype(dtype).name}", exact=False)
        if result["on"]:
            self.changed.append(f"precision={precision!r}")
        else:
            toggle(False)
        return result

    # ── the switches that keep the outputs exactly ──────────────────────────────────────────────────────────────────
    def cuda_graphs(self, names: dict, graphs, capture) -> tuple[dict, list[str]]:
        """Every module the census found, graphed; kept, all of them, when the outputs stay the same and the act is
        faster."""
        found = self.census.candidates(most=None)
        if not found:
            return self._off("cuda_graphs", "no module is called more than once a run with the same shapes"), []
        paths = [row["path"] for row in found]
        installed = graphs.install(names, paths, say=_quiet, capture=capture)
        if not installed:
            return self._off("cuda_graphs", "no module could be graphed"), []

        def toggle(on: bool) -> None:
            for graphed in installed.values():
                graphed.on = on

        def kept() -> Optional[str]:
            """Every module that kept no graph taken out again; why none did, when none did."""
            idle = [path for path, graphed in installed.items() if not graphed.graphs]
            why = _none_kept(installed) if len(idle) == len(installed) else None
            graphs.uninstall(names, idle)
            for path in idle:
                installed.pop(path)
            return why

        calls = {row["path"]: row["calls"] for row in found}
        result = self.verdict("cuda_graphs", toggle, {"modules": list(installed)},
                              lambda: ", ".join(f"{path} ({calls[path]} calls a run)" for path in installed),
                              kept=kept)
        if not result["on"]:
            graphs.uninstall(names, list(installed))
            return result, []
        result["modules"] = list(installed)
        return result, list(installed)

    def whole_graph(self, names: dict, graphs, capture, modules: set) -> dict:
        """The outermost calls a run makes into the model, tried one at a time as a whole graph: the first whose
        outputs stay the same and whose act is faster than with the modules alone stays on."""
        tried = [row for row in self.calls.outermost(most=WHOLE_TRIES + len(modules)) if row["path"] not in modules]
        tried = tried[:WHOLE_TRIES]
        if not tried:
            return self._off("whole_graph", "the model's calls were not found")
        whys = []
        for row in tried:
            path = row["path"]
            installed = graphs.install(names, [path], say=_quiet, capture=capture, whole=True)
            graphed = installed.get(path)
            if graphed is None:
                whys.append(f"{path} could not be graphed")
                continue

            def toggle(on: bool, graphed=graphed) -> None:
                graphed.on = on

            try:
                self.play(self.runs[0])                   # its first shape captured, or why not
            except Exception as exc:  # noqa: BLE001 (its own code refused it: the next call is tried)
                whys.append(f"{path}: the policy raised with it on: {type(exc).__name__}: {str(exc)[:160]}")
                graphs.uninstall(names, [path])
                continue
            if not graphed.graphs:
                whys.append(f"{path}: {_why_none(graphed)}")
                graphs.uninstall(names, [path])
                continue
            result = self.verdict("whole_graph", toggle, {"call": path}, f"{path}, one graph a run",
                                  kept=lambda graphed=graphed: None if graphed.graphs else _why_none(graphed))
            if result["on"]:
                return result
            whys.append(f"{path}: {result['why']}")
            graphs.uninstall(names, [path])
        return self._off("whole_graph", "; ".join(whys))


class _Stack:
    """The modules cuda_graphs graphs, graphed under a switch that changes the outputs while it is timed (where
    cuda_graphs is to be tried): one set of graphs of what runs without the switch - kept from one switch to the next
    while that is still what runs - and one of what runs with it, each put in front of its modules' forward for its own
    turns and taken out after. Both are let go of once the switches are judged: cuda_graphs, tried after them, captures
    and checks its own on what is kept.

    WHY two sets, swapped in front of the forward, and not one turned on and off: a graph replays the kernels it
    captured, so a set captured without the switch would replay the model without it whichever way the switch is."""

    def __init__(self, trial: _Trial, names: dict, graphs, capture) -> None:
        self.trial, self.names, self.graphs, self.capture = trial, names, graphs, capture
        self.paths = [row["path"] for row in trial.census.candidates(most=None)]    # the modules cuda_graphs graphs
        self.under: Optional[dict] = None        # {path: Graphed} of what runs now, without the switch being timed
        self.over: Optional[dict] = None         # {path: Graphed} of what runs with it

    def timed(self, toggle: Callable[[bool], Any]) -> tuple[float, float]:
        """The act's median milliseconds without the switch and with it, each under its own graphs, timed in turns;
        the switch left on, with no graph in front of it. While no switch is on and nothing has timed eager mode, its
        own time too, in the same turns (the report's eager time)."""
        toggle(False)
        if self.under is None:
            self.under = self._captured()        # captured once, then kept while it is what runs (settle)
        toggle(True)
        self.over = self._captured()
        arms = [lambda: self._turn(toggle, False, self.under), lambda: self._turn(toggle, True, self.over)]
        eager = self.trial.eager_ms is None and not self.trial.changed
        if eager:
            arms.append(lambda: self._turn(toggle, False, {}))     # nothing on, no graph: eager mode
        try:
            times = self.trial.turns(arms)
        finally:
            self._turn(toggle, True, {})          # as verdict expects it after timing: the switch on, alone
        if eager:
            self.trial.eager_ms = round(times[2], 2)
        return times[0], times[1]

    def settle(self, kept: bool) -> None:
        """After a switch's verdict: what runs now is what was timed with it (kept) or without it; the other set's
        graphs let go of."""
        if self.over is None:                     # its outputs did not pass: nothing was captured for it
            return
        if kept:
            self.under, dropped = self.over, self.under
        else:
            dropped = self.over
        self.over = None
        _drop(dropped)

    def close(self) -> None:
        """Every graph taken out of the modules and let go of."""
        for graphed in (self.under, self.over):
            self._take(graphed or {})
            _drop(graphed)
        self.under = self.over = None

    def _turn(self, toggle: Callable[[bool], Any], on: bool, graphed: dict) -> None:
        """The switch on or off, with `graphed` in front of its modules' forward ({}: none)."""
        for one in (self.under, self.over):
            self._take(one or {})                 # whichever is in front: what was there before it, there again
        toggle(on)
        for path, one in graphed.items():
            module, method = self.graphs._target(self.names, path)
            setattr(module, method, one)

    def _captured(self) -> dict:
        """Graphs of what runs now: the modules graphed (cuda_graphs.install), each timed run played once so that its
        shape is captured - or left in eager mode, as cuda_graphs would leave it - and taken out again."""
        installed = self.graphs.install(self.names, self.paths, say=_quiet, capture=self.capture)
        try:
            for run in self.trial.runs:
                if run.timed:
                    self.trial.play(run)
        finally:
            self._take(installed)
        return installed

    def _take(self, graphed: dict) -> None:
        """Each graph of `graphed` that is in front of its module's forward taken out, its graphs kept: what was there
        before it (its class's forward, or the one a switch put there), there again."""
        for path, one in graphed.items():
            module, method = self.graphs._target(self.names, path)
            if vars(module).get(method) is not one:
                continue
            if one.before is self.graphs._NONE:
                delattr(module, method)
            else:
                setattr(module, method, one.before)


def _drop(graphed: Optional[dict]) -> None:
    """A set of graphs let go of, the memory they hold with them."""
    for one in (graphed or {}).values():
        one.graphs.clear()


def _quiet(line: str) -> None:
    """The graphs' own lines while they are tried: what each switch comes to is said once, by its verdict."""


def _none_kept(installed: dict) -> str:
    """Why no module kept a graph: the first one's reason that has one."""
    for path, graphed in installed.items():
        why = _why_none(graphed)
        if why:
            return f"{path}: {why}"
    return "no graph was kept"


def _why_none(graphed) -> str:
    """Why a Graphed kept no graph: its first shape's reason, or that its calls could not be keyed on."""
    from .cuda_graphs import WHY_EAGER

    for kind, error in graphed.report()["eager"]:
        return WHY_EAGER[kind].format(error)
    if graphed.unkeyed:
        return "it is called with an argument a graph cannot be keyed on"
    return "it was not called"


def _to_dtype(value: Any, dtype: Any) -> Any:
    import torch

    if isinstance(value, torch.Tensor):
        return value.to(dtype) if value.is_floating_point() else value
    if type(value) in (list, tuple):
        return type(value)(_to_dtype(v, dtype) for v in value)
    if type(value) is dict:
        return {k: _to_dtype(v, dtype) for k, v in value.items()}
    return value


def _takes_seed(policy: Any) -> bool:
    """Whether the policy takes a `seed` keyword."""
    try:
        return "seed" in inspect.signature(policy).parameters
    except (TypeError, ValueError):
        return False


def _examples(examples: Any) -> list:
    """The examples as a list: None as none, one observation (a dict, or anything but a list or tuple) as a list of it."""
    if examples is None:
        return []
    if isinstance(examples, (list, tuple)):
        return list(examples)
    return [examples]


def _runs(examples: list, sizes: Optional[list[int]], seed: int) -> list[_Run]:
    """What each check runs: every example at least once, and again with another seed until MIN_RUNS - for a batch
    function in lists of its smallest size, and once at each of its other sizes."""
    first = 1 if sizes is None else sizes[0]
    runs = []
    for i in range(max(len(examples), MIN_RUNS)):
        if sizes is None:
            item = examples[i % len(examples)]
        else:
            item = [examples[(i + j) % len(examples)] for j in range(first)]
        runs.append(_Run(item, seed + i, True))
    for size in (sizes or [])[1:]:
        runs.append(_Run([examples[j % len(examples)] for j in range(size)], seed + 100_000 + size, False))
    return runs


def _namespace(policy: Any) -> dict[str, Any]:
    """What a policy reaches, by name, for its torch modules to be found in (cuda_graphs.modules_of): a bound method's
    object and a callable object, as "self"; a function's closure, and the globals its code names - also in the
    functions it calls by name, two levels down; a bound method among them by its object (`seq serve`'s call holds the
    policy's infer, bound to the policy)."""
    import functools

    out: dict[str, Any] = {}

    def add(name: str, value: Any) -> None:
        if value is not None and not isinstance(value, (types.ModuleType, type)) and not inspect.isroutine(value):
            out.setdefault(name, value)

    def names_of(code: types.CodeType) -> set[str]:
        found = set(code.co_names)
        for const in code.co_consts:
            if isinstance(const, types.CodeType):
                found |= names_of(const)                   # a comprehension's or a lambda's, inside it
        return found

    def take(name: str, value: Any, left: int) -> None:
        """One value the policy's code holds: a function walked, a bound method's object added under its name and its
        function walked, anything else added."""
        if inspect.ismethod(value):
            add(name, value.__self__)
            if left:
                walk(value.__func__, left - 1)
        elif inspect.isfunction(value) or isinstance(value, functools.partial):
            if left:
                walk(value, left - 1)
        else:
            add(name, value)

    def walk(fn: Any, left: int) -> None:
        if isinstance(fn, functools.partial):
            for i, arg in enumerate(fn.args):
                take(f"arg{i}", arg, left)
            for key, arg in fn.keywords.items():
                take(key, arg, left)
            walk(fn.func, left)
            return
        if inspect.ismethod(fn):
            add("self", fn.__self__)
            walk(fn.__func__, left)
            return
        if not inspect.isfunction(fn):
            if callable(fn):
                add("self", fn)
            return
        for name, cell in zip(fn.__code__.co_freevars, fn.__closure__ or ()):
            try:
                value = cell.cell_contents
            except ValueError:                             # a closure variable not yet assigned
                continue
            take(name, value, left)
        for name in sorted(names_of(fn.__code__)):
            if name in fn.__globals__:
                take(name, fn.__globals__[name], left)

    walk(policy, 2)
    return out


def _states() -> tuple:
    """Every global random state the checks draw from: Python's, NumPy's (where imported), torch's (where imported:
    the CPU's, and the current GPU's where CUDA is in use)."""
    np = sys.modules.get("numpy")
    torch = sys.modules.get("torch")
    gpu = None
    if torch is not None and torch.cuda.is_available() and torch.cuda.is_initialized():
        gpu = torch.cuda.get_rng_state()
    return (random.getstate(), np.random.get_state() if np is not None else None,
            torch.get_rng_state() if torch is not None else None, gpu)


def _put_states(states: tuple) -> None:
    py, np_state, cpu, gpu = states
    random.setstate(py)
    if np_state is not None:
        sys.modules["numpy"].random.set_state(np_state)
    torch = sys.modules.get("torch")
    if torch is not None and cpu is not None:
        torch.set_rng_state(cpu)
        if gpu is not None:
            torch.cuda.set_rng_state(gpu)


def _seed_all(seed: int) -> None:
    """Python's, NumPy's and torch's generators, the CPU's and every GPU's, seeded from `seed`."""
    random.seed(seed)
    np = sys.modules.get("numpy")
    if np is not None:
        np.random.seed(seed % (2 ** 32))
    torch = sys.modules.get("torch")
    if torch is not None:
        torch.manual_seed(seed)                        # every GPU's too, where CUDA is in use


def _digest(value: Any) -> str:
    """A short digest of the examples' contents, for a calibration kept on disk to be told apart."""
    h = hashlib.sha256()

    def feed(item: Any) -> None:
        if isinstance(item, dict):
            for key in sorted(item, key=str):
                h.update(f"<{key}>".encode())
                feed(item[key])
        elif isinstance(item, (list, tuple)):
            h.update(b"[")
            for sub in item:
                feed(sub)
            h.update(b"]")
        elif hasattr(item, "tobytes") and hasattr(item, "dtype"):
            h.update(f"{item.dtype}{getattr(item, 'shape', ())}".encode())
            h.update(item.tobytes())
        else:
            h.update(repr(item).encode())

    feed(value)
    return h.hexdigest()[:24]


def _host(value: Any) -> Any:
    """An output as the robot would get it: each torch tensor (copied off the GPU, which waits for it) and JAX array in
    it as a numpy array, a dtype numpy has none of (bfloat16, float8) as float32 - which keeps its every value."""
    if isinstance(value, dict):
        return {key: _host(item) for key, item in value.items()}
    if type(value) in (list, tuple):
        return type(value)(_host(item) for item in value)
    if isinstance(value, (list, tuple)):
        return [_host(item) for item in value]            # a named tuple, as msgpack sends it: its items in a list
    if value is None or isinstance(value, (str, bytes, bytearray, bool, int, float)):
        return value
    if callable(getattr(value, "detach", None)) and callable(getattr(value, "cpu", None)):   # a torch tensor
        tensor = value.detach().cpu()
        try:
            return tensor.numpy()
        except TypeError:
            return tensor.float().numpy()
    if hasattr(value, "__array__") and not hasattr(value, "tobytes"):
        import numpy as np

        return np.asarray(value)
    return value


def _leaves(value: Any, path: str = "") -> dict:
    """Every value of an output by its place in it (`actions`, `chunks[0]`): its structure flattened."""
    if isinstance(value, dict):
        out: dict = {}
        for key, item in value.items():
            out.update(_leaves(item, f"{path}.{key}" if path else str(key)))
        return out or {path: {}}
    if isinstance(value, (list, tuple)):
        out = {}
        for i, item in enumerate(value):
            out.update(_leaves(item, f"{path}[{i}]"))
        return out or {path: type(value)()}
    return {path: value}


def _same_leaf(a: Any, b: Any) -> bool:
    """Two values equal byte for byte: an array of the same dtype, shape and bytes; a float of the same bits (a NaN is
    the NaN it was, -0.0 is not 0.0)."""
    if isinstance(a, float) and isinstance(b, float):
        return struct.pack("<d", a) == struct.pack("<d", b)
    if hasattr(a, "tobytes") and hasattr(b, "tobytes") and hasattr(a, "dtype") and hasattr(b, "dtype"):
        return a.dtype == b.dtype and a.shape == b.shape and a.tobytes() == b.tobytes()
    return type(a) is type(b) and a == b


def _same(a: Any, b: Any, skip: Iterable[str] = ()) -> bool:
    """Two outputs equal byte for byte, but for the values at `skip` (measurements of a run): the same structure and
    each value the same."""
    left, right = _leaves(a), _leaves(b)
    if left.keys() != right.keys():
        return False
    skip = set(skip)
    return all(path in skip or _same_leaf(left[path], right[path]) for path in left)


def _varying(a: Any, b: Any) -> set:
    """The values two runs of the same input gave differently, each as "array:<place>" or "scalar:<place>"; a
    difference of structure as an array's."""
    left, right = _leaves(a), _leaves(b)
    if left.keys() != right.keys():
        return {"array:"}
    found = set()
    for path in left:
        value = left[path]
        if not _same_leaf(value, right[path]):
            # one number on its own - a Python number, or an array of no dimension - is a measurement of the run
            scalar = (isinstance(value, (int, float)) and not isinstance(value, bool)) or getattr(value, "ndim", 1) == 0
            found.add(("scalar:" if scalar else "array:") + path)
    return found


def differences(a: Any, b: Any, skip: Iterable[str] = ()) -> Optional[dict]:
    """How far apart two outputs of the same structure are, over every number in them but those at `skip`: the largest
    and the mean absolute difference, and the cosine similarity of the two as vectors; None when their structures
    differ, they disagree on a value that is not a number, or they hold no number."""
    import numpy as np

    left, right = _leaves(a), _leaves(b)
    if left.keys() != right.keys():
        return None
    xs, ys = [], []
    for path in left:
        if path in set(skip):
            continue
        x, y = left[path], right[path]
        if isinstance(x, (bool, str, bytes)) or x is None or isinstance(x, (dict, list, tuple)):
            if x != y:
                return None
            continue
        try:
            xa, ya = np.asarray(x, dtype=np.float64), np.asarray(y, dtype=np.float64)
        except (TypeError, ValueError):
            if not _same_leaf(x, y):
                return None
            continue
        if xa.shape != ya.shape:
            return None
        xs.append(xa.reshape(-1))
        ys.append(ya.reshape(-1))
    if not xs:
        return None
    x, y = np.concatenate(xs), np.concatenate(ys)
    if not x.size:
        return None
    diff = np.abs(x - y)
    xx, yy, xy = float(np.dot(x, x)), float(np.dot(y, y)), float(np.dot(x, y))
    if xx == 0 or yy == 0:
        cosine = 1.0 if xx == yy else 0.0              # two zero vectors are alike; a zero and another are not
    else:
        cosine = max(-1.0, min(1.0, xy / math.sqrt(xx * yy)))   # one square root of the product: x against x is 1
    return {"max_abs": float(np.nanmax(diff)), "mean_abs": float(np.nanmean(diff)), "cosine": cosine}


def _rounded(found: dict) -> dict:
    return {name: float(f"{value:.6g}") for name, value in found.items()}


def _largest(a: Any, b: Any, skip: Iterable[str] = ()) -> str:
    """" (largest difference x)" for two outputs whose numbers compare; "" otherwise."""
    found = differences(a, b, skip)
    return f" (largest difference {found['max_abs']:.3g})" if found else ""
