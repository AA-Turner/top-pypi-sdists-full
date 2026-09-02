"""Tests for check_schema_version() function."""

import json
from pathlib import Path

import pytest

from agentic_devtools.epic_tree.errors import VersionMismatchError
from agentic_devtools.epic_tree.validator import check_schema_version

FIXTURES_DIR = Path(__file__).resolve().parent.parent.parent.parent / "fixtures" / "epic-tree"


def _load_fixture(name: str) -> dict:
    return json.loads((FIXTURES_DIR / name).read_text(encoding="utf-8"))


class TestCheckSchemaVersion:
    """Tests for the check_schema_version function."""

    def test_supported_version_passes(self):
        """Version 1.0 passes when supported_major=1."""
        doc = _load_fixture("valid-epic.json")
        check_schema_version(doc, supported_major=1)

    def test_future_major_version_raises(self):
        """Version 2.0 raises VersionMismatchError when supported_major=1."""
        doc = {"schemaVersion": "2.0"}
        with pytest.raises(VersionMismatchError) as exc_info:
            check_schema_version(doc, supported_major=1)
        assert exc_info.value.found_version == "2.0"
        assert exc_info.value.supported_major == 1

    def test_missing_schema_version_raises_key_error(self):
        """Missing schemaVersion raises KeyError."""
        doc = {}
        with pytest.raises(KeyError):
            check_schema_version(doc)

    def test_version_1_1_passes(self):
        """Version 1.1 passes when supported_major=1 (minor mismatch ok)."""
        doc = {"schemaVersion": "1.1"}
        check_schema_version(doc, supported_major=1)

    def test_version_0_passes_for_major_0(self):
        """Version 0.1 passes when supported_major=0."""
        doc = {"schemaVersion": "0.1"}
        check_schema_version(doc, supported_major=0)

    def test_non_string_schema_version_raises_type_error(self):
        """Non-string schemaVersion raises TypeError before major parsing."""
        doc = {"schemaVersion": 1}
        with pytest.raises(TypeError, match="schemaVersion must be a string"):
            check_schema_version(doc)

    def test_invalid_format_raises_value_error(self):
        """Malformed schemaVersion raises ValueError."""
        doc = {"schemaVersion": "not-a-version"}
        with pytest.raises(ValueError, match="schemaVersion must match"):
            check_schema_version(doc)

    def test_three_segment_semver_raises_value_error(self):
        """Three-segment semver (1.0.0) is now invalid."""
        doc = {"schemaVersion": "1.0.0"}
        with pytest.raises(ValueError, match="schemaVersion must match"):
            check_schema_version(doc)

    def test_single_segment_raises_value_error(self):
        """Single-segment version (1) is invalid."""
        doc = {"schemaVersion": "1"}
        with pytest.raises(ValueError, match="schemaVersion must match"):
            check_schema_version(doc)

    def test_v_prefix_raises_value_error(self):
        """v-prefixed version (v1.0) is invalid."""
        doc = {"schemaVersion": "v1.0"}
        with pytest.raises(ValueError, match="schemaVersion must match"):
            check_schema_version(doc)
