from typing import Any
from unittest.mock import patch

import pytest

from agentic_devtools.cli.pull_request_publish import _github_request


@patch("agentic_devtools.cli.pull_request_publish.get_value", side_effect=[12, None])
@patch.dict("os.environ", {"GITHUB_REPOSITORY": "owner/repo"})
def test_builds_from_state_and_environment(mock_get) -> None:
    request = _github_request("github", None, None, False)
    assert request.pull_request_id == 12


def test_requires_pull_request_id() -> None:
    with patch("agentic_devtools.cli.pull_request_publish.get_value", return_value=None):
        with pytest.raises(ValueError, match="pull_request_id"):
            _github_request("github", None, "owner/repo", False)


def test_requires_repository() -> None:
    with patch("agentic_devtools.cli.pull_request_publish.get_value", side_effect=[1, None]):
        with patch(
            "agentic_devtools.cli.pull_request_publish.resolve_github_repo_safe",
            return_value=None,
        ):
            with patch("agentic_devtools.cli.pull_request_publish.get_repo_root", return_value=None):
                with patch.dict("os.environ", {}, clear=True):
                    with pytest.raises(ValueError, match="repository"):
                        _github_request("github", None, None, False)


def test_builds_from_platform_github_config() -> None:
    with patch("agentic_devtools.cli.pull_request_publish.get_value", side_effect=[1, None, None]):
        with patch("agentic_devtools.cli.pull_request_publish.get_repo_root", return_value="/repo"):
            with patch(
                "agentic_devtools.cli.pull_request_publish.load_platform_config",
                return_value={"github": {"repo": "owner/repo"}},
            ):
                with patch.dict("os.environ", {}, clear=True):
                    request = _github_request("github", None, None, False)
    assert request.repository == "owner/repo"


def test_blank_environment_and_config_fall_back_to_git_origin() -> None:
    with patch("agentic_devtools.cli.pull_request_publish.get_value", side_effect=[1, None]):
        with patch("agentic_devtools.cli.pull_request_publish.get_repo_root", return_value="/repo"):
            with patch(
                "agentic_devtools.cli.pull_request_publish.load_platform_config",
                return_value={"github": {"repo": "   "}},
            ):
                with patch(
                    "agentic_devtools.cli.pull_request_publish.resolve_github_repo_safe",
                    return_value="owner/repo",
                ):
                    with patch.dict("os.environ", {"GITHUB_REPOSITORY": "   "}):
                        request = _github_request("github", None, None, False)
    assert request.repository == "owner/repo"


def test_builds_from_git_origin_when_other_sources_are_missing() -> None:
    with patch("agentic_devtools.cli.pull_request_publish.get_value", side_effect=[1, None, None]):
        with patch("agentic_devtools.cli.pull_request_publish.get_repo_root", return_value=None):
            with patch(
                "agentic_devtools.cli.pull_request_publish.resolve_github_repo_safe",
                return_value="owner/repo",
            ):
                with patch.dict("os.environ", {}, clear=True):
                    request = _github_request("github", None, None, False)
    assert request.repository == "owner/repo"


def test_falls_back_when_platform_config_has_no_github_section() -> None:
    with patch("agentic_devtools.cli.pull_request_publish.get_value", side_effect=[1, None, None]):
        with patch("agentic_devtools.cli.pull_request_publish.get_repo_root", return_value="/repo"):
            with patch("agentic_devtools.cli.pull_request_publish.load_platform_config", return_value={"github": None}):
                with patch(
                    "agentic_devtools.cli.pull_request_publish.resolve_github_repo_safe",
                    return_value="owner/repo",
                ):
                    with patch.dict("os.environ", {}, clear=True):
                        request = _github_request("github", None, None, False)
    assert request.repository == "owner/repo"


def test_rejects_non_string_platform_github_repo() -> None:
    with patch("agentic_devtools.cli.pull_request_publish.get_value", side_effect=[1, None, None]):
        with patch("agentic_devtools.cli.pull_request_publish.get_repo_root", return_value="/repo"):
            with patch(
                "agentic_devtools.cli.pull_request_publish.load_platform_config",
                return_value={"github": {"repo": ["owner/repo"]}},
            ):
                with patch.dict("os.environ", {}, clear=True):
                    with pytest.raises(ValueError, match="platform.github.repo must be a string"):
                        _github_request("github", None, None, False)


def test_rejects_non_string_explicit_repository() -> None:
    with patch("agentic_devtools.cli.pull_request_publish.get_value", return_value=1):
        invalid_repository: Any = 123
        with pytest.raises(ValueError, match="repository must be a string"):
            _github_request("github", None, invalid_repository, False)


def test_rejects_non_string_state_repository() -> None:
    with patch("agentic_devtools.cli.pull_request_publish.get_value", side_effect=[1, ["owner/repo"]]):
        with pytest.raises(ValueError, match="github.repo must be a string"):
            _github_request("github", None, None, False)


def test_skips_blank_candidates_in_fallback_order() -> None:
    with patch("agentic_devtools.cli.pull_request_publish.get_value", side_effect=[1, "  "]):
        with patch.dict("os.environ", {"GITHUB_REPOSITORY": "env/repo"}):
            request = _github_request("github", None, "  ", False)
    assert request.repository == "env/repo"
