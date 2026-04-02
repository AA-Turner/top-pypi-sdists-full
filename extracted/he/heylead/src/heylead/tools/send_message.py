"""Tool: send_message — Send follow-ups, replies, or voice memos.

Thin dispatcher that routes to existing run_* functions based on the action parameter.
"""

from __future__ import annotations

import logging

logger = logging.getLogger(__name__)


async def run_send_message(
    action: str = "followup",
    campaign_id: str = "",
    outreach_id: str = "",
    mode: str = "autopilot",
    format: str = "text",
    text: str = "",
) -> str:
    """Send a message to a prospect.

    Actions:
      followup — Send a follow-up DM after connection accepted
      reply    — Reply to a prospect who has messaged you
      voice    — Send a voice memo on LinkedIn
      delete   — Delete a recently sent message (within 60 min on LinkedIn)

    Args:
        action: What to do: 'followup', 'reply', 'voice', 'delete'.
        campaign_id: Which campaign to send from. Uses active campaign if empty.
        outreach_id: Specific outreach to target. Auto-picks next if empty.
        mode: 'autopilot' (sends automatically) or 'copilot' (you review first).
        format: 'text' (default DM) or 'voice' (audio via Hume TTS). For followup/reply.
        text: Custom text to convert to voice. Auto-generates if empty. For voice action.
            For delete: optionally pass a Unipile message_id directly.
    """
    action = action.lower().strip()

    if action == "followup":
        from .send_followup import run_send_followup
        return await run_send_followup(campaign_id, outreach_id, mode, format=format)

    if action == "reply":
        from .reply_to_prospect import run_reply_to_prospect
        return await run_reply_to_prospect(outreach_id=outreach_id, mode=mode, format=format)

    if action == "voice":
        from .send_voice_memo import run_send_voice_memo
        return await run_send_voice_memo(campaign_id, outreach_id, text, mode)

    if action == "delete":
        from .delete_message import run_delete_message
        return await run_delete_message(campaign_id, outreach_id, message_id=text, mode=mode)

    return f"Unknown action: '{action}'. Use 'followup', 'reply', 'voice', or 'delete'."
