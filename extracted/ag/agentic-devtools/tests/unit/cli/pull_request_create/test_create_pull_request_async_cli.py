from unittest.mock import patch

import pytest

from agentic_devtools.cli import pull_request_create


def test_cli_parses_arguments_and_starts_async(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.setattr(
        "sys.argv",
        [
            "agdt-create-pull-request",
            "--provider",
            "github",
            "--source-branch",
            "feature",
            "--title",
            "Title",
            "--description",
            "Body",
            "--target-branch",
            "develop",
            "--reviewers",
            "alice",
            "--no-draft",
        ],
    )
    with patch.object(pull_request_create, "create_pull_request_async") as create:
        pull_request_create.create_pull_request_async_cli()
    assert create.call_args.kwargs["draft"] is False


def test_cli_accepts_repeated_and_comma_separated_reviewers(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.setattr(
        "sys.argv",
        [
            "agdt-create-pull-request",
            "--source-branch",
            "feature",
            "--title",
            "Title",
            "--reviewer",
            "alice,bob",
            "--reviewers",
            "carol",
        ],
    )
    with patch.object(pull_request_create, "create_pull_request_async") as create:
        pull_request_create.create_pull_request_async_cli()

    assert create.call_args.kwargs["reviewers"] == ["alice,bob", "carol"]


def test_cli_reports_invalid_arguments(monkeypatch: pytest.MonkeyPatch, capsys: pytest.CaptureFixture[str]) -> None:
    monkeypatch.setattr("sys.argv", ["agdt-create-pull-request"])
    with patch.object(pull_request_create, "create_pull_request_async", side_effect=ValueError("bad")):
        with pytest.raises(SystemExit):
            pull_request_create.create_pull_request_async_cli()
    assert "Error: bad" in capsys.readouterr().err
