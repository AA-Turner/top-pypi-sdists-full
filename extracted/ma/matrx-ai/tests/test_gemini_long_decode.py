"""Gemini long decode: an answer past one call's output limit, joined from continuation hops.

Gemini 4 Argon returns at most ~64K output tokens per call and answers
``finishReason: CONTINUATION`` + ``continuationToken`` until the requested total
(``max_output_tokens``, cumulative across calls) is reached. ``GoogleChat.execute`` runs that
loop ONLY for a model whose capabilities declare ``long_decode`` and only when the request asks
for more than the model's one-call limit (``ai.model_definition.max_tokens``). Every hop is the
same request plus the latest token; the hops join into one response whose usage is the sum of
every hop's (Google re-bills the prompt each hop).

These tests drive the REAL google-genai client over an httpx MockTransport, so the request
bodies asserted are what the SDK actually puts on the wire.
"""

from __future__ import annotations

import base64
import json
from typing import Any

import httpx
import pytest
from google import genai
from matrx_connect.context.app_context import AppContext, clear_app_context, set_app_context
from matrx_connect.emitters import SilentEmitter

from matrx_ai.catalog.controls import CompiledControlsMap
from matrx_ai.catalog.models import CellRef, ControlRule
from matrx_ai.config import FinishReason, TextContent, UnifiedConfig, UnifiedMessage
from matrx_ai.config.usage_config import ModelPricing, PricingTier
from matrx_ai.providers.google import google_api
from matrx_ai.providers.google.google_api import GoogleChat
from matrx_ai.testing.profile_factory import make_profile

MODEL = "gemini-4-argon"
ONE_CALL = 65_536
TOTAL = 1_048_576
SECRET = "test-google-key-0123456789"

ARGON_CAPS = {
    "input": ["text"],
    "output": ["text"],
    "features": ["function_calling", "structured_output", "thinking", "long_decode"],
    "interaction": "turn",
    "multilingual": True,
}


def _controls(*, declared_total: int | None = TOTAL) -> CompiledControlsMap:
    rule: dict[str, Any] = {"provider_key": "max_output_tokens"}
    cells: dict[str, CellRef] = {}
    if declared_total is not None:
        rule["clamp"] = {"max": declared_total}
        cells["max_output_tokens"] = CellRef(cell_id="argon-total", layer="offering", state="agent")
    return CompiledControlsMap(
        rules={"max_output_tokens": ControlRule.model_validate(rule)},
        cells=cells,
        output_maximum=ONE_CALL,
    )


def _profile(*, long_decode: bool = True, declared_total: int | None = TOTAL) -> Any:
    caps = dict(ARGON_CAPS)
    if not long_decode:
        caps["features"] = [f for f in caps["features"] if f != "long_decode"]
    return make_profile(
        model_name=MODEL,
        wire_format="google_chat",
        capabilities=caps,
        controls=_controls(declared_total=declared_total),
    )


def _config(*, stream: bool, max_output_tokens: int) -> UnifiedConfig:
    return UnifiedConfig(
        model=MODEL,
        stream=stream,
        max_output_tokens=max_output_tokens,
        messages=[UnifiedMessage(role="user", content=[TextContent(text="Write the whole manual.")])],
    )


def _token(n: int) -> str:
    return base64.b64encode(f"state-{n}".encode()).decode()


def _hop(n: int, *, text: str, finish: str, prompt: int, cached: int, out: int, thoughts: int) -> dict:
    candidate: dict[str, Any] = {
        "content": {"role": "model", "parts": [{"text": text}]},
        "finishReason": finish,
        "index": 0,
    }
    if finish == "CONTINUATION":
        candidate["continuationToken"] = _token(n)
    return {
        "candidates": [candidate],
        "usageMetadata": {
            "promptTokenCount": prompt,
            "cachedContentTokenCount": cached,
            "candidatesTokenCount": out,
            "thoughtsTokenCount": thoughts,
            "totalTokenCount": prompt + out + thoughts,
        },
        "modelVersion": MODEL,
        "responseId": f"resp-{n}",
    }


# Three hops: the prompt (1,000 tokens) is re-sent each hop; hops 2-3 hit the implicit cache.
HOPS = [
    _hop(1, text="Part one. ", finish="CONTINUATION", prompt=1_000, cached=0, out=60_000, thoughts=5_000),
    _hop(2, text="Part two. ", finish="CONTINUATION", prompt=1_000, cached=900, out=64_000, thoughts=1_000),
    _hop(3, text="The end.", finish="STOP", prompt=1_000, cached=900, out=20_000, thoughts=0),
]


class _Google:
    """A fake Gemini endpoint answering scripted hops; records every request body."""

    def __init__(self, hops: list[dict]) -> None:
        self.hops = hops
        self.bodies: list[dict] = []

    def handler(self, request: httpx.Request) -> httpx.Response:
        body = json.loads(request.content)
        self.bodies.append(body)
        hop = self.hops[min(len(self.bodies), len(self.hops)) - 1]
        if ":streamGenerateContent" in str(request.url):
            # Two SSE chunks per hop: text first, the closing chunk with finish + usage.
            head = {"candidates": [{"content": hop["candidates"][0]["content"], "index": 0}]}
            tail = json.loads(json.dumps(hop))
            tail["candidates"][0]["content"] = {"role": "model", "parts": [{"text": ""}]}
            sse = f"data: {json.dumps(head)}\r\n\r\ndata: {json.dumps(tail)}\r\n\r\n"
            return httpx.Response(200, text=sse, headers={"content-type": "text/event-stream"})
        return httpx.Response(200, json=hop)

    def client(self) -> genai.Client:
        return genai.Client(
            api_key=SECRET,
            http_options=genai.types.HttpOptions(
                httpx_async_client=httpx.AsyncClient(transport=httpx.MockTransport(self.handler))
            ),
        )


@pytest.fixture(autouse=True)
def _app_context():
    token = set_app_context(AppContext(emitter=SilentEmitter()))
    yield
    clear_app_context(token)


@pytest.fixture(autouse=True)
def _no_keys(monkeypatch):
    monkeypatch.setattr("matrx_ai.providers.keys.resolve_api_key", lambda *a, **kw: SECRET)


async def _run(google: _Google, profile: Any, *, stream: bool, max_output_tokens: int):
    chat = GoogleChat()
    chat.client = google.client()
    return await chat.execute(_config(stream=stream, max_output_tokens=max_output_tokens), profile)


def _text(response: Any) -> str:
    return "".join(
        part.text for msg in response.messages for part in msg.content if isinstance(part, TextContent)
    )


@pytest.mark.asyncio
@pytest.mark.parametrize("stream", [False, True])
async def test_hops_join_into_one_answer_with_every_hops_usage(stream):
    google = _Google(HOPS)
    response = await _run(google, _profile(), stream=stream, max_output_tokens=200_000)

    assert len(google.bodies) == 3
    assert _text(response) == "Part one. Part two. The end."
    assert response.finish_reason == FinishReason.STOP

    # Same request every hop (never the partial answer appended), latest token only.
    first = google.bodies[0]
    assert first["generationConfig"]["maxOutputTokens"] == 200_000
    assert "continuationToken" not in first
    for n, body in enumerate(google.bodies[1:], start=1):
        assert body["contents"] == first["contents"]
        assert body["generationConfig"] == first["generationConfig"]
        # The token rides at the top level of the request (Google's REST shape).
        assert body["continuationToken"] == _token(n)

    usage = response.usage
    assert usage is not None
    # input = uncached prompt of every hop; cached = every hop's cached share; output = text + thinking.
    assert usage.input_tokens == 1_000 + 100 + 100
    assert usage.cached_input_tokens == 900 + 900
    assert usage.output_tokens == (60_000 + 5_000) + (64_000 + 1_000) + 20_000
    assert usage.metadata["segmented_provider_calls"] == 3

    pricing = ModelPricing(
        model_name=MODEL,
        api="google",
        tiers=[PricingTier(max_tokens=None, input_price=2.0, output_price=10.0, cached_input_price=0.1)],
    )
    cost = usage.calculate_cost({MODEL: pricing})
    expected = (1_200 * 2.0 + 1_800 * 0.1 + 150_000 * 10.0) / 1_000_000
    assert cost == pytest.approx(expected)


@pytest.mark.asyncio
@pytest.mark.parametrize("stream", [False, True])
async def test_a_model_without_long_decode_is_exactly_one_call(stream):
    """Also proves the SDK's own continuation loop (on by default) is off on our requests."""
    google = _Google(HOPS)
    response = await _run(google, _profile(long_decode=False), stream=stream, max_output_tokens=200_000)
    assert len(google.bodies) == 1
    # Not continued: the answer ends at the output limit, honestly.
    assert response.finish_reason == FinishReason.MAX_TOKENS
    assert response.usage is not None and response.usage.output_tokens == 65_000


@pytest.mark.asyncio
async def test_a_request_within_one_call_never_loops_even_on_a_long_decode_model():
    google = _Google(HOPS)
    response = await _run(google, _profile(), stream=False, max_output_tokens=ONE_CALL)
    assert len(google.bodies) == 1
    assert response.finish_reason == FinishReason.MAX_TOKENS


@pytest.mark.asyncio
async def test_without_a_declared_total_the_model_maximum_clamps_and_no_loop_runs():
    google = _Google(HOPS)
    await _run(google, _profile(declared_total=None), stream=False, max_output_tokens=200_000)
    [body] = google.bodies
    assert body["generationConfig"]["maxOutputTokens"] == ONE_CALL


@pytest.mark.asyncio
async def test_a_provider_that_never_stops_continuing_is_cut_at_the_hop_limit(monkeypatch):
    monkeypatch.setattr(google_api, "LONG_DECODE_MAX_HOPS", 4)
    forever = [_hop(n, text=".", finish="CONTINUATION", prompt=10, cached=0, out=1, thoughts=0) for n in range(1, 10)]
    google = _Google(forever)
    response = await _run(google, _profile(), stream=False, max_output_tokens=200_000)
    assert len(google.bodies) == 4
    assert response.finish_reason == FinishReason.MAX_TOKENS
    assert response.usage is not None and response.usage.output_tokens == 4


def test_billed_usages_counts_a_hop_cut_off_mid_stream():
    from types import SimpleNamespace as NS

    closed = NS(candidates=[NS(finish_reason="CONTINUATION")], usage_metadata="hop1")
    partial_a = NS(candidates=[NS(finish_reason=None)], usage_metadata="hop2-partial")
    partial_b = NS(candidates=[NS(finish_reason=None)], usage_metadata="hop2-latest")
    assert GoogleChat._billed_usages([closed, partial_a, partial_b]) == ["hop1", "hop2-latest"]
    assert GoogleChat._billed_usages([closed]) == ["hop1"]


def test_a_long_decode_answer_is_priced_at_the_tier_one_hop_reached():
    from types import SimpleNamespace as NS

    from matrx_ai.providers.google.translator import GoogleTranslator

    hop = NS(prompt_token_count=120_000, cached_content_token_count=0, candidates_token_count=60_000, thoughts_token_count=0)
    usage = GoogleTranslator.summed_gemini_usage([hop, hop, hop], matrx_model_name=MODEL, provider_model_name=MODEL, response_id="r")
    pricing = ModelPricing(
        model_name=MODEL,
        api="google",
        tiers=[
            PricingTier(max_tokens=200_000, input_price=2.0, output_price=12.0, cached_input_price=0.2),
            PricingTier(max_tokens=None, input_price=4.0, output_price=18.0, cached_input_price=0.4),
        ],
    )
    # 3 x 120K prompt = 360K summed, but no single call crossed 200K: the short-context tier.
    assert usage.calculate_cost({MODEL: pricing}) == pytest.approx((360_000 * 2.0 + 180_000 * 12.0) / 1_000_000)


@pytest.mark.asyncio
async def test_a_hop_that_fails_after_paid_hops_is_never_retried_from_the_start():
    class _Fails(_Google):
        def handler(self, request: httpx.Request) -> httpx.Response:
            if len(self.bodies) >= 1:
                self.bodies.append(json.loads(request.content))
                return httpx.Response(503, json={"error": {"code": 503, "message": "overloaded", "status": "UNAVAILABLE"}})
            return super().handler(request)

    google = _Fails(HOPS)
    with pytest.raises(Exception) as failure:  # noqa: B017
        await _run(google, _profile(), stream=False, max_output_tokens=200_000)
    assert len(google.bodies) == 2
    assert failure.value.error_info.is_retryable is False
    # The paid first hop is on the error, so the spend is recorded once.
    from matrx_ai.providers.errors import get_billed_usage

    billed = get_billed_usage(failure.value)
    assert billed is not None and billed.output_tokens == 65_000
