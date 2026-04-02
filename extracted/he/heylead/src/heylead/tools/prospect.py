"""Tool: prospect — Manage prospects (skip, close, view conversation).

Thin dispatcher that routes to existing run_* functions based on the action parameter.
"""

from __future__ import annotations

import logging

logger = logging.getLogger(__name__)


async def run_prospect(
    action: str,
    outreach_id: str = "",
    campaign_id: str = "",
    outcome: str = "won",
    reason: str = "",
    meeting_link: str = "",
) -> str:
    """Manage a prospect's outreach status.

    Actions:
      skip         — Skip a prospect, removing them from the outreach queue
      close        — Record an outcome (won/lost/opt_out) for an outreach
      conversation — View the full conversation thread with a prospect
      timeline     — View chronological journey of all actions for a prospect

    Args:
        action: What to do: 'skip', 'close', 'conversation', 'timeline'.
        outreach_id: The outreach ID. Auto-selects if empty (except 'conversation'/'timeline').
        campaign_id: Which campaign (for 'skip'). Uses active if empty.
        outcome: 'won', 'lost', or 'opt_out' (for 'close' action).
        reason: Optional notes for the outcome (for 'close' action).
        meeting_link: Meeting/calendar URL if outcome is 'won' (for 'close' action).
            Could be the user's booking page or the prospect's shared calendar.
    """
    action = action.lower().strip()

    if action == "timeline":
        if not outreach_id:
            return "Error: 'outreach_id' is required for action='timeline'."
        from .prospect_timeline import run_prospect_timeline
        return await run_prospect_timeline(outreach_id)

    if action == "skip":
        from .skip_prospect import run_skip_prospect
        return await run_skip_prospect(outreach_id, campaign_id)

    if action == "close":
        from .close_outreach import run_close_outreach
        return await run_close_outreach(
            outreach_id=outreach_id,
            outcome=outcome,
            reason=reason,
            meeting_link=meeting_link,
        )

    if action == "conversation":
        if not outreach_id:
            return "Error: 'outreach_id' is required for action='conversation'. Use analytics(action='export') to find IDs."
        from .show_conversation import run_show_conversation
        return await run_show_conversation(outreach_id)

    return f"Unknown action: '{action}'. Use 'skip', 'close', 'conversation', or 'timeline'."
