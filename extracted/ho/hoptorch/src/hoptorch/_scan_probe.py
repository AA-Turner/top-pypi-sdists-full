"""Health probe for ``torch._higher_order_ops.scan`` backward.

This module intentionally has no dependencies beyond ``torch`` and the Python
standard library. The probe fails closed: any exception is interpreted as an
unhealthy scan backward implementation.
"""

from __future__ import annotations

import importlib
from typing import Any, Callable


def _get_torch_scan() -> Callable[..., Any] | None:
    try:
        scan_module = importlib.import_module("torch._higher_order_ops.scan")
        torch_scan = getattr(scan_module, "scan", None)
    except Exception:
        return None
    return torch_scan if callable(torch_scan) else None


def scan_backward_probe(device: str | object = "cpu") -> bool:
    """Return whether PyTorch scan backward passes a small regression check.

    The regression keeps the initial carry non-differentiable while the scan
    body closes over a differentiable weight. A healthy implementation must
    still propagate the full carry-chain gradient to that closed-over weight.
    """

    try:
        import torch

        torch_scan = _get_torch_scan()
        if torch_scan is None:
            return False

        device = torch.device(device)
        if device.type == "meta":
            return False

        with torch.enable_grad():
            xs = torch.linspace(0.2, 0.8, 4, device=device)
            carry0 = torch.zeros((), device=device)  # intentionally no grad
            weight = torch.tensor(0.7, device=device, requires_grad=True)

            def step(carry: torch.Tensor, x: torch.Tensor) -> tuple[torch.Tensor, torch.Tensor]:
                next_carry = carry * weight + x
                return next_carry, next_carry * weight

            carry, ys = torch_scan(step, carry0, xs, dim=0)
            (grad,) = torch.autograd.grad(carry + ys.sum(), weight)

            ref_weight = weight.detach().clone().requires_grad_(True)
            ref_carry = carry0.detach().clone()
            ref_ys = []
            for x in xs.detach().unbind(0):
                ref_carry = ref_carry * ref_weight + x
                ref_ys.append(ref_carry * ref_weight)
            ref_loss = ref_carry + torch.stack(ref_ys).sum()
            (ref_grad,) = torch.autograd.grad(ref_loss, ref_weight)

        return bool(torch.allclose(grad, ref_grad, atol=1e-5, rtol=1e-5))
    except Exception:
        return False
