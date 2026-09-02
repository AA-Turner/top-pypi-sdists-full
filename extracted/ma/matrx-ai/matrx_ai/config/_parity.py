"""Dual-construction parity — the mechanism that makes the pydantic migration
non-breaking (agent-engine-extraction CUTOVER.md §3).

                 ┌─► OLD path ──► result A  ── authoritative, returned to the caller
one input ───────┤
                 └─► NEW path ──► result B  ── compared to A; divergence recorded, never raised

Four rules, and every one of them is load-bearing:

1. **The old path stays authoritative.** ``shadow_compare`` returns A. Always.
   B is discarded. Flipping authority is a separate, deliberate act.
2. **The new path can never break the request.** Everything after the old call
   is inside one try/except that records and swallows — the same contract
   ``providers/outbound_capture.py`` already holds ("Never breaks the call").
3. **Divergence is a durable record, not a log line.** It goes through the
   host-injected ``record_error`` seam with the input and a structured diff, so
   it lands where a human reviews it (`error-capture` skill's close-the-loop
   guarantee). With no host configured this is a silent no-op and matrx-ai
   stays standalone.
4. **Off by default.** ``PARITY_SHADOW_ENABLED`` gates the whole thing. The fast
   path when disabled is one module-global read.

🚨 RETIREMENT — this module is TEMPORARY.
   It is row 1 of the Retirement Ledger (CUTOVER.md §9, D13). Its deletion
   trigger: **the last shadowed type reaches S4.** matrx-runtime's parallel
   rollout worked and its cleanup never happened; this docstring exists so that
   cannot quietly repeat here. If you are reading this and every type is
   converted, DELETE THIS FILE — that is the whole job.
"""

from __future__ import annotations

import os
from collections.abc import Callable
from typing import Any, TypeVar

T = TypeVar("T")

# Gate. A knob rather than a deploy is the point (CUTOVER.md §3 rule 4); until
# the host wires a real feature knob, the env var is the flip.
PARITY_SHADOW_ENABLED = os.environ.get("MATRX_PARITY_SHADOW") == "1"

# Bounded so a pathological payload can never turn a divergence record into its
# own incident.
_MAX_DIFF_ENTRIES = 25
_MAX_VALUE_REPR = 500


def _short(value: Any) -> str:
    text = repr(value)
    return text if len(text) <= _MAX_VALUE_REPR else text[:_MAX_VALUE_REPR] + "…<truncated>"


def diff_fields(old: Any, new: Any, *, fields: tuple[str, ...]) -> list[dict[str, Any]]:
    """Field-by-field comparison of two objects. Compares TYPE as well as value.

    Type matters as much as value: pydantic's non-strict mode coerces ``"5"``
    into ``5`` and a downstream ``x == "5"`` then silently goes false. A
    value-only comparison would call that pair equal (CUTOVER.md §4 #1).
    """
    out: list[dict[str, Any]] = []
    for name in fields:
        a = getattr(old, name, _MISSING)
        b = getattr(new, name, _MISSING)
        if a is _MISSING and b is _MISSING:
            continue
        if a == b and type(a) is type(b):
            continue
        out.append(
            {
                "field": name,
                "old": _short(a),
                "new": _short(b),
                "old_type": type(a).__name__,
                "new_type": type(b).__name__,
                "reason": "type" if a == b else "value",
            }
        )
        if len(out) >= _MAX_DIFF_ENTRIES:
            out.append({"field": "…", "reason": "diff truncated"})
            break
    return out


class _Missing:
    def __repr__(self) -> str:  # pragma: no cover - trivial
        return "<absent>"


_MISSING = _Missing()


def record_divergence(shape: str, payload: Any, diffs: list[dict[str, Any]]) -> None:
    """Durably record one parity divergence. Never raises, never blocks."""
    try:
        from matrx_ai._ext import get_ext

        record_error = get_ext("record_error")
    except Exception:
        record_error = None
    if record_error is None:
        return
    try:
        import asyncio

        coro = record_error(
            RuntimeError(f"parity divergence on {shape}"),
            kind="pydantic_parity_divergence",
            error_type="matrx_ai.config._parity.ParityDivergence",
            error_text=f"{shape}: {len(diffs)} field(s) diverged between the dataclass and the pydantic model",
            route="pydantic_migration_shadow",
            payload={"shape": shape, "diffs": diffs, "input": _short(payload)},
        )
        if asyncio.iscoroutine(coro):
            try:
                asyncio.get_running_loop()
            except RuntimeError:
                coro.close()
                return
            from matrx_utils import detached_task

            detached_task(coro, name=f"pydantic_parity:{shape}")
    except Exception:
        # Recording a divergence must never become a second failure.
        pass


def shadow_compare(
    shape: str,
    payload: Any,
    build_old: Callable[[], T],
    build_new: Callable[[], Any],
    *,
    fields: tuple[str, ...],
) -> T:
    """Build both, compare, record any divergence, and return the OLD result.

    The old result is returned unconditionally — including when the new path
    raises. That is the whole guarantee: turning the shadow on cannot change
    what a caller receives.
    """
    old = build_old()
    if not PARITY_SHADOW_ENABLED:
        return old
    try:
        new = build_new()
        diffs = diff_fields(old, new, fields=fields)
        if diffs:
            record_divergence(shape, payload, diffs)
    except Exception as exc:
        record_divergence(
            shape,
            payload,
            [{"field": "<construction>", "reason": "new path raised", "new": _short(exc)}],
        )
    return old
