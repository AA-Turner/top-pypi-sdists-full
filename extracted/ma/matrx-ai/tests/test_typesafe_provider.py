"""Forcing transport contracts for the native TypeSafe System One adapter."""

from __future__ import annotations

import json
from datetime import UTC, datetime, timedelta

import httpx
import pytest
from pydantic import ValidationError

from matrx_ai.providers.errors import get_billed_usage, was_billing_checked
from matrx_ai.providers.typesafe import (
    ChoiceQuestion,
    NoulQuestion,
    ScoreQuestion,
    SystemOneRequest,
    TypeSafeProviderError,
    call_system_one,
)
from matrx_ai.providers.typesafe.client import _retry_after


def _request() -> SystemOneRequest:
    return SystemOneRequest(
        state={"ticket": "I was billed twice and need help."},
        model="jev-1.13.0",
        questions={
            "billing": NoulQuestion(instructions="Is this about billing?"),
            "tone": ChoiceQuestion(
                instructions="What is the customer's tone?",
                criteria={"calm": "Neutral", "angry": "Expresses anger"},
            ),
            "urgency": ScoreQuestion(
                instructions="How urgent is this?",
                criteria=["can wait", "today", "immediate"],
            ),
        },
    )


def _result() -> dict[str, object]:
    return {
        "model": "jev-1.13.0",
        "request_id": "ts_123",
        "usage": {"input_tokens": 312, "output_tokens": 48},
        "answers": {
            "billing": {"type": "noul", "noul": 0.92},
            "tone": {
                "type": "choice",
                "choice": "angry",
                "probabilities": {"calm": 0.08, "angry": 0.92},
                "confidence": 0.84,
            },
            "urgency": {
                "type": "score",
                "score": 1.7,
                "legend": {"0": "can wait", "1": "today", "2": "immediate"},
                "probabilities": {"0": 0.05, "1": 0.2, "2": 0.75},
                "confidence": 0.78,
            },
        },
    }


@pytest.mark.asyncio
async def test_system_one_posts_the_official_typed_wire_contract() -> None:
    """Wrong endpoint, header, payload or answer correlation makes this fail."""
    seen: dict[str, object] = {}

    async def handler(request: httpx.Request) -> httpx.Response:
        seen["url"] = str(request.url)
        seen["authorization"] = request.headers["authorization"]
        seen["json"] = json.loads(request.content)
        return httpx.Response(200, json=_result())

    http = httpx.AsyncClient(transport=httpx.MockTransport(handler))
    try:
        result = await call_system_one(_request(), api_key="test-key", http=http)
    finally:
        await http.aclose()

    assert seen == {
        "url": "https://api.typesafe.ai/v1/systemone",
        "authorization": "Bearer test-key",
        "json": {
            "state": {"ticket": "I was billed twice and need help."},
            "model": "jev-1.13.0",
            "questions": {
                "billing": {"type": "noul", "instructions": "Is this about billing?", "criteria": None},
                "tone": {
                    "type": "choice",
                    "instructions": "What is the customer's tone?",
                    "criteria": {"calm": "Neutral", "angry": "Expresses anger"},
                },
                "urgency": {
                    "type": "score",
                    "instructions": "How urgent is this?",
                    "criteria": ["can wait", "today", "immediate"],
                },
            },
        },
    }
    assert result.answers["tone"].choice == "angry"  # type: ignore[union-attr]
    assert result.usage.input_tokens == 312


@pytest.mark.asyncio
async def test_system_one_uses_typesafe_request_id_header_when_body_omits_it() -> None:
    body = _result()
    body.pop("request_id")
    http = httpx.AsyncClient(
        transport=httpx.MockTransport(
            lambda _: httpx.Response(200, json=body, headers={"x-typesafe-request-id": "req_header"})
        )
    )
    try:
        result = await call_system_one(_request(), api_key="test-key", http=http)
    finally:
        await http.aclose()
    assert result.request_id == "req_header"


@pytest.mark.parametrize("state", ["plain text", {"record": ["a", 2]}, ["a", {"ok": True}]])
def test_request_preserves_each_supported_state_shape_without_coercion(state: object) -> None:
    request = SystemOneRequest(
        state=state,
        model="jev-1.13.0",
        questions={"q": NoulQuestion(instructions="Is it present?")},
    )
    assert request.model_dump()["state"] == state


@pytest.mark.parametrize(
    "question",
    [
        NoulQuestion(instructions=None, criteria={"true": {"proof": ["a", 2]}, "false": None}),
        ChoiceQuestion(instructions={"guide": ["one", 2]}, criteria={"a": ["A"], "b": None}),
        ScoreQuestion(instructions=["scale", {"v": 1}], criteria=[{"low": 0}, None, ["high"]]),
    ],
)
def test_request_preserves_advanced_entry_types_without_coercion(question: object) -> None:
    request = SystemOneRequest(state="x", model="jev-1.13.0", questions={"q": question})
    assert request.model_dump()["questions"]["q"] == question.model_dump()  # type: ignore[union-attr]


@pytest.mark.parametrize("state", [42, True, None, ("not", "a", "list")])
def test_request_refuses_non_system_one_state_roots(state: object) -> None:
    with pytest.raises(ValidationError):
        SystemOneRequest(
            state=state,
            model="jev-1.13.0",
            questions={"q": NoulQuestion(instructions="Is it present?")},
        )


@pytest.mark.parametrize(
    "question",
    [
        {"type": "choice", "instructions": "Pick", "criteria": {"only": None}},
        {"type": "score", "instructions": "Rate", "criteria": ["only"]},
        {"type": "unknown", "instructions": "No", "criteria": {}},
    ],
)
def test_request_refuses_invalid_primitives_before_the_wire(question: object) -> None:
    with pytest.raises(ValidationError):
        SystemOneRequest.model_validate(
            {"state": "x", "model": "jev-1.13.0", "questions": {"q": question}}
        )


@pytest.mark.asyncio
async def test_response_rejects_probabilities_that_do_not_match_requested_choice() -> None:
    broken = _result()
    broken["answers"]["tone"]["probabilities"] = {"calm": 1.0}  # type: ignore[index]
    http = httpx.AsyncClient(transport=httpx.MockTransport(lambda _: httpx.Response(200, json=broken)))
    try:
        with pytest.raises(TypeSafeProviderError, match="outside the requested criteria"):
            await call_system_one(_request(), api_key="test-key", http=http)
    finally:
        await http.aclose()


@pytest.mark.asyncio
async def test_malformed_post_inference_response_keeps_reported_usage_for_billing() -> None:
    broken = _result()
    broken["answers"] = {"billing": {"type": "noul", "noul": 0.92}}
    http = httpx.AsyncClient(transport=httpx.MockTransport(lambda _: httpx.Response(200, json=broken)))
    try:
        with pytest.raises(TypeSafeProviderError, match="do not match the requested question ids") as caught:
            await call_system_one(_request(), api_key="test-key", http=http)
    finally:
        await http.aclose()

    usage = get_billed_usage(caught.value)
    assert usage is not None
    assert (usage.input_tokens, usage.output_tokens, usage.api) == (312, 48, "typesafe")
    assert was_billing_checked(caught.value)


@pytest.mark.asyncio
async def test_http_error_does_not_expose_provider_body_or_api_key() -> None:
    http = httpx.AsyncClient(
        transport=httpx.MockTransport(
            lambda _: httpx.Response(422, text="api key test-key and private request content")
        )
    )
    try:
        with pytest.raises(TypeSafeProviderError) as caught:
            await call_system_one(_request(), api_key="test-key", http=http)
    finally:
        await http.aclose()

    assert caught.value.error_type == "invalid_request"
    assert "test-key" not in str(caught.value)
    assert "private request" not in str(caught.value)
    assert was_billing_checked(caught.value)


@pytest.mark.asyncio
@pytest.mark.parametrize(
    ("question", "status", "remedy"),
    [
        (NoulQuestion(instructions=None), 400, "null instructions"),
        (ScoreQuestion(instructions="rate", criteria=["low", None]), 422, "null Score criteria"),
    ],
)
async def test_provider_null_entry_refusal_names_remedy_without_stringifying(
    question: object, status: int, remedy: str
) -> None:
    request = SystemOneRequest(state="x", model="jev-1.13.0", questions={"q": question})
    http = httpx.AsyncClient(
        transport=httpx.MockTransport(lambda _: httpx.Response(status, text="private provider details"))
    )
    try:
        with pytest.raises(TypeSafeProviderError, match=remedy) as caught:
            await call_system_one(request, api_key="test-key", http=http)
    finally:
        await http.aclose()
    assert caught.value.error_type == "unsupported_entry_type"
    assert "private provider details" not in str(caught.value)


@pytest.mark.asyncio
async def test_rate_limit_retries_after_standard_http_date() -> None:
    calls = 0
    sleeps: list[float] = []
    now = datetime.now(tz=UTC)
    retry_header = (now + timedelta(seconds=4)).strftime("%a, %d %b %Y %H:%M:%S GMT")

    async def handler(_: httpx.Request) -> httpx.Response:
        nonlocal calls
        calls += 1
        if calls == 1:
            return httpx.Response(429, headers={"retry-after": retry_header})
        return httpx.Response(200, json=_result())

    async def record_sleep(delay: float) -> None:
        sleeps.append(delay)

    http = httpx.AsyncClient(transport=httpx.MockTransport(handler))
    try:
        result = await call_system_one(
            _request(), api_key="test-key", http=http, max_retries=1, sleep=record_sleep
        )
    finally:
        await http.aclose()

    assert result.model == "jev-1.13.0"
    assert calls == 2
    assert len(sleeps) == 1 and 0.0 <= sleeps[0] <= 4.1


def test_retry_after_supports_delta_and_http_date() -> None:
    now = datetime(2026, 9, 19, 12, 0, tzinfo=UTC)
    assert _retry_after({"retry-after": "2.5"}, now=now) == 2.5
    assert _retry_after({"retry-after": "Fri, 19 Sep 2026 12:00:03 GMT"}, now=now) == 3.0


@pytest.mark.asyncio
@pytest.mark.parametrize("counters", [{}, {"input_tokens": 312}, {"output_tokens": 48}, {"input_tokens": True, "output_tokens": 48}])
async def test_incomplete_usage_cannot_be_reported_as_free_success(counters):
    body = _result()
    body["usage"] = counters
    async with httpx.AsyncClient(transport=httpx.MockTransport(lambda _: httpx.Response(200, json=body))) as http:
        with pytest.raises(TypeSafeProviderError) as caught:
            await call_system_one(_request(), api_key="test-key", http=http)
    assert caught.value.error_type == "invalid_response"
    billed = get_billed_usage(caught.value)
    if counters:
        assert billed is not None
        assert billed.raw_usage == {k: v for k, v in counters.items() if type(v) is int}
    else:
        assert billed is None


@pytest.mark.asyncio
async def test_explicit_zero_usage_is_valid():
    body = _result()
    body["usage"] = {"input_tokens": 0, "output_tokens": 0}
    async with httpx.AsyncClient(transport=httpx.MockTransport(lambda _: httpx.Response(200, json=body))) as http:
        result = await call_system_one(_request(), api_key="test-key", http=http)
    assert result.usage.input_tokens == result.usage.output_tokens == 0


def test_vendor_option_and_level_caps_are_refused_before_transport() -> None:
    """docs.typesafe.ai/api: Choice ≤ 255 options, Score ≤ 10 levels."""
    from pydantic import ValidationError

    ChoiceQuestion(instructions="pick", criteria={f"o{i}": None for i in range(255)})
    with pytest.raises(ValidationError, match="at most 255"):
        ChoiceQuestion(instructions="pick", criteria={f"o{i}": None for i in range(256)})
    ScoreQuestion(instructions="rate", criteria=[f"l{i}" for i in range(10)])
    with pytest.raises(ValidationError, match="at most 10"):
        ScoreQuestion(instructions="rate", criteria=[f"l{i}" for i in range(11)])
