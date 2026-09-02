from __future__ import annotations

from matrx_connect import AppContext, ConsoleEmitter, clear_app_context, set_app_context

from matrx_ai.config import (
    ImageContent,
    MessageList,
    TextContent,
    UnifiedConfig,
    UnifiedMessage,
    UnifiedResponse,
)
from matrx_ai.orchestrator.requests import AIMatrixRequest, CompletedRequest


def test_existing_text_round_trips_exactly_and_same_slot_replaces() -> None:
    text = TextContent(text="ORIGINAL", metadata={"citations": [{"id": "c1"}]})
    messages = MessageList(_messages=[UnifiedMessage(role="user", content=[text])])

    messages.attach_ephemeral_to_last_user("FIRST", slot="ctx")
    messages.attach_ephemeral_to_last_user("SECOND", slot="ctx")

    assert "FIRST" not in text.text
    assert "SECOND" in text.text
    assert text.text.endswith("\n\nORIGINAL")
    assert text.to_storage_dict() == {
        "type": "text",
        "text": "ORIGINAL",
        "citations": [{"id": "c1"}],
    }

    messages.detach_ephemeral_from_last_user()
    assert text.text == "ORIGINAL"
    assert text.metadata == {"citations": [{"id": "c1"}]}


def test_media_only_user_omits_and_removes_synthetic_text_carrier() -> None:
    image = ImageContent(url="https://example.com/image.png", mime_type="image/png")
    message = UnifiedMessage(role="user", content=[image])
    messages = MessageList(_messages=[message])

    messages.attach_ephemeral_to_last_user("CONTEXT")

    assert len(message.content) == 2
    storage = message.to_storage_dict()
    assert [block["type"] for block in storage["content"]] == ["media"]
    assert all(block["type"] != "text" for block in storage["content"])

    messages.detach_ephemeral_from_last_user()
    assert message.content == [image]


def test_detach_removes_exact_carrier_if_content_is_reordered() -> None:
    image = ImageContent(url="https://example.com/image.png", mime_type="image/png")
    message = UnifiedMessage(role="user", content=[image])
    messages = MessageList(_messages=[message])
    messages.attach_ephemeral_to_last_user("CONTEXT")
    authored = TextContent(text="LATER")
    message.content.insert(0, authored)

    messages.detach_ephemeral_from_last_user()

    assert message.content == [authored, image]


def test_empty_list_ephemeral_message_never_enters_storage_and_detaches_cleanly() -> None:
    config = UnifiedConfig(model="test-model", messages=MessageList())

    config.messages.attach_ephemeral_to_last_user("CONTEXT")

    assert len(config.messages) == 1
    assert config.messages[0].is_ephemeral_only()
    assert config.to_storage_dict()["messages"] == []

    config.messages.detach_ephemeral_from_last_user()
    assert len(config.messages) == 0


def test_append_after_attach_preserves_real_text_in_storage_and_after_detach() -> None:
    config = UnifiedConfig(model="test-model", messages=MessageList())
    config.messages.attach_ephemeral_to_last_user("CONTEXT")

    config.append_or_extend_user_text("REAL")

    text = config.messages[0].content[0]
    assert isinstance(text, TextContent)
    assert "CONTEXT" in text.text
    assert text.text.endswith("\n\nREAL")
    assert config.to_storage_dict()["messages"] == [
        {"role": "user", "content": [{"type": "text", "text": "REAL"}]}
    ]

    config.messages.detach_ephemeral_from_last_user()
    assert len(config.messages) == 1
    assert text.text == "REAL"


def test_detach_targets_exact_leased_message_after_new_user_is_appended() -> None:
    messages = MessageList()
    messages.attach_ephemeral_to_last_user("CONTEXT")
    messages.append_user_text("NEW USER")

    messages.detach_ephemeral_from_last_user()

    assert len(messages) == 1
    assert messages[0].get_output() == "NEW USER"


def test_variable_replacement_while_attached_updates_pristine_storage_text() -> None:
    text = TextContent(text="Hello {{name}}")
    message = UnifiedMessage(role="user", content=[text])
    messages = MessageList(_messages=[message])
    messages.attach_ephemeral_to_last_user("CONTEXT")

    text.replace_variables({"name": "Ada"})

    assert "CONTEXT" in text.text
    assert text.text.endswith("\n\nHello Ada")
    assert message.to_storage_dict()["content"] == [{"type": "text", "text": "Hello Ada"}]
    messages.detach_ephemeral_from_last_user()
    assert text.text == "Hello Ada"


def test_completed_request_storage_omits_ephemeral_only_message() -> None:
    config = UnifiedConfig(model="test-model", messages=MessageList())
    config.messages.attach_ephemeral_to_last_user("CONTEXT")
    request = AIMatrixRequest(conversation_id="conversation-id", config=config)
    completed = CompletedRequest(
        request=request,
        iterations=0,
        final_response=UnifiedResponse(messages=[]),
    )
    token = set_app_context(AppContext(emitter=ConsoleEmitter(accumulate=False), user_id="user-id"))
    try:
        storage = completed.to_storage_dict()
    finally:
        clear_app_context(token)

    assert storage["messages"] == []
    assert storage["conversation"]["message_count"] == 0


# ---------------------------------------------------------------------------
# Regression: the turn-two role collapse (2026-08-26)
#
# After turn one the system prompt is frozen and every per-turn block rides the
# USER message instead. Two defects lived here: distinct contributors shared one
# slot (last writer annihilated the rest), and the surviving block was pasted
# into the user's text with no provenance, so the model read platform guidance
# as the user speaking and abandoned its role.
# ---------------------------------------------------------------------------


def test_distinct_slots_accumulate_instead_of_annihilating_each_other() -> None:
    text = TextContent(text="USER TURN TWO")
    messages = MessageList(_messages=[UnifiedMessage(role="user", content=[text])])

    # The real frozen-turn call order out of chat_run: skills first, then the
    # context engine block, then the deferred-context manifest.
    messages.attach_ephemeral_to_last_user("<attached_skills>S</attached_skills>", slot="skills")
    messages.attach_ephemeral_to_last_user("<agent_context>A</agent_context>", slot="agent_context")
    messages.attach_ephemeral_to_last_user(
        "<available_context>M</available_context>", slot="context_manifest"
    )

    for survivor in ("<attached_skills>", "<agent_context>", "<available_context>"):
        assert survivor in text.text, f"{survivor} was clobbered by a later slot"

    messages.detach_ephemeral_from_last_user()
    assert text.text == "USER TURN TWO"


def test_platform_blocks_are_framed_as_not_the_user_and_user_text_stays_last() -> None:
    text = TextContent(text="USER TURN TWO")
    messages = MessageList(_messages=[UnifiedMessage(role="user", content=[text])])

    messages.attach_ephemeral_to_last_user("<agent_context>A</agent_context>", slot="agent_context")

    rendered = text.text
    assert rendered.startswith("<turn_context ")
    assert "not_the_user" in rendered
    # The frame must close BEFORE the user's own words, and the user's words
    # must be the last thing the model reads.
    assert rendered.index("</turn_context>") < rendered.index("USER TURN TWO")
    assert rendered.endswith("USER TURN TWO")


def test_frame_is_absent_when_every_slot_is_cleared() -> None:
    text = TextContent(text="USER TURN TWO")
    messages = MessageList(_messages=[UnifiedMessage(role="user", content=[text])])

    messages.attach_ephemeral_to_last_user("BLOCK", slot="agent_context")
    text.attach_ephemeral("", slot="agent_context")

    assert text.text == "USER TURN TWO"
    assert "turn_context" not in text.text
