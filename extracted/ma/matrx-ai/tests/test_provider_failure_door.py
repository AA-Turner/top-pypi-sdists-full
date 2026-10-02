"""Every dispatched provider failure reaches the operator through ONE door.

SUT: ``UnifiedAIClient._dispatch_with_billing_net`` (the seam chat, image,
video and extraction calls share) and ``report_provider_failure`` (the door).
Double: ``capture_error`` (the system_error writer) and the dispatch itself
(raises the provider's real SDK error).

Breaks named:
* the out-of-credit alarm lives only in the text orchestrator → an image or
  video call on an exhausted account files nothing (the gap found 2026-10-01);
* two layers each file a row for the same failure → the operator class
  double-counts;
* the seam swallows or replaces the provider's exception;
* a non-billing failure is filed under the out-of-credit class.
"""

from __future__ import annotations

import asyncio
from types import SimpleNamespace
from typing import Any

import httpx
import openai
import pytest
from google.genai.errors import ClientError

from matrx_ai.providers.failure_report import report_provider_failure
from matrx_ai.providers.unified_client import UnifiedAIClient

_OUT_OF_CREDIT_KIND = "provider_account_out_of_credit"  # literal: the surfaces collapse by it
_REQ = httpx.Request("POST", "https://api.openai.com/v1/images/generations")


def _profile(vendor: str, model: str) -> SimpleNamespace:
    return SimpleNamespace(
        vendor=vendor, model_name=model, endpoint_id=f"{vendor}-test", base_url=None, offering_metadata={}
    )


@pytest.fixture
def captured(monkeypatch: pytest.MonkeyPatch) -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []

    async def capture_error(exc: BaseException, **kwargs: Any) -> None:
        rows.append({"exc": exc, **kwargs})

    monkeypatch.setattr("matrx_connect.streaming.error_capture.capture_error", capture_error)
    return rows


def _dispatch(exc: BaseException, profile: SimpleNamespace) -> BaseException | None:
    async def _boom() -> Any:
        raise exc

    async def _run() -> BaseException | None:
        try:
            await UnifiedAIClient._dispatch_with_billing_net(_boom, profile=profile)
        except BaseException as raised:  # noqa: BLE001
            return raised
        return None

    return asyncio.run(_run())


_MEDIA_REFUSALS = [
    pytest.param(
        openai.APIStatusError(
            "Error code: 429 - You exceeded your current quota.",
            response=httpx.Response(429, request=_REQ),
            body={"error": {"message": "You exceeded your current quota.", "type": "insufficient_quota", "code": "insufficient_quota"}},
        ),
        _profile("openai", "gpt-image-2"),
        "openai",
        id="openai-image",
    ),
    pytest.param(
        ClientError(
            429,
            {"error": {"code": 429, "status": "RESOURCE_EXHAUSTED",
                       "message": "Your prepayment credits are depleted. Please go to AI Studio to manage your project and billing."}},
        ),
        _profile("google", "veo-3.1"),
        "google",
        id="google-video",
    ),
]


@pytest.mark.parametrize(("exc", "profile", "provider"), _MEDIA_REFUSALS)
def test_a_media_call_on_an_exhausted_account_files_the_alarm(captured, exc, profile, provider) -> None:
    raised = _dispatch(exc, profile)
    assert raised is exc, "the seam must re-raise the provider's exception untouched"
    alarms = [row for row in captured if row["kind"] == _OUT_OF_CREDIT_KIND]
    assert len(alarms) == 1
    assert alarms[0]["error_type"] == f"{provider}.billing_error"
    assert alarms[0]["payload"]["model"] == profile.model_name


def test_a_second_layer_does_not_file_a_second_row(captured) -> None:
    exc = openai.APIError("You have no credits remaining.", _REQ, body=None)
    _dispatch(exc, _profile("openai", "gpt-5.4-nano"))
    # The orchestrator reports the same failure again with its own identity.
    asyncio.run(report_provider_failure(exc, provider="openai", route="orchestrator/provider_request"))
    assert [row["kind"] for row in captured].count(_OUT_OF_CREDIT_KIND) == 1


def test_a_traffic_limit_is_not_filed_as_out_of_credit(captured) -> None:
    exc = openai.RateLimitError(
        "Error code: 429 - Rate limit reached for gpt-image-2 on images per minute. Please try again in 6s.",
        response=httpx.Response(429, request=_REQ),
        body={"type": "requests", "code": "rate_limit_exceeded"},
    )
    raised = _dispatch(exc, _profile("openai", "gpt-image-2"))
    assert raised is exc
    assert [row for row in captured if row["kind"] == _OUT_OF_CREDIT_KIND] == []


def test_a_batched_call_files_one_row_per_request(captured, monkeypatch) -> None:
    """A batched embed gathers ~50 batches; each raises its OWN exception. One
    exhausted account on one person's action is one row, not fifty — while a
    different request, or a different provider, still gets its own."""
    from matrx_connect.context.app_context import AppContext, clear_app_context, set_app_context

    def _refusal() -> openai.APIError:
        return openai.APIError("You have no credits remaining.", _REQ, body=None)

    async def _run(request_id: str, provider: str, n: int) -> None:
        token = set_app_context(AppContext(emitter=None, user_id="e4687a9c-acf7-469f-aa12-860eb4d948d0", request_id=request_id))
        try:
            await asyncio.gather(*(report_provider_failure(_refusal(), provider=provider) for _ in range(n)))
        finally:
            clear_app_context(token)

    asyncio.run(_run("7c1f0e2a-5d3b-4e8f-9a61-2b4c6d8e0f13", "openai", 50))
    asyncio.run(_run("7c1f0e2a-5d3b-4e8f-9a61-2b4c6d8e0f13", "openai", 5))
    asyncio.run(_run("0b9e4d21-8c7a-4f36-b5e2-91d3a6c48f70", "openai", 3))
    asyncio.run(_run("0b9e4d21-8c7a-4f36-b5e2-91d3a6c48f70", "together", 2))

    rows = [(r["request_id"], r["error_type"]) for r in captured if r["kind"] == _OUT_OF_CREDIT_KIND]
    assert rows == [
        ("7c1f0e2a-5d3b-4e8f-9a61-2b4c6d8e0f13", "openai.billing_error"),
        ("0b9e4d21-8c7a-4f36-b5e2-91d3a6c48f70", "openai.billing_error"),
        ("0b9e4d21-8c7a-4f36-b5e2-91d3a6c48f70", "together.billing_error"),
    ]
