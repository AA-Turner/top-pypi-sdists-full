# SPDX-FileCopyrightText: Copyright (c) 2026 General Sequences Company
# SPDX-License-Identifier: Apache-2.0
"""
A module's forward compiled, or run in another dtype, for optimize()'s torch_compile, tensorrt and precision.

    from sequence_ai.engine import compiled

    forward = compiled.torch_compile(module)                     # its forward compiled by torch.compile
    forward = compiled.tensorrt(module, args, kwargs)            # built by TensorRT for these inputs, TF32 off
    copy = compiled.dtype_copy(module, torch.float16)            # a float16 copy of it
    forward = compiled.cast_around(copy, module_dtype)           # inputs cast to float16, outputs back

Each returns the function optimize() puts in front of the module's own forward; the module itself is not changed.

    torch_compile   torch.compile on the module's forward: its kernels fused by the compiler, one compilation per
                    input shape, kept in ~/.cache/sequence-ai/compile so a later start reads them
    tensorrt        the module built into a TensorRT engine for the inputs it was called with, float32 with TF32
                    off unless the module given is a float16 copy; the engine kept in ~/.cache/sequence-ai/tensorrt
                    by GPU model, input shapes, versions and weights, so a later start loads it (the
                    torch-tensorrt made for your torch: tensorrt_install())
    dtype_copy      a copy of the module in float16 (or float32), run by cast_around: its floating-point inputs
                    cast to the copy's dtype, its outputs back to the module's own; the module keeps its weights

WHY per module, never the whole policy: a policy's own code - turning an observation into tensors, reading the actions
back - is not a graph a compiler can take, and the module a model spends its time in is.
WHY TF32 off for TensorRT: TF32 multiplies float32 inputs rounded to 10 bits of mantissa; a model built in float32
computes in float32 unless half precision is asked for.
WHY an engine is kept on disk: building one takes minutes; the next start with the same GPU, shapes, versions and
weights loads it instead.

The outputs change - a compiler orders the arithmetic its own way - which is why optimize() turns these on only with
the `tolerance` you give it. torch is imported where it is used; TensorRT (torch_tensorrt) only by tensorrt().
"""
from __future__ import annotations

import copy as _copy
import hashlib
import importlib.metadata
import os
import re
from collections.abc import MutableMapping
from pathlib import Path
from typing import Any, Callable

__all__ = ["torch_compile", "tensorrt", "dtype_copy", "cast_around", "own_forward", "CACHE"]

CACHE = Path.home() / ".cache" / "sequence-ai"


def own_forward(module: Any) -> Callable:
    """The module's forward as its class defines it, bound to it - not an instance attribute put in front of it."""
    return type(module).forward.__get__(module, type(module))


def torch_compile(module: Any, *, cache: Path = CACHE / "compile") -> Callable:
    """The module's own forward compiled by torch.compile, recompiled for each new input shape; the compiler's cache
    in `cache` (where $TORCHINDUCTOR_CACHE_DIR names none)."""
    import torch

    os.environ.setdefault("TORCHINDUCTOR_CACHE_DIR", str(cache))
    return torch.compile(own_forward(module), dynamic=False)


def tensorrt_install() -> str:
    """The pip line that installs TensorRT for the torch installed here: torch-tensorrt makes each release for one torch
    minor version (torch-tensorrt 2.9 for torch 2.9) and brings the TensorRT it needs, so no version suits every torch.
    The torch version is read from its installed package's metadata: torch is not imported."""
    try:
        made = re.match(r"(\d+)\.(\d+)", importlib.metadata.version("torch"))
    except importlib.metadata.PackageNotFoundError:
        made = None
    if made is None:
        return 'pip install torch first, then the torch-tensorrt made for it ("torch-tensorrt==X.Y.*" for torch X.Y)'
    minor = f"{made.group(1)}.{made.group(2)}"
    return f'pip install "torch-tensorrt=={minor}.*" (the one for your torch {minor})'


def tensorrt(module: Any, args: tuple, kwargs: dict, *, cache: Path = CACHE / "tensorrt",
             say: Callable[[str], Any] = print) -> Callable:
    """The module built by TensorRT for inputs like `args` and `kwargs` (one call's, as the module got them), as a
    function called as the module is: loaded from `cache` when an engine for this GPU, these shapes, these versions
    and these weights was built before, built otherwise (minutes, said) and kept there. In the module's own dtype - a
    float16 copy (dtype_copy) builds a float16 engine - and float32 with TF32 off. A call unlike the one it was built
    for (another shape, another argument that is not a tensor) runs the module's own forward.
    RuntimeError naming what is missing when TensorRT is not installed; ValueError for a module given tensors inside
    other values (a dict of them), which an engine's inputs cannot be.

    WHY the module is built behind one that takes its tensors in order: TensorRT's compile takes positional inputs and
    refuses a module given none - a transformer whose forward takes keyword arguments alone, as GR00T N1.7's does.
    WHY no precision is named beside explicit typing: each layer then runs in the dtype it computes in, and TensorRT
    refuses a precision named as well (torch_tensorrt 2.9)."""
    import torch

    try:
        import torch_tensorrt
    except ImportError:
        raise RuntimeError(f"TensorRT is not installed: {tensorrt_install()}") from None
    flat, inputs, call = _positional(module, args, kwargs)
    dtype = next((p.dtype for p in module.parameters() if p.is_floating_point()), torch.float32)
    key = _engine_key(module, args, kwargs, str(dtype), getattr(torch_tensorrt, "__version__", "?"))
    path = Path(cache) / f"{key}.ep"
    if path.exists():
        try:
            return call(torch.export.load(str(path)).module())
        except Exception:  # noqa: BLE001 (an engine that does not load is built again)
            pass
    say(f"tensorrt: building an engine for {type(module).__name__} (minutes, the first time on this GPU)")
    settings = _accepted(torch_tensorrt.compile, {"ir": "dynamo", "inputs": inputs, "enabled_precisions": {dtype},
                                                  "disable_tf32": True, "use_explicit_typing": True,
                                                  "min_block_size": 1})
    if settings.get("use_explicit_typing"):
        settings.pop("enabled_precisions", None)
    kept = torch.backends.cuda.matmul.allow_tf32, torch.backends.cudnn.allow_tf32
    torch.backends.cuda.matmul.allow_tf32 = torch.backends.cudnn.allow_tf32 = False
    try:
        built = torch_tensorrt.compile(flat, **settings)
    finally:
        torch.backends.cuda.matmul.allow_tf32, torch.backends.cudnn.allow_tf32 = kept
    try:
        Path(cache).mkdir(parents=True, exist_ok=True)
        torch_tensorrt.save(built, str(path), inputs=inputs)
    except Exception:  # noqa: BLE001 (an engine that cannot be kept is built again at the next start)
        pass
    return call(built)


def _positional(module: Any, args: tuple, kwargs: dict) -> tuple[Any, list, Callable]:
    """`module` behind a module that takes its tensors alone, in order - the positional ones, then the keyword ones -
    with every other argument as this call gave it; those tensors; and what makes an engine built from it a function
    called as the module is, which runs the module's own forward for a call unlike this one."""
    import torch

    if any(not isinstance(value, torch.Tensor) and _holds_tensor(value) for value in (*args, *kwargs.values())):
        raise ValueError("its inputs hold tensors inside other values, which an engine's inputs cannot be")
    slots = [i for i, value in enumerate(args) if isinstance(value, torch.Tensor)]
    names = [name for name, value in kwargs.items() if isinstance(value, torch.Tensor)]
    if not slots and not names:
        raise ValueError("it is given no tensor")

    class Flat(torch.nn.Module):
        def __init__(self) -> None:
            super().__init__()
            self.inner = module

        def run(self, tensors: tuple):
            given = dict(zip(slots, tensors))
            return self.inner(*[given.get(i, value) for i, value in enumerate(args)],
                              **{**kwargs, **dict(zip(names, tensors[len(slots):]))})

    # A forward of one named parameter a tensor: TensorRT's export gives each parameter of the forward's signature its
    # shapes, and refuses a forward of *tensors (torch_tensorrt 2.9)
    params = ", ".join(f"t{i}" for i in range(len(slots) + len(names)))
    scope: dict = {}
    exec(f"def forward(self, {params}):\n    return self.run(({params},))\n", scope)  # noqa: S102 (its names alone)
    Flat.forward = scope["forward"]

    built_for, own = _call_shape(args, kwargs), own_forward(module)

    def call(engine: Callable) -> Callable:
        def run(*a, **k):
            if _call_shape(a, k) != built_for:
                return own(*a, **k)
            return engine(*[a[i] for i in slots], *[k[name] for name in names])
        return run

    return Flat(), [args[i] for i in slots] + [kwargs[name] for name in names], call


def _holds_tensor(value: Any) -> bool:
    import torch

    if isinstance(value, torch.Tensor):
        return True
    if isinstance(value, dict):
        return any(_holds_tensor(v) for v in value.values())
    return isinstance(value, (list, tuple)) and any(_holds_tensor(v) for v in value)


def _call_shape(args: tuple, kwargs: dict) -> tuple:
    """What an engine is built for in a call: each tensor's place, shape, dtype and device; each plain value (a
    number, a string, None) as it is; any other value by its identity."""
    import torch

    def one(value: Any) -> tuple:
        if isinstance(value, torch.Tensor):
            return ("tensor", tuple(value.shape), value.dtype, value.device)
        if value is None or isinstance(value, (bool, int, float, str)):
            return ("value", value)
        return ("object", id(value))

    return tuple(one(value) for value in args), tuple(sorted((name, one(value)) for name, value in kwargs.items()))


def _accepted(fn: Callable, settings: dict) -> dict:
    """The settings `fn` takes by name: torch_tensorrt's compile takes some of them only in some versions."""
    import inspect

    try:
        names = inspect.signature(fn).parameters
    except (TypeError, ValueError):
        return settings
    if any(p.kind is inspect.Parameter.VAR_KEYWORD for p in names.values()):
        return {k: v for k, v in settings.items() if v is not None}
    return {k: v for k, v in settings.items() if k in names and v is not None}


def _engine_key(module: Any, args: tuple, kwargs: dict, precision: str, version: str) -> str:
    """What an engine holds for: the GPU model, torch and TensorRT's versions, the precision, each input's shape and
    dtype, and the module's weights (each tensor's shape, dtype, sum and largest magnitude)."""
    import torch

    h = hashlib.sha256()
    gpu = torch.cuda.get_device_name() if torch.cuda.is_available() else "cpu"
    h.update(f"{gpu}|{torch.__version__}|{version}|{precision}|{type(module).__qualname__}".encode())
    for value in list(args) + [kwargs[k] for k in sorted(kwargs)]:
        if isinstance(value, torch.Tensor):
            h.update(f"|{tuple(value.shape)}|{value.dtype}".encode())
        else:
            h.update(f"|{type(value).__name__}:{value!r}"[:200].encode())
    for name, tensor in list(module.named_parameters()) + list(module.named_buffers()):
        t = tensor.detach()
        if t.is_floating_point():
            h.update(f"|{name}|{tuple(t.shape)}|{t.dtype}|{float(t.float().sum())!r}|"
                     f"{float(t.float().abs().amax()) if t.numel() else 0.0!r}".encode())
        else:
            h.update(f"|{name}|{tuple(t.shape)}|{t.dtype}".encode())
    return h.hexdigest()[:32]


def dtype_copy(module: Any, dtype: Any) -> Any:
    """A copy of `module` with its floating-point weights in `dtype` (torch.float16, torch.float32), as its class
    defines it: a forward put in front of its own, or of a submodule's, is not copied. The module keeps its own."""
    return _clean_copy(module).to(dtype)


def cast_around(fn: Callable, dtype: Any, to: Any = None) -> Callable:
    """`fn` with its floating-point inputs cast to `to` (default float16) and its floating-point outputs cast to
    `dtype`: the forward that runs a copy in another dtype (dtype_copy) in place of a module of `dtype`. Tensors are
    cast inside lists, tuples, named tuples, dicts and a model's output objects (any mutable mapping, cast in place):
    SmolVLA's vision model returns one, whose float16 hidden state reached the next layer uncast and was refused."""
    import torch

    to = to or torch.float16

    def cast(value, into):
        if isinstance(value, torch.Tensor):
            return value.to(into) if value.is_floating_point() else value
        if type(value) in (list, tuple):
            return type(value)(cast(v, into) for v in value)
        if isinstance(value, tuple) and hasattr(value, "_fields"):            # a named tuple, as its own type
            return type(value)(*(cast(v, into) for v in value))
        if type(value) is dict:
            return {k: cast(v, into) for k, v in value.items()}
        if isinstance(value, MutableMapping):         # a model's output object (transformers' ModelOutput): in place
            for key in list(value.keys()):
                value[key] = cast(value[key], into)
            return value
        return value

    def forward(*args, **kwargs):
        return cast(fn(*cast(args, to), **cast(kwargs, to)), dtype)

    return forward


def _clean_copy(module: Any) -> Any:
    """A deep copy of `module` without the forwards put in front of its modules' own (instance attributes), which
    hold what cannot be copied (graphs) or point back at the original."""
    held = []
    for sub in module.modules():
        if "forward" in vars(sub):
            held.append((sub, vars(sub).pop("forward")))
    try:
        return _copy.deepcopy(module)
    finally:
        for sub, forward in held:
            sub.forward = forward
