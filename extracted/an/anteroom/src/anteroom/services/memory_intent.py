"""Deterministic handling for explicit user memory-save requests."""

from __future__ import annotations

import re
from dataclasses import dataclass


@dataclass(frozen=True)
class ExplicitMemoryIntent:
    """A narrow, user-explicit request to save a durable memory."""

    content: str
    category: str = "preference"
    scope: str = "user"


_SAVE_VERB_RE = re.compile(r"\b(?:remember|save|store)\b", re.IGNORECASE)
_MEMORY_WORD_RE = re.compile(r"\bmem(?:ory|ories|orry)\b", re.IGNORECASE)
_NAME_PATTERNS = (
    re.compile(
        r"^\s*(?:please\s+)?(?:remember|save|store)(?:\s+that)?\s+my\s+name\s+is\s+(.+?)(?:\s+as\s+a\s+mem(?:ory|orry))?[\s.!?]*$",
        re.IGNORECASE,
    ),
    re.compile(
        r"^\s*(?:please\s+)?(?:remember|save|store)\s+my\s+name\s+(.+?)(?:\s+as\s+a\s+mem(?:ory|orry))?[\s.!?]*$",
        re.IGNORECASE,
    ),
)
_REMEMBER_THAT_RE = re.compile(
    r"^\s*(?:please\s+)?(?:remember|save|store)\s+that\s+(.+?)[\s.!?]*$",
    re.IGNORECASE,
)


def detect_explicit_memory_intent(text: str) -> ExplicitMemoryIntent | None:
    """Return a memory intent only for explicit, stable user facts.

    This intentionally avoids becoming a broad "remember anything" parser.
    Ambiguous requests are left for the normal agent loop and model-facing
    ``save_memory`` guidance.
    """

    stripped = text.strip()
    if not stripped or stripped.startswith(("/", "!")):
        return None
    if "```" in stripped or "\n" in stripped:
        return None
    lowered = stripped.lower()
    if lowered.startswith(("what do you remember", "what did you remember", "do you remember")):
        return None
    if not _SAVE_VERB_RE.search(stripped):
        return None

    for pattern in _NAME_PATTERNS:
        match = pattern.match(stripped)
        if match:
            name = _clean_value(match.group(1))
            if _looks_like_person_name(name):
                return ExplicitMemoryIntent(content=f"User's name is {name}.")
            return None

    match = _REMEMBER_THAT_RE.match(stripped)
    if match and _MEMORY_WORD_RE.search(stripped):
        fact = _clean_value(match.group(1))
        if _is_stable_personal_fact(fact):
            return ExplicitMemoryIntent(content=_normalize_fact(fact))

    return None


def _clean_value(value: str) -> str:
    value = re.sub(r"\s+", " ", value).strip(" \t\r\n\"'")
    value = re.sub(r"\s+as\s+a\s+mem(?:ory|orry)\s*$", "", value, flags=re.IGNORECASE).strip()
    return value.rstrip(".!? ")


def _looks_like_person_name(value: str) -> bool:
    if not value or len(value) > 80:
        return False
    if any(token in value.lower() for token in (" as a ", " remember ", " save ", " store ")):
        return False
    return bool(re.fullmatch(r"[A-Za-z][A-Za-z' -]{0,78}[A-Za-z]", value))


def _is_stable_personal_fact(value: str) -> bool:
    if not value or len(value) > 220:
        return False
    lowered = value.lower()
    if lowered.startswith(("my name is ", "i am ", "i'm ", "i prefer ", "my preference is ")):
        return True
    return False


def _normalize_fact(value: str) -> str:
    value = _clean_value(value)
    name_prefix = re.match(r"my\s+name\s+is\s+(.+)$", value, re.IGNORECASE)
    if name_prefix:
        name = _clean_value(name_prefix.group(1))
        if _looks_like_person_name(name):
            return f"User's name is {name}."
    return value[:1].upper() + value[1:] + "."
