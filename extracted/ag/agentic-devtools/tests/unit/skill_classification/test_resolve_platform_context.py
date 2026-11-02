"""Tests for resolve_platform_context function."""

from __future__ import annotations

from agentic_devtools.skill_classification import resolve_platform_context


class TestResolvePlatformContextFilterCapable:
    """Confidently-resolved, filter-capable values activate their axis."""

    def test_jira_and_github_both_resolved(self) -> None:
        assert resolve_platform_context({"issue_adapter": "jira", "code_hosting": "github"}) == ("jira", "github")

    def test_github_and_azure_devops_both_resolved(self) -> None:
        assert resolve_platform_context({"issue_adapter": "github", "code_hosting": "azure_devops"}) == (
            "github",
            "azure_devops",
        )

    def test_github_adapter_and_github_hosting(self) -> None:
        assert resolve_platform_context({"issue_adapter": "github", "code_hosting": "github"}) == ("github", "github")


class TestResolvePlatformContextSingleAxis:
    """A single filter-capable axis resolves; the other stays unrestricted."""

    def test_only_issue_adapter_resolved(self) -> None:
        # code_hosting "other" is a non-filter-capable catch-all → None
        assert resolve_platform_context({"issue_adapter": "jira", "code_hosting": "other"}) == ("jira", None)

    def test_only_code_hosting_resolved(self) -> None:
        # issue_adapter "markdown" is a non-filter-capable catch-all → None
        assert resolve_platform_context({"issue_adapter": "markdown", "code_hosting": "github"}) == (None, "github")

    def test_issue_adapter_present_hosting_absent(self) -> None:
        assert resolve_platform_context({"issue_adapter": "github"}) == ("github", None)

    def test_hosting_present_adapter_absent(self) -> None:
        assert resolve_platform_context({"code_hosting": "azure_devops"}) == (None, "azure_devops")


class TestResolvePlatformContextUnrestricted:
    """Non-filter-capable, absent, or malformed inputs leave both axes None."""

    def test_none_platform(self) -> None:
        assert resolve_platform_context(None) == (None, None)

    def test_empty_mapping(self) -> None:
        assert resolve_platform_context({}) == (None, None)

    def test_non_filter_capable_catch_all_values(self) -> None:
        assert resolve_platform_context({"issue_adapter": "markdown", "code_hosting": "other"}) == (None, None)

    def test_non_mapping_string(self) -> None:
        assert resolve_platform_context("not-a-mapping") == (None, None)

    def test_non_mapping_list(self) -> None:
        assert resolve_platform_context(["jira", "github"]) == (None, None)

    def test_non_string_axis_values(self) -> None:
        # A list issue_adapter and int code_hosting are ignored without raising
        assert resolve_platform_context({"issue_adapter": ["jira"], "code_hosting": 123}) == (None, None)

    def test_none_axis_values(self) -> None:
        assert resolve_platform_context({"issue_adapter": None, "code_hosting": None}) == (None, None)

    def test_case_sensitive_values_not_matched(self) -> None:
        # Config values are lowercase; a different casing is not filter-capable
        assert resolve_platform_context({"issue_adapter": "JIRA", "code_hosting": "GitHub"}) == (None, None)

    def test_unknown_values_not_matched(self) -> None:
        assert resolve_platform_context({"issue_adapter": "gitlab", "code_hosting": "bitbucket"}) == (None, None)

    def test_extra_keys_ignored(self) -> None:
        result = resolve_platform_context({"issue_adapter": "jira", "code_hosting": "github", "jira": {"url": "x"}})
        assert result == ("jira", "github")

    def test_does_not_mutate_input(self) -> None:
        platform = {"issue_adapter": "jira", "code_hosting": "github"}
        resolve_platform_context(platform)
        assert platform == {"issue_adapter": "jira", "code_hosting": "github"}
