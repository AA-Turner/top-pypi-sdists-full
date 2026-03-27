"""Unit tests for bugfix spec mode in spec_schema.py."""

from __future__ import annotations

import pytest

from anteroom.services.spec_schema import (
    BUGFIX_TEMPLATE,
    FEATURE_TEMPLATE,
    SpecMode,
    SpecPhaseStatus,
    SpecValidationError,
    default_phase_metadata,
    get_phase_status,
    parse_spec_content,
    serialize_spec_content,
    set_phase_status,
)

VALID_BUGFIX_YAML = """\
mode: bugfix
requirements: |
  ## Current Behavior
  Widget crashes on empty input.

  ## Expected Behavior
  Widget handles empty input gracefully.

  ## Steps to Reproduce
  1. Open widget
  2. Submit empty form
design: |
  ## Root Cause
  Missing null check in parser.

  ## Fix Approach
  Add guard clause before parse.

  ## Non-Regression Boundaries
  Existing widget tests must pass.
tasks:
  - id: t1
    summary: Add null check to parser
"""

VALID_FEATURE_YAML = """\
requirements: |
  Must support widgets.
design: |
  Use the widget parser pattern.
tasks:
  - id: t1
    summary: Implement widget parser
"""

EXPLICIT_FEATURE_YAML = """\
mode: feature
requirements: |
  Must support widgets.
design: |
  Use the widget parser pattern.
tasks:
  - id: t1
    summary: Implement widget parser
"""


class TestParseBugfixContent:
    def test_parse_bugfix_content(self) -> None:
        spec = parse_spec_content(VALID_BUGFIX_YAML)
        assert spec.mode == SpecMode.BUGFIX
        assert "Current Behavior" in spec.requirements
        assert "Root Cause" in spec.design
        assert len(spec.tasks) == 1
        assert spec.tasks[0].id == "t1"

    def test_parse_feature_content_default(self) -> None:
        spec = parse_spec_content(VALID_FEATURE_YAML)
        assert spec.mode == SpecMode.FEATURE

    def test_parse_explicit_feature_mode(self) -> None:
        spec = parse_spec_content(EXPLICIT_FEATURE_YAML)
        assert spec.mode == SpecMode.FEATURE

    def test_parse_invalid_mode(self) -> None:
        yaml_str = VALID_FEATURE_YAML.replace("requirements:", "mode: hotfix\nrequirements:")
        with pytest.raises(SpecValidationError, match="Invalid mode.*hotfix"):
            parse_spec_content(yaml_str)


class TestSerializeBugfix:
    def test_serialize_bugfix_includes_mode(self) -> None:
        spec = parse_spec_content(VALID_BUGFIX_YAML)
        output = serialize_spec_content(spec)
        assert "mode: bugfix" in output

    def test_serialize_feature_omits_mode(self) -> None:
        spec = parse_spec_content(VALID_FEATURE_YAML)
        output = serialize_spec_content(spec)
        assert "mode:" not in output


class TestBugfixTemplate:
    def test_bugfix_template_parses(self) -> None:
        spec = parse_spec_content(BUGFIX_TEMPLATE)
        assert spec.mode == SpecMode.BUGFIX
        assert "Current Behavior" in spec.requirements
        assert "Root Cause" in spec.design

    def test_feature_template_parses(self) -> None:
        spec = parse_spec_content(FEATURE_TEMPLATE)
        assert spec.mode == SpecMode.FEATURE


class TestBugfixApproval:
    def test_bugfix_approval_uses_same_phases(self) -> None:
        meta = default_phase_metadata()
        for phase in ("requirements", "design", "tasks"):
            assert get_phase_status(meta, phase) == SpecPhaseStatus.DRAFT

        meta = set_phase_status(meta, "requirements", SpecPhaseStatus.APPROVED, approved_by="user")
        assert get_phase_status(meta, "requirements") == SpecPhaseStatus.APPROVED


class TestBugfixInvalidation:
    def test_bugfix_invalidation_same_rules(self) -> None:
        from anteroom.services.spec_diff import evaluate_invalidation_rules

        old = parse_spec_content(VALID_BUGFIX_YAML)
        new_yaml = VALID_BUGFIX_YAML.replace("Widget crashes", "Widget fails")
        new = parse_spec_content(new_yaml)

        meta = default_phase_metadata()
        meta = set_phase_status(meta, "design", SpecPhaseStatus.APPROVED, approved_by="user")

        invalidations = evaluate_invalidation_rules(old, new, meta)
        phases_invalidated = [phase for phase, _reason in invalidations]
        assert "design" in phases_invalidated


class TestBugfixDiff:
    def test_bugfix_diff_same_engine(self) -> None:
        from anteroom.services.spec_diff import diff_spec_versions

        old = parse_spec_content(VALID_BUGFIX_YAML)
        new_yaml = VALID_BUGFIX_YAML.replace("Widget crashes", "Widget fails")
        new = parse_spec_content(new_yaml)

        diff = diff_spec_versions(old, new, version_from=1, version_to=2)
        req_change = next(pc for pc in diff.phase_changes if pc.phase == "requirements")
        assert req_change.content_changed


class TestBackwardCompat:
    def test_backward_compat_no_mode_field(self) -> None:
        spec = parse_spec_content(VALID_FEATURE_YAML)
        assert spec.mode == SpecMode.FEATURE
        output = serialize_spec_content(spec)
        reparsed = parse_spec_content(output)
        assert reparsed.mode == SpecMode.FEATURE
        assert reparsed.requirements == spec.requirements
