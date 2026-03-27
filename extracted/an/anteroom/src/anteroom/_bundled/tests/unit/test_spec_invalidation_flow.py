"""End-to-end invalidation flow tests — update content → stale marking → re-approval."""

from __future__ import annotations

from pathlib import Path
from typing import Any

import pytest

from anteroom.services.spec_schema import SpecPhaseStatus

SPEC_V1 = """\
requirements: |
  Must support widgets.
design: |
  Use the widget parser pattern.
tasks:
  - id: t1
    summary: Implement widget parser
"""

SPEC_V2_REQ_CHANGED = """\
requirements: |
  Must support widgets AND gadgets.
design: |
  Use the widget parser pattern.
tasks:
  - id: t1
    summary: Implement widget parser
"""

SPEC_V3_DESIGN_CHANGED = """\
requirements: |
  Must support widgets AND gadgets.
design: |
  Use the gadget-first parser pattern.
tasks:
  - id: t1
    summary: Implement widget parser
"""


@pytest.fixture()
def db(tmp_path: Path) -> Any:
    from anteroom.db import init_db

    return init_db(tmp_path / "test.db")


FQN = "@ns/spec/feat"


@pytest.fixture()
def spec(db: Any) -> dict[str, Any]:
    from anteroom.services.spec_service import create_spec

    return create_spec(db, "ns", "feat", SPEC_V1)


# ---------------------------------------------------------------------------
# Single-write invalidation
# ---------------------------------------------------------------------------


class TestSingleWriteInvalidation:
    def test_update_req_stales_approved_design(self, db: Any, spec: dict) -> None:
        from anteroom.services import artifact_storage
        from anteroom.services.spec_service import approve_phase, update_spec_content

        approve_phase(db, FQN, "design", "troy")
        result = update_spec_content(db, FQN, SPEC_V2_REQ_CHANGED)
        assert result is not None
        assert result["metadata"]["phases"]["design"]["status"] == "stale"
        assert result["metadata"]["phases"]["design"]["approved_by"] == "troy"

        # Verify single version created (V1 + V2 = 2 versions)
        versions = artifact_storage.list_artifact_versions(db, spec["id"])
        assert len(versions) == 2

    def test_update_req_stales_approved_tasks(self, db: Any, spec: dict) -> None:
        from anteroom.services.spec_service import approve_phase, update_spec_content

        approve_phase(db, FQN, "tasks", "troy")
        result = update_spec_content(db, FQN, SPEC_V2_REQ_CHANGED)
        assert result is not None
        assert result["metadata"]["phases"]["tasks"]["status"] == "stale"

    def test_update_design_stales_approved_tasks(self, db: Any, spec: dict) -> None:
        from anteroom.services.spec_service import approve_phase, update_spec_content

        # First update requirements so we have a base for design change
        update_spec_content(db, FQN, SPEC_V2_REQ_CHANGED)
        approve_phase(db, FQN, "tasks", "troy")
        result = update_spec_content(db, FQN, SPEC_V3_DESIGN_CHANGED)
        assert result is not None
        assert result["metadata"]["phases"]["tasks"]["status"] == "stale"

    def test_update_no_invalidation_when_draft(self, db: Any, spec: dict) -> None:
        from anteroom.services.spec_service import update_spec_content

        # All phases are draft — no invalidation
        result = update_spec_content(db, FQN, SPEC_V2_REQ_CHANGED)
        assert result is not None
        assert result["metadata"]["phases"]["design"]["status"] == "draft"
        assert result["metadata"]["phases"]["tasks"]["status"] == "draft"

    def test_update_both_staled_when_both_approved(self, db: Any, spec: dict) -> None:
        from anteroom.services.spec_service import approve_phase, update_spec_content

        approve_phase(db, FQN, "design", "troy")
        approve_phase(db, FQN, "tasks", "troy")
        result = update_spec_content(db, FQN, SPEC_V2_REQ_CHANGED)
        assert result is not None
        assert result["metadata"]["phases"]["design"]["status"] == "stale"
        assert result["metadata"]["phases"]["tasks"]["status"] == "stale"

    def test_same_content_no_invalidation(self, db: Any, spec: dict) -> None:
        from anteroom.services import artifact_storage
        from anteroom.services.spec_service import approve_phase, update_spec_content

        approve_phase(db, FQN, "design", "troy")
        result = update_spec_content(db, FQN, SPEC_V1)
        assert result is not None
        # No content change → no invalidation
        assert result["metadata"]["phases"]["design"]["status"] == "approved"
        versions = artifact_storage.list_artifact_versions(db, spec["id"])
        assert len(versions) == 1  # No new version


# ---------------------------------------------------------------------------
# Re-approval after stale
# ---------------------------------------------------------------------------


class TestReApprovalAfterStale:
    def test_reapprove_clears_stale(self, db: Any, spec: dict) -> None:
        from anteroom.services.spec_service import approve_phase, update_spec_content

        approve_phase(db, FQN, "design", "troy")
        update_spec_content(db, FQN, SPEC_V2_REQ_CHANGED)

        # Re-approve
        result = approve_phase(db, FQN, "design", "user2")
        assert result is not None
        assert result["metadata"]["phases"]["design"]["status"] == "approved"
        assert result["metadata"]["phases"]["design"]["approved_by"] == "user2"

    def test_reapprove_updates_approved_at_version(self, db: Any, spec: dict) -> None:
        from anteroom.services.spec_service import approve_phase, update_spec_content

        approve_phase(db, FQN, "design", "troy")
        update_spec_content(db, FQN, SPEC_V2_REQ_CHANGED)  # creates version 2

        result = approve_phase(db, FQN, "design", "user2")
        assert result is not None
        # approved_at_version should be 2 (the current version after the content update)
        assert result["metadata"]["phases"]["design"]["approved_at_version"] == 2


# ---------------------------------------------------------------------------
# approved_at_version recording
# ---------------------------------------------------------------------------


class TestApprovedAtVersion:
    def test_approve_records_version(self, db: Any, spec: dict) -> None:
        from anteroom.services.spec_service import approve_phase

        result = approve_phase(db, FQN, "requirements", "troy")
        assert result is not None
        assert result["metadata"]["phases"]["requirements"]["approved_at_version"] == 1

    def test_approve_after_content_update_records_new_version(self, db: Any, spec: dict) -> None:
        from anteroom.services.spec_service import approve_phase, update_spec_content

        update_spec_content(db, FQN, SPEC_V2_REQ_CHANGED)
        result = approve_phase(db, FQN, "requirements", "troy")
        assert result is not None
        assert result["metadata"]["phases"]["requirements"]["approved_at_version"] == 2

    def test_unapprove_clears_approved_at_version(self, db: Any, spec: dict) -> None:
        from anteroom.services.spec_service import approve_phase, unapprove_phase

        approve_phase(db, FQN, "design", "troy")
        result = unapprove_phase(db, FQN, "design")
        assert result is not None
        assert "approved_at_version" not in result["metadata"]["phases"]["design"]

    def test_stale_preserves_approved_at_version(self, db: Any, spec: dict) -> None:
        from anteroom.services.spec_service import approve_phase, update_spec_content

        approve_phase(db, FQN, "design", "troy")
        result = update_spec_content(db, FQN, SPEC_V2_REQ_CHANGED)
        assert result is not None
        assert result["metadata"]["phases"]["design"]["status"] == "stale"
        assert result["metadata"]["phases"]["design"]["approved_at_version"] == 1


# ---------------------------------------------------------------------------
# derive_stale_reason
# ---------------------------------------------------------------------------


class TestDeriveStaleReason:
    def test_not_stale_returns_none(self, db: Any, spec: dict) -> None:
        from anteroom.services.spec_diff import derive_stale_reason

        result = derive_stale_reason(db, spec["id"], "design", spec["metadata"])
        assert result is None

    def test_stale_with_approved_at_version(self, db: Any, spec: dict) -> None:
        from anteroom.services.spec_diff import derive_stale_reason
        from anteroom.services.spec_service import approve_phase, update_spec_content

        approve_phase(db, FQN, "design", "troy")
        updated = update_spec_content(db, FQN, SPEC_V2_REQ_CHANGED)
        assert updated is not None

        reason = derive_stale_reason(db, spec["id"], "design", updated["metadata"])
        assert reason is not None
        assert "requirements" in reason
        assert "version 1" in reason

    def test_stale_without_approved_at_version(self, db: Any, spec: dict) -> None:
        from anteroom.services import artifact_storage
        from anteroom.services.spec_diff import derive_stale_reason
        from anteroom.services.spec_schema import set_phase_status

        # Manually set stale without approved_at_version
        meta = set_phase_status(spec["metadata"], "design", SpecPhaseStatus.STALE)
        artifact_storage.update_artifact(db, spec["id"], metadata=meta)

        reason = derive_stale_reason(db, spec["id"], "design", meta)
        assert reason is not None
        assert "stale" in reason.lower()

    def test_stale_with_missing_version(self, db: Any, spec: dict) -> None:
        from anteroom.services import artifact_storage
        from anteroom.services.spec_diff import derive_stale_reason
        from anteroom.services.spec_schema import set_phase_status

        # Set stale with a version that doesn't exist
        meta = set_phase_status(spec["metadata"], "design", SpecPhaseStatus.STALE)
        meta["phases"]["design"]["approved_at_version"] = 999
        artifact_storage.update_artifact(db, spec["id"], metadata=meta)

        reason = derive_stale_reason(db, spec["id"], "design", meta)
        assert reason is not None
        assert "999" in reason
