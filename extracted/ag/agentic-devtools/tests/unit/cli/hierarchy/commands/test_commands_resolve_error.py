"""Tests for ValueError handling in resolve_owner_repo within CLI commands."""

from __future__ import annotations

from unittest.mock import patch

import pytest


class TestCommandsResolveError:
    """Cover ValueError exit paths in enforce_parent_command and cascade_trigger_command."""

    def test_enforce_parent_resolve_error(self):
        from agentic_devtools.cli.hierarchy.commands import enforce_parent_command

        with (
            patch("sys.argv", ["cmd", "--issue", "42"]),
            patch(
                "agentic_devtools.cli.hierarchy.commands.resolve_owner_repo",
                side_effect=ValueError("Cannot resolve"),
            ),
            pytest.raises(SystemExit) as exc_info,
        ):
            enforce_parent_command()
        assert exc_info.value.code == 1

    def test_cascade_trigger_resolve_error(self):
        from agentic_devtools.cli.hierarchy.commands import cascade_trigger_command

        with (
            patch(
                "sys.argv",
                ["cmd", "--issue", "42", "--hierarchy-yml", "/tmp/h.yml", "--mode", "first-child"],
            ),
            patch(
                "agentic_devtools.cli.hierarchy.commands.resolve_owner_repo",
                side_effect=ValueError("Cannot resolve"),
            ),
            pytest.raises(SystemExit) as exc_info,
        ):
            cascade_trigger_command()
        assert exc_info.value.code == 1
