"""ConflictAlerting instinct — alerts when memory conflicts accumulate."""

from __future__ import annotations

from yantrikdb.agent.instincts.protocol import CompanionState, UrgeSpec


class ConflictAlertingInstinct:
    name = "conflict_alerting"
    description = "Alerts when important memory conflicts need resolution"

    def __init__(self, threshold: int = 5):
        self.threshold = threshold

    def evaluate(self, state: CompanionState) -> list[UrgeSpec]:
        if state.open_conflicts_count < self.threshold:
            return []

        urgency = min(0.8, state.open_conflicts_count / 10)

        return [UrgeSpec(
            instinct_name=self.name,
            reason=f"{state.open_conflicts_count} memory conflicts need your help to resolve",
            urgency=urgency,
            context={"open_count": state.open_conflicts_count},
            cooldown_key="conflict_alert",
        )]

    def on_interaction(self, state: CompanionState, user_text: str) -> list[UrgeSpec]:
        return []
