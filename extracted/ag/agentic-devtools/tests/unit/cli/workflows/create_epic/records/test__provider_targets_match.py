"""Tests for ``_provider_targets_match``."""

from __future__ import annotations

from agentic_devtools.cli.workflows.create_epic.records import _provider_targets_match


class TestProviderTargetsMatch:
    """Jira matching treats only the project key as case-insensitive."""

    def test_matches_jira_project_key_case_insensitively(self) -> None:
        assert _provider_targets_match(
            "jira",
            "https://jira.example.com/JIRA/proj",
            "https://jira.example.com/JIRA/PROJ",
            allow_legacy_site_match=False,
        )

    def test_rejects_jira_context_path_case_difference(self) -> None:
        assert not _provider_targets_match(
            "jira",
            "https://jira.example.com/JIRA/proj",
            "https://jira.example.com/jira/PROJ",
            allow_legacy_site_match=False,
        )

    def test_rejects_jira_context_path_internal_slash_difference(self) -> None:
        assert not _provider_targets_match(
            "jira",
            "https://jira.example.com/team/jira/PROJ",
            "https://jira.example.com/team//jira/PROJ",
            allow_legacy_site_match=False,
        )

    def test_allows_legacy_site_match_only_when_enabled(self) -> None:
        assert _provider_targets_match(
            "jira",
            "https://jira.example.com/jira",
            "https://jira.example.com/jira/PROJ",
            allow_legacy_site_match=True,
        )

    def test_canonicalizes_legacy_site_before_matching_active_target(self) -> None:
        assert _provider_targets_match(
            "jira",
            "HTTPS://JIRA.Example.com:443/",
            "https://jira.example.com/PROJ",
            allow_legacy_site_match=True,
        )

    def test_rejects_invalid_legacy_site_target(self) -> None:
        assert not _provider_targets_match(
            "jira",
            "https://jira.example.com/?filter=recent",
            "https://jira.example.com/PROJ",
            allow_legacy_site_match=True,
        )

    def test_rejects_case_variant_ambiguous_legacy_jira_site_match(self) -> None:
        assert not _provider_targets_match(
            "jira",
            "https://jira.example.com/jira",
            "https://jira.example.com/JIRA",
            allow_legacy_site_match=False,
        )
