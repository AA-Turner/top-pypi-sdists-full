"""A provider error's user_message never claims a retry is happening.

``RetryableError.user_message`` is read on TERMINAL paths — the stream ``error``
event, the request row's ``error`` and the failed assistant turn's stored
content. On 2026-10-01 an "Extract Key Points" run on a busy OpenAI ended with
the saved answer reading "An unexpected OpenAI error occurred. Retrying..." —
a screen claiming a retry that was not happening, persisted as the answer.

The in-flight phrasing lives in ``retry_notice`` and is composed only by
``retrying_message`` where a retry is really scheduled.
"""

from __future__ import annotations

import ast
import re
from pathlib import Path

import httpx
import pytest

from matrx_ai.providers.errors import RetryableError, classify_provider_error

# A claim that a retry is happening or scheduled — not advice ("try again")
# and not a statement that nothing was retried.
_RETRY_CLAIM = re.compile(r"\bretrying\b|\bretr(y|ies) (automatically|in \d)|\bwill retry\b", re.I)
_PACKAGE = Path(__file__).resolve().parents[1] / "matrx_ai"

_PROVIDERS = ["openai", "anthropic", "google", "xai", "groq", "together", "cerebras", "unknown"]
_EXCEPTIONS = [
    RuntimeError("something odd happened upstream"),
    RuntimeError("429 rate limit exceeded"),
    RuntimeError("503 service unavailable"),
    RuntimeError("500 internal server error"),
    RuntimeError("529 overloaded"),
    RuntimeError("504 gateway timeout"),
    httpx.ReadError(""),
    httpx.ConnectError("connection refused"),
]


def _claims_retry(text: str) -> bool:
    return bool(_RETRY_CLAIM.search(text or ""))


def test_the_observed_sentence_is_honest_after_the_last_attempt() -> None:
    classified = classify_provider_error("openai", RuntimeError("something odd happened upstream"))
    assert classified.is_retryable is True
    assert classified.user_message == "An unexpected OpenAI error occurred."
    assert _claims_retry(classified.retrying_message)


def test_default_user_message_names_the_condition_only() -> None:
    assert not _claims_retry(RetryableError(error_type="x", message="y").user_message)


@pytest.mark.parametrize("provider", _PROVIDERS)
@pytest.mark.parametrize("exc", _EXCEPTIONS, ids=lambda e: f"{type(e).__name__}:{e}")
def test_no_classified_error_claims_a_retry(provider: str, exc: Exception) -> None:
    classified = classify_provider_error(provider, exc)
    assert not _claims_retry(classified.user_message), classified.user_message
    if classified.is_retryable:
        assert _claims_retry(classified.retrying_message), classified.retrying_message


def _literal_text(node: ast.expr) -> str:
    parts: list[str] = []
    for sub in ast.walk(node):
        if isinstance(sub, ast.Constant) and isinstance(sub.value, str):
            parts.append(sub.value)
    return " ".join(parts)


def test_no_retryable_error_construction_writes_retry_wording_into_user_message() -> None:
    offenders: list[str] = []
    for path in _PACKAGE.rglob("*.py"):
        tree = ast.parse(path.read_text(encoding="utf-8"))
        for node in ast.walk(tree):
            if not isinstance(node, ast.Call):
                continue
            name = getattr(node.func, "id", None) or getattr(node.func, "attr", None)
            if name != "RetryableError":
                continue
            for kw in node.keywords:
                if kw.arg == "user_message" and _claims_retry(_literal_text(kw.value)):
                    offenders.append(f"{path.relative_to(_PACKAGE)}:{node.lineno}")
    assert not offenders, (
        "RetryableError.user_message must name the condition only; put in-flight "
        f"phrasing in retry_notice: {offenders}"
    )
