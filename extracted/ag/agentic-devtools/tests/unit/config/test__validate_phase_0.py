"""Tests for agentic_devtools.config._validate_phase_0."""

import logging

import pytest

from agentic_devtools.config import (
    CONFIG_FILE,
    PHASE_0_DEFAULT_ENABLED,
    PHASE_0_DEFAULT_SYNC_BACK_FIELDS,
    PHASE_0_DEFAULT_SYNC_BACK_ON_MERGE,
    _validate_phase_0,
)


class TestValidatePhase0:
    """Tests for _validate_phase_0 private helper."""

    def test_returns_defaults_when_input_is_none(self):
        """Return full defaults when raw is None (missing key)."""
        result = _validate_phase_0(None)

        assert result["enabled"] is PHASE_0_DEFAULT_ENABLED
        assert result["sync_back_on_merge"] is PHASE_0_DEFAULT_SYNC_BACK_ON_MERGE
        assert result["sync_back_fields"] == list(PHASE_0_DEFAULT_SYNC_BACK_FIELDS)

    def test_returns_defaults_when_input_is_empty_dict(self):
        """Return all 3 default keys with correct types when input is empty dict."""
        result = _validate_phase_0({})

        assert result["enabled"] is False
        assert result["sync_back_on_merge"] is False
        assert result["sync_back_fields"] == ["comment"]

    def test_preserves_explicit_enabled_true(self):
        """Preserve explicit enabled=true, default other fields."""
        result = _validate_phase_0({"enabled": True})

        assert result["enabled"] is True
        assert result["sync_back_on_merge"] is False
        assert result["sync_back_fields"] == ["comment"]

    def test_preserves_all_explicit_values(self):
        """Preserve all 3 explicitly set fields without modification."""
        raw = {
            "enabled": True,
            "sync_back_on_merge": True,
            "sync_back_fields": ["comment", "label"],
        }

        result = _validate_phase_0(raw)

        assert result["enabled"] is True
        assert result["sync_back_on_merge"] is True
        assert result["sync_back_fields"] == ["comment", "label"]

    def test_warns_and_defaults_enabled_when_string(self, caplog):
        """Log warning and default enabled to false when set to string."""
        with caplog.at_level(logging.WARNING, logger="agentic_devtools.config"):
            result = _validate_phase_0({"enabled": "yes"})

        assert result["enabled"] is False
        warnings = [r for r in caplog.records if r.levelno == logging.WARNING]
        assert len(warnings) == 1
        assert "phase_0.enabled" in warnings[0].message
        assert CONFIG_FILE in warnings[0].message

    def test_warns_and_defaults_sync_back_on_merge_when_string(self, caplog):
        """Log warning and default sync_back_on_merge to false when set to string."""
        with caplog.at_level(logging.WARNING, logger="agentic_devtools.config"):
            result = _validate_phase_0({"sync_back_on_merge": "true"})

        assert result["sync_back_on_merge"] is False
        warnings = [r for r in caplog.records if r.levelno == logging.WARNING]
        assert len(warnings) == 1
        assert "phase_0.sync_back_on_merge" in warnings[0].message
        assert CONFIG_FILE in warnings[0].message

    def test_warns_and_defaults_sync_back_fields_when_string(self, caplog):
        """Log warning and default sync_back_fields when set to plain string."""
        with caplog.at_level(logging.WARNING, logger="agentic_devtools.config"):
            result = _validate_phase_0({"sync_back_fields": "comment"})

        assert result["sync_back_fields"] == ["comment"]
        warnings = [r for r in caplog.records if r.levelno == logging.WARNING]
        assert len(warnings) == 1
        assert "phase_0.sync_back_fields" in warnings[0].message
        assert CONFIG_FILE in warnings[0].message

    def test_warns_and_defaults_sync_back_fields_with_mixed_types(self, caplog):
        """Reject entire array and default when sync_back_fields has non-string elements."""
        with caplog.at_level(logging.WARNING, logger="agentic_devtools.config"):
            result = _validate_phase_0({"sync_back_fields": ["comment", 123]})

        assert result["sync_back_fields"] == ["comment"]
        warnings = [r for r in caplog.records if r.levelno == logging.WARNING]
        assert len(warnings) == 1

    def test_warns_and_defaults_when_raw_is_non_dict_string(self, caplog):
        """Log warning and return full defaults when phase_0 is a string."""
        with caplog.at_level(logging.WARNING, logger="agentic_devtools.config"):
            result = _validate_phase_0("invalid")

        assert result["enabled"] is False
        assert result["sync_back_on_merge"] is False
        assert result["sync_back_fields"] == ["comment"]
        warnings = [r for r in caplog.records if r.levelno == logging.WARNING]
        assert len(warnings) == 1
        assert "str" in warnings[0].message
        assert CONFIG_FILE in warnings[0].message

    def test_warns_and_defaults_when_raw_is_non_dict_list(self, caplog):
        """Log warning and return full defaults when phase_0 is a list."""
        with caplog.at_level(logging.WARNING, logger="agentic_devtools.config"):
            result = _validate_phase_0([1, 2, 3])

        assert result["enabled"] is False
        assert result["sync_back_fields"] == ["comment"]
        warnings = [r for r in caplog.records if r.levelno == logging.WARNING]
        assert len(warnings) == 1
        assert "list" in warnings[0].message

    def test_warns_and_defaults_when_raw_is_non_dict_int(self, caplog):
        """Log warning and return full defaults when phase_0 is an int."""
        with caplog.at_level(logging.WARNING, logger="agentic_devtools.config"):
            result = _validate_phase_0(42)

        assert result["enabled"] is False
        warnings = [r for r in caplog.records if r.levelno == logging.WARNING]
        assert len(warnings) == 1
        assert "int" in warnings[0].message

    def test_null_returns_defaults_without_warning(self, caplog):
        """phase_0: null returns full defaults without logging any warning."""
        with caplog.at_level(logging.WARNING, logger="agentic_devtools.config"):
            result = _validate_phase_0(None)

        assert result["enabled"] is False
        assert result["sync_back_on_merge"] is False
        assert result["sync_back_fields"] == ["comment"]
        warnings = [r for r in caplog.records if r.levelno == logging.WARNING]
        assert len(warnings) == 0

    def test_preserves_unknown_keys(self):
        """Unknown keys within phase_0 dict are preserved in returned value."""
        raw = {"enabled": True, "future_flag": "experiment", "priority": 5}

        result = _validate_phase_0(raw)

        assert result["future_flag"] == "experiment"
        assert result["priority"] == 5
        assert result["enabled"] is True

    def test_sync_back_fields_is_fresh_list_copy(self):
        """Returned sync_back_fields is a fresh mutable list copy per call."""
        result1 = _validate_phase_0(None)
        result2 = _validate_phase_0(None)

        assert result1["sync_back_fields"] == result2["sync_back_fields"]
        assert result1["sync_back_fields"] is not result2["sync_back_fields"]

    def test_explicit_sync_back_fields_is_copied(self):
        """Returned sync_back_fields is a copy, not the same list object as input."""
        original = ["comment", "status"]
        raw = {"sync_back_fields": original}

        result = _validate_phase_0(raw)

        assert result["sync_back_fields"] == original
        assert result["sync_back_fields"] is not original

    def test_empty_sync_back_fields_list_preserved(self):
        """An explicitly empty sync_back_fields list is preserved as-is."""
        result = _validate_phase_0({"sync_back_fields": [], "enabled": True, "sync_back_on_merge": True})

        assert result["sync_back_fields"] == []

    # --- US1: Default sync-back behavior tests ---

    def test_explicit_null_sync_back_fields_defaults_to_comment(self):
        """Explicit None for sync_back_fields defaults to ['comment'] with no warning."""
        result = _validate_phase_0({"enabled": True, "sync_back_on_merge": True, "sync_back_fields": None})

        assert result["sync_back_fields"] == ["comment"]

    def test_explicit_null_sync_back_fields_no_warning(self, caplog):
        """Explicit None for sync_back_fields emits no warning."""
        with caplog.at_level(logging.WARNING, logger="agentic_devtools.config"):
            _validate_phase_0({"enabled": True, "sync_back_on_merge": True, "sync_back_fields": None})

        warnings = [r for r in caplog.records if r.levelno == logging.WARNING]
        assert len(warnings) == 0

    def test_absent_sync_back_fields_with_both_gates_true_defaults(self):
        """Absent sync_back_fields key with both gates true resolves to ['comment']."""
        result = _validate_phase_0({"enabled": True, "sync_back_on_merge": True})

        assert result["sync_back_fields"] == ["comment"]

    def test_sync_back_on_merge_false_skips_validation(self):
        """sync_back_on_merge: false skips unknown-field rejection."""
        # "assignee" is unknown but should NOT raise because gate is false.
        result = _validate_phase_0({"enabled": True, "sync_back_on_merge": False, "sync_back_fields": ["assignee"]})

        assert result["sync_back_fields"] == ["assignee"]

    def test_enabled_false_skips_unknown_field_rejection(self):
        """enabled: false with sync_back_on_merge: true skips unknown-field rejection."""
        result = _validate_phase_0({"enabled": False, "sync_back_on_merge": True, "sync_back_fields": ["assignee"]})

        assert result["sync_back_fields"] == ["assignee"]

    def test_entire_phase_0_absent_resolves_to_safe_defaults(self):
        """Entire phase_0 section absent (None) resolves to safe disabled defaults."""
        result = _validate_phase_0(None)

        assert result["enabled"] is False
        assert result["sync_back_on_merge"] is False
        assert result["sync_back_fields"] == ["comment"]

    # --- US3: Unknown field rejection tests ---

    def test_unknown_field_raises_valueerror(self):
        """Unknown field raises ValueError naming the field and listing valid options."""
        with pytest.raises(ValueError, match=r'"assignee"') as exc_info:
            _validate_phase_0(
                {
                    "enabled": True,
                    "sync_back_on_merge": True,
                    "sync_back_fields": ["comment", "assignee"],
                }
            )

        assert "comment, label, status" in str(exc_info.value)

    def test_typo_field_raises_valueerror(self):
        """Typo field 'comments' raises ValueError."""
        with pytest.raises(ValueError, match=r'"comments"'):
            _validate_phase_0({"enabled": True, "sync_back_on_merge": True, "sync_back_fields": ["comments"]})

    def test_wrong_case_comment_raises_valueerror(self):
        """Wrong case 'Comment' raises ValueError — case-sensitive, no folding."""
        with pytest.raises(ValueError, match=r'"Comment"'):
            _validate_phase_0({"enabled": True, "sync_back_on_merge": True, "sync_back_fields": ["Comment"]})

    def test_wrong_case_status_raises_valueerror(self):
        """Wrong case 'STATUS' raises ValueError — case-sensitive, no folding."""
        with pytest.raises(ValueError, match=r'"STATUS"'):
            _validate_phase_0({"enabled": True, "sync_back_on_merge": True, "sync_back_fields": ["STATUS"]})

    def test_multiple_unknown_fields_all_named(self):
        """Multiple unknown fields all named in ValueError message."""
        with pytest.raises(ValueError) as exc_info:
            _validate_phase_0(
                {
                    "enabled": True,
                    "sync_back_on_merge": True,
                    "sync_back_fields": ["comment", "assignee", "label", "foo"],
                }
            )

        msg = str(exc_info.value)
        assert '"assignee"' in msg
        assert '"foo"' in msg
        assert "comment, label, status" in msg

    def test_unknown_field_with_special_chars_is_json_escaped(self):
        """Unknown field values are JSON-escaped in ValueError messages."""
        with pytest.raises(ValueError) as exc_info:
            _validate_phase_0(
                {
                    "enabled": True,
                    "sync_back_on_merge": True,
                    "sync_back_fields": ['bad"value\nfield'],
                }
            )

        msg = str(exc_info.value)
        assert '"bad\\"value\\nfield"' in msg
        assert "comment, label, status" in msg

    def test_empty_string_treated_as_unknown(self):
        """Empty string in sync_back_fields treated as unknown field."""
        with pytest.raises(ValueError, match=r'""'):
            _validate_phase_0({"enabled": True, "sync_back_on_merge": True, "sync_back_fields": [""]})

    def test_whitespace_string_treated_as_unknown(self):
        """Whitespace-only string in sync_back_fields treated as unknown field."""
        with pytest.raises(ValueError, match=r'"  "'):
            _validate_phase_0({"enabled": True, "sync_back_on_merge": True, "sync_back_fields": ["  "]})

    def test_duplicates_silently_deduplicated(self):
        """Duplicate entries silently deduplicated preserving order."""
        result = _validate_phase_0(
            {
                "enabled": True,
                "sync_back_on_merge": True,
                "sync_back_fields": ["comment", "comment"],
            }
        )

        assert result["sync_back_fields"] == ["comment"]

    def test_non_list_type_warns_and_defaults(self, caplog):
        """Non-list type for sync_back_fields warns and defaults regardless of gates."""
        with caplog.at_level(logging.WARNING, logger="agentic_devtools.config"):
            result = _validate_phase_0({"enabled": True, "sync_back_on_merge": True, "sync_back_fields": 42})

        assert result["sync_back_fields"] == ["comment"]
        warnings = [r for r in caplog.records if r.levelno == logging.WARNING]
        assert len(warnings) == 1

    def test_list_with_non_string_warns_and_defaults(self, caplog):
        """List with non-string elements warns and defaults."""
        with caplog.at_level(logging.WARNING, logger="agentic_devtools.config"):
            result = _validate_phase_0(
                {
                    "enabled": True,
                    "sync_back_on_merge": True,
                    "sync_back_fields": [1, True, "comment"],
                }
            )

        assert result["sync_back_fields"] == ["comment"]
        warnings = [r for r in caplog.records if r.levelno == logging.WARNING]
        assert len(warnings) == 1

    def test_unknown_fields_with_enabled_false_no_error(self):
        """Unknown fields with enabled: false do NOT raise ValueError."""
        result = _validate_phase_0({"enabled": False, "sync_back_on_merge": True, "sync_back_fields": ["assignee"]})

        assert result["sync_back_fields"] == ["assignee"]

    def test_unknown_fields_with_sync_back_on_merge_false_no_error(self):
        """Unknown fields with sync_back_on_merge: false do NOT raise ValueError."""
        result = _validate_phase_0({"enabled": True, "sync_back_on_merge": False, "sync_back_fields": ["assignee"]})

        assert result["sync_back_fields"] == ["assignee"]

    # --- US2: Opt-in to label and status tests ---

    def test_empty_list_accepted_with_both_gates_true(self):
        """Empty list accepted without error when both gates true."""
        result = _validate_phase_0({"enabled": True, "sync_back_on_merge": True, "sync_back_fields": []})

        assert result["sync_back_fields"] == []

    def test_all_three_valid_fields_accepted(self):
        """All three valid fields accepted with both gates true."""
        result = _validate_phase_0(
            {
                "enabled": True,
                "sync_back_on_merge": True,
                "sync_back_fields": ["comment", "label", "status"],
            }
        )

        assert result["sync_back_fields"] == ["comment", "label", "status"]

    def test_label_alone_accepted(self):
        """'label' alone accepted — 'comment' NOT implicitly added."""
        result = _validate_phase_0({"enabled": True, "sync_back_on_merge": True, "sync_back_fields": ["label"]})

        assert result["sync_back_fields"] == ["label"]

    def test_user_specified_order_preserved(self):
        """User-specified order is preserved."""
        result = _validate_phase_0(
            {
                "enabled": True,
                "sync_back_on_merge": True,
                "sync_back_fields": ["status", "comment"],
            }
        )

        assert result["sync_back_fields"] == ["status", "comment"]
