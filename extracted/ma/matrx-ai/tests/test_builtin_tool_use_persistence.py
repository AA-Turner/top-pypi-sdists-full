"""Provider-side search / url_context must be visible on the persisted request.

Defect (workflow runs d3d657a0, cad59856): a Gemini call grounded by Google
Search persisted chat.request.tool_calls_count=0 and nothing said searches ran.
"""

from __future__ import annotations

from types import SimpleNamespace

from matrx_ai.config.builtin_tool_use import collect_builtin_tool_use
from matrx_ai.config.extra_config import HostedToolContent, WebSearchCallContent
from matrx_ai.config.unified_config import UnifiedConfig, UnifiedMessage, UnifiedResponse
from matrx_ai.config.unified_content import TextContent
from matrx_ai.config.usage_config import TokenUsage
from matrx_ai.orchestrator.requests import AIMatrixRequest, CompletedRequest
from matrx_ai.providers.unified_client import UnifiedAIClient


def _resp(*content, usage=None) -> UnifiedResponse:
    return UnifiedResponse(
        messages=[UnifiedMessage(role="assistant", content=list(content))],
        usage=usage or TokenUsage(input_tokens=1, output_tokens=1, matrx_model_name="m", api="google"),
    )


def _gemini() -> UnifiedResponse:
    grounding = SimpleNamespace(
        web_search_queries=["q one", "q two"], grounding_chunks=[object()] * 3
    )
    return _resp(
        TextContent(
            text="answer",
            metadata={
                "grounding_metadata": grounding,
                "url_context_metadata": {"url_metadata": [{"retrieved_url": "https://a.test"}]},
            },
        )
    )


def test_gemini_grounding_and_url_context_collected():
    out = collect_builtin_tool_use(_gemini())
    assert out["web_search"] == {"count": 2, "queries": ["q one", "q two"], "sources_cited": 3}
    assert out["url_context"] == {"count": 1, "urls": ["https://a.test"]}


def test_openai_and_anthropic_siblings_collected():
    oa = collect_builtin_tool_use(
        _resp(WebSearchCallContent(id="w", status="completed", action={"query": "oa q"}))
    )
    assert oa["web_search"]["count"] == 1 and oa["web_search"]["queries"] == ["oa q"]
    an = collect_builtin_tool_use(
        _resp(
            HostedToolContent.from_anthropic(
                {"type": "server_tool_use", "name": "web_search", "input": {"query": "an q"}}
            )
        )
    )
    assert an["web_search"]["queries"] == ["an q"]


def test_nothing_ran_returns_none():
    assert collect_builtin_tool_use(_resp(TextContent(text="hi"))) is None


def test_request_row_records_builtin_tool_use():
    from matrx_ai.context.app_context import AppContext, clear_app_context, set_app_context

    token = set_app_context(AppContext(emitter=None, user_id="u1"))
    try:
        _row_check()
    finally:
        clear_app_context(token)


def _row_check():
    response = _gemini()
    UnifiedAIClient._stamp_offering_usage(
        response, SimpleNamespace(offering_id="o", resolution_route="preferred"), SimpleNamespace()
    )
    config = UnifiedConfig(model="gemini", messages=[{"role": "user", "content": "hi"}])
    req = AIMatrixRequest(conversation_id="c1", config=config, usage_history=[response.usage])
    row = CompletedRequest(request=req, iterations=1, final_response=None).to_storage_dict()[
        "requests"
    ][0]
    assert row["tool_calls_count"] == 0
    assert row["metadata"]["builtin_tool_use"]["web_search"]["queries"] == ["q one", "q two"]
    assert row["metadata"]["builtin_tool_use"]["url_context"]["count"] == 1
