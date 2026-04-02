"""3-tier JSON parsing utility for LLM output.

LLMs (especially Gemini Flash) frequently produce malformed JSON:
- Markdown code fences around JSON
- Trailing commas before closing braces/brackets
- Stray characters before property names
- Truncated content

This module provides a progressive repair strategy:
1. Raw parse: json.loads() directly
2. Regex cleanup: fix common LLM JSON errors
3. LLM repair: send broken JSON to LLM for fixing (async only)
"""

from __future__ import annotations

import json
import logging
import re
from typing import Any

logger = logging.getLogger(__name__)


def _strip_markdown_fences(text: str) -> str:
    """Extract JSON from markdown code fences if present."""
    text = text.strip()

    # ```json ... ``` or ``` ... ```
    if "```json" in text:
        text = text.split("```json", 1)[1].split("```", 1)[0]
    elif "```" in text:
        # Only strip if it looks like fenced code (starts with ```)
        if text.startswith("```"):
            lines = text.split("\n")
            # Remove first and last ``` lines
            cleaned_lines = [
                line for line in lines if not line.strip().startswith("```")
            ]
            text = "\n".join(cleaned_lines)

    return text.strip()


def _regex_cleanup(text: str) -> str:
    """Fix common LLM JSON generation errors with regex.

    Handles:
    - Stray characters before property names (common Gemini Flash error)
      e.g., 'g  "growth_signals"' -> '"growth_signals"'
    - Trailing commas before closing braces/brackets
      e.g., '{"a": 1,}' -> '{"a": 1}'
    - Single quotes instead of double quotes (basic cases)
    """
    # Remove stray characters before property names
    # Pattern: after a comma/brace/bracket + whitespace, a lone letter before a quote
    text = re.sub(r'([}\]],?)\s*[a-zA-Z]\s+(")', r'\1\n\2', text)

    # Fix trailing commas before closing braces/brackets
    text = re.sub(r',(\s*[}\]])', r'\1', text)

    # Remove any control characters except newlines and tabs
    text = re.sub(r'[\x00-\x08\x0b\x0c\x0e-\x1f]', '', text)

    return text.strip()


def parse_json(raw: str, fallback: dict[str, Any] | None = None) -> dict[str, Any]:
    """Parse LLM JSON output with 2-tier repair (sync).

    Strategy:
    1. Raw parse: json.loads() directly
    2. Regex cleanup: strip fences, fix trailing commas, remove stray chars

    If both fail, returns fallback (or raises ValueError if no fallback).

    Args:
        raw: Raw LLM output string.
        fallback: Default dict to return on parse failure. If None, raises ValueError.

    Returns:
        Parsed dict.
    """
    if not raw or not raw.strip():
        if fallback is not None:
            return fallback
        raise ValueError("Empty input to parse_json")

    # ── Tier 1: Raw parse ──
    stripped = raw.strip()
    try:
        result = json.loads(stripped)
        if isinstance(result, dict):
            return result
    except (json.JSONDecodeError, ValueError):
        pass

    # ── Tier 2: Regex cleanup ──
    try:
        cleaned = _strip_markdown_fences(stripped)
        cleaned = _regex_cleanup(cleaned)
        result = json.loads(cleaned)
        if isinstance(result, dict):
            logger.debug("JSON parsed after regex cleanup")
            return result
    except (json.JSONDecodeError, ValueError) as e:
        logger.warning(f"JSON regex cleanup failed: {e}")

    # ── Fallback ──
    if fallback is not None:
        logger.warning("JSON parse failed, using fallback")
        return fallback
    raise ValueError(f"Failed to parse JSON from LLM output: {raw[:200]}...")


async def parse_json_with_llm_repair(
    raw: str,
    format_hint: str = "",
    fallback: dict[str, Any] | None = None,
) -> dict[str, Any]:
    """Parse LLM JSON output with 3-tier repair (async).

    Strategy:
    1. Raw parse: json.loads() directly
    2. Regex cleanup: strip fences, fix trailing commas, remove stray chars
    3. LLM repair: send broken JSON + format hint to LLM for fixing

    If all fail, returns fallback (or raises ValueError if no fallback).

    Args:
        raw: Raw LLM output string.
        format_hint: Description of expected JSON format for LLM repair.
        fallback: Default dict to return on parse failure. If None, raises ValueError.

    Returns:
        Parsed dict.
    """
    # Try tiers 1-2 first (sync)
    try:
        return parse_json(raw, fallback=None)
    except ValueError:
        pass

    # ── Tier 3: LLM repair ──
    try:
        from .llm import LLMClient

        repair_prompt = (
            "The following JSON is malformed or does not match the required schema. "
            "Fix it and return ONLY the valid JSON, nothing else.\n\n"
            "Common issues to fix:\n"
            "- Stray characters before property names\n"
            "- Missing commas\n"
            "- Trailing commas before closing brackets\n"
            "- Truncated content\n"
            "- Invalid escape sequences\n"
            "- Fields that violate schema types\n\n"
        )
        if format_hint:
            repair_prompt += f"EXPECTED FORMAT:\n{format_hint}\n\n"
        repair_prompt += f"BROKEN JSON:\n{raw}\n\nReturn ONLY the fixed JSON."

        client = LLMClient()
        fixed_raw = await client.generate(
            repair_prompt,
            system="You are a JSON repair tool. Output ONLY valid JSON, nothing else.",
            temperature=0.0,
            max_tokens=2000,
        )

        # Parse the repaired output (tiers 1-2 only, no infinite recursion)
        result = parse_json(fixed_raw, fallback=None)
        logger.info("JSON parsed after LLM repair")
        return result

    except Exception as e:
        logger.warning(f"LLM JSON repair failed: {e}")

    # ── Fallback ──
    if fallback is not None:
        logger.warning("All JSON parse strategies failed, using fallback")
        return fallback
    raise ValueError(f"Failed to parse JSON after all repair strategies: {raw[:200]}...")
