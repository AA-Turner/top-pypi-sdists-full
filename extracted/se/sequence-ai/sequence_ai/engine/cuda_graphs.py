# SPDX-FileCopyrightText: Copyright (c) 2026 General Sequences Company
# SPDX-License-Identifier: Apache-2.0
"""
A torch module that a model calls many times with the same shapes (a diffusion or flow model's denoiser), replayed
from CUDA graphs captured from its own eager kernels, so the model runs faster and its outputs are exactly the same.

    from sequence_ai.engine import cuda_graphs

    cuda_graphs.install(model, ["action_head.denoiser"])    # model.action_head.denoiser, graphed in place
    model(observation)                                       # a new shape: run in eager mode, captured, checked
    model(observation)                                       # replayed

In one sentence: count, over a few of the model's runs, the calls each of its modules gets (Census) → a module called
more than once per run with the same shapes each time is a candidate, the outermost and slowest first
(Census.candidates) → each has its calls intercepted in place (install) by a Graphed, which runs a shape it has not seen
in eager mode, then captures those kernels into a graph and replays it on the same inputs: the graph is kept only when
its output is the same, byte for byte, never when the capture fails or differs (that shape then runs in eager mode
permanently, reported once) → on replay, a kept graph copies its inputs into its own buffers and its output out.

A whole call can be graphed the same way (install(..., whole=True)): the outermost method of a module that a run calls
(Calls), a model's forward or a method such as `sample_actions`, its denoising loop and the noise it draws included,
replayed as one graph. Its random draws come from the GPU's generator itself, as eager mode's do (Graphed's `bound`),
so it is kept only when, replayed from the random state its eager run began with, it returns the same output and leaves
the generator where eager mode left it.

WHY captured from its own kernels, never compiled: a graph replays the same kernels that eager mode ran, so its outputs
are eager mode's; torch.compile's fusion changes the order of the arithmetic and so the outputs (GR00T N1.7 on an L4:
inductor 1.45x faster, its outputs 0.0051 apart on average), and its own graph mode did not help (1.00x). Measured on
that model and GPU: its DiT captured this way, 224 -> 146 ms an act (2026-11-01), the same outputs on inputs it was
not captured on;
torch.compile(backend="cudagraphs") 225 ms.
WHY every new shape is checked against eager mode where it is captured: a graph is correct for the inputs it was
captured on, and may not be for others; and a shape first seen while serving (a new prompt's length, another batch size)
was never checked before.
WHY the GPU's generator is swapped for a clone of its state while a capture runs, and restored afterwards: a capture
that failed left the generator unusable for the rest of the process (restoring its state's bytes did not help), and a
model draws its noise from it. The clone absorbs whatever the capture does; the generator itself is unchanged, so a
failed shape costs nothing but its graph. (torch 2.9 on an L4: after a failed capture, torch.cuda.set_rng_state and then
torch.randn raised "Offset increment outside graph capture encountered unexpectedly"; with the swap, the draws after a
failed capture were those with no capture.) torch before 2.4 has no way to swap it (graphsafe_set_state), and captures
nothing.
WHY the module stays where it is in the model, the same object of the same class, with only its forward replaced: a
model may check what it holds before it runs, and a module put in its place fails that check
(`assert isinstance(self.dit, ...)`); and a wrapper holding the module would change its state_dict's keys and keep its
hooks out of replayed calls.
WHY a whole call is captured twice, first on a clone of the generator and then on the generator itself: a graph replays
the random draws it captured from the generator's state it was captured on. Captured on a clone, its replays would draw
from that clone, which no later seed reaches, and never answer as eager mode does; captured on the generator itself, a
capture that failed would leave the generator unusable. The first capture finds out whether the call can be captured at
no risk; the second, of a call that just captured, is the one kept. Should it fail all the same, the generator is given
a clone of its state, and every whole graph drawing from the old one is dropped.
WHY a call inside another graph's capture runs in eager mode: a whole call's capture records the kernels of the modules
it calls, and a module graph replayed inside it would be a graph within a graph.

Standard library and torch only; torch is imported where it is used, so importing this costs nothing.
"""
from __future__ import annotations

import copy
import os
import sys
import threading
import time
import weakref
from collections import defaultdict
from collections.abc import Mapping, MutableMapping
from contextlib import contextmanager
from typing import Any, Callable, Iterator, Optional

NOT_A_TENSOR = (bool, int, float, str, type(None))
# Whether wrapped modules replay their graphs: set it False to time the same model in eager mode, True otherwise.
ACTIVE = True
# Why a shape runs in eager mode, by kind: the text of its line (Graphed._eager), with its capture's error filled in.
WHY_EAGER = {"torch": "{}", "failed": "its capture failed ({})",
             "unreturnable": "its output is of a type a graph cannot return",
             "differs": "its graph's output differed from eager mode's",
             "dropped": "a later capture on the generator failed, and the graphs drawing from it went with it"}
# A thread's calls while one Graphed captures: run in eager mode, its own capture recording their kernels.
_LOCAL = threading.local()
# The whole graphs (Graphed's `bound`) whose replays draw from the GPU's generator's state: dropped together should a
# capture on that state fail (_repair).
_BOUND: "weakref.WeakSet" = weakref.WeakSet()


def _capturing() -> bool:
    return getattr(_LOCAL, "depth", 0) > 0



def _signature(value):
    """What a graph is keyed on for one argument: a tensor's shape, strides, dtype and device; a plain value itself; a
    container of them, each - a list, a tuple, a dict, or a mapping of another class that can be copied and written
    (a model's feature dict); None for anything else, which no graph is captured for."""
    import torch

    if isinstance(value, torch.Tensor):
        return ("T", tuple(value.shape), tuple(value.stride()), str(value.dtype), str(value.device))
    if isinstance(value, NOT_A_TENSOR):
        return ("V", type(value).__name__, value)
    if isinstance(value, (tuple, list)):
        inner = [_signature(v) for v in value]
        return None if any(s is None for s in inner) else (type(value).__name__, tuple(inner))
    if isinstance(value, dict) or isinstance(value, MutableMapping):
        inner = [(k, _signature(v)) for k, v in sorted(value.items(), key=lambda kv: str(kv[0]))]
        return None if any(s is None for _, s in inner) else (type(value).__name__, tuple(inner))
    return None


def signature(args: tuple, kwargs: dict) -> Optional[tuple]:
    """A call's key: its arguments' signatures and the modes it runs in (grad, inference, autocast); None when any
    argument is of a type no graph is kept for."""
    import torch

    sig = _signature((tuple(args), dict(kwargs)))
    if sig is None:
        return None
    return sig, torch.is_grad_enabled(), torch.is_inference_mode_enabled(), torch.is_autocast_enabled()


def _mapping(value, items: dict):
    """`items` in a mapping of `value`'s own class: a dict as a dict; another class (a model's feature dict, an output
    with its fields as attributes) as a copy of `value` with each item written into it, so what the model reads of it
    (its class, its attributes) is as it was."""
    if type(value) is dict:
        return items
    out = copy.copy(value)
    for k, v in items.items():
        out[k] = v
    return out


def _static(value):
    """A separate buffer for `value`, with its strides: a graph's inputs, into which each replay's inputs are copied."""
    import torch

    if isinstance(value, torch.Tensor):
        out = torch.empty_strided(value.size(), value.stride(), dtype=value.dtype, device=value.device)
        out.copy_(value)
        return out
    if isinstance(value, (tuple, list)):
        return type(value)(_static(v) for v in value)
    if isinstance(value, Mapping):
        return _mapping(value, {k: _static(v) for k, v in value.items()})
    return value


def _copy_into(static, value) -> None:
    import torch

    if isinstance(static, torch.Tensor):
        static.copy_(value)
    elif isinstance(static, (tuple, list)):
        for s, v in zip(static, value):
            _copy_into(s, v)
    elif isinstance(static, Mapping):
        for k in static:
            _copy_into(static[k], value[k])


def _clone(value):
    """An output copied out of a graph's memory, which its next replay overwrites; None for an output of a type it
    cannot copy."""
    import torch

    if isinstance(value, torch.Tensor):
        return value.clone()
    if isinstance(value, NOT_A_TENSOR):
        return value
    if isinstance(value, (tuple, list)):
        inner = [_clone(v) for v in value]
        missed = any(i is None and v is not None for i, v in zip(inner, value))
        return None if missed else type(value)(inner)
    if isinstance(value, dict) or isinstance(value, MutableMapping):
        inner = {k: _clone(v) for k, v in value.items()}
        if any(inner[k] is None and value[k] is not None for k in value):
            return None
        try:
            return _mapping(value, inner)
        except Exception:  # noqa: BLE001 (a mapping that cannot be copied is an output a graph cannot return)
            return None
    return None


def same(a: Any, b: Any) -> bool:
    """Whether two outputs are equal byte for byte: the same structure, each tensor of the same dtype and shape holding
    the same bytes (a NaN equals the same NaN, where == would report a difference)."""
    import torch

    if isinstance(a, torch.Tensor) or isinstance(b, torch.Tensor):
        if not (isinstance(a, torch.Tensor) and isinstance(b, torch.Tensor)):
            return False
        if a.dtype != b.dtype or a.shape != b.shape:
            return False
        return torch.equal(a.contiguous().view(-1).view(torch.uint8), b.contiguous().view(-1).view(torch.uint8))
    if isinstance(a, (tuple, list)) and isinstance(b, (tuple, list)):
        return len(a) == len(b) and all(same(x, y) for x, y in zip(a, b))
    if isinstance(a, Mapping) and isinstance(b, Mapping):
        return a.keys() == b.keys() and all(same(a[k], b[k]) for k in a)
    return a == b


class NoSwap(RuntimeError):
    """This torch cannot swap the GPU's generator for a capture: no graph is captured with it."""


class _Random:
    """The random state preserved across a capture: torch's CPU generator state, restored afterwards; and the current
    GPU's generator, swapped for a clone of its state while the capture runs and restored afterwards, so the capture,
    failed or not, never touches the generator the model draws from."""

    def __init__(self) -> None:
        import torch

        self.cpu = torch.get_rng_state()
        self.gen = self.state = None
        if torch.cuda.is_available() and torch.cuda.is_initialized():
            gen = torch.cuda.default_generators[torch.cuda.current_device()]
            if not all(hasattr(gen, n) for n in ("clone_state", "graphsafe_get_state", "graphsafe_set_state")):
                raise NoSwap("cuda graphs need torch 2.4 or later")
            self.gen, self.state = gen, gen.graphsafe_get_state()
            gen.graphsafe_set_state(gen.clone_state())

    def put_back(self) -> None:
        import torch

        torch.set_rng_state(self.cpu)
        if self.gen is not None:
            self.gen.graphsafe_set_state(self.state)


def _generator():
    """The current GPU's generator; None where CUDA is not in use."""
    import torch

    if torch.cuda.is_available() and torch.cuda.is_initialized():
        return torch.cuda.default_generators[torch.cuda.current_device()]
    return None


def _rng_state() -> tuple:
    """Every random state a call may draw from: Python's, NumPy's (where NumPy is imported), torch's CPU generator's
    and the current GPU's generator's (where CUDA is in use)."""
    import random

    import torch

    np = sys.modules.get("numpy")
    gpu = torch.cuda.get_rng_state() if _generator() is not None else None
    return random.getstate(), (np.random.get_state() if np is not None else None), torch.get_rng_state(), gpu


def _put_rng(state: tuple) -> None:
    import random

    import torch

    py, np_state, cpu, gpu = state
    random.setstate(py)
    if np_state is not None:
        sys.modules["numpy"].random.set_state(np_state)
    torch.set_rng_state(cpu)
    if gpu is not None:
        torch.cuda.set_rng_state(gpu)


def _same_rng(a: tuple, b: tuple) -> bool:
    """Whether two random states (_rng_state) are the same: whether two calls drew alike."""
    import torch

    if a[0] != b[0] or not torch.equal(a[2], b[2]):
        return False
    if (a[3] is None) != (b[3] is None) or (a[3] is not None and not torch.equal(a[3], b[3])):
        return False
    if (a[1] is None) != (b[1] is None):
        return False
    # NumPy's: (its generator's name, its keys, its position, whether it holds a Gaussian, that Gaussian)
    return a[1] is None or (a[1][0] == b[1][0] and bool((a[1][1] == b[1][1]).all()) and a[1][2:] == b[1][2:])


def _error(exc: BaseException) -> str:
    return f"{type(exc).__name__}: {str(exc)[:120]}"


def _drop_bound(say) -> None:
    """Every whole graph's shapes back to eager mode: their replays draw from a generator state that is no more."""
    dropped = 0
    for graphed in list(_BOUND):
        for key in list(graphed.graphs):
            graphed.graphs.pop(key)
            graphed.eager[key] = ("dropped", "")
            dropped += 1
    if dropped:
        say(f"cuda graphs: {dropped} whole-call shapes run in eager mode: {WHY_EAGER['dropped']}")


class _Graph:
    """One shape's graph of a module: its input buffers, its output, and the graph that replays its kernels."""

    def __init__(self, inner, args: tuple, kwargs: dict, pool) -> None:
        import torch

        self.pool = pool if pool is not None else torch.cuda.graph_pool_handle()   # one per module, for all its shapes
        self.args, self.kwargs = _static(tuple(args)), _static(dict(kwargs))
        side = torch.cuda.Stream()
        side.wait_stream(torch.cuda.current_stream())
        with torch.cuda.stream(side):
            inner(*self.args, **self.kwargs)                  # its first run on these buffers, outside the capture
        torch.cuda.current_stream().wait_stream(side)
        self.graph = torch.cuda.CUDAGraph()
        with torch.cuda.graph(self.graph, pool=self.pool):
            self.out = inner(*self.args, **self.kwargs)

    def replay(self, args: tuple, kwargs: dict):
        _copy_into(self.args, tuple(args))
        _copy_into(self.kwargs, dict(kwargs))
        self.graph.replay()
        return _clone(self.out)


class Graphed:
    """A module's calls served from graphs of its own kernels, one per shape. Each shape's first call runs in eager
    mode, and its graph is kept only when its output for that call is the same, byte for byte. A shape whose capture
    fails or differs runs in eager mode permanently, reported once. `inner` is what it runs in eager mode and captures:
    a module's original forward, or another method of it (install). `bound`: a whole call, whose graphs draw their
    random numbers from the GPU's generator itself (_try_bound). `capture` replaces the graph in tests: (inner, args,
    kwargs, pool) -> an object with replay(args, kwargs)."""

    def __init__(self, inner, path: str, *, say=print, capture=None, bound: bool = False) -> None:
        self.inner, self.path, self.say, self.bound = inner, path, say, bound
        self.on = True                             # False: every call runs in eager mode, as with ACTIVE False
        self.graphs: dict = {}
        self.eager: dict = {}                      # a shape's key -> why it runs in eager mode
        self.captures_s: list[float] = []
        self.unkeyed = 0                           # calls with an argument no graph is keyed on, run in eager mode
        self._capture = capture or _Graph
        self._pool = None
        self._lock = threading.Lock()
        self._running = threading.local()          # .on while this thread runs its inner, eagerly or under capture
        if bound:
            _BOUND.add(self)

    def __call__(self, *args, **kwargs):
        if getattr(self._running, "on", False) or _capturing():
            # its module's forward calling its own forward again (on its submodules, for example), or a call made within
            # another graph's capture: the original forward, within that call's eager run or its capture
            return self.inner(*args, **kwargs)
        if not (ACTIVE and self.on):
            return self.inner(*args, **kwargs)
        key = signature(args, kwargs)
        if key is None:
            self.unkeyed += 1
            return self.inner(*args, **kwargs)
        with self._lock:
            graph = self.graphs.get(key)
            if graph is not None:
                return graph.replay(args, kwargs)
            trying = key not in self.eager
            before = _rng_state() if trying and self.bound else None
            self._running.on = True
            _LOCAL.depth = getattr(_LOCAL, "depth", 0) + trying
            try:
                eager = self.inner(*args, **kwargs)
                if trying:
                    if self.bound:
                        self._try_bound(key, args, kwargs, eager, before)
                    else:
                        self._try(key, args, kwargs, eager)
                return eager
            finally:
                self._running.on = False
                _LOCAL.depth -= trying

    def _try(self, key, args: tuple, kwargs: dict, eager) -> None:
        """Capture a graph of this shape on this call's inputs and replay it on them: kept when its output equals
        eager's."""
        try:
            kept = _Random()
        except NoSwap as exc:
            self._eager(key, "torch", str(exc))
            return
        started = time.perf_counter()
        try:
            graph = self._capture(self.inner, args, kwargs, self._pool)
            self._pool = getattr(graph, "pool", self._pool)
            replayed = graph.replay(args, kwargs)
        except Exception as exc:  # noqa: BLE001 (a failed capture only leaves this shape in eager mode)
            self._eager(key, "failed", _error(exc))
            return
        finally:
            kept.put_back()
        self._judge(key, graph, replayed, eager, started)

    def _try_bound(self, key, args: tuple, kwargs: dict, eager, before: tuple) -> None:
        """A whole call's graph of this shape: captured on a clone of the generator, so that a capture that fails
        changes nothing; then again on the generator itself, so that each replay draws where eager mode would. Kept
        when, replayed from the random state its eager run began with (`before`), its output is eager's and it leaves
        every random state where eager mode left it - never when the call drew what a graph cannot draw again (on the
        CPU, from NumPy, from Python's generator)."""
        after = _rng_state()
        try:
            kept = _Random()
        except NoSwap as exc:
            self._eager(key, "torch", str(exc))
            return
        started = time.perf_counter()
        try:
            trial = self._capture(self.inner, args, kwargs, self._pool)
            self._pool = getattr(trial, "pool", self._pool)
        except Exception as exc:  # noqa: BLE001 (captured on a clone: a failure leaves this shape in eager mode alone)
            self._eager(key, "failed", _error(exc))
            return
        finally:
            kept.put_back()
        del trial
        gen = _generator()
        spare = gen.clone_state() if gen is not None else None
        try:
            graph = self._capture(self.inner, args, kwargs, self._pool)
        except Exception as exc:  # noqa: BLE001 (on the generator itself: it is given a clone of its state)
            if gen is not None:
                gen.graphsafe_set_state(spare)
                _drop_bound(self.say)
            _put_rng(after)
            self._eager(key, "failed", _error(exc))
            return
        try:
            _put_rng(before)
            replayed = graph.replay(args, kwargs)
            drew_alike = _same_rng(_rng_state(), after)
        except Exception as exc:  # noqa: BLE001 (a replay that fails leaves this shape in eager mode)
            self._eager(key, "failed", _error(exc))
            return
        finally:
            _put_rng(after)
        self._judge(key, graph, replayed if drew_alike else _Differs, eager, started)

    def _judge(self, key, graph, replayed, eager, started: float) -> None:
        if replayed is None:
            self._eager(key, "unreturnable")
        elif replayed is _Differs or not same(replayed, eager):
            self._eager(key, "differs")
        else:
            self.graphs[key] = graph
            self.captures_s.append(round(time.perf_counter() - started, 3))
            self.say(f"cuda graphs: captured {self.path} for a new shape in {self.captures_s[-1]:.1f} s")

    def _eager(self, key, kind: str, error: str = "") -> None:
        self.eager[key] = (kind, error)
        why = WHY_EAGER[kind].format(error)
        self.say(f"cuda graphs: {self.path} runs in eager mode for one of its shapes: {why}")

    def report(self) -> dict:
        """What it did: the number of shapes captured; each distinct reason a shape runs in eager mode, as [its kind
        (WHY_EAGER), its capture's error]; each capture's duration in seconds; and how many calls had an argument no
        graph is keyed on."""
        return {"shapes": len(self.graphs), "eager": [list(e) for e in sorted(set(self.eager.values()))],
                "captures_s": self.captures_s, "unkeyed": self.unkeyed}


class _Differs:
    """A replay that left a random state where eager mode did not: judged as an output that differs."""


# ── which modules ───────────────────────────────────────────────────────────────────────────────────────────────────
def modules_of(inst: Any, depth: int = 3) -> dict[str, object]:
    """The torch modules reachable from an object through its attributes (a policy's `self._policy.model`, for example),
    each by its path from the object ("" for an object that is itself a module); an attribute that is not a module is
    searched `depth` levels down. Empty in a process that never imported torch, which is not imported for the search: a
    JAX model's own CUDA libraries are left untouched."""
    if "torch" not in sys.modules:
        return {}
    import torch

    found: dict[str, object] = {}
    seen: set[int] = set()

    def walk(obj, path: str, left: int) -> None:
        if id(obj) in seen:
            return
        seen.add(id(obj))
        if isinstance(obj, torch.nn.Module):
            found[path] = obj
            return
        if left <= 0 or isinstance(obj, (*NOT_A_TENSOR, bytes, type)) or callable(obj) and not hasattr(obj, "__dict__"):
            return
        items = obj.items() if isinstance(obj, dict) else vars(obj).items() if hasattr(obj, "__dict__") else ()
        for name, value in items:
            if isinstance(name, str) and not name.startswith("__"):
                walk(value, f"{path}.{name}" if path else name, left - 1)

    walk(inst, "", depth + 1)
    return found


def resolve(inst: Any, path: str) -> Any:
    """(the object holding the module at `path`, its attribute's name)."""
    *parents, name = path.split(".")
    holder = inst
    for part in parents:
        holder = holder[part] if isinstance(holder, dict) else getattr(holder, part)
    return holder, name


def _target(inst: Any, path: str):
    """What `path` names, as (the module, the name of its method that is graphed): a module's "forward", or a method of
    a module (`model.sample_actions`); "" names `inst` itself. LookupError when it names nothing in the model, TypeError
    when it names something that is neither."""
    import torch

    if path == "":
        holder, name, found = None, "", inst
    else:
        try:
            holder, name = resolve(inst, path)
            found = holder[name] if isinstance(holder, dict) else getattr(holder, name)
        except (AttributeError, KeyError, TypeError, IndexError):
            raise LookupError(path) from None
    if isinstance(found, torch.nn.Module):
        return found, "forward"
    if isinstance(holder, torch.nn.Module) and (isinstance(vars(holder).get(name), Graphed)
                                                or callable(found) and getattr(found, "__self__", None) is holder):
        return holder, name
    raise TypeError(path)


def install(inst: Any, paths: list[str], *, say: Callable[[str], Any] = print,
            capture: Optional[Callable[..., Any]] = None, whole: bool = False) -> dict[str, Graphed]:
    """Graph each module at `paths` in place: the module stays, the same object of the same class, and only its calls
    are intercepted. Its `forward`, an instance attribute from now on, is a Graphed of its original forward. Returns
    {path: its Graphed}. So what the model checks about it (isinstance, its type) still holds, the methods the model
    calls on it directly are its own, its state_dict and parameters are unchanged, and its hooks fire around each call,
    including a replayed one, outside any graph. A path may also name a method of a module (`model.sample_actions`),
    graphed the same way: an instance attribute in front of its class's. A path that names neither is reported and
    skipped; a module named twice is graphed once. `whole`: each is a whole call, whose graphs draw from the GPU's
    generator itself (Graphed's `bound`). On a machine with no CUDA GPU nothing is graphed, which is reported once, and
    {} is returned; each path is still looked up, so a mistyped path is reported on a laptop and not first on the
    GPU."""
    import torch

    has_gpu = capture is not None or torch.cuda.is_available()
    out: dict[str, Graphed] = {}
    for path in paths:
        try:
            module, method = _target(inst, path)
        except LookupError:
            say(f"cuda graphs: {path} is not in this model: not captured")
            continue
        except TypeError:
            say(f"cuda graphs: {path} is not a torch module or a method of one: not captured")
            continue
        if not has_gpu:
            continue
        graphed = vars(module).get(method)
        if not isinstance(graphed, Graphed):
            before = vars(module).get(method, _NONE)          # another forward put there before: uninstall's again
            graphed = Graphed(getattr(module, method), path, say=say, capture=capture, bound=whole)
            graphed.before = before
            setattr(module, method, graphed)   # torch runs the hooks, then this instance attribute, not the class's
        out[path] = graphed
    if not has_gpu:
        say("cuda graphs: no CUDA GPU available: nothing captured")          # the model is unchanged, at no cost
    return out


def uninstall(inst: Any, paths: list[str]) -> list[str]:
    """Each path's graphs taken out: its module's forward, or its method, what it was before (its class's, or the
    forward another switch put there), and its graphs dropped. Returns the paths that were graphed."""
    out = []
    for path in paths:
        try:
            module, method = _target(inst, path)
        except (LookupError, TypeError):
            continue
        graphed = vars(module).get(method)
        if isinstance(graphed, Graphed):
            before = getattr(graphed, "before", _NONE)
            if before is _NONE:
                delattr(module, method)
            else:
                setattr(module, method, before)
            _BOUND.discard(graphed)
            graphed.graphs.clear()
            out.append(path)
    return out


class _None:
    """No instance attribute was there: the class's own applies."""


_NONE = _None()


class Census:
    """Each module's calls per run of the model (an "act"), counted while the model runs a few times: how many, whether
    their shapes stay the same, and the GPU time they take (CUDA events; the wall clock on a machine with no GPU). Hooks
    on every module under `roots` ({its path: a module}, as modules_of returns them), removed by close(); end_act() ends
    each run."""

    def __init__(self, roots: dict[str, object]) -> None:
        import torch

        self._cuda = torch.cuda.is_available()
        self.acts: list[dict] = []
        self._act: dict = defaultdict(lambda: {"calls": 0, "keys": set(), "spans": []})
        self._open: dict[int, list] = defaultdict(list)
        self._hooks = []
        for root, module in roots.items():
            for name, sub in module.named_modules():
                path = f"{root}.{name}" if root and name else name or root
                self._hooks.append(sub.register_forward_pre_hook(self._pre(path), with_kwargs=True))
                self._hooks.append(sub.register_forward_hook(self._post(path), with_kwargs=True))

    def _mark(self):
        import torch

        if self._cuda:
            e = torch.cuda.Event(enable_timing=True)
            e.record()
            return e
        return time.perf_counter()

    def _pre(self, path: str):
        def hook(module, args, kwargs):
            row = self._act[path]
            row["calls"] += 1
            row["keys"].add(signature(args, kwargs))
            self._open[id(module)].append(self._mark())
        return hook

    def _post(self, path: str):
        def hook(module, args, kwargs, output):
            opened = self._open[id(module)]
            if opened:
                self._act[path]["spans"].append((opened.pop(), self._mark()))
        return hook

    def end_act(self) -> None:
        """End one run: record each module's calls, shapes and time in it."""
        import torch

        if self._cuda:
            torch.cuda.synchronize()
        done = {}
        for path, row in self._act.items():
            ms = sum(a.elapsed_time(b) if self._cuda else (b - a) * 1e3 for a, b in row["spans"])
            done[path] = {"calls": row["calls"], "one_shape": len(row["keys"]) == 1 and None not in row["keys"],
                          "ms": ms}
        self.acts.append(done)
        self._act.clear()

    def close(self) -> None:
        """Remove the counting hooks from the modules: the census is over."""
        for h in self._hooks:
            h.remove()
        self._hooks = []

    def candidates(self, *, min_ms: float = 1.0, most: Optional[int] = 4) -> list[dict]:
        """The modules worth graphing: called more than once in every run counted, with one shape throughout each run,
        and at least `min_ms` of GPU time per run. The outermost of nested ones, the slowest first, at most `most`
        (None: all of them)."""
        return self._rows(2, min_ms, most)

    def called(self, *, min_ms: float = 1.0, most: Optional[int] = None) -> list[dict]:
        """The outermost modules every run counted calls at least once, with one shape throughout each run, and at
        least `min_ms` of time per run: where a model spends its time when no module of it is called again. The
        slowest first, at most `most` (None: all of them)."""
        return self._rows(1, min_ms, most)

    def _rows(self, calls: int, min_ms: float, most: Optional[int]) -> list[dict]:
        if not self.acts:
            return []
        paths = set.intersection(*(set(a) for a in self.acts))
        ok = {p for p in paths if all(a[p]["calls"] >= calls and a[p]["one_shape"] for a in self.acts)}
        outer = {p for p in ok if not any(_within(p, q) for q in ok)}
        rows = [{"path": p, "calls": min(a[p]["calls"] for a in self.acts),
                 "ms": round(sorted(a[p]["ms"] for a in self.acts)[len(self.acts) // 2], 2)} for p in outer]
        rows = [r for r in rows if r["ms"] >= min_ms]
        return sorted(rows, key=lambda r: -r["ms"])[:most]


def _within(path: str, other: str) -> bool:
    """Whether the module at `path` is inside the one at `other` ("" is the model itself, which holds every other)."""
    return path != other and (other == "" or path.startswith(other + "."))


class Calls:
    """The calls a run makes to its torch modules' methods - a module's forward, or a method of it the code calls
    directly (`sample_actions`, `get_action`) - each with where it was called from, found by Python's profiler while the
    model runs (`with calls.run(): model(...)`). The modules are those under `roots`, as Census takes them; a method of
    torch itself (a module's __call__, its hooks) is not counted.

    WHY the profiler and not forward hooks: a policy's whole run is often a method that is not a forward (a flow model's
    sampling loop, its noise drawn in it), which no hook sees; the profiler sees every Python call, and only the calls
    whose `self` is one of the model's modules are kept."""

    def __init__(self, roots: dict[str, object]) -> None:
        import torch

        self._paths: dict[int, str] = {}
        for root, module in roots.items():
            for name, sub in module.named_modules():
                self._paths.setdefault(id(sub), f"{root}.{name}" if root and name else name or root)
        self._torch = os.path.dirname(torch.__file__) + os.sep
        self.acts: list[list[dict]] = []
        self._stack: list = []
        self._act: list[dict] = []

    @contextmanager
    def run(self) -> Iterator[None]:
        """A context in which the calls are counted, as one run: `with calls.run(): model(...)`."""
        self._stack, self._act = [], []
        previous = sys.getprofile()
        sys.setprofile(self._hook)
        try:
            yield
        finally:
            sys.setprofile(previous)
            self.acts.append(self._act)

    def _hook(self, frame, event, arg) -> None:
        if event == "call":
            code = frame.f_code
            if not code.co_argcount or code.co_varnames[0] != "self" or code.co_filename.startswith(self._torch):
                return
            path = self._paths.get(id(frame.f_locals.get("self")))
            if path is not None:
                parent = self._stack[-1][3] if self._stack else None
                self._stack.append((frame, path, code.co_name, len(self._act), time.perf_counter()))
                self._act.append({"path": path, "method": code.co_name, "parent": parent, "ms": 0.0})
        elif event == "return" and self._stack and self._stack[-1][0] is frame:
            _, _, _, index, started = self._stack.pop()
            self._act[index]["ms"] = (time.perf_counter() - started) * 1e3

    def outermost(self, *, most: int = 4) -> list[dict]:
        """The calls worth a whole graph, in the order to try them: each made the same number of times in every run
        counted, the outermost first (those no other counted call made), then the calls they made, the slowest first
        within each; at most `most`. Each as {"path": the module's path, or its method's (`model.sample_actions`),
        "calls": per run, "ms": its time in the first run}."""
        if not self.acts:
            return []
        counts = [defaultdict(int) for _ in self.acts]
        for counted, act in zip(counts, self.acts):
            for call in act:
                counted[(call["path"], call["method"])] += 1
        steady = {k for k in counts[0] if all(c.get(k) == counts[0][k] for c in counts)}
        first, rows, seen = self.acts[0], [], set()
        for depth_of in _depths(first):
            level = sorted(((i, c) for i, c in enumerate(first) if depth_of(i)), key=lambda ic: -ic[1]["ms"])
            for _, call in level:
                key = (call["path"], call["method"])
                if key in steady and key not in seen:
                    seen.add(key)
                    path = call["path"] if call["method"] == "forward" else \
                        (f"{call['path']}.{call['method']}" if call["path"] else call["method"])
                    rows.append({"path": path, "calls": counts[0][key], "ms": round(call["ms"], 2)})
        return rows[:most]


def _depths(act: list[dict]):
    """For the calls of one run, a test per depth - the outermost calls first, then the calls they made, and so on."""
    depth: list[int] = []
    for call in act:
        depth.append(0 if call["parent"] is None else depth[call["parent"]] + 1)
    for d in range(max(depth, default=-1) + 1):
        yield lambda i, d=d: depth[i] == d
