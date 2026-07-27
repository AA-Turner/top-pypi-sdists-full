"""Item #1 — Install self-test."""

from __future__ import annotations

from collections.abc import Callable
from dataclasses import dataclass

from sage.core.model_floor import check_capability
from sage.core.readiness import check_readiness

__all__ = ["SelftestResult", "run_selftest"]


@dataclass
class SelftestResult:
    ok: bool
    summary: str
    floor_passed: bool = False
    readiness_passed: bool = False


def run_selftest(*, model: str, send_fn: Callable[..., str]) -> SelftestResult:
    cap = check_capability(model, task_kind="agentic")
    if not cap.ok:
        return SelftestResult(
            ok=False,
            summary=f"{model}: capability floor failed — {cap.detail}\n{cap.suggestion}",
            floor_passed=False,
        )
    r = check_readiness(model=model, send_fn=send_fn)
    if not r.ok:
        return SelftestResult(
            ok=False,
            summary=f"{model}: readiness probe failed — {r.detail}",
            floor_passed=True,
            readiness_passed=False,
        )
    return SelftestResult(
        ok=True,
        summary=f"{model}: self-test passed",
        floor_passed=True,
        readiness_passed=True,
    )
