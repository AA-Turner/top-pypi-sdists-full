"""PatternSurfacing instinct — shares discovered patterns with the user."""

from __future__ import annotations

from yantrikdb.agent.instincts.protocol import CompanionState, UrgeSpec


class PatternSurfacingInstinct:
    name = "pattern_surfacing"
    description = "Surfaces actionable patterns discovered by the cognition loop"

    def evaluate(self, state: CompanionState) -> list[UrgeSpec]:
        # Look for pattern_discovered triggers from think()
        pattern_triggers = [
            t for t in state.pending_triggers
            if t.get("trigger_type") == "pattern_discovered"
        ]

        urges = []
        for trigger in pattern_triggers[:2]:  # max 2 pattern urges
            ctx = trigger.get("context", {})
            urgency = trigger.get("urgency", 0.3)
            desc = ctx.get("description", trigger.get("reason", "A new pattern"))

            urges.append(UrgeSpec(
                instinct_name=self.name,
                reason=f"Pattern noticed: {desc}",
                urgency=urgency,
                context=ctx,
                cooldown_key=f"pattern:{ctx.get('pattern_type', '')}:{desc[:30]}",
            ))

        return urges

    def on_interaction(self, state: CompanionState, user_text: str) -> list[UrgeSpec]:
        return []
