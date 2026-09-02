"""Tests for _classify_status name-based detection."""

from __future__ import annotations

from agentic_devtools.cli.setup.dependency_checker import DependencyStatus
from agentic_devtools.cli.setup.doctor import _classify_status
from agentic_devtools.cli.setup.fixloop import ErrorClass


class TestClassifyStatusNameBased:
    """_classify_status classifies by dep.name for well-known deps."""

    def test_path_profile_classified_as_path_profile_not_updated(self) -> None:
        """dep.name == 'path-profile' → PATH_PROFILE_NOT_UPDATED."""
        dep = DependencyStatus(name="path-profile", found=False, required=True)
        assert _classify_status(dep) == ErrorClass.PATH_PROFILE_NOT_UPDATED

    def test_git_hooks_classified_as_git_hooks_not_configured(self) -> None:
        """dep.name == 'git-hooks' → GIT_HOOKS_NOT_CONFIGURED."""
        dep = DependencyStatus(name="git-hooks", found=False, required=True)
        assert _classify_status(dep) == ErrorClass.GIT_HOOKS_NOT_CONFIGURED

    def test_generic_dep_classified_as_missing_dependency(self) -> None:
        """Other required-but-missing deps → MISSING_DEPENDENCY."""
        dep = DependencyStatus(name="some-tool", found=False, required=True)
        assert _classify_status(dep) == ErrorClass.MISSING_DEPENDENCY

    def test_found_dep_returns_none(self) -> None:
        """Found dependency returns None (no problem)."""
        dep = DependencyStatus(name="path-profile", found=True, required=True)
        assert _classify_status(dep) is None

    def test_optional_missing_returns_none(self) -> None:
        """Optional missing dependency returns None."""
        dep = DependencyStatus(name="git-hooks", found=False, required=False)
        assert _classify_status(dep) is None

    def test_corrupted_install_artifacts_returns_stale_partial_install(self) -> None:
        """dep.name == 'corrupted-install-artifacts' and not found → STALE_PARTIAL_INSTALL."""
        dep = DependencyStatus(name="corrupted-install-artifacts", found=False, required=True)
        assert _classify_status(dep) == ErrorClass.STALE_PARTIAL_INSTALL

    def test_corrupted_install_artifacts_found_returns_none(self) -> None:
        """corrupted-install-artifacts + found=True → None (healthy)."""
        dep = DependencyStatus(name="corrupted-install-artifacts", found=True, required=True)
        assert _classify_status(dep) is None

    def test_corrupted_install_artifacts_takes_precedence_over_missing_dependency(self) -> None:
        """corrupted-install-artifacts returns STALE_PARTIAL_INSTALL, not MISSING_DEPENDENCY."""
        dep = DependencyStatus(name="corrupted-install-artifacts", found=False, required=True)
        result = _classify_status(dep)
        assert result == ErrorClass.STALE_PARTIAL_INSTALL
        assert result != ErrorClass.MISSING_DEPENDENCY
