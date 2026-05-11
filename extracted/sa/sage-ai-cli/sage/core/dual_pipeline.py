"""T11 — Two-model pipeline as default for `sage run`.

Picks a (planner, coder) pair from the available installed models. The
planner should be cheap+fast (handles task decomposition); the coder
strong (writes the actual code). When only one model is available, both
roles fall back to the same model.

Returns model identifiers ready to pass to `core/agent_pipeline.AgentPipeline`.
"""

from __future__ import annotations

from sage.core.model_floor import estimate_params_b

__all__ = ["resolve_planner_coder", "is_coder_model"]


_CODER_HINTS = ("coder", "code", "deepseek-coder", "starcoder", "codellama",
                "devstral", "codestral", "phind-codellama")


def is_coder_model(model_id: str) -> bool:
    name = model_id.lower()
    return any(hint in name for hint in _CODER_HINTS)


def resolve_planner_coder(available: list[str]) -> tuple[str, str]:
    """Pick (planner, coder) from a list of qualified model ids.

    Strategy:
      - Coder = strongest installed coding-specialist. If none, strongest model.
      - Planner = smallest model that's still ≥3B (fast but not too tiny).
                   If only one model exists, planner = coder.
      - If empty list, return ("", "").
    """
    if not available:
        return ("", "")
    if len(available) == 1:
        return (available[0], available[0])

    # Score each available model
    scored: list[tuple[str, float, bool]] = []
    for m in available:
        params = estimate_params_b(m) or 0.0
        scored.append((m, params, is_coder_model(m)))

    # Coder: prefer coder-specialist; tiebreak by params descending
    coders = [(m, p) for m, p, c in scored if c]
    if coders:
        coder = max(coders, key=lambda t: t[1])[0]
    else:
        coder = max(scored, key=lambda t: t[1])[0]

    # Planner: smallest model not the coder, with params ≥ 1B
    planner_pool = [(m, p) for m, p, _ in scored if m != coder and p >= 1.0]
    if planner_pool:
        planner = min(planner_pool, key=lambda t: t[1])[0]
    else:
        # Fall back to any non-coder model, then to coder
        non_coder = [m for m, _, _ in scored if m != coder]
        planner = non_coder[0] if non_coder else coder

    return (planner, coder)
