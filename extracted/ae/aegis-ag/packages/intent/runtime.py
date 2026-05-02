"""Hybrid intent resolution for Aegis.

INT-1 established the deterministic continuity-first fast path.
INT-2 extends the same resolver with embedding-backed candidate retrieval and
hybrid scoring for activities, guardians, and skills.
"""

from __future__ import annotations

from dataclasses import dataclass, field
import re
from typing import Protocol, runtime_checkable

from packages.contracts import (
    ActivityGraph,
    GoalNode,
    IntentCandidate,
    IntentCandidateScore,
    IntentDecision,
    IntentReason,
    IntentResolutionRequest,
)
from packages.embeddings import EmbeddingPreloadEntry, EmbeddingService, build_default_embedding_service, cosine_similarity

from .policy import (
    base_degradation_mode as _base_degradation_mode,
    budget_for as _budget_for,
    confidence_for as _confidence_for,
    fallback_path as _fallback_path,
    focus_seed_resume_shape as _focus_seed_resume_shape,
    has_continuation_cue as _has_continuation_cue,
    provisional_seed as _provisional_seed,
    scope_for as _scope_for,
    top_candidate as _top_candidate,
)

_INTENT_FAMILIES: tuple[str, ...] = (
    "execution",
    "exploration",
    "creation",
    "reference",
    "profile",
    "resume",
)

_CANDIDATE_ACTIVITY_TARGET = "intent-activities"
_CANDIDATE_GUARDIAN_TARGET = "intent-guardians"
_CANDIDATE_SKILL_TARGET = "intent-skills"

_PROFILE_MARKERS: tuple[str, ...] = (
    "profile",
    "persona",
    "identity",
    "voice",
    "tone",
    "preference",
    "preferences",
    "boundary",
    "boundaries",
    "clone",
    "user card",
    "画像",
    "人设",
    "身份",
    "声音",
    "语气",
    "偏好",
    "边界",
    "资料",
)

_REFERENCE_MARKERS: tuple[str, ...] = (
    "show",
    "list",
    "lookup",
    "inspect",
    "status",
    "explain",
    "summary",
    "summarize",
    "what",
    "why",
    "how",
    "where",
    "查看",
    "列出",
    "状态",
    "解释",
    "总结",
    "概况",
    "是什么",
    "为什么",
    "如何",
)

_EXPLORATION_MARKERS: tuple[str, ...] = (
    "research",
    "analyze",
    "analysis",
    "investigate",
    "compare",
    "comparison",
    "survey",
    "tradeoff",
    "approach",
    "approaches",
    "option",
    "options",
    "调研",
    "分析",
    "比较",
    "探索",
    "方案",
    "思路",
)

_CREATION_MARKERS: tuple[str, ...] = (
    "write",
    "draft",
    "compose",
    "create",
    "generate",
    "outline",
    "proposal",
    "readme",
    "report",
    "doc",
    "document",
    "draft a",
    "草稿",
    "写一份",
    "撰写",
    "生成",
    "文档",
    "计划",
    "方案文档",
)

_EXECUTION_MARKERS: tuple[str, ...] = (
    "fix",
    "implement",
    "update",
    "refactor",
    "add",
    "remove",
    "ship",
    "run",
    "test",
    "debug",
    "patch",
    "repair",
    "bug",
    "error",
    "traceback",
    "failing",
    "修复",
    "实现",
    "更新",
    "改",
    "重构",
    "新增",
    "删除",
    "运行",
    "测试",
    "排查",
    "报错",
    "异常",
)

_PROFILE_SURFACE_MARKERS = frozenset({"/profile", "profile", "identity", "persona"})
_INSPECT_SURFACE_MARKERS = frozenset({"/activity", "/memory", "/audit", "activity", "memory", "audit", "inspect"})
_CREATION_ARTIFACT_MARKERS: tuple[str, ...] = (".md", ".docx", ".pptx", ".pdf", "readme", "report", "draft")
_EXECUTION_ARTIFACT_MARKERS: tuple[str, ...] = (
    ".py",
    ".ts",
    ".tsx",
    ".js",
    ".sql",
    ".sh",
    "traceback",
    "stack trace",
    "failing test",
)

_TOKEN_PATTERN = re.compile(r"[a-z0-9_./-]+|[\u4e00-\u9fff]+")


@runtime_checkable
class IntentResolver(Protocol):
    """Resolve a revocable working intent hypothesis for one runtime step."""

    def resolve(self, request: IntentResolutionRequest) -> IntentDecision:
        """Return one intent decision for the current request."""


@dataclass(frozen=True, slots=True)
class HybridIntentResolver:
    """Cheap continuity-first resolver with shared embedding-backed candidate scoring."""

    ambiguity_margin: float = 0.35
    candidate_limit_per_kind: int = 2
    embedding_service: EmbeddingService = field(default_factory=build_default_embedding_service)

    def resolve(self, request: IntentResolutionRequest) -> IntentDecision:
        normalized_prompt = _normalize_text(request.prompt)
        surface_hints = tuple(_normalize_hint(hint) for hint in request.surface_hints if str(hint).strip())
        focus_activity_ids = _focus_activity_ids(request.activity_graph, request)
        continuity_mode = request.continuity.mode if request.continuity is not None else "foreground"
        audit_trace: list[str] = [
            f"stage0: continuity mode={continuity_mode}",
            f"stage0: surface hints={', '.join(surface_hints) if surface_hints else 'none'}",
        ]

        if self._should_inherit_previous(request, normalized_prompt, focus_activity_ids):
            reasons = [
                IntentReason(
                    code="continuity.inherit",
                    detail="explicit continuation cue kept the previous intent decision active",
                    weight=1.0,
                )
            ]
            if request.continuity is not None and request.continuity.active_goal_id is not None:
                reasons.append(
                    IntentReason(
                        code="continuity.active-goal",
                        detail=f"active activity {request.continuity.active_goal_id} remains in focus",
                        weight=0.8,
                    )
                )
            audit_trace.append("stage0: inherited previous intent from continuity carry-forward")
            return self._build_decision(
                request,
                intent=request.previous_decision.intent,
                confidence=max(request.previous_decision.confidence, 0.92),
                focus_activity_ids=focus_activity_ids or request.previous_decision.focus_activity_ids,
                provisional_activity_seed=request.previous_decision.provisional_activity_seed,
                resume_signal="inherit",
                scope_suggestion=request.previous_decision.scope_suggestion,
                budget_class=request.previous_decision.budget_class,
                reasons=reasons,
                candidate_scores=(),
                audit_trace=audit_trace,
            )

        if self._should_resume_from_continuity(normalized_prompt, request, focus_activity_ids):
            reasons = [
                IntentReason(
                    code="continuity.resume",
                    detail="explicit continuation or interruption cues mapped the turn to resume intent",
                    weight=1.0,
                )
            ]
            if request.continuity is not None and request.continuity.summary:
                reasons.append(
                    IntentReason(
                        code="continuity.summary",
                        detail=request.continuity.summary,
                        weight=0.7,
                    )
                )
            audit_trace.append("stage0: continuity and resume cues short-circuited to resume intent")
            return self._build_decision(
                request,
                intent="resume",
                confidence=0.94 if request.continuity is not None and request.continuity.requires_recovery else 0.88,
                focus_activity_ids=focus_activity_ids,
                provisional_activity_seed=_provisional_seed(request.prompt, focus_activity_ids=focus_activity_ids),
                resume_signal="resume" if request.continuity is not None and request.continuity.requires_recovery else "continue",
                scope_suggestion="lineage" if request.continuity is not None and request.continuity.requires_recovery else "session",
                budget_class="narrow",
                reasons=reasons,
                candidate_scores=(),
                audit_trace=audit_trace,
            )

        if any(hint in _PROFILE_SURFACE_MARKERS for hint in surface_hints):
            audit_trace.append("stage1: profile surface hint short-circuited to profile intent")
            return self._build_decision(
                request,
                intent="profile",
                confidence=0.96,
                focus_activity_ids=(),
                provisional_activity_seed=None,
                resume_signal="none",
                scope_suggestion="profile",
                budget_class="narrow",
                reasons=(
                    IntentReason(
                        code="surface.profile",
                        detail="operator surface already narrowed this turn to profile work",
                        weight=1.0,
                    ),
                ),
                candidate_scores=(),
                audit_trace=audit_trace,
            )

        if any(hint in _INSPECT_SURFACE_MARKERS for hint in surface_hints) and not _has_continuation_cue(normalized_prompt):
            audit_trace.append("stage1: inspect-oriented surface hint biased the turn toward reference intent")

        scores: dict[str, float] = {family: 0.0 for family in _INTENT_FAMILIES}
        reasons_by_intent: dict[str, list[IntentReason]] = {family: [] for family in _INTENT_FAMILIES}

        def add(intent: str, code: str, detail: str, weight: float) -> None:
            scores[intent] += weight
            reasons_by_intent[intent].append(IntentReason(code=code, detail=detail, weight=weight))

        if any(hint in _INSPECT_SURFACE_MARKERS for hint in surface_hints):
            add("reference", "surface.inspect", "inspect-style surface hints favor reference intent", 0.9)

        if request.continuity is not None and request.continuity.requires_recovery:
            add("resume", "continuity.requires-recovery", "continuity state still requires explicit recovery handling", 0.7)
        if focus_activity_ids and _is_short_follow_up(normalized_prompt):
            add("resume", "continuity.short-follow-up", "short follow-up with an active activity keeps continuity hot", 0.55)

        profile_hits = _count_matches(normalized_prompt, _PROFILE_MARKERS)
        if profile_hits:
            add("profile", "heuristic.profile", "profile or identity cues dominate the turn", min(1.4, 0.6 + (profile_hits * 0.35)))

        reference_hits = _count_matches(normalized_prompt, _REFERENCE_MARKERS)
        if reference_hits:
            add("reference", "heuristic.reference", "inspect, explain, or status cues match reference intent", min(1.4, 0.55 + (reference_hits * 0.3)))
        if _is_question_like(normalized_prompt):
            add("reference", "heuristic.question", "question form keeps the turn in a reference lane by default", 0.4)

        exploration_hits = _count_matches(normalized_prompt, _EXPLORATION_MARKERS)
        if exploration_hits:
            add("exploration", "heuristic.exploration", "research and comparison cues match exploration intent", min(1.6, 0.7 + (exploration_hits * 0.35)))

        creation_hits = _count_matches(normalized_prompt, _CREATION_MARKERS)
        if creation_hits:
            add("creation", "heuristic.creation", "drafting or authoring cues match creation intent", min(1.5, 0.65 + (creation_hits * 0.32)))

        execution_hits = _count_matches(normalized_prompt, _EXECUTION_MARKERS)
        if execution_hits:
            add("execution", "heuristic.execution", "implementation or repair cues match execution intent", min(1.6, 0.7 + (execution_hits * 0.3)))

        artifact_hint_text = " ".join((*request.artifact_hints, *request.recent_turn_summaries)).lower()
        if artifact_hint_text:
            if any(marker in artifact_hint_text for marker in _CREATION_ARTIFACT_MARKERS):
                add("creation", "artifact.creation", "artifact hints look like a document or authored deliverable", 0.45)
            if any(marker in artifact_hint_text for marker in _EXECUTION_ARTIFACT_MARKERS):
                add("execution", "artifact.execution", "artifact hints look like code or failure-oriented work", 0.45)

        if focus_activity_ids:
            add("execution", "activity.active", "an active activity keeps task execution plausible", 0.25)
            add("resume", "activity.active", "an active activity keeps continuity resume plausible", 0.25)

        candidate_scores = self._score_candidate_pools(
            request,
            normalized_prompt=normalized_prompt,
            surface_hints=surface_hints,
            audit_trace=audit_trace,
        )
        top_activity = _top_candidate(candidate_scores, kind="activity")
        top_guardian = _top_candidate(candidate_scores, kind="guardian")
        top_skill = _top_candidate(candidate_scores, kind="skill")

        if top_activity is not None:
            activity_status = top_activity.metadata.get("status", "")
            activity_title = top_activity.label
            add("execution", "candidate.activity", f"top activity candidate {activity_title} stayed relevant during hybrid scoring", min(0.7, 0.22 + top_activity.total_score))
            if activity_status in {"blocked", "paused"}:
                add("resume", "candidate.activity-recovery", f"top activity candidate {activity_title} still looks like interrupted work", min(0.75, 0.28 + top_activity.total_score))
            elif activity_status == "proposed":
                add("exploration", "candidate.activity-explore", f"top activity candidate {activity_title} is still exploratory", min(0.6, 0.16 + top_activity.total_score))
            elif activity_status == "done":
                add("reference", "candidate.activity-done", f"top activity candidate {activity_title} looks like finished state to inspect", min(0.45, 0.1 + top_activity.total_score))
            if creation_hits:
                add("creation", "candidate.activity-creation", f"top activity candidate {activity_title} stayed attached to authored output", min(0.45, 0.08 + top_activity.total_score))
            if _has_continuation_cue(normalized_prompt) or (request.continuity is not None and request.continuity.requires_recovery):
                add("resume", "candidate.activity-continuity", f"continuity cues and top activity candidate {activity_title} align", min(0.7, 0.2 + top_activity.total_score))

        if top_guardian is not None and _tool_policy_tags(request):
            add(
                "execution",
                "candidate.guardian",
                f"guardian candidate {top_guardian.label} fits the current tool or policy shape",
                min(0.45, 0.08 + top_guardian.total_score),
            )

        if top_skill is not None:
            skill_weight = min(0.4, 0.06 + top_skill.total_score)
            if execution_hits:
                add("execution", "candidate.skill", f"skill candidate {top_skill.label} matches the current implementation lane", skill_weight)
            elif creation_hits:
                add("creation", "candidate.skill", f"skill candidate {top_skill.label} matches the current authored output lane", skill_weight)
            elif exploration_hits:
                add("exploration", "candidate.skill", f"skill candidate {top_skill.label} matches the current exploratory lane", skill_weight)
            else:
                add("reference", "candidate.skill", f"skill candidate {top_skill.label} stayed relevant for this turn", min(0.28, skill_weight))

        ranked = sorted(_INTENT_FAMILIES, key=lambda name: (scores[name], name), reverse=True)
        best_intent = ranked[0]
        best_score = scores[best_intent]
        second_score = scores[ranked[1]] if len(ranked) > 1 else 0.0
        confidence = _confidence_for(best_score, second_score, candidate_scores=candidate_scores)
        ambiguity_detected = best_score <= 0.0 or (best_score - second_score) < self.ambiguity_margin

        if best_score <= 0.0:
            best_intent = "reference"
            confidence = 0.35
            reasons_by_intent[best_intent].append(
                IntentReason(
                    code="fallback.default-reference",
                    detail="no deterministic cue was strong enough, so the resolver stayed conservative",
                    weight=0.35,
                )
            )

        reasons = sorted(reasons_by_intent[best_intent], key=lambda item: item.weight, reverse=True)[:4]
        scope_suggestion = _scope_for(best_intent, request)
        budget_class = _budget_for(best_intent)
        final_focus, provisional_activity_seed, resume_signal = _focus_seed_resume_shape(
            best_intent,
            request.prompt,
            heuristic_focus=focus_activity_ids,
            candidate_scores=candidate_scores,
        )

        if ambiguity_detected:
            reasons = [
                *reasons,
                IntentReason(
                    code="ambiguity.margin",
                    detail="deterministic and hybrid scores were still too close for a fully confident decision",
                    weight=max(0.0, best_score - second_score),
                ),
            ][:4]
        if confidence < 0.6:
            scope_suggestion = "session" if scope_suggestion == "workspace" else scope_suggestion
            budget_class = "narrow"
            if best_intent not in {"resume", "execution"}:
                final_focus = ()
                provisional_activity_seed = None

        score_summary = ", ".join(f"{name}={scores[name]:.2f}" for name in ranked if scores[name] > 0.0) or "no-strong-signals"
        audit_trace.append(f"stage1: heuristic+hybrid scores -> {score_summary}")
        if candidate_scores:
            audit_trace.append(
                "stage2: top candidates -> "
                + ", ".join(
                    f"{match.kind}:{match.candidate_id}={match.total_score:.2f}"
                    for match in candidate_scores[: min(4, len(candidate_scores))]
                )
            )
        audit_trace.append(
            f"stage2: selected {best_intent} confidence={confidence:.2f} ambiguous={str(ambiguity_detected).lower()}"
        )
        return self._build_decision(
            request,
            intent=best_intent,
            confidence=confidence,
            focus_activity_ids=final_focus,
            provisional_activity_seed=provisional_activity_seed,
            resume_signal=resume_signal,
            scope_suggestion=scope_suggestion,
            budget_class=budget_class,
            reasons=reasons,
            candidate_scores=candidate_scores,
            audit_trace=audit_trace,
            needs_weak_model_assist=False,
        )

    def _score_candidate_pools(
        self,
        request: IntentResolutionRequest,
        *,
        normalized_prompt: str,
        surface_hints: tuple[str, ...],
        audit_trace: list[str],
    ) -> tuple[IntentCandidateScore, ...]:
        activity_candidates = request.activity_candidates or _activity_candidates_from_graph(request.activity_graph)
        pools = (
            ("activity", _CANDIDATE_ACTIVITY_TARGET, activity_candidates),
            ("guardian", _CANDIDATE_GUARDIAN_TARGET, request.guardian_candidates),
            ("skill", _CANDIDATE_SKILL_TARGET, request.skill_candidates),
        )
        query_tokens = _tokenize(normalized_prompt)
        query_vector: tuple[float, ...] = ()
        dimensions = 64
        if request.embedding_available:
            if _should_skip_query_embedding(
                normalized_prompt,
                surface_hints=surface_hints,
                request=request,
            ):
                audit_trace.append(
                    "stage2: skipped query embedding for an obvious control or short continuity turn; heuristics stay authoritative"
                )
            else:
                try:
                    query_embedding = self.embedding_service.embed_text(
                        request.prompt,
                        request_id=f"{request.session_id}:intent-query",
                        task="intent.resolve",
                        latency_mode="fast",
                    )
                    query_vector = query_embedding.values
                    dimensions = query_embedding.dimensions
                    audit_trace.append(
                        f"stage2: query embedding ready via fast {dimensions}d intent vector"
                    )
                except RuntimeError as error:
                    audit_trace.append(
                        f"stage2: query embedding degraded to heuristics-only because {error.__class__.__name__}: {str(error).strip()}"
                    )
        else:
            audit_trace.append("stage2: embeddings unavailable for this turn; candidate scoring stayed heuristic-first")
        scored: list[IntentCandidateScore] = []
        for kind, target, candidates in pools:
            if not candidates:
                continue
            if request.embedding_available:
                preload_state = self.embedding_service.queue_backfill(
                    target=target,
                    entries=tuple(_candidate_preload_entry(candidate) for candidate in candidates),
                    latency_mode="fast",
                )
                audit_trace.append(
                    f"stage2: queued {kind} candidates for {target} preload status={preload_state.status}"
                )
            scored.extend(
                self._score_candidate_pool(
                    request,
                    normalized_prompt=normalized_prompt,
                    query_tokens=query_tokens,
                    query_vector=query_vector,
                    dimensions=dimensions,
                    kind=kind,
                    target=target,
                    candidates=candidates,
                    surface_hints=surface_hints,
                )
            )
        scored.sort(key=lambda item: (-item.total_score, item.kind, item.candidate_id))
        return tuple(scored)

    def _score_candidate_pool(
        self,
        request: IntentResolutionRequest,
        *,
        normalized_prompt: str,
        query_tokens: set[str],
        query_vector: tuple[float, ...],
        dimensions: int,
        kind: str,
        target: str,
        candidates: tuple[IntentCandidate, ...],
        surface_hints: tuple[str, ...],
    ) -> tuple[IntentCandidateScore, ...]:
        scored: list[IntentCandidateScore] = []
        policy_tags = _tool_policy_tags(request)
        for candidate in candidates:
            reasons: list[IntentReason] = []
            heuristics_score = 0.0
            candidate_text = _candidate_search_text(candidate)
            overlap = sorted(query_tokens & _tokenize(candidate_text))
            if overlap:
                lexical_weight = 0.18 if kind == "activity" else 0.14
                overlap_score = min(0.8, float(len(overlap)) * lexical_weight)
                heuristics_score += overlap_score
                reasons.append(
                    IntentReason(
                        code=f"heuristic.{kind}.overlap",
                        detail=f"query overlap with candidate terms: {','.join(overlap)}",
                        weight=overlap_score,
                    )
                )

            if kind == "activity":
                candidate_status = candidate.metadata.get("status", "")
                if candidate_status == "active":
                    heuristics_score += 0.38
                    reasons.append(
                        IntentReason(
                            code="activity.status.active",
                            detail=f"{candidate.label} is still the active activity",
                            weight=0.38,
                        )
                    )
                elif candidate_status in {"blocked", "paused"}:
                    bonus = 0.46 if (request.continuity is not None and request.continuity.requires_recovery) else 0.24
                    heuristics_score += bonus
                    reasons.append(
                        IntentReason(
                            code="activity.status.recovery",
                            detail=f"{candidate.label} is still blocked or paused, so continuity remains relevant",
                            weight=bonus,
                        )
                    )
                elif candidate_status == "proposed":
                    heuristics_score += 0.16
                    reasons.append(
                        IntentReason(
                            code="activity.status.proposed",
                            detail=f"{candidate.label} is still a proposed activity and stays eligible for exploration",
                            weight=0.16,
                        )
                    )
                if request.continuity is not None and request.continuity.active_goal_id == candidate.candidate_id:
                    heuristics_score += 0.42
                    reasons.append(
                        IntentReason(
                            code="activity.continuity-focus",
                            detail=f"continuity already anchors the turn on {candidate.candidate_id}",
                            weight=0.42,
                        )
                    )
                if _has_continuation_cue(normalized_prompt) and request.continuity is not None and request.continuity.active_goal_id == candidate.candidate_id:
                    heuristics_score += 0.3
                    reasons.append(
                        IntentReason(
                            code="activity.continuation-cue",
                            detail="continuation cues and the carried activity point to the same candidate",
                            weight=0.3,
                        )
                    )
            elif kind == "guardian":
                guardian_overlap = tuple(tag for tag in policy_tags if tag in set(candidate.tags))
                if guardian_overlap:
                    tag_score = min(0.7, 0.22 * float(len(guardian_overlap)))
                    heuristics_score += tag_score
                    reasons.append(
                        IntentReason(
                            code="guardian.capability-fit",
                            detail=f"tool and policy hints map to guardian tags: {','.join(guardian_overlap)}",
                            weight=tag_score,
                        )
                    )
                if any(hint in candidate_text for hint in surface_hints):
                    heuristics_score += 0.12
                    reasons.append(
                        IntentReason(
                            code="guardian.surface-fit",
                            detail="surface hints stay aligned with this guardian bundle",
                            weight=0.12,
                        )
                    )
            elif kind == "skill":
                direct_hits = [
                    token
                    for token in (
                        candidate.candidate_id.lower(),
                        candidate.label.lower(),
                    )
                    if token and token in normalized_prompt
                ]
                if direct_hits:
                    direct_score = 0.55
                    heuristics_score += direct_score
                    reasons.append(
                        IntentReason(
                            code="skill.direct-hit",
                            detail=f"prompt directly referenced skill metadata: {', '.join(dict.fromkeys(direct_hits))}",
                            weight=direct_score,
                        )
                    )
                if candidate.metadata.get("include_in_overlay", "false") == "true":
                    heuristics_score += 0.1
                    reasons.append(
                        IntentReason(
                            code="skill.overlay",
                            detail=f"{candidate.label} is allowed to surface as procedural overlay",
                            weight=0.1,
                        )
                    )

            embedding_score = 0.0
            if query_vector:
                cached = self.embedding_service.cached_vector(
                    target=target,
                    cache_key=candidate.resolved_cache_key,
                    dimensions=dimensions,
                )
                if cached is not None:
                    similarity = max(0.0, cosine_similarity(query_vector, cached.values))
                    similarity_weight = 0.95 if kind == "activity" else 0.75
                    embedding_score = similarity * similarity_weight
                    if embedding_score > 0.0:
                        reasons.append(
                            IntentReason(
                                code=f"embedding.{kind}",
                                detail=f"semantic match via shared intent vector cache for {candidate.label}",
                                weight=embedding_score,
                            )
                        )
                else:
                    reasons.append(
                        IntentReason(
                            code=f"embedding.{kind}.cold-cache",
                            detail=f"candidate cache for {candidate.label} is still warming, so scoring stayed heuristic-first",
                            weight=0.0,
                        )
                    )

            total_score = heuristics_score + embedding_score
            if total_score <= 0.0:
                continue
            scored.append(
                IntentCandidateScore(
                    candidate_id=candidate.candidate_id,
                    kind=kind,
                    label=candidate.label,
                    total_score=total_score,
                    heuristics_score=heuristics_score,
                    embedding_score=embedding_score,
                    reasons=tuple(sorted(reasons, key=lambda item: item.weight, reverse=True)[:4]),
                    metadata=candidate.metadata,
                )
            )
        scored.sort(key=lambda item: (-item.total_score, item.candidate_id))
        return tuple(scored[: self.candidate_limit_per_kind])

    def _should_inherit_previous(
        self,
        request: IntentResolutionRequest,
        normalized_prompt: str,
        focus_activity_ids: tuple[str, ...],
    ) -> bool:
        return (
            request.previous_decision is not None
            and _has_continuation_cue(normalized_prompt)
            and bool(focus_activity_ids or request.previous_decision.focus_activity_ids)
        )

    def _should_resume_from_continuity(
        self,
        normalized_prompt: str,
        request: IntentResolutionRequest,
        focus_activity_ids: tuple[str, ...],
    ) -> bool:
        if _has_continuation_cue(normalized_prompt):
            return bool(focus_activity_ids or (request.continuity is not None and request.continuity.requires_recovery))
        return request.continuity is not None and request.continuity.requires_recovery and _is_short_follow_up(normalized_prompt)

    def _build_decision(
        self,
        request: IntentResolutionRequest,
        *,
        intent: str,
        confidence: float,
        focus_activity_ids: tuple[str, ...],
        provisional_activity_seed: str | None,
        resume_signal: str,
        scope_suggestion: str,
        budget_class: str,
        reasons: tuple[IntentReason, ...] | list[IntentReason],
        candidate_scores: tuple[IntentCandidateScore, ...] | list[IntentCandidateScore],
        audit_trace: tuple[str, ...] | list[str],
        needs_weak_model_assist: bool = False,
    ) -> IntentDecision:
        base_degradation = _base_degradation_mode(request)
        degradation_mode = base_degradation if base_degradation != "none" else (
            "conservative" if confidence < 0.6 or needs_weak_model_assist else "none"
        )
        fallback_path = _fallback_path(
            degradation_mode=degradation_mode,
            needs_weak_model_assist=needs_weak_model_assist,
            budget_class=budget_class,
        )
        final_audit_trace = (
            *tuple(audit_trace),
            f"stage3: fallback path -> {fallback_path}",
        )
        return IntentDecision(
            intent=intent,
            confidence=confidence,
            focus_activity_ids=focus_activity_ids,
            provisional_activity_seed=provisional_activity_seed,
            resume_signal=resume_signal,
            scope_suggestion=scope_suggestion,
            budget_class=budget_class,
            embedding_available=bool(request.embedding_available),
            degradation_mode=degradation_mode,
            needs_weak_model_assist=needs_weak_model_assist,
            fallback_path=fallback_path,
            reasons=tuple(reasons),
            candidate_scores=tuple(candidate_scores),
            audit_trace=final_audit_trace,
        )


def _normalize_text(value: str) -> str:
    return re.sub(r"\s+", " ", str(value or "").strip()).lower()


def _normalize_hint(value: str) -> str:
    normalized = _normalize_text(value)
    if not normalized:
        return ""
    if normalized.startswith("/"):
        return normalized.split()[0]
    return normalized


def _tokenize(text: str) -> set[str]:
    normalized = _normalize_text(text)
    if not normalized:
        return set()
    return {match.group(0) for match in _TOKEN_PATTERN.finditer(normalized)}


def _candidate_search_text(candidate: IntentCandidate) -> str:
    metadata_terms = " ".join(f"{key} {value}" for key, value in candidate.metadata.items() if str(value).strip())
    return " ".join(
        part
        for part in (
            candidate.label,
            candidate.summary,
            " ".join(candidate.tags),
            metadata_terms,
        )
        if part
    ).lower()


def _candidate_preload_entry(candidate: IntentCandidate) -> EmbeddingPreloadEntry:
    return EmbeddingPreloadEntry(
        cache_key=candidate.resolved_cache_key,
        text=_candidate_search_text(candidate),
        metadata={
            "candidate_id": candidate.candidate_id,
            "kind": candidate.kind,
            **{str(key): str(value) for key, value in candidate.metadata.items()},
        },
    )


def _contains_any(text: str, phrases: tuple[str, ...]) -> bool:
    return any(phrase in text for phrase in phrases)


def _count_matches(text: str, phrases: tuple[str, ...]) -> int:
    return sum(1 for phrase in phrases if phrase in text)


def _is_question_like(text: str) -> bool:
    if not text:
        return False
    if "?" in text or "？" in text:
        return True
    if any(marker in text for marker in ("为什么", "如何", "怎么", "what ", "why ", "how ", "where ")):
        return True
    return text.startswith(
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
            "is ",
            "are ",
            "怎么",
            "如何",
            "为什么",
            "什么",
            "是否",
            "要不要",
        )
    )


def _is_short_follow_up(text: str) -> bool:
    return bool(text) and len(text) <= 48 and len(text.split()) <= 10


def _should_skip_query_embedding(
    normalized_prompt: str,
    *,
    surface_hints: tuple[str, ...],
    request: IntentResolutionRequest,
) -> bool:
    if normalized_prompt.startswith("/"):
        return True
    if any(hint.startswith("/") for hint in surface_hints):
        return True
    if _is_short_follow_up(normalized_prompt):
        continuity = request.continuity
        if continuity is not None and (continuity.active_goal_id is not None or continuity.requires_recovery):
            return True
    return False


def _focus_activity_ids(activity_graph: ActivityGraph | None, request: IntentResolutionRequest) -> tuple[str, ...]:
    active_goal_id = activity_graph.active_goal_id if activity_graph is not None else None
    if active_goal_id is None and request.continuity is not None:
        active_goal_id = request.continuity.active_goal_id
    if active_goal_id is None:
        return ()
    return (active_goal_id,)


def _activity_candidates_from_graph(activity_graph: ActivityGraph | None) -> tuple[IntentCandidate, ...]:
    if activity_graph is None:
        return ()
    candidates: list[IntentCandidate] = []
    for goal in activity_graph.goals:
        if not isinstance(goal, GoalNode):
            continue
        candidates.append(_activity_candidate_from_goal(goal, active_goal_id=activity_graph.active_goal_id))
    return tuple(candidates)


def _activity_candidate_from_goal(goal: GoalNode, *, active_goal_id: str | None) -> IntentCandidate:
    status = goal.status.strip().lower() or "unknown"
    tags = [status, goal.priority.strip().lower() or "priority:unknown", "activity"]
    if goal.goal_id == active_goal_id:
        tags.append("active-focus")
    summary_bits = [
        goal.title,
        f"status={status}",
        f"priority={goal.priority}",
    ]
    if goal.dependency_refs:
        summary_bits.append("dependencies=" + ",".join(goal.dependency_refs[:3]))
    if goal.evidence_refs:
        summary_bits.append("evidence=" + ",".join(goal.evidence_refs[:3]))
    if goal.related_memory_ids:
        summary_bits.append("memory=" + ",".join(goal.related_memory_ids[:3]))
    return IntentCandidate(
        candidate_id=goal.goal_id,
        kind="activity",
        label=goal.title,
        summary="; ".join(summary_bits),
        cache_key=f"{goal.goal_id}:{status}:{goal.title.strip().lower()}",
        tags=tuple(dict.fromkeys(tag for tag in tags if str(tag).strip())),
        metadata={
            "status": status,
            "priority": goal.priority.strip().lower() or "unknown",
            "session_id": goal.session_id,
        },
    )


def _tool_policy_tags(request: IntentResolutionRequest) -> tuple[str, ...]:
    tags: list[str] = []
    for hint in request.capability_hints:
        normalized = str(hint).strip().lower()
        if not normalized.startswith("tool:"):
            continue
        tool_name = normalized.split(":", 1)[1]
        if any(token in tool_name for token in ("search", "web", "http", "fetch", "url", "browser", "network")):
            tags.extend(("network", "read"))
        if any(token in tool_name for token in ("write", "edit", "patch", "apply", "file")):
            tags.append("write")
        if any(token in tool_name for token in ("run", "exec", "command", "shell", "terminal", "deploy")):
            tags.append("exec")
        if any(token in tool_name for token in ("message", "mail", "wechat", "chat", "slack")):
            tags.append("messaging")
        if any(token in tool_name for token in ("voice", "audio", "mic", "record")):
            tags.append("voice_device")
    return tuple(dict.fromkeys(tags))
