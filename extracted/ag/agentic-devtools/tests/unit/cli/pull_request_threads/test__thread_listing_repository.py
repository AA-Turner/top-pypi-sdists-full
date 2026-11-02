from unittest.mock import patch

import pytest

from agentic_devtools.cli.pull_request_threads import _thread_listing_repository


def test_reads_github_repository_from_github_state_key() -> None:
    with patch("agentic_devtools.cli.pull_request_threads.get_value", return_value=" owner/repo "):
        assert _thread_listing_repository("github") == "owner/repo"


def test_reads_github_repository_from_environment_when_state_missing(monkeypatch) -> None:
    monkeypatch.setenv("GITHUB_REPOSITORY", "owner/repo")
    with patch("agentic_devtools.cli.pull_request_threads.get_value", return_value=None):
        assert _thread_listing_repository("github") == "owner/repo"


def test_reads_github_repository_from_git_remote_when_state_missing(monkeypatch) -> None:
    monkeypatch.delenv("GITHUB_REPOSITORY", raising=False)
    with (
        patch("agentic_devtools.cli.pull_request_threads.get_value", return_value=None),
        patch("agentic_devtools.cli.pull_request_threads.get_repo_root", return_value=None),
        patch("agentic_devtools.cli.pull_request_threads.resolve_github_repo_safe", return_value="owner/repo"),
    ):
        assert _thread_listing_repository("github") == "owner/repo"


def test_reads_github_repository_from_root_config_when_other_sources_missing(monkeypatch) -> None:
    monkeypatch.delenv("GITHUB_REPOSITORY", raising=False)
    with (
        patch("agentic_devtools.cli.pull_request_threads.get_value", return_value=None),
        patch("agentic_devtools.cli.pull_request_threads.get_repo_root", return_value="/repo"),
        patch(
            "agentic_devtools.cli.pull_request_threads.load_platform_config",
            return_value={"github": {"repo": "owner/repo"}},
        ),
        patch("agentic_devtools.cli.pull_request_threads.resolve_github_repo_safe", return_value=None),
    ):
        assert _thread_listing_repository("github") == "owner/repo"


def test_rejects_non_string_github_repository_from_root_config(monkeypatch) -> None:
    monkeypatch.delenv("GITHUB_REPOSITORY", raising=False)
    with (
        patch("agentic_devtools.cli.pull_request_threads.get_value", return_value=None),
        patch("agentic_devtools.cli.pull_request_threads.get_repo_root", return_value="/repo"),
        patch(
            "agentic_devtools.cli.pull_request_threads.load_platform_config",
            return_value={"github": {"repo": 123}},
        ),
    ):
        with pytest.raises(ValueError, match="platform.github.repo"):
            _thread_listing_repository("github")


def test_ignores_missing_github_section_in_root_config(monkeypatch) -> None:
    monkeypatch.delenv("GITHUB_REPOSITORY", raising=False)
    with (
        patch("agentic_devtools.cli.pull_request_threads.get_value", return_value=None),
        patch("agentic_devtools.cli.pull_request_threads.get_repo_root", return_value="/repo"),
        patch("agentic_devtools.cli.pull_request_threads.load_platform_config", return_value={"github": None}),
        patch("agentic_devtools.cli.pull_request_threads.resolve_github_repo_safe", return_value=None),
    ):
        with pytest.raises(ValueError, match="repository is required"):
            _thread_listing_repository("github")


def test_reads_azure_repository_from_repository_state_key() -> None:
    with patch("agentic_devtools.cli.pull_request_threads.get_value", return_value=" repo "):
        assert _thread_listing_repository("azure_devops") == "repo"


@pytest.mark.parametrize("provider", ["azure_devops", "github"])
@pytest.mark.parametrize("value", [None, "", "   "])
def test_rejects_missing_repository(monkeypatch, provider: str, value: object) -> None:
    monkeypatch.delenv("GITHUB_REPOSITORY", raising=False)
    with (
        patch("agentic_devtools.cli.pull_request_threads.get_value", return_value=value),
        patch("agentic_devtools.cli.pull_request_threads.get_repo_root", return_value=None),
        patch("agentic_devtools.cli.pull_request_threads.resolve_github_repo_safe", return_value=None),
    ):
        with pytest.raises(ValueError, match="repository is required"):
            _thread_listing_repository(provider)
