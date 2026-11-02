"""Tests for _seed_commit_issue_type_defaults."""

from agentic_devtools.cli.config.commit_type_resolution import STANDARD_COMMIT_TYPES
from agentic_devtools.cli.setup import commands


class TestSeedCommitIssueTypeDefaults:
    """Verify commit-issue defaults are seeded idempotently."""

    def test_adds_defaults_when_both_key_forms_are_missing(self) -> None:
        """Missing commit-type keys are populated with canonical defaults."""
        config = {"jira_project_keys": "ACME"}

        result = commands._seed_commit_issue_type_defaults(config)

        assert result is config
        assert config["defaultCommitIssueType"] == "feat"
        assert config["availableCommitIssueTypes"] == list(STANDARD_COMMIT_TYPES)

    def test_does_not_overwrite_existing_canonical_values(self) -> None:
        """Existing canonical values are preserved."""
        config = {
            "defaultCommitIssueType": "fix",
            "availableCommitIssueTypes": ["fix", "chore"],
        }

        commands._seed_commit_issue_type_defaults(config)

        assert config["defaultCommitIssueType"] == "fix"
        assert config["availableCommitIssueTypes"] == ["fix", "chore"]

    def test_does_not_add_canonical_keys_when_aliases_exist(self) -> None:
        """Alias keys suppress canonical default insertion."""
        config = {
            "default_commit_issue_type": "perf",
            "available_commit_issue_types": ["perf"],
        }

        commands._seed_commit_issue_type_defaults(config)

        assert "defaultCommitIssueType" not in config
        assert "availableCommitIssueTypes" not in config
