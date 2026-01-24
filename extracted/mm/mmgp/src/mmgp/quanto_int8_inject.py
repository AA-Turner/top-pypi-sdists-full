from __future__ import annotations

import importlib
import os
from types import SimpleNamespace
from typing import Optional, Tuple

import torch
import torch.nn.functional as F

# Env toggles
_ENV_ENABLE = "WAN2GP_QUANTO_INT8_KERNEL"
_ENV_DEBUG = "WAN2GP_QUANTO_INT8_DEBUG"
_ENV_ALIGN_M = "WAN2GP_QUANTO_INT8_ALIGN_M"
_ENV_ALIGN_N = "WAN2GP_QUANTO_INT8_ALIGN_N"
_ENV_ALIGN_K = "WAN2GP_QUANTO_INT8_ALIGN_K"
_ENV_USE_TC = "WAN2GP_QUANTO_INT8_TC"

# Kernel namespace/entrypoints (resolved lazily)
_KERNEL_OP = None
_KERNEL_MODULES = (
    "mmgp.quanto_int8_cuda",
    "mmgp_quanto_int8_cuda",
    "mmgp_quanto_int8",
)


def _env_flag(name: str, default: str = "1") -> bool:
    val = os.environ.get(name, default)
    return str(val).strip().lower() in ("1", "true", "yes", "on")


def _env_int(name: str, default: int) -> int:
    raw = os.environ.get(name)
    if raw is None:
        return default
    try:
        return int(raw)
    except ValueError:
        return default


def _debug(msg: str) -> None:
    if _env_flag(_ENV_DEBUG, "0"):
        print(f"[WAN2GP][INT8][quanto] {msg}")


def _get_alignments() -> Tuple[int, int, int]:
    # Conservative defaults; keep in sync with kernel requirements.
    align_m = _env_int(_ENV_ALIGN_M, 16)
    align_n = _env_int(_ENV_ALIGN_N, 16)
    align_k = _env_int(_ENV_ALIGN_K, 16)
    return align_m, align_n, align_k


def _is_qbytes_tensor(t: torch.Tensor) -> bool:
    try:
        from optimum.quanto.tensor.qbytes import QBytesTensor
    except Exception:
        return False
    return isinstance(t, QBytesTensor)


def _is_weight_qbytes(t: torch.Tensor) -> bool:
    try:
        from optimum.quanto.tensor.weights.qbytes import WeightQBytesTensor
    except Exception:
        return False
    return isinstance(t, WeightQBytesTensor)


def _flatten_scale(scale: torch.Tensor) -> torch.Tensor:
    if scale.ndim == 2 and scale.shape[1] == 1:
        return scale.view(-1)
    if scale.ndim == 1:
        return scale
    return scale.reshape(-1)


def _quantize_activation_per_row(x_2d: torch.Tensor, scale_dtype: torch.dtype) -> Tuple[torch.Tensor, torch.Tensor]:
    # Symmetric int8 quantization per-row: scale = max(abs(row)) / 127
    x_fp32 = x_2d.to(torch.float32)
    amax = x_fp32.abs().amax(dim=1)
    qmax = 127.0
    scale = amax / qmax
    scale = torch.where(scale == 0, torch.ones_like(scale), scale)
    q = torch.round(x_fp32 / scale[:, None]).clamp(-qmax, qmax).to(torch.int8)
    return q, scale.to(scale_dtype)


def _pad_to_multiple(x: torch.Tensor, m_pad: int, k_pad: int) -> torch.Tensor:
    if m_pad == 0 and k_pad == 0:
        return x
    # Pad last dim (K) and then rows (M)
    if k_pad:
        x = F.pad(x, (0, k_pad))
    if m_pad:
        x = F.pad(x, (0, 0, 0, m_pad))
    return x


def _pad_weights_to_multiple(w: torch.Tensor, n_pad: int, k_pad: int) -> torch.Tensor:
    if n_pad == 0 and k_pad == 0:
        return w
    if k_pad:
        w = F.pad(w, (0, k_pad))
    if n_pad:
        w = F.pad(w, (0, 0, 0, n_pad))
    return w


def _pad_scale_to_multiple(scale: torch.Tensor, pad: int, pad_value: float = 1.0) -> torch.Tensor:
    if pad == 0:
        return scale
    return F.pad(scale, (0, pad), value=pad_value)


def _resolve_kernel_op():
    global _KERNEL_OP
    if _KERNEL_OP is not None:
        return _KERNEL_OP
    # torch.ops path (preferred)
    ops_ns = getattr(torch.ops, "mmgp_quanto_int8", None)
    if ops_ns is not None and hasattr(ops_ns, "int8_scaled_mm"):
        _KERNEL_OP = ops_ns.int8_scaled_mm
        return _KERNEL_OP
    # import module path
    for mod_name in _KERNEL_MODULES:
        try:
            mod = importlib.import_module(mod_name)
        except Exception:
            continue
        if hasattr(mod, "int8_scaled_mm"):
            _KERNEL_OP = mod.int8_scaled_mm
            return _KERNEL_OP
        ops_ns = getattr(torch.ops, "mmgp_quanto_int8", None)
        if ops_ns is not None and hasattr(ops_ns, "int8_scaled_mm"):
            _KERNEL_OP = ops_ns.int8_scaled_mm
            return _KERNEL_OP
    raise RuntimeError(
        "mmgp int8 kernel extension not loaded. Expected torch.ops.mmgp_quanto_int8.int8_scaled_mm "
        "or a module exposing int8_scaled_mm (mmgp.quanto_int8_cuda)."
    )


def _quantize_with_kernel(x_2d: torch.Tensor, scale_dtype: torch.dtype) -> Tuple[torch.Tensor, torch.Tensor]:
    try:
        mod = importlib.import_module("mmgp.quanto_int8_cuda")
        q, s = mod.quantize_per_row_int8(x_2d)
        if s.dtype != scale_dtype:
            s = s.to(scale_dtype)
        return q, s
    except Exception:
        return _quantize_activation_per_row(x_2d, scale_dtype)


def _maybe_get_transposed_weight(other: torch.Tensor) -> torch.Tensor:
    cached = getattr(other, "_mmgp_int8_t", None)
    if isinstance(cached, torch.Tensor) and cached.device == other._data.device:
        if cached.shape == (other._data.shape[1], other._data.shape[0]):
            return cached
    w_t = other._data.t().contiguous()
    try:
        setattr(other, "_mmgp_int8_t", w_t)
    except Exception:
        pass
    return w_t


def _int8_tc_mm(
    a_int8: torch.Tensor,
    b_int8: torch.Tensor,
    a_scale: torch.Tensor,
    b_scale: torch.Tensor,
    b_int8_t: Optional[torch.Tensor] = None,
) -> torch.Tensor:
    if a_int8.dtype != torch.int8 or b_int8.dtype != torch.int8:
        raise RuntimeError("int8 TC path requires int8 tensors")
    a_int8 = a_int8.contiguous()
    if b_int8_t is None:
        b_int8_t = b_int8.t().contiguous()

    # torch._int_mm expects [M, K] @ [K, N]
    acc = torch._int_mm(a_int8, b_int8_t)
    try:
        mod = importlib.import_module("mmgp.quanto_int8_cuda")
        return mod.scale_int32_to(acc, a_scale, b_scale)
    except Exception:
        # Fallback to torch ops if the scaling kernel isn't available
        return (acc.float() * a_scale[:, None] * b_scale[None, :]).to(a_scale.dtype)


def _int8_scaled_mm(
    a_int8: torch.Tensor,
    b_int8: torch.Tensor,
    a_scale: torch.Tensor,
    b_scale: torch.Tensor,
    b_int8_t: Optional[torch.Tensor] = None,
) -> torch.Tensor:
    # a_int8: [M, K], b_int8: [N, K], scales: a=[M], b=[N]
    if not a_int8.is_cuda or not b_int8.is_cuda:
        raise RuntimeError("int8 kernel requires CUDA tensors")
    if a_int8.dtype != torch.int8 or b_int8.dtype != torch.int8:
        raise RuntimeError("int8 kernel requires int8 activations and weights")

    a_int8 = a_int8.contiguous()
    b_int8 = b_int8.contiguous()
    a_scale = _flatten_scale(a_scale).contiguous()
    b_scale = _flatten_scale(b_scale).contiguous()

    m, k = a_int8.shape
    n = b_int8.shape[0]
    use_tc = _env_flag(_ENV_USE_TC, "1")
    if use_tc:
        # torch._int_mm requires M > 16 and M/N/K multiples of 8
        if m <= 16:
            m_pad = 24 - m
        else:
            m_pad = (8 - (m % 8)) % 8
        n_pad = (8 - (n % 8)) % 8
        k_pad = (8 - (k % 8)) % 8
    else:
        align_m, align_n, align_k = _get_alignments()
        m_pad = (align_m - (m % align_m)) % align_m
        n_pad = (align_n - (n % align_n)) % align_n
        k_pad = (align_k - (k % align_k)) % align_k

    if m_pad or n_pad or k_pad:
        a_int8 = _pad_to_multiple(a_int8, m_pad=m_pad, k_pad=k_pad)
        b_int8 = _pad_weights_to_multiple(b_int8, n_pad=n_pad, k_pad=k_pad)
        a_scale = _pad_scale_to_multiple(a_scale, pad=m_pad, pad_value=1.0)
        b_scale = _pad_scale_to_multiple(b_scale, pad=n_pad, pad_value=1.0)
        if b_int8_t is not None and b_int8_t.shape != (b_int8.shape[1], b_int8.shape[0]):
            b_int8_t = None

    if use_tc:
        out = _int8_tc_mm(a_int8, b_int8, a_scale, b_scale, b_int8_t=b_int8_t)
    else:
        op = _resolve_kernel_op()
        out = op(a_int8, b_int8, a_scale, b_scale)
    if m_pad or n_pad:
        out = out[:m, :n]
    return out


def _use_int8_kernel(input: torch.Tensor, other: torch.Tensor) -> bool:
    if not _is_weight_qbytes(other):
        return False
    if other._data.dtype != torch.int8:
        return False
    if not other._data.is_cuda:
        return False
    if _is_qbytes_tensor(input):
        return input._data.dtype == torch.int8 and input._data.is_cuda
    return input.is_cuda and input.dtype in (torch.bfloat16, torch.float16, torch.float32)


def _int8_linear_forward(ctx, input: torch.Tensor, other: torch.Tensor, bias: Optional[torch.Tensor]):
    ctx.save_for_backward(input, other)

    input_shape = input.shape
    in_features = input_shape[-1]
    out_features = other.shape[0]

    # Prepare activations
    if _is_qbytes_tensor(input):
        a_2d = input._data.reshape(-1, in_features)
        a_scale = input._scale
        a_scale = _flatten_scale(a_scale).to(other._scale.dtype)
        if a_scale.numel() == 1:
            a_scale = a_scale.reshape(1).expand(a_2d.shape[0]).contiguous()
        elif a_scale.numel() != a_2d.shape[0]:
            raise RuntimeError("Activation scale length does not match token count")
        a_int8 = a_2d
    else:
        a_2d = input.reshape(-1, in_features)
        a_int8, a_scale = _quantize_with_kernel(a_2d, other._scale.dtype)

    # Per-output scale is handled inside the kernel: out = sum(a*b) * a_scale[row] * b_scale[col]
    b_scale = _flatten_scale(other._scale).to(other._scale.dtype)
    if b_scale.numel() != out_features:
        raise RuntimeError("Weight scale length does not match output features")

    b_int8_t = _maybe_get_transposed_weight(other)
    out_2d = _int8_scaled_mm(a_int8, other._data, a_scale, b_scale, b_int8_t=b_int8_t)
    out = out_2d.reshape(input_shape[:-1] + (out_features,))

    if bias is not None:
        out = out + bias
    return out


_PATCH_STATE = SimpleNamespace(enabled=False, orig_forward=None)


def enable_quanto_int8_kernel() -> bool:
    if _PATCH_STATE.enabled:
        return True
    try:
        from optimum.quanto.tensor.weights import qbytes as _qbytes
    except Exception:
        return False

    orig_forward = _qbytes.WeightQBytesLinearFunction.forward

    def forward(ctx, input, other, bias=None):
        if _use_int8_kernel(input, other):
            _debug("using mmgp int8 kernel")
            return _int8_linear_forward(ctx, input, other, bias)
        return orig_forward(ctx, input, other, bias)

    _qbytes.WeightQBytesLinearFunction.forward = staticmethod(forward)
    _PATCH_STATE.enabled = True
    _PATCH_STATE.orig_forward = orig_forward
    return True


def disable_quanto_int8_kernel() -> bool:
    if not _PATCH_STATE.enabled:
        return False
    from optimum.quanto.tensor.weights import qbytes as _qbytes
    _qbytes.WeightQBytesLinearFunction.forward = staticmethod(_PATCH_STATE.orig_forward)
    _PATCH_STATE.enabled = False
    _PATCH_STATE.orig_forward = None
    return True


def maybe_enable_quanto_int8_kernel() -> bool:
    if not _env_flag(_ENV_ENABLE, "1"):
        return False
    return enable_quanto_int8_kernel()


# Auto-enable on import (default on, can be disabled via env)
maybe_enable_quanto_int8_kernel()
