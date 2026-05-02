"""Progression rollout helpers for the operator dashboard surface."""

from __future__ import annotations

from packages.growth import (
    ProgressionProjection,
    ProgressionProjectionBuilder,
    default_progression_rollout_scorecard,
)
from packages.operator import DashboardProgressionRecord

_PROGRESSION_BUILDER = ProgressionProjectionBuilder()


def build_progression_projection(app, *, profile_id: str, session_id: str | None = None, state=None) -> ProgressionProjection:
    active_goal = None
    continuity_mode = "foreground"
    wake_action = ""
    if session_id is not None:
        continuity = app.inspect_continuity(session_id)
        continuity_mode = continuity.continuity.continuity.mode
        wake_action = continuity.wake_action
        graph = app.repository.load_activity_graph(session_id)
        if graph is not None and graph.active_goal_id is not None:
            active_goal = graph.goal(graph.active_goal_id)
    experiences = app.repository.list_experiences(profile_id=profile_id)
    procedure_library = app.repository.load_procedure_library(profile_id)
    return _PROGRESSION_BUILDER.build(
        profile_id=profile_id,
        state=state,
        experiences=experiences,
        procedures=procedure_library.procedures if procedure_library is not None else (),
        active_goal=active_goal,
        continuity_mode=continuity_mode,
        wake_action=wake_action,
    )


def build_dashboard_progression(projection: ProgressionProjection) -> DashboardProgressionRecord:
    scorecard = default_progression_rollout_scorecard()
    return DashboardProgressionRecord(
        title=projection.stage_title,
        cycle=projection.cycle_label,
        level=f"Lv.{projection.ascension_level} · power {projection.power_score}",
        momentum=projection.momentum_state,
        challenge=(
            projection.active_challenge_tracks[0].summary
            if projection.active_challenge_tracks
            else projection.next_milestone
        ),
        proof=projection.proof_state,
        rollout=(
            "shadow-certified · curated replay pack is green"
            if scorecard.certified
            else "compatibility fallback required"
        ),
        fallback="Compatibility snapshot takes over if fairness, explanation drift, or UI budget regresses.",
        tone="attention" if projection.title_window_open else "healthy",
    )


def progression_metric_note(
    projection: ProgressionProjection | None,
    dashboard_progression: DashboardProgressionRecord | None,
) -> str:
    if projection is None:
        return "Progression only appears once canonical work or evidence exists."
    if dashboard_progression is None:
        return projection.proof_state
    return f"{projection.proof_state} · {dashboard_progression.rollout}"
