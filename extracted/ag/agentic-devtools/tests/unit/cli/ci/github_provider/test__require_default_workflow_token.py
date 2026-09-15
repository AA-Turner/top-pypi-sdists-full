"""Tests for _require_default_workflow_token()."""

from unittest.mock import patch

from agentic_devtools.cli.ci.github_provider import _require_default_workflow_token


def test_require_default_workflow_token_delegates_to_centralized_helper() -> None:
    with patch(
        "agentic_devtools.cli.ci.github_provider.require_default_repo_workflow_token",
        return_value="token-value",
    ) as require_token:
        assert _require_default_workflow_token("dispatch workflows") == "token-value"

    require_token.assert_called_once_with("dispatch workflows")
