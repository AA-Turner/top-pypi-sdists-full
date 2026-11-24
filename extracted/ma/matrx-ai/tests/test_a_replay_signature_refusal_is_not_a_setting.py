"""A provider refusing replayed reasoning material is never reported as a rejected SETTING.

Live 2026-11-19 (conversation 735c85b2, request 9216c6dd): Gemini answered a replayed turn with
400 INVALID_ARGUMENT "Invalid thought signature." (reason INVALID_THOUGHT_SIGNATURE). The cause was
history content (search-step parts replayed as signed empty thoughts), yet the setting-rejection net
filed a ``provider_setting_rejected`` row blaming ``config.automatic_continuation`` — sending the fixer
after a knob that had nothing to do with it. Signatures and encrypted reasoning are message content.
"""

from __future__ import annotations

import pytest
from google.genai import errors as genai_errors

from matrx_ai.providers import setting_rejection
from matrx_ai.providers.errors import classify_provider_error

_GOOGLE_BODY = {
    "error": {
        "code": 400,
        "message": "Invalid thought signature.",
        "status": "INVALID_ARGUMENT",
        "details": [
            {
                "@type": "type.googleapis.com/google.rpc.ErrorInfo",
                "reason": "INVALID_THOUGHT_SIGNATURE",
                "domain": "generativelanguage.googleapis.com",
            }
        ],
    }
}


def test_googles_invalid_thought_signature_is_not_a_setting_rejection() -> None:
    info = classify_provider_error("google", genai_errors.ClientError(400, _GOOGLE_BODY))
    assert setting_rejection.net_candidate(info) is None


@pytest.mark.parametrize(
    "message",
    [
        "Invalid thought signature.",
        "messages.1.content.0: Invalid `signature` in `thinking` block",
        "The encrypted content for item rs_123 could not be verified.",
    ],
)
def test_no_replayed_reasoning_refusal_reaches_the_setting_net(message: str) -> None:
    assert setting_rejection._NET_NOT_A_SETTING.search(message), message


def test_a_real_unnamed_setting_refusal_still_reaches_the_net() -> None:
    assert not setting_rejection._NET_NOT_A_SETTING.search("`glimmer` is out of band for this deployment")
