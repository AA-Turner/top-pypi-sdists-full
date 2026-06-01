"""FollowUp instinct — tracks unresolved topics and urges follow-up."""

from __future__ import annotations

from yantrikdb.agent.instincts.protocol import CompanionState, UrgeSpec


class FollowUpInstinct:
    name = "follow_up"
    description = "Generates urges to follow up on unresolved topics"

    def __init__(self, min_hours: float = 4.0):
        self.min_hours = min_hours

    def evaluate(self, state: CompanionState) -> list[UrgeSpec]:
        # This instinct needs the YantrikDB instance to query open topics.
        # Since CompanionState doesn't carry the db reference (intentionally),
        # the background tick populates pending_triggers with relevant info.
        # We look for any trigger that mentions unresolved topics,
        # or we use the temporal_drift trigger as a proxy.

        # For now, look for decay_review triggers on important memories
        # that might represent unresolved items
        decay_triggers = [
            t for t in state.pending_triggers
            if t.get("trigger_type") == "decay_review"
        ]

        urges = []
        for trigger in decay_triggers[:2]:  # max 2 follow-ups
            ctx = trigger.get("context", {})
            reason = trigger.get("reason", "An important memory is fading")
            urgency = trigger.get("urgency", 0.4)

            urges.append(UrgeSpec(
                instinct_name=self.name,
                reason=f"Follow up: {reason}",
                urgency=min(0.7, urgency),
                context=ctx,
                cooldown_key=f"follow_up:{trigger.get('trigger_id', '')}",
            ))

        return urges

    def on_interaction(self, state: CompanionState, user_text: str) -> list[UrgeSpec]:
        return []
