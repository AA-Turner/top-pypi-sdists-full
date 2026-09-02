"""
Token counting utilities.

Uses tiktoken for OpenAI-compatible models. Falls back to a simple character-based
approximation (÷4) for other providers.

Mirrors: packages/memory/src/processors/observational-memory/token-counter.ts
(TS uses the 'tokenx' package — a fast regex-based counter.)
"""

from __future__ import annotations

import re
from functools import lru_cache
from typing import Optional


# ---------------------------------------------------------------------------
# tiktoken-based counter (preferred, accurate)
# ---------------------------------------------------------------------------

def _try_import_tiktoken():
    try:
        import tiktoken
        return tiktoken
    except ImportError:
        return None


@lru_cache(maxsize=8)
def _get_encoding(model_or_encoding: str):
    tiktoken = _try_import_tiktoken()
    if tiktoken is None:
        return None
    try:
        return tiktoken.encoding_for_model(model_or_encoding)
    except KeyError:
        try:
            return tiktoken.get_encoding(model_or_encoding)
        except Exception:
            return None


def count_tokens_tiktoken(text: str, model: str = "gpt-4o") -> Optional[int]:
    """Count tokens using tiktoken. Returns None if tiktoken is unavailable."""
    enc = _get_encoding(model)
    if enc is None:
        return None
    return len(enc.encode(text))


# ---------------------------------------------------------------------------
# Approximate counter (no dependencies)
# ---------------------------------------------------------------------------

# Rough approximation: average 4 chars per token.
# Slightly better: count whitespace-separated words * 1.3
_WORD_RE = re.compile(r"\S+")


def count_tokens_approx(text: str) -> int:
    """
    Fast approximate token count with no dependencies.
    
    Uses word count × 1.3 as a rough heuristic (~10-20% error).
    For JSON-heavy content (tool calls), accuracy may be lower.
    """
    words = _WORD_RE.findall(text)
    return max(1, round(len(words) * 1.3))


# ---------------------------------------------------------------------------
# Public interface
# ---------------------------------------------------------------------------

class TokenCounter:
    """
    Token counter that prefers tiktoken when available, falls back to approximation.
    
    Construct once and reuse — tiktoken encoding is loaded once and cached.
    """

    def __init__(self, model: str = "gpt-4o") -> None:
        self.model = model
        self._use_tiktoken = _try_import_tiktoken() is not None

    def count(self, text: str) -> int:
        """Return the token count for text."""
        if not text:
            return 0
        if self._use_tiktoken:
            result = count_tokens_tiktoken(text, self.model)
            if result is not None:
                return result
        return count_tokens_approx(text)

    def count_messages(self, messages: list[dict]) -> int:
        """Count tokens across a list of {role, content} dicts."""
        total = 0
        for msg in messages:
            content = msg.get("content", "")
            if isinstance(content, str):
                total += self.count(content)
            elif isinstance(content, list):
                for part in content:
                    if isinstance(part, dict) and "text" in part:
                        total += self.count(part["text"])
                    elif isinstance(part, str):
                        total += self.count(part)
            # Add a small overhead per message (role tokens, formatting)
            total += 4
        return total


# ---------------------------------------------------------------------------
# Module-level default counter (gpt-4o encoding, ~compatible with Gemini/Claude)
# ---------------------------------------------------------------------------

_default_counter = TokenCounter(model="gpt-4o")


def count_tokens(text: str) -> int:
    """Count tokens using the default counter (gpt-4o encoding)."""
    return _default_counter.count(text)
