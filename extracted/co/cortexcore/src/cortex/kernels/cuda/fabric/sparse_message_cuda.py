from __future__ import annotations

import os

import torch
from cortex.kernels.cuda.extension_loader import safe_load_extension
from torch.autograd import Function

_mod_path = os.path.dirname(__file__)
_ext = None


def _load_ext():
    global _ext
    if _ext is not None:
        return _ext
    _ext = safe_load_extension(
        name="fabric_sparse_message_cuda",
        sources=[
            os.path.join(_mod_path, "sparse_message_binding.cpp"),
            os.path.join(_mod_path, "sparse_message_kernels.cu"),
        ],
        extra_cflags=["-O3"],
        extra_cuda_cflags=["-O3", "-Xptxas", "-O3"],
        verbose=False,
    )
    return _ext


class _FabricSparseMessageCUDA(Function):
    @staticmethod
    def forward(
        q: torch.Tensor,
        k_all: torch.Tensor,
        v_all: torch.Tensor,
        neighbor_idx: torch.Tensor,
        neighbor_valid: torch.Tensor,
        edge_distance: torch.Tensor,
        edge_delay: torch.Tensor,
        step_flat: torch.Tensor,
        distance_scale: float,
        use_delay: bool,
    ) -> torch.Tensor:
        (msg,) = _load_ext().forward(
            q.contiguous(),
            k_all.contiguous(),
            v_all.contiguous(),
            neighbor_idx.contiguous(),
            neighbor_valid.contiguous(),
            edge_distance.contiguous(),
            edge_delay.contiguous(),
            step_flat.contiguous(),
            float(distance_scale),
            bool(use_delay),
        )
        return msg

    @staticmethod
    def setup_context(ctx, inputs, output):
        (
            q,
            k_all,
            v_all,
            neighbor_idx,
            neighbor_valid,
            edge_distance,
            edge_delay,
            step_flat,
            distance_scale,
            use_delay,
        ) = inputs
        ctx.save_for_backward(q, k_all, v_all, neighbor_idx, neighbor_valid, edge_distance, edge_delay, step_flat)
        ctx.distance_scale = float(distance_scale)
        ctx.use_delay = bool(use_delay)

    @staticmethod
    def backward(ctx, grad_msg: torch.Tensor):
        q, k_all, v_all, neighbor_idx, neighbor_valid, edge_distance, edge_delay, step_flat = ctx.saved_tensors
        grad_q, grad_k, grad_v = _load_ext().backward(
            grad_msg.contiguous(),
            q.contiguous(),
            k_all.contiguous(),
            v_all.contiguous(),
            neighbor_idx.contiguous(),
            neighbor_valid.contiguous(),
            edge_distance.contiguous(),
            edge_delay.contiguous(),
            step_flat.contiguous(),
            ctx.distance_scale,
            ctx.use_delay,
        )
        return grad_q, grad_k, grad_v, None, None, None, None, None, None, None


def fabric_sparse_message_cuda(
    q: torch.Tensor,
    k_all: torch.Tensor,
    v_all: torch.Tensor,
    neighbor_idx: torch.Tensor,
    neighbor_valid: torch.Tensor,
    edge_distance: torch.Tensor,
    edge_delay: torch.Tensor,
    step_flat: torch.Tensor,
    *,
    distance_scale: float,
    use_delay: bool,
) -> torch.Tensor:
    return _FabricSparseMessageCUDA.apply(
        q,
        k_all,
        v_all,
        neighbor_idx,
        neighbor_valid,
        edge_distance,
        edge_delay,
        step_flat,
        distance_scale,
        use_delay,
    )


__all__ = ["fabric_sparse_message_cuda"]
