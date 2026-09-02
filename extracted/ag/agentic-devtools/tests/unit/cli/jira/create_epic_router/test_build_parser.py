"""Tests for build_parser (issue #2117)."""

import pytest

from agentic_devtools.cli.jira.create_epic_router import build_parser


def test_defaults_are_none_and_false():
    args = build_parser().parse_args([])
    assert args.file is None
    assert args.start_from is None
    assert args.provider is None
    assert args.dry_run is False


def test_parses_positional_and_flags():
    args = build_parser().parse_args(["plan.json", "--dry-run", "--start-from", "n1", "--provider", "github"])
    assert args.file == "plan.json"
    assert args.dry_run is True
    assert args.start_from == "n1"
    assert args.provider == "github"


def test_help_exits_zero(capsys):
    with pytest.raises(SystemExit) as exc:
        build_parser().parse_args(["--help"])
    assert exc.value.code == 0
    assert "usage" in capsys.readouterr().out.lower()
