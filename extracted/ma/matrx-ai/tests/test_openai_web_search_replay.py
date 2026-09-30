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


def test_search_call_after_an_unreplayable_reasoning_is_dropped_even_if_another_was_kept() -> None:
    """Live refusal #2: an earlier signed reasoning was replayed, the search's OWN reasoning was
    not — OpenAI still refused the search call."""
    msg = UnifiedMessage(
        role=Role.ASSISTANT,
        content=[
            ThinkingContent(text="", provider="openai", id="rs_1", signature="enc", summary=[]),
            _search(),
            TextContent(text="interim"),
            ThinkingContent(text="thought", provider="openai"),
            WebSearchCallContent(
                id="ws_2", status="completed", action={"type": "search", "query": "q2"}
            ),
        ],
    )
    ids = [
        i.get("id") for i in msg.to_openai_items_modified() if i.get("type") == "web_search_call"
    ]
    assert ids == ["ws_1"]


def test_two_search_calls_in_a_row_keep_only_the_one_with_reasoning() -> None:
    """Live refusal #3: the provider stored one reasoning item then two search calls; the second
    call had no reasoning of its own and OpenAI refused it."""
    msg = UnifiedMessage(
        role=Role.ASSISTANT,
        content=[
            ThinkingContent(text="", provider="openai", id="rs_1", signature="enc", summary=[]),
            _search(),
            WebSearchCallContent(
                id="ws_2", status="completed", action={"type": "search", "query": "q2"}
            ),
            TextContent(text="answer"),
        ],
    )
    ids = [
        i.get("id") for i in msg.to_openai_items_modified() if i.get("type") == "web_search_call"
    ]
    assert ids == ["ws_1"]


def test_response_keeps_reasoning_and_search_interleaved() -> None:
    """Root cause: the response was regrouped as all reasoning then all searches, so on replay
    each search no longer followed its own reasoning item."""
    from types import SimpleNamespace as NS

    from matrx_ai.providers.openai.translator import OpenAITranslator

    class _Item(NS):
        def model_dump(self, exclude=None):  # noqa: ANN001, ANN201
            return {}

    items = [
        _Item(type="reasoning", id="rs_1", summary=[], encrypted_content="e1"),
        _Item(type="web_search_call", id="ws_1", status="completed", action=None),
        _Item(type="reasoning", id="rs_2", summary=[], encrypted_content="e2"),
        _Item(type="web_search_call", id="ws_2", status="completed", action=None),
    ]
    translator = OpenAITranslator.__new__(OpenAITranslator)
    messages = translator._build_unified_messages(items)
    order = [getattr(c, "id", None) for m in messages for c in m.content]
    assert order[:4] == ["rs_1", "ws_1", "rs_2", "ws_2"]
    replay = [i["id"] for m in messages for i in m.to_openai_items_modified() if "id" in i]
    assert replay[:4] == ["rs_1", "ws_1", "rs_2", "ws_2"]
