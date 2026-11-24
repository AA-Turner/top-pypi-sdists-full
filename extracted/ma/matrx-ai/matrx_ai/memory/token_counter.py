"""
Token counting utilities.

Uses tiktoken for OpenAI-compatible models. Falls back to a simple character-based
approximation (÷4) for other providers.

Mirrors: packages/memory/src/processors/observational-memory/token-counter.ts
(TS uses the 'tokenx' package — a fast regex-based counter.)
"""

from __future__ import annotations

import asyncio
import re
import threading
from functools import lru_cache

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


# AN ENCODING NEVER LOADS ON THE EVENT LOOP (2026-11-11). tiktoken's first ``get_encoding`` downloads the BPE file
# (o200k_base is ~3.6 MB from openaipublic) with a blocking ``requests.get`` and then parses it; in production that
# ran inside the send boundary's token estimate and froze the whole server for 1.1-3.9s on every fresh container
# (event_loop_stall aidream-api:698eecc767d01e9e). On a loop thread a not-yet-loaded encoding is loaded in a worker
# thread instead and this call answers ``None`` (every caller then counts by its approximation); off the loop it loads
# in place, as before.
_loaded: set[str] = set()
_loading: set[str] = set()
_loading_lock = threading.Lock()


def _on_event_loop_thread() -> bool:
    try:
        asyncio.get_running_loop()
    except RuntimeError:
        return False
    return True


def _load_in_background(model_or_encoding: str) -> None:
    with _loading_lock:
        if model_or_encoding in _loading or model_or_encoding in _loaded:
            return
        _loading.add(model_or_encoding)

    def _load() -> None:
        try:
            _get_encoding(model_or_encoding)
            _loaded.add(model_or_encoding)
        finally:
            with _loading_lock:
                _loading.discard(model_or_encoding)

    threading.Thread(target=_load, name=f"tiktoken-load-{model_or_encoding}", daemon=True).start()


def _encoding_without_blocking_the_loop(model_or_encoding: str):
    if model_or_encoding in _loaded:
        return _get_encoding(model_or_encoding)
    if _on_event_loop_thread():
        _load_in_background(model_or_encoding)
        return None
    enc = _get_encoding(model_or_encoding)
    _loaded.add(model_or_encoding)
    return enc


def count_tokens_tiktoken(text: str, model: str = "gpt-4o") -> int | None:
    """Count tokens using tiktoken. Returns None if tiktoken is unavailable, or while the encoding is still loading
    in a worker thread (a call on the event loop never loads it there)."""
    enc = _encoding_without_blocking_the_loop(model)
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
