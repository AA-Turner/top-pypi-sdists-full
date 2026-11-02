"""Tests for the shared ``--issue-number``/``--repo``/``--ref`` argument parsing helper."""

import argparse
import sys

import pytest

from agentic_devtools.cli.speckit.resolve_hierarchy import _add_common_resolver_args


def test_parses_required_and_default_arguments(monkeypatch) -> None:
    parser = argparse.ArgumentParser(prog="test")
    monkeypatch.setattr(sys, "argv", ["test", "--issue-number", "7", "--repo", "owner/repo"])
    args = _add_common_resolver_args(parser)
    assert args.issue_number == 7
    assert args.repo == "owner/repo"
    assert args.ref == "main"


def test_rejects_nonpositive_issue_number(monkeypatch, capsys) -> None:
    parser = argparse.ArgumentParser(prog="test")
    monkeypatch.setattr(sys, "argv", ["test", "--issue-number", "0", "--repo", "owner/repo"])
    with pytest.raises(SystemExit) as exc_info:
        _add_common_resolver_args(parser)
    assert exc_info.value.code == 2
    assert "positive" in capsys.readouterr().err
