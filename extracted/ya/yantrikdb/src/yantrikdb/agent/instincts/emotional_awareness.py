"""EmotionalAwareness instinct — detects valence shifts and urges acknowledgment."""

from __future__ import annotations

from yantrikdb.agent.instincts.protocol import CompanionState, UrgeSpec


class EmotionalAwarenessInstinct:
    name = "emotional_awareness"
    description = "Detects negative emotional trends and urges gentle acknowledgment"

    def evaluate(self, state: CompanionState) -> list[UrgeSpec]:
        # Look for valence_trend triggers from think()
        valence_triggers = [
            t for t in state.pending_triggers
            if t.get("trigger_type") == "valence_trend"
        ]
        if not valence_triggers:
            return []

        trigger = valence_triggers[0]
        ctx = trigger.get("context", {})
        direction = ctx.get("direction", "")

        if direction != "negative":
            return []

        delta = abs(ctx.get("delta", 0))
        urgency = min(0.9, delta)

        return [UrgeSpec(
            instinct_name=self.name,
            reason=f"Emotional tone has shifted negative (delta: {delta:.2f})",
            urgency=urgency,
            context={
                "direction": direction,
                "delta": delta,
                "recent_avg": ctx.get("recent_avg"),
                "baseline_avg": ctx.get("baseline_avg"),
            },
            cooldown_key="emotional_awareness:negative",
        )]

    def on_interaction(self, state: CompanionState, user_text: str) -> list[UrgeSpec]:
        return []
