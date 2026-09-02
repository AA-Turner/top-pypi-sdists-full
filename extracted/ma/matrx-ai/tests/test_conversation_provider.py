"""UnifiedProviderTurn — maps one real UnifiedAIClient turn into the conversation
executor's TurnResult. Crafted UnifiedResponse objects + a fake client; no DB."""

from __future__ import annotations

from decimal import Decimal

from matrx_ai.config.message_config import UnifiedMessage
from matrx_ai.config.tools_config import ToolCallContent
from matrx_ai.config.unified_config import UnifiedResponse
from matrx_ai.config.unified_content import TextContent
from matrx_ai.config.usage_config import TokenUsage
from matrx_ai.orchestrator.conversation_provider import UnifiedProviderTurn


def _usage():
    return TokenUsage(input_tokens=20, output_tokens=8, api="mock", matrx_model_name="mock-1")


def _text(text="hi", finish="stop"):
    return UnifiedResponse(
        messages=[UnifiedMessage(role="assistant", content=[TextContent(text=text)])],
        usage=_usage(), finish_reason=finish,
    )


def _tool(name="search", args=None, call_id="c1"):
    return UnifiedResponse(
        messages=[UnifiedMessage(role="assistant",
                                 content=[ToolCallContent(id=call_id, name=name, arguments=args or {})])],
        usage=_usage(), finish_reason="tool_calls",
    )


class FakeClient:
    def __init__(self, response=None, exc=None):
        self._r, self._e, self.requests = response, exc, []

    async def execute(self, request):
        self.requests.append(request)
        if self._e is not None:
            raise self._e
        return self._r


def _turn(client, **kw):
    return UnifiedProviderTurn(client, model="mock-1",
                              cost_resolver=lambda u: Decimal("0.10"), **kw)


async def test_text_stop_maps_to_turnresult():
    t = await _turn(FakeClient(_text("hello")))(conversation_id="c", history=[], iteration=1)
    assert t.finish == "stop" and t.text == "hello"
    assert t.spend.usd == Decimal("0.10")
    assert t.spend.input_tokens == 20 and t.spend.output_tokens == 8


async def test_tool_call_maps_to_tools_finish():
    t = await _turn(FakeClient(_tool("search", {"q": "x"})))(conversation_id="c", history=[], iteration=2)
    assert t.finish == "tools"
    assert len(t.tool_calls) == 1
    assert t.tool_calls[0].name == "search" and t.tool_calls[0].arguments == {"q": "x"}
    assert t.tool_calls[0].spawns_conversation is False


async def test_sub_conversation_tool_marks_spawn_and_extracts_prompt():
    runner = _turn(FakeClient(_tool("ask_expert", {"prompt": "deep question"})),
                   sub_conversation_tools=frozenset({"ask_expert"}))
    t = await runner(conversation_id="c", history=[], iteration=1)
    assert t.tool_calls[0].spawns_conversation is True
    assert t.tool_calls[0].child_prompt == "deep question"


async def test_error_finish_reason_maps_to_error():
    t = await _turn(FakeClient(_text(finish="content_filter")))(conversation_id="c", history=[], iteration=1)
    assert t.finish == "error"
    assert t.error.error_type == "provider_finish_reason"


async def test_provider_exception_with_usage_records_spend():
    exc = RuntimeError("upstream")
    exc.usage = _usage()
    t = await _turn(FakeClient(exc=exc))(conversation_id="c", history=[], iteration=1)
    assert t.finish == "error"
    assert t.error.error_type == "RuntimeError"
    assert t.spend is not None and t.spend.usd == Decimal("0.10")  # billed-then-failed still metered


async def test_request_built_from_history():
    client = FakeClient(_text())
    await _turn(client)(conversation_id="conv-9",
                        history=[{"role": "user", "content": "hi there"}], iteration=1)
    req = client.requests[0]
    assert req.conversation_id == "conv-9"
    assert req.config.model == "mock-1"
    msgs = req.config.messages
    msgs = msgs.to_list() if hasattr(msgs, "to_list") else msgs
    assert msgs[0].role == "user" and msgs[0].content[0].text == "hi there"
