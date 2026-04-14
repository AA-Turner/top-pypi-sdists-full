"""Integration test for pack-installed skill provenance (#1397).

Exercises the full DB path: pack install → artifact registry → skill load
with update_guidance reflecting the pack source.
"""

from __future__ import annotations

import tempfile
from pathlib import Path
from typing import Any

import pytest

from anteroom.db import init_db
from anteroom.services.artifact_storage import get_pack_for_artifact, upsert_artifact
from anteroom.services.artifacts import ArtifactSource, ArtifactType


@pytest.fixture()
def db():
    with tempfile.TemporaryDirectory() as td:
        conn = init_db(Path(td) / "test.db")
        yield conn
        conn.close()


def _install_pack_with_skill(db: Any, *, source_path: str = "") -> str:
    """Create a pack with one skill artifact, return the artifact_id."""
    import uuid

    pack_id = str(uuid.uuid4())

    # Insert pack row
    import time as _time

    now = _time.strftime("%Y-%m-%dT%H:%M:%SZ")
    db.execute(
        "INSERT INTO packs (id, name, namespace, version, source_path, installed_at, updated_at)"
        " VALUES (?, ?, ?, ?, ?, ?, ?)",
        (pack_id, "test-pack", "testns", "1.0.0", source_path, now, now),
    )
    db.commit()

    # Insert artifact row
    upsert_artifact(
        db,
        fqn="@testns/skill/deploy",
        artifact_type=ArtifactType.SKILL,
        namespace="testns",
        name="deploy",
        content="---\nname: deploy\ndescription: Deploy skill\n---\nDeploy the app.\n",
        source=ArtifactSource.PROJECT,
        metadata={},
    )

    # Get the artifact's DB id
    row = db.execute_fetchone(
        "SELECT id FROM artifacts WHERE fqn = ?",
        ("@testns/skill/deploy",),
    )
    assert row is not None
    real_artifact_id = row["id"] if hasattr(row, "keys") else row[0]

    # Link artifact to pack
    db.execute(
        "INSERT INTO pack_artifacts (pack_id, artifact_id) VALUES (?, ?)",
        (pack_id, real_artifact_id),
    )
    # Attach pack globally so load_from_db sees it
    att_id = str(uuid.uuid4())
    db.execute(
        "INSERT INTO pack_attachments (id, pack_id, scope, priority, created_at) VALUES (?, ?, ?, ?, ?)",
        (att_id, pack_id, "global", 50, now),
    )
    db.commit()

    return real_artifact_id


class TestPackSkillProvenance:
    def test_get_pack_for_artifact_returns_pack_info(self, db: Any) -> None:
        """get_pack_for_artifact returns pack name and source_path."""
        artifact_id = _install_pack_with_skill(db, source_path="/home/user/packs/test-pack")
        result = get_pack_for_artifact(db, artifact_id)
        assert result is not None
        assert result["pack_name"] == "test-pack"
        assert result["namespace"] == "testns"
        assert result["source_path"] == "/home/user/packs/test-pack"

    def test_get_pack_for_artifact_no_source_path(self, db: Any) -> None:
        """Pack without source_path returns empty string."""
        artifact_id = _install_pack_with_skill(db, source_path="")
        result = get_pack_for_artifact(db, artifact_id)
        assert result is not None
        assert result["source_path"] == ""

    def test_get_pack_for_artifact_standalone(self, db: Any) -> None:
        """Standalone artifact (no pack link) returns None."""
        result = get_pack_for_artifact(db, "nonexistent-id")
        assert result is None

    def test_artifact_registry_preserves_artifact_id(self, db: Any) -> None:
        """Artifact loaded via registry carries its DB id."""
        _install_pack_with_skill(db)
        from anteroom.services.artifact_registry import ArtifactRegistry

        registry = ArtifactRegistry()
        registry.load_from_db(db)
        skills = registry.list_all(artifact_type="skill")
        assert len(skills) >= 1
        deploy = [s for s in skills if s.name == "deploy"]
        assert len(deploy) == 1
        assert deploy[0].artifact_id != "", "artifact_id should be populated from DB row"

    def test_skill_load_from_artifacts_with_pack_guidance(self, db: Any) -> None:
        """Full flow: pack skill loaded via artifacts gets update_guidance with pack name."""
        _install_pack_with_skill(db, source_path="/packs/test-pack")
        from anteroom.cli.skills import SkillRegistry
        from anteroom.services.artifact_registry import ArtifactRegistry

        registry = ArtifactRegistry()
        registry.load_from_db(db)
        skill_reg = SkillRegistry()
        skill_reg.load_from_artifacts(registry, db=db)

        skill = skill_reg.get("testns/deploy")
        assert skill is not None
        assert "testns" in skill.update_guidance
        assert "/packs/test-pack" in skill.update_guidance
