"""Bounded weak-model adjudication for ambiguous intent decisions."""

from __future__ import annotations

from dataclasses import dataclass, replace
import re

from packages.contracts import ContextBundle, IntentDecision, IntentReason, ProfileState, SessionState
from packages.intent.policy import fallback_path as build_fallback_path, focus_seed_resume_shape

_ALLOWED_INTENTS = frozenset({"execution", "exploration", "creation", "reference", "profile", "resume"})
_INTENT_PATTERN = re.compile(r"intent\s*[:=]\s*([a-z-]+)", re.IGNORECASE)
_CONFIDENCE_PATTERN = re.compile(r"confidence\s*[:=]\s*([01](?:\.\d+)?)", re.IGNORECASE)
_REASON_PATTERN = re.compile(r"reason\s*[:=]\s*(.+)", re.IGNORECASE | re.DOTALL)


@dataclass(frozen=True, slots=True)
class _WeakAssistSignal:
    intent: str
    confidence: float
    reason: str


def maybe_apply_weak_intent_assist(
    *,
    decision: IntentDecision,
    prompt: str,
    profile: ProfileState,
    session: SessionState,
    model_provider: object,
) -> IntentDecision:
    if not decision.needs_weak_model_assist:
        return decision
    selection_getter = getattr(model_provider, "selection_state", None)
    if not callable(selection_getter):
        return _updated_decision(
            decision,
            prompt=prompt,
            outcome="unsupported",
            audit_line="stage4: weak assist unavailable because the model provider exposed no selection_state",
        )

    assist_context = ContextBundle(
        bundle_id=f"intent-weak-assist:{session.session_id}",
        session_id=session.session_id,
        instruction_refs=("intent.weak-assist",),
        token_budget=256,
    )
    try:
        response = model_provider.generate(
            profile=profile,
            session=session,
            context=assist_context,
            prompt=_weak_assist_prompt(prompt=prompt, decision=decision),
            model_role="weak",
        )
    except TypeError:
        return _updated_decision(
            decision,
            prompt=prompt,
            outcome="unsupported",
            audit_line="stage4: weak assist unavailable because the model provider rejected model_role=weak",
        )
    except Exception as error:
        return _updated_decision(
            decision,
            prompt=prompt,
            outcome="error",
            audit_line=f"stage4: weak assist errored with {error.__class__.__name__}",
        )

    signal = _parse_signal(response.summary)
    if signal is None:
        return _updated_decision(
            decision,
            prompt=prompt,
            outcome="unresolved",
            audit_line="stage4: weak assist returned an unparseable adjudication",
        )
    if signal.intent == decision.intent:
        return _updated_decision(
            decision,
            prompt=prompt,
            outcome="confirmed",
            audit_line=f"stage4: weak assist confirmed {signal.intent} ({signal.confidence:.2f})",
            signal=signal,
            apply_resolution=True,
        )
    if _should_adopt_signal(decision, signal):
        return _updated_decision(
            decision,
            prompt=prompt,
            outcome="suggested",
            audit_line=(
                f"stage4: weak assist suggested {signal.intent} ({signal.confidence:.2f}) "
                f"and runtime adopted it conservatively"
            ),
            signal=signal,
            apply_resolution=True,
        )
    return _updated_decision(
        decision,
        prompt=prompt,
        outcome="suggested",
        audit_line=(
            f"stage4: weak assist suggested {signal.intent} ({signal.confidence:.2f}) "
            f"but runtime kept {decision.intent} for now"
        ),
        signal=signal,
    )


def _updated_decision(
    decision: IntentDecision,
    *,
    prompt: str,
    outcome: str,
    audit_line: str,
    signal: _WeakAssistSignal | None = None,
    apply_resolution: bool = False,
) -> IntentDecision:
    reasons = decision.reasons
    next_intent = decision.intent
    next_confidence = decision.confidence
    next_scope = decision.scope_suggestion
    next_budget = decision.budget_class
    next_focus = decision.focus_activity_ids
    next_seed = decision.provisional_activity_seed
    next_resume_signal = decision.resume_signal
    if signal is not None:
        reasons = (
            *decision.reasons[:3],
            IntentReason(
                code=f"weak-assist.{outcome}",
                detail=signal.reason,
                weight=signal.confidence,
            ),
        )
        if apply_resolution:
            next_intent = signal.intent
            next_confidence = max(decision.confidence, signal.confidence)
            next_scope, next_budget, next_focus, next_seed, next_resume_signal = _resolved_shape(
                decision,
                prompt=prompt,
                intent=signal.intent,
            )
    return replace(
        decision,
        intent=next_intent,
        confidence=next_confidence,
        scope_suggestion=next_scope,
        budget_class=next_budget,
        focus_activity_ids=next_focus,
        provisional_activity_seed=next_seed,
        resume_signal=next_resume_signal,
        weak_assist_outcome=outcome,
        fallback_path=build_fallback_path(
            degradation_mode=decision.degradation_mode,
            needs_weak_model_assist=decision.needs_weak_model_assist,
            budget_class=next_budget,
            weak_assist_outcome=outcome,
        ),
        reasons=tuple(reasons),
        audit_trace=(*decision.audit_trace, audit_line),
    )


def _should_adopt_signal(decision: IntentDecision, signal: _WeakAssistSignal) -> bool:
    if signal.confidence < 0.75:
        return False
    if decision.intent == "reference" and signal.intent in {"execution", "creation", "exploration", "resume"}:
        return True
    if decision.intent == "execution" and signal.intent == "reference" and decision.confidence <= 0.5:
        return True
    return False


def _resolved_shape(
    decision: IntentDecision,
    *,
    prompt: str,
    intent: str,
) -> tuple[str, str, tuple[str, ...], str | None, str]:
    budget = "narrow"
    focus, seed, resume_signal = focus_seed_resume_shape(
        intent,
        prompt,
        heuristic_focus=decision.focus_activity_ids,
        candidate_scores=decision.candidate_scores,
    )
    if intent == "profile":
        return "profile", budget, (), None, "none"
    if intent == "reference":
        return "session", budget, (), None, "none"
    if intent == "resume":
        return decision.scope_suggestion, budget, focus, seed, resume_signal
    if intent == "execution":
        return "session", budget, focus, seed, resume_signal
    if intent in {"creation", "exploration"}:
        return "session", budget, (), decision.provisional_activity_seed, "none"
    return decision.scope_suggestion, decision.budget_class, decision.focus_activity_ids, decision.provisional_activity_seed, decision.resume_signal


def _weak_assist_prompt(*, prompt: str, decision: IntentDecision) -> str:
    candidate_summary = ", ".join(
        f"{score.kind}:{score.candidate_id}={score.total_score:.2f}"
        for score in decision.candidate_scores[:4]
    ) or "none"
    reasons = " | ".join(f"{reason.code}:{reason.detail}" for reason in decision.reasons[:3]) or "none"
    return (
        "Weak intent adjudication.\n"
        "Choose the best intent family for this turn.\n"
        "Reply with exactly three lines:\n"
        "intent=<execution|exploration|creation|reference|profile|resume>\n"
        "confidence=<0.00-1.00>\n"
        "reason=<short explanation>\n"
        f"prompt={prompt.strip()}\n"
        f"current_intent={decision.intent}\n"
        f"current_confidence={decision.confidence:.2f}\n"
        f"fallback_path={decision.fallback_path}\n"
        f"candidate_summary={candidate_summary}\n"
        f"reasons={reasons}\n"
    )


def _parse_signal(summary: str) -> _WeakAssistSignal | None:
    intent_match = _INTENT_PATTERN.search(summary or "")
    confidence_match = _CONFIDENCE_PATTERN.search(summary or "")
    if intent_match is None or confidence_match is None:
        return None
    intent = intent_match.group(1).strip().lower()
    if intent not in _ALLOWED_INTENTS:
        return None
    confidence = float(confidence_match.group(1))
    if not 0.0 <= confidence <= 1.0:
        return None
    reason_match = _REASON_PATTERN.search(summary or "")
    reason = (
        reason_match.group(1).strip().splitlines()[0][:180]
        if reason_match is not None and reason_match.group(1).strip()
        else "weak model returned a structured intent adjudication"
    )
    return _WeakAssistSignal(intent=intent, confidence=confidence, reason=reason)
