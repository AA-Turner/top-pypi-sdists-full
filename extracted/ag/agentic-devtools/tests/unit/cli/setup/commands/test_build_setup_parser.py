"""Tests for agentic_devtools.cli.setup.commands.build_setup_parser."""

from __future__ import annotations

import argparse

from agentic_devtools.cli.setup.commands import build_setup_parser


def _flags(parser: argparse.ArgumentParser) -> set[str]:
    return {option for action in parser._actions for option in action.option_strings}


def _help_for(parser: argparse.ArgumentParser, flag: str) -> str:
    return next(action.help or "" for action in parser._actions if flag in action.option_strings)


class TestBuildSetupParser:
    """Tests for the module-level agdt-setup parser factory."""

    def test_returns_argument_parser_for_agdt_setup(self) -> None:
        """The factory builds the agdt-setup parser without executing anything."""
        parser = build_setup_parser()
        assert isinstance(parser, argparse.ArgumentParser)
        assert parser.prog == "agdt-setup"

    def test_offers_dry_run_and_yes_flags(self) -> None:
        """Both safety flags are present and can be asserted without running the command."""
        assert {"--dry-run", "--yes"} <= _flags(build_setup_parser())

    def test_new_flags_have_help_text_naming_them(self) -> None:
        """Help text explains the manifest diff and the deletion opt-in."""
        parser = build_setup_parser()
        assert "manifest diff" in _help_for(parser, "--dry-run")
        yes_help = _help_for(parser, "--yes")
        assert "delet" in yes_help.lower()

    def test_defaults_are_false(self) -> None:
        """Neither safety flag is on by default."""
        args = build_setup_parser().parse_args([])
        assert args.dry_run is False
        assert args.yes is False

    def test_flags_parse_to_true(self) -> None:
        """Passing the flags sets the corresponding attributes."""
        args = build_setup_parser().parse_args(["--dry-run", "--yes"])
        assert args.dry_run is True
        assert args.yes is True

    def test_preexisting_flags_are_preserved(self) -> None:
        """Extraction changed no existing flag's behaviour."""
        flags = _flags(build_setup_parser())
        assert {
            "--system-only",
            "--no-verify-ssl",
            "--no-persist-env",
            "--overwrite-env",
            "--skip-platform-detection",
            "--issue-adapter",
            "--skip-templates",
            "--reconfigure",
            "--defaults",
            "--skip-pr-workflow",
            "--force-old-version",
            "--npm",
            "--no-npm",
            "--run",
            "--no-run",
            "--refresh-issue-types",
        } <= flags

    def test_no_refresh_models_flag_defaults_to_false(self) -> None:
        """Model discovery refreshes by default; the opt-out flag exists."""
        parser = build_setup_parser()
        assert "--no-refresh-models" in _flags(parser)
        assert parser.parse_args([]).no_refresh_models is False
        assert parser.parse_args(["--no-refresh-models"]).no_refresh_models is True
        assert "cached model inventory" in _help_for(parser, "--no-refresh-models")
