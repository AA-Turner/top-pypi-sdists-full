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

WHY captured from its own kernels, never compiled: a graph replays the same kernels that eager mode ran, so its outputs
are eager mode's; torch.compile's fusion changes the order of the arithmetic and so the outputs (GR00T N1.7 on an L4:
inductor 1.45x faster, its outputs 0.0051 apart on average), and its own graph mode did not help (1.00x). Measured on
that model and GPU: its DiT captured this way, 224 -> 146 ms per run, the same outputs on inputs it was not captured on;
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

Standard library and torch only; torch is imported where it is used, so importing this costs nothing.
"""
from __future__ import annotations

import sys
import threading
import time
from collections import defaultdict, deque
from typing import Any, Callable, Optional

NOT_A_TENSOR = (bool, int, float, str, type(None))
# Whether wrapped modules replay their graphs: set it False to time the same model in eager mode, True otherwise.
ACTIVE = True
# What the graphs did since the events were last drained (drain_events): a shape captured, a shape left in eager
# mode. A server can write them as its own log lines.
EVENTS: deque = deque(maxlen=200)
# Why a shape runs in eager mode, by kind: the text of its line (Graphed._eager), with its capture's error filled in.
WHY_EAGER = {"torch": "{}", "failed": "its capture failed ({})",
             "unreturnable": "its output is of a type a graph cannot return",
             "differs": "its graph's output differed from eager mode's"}


def drain_events() -> list[dict]:
    """Every event noted since the last drain, oldest first."""
    out = []
    while EVENTS:
        try:
            out.append(EVENTS.popleft())
        except IndexError:
            break
    return out


def _signature(value):
    """What a graph is keyed on for one argument: a tensor's shape, strides, dtype and device; a plain value itself; a
    container of them, each; None for anything else, which no graph is captured for."""
    import torch

    if isinstance(value, torch.Tensor):
        return ("T", tuple(value.shape), tuple(value.stride()), str(value.dtype), str(value.device))
    if isinstance(value, NOT_A_TENSOR):
        return ("V", type(value).__name__, value)
    if isinstance(value, (tuple, list)):
        inner = [_signature(v) for v in value]
        return None if any(s is None for s in inner) else (type(value).__name__, tuple(inner))
    if isinstance(value, dict):
        inner = [(k, _signature(v)) for k, v in sorted(value.items(), key=lambda kv: str(kv[0]))]
        return None if any(s is None for _, s in inner) else ("dict", tuple(inner))
    return None


def signature(args: tuple, kwargs: dict) -> Optional[tuple]:
    """A call's key: its arguments' signatures and the modes it runs in (grad, inference, autocast); None when any
    argument is of a type no graph is kept for."""
    import torch

    sig = _signature((tuple(args), dict(kwargs)))
    if sig is None:
        return None
    return sig, torch.is_grad_enabled(), torch.is_inference_mode_enabled(), torch.is_autocast_enabled()


def _static(value):
    """A separate buffer for `value`, with its strides: a graph's inputs, into which each replay's inputs are copied."""
    import torch

    if isinstance(value, torch.Tensor):
        out = torch.empty_strided(value.size(), value.stride(), dtype=value.dtype, device=value.device)
        out.copy_(value)
        return out
    if isinstance(value, (tuple, list)):
        return type(value)(_static(v) for v in value)
    if isinstance(value, dict):
        return {k: _static(v) for k, v in value.items()}
    return value


def _copy_into(static, value) -> None:
    import torch

    if isinstance(static, torch.Tensor):
        static.copy_(value)
    elif isinstance(static, (tuple, list)):
        for s, v in zip(static, value):
            _copy_into(s, v)
    elif isinstance(static, dict):
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
    if isinstance(value, dict):
        inner = {k: _clone(v) for k, v in value.items()}
        return None if any(inner[k] is None and value[k] is not None for k in value) else inner
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
    if isinstance(a, dict) and isinstance(b, dict):
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
    a module's original forward (install). `capture` replaces the graph in tests: (inner, args, kwargs, pool) -> an
    object with replay(args, kwargs)."""

    def __init__(self, inner, path: str, *, say=print, capture=None) -> None:
        self.inner, self.path, self.say = inner, path, say
        self.graphs: dict = {}
        self.eager: dict = {}                      # a shape's key -> why it runs in eager mode
        self.captures_s: list[float] = []
        self._capture = capture or _Graph
        self._pool = None
        self._lock = threading.Lock()
        self._running = threading.local()          # .on while this thread runs its inner, eagerly or under capture

    def __call__(self, *args, **kwargs):
        if getattr(self._running, "on", False):
            # its module's forward calling its own forward again (on its submodules, for example): the original forward,
            # within this call's eager run or its capture
            return self.inner(*args, **kwargs)
        key = signature(args, kwargs) if ACTIVE else None
        if key is None:
            return self.inner(*args, **kwargs)
        with self._lock:
            graph = self.graphs.get(key)
            if graph is not None:
                return graph.replay(args, kwargs)
            self._running.on = True
            try:
                eager = self.inner(*args, **kwargs)
                if key not in self.eager:
                    self._try(key, args, kwargs, eager)
                return eager
            finally:
                self._running.on = False

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
            self._eager(key, "failed", f"{type(exc).__name__}: {str(exc)[:120]}")
            return
        finally:
            kept.put_back()
        if replayed is None:
            self._eager(key, "unreturnable")
        elif not same(replayed, eager):
            self._eager(key, "differs")
        else:
            self.graphs[key] = graph
            self.captures_s.append(round(time.perf_counter() - started, 3))
            EVENTS.append({"ev": "cuda_graphs.captured", "path": self.path, "s": self.captures_s[-1]})
            self.say(f"cuda graphs: captured {self.path} for a new shape in {self.captures_s[-1]:.1f} s")

    def _eager(self, key, kind: str, error: str = "") -> None:
        self.eager[key] = (kind, error)
        why = WHY_EAGER[kind].format(error)
        EVENTS.append({"ev": "cuda_graphs.eager", "path": self.path, "why": why})
        self.say(f"cuda graphs: {self.path} runs in eager mode for one of its shapes: {why}")

    def report(self) -> dict:
        """What it did: the number of shapes captured; each distinct reason a shape runs in eager mode, as [its kind
        (WHY_EAGER), its capture's error]; each capture's duration in seconds."""
        return {"shapes": len(self.graphs), "eager": [list(e) for e in sorted(set(self.eager.values()))],
                "captures_s": self.captures_s}


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


def install(inst: Any, paths: list[str], *, say: Callable[[str], Any] = print,
            capture: Optional[Callable[..., Any]] = None) -> dict[str, Graphed]:
    """Graph each module at `paths` in place: the module stays, the same object of the same class, and only its calls
    are intercepted. Its `forward`, an instance attribute from now on, is a Graphed of its original forward. Returns
    {path: its Graphed}. So what the model checks about it (isinstance, its type) still holds, the methods the model
    calls on it directly are its own, its state_dict and parameters are unchanged, and its hooks fire around each call,
    including a replayed one, outside any graph. A path that does not name a module is reported and skipped; a module
    named twice is graphed once. On a machine with no CUDA GPU nothing is graphed, which is reported once, and {} is
    returned; each path is still looked up, so a mistyped path is reported on a laptop and not first on the GPU."""
    import torch

    has_gpu = capture is not None or torch.cuda.is_available()
    out: dict[str, Graphed] = {}
    for path in paths:
        try:
            holder, name = resolve(inst, path)
            module = holder[name] if isinstance(holder, dict) else getattr(holder, name)
        except (AttributeError, KeyError, TypeError):
            say(f"cuda graphs: {path} is not in this model: not captured")
            continue
        if not isinstance(module, torch.nn.Module):
            say(f"cuda graphs: {path} is not a torch module: not captured")
            continue
        if not has_gpu:
            continue
        graphed = vars(module).get("forward")
        if not isinstance(graphed, Graphed):
            graphed = Graphed(module.forward, path, say=say, capture=capture)
            module.forward = graphed       # torch runs the hooks, then this instance attribute, not the class's
        out[path] = graphed
    if not has_gpu:
        say("cuda graphs: no CUDA GPU available: nothing captured")          # the model is unchanged, at no cost
    return out






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

    def candidates(self, *, min_ms: float = 1.0, most: int = 4) -> list[dict]:
        """The modules worth graphing: called more than once in every run counted, with one shape throughout each run,
        and at least `min_ms` of GPU time per run. The outermost of nested ones, the slowest first, at most `most`."""
        if not self.acts:
            return []
        paths = set.intersection(*(set(a) for a in self.acts))
        ok = {p for p in paths if all(a[p]["calls"] >= 2 and a[p]["one_shape"] for a in self.acts)}
        outer = {p for p in ok if not any(p.startswith(q + ".") for q in ok)}
        rows = [{"path": p, "calls": min(a[p]["calls"] for a in self.acts),
                 "ms": round(sorted(a[p]["ms"] for a in self.acts)[len(self.acts) // 2], 2)} for p in outer]
        rows = [r for r in rows if r["ms"] >= min_ms]
        return sorted(rows, key=lambda r: -r["ms"])[:most]
