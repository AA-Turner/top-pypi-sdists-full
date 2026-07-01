"""Live loop state registry.

Holds references to the active ``IterationBudget`` and
``ToolCallGuardrailController`` so the dashboard can introspect them. The
chat loop registers itself here on startup; if no loop is active we fall
back to default-configuration views.
"""
from __future__ import annotations

from dataclasses import dataclass, field
from threading import Lock
from typing import Any, Dict, List, Optional


@dataclass
class _LoopRegistry:
    budget: Optional[Any] = None
    guardrails: Optional[Any] = None
    compressor: Optional[Any] = None
    recorder: Optional[Any] = None
    last_turn: Dict[str, Any] = field(default_factory=dict)
    history: List[Dict[str, Any]] = field(default_factory=list)
    _lock: Lock = field(default_factory=Lock)


_REGISTRY = _LoopRegistry()


def register_loop(
    budget: Any | None = None,
    guardrails: Any | None = None,
    compressor: Any | None = None,
    recorder: Any | None = None,
) -> None:
    with _REGISTRY._lock:
        if budget is not None:
            _REGISTRY.budget = budget
        if guardrails is not None:
            _REGISTRY.guardrails = guardrails
        if compressor is not None:
            _REGISTRY.compressor = compressor
        if recorder is not None:
            _REGISTRY.recorder = recorder


def record_turn(turn: Dict[str, Any]) -> None:
    with _REGISTRY._lock:
        _REGISTRY.last_turn = dict(turn)
        _REGISTRY.history.append(dict(turn))
        if len(_REGISTRY.history) > 200:
            _REGISTRY.history = _REGISTRY.history[-200:]


def snapshot() -> Dict[str, Any]:
    with _REGISTRY._lock:
        budget = _REGISTRY.budget
        guard = _REGISTRY.guardrails
        comp = _REGISTRY.compressor
        rec = _REGISTRY.recorder
        last = dict(_REGISTRY.last_turn)
        history = list(_REGISTRY.history[-30:])

    budget_view: Dict[str, Any]
    if budget is not None:
        try:
            budget_view = {
                "active": True,
                "max": budget.max_iterations,
                "used": budget.used(),
                "remaining": budget.remaining(),
                "exhausted": budget.is_exhausted(),
            }
        except Exception:
            budget_view = {"active": False}
    else:
        from cvc.agent.loop.budget import IterationBudget

        budget_view = {
            "active": False,
            "max": IterationBudget.DEFAULT_PARENT_MAX,
            "used": 0,
            "remaining": IterationBudget.DEFAULT_PARENT_MAX,
            "exhausted": False,
        }

    guard_view: Dict[str, Any]
    if guard is not None:
        try:
            guard_view = {
                "active": True,
                "max_identical_per_turn": guard.max_identical_per_turn,
                "max_total_per_turn": guard.max_total_per_turn,
                "calls_this_turn": getattr(guard, "_total", 0),
            }
        except Exception:
            guard_view = {"active": False}
    else:
        guard_view = {
            "active": False,
            "max_identical_per_turn": 3,
            "max_total_per_turn": 50,
            "calls_this_turn": 0,
        }

    comp_view: Dict[str, Any] = {"active": comp is not None}
    if comp is not None:
        try:
            cfg = getattr(comp, "config", None)
            if cfg is not None:
                comp_view.update(
                    {
                        "trigger_tokens": getattr(cfg, "trigger_tokens", None),
                        "target_ratio": getattr(cfg, "target_ratio", None),
                        "keep_recent": getattr(cfg, "keep_recent", None),
                    }
                )
        except Exception:
            pass

    recorder_view = {
        "active": rec is not None,
        "path": str(getattr(rec, "path", "")) if rec is not None else None,
        "enabled": bool(getattr(rec, "enabled", False)) if rec is not None else False,
    }

    return {
        "budget": budget_view,
        "guardrails": guard_view,
        "compressor": comp_view,
        "recorder": recorder_view,
        "last_turn": last,
        "recent_turns": history,
    }
