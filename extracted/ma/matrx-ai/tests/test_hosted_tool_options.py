"""A held call carries a provider-run tool its Holder turns on, narrowed for one call (social.x_search).

Proven live 2026-10-22: a Grok 4.5 held call with ``internal_x_search`` + ``allowed_x_handles=["NASA"]`` ran in
one iteration with zero client tool calls and returned 3 real @NASA posts ($0.019).
"""

from __future__ import annotations

from types import SimpleNamespace

import pytest
from test_xai_native_translator import _profile
from xai_sdk.proto import chat_pb2

from matrx_ai.config import UnifiedConfig
from matrx_ai.mandates import HeldCall, MandateRefused, held_request_config
from matrx_ai.providers.xai.translator import XAITranslator, hosted_tool_kwargs, is_client_tool_call


def _held(**config: object) -> HeldCall:
    return HeldCall(mandate_key="social.x_search", model="grok-4.5", system="s", temperature=None,
                    max_output_tokens=None, turns=[{"role": "user", "content": "u"}],
                    config=UnifiedConfig.from_dict({"model": "grok-4.5", **config}), metadata={})


def test_the_held_request_carries_the_holders_hosted_tool_and_the_calls_narrowing():
    cfg = held_request_config(_held(internal_x_search=True),
                              hosted_tool_options={"internal_x_search": {"allowed_x_handles": ["NASA"]}, "max_turns": 2})
    assert cfg.internal_x_search is True
    assert cfg.hosted_tool_options == {"internal_x_search": {"allowed_x_handles": ["NASA"]}, "max_turns": 2}
    kwargs = XAITranslator().to_xai(cfg, _profile("xai_standard"))
    x_tool = next(t for t in kwargs["tools"] if t.HasField("x_search"))
    assert list(x_tool.x_search.allowed_x_handles) == ["NASA"]
    assert kwargs["max_turns"] == 2


def test_a_call_cannot_turn_on_a_tool_its_holder_does_not_run():
    with pytest.raises(MandateRefused) as exc:
        held_request_config(_held(), hosted_tool_options={"internal_x_search": {"allowed_x_handles": ["NASA"]}})
    assert exc.value.code == "holder_lacks_hosted_tool"


def test_an_option_the_tool_does_not_take_is_refused_never_dropped():
    cfg = UnifiedConfig.from_dict({"model": "grok-4.5", "internal_x_search": True,
                                   "hosted_tool_options": {"internal_x_search": {"allowed_handles": ["x"]}}})
    with pytest.raises(ValueError, match="allowed_handles"):
        hosted_tool_kwargs(cfg, "internal_x_search")


def test_a_held_call_without_options_sends_what_it_always_sent():
    cfg = held_request_config(_held(internal_x_search=True))
    assert cfg.internal_x_search is None and cfg.hosted_tool_options is None


def test_a_server_side_tool_call_is_never_a_tool_the_executor_owes():
    server = chat_pb2.ToolCall(id="a", type=chat_pb2.ToolCallType.TOOL_CALL_TYPE_X_SEARCH_TOOL,
                               function=chat_pb2.FunctionCall(name="x_keyword_search", arguments="{}"))
    client = chat_pb2.ToolCall(id="b", type=chat_pb2.ToolCallType.TOOL_CALL_TYPE_CLIENT_SIDE_TOOL,
                               function=chat_pb2.FunctionCall(name="lookup", arguments='{"q": 1}'))
    legacy = chat_pb2.ToolCall(id="c", function=chat_pb2.FunctionCall(name="old", arguments="{}"))
    assert not is_client_tool_call(server)
    assert is_client_tool_call(client) and is_client_tool_call(legacy)
    response = SimpleNamespace(reasoning_content=None, content='{"posts": []}', tool_calls=[server, client],
                               usage=None, id="r", finish_reason="REASON_STOP", citations=[])
    unified = XAITranslator().from_xai(response)
    names = [getattr(c, "name", None) for m in unified.messages for c in m.content if getattr(c, "name", None)]
    assert names == ["lookup"]
