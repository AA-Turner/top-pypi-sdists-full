"""The catch-all error sentence shows the provider's own words; credentials and emails in them are masked first."""
from __future__ import annotations

import pytest

from matrx_ai.providers.errors import _provider_words

SECRETS = [
    "Incorrect API key provided: sk-proj-abcdEFGH1234567890xyz",
    "request failed key=AbCdEf123456 retry",
    "Authorization: Bearer eyJhbGciOiJIUzI1NiJ9.payload.sig",
    "bad header Bearer abc123DEF456ghi",
    "invalid key AIzaSyA1b2C3d4E5f6G7h8I9j0K",
    "auth xai-AbCdEf1234567890",
    "blob 0123456789abcdef0123456789abcdef01234567 end",
    "contact jane.roe@example.com for access",
]
MARKERS = ["sk-proj", "AbCdEf123456", "eyJhbGci", "abc123DEF456ghi", "AIzaSy", "xai-AbCd", "0123456789abcdef0123", "jane.roe@"]


@pytest.mark.parametrize(("raw", "marker"), list(zip(SECRETS, MARKERS)))
def test_a_secret_never_reaches_the_sentence(raw: str, marker: str) -> None:
    out = _provider_words(raw)
    assert marker not in out, out
    assert "[hidden]" in out


def test_plain_words_pass_through_untouched() -> None:
    assert _provider_words("The model is overloaded, try again") == "The model is overloaded, try again"
