"""A provider refusing a call because the PLATFORM's account has no credit is a
named, non-retryable ``billing_error`` — for every provider classifier.

Break this guards (live 2026-10-01, request 5c4a458e…): OpenAI raised a bare
``openai.APIError`` ("You have no credits remaining…") with no status code; the
classifier fell through to the string fallback, called it a retryable
``unknown_error``, retried it 3× and told the person "An unexpected OpenAI error
occurred". Any provider wording that reaches the fallback (or a 429/403/401
branch) without being recognised as a billing refusal turns these red.

Every message below is the provider's own wording for an out-of-credit or
quota-exhausted account. The negative controls are genuine traffic limits that
MUST stay retryable — so a classifier that calls everything billing goes red too.
"""

from __future__ import annotations

from types import SimpleNamespace

import anthropic
import groq
import httpx
import openai
import pytest
from google.genai.errors import ClientError

from matrx_ai.providers.errors import RetryableError, classify_provider_error

_REQ = httpx.Request("POST", "https://provider.invalid/v1/responses")


def _resp(status: int) -> httpx.Response:
    return httpx.Response(status, request=_REQ)


class _StatusError(Exception):
    """An SDK-less provider error: status + JSON body (ElevenLabs/Cerebras shape)."""

    def __init__(self, status_code: int, message: str, body: object | None = None) -> None:
        super().__init__(message)
        self.status_code = status_code
        self.body = body
        self.response = SimpleNamespace(headers={})


OPENAI_NO_CREDITS = (
    "You have no credits remaining. Add credits to continue using the API at "
    "https://platform.openai.com/settings/organization/billing/."
)
QUOTA_EXCEEDED = (
    "You exceeded your current quota, please check your plan and billing details. "
    "For more information on this error, read the docs: "
    "https://platform.openai.com/docs/guides/error-codes/api-errors."
)


def _google(status_code: int, status: str, message: str) -> ClientError:
    return ClientError(
        status_code,
        {"error": {"code": status_code, "message": message, "status": status}},
    )


BILLING_REFUSALS: list[tuple[str, str, Exception]] = [
    # The live incident: a mid-stream APIError with no status code.
    ("openai", "OpenAI", openai.APIError(OPENAI_NO_CREDITS, _REQ, body=None)),
    (
        "openai",
        "OpenAI",
        openai.RateLimitError(
            f"Error code: 429 - {QUOTA_EXCEEDED}",
            response=_resp(429),
            body={"message": QUOTA_EXCEEDED, "type": "insufficient_quota", "code": "insufficient_quota"},
        ),
    ),
    (
        "anthropic",
        "Anthropic",
        anthropic.APIError(
            "Your credit balance is too low to access the Anthropic API. "
            "Please go to Plans & Billing to upgrade or purchase credits.",
            _REQ,
            body=None,
        ),
    ),
    (
        "google",
        "Google",
        _google(
            403,
            "PERMISSION_DENIED",
            "This API method requires billing to be enabled. Please enable billing on project "
            "#418273650912 by visiting https://console.developers.google.com/billing/enable?"
            "project=418273650912 then retry.",
        ),
    ),
    (
        "google",
        "Google",
        _google(
            429,
            "RESOURCE_EXHAUSTED",
            "Your prepayment credits are depleted. Please go to AI Studio at "
            "https://ai.studio/projects to manage your project and billing.",
        ),
    ),
    (
        "groq",
        "Groq",
        groq.APIStatusError(
            "Error code: 402 - Your organization has insufficient balance.",
            response=_resp(402),
            body={"error": {"message": "Your organization has insufficient balance.", "type": "insufficient_balance"}},
        ),
    ),
    (
        "xai",
        "xAI",
        openai.PermissionDeniedError(
            "Error code: 403 - Your newly created team doesn't have any credits yet. "
            "You can purchase credits on https://console.x.ai/team/default.",
            response=_resp(403),
            body=None,
        ),
    ),
    (
        "together",
        "Together AI",
        openai.APIStatusError(
            "Error code: 402 - Credit limit exceeded. Please navigate to "
            "https://api.together.xyz/settings/billing to add credit or upgrade your plan.",
            response=_resp(402),
            body=None,
        ),
    ),
    ("cerebras", "Cerebras", _StatusError(402, "Payment Required")),
    # Gemini prepay depleted now answers HTTP 402 (Google AI forum, API update
    # "Depleted prepay credits now return HTTP 402 instead of 429").
    (
        "google",
        "Google",
        _StatusError(
            402,
            "Your prepayment credits are depleted. Please go to AI Studio at "
            "https://ai.studio/projects to manage your project and billing.",
        ),
    ),
    # Cohere's documented 402 body, but reaching us as a bare string error.
    (
        "cohere",
        "Cohere",
        RuntimeError(
            "Maximum billing reached for this API key as set in your dashboard, please go to "
            "https://dashboard.cohere.com/billing?tab=payment to increase your maximum amount."
        ),
    ),
    (
        "huggingface",
        "Hugging Face",
        openai.APIStatusError(
            "Error code: 402 - You have exceeded your monthly included credits for "
            "Inference Providers. Subscribe to PRO to get 20x more monthly included credits.",
            response=_resp(402),
            body=None,
        ),
    ),
    (
        "moonshot",
        "Moonshot",
        _StatusError(
            429,
            "Your account is suspended, please check your plan and billing details",
            {"error": {"type": "exceeded_current_quota_error", "message": "Your account is suspended, please check your plan and billing details"}},
        ),
    ),
    (
        "elevenlabs",
        "ElevenLabs",
        _StatusError(
            401,
            "status_code: 401, body: {'detail': {'status': 'quota_exceeded', 'message': "
            "'This request exceeds your quota of 10000. You have 35 credits remaining, "
            "while 210 credits are required for this request.'}}",
        ),
    ),
]


@pytest.mark.parametrize(
    ("provider", "display", "exc"),
    BILLING_REFUSALS,
    ids=[f"{p}-{i}" for i, (p, _, _) in enumerate(BILLING_REFUSALS)],
)
def test_out_of_credit_refusal_is_a_named_non_retryable_billing_error(
    provider: str, display: str, exc: Exception
) -> None:
    result = classify_provider_error(provider, exc)

    assert result.error_type == "billing_error", (provider, result.error_type, result.message)
    assert result.is_retryable is False
    # The person reads ONE plain sentence naming the provider and the
    # platform's account — never a billing URL they cannot use.
    assert result.user_message.startswith(f"{display} refused this request"), result.user_message
    assert f"the platform's {display} account" in result.user_message
    assert "http" not in result.user_message.lower()
    assert "retrying" not in result.user_message.lower()
    # The operator keeps the provider's raw words.
    assert result.message


def test_suspended_account_says_suspended_not_out_of_credit() -> None:
    result = classify_provider_error(
        "openai",
        openai.APIError("Your account is suspended. Contact support.", _REQ, body=None),
    )
    assert result.error_type == "billing_error"
    assert result.user_message == "OpenAI refused this request: the platform's OpenAI account is suspended."


def test_openai_no_credits_sentence_is_exact() -> None:
    result = classify_provider_error("openai", openai.APIError(OPENAI_NO_CREDITS, _REQ, body=None))
    assert result.user_message == "OpenAI refused this request: the platform's OpenAI account is out of credit."


TRAFFIC_LIMITS: list[tuple[str, Exception]] = [
    # Gemini's ORDINARY per-minute limit uses the same "current quota … plan and
    # billing details" words as a real quota refusal — it must stay retryable.
    (
        "google",
        _google(
            429,
            "RESOURCE_EXHAUSTED",
            "You exceeded your current quota, please check your plan and billing details. "
            "For more information on this error, head to: https://ai.google.dev/gemini-api/docs/rate-limits. "
            "Please retry in 21.4s.",
        ),
    ),
    (
        "openai",
        openai.RateLimitError(
            "Error code: 429 - Rate limit reached for gpt-5.4-nano on tokens per min (TPM): "
            "Limit 200000, Used 199000, Requested 3000. Please try again in 1.2s.",
            response=_resp(429),
            body={"type": "tokens", "code": "rate_limit_exceeded"},
        ),
    ),
    ("google", _google(429, "RESOURCE_EXHAUSTED", "Resource has been exhausted (e.g. check quota).")),
    (
        "anthropic",
        anthropic.RateLimitError(
            "Error code: 429 - This request would exceed the rate limit for your organization "
            "of 400,000 input tokens per minute.",
            response=_resp(429),
            body=None,
        ),
    ),
]


@pytest.mark.parametrize(
    ("provider", "exc"), TRAFFIC_LIMITS, ids=[f"{p}-{i}" for i, (p, _) in enumerate(TRAFFIC_LIMITS)]
)
def test_a_traffic_limit_stays_a_retryable_rate_limit(provider: str, exc: Exception) -> None:
    result: RetryableError = classify_provider_error(provider, exc)
    assert result.error_type == "rate_limit"
    assert result.is_retryable is True


@pytest.mark.parametrize(
    ("provider", "sentence"),
    [
        ("replicate", "Replicate refused this request: the platform's Replicate account is out of credit."),
        ("unknown", "The AI provider refused this request: the platform's account is out of credit."),
    ],
)
def test_a_provider_without_its_own_classifier_is_still_named_plainly(provider: str, sentence: str) -> None:
    result = classify_provider_error(provider, _StatusError(402, "Payment Required"))
    assert result.error_type == "billing_error"
    assert result.user_message == sentence


def test_a_timeout_is_never_billing_whatever_its_text() -> None:
    exc = httpx.ReadTimeout("insufficient balance check timed out while reading the response")
    result = classify_provider_error("openai", exc)
    assert result.error_type == "provider_timeout"
    assert result.is_retryable is True


def test_the_operator_key_stays_the_routing_key() -> None:
    """Telemetry (_issue_key, details.provider) keys on the routing key."""
    result = classify_provider_error("together", _StatusError(402, "Payment Required"))
    assert result.details["provider"] == "together"
    assert result.user_message.startswith("Together AI refused this request")
