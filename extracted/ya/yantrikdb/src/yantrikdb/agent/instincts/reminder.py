"""Reminder instinct — surfaces reminders that are coming due."""

from __future__ import annotations

import time

from yantrikdb.agent.instincts.protocol import CompanionState, UrgeSpec


class ReminderInstinct:
    name = "reminder"
    description = "Surfaces reminders that are coming due within the next hour"

    def evaluate(self, state: CompanionState) -> list[UrgeSpec]:
        # This instinct needs DB access to query reminder memories.
        # The companion's background tick calls this after populating
        # pending_triggers. We also check for any triggers related to
        # reminder-domain memories.
        #
        # In the full flow, the background tick queries YantrikDB for memories
        # with domain="reminder" and metadata.remind_at near current time,
        # then creates triggers. Here we just surface those.

        urges = []
        for trigger in state.pending_triggers:
            ctx = trigger.get("context", {})
            if ctx.get("domain") == "reminder" or "remind" in trigger.get("reason", "").lower():
                urgency = max(0.6, trigger.get("urgency", 0.5))
                urges.append(UrgeSpec(
                    instinct_name=self.name,
                    reason=trigger.get("reason", "A reminder is due"),
                    urgency=urgency,
                    context=ctx,
                    cooldown_key=f"reminder:{trigger.get('trigger_id', '')}",
                ))

        return urges

    def on_interaction(self, state: CompanionState, user_text: str) -> list[UrgeSpec]:
        return []
