"""Tests for _add_headless_options."""

import argparse

from agentic_devtools.cli.workflows.commands import _add_headless_options


def test_defaults_headless_to_false() -> None:
    """Keep headless disabled when no flag is provided."""
    parser = argparse.ArgumentParser()
    _add_headless_options(parser)

    args = parser.parse_args([])

    assert args.headless is False


def test_sets_headless_true_for_headless_alias() -> None:
    """Enable headless mode via the --headless flag."""
    parser = argparse.ArgumentParser()
    _add_headless_options(parser)

    args = parser.parse_args(["--headless"])

    assert args.headless is True


def test_sets_headless_true_for_no_vscode_alias() -> None:
    """Enable headless mode via the --no-vscode alias."""
    parser = argparse.ArgumentParser()
    _add_headless_options(parser)

    args = parser.parse_args(["--no-vscode"])

    assert args.headless is True
