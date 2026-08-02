"""Shared multiprocessing.resource_tracker patch (SCALE-002).

Extracted so the identical patch body is defined once and applied by both
``matrice_streaming/__init__.py`` and the NVDEC module instead of being
copy-pasted (drift risk for a subtle interpreter patch).

The patch disables semaphore *unlinking* in the resource_tracker so a
hard-killed worker cannot sem_unlink a semaphore that a still-live sibling
worker is about to rebuild (``SemLock._rebuild`` FileNotFoundError). It is
idempotent: a marker attribute guards against double application, so it is
safe to call from multiple entry points.

Import side effects are intentionally minimal (only
``multiprocessing.resource_tracker``) so importing this module never pulls in
heavy dependencies.
"""

import multiprocessing.resource_tracker as _rt


def install_resource_tracker_patch() -> None:
    """Install the semaphore-unlink no-op patch on this interpreter.

    Must run BEFORE any ``mp.Queue``/``mp.Lock`` is created. Safe to call
    repeatedly and from any process.
    """
    if getattr(_rt, "_matrice_sem_unlink_patch_installed", False):
        return

    _orig_register = _rt.register
    _orig_unregister = _rt.unregister

    def _safe_register(name, rtype):
        if rtype == "semaphore":
            return
        return _orig_register(name, rtype)

    def _safe_unregister(name, rtype):
        if rtype == "semaphore":
            return
        return _orig_unregister(name, rtype)

    _rt.register = _safe_register
    _rt.unregister = _safe_unregister
    if "semaphore" in getattr(_rt, "_CLEANUP_FUNCS", {}):
        _rt._CLEANUP_FUNCS["semaphore"] = lambda name: None
    _rt._matrice_sem_unlink_patch_installed = True
