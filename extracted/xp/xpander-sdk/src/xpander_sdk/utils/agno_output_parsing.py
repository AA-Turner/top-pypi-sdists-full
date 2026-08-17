"""Lenient-first structured-output parsing for agno runs.

Mirror of ``xpander_dev_utils/utils/agno_output_parsing.py`` - keep the tiers
identical.

agno's ``_clean_json_content`` replaces literal newlines with spaces and slices
the text at the first ``` fence, so a model that writes real line breaks (or a
fenced block) inside a JSON string value loses them before parsing. Parse the
raw text first and accept it only when it validates against the same schema;
anything else falls through to agno untouched.
"""

import json
import re
from typing import Any, Callable, List, Optional

from loguru import logger

from xpander_sdk.utils.json_parsing import parse_structured_string

_OPENING_FENCE = re.compile(r"^```[A-Za-z0-9_-]*[ \t]*\r?\n")

_INSTALLED = False


def _strip_code_fence(text: str) -> str:
    """Drop one wrapping ```json fence, leaving any fences INSIDE the payload alone."""
    stripped = text.strip()
    match = _OPENING_FENCE.match(stripped)
    if not match:
        return stripped
    body = stripped[match.end():]
    if body.rstrip().endswith("```"):
        body = body.rstrip()[:-3]
    return body.strip()


def _iter_json_objects(text: str) -> List[str]:
    """Top-level ``{...}`` slices, counting braces only outside string literals."""
    objects: List[str] = []
    depth = 0
    start = -1
    in_str = escape = False
    for i, ch in enumerate(text):
        if in_str:
            if escape:
                escape = False
            elif ch == "\\":
                escape = True
            elif ch == '"':
                in_str = False
            continue
        if ch == '"':
            in_str = True
        elif ch == "{":
            if depth == 0:
                start = i
            depth += 1
        elif ch == "}":
            if depth:
                depth -= 1
                if depth == 0 and start != -1:
                    objects.append(text[start:i + 1])
                    start = -1
    return objects


def lenient_structured_parse(content: str) -> Optional[dict]:
    """Parse `content` into a dict keeping literal newlines; None defers to agno."""
    if not isinstance(content, str) or not content.strip():
        return None
    body = content
    # reasoning models put the envelope after their thinking, exactly as agno assumes
    if "</think>" in body:
        body = body.rsplit("</think>", 1)[-1]
    body = _strip_code_fence(body)
    direct = parse_structured_string(body)
    if isinstance(direct, dict):
        return direct
    candidates = _iter_json_objects(body)
    # several objects: agno merges them field by field - leave that path to agno
    if len(candidates) != 1:
        return None
    parsed = parse_structured_string(candidates[0])
    return parsed if isinstance(parsed, dict) else None


def _nothing_to_parse(content: Any) -> bool:
    """True when no parser could extract anything: empty or brace-less non-JSON text."""
    if not isinstance(content, str):
        return False
    if not content.strip():
        return True
    if "{" in content or "[" in content:
        return False
    try:
        # a bare scalar ("true", "42", a quoted string) is agno's to handle
        json.loads(content)
        return False
    except Exception:
        return True


def _patch_parse_response_model_str(original: Callable) -> Callable:
    """Wrap agno's schema parser with the lenient tier, falling back to `original`."""

    def parse_response_model_str(content: Any, output_schema: Any) -> Optional[Any]:
        # streaming feeds every narration/empty turn here - skip agno's warning chain
        if _nothing_to_parse(content):
            return None
        try:
            data = lenient_structured_parse(content)
            if data is not None:
                return output_schema.model_validate(data)
        except Exception:
            pass
        return original(content, output_schema)

    return parse_response_model_str


def _patch_parse_response_dict_str(original: Callable) -> Callable:
    """Wrap agno's dict parser with the lenient tier, falling back to `original`."""

    def parse_response_dict_str(content: Any) -> Optional[dict]:
        if _nothing_to_parse(content):
            return None
        try:
            data = lenient_structured_parse(content)
            if data is not None:
                return data
        except Exception:
            pass
        return original(content)

    return parse_response_dict_str


# agno's response modules bind these names at import time, so patching
# agno.utils.string alone would never reach the code that actually runs.
_TARGET_MODULES = (
    "agno.utils.string",
    "agno.agent._response",
    "agno.team._response",
    "agno.memory.manager",
    "agno.session.summary",
)

_PATCHERS = {
    "parse_response_model_str": _patch_parse_response_model_str,
    "parse_response_dict_str": _patch_parse_response_dict_str,
}


def install_agno_output_parsing_patch() -> bool:
    """Make agno's parsing keep literal newlines; safe to call repeatedly."""
    global _INSTALLED
    if _INSTALLED:
        return True
    import importlib

    reached_agno = False
    for module_name in _TARGET_MODULES:
        try:
            module = importlib.import_module(module_name)
        except Exception:
            continue
        for attr, wrap in _PATCHERS.items():
            original = getattr(module, attr, None)
            if original is None:
                continue
            reached_agno = True
            if getattr(original, "_xpander_lenient", False):
                continue
            replacement = wrap(original)
            replacement._xpander_lenient = True  # type: ignore[attr-defined]
            setattr(module, attr, replacement)
    # only latch once the patch is really in effect, so a failed import can retry later
    _INSTALLED = reached_agno
    if not reached_agno:
        logger.debug("[agno-parsing] patch not installed - agno parsers unreachable")
    return reached_agno
