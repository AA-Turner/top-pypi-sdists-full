"""Provider-error classification for context-window overflows.

Used by Layer 2 to decide whether to fall through to the chunked map-reduce
path and to extract the provider-reported max-input-tokens hint so chunks
are sized to the provider's actual ceiling on the next attempt.
"""

import re
from typing import Optional

# Regex patterns that signal the LLM rejected the prompt because it exceeded
# the model context window. Covers Anthropic, OpenAI, vLLM / OpenAI-compat,
# Bedrock Claude, and Gemini. Matched against ``str(exc).lower()``.
_CONTEXT_OVERFLOW_PATTERNS = [
    re.compile(r"prompt is too long", re.IGNORECASE),
    re.compile(r"context_length_exceeded", re.IGNORECASE),
    re.compile(r"maximum context length", re.IGNORECASE),
    re.compile(r"input length exceeds the context length", re.IGNORECASE),
    re.compile(r"input is too long for requested model", re.IGNORECASE),
    re.compile(r"input_length and max_tokens exceed context limit", re.IGNORECASE),
    re.compile(r"model's context length is only", re.IGNORECASE),
    re.compile(r"request_too_large", re.IGNORECASE),
]

# Patterns that extract the provider-reported maximum input tokens from the
# error message. Order matters: first match wins.
_MAX_TOKEN_PATTERNS = [
    # Anthropic: "prompt is too long: 6432565 tokens > 1000000 maximum"
    re.compile(r">\s*(\d{3,})\s*maximum", re.IGNORECASE),
    # Anthropic Bedrock: "input_length and max_tokens exceed context limit: A+B > 2000000"
    re.compile(r"context\s+limit[:\s]+[^>]*>\s*(\d{3,})", re.IGNORECASE),
    # OpenAI: "This model's maximum context length is 16385 tokens"
    re.compile(r"maximum context length is\s*(\d{3,})\s*tokens?", re.IGNORECASE),
    # vLLM-style: "model's context length is only 131072 tokens"
    re.compile(r"context length is only\s*(\d{3,})\s*tokens?", re.IGNORECASE),
]


def _is_context_overflow_error(exc: BaseException) -> bool:
    """Return True when *exc* looks like a provider context-window overflow."""
    try:
        text = str(exc)
    except Exception:
        return False
    if not text:
        return False
    for pat in _CONTEXT_OVERFLOW_PATTERNS:
        if pat.search(text):
            return True
    return False


def _parse_provider_max_tokens(exc: BaseException) -> Optional[int]:
    """Extract the provider-reported max input tokens from *exc*, if present."""
    try:
        text = str(exc)
    except Exception:
        return None
    if not text:
        return None
    for pat in _MAX_TOKEN_PATTERNS:
        m = pat.search(text)
        if m:
            try:
                return int(m.group(1))
            except Exception:
                continue
    return None
