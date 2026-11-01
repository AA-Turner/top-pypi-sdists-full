"""Minimal stand-ins for transformers, Lightning and Miles, installed only inside one test.

Only the names Probe's integrations import, with the same class names as the real ones.
"""

from __future__ import annotations

import contextlib
import functools
import importlib
import signal
import sys
import types
from argparse import Namespace
from collections.abc import Iterator
from typing import Any

#: The integration modules a fake framework lets import; dropped again afterwards.
INTEGRATIONS = ("probe.integrations.huggingface", "probe.integrations.lightning")


class TrainerCallback:
    """transformers.trainer_callback.TrainerCallback: every hook a no-op."""


class Logger:
    """lightning.pytorch.loggers.logger.Logger: the base ProbeLogger extends."""

    def __init__(self) -> None:
        pass


class DummyExperiment:
    """lightning's stand-in experiment on ranks that hold no run."""


def rank_zero_only(fn):
    @functools.wraps(fn)
    def wrapped(*args, **kwargs):
        return fn(*args, **kwargs) if rank_zero_only.rank == 0 else None

    return wrapped


rank_zero_only.rank = 0


def _convert_params(params: Any) -> dict:
    if params is None:
        return {}
    return dict(vars(params)) if isinstance(params, Namespace) else dict(params)


def _sanitize_callable_params(params: dict) -> dict:
    return {k: (getattr(v, "__name__", None) if callable(v) else v) for k, v in params.items()}


def _add_prefix(metrics: dict, prefix: str, separator: str) -> dict:
    return {f"{prefix}{separator}{k}": v for k, v in metrics.items()} if prefix else dict(metrics)


def _module(name: str, **attrs: Any) -> types.ModuleType:
    module = types.ModuleType(name)
    module.__dict__.update(attrs)
    return module


def _tree(leaves: dict[str, dict[str, Any]]) -> dict[str, types.ModuleType]:
    """Every package on the way to each leaf, linked parent -> child."""
    modules: dict[str, types.ModuleType] = {}
    for dotted, attrs in leaves.items():
        parts = dotted.split(".")
        for depth in range(1, len(parts) + 1):
            name = ".".join(parts[:depth])
            modules.setdefault(name, _module(name))
        modules[dotted].__dict__.update(attrs)
    for name, module in modules.items():
        if "." in name:
            parent, _, child = name.rpartition(".")
            setattr(modules[parent], child, module)
    return modules


def transformers_modules() -> dict[str, types.ModuleType]:
    return _tree(
        {
            "transformers.trainer_callback": {"TrainerCallback": TrainerCallback},
            "transformers.integrations.integration_utils": {"INTEGRATION_TO_CALLBACK": {}},
        }
    )


def lightning_modules() -> dict[str, types.ModuleType]:
    return _tree(
        {
            "lightning.fabric.utilities.logger": {
                "_add_prefix": _add_prefix,
                "_convert_params": _convert_params,
                "_sanitize_callable_params": _sanitize_callable_params,
            },
            "lightning.pytorch.loggers.logger": {"DummyExperiment": DummyExperiment, "Logger": Logger},
            "lightning.pytorch.utilities.rank_zero": {"rank_zero_only": rank_zero_only},
        }
    )


def miles_registry(monkeypatch) -> dict:
    """Stock miles' `BACKEND_REGISTRY`, as `probe.connectors.miles.register` finds it."""
    registry: dict = {}
    modules = _tree({"miles.utils.tracking_utils.base": {"BACKEND_REGISTRY": registry}})
    for name, module in modules.items():
        monkeypatch.setitem(sys.modules, name, module)
    return registry


@contextlib.contextmanager
def frameworks(monkeypatch) -> Iterator[dict[str, types.ModuleType]]:
    """Fake transformers + Lightning; yields the two integration modules imported over them."""
    for name, module in {**transformers_modules(), **lightning_modules()}.items():
        monkeypatch.setitem(sys.modules, name, module)
    handlers = {s: signal.getsignal(s) for s in (signal.SIGINT, signal.SIGTERM)}
    before = set(sys.modules)
    try:
        yield {name: importlib.import_module(name) for name in INTEGRATIONS}
    finally:
        # Never leave an integration bound to fake bases for a later test.
        for name in set(sys.modules) - before:
            if name.startswith(INTEGRATIONS):
                del sys.modules[name]
        package = sys.modules.get("probe.integrations")
        for name in INTEGRATIONS:
            if package is not None:
                package.__dict__.pop(name.rsplit(".", 1)[1], None)
        for signum, handler in handlers.items():
            signal.signal(signum, handler)
