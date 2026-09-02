"""Tests for _validate_repo_slug."""

from __future__ import annotations

import pytest

from agentic_devtools.adapters.factory import _validate_repo_slug
from agentic_devtools.epic_tree.errors import ConfigError


class TestValidateRepoSlug:
    """Verify repo slug format validation."""

    def test_malformed_slug_no_slash(self):
        """Slug without slash raises ConfigError."""
        with pytest.raises(ConfigError) as exc_info:
            _validate_repo_slug("ownerrepo")
        assert "platform.github.repo" in str(exc_info.value)
        assert "owner/repo" in str(exc_info.value)

    def test_malformed_slug_empty_owner(self):
        """Slug with empty owner raises ConfigError."""
        with pytest.raises(ConfigError) as exc_info:
            _validate_repo_slug("/repo")
        assert "platform.github.repo" in str(exc_info.value)

    def test_malformed_slug_empty_repo(self):
        """Slug with empty repo raises ConfigError."""
        with pytest.raises(ConfigError) as exc_info:
            _validate_repo_slug("owner/")
        assert "platform.github.repo" in str(exc_info.value)

    def test_malformed_slug_extra_slash(self):
        """Slug with extra slash raises ConfigError."""
        with pytest.raises(ConfigError) as exc_info:
            _validate_repo_slug("owner/sub/repo")
        assert "platform.github.repo" in str(exc_info.value)

    def test_valid_slug_passes(self):
        """Valid owner/repo slug does not raise."""
        _validate_repo_slug("owner/repo")

    def test_valid_slug_with_hyphens(self):
        """Valid slug with hyphens passes."""
        _validate_repo_slug("my-org/my-repo")

    def test_slug_with_space_in_owner_raises(self):
        """Slug with whitespace in owner segment raises ConfigError."""
        with pytest.raises(ConfigError) as exc_info:
            _validate_repo_slug("owner /repo")
        assert "platform.github.repo" in str(exc_info.value)
        assert "owner /repo" in str(exc_info.value)

    def test_slug_with_space_in_repo_raises(self):
        """Slug with whitespace in repo segment raises ConfigError."""
        with pytest.raises(ConfigError) as exc_info:
            _validate_repo_slug("owner/my repo")
        assert "platform.github.repo" in str(exc_info.value)

    def test_slug_with_leading_space_in_owner_raises(self):
        """Slug with leading whitespace in owner segment raises ConfigError."""
        with pytest.raises(ConfigError) as exc_info:
            _validate_repo_slug(" owner/repo")
        assert "platform.github.repo" in str(exc_info.value)
