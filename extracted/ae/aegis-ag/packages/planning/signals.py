"""Prompt and event signal parsing for durable goal mutation."""

from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime
from uuid import uuid4

from packages.contracts import EventEnvelope

from .model import (
    GoalGraph,
    GoalGraphNode,
    GoalStatus,
    TimeSensitivity,
    _goal_similarity,
    _goal_title_from_text,
    _tokenize_goal_text,
)


@dataclass(frozen=True, slots=True)
class _PromptGoalSignal:
    source_text: str
    task_like: bool
    completion: bool
    deferred: bool
    blocked: bool
    focus: bool
    time_sensitivity: TimeSensitivity


_TASK_KEYWORDS: tuple[str, ...] = (
    "add",
    "adjust",
    "analyze",
    "audit",
    "build",
    "check",
    "create",
    "debug",
    "design",
    "document",
    "explore",
    "fix",
    "implement",
    "investigate",
    "plan",
    "refactor",
    "research",
    "review",
    "ship",
    "update",
    "看看",
    "分析",
    "修",
    "修复",
    "实现",
    "改",
    "排查",
    "整理",
    "检查",
    "补",
    "规划",
    "设计",
    "调研",
)

_COMPLETION_KEYWORDS: tuple[str, ...] = (
    "done",
    "complete",
    "completed",
    "finished",
    "resolved",
    "shipped",
    "closed",
    "完成",
    "搞定",
    "做完",
    "好了",
    "已完成",
)

_DEFER_KEYWORDS: tuple[str, ...] = (
    "defer",
    "later",
    "pause",
    "park",
    "hold off",
    "not now",
    "afterward",
    "later on",
    "之后",
    "后面",
    "稍后",
    "晚点",
    "先放一下",
    "先不做",
    "回头",
)

_BLOCKED_KEYWORDS: tuple[str, ...] = (
    "blocked",
    "stuck",
    "can't",
    "cannot",
    "unable",
    "waiting on",
    "need more information",
    "卡住",
    "受阻",
    "没法",
    "做不了",
    "缺信息",
    "没权限",
    "等一下",
)

_FOCUS_KEYWORDS: tuple[str, ...] = (
    "focus",
    "resume",
    "continue",
    "pick up",
    "come back to",
    "继续",
    "接着",
    "回到",
    "继续做",
    "先做",
)

def _contains_signal(text: str, signals: tuple[str, ...]) -> bool:
    lowered = text.lower()
    return any(signal in lowered for signal in signals)


def _time_sensitivity_from_text(text: str) -> TimeSensitivity:
    lowered = text.lower()
    if any(token in lowered for token in ("urgent", "asap", "immediately", "today", "now", "紧急", "尽快", "马上", "今天", "现在")):
        return "urgent"
    if any(token in lowered for token in ("soon", "this week", "tomorrow", "priority", "很快", "本周", "明天", "优先")):
        return "high"
    return "normal"


def _is_question_like(text: str) -> bool:
    stripped = text.strip().lower()
    if "?" in stripped or "？" in stripped:
        return True
    return stripped.startswith(
        (
            "what ",
            "why ",
            "how ",
            "when ",
            "where ",
            "which ",
            "can ",
            "could ",
            "should ",
            "would ",
            "do ",
            "does ",
            "is ",
            "are ",
            "what should",
            "怎么",
            "如何",
            "为什么",
            "什么",
            "要不要",
            "该不该",
        )
    )


def _analyze_goal_signal(text: str) -> _PromptGoalSignal:
    normalized = " ".join(text.strip().split())
    lowered = normalized.lower()
    task_like = _contains_signal(lowered, _TASK_KEYWORDS) or (
        len(_tokenize_goal_text(normalized)) >= 6 and not _is_question_like(normalized)
    )
    completion = _contains_signal(lowered, _COMPLETION_KEYWORDS)
    deferred = _contains_signal(lowered, _DEFER_KEYWORDS)
    blocked = _contains_signal(lowered, _BLOCKED_KEYWORDS)
    focus = _contains_signal(lowered, _FOCUS_KEYWORDS)
    return _PromptGoalSignal(
        source_text=normalized,
        task_like=task_like,
        completion=completion,
        deferred=deferred,
        blocked=blocked,
        focus=focus,
        time_sensitivity=_time_sensitivity_from_text(lowered),
    )


def _goal_seed_text(
    *,
    prompt: str,
    goal_query: str | None,
    event: EventEnvelope | None,
) -> str:
    """Return only explicit durable-goal input.

    Ordinary user prompt text is execution context. It must not be promoted into
    durable activity state unless the caller or model has routed it through an
    explicit goal field or activity tool.
    """
    del prompt
    for candidate in (
        goal_query,
        event.payload.get("goal_query") if event is not None else None,
    ):
        text = str(candidate or "").strip()
        if text:
            return text
    return ""


def _rank_goal_match(goal: GoalGraphNode, signal: _PromptGoalSignal, graph: GoalGraph) -> tuple[float, float]:
    similarity = _goal_similarity(signal.source_text, goal.title)
    continuity = 0.25 if goal.goal_id == graph.active_goal_id else 0.0
    return (similarity + continuity, similarity)


def _match_goal_for_signal(graph: GoalGraph, signal: _PromptGoalSignal) -> GoalGraphNode | None:
    active = graph.active_goal()
    if (signal.completion or signal.deferred or signal.blocked or signal.focus) and active is not None:
        return active
    candidates = [
        goal
        for goal in graph.nodes
        if goal.status not in {"completed", "done", "failed", "dropped"}
    ]
    if not candidates:
        return active
    ranked = sorted(
        candidates,
        key=lambda goal: _rank_goal_match(goal, signal, graph),
        reverse=True,
    )
    if not ranked:
        return active
    best = ranked[0]
    _, similarity = _rank_goal_match(best, signal, graph)
    if similarity >= 0.35:
        return best
    return active


def _status_for_signal(signal: _PromptGoalSignal, goal: GoalGraphNode | None) -> GoalStatus | None:
    if signal.completion:
        return "completed"
    if signal.blocked:
        return "blocked"
    if signal.deferred:
        return "deferred"
    if signal.focus:
        return "active"
    if goal is None and signal.task_like:
        return "active"
    return None


def _new_goal_node(
    *,
    graph: GoalGraph,
    session_id: str,
    signal: _PromptGoalSignal,
    updated_at: datetime,
    revision_id: str,
) -> GoalGraphNode:
    root_goal_id = graph.root_goal_id or graph.active_goal_id or (graph.nodes[0].goal_id if graph.nodes else None)
    return GoalGraphNode(
        goal_id=f"goal:{uuid4().hex[:12]}",
        session_id=session_id,
        title=_goal_title_from_text(signal.source_text),
        status="active",
        priority="high" if signal.time_sensitivity in {"high", "urgent"} else "medium",
        owner="shared",
        parent_goal_id=root_goal_id if root_goal_id is not None else None,
        time_sensitivity=signal.time_sensitivity,
        revision_id=revision_id,
        updated_at=updated_at,
    )
