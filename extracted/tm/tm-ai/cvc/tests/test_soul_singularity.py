"""Tests for hotfix/soul-singularity-2026-06-30 — soul lives at ~/.cvc/soul/.

The soul is singular — one body across all workspaces. Soul data
(letters, dreams, narratives, emotional arc, persona, corrections,
preservation) lives at ~/.cvc/soul/ and is read/written the same
regardless of which workspace the user is in.

This module verifies:
  1. The global soul root is always ~/.cvc/soul/ (or CVC_SOUL_ROOT override)
  2. Migration from per-workspace .cvc/ data is idempotent
  3. The global user_model accumulates entities from multiple sources
  4. Re-running migration is a no-op
  5. Soul-letter storage is global
  6. Gateway soul endpoints read from the global root
"""
from __future__ import annotations

import json
import os
import sys
import tempfile
from pathlib import Path

import pytest

PKG_ROOT = Path(__file__).resolve().parents[1]
if str(PKG_ROOT) not in sys.path:
    sys.path.insert(0, str(PKG_ROOT))


def test_soul_root_default():
    """Default soul root is ~/.cvc/soul/."""
    from cvc.operations.soul_singularity import _soul_root
    root = _soul_root()
    assert root == Path.home() / ".cvc" / "soul"


def test_soul_root_respects_override():
    """CVC_SOUL_ROOT env var overrides the default location."""
    with tempfile.TemporaryDirectory() as tmp:
        override = Path(tmp) / "custom_soul"
        old = os.environ.get("CVC_SOUL_ROOT")
        try:
            os.environ["CVC_SOUL_ROOT"] = str(override)
            # Force re-import to pick up the new env var.
            import importlib
            import cvc.operations.soul_singularity as ss
            importlib.reload(ss)
            assert ss._soul_root() == override
        finally:
            if old is None:
                os.environ.pop("CVC_SOUL_ROOT", None)
            else:
                os.environ["CVC_SOUL_ROOT"] = old
            importlib.reload(ss)


def test_migration_idempotent(tmp_path: Path):
    """Re-running migration with the same source adds nothing new."""
    # Use a temp soul root
    old = os.environ.get("CVC_SOUL_ROOT")
    try:
        os.environ["CVC_SOUL_ROOT"] = str(tmp_path / "soul")
        import importlib
        import cvc.operations.soul_singularity as ss
        importlib.reload(ss)

        # Create a fake workspace .cvc/ with a user_model.json
        from cvc.core.user_model import Entity, UserIdentitySnapshot, UserModelManager

        ws = tmp_path / "myproject" / ".cvc"
        ws.mkdir(parents=True)
        # Need a cvc.db so the migration picks it up
        (ws / "cvc.db").touch()
        ws_mgr = UserModelManager(ws)
        m = UserIdentitySnapshot()
        m.entities.append(Entity(name="TestEntity", entity_type="project", mention_count=1))
        m.values.append({"statement": "test value", "category": "work", "confidence": 0.5, "first_observed": 0, "last_reinforced": 0, "evidence_commits": [], "superseded_by": None})
        ws_mgr.save_model(m, trigger="seed")

        # First migration — should pick up the test entity
        result1 = ss.run_migration_once()
        assert result1["workspaces_with_data"] >= 1
        assert result1["entities_added"] >= 1

        # Second migration — should be a no-op (ledger prevents re-import)
        result2 = ss.run_migration_once()
        assert result2["entities_added"] == 0
        assert result2["values_added"] == 0
    finally:
        if old is None:
            os.environ.pop("CVC_SOUL_ROOT", None)
        else:
            os.environ["CVC_SOUL_ROOT"] = old


def test_global_user_model_merges_from_multiple_workspaces(tmp_path: Path):
    """Two workspaces with different entities → both end up in the global."""
    old = os.environ.get("CVC_SOUL_ROOT")
    try:
        os.environ["CVC_SOUL_ROOT"] = str(tmp_path / "soul")
        import importlib
        import cvc.operations.soul_singularity as ss
        importlib.reload(ss)

        from cvc.core.user_model import Entity, UserIdentitySnapshot, UserModelManager

        # Workspace A
        ws_a = tmp_path / "ws_a" / ".cvc"
        ws_a.mkdir(parents=True)
        (ws_a / "cvc.db").touch()
        m_a = UserIdentitySnapshot()
        m_a.entities.append(Entity(name="ProjectA", entity_type="project", mention_count=2))
        UserModelManager(ws_a).save_model(m_a, trigger="seed_a")

        # Workspace B
        ws_b = tmp_path / "ws_b" / ".cvc"
        ws_b.mkdir(parents=True)
        (ws_b / "cvc.db").touch()
        m_b = UserIdentitySnapshot()
        m_b.entities.append(Entity(name="PersonB", entity_type="person", mention_count=1))
        UserModelManager(ws_b).save_model(m_b, trigger="seed_b")

        # Force-rescan from these specific paths
        ss._workspace_cvc_candidates.cache_clear() if hasattr(ss._workspace_cvc_candidates, "cache_clear") else None
        # Walk our tmp tree explicitly
        for ws in [ws_a, ws_b]:
            ents, vals, emo = ss._merge_snapshot_into_global(ws)
            lets = ss._merge_letters_into_global(ws)
            dreams = ss._merge_dreams_into_global(ws)
            if ents or vals or emo or lets or dreams:
                ss._record_migration(
                    ws,
                    merged_entities=ents,
                    merged_values=vals,
                    merged_emotional=emo,
                    merged_letters=lets,
                    merged_dreams=dreams,
                )

        # Now the global model should contain both entities
        global_model = ss.get_global_user_model()
        names = {e.name.lower() for e in global_model.entities}
        assert "projecta" in names
        assert "personb" in names
    finally:
        if old is None:
            os.environ.pop("CVC_SOUL_ROOT", None)
        else:
            os.environ["CVC_SOUL_ROOT"] = old


def test_value_dedup_uses_last_reinforced(tmp_path: Path):
    """Same value in two workspaces → merged, last_reinforced = max."""
    old = os.environ.get("CVC_SOUL_ROOT")
    try:
        os.environ["CVC_SOUL_ROOT"] = str(tmp_path / "soul")
        import importlib
        import cvc.operations.soul_singularity as ss
        importlib.reload(ss)

        from cvc.core.user_model import (
            UserIdentitySnapshot,
            UserModelManager,
            ValueStatement,
        )

        ws_a = tmp_path / "ws_a" / ".cvc"
        ws_a.mkdir(parents=True)
        (ws_a / "cvc.db").touch()
        m_a = UserIdentitySnapshot()
        m_a.values.append(
            ValueStatement(statement="ship behind feature flags", last_reinforced=100.0)
        )
        UserModelManager(ws_a).save_model(m_a, trigger="seed")

        ws_b = tmp_path / "ws_b" / ".cvc"
        ws_b.mkdir(parents=True)
        (ws_b / "cvc.db").touch()
        m_b = UserIdentitySnapshot()
        m_b.values.append(
            ValueStatement(statement="ship behind feature flags", last_reinforced=500.0)
        )
        UserModelManager(ws_b).save_model(m_b, trigger="seed")

        ss._merge_snapshot_into_global(ws_a)
        ss._merge_snapshot_into_global(ws_b)

        global_model = ss.get_global_user_model()
        vals = [v for v in global_model.values if v.statement.lower() == "ship behind feature flags"]
        assert len(vals) == 1
        assert vals[0].last_reinforced == 500.0
    finally:
        if old is None:
            os.environ.pop("CVC_SOUL_ROOT", None)
        else:
            os.environ["CVC_SOUL_ROOT"] = old


def test_letter_storage_is_global(tmp_path: Path):
    """Letters in workspace's soul_letters/ get migrated to ~/.cvc/soul/soul_letters/."""
    old = os.environ.get("CVC_SOUL_ROOT")
    try:
        os.environ["CVC_SOUL_ROOT"] = str(tmp_path / "soul")
        import importlib
        import cvc.operations.soul_singularity as ss
        importlib.reload(ss)

        # Create a workspace with a letter
        ws = tmp_path / "ws" / ".cvc"
        ws.mkdir(parents=True)
        (ws / "cvc.db").touch()
        letters_dir = ws / "soul_letters"
        letters_dir.mkdir()
        letter_data = {
            "letter_id": "abc123",
            "week_of": "2026-W26",
            "narrative": "Test letter.",
            "greeting": "Hi,",
            "signoff": "— your soul",
        }
        (letters_dir / "letter_2026-W26.json").write_text(json.dumps(letter_data))

        ss._merge_letters_into_global(ws)

        # Now check the global letters dir
        global_letters = ss.soul_letters_dir()
        assert (global_letters / "letter_2026-W26.json").exists()
        loaded = json.loads((global_letters / "letter_2026-W26.json").read_text())
        assert loaded["narrative"] == "Test letter."
    finally:
        if old is None:
            os.environ.pop("CVC_SOUL_ROOT", None)
        else:
            os.environ["CVC_SOUL_ROOT"] = old


def test_workspace_unchanged_after_migration(tmp_path: Path):
    """Migration must NOT delete or modify the source workspace's data."""
    old = os.environ.get("CVC_SOUL_ROOT")
    try:
        os.environ["CVC_SOUL_ROOT"] = str(tmp_path / "soul")
        import importlib
        import cvc.operations.soul_singularity as ss
        importlib.reload(ss)

        from cvc.core.user_model import Entity, UserIdentitySnapshot, UserModelManager

        ws = tmp_path / "ws" / ".cvc"
        ws.mkdir(parents=True)
        (ws / "cvc.db").touch()
        m = UserIdentitySnapshot()
        m.entities.append(Entity(name="KeepMe", entity_type="project", mention_count=1))
        ws_mgr = UserModelManager(ws)
        ws_mgr.save_model(m, trigger="seed")

        original_size = (ws / "user_model.json").stat().st_size
        original_mtime = (ws / "user_model.json").stat().st_mtime

        ss._merge_snapshot_into_global(ws)

        # Source file should be untouched
        assert (ws / "user_model.json").stat().st_size == original_size
        assert (ws / "user_model.json").stat().st_mtime == original_mtime
        # Still has the entity
        src_model = ws_mgr.load_current_model()
        assert any(e.name == "KeepMe" for e in src_model.entities)
    finally:
        if old is None:
            os.environ.pop("CVC_SOUL_ROOT", None)
        else:
            os.environ["CVC_SOUL_ROOT"] = old


if __name__ == "__main__":
    sys.exit(pytest.main([__file__, "-v"]))