import re
from typing import Optional

# Forward-promise openings a run must never END on ("I will read X... then proceed").
_PROMISE_RE = re.compile(
    r"\b(i\s+will|i'll|i\s+am\s+going\s+to|let\s+me\s+(?:first|now|start|begin))\b",
    re.IGNORECASE,
)
_PROMISE_ONLY_MAX_CHARS = 600

PROMISE_CONTINUATION_NUDGE = (
    "<continuation>Your previous message was a promise, not an outcome. "
    "Do not narrate intent - execute the work NOW with tool calls, then "
    "answer with what you actually did and found.</continuation>"
)


def is_promise_only_answer(text: Optional[str], tool_call_count: int) -> bool:
    """True when a run's final answer is a short forward promise made with ZERO tool calls.

    Conservative on purpose: a legitimate tool-free Q&A answer is long or promise-free;
    a long answer that merely contains "I will" is substance, not a promise.
    """
    if tool_call_count > 0:
        return False
    stripped = (text or "").strip()
    if not stripped or len(stripped) > _PROMISE_ONLY_MAX_CHARS:
        return False
    # A question to the user is a legitimate stop - nudging would act instead of waiting.
    if "?" in stripped:
        return False
    return bool(_PROMISE_RE.search(stripped))
