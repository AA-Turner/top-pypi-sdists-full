"""The permanent Personal Staff thread is named for WHO the person is
talking to, never for the first topic — it must never be auto-titled.

THE DEFECT (adjudication 2026-09-21). Production row
``3755cc8a-4ab8-5127-b99d-955819018c6e`` — the person's one permanent staff
thread — was retitled "Supabase Backup Basics" with topic keywords attached
by the conversation-labeler on its first turn, exactly like any ordinary
chat. The thread's own persisted ``metadata.channel == "staff"`` is the
constant every door (SMS, voice, the signed-in ``/staff`` app) agrees on;
``_run_labeling`` must check it and refuse to spend an LLM call or write a
title/description/keywords when it is set.

Proven failing at the pre-fix behaviour (asserted directly against
``_is_staff_channel_conversation`` and by exercising ``_run_labeling`` end to
end with every downstream call stubbed to record whether it ran), then
passing after the guard: a staff-channel conversation makes zero calls past
the check; an ordinary conversation is unaffected.
"""

from __future__ import annotations

from types import SimpleNamespace

import matrx_ai.agents.services.conversation_labeler as labeler
from matrx_ai.agent_runners.conversation_labeler import LabelResult


class _FakeConversationModel:
    def __init__(self, metadata: dict | None):
        self._row = SimpleNamespace(metadata=metadata) if metadata is not None else None

    def filter(self, **kwargs):
        return self

    def limit(self, _n):
        return self

    async def all(self):
        return [self._row] if self._row is not None else []


class _FakeConversationManager:
    def __init__(self, metadata: dict | None):
        self.model = _FakeConversationModel(metadata)


class _FakeCxm:
    def __init__(self, metadata: dict | None):
        self.conversation = _FakeConversationManager(metadata)


async def test_is_staff_channel_conversation_true_for_staff_metadata(monkeypatch):
    monkeypatch.setattr(labeler, "cxm", _FakeCxm({"channel": "staff"}))
    assert await labeler._is_staff_channel_conversation("cid-1") is True


async def test_is_staff_channel_conversation_false_for_ordinary_chat(monkeypatch):
    monkeypatch.setattr(labeler, "cxm", _FakeCxm({"channel": "web"}))
    assert await labeler._is_staff_channel_conversation("cid-2") is False


async def test_is_staff_channel_conversation_false_when_row_missing(monkeypatch):
    monkeypatch.setattr(labeler, "cxm", _FakeCxm(None))
    assert await labeler._is_staff_channel_conversation("cid-3") is False


async def test_run_labeling_skips_staff_thread_before_any_llm_call(monkeypatch):
    """THE GUARD. Before the fix, ``_run_labeling`` always called
    ``_fetch_recent_titles`` / the labeling model / ``_update_conversation_labels``
    regardless of channel — this is the exact call sequence that overwrote the
    staff thread's title in production. Every downstream call is stubbed to
    append to ``called``; with the guard in place none of them fire."""
    called: list[str] = []

    async def _fetch_recent_titles(_user_id):
        called.append("fetch_recent_titles")
        return []

    async def _label_chat_conversation(**kwargs):
        called.append("label_chat_conversation")
        raise AssertionError("must never call the labeling model for the staff thread")

    async def _update_conversation_labels(*args, **kwargs):
        called.append("update_conversation_labels")

    monkeypatch.setattr(labeler, "cxm", _FakeCxm({"channel": "staff"}))
    monkeypatch.setattr(labeler, "_fetch_recent_titles", _fetch_recent_titles)
    monkeypatch.setattr(labeler, "label_chat_conversation", _label_chat_conversation)
    monkeypatch.setattr(labeler, "_update_conversation_labels", _update_conversation_labels)

    await labeler._run_labeling(
        conversation_id="3755cc8a-4ab8-5127-b99d-955819018c6e",
        user_id="user-1",
        messages=[{"role": "user", "content": "back up my supabase project"}],
    )

    assert called == []


async def test_run_labeling_still_labels_an_ordinary_conversation(monkeypatch):
    """The guard must not swallow ordinary chats — belt-and-suspenders on the
    fix itself: a non-staff conversation reaches the update call as before."""
    called: list[str] = []

    async def _fetch_recent_titles(_user_id):
        called.append("fetch_recent_titles")
        return []

    async def _label_chat_conversation(**kwargs):
        called.append("label_chat_conversation")
        return LabelResult(
            success=True,
            output='{"label": "Trip Planning", "description": "d", "keywords": ["travel"]}',
        )

    async def _update_conversation_labels(conversation_id, user_id, fields):
        called.append("update_conversation_labels")
        assert fields["title"] == "Trip Planning"

    monkeypatch.setattr(labeler, "cxm", _FakeCxm({"channel": "web"}))
    monkeypatch.setattr(labeler, "_fetch_recent_titles", _fetch_recent_titles)
    monkeypatch.setattr(labeler, "label_chat_conversation", _label_chat_conversation)
    monkeypatch.setattr(labeler, "_update_conversation_labels", _update_conversation_labels)
    monkeypatch.setattr(labeler, "try_get_app_context", lambda: None)

    await labeler._run_labeling(
        conversation_id="cid-ordinary",
        user_id="user-1",
        messages=[{"role": "user", "content": "plan my trip to Japan"}],
    )

    assert called == ["fetch_recent_titles", "label_chat_conversation", "update_conversation_labels"]
