"""Tests for conversation_enricher — merging local DB + LinkedIn chat history."""

from __future__ import annotations

import pytest

from heylead.services.conversation_enricher import (
    DEDUP_WINDOW_SECONDS,
    fetch_linkedin_history,
    get_enriched_conversation,
    merge_conversation_history,
)


# ── merge_conversation_history tests ──


def test_merge_no_linkedin_messages():
    """When LinkedIn returns nothing, local messages pass through unchanged."""
    local = [
        {"role": "sdr", "text": "Hey!", "timestamp": 1000},
        {"role": "prospect", "text": "Hi", "timestamp": 2000},
    ]
    result = merge_conversation_history(local, [])
    assert result == local


def test_merge_no_local_messages():
    """When local DB is empty, LinkedIn messages are returned."""
    linkedin = [
        {"role": "prospect", "text": "Hello", "timestamp": 500},
        {"role": "sdr", "text": "Hi there", "timestamp": 600},
    ]
    result = merge_conversation_history([], linkedin)
    assert len(result) == 2
    assert result[0]["text"] == "Hello"
    assert result[1]["text"] == "Hi there"


def test_merge_prepends_old_linkedin_messages():
    """LinkedIn messages from before local tracking get prepended."""
    local = [
        {"role": "sdr", "text": "Follow-up", "timestamp": 5000},
    ]
    linkedin = [
        {"role": "prospect", "text": "Old hello", "timestamp": 1000},
        {"role": "sdr", "text": "Old reply", "timestamp": 1100},
    ]
    result = merge_conversation_history(local, linkedin)
    assert len(result) == 3
    assert result[0]["text"] == "Old hello"
    assert result[1]["text"] == "Old reply"
    assert result[2]["text"] == "Follow-up"


def test_merge_dedup_within_window():
    """Messages within the dedup window with same role are deduplicated."""
    local = [
        {"role": "sdr", "text": "Hey!", "timestamp": 1000},
        {"role": "prospect", "text": "Hi", "timestamp": 2000},
    ]
    # LinkedIn has same messages with slightly different timestamps
    linkedin = [
        {"role": "sdr", "text": "Hey!", "timestamp": 1000 + DEDUP_WINDOW_SECONDS - 1},
        {"role": "prospect", "text": "Hi", "timestamp": 2000 + 10},
    ]
    result = merge_conversation_history(local, linkedin)
    # Both LinkedIn messages should be deduped
    assert len(result) == 2


def test_merge_dedup_different_roles_not_deduped():
    """Same timestamp but different roles should NOT be deduped."""
    local = [
        {"role": "sdr", "text": "Hey!", "timestamp": 1000},
    ]
    linkedin = [
        {"role": "prospect", "text": "Hey back!", "timestamp": 1000},
    ]
    result = merge_conversation_history(local, linkedin)
    assert len(result) == 2


def test_merge_dedup_outside_window_not_deduped():
    """Messages outside the dedup window should NOT be deduped."""
    local = [
        {"role": "sdr", "text": "Hey!", "timestamp": 1000},
    ]
    linkedin = [
        {"role": "sdr", "text": "Different msg", "timestamp": 1000 + DEDUP_WINDOW_SECONDS + 1},
    ]
    result = merge_conversation_history(local, linkedin)
    assert len(result) == 2


def test_merge_sorted_output():
    """Merged output should be sorted by timestamp ascending."""
    local = [
        {"role": "sdr", "text": "Later msg", "timestamp": 5000},
    ]
    linkedin = [
        {"role": "prospect", "text": "Earlier msg", "timestamp": 1000},
        {"role": "sdr", "text": "Middle msg", "timestamp": 3000},
    ]
    result = merge_conversation_history(local, linkedin)
    timestamps = [m["timestamp"] for m in result]
    assert timestamps == sorted(timestamps)


# ── fetch_linkedin_history tests ──


class MockLinkedInClient:
    """Mock LinkedIn client for testing."""

    def __init__(self, messages: list[dict] | None = None, raise_error: bool = False):
        self._messages = messages or []
        self._raise_error = raise_error

    async def get_chat_messages(self, account_id: str, chat_id: str, limit: int = 20):
        if self._raise_error:
            raise Exception("API error")
        return self._messages

    async def close(self):
        pass


@pytest.mark.asyncio
async def test_fetch_linkedin_history_sender_mapping():
    """Sender ID matching should correctly assign sdr vs prospect roles."""
    client = MockLinkedInClient(messages=[
        {"sender_id": "ACoAAA123", "text": "My message", "timestamp": 1000},
        {"sender_id": "ACoAAA456", "text": "Their reply", "timestamp": 2000},
    ])
    result = await fetch_linkedin_history(
        client, "acc1", "chat1", sender_provider_id="ACoAAA123",
    )
    assert len(result) == 2
    assert result[0]["role"] == "sdr"
    assert result[1]["role"] == "prospect"


@pytest.mark.asyncio
async def test_fetch_linkedin_history_empty_text_skipped():
    """Messages with empty text should be filtered out."""
    client = MockLinkedInClient(messages=[
        {"sender_id": "ACoAAA123", "text": "", "timestamp": 1000},
        {"sender_id": "ACoAAA123", "text": "Real message", "timestamp": 2000},
    ])
    result = await fetch_linkedin_history(
        client, "acc1", "chat1", sender_provider_id="ACoAAA123",
    )
    assert len(result) == 1
    assert result[0]["text"] == "Real message"


@pytest.mark.asyncio
async def test_fetch_linkedin_history_sorted_chronologically():
    """Output should be sorted oldest-first regardless of API order."""
    client = MockLinkedInClient(messages=[
        {"sender_id": "ACoAAA123", "text": "Newer", "timestamp": 5000},
        {"sender_id": "ACoAAA456", "text": "Older", "timestamp": 1000},
    ])
    result = await fetch_linkedin_history(
        client, "acc1", "chat1", sender_provider_id="ACoAAA123",
    )
    assert result[0]["timestamp"] < result[1]["timestamp"]


# ── get_enriched_conversation tests ──


@pytest.mark.asyncio
async def test_get_enriched_conversation_no_chat_id(monkeypatch):
    """When chat_id is None, should return local-only messages."""
    local_msgs = [{"role": "sdr", "text": "Hey", "timestamp": 1000}]
    monkeypatch.setattr(
        "heylead.services.conversation_enricher.get_messages_for_outreach",
        lambda oid: local_msgs,
    )
    client = MockLinkedInClient()
    result = await get_enriched_conversation(
        client, "acc1", None, "outreach1", "ACoAAA123",
    )
    assert result == local_msgs


@pytest.mark.asyncio
async def test_get_enriched_conversation_api_error_fallback(monkeypatch):
    """When LinkedIn API fails, should fall back to local-only messages."""
    local_msgs = [{"role": "sdr", "text": "Hey", "timestamp": 1000}]
    monkeypatch.setattr(
        "heylead.services.conversation_enricher.get_messages_for_outreach",
        lambda oid: local_msgs,
    )
    client = MockLinkedInClient(raise_error=True)
    result = await get_enriched_conversation(
        client, "acc1", "chat1", "outreach1", "ACoAAA123",
    )
    assert result == local_msgs


@pytest.mark.asyncio
async def test_get_enriched_conversation_merges_history(monkeypatch):
    """Should merge LinkedIn and local messages together."""
    local_msgs = [{"role": "sdr", "text": "Follow-up", "timestamp": 5000}]
    monkeypatch.setattr(
        "heylead.services.conversation_enricher.get_messages_for_outreach",
        lambda oid: local_msgs,
    )
    client = MockLinkedInClient(messages=[
        {"sender_id": "ACoAAA456", "text": "Old hello", "timestamp": 1000},
        {"sender_id": "ACoAAA123", "text": "Old reply", "timestamp": 1100},
    ])
    result = await get_enriched_conversation(
        client, "acc1", "chat1", "outreach1", "ACoAAA123",
    )
    assert len(result) == 3
    assert result[0]["text"] == "Old hello"
    assert result[0]["role"] == "prospect"
    assert result[2]["text"] == "Follow-up"
