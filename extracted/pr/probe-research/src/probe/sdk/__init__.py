"""Typed Probe SDK.

The SDK is the single implementation surface. The CLI, MCP read adapter, future
hooks, Python experiments, and passive platform integrations all build on it.

Exports load lazily (PEP 562 ``__getattr__``): naming a class here imports exactly
the one submodule that defines it, and nothing else. So ``import probe.foundation.durable.durable``
(or any other stdlib-only leaf) never drags in ``client`` -- and therefore never
drags in ``httpx`` -- which is what lets a distributed Miles actor spill metric
batches to disk without importing the network stack. Type checkers and IDEs still
see the real names through the ``TYPE_CHECKING`` block below.
"""

from __future__ import annotations

import importlib
from typing import TYPE_CHECKING

# Public name -> the submodule that defines it. Keep in step with ``__all__``.
_LAZY: dict[str, str] = {
    "Authorship": "client.client",
    "CaptureLedger": "capture.capture",
    "CaptureState": "capture.capture",
    "stable_external_key": "capture.capture",
    "stable_span_id": "capture.capture",
    "Aligned": "reads.compare",
    "Comparison": "reads.compare",
    "Client": "client.client",
    "DatasetRef": "catalog",
    "FROM_ENV": "client",
    # The views a coding agent pins, and the pin it gets back (pinned views T10).
    "ChartView": "client",
    "KeyMetricsView": "client",
    "PaneView": "client",
    "ParallelView": "client",
    "Pin": "client",
    "SourceRef": "catalog",
    "source": "catalog",
    "Rewind": "client.resources.runs.reopen.conflict",
    "Edit": "client",
    "CommandKind": "run.commands.commands",
    "Reader": "reads.reads",
    "Reference": "reads.reads",
    "Settings": "settings.settings",
    "resolve": "settings.settings",
    "EventsReadClient": "reads.events",
    "active_run": "fluent.fluent",
    "context": "fluent.fluent",
    "expect": "fluent.fluent",
    "finish": "fluent.fluent",
    "init": "fluent.fluent",
    "log": "fluent.fluent",
    "log_artifact": "fluent.fluent",
    "log_hw": "fluent.fluent",
    "span": "fluent.fluent",
    "update_config": "fluent.fluent",
    "Run": "run.run",
    "SpanHandle": "run.metrics.spans",
    "FailureContext": "run.context.context",
    "UnitContext": "run.context.context",
    "DeliveryIncomplete": "delivery.outbox.waiter",
}


def __getattr__(name: str) -> object:
    submodule = _LAZY.get(name)
    if submodule is None:
        raise AttributeError(f"module {__name__!r} has no attribute {name!r}")
    value = getattr(importlib.import_module(f".{submodule}", __name__), name)
    globals()[name] = value  # cache: the lazy import runs once per name
    return value


def __dir__() -> list[str]:
    return sorted(set(globals()) | set(_LAZY))


if TYPE_CHECKING:  # eager names for type checkers / IDEs; never executed at runtime
    from .reads.compare import Aligned, Comparison
    from .catalog.refs import DatasetRef, SourceRef
    from .catalog.catalog import source
    from .capture.capture import (
        CaptureLedger,
        CaptureState,
        stable_external_key,
        stable_span_id,
    )
    from .client.client import Authorship, Client
    from .client import Edit
    from .run.commands.commands import CommandKind
    from .client import FROM_ENV, ChartView, KeyMetricsView, PaneView, ParallelView, Pin
    from .settings.settings import Settings, resolve
    from .reads.events import EventsReadClient
    from .reads.reads import Reader, Reference
    from .fluent.fluent import (
        active_run,
        context,
        finish,
        init,
        log,
        log_artifact,
        log_hw,
        span,
        update_config,
    )
    from .run.run import Run
    from .run.metrics.spans import SpanHandle
    from .run.context.context import FailureContext, UnitContext
    from .delivery.outbox.waiter import DeliveryIncomplete


__all__ = [
    "Aligned",
    "Authorship",
    "ChartView",
    "DeliveryIncomplete",
    "CaptureLedger",
    "CaptureState",
    "Client",
    "Comparison",
    "DatasetRef",
    "EventsReadClient",
    "FROM_ENV",
    "FailureContext",
    "KeyMetricsView",
    "PaneView",
    "ParallelView",
    "Pin",
    "Reader",
    "Reference",
    "Rewind",
    "Edit",
    "CommandKind",
    "Run",
    "Settings",
    "SourceRef",
    "SpanHandle",
    "UnitContext",
    "active_run",
    "context",
    "expect",
    "finish",
    "init",
    "log",
    "log_artifact",
    "log_hw",
    "resolve",
    "source",
    "span",
    "stable_external_key",
    "stable_span_id",
    "update_config",
]
