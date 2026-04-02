"""Shared Generate → Improve → Validate → Fix pipeline for reply messages.

Used by both outbound (reply_to_prospect) and inbound (inbound_pipeline)
to avoid duplicating the 4-stage reply generation logic.
"""

from __future__ import annotations

import logging
from typing import Any

from .message_fixer import fix_message
from .message_improver import improve_message
from .message_validator import validate_reply
from .reply_generator import NEGATIVE_MAX_CHARS, REPLY_MAX_CHARS, generate_reply

logger = logging.getLogger(__name__)


async def run_reply_pipeline(
    prospect: dict[str, Any],
    sender_profile: dict[str, Any],
    voice_signature: dict[str, Any],
    campaign_context: dict[str, Any],
    conversation_history: list[dict[str, Any]],
    reply_text: str,
    sentiment: str,
    prospect_analysis: dict[str, Any] | None = None,
    booking_link: str = "",
    max_chars: int | None = None,
    previous_sdr_messages: list[str] | None = None,
    prospect_calendar_url: str = "",
) -> tuple[str, dict, Any]:
    """Execute the full Generate → Improve → Validate → Fix reply pipeline.

    Args:
        prospect: Prospect profile data.
        sender_profile: User's own profile data.
        voice_signature: Voice analysis results.
        campaign_context: Campaign ICP and target description.
        conversation_history: Previous messages in the thread.
        reply_text: The prospect's latest message text.
        sentiment: Classified sentiment.
        prospect_analysis: Cached prospect intelligence.
        booking_link: Optional calendar booking URL.
        max_chars: Override character limit (default: based on sentiment).
        previous_sdr_messages: Prior SDR messages for anti-repetition validation.
        prospect_calendar_url: Prospect's inbound calendar URL (from check_replies detection).

    Returns:
        Tuple of (message_text, reasoning_dict, validation_result).
        message_text may be empty if all attempts fail.
    """
    if max_chars is None:
        max_chars = NEGATIVE_MAX_CHARS if sentiment == "negative" else REPLY_MAX_CHARS
    if previous_sdr_messages is None:
        previous_sdr_messages = []

    message = ""
    reasoning: dict = {}
    validation = None

    # Attempt 1: Generate + Improve + Validate (+ Fix if needed)
    try:
        result = await generate_reply(
            prospect=prospect,
            sender_profile=sender_profile,
            voice_signature=voice_signature,
            campaign_context=campaign_context,
            conversation_history=conversation_history,
            reply_text=reply_text,
            sentiment=sentiment,
            prospect_analysis=prospect_analysis,
            booking_link=booking_link,
            prospect_calendar_url=prospect_calendar_url,
        )
        message = result.get("message", "")
        reasoning = result.get("reasoning", {})
    except Exception as e:
        logger.error("Reply generation failed: %s", e)
        return "", {}, None

    # Improve stage — polish for naturalness
    try:
        message = await improve_message(
            draft=message,
            voice_signature=voice_signature,
            message_type="reply",
            max_chars=max_chars,
        )
    except Exception as e:
        logger.warning("Improve stage failed, using raw message: %s", e)

    # Validate
    validation = validate_reply(
        message,
        voice_signature,
        sentiment=sentiment,
        previous_messages=previous_sdr_messages,
        max_chars=max_chars,
    )

    # Fix stage — if validation failed, surgically fix issues
    if not validation.is_valid:
        logger.info("Reply validation failed, attempting fix: %s", validation.issues)
        try:
            message = await fix_message(
                message=message,
                issues=validation.issues,
                voice_signature=voice_signature,
                message_type="reply",
                max_chars=max_chars,
            )
            validation = validate_reply(
                message,
                voice_signature,
                sentiment=sentiment,
                previous_messages=previous_sdr_messages,
                max_chars=max_chars,
            )
        except Exception as e:
            logger.warning("Fix stage failed: %s", e)

    # Last resort: regenerate from scratch if still invalid
    if not validation.is_valid:
        logger.info("Fix failed, regenerating reply from scratch: %s", validation.issues)
        try:
            result = await generate_reply(
                prospect=prospect,
                sender_profile=sender_profile,
                voice_signature=voice_signature,
                campaign_context=campaign_context,
                conversation_history=conversation_history,
                reply_text=reply_text,
                sentiment=sentiment,
                prospect_analysis=prospect_analysis,
                booking_link=booking_link,
            )
            message = result.get("message", "")
            reasoning = result.get("reasoning", {})
            message = await improve_message(
                draft=message,
                voice_signature=voice_signature,
                message_type="reply",
                max_chars=max_chars,
            )
            validation = validate_reply(
                message,
                voice_signature,
                sentiment=sentiment,
                previous_messages=previous_sdr_messages,
                max_chars=max_chars,
            )
        except Exception as e:
            logger.error("Regeneration failed: %s", e)

    # Clean up
    message = message.strip().strip('"').strip("'").strip()
    return message, reasoning, validation
