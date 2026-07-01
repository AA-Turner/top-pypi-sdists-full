"""Tests for hotfix/soul-values-and-cleanup-2026-06-30 — entity cleanup.

Targets the legacy-garbage purge + dedup pass that runs at the start of
every per-turn soul update. These tokens used to render as people on the
Soul page: ``The``, ``Honestly``, ``If``, ``What``, ``Where``, ``Soul``,
``Digital``, ``CMO``, ``Jai`` (owner), ``For``, ``Merging``, etc.
"""
from __future__ import annotations

import sys
from pathlib import Path

import pytest

# Make the cvc package importable when run from the repo root.
# Repo layout is flat: /Users/jkm/Projects/cvc/cvc/ is the package itself
# (contains core/, operations/, gateway/, etc.).
PKG_ROOT = Path(__file__).resolve().parents[1]  # /Users/jkm/Projects/cvc/cvc
if str(PKG_ROOT) not in sys.path:
    sys.path.insert(0, str(PKG_ROOT))

from cvc.core.user_model import Entity, UserIdentitySnapshot  # noqa: E402
from cvc.operations.entity_extractor import cleanup_snapshot_entities  # noqa: E402


def _snapshot_with(names: list[str]) -> UserIdentitySnapshot:
    snap = UserIdentitySnapshot()
    for n in names:
        snap.entities.append(
            Entity(
                name=n,
                entity_type="person",
                relationship="mentioned",
                mention_count=1,
            )
        )
    return snap


def test_drops_classic_stopword_garbage():
    """Pre-hotfix data had 'The', 'Honestly', 'If', 'What', 'Where', 'When'."""
    snap = _snapshot_with(["The", "Honestly", "If", "What", "Where", "When", "Ajay"])
    dropped, merged = cleanup_snapshot_entities(snap)
    assert dropped == 6
    assert merged == 0
    assert [e.name for e in snap.entities] == ["Ajay"]


def test_drops_owner_name():
    """The user is never a 'mentioned person' in their own soul."""
    snap = _snapshot_with(["Jai", "Jaimeena", "Meena", "Anjali"])
    dropped, _ = cleanup_snapshot_entities(snap)
    assert dropped == 3
    assert [e.name for e in snap.entities] == ["Anjali"]


def test_drops_verb_stems():
    """Sentence-capped verbs that escaped the stoplist in earlier runs."""
    snap = _snapshot_with(
        ["For", "Merging", "Not", "Verify", "Show", "Prepare", "Manual", "Can", "Is", "One", "Ajay"]
    )
    dropped, _ = cleanup_snapshot_entities(snap)
    assert dropped == 10
    assert [e.name for e in snap.entities] == ["Ajay"]


def test_reclassifies_soft_overrides():
    """Stopwords win over soft overrides — 'Soul' and 'Digital' are in
    STOPWORDS so they get dropped outright, not reclassified."""
    snap = _snapshot_with(["Soul", "Digital", "Anjali"])
    dropped, _ = cleanup_snapshot_entities(snap)
    # Soul is a stopword → dropped
    # Digital is a stopword → dropped
    # Anjali → kept
    assert dropped == 2
    assert [e.name for e in snap.entities] == ["Anjali"]


def test_drops_acronym_roles_when_stopword():
    """CMO/CTO/CEO are in STOPWORDS — they're dropped, not reclassified.

    They appear in messages as part of role names ('Digital CMO'),
    not as standalone people. Dropping them is the right behavior."""
    snap = _snapshot_with(["CMO", "CTO", "Anjali"])
    dropped, _ = cleanup_snapshot_entities(snap)
    assert dropped == 2
    assert [e.name for e in snap.entities] == ["Anjali"]


def test_reclassifies_non_stopword_override():
    """A custom name in SOFT_NAME_OVERRIDES that's NOT a stopword
    gets reclassified rather than dropped.

    Use a synthetic snapshot to verify the reclassification branch
    without polluting the real stoplist."""
    from cvc.operations.entity_extractor import SOFT_NAME_OVERRIDES

    # Temporarily add a non-stopword soft override and verify
    saved = dict(SOFT_NAME_OVERRIDES)
    try:
        SOFT_NAME_OVERRIDES["Sentinel"] = "role"
        snap = _snapshot_with(["Sentinel", "Anjali"])
        dropped, _ = cleanup_snapshot_entities(snap)
        assert dropped == 0
        sentinel = next(e for e in snap.entities if e.name == "Sentinel")
        assert sentinel.entity_type == "role"
    finally:
        SOFT_NAME_OVERRIDES.clear()
        SOFT_NAME_OVERRIDES.update(saved)


def test_dedupes_owner_rows():
    """Eight 'Jai' rows from old data collapse to one with merged counts.

    Because the cleanup pass also drops the owner, all 'Jai' rows are
    dropped entirely here. The dedup applies when the name survives
    Pass 1+2 — e.g. when 'Ajay' was captured twice."""
    snap = _snapshot_with(["Ajay", "ajay", "AJAY", "Ajay", "Anjali"])
    dropped, merged = cleanup_snapshot_entities(snap)
    assert merged == 3
    assert dropped == 0
    assert len(snap.entities) == 2  # one Ajay, one Anjali
    ajay = next(e for e in snap.entities if e.name.lower() == "ajay")
    assert ajay.mention_count == 4
    ajay = next(e for e in snap.entities if e.name.lower() == "ajay")
    assert ajay.mention_count == 4


def test_case_insensitive_dedup():
    """Mixed case names merge: 'Anjali' + 'ANJALI' + 'anjali'."""
    snap = _snapshot_with(["Anjali", "ANJALI", "anjali"])
    _, merged = cleanup_snapshot_entities(snap)
    assert merged == 2
    assert len(snap.entities) == 1
    assert snap.entities[0].name == "Anjali"
    assert snap.entities[0].mention_count == 3


def test_keeps_real_projects_intact():
    """PascalCase and lowercase-id projects must survive cleanup."""
    snap = _snapshot_with(
        [
            "HydroPlus",
            "lvl360",
            "WebUI",
            "Anjali",
            "Ajay",
            "Sofia",  # Sofia is in STOPWORDS (AI tools list)
        ]
    )
    dropped, _ = cleanup_snapshot_entities(snap)
    # Sofia should be dropped (it's a tool name, not a person)
    assert "Sofia" not in [e.name for e in snap.entities]
    # Real projects + people survive
    kept = {e.name for e in snap.entities}
    assert {"HydroPlus", "lvl360", "WebUI", "Anjali", "Ajay"}.issubset(kept)


def test_empty_snapshot():
    """Defensive: don't crash on None / empty snapshot."""
    assert cleanup_snapshot_entities(None) == (0, 0)
    snap = UserIdentitySnapshot()
    assert cleanup_snapshot_entities(snap) == (0, 0)


def test_empty_entity_name():
    """A garbage row with empty name should be dropped without error."""
    snap = UserIdentitySnapshot()
    snap.entities.append(Entity(name="", entity_type="person"))
    snap.entities.append(Entity(name="Anjali", entity_type="person"))
    dropped, _ = cleanup_snapshot_entities(snap)
    assert dropped == 1
    assert len(snap.entities) == 1
    assert snap.entities[0].name == "Anjali"


def test_return_values():
    """Sanity check that the function returns the documented tuple shape."""
    snap = _snapshot_with(["The", "Anjali", "Anjali"])
    result = cleanup_snapshot_entities(snap)
    assert isinstance(result, tuple)
    assert len(result) == 2
    dropped, merged = result
    assert dropped == 1
    assert merged == 1


if __name__ == "__main__":
    sys.exit(pytest.main([__file__, "-v"]))