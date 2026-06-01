"""
Generic resilience helpers for SDK-internal OTel instrumentation.

Import these instead of calling OTel primitives directly so that:
- A missing or broken OTel installation never raises in production code.
- An unreachable export endpoint is silently absorbed by the batch processor.
- Any unexpected OTel SDK error is swallowed with a debug log, not propagated.
"""

from __future__ import annotations

import logging
from contextlib import contextmanager, suppress
from typing import TYPE_CHECKING, Any

if TYPE_CHECKING:
    from collections.abc import Generator

_log = logging.getLogger("aigie.telemetry")


def _enter_span(tracer: Any, name: str) -> tuple[Any, Any]:
    """Try to enter a real OTel span; return (cm, span) or (None, NoOp) on failure."""
    from aigie.telemetry._noop import _NoOpSpan
    try:
        cm = tracer.start_as_current_span(name)
        return cm, cm.__enter__()
    except Exception:
        return None, _NoOpSpan()


def _exit_span(cm: Any, exc_info: tuple[Any, Any, Any] = (None, None, None)) -> None:
    """Exit a real span context manager, swallowing any OTel teardown error."""
    if cm is not None:
        with suppress(Exception):
            cm.__exit__(*exc_info)


@contextmanager
def safe_span(name: str, tracer: Any = None) -> Generator[Any, None, None]:
    """Start an OTel span; fall back to a NoOp span if OTel setup fails.

    User-code exceptions inside the ``with`` block always propagate unchanged.

    Args:
        name: The span name.
        tracer: Optional pre-fetched tracer. If omitted the module-level
                ``get_tracer`` singleton is used (appropriate for most call sites).
    """
    from aigie.telemetry import get_tracer
    _tracer = tracer if tracer is not None else get_tracer(name.split(".")[0])
    real_cm, span = _enter_span(_tracer, name)
    try:
        yield span
    except BaseException as exc:
        _exit_span(real_cm, (type(exc), exc, exc.__traceback__))
        raise
    else:
        _exit_span(real_cm)


def _metric_add(
    instrument_fn: Any,
    amount: int | float,
    attrs: dict[str, Any] | None = None,
) -> None:
    """Call ``instrument_fn().add(amount, attrs)``, swallowing any OTel error."""
    try:
        inst = instrument_fn()
        if attrs:
            inst.add(amount, attrs)
        else:
            inst.add(amount)
    except Exception as exc:
        _log.debug("telemetry metric add failed (non-fatal): %s", exc)


def _metric_record(
    instrument_fn: Any,
    value: float,
    attrs: dict[str, Any] | None = None,
) -> None:
    """Call ``instrument_fn().record(value, attrs)``, swallowing any OTel error."""
    try:
        inst = instrument_fn()
        if attrs:
            inst.record(value, attrs)
        else:
            inst.record(value)
    except Exception as exc:
        _log.debug("telemetry metric record failed (non-fatal): %s", exc)
