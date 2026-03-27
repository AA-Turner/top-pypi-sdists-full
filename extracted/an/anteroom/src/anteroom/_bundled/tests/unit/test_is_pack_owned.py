"""Tests for is_pack_owned and is_artifact_attached helpers (#1010)."""

from __future__ import annotations

import uuid
from pathlib import Path
from typing import Any

import pytest

from anteroom.services.artifact_storage import (
    create_artifact,
    is_artifact_attached,
    is_pack_owned,
)
from anteroom.services.artifacts import ArtifactSource, ArtifactType


@pytest.fixture()
def db(tmp_path: Path) -> Any:
    from anteroom.db import init_db

    return init_db(tmp_path / "test.db")


def _create_test_artifact(db: Any, fqn: str = "@testns/skill/greet") -> dict[str, Any]:
    return create_artifact(
        db,
        fqn=fqn,
        artifact_type=ArtifactType.SKILL,
        namespace="testns",
        name="greet",
        content="Hello!",
        source=ArtifactSource.PROJECT,
    )


def _create_pack_with_artifact(db: Any, artifact_id: str) -> str:
    """Create a pack row and link an artifact to it. Returns pack_id."""
    from datetime import datetime, timezone

    pack_id = uuid.uuid4().hex
    now = datetime.now(timezone.utc).isoformat()
    db.execute(
        "INSERT INTO packs (id, name, namespace, version, description, source_path, installed_at, updated_at)"
        " VALUES (?, ?, ?, ?, ?, ?, ?, ?)",
        (pack_id, "test-pack", "testns", "1.0.0", "", "/tmp/pack", now, now),
    )
    db.execute(
        "INSERT INTO pack_artifacts (pack_id, artifact_id) VALUES (?, ?)",
        (pack_id, artifact_id),
    )
    db.commit()
    return pack_id


def _ensure_space(db: Any, space_id: str) -> None:
    """Create a space row if it doesn't exist."""
    from datetime import datetime, timezone

    now = datetime.now(timezone.utc).isoformat()
    existing = db.execute("SELECT 1 FROM spaces WHERE id = ?", (space_id,)).fetchone()
    if not existing:
        db.execute(
            "INSERT INTO spaces (id, name, instructions, source_file, source_hash, created_at, updated_at)"
            " VALUES (?, ?, '', '', '', ?, ?)",
            (space_id, space_id, now, now),
        )
        db.commit()


def _attach_pack(
    db: Any, pack_id: str, scope: str = "global", project_path: str | None = None, space_id: str | None = None
) -> None:
    from datetime import datetime, timezone

    if space_id:
        _ensure_space(db, space_id)

    att_id = uuid.uuid4().hex
    now = datetime.now(timezone.utc).isoformat()
    db.execute(
        "INSERT INTO pack_attachments (id, pack_id, project_path, space_id, scope, priority, created_at)"
        " VALUES (?, ?, ?, ?, ?, ?, ?)",
        (att_id, pack_id, project_path, space_id, scope, 50, now),
    )
    db.commit()


class TestIsPackOwned:
    def test_true_when_pack_linked(self, db: Any) -> None:
        art = _create_test_artifact(db)
        _create_pack_with_artifact(db, art["id"])
        assert is_pack_owned(db, art["id"]) is True

    def test_false_when_no_pack(self, db: Any) -> None:
        art = _create_test_artifact(db)
        assert is_pack_owned(db, art["id"]) is False

    def test_false_for_nonexistent_artifact(self, db: Any) -> None:
        assert is_pack_owned(db, "nonexistent-id") is False


class TestIsArtifactAttached:
    def test_standalone_always_attached(self, db: Any) -> None:
        art = _create_test_artifact(db)
        assert is_artifact_attached(db, art["id"]) is True

    def test_pack_with_global_attachment(self, db: Any) -> None:
        art = _create_test_artifact(db)
        pack_id = _create_pack_with_artifact(db, art["id"])
        _attach_pack(db, pack_id, scope="global")
        assert is_artifact_attached(db, art["id"]) is True

    def test_pack_without_attachment_detached(self, db: Any) -> None:
        art = _create_test_artifact(db)
        _create_pack_with_artifact(db, art["id"])
        # No attachment — should be detached
        assert is_artifact_attached(db, art["id"]) is False

    def test_pack_with_space_attachment_matches(self, db: Any) -> None:
        art = _create_test_artifact(db)
        pack_id = _create_pack_with_artifact(db, art["id"])
        _attach_pack(db, pack_id, scope="space", space_id="space-1")
        assert is_artifact_attached(db, art["id"], space_id="space-1") is True

    def test_pack_with_space_attachment_no_match(self, db: Any) -> None:
        art = _create_test_artifact(db)
        pack_id = _create_pack_with_artifact(db, art["id"])
        _attach_pack(db, pack_id, scope="space", space_id="space-1")
        assert is_artifact_attached(db, art["id"], space_id="space-2") is False

    def test_pack_with_project_attachment_matches(self, db: Any, tmp_path: Path) -> None:
        from anteroom.services.pack_attachments import _normalize_project_path

        proj = _normalize_project_path(str(tmp_path / "project"))
        art = _create_test_artifact(db)
        pack_id = _create_pack_with_artifact(db, art["id"])
        _attach_pack(db, pack_id, scope="project", project_path=proj)
        assert is_artifact_attached(db, art["id"], project_path=str(tmp_path / "project")) is True

    def test_pack_with_project_attachment_ancestor_matches(self, db: Any, tmp_path: Path) -> None:
        from anteroom.services.pack_attachments import _normalize_project_path

        proj = _normalize_project_path(str(tmp_path / "project"))
        art = _create_test_artifact(db)
        pack_id = _create_pack_with_artifact(db, art["id"])
        _attach_pack(db, pack_id, scope="project", project_path=proj)
        assert is_artifact_attached(db, art["id"], project_path=str(tmp_path / "project" / "subdir")) is True

    def test_pack_with_project_attachment_no_match(self, db: Any, tmp_path: Path) -> None:
        from anteroom.services.pack_attachments import _normalize_project_path

        proj = _normalize_project_path(str(tmp_path / "project"))
        art = _create_test_artifact(db)
        pack_id = _create_pack_with_artifact(db, art["id"])
        _attach_pack(db, pack_id, scope="project", project_path=proj)
        assert is_artifact_attached(db, art["id"], project_path=str(tmp_path / "other")) is False
