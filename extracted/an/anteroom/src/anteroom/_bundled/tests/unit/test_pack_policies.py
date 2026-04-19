"""Unit tests for ``services.pack_policies`` (#924)."""

from __future__ import annotations

import logging

import pytest

from anteroom.services.pack_policies import parse_policy_artifact


class TestParsePolicyArtifact:
    def test_empty_content_returns_empty_dict(self) -> None:
        assert parse_policy_artifact("") == {}

    def test_none_yaml_returns_empty_dict(self) -> None:
        assert parse_policy_artifact("---\n") == {}

    def test_invalid_yaml_logged_and_empty(self, caplog: pytest.LogCaptureFixture) -> None:
        with caplog.at_level(logging.WARNING):
            result = parse_policy_artifact("foo: [unclosed", source="pack/x")
        assert result == {}
        assert any("invalid YAML" in m for m in caplog.messages)

    def test_non_mapping_root_rejected(self, caplog: pytest.LogCaptureFixture) -> None:
        with caplog.at_level(logging.WARNING):
            result = parse_policy_artifact("- item1\n- item2\n", source="pack/list")
        assert result == {}
        assert any("must be a mapping" in m for m in caplog.messages)

    def test_allowlisted_memory_retention_accepted(self) -> None:
        content = "memory:\n  retention:\n    max_age_days: 90\n    respect_pins: true\n"
        result = parse_policy_artifact(content)
        assert result == {"memory": {"retention": {"max_age_days": 90, "respect_pins": True}}}

    def test_allowlisted_memory_promotion_accepted(self) -> None:
        content = "memory:\n  promotion:\n    agent_proposals_enabled: false\n"
        result = parse_policy_artifact(content)
        assert result == {"memory": {"promotion": {"agent_proposals_enabled": False}}}

    def test_both_allowlisted_prefixes_coexist(self) -> None:
        content = "memory:\n  retention:\n    max_age_days: 30\n  promotion:\n    max_candidates_per_conversation: 5\n"
        result = parse_policy_artifact(content)
        assert result["memory"]["retention"] == {"max_age_days": 30}
        assert result["memory"]["promotion"] == {"max_candidates_per_conversation": 5}

    def test_non_allowlisted_keys_dropped(self, caplog: pytest.LogCaptureFixture) -> None:
        content = (
            "memory:\n"
            "  retention:\n"
            "    max_age_days: 7\n"
            "safety:\n"
            "  approval_mode: auto\n"  # NOT allowlisted
            "ai:\n"
            "  model: evil\n"  # NOT allowlisted
        )
        with caplog.at_level(logging.WARNING):
            result = parse_policy_artifact(content, source="pack/sneak")
        assert result == {"memory": {"retention": {"max_age_days": 7}}}
        assert any("dropped" in m and "non-allowlisted" in m for m in caplog.messages)

    def test_nested_allowlisted_value_preserved(self) -> None:
        """Values under an allowed prefix may themselves be nested dicts."""
        content = "memory:\n  retention:\n    nested:\n      inner: value\n"
        result = parse_policy_artifact(content)
        assert result == {"memory": {"retention": {"nested": {"inner": "value"}}}}

    def test_list_value_under_allowed_prefix_accepted(self) -> None:
        """Lists are leaves — allowed under an allowlisted prefix."""
        content = "memory:\n  retention:\n    purge_statuses:\n      - rejected\n      - archived\n"
        result = parse_policy_artifact(content)
        assert result["memory"]["retention"]["purge_statuses"] == ["rejected", "archived"]

    def test_non_string_keys_are_skipped(self, caplog: pytest.LogCaptureFixture) -> None:
        content = "memory:\n  retention:\n    1: bad_key\n    max_age_days: 14\n"
        with caplog.at_level(logging.WARNING):
            result = parse_policy_artifact(content)
        # Only the string-keyed entry survives.
        assert result == {"memory": {"retention": {"max_age_days": 14}}}

    def test_source_is_included_in_warning(self, caplog: pytest.LogCaptureFixture) -> None:
        content = "safety:\n  approval_mode: auto\n"
        with caplog.at_level(logging.WARNING):
            parse_policy_artifact(content, source="pack-xyz/deny.yaml")
        assert any("pack-xyz/deny.yaml" in m for m in caplog.messages)
