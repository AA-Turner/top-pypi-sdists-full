"""Fallback parsing pipeline for structured LLM output schemas.

Implements six strategies to handle common LLM output deviations,
applied in order from least-destructive to most-destructive with
short-circuit on first successful parse.
"""

from __future__ import annotations

import json
import logging
import re
from ast import literal_eval
from typing import TypeVar

from pydantic import BaseModel, ValidationError

logger = logging.getLogger(__name__)

T = TypeVar("T", bound=BaseModel)

# BOM and invisible Unicode characters to strip from the boundaries only
_INVISIBLE_CHARS = "\ufeff\u200b\u200c\u200d\u2060\ufffe\u00a0\u2028\u2029"

# Markdown code fence pattern
_CODE_FENCE_PATTERN = re.compile(r"```(?:json|JSON)?\s*\r?\n(.*?)\r?\n\s*```", re.DOTALL)


def _try_validate(model_class: type[T], text: str) -> T | None:
    """Attempt to validate text as JSON against the model. Returns None on failure."""
    try:
        return model_class.model_validate_json(text)
    except (ValidationError, ValueError):
        return None


def strip_bom_and_invisible(text: str) -> str:
    """Strategy 1: Strip BOM and invisible Unicode characters."""
    return text.strip(_INVISIBLE_CHARS).strip().strip(_INVISIBLE_CHARS)


def extract_code_fences(text: str) -> list[str]:
    """Strategy 2: Extract content from markdown code fences."""
    matches = _CODE_FENCE_PATTERN.findall(text)
    return [m.strip() for m in matches] if matches else []


def _scan_json_spans(text: str, open_char: str, close_char: str) -> list[str]:
    """Find top-level JSON object or array spans in *text*, string-aware.

    Tracks whether the current position is inside a JSON string (``"…"``)
    and skips ``open_char``/``close_char`` that appear inside strings, so
    code snippets or template literals in field values do not confuse the
    depth counter.

    Args:
        text: The raw text to scan.
        open_char: The opening delimiter (``{`` or ``[``).
        close_char: The closing delimiter (``}`` or ``]``).

    Returns:
        Unique candidate substrings in document order.
    """
    results: list[str] = []
    depth = 0
    start = -1
    in_string = False
    i = 0
    n = len(text)
    while i < n:
        ch = text[i]
        if in_string:
            if ch == "\\" and i + 1 < n:
                i += 2  # skip over the escape sequence
                continue
            elif ch == '"':
                in_string = False
        else:
            if ch == '"':
                in_string = True
            elif ch == open_char:
                if depth == 0:
                    start = i
                depth += 1
            elif ch == close_char and depth > 0:
                depth -= 1
                if depth == 0 and start >= 0:
                    candidate = text[start : i + 1]
                    if candidate not in results:
                        results.append(candidate)
                    start = -1
        i += 1
    return results


def extract_json_from_prose(text: str) -> list[str]:
    """Strategy 3: Extract JSON objects from surrounding prose.

    Finds the outermost JSON objects or arrays in the text using a
    string-aware scanner that correctly handles ``{``/``}``/``[``/``]``
    characters inside JSON string values (e.g. code snippets in
    ``original_code`` or ``replacement_code`` fields).
    """
    # _scan_json_spans deduplicates within each call, and {…} / […] spans
    # are disjoint (different delimiter characters), so no cross-call
    # deduplication is needed.
    results = list(_scan_json_spans(text, "{", "}"))
    results.extend(_scan_json_spans(text, "[", "]"))
    return results


def normalize_single_quotes(text: str) -> str:
    """Strategy 4: Replace single quotes with double quotes for JSON parsing.

    Only handles simple cases where single quotes are used as JSON string delimiters.
    """
    try:
        parsed = literal_eval(text)
    except (ValueError, SyntaxError):
        return text
    return json.dumps(parsed)


def remove_trailing_commas(text: str) -> str:
    """Strategy 5: Remove trailing commas before closing braces/brackets.

    String-aware: commas inside quoted JSON string values are never removed,
    so code snippets like ``"return x,}"`` are preserved intact.
    """
    result: list[str] = []
    in_string = False
    i = 0
    n = len(text)
    while i < n:
        ch = text[i]
        if in_string:
            if ch == "\\" and i + 1 < n:
                result.append(ch)
                result.append(text[i + 1])
                i += 2
                continue
            if ch == '"':
                in_string = False
            result.append(ch)
        else:
            if ch == '"':
                in_string = True
                result.append(ch)
            elif ch == ",":
                # Look ahead past whitespace to check for a closing delimiter
                j = i + 1
                while j < n and text[j] in " \t\r\n":
                    j += 1
                if j < n and text[j] in "}]":
                    # Trailing comma outside a string — drop it
                    pass
                else:
                    result.append(ch)
            else:
                result.append(ch)
        i += 1
    return "".join(result)


def unwrap_list_to_single(text: str) -> str | None:
    """Strategy 6: Unwrap a JSON array containing a single object.

    If the text is a JSON array with exactly one element, return that element.
    """
    try:
        data = json.loads(text)
    except (json.JSONDecodeError, ValueError):
        return None
    if isinstance(data, list) and len(data) == 1:
        return json.dumps(data[0])
    return None


def run_fallback_pipeline(model_class: type[T], raw_response: str) -> T | None:
    """Run the fallback parsing pipeline.

    Applies strategies in order from least-destructive to most-destructive,
    short-circuiting on first successful parse+validate.

    Args:
        model_class: The Pydantic model class to validate against.
        raw_response: The raw LLM response string.

    Returns:
        A validated model instance, or None if all strategies fail.
    """
    # Strategy 1: Strip BOM/invisible Unicode
    cleaned = strip_bom_and_invisible(raw_response)
    if cleaned != raw_response:
        result = _try_validate(model_class, cleaned)
        if result is not None:
            logger.debug("Fallback strategy succeeded: strip_bom_and_invisible")
            return result

    # Strategy 2: Extract from markdown code fences
    blocks = extract_code_fences(raw_response)
    if blocks:
        if len(blocks) > 1:
            logger.warning(
                "Multiple JSON blocks detected in LLM response (%d blocks); trying each in document order",
                len(blocks),
            )
        for block in blocks:
            result = _try_validate(model_class, block)
            if result is not None:
                logger.debug("Fallback strategy succeeded: extract_code_fences")
                return result

    # Strategy 3: Extract JSON from surrounding prose
    json_candidates = extract_json_from_prose(raw_response)
    if json_candidates:
        for candidate in json_candidates:
            result = _try_validate(model_class, candidate)
            if result is not None:
                logger.debug("Fallback strategy succeeded: extract_json_from_prose")
                return result

    # Combined: remove trailing commas from prose-extracted candidates
    for candidate in json_candidates:
        fixed = remove_trailing_commas(candidate)
        if fixed != candidate:
            result = _try_validate(model_class, fixed)
            if result is not None:
                logger.debug("Fallback strategy succeeded: extract_json_from_prose + remove_trailing_commas")
                return result

    # Strategy 4: Normalize single quotes
    normalized = normalize_single_quotes(raw_response)
    if normalized != raw_response:
        result = _try_validate(model_class, normalized)
        if result is not None:
            logger.debug("Fallback strategy succeeded: normalize_single_quotes")
            return result

    # Strategy 5: Remove trailing commas
    no_trailing = remove_trailing_commas(raw_response)
    if no_trailing != raw_response:
        result = _try_validate(model_class, no_trailing)
        if result is not None:
            logger.debug("Fallback strategy succeeded: remove_trailing_commas")
            return result

    # Strategy 6: Unwrap list to single object
    # Try on cleaned/extracted text too
    for text in [raw_response, cleaned, *blocks, *json_candidates]:
        unwrapped = unwrap_list_to_single(text)
        if unwrapped is not None:
            result = _try_validate(model_class, unwrapped)
            if result is not None:
                logger.debug("Fallback strategy succeeded: unwrap_list_to_single")
                return result

    # Combined strategies: try removing trailing commas on code fence content
    for block in blocks:
        fixed = remove_trailing_commas(block)
        if fixed != block:
            result = _try_validate(model_class, fixed)
            if result is not None:
                logger.debug("Fallback strategy succeeded: extract_code_fences + remove_trailing_commas")
                return result

    return None
