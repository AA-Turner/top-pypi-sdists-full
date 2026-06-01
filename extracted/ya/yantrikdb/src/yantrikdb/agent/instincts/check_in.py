"""CheckIn instinct — urges the companion to check in when user is away."""

from __future__ import annotations

from yantrikdb.agent.instincts.protocol import CompanionState, UrgeSpec


class CheckInInstinct:
    name = "check_in"
    description = "Generates urge to check in when user hasn't interacted in a while"

    def __init__(self, hours_threshold: float = 8.0):
        self.hours_threshold = hours_threshold

    def evaluate(self, state: CompanionState) -> list[UrgeSpec]:
        hours_since = (state.current_ts - state.last_interaction_ts) / 3600

        if hours_since < self.hours_threshold:
            return []

        # Urgency scales with time away, caps at 0.8
        urgency = min(0.8, (hours_since - self.hours_threshold) / (self.hours_threshold * 2))

        return [UrgeSpec(
            instinct_name=self.name,
            reason=f"{state.config_user_name} hasn't interacted in {hours_since:.0f} hours",
            urgency=urgency,
            context={"hours_since_interaction": round(hours_since, 1)},
            cooldown_key="check_in",
        )]

    def on_interaction(self, state: CompanionState, user_text: str) -> list[UrgeSpec]:
        return []
