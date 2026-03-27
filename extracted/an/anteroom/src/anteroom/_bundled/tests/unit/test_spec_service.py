"""Unit tests for spec_service — CRUD, phase approval, traceability."""

from __future__ import annotations

import sqlite3
from pathlib import Path
from typing import Any

import pytest

from anteroom.services.spec_schema import SpecPhaseStatus, SpecValidationError

# We import the full schema so init_db creates all tables including workflow_runs
_SCHEMA: str = ""

VALID_SPEC_YAML = """\
requirements: |
  Must support widgets.
design: |
  Use the widget parser pattern.
tasks:
  - id: t1
    summary: Implement widget parser
  - id: t2
    summary: Add validation layer
    depends_on: [t1]
"""

UPDATED_SPEC_YAML = """\
requirements: |
  Must support widgets and gadgets.
design: |
  Use the widget parser pattern with gadget extension.
tasks:
  - id: t1
    summary: Implement widget parser
  - id: t2
    summary: Add validation layer
    depends_on: [t1]
  - id: t3
    summary: Add gadget support
    depends_on: [t1]
"""

INVALID_SPEC_YAML = """\
requirements: |
  Valid requirements.
design: |
  Valid design.
tasks: not-a-list
"""


@pytest.fixture()
def db(tmp_path: Path) -> Any:
    """Create a real DB via init_db for spec service tests."""
    from anteroom.db import init_db

    return init_db(tmp_path / "test.db")


# ---------------------------------------------------------------------------
# create_spec
# ---------------------------------------------------------------------------


class TestCreateSpec:
    def test_create_valid_spec(self, db: Any) -> None:
        from anteroom.services.spec_service import create_spec

        art = create_spec(db, "myns", "feature-x", VALID_SPEC_YAML)
        assert art["type"] == "spec"
        assert art["namespace"] == "myns"
        assert art["name"] == "feature-x"
        assert art["fqn"] == "@myns/spec/feature-x"
        assert art["metadata"]["phases"]["requirements"]["status"] == "draft"
        assert art["metadata"]["phases"]["design"]["status"] == "draft"
        assert art["metadata"]["phases"]["tasks"]["status"] == "draft"

    def test_create_invalid_yaml(self, db: Any) -> None:
        from anteroom.services.spec_service import create_spec

        with pytest.raises(SpecValidationError, match="tasks.*list"):
            create_spec(db, "ns", "bad", INVALID_SPEC_YAML)

    def test_create_duplicate_fqn(self, db: Any) -> None:
        from anteroom.services.spec_service import create_spec

        create_spec(db, "ns", "x", VALID_SPEC_YAML)
        with pytest.raises(sqlite3.IntegrityError):
            create_spec(db, "ns", "x", VALID_SPEC_YAML)


# ---------------------------------------------------------------------------
# get_spec
# ---------------------------------------------------------------------------


class TestGetSpec:
    def test_get_existing(self, db: Any) -> None:
        from anteroom.services.spec_service import create_spec, get_spec

        create_spec(db, "ns", "feat", VALID_SPEC_YAML)
        result = get_spec(db, "@ns/spec/feat")
        assert result is not None
        art, content = result
        assert art["fqn"] == "@ns/spec/feat"
        assert content.requirements.strip() == "Must support widgets."
        assert len(content.tasks) == 2

    def test_get_nonexistent(self, db: Any) -> None:
        from anteroom.services.spec_service import get_spec

        assert get_spec(db, "@ns/spec/nope") is None

    def test_get_non_spec_type(self, db: Any) -> None:
        from anteroom.services import artifact_storage
        from anteroom.services.spec_service import get_spec

        artifact_storage.create_artifact(db, "@ns/skill/x", "skill", "ns", "x", "content")
        with pytest.raises(SpecValidationError, match="not 'spec'"):
            get_spec(db, "@ns/skill/x")


# ---------------------------------------------------------------------------
# update_spec_content
# ---------------------------------------------------------------------------


class TestUpdateSpecContent:
    def test_update_creates_new_version(self, db: Any) -> None:
        from anteroom.services import artifact_storage
        from anteroom.services.spec_service import create_spec, update_spec_content

        art = create_spec(db, "ns", "feat", VALID_SPEC_YAML)
        updated = update_spec_content(db, "@ns/spec/feat", UPDATED_SPEC_YAML)
        assert updated is not None
        versions = artifact_storage.list_artifact_versions(db, art["id"])
        assert len(versions) == 2
        assert versions[0]["version"] == 2

    def test_update_same_content_no_new_version(self, db: Any) -> None:
        from anteroom.services import artifact_storage
        from anteroom.services.spec_service import create_spec, update_spec_content

        art = create_spec(db, "ns", "feat", VALID_SPEC_YAML)
        update_spec_content(db, "@ns/spec/feat", VALID_SPEC_YAML)
        versions = artifact_storage.list_artifact_versions(db, art["id"])
        assert len(versions) == 1

    def test_update_invalid_yaml(self, db: Any) -> None:
        from anteroom.services.spec_service import create_spec, update_spec_content

        create_spec(db, "ns", "feat", VALID_SPEC_YAML)
        with pytest.raises(SpecValidationError):
            update_spec_content(db, "@ns/spec/feat", INVALID_SPEC_YAML)

    def test_update_nonexistent(self, db: Any) -> None:
        from anteroom.services.spec_service import update_spec_content

        assert update_spec_content(db, "@ns/spec/nope", VALID_SPEC_YAML) is None

    def test_update_does_not_touch_metadata(self, db: Any) -> None:
        from anteroom.services.spec_service import approve_phase, create_spec, update_spec_content

        create_spec(db, "ns", "feat", VALID_SPEC_YAML)
        approve_phase(db, "@ns/spec/feat", "requirements", "troy")
        updated = update_spec_content(db, "@ns/spec/feat", UPDATED_SPEC_YAML)
        assert updated is not None
        assert updated["metadata"]["phases"]["requirements"]["status"] == "approved"


# ---------------------------------------------------------------------------
# approve_phase / unapprove_phase
# ---------------------------------------------------------------------------


class TestPhaseApproval:
    def test_approve_sets_status(self, db: Any) -> None:
        from anteroom.services.spec_service import approve_phase, create_spec

        create_spec(db, "ns", "feat", VALID_SPEC_YAML)
        art = approve_phase(db, "@ns/spec/feat", "design", "troy")
        assert art is not None
        assert art["metadata"]["phases"]["design"]["status"] == "approved"
        assert art["metadata"]["phases"]["design"]["approved_by"] == "troy"
        assert art["metadata"]["phases"]["design"]["approved_at"] is not None

    def test_approve_does_not_create_version(self, db: Any) -> None:
        from anteroom.services import artifact_storage
        from anteroom.services.spec_service import approve_phase, create_spec

        art = create_spec(db, "ns", "feat", VALID_SPEC_YAML)
        approve_phase(db, "@ns/spec/feat", "design", "troy")
        versions = artifact_storage.list_artifact_versions(db, art["id"])
        assert len(versions) == 1

    def test_approve_nonexistent(self, db: Any) -> None:
        from anteroom.services.spec_service import approve_phase

        assert approve_phase(db, "@ns/spec/nope", "design") is None

    def test_approve_invalid_phase(self, db: Any) -> None:
        from anteroom.services.spec_service import approve_phase, create_spec

        create_spec(db, "ns", "feat", VALID_SPEC_YAML)
        with pytest.raises(ValueError, match="Invalid phase name"):
            approve_phase(db, "@ns/spec/feat", "invalid_phase")

    def test_unapprove_resets_to_draft(self, db: Any) -> None:
        from anteroom.services.spec_service import approve_phase, create_spec, unapprove_phase

        create_spec(db, "ns", "feat", VALID_SPEC_YAML)
        approve_phase(db, "@ns/spec/feat", "design", "troy")
        art = unapprove_phase(db, "@ns/spec/feat", "design")
        assert art is not None
        assert art["metadata"]["phases"]["design"]["status"] == "draft"
        assert art["metadata"]["phases"]["design"]["approved_at"] is None

    def test_unapprove_nonexistent(self, db: Any) -> None:
        from anteroom.services.spec_service import unapprove_phase

        assert unapprove_phase(db, "@ns/spec/nope", "design") is None

    def test_approve_already_approved(self, db: Any) -> None:
        from anteroom.services.spec_service import approve_phase, create_spec

        create_spec(db, "ns", "feat", VALID_SPEC_YAML)
        approve_phase(db, "@ns/spec/feat", "design", "user1")
        art = approve_phase(db, "@ns/spec/feat", "design", "user2")
        assert art is not None
        assert art["metadata"]["phases"]["design"]["approved_by"] == "user2"


# ---------------------------------------------------------------------------
# get_phase_statuses
# ---------------------------------------------------------------------------


class TestGetPhaseStatuses:
    def test_all_draft(self, db: Any) -> None:
        from anteroom.services.spec_service import create_spec, get_phase_statuses

        create_spec(db, "ns", "feat", VALID_SPEC_YAML)
        statuses = get_phase_statuses(db, "@ns/spec/feat")
        assert statuses is not None
        assert all(s == SpecPhaseStatus.DRAFT for s in statuses.values())

    def test_mixed_statuses(self, db: Any) -> None:
        from anteroom.services.spec_service import approve_phase, create_spec, get_phase_statuses

        create_spec(db, "ns", "feat", VALID_SPEC_YAML)
        approve_phase(db, "@ns/spec/feat", "requirements", "troy")
        statuses = get_phase_statuses(db, "@ns/spec/feat")
        assert statuses is not None
        assert statuses["requirements"] == SpecPhaseStatus.APPROVED
        assert statuses["design"] == SpecPhaseStatus.DRAFT

    def test_nonexistent(self, db: Any) -> None:
        from anteroom.services.spec_service import get_phase_statuses

        assert get_phase_statuses(db, "@ns/spec/nope") is None


# ---------------------------------------------------------------------------
# get_traceability
# ---------------------------------------------------------------------------


class TestGetTraceability:
    def test_no_runs(self, db: Any) -> None:
        from anteroom.services.spec_service import create_spec, get_traceability

        create_spec(db, "ns", "feat", VALID_SPEC_YAML)
        trace = get_traceability(db, "@ns/spec/feat")
        assert trace is not None
        assert trace == {"t1": [], "t2": []}

    def test_with_linked_runs(self, db: Any) -> None:
        from anteroom.services.spec_service import create_spec, get_traceability
        from anteroom.services.workflow_storage import create_workflow_run

        create_spec(db, "ns", "feat", VALID_SPEC_YAML)
        create_workflow_run(
            db,
            workflow_id="wf1",
            workflow_version="1.0",
            target_kind="spec",
            target_ref="@ns/spec/feat",
            inputs={"spec_fqn": "@ns/spec/feat", "task_id": "t1"},
        )
        trace = get_traceability(db, "@ns/spec/feat")
        assert trace is not None
        assert len(trace["t1"]) == 1
        assert trace["t1"][0]["spec_fqn"] == "@ns/spec/feat"
        assert trace["t1"][0]["task_id"] == "t1"
        assert trace["t2"] == []

    def test_nonexistent_spec(self, db: Any) -> None:
        from anteroom.services.spec_service import get_traceability

        assert get_traceability(db, "@ns/spec/nope") is None

    def test_runs_without_task_id(self, db: Any) -> None:
        from anteroom.services.spec_service import create_spec, get_traceability
        from anteroom.services.workflow_storage import create_workflow_run

        create_spec(db, "ns", "feat", VALID_SPEC_YAML)
        create_workflow_run(
            db,
            workflow_id="wf1",
            workflow_version="1.0",
            target_kind="spec",
            target_ref="@ns/spec/feat",
            inputs={"spec_fqn": "@ns/spec/feat"},
        )
        trace = get_traceability(db, "@ns/spec/feat")
        assert trace is not None
        assert trace["t1"] == []
        assert trace["t2"] == []

    def test_multiple_runs_for_same_task(self, db: Any) -> None:
        from anteroom.services.spec_service import create_spec, get_traceability
        from anteroom.services.workflow_storage import create_workflow_run

        create_spec(db, "ns", "feat", VALID_SPEC_YAML)
        for _ in range(3):
            create_workflow_run(
                db,
                workflow_id="wf1",
                workflow_version="1.0",
                target_kind="spec",
                target_ref="@ns/spec/feat",
                inputs={"spec_fqn": "@ns/spec/feat", "task_id": "t1"},
            )
        trace = get_traceability(db, "@ns/spec/feat")
        assert trace is not None
        assert len(trace["t1"]) == 3


# ---------------------------------------------------------------------------
# DB migration
# ---------------------------------------------------------------------------


class TestDbMigration:
    def test_spec_type_accepted_on_fresh_db(self, db: Any) -> None:
        from anteroom.services.spec_service import create_spec

        art = create_spec(db, "ns", "feat", VALID_SPEC_YAML)
        assert art["type"] == "spec"

    def test_migration_adds_spec_type(self, tmp_path: Path) -> None:
        """Simulate an old DB without 'spec' in CHECK, then migrate."""
        db_path = tmp_path / "old.db"
        conn = sqlite3.connect(str(db_path))
        conn.execute(
            """CREATE TABLE artifacts (
                id TEXT PRIMARY KEY,
                fqn TEXT UNIQUE NOT NULL,
                type TEXT NOT NULL CHECK(type IN (
                    'skill','rule','instruction','context','memory','mcp_server','config_overlay')),
                namespace TEXT NOT NULL,
                name TEXT NOT NULL,
                content TEXT NOT NULL,
                content_hash TEXT NOT NULL,
                source TEXT NOT NULL,
                metadata TEXT NOT NULL DEFAULT '{}',
                user_id TEXT DEFAULT NULL,
                user_display_name TEXT DEFAULT NULL,
                created_at TEXT NOT NULL,
                updated_at TEXT NOT NULL
            )"""
        )
        conn.execute(
            "INSERT INTO artifacts VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)",
            (
                "id1",
                "@ns/skill/x",
                "skill",
                "ns",
                "x",
                "content",
                "hash",
                "local",
                "{}",
                None,
                None,
                "2026-01-01",
                "2026-01-01",
            ),
        )
        conn.commit()
        conn.close()

        from anteroom.db import init_db

        db = init_db(db_path)

        # Old data should still be there
        from anteroom.services import artifact_storage

        existing = artifact_storage.get_artifact_by_fqn(db, "@ns/skill/x")
        assert existing is not None

        # Should now accept spec type
        from anteroom.services.spec_service import create_spec

        art = create_spec(db, "ns", "feat", VALID_SPEC_YAML)
        assert art["type"] == "spec"


# ---------------------------------------------------------------------------
# Local discovery exclusion
# ---------------------------------------------------------------------------


class TestSpecNotDiscoveredFromFilesystem:
    def test_spec_files_ignored_by_discover(self, tmp_path: Path) -> None:
        """Spec artifacts must NOT be auto-discovered from the filesystem."""
        from anteroom.services.local_artifacts import discover_local_artifacts

        local_dir = tmp_path / "local"
        spec_dir = local_dir / "spec"
        spec_dir.mkdir(parents=True)
        (spec_dir / "my-spec.yaml").write_text("requirements: r\ndesign: d\ntasks:\n  - id: t1\n    summary: s\n")
        # Also add a skill to prove other types still work
        skill_dir = local_dir / "skills"
        skill_dir.mkdir()
        (skill_dir / "my-skill.yaml").write_text("name: test\nprompt: hello\n")

        artifacts = discover_local_artifacts(local_dir)
        types_found = {a["type"] for a in artifacts}
        assert "spec" not in types_found
        assert "skill" in types_found
