"""Tests for spec visibility with attachment awareness (#1010)."""

from __future__ import annotations

import uuid
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

import pytest

from anteroom.services.artifact_storage import list_artifacts
from anteroom.services.artifacts import ArtifactType

VALID_SPEC_YAML = """\
requirements: |
  Must support widgets.
design: |
  Use the widget parser pattern.
tasks:
  - id: t1
    summary: Implement widget parser
"""


@pytest.fixture()
def db(tmp_path: Path) -> Any:
    from anteroom.db import init_db

    return init_db(tmp_path / "test.db")


def _create_spec(db: Any, name: str = "my-spec", namespace: str = "testns") -> dict[str, Any]:
    from anteroom.services.spec_service import create_spec

    return create_spec(db, namespace, name, VALID_SPEC_YAML)


def _make_pack_with_artifact(db: Any, artifact_id: str, pack_name: str = "test-pack") -> str:
    pack_id = uuid.uuid4().hex
    now = datetime.now(timezone.utc).isoformat()
    db.execute(
        "INSERT INTO packs (id, name, namespace, version, description, source_path, installed_at, updated_at)"
        " VALUES (?, ?, ?, ?, ?, ?, ?, ?)",
        (pack_id, pack_name, "testns", "1.0.0", "", "/tmp/pack", now, now),
    )
    db.execute(
        "INSERT INTO pack_artifacts (pack_id, artifact_id) VALUES (?, ?)",
        (pack_id, artifact_id),
    )
    db.commit()
    return pack_id


def _attach_pack(db: Any, pack_id: str, scope: str = "global", **kwargs: Any) -> None:
    att_id = uuid.uuid4().hex
    now = datetime.now(timezone.utc).isoformat()
    project_path = kwargs.get("project_path")
    if project_path is not None:
        from anteroom.services.pack_attachments import _normalize_project_path

        project_path = _normalize_project_path(project_path)
    db.execute(
        "INSERT INTO pack_attachments (id, pack_id, project_path, space_id, scope, priority, created_at)"
        " VALUES (?, ?, ?, ?, ?, ?, ?)",
        (att_id, pack_id, project_path, kwargs.get("space_id"), scope, 50, now),
    )
    db.commit()


class TestSpecListAttachedOnly:
    def test_standalone_spec_visible(self, db: Any) -> None:
        _create_spec(db)
        results = list_artifacts(db, artifact_type=ArtifactType.SPEC, attached_only=True)
        assert len(results) == 1

    def test_attached_pack_spec_visible(self, db: Any) -> None:
        art = _create_spec(db)
        pack_id = _make_pack_with_artifact(db, art["id"])
        _attach_pack(db, pack_id)
        results = list_artifacts(db, artifact_type=ArtifactType.SPEC, attached_only=True)
        assert len(results) == 1

    def test_detached_pack_spec_hidden(self, db: Any) -> None:
        art = _create_spec(db)
        _make_pack_with_artifact(db, art["id"])
        # No attachment
        results = list_artifacts(db, artifact_type=ArtifactType.SPEC, attached_only=True)
        assert len(results) == 0

    def test_project_scoped_attached_pack_visible_with_matching_path(self, db: Any) -> None:
        art = _create_spec(db)
        pack_id = _make_pack_with_artifact(db, art["id"])
        _attach_pack(db, pack_id, scope="project", project_path="/home/user/myproject")
        results = list_artifacts(
            db,
            artifact_type=ArtifactType.SPEC,
            attached_only=True,
            project_path="/home/user/myproject",
        )
        assert len(results) == 1

    def test_project_scoped_attached_pack_hidden_without_path(self, db: Any) -> None:
        art = _create_spec(db)
        pack_id = _make_pack_with_artifact(db, art["id"])
        _attach_pack(db, pack_id, scope="project", project_path="/home/user/myproject")
        # No project_path passed — project-scoped attachment not matched
        results = list_artifacts(
            db,
            artifact_type=ArtifactType.SPEC,
            attached_only=True,
        )
        assert len(results) == 0

    def test_project_scoped_attached_pack_hidden_with_wrong_path(self, db: Any) -> None:
        art = _create_spec(db)
        pack_id = _make_pack_with_artifact(db, art["id"])
        _attach_pack(db, pack_id, scope="project", project_path="/home/user/myproject")
        results = list_artifacts(
            db,
            artifact_type=ArtifactType.SPEC,
            attached_only=True,
            project_path="/home/user/other-project",
        )
        assert len(results) == 0


class TestSpecGateAttachment:
    @pytest.mark.asyncio
    async def test_gate_passes_for_attached(self, db: Any) -> None:
        art = _create_spec(db)
        pack_id = _make_pack_with_artifact(db, art["id"])
        _attach_pack(db, pack_id)

        # Approve the phase
        from anteroom.services.spec_service import approve_phase

        approve_phase(db, art["fqn"], "requirements")

        from anteroom.services.spec_gates import _make_phase_gate

        gate_fn = _make_phase_gate(db, "requirements")
        result = await gate_fn({}, None, {"spec_fqn": art["fqn"]})
        assert result.passed is True

    @pytest.mark.asyncio
    async def test_gate_fails_for_detached(self, db: Any) -> None:
        art = _create_spec(db)
        _make_pack_with_artifact(db, art["id"])
        # No attachment

        from anteroom.services.spec_gates import _make_phase_gate

        gate_fn = _make_phase_gate(db, "requirements")
        result = await gate_fn({}, None, {"spec_fqn": art["fqn"]})
        assert result.passed is False
        assert "detached pack" in result.reason

    @pytest.mark.asyncio
    async def test_gate_evaluates_normally_for_standalone(self, db: Any) -> None:
        art = _create_spec(db)
        # Standalone, not pack-owned

        from anteroom.services.spec_gates import _make_phase_gate

        gate_fn = _make_phase_gate(db, "requirements")
        result = await gate_fn({}, None, {"spec_fqn": art["fqn"]})
        # Should fail because not approved, but NOT because of detached pack
        assert result.passed is False
        assert "draft" in result.reason

    @pytest.mark.asyncio
    async def test_gate_passes_for_project_scoped_with_matching_context(self, db: Any) -> None:
        art = _create_spec(db)
        pack_id = _make_pack_with_artifact(db, art["id"])
        _attach_pack(db, pack_id, scope="project", project_path="/home/user/myproject")

        from anteroom.services.spec_service import approve_phase

        approve_phase(db, art["fqn"], "requirements")

        from anteroom.services.spec_gates import _make_phase_gate

        gate_fn = _make_phase_gate(db, "requirements")
        # Pass project_path in inputs to simulate context from the workflow run
        result = await gate_fn({}, None, {"spec_fqn": art["fqn"], "project_path": "/home/user/myproject"})
        assert result.passed is True

    @pytest.mark.asyncio
    async def test_gate_fails_for_project_scoped_without_context(self, db: Any) -> None:
        art = _create_spec(db)
        pack_id = _make_pack_with_artifact(db, art["id"])
        _attach_pack(db, pack_id, scope="project", project_path="/home/user/myproject")

        from anteroom.services.spec_gates import _make_phase_gate

        gate_fn = _make_phase_gate(db, "requirements")
        # No project context — project-scoped attachment won't match
        result = await gate_fn({}, None, {"spec_fqn": art["fqn"]})
        assert result.passed is False
        assert "detached pack" in result.reason

    @pytest.mark.asyncio
    async def test_gate_passes_for_space_scoped_via_inputs(self, db: Any) -> None:
        """Gate reads space_id from inputs when run record has no space_id."""
        art = _create_spec(db)
        pack_id = _make_pack_with_artifact(db, art["id"])
        space_id = uuid.uuid4().hex
        now = datetime.now(timezone.utc).isoformat()
        db.execute(
            "INSERT INTO spaces (id, name, created_at, updated_at) VALUES (?, ?, ?, ?)",
            (space_id, "test-space", now, now),
        )
        db.commit()
        _attach_pack(db, pack_id, scope="space", space_id=space_id)

        from anteroom.services.spec_service import approve_phase

        approve_phase(db, art["fqn"], "requirements")

        from anteroom.services.spec_gates import _make_phase_gate

        gate_fn = _make_phase_gate(db, "requirements")
        # run has no space_id, but inputs do — gate should fall back to inputs
        result = await gate_fn({}, None, {"spec_fqn": art["fqn"], "space_id": space_id})
        assert result.passed is True

    @pytest.mark.asyncio
    async def test_gate_fails_for_space_scoped_without_context(self, db: Any) -> None:
        """Gate fails when space-scoped attachment has no matching context."""
        art = _create_spec(db)
        pack_id = _make_pack_with_artifact(db, art["id"])
        space_id = uuid.uuid4().hex
        now = datetime.now(timezone.utc).isoformat()
        db.execute(
            "INSERT INTO spaces (id, name, created_at, updated_at) VALUES (?, ?, ?, ?)",
            (space_id, "test-space-2", now, now),
        )
        db.commit()
        _attach_pack(db, pack_id, scope="space", space_id=space_id)

        from anteroom.services.spec_gates import _make_phase_gate

        gate_fn = _make_phase_gate(db, "requirements")
        # No space context at all
        result = await gate_fn({}, None, {"spec_fqn": art["fqn"]})
        assert result.passed is False
        assert "detached pack" in result.reason

    @pytest.mark.asyncio
    async def test_gate_fails_for_project_scoped_with_wrong_context(self, db: Any) -> None:
        art = _create_spec(db)
        pack_id = _make_pack_with_artifact(db, art["id"])
        _attach_pack(db, pack_id, scope="project", project_path="/home/user/myproject")

        from anteroom.services.spec_gates import _make_phase_gate

        gate_fn = _make_phase_gate(db, "requirements")
        result = await gate_fn({}, None, {"spec_fqn": art["fqn"], "project_path": "/home/user/other"})
        assert result.passed is False
        assert "detached pack" in result.reason
