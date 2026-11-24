"""xAI server-side tool calls are counted and priced per call.

A grok-4.7 call reporting ``server_side_tools_used`` = 28 x WEB_SEARCH was billed tokens only
(under-billed 28 x $0.005 = $0.14). The unit count now rides ``billing_components`` and the
offering's ``component_prices`` carries the per-million-unit price (5000 = $5/1,000).
"""

from __future__ import annotations

from xai_sdk.proto import usage_pb2

from matrx_ai.config.usage_config import (
    TokenUsage,
    serialize_provider_usage,
    xai_server_side_tool_components,
)

_T = usage_pb2.ServerSideTool


def _usage():
    return usage_pb2.SamplingUsage(
        prompt_tokens=1000,
        completion_tokens=500,
        total_tokens=1500,
        server_side_tools_used=[_T.SERVER_SIDE_TOOL_WEB_SEARCH] * 28
        + [_T.SERVER_SIDE_TOOL_X_SEARCH] * 3
        + [_T.SERVER_SIDE_TOOL_CODE_EXECUTION],
    )


def test_counts_priced_tools_from_the_proto_and_its_serialized_form():
    expected = {"service.web_search": 28, "service.code_execution": 1}
    assert xai_server_side_tool_components(_usage()) == expected
    assert xai_server_side_tool_components(serialize_provider_usage(_usage())) == expected


def test_no_tools_means_no_components():
    assert xai_server_side_tool_components(usage_pb2.SamplingUsage(prompt_tokens=5)) == {}


def test_translator_puts_the_count_on_the_token_usage():
    from matrx_ai.providers.xai.translator import XAITranslator

    class _Proto:
        model = "grok-4.7"

    class _Resp:
        content = "ok"
        tool_calls: list = []
        usage = _usage()
        id = "r1"
        finish_reason = "REASON_STOP"
        citations: list = []
        proto = _Proto()

    u = XAITranslator().from_xai(_Resp())
    assert u.usage.billing_components == {"service.web_search": 28, "service.code_execution": 1}


def test_tokens_alone_no_longer_stand_in_for_the_bill():
    from matrx_ai.config.usage_config import ModelPricing, PricingTier

    usage = TokenUsage(
        input_tokens=1000,
        output_tokens=500,
        matrx_model_name="grok-4.7",
        billing_components=xai_server_side_tool_components(_usage()),
    )
    tier = PricingTier(
        max_tokens=None,
        input_price=2.0,
        output_price=6.0,
        cached_input_price=0.5,
        component_prices={"service.web_search": 5000, "service.code_execution": 5000},
    )
    cost = usage.calculate_cost(
        {"grok-4.7": ModelPricing(model_name="grok-4.7", api="xai", tiers=[tier])}
    )
    assert cost is not None
    assert abs(cost - (0.002 + 0.003 + 29 * 0.005)) < 1e-9
