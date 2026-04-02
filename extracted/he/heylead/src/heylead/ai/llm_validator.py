"""LLM-based message validation using v63 production prompts.

Complements the rule-based validator (message_validator.py) with context-sensitive
checks that regexes can't do:

1. Bullet reuse across last 2 messages
2. Greeting/signoff reuse vs previous
3. Length variation (±15% of previous)
4. CTA variation (identical check)
5. First-sentence overlap (stopword removal, >30%)
6. Guardrails (company names, roles, buzzwords)
7. Link-gating (link present + SDR count < 2)

Usage:
    from .llm_validator import llm_validate
    result = await llm_validate(message, history, company)
    if not result.is_valid:
        # merge with rule-based issues
"""

from __future__ import annotations

import logging
from typing import Any

from .json_repair import parse_json
from .llm import LLMClient
from .message_validator import ValidationResult
from .prompt_loader import has_prompt, render_prompt, get_prompt_temperature

logger = logging.getLogger(__name__)


def _format_history_for_validation(messages: list[dict[str, Any]]) -> str:
    """Format conversation history for the validation prompt."""
    if not messages:
        return "No previous messages."
    lines = []
    for msg in messages:
        role = msg.get("role", "unknown")
        text = msg.get("text", "")
        label = "SDR" if role == "sdr" else "PROSPECT"
        lines.append(f"[{label}]: {text}")
    return "\n".join(lines)


async def llm_validate(
    message: str,
    history: list[dict[str, Any]],
    company: str,
    calendar_link: str = "",
    message_type: str = "followup",
    prospect_company: str = "",
    max_chars: int = 500,
) -> ValidationResult:
    """Run LLM-based validation using v63's validate prompt.

    Args:
        message: The generated message to validate
        history: Conversation history (list of {role, text} dicts)
        company: Sender's company name (for name-leak detection)
        calendar_link: Calendar link (for link-gating check)
        message_type: "invitation" or "followup"
        prospect_company: Prospect's company name (for invitation validation)
        max_chars: Character limit for validation

    Returns:
        ValidationResult with is_valid, issues, and warnings
    """
    result = ValidationResult()

    # Pick the right prompt based on message type
    if message_type == "invitation":
        prompt_name = "outreach_validate"
    else:
        prompt_name = "followup_validate"

    if not has_prompt(prompt_name):
        result.pass_stage("LLM")
        return result

    try:
        if message_type == "invitation":
            ctx = {
                "message": message,
                "company": company,
                "prospect_company": prospect_company,
                "max_chars": str(max_chars),
            }
        else:
            ctx = {
                "message": message,
                "history": _format_history_for_validation(history),
                "company": company,
                "calendar_link": calendar_link or "Not configured",
            }

        prompt = render_prompt(prompt_name, ctx)
        temp = get_prompt_temperature(prompt_name)

        llm_client = LLMClient()
        raw = await llm_client.generate(prompt, temperature=temp, max_tokens=500)

        # Parse structured response
        parsed = parse_json(raw, fallback=None)

        if parsed and isinstance(parsed, dict):
            is_valid = parsed.get("valid", True)
            issues = parsed.get("issues", [])

            if not is_valid and issues:
                for issue in issues:
                    if isinstance(issue, str):
                        result.fail("LLM-Validate", issue)
            else:
                result.pass_stage("LLM-Validate")
        else:
            # Try to parse plain text response (VALID/INVALID format)
            raw_upper = raw.strip().upper()
            if raw_upper.startswith("INVALID"):
                # Extract reason after INVALID
                reason = raw.strip()[len("INVALID"):].strip().strip(":").strip()
                result.fail("LLM-Validate", reason or "LLM validator flagged message as invalid")
            else:
                result.pass_stage("LLM-Validate")

    except Exception as e:
        # LLM validation is optional — don't block on errors
        logger.warning("LLM validation failed (non-blocking): %s", e)
        result.pass_stage("LLM-Validate")
        result.warn("LLM-Validate", f"LLM validation unavailable: {e}")

    return result
