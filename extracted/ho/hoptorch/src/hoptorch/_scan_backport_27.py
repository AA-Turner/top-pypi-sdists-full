"""PyTorch 2.7 scan backport.

PyTorch 2.7 exposes ``torch._higher_order_ops.scan.scan`` but registers its
Autograd dispatch key as ``autograd_not_implemented``. For that version, patch
the public scan function to a small eager Python implementation whose backward
is handled by ordinary PyTorch autograd through the unrolled loop.
"""

from __future__ import annotations

from typing import Any, Callable


def _canonicalize_dim(ndim: int, dim: int) -> int:
    if not isinstance(dim, int):
        raise RuntimeError(f"Dim must be an int, but got {type(dim)}")
    if ndim == 0:
        raise RuntimeError("Cannot scan over a scalar xs tensor")
    if dim < 0:
        dim += ndim
    if dim < 0 or dim >= ndim:
        raise IndexError(f"Dimension out of range (expected 0 <= dim < {ndim}, got {dim})")
    return dim


def _validate_tensor_leaves(torch: Any, leaves: list[Any], name: str) -> None:
    if not leaves:
        raise RuntimeError(f"scan() operator requires {name} leaves.")
    for leaf in leaves:
        if not isinstance(leaf, torch.Tensor):
            raise RuntimeError(f"All {name} leaves must be tensors, but got {leaf!r}")


def scan_27_backport(
    combine_fn: Callable[[Any, Any], tuple[Any, Any]],
    init: Any,
    xs: Any,
    *,
    dim: int = 0,
    reverse: bool = False,
) -> tuple[Any, Any]:
    """Eager scan implementation for PyTorch 2.7 with normal autograd support."""

    import torch
    import torch.utils._pytree as pytree

    if not callable(combine_fn):
        raise RuntimeError(f"Combine_fn must be callable, but got {combine_fn!r}")
    if not isinstance(reverse, bool):
        raise RuntimeError(f"Reverse must be a bool, but got {type(reverse)}")

    leaves_init, spec_init = pytree.tree_flatten(init)
    leaves_xs_orig, spec_xs = pytree.tree_flatten(xs)
    if not leaves_xs_orig:
        return init, []

    _validate_tensor_leaves(torch, leaves_init, "init")
    _validate_tensor_leaves(torch, leaves_xs_orig, "xs")

    ndim = leaves_xs_orig[0].ndim
    dim = _canonicalize_dim(ndim, dim)
    scan_length = leaves_xs_orig[0].shape[dim]
    for leaf in leaves_xs_orig:
        if leaf.ndim <= dim:
            raise RuntimeError(
                f"All xs leaves must have dimension {dim}, but got shape {tuple(leaf.shape)}"
            )
        if leaf.shape[dim] != scan_length:
            raise RuntimeError("All xs leaves must have the same scan dimension size")

    leaves_xs = [torch.movedim(leaf, dim, 0) for leaf in leaves_xs_orig]
    if reverse:
        leaves_xs = [torch.flip(leaf, [0]) for leaf in leaves_xs]

    carry = init
    out_spec = None
    flat_outputs_by_step: list[list[Any]] = []
    for index in range(scan_length):
        x_slice = pytree.tree_unflatten(
            [leaf.select(0, index) for leaf in leaves_xs], spec_xs
        )
        carry, output = combine_fn(carry, x_slice)
        flat_output, current_out_spec = pytree.tree_flatten(output)
        if out_spec is None:
            out_spec = current_out_spec
        elif current_out_spec != out_spec:
            raise RuntimeError("scan output pytree structure changed across iterations")
        for leaf in flat_output:
            if not isinstance(leaf, torch.Tensor):
                raise RuntimeError(
                    "hoptorch's PyTorch 2.7 scan backport only supports tensor output leaves"
                )
        flat_outputs_by_step.append(flat_output)

    flat_carry, current_carry_spec = pytree.tree_flatten(carry)
    if current_carry_spec != spec_init:
        raise RuntimeError("scan carry pytree structure must match init")
    for init_leaf, carry_leaf in zip(leaves_init, flat_carry):
        if not isinstance(carry_leaf, torch.Tensor):
            raise RuntimeError("All carry leaves must be tensors")
        if init_leaf.shape != carry_leaf.shape or init_leaf.dtype != carry_leaf.dtype:
            raise RuntimeError("scan carry tensor metadata must match init")

    if out_spec is None:
        return carry, []

    flat_stacked_outputs = []
    for output_index in range(len(flat_outputs_by_step[0])):
        leaves = [step[output_index] for step in flat_outputs_by_step]
        stacked = torch.stack(leaves, dim=0)
        if reverse:
            stacked = torch.flip(stacked, [0])
        flat_stacked_outputs.append(stacked)

    return carry, pytree.tree_unflatten(flat_stacked_outputs, out_spec)


def install_scan_27_backport(scan_module: Any) -> bool:
    """Patch ``torch._higher_order_ops.scan.scan`` for PyTorch 2.7."""

    if getattr(scan_module, "_hoptorch_scan_27_backport", False):
        return True
    original_scan = getattr(scan_module, "scan", None)
    if original_scan is None:
        return False
    scan_27_backport._hoptorch_scan_backward_original = original_scan  # type: ignore[attr-defined]
    scan_module.scan = scan_27_backport
    scan_module._hoptorch_scan_27_backport = True
    return True


def rollback_scan_27_backport(scan_module: Any) -> bool:
    """Restore the original PyTorch 2.7 scan function if this patch was applied."""

    if not getattr(scan_module, "_hoptorch_scan_27_backport", False):
        return False
    original_scan = getattr(
        getattr(scan_module, "scan", None), "_hoptorch_scan_backward_original", None
    )
    if original_scan is None:
        return False
    scan_module.scan = original_scan
    scan_module._hoptorch_scan_27_backport = False
    return True
