"""Tests for design-first spec flow (#1013)."""

from __future__ import annotations

from pathlib import Path
from typing import Any

import pytest

from anteroom.services.spec_schema import (
    DESIGN_FIRST_TEMPLATE,
    PENDING_SENTINEL,
    SpecContent,
    SpecMode,
    SpecTask,
    is_pending_content,
    parse_spec_content,
    serialize_spec_content,
)

# ---------------------------------------------------------------------------
# Schema layer — sentinel & template
# ---------------------------------------------------------------------------


class TestPendingSentinel:
    def test_sentinel_passes_validation(self) -> None:
        """PENDING_SENTINEL is a valid non-empty string that parses."""
        content = parse_spec_content(DESIGN_FIRST_TEMPLATE)
        assert content.requirements.strip() == PENDING_SENTINEL

    def test_design_first_template_valid(self) -> None:
        content = parse_spec_content(DESIGN_FIRST_TEMPLATE)
        assert content.design.strip() != ""
        assert len(content.tasks) >= 1

    def test_is_pending_requirements(self) -> None:
        content = SpecContent(
            requirements=PENDING_SENTINEL,
            design="real",
            tasks=[SpecTask(id="t1", summary="task")],
        )
        assert is_pending_content("requirements", content) is True

    def test_is_pending_design(self) -> None:
        content = SpecContent(
            requirements="real",
            design=PENDING_SENTINEL,
            tasks=[SpecTask(id="t1", summary="task")],
        )
        assert is_pending_content("design", content) is True

    def test_is_pending_tasks(self) -> None:
        content = SpecContent(
            requirements="real",
            design="real",
            tasks=[SpecTask(id="t1", summary="[pending — derive from design]")],
        )
        assert is_pending_content("tasks", content) is True

    def test_is_not_pending_real_content(self) -> None:
        content = SpecContent(
            requirements="Real requirements",
            design="Real design",
            tasks=[SpecTask(id="t1", summary="Real task")],
        )
        assert is_pending_content("requirements", content) is False
        assert is_pending_content("design", content) is False
        assert is_pending_content("tasks", content) is False

    def test_is_pending_invalid_phase(self) -> None:
        content = SpecContent(requirements="x", design="x", tasks=[SpecTask(id="t1", summary="x")])
        assert is_pending_content("bogus", content) is False

    def test_template_mode_defaults_to_feature(self) -> None:
        content = parse_spec_content(DESIGN_FIRST_TEMPLATE)
        assert content.mode == SpecMode.FEATURE

    def test_template_round_trips(self) -> None:
        content = parse_spec_content(DESIGN_FIRST_TEMPLATE)
        yaml_out = serialize_spec_content(content)
        content2 = parse_spec_content(yaml_out)
        assert content.requirements == content2.requirements
        assert content.design == content2.design


# ---------------------------------------------------------------------------
# Service layer — DB-backed tests
# ---------------------------------------------------------------------------

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
    """Create a real DB via init_db for spec service tests."""
    from anteroom.db import init_db

    return init_db(tmp_path / "test.db")


class TestCreateSpecDesignFirst:
    def test_creation_flow_stored_in_metadata(self, db: Any) -> None:
        from anteroom.services.spec_service import create_spec

        art = create_spec(db, "ns", "design-x", DESIGN_FIRST_TEMPLATE, creation_flow="design_first")
        assert art["metadata"]["creation_flow"] == "design_first"

    def test_creation_flow_none_by_default(self, db: Any) -> None:
        from anteroom.services.spec_service import create_spec

        art = create_spec(db, "ns", "feat-x", VALID_SPEC_YAML)
        assert "creation_flow" not in art["metadata"]


class TestApproveSentinelBlocked:
    def test_approve_pending_requirements_blocked(self, db: Any) -> None:
        from anteroom.services.spec_service import approve_phase, create_spec

        create_spec(db, "ns", "design-x", DESIGN_FIRST_TEMPLATE)
        with pytest.raises(ValueError, match="content is still pending"):
            approve_phase(db, "@ns/spec/design-x", "requirements")

    def test_approve_real_content_allowed(self, db: Any) -> None:
        from anteroom.services.spec_service import approve_phase, create_spec

        create_spec(db, "ns", "feat-x", VALID_SPEC_YAML)
        art = approve_phase(db, "@ns/spec/feat-x", "requirements", "troy")
        assert art is not None
        assert art["metadata"]["phases"]["requirements"]["status"] == "approved"

    def test_approve_pending_design_blocked(self, db: Any) -> None:
        """A spec with sentinel in design cannot have design approved."""
        from anteroom.services.spec_service import approve_phase, create_spec

        sentinel_design_yaml = (
            "requirements: Real requirements\n"
            f'design: "{PENDING_SENTINEL}"\n'
            "tasks:\n  - id: t1\n    summary: Real task\n"
        )
        create_spec(db, "ns", "pending-d", sentinel_design_yaml)
        with pytest.raises(ValueError, match="content is still pending"):
            approve_phase(db, "@ns/spec/pending-d", "design")


class TestUpdateSpecPhase:
    def test_update_requirements_preserves_other_phases(self, db: Any) -> None:
        from anteroom.services.spec_service import create_spec, get_spec, update_spec_phase

        create_spec(db, "ns", "feat-x", VALID_SPEC_YAML)
        result = update_spec_phase(db, "@ns/spec/feat-x", "requirements", "New requirements")
        assert result is not None

        updated = get_spec(db, "@ns/spec/feat-x")
        assert updated is not None
        _, spec = updated
        assert spec.requirements == "New requirements"
        assert "widget parser" in spec.design
        assert len(spec.tasks) == 1

    def test_update_design_preserves_other_phases(self, db: Any) -> None:
        from anteroom.services.spec_service import create_spec, get_spec, update_spec_phase

        create_spec(db, "ns", "feat-x", VALID_SPEC_YAML)
        result = update_spec_phase(db, "@ns/spec/feat-x", "design", "New design approach")
        assert result is not None

        updated = get_spec(db, "@ns/spec/feat-x")
        assert updated is not None
        _, spec = updated
        assert spec.design == "New design approach"
        assert "widgets" in spec.requirements

    def test_update_tasks_phase_rejected(self, db: Any) -> None:
        from anteroom.services.spec_service import create_spec, update_spec_phase

        create_spec(db, "ns", "feat-x", VALID_SPEC_YAML)
        with pytest.raises(ValueError, match="tasks require structured YAML"):
            update_spec_phase(db, "@ns/spec/feat-x", "tasks", "some text")

    def test_update_invalid_phase_name(self, db: Any) -> None:
        from anteroom.services.spec_service import create_spec, update_spec_phase

        create_spec(db, "ns", "feat-x", VALID_SPEC_YAML)
        with pytest.raises(ValueError, match="Invalid phase"):
            update_spec_phase(db, "@ns/spec/feat-x", "bogus", "content")

    def test_update_nonexistent_spec(self, db: Any) -> None:
        from anteroom.services.spec_service import update_spec_phase

        assert update_spec_phase(db, "@ns/spec/nope", "design", "content") is None

    def test_update_triggers_invalidation(self, db: Any) -> None:
        """Changing requirements after design is approved should mark design stale."""
        from anteroom.services.spec_service import (
            approve_phase,
            create_spec,
            get_phase_statuses,
            update_spec_phase,
        )

        create_spec(db, "ns", "feat-x", VALID_SPEC_YAML)
        approve_phase(db, "@ns/spec/feat-x", "requirements", "troy")
        approve_phase(db, "@ns/spec/feat-x", "design", "troy")

        update_spec_phase(db, "@ns/spec/feat-x", "requirements", "Changed requirements")

        statuses = get_phase_statuses(db, "@ns/spec/feat-x")
        assert statuses is not None
        # Design should be stale because requirements changed while design was approved
        from anteroom.services.spec_schema import SpecPhaseStatus

        assert statuses["design"] == SpecPhaseStatus.STALE

    def test_stale_detection_sentinel_to_real(self, db: Any) -> None:
        """Replacing sentinel content with real content triggers stale on approved downstream."""
        from anteroom.services.spec_schema import SpecPhaseStatus
        from anteroom.services.spec_service import (
            approve_phase,
            create_spec,
            get_phase_statuses,
            update_spec_phase,
        )

        create_spec(db, "ns", "design-x", VALID_SPEC_YAML)
        # Approve all phases
        approve_phase(db, "@ns/spec/design-x", "requirements", "troy")
        approve_phase(db, "@ns/spec/design-x", "design", "troy")
        approve_phase(db, "@ns/spec/design-x", "tasks", "troy")

        # Update requirements — should invalidate downstream (design, tasks)
        update_spec_phase(db, "@ns/spec/design-x", "requirements", "Completely new requirements")

        statuses = get_phase_statuses(db, "@ns/spec/design-x")
        assert statuses is not None
        assert statuses["design"] == SpecPhaseStatus.STALE
        assert statuses["tasks"] == SpecPhaseStatus.STALE
