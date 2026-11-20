# SPDX-FileCopyrightText: Copyright (c) 2026 General Sequences Company
# SPDX-License-Identifier: Apache-2.0
"""
A module's linear layers in 8-bit floating point (E4M3), on a GPU with FP8 tensor cores (optimize()'s precision="fp8").

    from sequence_ai.engine import fp8

    fp8.unsupported()                              # None on a GPU of compute capability 8.9 or later; else why not
    done = fp8.install(module, calibrate=run)      # the layers fp8 keeps close, each now running in fp8
    fp8.uninstall(done)                            # each running as it did

In one sentence: each plain nn.Linear of the module whose sides are multiples of 16 → calibrated: while `calibrate`
runs the model (on your examples), each layer's fp8 output is computed beside its own on the very inputs it gets, and
a layer whose fp8 output is further than `max_error` from its own (relative) keeps its own precision; the layers kept
are written to ~/.cache/sequence-ai/fp8, so a start with the same weights and examples does not calibrate again →
each kept layer's weight packed once to E4M3 with one scale, its largest magnitude / 448 → on each call, the input's
scale found on the GPU (its largest magnitude / 448), the input packed with it, one scaled matrix multiply
accumulated in float32 (torch._scaled_mm), bfloat16 out, cast back to the input's dtype.

WHY each layer measured on its own inputs: a layer whose activations hold a few large values loses its small ones to
one scale; measured where it runs, such a layer is found and left as it is, and the others gain fp8's speed.
WHY the input's scale found on every call, not set once from the examples: a robot's inputs move beyond any set of
examples, and a scale set on them would clip a larger activation; finding it is two small reductions on the GPU.
WHY the input packed by a kernel of its own on compute capability 8.9: there, Triton's conversion to E4M3 rounds
through float16, twice; the kernel rounds the float32 value to E4M3 directly, as torch's own conversion does.
WHY the layer kept and only its forward replaced: the model's code may read a layer's weight or check its class; the
weight stays the layer's, in its own dtype, beside its packed copy.

The outputs change - E4M3 keeps 3 bits of mantissa - which is why optimize() turns this on only with the `tolerance`
you give it. Off a GPU, and for the tests, the same arithmetic runs on the CPU (the reference).

Adapted from General-Instinct/InstinctFlash instinctflash/runtime/torch_fp8_linear.py (Apache-2.0), with its
instinctflash/runtime/fp8_pack.py: see THIRD_PARTY_NOTICES.md. Changed here: any plain nn.Linear of any
float dtype found in a module, its input cast to bfloat16 for the multiply and its output cast back, in place of a
model family's audited projections in bfloat16; the layer kept, its forward replaced; the calibration and its cache.
"""
from __future__ import annotations

import hashlib
import json
import os
from pathlib import Path
from typing import Any, Callable, Optional

__all__ = ["install", "uninstall", "reapply", "unsupported", "eligible", "pack", "matmul", "MAX_ERROR", "CACHE"]

FP8_MAX = 448.0
MAX_ERROR = 0.05          # a layer whose fp8 output is further than this from its own, relative, keeps its precision
CACHE = Path.home() / ".cache" / "sequence-ai" / "fp8"
RECIPE = "e4m3-per-tensor-weight-dynamic-per-tensor-input-bf16-out-v1"

_KERNELS: dict = {}


def unsupported(device: Any = None) -> Optional[str]:
    """Why this machine cannot run fp8 layers, or None: a CUDA GPU of compute capability 8.9 or later, and a torch
    with its FP8 matrix multiply."""
    import torch

    if not torch.cuda.is_available():
        return "fp8 needs a CUDA GPU"
    major, minor = torch.cuda.get_device_capability(device)
    if (major, minor) < (8, 9):
        return (f"fp8 needs a GPU with FP8 tensor cores, of compute capability 8.9 or later; this "
                f"{torch.cuda.get_device_name(device)} is {major}.{minor}")
    if not callable(getattr(torch, "_scaled_mm", None)) or not hasattr(torch, "float8_e4m3fn"):
        return "this torch has no FP8 matrix multiply (torch._scaled_mm)"
    return None


class Packed:
    """One linear layer's weight in E4M3: the packed weight [out, in], its one float32 scale, and its bias in
    bfloat16."""

    def __init__(self, linear: Any) -> None:
        import torch

        w = linear.weight.detach()
        self.in_features, self.out_features = linear.in_features, linear.out_features
        self.scale = (w.float().abs().amax().clamp_min(1e-12) / FP8_MAX).reshape(1)
        self.weight = (w.float() / self.scale).clamp(-FP8_MAX, FP8_MAX).to(torch.float8_e4m3fn).contiguous()
        self.bias = None if linear.bias is None else linear.bias.detach().to(torch.bfloat16)


def pack(rows: Any) -> tuple:
    """`rows` [M, K] packed to E4M3 with one scale, their largest magnitude / 448: (packed, scale [1], float32). A
    NaN in `rows` makes the scale NaN, as torch's own reduction does."""
    import torch

    kernels = _triton_kernels() if rows.is_cuda and rows.dtype == torch.bfloat16 and rows.is_contiguous() else None
    if kernels is None or not rows.numel():
        scale = (rows.abs().amax().float().clamp_min(1e-12) / FP8_MAX).reshape(1)
        return (rows.float() / scale).clamp(-FP8_MAX, FP8_MAX).to(torch.float8_e4m3fn), scale
    triton = kernels["triton"]
    count = triton.cdiv(rows.numel(), 4096)
    partial = torch.empty((count,), device=rows.device, dtype=torch.float32)
    scale = torch.empty((1,), device=rows.device, dtype=torch.float32)
    kernels["amax"][(count,)](rows, partial, rows.numel(), 4096)
    kernels["finish"][(1,)](partial, scale, count, triton.next_power_of_2(count))
    out = torch.empty_like(rows, dtype=torch.float8_e4m3fn)
    kernels["pack"][(triton.cdiv(rows.numel(), 1024),)](
        rows, scale, out, rows.numel(), 1024, DIRECT=torch.cuda.get_device_capability(rows.device) == (8, 9))
    return out, scale


def matmul(packed: Packed, x: Any) -> Any:
    """x @ weight.T + bias with the weight and `x` in E4M3: bfloat16 out, cast to `x`'s dtype."""
    import torch

    rows = x.reshape(-1, packed.in_features)
    if rows.dtype != torch.bfloat16:
        rows = rows.to(torch.bfloat16)
    rows = rows.contiguous()
    shape = (*x.shape[:-1], packed.out_features)
    if not rows.shape[0]:
        return x.new_empty(shape)
    q, scale = pack(rows)
    if rows.is_cuda:
        out = torch._scaled_mm(q, packed.weight.t(), scale_a=scale, scale_b=packed.scale, bias=packed.bias,
                               out_dtype=torch.bfloat16, use_fast_accum=False)
    else:                           # the reference: the same E4M3 values, multiplied in float32
        out = (q.float() * scale) @ (packed.weight.float() * packed.scale).t()
        if packed.bias is not None:
            out = out + packed.bias.float()
        out = out.to(torch.bfloat16)
    return out.reshape(shape).to(x.dtype)


def eligible(module: Any) -> list[tuple[str, Any]]:
    """The layers fp8 can run: each plain nn.Linear of `module`, of a float dtype, its sides multiples of 16, its
    weight finite, no hook on it and its forward its own."""
    import torch

    found = []
    for path, layer in module.named_modules():
        if type(layer) is not torch.nn.Linear or "forward" in vars(layer):
            continue
        if layer._forward_hooks or layer._forward_pre_hooks:
            continue
        if layer.in_features % 16 or layer.out_features % 16 or not layer.weight.is_floating_point():
            continue
        if not bool(torch.isfinite(layer.weight).all()):
            continue
        found.append((path, layer))
    return found


def install(module: Any, *, calibrate: Callable[[], Any], key: str = "", max_error: float = MAX_ERROR,
            cache: Optional[Path] = CACHE, say: Callable[[str], Any] = print) -> list:
    """Each eligible layer of `module` whose fp8 output stays within `max_error` of its own - measured while
    `calibrate()` runs the model, or read from `cache` for the same weights and `key` (your examples) - running in fp8
    from now on: the patches, for uninstall (the patches of fused.py, so either can take them back)."""
    from .fused import _ABSENT, Patch

    layers = eligible(module)
    if not layers:
        return []
    packed = {path: Packed(layer) for path, layer in layers}
    digest = _fingerprint(layers, key, max_error)
    found = _read(cache, digest)
    if found is None:
        errors = _measure(layers, packed, calibrate)
        kept = [path for path, _ in layers if errors.get(path) is not None and errors[path] <= max_error]
        _write(cache, digest, {"recipe": RECIPE, "kept": kept, "errors": errors, "max_error": max_error})
        said = "calibrated"
    else:
        kept, said = [path for path in found.get("kept") or [] if path in packed], "calibration read from its cache"
    patches = []
    for path, layer in layers:
        if path in kept:
            patches.append(Patch(layer, "forward", _forward(packed[path]), _ABSENT, path or "module"))
    reapply(patches)
    say(f"fp8: {len(patches)} of {len(layers)} linear layers in fp8 ({said}; the others moved more than "
        f"{max_error:.0%} in fp8)" if len(patches) < len(layers) else
        f"fp8: all {len(layers)} linear layers in fp8 ({said})")
    return patches


def reapply(patches: list) -> None:
    """Each patch put in place (again)."""
    from .fused import reapply as _reapply

    _reapply(patches)


def uninstall(patches: list) -> None:
    """Each layer running its own forward again."""
    from .fused import uninstall as _uninstall

    _uninstall(patches)


def _forward(packed: Packed) -> Callable:
    def forward(x):
        return matmul(packed, x)

    return forward


def _measure(layers: list, packed: dict, calibrate: Callable[[], Any]) -> dict:
    """Each layer's largest relative distance between its fp8 output and its own, over what `calibrate()` runs."""
    import torch

    errors: dict = {}
    hooks = []

    def watch(path):
        def hook(layer, args, output):
            if not args or not isinstance(output, torch.Tensor):
                return
            with torch.no_grad():
                got = matmul(packed[path], args[0]).float()
                want = output.float()
                far = float((got - want).norm() / want.norm().clamp_min(1e-12))
            errors[path] = max(errors.get(path, 0.0), far if far == far else float("inf"))
        return hook

    for path, layer in layers:
        hooks.append(layer.register_forward_hook(watch(path)))
    try:
        calibrate()
    finally:
        for hook in hooks:
            hook.remove()
    return errors


def _fingerprint(layers: list, key: str, max_error: float) -> str:
    """What a calibration holds for: the recipe, torch, the GPU, each layer's place, shape, dtype and weights (their
    sum and largest magnitude), your key (the examples) and max_error."""
    import torch

    h = hashlib.sha256()
    gpu = torch.cuda.get_device_name() if torch.cuda.is_available() else "cpu"
    h.update(f"{RECIPE}|{torch.__version__}|{gpu}|{key}|{max_error}".encode())
    for path, layer in layers:
        w = layer.weight.detach()
        h.update(f"|{path}|{tuple(w.shape)}|{w.dtype}|{float(w.float().sum())!r}|"
                 f"{float(w.float().abs().amax())!r}".encode())
    return h.hexdigest()[:32]


def _read(cache: Optional[Path], digest: str) -> Optional[dict]:
    if cache is None:
        return None
    try:
        found = json.loads((Path(cache) / f"{digest}.json").read_text())
    except (OSError, ValueError):
        return None
    return found if isinstance(found, dict) and found.get("recipe") == RECIPE else None


def _write(cache: Optional[Path], digest: str, found: dict) -> None:
    if cache is None:
        return
    try:
        Path(cache).mkdir(parents=True, exist_ok=True)
        part = Path(cache) / f".{digest}.{os.getpid()}"
        part.write_text(json.dumps(found, sort_keys=True))
        os.replace(part, Path(cache) / f"{digest}.json")
    except OSError:
        pass                        # a cache that cannot be written only means calibrating again next time


def _triton_kernels() -> Optional[dict]:
    """The packing kernels, compiled on first use; None where Triton is not installed."""
    if _KERNELS:
        return None if "missing" in _KERNELS else _KERNELS
    try:
        import triton
        import triton.language as tl
    except ImportError:
        _KERNELS["missing"] = True
        return None
    # A kernel's annotations (tl.constexpr) and names are read from its module's globals by Triton before 3.4, which
    # refused this file's kernels with NameError('tl is not defined') on Triton 3.3.1 (torch 2.7, GR00T N1.6's)
    globals()["tl"] = tl

    @triton.jit
    def e4m3_bytes(value):
        # Round the float32 mantissa to E4M3 directly, ties to even; below 2**-6, adding 2**14 makes one float32 unit
        # in the last place one E4M3 subnormal (2**-9).
        bits = value.to(tl.uint32, bitcast=True)
        magnitude = bits & 0x7FFFFFFF
        normal = ((magnitude + 0x7FFFF + ((magnitude >> 20) & 1)) >> 20) - 960
        absolute = magnitude.to(tl.float32, bitcast=True)
        subnormal = (absolute + 16384.0).to(tl.uint32, bitcast=True) - (141 << 23)
        rounded = tl.where(magnitude < (121 << 23), subnormal, normal)
        rounded = tl.where(magnitude >= 0x7F800000, 0x7F, rounded)
        return (rounded | ((bits >> 24) & 0x80)).to(tl.uint8)

    @triton.jit
    def pack_kernel(X, SCALE, Y, N, BLOCK: tl.constexpr, DIRECT: tl.constexpr):
        offsets = tl.program_id(0) * BLOCK + tl.arange(0, BLOCK)
        x = tl.load(X + offsets, offsets < N, other=0).to(tl.float32)
        divided = tl.div_rn(x, tl.load(SCALE))
        clipped = tl.minimum(tl.maximum(divided, -448.0, propagate_nan=tl.PropagateNan.ALL), 448.0,
                             propagate_nan=tl.PropagateNan.ALL)
        if DIRECT:
            tl.store(Y.to(tl.pointer_type(tl.uint8)) + offsets, e4m3_bytes(clipped), offsets < N)
        else:
            tl.store(Y + offsets, clipped.to(tl.float8e4nv), offsets < N)

    @triton.jit
    def amax_kernel(X, PARTIAL, N, BLOCK: tl.constexpr):
        i = tl.program_id(0) * BLOCK + tl.arange(0, BLOCK)
        x = tl.load(X + i, i < N, other=0).to(tl.float32)
        nan = tl.sum((x != x).to(tl.int32), 0) != 0
        value = tl.max(tl.where(x != x, 0.0, tl.abs(x)), 0)
        tl.store(PARTIAL + tl.program_id(0), tl.where(nan, float("nan"), value))

    @triton.jit
    def finish_kernel(PARTIAL, SCALE, COUNT, BLOCK: tl.constexpr):
        i = tl.arange(0, BLOCK)
        x = tl.load(PARTIAL + i, i < COUNT, other=0.0)
        nan = tl.sum((x != x).to(tl.int32), 0) != 0
        value = tl.maximum(tl.max(tl.where(x != x, 0.0, x), 0), 1.0e-12)
        tl.store(SCALE, tl.where(nan, float("nan"), value * (1.0 / 448.0)))

    # the jitted functions a kernel calls by name, beside tl, where Triton before 3.4 looks for them (fp8's pack_kernel
    # calling e4m3_bytes failed to compile on Triton 3.3.1 without it)
    globals().update({name: value for name, value in locals().items() if isinstance(value, triton.runtime.JITFunction)})
    _KERNELS.update(triton=triton, pack=pack_kernel, amax=amax_kernel, finish=finish_kernel)
    return _KERNELS
