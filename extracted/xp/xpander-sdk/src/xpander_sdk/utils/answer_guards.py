import re
from typing import Optional

# Forward-promise openings a run must never END on ("I will read X... then proceed").
_PROMISE_RE = re.compile(
    r"\b(i\s+will|i'll|i\s+am\s+going\s+to|let\s+me\s+(?:first|now|start|begin))\b",
    re.IGNORECASE,
)
# Openings only: "on it" / "checking" mid-sentence are legitimate prose ("Sarah is
# working on it"); as the answer's first words they are the observed zero-tool promise.
_PROMISE_OPENING_RE = re.compile(
    r"^\W{0,8}(on\s+it\b|checking\b|looking\s+into\b)",
    re.IGNORECASE,
)
# Mid-work promise shapes ("Now generating the classification...") - a run that ENDS
# on one of these produced activity but no outcome, regardless of tool count. Anchored
# to the answer's OPENING: mid-sentence "is now running" describes achieved state
# ("Deployed. The service is now running.") and must never trigger a re-drive.
_PROMISE_PROGRESS_RE = re.compile(
    r"^\W{0,8}(?:i(?:'m| am| will)?\s+)?"
    r"(now\s+(?:generating|running|executing|building|creating|processing)"
    r"|proceeding\s+to|about\s+to\s+(?:generate|run|execute|build|create|write))\b",
    re.IGNORECASE,
)
_PROMISE_ONLY_MAX_CHARS = 600

PROMISE_CONTINUATION_NUDGE = (
    "<continuation>Your previous message was a promise, not an outcome. "
    "Do not narrate intent - execute the work NOW with tool calls, then "
    "answer with what you actually did and found.</continuation>"
)


def is_promise_only_answer(text: Optional[str], tool_call_count: int) -> bool:
    """True when a run's final answer is a short forward promise instead of an outcome.

    Conservative on purpose: a legitimate answer is long or promise-free; a long answer
    that merely contains "I will" is substance, not a promise. Runs WITH tool calls are
    caught too - a run that worked for minutes then ended on "Now generating..." produced
    activity but no outcome (the mandated artifact never happened).
    """
    stripped = (text or "").strip()
    if not stripped or len(stripped) > _PROMISE_ONLY_MAX_CHARS:
        return False
    # A question to the user is a legitimate stop - nudging would act instead of waiting.
    if "?" in stripped:
        return False
    if _PROMISE_PROGRESS_RE.match(stripped):
        return True
    # The bare-promise shapes stay zero-tool-only: with real work done, a short
    # "let me now..."-style line is usually a trailing narration, not the whole answer.
    if tool_call_count > 0:
        return False
    return bool(_PROMISE_RE.search(stripped)) or bool(_PROMISE_OPENING_RE.match(stripped))
