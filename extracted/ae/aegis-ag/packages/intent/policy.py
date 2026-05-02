"""Pure policy helpers for intent scope, confidence, and fallback paths."""

from __future__ import annotations

from packages.contracts import IntentCandidateScore, IntentResolutionRequest

_CONTINUATION_EXACT_MARKERS = frozenset(
    {
        "continue",
        "resume",
        "keep going",
        "go on",
        "carry on",
        "pick up",
        "finish this",
        "finish it",
        "继续",
        "接着",
        "恢复",
    }
)
_CONTINUATION_INLINE_MARKERS: tuple[str, ...] = (
    "continue the same",
    "pick up from there",
    "按刚才",
    "按刚才那个",
    "沿着刚才",
    "继续做",
)


def scope_for(intent: str, request: IntentResolutionRequest) -> str:
    if intent == "profile":
        return "profile"
    if intent == "resume":
        return "lineage" if request.continuity is not None and request.continuity.requires_recovery else "session"
    if intent in {"exploration", "reference"} and request.workspace_id is not None:
        return "workspace"
    return "session"


def budget_for(intent: str) -> str:
    if intent == "exploration":
        return "broad"
    if intent in {"resume", "profile", "reference"}:
        return "narrow"
    return "standard"


def has_continuation_cue(text: str) -> bool:
    normalized = str(text or "").strip().lower()
    if normalized in _CONTINUATION_EXACT_MARKERS:
        return True
    return any(phrase in normalized for phrase in _CONTINUATION_INLINE_MARKERS)


def top_candidate(candidate_scores: tuple[IntentCandidateScore, ...], *, kind: str) -> IntentCandidateScore | None:
    for score in candidate_scores:
        if score.kind == kind:
            return score
    return None


def final_focus_activity_ids(
    intent: str,
    *,
    heuristic_focus: tuple[str, ...],
    candidate_scores: tuple[IntentCandidateScore, ...],
) -> tuple[str, ...]:
    if intent not in {"resume", "execution", "creation", "exploration"}:
        return ()
    top_activity = top_candidate(candidate_scores, kind="activity")
    if top_activity is not None:
        return (top_activity.candidate_id,)
    return heuristic_focus


def provisional_seed(prompt: str, *, focus_activity_ids: tuple[str, ...]) -> str | None:
    if focus_activity_ids:
        return None
    normalized = " ".join(str(prompt).strip().split())
    if len(normalized) < 8:
        return None
    return normalized[:96]


def focus_seed_resume_shape(
    intent: str,
    prompt: str,
    *,
    heuristic_focus: tuple[str, ...],
    candidate_scores: tuple[IntentCandidateScore, ...],
) -> tuple[tuple[str, ...], str | None, str]:
    focus_activity_ids = final_focus_activity_ids(
        intent,
        heuristic_focus=heuristic_focus,
        candidate_scores=candidate_scores,
    )
    provisional_activity_seed = provisional_seed(prompt, focus_activity_ids=focus_activity_ids)
    resume_signal = "continue" if has_continuation_cue(prompt) and focus_activity_ids else "none"
    return focus_activity_ids, provisional_activity_seed, resume_signal


def confidence_for(best_score: float, second_score: float, *, candidate_scores: tuple[IntentCandidateScore, ...]) -> float:
    margin = best_score - second_score
    best_candidate_score = candidate_scores[0].total_score if candidate_scores else 0.0
    best_strength = max(0.0, min(best_score / 2.0, 1.0))
    margin_strength = max(0.0, min(margin / 1.2, 1.0))
    candidate_strength = max(0.0, min(best_candidate_score / 1.1, 1.0))
    confidence = (
        0.32
        + (0.36 * best_strength)
        + (0.21 * margin_strength)
        + (0.08 * candidate_strength)
    )
    return round(min(0.98, confidence), 2)


def base_degradation_mode(request: IntentResolutionRequest) -> str:
    if request.mixture is not None and request.mixture.intent_mode == "skip":
        return "skip"
    if request.mixture is not None and request.mixture.intent_mode == "embedded" and not request.embedding_available:
        return "embedding-unavailable"
    return "none"


def fallback_path(
    *,
    degradation_mode: str,
    needs_weak_model_assist: bool,
    budget_class: str,
    weak_assist_outcome: str = "not-requested",
) -> str:
    components: list[str] = []
    if degradation_mode != "none":
        components.append(degradation_mode)
        if degradation_mode in {"skip", "embedding-unavailable"} and not needs_weak_model_assist:
            components.append("heuristics-only")
    if needs_weak_model_assist:
        components.append("weak-assist")
        if weak_assist_outcome != "not-requested":
            components.append(weak_assist_outcome)
    if budget_class == "narrow" and components:
        components.append("narrow")
    return ".".join(components) if components else "direct"
