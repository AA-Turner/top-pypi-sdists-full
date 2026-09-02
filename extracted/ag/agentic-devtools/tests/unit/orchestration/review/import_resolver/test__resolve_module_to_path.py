"""Tests for _resolve_module_to_path function."""

from __future__ import annotations

from agentic_devtools.orchestration.review.import_resolver import _resolve_module_to_path


class TestResolveModuleToPath:
    """Tests for module-to-path resolution."""

    def test_first_party_resolves(self) -> None:
        result = _resolve_module_to_path("agentic_devtools.cli.git.core")
        assert result == "agentic_devtools/cli/git/core.py"

    def test_third_party_returns_none(self) -> None:
        assert _resolve_module_to_path("requests") is None
        assert _resolve_module_to_path("os.path") is None

    def test_package_with_same_prefix_excluded(self) -> None:
        """agentic_devtools_ext is not first-party despite sharing the prefix."""
        assert _resolve_module_to_path("agentic_devtools_ext.foo") is None
        assert _resolve_module_to_path("agentic_devtools_extra") is None

    def test_exact_package_name_resolves(self) -> None:
        """The exact package name 'agentic_devtools' itself resolves."""
        result = _resolve_module_to_path("agentic_devtools")
        assert result == "agentic_devtools.py"
