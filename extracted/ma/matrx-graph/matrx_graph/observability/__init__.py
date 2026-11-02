"""OpenTelemetry instrumentation for matrx-graph.

Tracing is opt-in BY INSTALLATION. If the ``opentelemetry-api`` package isn't
installed, every tracing call is a silent no-op — no runtime cost, no import
errors. There is deliberately no switch: presence of the dependency IS the
signal, and a host that does not want tracing does not install it or does not
configure an SDK.

(``MATRX_GRAPH_OTEL=0`` was removed 2026-08-25. It was an env TOGGLE — the
class Arman ruled out entirely: a switch in the environment lets local, server,
container and sandbox disagree about identical code. It was also redundant,
because the try/except below already no-ops without the package, and it was set
in no environment anywhere. See
``common-docs/policies/env-vars-are-values-not-toggles.md``.)

When OTel is available and an SDK has been configured by the host app,
the scheduler emits three nested spans per workflow run:

    span(workflow.run)                  run_id, definition_id, status
      span(workflow.super_step)         run_id, step, pending_count
        span(workflow.node)             node_id, spec_type, attempt,
                                        duration_ms, determinism, outcome

Attributes match the Pydantic event vocabulary so dashboards can join OTel
traces to wf_node_events rows by (run_id, step, node_id, attempt).

Usage from the scheduler::

    from matrx_graph.observability import tracer, span

    with span("workflow.run", run_id=run_id, ...):
        ...

Authors who want per-node attributes on an already-open span use
``set_attributes(**kv)``.
"""

from __future__ import annotations

from collections.abc import Iterator
from contextlib import contextmanager
from typing import Any

_TRACER: Any = None
_OTEL_ENABLED: bool = False


def _init() -> None:
    """Best-effort tracer initialization. Called lazily on first use."""
    global _TRACER, _OTEL_ENABLED

    try:
        from opentelemetry import trace
    except Exception:  # noqa: BLE001 — package may not be installed
        return

    _TRACER = trace.get_tracer("matrx_graph", "0.1.0")
    _OTEL_ENABLED = True


_init()


def is_enabled() -> bool:
    return _OTEL_ENABLED


@contextmanager
def span(name: str, /, **attributes: Any) -> Iterator[Any]:
    """Open an OTel span with the given name + attributes.

    No-op when OTel isn't available — yields ``None`` so callers can
    still use ``with span(...)`` unconditionally. When active, yields
    the underlying ``Span`` object so the caller can ``set_attribute``
    after creation (e.g. duration measured inside the block).
    """
    if not _OTEL_ENABLED or _TRACER is None:
        yield None
        return

    attr_items = {k: _coerce(v) for k, v in attributes.items() if v is not None}
    with _TRACER.start_as_current_span(name, attributes=attr_items) as sp:
        yield sp


def set_attributes(sp: Any, /, **attributes: Any) -> None:
    """Apply attributes to a span if OTel is active."""
    if sp is None:
        return
    for k, v in attributes.items():
        if v is None:
            continue
        try:
            sp.set_attribute(k, _coerce(v))
        except Exception:  # noqa: BLE001
            pass


def record_exception(sp: Any, exc: BaseException) -> None:
    if sp is None:
        return
    try:
        sp.record_exception(exc)
    except Exception:  # noqa: BLE001
        pass


def _coerce(value: Any) -> Any:
    """OTel attributes must be primitives. Coerce or stringify."""
    if isinstance(value, str | bool | int | float):
        return value
    if isinstance(value, list | tuple):
        return [_coerce(v) for v in value]
    return str(value)


__all__ = [
    "is_enabled",
    "record_exception",
    "set_attributes",
    "span",
]
