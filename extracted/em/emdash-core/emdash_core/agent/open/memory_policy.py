"""MemoryPolicy — Routing logic for memory writes.

Determines whether a piece of information should be stored as:
- **daily** → appended to today's rolling daily log
- **longterm** → appended to MEMORY.md (curated, durable)

Start with simple keyword heuristics. This can be upgraded to
LLM-based classification later.
"""

import re
from typing import Literal

MemoryTarget = Literal["daily", "longterm"]

# Patterns that strongly signal long-term storage
_LONGTERM_PATTERNS: list[re.Pattern] = [
    re.compile(r"\bremember\s+(this\s+)?forever\b", re.IGNORECASE),
    re.compile(r"\balways\s+(use|prefer|do|remember)\b", re.IGNORECASE),
    re.compile(r"\bnever\s+(use|do|forget)\b", re.IGNORECASE),
    re.compile(r"\bmy\s+preference\b", re.IGNORECASE),
    re.compile(r"\bi\s+(always|prefer|like|want)\b", re.IGNORECASE),
    re.compile(r"\bimportant\s*:\s", re.IGNORECASE),
    re.compile(r"\barchitecture\s+decision\b", re.IGNORECASE),
    re.compile(r"\bconvention\b", re.IGNORECASE),
    re.compile(r"\blong[- ]?term\b", re.IGNORECASE),
    re.compile(r"\bdurable\b", re.IGNORECASE),
    re.compile(r"\bpermanent\b", re.IGNORECASE),
]

# Keywords that weakly push toward long-term
_LONGTERM_KEYWORDS: set[str] = {
    "preference", "rule", "constraint", "standard", "guideline",
    "style", "convention", "policy", "principle", "decision",
}


def classify_memory(text: str) -> MemoryTarget:
    """Classify whether a memory write should go to daily log or MEMORY.md.

    Rules (in priority order):
    1. Strong pattern match (regex) → longterm
    2. Multiple keyword hits → longterm
    3. Default → daily

    Args:
        text: The memory content to classify.

    Returns:
        ``"longterm"`` or ``"daily"``.
    """
    # 1. Strong pattern match
    for pattern in _LONGTERM_PATTERNS:
        if pattern.search(text):
            return "longterm"

    # 2. Keyword density check
    text_lower = text.lower()
    hits = sum(1 for kw in _LONGTERM_KEYWORDS if kw in text_lower)
    if hits >= 2:
        return "longterm"

    # 3. Default to daily
    return "daily"
