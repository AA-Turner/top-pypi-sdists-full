from __future__ import annotations

from unittest.mock import patch

import pytest

from agentic_devtools.cli import pull_request_approval as commands


def test_forwards_parsed_arguments() -> None:
    with (
        patch(
            "sys.argv",
            [
                "agdt-approve-pull-request",
                "--pull-request-id",
                "23046",
                "--content",
                "LGTM",
                "--provider",
                "github",
                "--repo",
                "owner/repo",
                "--expected-head",
                "a" * 40,
            ],
        ),
        patch.object(commands, "approve_pull_request_async") as mock_approve,
    ):
        commands.approve_pull_request_async_cli()

    mock_approve.assert_called_once_with(
        provider="github",
        repository="owner/repo",
        pull_request_id="23046",
        content="LGTM",
        expected_head="a" * 40,
    )


def test_head_sha_alias_forwarded_as_expected_head() -> None:
    with (
        patch(
            "sys.argv",
            ["agdt-approve-pull-request", "-p", "23046", "-c", "LGTM", "--head-sha", "b" * 40],
        ),
        patch.object(commands, "approve_pull_request_async") as mock_approve,
    ):
        commands.approve_pull_request_async_cli()

    mock_approve.assert_called_once_with(
        provider=None,
        repository=None,
        pull_request_id="23046",
        content="LGTM",
        expected_head="b" * 40,
    )


def test_validation_error_exits_with_parser_error() -> None:
    with (
        patch("sys.argv", ["agdt-approve-pull-request", "-p", "23046", "-c", "LGTM"]),
        patch.object(commands, "approve_pull_request_async", side_effect=ValueError("boom")),
        pytest.raises(SystemExit) as exc_info,
    ):
        commands.approve_pull_request_async_cli()

    assert exc_info.value.code == 2


def test_type_error_exits_with_parser_error() -> None:
    with (
        patch("sys.argv", ["agdt-approve-pull-request", "-p", "23046", "-c", "LGTM"]),
        patch.object(commands, "approve_pull_request_async", side_effect=TypeError("bad type")),
        pytest.raises(SystemExit) as exc_info,
    ):
        commands.approve_pull_request_async_cli()

    assert exc_info.value.code == 2
