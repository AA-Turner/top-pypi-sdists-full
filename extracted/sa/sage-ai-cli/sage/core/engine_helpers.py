"""Engine-layer helpers that bind the new abstractions to runtime behavior.

This module is the seam between the engine (which orchestrates a turn)
and the various abstractions added earlier (structured tools, ReAct,
specialists). The engine imports from here rather than directly from
the abstraction modules — keeps the engine's surface area small and
makes each integration testable in isolation.
"""

from __future__ import annotations

from sage.core.react_loop import ReActConfig, bound_actions
from sage.core.specialists import (
    Specialist,
    default_specialists,
    delegate_to,
)
from sage.providers.base import ProviderBase

__all__ = [
    "should_use_structured_tools",
    "extract_and_bound",
    "handle_delegate_action",
    "find_specialist_by_domain",
    "is_small_model",
]


# ── Small-model detection (for auto-compression) ────────────────────────


# Lower-case substrings that indicate a small (< 8B-class) model. We
# compare against the model_id (with or without `<provider>:` prefix).
_SMALL_MODEL_HINTS = (
    "llama3.2",
    "llama-3.2",
    "qwen2.5-coder-3b",
    "qwen2.5-3b",
    "qwen-3b",
    "phi3-mini",
    "phi-3-mini",
    "phi4-mini",
    "phi-4-mini",
    "gemma2-2b",
    "gemma3-2b",
    "tinyllama",
    "smollm",
    "stablelm-3b",
    "starcoder2-3b",
    "haiku",  # claude haiku (small frontier model)
)


def is_small_model(model_id: str) -> bool:
    """Return True iff `model_id` names a small (<8B-class) model.

    Used by the engine to decide whether to auto-compress history before
    sending — large histories degrade small-model reasoning sharply.
    """
    if not model_id:
        return False
    s = model_id.lower()
    # Strip provider prefix if present
    if ":" in s:
        s = s.split(":", 1)[1]
    return any(hint in s for hint in _SMALL_MODEL_HINTS)


# ── B5: Structured tool routing ─────────────────────────────────────────


def should_use_structured_tools(provider: ProviderBase) -> bool:
    """Return True iff this provider declares structured-tool support.

    The engine calls this to decide whether to send a `tools=...`
    parameter (Gemini function_declarations, OpenAI tools array) or to
    fall back to the text-protocol READ:/SEARCH:/RUN:/FILE: extraction.
    """
    try:
        return bool(provider.supports_tools())
    except Exception:
        return False


# ── B6: ReAct loop helpers ──────────────────────────────────────────────


def extract_and_bound(
    response: str,
    cfg: ReActConfig,
) -> list[tuple[str, str]]:
    """Extract tool actions and apply ReAct gating in one call.

    Engine call site: `extract_and_bound(model_response, engine.react_cfg)`
    then iterate the returned actions. Legacy mode returns every action;
    ReAct mode returns only the first so the engine can observe before
    re-prompting.
    """
    # Local import keeps engine_helpers free of heavy deps when not needed.
    import re
    actions: list[tuple[str, str]] = []
    pattern = re.compile(
        r"^\s*(?:[-*]\s*)?(READ|SEARCH|RUN|FILE|DELEGATE_[A-Z]+):\s*(\S.*)$",
        re.MULTILINE,
    )
    for m in pattern.finditer(response or ""):
        actions.append((m.group(1).upper(), m.group(2).strip()))
    return bound_actions(actions, cfg)


# ── D12: Delegate action handler ────────────────────────────────────────


def find_specialist_by_domain(
    domain: str,
    registry: tuple[Specialist, ...] | None = None,
) -> Specialist | None:
    """Look up a specialist by domain name (case-insensitive)."""
    registry = registry or default_specialists()
    domain_lower = domain.lower()
    for s in registry:
        if s.domain.lower() == domain_lower:
            return s
    return None


def handle_delegate_action(
    action_name: str,
    task: str,
    router,
    registry: tuple[Specialist, ...] | None = None,
) -> str:
    """Route a DELEGATE_<DOMAIN> action to the matching specialist.

    `action_name`: e.g. "DELEGATE_FRONTEND"
    `task`: the task description the model emitted as the argument
    `router`: any router with a .generate(messages, model_id="auto", ...) method
    `registry`: optional override for default_specialists()

    Returns the specialist's response string. If the domain doesn't
    match any registered specialist, returns a short error string —
    the engine surfaces this as the action's output so the loop can
    continue rather than crashing.
    """
    if not action_name.startswith("DELEGATE_"):
        return f"error: not a delegate action: {action_name!r}"
    domain = action_name[len("DELEGATE_"):].lower()
    specialist = find_specialist_by_domain(domain, registry)
    if specialist is None:
        known = ", ".join(s.domain for s in (registry or default_specialists()))
        return (
            f"error: unknown specialist domain {domain!r}. "
            f"Known domains: {known}"
        )
    return delegate_to(specialist, task, router)
