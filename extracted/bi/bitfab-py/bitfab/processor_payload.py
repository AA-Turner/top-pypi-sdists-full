"""Shared payload finalization for the framework tracing processors.

The OpenAI-Agents, LangGraph, and Claude Agent SDK processors each build an
external span/trace payload that must be made JSON-safe before it is sent.

Doing that with a bare ``json.dumps`` drops the whole span/trace on a single
non-serializable value; doing it silently with ``to_json_safe`` hides a lossy
capture. These helpers do it in one place: sanitize via ``to_json_safe_report``
(so a model is dumped, not stubbed) and, when a value could only be captured as
a placeholder, mark the span (a ``serialization_degraded`` error) or warn for
the trace, so a degraded capture is surfaced as non-replayable instead of being
dropped or shipped silently. The HTTP boundary stays as the final net.
"""

from __future__ import annotations

import logging
from typing import Any

from bitfab.serialize import to_json_safe_report

SERIALIZATION_DEGRADED_STEP = "serialization_degraded"


def _rebuild_envelope(payload: Any, body_key: str, placeholder: Any) -> dict[str, Any]:
    """Rebuild a minimal payload envelope when ``to_json_safe_report`` collapsed
    the whole payload to a placeholder string (pathological: a top-level value
    that even the cycle-aware walker could not turn into a dict).

    Without this, ``finalize_*`` would call ``.get`` on a string and raise,
    aborting the send - the opposite of degrading gracefully. Carry the plain
    control fields through and tuck the placeholder under the body key so the
    span/trace still ships.
    """
    base = payload if isinstance(payload, dict) else {}
    rebuilt: dict[str, Any] = {
        k: base.get(k)
        for k in ("type", "source", "sourceTraceId", "completed")
        if k in base
    }
    rebuilt[body_key] = {"serialized": placeholder}
    return rebuilt


def _degraded_error(dropped: list[str]) -> dict[str, str]:
    return {
        "source": "sdk",
        "step": SERIALIZATION_DEGRADED_STEP,
        "error": (
            "non-replayable: could not faithfully capture "
            + ", ".join(sorted(set(dropped)))
        ),
    }


def finalize_span_payload(
    payload: dict[str, Any], extra_dropped: list[str] | None = None
) -> dict[str, Any]:
    """Return a JSON-safe span payload, marking a lossy capture on its errors.

    The span body is preserved (never gutted to id + trace_id). When a value
    could only be captured as a placeholder, a ``serialization_degraded`` error
    is appended so the lossy capture is recorded rather than shipped silently.

    ``extra_dropped`` carries losses detected by an earlier sanitization pass -
    e.g. input/output that a processor serialized at capture time to snapshot a
    mutable value. Without it, those fields reach this point as plain placeholder
    strings and their loss would go unreported.
    """
    safe, dropped = to_json_safe_report(payload)
    all_dropped = [*(extra_dropped or []), *dropped]
    if not isinstance(safe, dict):
        safe = _rebuild_envelope(payload, "rawSpan", safe)
        if not all_dropped:
            all_dropped = [type(payload).__qualname__]
    if all_dropped:
        errors = safe.get("errors")
        if not isinstance(errors, list):
            errors = []
            safe["errors"] = errors
        errors.append(_degraded_error(all_dropped))
    return safe


def finalize_trace_payload(
    payload: dict[str, Any], logger: logging.Logger
) -> dict[str, Any]:
    """Return a JSON-safe trace payload, warning when the capture was lossy.

    The trace is preserved (never dropped). A trace payload has no errors field,
    so a lossy capture is surfaced via ``logger`` instead.
    """
    safe, dropped = to_json_safe_report(payload)
    collapsed = not isinstance(safe, dict)
    if collapsed:
        safe = _rebuild_envelope(payload, "externalTrace", safe)
    if dropped or collapsed:
        external_trace = safe.get("externalTrace")
        trace_id = (
            external_trace.get("id", "unknown")
            if isinstance(external_trace, dict)
            else "unknown"
        )
        names = (
            ", ".join(sorted(set(dropped))) if dropped else type(payload).__qualname__
        )
        logger.warning(
            "Bitfab: trace %s held %d non-serializable value(s) (%s); they were "
            "captured as placeholders, so the trace may not be replayable.",
            trace_id,
            len(dropped) if dropped else 1,
            names,
        )
    return safe
