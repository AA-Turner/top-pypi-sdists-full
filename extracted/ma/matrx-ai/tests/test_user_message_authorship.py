"""What a stored user message contains, and who is recorded as having written it.

Inherited from the retired ``test_ephemeral_message_lease.py``: the per-turn
platform block no longer lives inside a message at all (see
``test_the_persons_turn_is_the_persons_alone.py``), but the authorship split
these cases pin — ``content`` is the provider payload, ``user_content`` is the
human's own words — is unchanged and still load-bearing.
"""

from __future__ import annotations

from matrx_ai.config import (
    ImageContent,
    MessageList,
    TextContent,
    UnifiedConfig,
    UnifiedMessage,
)


def test_authored_text_round_trips_into_storage_exactly() -> None:
    text = TextContent(text="ORIGINAL", metadata={"citations": [{"id": "c1"}]})
    messages = MessageList(_messages=[UnifiedMessage(role="user", content=[text])])
    messages.attach_turn_context("PLATFORM BLOCK", slot="ctx")

    assert text.text == "ORIGINAL"
    assert text.to_storage_dict() == {
        "type": "text",
        "text": "ORIGINAL",
        "citations": [{"id": "c1"}],
    }


def test_a_media_only_user_message_never_grows_a_text_block() -> None:
    image = ImageContent(url="https://example.com/image.png", mime_type="image/png")
    message = UnifiedMessage(role="user", content=[image])
    messages = MessageList(_messages=[message])

    messages.attach_turn_context("CONTEXT")

    assert message.content == [image]
    assert [block["type"] for block in message.to_storage_dict()["content"]] == ["media"]


def test_the_turn_channel_never_invents_a_message() -> None:
    config = UnifiedConfig(model="test-model", messages=MessageList())

    config.messages.attach_turn_context("CONTEXT")

    assert len(config.messages) == 0
    assert config.to_storage_dict()["messages"] == []


def test_appending_user_text_after_staging_context_stores_only_the_text() -> None:
    config = UnifiedConfig(model="test-model", messages=MessageList())
    config.messages.attach_turn_context("CONTEXT")

    config.append_or_extend_user_text("REAL")

    assert config.to_storage_dict()["messages"] == [
        {
            "role": "user",
            "content": [{"type": "text", "text": "REAL"}],
            "user_content": [{"type": "text", "text": "REAL"}],
        }
    ]


def test_agent_template_and_pristine_user_content_persist_separately() -> None:
    messages = MessageList(
        _messages=[
            UnifiedMessage(
                role="user",
                content=[TextContent(text="MACHINE: resolved context")],
            )
        ]
    )

    messages.append_or_extend_user_text("HUMAN: my actual words")

    storage = messages[0].to_storage_dict()
    assert storage["content"] == [
        {
            "type": "text",
            "text": "MACHINE: resolved context\nHUMAN: my actual words",
        }
    ]
    assert storage["user_content"] == [{"type": "text", "text": "HUMAN: my actual words"}]

    hydrated = UnifiedMessage.from_dict(storage)
    assert hydrated.to_storage_dict() == storage


def test_variable_replacement_updates_the_stored_text() -> None:
    text = TextContent(text="Hello {{name}}")
    message = UnifiedMessage(role="user", content=[text])
    messages = MessageList(_messages=[message])
    messages.attach_turn_context("CONTEXT")

    text.replace_variables({"name": "Ada"})

    assert text.text == "Hello Ada"
    assert message.to_storage_dict()["content"] == [{"type": "text", "text": "Hello Ada"}]
