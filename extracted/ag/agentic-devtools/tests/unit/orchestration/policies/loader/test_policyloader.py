"""Tests for PolicyLoader."""

from __future__ import annotations

from pathlib import Path
from unittest.mock import patch

import pytest

from agentic_devtools.orchestration.policies.config import PolicyConfig
from agentic_devtools.orchestration.policies.defaults import (
    DEFAULT_BLOCKED_AFTER_MINUTES,
    DEFAULT_CONFIDENCE_MINIMUM,
    DEFAULT_COVERAGE_THRESHOLD,
    DEFAULT_ESCALATION_TRIGGERS,
    DEFAULT_MAX_HIGH_SEVERITY,
    DEFAULT_MAX_MEDIUM_SEVERITY,
    DEFAULT_MAX_TOKENS,
    DEFAULT_MAX_WALL_CLOCK_MINUTES,
    DEFAULT_RETRY_BUDGET,
)
from agentic_devtools.orchestration.policies.exceptions import PolicyValidationError
from agentic_devtools.orchestration.policies.loader import PolicyLoader


@pytest.fixture()
def loader() -> PolicyLoader:
    return PolicyLoader()


@pytest.fixture()
def tmp_repo(tmp_path: Path) -> Path:
    """Create a temporary 'repo' with .agdt/config/ directory."""
    config_dir = tmp_path / ".agdt" / "config"
    config_dir.mkdir(parents=True)
    return tmp_path


class TestPolicyLoaderDefaults:
    """Test default behavior when no config file exists."""

    def test_absent_file_returns_defaults(self, loader: PolicyLoader, tmp_repo: Path) -> None:
        with patch("agentic_devtools.orchestration.policies.loader._get_git_repo_root", return_value=tmp_repo):
            config = loader.load()
        assert config.pr_review.max_high_severity == DEFAULT_MAX_HIGH_SEVERITY
        assert config.pr_review.max_medium_severity == DEFAULT_MAX_MEDIUM_SEVERITY
        assert config.pr_review.confidence_minimum == DEFAULT_CONFIDENCE_MINIMUM
        assert config.pr_review.escalation_triggers == DEFAULT_ESCALATION_TRIGGERS
        assert config.work_on_issue.retry_budget == DEFAULT_RETRY_BUDGET
        assert config.work_on_issue.blocked_after_minutes == DEFAULT_BLOCKED_AFTER_MINUTES
        assert config.work_on_issue.coverage_threshold == DEFAULT_COVERAGE_THRESHOLD
        assert config.shared.max_tokens == DEFAULT_MAX_TOKENS
        assert config.shared.max_wall_clock_minutes == DEFAULT_MAX_WALL_CLOCK_MINUTES

    def test_empty_file_returns_defaults(self, loader: PolicyLoader, tmp_repo: Path) -> None:
        config_file = tmp_repo / ".agdt" / "config" / "autonomy-policies.yml"
        config_file.write_text("")
        with patch("agentic_devtools.orchestration.policies.loader._get_git_repo_root", return_value=tmp_repo):
            config = loader.load()
        assert config.pr_review.max_high_severity == DEFAULT_MAX_HIGH_SEVERITY

    def test_whitespace_only_file_returns_defaults(self, loader: PolicyLoader, tmp_repo: Path) -> None:
        config_file = tmp_repo / ".agdt" / "config" / "autonomy-policies.yml"
        config_file.write_text("   \n\n   ")
        with patch("agentic_devtools.orchestration.policies.loader._get_git_repo_root", return_value=tmp_repo):
            config = loader.load()
        assert isinstance(config, PolicyConfig)

    def test_comments_only_file_returns_defaults(self, loader: PolicyLoader, tmp_repo: Path) -> None:
        config_file = tmp_repo / ".agdt" / "config" / "autonomy-policies.yml"
        config_file.write_text("# just a comment\n# another comment\n")
        with patch("agentic_devtools.orchestration.policies.loader._get_git_repo_root", return_value=tmp_repo):
            config = loader.load()
        assert isinstance(config, PolicyConfig)


class TestPolicyLoaderOverrides:
    """Test partial override merging."""

    def test_partial_override_merges(self, loader: PolicyLoader, tmp_repo: Path) -> None:
        config_file = tmp_repo / ".agdt" / "config" / "autonomy-policies.yml"
        config_file.write_text("pr_review:\n  approval_threshold:\n    max_high_severity: 1\n")
        with patch("agentic_devtools.orchestration.policies.loader._get_git_repo_root", return_value=tmp_repo):
            config = loader.load()
        assert config.pr_review.max_high_severity == 1
        assert config.pr_review.max_medium_severity == DEFAULT_MAX_MEDIUM_SEVERITY
        assert config.work_on_issue.retry_budget == DEFAULT_RETRY_BUDGET

    def test_unknown_keys_ignored(self, loader: PolicyLoader, tmp_repo: Path) -> None:
        config_file = tmp_repo / ".agdt" / "config" / "autonomy-policies.yml"
        config_file.write_text(
            "pr_review:\n"
            "  approval_threshold:\n"
            "    max_hgh_severity: 1\n"
            "    unknown_nested: true\n"
            "unknown_top_level: 42\n"
        )
        with patch("agentic_devtools.orchestration.policies.loader._get_git_repo_root", return_value=tmp_repo):
            config = loader.load()
        assert config.pr_review.max_high_severity == DEFAULT_MAX_HIGH_SEVERITY

    def test_escalation_triggers_list_to_tuple(self, loader: PolicyLoader, tmp_repo: Path) -> None:
        config_file = tmp_repo / ".agdt" / "config" / "autonomy-policies.yml"
        config_file.write_text(
            "pr_review:\n  escalation_triggers:\n    - security vulnerability\n    - breaking change\n"
        )
        with patch("agentic_devtools.orchestration.policies.loader._get_git_repo_root", return_value=tmp_repo):
            config = loader.load()
        assert config.pr_review.escalation_triggers == ("security vulnerability", "breaking change")
        assert isinstance(config.pr_review.escalation_triggers, tuple)


class TestPolicyLoaderValidation:
    """Test validation errors for invalid values."""

    def test_negative_retry_budget_raises(self, loader: PolicyLoader, tmp_repo: Path) -> None:
        config_file = tmp_repo / ".agdt" / "config" / "autonomy-policies.yml"
        config_file.write_text("work_on_issue:\n  retry_budget: -5\n")
        with patch("agentic_devtools.orchestration.policies.loader._get_git_repo_root", return_value=tmp_repo):
            with pytest.raises(PolicyValidationError) as exc_info:
                loader.load()
        assert "work_on_issue.retry_budget" in exc_info.value.field_path

    def test_confidence_above_1_raises(self, loader: PolicyLoader, tmp_repo: Path) -> None:
        config_file = tmp_repo / ".agdt" / "config" / "autonomy-policies.yml"
        config_file.write_text("pr_review:\n  confidence_minimum: 1.5\n")
        with patch("agentic_devtools.orchestration.policies.loader._get_git_repo_root", return_value=tmp_repo):
            with pytest.raises(PolicyValidationError) as exc_info:
                loader.load()
        assert "confidence_minimum" in exc_info.value.field_path

    def test_confidence_below_0_raises(self, loader: PolicyLoader, tmp_repo: Path) -> None:
        config_file = tmp_repo / ".agdt" / "config" / "autonomy-policies.yml"
        config_file.write_text("pr_review:\n  confidence_minimum: -0.1\n")
        with patch("agentic_devtools.orchestration.policies.loader._get_git_repo_root", return_value=tmp_repo):
            with pytest.raises(PolicyValidationError):
                loader.load()

    def test_confidence_nan_raises(self, loader: PolicyLoader, tmp_repo: Path) -> None:
        config_file = tmp_repo / ".agdt" / "config" / "autonomy-policies.yml"
        config_file.write_text("pr_review:\n  confidence_minimum: !!float .nan\n")
        with patch("agentic_devtools.orchestration.policies.loader._get_git_repo_root", return_value=tmp_repo):
            with pytest.raises(PolicyValidationError) as exc_info:
                loader.load()
        assert exc_info.value.field_path == "pr_review.confidence_minimum"

    def test_wrong_type_raises(self, loader: PolicyLoader, tmp_repo: Path) -> None:
        config_file = tmp_repo / ".agdt" / "config" / "autonomy-policies.yml"
        config_file.write_text("work_on_issue:\n  retry_budget: not_a_number\n")
        with patch("agentic_devtools.orchestration.policies.loader._get_git_repo_root", return_value=tmp_repo):
            with pytest.raises(PolicyValidationError):
                loader.load()

    def test_yaml_syntax_error_raises(self, loader: PolicyLoader, tmp_repo: Path) -> None:
        config_file = tmp_repo / ".agdt" / "config" / "autonomy-policies.yml"
        config_file.write_text("invalid: yaml: content: [unclosed")
        with patch("agentic_devtools.orchestration.policies.loader._get_git_repo_root", return_value=tmp_repo):
            with pytest.raises(PolicyValidationError) as exc_info:
                loader.load()
        assert "YAML syntax error" in exc_info.value.constraint

    def test_git_root_none_raises(self, loader: PolicyLoader) -> None:
        with patch("agentic_devtools.orchestration.policies.loader._get_git_repo_root", return_value=None):
            with pytest.raises(PolicyValidationError) as exc_info:
                loader.load()
        assert "Repository root resolution failed" in exc_info.value.constraint

    def test_boolean_value_for_int_field_raises(self, loader: PolicyLoader, tmp_repo: Path) -> None:
        config_file = tmp_repo / ".agdt" / "config" / "autonomy-policies.yml"
        config_file.write_text("work_on_issue:\n  retry_budget: true\n")
        with patch("agentic_devtools.orchestration.policies.loader._get_git_repo_root", return_value=tmp_repo):
            with pytest.raises(PolicyValidationError):
                loader.load()

    def test_escalation_triggers_not_list_raises(self, loader: PolicyLoader, tmp_repo: Path) -> None:
        config_file = tmp_repo / ".agdt" / "config" / "autonomy-policies.yml"
        config_file.write_text("pr_review:\n  escalation_triggers: not_a_list\n")
        with patch("agentic_devtools.orchestration.policies.loader._get_git_repo_root", return_value=tmp_repo):
            with pytest.raises(PolicyValidationError):
                loader.load()

    def test_escalation_triggers_non_string_item_raises(self, loader: PolicyLoader, tmp_repo: Path) -> None:
        config_file = tmp_repo / ".agdt" / "config" / "autonomy-policies.yml"
        config_file.write_text("pr_review:\n  escalation_triggers:\n    - security\n    - 123\n")
        with patch("agentic_devtools.orchestration.policies.loader._get_git_repo_root", return_value=tmp_repo):
            with pytest.raises(PolicyValidationError) as exc_info:
                loader.load()
        assert "list of strings" in exc_info.value.constraint

    def test_escalation_triggers_whitespace_only_item_raises(self, loader: PolicyLoader, tmp_repo: Path) -> None:
        config_file = tmp_repo / ".agdt" / "config" / "autonomy-policies.yml"
        config_file.write_text("pr_review:\n  escalation_triggers:\n    - security\n    - '   '\n")
        with patch("agentic_devtools.orchestration.policies.loader._get_git_repo_root", return_value=tmp_repo):
            with pytest.raises(PolicyValidationError) as exc_info:
                loader.load()
        assert "non-whitespace" in exc_info.value.constraint

    def test_boolean_for_confidence_raises(self, loader: PolicyLoader, tmp_repo: Path) -> None:
        config_file = tmp_repo / ".agdt" / "config" / "autonomy-policies.yml"
        config_file.write_text("pr_review:\n  confidence_minimum: true\n")
        with patch("agentic_devtools.orchestration.policies.loader._get_git_repo_root", return_value=tmp_repo):
            with pytest.raises(PolicyValidationError):
                loader.load()

    def test_negative_max_tokens_raises(self, loader: PolicyLoader, tmp_repo: Path) -> None:
        config_file = tmp_repo / ".agdt" / "config" / "autonomy-policies.yml"
        config_file.write_text("shared:\n  max_tokens: -100\n")
        with patch("agentic_devtools.orchestration.policies.loader._get_git_repo_root", return_value=tmp_repo):
            with pytest.raises(PolicyValidationError):
                loader.load()

    def test_float_non_integer_for_int_field_raises(self, loader: PolicyLoader, tmp_repo: Path) -> None:
        """A float with a fractional part (e.g. 3.7) is rejected, not silently truncated."""
        config_file = tmp_repo / ".agdt" / "config" / "autonomy-policies.yml"
        config_file.write_text("work_on_issue:\n  retry_budget: 3.7\n")
        with patch("agentic_devtools.orchestration.policies.loader._get_git_repo_root", return_value=tmp_repo):
            with pytest.raises(PolicyValidationError) as exc_info:
                loader.load()
        assert "whole number" in exc_info.value.constraint

    def test_float_whole_number_for_int_field_accepted(self, loader: PolicyLoader, tmp_repo: Path) -> None:
        """A float that is a whole number (e.g. 3.0) is accepted."""
        config_file = tmp_repo / ".agdt" / "config" / "autonomy-policies.yml"
        config_file.write_text("work_on_issue:\n  retry_budget: 3.0\n")
        with patch("agentic_devtools.orchestration.policies.loader._get_git_repo_root", return_value=tmp_repo):
            config = loader.load()
        assert config.work_on_issue.retry_budget == 3

    def test_non_dict_section_treated_as_empty(self, loader: PolicyLoader, tmp_repo: Path) -> None:
        config_file = tmp_repo / ".agdt" / "config" / "autonomy-policies.yml"
        config_file.write_text("pr_review: not_a_dict\nwork_on_issue: 42\nshared: true\n")
        with patch("agentic_devtools.orchestration.policies.loader._get_git_repo_root", return_value=tmp_repo):
            config = loader.load()
        assert isinstance(config, PolicyConfig)

    def test_non_dict_approval_threshold_treated_as_empty(self, loader: PolicyLoader, tmp_repo: Path) -> None:
        config_file = tmp_repo / ".agdt" / "config" / "autonomy-policies.yml"
        config_file.write_text("pr_review:\n  approval_threshold: not_a_dict\n")
        with patch("agentic_devtools.orchestration.policies.loader._get_git_repo_root", return_value=tmp_repo):
            config = loader.load()
        assert config.pr_review.max_high_severity == 0


class TestPolicyLoaderFullOverrides:
    """Test full overrides for all sections to ensure code paths are covered."""

    def test_work_on_issue_all_fields(self, loader: PolicyLoader, tmp_repo: Path) -> None:
        config_file = tmp_repo / ".agdt" / "config" / "autonomy-policies.yml"
        config_file.write_text(
            "work_on_issue:\n  retry_budget: 5\n  blocked_after_minutes: 45\n  coverage_threshold: 80\n"
        )
        with patch("agentic_devtools.orchestration.policies.loader._get_git_repo_root", return_value=tmp_repo):
            config = loader.load()
        assert config.work_on_issue.retry_budget == 5
        assert config.work_on_issue.blocked_after_minutes == 45
        assert config.work_on_issue.coverage_threshold == 80

    def test_shared_all_fields(self, loader: PolicyLoader, tmp_repo: Path) -> None:
        config_file = tmp_repo / ".agdt" / "config" / "autonomy-policies.yml"
        config_file.write_text("shared:\n  max_tokens: 1000000\n  max_wall_clock_minutes: 120\n")
        with patch("agentic_devtools.orchestration.policies.loader._get_git_repo_root", return_value=tmp_repo):
            config = loader.load()
        assert config.shared.max_tokens == 1000000
        assert config.shared.max_wall_clock_minutes == 120

    def test_pr_review_confidence_and_medium(self, loader: PolicyLoader, tmp_repo: Path) -> None:
        config_file = tmp_repo / ".agdt" / "config" / "autonomy-policies.yml"
        config_file.write_text(
            "pr_review:\n  confidence_minimum: 0.8\n  approval_threshold:\n    max_medium_severity: 5\n"
        )
        with patch("agentic_devtools.orchestration.policies.loader._get_git_repo_root", return_value=tmp_repo):
            config = loader.load()
        assert config.pr_review.confidence_minimum == 0.8
        assert config.pr_review.max_medium_severity == 5


class TestNodeRetryBudgets:
    """Tests for node_retry_budgets parsing in work_on_issue section."""

    def test_valid_node_retry_budgets(self, loader: PolicyLoader, tmp_repo: Path) -> None:
        config_file = tmp_repo / ".agdt" / "config" / "autonomy-policies.yml"
        config_file.write_text("work_on_issue:\n  node_retry_budgets:\n    planning: 3\n    implementation: 5\n")
        with patch("agentic_devtools.orchestration.policies.loader._get_git_repo_root", return_value=tmp_repo):
            config = loader.load()
        assert config.work_on_issue.node_retry_budgets == {"planning": 3, "implementation": 5}

    def test_node_retry_budgets_not_a_dict_raises(self, loader: PolicyLoader, tmp_repo: Path) -> None:
        config_file = tmp_repo / ".agdt" / "config" / "autonomy-policies.yml"
        config_file.write_text("work_on_issue:\n  node_retry_budgets: 42\n")
        with patch("agentic_devtools.orchestration.policies.loader._get_git_repo_root", return_value=tmp_repo):
            with pytest.raises(PolicyValidationError) as exc_info:
                loader.load()
        assert "node_retry_budgets" in exc_info.value.field_path
        assert "mapping" in exc_info.value.constraint

    def test_node_retry_budgets_empty_name_raises(self, loader: PolicyLoader, tmp_repo: Path) -> None:
        config_file = tmp_repo / ".agdt" / "config" / "autonomy-policies.yml"
        config_file.write_text("work_on_issue:\n  node_retry_budgets:\n    '': 3\n")
        with patch("agentic_devtools.orchestration.policies.loader._get_git_repo_root", return_value=tmp_repo):
            with pytest.raises(PolicyValidationError) as exc_info:
                loader.load()
        assert "non-empty string" in exc_info.value.constraint

    def test_node_retry_budgets_whitespace_name_raises(self, loader: PolicyLoader, tmp_repo: Path) -> None:
        config_file = tmp_repo / ".agdt" / "config" / "autonomy-policies.yml"
        config_file.write_text("work_on_issue:\n  node_retry_budgets:\n    '   ': 3\n")
        with patch("agentic_devtools.orchestration.policies.loader._get_git_repo_root", return_value=tmp_repo):
            with pytest.raises(PolicyValidationError) as exc_info:
                loader.load()
        assert "non-empty string" in exc_info.value.constraint

    def test_node_retry_budgets_negative_value_raises(self, loader: PolicyLoader, tmp_repo: Path) -> None:
        config_file = tmp_repo / ".agdt" / "config" / "autonomy-policies.yml"
        config_file.write_text("work_on_issue:\n  node_retry_budgets:\n    planning: -1\n")
        with patch("agentic_devtools.orchestration.policies.loader._get_git_repo_root", return_value=tmp_repo):
            with pytest.raises(PolicyValidationError) as exc_info:
                loader.load()
        assert "planning" in exc_info.value.field_path

    def test_node_retry_budgets_zero_is_valid(self, loader: PolicyLoader, tmp_repo: Path) -> None:
        config_file = tmp_repo / ".agdt" / "config" / "autonomy-policies.yml"
        config_file.write_text("work_on_issue:\n  node_retry_budgets:\n    planning: 0\n")
        with patch("agentic_devtools.orchestration.policies.loader._get_git_repo_root", return_value=tmp_repo):
            config = loader.load()
        assert config.work_on_issue.node_retry_budgets == {"planning": 0}

    def test_node_retry_budgets_key_with_surrounding_whitespace_is_normalized(
        self, loader: PolicyLoader, tmp_repo: Path
    ) -> None:
        """Keys with surrounding whitespace are stripped before storing so runtime lookups succeed."""
        config_file = tmp_repo / ".agdt" / "config" / "autonomy-policies.yml"
        # YAML requires quoting to preserve leading/trailing whitespace in a plain scalar key
        config_file.write_text("work_on_issue:\n  node_retry_budgets:\n    '  planning  ': 2\n")
        with patch("agentic_devtools.orchestration.policies.loader._get_git_repo_root", return_value=tmp_repo):
            config = loader.load()
        assert "planning" in config.work_on_issue.node_retry_budgets
        assert "  planning  " not in config.work_on_issue.node_retry_budgets
        assert config.work_on_issue.node_retry_budgets["planning"] == 2

    def test_duplicate_keys_after_normalization_raises(self, loader: PolicyLoader, tmp_repo: Path) -> None:
        """Two keys that differ only by whitespace produce a PolicyValidationError after normalization."""
        config_file = tmp_repo / ".agdt" / "config" / "autonomy-policies.yml"
        # 'planning' and '  planning  ' both normalize to 'planning' — must be detected
        config_file.write_text("work_on_issue:\n  node_retry_budgets:\n    planning: 2\n    '  planning  ': 3\n")
        with patch("agentic_devtools.orchestration.policies.loader._get_git_repo_root", return_value=tmp_repo):
            with pytest.raises(PolicyValidationError) as exc_info:
                loader.load()
        assert "planning" in exc_info.value.field_path
        assert "duplicate" in exc_info.value.constraint
