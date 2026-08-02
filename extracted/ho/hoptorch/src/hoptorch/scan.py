"""Safe wrapper around ``torch._higher_order_ops.scan``."""

from __future__ import annotations

import importlib
from typing import Any, Callable

try:
    import torch
except Exception:  # pragma: no cover - torch is a runtime dependency.
    torch = None  # type: ignore[assignment]

if torch is not None:
    try:
        from torch.compiler import assume_constant_result
        from torch.compiler import disable as _disable_compile
    except (AttributeError, ImportError):
        try:
            from torch._dynamo import assume_constant_result  # type: ignore[no-redef]
            from torch._dynamo import disable as _disable_compile  # type: ignore[no-redef]
        except (AttributeError, ImportError):

            def assume_constant_result(fn: Callable[..., Any]) -> Callable[..., Any]:
                return fn

            def _disable_compile(
                fn: Callable[..., Any] | None = None,
                recursive: bool = True,
                **kwargs: Any,
            ) -> Callable[..., Any]:
                if fn is None:
                    return lambda inner: inner
                return fn
else:

    def assume_constant_result(fn: Callable[..., Any]) -> Callable[..., Any]:
        return fn

    def _disable_compile(
        fn: Callable[..., Any] | None = None,
        recursive: bool = True,
        **kwargs: Any,
    ) -> Callable[..., Any]:
        if fn is None:
            return lambda inner: inner
        return fn


_SCAN_BACKWARD_HEALTH: dict[str, bool] = {}
_SCAN_BACKWARD_PATCH_ATTEMPTED = False
_SCAN_BACKWARD_PATCHED = False
_SCAN_MISSING_REASON = "torch._higher_order_ops.scan is not available"
_TORCH_SCAN: Callable[..., Any] | None = None
_TORCH_SCAN_MODULE: Any | None = None
_TORCH_SCAN_REASON: str | None = None


def _torch() -> Any:
    if torch is None:
        raise RuntimeError("hoptorch requires torch>=2.7")
    return torch


def _canonical_device(device: str | Any | None = None) -> Any:
    torch_mod = _torch()
    if device is None:
        return torch_mod.device("cpu")
    return torch_mod.device(device)


def _device_cache_key(device: str | Any | None = None) -> str:
    return _canonical_device(device).type


def _get_torch_scan() -> tuple[Callable[..., Any] | None, str | None]:
    global _TORCH_SCAN
    global _TORCH_SCAN_MODULE
    global _TORCH_SCAN_REASON

    if _TORCH_SCAN is not None:
        return _TORCH_SCAN, None
    if _TORCH_SCAN_REASON is not None:
        return None, _TORCH_SCAN_REASON
    if torch is None:
        _TORCH_SCAN_REASON = "torch is not installed"
        return None, _TORCH_SCAN_REASON
    try:
        scan_module = importlib.import_module("torch._higher_order_ops.scan")
    except Exception as exc:
        _TORCH_SCAN_REASON = f"{_SCAN_MISSING_REASON}: {exc}"
        return None, _TORCH_SCAN_REASON
    torch_scan = getattr(scan_module, "scan", None)
    if not callable(torch_scan):
        _TORCH_SCAN_REASON = _SCAN_MISSING_REASON
        return None, _TORCH_SCAN_REASON
    _TORCH_SCAN_MODULE = scan_module
    _TORCH_SCAN = torch_scan
    return _TORCH_SCAN, None


def _get_torch_scan_module() -> tuple[Any | None, str | None]:
    global _TORCH_SCAN_MODULE

    torch_scan, reason = _get_torch_scan()
    if torch_scan is None:
        return None, reason
    if _TORCH_SCAN_MODULE is not None:
        return _TORCH_SCAN_MODULE, None
    if torch is None:
        return None, "torch is not installed"
    try:
        scan_module = importlib.import_module("torch._higher_order_ops.scan")
    except Exception as exc:
        return None, f"{_SCAN_MISSING_REASON}: {exc}"
    if not callable(getattr(scan_module, "scan", None)):
        return None, _SCAN_MISSING_REASON
    _TORCH_SCAN_MODULE = scan_module
    return scan_module, None


def _is_compiling() -> bool:
    if torch is None:
        return False
    compiler = getattr(torch, "compiler", None)
    for attr in ("is_compiling", "is_dynamo_compiling"):
        fn = getattr(compiler, attr, None) if compiler is not None else None
        if callable(fn):
            try:
                if bool(fn()):
                    return True
            except Exception:
                pass
    try:
        import torch._dynamo as dynamo

        fn = getattr(dynamo, "is_compiling", None)
        if callable(fn):
            return bool(fn())
    except Exception:
        pass
    return False


def _first_tensor_device(value: Any) -> Any:
    torch_mod = _torch()
    if isinstance(value, torch_mod.Tensor):
        return value.device
    if isinstance(value, dict):
        iterable = value.values()
    elif isinstance(value, (tuple, list)):
        iterable = value
    else:
        return torch_mod.device("cpu")
    for item in iterable:
        device = _first_tensor_device(item)
        if device.type != "cpu" or isinstance(item, torch_mod.Tensor):
            return device
    return torch_mod.device("cpu")


@_disable_compile
def _run_scan_backward_probe(device: Any) -> bool:
    from ._scan_probe import scan_backward_probe

    return scan_backward_probe(device)


def _install_scan_backward_patch(scan_module: Any) -> bool:
    from ._scan_patch import install_scan_backward_patch

    return install_scan_backward_patch(scan_module)


def _rollback_failed_scan_backward_patch(scan_module: Any) -> bool:
    from ._scan_patch import rollback_failed_scan_backward_patch

    return rollback_failed_scan_backward_patch(scan_module)


def has_scan() -> bool:
    """Return whether ``torch._higher_order_ops.scan.scan`` exists."""

    torch_scan, _ = _get_torch_scan()
    return torch_scan is not None


@_disable_compile
def patch_scan_backward() -> bool:
    """Attempt to install the scan backward compatibility patch.

    This function reports whether a patch was installed or was already present.
    Call :func:`ensure_scan_backward` to verify that scan backward is actually
    usable after patching.
    """

    global _SCAN_BACKWARD_PATCH_ATTEMPTED, _SCAN_BACKWARD_PATCHED

    if _SCAN_BACKWARD_PATCH_ATTEMPTED:
        return _SCAN_BACKWARD_PATCHED

    _SCAN_BACKWARD_PATCH_ATTEMPTED = True
    scan_module, _ = _get_torch_scan_module()
    if scan_module is None:
        _SCAN_BACKWARD_PATCHED = False
        return False

    _SCAN_BACKWARD_PATCHED = bool(_install_scan_backward_patch(scan_module))
    if _SCAN_BACKWARD_PATCHED:
        _SCAN_BACKWARD_HEALTH.clear()
    return _SCAN_BACKWARD_PATCHED


def _enable_capture_scalar_outputs() -> None:
    """Turn on dynamo's ``capture_scalar_outputs`` so scan can be compiled.

    Inductor lowers scan to a ``while_loop`` whose body computes a
    data-dependent ``loop_idx.item()``
    (``torch/_inductor/fx_passes/post_grad.py``, ``decompose_scan_to_while_loop``).
    Under the default ``capture_scalar_outputs=False`` Inductor raises
    ``DataDependentOutputException`` on ``aten._local_scalar_dense``, breaking
    ``torch.compile`` of any scan (a hard crash on torch>=2.11, a silent
    eager-fallback graph break on earlier builds).

    The flag is flipped here, in eager, rather than inside the compiled frame:
    it persists into the subsequent compilation without forcing a graph break.
    Patching it from within the traced scan call (e.g. via
    ``torch._dynamo.config.patch``) would graph-break, which is illegal under
    ``fullgraph=True`` and regresses scan compilations that already work.
    """

    if torch is None:
        return
    try:
        torch._dynamo.config.capture_scalar_outputs = True
    except Exception:  # pragma: no cover - extremely defensive.
        pass


@assume_constant_result
def ensure_scan_backward(device: str | Any | None = None) -> bool:
    """Return ``True`` when scan backward is healthy after optional patching.

    The health result is cached per device type. The function fails closed and
    never reports success unless the regression probe passes.
    """

    if not has_scan():
        return False

    device_obj = _canonical_device(device)
    if device_obj.type == "meta":
        return False
    key = device_obj.type

    if _is_compiling():
        return _SCAN_BACKWARD_HEALTH.get(key) is True

    # Runs in eager here (also during ``torch.compile`` tracing, because this
    # function is ``@assume_constant_result``), i.e. before Inductor lowers the
    # scan -- exactly when the flag must be set. See
    # :func:`_enable_capture_scalar_outputs`.
    _enable_capture_scalar_outputs()

    healthy = _SCAN_BACKWARD_HEALTH.get(key)
    if healthy is True:
        return True
    if healthy is None:
        healthy = bool(_run_scan_backward_probe(device_obj))
        _SCAN_BACKWARD_HEALTH[key] = healthy
        if healthy:
            return True
    elif healthy is False and _SCAN_BACKWARD_PATCH_ATTEMPTED:
        return False

    if _SCAN_BACKWARD_PATCH_ATTEMPTED:
        return False
    if not patch_scan_backward():
        return False

    healthy = bool(_run_scan_backward_probe(device_obj))
    _SCAN_BACKWARD_HEALTH[key] = healthy
    if not healthy:
        scan_module, _ = _get_torch_scan_module()
        if scan_module is not None:
            _rollback_failed_scan_backward_patch(scan_module)
    return healthy


@assume_constant_result
def scan_unavailable_reason(device: str | Any | None = None) -> str | None:
    """Return why scan backward is unavailable, or ``None`` when usable."""

    _, reason = _get_torch_scan()
    if reason is not None:
        return reason

    device_obj = _canonical_device(device)
    if device_obj.type == "meta":
        return "torch._higher_order_ops.scan backward is not checked for meta tensors"
    key = device_obj.type

    if _is_compiling():
        healthy = _SCAN_BACKWARD_HEALTH.get(key)
        if healthy is True:
            return None
        if healthy is False or _SCAN_BACKWARD_PATCH_ATTEMPTED:
            return "torch._higher_order_ops.scan backward failed its health check"
        return (
            "torch._higher_order_ops.scan backward has not been checked before "
            "torch.compile"
        )

    if not ensure_scan_backward(device_obj):
        return "torch._higher_order_ops.scan backward failed its health check"
    return None


def scan(fn: Callable[..., Any], init: Any, xs: Any, *, dim: int = 0, **kwargs: Any) -> Any:
    """Call PyTorch scan after verifying scan backward compatibility.

    The device is inferred from ``init``, ``xs``, and keyword arguments. If the
    health check has not passed, this wrapper raises ``RuntimeError`` instead of
    using a potentially incorrect scan backward implementation.
    """

    torch_scan, reason = _get_torch_scan()
    if torch_scan is None:
        raise RuntimeError(reason or _SCAN_MISSING_REASON)

    device = _first_tensor_device((init, xs, kwargs))
    reason = scan_unavailable_reason(device)
    if reason is not None:
        raise RuntimeError(
            "torch._higher_order_ops.scan backward support is required, "
            f"but {reason}."
        )
    return torch_scan(fn, init, xs, dim=dim, **kwargs)


def _reset_scan_backward_state_for_tests() -> None:
    global _SCAN_BACKWARD_PATCH_ATTEMPTED, _SCAN_BACKWARD_PATCHED
    global _TORCH_SCAN, _TORCH_SCAN_MODULE, _TORCH_SCAN_REASON

    _SCAN_BACKWARD_HEALTH.clear()
    _SCAN_BACKWARD_PATCH_ATTEMPTED = False
    _SCAN_BACKWARD_PATCHED = False
    _TORCH_SCAN = None
    _TORCH_SCAN_MODULE = None
    _TORCH_SCAN_REASON = None


__all__ = [
    "ensure_scan_backward",
    "has_scan",
    "patch_scan_backward",
    "scan",
    "scan_unavailable_reason",
]
