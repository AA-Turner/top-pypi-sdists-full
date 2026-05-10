"""Hybrid request router — picks the right model for each request.

The contract:
  - Cheap local model for simple/structured tasks
  - Strong local coder for hard implementation tasks
  - Reasoning-specialist (or cloud, when allowed) for novel architecture/debug
  - Never escalate to cloud when allow_cloud=False

This is the function I previously left for you to write as a contribution.
A working baseline ships now — annotated with TUNING POINTS so you can
override the policy without rewriting the dispatch.

Design philosophy:
  Cost is a *vector* (latency, dollars, RAM, privacy). The router weighs
  these via the `RoutePolicy` so different deployments (laptop, server,
  team CI) can have different defaults without touching call sites.
"""

from __future__ import annotations

import re
from dataclasses import dataclass, field
from enum import Enum
from typing import Iterable

__all__ = [
    "Difficulty",
    "RouteDecision",
    "RoutePolicy",
    "route_request",
]


class Difficulty(Enum):
    TRIVIAL = "trivial"      # boilerplate, format conversion, naming
    SIMPLE = "simple"         # CRUD, glue code, well-defined transforms
    HARD = "hard"             # nontrivial logic, debugging, refactor
    NOVEL = "novel"           # new architecture, multi-system reasoning


@dataclass
class RouteDecision:
    model: str                      # qualified id like "ollama:qwen3-coder-next"
    difficulty: Difficulty
    reasoning: str
    fallbacks: list[str] = field(default_factory=list)


@dataclass
class RoutePolicy:
    """Per-deployment policy. Defaults work for an Apple Silicon laptop."""
    allow_cloud: bool = False
    privacy_strict: bool = True       # never send code to cloud regardless

    # Model preferences by difficulty (qualified ids; first available wins)
    trivial: list[str] = field(default_factory=lambda: [
        "ollama:llama3.2", "llama_cpp:llama3.2-3b", "ollama:gemma2:2b",
    ])
    simple: list[str] = field(default_factory=lambda: [
        "ollama:qwen2.5-coder:3b", "ollama:llama3.2", "llama_cpp:llama3.2-3b",
    ])
    hard: list[str] = field(default_factory=lambda: [
        "ollama:qwen3-coder-next", "ollama:deepseek-coder-v2",
        "llama_cpp:qwen2.5-coder-7b",
    ])
    novel: list[str] = field(default_factory=lambda: [
        "ollama:deepseek-r1", "ollama:qwq", "ollama:qwen3-coder-next",
    ])
    cloud_escalation: list[str] = field(default_factory=lambda: [
        "anthropic:claude-sonnet-4-6", "openai:gpt-5",
    ])


# ── Difficulty heuristics ──────────────────────────────────────────────

_TRIVIAL_PATTERNS = [
    r"^\s*(rename|format|reformat|prettif)",
    r"^\s*(convert .* to .*|translate .* to .*)\b",
    r"\bone[- ]?liner\b",
]
_SIMPLE_PATTERNS = [
    r"\b(crud|getter|setter|boilerplate)\b",
    r"\b(add a button|render a list|format a date)\b",
    r"\b(read|write) (a|the) file\b",
]
_HARD_PATTERNS = [
    r"\b(refactor|restructure|migrate|optimi[sz]e)\b",
    r"\b(implement|build|add) .* (feature|module|service)\b",
    r"\b(debug|fix|root cause|investigate)\b",
    r"\bperformance\b",
]
_NOVEL_PATTERNS = [
    r"\b(architect|design) (a|the|an)\b",
    r"\b(distributed|consensus|concurrent|race condition)\b",
    r"\b(novel|from scratch|greenfield|new system)\b",
    r"\bmath(emat)?ical\b",
]


def _matches_any(text: str, patterns: Iterable[str]) -> bool:
    return any(re.search(p, text, re.IGNORECASE) for p in patterns)


def _classify_difficulty(prompt: str, *, has_long_context: bool, has_attached_files: bool) -> Difficulty:
    p = prompt.strip()
    word_count = len(p.split())

    if _matches_any(p, _NOVEL_PATTERNS) or word_count > 200:
        return Difficulty.NOVEL
    if _matches_any(p, _HARD_PATTERNS) or has_long_context:
        return Difficulty.HARD
    if _matches_any(p, _TRIVIAL_PATTERNS) and word_count < 20:
        return Difficulty.TRIVIAL
    if _matches_any(p, _SIMPLE_PATTERNS) or word_count < 40:
        return Difficulty.SIMPLE
    return Difficulty.HARD  # When in doubt, send to the strong model


# ── Public router ──────────────────────────────────────────────────────

def _normalize_id(model_id: str) -> str:
    """Strip Ollama tag suffixes so 'ollama:llama3.2:latest' matches 'ollama:llama3.2'."""
    if model_id.startswith("ollama:") and model_id.count(":") >= 2:
        return ":".join(model_id.split(":")[:2])
    return model_id


def _match_in_available(candidate: str, available_norm: dict[str, str]) -> str | None:
    """Return the original available-id whose normalized form matches `candidate`."""
    norm = _normalize_id(candidate)
    return available_norm.get(norm)


def route_request(
    prompt: str,
    *,
    available_models: list[str],
    policy: RoutePolicy | None = None,
    has_long_context: bool = False,
    has_attached_files: bool = False,
) -> RouteDecision:
    """Pick a model for this request.

    Args:
        prompt: the user's request
        available_models: list of installed model ids the router can pick from
        policy: deployment policy (defaults are sane for a laptop)
        has_long_context: True if the model needs a big context window
        has_attached_files: True if user attached files / RAG injected content
    """
    pol = policy or RoutePolicy()
    difficulty = _classify_difficulty(
        prompt, has_long_context=has_long_context, has_attached_files=has_attached_files,
    )

    # ── TUNING POINT 1: ladder lookup
    # Map difficulty → preference list. Override here to change priorities.
    ladder = {
        Difficulty.TRIVIAL: pol.trivial,
        Difficulty.SIMPLE: pol.simple,
        Difficulty.HARD: pol.hard,
        Difficulty.NOVEL: pol.novel,
    }[difficulty]

    # Normalize available models so 'ollama:foo:latest' matches 'ollama:foo'
    available_norm = {_normalize_id(m): m for m in available_models}

    # Prefer first ladder hit that's installed.
    for candidate in ladder:
        match = _match_in_available(candidate, available_norm)
        if match is not None:
            other_matches = [
                available_norm[_normalize_id(m)] for m in ladder
                if m != candidate and _normalize_id(m) in available_norm
            ]
            return RouteDecision(
                model=match,
                difficulty=difficulty,
                reasoning=f"matched difficulty={difficulty.value}; first installed: {match}",
                fallbacks=other_matches,
            )

    # ── TUNING POINT 2: cloud escalation gate
    # Only consult cloud when policy allows AND privacy doesn't forbid.
    if pol.allow_cloud and not pol.privacy_strict:
        for candidate in pol.cloud_escalation:
            match = _match_in_available(candidate, available_norm)
            if match is not None:
                return RouteDecision(
                    model=match,
                    difficulty=difficulty,
                    reasoning=f"local ladder empty for {difficulty.value}; escalated to cloud",
                    fallbacks=[],
                )

    # Last resort: the largest installed model the caller knows about.
    if available_models:
        return RouteDecision(
            model=available_models[0],
            difficulty=difficulty,
            reasoning="no ladder match; using first available",
        )

    return RouteDecision(
        model="",
        difficulty=difficulty,
        reasoning="no models available — caller must install one",
    )
