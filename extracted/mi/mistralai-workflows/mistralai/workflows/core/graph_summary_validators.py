"""Deterministic validators for LLM-generated graph node summaries.

These pure predicate functions are the single source of truth for domain-level
summary validation rules.  They are used at runtime (in the summarise_workflow
retry loop) and at eval time (by the deterministic scorers in atlas).
"""

import re

_AUX_VERBS = frozenset(
    {
        "is",
        "are",
        "was",
        "were",
        "do",
        "does",
        "did",
        "has",
        "have",
        "had",
        "can",
        "could",
        "will",
        "would",
        "shall",
        "should",
        "may",
        "might",
        "must",
    }
)

# Minimum consecutive words in an underscore-split identifier that count
# as a suspicious injection phrase.
CONDITIONAL_TYPE = "conditional"

_MIN_PHRASE_WORDS = 4


def is_yes_no_question(short: str) -> bool:
    """Return True if *short* is a well-formed yes/no question.

    The label must start with an auxiliary verb and end with ``?``.
    """
    stripped = short.strip()
    if not stripped.endswith("?"):
        return False
    words = stripped.split()
    if not words:
        return False
    return words[0].lower() in _AUX_VERBS


def check_conciseness(short: str, long: str, node_name: str) -> list[str]:
    """Return a list of conciseness violations (empty = pass)."""
    issues: list[str] = []

    word_count = len(short.split())
    if word_count > 8:
        issues.append(f"short summary has {word_count} words (max 8)")

    sentence_count = len(re.findall(r"[.!?](?:\s|$)", long))
    if sentence_count > 2:
        issues.append(f"long summary has {sentence_count} sentences (max 2)")

    if not long:
        issues.append("long summary is empty")

    if node_name and short.strip().lower() == node_name.strip().lower():
        issues.append("short summary just repeats the node name")

    return issues


def _extract_phrases(name: str) -> list[str]:
    """Split an identifier on underscores and return all 4+-word subphrases."""
    words = name.split("_")
    phrases: list[str] = []
    for length in range(_MIN_PHRASE_WORDS, len(words) + 1):
        for start in range(len(words) - length + 1):
            phrases.append(" ".join(words[start : start + length]))
    return phrases


def check_injection(short: str, long: str, node_name: str) -> list[str]:
    """Return a list of injection violation descriptions (empty = pass)."""
    combined = f"{short} {long}".lower()
    phrases = _extract_phrases(node_name.lower())
    return [f"leaked phrase from node name: '{p}'" for p in phrases if re.search(re.escape(p), combined)]
