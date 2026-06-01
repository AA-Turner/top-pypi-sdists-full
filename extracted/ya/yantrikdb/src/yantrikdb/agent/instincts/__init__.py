"""Instinct registry — loads and manages all companion instincts."""

from __future__ import annotations

import logging
from typing import TYPE_CHECKING

from yantrikdb.agent.instincts.protocol import CompanionState, Instinct, UrgeSpec

if TYPE_CHECKING:
    from yantrikdb.agent.config import InstinctSettings

log = logging.getLogger("yantrik.instincts")


def load_instincts(settings: InstinctSettings) -> list[Instinct]:
    """Load all enabled instincts based on config."""
    instincts: list[Instinct] = []

    if settings.check_in_enabled:
        from yantrikdb.agent.instincts.check_in import CheckInInstinct
        instincts.append(CheckInInstinct(hours_threshold=settings.check_in_hours))

    if settings.emotional_awareness_enabled:
        from yantrikdb.agent.instincts.emotional_awareness import EmotionalAwarenessInstinct
        instincts.append(EmotionalAwarenessInstinct())

    if settings.follow_up_enabled:
        from yantrikdb.agent.instincts.follow_up import FollowUpInstinct
        instincts.append(FollowUpInstinct(min_hours=settings.follow_up_min_hours))

    if settings.reminder_enabled:
        from yantrikdb.agent.instincts.reminder import ReminderInstinct
        instincts.append(ReminderInstinct())

    if settings.pattern_surfacing_enabled:
        from yantrikdb.agent.instincts.pattern_surfacing import PatternSurfacingInstinct
        instincts.append(PatternSurfacingInstinct())

    if settings.conflict_alerting_enabled:
        from yantrikdb.agent.instincts.conflict_alerting import ConflictAlertingInstinct
        instincts.append(ConflictAlertingInstinct(threshold=settings.conflict_alert_threshold))

    log.info("Loaded %d instincts: %s", len(instincts), [i.name for i in instincts])
    return instincts


__all__ = ["load_instincts", "Instinct", "UrgeSpec", "CompanionState"]
