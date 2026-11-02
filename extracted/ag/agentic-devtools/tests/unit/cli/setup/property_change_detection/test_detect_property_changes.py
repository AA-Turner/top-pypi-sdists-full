"""Tests for detect_property_changes function."""

from __future__ import annotations

import logging

import pytest

from agentic_devtools.cli.setup.property_change_detection import (
    CATEGORY_ORDER,
    detect_property_changes,
)


def _prop(
    name: str,
    *,
    type_: str = "string",
    required: bool = False,
    included_in_template: bool = True,
    display_name: str | None = None,
    allowed_values: list[str] | None = None,
) -> dict[str, object]:
    """Build a property dict for testing."""
    d: dict[str, object] = {
        "name": name,
        "type": type_,
        "required": required,
        "included_in_template": included_in_template,
    }
    if display_name is not None:
        d["display_name"] = display_name
    if allowed_values is not None:
        d["allowed_values"] = allowed_values
    return d


class TestDetectPropertyChangesNew:
    """Tests for NEW property detection (FR-001, FR-002)."""

    def test_single_new_property(self) -> None:
        """Single property in fresh not in saved is classified as NEW."""
        saved = {"summary": _prop("summary")}
        fresh = {"summary": _prop("summary"), "priority": _prop("priority")}
        result = detect_property_changes(saved, fresh)

        new_changes = [c for c in result.changes if c.category == "NEW"]
        assert len(new_changes) == 1
        assert new_changes[0].key == "priority"
        assert result.merged["priority"]["included_in_template"] is True

    def test_multiple_new_properties(self) -> None:
        """Multiple new properties are all classified as NEW."""
        saved = {"a": _prop("a")}
        fresh = {"a": _prop("a"), "b": _prop("b"), "c": _prop("c")}
        result = detect_property_changes(saved, fresh)

        new_changes = [c for c in result.changes if c.category == "NEW"]
        assert len(new_changes) == 2
        assert {c.key for c in new_changes} == {"b", "c"}

    def test_new_property_defaults_included_in_template_true(self) -> None:
        """New properties default to included_in_template=true in merged output."""
        saved: dict[str, dict[str, object]] = {}
        fresh = {"x": {"name": "x", "type": "number"}}
        result = detect_property_changes(saved, fresh)

        assert result.merged["x"]["included_in_template"] is True

    def test_new_log_output(self, caplog: pytest.LogCaptureFixture) -> None:
        """NEW log includes INFO-level literal label, key, and included_in_template=true."""
        saved: dict[str, dict[str, object]] = {}
        fresh = {"field_a": _prop("field_a")}
        with caplog.at_level(logging.INFO):
            detect_property_changes(saved, fresh)

        new_logs = [r for r in caplog.records if "NEW:" in r.message]
        assert len(new_logs) == 1
        assert "field_a" in new_logs[0].message
        assert "included_in_template=true" in new_logs[0].message
        assert new_logs[0].levelno == logging.INFO


class TestDetectPropertyChangesRemoved:
    """Tests for REMOVED property detection (FR-001, FR-003)."""

    def test_single_removed_property(self) -> None:
        """Property in saved but not in fresh is classified as REMOVED."""
        saved = {"a": _prop("a"), "b": _prop("b")}
        fresh = {"a": _prop("a")}
        result = detect_property_changes(saved, fresh)

        removed = [c for c in result.changes if c.category == "REMOVED"]
        assert len(removed) == 1
        assert removed[0].key == "b"
        assert "b" not in result.merged

    def test_excluded_property_removed(self) -> None:
        """Previously excluded property that disappears logs as REMOVED, not EXCLUDED."""
        saved = {"x": _prop("x", included_in_template=False)}
        fresh: dict[str, dict[str, object]] = {}
        result = detect_property_changes(saved, fresh)

        removed = [c for c in result.changes if c.category == "REMOVED"]
        assert len(removed) == 1
        assert removed[0].key == "x"
        excluded = [c for c in result.changes if c.category == "EXCLUDED"]
        assert len(excluded) == 0

    def test_mixed_new_and_removed(self) -> None:
        """Mix of new and removed properties both correctly classified."""
        saved = {"a": _prop("a"), "b": _prop("b")}
        fresh = {"a": _prop("a"), "c": _prop("c")}
        result = detect_property_changes(saved, fresh)

        new = [c for c in result.changes if c.category == "NEW"]
        removed = [c for c in result.changes if c.category == "REMOVED"]
        assert len(new) == 1 and new[0].key == "c"
        assert len(removed) == 1 and removed[0].key == "b"

    def test_removed_log_output(self, caplog: pytest.LogCaptureFixture) -> None:
        """REMOVED log includes INFO-level literal label and property key."""
        saved = {"gone": _prop("gone")}
        fresh: dict[str, dict[str, object]] = {}
        with caplog.at_level(logging.INFO):
            detect_property_changes(saved, fresh)

        removed_logs = [r for r in caplog.records if "REMOVED:" in r.message]
        assert len(removed_logs) == 1
        assert "gone" in removed_logs[0].message
        assert removed_logs[0].levelno == logging.INFO


class TestDetectPropertyChangesExcluded:
    """Tests for EXCLUDED property preservation (FR-004, FR-005)."""

    def test_single_exclusion_preserved(self) -> None:
        """included_in_template=false is preserved in merged output."""
        saved = {"x": _prop("x", included_in_template=False)}
        fresh = {"x": _prop("x")}
        result = detect_property_changes(saved, fresh)

        assert result.merged["x"]["included_in_template"] is False

    def test_multiple_exclusions_preserved(self) -> None:
        """Multiple excluded properties are all preserved."""
        saved = {
            "a": _prop("a", included_in_template=False),
            "b": _prop("b", included_in_template=False),
            "c": _prop("c"),
        }
        fresh = {"a": _prop("a"), "b": _prop("b"), "c": _prop("c")}
        result = detect_property_changes(saved, fresh)

        assert result.merged["a"]["included_in_template"] is False
        assert result.merged["b"]["included_in_template"] is False
        assert result.merged["c"]["included_in_template"] is True

    def test_exclusion_survives_attribute_changes(self) -> None:
        """included_in_template=false survives when other attributes change."""
        saved = {"x": _prop("x", included_in_template=False, required=False)}
        fresh = {"x": _prop("x", required=True)}
        result = detect_property_changes(saved, fresh)

        assert result.merged["x"]["included_in_template"] is False
        assert result.merged["x"]["required"] is True

    def test_baseline_excluded_log_format(self, caplog: pytest.LogCaptureFixture) -> None:
        """Baseline EXCLUDED log matches exact format from FR-005."""
        saved = {"secret": _prop("secret", included_in_template=False)}
        fresh = {"secret": _prop("secret")}
        with caplog.at_level(logging.INFO):
            detect_property_changes(saved, fresh)

        excluded_logs = [r for r in caplog.records if "EXCLUDED:" in r.message and "attribute" not in r.message]
        assert len(excluded_logs) == 1
        expected = "EXCLUDED: property 'secret' is excluded from template (included_in_template=false)"
        assert excluded_logs[0].message == expected

    def test_excluded_only_schema_match_has_no_changes(self) -> None:
        """EXCLUDED-only classification without schema delta keeps has_changes=False."""
        saved = {"secret": _prop("secret", included_in_template=False)}
        fresh = {"secret": _prop("secret")}
        result = detect_property_changes(saved, fresh)

        assert result.has_changes is False

    def test_three_independent_exclusion_scenarios(self) -> None:
        """At least 3 independent scenarios preserve included_in_template=false (SC-002)."""
        # Scenario 1: Simple exclusion, no attribute changes
        saved1 = {"x": _prop("x", included_in_template=False)}
        fresh1 = {"x": _prop("x")}
        r1 = detect_property_changes(saved1, fresh1)
        assert r1.merged["x"]["included_in_template"] is False

        # Scenario 2: Exclusion with type change
        saved2 = {"y": _prop("y", included_in_template=False, type_="string")}
        fresh2 = {"y": _prop("y", type_="number")}
        r2 = detect_property_changes(saved2, fresh2)
        assert r2.merged["y"]["included_in_template"] is False

        # Scenario 3: Exclusion alongside new and included properties
        saved3 = {"a": _prop("a", included_in_template=False), "b": _prop("b")}
        fresh3 = {"a": _prop("a"), "b": _prop("b"), "c": _prop("c")}
        r3 = detect_property_changes(saved3, fresh3)
        assert r3.merged["a"]["included_in_template"] is False


class TestDetectPropertyChangesChanged:
    """Tests for CHANGED attribute detection (FR-006)."""

    def test_required_attribute_change(self) -> None:
        """Change in 'required' attribute is detected."""
        saved = {"p": _prop("p", required=False)}
        fresh = {"p": _prop("p", required=True)}
        result = detect_property_changes(saved, fresh)

        changed = [c for c in result.changes if c.category == "CHANGED"]
        assert any(c.attribute == "required" for c in changed)

    def test_type_attribute_change(self) -> None:
        """Change in 'type' attribute is detected."""
        saved = {"p": _prop("p", type_="string")}
        fresh = {"p": _prop("p", type_="number")}
        result = detect_property_changes(saved, fresh)

        changed = [c for c in result.changes if c.category == "CHANGED"]
        assert any(c.attribute == "type" and c.details == {"old": "string", "new": "number"} for c in changed)

    def test_display_name_attribute_change(self) -> None:
        """Change in 'display_name' attribute is detected."""
        saved = {"p": {**_prop("p"), "display_name": "Old Name"}}
        fresh = {"p": {**_prop("p"), "display_name": "New Name"}}
        result = detect_property_changes(saved, fresh)

        changed = [c for c in result.changes if c.category == "CHANGED"]
        assert any(c.attribute == "display_name" for c in changed)

    def test_missing_attribute_sentinel(self) -> None:
        """Missing attribute on one side uses <missing> sentinel (FR-006, SC-006)."""
        saved = {"p": {"name": "p", "type": "string", "included_in_template": True}}
        fresh = {"p": {"name": "p", "type": "string", "included_in_template": True, "extra": "val"}}
        result = detect_property_changes(saved, fresh)

        changed = [c for c in result.changes if c.category == "CHANGED"]
        assert any(c.attribute == "extra" and c.details["old"] == "<missing>" for c in changed)

    def test_missing_sentinel_saved_side(self) -> None:
        """Attribute removed from fresh uses <missing> on new side."""
        saved = {"p": {"name": "p", "type": "string", "included_in_template": True, "extra": "val"}}
        fresh = {"p": {"name": "p", "type": "string", "included_in_template": True}}
        result = detect_property_changes(saved, fresh)

        changed = [c for c in result.changes if c.category == "CHANGED"]
        assert any(c.attribute == "extra" and c.details["new"] == "<missing>" for c in changed)

    def test_none_value_vs_present(self) -> None:
        """None value is distinct from missing key."""
        saved = {"p": {"name": "p", "type": "string", "included_in_template": True, "allowed_values": None}}
        fresh = {"p": {"name": "p", "type": "string", "included_in_template": True, "allowed_values": ["a", "b"]}}
        result = detect_property_changes(saved, fresh)

        changed = [c for c in result.changes if c.category == "CHANGED"]
        assert any(c.attribute == "allowed_values" and c.details["old"] is None for c in changed)

    def test_changed_log_output(self, caplog: pytest.LogCaptureFixture) -> None:
        """CHANGED log includes literal label, key, attr, old, and new values."""
        saved = {"p": _prop("p", required=False)}
        fresh = {"p": _prop("p", required=True)}
        with caplog.at_level(logging.INFO):
            detect_property_changes(saved, fresh)

        changed_logs = [r for r in caplog.records if "CHANGED:" in r.message]
        assert len(changed_logs) >= 1
        msg = changed_logs[0].message
        assert "p" in msg
        assert "required" in msg
        assert "False" in msg
        assert "True" in msg

    def test_unchanged_log_output(self, caplog: pytest.LogCaptureFixture) -> None:
        """UNCHANGED properties emit an INFO log entry (FR-004)."""
        schema = {"p": _prop("p")}
        with caplog.at_level(logging.INFO):
            detect_property_changes(schema, dict(schema))

        unchanged_logs = [r for r in caplog.records if "UNCHANGED:" in r.message]
        assert len(unchanged_logs) == 1
        assert "p" in unchanged_logs[0].message

    def test_excluded_property_with_attribute_changes(self, caplog: pytest.LogCaptureFixture) -> None:
        """Excluded property with attr changes emits baseline + per-attr EXCLUDED entries."""
        saved = {"x": _prop("x", included_in_template=False, required=False)}
        fresh = {"x": _prop("x", required=True)}
        with caplog.at_level(logging.INFO):
            result = detect_property_changes(saved, fresh)

        excluded = [c for c in result.changes if c.category == "EXCLUDED"]
        # At least baseline + one per-attribute entry
        assert len(excluded) >= 2
        baseline = [c for c in excluded if c.attribute is None]
        attr_entries = [c for c in excluded if c.attribute is not None]
        assert len(baseline) == 1
        assert len(attr_entries) >= 1
        assert any(c.attribute == "required" for c in attr_entries)

        # Verify log messages
        excluded_logs = [r for r in caplog.records if "EXCLUDED:" in r.message]
        assert len(excluded_logs) >= 2

    def test_excluded_per_attribute_log_format(self, caplog: pytest.LogCaptureFixture) -> None:
        """Per-attribute EXCLUDED log includes preserved flag notation."""
        saved = {"x": _prop("x", included_in_template=False, type_="string")}
        fresh = {"x": _prop("x", type_="number")}
        with caplog.at_level(logging.INFO):
            detect_property_changes(saved, fresh)

        attr_logs = [r for r in caplog.records if "EXCLUDED:" in r.message and "attribute" in r.message]
        assert len(attr_logs) >= 1
        assert "included_in_template=false preserved" in attr_logs[0].message


class TestDetectPropertyChangesBootstrap:
    """Tests for first-time discovery with no prior schema (FR-008)."""

    def test_bootstrap_all_new(self) -> None:
        """saved=None treats all fresh properties as NEW."""
        fresh = {"a": _prop("a"), "b": _prop("b")}
        result = detect_property_changes(None, fresh)

        assert all(c.category == "NEW" for c in result.changes)
        assert len(result.changes) == 2
        assert result.has_changes is True

    def test_bootstrap_empty_fresh(self) -> None:
        """saved=None with empty fresh still sets has_changes=True (FR-008)."""
        result = detect_property_changes(None, {})
        assert result.has_changes is True
        assert result.merged == {}
        assert result.changes == []

    def test_steady_state_both_empty(self) -> None:
        """saved={} and fresh={} is a no-op (has_changes=False, FR-009)."""
        result = detect_property_changes({}, {})
        assert result.has_changes is False
        assert result.merged == {}

    def test_identical_schemas_no_changes(self) -> None:
        """Identical saved and fresh schemas produce has_changes=False."""
        schema = {"a": _prop("a"), "b": _prop("b")}
        result = detect_property_changes(schema, dict(schema))
        assert result.has_changes is False
        assert all(c.category == "UNCHANGED" for c in result.changes)


class TestDetectPropertyChangesSorting:
    """Tests for deterministic sorting (FR-011)."""

    def test_category_order(self) -> None:
        """Changes are sorted by category order: NEW < REMOVED < EXCLUDED < CHANGED < UNCHANGED."""
        saved = {
            "existing": _prop("existing"),
            "removed": _prop("removed"),
            "excluded": _prop("excluded", included_in_template=False),
            "changed": _prop("changed", required=False),
        }
        fresh = {
            "existing": _prop("existing"),
            "new_one": _prop("new_one"),
            "excluded": _prop("excluded"),
            "changed": _prop("changed", required=True),
        }
        result = detect_property_changes(saved, fresh)

        categories = [c.category for c in result.changes]
        category_indices = [CATEGORY_ORDER[cat] for cat in categories]
        assert category_indices == sorted(category_indices)

    def test_alphabetical_within_category(self) -> None:
        """Within same category, keys are alphabetically sorted."""
        saved: dict[str, dict[str, object]] = {}
        fresh = {"z": _prop("z"), "a": _prop("a"), "m": _prop("m")}
        result = detect_property_changes(saved, fresh)

        keys = [c.key for c in result.changes if c.category == "NEW"]
        assert keys == sorted(keys)

    def test_baseline_before_attribute_entries(self) -> None:
        """Baseline entries (attribute=None) come before attribute-level entries."""
        saved = {"x": _prop("x", included_in_template=False, required=False, type_="string")}
        fresh = {"x": _prop("x", required=True, type_="number")}
        result = detect_property_changes(saved, fresh)

        x_changes = [c for c in result.changes if c.key == "x"]
        assert x_changes[0].attribute is None  # baseline first
        attr_entries = [c for c in x_changes if c.attribute is not None]
        assert len(attr_entries) >= 2
        attr_names = [c.attribute for c in attr_entries if c.attribute is not None]
        assert attr_names == sorted(attr_names)


class TestDetectPropertyChangesSummary:
    """Tests for summary log line (FR-010)."""

    def test_summary_mixed_changes(self, caplog: pytest.LogCaptureFixture) -> None:
        """Summary line emitted with accurate counts for mixed changes."""
        saved = {"a": _prop("a"), "b": _prop("b"), "c": _prop("c", included_in_template=False)}
        fresh = {"a": _prop("a"), "c": _prop("c"), "d": _prop("d")}
        with caplog.at_level(logging.INFO):
            detect_property_changes(saved, fresh)

        summary_logs = [r for r in caplog.records if "Property change detection complete:" in r.message]
        assert len(summary_logs) == 1
        msg = summary_logs[0].message
        assert "1 new" in msg
        assert "1 removed" in msg
        assert "1 excluded" in msg
        assert "0 changed" in msg
        assert "1 unchanged" in msg  # "a" is unchanged

    def test_summary_no_changes(self, caplog: pytest.LogCaptureFixture) -> None:
        """Summary line for identical schemas shows all zeros except unchanged."""
        schema = {"a": _prop("a"), "b": _prop("b")}
        with caplog.at_level(logging.INFO):
            detect_property_changes(schema, dict(schema))

        summary_logs = [r for r in caplog.records if "Property change detection complete:" in r.message]
        assert len(summary_logs) == 1
        msg = summary_logs[0].message
        assert "0 new" in msg
        assert "0 removed" in msg
        assert "0 excluded" in msg
        assert "0 changed" in msg
        assert "2 unchanged" in msg

    def test_summary_bootstrap(self, caplog: pytest.LogCaptureFixture) -> None:
        """Summary line for bootstrap shows all as new."""
        fresh = {"a": _prop("a"), "b": _prop("b"), "c": _prop("c")}
        with caplog.at_level(logging.INFO):
            detect_property_changes(None, fresh)

        summary_logs = [r for r in caplog.records if "Property change detection complete:" in r.message]
        assert len(summary_logs) == 1
        assert "3 new" in summary_logs[0].message


class TestDetectPropertyChangesMerged:
    """Tests for merged output (FR-007)."""

    def test_merged_contains_fresh_properties_with_flags(self) -> None:
        """Merged dict contains exactly fresh properties with flags carried forward."""
        saved = {"a": _prop("a", included_in_template=False), "b": _prop("b")}
        fresh = {"a": _prop("a"), "b": _prop("b"), "c": _prop("c")}
        result = detect_property_changes(saved, fresh)

        assert set(result.merged.keys()) == {"a", "b", "c"}
        assert result.merged["a"]["included_in_template"] is False
        assert result.merged["b"]["included_in_template"] is True
        assert result.merged["c"]["included_in_template"] is True

    def test_merged_preserves_fresh_discovery_order(self) -> None:
        """Merged dict preserves insertion order from fresh discovery."""
        saved = {"z": _prop("z"), "a": _prop("a")}
        fresh = {"z": _prop("z"), "m": _prop("m"), "a": _prop("a")}
        result = detect_property_changes(saved, fresh)

        assert list(result.merged.keys()) == ["z", "m", "a"]


class TestDetectPropertyChangesEdgeCases:
    """Tests for edge cases (FR-006, FR-009)."""

    def test_reorder_only_no_changes(self) -> None:
        """Reorder-only difference does not produce has_changes=True."""
        saved = {"a": _prop("a"), "b": _prop("b")}
        fresh = {"b": _prop("b"), "a": _prop("a")}
        result = detect_property_changes(saved, fresh)

        assert result.has_changes is False

    def test_none_value_distinct_from_missing(self) -> None:
        """None attribute value is different from key not present at all."""
        saved = {"p": {"name": "p", "type": "string", "included_in_template": True, "x": None}}
        fresh = {"p": {"name": "p", "type": "string", "included_in_template": True}}
        result = detect_property_changes(saved, fresh)

        changed = [c for c in result.changes if c.category == "CHANGED"]
        assert any(c.attribute == "x" and c.details["old"] is None and c.details["new"] == "<missing>" for c in changed)
