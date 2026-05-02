"""Profile growth scoring and progression helpers."""

from __future__ import annotations

from collections.abc import Iterable
from dataclasses import dataclass
from datetime import date, datetime, timedelta, timezone
import math

from packages.contracts.runtime import ExperienceRecord, ProfileGrowthState

MAX_GROWTH_LEVEL = 40

_GOOD_EXECUTION_OUTCOMES = frozenset({"delivered", "observed", "ok", "ready", "success"})
_RECOVERY_RESUME_SIGNALS = frozenset({"continue", "inherit", "interrupted", "resume"})
_GOAL_PRIORITY_POINTS = {
    "low": 1,
    "medium": 2,
    "high": 3,
    "critical": 4,
}
_GOAL_STATUS_POINTS = {
    "proposed": 1,
    "queued": 2,
    "active": 3,
    "blocked": 2,
    "deferred": 1,
}
_PROGRESSION_ACTION_POINTS = {
    "advance": 4,
    "replan": 3,
    "defer": 1,
}
_PROMOTED_PROCEDURE_STATUSES = frozenset({"active", "promoted", "verified"})
_ROMAN_NUMERALS = (
    (1000, "M"),
    (900, "CM"),
    (500, "D"),
    (400, "CD"),
    (100, "C"),
    (90, "XC"),
    (50, "L"),
    (40, "XL"),
    (10, "X"),
    (9, "IX"),
    (5, "V"),
    (4, "IV"),
    (1, "I"),
)


@dataclass(frozen=True, slots=True)
class GrowthStageDescriptor:
    stage_id: str
    display_name: str
    title: str
    logo_asset: str
    min_level: int
    max_level: int


@dataclass(frozen=True, slots=True)
class GrowthRewardReason:
    reason_id: str
    label: str
    summary: str
    score: int
    evidence_refs: tuple[str, ...] = ()
    facts: tuple[str, ...] = ()
    bounded: bool = False


@dataclass(frozen=True, slots=True)
class GrowthTurnSignals:
    session_id: str
    profile_id: str
    total_tokens: int
    captured_experiences: int = 0
    promoted_experiences: int = 0
    continuity_bonus: bool = False
    occurred_at: datetime | None = None
    goal_id: str | None = None
    goal_status: str | None = None
    goal_priority: str | None = None
    progression_action: str = ""
    resume_signal: str = "none"
    continuity_mode: str = "foreground"
    execution_outcome: str = ""
    experience_status: str | None = None
    active_goal_present: bool = False
    plan_step_count: int = 0
    goal_dependency_count: int = 0
    memory_count: int = 0
    context_goal_count: int = 0
    tool_call_count: int = 0
    model_turn_count: int = 0
    blocked_goal_count: int = 0
    goal_evidence_refs: tuple[str, ...] = ()
    replay_evidence_refs: tuple[str, ...] = ()
    skill_ids: tuple[str, ...] = ()
    artifact_ids: tuple[str, ...] = ()
    promoted_procedure_ids: tuple[str, ...] = ()
    elapsed_since_last_turn_seconds: int | None = None


@dataclass(frozen=True, slots=True)
class GrowthSnapshot:
    state: ProfileGrowthState
    level: int
    stage: GrowthStageDescriptor
    level_floor_score: int
    next_level_score: int | None
    score_into_level: int
    score_to_next_level: int
    progress_ratio: float
    progress_percent: int
    lifetime_days: int


@dataclass(frozen=True, slots=True)
class GrowthUpdate:
    before: GrowthSnapshot
    after: GrowthSnapshot
    delta_score: int
    awarded_for: tuple[str, ...]
    reward_reasons: tuple[GrowthRewardReason, ...] = ()

    @property
    def leveled_up(self) -> bool:
        return self.after.level > self.before.level

    @property
    def stage_changed(self) -> bool:
        return self.after.stage.stage_id != self.before.stage.stage_id


GROWTH_STAGES = (
    GrowthStageDescriptor(
        stage_id="seed",
        display_name="Seed",
        title="Seed",
        logo_asset="evolution-stage-1",
        min_level=0,
        max_level=9,
    ),
    GrowthStageDescriptor(
        stage_id="hatchling",
        display_name="Hatchling",
        title="Hatchling",
        logo_asset="evolution-stage-2",
        min_level=10,
        max_level=19,
    ),
    GrowthStageDescriptor(
        stage_id="scout",
        display_name="Scout",
        title="Scout",
        logo_asset="evolution-stage-3",
        min_level=20,
        max_level=29,
    ),
    GrowthStageDescriptor(
        stage_id="guardian",
        display_name="Guardian",
        title="Guardian",
        logo_asset="aegis-logo",
        min_level=30,
        max_level=MAX_GROWTH_LEVEL,
    ),
)

_STAGE_BONUS = {
    "seed": 0,
    "hatchling": 60,
    "scout": 180,
    "guardian": 500,
}


def _utc_now() -> datetime:
    return datetime.now(timezone.utc)


def _local_day(moment: datetime) -> date:
    return moment.astimezone().date()


def _dedupe_text(values: Iterable[str]) -> tuple[str, ...]:
    ordered: list[str] = []
    seen: set[str] = set()
    for value in values:
        text = str(value).strip()
        if not text or text in seen:
            continue
        seen.add(text)
        ordered.append(text)
    return tuple(ordered)


def _contains_any(text: str, needles: tuple[str, ...]) -> bool:
    lowered = " ".join(str(text).split()).lower()
    return any(needle in lowered for needle in needles)


def _round_to_five(value: int) -> int:
    return int(round(max(0, value) / 5.0) * 5)


def _roman_numeral(value: int) -> str:
    remaining = max(1, int(value))
    rendered: list[str] = []
    for amount, token in _ROMAN_NUMERALS:
        while remaining >= amount:
            rendered.append(token)
            remaining -= amount
    return "".join(rendered)


def _curve_stage_id_for_level(level: int) -> str:
    normalized = max(0, level)
    if normalized < 10:
        return "seed"
    if normalized < 20:
        return "hatchling"
    if normalized < 30:
        return "scout"
    return "guardian"


def _brand_stage_id_for_level(level: int) -> str:
    return _curve_stage_id_for_level(level)


def unbounded_xp_to_next_level(level: int) -> int:
    curve_stage_id = _curve_stage_id_for_level(level)
    required = 100 + (6 * max(0, level)) + (1.4 * (max(0, level) ** 2)) + _STAGE_BONUS[curve_stage_id]
    return int(round(required / 5.0) * 5)


def unbounded_level_floor_score(level: int) -> int:
    score = 0
    for current in range(max(0, level)):
        score += unbounded_xp_to_next_level(current)
    return score


def unbounded_level_for_score(score: int) -> int:
    if score <= 0:
        return 0
    level = 0
    remaining = score
    while True:
        required = unbounded_xp_to_next_level(level)
        if remaining < required:
            return level
        remaining -= required
        level += 1


def _canonical_active_days(experiences: tuple[ExperienceRecord, ...]) -> int:
    days = {
        _local_day(moment)
        for experience in experiences
        for moment in (experience.updated_at or experience.created_at,)
        if moment is not None
    }
    return len(days)


def _reward_reason(
    reason_id: str,
    label: str,
    summary: str,
    score: int,
    *,
    evidence_refs: tuple[str, ...] = (),
    facts: tuple[str, ...] = (),
    bounded: bool = False,
) -> GrowthRewardReason | None:
    if score <= 0:
        return None
    return GrowthRewardReason(
        reason_id=reason_id,
        label=label,
        summary=summary,
        score=score,
        evidence_refs=_dedupe_text(evidence_refs),
        facts=_dedupe_text(facts),
        bounded=bounded,
    )


def _awarded_for_token(reason: GrowthRewardReason) -> str:
    return f"{reason.reason_id}:{reason.score}"


def default_growth_state(profile_id: str, *, now: datetime | None = None) -> ProfileGrowthState:
    timestamp = now or _utc_now()
    return ProfileGrowthState(
        profile_id=profile_id,
        created_at=timestamp,
        updated_at=timestamp,
    )


def stage_for_level(level: int) -> GrowthStageDescriptor:
    for stage in GROWTH_STAGES:
        if stage.min_level <= level <= stage.max_level:
            return stage
    return GROWTH_STAGES[-1]


def xp_to_next_level(level: int) -> int:
    if level >= MAX_GROWTH_LEVEL:
        return 0
    stage = stage_for_level(level)
    required = 100 + (6 * level) + (1.4 * (level**2)) + _STAGE_BONUS[stage.stage_id]
    return int(round(required / 5.0) * 5)


def level_floor_score(level: int) -> int:
    capped = min(max(level, 0), MAX_GROWTH_LEVEL)
    score = 0
    for current in range(capped):
        score += xp_to_next_level(current)
    return score


def level_for_score(score: int) -> int:
    if score <= 0:
        return 0
    level = 0
    remaining = score
    while level < MAX_GROWTH_LEVEL:
        required = xp_to_next_level(level)
        if remaining < required:
            return level
        remaining -= required
        level += 1
    return MAX_GROWTH_LEVEL


def build_growth_snapshot(state: ProfileGrowthState) -> GrowthSnapshot:
    level = level_for_score(state.growth_score)
    stage = stage_for_level(level)
    floor_score = level_floor_score(level)
    next_cost = xp_to_next_level(level) if level < MAX_GROWTH_LEVEL else 0
    next_level_score = floor_score + next_cost if next_cost else None
    score_into_level = max(0, state.growth_score - floor_score)
    progress_ratio = 1.0 if next_cost == 0 else min(1.0, score_into_level / next_cost)
    progress_percent = int(round(progress_ratio * 100))
    lifetime_days = 0
    if state.first_dialogue_at is not None and state.last_dialogue_at is not None:
        lifetime_days = max(1, (_local_day(state.last_dialogue_at) - _local_day(state.first_dialogue_at)).days + 1)
    return GrowthSnapshot(
        state=state,
        level=level,
        stage=stage,
        level_floor_score=floor_score,
        next_level_score=next_level_score,
        score_into_level=score_into_level,
        score_to_next_level=0 if next_cost == 0 else max(0, next_cost - score_into_level),
        progress_ratio=progress_ratio,
        progress_percent=progress_percent,
        lifetime_days=lifetime_days,
    )


def apply_turn_growth(
    state: ProfileGrowthState | None,
    signals: GrowthTurnSignals,
) -> GrowthUpdate:
    timestamp = signals.occurred_at or _utc_now()
    current = state or default_growth_state(signals.profile_id, now=timestamp)
    before = build_growth_snapshot(current)
    delta_score, reward_reasons, active_days_delta, next_streak = _score_turn_delta(
        current,
        signals,
        timestamp=timestamp,
    )
    total_experiences = current.total_experiences + max(0, signals.captured_experiences)
    promoted_experiences = current.promoted_experiences + max(0, signals.promoted_experiences)
    current_local_day = _local_day(timestamp).isoformat()
    next_state = ProfileGrowthState(
        profile_id=current.profile_id,
        growth_score=current.growth_score + delta_score,
        total_dialogues=current.total_dialogues + 1,
        total_tokens=current.total_tokens + max(0, signals.total_tokens),
        total_experiences=total_experiences,
        promoted_experiences=promoted_experiences,
        active_days=current.active_days + active_days_delta,
        streak_days=next_streak,
        first_dialogue_at=current.first_dialogue_at or timestamp,
        last_dialogue_at=timestamp,
        last_active_day=current_local_day,
        created_at=current.created_at or timestamp,
        updated_at=timestamp,
    )
    after = build_growth_snapshot(next_state)
    return GrowthUpdate(
        before=before,
        after=after,
        delta_score=delta_score,
        awarded_for=tuple(_awarded_for_token(reason) for reason in reward_reasons),
        reward_reasons=tuple(reward_reasons),
    )


def _score_turn_delta(
    state: ProfileGrowthState,
    signals: GrowthTurnSignals,
    *,
    timestamp: datetime,
) -> tuple[int, list[GrowthRewardReason], int, int]:
    last_active_day = date.fromisoformat(state.last_active_day) if state.last_active_day else None
    current_day = _local_day(timestamp)
    active_days_delta = 0
    streak_days = state.streak_days

    if last_active_day is None:
        active_days_delta = 1
        streak_days = 1
    elif current_day > last_active_day:
        active_days_delta = 1
        streak_days = state.streak_days + 1 if current_day == last_active_day + timedelta(days=1) else 1

    if state.total_dialogues == 0:
        bootstrap = _reward_reason(
            "first-turn-boost",
            "First Turn Boost",
            "The first durable turn gets a fixed onboarding reward.",
            40,
            facts=(f"session={signals.session_id}",),
        )
        assert bootstrap is not None
        return 40, [bootstrap], active_days_delta or 1, max(streak_days, 1)

    if state.total_dialogues == 1 and state.growth_score < xp_to_next_level(0):
        required = xp_to_next_level(0) - state.growth_score
        promotion = _reward_reason(
            "second-turn-promotion",
            "Second Turn Promotion",
            "The second durable turn guarantees level-one progression.",
            required,
            facts=(f"target-score={xp_to_next_level(0)}",),
        )
        assert promotion is not None
        return required, [promotion], active_days_delta, streak_days

    reward_reasons = _build_reward_reasons(
        state,
        signals,
        active_days_delta=active_days_delta,
        streak_days=streak_days,
    )
    delta_score = sum(reason.score for reason in reward_reasons)
    return delta_score, reward_reasons, active_days_delta, streak_days


def _build_reward_reasons(
    state: ProfileGrowthState,
    signals: GrowthTurnSignals,
    *,
    active_days_delta: int,
    streak_days: int,
) -> list[GrowthRewardReason]:
    reward_reasons = [
        _work_depth_reason(signals),
        _outcome_quality_reason(signals),
        _continuity_reason(signals),
        _learning_yield_reason(signals),
        _capability_leverage_reason(signals),
        _novelty_transfer_reason(signals),
        _resilience_reason(signals),
        _token_support_reason(signals),
        _cadence_support_reason(signals),
        _streak_support_reason(active_days_delta=active_days_delta, streak_days=streak_days),
        _anti_grind_penalty_reason(state, signals),
    ]
    return [reason for reason in reward_reasons if reason is not None]


def _work_depth_reason(signals: GrowthTurnSignals) -> GrowthRewardReason | None:
    score = 0
    facts: list[str] = []
    if signals.goal_id:
        score += 3
        facts.append(f"goal={signals.goal_id}")
    goal_status = signals.goal_status.strip().lower() if signals.goal_status else ""
    if goal_status:
        score += _GOAL_STATUS_POINTS.get(goal_status, 0)
        facts.append(f"goal-status={goal_status}")
    goal_priority = signals.goal_priority.strip().lower() if signals.goal_priority else ""
    if goal_priority:
        score += _GOAL_PRIORITY_POINTS.get(goal_priority, 0)
        facts.append(f"goal-priority={goal_priority}")
    if signals.plan_step_count:
        score += min(4, signals.plan_step_count)
        facts.append(f"plan-steps={signals.plan_step_count}")
    if signals.goal_dependency_count:
        score += min(2, signals.goal_dependency_count)
        facts.append(f"goal-dependencies={signals.goal_dependency_count}")
    action = signals.progression_action.strip().lower()
    if action:
        score += _PROGRESSION_ACTION_POINTS.get(action, 0)
        facts.append(f"progression-action={action}")
    return _reward_reason(
        "work-depth",
        "Work Depth",
        "Goal-directed work depth came from active planning context instead of raw turn volume.",
        score,
        evidence_refs=signals.goal_evidence_refs,
        facts=tuple(facts),
    )


def _outcome_quality_reason(signals: GrowthTurnSignals) -> GrowthRewardReason | None:
    score = 0
    facts: list[str] = []
    outcome = signals.execution_outcome.strip().lower()
    if outcome in _GOOD_EXECUTION_OUTCOMES:
        score += 2
        facts.append(f"execution-outcome={outcome}")
    elif outcome in {"blocked", "paused"}:
        score += 1
        facts.append(f"execution-outcome={outcome}")
    if signals.experience_status == "captured":
        score += 2
        facts.append("experience=captured")
    if signals.artifact_ids:
        score += min(4, len(signals.artifact_ids) * 2)
        facts.append(f"artifacts={len(signals.artifact_ids)}")
    if signals.goal_evidence_refs:
        score += min(3, len(signals.goal_evidence_refs))
        facts.append(f"goal-evidence={len(signals.goal_evidence_refs)}")
    return _reward_reason(
        "outcome-quality",
        "Outcome Quality",
        "The turn produced inspectable outcome evidence instead of only more text.",
        score,
        evidence_refs=signals.goal_evidence_refs,
        facts=tuple(facts),
    )


def _continuity_reason(signals: GrowthTurnSignals) -> GrowthRewardReason | None:
    score = 0
    facts: list[str] = []
    continuity_mode = signals.continuity_mode.strip().lower()
    if continuity_mode and continuity_mode != "foreground":
        score += 4
        facts.append(f"continuity-mode={continuity_mode}")
    resume_signal = signals.resume_signal.strip().lower()
    if resume_signal in _RECOVERY_RESUME_SIGNALS:
        score += 3
        facts.append(f"resume-signal={resume_signal}")
    if signals.active_goal_present:
        score += 2
        facts.append("active-goal-context")
    if signals.memory_count:
        score += min(3, signals.memory_count)
        facts.append(f"memory-refs={signals.memory_count}")
    if signals.replay_evidence_refs:
        score += min(4, len(signals.replay_evidence_refs))
        facts.append(f"resume-evidence={len(signals.replay_evidence_refs)}")
    if signals.context_goal_count:
        score += min(2, signals.context_goal_count)
        facts.append(f"context-goals={signals.context_goal_count}")
    return _reward_reason(
        "continuity",
        "Continuity",
        "Resume state, active-goal context, and replay evidence stayed explicit in the turn.",
        score,
        evidence_refs=signals.replay_evidence_refs,
        facts=tuple(facts),
    )


def _learning_yield_reason(signals: GrowthTurnSignals) -> GrowthRewardReason | None:
    score = 0
    facts: list[str] = []
    if signals.captured_experiences:
        score += min(4, signals.captured_experiences * 2)
        facts.append(f"captured-experiences={signals.captured_experiences}")
    if signals.promoted_experiences:
        score += signals.promoted_experiences * 8
        facts.append(f"promoted-experiences={signals.promoted_experiences}")
    for procedure_id in signals.promoted_procedure_ids:
        facts.append(f"promoted-procedure={procedure_id}")
    return _reward_reason(
        "learning-yield",
        "Learning Yield",
        "The turn created reusable experience or promoted procedure knowledge.",
        score,
        facts=tuple(facts),
    )


def _capability_leverage_reason(signals: GrowthTurnSignals) -> GrowthRewardReason | None:
    score = 0
    facts: list[str] = []
    if signals.tool_call_count:
        score += min(4, signals.tool_call_count)
        facts.append(f"tool-calls={signals.tool_call_count}")
    if signals.skill_ids:
        score += min(4, len(signals.skill_ids) * 2)
        facts.append(f"skills={len(signals.skill_ids)}")
    if signals.model_turn_count > 1:
        score += min(2, signals.model_turn_count - 1)
        facts.append(f"model-turns={signals.model_turn_count}")
    return _reward_reason(
        "capability-leverage",
        "Capability Leverage",
        "The turn leveraged tools, skills, or multi-step execution instead of a flat single reply.",
        score,
        facts=tuple(facts),
    )


def _novelty_transfer_reason(signals: GrowthTurnSignals) -> GrowthRewardReason | None:
    score = 0
    facts: list[str] = []
    if signals.artifact_ids and signals.skill_ids:
        score += min(4, len(signals.artifact_ids) + len(signals.skill_ids))
        facts.append("skills-produced-artifacts")
    if len(signals.skill_ids) > 1:
        score += 2
        facts.append(f"skill-combination={len(signals.skill_ids)}")
    if len(signals.goal_evidence_refs) >= 2 and signals.artifact_ids:
        score += 1
        facts.append("artifact-linked-evidence")
    return _reward_reason(
        "novelty-transfer",
        "Novelty Or Transfer",
        "The turn combined evidence, skills, and outputs in a way that can transfer beyond one reply.",
        score,
        evidence_refs=signals.goal_evidence_refs,
        facts=tuple(facts),
    )


def _resilience_reason(signals: GrowthTurnSignals) -> GrowthRewardReason | None:
    score = 0
    facts: list[str] = []
    action = signals.progression_action.strip().lower()
    if signals.blocked_goal_count and action in {"advance", "replan"}:
        score += 4
        facts.append(f"blocked-goals={signals.blocked_goal_count}")
        facts.append(f"progression-action={action}")
    if signals.continuity_bonus and signals.execution_outcome.strip().lower() in _GOOD_EXECUTION_OUTCOMES:
        score += 3
        facts.append("recovery-turn")
    if signals.resume_signal.strip().lower() in {"interrupted", "resume"} and signals.goal_status == "blocked":
        score += 2
        facts.append("blocked-goal-recovery")
    return _reward_reason(
        "resilience",
        "Resilience",
        "The turn preserved momentum while recovering from interruption or blockers.",
        score,
        facts=tuple(facts),
    )


def _token_support_reason(signals: GrowthTurnSignals) -> GrowthRewardReason | None:
    token_score = min(6, round(2.6 * math.log1p(max(0, signals.total_tokens) / 180.0)))
    return _reward_reason(
        "tokens-support",
        "Token Support",
        "Token volume contributes only a bounded support term.",
        token_score,
        facts=(f"total-tokens={max(0, signals.total_tokens)}",),
        bounded=True,
    )


def _cadence_support_reason(signals: GrowthTurnSignals) -> GrowthRewardReason | None:
    elapsed = signals.elapsed_since_last_turn_seconds
    if elapsed is None or elapsed < 0:
        return None
    score = 0
    if elapsed <= 6 * 60 * 60:
        score = 3
    elif elapsed <= 48 * 60 * 60:
        score = 2
    elif signals.continuity_bonus and elapsed <= 7 * 24 * 60 * 60:
        score = 3
    elif elapsed <= 7 * 24 * 60 * 60:
        score = 1
    return _reward_reason(
        "cadence-support",
        "Cadence Support",
        "Return cadence and recovery pacing stay visible but bounded.",
        score,
        facts=(f"elapsed-seconds={elapsed}",),
        bounded=True,
    )


def _streak_support_reason(*, active_days_delta: int, streak_days: int) -> GrowthRewardReason | None:
    if not active_days_delta:
        return None
    score = 2 + min(4, max(0, streak_days - 1))
    return _reward_reason(
        "streak-support",
        "Streak Support",
        "Active-day and streak momentum remain bounded support terms.",
        score,
        facts=(
            f"active-days+={active_days_delta}",
            f"streak-days={streak_days}",
        ),
        bounded=True,
    )


def _anti_grind_penalty_reason(
    state: ProfileGrowthState,
    signals: GrowthTurnSignals,
) -> GrowthRewardReason | None:
    low_value_pattern = (
        not signals.goal_id
        and not signals.active_goal_present
        and not signals.goal_evidence_refs
        and not signals.artifact_ids
        and not signals.promoted_procedure_ids
        and not signals.skill_ids
        and signals.tool_call_count <= 0
        and signals.progression_action.strip().lower() not in {"advance", "replan"}
        and signals.continuity_mode.strip().lower() == "foreground"
    )
    token_heavy_without_proof = (
        signals.total_tokens >= 6_000
        and not signals.goal_evidence_refs
        and not signals.artifact_ids
        and not signals.promoted_procedure_ids
    )
    if not low_value_pattern and not token_heavy_without_proof:
        return None

    duplicate_pressure = max(0, state.total_dialogues - max(1, state.total_experiences))
    penalty = 0
    facts: list[str] = []
    if low_value_pattern:
        penalty += 2 + min(4, duplicate_pressure)
        facts.append("pattern=low-value")
    if token_heavy_without_proof:
        penalty += min(3, max(1, signals.total_tokens // 6_000))
        facts.append(f"token-heavy={signals.total_tokens}")
    if duplicate_pressure:
        facts.append(f"duplicate-pressure={duplicate_pressure}")
    if penalty <= 0:
        return None
    return GrowthRewardReason(
        reason_id="anti-grind-compression",
        label="Anti-Grind Compression",
        summary="Repeated low-proof patterns are compressed so flat narration cannot outrank validated work.",
        score=-penalty,
        facts=tuple(facts),
        bounded=True,
    )
