"""A replayed OpenAI web_search_call must travel with its reasoning item, or not at all.

Live refusal (2026-09-28, gpt-6-astra, the AI-visibility research agent's second tool turn):
"Item 'ws_…' of type 'web_search_call' was provided without its required 'reasoning' item".
"""

from matrx_ai.config.enums import Role
from matrx_ai.config.extra_config import WebSearchCallContent
from matrx_ai.config.message_config import UnifiedMessage
from matrx_ai.config.unified_content import TextContent, ThinkingContent


def _search() -> WebSearchCallContent:
    return WebSearchCallContent(
        id="ws_1", status="completed", action={"type": "search", "query": "q"}
    )


def test_search_call_without_replayable_reasoning_is_not_sent() -> None:
    msg = UnifiedMessage(
        role=Role.ASSISTANT,
        content=[
            ThinkingContent(text="thought", provider="openai"),
            _search(),
            TextContent(text="answer"),
        ],
    )
    types = [i.get("type") for i in msg.to_openai_items_modified()]
    assert "web_search_call" not in types


def test_search_call_with_its_reasoning_item_is_kept() -> None:
    msg = UnifiedMessage(
        role=Role.ASSISTANT,
        content=[
            ThinkingContent(text="", provider="openai", id="rs_1", signature="enc", summary=[]),
            _search(),
            TextContent(text="answer"),
        ],
    )
    types = [i.get("type") for i in msg.to_openai_items_modified()]
    assert types.index("reasoning") < types.index("web_search_call")
