from datetime import UTC, datetime

from aviary.core import Message, ToolRequestMessage, ToolResponseMessage

from edison_client.models.chat import ConversationMessage

_CREATED_AT = datetime.now(UTC)


def test_plain_message_becomes_message() -> None:
    m = ConversationMessage(
        role="assistant", content="hello", created_at=_CREATED_AT
    ).to_aviary_message()
    assert type(m) is Message  # not a tool subclass
    assert m.role == "assistant"
    assert m.content == "hello"


def test_tool_calls_become_tool_request_message() -> None:
    cm = ConversationMessage(
        role="assistant",
        content="calling search",
        created_at=_CREATED_AT,
        tool_calls=[
            {
                "id": "c1",
                "type": "function",
                "function": {"name": "search", "arguments": '{"q": "x"}'},
            }
        ],
    )
    m = cm.to_aviary_message()
    assert isinstance(m, ToolRequestMessage)
    assert len(m.tool_calls) == 1
    assert m.tool_calls[0].function.name == "search"


def test_tool_call_id_becomes_tool_response_message() -> None:
    cm = ConversationMessage(
        role="tool",
        content="result",
        tool_call_id="c1",
        name="search",
        created_at=_CREATED_AT,
    )
    m = cm.to_aviary_message()
    assert isinstance(m, ToolResponseMessage)
    assert m.tool_call_id == "c1"
    assert m.name == "search"


def test_info_round_trips_to_aviary_info() -> None:
    cm = ConversationMessage(
        role="user",
        content="hi",
        info={"is_human": False, "sort_order": 3},
        created_at=_CREATED_AT,
    )
    m = cm.to_aviary_message()
    assert m.info == {"is_human": False, "sort_order": 3}


def test_multimodal_content_round_trips() -> None:
    blocks = [
        {"type": "text", "text": "hi"},
        {"type": "image_url", "image_url": {"url": "data:image/png;base64,AAAA"}},
    ]
    m = ConversationMessage(
        role="user", content=blocks, created_at=_CREATED_AT
    ).to_aviary_message()
    assert type(m) is Message
    # list content survives as multimodal blocks (not stringified)
    assert m.deserialized_content == blocks
