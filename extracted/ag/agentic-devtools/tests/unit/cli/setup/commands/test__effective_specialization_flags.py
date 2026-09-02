"""Tests for _effective_specialization_flags."""

from argparse import Namespace

from agentic_devtools.cli.setup import commands


def _full_args(**overrides) -> Namespace:
    """Return a Namespace with all expected attributes set to their defaults."""
    defaults = {
        "system_only": False,
        "no_verify_ssl": False,
        "no_persist_env": False,
        "overwrite_env": False,
        "skip_platform_detection": False,
        "issue_adapter": None,
        "skip_templates": False,
        "reconfigure": False,
        "defaults": False,
        "skip_pr_workflow": False,
        "force_old_version": False,
        "npm": False,
        "no_npm": False,
        "cli_run": None,
        "cli_no_run": None,
        "no_refresh_models": False,
        "refresh_issue_types": False,
        "dry_run": False,
        "yes": False,
        "autorun_enabled": None,
    }
    defaults.update(overrides)
    return Namespace(**defaults)


class TestEffectiveSpecializationFlags:
    """Direct tests for _effective_specialization_flags."""

    def test_all_false_defaults(self) -> None:
        """All boolean flags default to False and string flags default to None/False."""
        result = commands._effective_specialization_flags(_full_args(), npm_enabled=False)
        assert result["--system-only"] is False
        assert result["--no-verify-ssl"] is False
        assert result["--no-persist-env"] is False
        assert result["--overwrite-env"] is False
        assert result["--skip-platform-detection"] is False
        assert result["--issue-adapter"] is None
        assert result["--skip-templates"] is False
        assert result["--reconfigure"] is False
        assert result["--defaults"] is False
        assert result["--skip-pr-workflow"] is False
        assert result["--force-old-version"] is False
        assert result["--npm"] is False
        assert result["--no-npm"] is False
        assert result["--run"] is False
        assert result["--no-run"] is False
        assert result["--no-refresh-models"] is False
        assert result["--refresh-issue-types"] is False
        assert result["--dry-run"] is False
        assert result["--yes"] is False
        assert result["autorun_enabled"] is None
        assert result["npm_enabled"] is False

    def test_boolean_flags_are_reflected(self) -> None:
        """Boolean flag values set on args are reflected in the returned mapping."""
        result = commands._effective_specialization_flags(
            _full_args(system_only=True, dry_run=True, no_refresh_models=True, yes=True),
            npm_enabled=True,
        )
        assert result["--system-only"] is True
        assert result["--dry-run"] is True
        assert result["--no-refresh-models"] is True
        assert result["--yes"] is True
        assert result["npm_enabled"] is True

    def test_issue_adapter_string_is_passed_through(self) -> None:
        """The --issue-adapter string value is passed through as-is."""
        result = commands._effective_specialization_flags(
            _full_args(issue_adapter="jira"),
            npm_enabled=False,
        )
        assert result["--issue-adapter"] == "jira"

    def test_cli_run_true_sets_run_flag(self) -> None:
        """cli_run=True maps to --run: True."""
        result = commands._effective_specialization_flags(
            _full_args(cli_run=True),
            npm_enabled=False,
        )
        assert result["--run"] is True

    def test_cli_run_none_sets_run_false(self) -> None:
        """cli_run=None (default) maps to --run: False."""
        result = commands._effective_specialization_flags(
            _full_args(cli_run=None),
            npm_enabled=False,
        )
        assert result["--run"] is False

    def test_cli_no_run_true_sets_no_run_flag(self) -> None:
        """cli_no_run=True maps to --no-run: True."""
        result = commands._effective_specialization_flags(
            _full_args(cli_no_run=True),
            npm_enabled=False,
        )
        assert result["--no-run"] is True

    def test_autorun_enabled_is_forwarded(self) -> None:
        """autorun_enabled is forwarded verbatim from args."""
        result = commands._effective_specialization_flags(
            _full_args(autorun_enabled=True),
            npm_enabled=False,
        )
        assert result["autorun_enabled"] is True

    def test_missing_attributes_default_to_false_or_none(self) -> None:
        """When an attribute is absent from args, the mapping falls back to False or None."""
        sparse_args = Namespace()
        result = commands._effective_specialization_flags(sparse_args, npm_enabled=False)
        assert result["--system-only"] is False
        assert result["--issue-adapter"] is None
        assert result["autorun_enabled"] is None
