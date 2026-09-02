"""Tests for provider-neutral pull-request comments."""

from __future__ import annotations

from agentic_devtools.adapters.pull_request_comments import discover_github_token


def test_token_precedence_and_fallbacks() -> None:
    assert discover_github_token({"SPECKIT_PR_TOKEN": " primary ", "GH_TOKEN": "fallback"}) == "primary"
    assert discover_github_token({"GITHUB_TOKEN": "github"}) == "github"
    assert discover_github_token({"GH_TOKEN": "gh"}) == "gh"
    assert discover_github_token({}) == ""
