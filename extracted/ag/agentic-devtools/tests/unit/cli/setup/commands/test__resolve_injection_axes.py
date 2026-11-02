"""Tests for _resolve_injection_axes."""

from __future__ import annotations

from agentic_devtools.cli.setup.commands import _resolve_injection_axes


class TestResolveInjectionAxes:
    """Tests for _resolve_injection_axes."""

    def test_skip_platform_detection_returns_none_none(self) -> None:
        """--skip-platform-detection → (None, None) inject-all regardless of explicit axes."""
        assert _resolve_injection_axes(
            "github",
            "github",
            skip_platform_detection=True,
            detection_failed=False,
            is_interactive=True,
        ) == (None, None)

    def test_detection_failed_returns_none_none(self) -> None:
        """Detection raises → (None, None) inject-all."""
        assert _resolve_injection_axes(
            "github",
            "github",
            skip_platform_detection=False,
            detection_failed=True,
            is_interactive=True,
        ) == (None, None)

    def test_no_tty_returns_none_none(self) -> None:
        """Non-interactive (no TTY) → (None, None) inject-all."""
        assert _resolve_injection_axes(
            "jira",
            "azure_devops",
            skip_platform_detection=False,
            detection_failed=False,
            is_interactive=False,
        ) == (None, None)

    def test_filter_capable_both_axes(self) -> None:
        """A resolved github/github pair resolves both axes."""
        assert _resolve_injection_axes(
            "github",
            "github",
            skip_platform_detection=False,
            detection_failed=False,
            is_interactive=True,
        ) == ("github", "github")

    def test_jira_azure_devops(self) -> None:
        """A resolved jira/azure_devops pair resolves both axes."""
        assert _resolve_injection_axes(
            "jira",
            "azure_devops",
            skip_platform_detection=False,
            detection_failed=False,
            is_interactive=True,
        ) == ("jira", "azure_devops")

    def test_non_filter_capable_defaults_unrestricted(self) -> None:
        """Non-filter-capable catch-all values (markdown/other) → (None, None)."""
        assert _resolve_injection_axes(
            "markdown",
            "other",
            skip_platform_detection=False,
            detection_failed=False,
            is_interactive=True,
        ) == (None, None)

    def test_partial_axis_resolution(self) -> None:
        """Only the filter-capable axis resolves; the catch-all axis stays None."""
        assert _resolve_injection_axes(
            "jira",
            "other",
            skip_platform_detection=False,
            detection_failed=False,
            is_interactive=True,
        ) == ("jira", None)

    def test_none_none_returns_none_none(self) -> None:
        """Both explicit axes None (nothing detected/overridden) → (None, None) inject-all."""
        assert _resolve_injection_axes(
            None,
            None,
            skip_platform_detection=False,
            detection_failed=False,
            is_interactive=True,
        ) == (None, None)

    def test_issue_adapter_override_with_undetected_hosting(self) -> None:
        """Explicit issue adapter with no detected hosting → code_hosting=None."""
        assert _resolve_injection_axes(
            "github",
            None,
            skip_platform_detection=False,
            detection_failed=False,
            is_interactive=True,
        ) == ("github", None)

    def test_skip_with_preexisting_axes_still_returns_none_none(self) -> None:
        """--skip-platform-detection + genuine explicit axes → unconditionally (None, None)."""
        assert _resolve_injection_axes(
            "jira",
            "github",
            skip_platform_detection=True,
            detection_failed=False,
            is_interactive=True,
        ) == (None, None)

    def test_code_hosting_other_coerced_to_none(self) -> None:
        """Explicit code_hosting='other' → None for injection (not filter-capable)."""
        assert _resolve_injection_axes(
            "github",
            "other",
            skip_platform_detection=False,
            detection_failed=False,
            is_interactive=True,
        ) == ("github", None)

    def test_warning_suppressed_when_inject_all(self) -> None:
        """When both axes are None (inject-all), no warning scenario — both None."""
        result = _resolve_injection_axes(
            None,
            None,
            skip_platform_detection=True,
            detection_failed=False,
            is_interactive=True,
        )
        assert result == (None, None)
