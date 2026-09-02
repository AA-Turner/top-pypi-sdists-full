"""Tests for _validate_mapping_config helper (FR-007)."""

from __future__ import annotations

import pytest

from agentic_devtools.adapters.issue_type_mapping import _validate_mapping_config


class TestValidateMappingConfig:
    def test_valid_entries_pass(self) -> None:
        raw = {"epic": "MyEpic", "bug": "MyBug"}
        result = _validate_mapping_config(raw, "test_field")
        assert result == {"epic": "MyEpic", "bug": "MyBug"}

    def test_values_are_trimmed_before_storing(self) -> None:
        raw = {"epic": "  MyEpic  "}
        result = _validate_mapping_config(raw, "test_field")
        assert result == {"epic": "MyEpic"}

    def test_invalid_key_rejected(self) -> None:
        with pytest.raises(ValueError, match="Invalid key 'story'"):
            _validate_mapping_config({"story": "Story"}, "test_field")

    def test_empty_value_rejected(self) -> None:
        with pytest.raises(ValueError, match="non-empty string"):
            _validate_mapping_config({"epic": ""}, "test_field")

    def test_whitespace_value_rejected(self) -> None:
        with pytest.raises(ValueError, match="non-empty string"):
            _validate_mapping_config({"epic": "   "}, "test_field")

    def test_non_string_value_rejected(self) -> None:
        with pytest.raises(ValueError, match="non-empty string"):
            _validate_mapping_config({"epic": 42}, "test_field")  # type: ignore[dict-item]

    def test_error_includes_config_path(self) -> None:
        with pytest.raises(ValueError, match="in /path/to/config.json"):
            _validate_mapping_config({"story": "x"}, "field", "/path/to/config.json")

    def test_error_includes_field_name(self) -> None:
        with pytest.raises(ValueError, match="platform.github.issue_type_labels"):
            _validate_mapping_config({"story": "x"}, "platform.github.issue_type_labels")
