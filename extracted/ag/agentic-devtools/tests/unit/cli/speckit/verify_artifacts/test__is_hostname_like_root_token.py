"""Tests for ``_is_hostname_like_root_token()``."""

import pytest

from agentic_devtools.cli.speckit.verify_artifacts import _is_hostname_like_root_token


class TestIsHostnameLikeRootToken:
    """Hostname-like root token detection for bare prose references."""

    @pytest.mark.parametrize("text", ["example.com", "service.internal", "docs.local"])
    def test_returns_true_for_hostname_like_tokens(self, text: str) -> None:
        assert _is_hostname_like_root_token(text) is True

    @pytest.mark.parametrize("text", ["runner.py", "uv.lock", ".gitignore", "pkg/module.py"])
    def test_returns_false_for_repository_style_paths(self, text: str) -> None:
        assert _is_hostname_like_root_token(text) is False

    def test_returns_false_for_requirements_in_filename(self) -> None:
        assert _is_hostname_like_root_token("requirements.in") is False

    @pytest.mark.parametrize("text", ["", "foo..com", "-foo.com", "foo-.com", "foo_.com"])
    def test_returns_false_for_malformed_tokens(self, text: str) -> None:
        assert _is_hostname_like_root_token(text) is False
