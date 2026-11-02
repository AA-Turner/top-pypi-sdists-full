"""Tests for ``_build_github_adapter`` in ``agentic_devtools.adapters``."""

from __future__ import annotations

import pytest

from agentic_devtools.adapters import _build_github_adapter

# ---------------------------------------------------------------------------
# US1 — Adapter works with auto-detected ``repo`` slug config
# ---------------------------------------------------------------------------


class TestRepoSlugKey:
    """FR-001: ``github.repo`` slug is used directly."""

    @pytest.mark.parametrize(
        "slug",
        [
            "swai-factory/agentic-devtools",
            "octocat/Hello-World",
            "my-org/my-repo",
        ],
    )
    def test_repo_slug_resolves(self, slug: str) -> None:
        config = {"github": {"repo": slug}}
        adapter = _build_github_adapter(config)
        assert adapter._repo == slug

    def test_repo_slug_stripped(self) -> None:
        """FR-004: whitespace around slug is stripped."""
        config = {"github": {"repo": "  owner/name  "}}
        adapter = _build_github_adapter(config)
        assert adapter._repo == "owner/name"

    def test_repo_slug_takes_precedence(self) -> None:
        """FR-003: slug key wins over split keys silently."""
        config = {
            "github": {
                "repo": "slug-owner/slug-repo",
                "repo_owner": "legacy-owner",
                "repo_name": "legacy-repo",
            },
        }
        adapter = _build_github_adapter(config)
        assert adapter._repo == "slug-owner/slug-repo"

    def test_whitespace_only_repo_falls_back(self) -> None:
        """FR-002: whitespace-only ``repo`` triggers fallback to split keys."""
        config = {
            "github": {
                "repo": "   ",
                "repo_owner": "fb-owner",
                "repo_name": "fb-repo",
            },
        }
        adapter = _build_github_adapter(config)
        assert adapter._repo == "fb-owner/fb-repo"

    def test_none_repo_falls_back(self) -> None:
        """``None`` value for repo triggers fallback."""
        config = {
            "github": {
                "repo": None,
                "repo_owner": "owner",
                "repo_name": "name",
            },
        }
        adapter = _build_github_adapter(config)
        assert adapter._repo == "owner/name"

    def test_non_string_repo_falls_back(self) -> None:
        """Non-string ``repo`` values are ignored and fallback is used."""
        config = {
            "github": {
                "repo": 123,
                "repo_owner": "owner",
                "repo_name": "name",
            },
        }
        adapter = _build_github_adapter(config)
        assert adapter._repo == "owner/name"


# ---------------------------------------------------------------------------
# US2 — Adapter works with legacy split keys
# ---------------------------------------------------------------------------


class TestLegacySplitKeys:
    """FR-002: legacy ``repo_owner`` / ``repo_name`` concatenation."""

    def test_split_keys_produce_slug(self) -> None:
        config = {"github": {"repo_owner": "myorg", "repo_name": "myrepo"}}
        adapter = _build_github_adapter(config)
        assert adapter._repo == "myorg/myrepo"

    def test_split_keys_stripped(self) -> None:
        """FR-004: whitespace in split keys is stripped."""
        config = {"github": {"repo_owner": " org ", "repo_name": " repo "}}
        adapter = _build_github_adapter(config)
        assert adapter._repo == "org/repo"

    def test_only_repo_owner_produces_empty(self) -> None:
        """FR-005: missing ``repo_name`` → empty slug, no exception."""
        config = {"github": {"repo_owner": "org"}}
        adapter = _build_github_adapter(config)
        assert adapter._repo == ""

    def test_only_repo_name_produces_empty(self) -> None:
        """FR-005: missing ``repo_owner`` → empty slug, no exception."""
        config = {"github": {"repo_name": "repo"}}
        adapter = _build_github_adapter(config)
        assert adapter._repo == ""

    def test_none_split_values_produce_empty(self) -> None:
        """``None`` values in split keys don't raise."""
        config = {"github": {"repo_owner": None, "repo_name": None}}
        adapter = _build_github_adapter(config)
        assert adapter._repo == ""


# ---------------------------------------------------------------------------
# US3 — Graceful handling of empty / missing config
# ---------------------------------------------------------------------------


class TestEmptyAndMissingConfig:
    """FR-005: no exception for any combination of absent keys."""

    def test_empty_github_dict(self) -> None:
        adapter = _build_github_adapter({"github": {}})
        assert adapter._repo == ""

    def test_missing_github_key(self) -> None:
        adapter = _build_github_adapter({})
        assert adapter._repo == ""

    def test_malformed_slug_passed_through(self) -> None:
        """A slug without ``/`` is passed through as-is."""
        config = {"github": {"repo": "justreponame"}}
        adapter = _build_github_adapter(config)
        assert adapter._repo == "justreponame"

    def test_empty_string_repo(self) -> None:
        config = {"github": {"repo": ""}}
        adapter = _build_github_adapter(config)
        assert adapter._repo == ""

    def test_github_none_produces_empty(self) -> None:
        """FR-005: ``github`` key present but ``None`` must not raise."""
        adapter = _build_github_adapter({"github": None})
        assert adapter._repo == ""

    def test_github_non_dict_produces_empty(self) -> None:
        """FR-005: ``github`` key present but not a dict must not raise."""
        adapter = _build_github_adapter({"github": "not-a-dict"})
        assert adapter._repo == ""

    def test_github_integer_produces_empty(self) -> None:
        """FR-005: integer ``github`` value must not raise."""
        adapter = _build_github_adapter({"github": 42})
        assert adapter._repo == ""
