"""The titler quotes what the person typed — never the Python repr of their message's blocks.

Live 2026-10-20 (snapshot 9f2bfc6d): the Agent Conversation Labeler received
``What I typed myself:\\n[{'type': 'text', 'text': "Every Monday morning, ..."}]`` because the
executor passed ``str(content)`` for a block-list message.
"""

from __future__ import annotations

from matrx_utils.source_guard import stable_source

from matrx_ai.config.typed_text_last import typed_words_of
from matrx_ai.config.unified_content import TextContent


def test_a_block_list_message_gives_its_words() -> None:
    content = [{"type": "text", "text": "Every Monday morning, pull the notes.", "id": "", "metadata": {}}]
    assert typed_words_of(content) == "Every Monday morning, pull the notes."


def test_attachments_carry_no_words_and_text_objects_count() -> None:
    content = [{"type": "image", "url": "https://x/y.png"}, TextContent(text="Use the attached notes.")]
    assert typed_words_of(content) == "Use the attached notes."
    assert typed_words_of("plain") == "plain"
    assert typed_words_of(None) == ""


def test_the_executor_never_stringifies_the_persons_message_for_the_titler() -> None:
    from matrx_ai.orchestrator import executor

    source = stable_source(executor)
    assert "user_prompt = typed_words_of(" in source
    assert "else str(content)" not in source
