"""Item #12 — Quantization-on-pull."""

from __future__ import annotations

from pathlib import Path

__all__ = ["plan_quantizations", "should_requantize"]


_DESIRED_QUANTS = ("Q5_K_M", "Q8_0")


def plan_quantizations(gguf_path: Path, *, available_quants: list[str]) -> list[str]:
    available = set(available_quants)
    return [q for q in _DESIRED_QUANTS if q not in available]


def should_requantize(gguf_path: Path, *, available_quants: list[str]) -> bool:
    return bool(plan_quantizations(gguf_path, available_quants=available_quants))
