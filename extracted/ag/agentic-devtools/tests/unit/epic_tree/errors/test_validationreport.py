"""Tests for ValidationReport and ValidationReportEntry."""

import json

import pytest

from agentic_devtools.epic_tree.errors import ValidationReport, ValidationReportEntry


class TestValidationReport:
    """Tests for ValidationReport dataclass."""

    def test_valid_report_empty_errors(self):
        """Fresh report has valid=True and empty errors list."""
        report = ValidationReport()
        assert report.valid is True
        assert report.errors == []

    def test_valid_report_empty_warnings(self):
        """Fresh report has empty warnings list."""
        report = ValidationReport()
        assert report.warnings == []

    def test_add_error_sets_invalid(self):
        """Adding an error sets valid to False."""
        report = ValidationReport()
        report.add_error("duplicate_ref", "Duplicate ref 'x'", ["epic.features[0]"])
        assert report.valid is False
        assert len(report.errors) == 1

    def test_error_entry_attributes(self):
        """ValidationReportEntry has category, message, and paths."""
        entry = ValidationReportEntry(
            category="unresolved_reference",
            message="Ref 'x' not found",
            paths=["epic.features[0]"],
        )
        assert entry.category == "unresolved_reference"
        assert entry.message == "Ref 'x' not found"
        assert entry.paths == ["epic.features[0]"]

    def test_multiple_errors_aggregated(self):
        """Multiple add_error calls aggregate errors."""
        report = ValidationReport()
        report.add_error("duplicate_ref", "Dup 1", ["path1"])
        report.add_error("cycle_detected", "Cycle found", ["path2", "path3"])
        assert len(report.errors) == 2

    def test_paths_default_empty(self):
        """paths defaults to empty list when not provided."""
        report = ValidationReport()
        report.add_error("depth_exceeded", "Too deep")
        assert report.errors[0].paths == []

    def test_property_name_defaults_to_none(self):
        """property_name defaults to None when not supplied."""
        entry = ValidationReportEntry(category="duplicate_ref", message="Dup")
        assert entry.property_name is None

    def test_property_name_propagated_via_add_error(self):
        """add_error propagates property_name to the stored entry."""
        report = ValidationReport()
        report.add_error("required", "'ref' is a required property", ["/epic"], property_name="ref")
        assert report.errors[0].property_name == "ref"

    def test_add_error_property_name_none_by_default(self):
        """property_name is None when add_error is called without it."""
        report = ValidationReport()
        report.add_error("type", "Type mismatch", ["/epic/ref"])
        assert report.errors[0].property_name is None


class TestValidationReportWarnings:
    """Tests for warnings field behavior."""

    def test_add_warning_does_not_set_invalid(self):
        """Adding a warning does not change valid to False."""
        report = ValidationReport()
        report.add_warning("depth_exceeded", "Close to limit", ["epic.features[0]"])
        assert report.valid is True
        assert len(report.warnings) == 1

    def test_warnings_only_report_is_valid(self):
        """Report with errors=[] and warnings=[entry] has valid=True."""
        report = ValidationReport()
        report.add_warning("info", "Informational", ["path"])
        assert report.valid is True
        assert report.errors == []
        assert len(report.warnings) == 1

    def test_errors_and_warnings_independent(self):
        """Errors and warnings are stored in independent lists."""
        report = ValidationReport()
        report.add_error("cycle_detected", "Cycle", ["p1"])
        report.add_warning("info", "Note", ["p2"])
        assert report.valid is False
        assert len(report.errors) == 1
        assert len(report.warnings) == 1
        assert report.errors[0].category == "cycle_detected"
        assert report.warnings[0].category == "info"


class TestValidationReportSortEntries:
    """Tests for sort_entries() method."""

    def test_sort_entries_sorts_intra_paths(self):
        """sort_entries() sorts each entry's paths list first."""
        report = ValidationReport()
        report.add_error("cycle_detected", "Cycle", ["z_path", "a_path"])
        report.sort_entries()
        assert report.errors[0].paths == ["a_path", "z_path"]

    def test_sort_entries_by_path(self):
        """Entries are sorted by first path."""
        report = ValidationReport()
        report.add_error("err", "B", ["epic.features[1]"])
        report.add_error("err", "A", ["epic.features[0]"])
        report.sort_entries()
        assert report.errors[0].paths == ["epic.features[0]"]
        assert report.errors[1].paths == ["epic.features[1]"]

    def test_sort_entries_numeric_ordering(self):
        """Numeric indices sort numerically: [2] before [10]."""
        report = ValidationReport()
        report.add_error("err", "msg", ["epic.features[10]"])
        report.add_error("err", "msg", ["epic.features[2]"])
        report.sort_entries()
        assert report.errors[0].paths == ["epic.features[2]"]
        assert report.errors[1].paths == ["epic.features[10]"]

    def test_sort_entries_same_path_by_category(self):
        """Same path → sub-sorted by category alphabetically."""
        report = ValidationReport()
        report.add_error("zzz", "msg", ["epic"])
        report.add_error("aaa", "msg", ["epic"])
        report.sort_entries()
        assert report.errors[0].category == "aaa"
        assert report.errors[1].category == "zzz"

    def test_sort_entries_applies_to_warnings(self):
        """sort_entries() applies same ordering to warnings."""
        report = ValidationReport()
        report.add_warning("zzz", "msg", ["b"])
        report.add_warning("aaa", "msg", ["a"])
        report.sort_entries()
        assert report.warnings[0].paths == ["a"]
        assert report.warnings[1].paths == ["b"]


class TestValidationReportToDict:
    """Tests for to_dict() serialization."""

    def test_to_dict_basic(self):
        """to_dict returns valid/errors/warnings keys."""
        report = ValidationReport()
        report.add_error("err", "msg", ["p"])
        d = report.to_dict()
        assert d["valid"] is False
        assert len(d["errors"]) == 1
        assert d["warnings"] == []

    def test_to_dict_entry_fields(self):
        """Each entry dict includes all fields including property_name."""
        report = ValidationReport()
        report.add_error("required", "missing", ["/epic"], property_name="ref")
        d = report.to_dict()
        entry = d["errors"][0]
        assert entry["category"] == "required"
        assert entry["message"] == "missing"
        assert entry["paths"] == ["/epic"]
        assert entry["property_name"] == "ref"

    def test_to_dict_property_name_none(self):
        """property_name appears in output even when None."""
        report = ValidationReport()
        report.add_error("err", "msg", ["p"])
        d = report.to_dict()
        assert "property_name" in d["errors"][0]
        assert d["errors"][0]["property_name"] is None

    def test_empty_report_to_dict(self):
        """Empty report serializes correctly."""
        report = ValidationReport()
        d = report.to_dict()
        assert d == {"valid": True, "errors": [], "warnings": []}


class TestValidationReportFromDict:
    """Tests for from_dict() deserialization."""

    def test_round_trip_with_errors(self):
        """Round-trip to_dict/from_dict with errors preserves equality."""
        report = ValidationReport()
        report.add_error("cycle_detected", "Cycle", ["p1", "p2"])
        report.add_error("duplicate_ref", "Dup", ["p3"])
        restored = ValidationReport.from_dict(report.to_dict())
        assert restored.valid == report.valid
        assert restored.errors == report.errors
        assert restored.warnings == report.warnings

    def test_round_trip_with_warnings(self):
        """Round-trip with warnings preserves equality."""
        report = ValidationReport()
        report.add_warning("info", "Note", ["p1"])
        restored = ValidationReport.from_dict(report.to_dict())
        assert restored.valid is True
        assert restored.warnings == report.warnings

    def test_round_trip_with_property_name(self):
        """Round-trip preserves property_name on entries."""
        report = ValidationReport()
        report.add_error("required", "missing ref", ["/epic"], property_name="ref")
        report.add_warning("info", "Note", ["p"])
        restored = ValidationReport.from_dict(report.to_dict())
        assert restored.errors[0].property_name == "ref"

    def test_from_dict_missing_valid_raises(self):
        """from_dict raises ValueError when 'valid' key is missing."""

        with pytest.raises(ValueError, match="valid"):
            ValidationReport.from_dict({"errors": [], "warnings": []})

    def test_from_dict_missing_errors_raises(self):
        """from_dict raises ValueError when 'errors' key is missing."""

        with pytest.raises(ValueError, match="errors"):
            ValidationReport.from_dict({"valid": True, "warnings": []})

    def test_from_dict_missing_warnings_raises(self):
        """from_dict raises ValueError when 'warnings' key is missing."""

        with pytest.raises(ValueError, match="warnings"):
            ValidationReport.from_dict({"valid": True, "errors": []})

    def test_from_dict_ignores_unknown_top_level_keys(self):
        """from_dict silently ignores unknown top-level keys."""
        data = {"valid": True, "errors": [], "warnings": [], "extra": "ignored"}
        report = ValidationReport.from_dict(data)
        assert report.valid is True

    def test_from_dict_ignores_unknown_entry_keys(self):
        """from_dict silently ignores unknown per-entry keys."""
        data = {
            "valid": False,
            "errors": [
                {
                    "category": "err",
                    "message": "msg",
                    "paths": ["p"],
                    "property_name": None,
                    "unknown_field": 42,
                }
            ],
            "warnings": [],
        }
        report = ValidationReport.from_dict(data)
        assert report.errors[0].category == "err"

    def test_from_dict_accepts_unknown_categories(self):
        """from_dict accepts unknown category values without error."""
        data = {
            "valid": False,
            "errors": [{"category": "totally_custom_category", "message": "m", "paths": []}],
            "warnings": [],
        }
        report = ValidationReport.from_dict(data)
        assert report.errors[0].category == "totally_custom_category"

    def test_from_dict_errors_force_invalid(self):
        """from_dict enforces valid=False whenever errors are present."""
        data = {
            "valid": True,
            "errors": [{"category": "err", "message": "m", "paths": ["p"]}],
            "warnings": [],
        }
        report = ValidationReport.from_dict(data)
        assert report.valid is False

    def test_from_dict_entry_missing_category_raises_value_error(self):
        """from_dict raises ValueError (not KeyError) when entry is missing 'category'."""

        data = {
            "valid": False,
            "errors": [{"message": "msg", "paths": ["p"]}],
            "warnings": [],
        }
        with pytest.raises(ValueError, match="category"):
            ValidationReport.from_dict(data)

    def test_from_dict_entry_missing_message_raises_value_error(self):
        """from_dict raises ValueError (not KeyError) when entry is missing 'message'."""

        data = {
            "valid": False,
            "errors": [{"category": "err", "paths": ["p"]}],
            "warnings": [],
        }
        with pytest.raises(ValueError, match="message"):
            ValidationReport.from_dict(data)

    def test_from_dict_entry_missing_paths_raises_value_error(self):
        """from_dict raises ValueError (not KeyError) when entry is missing 'paths'."""

        data = {
            "valid": False,
            "errors": [{"category": "err", "message": "msg"}],
            "warnings": [],
        }
        with pytest.raises(ValueError, match="paths"):
            ValidationReport.from_dict(data)

    def test_json_round_trip(self):
        """Empty report survives JSON serialization round-trip."""
        report = ValidationReport()
        json_str = json.dumps(report.to_dict())
        restored = ValidationReport.from_dict(json.loads(json_str))
        assert restored == report
