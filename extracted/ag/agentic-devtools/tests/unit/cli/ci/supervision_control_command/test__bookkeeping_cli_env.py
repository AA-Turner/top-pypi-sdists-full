"""Tests for _bookkeeping_cli_env."""

import os
from unittest.mock import patch

import pytest

from agentic_devtools.cli.ci.supervision_control_command import _bookkeeping_cli_env


def test_rejects_unverified_bookkeeping_identity() -> None:
    with (
        patch(
            "agentic_devtools.cli.ci.supervision_control_command.require_ai_pr_loop_bookkeeping_token",
            return_value="token",
        ),
        patch(
            "agentic_devtools.cli.ci.supervision_control_command._run_gh",
            return_value={"data": {"viewer": {"login": " "}}},
        ),
        pytest.raises(RuntimeError, match="identity could not be verified"),
    ):
        _bookkeeping_cli_env()


def test_resolves_bookkeeping_identity_with_graphql_viewer_login() -> None:
    with (
        patch(
            "agentic_devtools.cli.ci.supervision_control_command.require_ai_pr_loop_bookkeeping_token",
            return_value="token",
        ),
        patch(
            "agentic_devtools.cli.ci.supervision_control_command._run_gh",
            return_value={"data": {"viewer": {"login": "github-actions[bot]"}}},
        ) as run_gh,
    ):
        env, login = _bookkeeping_cli_env()

    assert login == "github-actions[bot]"
    assert env["GH_TOKEN"] == "token"
    assert run_gh.call_args.args[0] == [
        "api",
        "graphql",
        "-f",
        "query=query { viewer { login } }",
    ]
    assert run_gh.call_args.kwargs["env"] == {**os.environ, "GH_TOKEN": "token"}


@pytest.mark.parametrize(
    "response",
    [
        None,
        [],
        {"data": None},
        {"data": {"viewer": None}},
        {"data": {"viewer": {"login": 42}}},
        {"data": {"viewer": {"login": " "}}},
        {"errors": [{"message": "viewer unavailable"}], "data": {"viewer": {"login": "bot"}}},
    ],
)
def test_rejects_malformed_or_failed_graphql_identity(response: object) -> None:
    with (
        patch(
            "agentic_devtools.cli.ci.supervision_control_command.require_ai_pr_loop_bookkeeping_token",
            return_value="token",
        ),
        patch(
            "agentic_devtools.cli.ci.supervision_control_command._run_gh",
            return_value=response,
        ),
        pytest.raises(RuntimeError, match="identity could not be verified"),
    ):
        _bookkeeping_cli_env()
