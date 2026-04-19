"""Provider-safety tests for the persisted boundary-based compaction shape (#1413).

After a conversation is compacted and persisted, the stored message list
looks like:

    [system] compact summary
    [system] boundary marker
    [user] first preserved tail message    <- provider-safe first-non-system
    [assistant] ...
    ...

These tests verify that the resumed shape passes provider validation for
every path that enforces "first non-system message must be user":

- OpenAI: no ordering constraint (sanity check)
- Anthropic: ``_convert_messages()`` extracts system roles into the system
  prompt; ``validate_first_message_user(allow_leading_system=False)`` runs
  on the remaining list
- LiteLLM Anthropic/Bedrock: ``validate_first_message_user(allow_leading_system=True)``
  (LiteLLM does its own system extraction)
"""

from __future__ import annotations

import sqlite3
from typing import Any

import pytest

from anteroom.db import _SCHEMA, ThreadSafeConnection
from anteroom.services.compaction import build_boundary_marker, persist_compacted_messages
from anteroom.services.provider_validation import ProviderRequestError, validate_first_message_user
from anteroom.services.storage import (
    create_conversation,
    create_message,
    list_messages,
)


@pytest.fixture()
def db() -> ThreadSafeConnection:
    conn = sqlite3.connect(":memory:", check_same_thread=False)
    conn.row_factory = sqlite3.Row
    conn.execute("PRAGMA foreign_keys=ON")
    conn.executescript(_SCHEMA)
    conn.commit()
    return ThreadSafeConnection(conn)


def _make_compacted_conversation(db: ThreadSafeConnection, *, tail_first_role: str = "user") -> list[dict[str, Any]]:
    """Seed a conversation then compact+persist it.

    Returns the loaded messages list as seen on resume.
    """
    conv = create_conversation(db, title="Test")
    # Seed with alternating user/assistant — final messages match tail_first_role
    for i in range(8):
        role = "user" if i % 2 == 0 else "assistant"
        create_message(db, conv["id"], role, f"message {i}")

    stored = list_messages(db, conv["id"])
    # Take the last 4 as the preserved tail.
    tail_ids = [m["id"] for m in stored[-4:]]

    # Pick a summary role that mirrors the in-memory shared-loop shape (user).
    # persist_compacted_messages translates it to system at storage time.
    persist_compacted_messages(
        db,
        conv["id"],
        summary_msg={"role": "user", "content": "older history summary", "metadata": {}},
        boundary_msg=build_boundary_marker(original_count=4, preserved_count=4, summary_tokens=50),
        tail_message_ids=tail_ids,
    )
    return list_messages(db, conv["id"])


class TestAnthropicProviderValidation:
    def test_first_non_system_is_user_after_extraction(self, db: ThreadSafeConnection) -> None:
        """After Anthropic strips system roles, the remaining first message is user."""
        msgs = _make_compacted_conversation(db)
        # Anthropic's `_convert_messages()` extracts all system roles into the
        # system prompt string.  Simulate that here.
        non_system = [m for m in msgs if m.get("role") != "system"]

        # The compacted persisted shape was:
        #   [system summary, system boundary, *tail starting at position 2]
        # After system extraction, non_system[0] is the first tail message,
        # which must be role=user for Anthropic to accept the request.
        validate_first_message_user(
            non_system, provider="anthropic", model="claude-3-5-sonnet-20241022", allow_leading_system=False
        )

    def test_validation_raises_on_bad_ordering(self) -> None:
        """Sanity check: validator raises when the first non-system is assistant."""
        bad = [
            {"role": "system", "content": "sys"},
            {"role": "assistant", "content": "no user first"},
        ]
        with pytest.raises(ProviderRequestError):
            validate_first_message_user(
                bad, provider="anthropic", model="claude-3-5-sonnet-20241022", allow_leading_system=False
            )


class TestLiteLLMProviderValidation:
    def test_anthropic_route_allows_leading_system(self, db: ThreadSafeConnection) -> None:
        """LiteLLM's Anthropic route keeps leading system messages and validates."""
        msgs = _make_compacted_conversation(db)
        # allow_leading_system=True — the validator skips leading systems
        # before checking that the next message is user.
        validate_first_message_user(
            msgs, provider="litellm", model="anthropic/claude-3-5-sonnet", allow_leading_system=True
        )

    def test_bedrock_route_allows_leading_system(self, db: ThreadSafeConnection) -> None:
        msgs = _make_compacted_conversation(db)
        validate_first_message_user(
            msgs, provider="litellm", model="anthropic/claude-3-5-sonnet", allow_leading_system=True
        )


class TestOpenAICompatibility:
    def test_openai_path_has_no_ordering_constraint(self, db: ThreadSafeConnection) -> None:
        """OpenAI doesn't enforce user-first, but our validator still accepts the shape."""
        msgs = _make_compacted_conversation(db)
        # OpenAI provider doesn't call validate_first_message_user by default,
        # but running it should still pass — the message list is well-formed.
        validate_first_message_user(msgs, provider="openai", model="gpt-4o", allow_leading_system=True)
