import argparse
from unittest.mock import Mock
from uuid import uuid4

import pytest
from polars_cloud.cli import main as cli
from polars_cloud.cli.parsers import create_parser


def test_execute_command_workspace_setup(monkeypatch: pytest.MonkeyPatch) -> None:
    mock_parser = Mock(argparse.ArgumentParser)

    mock_args = Mock(argparse.Namespace)
    mock_args.version = False
    mock_args.command = "workspace"
    mock_args.workspace_command = "setup"
    mock_args.name = "my_workspace"
    mock_args.organization_name = "my_organization"
    mock_args.verify = True
    mock_args.token = None
    mock_args.token_path = None

    mock_setup = Mock()
    monkeypatch.setattr(cli, "set_up_workspace", mock_setup)

    cli._execute_command(mock_parser, mock_args)
    mock_setup.assert_called_with("my_workspace", "my_organization", verify=True)


def test_execute_command_compute_stop(monkeypatch: pytest.MonkeyPatch) -> None:
    id = uuid4()

    mock_parser = Mock(argparse.ArgumentParser)

    mock_args = Mock(argparse.Namespace)
    mock_args.version = False
    mock_args.command = "compute"
    mock_args.compute_command = "stop"
    mock_args.workspace = id
    mock_args.id = id
    mock_args.wait = False
    mock_args.token = None
    mock_args.token_path = None

    mock_stop = Mock()
    monkeypatch.setattr(cli, "stop_compute", mock_stop)

    cli._execute_command(mock_parser, mock_args)
    mock_stop.assert_called_with(id, id, wait=False)


def test_execute_command_invalid() -> None:
    mock_parser = Mock(argparse.ArgumentParser)

    mock_args = Mock(argparse.Namespace)
    mock_args.version = False

    mock_args.command = "nonexistent"
    with pytest.raises(RuntimeError):
        cli._execute_command(mock_parser, mock_args)

    mock_args.command = "workspace"
    mock_args.workspace_command = "nonexistent"
    with pytest.raises(RuntimeError):
        cli._execute_command(mock_parser, mock_args)


def test_execute_command_version(capsys: pytest.CaptureFixture[str]) -> None:
    parser = create_parser()

    with pytest.raises(SystemExit):
        parser.parse_args(["--version"])

    out = capsys.readouterr().out
    # Check that output is a valid version specifier
    assert len(out.split(".")) == 3
    assert out.endswith("\n")
