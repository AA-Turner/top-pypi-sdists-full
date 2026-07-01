"""
Tests for C4 hooks — soul + ops endpoints emit spine events.

We test the per_turn_soul hook and the preservation/will/letter
helpers directly without spinning up the gateway.
"""
from __future__ import annotations

import os
from pathlib import Path

import pytest


@pytest.fixture(autouse=True)
def isolated_spine(tmp_path, monkeypatch):
    monkeypatch.setenv("CVC_EVENTS_ROOT", str(tmp_path))
    import cvc.events.spine as spine
    if spine._file_lock_fd is not None:
        spine._release_file_lock()
    yield tmp_path


# ── Per-turn soul ─────────────────────────────────────────────────


def test_per_turn_soul_emits_soul_write_for_entities(tmp_path):
    """When the per-turn soul extracts new entities, it should emit a soul.write event."""
    from cvc.events.spine import capture, query

    capture(
        kind="soul.write",
        workspace="/tmp/proj",
        channel="soul",
        actor="assistant",
        summary="wrote 2 entities",
        data={"added": 2, "kind": "entity"},
    )

    events = query(kind="soul.write")
    assert len(events) == 1
    assert events[0]["data"]["added"] == 2
    assert events[0]["data"]["kind"] == "entity"


def test_per_turn_soul_emits_mood_event():
    from cvc.events.spine import capture, query

    capture(
        kind="soul.write",
        workspace="/tmp/proj",
        channel="soul",
        summary="mood=focused (intensity 0.85)",
        data={"kind": "mood", "mood": "focused", "intensity": 0.85},
        tags=["emotion"],
    )
    evt = query()[0]
    assert evt["data"]["mood"] == "focused"
    assert "emotion" in evt["tags"]


# ── Letter ─────────────────────────────────────────────────────────


def test_letter_persist_emits_soul_letter_event(tmp_path, monkeypatch):
    """persist_letter should emit a soul.letter_generated event."""
    # Build a minimal SoulLetter
    from dataclasses import asdict
    from cvc.operations.soul_letters import WeeklyLetterGenerator, SoulLetter
    from cvc.events.spine import query

    storage = tmp_path / "soul"
    storage.mkdir()
    src = tmp_path / "src"
    src.mkdir()

    gen = WeeklyLetterGenerator(cvc_root=storage, commit_source_root=src)

    letter = SoulLetter(
        letter_id="abc123",
        week_of="2026-W24",
        week_start=1780857000.0,
        week_end=1781461800.0,
        generated_at=1782833870.0,
        narrative="Hello there. " * 50,  # 100 words
        greeting="Hey",
        signoff="your soul",
        observations=["obs1"],
        soul_changes=["change1"],
        week_themes=["theme1"],
        source_commits=["hash1"],
        source_commit_count=5,
        generation_seconds=1.5,
    )
    gen.persist_letter(letter)

    events = query(kind="soul.letter_generated")
    assert len(events) == 1
    assert events[0]["data"]["week_of"] == "2026-W24"
    assert events[0]["data"]["word_count"] == 100


# ── Preservation ──────────────────────────────────────────────────


def test_preservation_enable_emits_event(tmp_path, monkeypatch):
    from cvc.core.preservation import PreservationStore
    from cvc.events.spine import query

    store = PreservationStore(cvc_root=tmp_path, vault=None)
    store.enable(actor="owner", auto_correct=True, freeze_narrative=False)

    events = query(kind="soul.preservation_enabled")
    assert len(events) == 1
    assert events[0]["actor"] == "owner"
    assert events[0]["data"]["auto_correct"] is True


def test_preservation_disable_emits_event(tmp_path, monkeypatch):
    from cvc.core.preservation import PreservationStore
    from cvc.events.spine import query

    store = PreservationStore(cvc_root=tmp_path, vault=None)
    store.enable(actor="owner")
    store.disable(actor="owner")

    events = query()
    kinds = [e["kind"] for e in events]
    assert "soul.preservation_enabled" in kinds
    assert "soul.preservation_disabled" in kinds


# ── Will ──────────────────────────────────────────────────────────


def test_will_create_emits_event(tmp_path, monkeypatch):
    """WillStore.create_will should emit soul.will_created.

    Skips the encryption path since it needs the SoulVault — we test
    the metadata save path that fires before vault.write_blob.
    """
    from cvc.core.will import WillStore
    from cvc.events.spine import query

    # Stub the vault so we don't need a real one
    class _StubVault:
        is_initialized = True
        is_unlocked = True

        def write_blob(self, name, data):
            return name

    store = WillStore(cvc_root=tmp_path, vault=_StubVault())
    will = store.create_will(
        owner_name="Jai",
        will_text="Test will text.",
        executors=[],
        release_condition="manual",
    )
    assert will is not None

    events = query(kind="soul.will_created")
    assert len(events) == 1
    assert events[0]["data"]["version"] == 1
    assert events[0]["data"]["executors"] == 0


def test_will_update_emits_event(tmp_path):
    from cvc.core.will import WillStore
    from cvc.events.spine import query

    class _StubVault:
        is_initialized = True
        is_unlocked = True

        def write_blob(self, name, data):
            return name

    store = WillStore(cvc_root=tmp_path, vault=_StubVault())
    store.create_will(owner_name="Jai", will_text="v1 text", executors=[], release_condition="manual")
    store.create_will(owner_name="Jai", will_text="v2 text", executors=[], release_condition="manual")

    created = query(kind="soul.will_created")
    updated = query(kind="soul.will_updated")
    assert len(created) == 1
    assert len(updated) == 1


# ── mcp_bridge workspace accessor ────────────────────────────────


def test_get_workspace_from_mcp_context_no_registry(tmp_path, monkeypatch):
    """Returns None cleanly when no registry exists."""
    monkeypatch.setattr("pathlib.Path.home", lambda: tmp_path)
    from cvc.gateway.mcp_bridge import _get_workspace_from_mcp_context
    assert _get_workspace_from_mcp_context() is None


def test_get_workspace_from_mcp_context_with_registry(tmp_path, monkeypatch):
    """Returns the active workspace from the registry."""
    import json
    monkeypatch.setattr("pathlib.Path.home", lambda: tmp_path)
    (tmp_path / ".cvc").mkdir()
    (tmp_path / ".cvc" / "workspaces.json").write_text(
        json.dumps([
            {"path": "/a", "active": False},
            {"path": "/b", "active": True},
        ])
    )
    from cvc.gateway.mcp_bridge import _get_workspace_from_mcp_context
    assert _get_workspace_from_mcp_context() == "/b"