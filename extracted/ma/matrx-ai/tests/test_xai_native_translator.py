"""xAI native (xai_sdk gRPC) translator coverage.

The xAI chat path uses the native ``xai_sdk`` SDK (not the OpenAI-compatible
shim), so its request shape is proto objects — distinct from the OpenAI-chat
dict shape exercised in test_openai_chat_tool_result_image.py. These tests pin:

- reasoning_effort mapping per rules contract (none omits vs native none-disable)
- native web_search() / x_search() server tools driven by the unified flags
- function-tool conversion + the name-dedup guarantee
- the message round-trip (user / assistant-with-tool-calls / tool_result + image)
- from_xai response parsing (text, tool_calls, usage, finish_reason, citations)
"""
from __future__ import annotations

import json

from test_chat_param_golden import load_golden
from xai_sdk.proto import chat_pb2, usage_pb2

from matrx_ai.config import (
    TextContent,
    ToolCallContent,
    ToolResultContent,
    UnifiedConfig,
    UnifiedMessage,
)
from matrx_ai.config.media_config import ImageContent
from matrx_ai.providers.xai.translator import (
    XAITranslator,
    billed_output_tokens_from_xai_usage,
    provider_charge_from_xai_usage,
)
from matrx_ai.testing.profile_factory import make_profile


def _profile(family: str):
    payload = load_golden(family)
    return make_profile(
        model_name="grok-4.3",
        wire_format=payload["wire_format"],
        rules=payload["rules"],
        value_orders=payload["value_orders"],
    )


_REASONING = _profile("xai_reasoning")
_STANDARD = _profile("xai_standard")


def _cfg(messages, **kw):
    return UnifiedConfig(model="grok-4.3", messages=messages, **kw)


# --------------------------------------------------------------------- reasoning
def _effort_sent(profile, effort):
    kw = XAITranslator().to_xai(
        _cfg([UnifiedMessage(role="user", content=[TextContent(text="hi")])],
             reasoning_effort=effort),
        profile,
    )
    return kw.get("reasoning_effort")


def test_xai_standard_none_sends_nothing():
    # House standard (ai_041): xai_standard has no native off token, so "none"
    # OMITS the key entirely — it must never floor to a concrete level ("low"
    # was the pre-standard behavior this test used to pin).
    assert _effort_sent(_STANDARD, "none") is None


def test_xai_reasoning_allows_none_disable():
    assert _effort_sent(_REASONING, "none") == "none"


def test_reasoning_maps_all_unified_values():
    expected = {
        "auto": None, "none": "none", "minimal": "low", "low": "low",
        "medium": "medium", "high": "high", "xhigh": "high",
    }
    for unified, want in expected.items():
        got = _effort_sent(_REASONING, unified)
        assert got == want, f"{unified} -> {got}, expected {want}"


def test_reasoning_effort_emitted_in_request():
    assert _effort_sent(_REASONING, "medium") == "medium"


# ------------------------------------------------------------------ search tools
def _tool_kinds(tools):
    kinds = []
    for t in tools:
        if t.HasField("web_search"):
            kinds.append("web_search")
        elif t.HasField("x_search"):
            kinds.append("x_search")
        elif t.HasField("function"):
            kinds.append(f"fn:{t.function.name}")
    return kinds


def test_web_and_x_search_become_native_tools():
    kw = XAITranslator().to_xai(
        _cfg([UnifiedMessage(role="user", content=[TextContent(text="news?")])],
             internal_web_search=True, internal_x_search=True),
        _REASONING,
    )
    kinds = _tool_kinds(kw["tools"])
    assert "web_search" in kinds and "x_search" in kinds


def test_no_search_flags_no_native_tools():
    kw = XAITranslator().to_xai(
        _cfg([UnifiedMessage(role="user", content=[TextContent(text="hi")])]),
        _REASONING,
    )
    assert "tools" not in kw  # nothing to send


# ------------------------------------------------------------------- messages
def test_tool_loop_roundtrip():
    cfg = _cfg([
        UnifiedMessage(role="user", content=[TextContent(text="weather in SF?")]),
        UnifiedMessage(role="assistant", content=[
            ToolCallContent(id="c1", name="get_weather", arguments={"city": "SF"}),
        ]),
        UnifiedMessage(role="tool", content=[
            ToolResultContent(tool_use_id="c1", name="get_weather", content="72F sunny"),
        ]),
    ])
    msgs = XAITranslator().to_xai(cfg, _REASONING)["messages"]
    roles = [chat_pb2.MessageRole.Name(m.role) for m in msgs]
    assert roles == ["ROLE_USER", "ROLE_ASSISTANT", "ROLE_TOOL"]
    assistant = msgs[1]
    assert [tc.function.name for tc in assistant.tool_calls] == ["get_weather"]
    assert json.loads(assistant.tool_calls[0].function.arguments) == {"city": "SF"}
    tool_msg = msgs[2]
    assert tool_msg.tool_call_id == "c1"
    assert any(c.text == "72F sunny" for c in tool_msg.content)


def test_user_image_becomes_native_image_content():
    cfg = _cfg([
        UnifiedMessage(role="user", content=[
            TextContent(text="what's this?"),
            ImageContent(url="https://example.com/cat.jpg", mime_type="image/jpeg"),
        ]),
    ])
    msgs = XAITranslator().to_xai(cfg, _REASONING)["messages"]
    user_msg = next(m for m in msgs if m.role == chat_pb2.MessageRole.ROLE_USER)
    assert any(c.HasField("image_url") for c in user_msg.content)
    assert any(c.text for c in user_msg.content)


# ------------------------------------------------------------------- response
class _FakeFn:
    name = "get_weather"
    arguments = '{"city": "SF"}'


class _FakeTC:
    id = "c1"
    function = _FakeFn()


class _FakeUsage:
    prompt_tokens = 10
    completion_tokens = 5
    total_tokens = 15


class _FakeProto:
    model = "grok-4.3"


class _FakeResponse:
    content = "It is sunny"
    tool_calls = [_FakeTC()]
    usage = _FakeUsage()
    id = "r1"
    finish_reason = "REASON_TOOL_CALLS"
    citations = ["https://x.com/post/1"]
    proto = _FakeProto()


def test_from_xai_parses_full_response():
    u = XAITranslator().from_xai(_FakeResponse())
    assert len(u.messages) == 1
    types = [type(c).__name__ for c in u.messages[0].content]
    assert "TextContent" in types and "ToolCallContent" in types
    assert u.finish_reason == "tool_calls"
    assert u.usage.input_tokens == 10 and u.usage.output_tokens == 5
    assert u.metadata["citations"] == ["https://x.com/post/1"]


def test_xai_provider_charge_is_preserved_as_exact_cost_evidence():
    usage = usage_pb2.SamplingUsage(
        prompt_tokens=10,
        completion_tokens=5,
        total_tokens=15,
        cost_in_usd_ticks=12_345_678,
    )
    charge = provider_charge_from_xai_usage(usage)
    assert charge is not None
    assert charge.raw_amount == 12_345_678
    assert charge.amount_usd == 0.0012345678


# ------------------------------------------------------------- reasoning cost
# xAI's usage_pb2.SamplingUsage carries reasoning_tokens as a field SEPARATE
# from completion_tokens (total_tokens = prompt + completion + reasoning),
# unlike OpenAI's Responses API / Anthropic, whose output_tokens already fold
# reasoning/thinking in. Dropping it under-recorded a real bake-off run at
# $0.74 vs xAI's own $3.92 (2026-09-26) because TokenUsage.output_tokens —
# the field ``calculate_cost`` actually prices off — held only completion_tokens.
def test_billed_output_tokens_adds_reasoning_to_completion():
    # A realistic reasoning-heavy Grok run: small visible completion, large
    # reasoning burn — the shape that produced the 5x ledger undercount.
    usage = usage_pb2.SamplingUsage(
        prompt_tokens=500,
        completion_tokens=1200,
        reasoning_tokens=6400,
        total_tokens=8100,
    )
    assert billed_output_tokens_from_xai_usage(usage) == 1200 + 6400


def test_billed_output_tokens_handles_no_reasoning_field():
    # A plain (non-reasoning) usage payload with reasoning_tokens unset/zero
    # must not be affected — output stays exactly completion_tokens.
    usage = usage_pb2.SamplingUsage(prompt_tokens=10, completion_tokens=5, total_tokens=15)
    assert billed_output_tokens_from_xai_usage(usage) == 5


class _FakeReasoningUsage:
    prompt_tokens = 500
    completion_tokens = 1200
    reasoning_tokens = 6400
    total_tokens = 8100


class _FakeReasoningResponse:
    content = "It is sunny"
    tool_calls = []
    usage = _FakeReasoningUsage()
    id = "r2"
    finish_reason = "REASON_STOP"
    citations = []
    proto = _FakeProto()


def test_from_xai_bills_reasoning_tokens_as_output():
    u = XAITranslator().from_xai(_FakeReasoningResponse())
    assert u.usage.input_tokens == 500
    # Must equal completion + reasoning (1,200 + 6,400), never completion alone.
    assert u.usage.output_tokens == 7600
