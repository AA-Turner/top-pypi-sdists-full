# SPDX-FileCopyrightText: Copyright (c) 2026 General Sequences Company
# SPDX-License-Identifier: Apache-2.0
"""
A JAX policy's counterparts of optimize()'s switches, for a policy whose model jax.jit compiles:

    cuda_graphs      XLA's command buffers - its CUDA graphs - for the straight-line work of each jitted function,
                     down to the smallest stretch of it: XLA's own defaults already put its fusions, cuBLAS and cuDNN
                     calls and custom calls in them, from a few operations up
    whole_graph      its loops in command buffers too (a denoising loop), so a run is about one graph
                     (both tried on a JAX policy only when asked: optimize.JAX_GRAPHS)
    precision        the floating-point parameters its jitted functions are given, in that dtype ("fp16", "fp32")
    torch_compile, fused_kernels    XLA compiles each jitted function whole and fuses its kernels already
    tensorrt         none: TensorRT builds torch modules

In one sentence: walk what the policy reaches (find) → the functions jax.jit made, in an attribute or a closure; the
typed random keys it holds in attributes, which optimize() sets from each run's seed so that two runs draw alike; the
parameter trees its jitted functions close over → a command-buffer switch puts in each jitted function's place one that
compiles it, for each new input signature, with XLA's command-buffer options added to its defaults (Buffered) →
precision puts in each
parameter tree's place its floating-point arrays cast → optimize() judges each as it judges a torch switch.

WHY each jitted function recompiled with options of its own, never a flag set for the process: XLA reads its flags once,
when its backend starts, which is before any policy is loaded; options given to one compilation take effect there
alone, can be tried, and taken back.
WHY a key set from each run's seed: a JAX policy draws its noise from a key it holds and splits on every call, so its
second run of an observation draws other noise than its first; set from the run's seed before each call, eager mode and
each switch begin from the same key.
WHY options added to XLA's defaults, one kind at a time: a compilation's options set XLA's list of kinds of work it puts
in command buffers by adding one kind to its defaults, never by replacing the list; so cuda_graphs keeps the defaults
and lowers the smallest graph to one operation, and whole_graph adds loops.
WHY whole() compiles a small loop with each way of naming loops' kind, and looks for the loop inside a command buffer:
an XLA that reads the kinds' names takes WHILE; an earlier one reads only their numbers and refuses every name (jax
0.5.3's, where loops are 6); and one kind's number is another's in another version. What was compiled says which
works here.

jax is imported where it is used: importing this costs nothing.
"""
from __future__ import annotations

from typing import Any, Callable, NamedTuple

__all__ = ["find", "Found", "Place", "Buffered", "GRAPHS", "whole", "gpu", "cast"]

# cuda_graphs' options, added to XLA's defaults: straight-line work in command buffers down to one operation
GRAPHS = {"xla_gpu_graph_min_graph_size": 1}
LOOPS = ("WHILE", "6")   # loops' kind of command-buffer work: by name, and by number for an XLA that reads only numbers
MIN_TREE = 1024          # a parameter tree holds at least this many floating-point numbers
_WHOLE: list = []        # whole()'s answer, once asked


def whole() -> dict | None:
    """whole_graph's options for this XLA: GRAPHS, and loops in command buffers too, by the first way of naming their
    kind that puts a small loop in a command buffer here; None where none does (no GPU, or an XLA that cannot)."""
    if not _WHOLE:
        _WHOLE.append(next((options for options in ({"xla_gpu_enable_command_buffer": kind, **GRAPHS} for kind in LOOPS)
                            if _buffers_loops(options)), None))
    return _WHOLE[0]


def _buffers_loops(options: dict) -> bool:
    """Whether a loop of ten steps, compiled with `options`, runs inside a command buffer: a while among the operations
    of one in the compiled program; False where XLA refuses the options."""
    import re

    import jax
    import jax.numpy as jnp

    def loop(w, x):
        return jax.lax.fori_loop(0, 10, lambda i, h: jnp.tanh(h @ w + 0.01 * i), x)

    try:
        text = jax.jit(loop, compiler_options=options).lower(jnp.ones((256, 256)), jnp.ones((1, 256))).compile().as_text()
    except Exception as exc:  # noqa: BLE001 (XLA says which option it refuses in its message alone)
        if "is not a valid enum value" in str(exc):
            return False
        raise
    return any(" while(" in part for part in re.split(r"\n(?=\S)", text) if "command_buffer" in part.split("\n", 1)[0])


class Place(NamedTuple):
    """Where a value is held, so it can be put back: an object's attribute ("attr"), a closure's cell ("cell") or a
    dict's item ("item"); `value` what was there."""
    holder: Any
    kind: str
    key: Any
    value: Any

    def get(self) -> Any:
        """What is there now."""
        if self.kind == "attr":
            return getattr(self.holder, self.key)
        if self.kind == "cell":
            return self.holder.cell_contents
        return self.holder[self.key]

    def set(self, value: Any) -> None:
        """Put `value` there."""
        if self.kind == "attr":
            setattr(self.holder, self.key, value)
        elif self.kind == "cell":
            self.holder.cell_contents = value
        else:
            self.holder[self.key] = value

    def put_back(self) -> None:
        """Put back what was there."""
        self.set(self.value)


class Found(NamedTuple):
    """What a JAX policy holds: its jitted functions, its typed random keys, and the parameter trees its jitted
    functions close over, each where it is held."""
    jitted: list
    keys: list
    trees: list

    def seed(self, seed: int) -> None:
        """Each random key the policy holds, from its first value and `seed`: two runs with one seed draw alike."""
        import jax

        for place in self.keys:
            place.set(jax.random.fold_in(place.value, seed))

    def put_back_keys(self) -> None:
        """Each random key as it was found."""
        for place in self.keys:
            place.put_back()


def gpu() -> bool:
    """Whether JAX runs on a GPU here."""
    try:
        import jax

        return any(device.platform == "gpu" for device in jax.devices())
    except Exception:  # noqa: BLE001 (a JAX that cannot start its backend runs nothing)
        return False


def _jitted(value: Any) -> bool:
    return callable(value) and hasattr(value, "lower") and hasattr(value, "eval_shape")


def _key(value: Any) -> bool:
    try:
        import jax

        return isinstance(value, jax.Array) and jax.dtypes.issubdtype(value.dtype, jax.dtypes.prng_key)
    except Exception:  # noqa: BLE001 (an array that cannot say its dtype is no key)
        return False


def _floats(value: Any) -> int:
    """How many floating-point numbers the jax arrays of a tree hold (0 for anything else)."""
    import jax
    import jax.numpy as jnp

    try:
        leaves = jax.tree_util.tree_leaves(value)
    except Exception:  # noqa: BLE001 (not a tree)
        return 0
    return sum(int(leaf.size) for leaf in leaves
               if isinstance(leaf, jax.Array) and not _key(leaf) and jnp.issubdtype(leaf.dtype, jnp.floating))


def find(names: dict, *, depth: int = 3) -> Found:
    """The jitted functions, typed random keys and parameter trees reachable from `names` (what the policy reaches, by
    name): through objects' attributes, dicts' items and functions' closures, `depth` levels down. A parameter tree is
    a closure's value beside a jitted function in that closure - jax.jit's function of a model's state - holding at
    least MIN_TREE floating-point numbers."""
    import types

    jitted, keys, trees = [], [], []
    seen: set = set()

    def walk(value: Any, left: int) -> None:
        if id(value) in seen or left < 0 or value is None or isinstance(value, (str, bytes, int, float, bool, type,
                                                                                 types.ModuleType)):
            return
        seen.add(id(value))
        if isinstance(value, types.FunctionType):
            cells = list(zip(value.__code__.co_freevars, value.__closure__ or ()))
            held = []
            for _, cell in cells:
                try:
                    held.append((cell, cell.cell_contents))
                except ValueError:
                    continue
            has_jitted = any(_jitted(contents) for _, contents in held)
            for cell, contents in held:
                if _jitted(contents):
                    jitted.append(Place(cell, "cell", None, contents))
                elif has_jitted and _floats(contents) >= MIN_TREE:
                    trees.append(Place(cell, "cell", None, contents))
                else:
                    walk(contents, left - 1)
            wrapped = getattr(value, "__wrapped__", None)
            if wrapped is not None:
                walk(wrapped, left - 1)
            return
        if isinstance(value, types.MethodType):
            walk(value.__func__, left)
            walk(value.__self__, left - 1)
            return
        if isinstance(value, dict):
            for key, item in list(value.items()):
                if _jitted(item):
                    jitted.append(Place(value, "item", key, item))
                elif _key(item):
                    keys.append(Place(value, "item", key, item))
                else:
                    walk(item, left - 1)
            return
        attrs = getattr(value, "__dict__", None)
        if not isinstance(attrs, dict):
            return
        for name, item in list(attrs.items()):
            if name.startswith("__"):
                continue
            if _jitted(item):
                jitted.append(Place(value, "attr", name, item))
            elif _key(item):
                keys.append(Place(value, "attr", name, item))
            else:
                walk(item, left - 1)

    for name, value in names.items():
        if _jitted(value) or _key(value):
            continue                                   # held by the policy's code module: not its to replace here
        walk(value, depth)
    return Found(jitted, keys, trees)


class Buffered:
    """A jitted function compiled with XLA `options` added to its defaults (GRAPHS, whole()), called in its place: the
    function jax.jit was given, jitted again with those compiler options, so each new input signature is traced and
    compiled the way the original's is.

    WHY jitted again, not lowered and compiled by hand: a lowering unflattens the arguments' tree outside jax's own
    tree functions, where a model's typed dataclass checks what it is given and refuses the placeholders it gets;
    jitted again, the calls take jax's own path. A function whose original is not to be had (no __wrapped__) is
    lowered and compiled for each signature, with jaxtyping's checks off while it is."""

    def __init__(self, fn: Callable, options: dict) -> None:
        self.fn, self.options = fn, dict(options)
        self.compiled: dict = {}
        original = getattr(fn, "__wrapped__", None)
        self.jitted = None
        if callable(original):
            import jax

            self.jitted = jax.jit(original, compiler_options=self.options)

    def __call__(self, *args, **kwargs):
        if self.jitted is not None:
            return self.jitted(*args, **kwargs)
        import jax

        leaves, tree = jax.tree_util.tree_flatten((args, kwargs))
        signature = (tree, tuple((tuple(getattr(x, "shape", ())), str(getattr(x, "dtype", type(x).__name__)))
                                 for x in leaves))
        executable = self.compiled.get(signature)
        if executable is None:
            with _unchecked():
                executable = self.fn.lower(*args, **kwargs).compile(compiler_options=self.options)
            self.compiled[signature] = executable
        return executable(*args, **kwargs)

    def lower(self, *args, **kwargs) -> Any:
        """The function's own lowering, so a Buffered is found as a jitted function too."""
        return self.fn.lower(*args, **kwargs)

    def eval_shape(self, *args, **kwargs) -> Any:
        """The function's own output shapes."""
        return self.fn.eval_shape(*args, **kwargs)


class _unchecked:
    """jaxtyping's runtime checks off while a lowering runs, where they would check placeholders, not arrays."""

    def __enter__(self):
        import sys

        self.config = getattr(sys.modules.get("jaxtyping"), "config", None)
        if self.config is not None:
            self.before = self.config.jaxtyping_disable
            self.config.update("jaxtyping_disable", True)
        return self

    def __exit__(self, *exc):
        if self.config is not None:
            self.config.update("jaxtyping_disable", self.before)
        return False


def cast(tree: Any, dtype: Any) -> Any:
    """`tree` with each floating-point jax array in it as `dtype`; everything else as it is."""
    import jax
    import jax.numpy as jnp

    def one(leaf):
        if isinstance(leaf, jax.Array) and not _key(leaf) and jnp.issubdtype(leaf.dtype, jnp.floating):
            return leaf.astype(dtype)
        return leaf

    return jax.tree_util.tree_map(one, tree)
