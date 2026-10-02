from __future__ import annotations

import importlib
from collections.abc import Callable
from typing import Any


def load_handler(
    dotted_path: str,
) -> tuple[Callable[..., Any], Callable[[], None] | None, Callable[[], None] | None]:
    """Load a handler function from a dotted module path.

    Returns (handler_fn, on_startup_fn_or_None, on_shutdown_fn_or_None).
    The on_startup/on_shutdown functions are auto-discovered if the handler's
    module defines top-level callables with those names.
    """
    if "." not in dotted_path:
        raise ValueError(f"Handler path must be a dotted path like 'my_module.handler', got: {dotted_path!r}")

    module_path, func_name = dotted_path.rsplit(".", 1)
    module = importlib.import_module(module_path)
    handler = getattr(module, func_name, None)
    if handler is None:
        raise AttributeError(f"Module {module_path!r} has no attribute {func_name!r}")
    if not callable(handler):
        raise TypeError(f"{dotted_path!r} is not callable")

    on_startup = getattr(module, "on_startup", None)
    if on_startup is not None and not callable(on_startup):
        on_startup = None

    on_shutdown = getattr(module, "on_shutdown", None)
    if on_shutdown is not None and not callable(on_shutdown):
        on_shutdown = None

    return handler, on_startup, on_shutdown


def load_function(dotted_path: str, label: str = "Function") -> Callable[[], None]:
    """Load a callable from a dotted module path.

    Args:
        dotted_path: e.g. 'my_module.setup'
        label: Human-readable label for error messages (e.g. "Startup", "Shutdown").
    """
    if "." not in dotted_path:
        raise ValueError(f"{label} path must be a dotted path like 'my_module.func', got: {dotted_path!r}")

    module_path, func_name = dotted_path.rsplit(".", 1)
    module = importlib.import_module(module_path)
    func = getattr(module, func_name, None)
    if func is None:
        raise AttributeError(f"Module {module_path!r} has no attribute {func_name!r}")
    if not callable(func):
        raise TypeError(f"{dotted_path!r} is not callable")

    return func
