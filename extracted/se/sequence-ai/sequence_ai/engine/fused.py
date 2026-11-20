# SPDX-FileCopyrightText: Copyright (c) 2026 General Sequences Company
# SPDX-License-Identifier: Apache-2.0
"""
A model's memory-bound steps - a norm, a gated activation, a rotary embedding - each run as one kernel that reads its
data once, in place of the several kernels the model's own code launches for it (optimize()'s fused_kernels).

    from sequence_ai.engine import fused

    done = fused.install(model)        # each norm, gated MLP and rotary function found in it, replaced in place
    fused.uninstall(done)              # each put back as it was

What is replaced, each only where a probe shows it computes what the original computes - the original's own output on
a random input of its width, within the difference a different order of the arithmetic makes:

    LayerNorm, RMSNorm      the row's mean and variance (or mean square), the normalization and the learned scale
                            and shift, in float32, one kernel per row
    a gated MLP             act(gate(x)) * up(x) between its projections, SiLU or GELU, one kernel
    apply_rotary_pos_emb    the rotary embedding of the query and of the key, one kernel each

On a CUDA GPU with Triton the kernels run; anywhere else the same arithmetic runs in torch (the reference), which is
what the kernels are checked against.

In one sentence: walk the model's modules (install) → a norm module, a module with gate, up and down projections, and
the rotary function of each module's own code are candidates → each is probed: its original and the fused version run
on one random input on its device, kept only when they agree → a kept module's forward is an instance attribute in
front of its class's (the module stays where it is, of its own class), a kept rotary function is put in its code
module's namespace → uninstall takes each back.

WHY fused: at a robot's batch sizes, a norm or an activation moves its tensor through memory once per kernel and
computes almost nothing, so a step of five kernels takes about five times one; one kernel reads the row once.
WHY probed, and never assumed from a class's name: two RMSNorms scale by `weight` and by `1 + weight`, two GELUs are
exact and approximate, and a rotary function may index its angles by position; the probe tells which, or leaves the
module alone.
WHY the arithmetic in float32: the kernel reads 16-bit values and writes them, but sums and normalizes as the models'
own float32 code paths do.

The outputs change by the rounding of a different order of the arithmetic, which is why optimize() turns this on only
with the `tolerance` you give it. Standard library, torch, and Triton where it is installed (Linux with a CUDA torch
has it); each imported where it is used.

Adapted from General-Instinct/InstinctFlash instinctflash/kernels/norm.py (Apache-2.0), with its
instinctflash/kernels/activation.py and instinctflash/kernels/rope.py: see THIRD_PARTY_NOTICES.md. Changed here: the
norm kernel without the residual update, the quantization and the routing its source fuses with it; the gated activation
reading its two halves from two tensors and writing the activation instead of quantizing it, with exact GELU added; the
rotary kernel taking the model's own angle tables, query and key apart, in place of splitting a fused projection.
"""
from __future__ import annotations

import inspect
import sys
from typing import Any, Callable, NamedTuple, Optional

__all__ = ["install", "uninstall", "reapply", "norm", "gated", "rotary", "Patch"]

GELU_TANH, SILU, GELU = 0, 1, 2
_ACTS = {GELU_TANH: "gelu_tanh", SILU: "silu", GELU: "gelu"}
_MAX_WIDTH = 65536        # the widest row one program normalizes


class Patch(NamedTuple):
    """One replacement: on `holder` (a module, or a code module for a function), `name` set to `value`; `before` what
    was there - _ABSENT when it was the class's own."""
    holder: Any
    name: str
    value: Any
    before: Any
    what: str


class _Absent:
    """Nothing in the holder's own namespace: its class's attribute applies."""


_ABSENT = _Absent()


# ── kernels ─────────────────────────────────────────────────────────────────────────────────────────────────────────
_KERNELS: dict = {}


def _triton_kernels() -> Optional[dict]:
    """The Triton kernels, compiled on first use: None where Triton is not installed."""
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
    def norm_kernel(X, W, B, Y, stride_x, stride_y, D, eps, LAYERNORM: tl.constexpr, HAS_W: tl.constexpr,
                    HAS_B: tl.constexpr, ONE_PLUS: tl.constexpr, BLOCK: tl.constexpr):
        row = tl.program_id(0)
        cols = tl.arange(0, BLOCK)
        mask = cols < D
        x = tl.load(X + row * stride_x + cols, mask=mask, other=0.0).to(tl.float32)
        if LAYERNORM:
            mean = tl.sum(x, 0) / D
            xc = tl.where(mask, x - mean, 0.0)
            var = tl.sum(xc * xc, 0) / D
            y = xc * tl.math.rsqrt(var + eps)
        else:
            var = tl.sum(x * x, 0) / D
            y = x * tl.math.rsqrt(var + eps)
        if HAS_W:
            w = tl.load(W + cols, mask=mask, other=0.0).to(tl.float32)
            if ONE_PLUS:
                w = w + 1.0
            y = y * w
        if HAS_B:
            y = y + tl.load(B + cols, mask=mask, other=0.0).to(tl.float32)
        tl.store(Y + row * stride_y + cols, y.to(Y.dtype.element_ty), mask=mask)

    @triton.jit
    def gated_kernel(G, U, H, stride_g, stride_u, stride_h, F, ACT: tl.constexpr, BLOCK: tl.constexpr):
        row = tl.program_id(0)
        cols = tl.program_id(1) * BLOCK + tl.arange(0, BLOCK)
        mask = cols < F
        g = tl.load(G + row * stride_g + cols, mask=mask, other=0.0).to(tl.float32)
        u = tl.load(U + row * stride_u + cols, mask=mask, other=0.0).to(tl.float32)
        if ACT == 0:
            inner = 0.7978845608028654 * (g + 0.044715 * g * g * g)
            a = 0.5 * g * (1.0 + (2.0 / (1.0 + tl.exp(-2.0 * inner)) - 1.0))
        elif ACT == 1:
            a = g / (1.0 + tl.exp(-g))
        else:
            a = 0.5 * g * (1.0 + tl.math.erf(g * 0.7071067811865476))
        tl.store(H + row * stride_h + cols, (a * u).to(H.dtype.element_ty), mask=mask)

    @triton.jit
    def rotary_kernel(X, COS, SIN, Y, sx_b, sx_h, sx_t, sc_b, sc_t, sy_b, sy_h, sy_t, H, T,
                      HALF: tl.constexpr, BLOCK_HALF: tl.constexpr):
        pid = tl.program_id(0)                 # one row of one head: (b, h, t)
        t = pid % T
        h = (pid // T) % H
        b = pid // (T * H)
        i = tl.arange(0, BLOCK_HALF)
        m = i < HALF
        x = X + b * sx_b + h * sx_h + t * sx_t
        lo = tl.load(x + i, mask=m, other=0.0).to(tl.float32)
        hi = tl.load(x + HALF + i, mask=m, other=0.0).to(tl.float32)
        c = COS + b * sc_b + t * sc_t
        s = SIN + b * sc_b + t * sc_t
        c_lo = tl.load(c + i, mask=m, other=0.0).to(tl.float32)
        c_hi = tl.load(c + HALF + i, mask=m, other=0.0).to(tl.float32)
        s_lo = tl.load(s + i, mask=m, other=0.0).to(tl.float32)
        s_hi = tl.load(s + HALF + i, mask=m, other=0.0).to(tl.float32)
        y = Y + b * sy_b + h * sy_h + t * sy_t
        tl.store(y + i, (lo * c_lo - hi * s_lo).to(Y.dtype.element_ty), mask=m)
        tl.store(y + HALF + i, (hi * c_hi + lo * s_hi).to(Y.dtype.element_ty), mask=m)

    # the jitted functions a kernel calls by name, beside tl, where Triton before 3.4 looks for them (fp8's pack_kernel
    # calling e4m3_bytes failed to compile on Triton 3.3.1 without it)
    globals().update({name: value for name, value in locals().items() if isinstance(value, triton.runtime.JITFunction)})
    _KERNELS.update(triton=triton, norm=norm_kernel, gated=gated_kernel, rotary=rotary_kernel)
    return _KERNELS


def _on_gpu(*tensors) -> Optional[dict]:
    """The kernels, when every tensor is on a CUDA GPU and Triton is installed; None: the reference runs."""
    if not all(t is None or t.is_cuda for t in tensors):
        return None
    kernels = _triton_kernels()
    return None if kernels is None or "missing" in kernels else kernels


# ── the fused steps, each with its reference in torch ───────────────────────────────────────────────────────────────
def norm(x: Any, weight: Any = None, bias: Any = None, *, eps: float = 1e-6, layernorm: bool = False,
         one_plus: bool = False, out_dtype: Any = None) -> Any:
    """`x` normalized over its last dimension, in float32: LayerNorm (`layernorm`) or RMSNorm, then scaled by
    `weight` (by 1 + `weight` with `one_plus`) and shifted by `bias`; `out_dtype` (default `x`'s)."""
    import torch

    out_dtype = out_dtype or x.dtype
    width = x.shape[-1]
    kernels = _on_gpu(x, weight, bias)
    if kernels is None or width > _MAX_WIDTH:
        return _norm_reference(x, weight, bias, eps, layernorm, one_plus).to(out_dtype)
    rows = x.reshape(-1, width)
    if rows.stride(-1) != 1:
        rows = rows.contiguous()
    out = torch.empty(rows.shape, dtype=out_dtype, device=x.device)
    if rows.shape[0]:
        block = kernels["triton"].next_power_of_2(width)
        kernels["norm"][(rows.shape[0],)](
            rows, weight if weight is not None else rows, bias if bias is not None else rows, out,
            rows.stride(0), out.stride(0), width, float(eps), LAYERNORM=layernorm, HAS_W=weight is not None,
            HAS_B=bias is not None, ONE_PLUS=one_plus, BLOCK=block, num_warps=4 if block <= 1024 else 8)
    return out.reshape(x.shape)


def _norm_reference(x, weight, bias, eps, layernorm, one_plus):
    import torch

    y = x.float()
    if layernorm:
        y = y - y.mean(-1, keepdim=True)
    y = y * torch.rsqrt(y.pow(2).mean(-1, keepdim=True) + eps)
    if weight is not None:
        y = y * (weight.float() + 1.0 if one_plus else weight.float())
    if bias is not None:
        y = y + bias.float()
    return y


def gated(gate: Any, up: Any, act: int = SILU) -> Any:
    """act(`gate`) * `up`, in float32, in `gate`'s dtype: act GELU_TANH, SILU or GELU (exact)."""
    import torch

    kernels = _on_gpu(gate, up)
    if kernels is None or gate.shape != up.shape:
        return _gated_reference(gate, up, act).to(gate.dtype)
    width = gate.shape[-1]
    g, u = gate.reshape(-1, width), up.reshape(-1, width)
    if g.stride(-1) != 1:
        g = g.contiguous()
    if u.stride(-1) != 1:
        u = u.contiguous()
    out = torch.empty(g.shape, dtype=gate.dtype, device=gate.device)
    if g.shape[0]:
        block = min(1024, kernels["triton"].next_power_of_2(width))
        kernels["gated"][(g.shape[0], kernels["triton"].cdiv(width, block))](
            g, u, out, g.stride(0), u.stride(0), out.stride(0), width, ACT=act, BLOCK=block, num_warps=4)
    return out.reshape(gate.shape)


def _gated_reference(gate, up, act):
    import torch

    g = gate.float()
    if act == GELU_TANH:
        a = torch.nn.functional.gelu(g, approximate="tanh")
    elif act == SILU:
        a = torch.nn.functional.silu(g)
    else:
        a = torch.nn.functional.gelu(g)
    return a * up.float()


def rotary(x: Any, cos: Any, sin: Any, *, heads_dim: int = 1) -> Any:
    """`x` ([B, H, T, D] with `heads_dim` 1, [B, T, H, D] with 2) rotated by the angles `cos`, `sin` ([B, T, D] or
    [T, D]), the halves of its last dimension paired as rotate_half pairs them: x * cos + rotate_half(x) * sin."""
    import torch

    kernels = _on_gpu(x, cos, sin)
    if kernels is None or not _rotary_fits(x, cos, sin, heads_dim):
        return _rotary_reference(x, cos, sin, heads_dim).to(x.dtype)
    b, t, h = (0, 2, 1) if heads_dim == 1 else (0, 1, 2)
    batch, heads, steps, width = x.shape[b], x.shape[h], x.shape[t], x.shape[-1]
    out = torch.empty_like(x)
    cb = cos.stride(0) if cos.dim() == 3 else 0
    ct = cos.stride(-2)
    if batch * heads * steps:
        kernels["rotary"][(batch * heads * steps,)](
            x, cos, sin, out, x.stride(b), x.stride(h), x.stride(t), cb, ct, out.stride(b), out.stride(h),
            out.stride(t), heads, steps, HALF=width // 2,
            BLOCK_HALF=kernels["triton"].next_power_of_2(width // 2), num_warps=1 if width <= 256 else 2)
    return out


def _rotary_fits(x, cos, sin, heads_dim) -> bool:
    """The layouts the kernel reads: x 4-d with its last dimension even and contiguous, cos and sin alike, 2-d or 3-d,
    as wide as x and as long as its steps."""
    if x.dim() != 4 or x.shape[-1] % 2 or x.stride(-1) != 1 or heads_dim not in (1, 2):
        return False
    steps = x.shape[2] if heads_dim == 1 else x.shape[1]
    for angles in (cos, sin):
        if angles.dim() not in (2, 3) or angles.shape[-1] != x.shape[-1] or angles.shape[-2] != steps \
                or angles.stride(-1) != 1:
            return False
        if angles.dim() == 3 and angles.shape[0] not in (1, x.shape[0]):
            return False
    return cos.stride() == sin.stride()


def _rotary_reference(x, cos, sin, heads_dim):
    import torch

    c, s = cos.float(), sin.float()
    if c.dim() == 2:
        c, s = c[None], s[None]
    c, s = c.unsqueeze(heads_dim), s.unsqueeze(heads_dim)
    y = x.float()
    half = y.shape[-1] // 2
    turned = torch.cat([-y[..., half:], y[..., :half]], dim=-1)
    return y * c + turned * s


# ── finding and probing what to replace ─────────────────────────────────────────────────────────────────────────────
def install(model: Any, *, say: Callable[[str], Any] = print) -> list[Patch]:
    """Every norm module, gated MLP and rotary function of `model` (a torch module) that its probe shows the fused
    version agrees with, replaced in place; the patches, for uninstall. A module already patched is left as it is."""
    patches: list[Patch] = []
    codes: dict = {}
    for path, module in model.named_modules():
        if "forward" in vars(module):
            continue                               # replaced already (a graph, another switch): left alone
        found = _norm_patch(module) or _gated_patch(module)
        if found is not None:
            patches.append(Patch(module, "forward", found[0], _ABSENT, f"{path or 'model'}: {found[1]}"))
        code = sys.modules.get(type(module).__module__)
        if code is not None and id(code) not in codes and not type(module).__module__.startswith("torch."):
            codes[id(code)] = code
    for code in codes.values():
        found = _rotary_patch(code, model)
        if found is not None:
            patches.append(found)
    reapply(patches)
    if patches:
        say(f"fused kernels: {len(patches)} replaced - " + ", ".join(p.what for p in patches[:6])
            + (", ..." if len(patches) > 6 else ""))
    return patches


def reapply(patches: list[Patch]) -> None:
    """Each patch put in place (again, after uninstall)."""
    for patch in patches:
        setattr(patch.holder, patch.name, patch.value)


def uninstall(patches: list[Patch]) -> None:
    """Each patch taken back: the module's own forward, the code module's own function."""
    for patch in reversed(patches):
        if patch.before is _ABSENT:
            if patch.name in vars(patch.holder):
                delattr(patch.holder, patch.name)
        else:
            setattr(patch.holder, patch.name, patch.before)


def _probe_input(module, width: int, dtype=None):
    import torch

    device, dtype_of = _where(module)
    generator = torch.Generator(device="cpu").manual_seed(1234)
    x = torch.randn(3, width, generator=generator) * 2.0
    return x.to(device=device, dtype=dtype or dtype_of)


def _where(module):
    import torch

    for tensor in list(module.parameters(recurse=True)) + list(module.buffers(recurse=True)):
        if tensor.is_floating_point():
            return tensor.device, tensor.dtype
    return torch.device("cpu"), torch.float32


def _agree(got, want) -> bool:
    """Whether a fused output agrees with the original's, as two orders of the same arithmetic do."""
    import torch

    if not isinstance(got, torch.Tensor) or not isinstance(want, torch.Tensor) or got.shape != want.shape:
        return False
    if got.dtype != want.dtype:
        return False
    a, b = got.float(), want.float()
    if not (torch.isfinite(a).all() and torch.isfinite(b).all()):
        return False
    scale = max(1.0, float(b.abs().max()))
    loose = want.dtype in (torch.float16, torch.bfloat16)
    return float((a - b).abs().max()) <= (2e-2 if loose else 2e-4) * scale


def _norm_patch(module):
    """(the forward that replaces a norm module's, what it is), when the module is a LayerNorm or an RMSNorm over its
    last dimension that the fused norm agrees with; None otherwise."""
    import torch

    layer_norm = type(module) is torch.nn.LayerNorm
    rms_class = getattr(torch.nn, "RMSNorm", None)
    rms = (rms_class is not None and type(module) is rms_class) or type(module).__name__.endswith("RMSNorm")
    if not (layer_norm or rms):
        return None
    shape = getattr(module, "normalized_shape", None)
    weight = getattr(module, "weight", None)
    if shape is not None and len(tuple(shape)) != 1:
        return None
    width = int(tuple(shape)[0]) if shape is not None else (int(weight.shape[0]) if weight is not None else 0)
    if not width or (weight is not None and tuple(weight.shape) != (width,)):
        return None
    eps = getattr(module, "eps", None)
    if eps is None:
        eps = getattr(module, "variance_epsilon", None)
    if eps is None:                                 # torch.nn.RMSNorm(eps=None): the dtype's own epsilon
        eps = torch.finfo(_where(module)[1]).eps
    x = _probe_input(module, width)
    with torch.no_grad():
        want = module(x)
        probed = want.dtype if isinstance(want, torch.Tensor) else None
        for one_plus in ((False,) if layer_norm else (False, True)):
            def forward(hidden, module=module, one_plus=one_plus, eps=float(eps)):
                w = getattr(module, "weight", None)
                b = getattr(module, "bias", None) if layer_norm else None
                return norm(hidden, w, b, eps=eps, layernorm=layer_norm, one_plus=one_plus,
                            out_dtype=_out_dtype(hidden, w, probed))

            if _agree(forward(x), want):
                kind = "LayerNorm" if layer_norm else ("RMSNorm (1 + weight)" if one_plus else "RMSNorm")
                return forward, kind
    return None


def _out_dtype(hidden, weight, probed):
    """The dtype the original returned on the probe: the input's, or the weight's where it promotes the input."""
    if probed is None or probed == hidden.dtype or weight is None:
        return hidden.dtype
    return probed


def _activation(fn) -> Optional[int]:
    """Which activation `fn` computes, found by running it: GELU_TANH, SILU or GELU; None for another."""
    import torch

    x = torch.linspace(-4.0, 4.0, 81)
    try:
        with torch.no_grad():
            y = fn(x)
    except Exception:  # noqa: BLE001 (an activation that does not take a float32 tensor is none of these)
        return None
    for act in (SILU, GELU_TANH, GELU):
        if isinstance(y, torch.Tensor) and y.shape == x.shape and \
                float((y.float() - _gated_reference(x, torch.ones_like(x), act)).abs().max()) < 1e-5:
            return act
    return None


def _gated_patch(module):
    """(the forward that replaces a gated MLP's - down(act(gate(x)) * up(x)) - and what it is), when the fused
    activation agrees with the module's own forward; None otherwise."""
    import torch

    names = ("gate_proj", "up_proj", "down_proj")
    if not all(isinstance(getattr(module, n, None), torch.nn.Linear) for n in names):
        return None
    act_fn = getattr(module, "act_fn", None)
    act = _activation(act_fn) if callable(act_fn) else None
    if act is None:
        return None

    def forward(x, module=module, act=act):
        return module.down_proj(gated(module.gate_proj(x), module.up_proj(x), act))

    x = _probe_input(module, module.gate_proj.in_features)
    with torch.no_grad():
        if _agree(forward(x), module(x)):
            return forward, f"gated MLP ({_ACTS[act]})"
    return None


def _rotary_patch(code, model) -> Optional[Patch]:
    """The patch putting the fused rotary embedding in place of a code module's apply_rotary_pos_emb(q, k, cos, sin,
    ...), when the two agree on a probe on the model's device and dtype; None otherwise."""
    import torch

    original = vars(code).get("apply_rotary_pos_emb")
    if not inspect.isfunction(original) or getattr(original, "__sequence_ai_fused__", False):
        return None
    try:
        names = list(inspect.signature(original).parameters)
    except (TypeError, ValueError):
        return None
    if names[:4] != ["q", "k", "cos", "sin"]:
        return None
    device, dtype = _where(model)
    fused_fn = _fused_rotary(original)
    generator = torch.Generator(device="cpu").manual_seed(4321)
    q, k = (torch.randn(1, 2, 3, 8, generator=generator).to(device, dtype) for _ in range(2))
    cos, sin = (torch.randn(1, 3, 8, generator=generator).to(device, dtype) for _ in range(2))
    try:
        with torch.no_grad():
            want, got = original(q, k, cos, sin), fused_fn(q, k, cos, sin)
    except Exception:  # noqa: BLE001 (a function that does not take these is left alone)
        return None
    if not (isinstance(want, tuple) and len(want) == 2 and all(_agree(g, w) for g, w in zip(got, want))):
        return None
    return Patch(code, "apply_rotary_pos_emb", fused_fn, original, f"{code.__name__}.apply_rotary_pos_emb")


def _fused_rotary(original: Callable) -> Callable:
    """apply_rotary_pos_emb(q, k, cos, sin, position_ids=None, unsqueeze_dim=1) by the fused kernel; the original for
    the calls it does not cover (angles indexed by position, a rotary narrower than the head)."""
    def apply_rotary_pos_emb(q, k, cos, sin, *args, **kwargs):
        position_ids = kwargs.get("position_ids", args[0] if args else None)
        unsqueeze_dim = kwargs.get("unsqueeze_dim", args[1] if len(args) > 1 else 1)
        if position_ids is not None or set(kwargs) - {"position_ids", "unsqueeze_dim"} or len(args) > 2 \
                or not (_rotary_fits(q, cos, sin, unsqueeze_dim) and _rotary_fits(k, cos, sin, unsqueeze_dim)):
            return original(q, k, cos, sin, *args, **kwargs)
        return rotary(q, cos, sin, heads_dim=unsqueeze_dim), rotary(k, cos, sin, heads_dim=unsqueeze_dim)

    apply_rotary_pos_emb.__wrapped__ = original
    apply_rotary_pos_emb.__sequence_ai_fused__ = True
    return apply_rotary_pos_emb
