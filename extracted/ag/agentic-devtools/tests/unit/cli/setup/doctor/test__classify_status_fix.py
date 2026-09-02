"""Tests for _classify_status with fix kwarg — managed CLI and ca-bundle branches."""

from __future__ import annotations

from agentic_devtools.cli.setup.dependency_checker import DependencyStatus
from agentic_devtools.cli.setup.doctor import _classify_status
from agentic_devtools.cli.setup.fixloop import ErrorClass


class TestClassifyStatusFixMode:
    """_classify_status with fix=True classifies managed CLIs as MANAGED_CLI_MISSING."""

    def test_gh_missing_fix_true_returns_managed_cli_missing(self) -> None:
        """fix=True + gh missing + optional → MANAGED_CLI_MISSING."""
        dep = DependencyStatus(name="gh", found=False, required=False)
        assert _classify_status(dep, fix=True) == ErrorClass.MANAGED_CLI_MISSING

    def test_copilot_missing_fix_true_returns_managed_cli_missing(self) -> None:
        """fix=True + copilot missing + optional → MANAGED_CLI_MISSING."""
        dep = DependencyStatus(name="copilot", found=False, required=False)
        assert _classify_status(dep, fix=True) == ErrorClass.MANAGED_CLI_MISSING

    def test_gh_missing_fix_false_returns_none(self) -> None:
        """fix=False + gh missing + optional → None (not a problem in check-only)."""
        dep = DependencyStatus(name="gh", found=False, required=False)
        assert _classify_status(dep, fix=False) is None

    def test_copilot_missing_fix_false_returns_none(self) -> None:
        """fix=False + copilot missing + optional → None."""
        dep = DependencyStatus(name="copilot", found=False, required=False)
        assert _classify_status(dep, fix=False) is None

    def test_gh_found_fix_true_returns_none(self) -> None:
        """fix=True + gh found → None (already present)."""
        dep = DependencyStatus(name="gh", found=True, required=False)
        assert _classify_status(dep, fix=True) is None

    def test_copilot_found_fix_true_returns_none(self) -> None:
        """fix=True + copilot found → None."""
        dep = DependencyStatus(name="copilot", found=True, required=False)
        assert _classify_status(dep, fix=True) is None

    def test_other_optional_missing_fix_true_returns_none(self) -> None:
        """fix=True + non-managed optional CLI missing → None."""
        dep = DependencyStatus(name="node", found=False, required=False)
        assert _classify_status(dep, fix=True) is None


class TestClassifyStatusCaBundle:
    """_classify_status classifies ca-bundle as CERT_CA_FETCH regardless of fix."""

    def test_ca_bundle_missing_fix_false(self) -> None:
        """ca-bundle missing → CERT_CA_FETCH regardless of fix flag."""
        dep = DependencyStatus(name="ca-bundle", found=False, required=True)
        assert _classify_status(dep, fix=False) == ErrorClass.CERT_CA_FETCH

    def test_ca_bundle_missing_fix_true(self) -> None:
        """ca-bundle missing → CERT_CA_FETCH with fix=True."""
        dep = DependencyStatus(name="ca-bundle", found=False, required=True)
        assert _classify_status(dep, fix=True) == ErrorClass.CERT_CA_FETCH

    def test_ca_bundle_found_returns_none(self) -> None:
        """ca-bundle found → None (no problem)."""
        dep = DependencyStatus(name="ca-bundle", found=True, required=True)
        assert _classify_status(dep, fix=True) is None

    def test_ca_bundle_missing_not_required_still_classified(self) -> None:
        """ca-bundle missing even when required=False → CERT_CA_FETCH (name match)."""
        dep = DependencyStatus(name="ca-bundle", found=False, required=False)
        assert _classify_status(dep) == ErrorClass.CERT_CA_FETCH


class TestClassifyStatusDefaultFixKwarg:
    """_classify_status defaults fix=False for backward compatibility."""

    def test_default_fix_is_false(self) -> None:
        """Calling without fix kwarg uses fix=False (no managed CLI classification)."""
        dep = DependencyStatus(name="gh", found=False, required=False)
        assert _classify_status(dep) is None

    def test_git_required_missing_still_classified(self) -> None:
        """Required dep 'git' missing → MISSING_DEPENDENCY regardless of fix."""
        dep = DependencyStatus(name="git", found=False, required=True)
        assert _classify_status(dep) == ErrorClass.MISSING_DEPENDENCY

    def test_git_required_missing_with_fix_true(self) -> None:
        """Required non-managed dep missing with fix=True → MISSING_DEPENDENCY."""
        dep = DependencyStatus(name="git", found=False, required=True)
        assert _classify_status(dep, fix=True) == ErrorClass.MISSING_DEPENDENCY
